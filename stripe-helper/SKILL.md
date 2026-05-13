---
name: stripe-helper
description: Handle Shaw's Stripe operations — creating and sending invoices, generating payment links, and pulling reporting data (balance, recent payments, customer history). Use this skill whenever Shaw mentions Stripe, invoicing a client, billing someone, sending a payment link, checking what someone has paid, or any reference to charges, refunds, or revenue activity. Triggers include "send X an invoice", "bill X for Y", "create a Stripe invoice", "make a payment link", "how much did X pay", "what's my Stripe balance", "did X's invoice go through", "void this invoice", "refund X", "check my Stripe", or any casual phrasing like "throw an invoice on the books for X". Even when Shaw doesn't say "Stripe" explicitly — anything about billing a client, generating a paid link, or looking up payment history — this skill should fire.
---

# Stripe Helper

Workflow skill for Shaw's Stripe account. Covers three things:
1. Creating and sending invoices for 1:1 offers and one-off engagements
2. Generating payment links
3. Pulling reporting data (balance, invoice status, customer history)

## Heads up: this is the LIVE Stripe account

Shaw's Stripe MCP is connected to his live account, not test mode. Real money moves. Always confirm with Shaw before finalizing anything that touches a real customer.

## Shaw's offers (default product/price IDs)

These are the canonical paid offers. When Shaw says "1-on-1 Claude workshop" or similar, default to the matching price below — confirm the choice if there's any ambiguity.

| Offer | Product ID | Price ID | Amount |
|---|---|---|---|
| 1:1 Claude Workshop (90-min) | `prod_[id]` | `price_[id]` | $1,500 |
| 1:1 AI Coaching (90 min) | `prod_[id]` | `price_[id]` | $1,500 |
| 1:1 AI Coaching (1 hr) | `prod_[id]` | `price_[id]` | $1,500 |
| 1:1 AI Coaching (1 hr, discounted) | `prod_[id]` | `price_[id]` | $1,000 |

For custom engagements (training contracts, retainers, etc.), Shaw's pattern is one-off invoices in the $1,500–$7,500 range with a custom line item — not always tied to a product. Ask him for the amount and a short description.

## Sending an invoice (the standard workflow)

Stripe doesn't have a single "send invoice" action — it's four steps. Follow this order:

1. **Find or create the customer.** Always call `list_customers` with the email first to avoid duplicates. Only call `create_customer` if no match.
2. **Create a draft invoice** with `create_invoice` (sets `customer` and `days_until_due`).
3. **Attach a line item** with `create_invoice_item` (using either a `price` ID for a standard offer, or a custom amount/description for bespoke work).
4. **Pause and confirm with Shaw.** Show the summary — customer, line item, amount, due date — and wait for explicit OK before finalizing. This is the rule, even when the request feels obvious.
5. **Finalize** with `finalize_invoice`. This locks the invoice and triggers Stripe to email the hosted invoice link to the customer.

The `finalize_invoice` response includes a hosted invoice URL (`url` field). Always include this in the reply to Shaw, plus the dashboard URL (see URL patterns below).

### Computing days_until_due

Shaw often says "due May 10" or "due next Friday". Convert to a day count from today using `date` in bash if needed. Stripe's API takes an integer count, not a date.

## Critical: finalized invoices can't be edited

Once an invoice is finalized (status `open`), the API blocks updates to `due_date`, line items, and most other fields — this is a Stripe constraint, not an MCP limitation. The Stripe MCP also does NOT expose `void_invoice` or an invoice update operation, so neither can be done from this skill.

When Shaw asks to change a finalized invoice:

1. Tell him the limitation up front.
2. Direct him to void the existing one in the dashboard (steps below).
3. Offer to create a fresh invoice with the corrected details.

### How to void in the Stripe dashboard (give Shaw these exact steps)

1. Open the invoice in the dashboard
2. Click the **three dots** (top right of the invoice page)
3. Select **Change invoice status**
4. Choose **Mark invoice as void**
5. Click **Update status**

## Payment links

For "create a Stripe link for X" — use `create_payment_link` with a price ID. Payment links are shareable and don't require a customer record. Good for: course/intensive checkouts, lead magnets with a paid tier, one-off offers Shaw wants to drop into a DM or post.

Confirm with Shaw before creating: which price, any quantity limits, where he plans to share it. Return the payment link URL when done.

## Reporting and lookups

When Shaw asks "did X pay", "how much is in my account", "what's my Stripe doing", reach for:

- **`retrieve_balance`** — current available + pending balance
- **`list_invoices`** — recent invoices with status (`paid`, `open`, `void`, `draft`, `uncollectible`). Filter by `customer` ID if Shaw names a specific person.
- **`list_payment_intents`** — actual successful payments (`status: succeeded`) vs. canceled attempts. Useful for verifying a charge actually went through.
- **`list_customers`** with `email` filter — quick lookup for a specific person

Shaw's account has no subscriptions and no coupons — everything is one-off invoicing. Don't waste time checking those unless he specifically asks.

## URL patterns

These are stable Stripe dashboard patterns — useful for giving Shaw a clickable link to manage things.

- Invoice (dashboard): `https://dashboard.stripe.com/invoices/{invoice_id}`
- Customer (dashboard): `https://dashboard.stripe.com/customers/{customer_id}`
- Payment intent (dashboard): `https://dashboard.stripe.com/payments/{payment_intent_id}`
- Hosted invoice (customer-facing): returned in the `url` field on `finalize_invoice`

When Shaw asks for "the link to that invoice", he usually means the dashboard URL (so he can manage it), not the hosted one (which is for the customer to pay). If unclear, share both.

## Working pattern reminders

- **Confirm before finalizing.** Always pause after step 3 of the invoice flow.
- **Surface the live-mode caveat** when creating anything for a real customer — quick reminder, no need to belabor it.
- **Don't create duplicate customers.** Email lookup first, every time.
- **When something is blocked by API limits** (void, update finalized invoice, etc.), tell Shaw what the wall is and offer the dashboard workaround. Don't loop trying alternative API operations.
- **Default to including dashboard links** in any summary — Shaw moves between Claude and the dashboard frequently.
