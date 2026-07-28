# Pricing Principles

How to arrive at the `Price` on an engagement row. This file deliberately contains **no dollar
figures and no list of current offers** — both change faster than a skill file can track, and a
stale number is worse than no number because it reads as authoritative.

Companion to `offer-scopes.md` (deliverable shapes, which are stable).

---

## Where price actually comes from

In priority order:

1. **The agreement itself** — the email thread, proposal, or call where the number was named.
   This is the real source of truth and it wins over everything below. In practice this is where
   the price comes from nearly every time.
2. **Stripe** — the live product catalog (`GetProducts`) for list prices, and the actual invoice
   for what was billed. See `stripe-helper` and `workflow-4-stripe-fill.md`.
3. **Ask Shaw.**

If those disagree, surface the discrepancy rather than picking one. A deal priced off-catalog is
usually intentional (a shorter format, a bundled rate, a favor) and the reason belongs in the
body Notes.

**Leave `Price` blank rather than guessing.** A blank flags itself for follow-up; a wrong number
propagates silently into revenue reporting.

---

## Where the offer *names* come from

The `Offer` property is a multi-select, and **the data source schema is the source of truth for
its options** — fetch the Engagements data source and read them rather than working from a list
written down here. Hardcoded lists drift: this file previously named the team offer
`1:1 Claude Workshops — Team` while every actual row in the database used
`1:1 Claude Workshops (Group)`, and nothing caught it.

If a deal doesn't fit any existing option, that's a signal worth raising with Shaw before
inventing one — new offers show up as new SKUs in Stripe and new multi-select options, and both
should be created deliberately.

---

## Judgment rules that don't decay

These are the parts of pricing that survive a price change.

- **Team/group workshops price per head, not as a bundle.** The total should equal the per-seat
  rate × attendee count unless Shaw explicitly names a bundle rate. When reconciling an invoice,
  cross-check the total against the attendee count in the engagement body — a mismatch usually
  means a miscounted roster, not a discount.
- **Re-ups price independently of the prior engagement.** Don't assume a returning client gets
  the earlier rate or a loyalty discount unless Shaw said so in the close conversation.
- **Short formats are their own offer, not a prorated one.** A 30-min session isn't half a
  90-min workshop with half the scope; it's a distinct thing sold at a distinct price. Treat it
  as a separate SKU rather than deriving it arithmetically.
- **Free engagements** — `Price = 0`, `Paid Status = Paid in Full`, and a body note explaining
  why it was free. Some 1:1 workshops are intentionally free and correctly have no engagement
  row at all (see `workflow-5-sync.md`); a free session is a decision, not an omission.
- **Friend/family or courtesy rate** — record the actual amount paid, never the standard rate.
  Note the context in the body so revenue reporting isn't quietly distorted.
- **Refunds** — keep `Price` as the original contract value and track the refund amount in
  Notes. See `workflow-2-status.md`.
