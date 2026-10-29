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

### Timing: each window counts from the previous send

- **FU #1: +2–3 days** after the initial send
- **FU #2: +7 days** after FU #1
- **Then close** — the register of the close depends on the relationship (see below)

+7 is the gap *between* the first and second nudge, never the wait for the first. Every section
below inherits these windows; where one gives a different number, it is describing the close or
how far out to park afterward, not a different first-FU window.

Cadence follows the thread state; register follows the relationship. A message awaiting a reply
gets these same windows whoever the recipient is: a Friends row, family included, inherits the
+2–3 / +7 clock the moment Shaw has an open question out to them. What the relationship changes is
the message and the close, not the timing. The "natural rhythm" language elsewhere describes how
far out to park a row when nothing is pending, never how long to wait on an unanswered message.

Sending a rung moves the dates and nothing else: `Last Contact?` to the send date, `Next Contact`
to the next window. It never earns a Notes line — Notes log *that* something moved (they
replied, asked, agreed, declined; the status changed), and a nudge is neither. Log the move, not
its content: `Replied, offered call (3/13)`, never a summary of what the reply said — that goes in
the page body's `## Context` (see SKILL.md → "Notes Format").

A reply ends the ladder, so the dates have to be reset from it rather than from the last rung.
If Shaw's response to it carries a new ask — a question, times offered, a link to act on — that
is fresh unanswered outbound and the ladder restarts at FU #1 (+2–3 days). A row still parked at
the window set for the old silence is how a live thread goes quiet for a week.

### Contact form & LinkedIn leads

For any inbound contact form lead (ABA Contact, ABB, etc.) or LinkedIn lead, set `Next Contact`
based on where they are in this cadence:

| After this send | Set `Next Contact` to | What the next send says |
|---|---|---|
| Initial reply | +2–3 days → FU #1 | — |
| FU #1 | +7 days → FU #2 | A short nudge written from the unanswered message — email-helper's `references/nudges.md` owns the wording |
| FU #2 | Clear the field; mark `Lost` | The closing nudge — which line depends on whether they opted in (below) |

**FU #2 wording:** It depends on whether they ever expressed interest. If they did — wrote in, asked
for a proposal, said yes to a call — it is literally the single line "Have you given up on this?": no
"Hey [Name]," no sign-off, no "-Shaw". Intentionally blunt and short. If they never opted in — Shaw
opened the thread with a check-in, a re-engagement, or an offer they didn't ask for — it's the softer
"Seems like the timing is bad right now." close instead. If someone else opened the thread (an
intro Shaw replied to), it's the no-oriented "Is it a bad time for this?" instead. All three are
spelled out in email-helper's `references/nudges.md` → "The closing nudge".

**After FU #2 with no response:** Mark the lead as `Lost` and set `Next Contact` to the
re-engagement date (see below).

### The two tables compose — one is a clock, the other is a ladder

These tables answer different questions, so a lead is rarely governed by just one of them.

The **B2B pipeline** table below is a *clock*: it says how far out to set `Next Contact` after a
pipeline event — a call gets booked, a proposal goes out. It names the first FU after a proposal
and stops there.

The **contact form & LinkedIn** table above is a *ladder*: it says how many follow-ups an
unanswered thread gets and what each rung says. That ladder governs any outbound that has gone
quiet, whatever put it there. A proposal that no one replied to is an unanswered thread, so it
climbs the same rungs — FU #1, then the bare "Have you given up on this?" one-liner, then `Lost`
with a re-engagement date.

So for a lead who booked through Calendly and now has a proposal sitting unanswered, read the
clock for *when* and the ladder for *what to say*. Reaching for only the pipeline table leaves you
with no template past the first FU, which is an invitation to improvise a nudge — and the
improvised version is almost always softer than the rung the lead has actually earned.

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

- **`Active`** — set to the next planned touchpoint with this person, or leave blank when
  none is planned.
- **`Nurturing`** — set to a forward-looking outreach date, ~3 months out by default.
- **`Expansion`** — same as Nurturing; reset to ~3 months out if the opportunity doesn't close.
- **`Churned`** — leave alone or clear.

Each person in a commercial conversation has their own row and their own dates; session
participants' reviews and referrals are tracked on their Reviews/Referrals rows. See SKILL.md →
"Companies, people, and who gets a CRM row".

**Status transitions in the Clients table:**

- **Active → Nurturing** — when the current engagement wraps up. Set `Next Contact` to a forward-looking outreach date ~3 months out.
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

Set `Next Contact` on an escalating ladder between reconnect *attempts* — ~6wk → 3mo → 6mo → 12mo
— so the next one auto-surfaces in the sync. That interval governs the gap between attempts, each of
which is a fresh thread; it doesn't replace the follow-ups *within* one. Run the FUs first, then
lengthen. No response never ends the relationship, it just widens the next gap. (Distinct from
"Lost lead re-engagement" above, which is for unconverted *leads*, not past *clients*.)

**Expansion signals to watch for during nurture review:**

- Client asking about new use cases, new teams, or new departments
- References to budget cycles, new hires, or organizational changes
- Positive sentiment about past work ("that workshop was great, we want more")

When expansion signals appear, flag them in the summary and recommend moving the client's
status to `Expansion` — don't auto-change the status without Shaw's confirmation.

After a check-in is sent, update the client's `Last Contact?`. What `Next Contact` becomes depends
on whether the loop closed, not on whether the email went out or a reply came back.

**The park is earned by the loop, not the thread.** A touch goes out to get something done: a call
held, a question answered, a wrap-up delivered. `Next Contact` goes ~3 months out only once that
thing is done or they've declined it. Until then the row stays on a short clock:

- **No reply yet** — this is unanswered outbound, so it climbs the one ladder above: FU #1 at +2–3
  days, FU #2 at +7 after that.
- **They said yes but not yet** (traveling, slammed until X) — the date they named, or about a
  week when they named none. A deferral is an acceptance still waiting on a time.
- **Shaw's reply carried a new ask** (times offered, a link sent) — that is unanswered outbound
  again, and the ladder restarts from it.
- **The ladder ran out in silence** — park only when nothing is owed. If the engagement still owes
  a step (a wrap-up call, a results check-in), silence ends the thread, not the obligation. Keep a
  near date and surface it as a decision.

Keep both rungs in the register of the check-in itself — warm, one line, low-friction. The lead
ladder's blunt "Have you given up on this?" is built for a lead who expressed interest and doesn't
transfer to a past client; the closing rung here is the "Seems like the timing is bad right now."
line.

A check-in is an ask, and an unanswered ask isn't a completed touchpoint. Parking one a quarter on
send is worth guarding against specifically, because it looks like a healthy cadence from outside:
the record drops out of the sync's `Next Contact <= today` filter and the `Last Contact?` >4-month
flag stays quiet, so the silence surfaces a quarter late or not at all.

A routine check-in doesn't need its own Notes line — the dates carry it; add one only if the
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
