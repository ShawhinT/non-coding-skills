# Follow-Up Rules & Drafting Guidance

Apply these rules during CRM review or whenever Shaw mentions a lead's status.

---

## How to read this file

The `Next Contact` field on Active Leads is the **primary structured signal** for when a lead
is due. Workflow 1 sorts on it directly — any lead with `Next Contact <= today` is up for
review. This file tells you what date to *set* on `Next Contact` in different situations.

Think of each section below as "default windows for setting `Next Contact`" — not as math to
re-derive each time a sync runs.

---

## Cadence defaults by situation

### Contact form & LinkedIn leads

For any inbound contact form lead (ABA Contact, ABB, etc.) or LinkedIn lead, set `Next Contact`
based on where they are in this cadence:

| Step | Set `Next Contact` to | Template |
|---|---|---|
| Initial reply sent | +2–3 days (→ FU #1 date) | — |
| FU #1 sent, no response | +7 days (→ FU #2 date) | Short direct question: *"Did you get a chance to look at this?"* |
| FU #2 sent, no response | Clear the field; mark `Lost` | One-liner, no greeting, no sign-off: *"Have you given up on this?"* |

**FU #2 formatting:** This is literally just the single line "Have you given up on this?" — no "Hey [Name],"
no sign-off, no "-Shaw". Just the question by itself. It's intentionally blunt and short.

**After FU #2 with no response:** Mark the lead as `Lost` and set `Next Contact` to the
re-engagement date (see below).

### B2B pipeline

| Situation | Set `Next Contact` to |
|---|---|
| Booking link sent or time proposed, awaiting confirmation | +2 days |
| Call booked | The call date |
| Outline/proposal sent (`Outline Sent`) | +2 days for first FU; extend if they've asked for time |
| Explicit future FU date agreed with the lead (e.g. "let's check in in April") | That date |

### Lost lead re-engagement

When marking a lead `Lost`, set `Next Contact` to the re-engagement date. **Default: +6 weeks.**
Extend when context suggests a longer natural window — treat this as a judgment call, not a
blanket rule.

Signals that warrant a longer window:
- Explicit timeline from the lead ("we're set through Q2", "revisit after fiscal year-end")
- They just bought a competing or adjacent solution — wait until it runs its course
- Organizational disruption (reorg, sabbatical, leadership change) that will take months to settle
- Budget cycle is known and near — align to it instead of picking an arbitrary week

Re-engagement tone is a low-pressure check-in, not a hard sell. Acknowledge time has passed and
ask if circumstances have changed. If no response to the re-engagement, leave them as Lost
permanently (clear `Next Contact` or set far in the future).

## Closed lead nurture

When a lead reaches `Closed` (deal won), move them to the Clients (Nurture) database using
**Workflow 5**. The Active Leads database is for pipeline leads only; closed leads graduate out.

**Client nurture cadence:**

| Rhythm | Details |
|---|---|
| Quarterly check-ins | Free, casual calls or emails every ~3 months, for clients in `Nurturing`. The `Next Check-in` field tracks when each is due. |
| Ad hoc touchpoints | When a client reaches out, or when Shaw has something relevant to share. Log these in Notes and update `Last Contact?`. |

**`Next Check-in` semantics by status:**

- **`Active`** — set to the date of the next scheduled training/session. Update it whenever the next session moves.
- **`Nurturing`** — set to a forward-looking outreach date, ~3 months out by default.
- **`Expansion`** — same as Nurturing; reset to ~3 months out if the opportunity doesn't close.
- **`Churned`** — leave alone or clear.

**Status transitions in the Clients table:**

- **Active → Nurturing** — when the current engagement wraps up. Reset Next Check-in from "next session" to a forward-looking outreach date ~3 months out.
- **Nurturing → Expansion** — when a check-in or ad hoc conversation surfaces a new buying opportunity.
- **Expansion → Nurturing** — if the expansion opportunity doesn't materialize. Reset Next Check-in.
- **Nurturing → Churned** — after 2+ check-ins with no response, or client explicitly disengages.

**Purpose of nurture check-ins:**
The goal isn't to sell — it's to stay close and hear their problems. What clients are struggling
with directly informs Shaw's marketing content and new offers. Expansion opportunities emerge
naturally from these conversations when the timing is right.

**Check-in timing buckets (used by Workflow 1's client sync):**

- **Overdue** — `Next Check-in` is in the past
- **Due soon** — `Next Check-in` is within the next 7 days
- **On track** — `Next Check-in` is more than 7 days away

Also flag any client whose `Last Contact?` is more than 4 months ago, regardless of
`Next Check-in` — this catches clients where a check-in may have been missed.

**Expansion signals to watch for during nurture review:**

- Client asking about new use cases, new teams, or new departments
- References to budget cycles, new hires, or organizational changes
- Positive sentiment about past work ("that workshop was great, we want more")

When expansion signals appear, flag them in the summary and recommend moving the client's
status to `Expansion` — don't auto-change the status without Shaw's confirmation.

**Check-in email tone:**

These are relationship-maintenance emails, not sales pitches. Casual, curious, genuinely
interested in what they're working on.

Good check-in openers:
- *"Hey [Name], been a few months — how's the [thing they were working on] going?"*
- *"Hey [Name], wanted to check in. Any new AI challenges on your plate?"*
- *"Hey [Name], hope things are going well. Anything I can help with?"*

After drafting, update the client's Notes and Last Contact? in the CRM, and set Next Check-in
~3 months out.

## When NOT to draft a follow-up

- `Next Contact` is still in the future (the lead isn't due yet)
- Status is `Closed` (lead has moved to nurture/expansion database)
- Status is `Lost` and re-engagement was already sent with no response (permanently done — `Next Contact` should be cleared)
- Lead responded recently and conversation is active — the ball is in Shaw's court but the timing isn't stale

---

## How to draft follow-ups

**Default behavior: create Gmail drafts directly.** Do not present draft options to Shaw for
review unless the situation is genuinely ambiguous (e.g., unclear whether to follow up at all,
or unclear tone for a sensitive deal). For routine follow-ups, just draft them in Gmail and
report what was drafted in the summary.

**LinkedIn-only leads:** Don't auto-create Gmail drafts — there's no email to draft to. Instead,
flag them in the summary under "Follow-ups due (via LinkedIn DM)" so Shaw knows to ping them on
LinkedIn. If Shaw explicitly asks for a draft message to a LinkedIn lead, write one for him to
copy-paste into a DM.

1. Read the full Gmail thread to understand tone and context
2. Draft a short, casual reply in the existing thread — match Shaw's voice (direct, friendly, low-pressure)
3. **Self-check before finalizing:** verify the last sentence is a question, not a statement.
   If it ends with "let me know," "happy to help," or any passive closer, rewrite it as a question.
4. Create the draft using `gmail_create_draft` with the `threadId` of the existing thread.
   For Gmail formatting details (HTML structure, emoji reaction handling), see the **email-writer** skill's Gmail Technical Notes.
5. Update the lead's CRM Notes to reflect the follow-up: e.g. `FU (3/18).`
6. Call it out clearly in the summary report under **"Follow-ups due"**

**Never create a replacement draft without deleting the old one first.** If a draft needs to be
redone (e.g., wrong formatting, wrong template), ask Shaw to delete the old draft before creating
a new one. Creating two drafts in the same thread causes a real problem: when the email is sent,
Gmail sees the unsent draft as a "duplicate" message in the thread and hides the actually-sent
email by default. The recipient gets it fine, but Shaw can't see it in his sent view without
expanding hidden messages — which looks broken and is confusing.

**Always end follow-ups with a question, not a statement.** Questions create a response obligation;
statements and commands ("let me know", "happy to help") are easy to ignore. Examples:
- Good: *"Did you get a chance to look at this?"*
- Good: *"Is this still something you're interested in?"*
- Bad: *"Let me know if you have any questions."*
- Bad: *"Happy to help if you need anything."*

---

## Tone guidance from observed examples

- Contact form FU #1: *"Did you get a chance to look at this?"*
- Contact form FU #2: *"Have you given up on this?"* (no greeting, no sign-off — just this one line)
- Scheduling: *"Would [day] at [time] work?"* or *"Is [tomorrow] a bad time?"*
- Casual re-engagement: *"Is [tomorrow] a bad time? Happy to work around your schedule if you think this is worth pursuing :)"*
- Never pushy; always leave the door open

---

## Lead source context for drafting

When drafting follow-ups or replies, adjust approach based on the lead's source:

- **ABB** (Bootcamp alums) — warm relationship; Shaw already knows them. Tone is peer-level,
  casual. They may be interested as a client, a partner, or just staying in touch — don't assume.
- **ABA Contact** (inbound contact form) — interested but cold; they reached out but have no
  prior relationship. Tone is friendly but slightly more structured. Follow the contact form
  cadence strictly.
- **YouTube** — they know Shaw's content but haven't worked with him. Warmer than cold
  outreach but still need to build trust. Reference shared context where possible.
- **LinkedIn** — often exploratory; may be looking for partnership, consulting, or just networking.
  Clarify intent early rather than assuming they want training. Follows the same cadence as
  contact form leads (see above).
- **Personal** — existing relationship. Match whatever tone the relationship has.
