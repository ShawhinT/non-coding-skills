# Offer Pricing

Canonical offer names + default prices for the Engagements DB. Use these as starting values when
creating new engagement rows; verify against Stripe and Shaw's specifics for the actual deal.

| Offer (canonical) | Default Price | Source / Notes |
|---|---|---|
| 1:1 Claude Workshop | $1,500 | Single 90-min session + 30-min check-in. Per the [1:1 Claude Workshop one-pager](https://www.notion.so/[page-id]). Verified against past client engagements ($1,500). |
| 1:1 Claude Workshops — Team | $1,500 × N attendees | One payer, multiple attendees, single invoice. **No team discount currently** — verified against past team engagements ($[amount] = 5 × $1,500). |
| 30-Day Claude Intensive | $6,000 | Per the [30-Day 1:1 Claude Intensive one-pager](https://www.notion.so/[page-id]). Verified against past client engagement ($6,000). |
| Custom AI Training | TBD per scope | Group trainings, talks, keynotes for external companies. Pricing varies by audience size, scope, and prep required. Always confirm with Shaw. |
| AI Advisory | TBD per retainer | Ongoing retainer engagement. Pricing depends on cadence and scope. Always confirm with Shaw. |
| Ad Hoc Consulting | TBD per session | One-off strategy or advisory sessions. Past rate: $1,000 for 1hr session. Rate varies — always confirm with Shaw. |

---

## Pricing Principles

- **Offers with fixed prices** (1:1 Workshop, Intensive) — fill in the default and proceed
  unless Shaw indicates a different number
- **Offers with variable prices** (Custom Training, Advisory, Ad Hoc) — leave blank and ask Shaw
  for the dollar amount before completing the row
- **Team workshops** — multiply $1,500 × headcount unless Shaw specifies a bundle rate. Cross-check
  the invoice amount against the attendee count in the engagement body when running Stripe Fill
- **Re-ups** — the re-up offer's price is independent of the prior engagement. Don't assume a
  discount unless Shaw explicitly mentioned one in the close conversation

---

## Pricing Changes

If Shaw raises a price (e.g., next cohort of Intensive moves from $6,000 → $7,500), update this
file in the same pass. The default should always reflect Shaw's current pricing for the current
cohort/round.

When a price changes, also note it in the row of any in-flight engagements that haven't been
invoiced yet (rare, but possible if Shaw closed at one price and is invoicing later at a new
price).

---

## Discounts & Special Cases

- **Free engagements** — set `Price = 0` and `Paid Status = Paid in Full`. Add a body note
  explaining why it was free.
- **Friend/family rate** — set the actual price paid (don't fudge to the standard rate). Note the
  context in the body.
- **Refunds** — see Workflow 2 (Status Transitions) → Refunded section. Track the refund amount
  in the Notes; keep `Price` as the original contract value.
