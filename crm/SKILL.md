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
  any mention of existing clients and expansion opportunities. Follow-up reviews cover Active
  Leads, Clients (Nurture), AND any active campaign trackers linked from the CRM page.
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

For **ABA Calls** (sales calls), **ABA Trainings** (delivery sessions: 1:1 workshops, trainings,
ongoing engagements), and **ABA** (tasks, launches, events, outreach) — see the canonical
catalog in `notion-helper/SKILL.md` → "Main Databases."

**Gmail account:** `shaw@aibuilder.academy` (all outbound sales activity lives here)
**Google Calendar:** Available via the `gcal_list_events` tool — use as an additional signal for recent meetings

---

## Active Leads Database Schema

| Field | Type | Notes |
|---|---|---|
| Name | Title | Full name |
| Email | Text | Email address |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact` |
| Status | Multi-select | `Pending Call`, `Booked Call`, `Outline Sent`, `Closed`, `Lost` |
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
- `Call w/ [Person] & [Person] (3/27). Sending proposal (3/28).`

**Bad example (too much context):**
- `Call w/ [Person] & [Person] (3/27). [Company] growth analytics, small team, already using MCP + agents. $[amount] L&D budget/person. Sending proposal (3/28).`

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
  Example: `[Person] ([email]) responded, evaluating proposals (3/17).`

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
- **Lost** — explicitly not moving forward

---

## Clients (Nurture) Database Schema

This table holds people who have paid Shaw — the goal is to nurture clients for expansion and to
constantly hear their problems to inform marketing and new offers.

| Field | Type | Notes |
|---|---|---|
| Name | Title | Full name |
| Email | Text | Email address |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact`, `Homepage Contact` |
| Status | Multi-select | `Active`, `Nurturing`, `Expansion`, `Churned` |
| Last Contact? | Date | Date of most recent touchpoint |
| Next Check-in | Date | `Active` → date of next scheduled training/session. `Nurturing` → future outreach date (quarterly cadence). See lifecycle stages below. |
| Engagement Type | Multi-select | `1:1`, `Workshop`, `Bootcamp`, `Ad Hoc Advisory` |
| Notes | Text | Short chronological log (see Client Notes Format below) |

### Client Lifecycle Stages

```
Active → Nurturing → Expansion → (back to Nurturing or Churned)
```

- **Active** — currently in an engagement (delivering workshops, consulting, etc.). No nurture
  outreach needed because Shaw is already talking to them regularly. `Next Check-in` should mirror
  the date of the next scheduled training/session — it doubles as an "are we still on track" signal,
  not a future outreach date.
- **Nurturing** — engagement is complete; now in the quarterly check-in rhythm. The default state
  for most clients. Stay close, hear their problems, inform marketing and new offers. `Next Check-in`
  holds a forward-looking outreach date (~3 months out by default) — this is the only stage where
  that field means "reach out next."
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

- **ABA Calls** — *sales calls only*. Discovery, follow-up, proposal review, research chats.
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
2. Query the tracker for contacts where `Next Contact <= today` or `Next Contact` is blank
   on a non-terminal status (i.e., not `Passed` or `Workshop Booked`). Same filter logic as
   Active Leads.
3. Cross-reference Gmail (or LinkedIn for LinkedIn-only contacts) for replies since
   `Last Contact`, exactly as you would for an Active Lead.
4. Surface contacts that are due, replied, or have stale `Next Contact` dates in the summary.

**Keep tracker updates light.** When a reply or status change comes in, append a dated note
and bump `Last Contact` / `Next Contact` — same conventions as Active Leads notes. Don't
restructure the tracker; that's the outreach skill's job.

## Gmail & Calendly Signals

All outbound sales activity lives in Gmail at `shaw@aibuilder.academy`. Two patterns to know:

- **Direct thread activity** — search `from:<email> OR to:<email>`
- **Calendly bookings** — land in the inbox from `notifications@calendly.com` with subject
  `"New Event: <name> - <time> - <event type>"`. The invitee email in the notification body
  **may differ from the CRM email on file** (e.g., a lead can book with a personal email even
  when their CRM entry has a work email). Match Calendly bookings by name, not email.

This is the canonical detection path for new bookings. A global scan for `from:notifications@calendly.com subject:"New Event" after:<last-sync-date>` catches brand-new leads who booked
without an existing CRM entry.

---

## Key Principles

- **Always read before writing** — fetch the lead's current Notion page before making any updates
- **Append, never overwrite** — notes are a chronological log; always add to the end
- **Match Shaw's voice** — short, direct, friendly; no corporate filler
- **Don't over-follow-up** — respect the cadence limits; after FU #2 on contact form leads, stop
- **Every touchpoint updates two dates** — `Last Contact?` (when it happened) and `Next Contact` (when to touch them again). Set both, every time. `Next Contact` is the structured signal Workflow 1 sorts on; leaving it stale is how leads fall through the cracks.
- **Default to action** — when follow-ups are due, create Gmail drafts directly rather than presenting options. For LinkedIn-only leads, flag them in the summary for DM follow-up instead
- **Every call deserves a follow-up email** — whenever a call or meeting is logged (via Workflow 2) or detected (via Workflow 1), check whether a follow-up email was sent. If not, prompt Shaw or flag it. Sources to check: ABA Calls, ABA Trainings, CRM notes, and Google Calendar
