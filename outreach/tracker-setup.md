# Tracker Setup (Notion)

Use this when Phase 5 of the outreach flow calls for creating a tracker. Shaw's campaigns live on Notion pages with an **inline** database for the tracker, a segment legend, templates, and context — all on one page.

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
| Next Contact | Date | Date of next planned touchpoint. **Standard column — always include.** Mirrors the CRM field; CRM Workflow 1's active-campaign sweep sorts on it (`Next Contact <= today`) to surface due follow-ups. Blank = no FU planned (intentional, never backfilled). On a **batch send**, set it uniformly to the **FU1 date from the campaign's Promo Calendar** so the whole batch surfaces together. |
| Medium | Select | Channel the outreach goes out on: `Email` / `LinkedIn` / `Text`. Add for multi-channel campaigns — it **drives the per-prospect script format** (email rows need a subject line + hyperlinked CTA; DM/text rows keep the raw link — see `per-prospect-scripting.md`). |
| Notes | Rich text | **FU log ONLY** — short dated pipeline actions (see Notes format in CRM skill). Not for background/context. |

Additional columns when the campaign calls for them: Company, Company Size, LinkedIn URL, Location, topic-specific checkboxes.

**Post-event attendee trackers** add behavioural columns, since engagement during the session is the only intent signal available: `Minutes` (number — time in the session), `Chat` (number — messages posted), `Source` (select — acquisition channel, including a `Forwarded` option for links that were passed along), and `Email Type` (select — `Work` / `Personal`). Sort on Minutes + Chat to prioritise. Company belongs in the row's Context body, not a column — attendee lists run 90+ rows and a mostly-empty Company column earns less than it costs. Building the list is `event-attendance-reconciliation.md`.

**`Next Contact` is not optional** — every outreach DB gets it. It's the structured home for "FU on 7/14"-type markers (which must never live in Notes), and the CRM skill's campaign sweep depends on it.

### Context goes in the row's page body, not the Notes column

Background on a contact — role, company, size, location, DM/relationship history, personalization hooks — lives in a `## Context` section **inside the contact's row page**, mirroring the CRM page-body convention. The Notes *column* is reserved for the dated FU log (`Ask sent (7/10). FU1 (7/14). Replied (7/15).`). When seeding a tracker from an enriched list, write the enrichment into each row page's Context section via `notion-update-page` `insert_content`, and leave the Notes column empty. (Shaw's call, 2026-07-06 — July event promo tracker.)

### Status options

**Only meaningful forward progress.** If blank already communicates the default ("message sent, no reply yet"), there's no status for it. No `Sent`, no `No response`.

Campaign-specific examples:
- **Workshop outreach:** Replied, Applied, Selected
- **Event outreach:** Booked Call, Pending Call
- **Research calls:** Replied, Scheduled, Completed

**Universal terminal status — always include:** `Added to CRM`. When a campaign contact graduates to Active Leads / Clients, this status moves the tracker entry out of the active sweep and the main CRM takes over. See CRM skill → "Promotion to main CRM" for what happens next.

## Add a segment legend

After the database, add a simple reference table so Shaw (and future Claude sessions) can decode the numbers:

```
| Segment | Description |
|---------|-------------|
| 1       | Met in person |
| 2       | Met on a virtual call |
| 3       | Have their email |
```

Use `notion-update-page` with `update_content` to insert the table after the database.

## Place it in the right spot

Look for cues on the page about where the tracker goes. Shaw sometimes leaves placeholders like `{Add outreach database here}`. If there's a natural section (e.g., an "Outreach" heading), use that.

## Common segment schemes

Pick the one that matches how Shaw wants to prioritize:

- **Relationship proximity** — met in person → met virtually → have their email → cold
- **Seniority × location** — DFW leaders → DFW managers → DFW ICs → non-DFW leaders → ...
- **Channel** — existing DMs → LinkedIn-only → cold email
- **Heat tier** — warm intros → known but not close → cold

The number of segments matches the number of distinct message templates Shaw will write.
