# Offer Scopes

Canonical **deliverable shapes** per offer. Fill these into the **Program Scope** section of every
new engagement page body unless Shaw indicates a deviation.

Shapes are here because they're stable and because getting them wrong causes a recurring bug:
when a scope omits its closing deliverable, the daily sync mis-times the `Active → Delivered`
flip (see E009 below). Prices are deliberately **not** here — they change faster than this file
can track. For how to arrive at a price, see `pricing-principles.md`. Scope captures what was **promised at
sale** — what the client paid for. Actual delivery may differ; if it does materially, that
usually means a new engagement row, not a scope edit (see "Scope reflects what was sold" in
`SKILL.md` Key Principles).

---

## 1:1 Claude Workshop

**Deliverables:**
- 1 × 90-min 1:1 workshop
- 1 × 30-min Day-7 check-in

**Bonus:** Claude Skills Starter Pack

**Guarantee:** 5-Hour Guarantee — if by the 7-Day Check-In the skill built isn't on pace to save
5 hours of busy work per month (with both sessions attended and used on real work), full refund.

Source: [1:1 Claude Workshop one-pager](https://www.notion.so/[page-id]).

---

## Team / group 1:1 Claude Workshops

_Check the Engagements `Offer` multi-select for the exact current option name — it has been
`1:1 Claude Workshops (Group)` in practice._

**Deliverables (per N attendees):**
- N × 90-min individual 1:1 sessions (one per attendee)
- 1 × wrap-up call with AI champion / company contact (the payer or designated lead)

No per-attendee bonus or guarantee bundled at the current price point — confirm with Shaw before
adding one to a specific deal. The wrap-up call is the **closing deliverable**: the last
participant session going by does not finish the engagement, and omitting this bullet is what
made the sync repeatedly flag E009 as a status decision when it was really a scope gap.

---

## 30-Day Claude Intensive — current scope

**Deliverables:**
- 1:1 Skill Building — 4 × 90-min sessions
- EA Skill Building — 1 × 90-min session
- 30-day Roadmap — 1 × 60-min session

**Guarantees:**
- Full refund after the 1st session if it doesn't seem like a good fit
- If by the end the client hasn't saved at least 5 hr/wk of busy work, Shaw keeps working with
  them until they do

Source: [30-Day 1:1 Claude Intensive one-pager](https://www.notion.so/[page-id]).

**Prior format (pre-April 2026):** 2 × half-day in-person sessions. Pre-dates the
productized 30-Day Intensive — log under `Custom AI Training` if encountered in a backfill (see
[Client Name] E002).

---

## Custom AI Training / AI Advisory / Ad Hoc Consulting

Variable by deal. No canonical scope — ask Shaw and describe per engagement. Examples on record:
- [Person] / [Company] (E001): 1 × 60-min strategy call, no guarantees.
- [Client Name] / pre-April (E002): 2 × half-day in-person 1:1 AI Coaching sessions, no
  guarantees.
- [Company] (E012): 1 × 30-min working session, office-hour format, no check-in or guarantee.

**Short one-off sessions (office hours, working sessions) land here** until they're common enough
to earn their own multi-select option. They're a distinct format, not a trimmed-down workshop:
no Day-7 check-in, no guarantee, and the client is usually bringing a specific blocker rather
than building from scratch.

---

## Pattern for the Program Scope section

The body section follows this template:

```markdown
## Program Scope
**Deliverables:**
- <bullet per deliverable, with count × duration when relevant>

**Bonus:** <if any; omit the line entirely if none>

**Guarantee:** <if any, with specifics on what triggers it; omit if none>
```

Keep it terse — one line per deliverable, one line per guarantee. Don't paraphrase marketing
copy; capture what was sold in operationally clear language.
