# Workflow 4: Stripe Fill

**Triggers:**
- Engagement row has blank `Price`, `Paid Status`, or Stripe link in body
- "Look up Stripe for X" / "Pull invoice for E####" / "Fill in payment info for X"
- Run as a sub-step of **Workflow 1 (Create)** when an invoice is expected to exist already

**Goal:** Pull invoice ID, amount, and status from Stripe; fill in `Price`, `Paid Status`, and
the Stripe link in the engagement body. Handle proxy payers, voided/replaced invoices, and
missing customer records.

---

## Steps

### 1. Try direct email lookup

Use `list_customers` with the client's email (from their Nurture or Active Leads row).

```
list_customers(email="<client_email>")
```

If a customer is returned, run `list_invoices(customer=<cus_id>)` and skip to step 4.

### 2. If no match, try fuzzy customer search

The client may have paid under a different email (work vs. personal) or via a proxy payer.

Try in order:
- **Name search:** `search_stripe_resources(query='customers:name~"<First Last>"')`
- **Last name only:** `search_stripe_resources(query='customers:name~"<Last>"')`
- **First name only** if last name is uncommon
- **Company domain substring:** `search_stripe_resources(query='customers:email~"<domain>"')`
  e.g., `email~"<company-domain>"` finds anyone billed at that company

If a customer matches but the name/email looks like a different person (e.g., a procurement
contact at the client's company instead of the named client), that's likely the **proxy payer** — a
procurement contact at the client's company. Use that customer.

### 3. Handle voided/replaced invoices

When listing invoices, check the `status` field carefully:

- `paid` → use this invoice
- `open` → invoice exists, payment pending. Set `Paid Status = Unpaid` (or `Partial` if
  `amount_paid > 0`)
- `void` → invoice was cancelled. Don't assume no payment. Look for:
  - A second invoice on the same customer with the same amount and `paid` status (the
    replacement)
  - A note from Shaw explaining the void (often: client paid via their own Stripe account /
    vendor portal, so Shaw voided the duplicate)
- `draft` → not finalized yet; ignore

If the only invoice is voided and there's no obvious replacement, ask Shaw before assuming
"unpaid." Many of his clients pay via their company's vendor payment service which routes to a
different Stripe account.

### 4. Update the engagement row

**Properties to update:**

```json
{
  "Price": <amount in dollars, e.g., 7500>,
  "Paid Status": "Paid in Full" | "Unpaid" | "Partial" | "Refunded"
}
```

Stripe `amount_paid` and `amount_due` are in **cents**. Convert: `7500 USD = 750000 cents`.

**Body update — replace the Stripe link line:**

For a paid invoice:

```
old_str:
**Stripe link:** _paste invoice URL_

new_str:
**Stripe link:** [<invoice_id>](https://dashboard.stripe.com/invoices/<invoice_id>) — Paid in full M/D ($X). Billed to <customer_email>.
```

For an open (unpaid) invoice:

```
new_str:
**Stripe link:** [<invoice_id>](https://dashboard.stripe.com/invoices/<invoice_id>) — **Open** (unpaid). Billed to <customer_email>.
```

For a proxy-paid invoice (no record on Shaw's main Stripe):

```
new_str:
**Stripe link:** *Paid $X via <company>'s vendor payment service — didn't route through Shaw's main Stripe account.*
```

For a voided invoice with no clear replacement:

```
new_str:
**Stripe link:** [<invoice_id>](https://dashboard.stripe.com/invoices/<invoice_id>) — **VOID** (invoice for $X, voided — payment status unclear, ask Shaw).
```

### 5. Special case: Team workshops

For `1:1 Claude Workshops — Team` engagements, the invoice should equal `$1,500 × N attendees`
(no team discount currently). If the invoice amount doesn't match the expected count, flag it:

> [Client A]'s invoice was $[amount] = 5 × $1,500. ✓
> [Client B]'s invoice was $[amount] but I counted 5 attendees in the body — confirms 5 × $1,500.

If the amount and attendee count don't match, ask Shaw.

### 6. Confirm with Shaw

Reply with what you found and what you couldn't:

> Filled in [E0003](url) — $7,500, Paid in Full, billed to [email] (4/20).
>
> [E0001](url) — no Stripe record under any email or name search. Likely paid via [Company]'s
> vendor portal. Need you to confirm the price.

Always flag uncertainty rather than guessing.

---

## Common Proxy Payer Patterns

Document any new proxy patterns encountered to make future lookups faster:

- **[Company A]** ([Client Name]) — pays via internal portal, routes to a different Stripe account.
  The original invoice on Shaw's account gets voided.
- **[Company B]** ([Client Name]) — pays via internal vendor service, no Stripe record on Shaw's
  account at all.
- **[Company C]** ([Client Name]) — billed via [Procurement Contact] (procurement),
  `[email]`. Search by company domain.

When a new proxy pattern is discovered, suggest adding it to this list.
