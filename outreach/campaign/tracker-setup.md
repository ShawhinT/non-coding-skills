# Tracker Setup (Notion)

Use this when the flow calls for creating a tracker. Shaw's campaigns live on Notion pages with an **inline** database for the tracker, a segment legend, templates, and context — all on one page.

## Before creating anything: confirm the plan

Use AskUserQuestion to present the proposed schema before building it. Rework on structural things (column names, status options, placement) is tedious. Present something like:

- **Columns:** Name, Segment, Contact, Status, Last Contact, Notes
- **Segment options:** 1 = [description], 2 = [description], ...
- **Status options:** [only the milestones that matter]
- **Placement:** inline table under [section name]

If Shaw has already been very explicit about exactly what he wants, it's fine to just build it — use judgment.

## Create the inline database

Use `notion-create-database` with `parent` set to the page ID. If the table doesn't render inline, follow with `notion-update-data-source` setting `is_inline: true`. Shaw prefers inline databases over full-page databases — they live in the flow of the page alongside context, legends, and templates.

### Standard columns

Adapt names and options per campaign:

| Column | Type | Purpose |
|---|---|---|
| Name | Title | Contact's full name |
| Segment | Select | Numbered options — just the number, keep it clean |
| Contact | Rich text | How Shaw reached them: email, phone, "iMessage", "WhatsApp", "LinkedIn DM" |
| Status | Multi-select | Campaign-specific milestones only |
| Last Contact | Date | Date of most recent touchpoint |
| Next Contact | Date | Date of next planned touchpoint. **Standard column — always include.** Mirrors the CRM field; CRM Workflow 1's active-campaign sweep sorts on it (`Next Contact <= today`) to surface due follow-ups. Blank = no FU planned (intentional, never backfilled). On a **batch send**, set it uniformly across everyone who got the same ask so the whole batch surfaces together. The date comes from the campaign's Promo Calendar, or from `crm/references/follow-up-guidance.md` when there isn't one. Those are the only two sources; per-person timing comes from evidence on the record, never from norms about when people read mail. |
| Medium | Select | Channel the outreach goes out on: `Email` / `LinkedIn` / `Text`. Add for multi-channel campaigns — it **drives the per-prospect script format** (email rows need a subject line + hyperlinked CTA; DM/text rows keep the raw link — see `per-prospect-scripting.md`). |
| Notes | Rich text | **FU log ONLY** — short dated pipeline actions (see Notes format in CRM skill). Not for background/context. |

Additional columns when the campaign calls for them: Company, Company Size, LinkedIn URL, Location, topic-specific checkboxes.

**Post-event attendee trackers** add behavioural columns, since engagement during the session is the only intent signal available: `Minutes` (number — time in the session), `Chat` (number — messages posted), `Source` (select — acquisition channel, including a `Forwarded` option for links that were passed along), and `Email Type` (select — `Work` / `Personal`). Sort on Minutes + Chat to prioritise. Company belongs in the row's Context body, not a column — attendee lists run 90+ rows and a mostly-empty Company column earns less than it costs. Building the list is `../events/event-attendance-reconciliation.md`.

**`Next Contact` is not optional** — every outreach DB gets it. It's the structured home for "FU on 7/14"-type markers (which must never live in Notes), and the CRM skill's campaign sweep depends on it.

### Seeding from a lead list

The common case: an extracted list (Sales Nav → `../sales-navigator/lead-lists.md`, which owns the row parsing) becomes rows. What the Notion side needs:

- **The LinkedIn column links to wherever Shaw will message the person — decided by the send channel, not the sourcing tool.** Neither inbox can see the other's threads, so the link should open the one that holds the conversation. Default to the public vanity `/in/<slug>` URL (resolved per `../sales-navigator/lead-lists.md` → "Public profile URLs"; an `/in/ACoAA…` member-id URL works but isn't readable, so resolve it too): Shaw works from regular LinkedIn, and a list merely *searched* in Sales Navigator — e.g. 1st-degree connections he'll DM casually — is still a LinkedIn-messaging campaign. Use the `/sales/lead/` URL only when the campaign actually sends from Sales Nav (connection requests or InMail worked through the Sales Nav inbox). Keep the lead ID in the campaign CSV either way, since the accept sweep joins on it (`../sales-navigator/accepts.md`).
- **Blank means unresolved, never small.** A lead with no company record gets an empty Company Size, and the Context body says so. Don't infer a number from the title.
- **Batch about 17 rows per `notion-create-pages` call with `allow_async: false`**, so the created pages come back in the response and can be checked — the async path returns a task id and nothing to verify against.
- **Verify with one SQL aggregate**, not by eyeballing rows: `COUNT(*)`, `COUNT(DISTINCT Name)`, `COUNT(DISTINCT LinkedIn)`, the null count on any column that should be full, and the count of rows carrying a Status (should be zero on a fresh seed). One query catches duplicates, a dropped batch, and a mis-set property together.
- **Segment comes from the list, not the row.** A Sales Nav list is built per segment (the geography filter is the only thing that changes between them), so every row from one list gets the same Segment value — read it off the list name.

Nothing about the send goes on the row at seed time: Status, Last Contact, Next Contact and Notes stay empty until the ask actually goes out (SKILL.md, "Logging a batch send").

### Seeding from sends that already happened

A tracker is sometimes built to catch up with a campaign run by hand — that's step 7, not step 5, so seed rows are logs: real send date, cadence-derived `Next Contact`, dated Notes line. Reconstruct from sent mail, not the campaign page; a hand-run batch usually drifted.

### Context goes in the row's page body, not the Notes column

Background on a contact — role, company, size, location, DM/relationship history, personalization hooks — lives in a `## Context` section **inside the contact's row page**, mirroring the CRM page-body convention. How to write the bullets is `notion-helper` → "Writing page bodies"; what survives the keep-filter is `crm/references/context-sections.md`.

**A row that reaches drafting with no Context gets enriched or left blank — never inferred.** The draft notes are not a source: reading a company name back out of copy that was written *from* the row is circular, and it lands an unverifiable identity in a record Shaw may act on. Blank means unresolved, the same as an empty Company Size. The Notes *column* is reserved for the dated conversation log, in the CRM's Notes Format (`Ask sent (7/10). Replied, booked (7/15).`) — moves only, never nudges and never what a reply said. When seeding a tracker from an enriched list, write the enrichment into each row page's Context section via `notion-update-page` `insert_content`, and leave the Notes column empty.

### Status options

**Only meaningful forward progress.** If blank already communicates the default ("message sent, no reply yet"), there's no status for it. No `Sent`, no `No response`.

Campaign-specific examples:
- **Workshop outreach:** Replied, Applied, Selected
- **Event outreach:** Booked Call, Pending Call
- **Research calls:** Replied, Scheduled, Completed

**Universal terminal status — always include:** `Added to CRM`. When a campaign contact graduates to Active Leads / Clients, this status moves the tracker entry out of the active sweep and the main CRM takes over. See CRM skill → "Promotion to main CRM" for what happens next.

## Setting up the campaign page

Open the two or three most recent campaign pages under the Campaigns parent page (ID in `notion-helper`) and match their shape — section order, column layout, table vs. bullets, what lives on a sub-page. Weight recency first: the newest page reflects the current format even when its campaign was a different type. Then similarity — among recent ones, a same-shape campaign (cold DM, event promo, partnership push) is the closer model. Read finished campaigns, not one mid-build.

Keep the page skimmable — the offer, the cohort, the numbers, the tracker, all at a glance. Anything that would grow past a few lines becomes a sub-page with a link left behind: search filters, message scripts, research notes. A section that earns its place on the main page fits in a screenful.

Shaw sometimes leaves placeholders like `{Add outreach database here}` — follow those when present.

## Common segment schemes

Pick the one that matches how Shaw wants to prioritize:

- **Relationship proximity** — met in person → met virtually → have their email → cold
- **Seniority × location** — DFW leaders → DFW managers → DFW ICs → non-DFW leaders → ...
- **Channel** — existing DMs → LinkedIn-only → cold email
- **Heat tier** — warm intros → known but not close → cold

The number of segments matches the number of distinct message templates Shaw will write.
