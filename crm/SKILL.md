---
name: crm
description: >
  Use this skill whenever Shaw mentions leads, contacts, sales pipeline activity, or anything
  CRM-related — even casually. Triggers include: "check my CRM", "update the CRM", "any
  updates on leads?", "add this person to the CRM", "review my pipeline", "follow up with X",
  "anyone worth following up with", "check active campaigns", "did anyone respond?",
  "cross-reference Gmail", "ABA contact form", or any mention of a specific lead's name in a
  sales context. Also triggers when Shaw shares new contact form submissions or inbound emails
  that look like potential leads. Also triggers for client/nurture activity: "check on my
  clients", "any clients due for check-ins", "move this lead to clients", "nurture review", or
  any mention of existing clients and expansion opportunities. Also triggers when a discovery
  call is booked — directly or surfaced during a sync. Follow-up reviews cover Active Leads,
  Clients (Nurture), AND any active campaign trackers linked from the CRM page.
---

# CRM Skill

Shaw runs a B2B AI enablement sales pipeline and client nurture system. This skill governs how to
read, update, and act on his CRM in Notion — both the Active Leads pipeline and the Clients (Nurture)
database. It covers cross-referencing Gmail for new activity, checking call notes in Notion, adding
new leads, moving closed deals to the client database, and proactively managing follow-ups across
both tables.

---

## Key Locations

CRM-specific sub-databases (sub-pages of the CRM page, not in the main database catalog):

| Resource | Location |
|---|---|
| CRM page | Notion page ID: `[page-id]` |
| Active Leads database | Data source: `collection://[database-id]` |
| Clients (Nurture) database | Data source: `collection://[database-id]` |
| 🧊 Archived Leads database | Data source: `collection://[database-id]` (parent: CRM page) |

For **ABA Calls** (sales calls), **ABA Trainings** (delivery sessions: 1:1 workshops, trainings,
ongoing engagements), and **ABA** (tasks, launches, events, outreach) — see the canonical
catalog in `notion-helper/SKILL.md` → "Main Databases." Event-type SOPs (Discovery Call,
Check-in Call, Wrap-up Call, 1:1 Claude Workshop) are catalogued in `notion-helper/SKILL.md` →
"Event-Type SOPs."

**Gmail account:** `shaw@aibuilder.academy` (all outbound sales activity lives here)
**Google Calendar:** Available via the `gcal_list_events` tool — use as an additional signal for recent meetings

---

## Active Leads Database Schema

| Field | Type | Notes |
|---|---|---|
| Name | Title | Full name |
| Email | Text | Email address |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `Referral`, `ABB`, `ABA Contact`, `ABA Discovery Call`, `Homepage Contact`. `Referral` = warm intro from an existing client, partner, or other contact (e.g., a current client introduces Shaw to an investor or peer). `ABA Contact` = aibuilder.academy contact form. `ABA Discovery Call` = direct Calendly booking on aibuilder.academy (no contact form first — they jumped straight to scheduling). `Homepage Contact` = shawhintalebi.com contact form. |
| Status | Multi-select | `Pending Call`, `Booked Call`, `Outline Sent`, `Closed`, `Lost`, `Disqualified` |
| Last Contact? | Date | Date of most recent touchpoint |
| Next Contact | Date | Date of next planned touchpoint. Structured replacement for "FU in April"-style notes. Workflow 1 uses this to surface what's due. See `references/follow-up-guidance.md` for cadence defaults by situation. |
| Notes | Text | Short chronological log (see format below) |

### Notes Format

Short, comma-separated, date-stamped **pipeline actions only**. Never write full sentences.
Notes should record *what happened* in the sales process — not details about the lead's business,
team, tech stack, budget, or call content. That context lives in the ABA Calls page and doesn't
need to be duplicated here.

**Good examples:**
- `Warm outreach (3/4). FU (3/11). Asked about individual training (3/12). Replied about ABA (3/13).`
- `ABA contact form (3/16). Replied, offered call (3/16).`
- `Call on 3/13. Not right now.`
- `Call w/ [Lead Name] & [Lead Name] (3/27). Sending proposal (3/28).`

**Bad example (too much context):**
- `Call w/ [Lead Name] & [Lead Name] (3/27). [Company] growth analytics, small team, already using MCP + agents. $[amount] L&D budget/person. Sending proposal (3/28).`

**Rules:**
- Always append new entries; never overwrite existing notes
- Use `(M/D)` date format
- Common shorthands: `FU` = follow up, `BAMFAM` = book a meeting, from a meeting, `ABA` = AI Builder Academy, `ABB` = AI Builders Bootcamp
- Only include: outreach actions, call dates, proposal/outline sent, follow-ups, responses, status changes
- Do NOT include: company details, team size, tech stack, budget info, call discussion topics
- **Do NOT include future-FU markers** (e.g., "FU in April", "BAMFAM 4/30"). Those belong in the
  `Next Contact` field. Notes log what *happened*; `Next Contact` tracks what's *next*.
- When other stakeholders are involved in a deal (e.g. a second contact on the thread), mention them
  by name so future sessions have context without re-reading the full email chain.
  Example: `Srikanth ([email]) responded, evaluating proposals (3/17).`

---

## Sales Pipeline Stages

```
Contact → Book Call → Attend Call → Send Outline/Proposal → Closed
```

Status should reflect the furthest confirmed stage reached:
- **Pending Call** — call link sent or time proposed, awaiting confirmation
- **Booked Call** — call confirmed on calendar
- **Outline Sent** — proposal/outline sent after call
- **Closed** — deal won
- **Lost** — explicitly not moving forward (but may circle back later — set `Next Contact` to the re-engagement date)
- **Disqualified** — not a fit at all (wrong audience, wrong ask, low-quality inbound). No re-engagement — leave `Next Contact` blank. Can be dual-tagged with `Lost` for view tidiness; the sync ignores them either way because their `Next Contact` is blank.

---

## Lead Archiving

The **🧊 Archived Leads** database (sub-page of the CRM page) holds `Lost` and `Disqualified`
leads that have aged out — Shaw periodically batch-moves them out of Active Leads to keep the
working pipeline focused. Same schema as Active Leads minus formula columns; `Next Contact` is
blank on every archived record (terminal, no re-engagement planned from this table — true
re-engagements get re-added to Active Leads).

Archived Leads are a historical record, not a working queue. Don't draft follow-ups against
them, don't auto-fill `Next Contact`, and don't surface them in syncs as "due" or "worth
reviewing". Do treat them as known not-orphans when reconciling ABA Calls — see Workflow 1.

Lifecycle: **Active Leads (working pipeline) → status changes to `Lost` / `Disqualified` →
stays in Active Leads with a re-engagement date or blank `Next Contact` → moved to Archived
Leads manually when the re-engagement window has clearly closed.**

Archiving is a manual batch operation — no dedicated workflow.

---

## Clients (Nurture) Database Schema

This table holds people who have paid Shaw — the goal is to nurture clients for expansion and to
constantly hear their problems to inform marketing and new offers.

| Field | Type | Notes |
|---|---|---|
| Name | Title | Full name |
| Email | Text | Email address |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `Referral`, `ABB`, `ABA Contact`, `ABA Discovery Call`, `Homepage Contact`. Mirrors Active Leads — source carries over when a lead graduates to a client. |
| Status | Multi-select | `Active`, `Nurturing`, `Expansion`, `Churned` |
| Last Contact? | Date | Date of most recent touchpoint |
| Next Contact | Date | Date of next planned touchpoint — same field as Active Leads. See "Next Contact semantics" below for how its meaning shifts by status. |
| Engagement Type | Multi-select | `1:1`, `Workshop`, `Bootcamp`, `Ad Hoc Advisory` |
| Notes | Text | Short chronological log (see Client Notes Format below) |

### Next Contact semantics

`Next Contact` is a catch-all for the next planned touchpoint of any kind. Most often it's a follow-up message; sometimes it's a scheduled call. The type of touchpoint is read from the linked pages on the CRM record, not from a separate field — if there's an ABA Calls or ABA Trainings page dated `Next Contact`, the touchpoint is a call. Otherwise assume a follow-up message.

This is the same field on both Active Leads and Clients. Workflow 1 sorts on `Next Contact <= today` for both tables.

### Client Lifecycle Stages

```
Active → Nurturing → Expansion → (back to Nurturing or Churned)
```

- **Active** — currently in an engagement (delivering workshops, consulting, etc.). No nurture
  outreach needed because Shaw is already talking to them regularly. `Next Contact` mirrors the
  date of the next scheduled session — the linked ABA Trainings page is what makes it legible
  as a session rather than a message.
- **Nurturing** — engagement is complete; now in the quarterly check-in rhythm. The default state
  for most clients. Stay close, hear their problems, inform marketing and new offers. `Next Contact`
  holds a forward-looking outreach date (~3 months out by default) — typically a check-in message.
- **Expansion** — a nurture conversation has surfaced a new opportunity. They're back in a "buying"
  mode but warmer than a new lead because of existing trust and context. This is the highest-leverage
  sales motion in the CRM.
- **Churned** — gone quiet, stopped responding to check-ins, or explicitly said they're not
  interested in further engagement.

### Client Notes Format

Same short-log style as Active Leads, but vocabulary shifts from pipeline actions to relationship
actions. Record check-ins, expansion conversations, and status changes — not business context
(that goes in the page body).

**Good examples:**
- `Quarterly check-in (1/15). Exploring data team training (1/20). Sent proposal (1/22).`
- `Check-in (4/1). Happy with workshop results. Next check-in July.`
- `Reached out about new team members (5/3). Booked call (5/5).`

**Rules:**
- Same rules as Active Leads notes: append only, `(M/D)` date format, use shorthands
- Track: check-in dates, expansion conversations, proposals, status changes
- Do NOT duplicate business context that belongs in the page body

---

## Workflows

Read the relevant workflow file before executing. Each contains step-by-step instructions.

| Workflow | Trigger | File |
|---|---|---|
| 1. Three-Source Sync (Gmail ↔ ABA Calls ↔ CRM) | Shaw asks to review, sync, or audit the CRM — covers both Active Leads and Clients in a single pass | `workflows/workflow-1-sync.md` |
| 2. Update a Lead | Shaw shares new info about a single lead out-of-band (reply received, call happened, proposal sent) | `workflows/workflow-2-update.md` |
| 3. Add a New Lead | Shaw shares a new contact form submission, inbound email, or new lead | `workflows/workflow-3-add-lead.md` |
| 4. Link Call Notes to CRM Lead Page | Connecting (or refreshing) the full list of call-note links on a lead/client page | `workflows/workflow-4-link-calls.md` |
| 5. Move Lead to Clients | A deal closes and the lead needs to graduate to Clients (Nurture) | `workflows/workflow-5-move-to-clients.md` |
| 6. Onboard Workshop Participant | A new participant is accepted for a free 1:1 Claude Workshop and needs CRM + ABA Trainings setup | `workflows/workflow-6-onboard-workshop.md` |
| 7. Discovery Call Intake | A discovery call is booked — detected during a Workflow 1 sync, or Shaw mentions in chat that one was booked. Orchestrates CRM resolution, the ABA Calls page + brief, the FU task, and the confirmation email | `workflows/workflow-7-discovery-intake.md` |

Client/nurture review is handled by Workflow 1, which syncs Active Leads and Clients in the
same pass. Nurture-specific guidance (check-in cadence buckets, expansion signals, check-in
email tone) lives in `references/follow-up-guidance.md`.

---

## References

Read these when the workflow requires follow-up assessment or email drafting.

| Reference | Contents | File |
|---|---|---|
| Follow-Up Guidance | Follow-up cadences, drafting rules, tone guidance, lead source context | `references/follow-up-guidance.md` |

---

## Three Databases Show Up During CRM Work

Shaw's leads and clients leave a trail across three databases. Keeping them straight matters
because the sync workflow treats each one differently.

- **ABA Calls** — *lead and client 1:1 conversations*. Discovery, follow-up, proposal review,
  research chats, and check-ins — check-ins pair with leads (warm-but-not-converted nurture)
  as well as clients (post-session and quarterly nurture); see the Check-in Call SOP.
  Workflow 1 reconciles this against the CRM in both directions, and Workflow 3 creates new
  entries when a brand-new sales call shows up in Gmail.
- **ABA Trainings** — *delivery sessions only*. 1:1 workshops, trainings, ongoing engagements.
  Shaw creates these when an engagement is scheduled (or Workflow 6 does it on onboarding);
  the sync workflow does NOT auto-create them.
- **ABA** — *tasks and events*. Launches, outreach, partnerships, follow-up task pages, and
  events. Not a lead-facing database; rarely linked on CRM pages directly.

**Linking rule for CRM page bodies:** ABA Calls and ABA Trainings pages both belong linked on a
lead or client's CRM page. Use Workflow 4's full-rewrite rule. A lead typically accumulates sales
calls (ABA Calls) before conversion and delivery sessions (ABA Trainings) after — both belong on
the CRM page so the full history is one click away. ABA task/event pages are generally not
linked unless a specific event is directly relevant.

**Page body structure:** the `## Calls` section always sits at the bottom of a CRM page. Anything
else — `## Context` (engagement details, stakeholders, blockers, campaign tracker links),
scratchwork, ad hoc sections — goes above it. Calls is a growing trail of historical links;
pinning it to the bottom keeps the durable signal Shaw scans first from getting buried.

**Search behavior:** when fetching context for a lead, search ABA Calls and ABA Trainings by
name, email, company name, and email domain — pages are sometimes filed under company name,
and stakeholders get cc'd from the same domain.

To reconcile ABA Calls against the CRM in both directions during a sync, see **Workflow 1**.

## Active Campaigns

The CRM page has an **Active Campaigns** section that links to currently-running outreach
campaigns (e.g., "Sell 1:1 Claude Workshops"). Each linked campaign page contains its own
**outreach tracker** — an inline Notion database with `Name`, `Contact`, `Status`, `Last Contact`,
`Next Contact`, `Notes`, and `Segment` columns. These trackers are created and structurally
owned by the **outreach** skill; the CRM skill only reads them.

**Why this matters:** active campaign contacts are not in Active Leads. They're prospects in
the middle of a structured outreach push. If you only check Active Leads + Clients during a
follow-up review, you'll miss everyone Shaw is currently working on a campaign.

**Behavior during follow-up reviews:** any time Shaw asks "anyone worth following up with",
"check the CRM", "review my pipeline", or any equivalent — fetch the Active Campaigns list
off the CRM page first, then for each linked campaign:

1. Open the campaign page and find its outreach tracker (inline database).
2. Query the tracker for contacts where `Next Contact <= today`. Only surface contacts with
   an explicit due date. Blank `Next Contact` on campaign contacts is intentional (no follow-up
   planned) — never flag it or backfill it.
3. Cross-reference Gmail (or LinkedIn for LinkedIn-only contacts) for replies since
   `Last Contact`, exactly as you would for an Active Lead.
4. Surface contacts that are due, replied, or have stale `Next Contact` dates in the summary.

**Keep tracker updates light.** When a reply or status change comes in, append a dated note
and bump `Last Contact` / `Next Contact` — same conventions as Active Leads notes. Don't
restructure the tracker; that's the outreach skill's job.

### Promotion to main CRM

When a campaign contact graduates to the main CRM (Active Leads or Clients) — typically after
they reply with intent and Workflow 3 creates a lead record — mark them `Added to CRM` in the
campaign tracker and clear their `Next Contact` field. From that point on:

- All future updates (Notes, Last Contact, Next Contact, Status) happen **only** in the main
  CRM record
- The campaign tracker entry remains as a historical breadcrumb showing where the lead originated
- Workflow 1's active campaign sweep skips `Added to CRM` contacts — they're already covered by
  the Active Leads / Clients filter

This prevents two records from drifting apart and avoids duplicate cadences (one from the
tracker, one from the CRM). If a campaign tracker doesn't have `Added to CRM` as a Status
option yet, add it (orange or pink works well for visual distinction from active statuses).

## Gmail & Calendly Signals

All outbound sales activity lives in Gmail at `shaw@aibuilder.academy`. Two patterns to know:

- **Direct thread activity** — search `from:<email> OR to:<email>`
- **Calendly bookings** — land in the inbox from `notifications@calendly.com` with subject
  `"New Event: <name> - <time> - <event type>"`. The invitee email in the notification body
  **may differ from the CRM email on file** (e.g., a lead can book with a personal email even
  when their CRM entry has a work email). Match Calendly bookings by name, not email.

This is the canonical detection path for new bookings. A global scan for `from:notifications@calendly.com subject:"New Event" after:<last-sync-date>` catches brand-new leads who booked
without an existing CRM entry.

**Discovery-call bookings route to Workflow 7.** When a detected Calendly booking is a
*discovery call* (event types per the Discovery Call SOP — `ABA Intro Call`, `AI Transformation`,
`1:1 Claude Workshop (Discovery)`), hand it to **Workflow 7 (Discovery Call Intake)** rather
than processing it piecemeal. Workflow 7 orchestrates CRM resolution, the ABA Calls page and
brief, the FU task, and the confirmation email in one pass.

---

## Key Principles

- **Always read before writing** — fetch the lead's current Notion page before making any updates
- **Append, never overwrite** — notes are a chronological log; always add to the end
- **Match Shaw's voice** — short, direct, friendly; no corporate filler
- **Don't over-follow-up** — respect the cadence limits; after FU #2 on contact form leads, stop
- **Blank `Next Contact` is assumed intentional** — not every lead needs an active follow-up date. `Next Contact` is the structured signal Workflow 1 sorts on, and Shaw leaves it blank deliberately when no follow-up is planned. If context strongly suggests a miss (e.g., an active lead with recent activity but no date), flag it in the summary as "worth reviewing" — but never auto-fill without Shaw's approval.
- **Drafts aren't touchpoints — only sent is.** A drafted email sitting in Gmail is not a touchpoint until Shaw sends it. Update `Status`, `Last Contact?`, and `Next Contact` based only on actions that have actually happened — calls that took place, emails confirmed sent. When a workflow drafts a follow-up email in the same run as a CRM update, only update CRM for the action that actually occurred (e.g., the call). Leave email-dependent state changes (like advancing to `Outline Sent`, or the +2-day post-outline FU date) for a later update once Shaw confirms send — the next sync will pick up the send via Gmail signal anyway.
- **Default to action** — when follow-ups are due, create Gmail drafts directly rather than presenting options. For LinkedIn-only leads, flag them in the summary for DM follow-up instead
- **Always invoke email-helper before drafting an email** — every Gmail draft created during a CRM workflow goes through email-helper first. Skills compose: CRM owns the *who/when/why* of the follow-up; email-helper owns the *voice, threading, and Gmail mechanics*. Skipping it is how plain-body drafts, missed em-dash rules, and snippet-driven (rather than thread-driven) follow-ups slip through. This applies in Workflow 1's step 6, Workflow 2 follow-ups, Workflow 7's confirmation email, and any other CRM step that creates a draft.
- **Every call deserves a follow-up email** — whenever a call or meeting is logged (via Workflow 2) or detected (via Workflow 1), check whether a follow-up email was sent. If not, prompt Shaw or flag it. Sources to check: ABA Calls, ABA Trainings, CRM notes, and Google Calendar
