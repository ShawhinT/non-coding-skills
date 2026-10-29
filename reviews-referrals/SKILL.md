---
name: "reviews-referrals"
description: "Manage the Reviews/Referrals database in ABA (Master), the single tracker for the testimonial (review) and referral lifecycles. Use whenever Shaw mentions testimonials, reviews, referrals, intros, or pull-quotes — \"did X approve?\", \"polish X's form response\", \"process new form submissions\", \"kick off a testimonial/referral ask for X\", \"who owes me referrals?\", \"X intro'd me to Y\", \"log these names\", \"publish X's quote\", \"which testimonials are stuck\", \"sweep reviews/referrals\", \"thank X for the referral\". Also fires when a training wraps (queue the review ask), when a testimonial greenlight lands (advance the row), when a 3-way intro email arrives (subjects like \"[Name] <> Shaw\"), when a client offers referrals unprompted, and for the daily reconcile/sweep. Trigger words: testimonial, review, referral, intro, warm intro, pull-quote, social proof, form response. Do NOT use for SOP edits (sop-helper), generic CRM work (crm), or pre-call context (meeting-prep)."
---

# Reviews/Referrals Skill

One database, two sequential tracks. The **Reviews/Referrals** database in ABA (Master)
tracks, per person, the testimonial (review) lifecycle and the referral lifecycle — the
"Reviews" and "Referrals" Rs of the 4Rs. The tracks run one after the other, never in
parallel: review ask → publish → referral ask at the Results call. A referral runs first only
when the person offered it, or when there was no training (coffee chat, free call). Because
the tracks are sequential, the row's single Last/Next Contact always belongs to whichever
track is live.

This SKILL.md is a router: shared facts and rules only. Mechanics live in `workflows/`.
Policy (cadence, status meanings, templates, ask policy) lives in the two SOPs — when a
question is about *what to do or when*, the SOP answers it; when it's about *how* (payloads,
tools, body formats), this skill answers it.

## Where Things Live

| Thing | ID / URL |
|---|---|
| Reviews/Referrals database (page) | `[database-id]` |
| Data source | `[page-id]` |
| Database URL (default view `?v=[database-id]`) | https://www.notion.so/[page-id] |
| Testimonial Ask SOP | `[page-id]` |
| Referral Ask SOP | `[page-id]` |

### Form response sheets (Google Drive)

The response sheets are the reconcile source for submissions (there is no per-row `Form`
property; the row's training type says which sheet applies). The `forms.gle` URL is what goes in
ask emails via `email-helper`.

| Form | Response sheet ID | Public URL |
|---|---|---|
| 1:1 Claude Workshop - Testimonial | `[sheet-id]` | [form-url] |
| ABA Training - Testimonial (group/team) | `[sheet-id]` | *not in use — recent group sends use the 1:1 URL above ([Person] / [Company], 6/30/26)* |

Both share the 4-question spine: Before → Impact → Worth it? → Permission.

### Related databases

| DB | Data source ID |
|---|---|
| Companies | `[database-id]` |
| CRM Active Leads | `[page-id]` |
| Clients (Nurture) | `[page-id]` |
| Archived Leads | `[page-id]` |
| Friends | `[page-id]` |
| Engagements | `[page-id]` |

## Schema Cheat Sheet

| Property | Type | Notes |
|---|---|---|
| Name | title | One row per person. Multiple per company is fine |
| Email | email | Direct email |
| Company | relation | → Companies. The account this person belongs to; hidden in the default table view. What the company page uses to list its people |
| Friend | relation | → Friends. Set instead of Company when the person is in the non-lead network (a friend, partner, channel). Hidden in the default view. Exactly one of Company / Friend is filled; both blank only for a solo client or a person with no record anywhere |
| CRM | url | The person's **own** row in Active Leads / Clients (Nurture) / Archived Leads, filled only when they have one (a buyer, a lead, an archived lead). A session participant at a client company has a `Company` and no `CRM` — never point this at the buyer's row on their behalf |
| Engagement | relation | → Engagements DB, only for paid work |
| Review Status | select | `Not Asked` · `Asked` · `Form Submitted` · `Approved` · `Published` · `Declined`. `Published` means the quote is live on one of Shaw's own surfaces (website, sales letter, deck, post), put there by Shaw |
| Referral Status | select | `Not Asked` · `Asked` · `Intro Made` · `Converted` · `Declined`. Reflects the furthest stage across that person's referrals. The status tracks whose court the ball is in; *who* was named lives on the `## Referrals` ledger, so names arriving leave the row at `Asked` until an intro actually lands |
| Last Contact | date | Most recent touch on whichever track is live |
| Next Contact | date | When the next touch is due, on whichever track is live. Clear when nothing is pending |
| Notes | text | Conversation log, `(M/D)` format, append-only — same principle as `crm`'s Notes Format: what the person said, offered, or approved and what changed on the row, never a touch that's coming and never a follow-up that went out (the dates carry cadence). Referral events carry a `Referral track:` prefix the first time the track opens. No em dashes |

New rows default both statuses to `Not Asked`. Which track a date belongs to is never
ambiguous: only one track is live at a time, and Notes say which.

## Page Body Conventions

- `## Context` — pinned at the top, present on every row. The durable picture of the person:
  which channel they actually reply on, the win a review ask would anchor on, the state of
  whichever track has run, and `Open items` last. Written per
  `../crm/references/context-sections.md` — that file is the single home for bullet shape,
  the keep/cut filter, ordering, and date-stamping, so don't restate its rules here. What does
  *not* transfer is CRM's two-sections-only rule: these rows carry the sections below as well,
  and Context sits above all of them.
- `## Form Response` — verbatim form answers (review track, historical record).
- `## Testimonial` / `## Drafts` — polished quote(s); see `references/polish-framework.md`.
- `## Pre-Drafted (FU2, sent M/D)` — exact sent pre-draft quote, read from sent mail.
- `## Referrals` — the referral ledger, one line per referred person:
  `- [Name] ([title], [company]) — [stage: named M/D / intro'd M/D / converted M/D]`,
  upgraded to a `<mention-page>` link once their Active Leads page exists. Ledger lines only —
  narrative about the referral belongs in `## Context` — and the section stays pinned at the
  bottom. Created when the referral track opens.

## Routing

| Situation | File |
|---|---|
| Open a review ask, placeholder rows, FU stages, process a form submission, pre-drafted testimonials | `workflows/testimonial-ask.md` |
| Approval replies, edits, anonymity, publish, review-track declines | `workflows/testimonial-approve.md` |
| Open a referral ask (on-ramp or offered), log names | `workflows/referral-ask.md` |
| Intro lands → CRM handoff, converted, thank-you, referral-track close-out | `workflows/referral-intro.md` |
| Daily reconcile + sweep (both tracks), due-row detection | `workflows/sync.md` |

The track handoff lives here so both sides see it: the referral ask is made at the Results
call, which its own dated ABA task carries (created at the session, dated session + 29) —
not from a date on this row. Flow and templates in the Referral Ask SOP.

## Rules

- **Defer policy to the SOPs.** Cadence numbers, status meanings, templates, and ask policy
  are never restated here. If a process question can't be answered from these files, the SOP
  has it.
- **Send on the channel they answer, not the one the SOP was written for.** Every workflow
  here hands off to `email-helper` because email is the common case, not because email is
  required. When the person's live channel is text, DM, or Slack, the SOP's sequence and
  cadence still hold and only the delivery changes: adapt the template to that channel's
  register (a text is one or two lines, no greeting, no sign-off) and send it there. A row's
  `## Context` records the channel and the evidence for it, so check that before drafting.
  An ask sent where someone has stopped replying reads as no ask at all, and the row goes
  stale waiting on a response that was never coming.
- **Defer email composition to `email-helper`.** Hand off the SOP template name + row
  context; it produces the draft. Non-email sends still go through it for voice, then get
  compressed to the channel.
- **Reviews come from two places: the testimonial form and Trustpilot.** The database
  tracks the review lifecycle per person, not the form, so a Trustpilot review earns a row
  exactly as a form submission does, with the Trustpilot review standing in for
  `## Form Response`. The Trustpilot campaign tracker owns its own ask
  cadence and is the wrong home for the quote itself: it goes stale when the campaign closes,
  while the row is where a person's social proof accumulates. Praise landing anywhere else, a
  LinkedIn comment or a warm line in an email, is not a review and doesn't earn a row.
- **Drafts aren't touchpoints.** Advance Status / Last Contact / Next Contact only on sends
  and events that actually happened.
- **Reconcile before acting on Status.** The form sheets are truth for submissions, Gmail
  for everything after; the row lags both. Run `workflows/sync.md` reconcile before any
  sweep or pre-draft.
- **One person, one next touch.** The row's single Next Contact enforces this within the
  database. When either track goes live, clear the sibling's Next Contact (the row `CRM`
  points at, or the `Friend` row) and add a Notes pointer (`Next touch owned by
  Reviews/Referrals, due M/D.`); hand it back when both tracks are terminal or parked. A
  participant with neither `CRM` nor `Friend` has no sibling, so this row is the only place
  they are scheduled and its Next Contact never goes blank while anything is pending.
  Handing the date to a call page or ABA task is only valid when the sibling carries the
  schedule. `Company` is not a sibling. The full rule lives in the `crm` skill.
- **Next Contact is the only schedule.** The property is the single source of truth for
  when the next touch is due; the Notes property is a log of what already happened. A
  forward-looking date in Notes duplicates the property and goes stale the moment the date
  moves, so keep the rule and drop the date: "flip to Declined on silence at the Next
  Contact date," not "no response by 8/14: flip to Declined." If the scheduling context
  genuinely needs prose (why the date sits where it does), it lives as a dated bullet in
  the context section of the page body, never in the Notes property. When a Notes date
  contradicts the property, the property wins and the Notes line gets repaired in the same
  pass.
- **Status flips and body updates are atomic.** Update properties and body together.
- **Honor permission level.** The form's Permission column dictates attribution; default to
  less when ambiguous.
- **Polish from real submissions or primary records only.** Never invent or amplify; see the
  polish framework's maximum-verbatim discipline.
- **No em dashes** in notes, polished quotes, or attribution lines (raw verbatim excepted).
- **Notion + Drive + Gmail-via-email-helper only.** No calendar events, invoices, or other
  side effects; those compose via other skills.

## Composition

- `email-helper` — all drafts. `google-drive-helper` — form sheets, transcripts.
- `crm` — CRM page lookup, referred-lead creation (its Workflow 3), touch ownership.
- `engagements` — opens placeholder rows here at engagement creation (its Workflow 1);
  links this row under the engagement's Reviews 4R.
- `conversion-copy` — sharper polish for high-leverage quotes.
- `sop-helper` — edits to either SOP. `notion-helper` — ad hoc FU task pages.

## Quick Reference: Tools

| Need | Tool |
|---|---|
| Find a CRM page / Engagement | `notion-search` |
| Read a row | `notion-fetch` |
| Create a row | `notion-create-pages` (both statuses explicit) |
| Update properties / body | `notion-update-page` |
| Query for the sweep | `notion-query-data-sources` (`mode: "view"`) |
| Read a form sheet | Drive `read_file_content` |
| Check replies / intro threads | Gmail `search_threads`, then `get_thread` (always — the search message list truncates) |

