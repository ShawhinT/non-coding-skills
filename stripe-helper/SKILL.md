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

## Shaw's offers — read them live, don't trust a list

**Start every invoice by pulling the live catalog** (`GetProducts` with `active: true`, one call,
returns everything). Do not work from product/price IDs written down in this skill.

This section used to hold a table of four products and prices. It went stale: by the time it was
next used, the account had products the table didn't list, one of the products it *did* list had
been archived, and the model had to do the lookup anyway — so the table's only effect was to
supply a wrong prior. Offers change often enough that any cached copy is wrong within weeks.

What's stable and worth knowing:

- Everything is **one-off invoicing**. No subscriptions, no coupons — don't check them unless
  Shaw asks.
- Products are **services** (`type: service`, tax code `txcd_20030000`) with a single one-time
  price attached.
- Product names encode the format and duration, e.g. `1:1 Claude Workshop (90-min)`,
  `Office Hour (30 min)`. Match on that when picking a price.
- Older products linger as `active` after Shaw stops selling them. Presence in the catalog is not
  evidence an offer is current — if the name doesn't match what the deal actually was, ask.

### When the amount has no matching price

If the total doesn't equal a catalog price × a whole-number quantity, **stop and ask Shaw** before
improvising. This guardrail is the reason the price table wasn't needed: checked against live
Stripe, it catches both a mistyped amount and a genuinely new offer, and it distinguishes them by
asking rather than guessing.

The two resolutions look different:

- **A new offer** (Shaw sold a format that doesn't exist yet) — create the product and price
  deliberately, named for its format and duration. Confirm with Shaw first; a new SKU is
  permanent and lands in the live catalog. Then tell the `engagements` skill it needs a matching
  `Offer` multi-select option.
- **A one-off deviation** (courtesy rate, bundled favor) — don't mint a price for it. Never
  create a price purely to make a total come out right, e.g. a $6,000 price when the deal is
  4 × the $1,500 workshop. Shaw builds that line item in the dashboard.

## Sending an invoice (the standard workflow)

Stripe doesn't have a single "send invoice" action — follow this order:

0. **Ground the amount in the agreement, not a summary.** Before touching Stripe, confirm what was actually agreed from the source — the email thread with the client, not CRM notes (notes lag and compress; a restructured deal can change the total). Watch for a price the client never restated in writing: if they replied "let's do it" to a two-option email, the number is implied, not confirmed, and the invoice line is what pins it down. Then reconcile against the live catalog per the section above.
1. **Find or create the customer.** Search by email first to avoid duplicates (`search_stripe_resources` with `customers:email~"domain.com"`). Only call `create_customer` if no match.
2. **Create a draft invoice** with `create_invoice` (sets `customer` and `days_until_due`).
3. **Attach ONE line item** with `create_invoice_item` using a price ID from the live catalog you pulled above. The MCP can't set quantity, so for multi-unit invoices create a single line item and tell Shaw what quantity to set in the dashboard — do NOT create N duplicate line items, and never create a new price to fake a total (e.g. don't mint a $6,000 price when the deal is 4 × the $1,500 workshop price).
4. **Remind Shaw about ACH and the due date.** The MCP can't set payment methods, and `days_until_due` is fixed at creation on a draft that can't be edited afterward. Shaw's policy is **due ~7 days before the session** — compute from the session date rather than defaulting to net-14, and if the session is too near for that, say so instead of silently picking a longer term. If the client has paid by bank transfer before (most companies do), remind him to check **ACH Direct Debit** under Payment options before finalizing.
5. **Pause and confirm with Shaw.** Show the summary — customer, line item, quantity to set, amount, due date — and wait for explicit OK before finalizing. This is the rule, even when the request feels obvious.
6. **Finalize** with `finalize_invoice` after Shaw has made his dashboard tweaks (quantity, ACH). This locks the invoice and triggers Stripe to email the hosted invoice link to the customer.

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

### Draft invoices are nearly as locked (MCP walls)

Discovered limits of the Stripe MCP, even on drafts: no invoice update (due date, payment methods), no invoice or invoice-item deletion, and `create_invoice_item` accepts only a price ID — no quantity, no custom amount, no description. `stripe_api_execute` doesn't expose invoiceitems operations either. Practical upshot: get the draft right at creation; anything wrong on a draft is fixed or deleted by Shaw in the dashboard (drafts delete cleanly from the ⋯ menu). If you create a price by mistake, deactivate it with `PostPricesPrice` (`active: false`).

## Payment links

For "create a Stripe link for X" — use `create_payment_link` with a price ID. Payment links are shareable and don't require a customer record. Good for: course/intensive checkouts, lead magnets with a paid tier, one-off offers Shaw wants to drop into a DM or post.

Confirm with Shaw before creating: which price, any quantity limits, where he plans to share it. Return the payment link URL when done.

## Reporting and lookups

When Shaw asks "did X pay", "how much is in my account", "what's my Stripe doing", reach for:

- **`retrieve_balance`** — current available + pending balance
- **`GetInvoices`** via `stripe_api_execute` — recent invoices with status (`paid`, `open`, `void`, `draft`, `uncollectible`) and full line items. Filter with the `customer` param if Shaw names a specific person. (There is no `list_invoices` tool.)
- **`list_payment_intents`** — actual successful payments (`status: succeeded`) vs. canceled attempts. Useful for verifying a charge actually went through.
- **`search_stripe_resources`** with `customers:email~"..."` — quick lookup for a specific person (there is no `list_customers` tool)

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
