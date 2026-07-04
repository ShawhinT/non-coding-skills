# Follow-Up Cadence Rules

This file governs CRM-specific cadence: *who* needs a follow-up, *when* they're due, and *what*
the message should say at each step. For email drafting mechanics — voice, threading, draft
management — defer to the **email-helper** skill.

---

## How to read this file

The `Next Contact` field is the **primary structured signal** for when a lead or client is due.
Workflow 1 sorts on it directly — any record with `Next Contact <= today` is up for review.
This file tells you what date to *set* on `Next Contact` in different situations, and what
specific message to send at each cadence step.

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

### Disqualified leads

Some inbound leads aren't a fit at all — wrong audience, wrong ask, low-quality contact form.
Use the `Disqualified` Status instead of `Lost` for these. Leave `Next Contact` blank; there's
no re-engagement cadence. If you also want them to show up in a "Lost" view for CRM tidiness,
it's fine to dual-tag with `Lost` — Workflow 1 filters on `Next Contact <= today`, so a blank
field keeps them out of the sync regardless of the Lost tag.

Use `Lost` for leads who didn't convert *this round* but might later. Use `Disqualified` for
leads you'd never want to work with in the first place.

## Closed lead nurture

When a lead reaches `Closed` (deal won), move them to the Clients (Nurture) database using
**Workflow 5**. The Active Leads database is for pipeline leads only; closed leads graduate out.

**Client nurture cadence:**

| Rhythm | Details |
|---|---|
| Quarterly check-ins | Free, casual calls or emails every ~3 months, for clients in `Nurturing`. `Next Contact` tracks when each is due. |
| Ad hoc touchpoints | When a client reaches out, or when Shaw has something relevant to share. Update `Last Contact?` (and `Next Contact` if it shifts); add a Notes line only if the touchpoint surfaces something relationship-level. |

**`Next Contact` semantics by client status:**

- **`Active`** — set to the date of the next scheduled session. The session also has its own
  page in ABA Trainings, linked from the CRM page body — that's how the touchpoint is legible
  as a session rather than a message.
- **`Nurturing`** — set to a forward-looking outreach date, ~3 months out by default.
- **`Expansion`** — same as Nurturing; reset to ~3 months out if the opportunity doesn't close.
- **`Churned`** — leave alone or clear.

For accounts that span multiple people, only the **point person** carries `Last Contact?` and
`Next Contact` — teammate sessions and replies don't move these dates (they're captured by their
linked session pages). See SKILL.md → "Point-person anchoring (multi-person accounts)".

**Status transitions in the Clients table:**

- **Active → Nurturing** — when the current engagement wraps up. Reset `Next Contact` from "next session" to a forward-looking outreach date ~3 months out.
- **Nurturing → Expansion** — when a check-in or ad hoc conversation surfaces a new buying opportunity.
- **Expansion → Nurturing** — if the expansion opportunity doesn't materialize. Reset `Next Contact`.
- **Nurturing → Churned** — after 2+ check-ins with no response, or client explicitly disengages.

**Purpose of nurture check-ins:**
The goal isn't to sell — it's to stay close and hear their problems. What clients are struggling
with directly informs Shaw's marketing content and new offers. Expansion opportunities emerge
naturally from these conversations when the timing is right.

Also flag any client whose `Last Contact?` is more than 4 months ago, regardless of
`Next Contact` — this catches clients where a check-in may have been missed.

**Long-gap reconnect (lapsed past clients):**
When a past client (`Nurturing` or `Churned`, engagement closed) comes due with `Last Contact?`
~6-12 weeks back or more, treat it as a re-warm from cold rather than a continuation of an active
rhythm — the gap itself shapes the touch. This is the play the ">4 months ago" flag above should
trigger. Keep the cadence here; the message lives in the **Check-in Call (Client Nurture)** SOP
("Checking in" outreach) and is drafted via email-helper — anchor on one specific detail from the
last real conversation, lead with genuine curiosity, no pitch, no calendar ask.

Set `Next Contact` on an escalating ladder after each reconnect — ~6wk → 3mo → 6mo → 12mo — so the
next one auto-surfaces in the sync. No response just lengthens the next interval; it doesn't end
the relationship. (Distinct from "Lost lead re-engagement" above, which is for unconverted *leads*,
not past *clients*.)

**Expansion signals to watch for during nurture review:**

- Client asking about new use cases, new teams, or new departments
- References to budget cycles, new hires, or organizational changes
- Positive sentiment about past work ("that workshop was great, we want more")

When expansion signals appear, flag them in the summary and recommend moving the client's
status to `Expansion` — don't auto-change the status without Shaw's confirmation.

After a check-in is sent, update the client's `Last Contact?` and set `Next Contact` ~3 months
out. A routine check-in doesn't need its own Notes line — the dates carry it; add one only if the
check-in surfaces something relationship-level (an expansion signal, a status change). See
SKILL.md → "Client Notes Format".

## When NOT to draft a follow-up

- `Next Contact` is still in the future (the lead isn't due yet)
- Status is `Closed` (lead has moved to nurture/expansion database)
- Status is `Lost` and re-engagement was already sent with no response (permanently done — `Next Contact` should be cleared)
- Lead responded recently and conversation is active — the ball is in Shaw's court but the timing isn't stale

**LinkedIn-only leads:** Don't auto-create email drafts — there's no email to draft to. Flag
them in the summary under "Follow-ups due (via LinkedIn DM)" so Shaw knows to ping them on
LinkedIn.

For *how* to draft and send the follow-up email itself once you've decided to send one — defer
to the **email-helper** skill.

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
