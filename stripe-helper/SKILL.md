---
name: stripe-helper
description: Handle Shaw's Stripe operations — creating and sending invoices, generating payment links, and pulling reporting data (balance, recent payments, customer history). Use this skill whenever Shaw mentions Stripe, invoicing a client, billing someone, sending a payment link, checking what someone has paid, or any reference to charges, refunds, or revenue activity. Triggers include "send X an invoice", "bill X for Y", "create a Stripe invoice", "make a payment link", "how much did X pay", "what's my Stripe balance", "did X's invoice go through", "void this invoice", "refund X", "check my Stripe", or any casual phrasing like "throw an invoice on the books for X". Even when Shaw doesn't say "Stripe" explicitly — anything about billing a client, generating a paid link, or looking up payment history — this skill should fire.
---

# Stripe Helper

Workflow skill for Shaw's Stripe account. Covers four things:
1. Creating and sending invoices for 1:1 offers and one-off engagements
2. Billing a multi-month engagement as an installment plan
3. Generating payment links
4. Pulling reporting data (balance, invoice status, customer history)

## Heads up: this is the LIVE Stripe account

Shaw's Stripe MCP is connected to his live account, not test mode. Real money moves. Always confirm with Shaw before finalizing anything that touches a real customer.

## Confirm what only Shaw knows — don't infer it

Two facts vary per deal and can't be reasoned out from history. Getting either wrong is expensive
to undo, because a finalized invoice can only be voided and reissued.

- **Who gets billed.** The payer does not follow from who was billed last, who the champion is, or
  who approves spend. A company with several contacts routes invoices differently deal to deal. Ask.
  (One deal at [Company] went to [Person] every time, then the next one the VP of Ops asked for it
  directly — a "bill whoever approves spend" heuristic would have looked right and still been a
  guess.) Once Shaw names the payer, search that person's email to reuse their existing customer
  record rather than creating a duplicate.
- **Who else should see it.** CC recipients are dashboard-only — the API can't set them. If a
  second stakeholder owns cost or governance, tell Shaw to add them before the invoice is
  finalized: Customers → the payer → **Edit** in the Details pane → uncheck "Same as account
  email" → *Add more recipients*.

The general shape: when a detail is deal-specific, cheap to ask about, and costly to get wrong,
ask rather than deducing it from precedent.

## What this connector can actually write

**The MCP's write surface is much narrower than the Stripe API.** "Stripe supports X" is not
evidence that you can do X here. Before promising Shaw an outcome that depends on a write, confirm
the operation exists with `stripe_api_details` — a missing operation returns a plain "not
available" error, so the check is one cheap call. Skipping it is how a plan gets built on an
operation that was never there, and the correction lands after Shaw has already agreed to it.

Observed as of this writing — treat as a starting map to re-verify, not a contract:

| Available | Absent |
|---|---|
| `PostPrices`, `PostPricesPrice` | `PostCheckoutSessions` (and all Checkout Session writes) |
| `PostPaymentLinks`, `PostPaymentLinksPaymentLink` | `PostSubscriptions`, `PostSubscriptionsSubscription` |
| `PostInvoices`, `PostInvoiceitems` | subscription schedules (any operation) |
| `PostInvoicesInvoiceFinalize` | `PostInvoicesInvoice` (invoice update — even on a draft) |
| `GetCheckoutSessions` (read only) | `DeleteInvoicesInvoice` (invoice delete) |
| | `PostInvoiceitemsInvoiceitem` (line item update) |
| | `DeleteInvoiceitemsInvoiceitem` (line item delete) |
| | `PostInvoicesInvoiceLines`, `PostInvoicesInvoiceLinesLineItemId` |

`stripe_api_search` is not a reliable way to discover what's available — it requires `intent` and
`resource` arguments and still returns empty for these lookups. Probe candidate operation IDs with
`stripe_api_details` instead; that's what mapped the invoice-item wall above.

**The practical consequence: anything subscription-shaped is a dashboard job.** Creating a
subscription, capping one at N cycles, setting `cancel_at`, or generating a Checkout Session all
have to happen in the Stripe UI. Say so early rather than designing an API plan around them.

## Shaw's offers — read them live, don't trust a list

**Start every invoice by pulling the live catalog** (`GetProducts` with `active: true`, one call,
returns everything). Do not work from product/price IDs written down in this skill.

This section used to hold a table of four products and prices. It went stale: by the time it was
next used, the account had products the table didn't list, one of the products it *did* list had
been archived, and the model had to do the lookup anyway — so the table's only effect was to
supply a wrong prior. Offers change often enough that any cached copy is wrong within weeks.

What's stable and worth knowing:

- Products are **services** (`type: service`, tax code `txcd_20030000`), usually with a single
  one-time price attached.
- Product names encode the format and duration, e.g. `1:1 Claude Workshop (90-min)`,
  `Office Hour (30 min)`. Match on that when picking a price.
- Older products linger as `active` after Shaw stops selling them. Presence in the catalog is not
  evidence an offer is current — if the name doesn't match what the deal actually was, ask.

**Read billing *mode* live too, not just prices.** This section once asserted "everything is
one-off invoicing, no subscriptions, no coupons — don't check them unless Shaw asks." That aged the
same way the price table did: Shaw added a recurring product and a percentage coupon in the middle
of a working session, and the stale claim caused a flat "a subscription can't do that" answer to a
question where the real answer was "it can, but not through this connector." A recurring price or a
coupon may exist by the time you read this. Pull the catalog and check rather than asserting what
the account does and doesn't have.

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
2. **Assemble the full spec and confirm it with Shaw — before creating anything.** See
   "Creation is the commit point" below for why this sits here rather than before finalize.
   Show him the exact strings that will render on the client's invoice: line item text, memo
   text, quantity, amount, due date, payment methods. Wait for explicit OK. This is the rule
   even when the request feels obvious.
3. **Create the draft invoice** with `PostInvoices`, setting everything at once — `customer`,
   `days_until_due` or `due_date`, `description` (the memo), and
   `payment_settings.payment_method_types`. None of these can be changed afterward.
4. **Attach the line item** with `PostInvoiceitems`. Pass a catalog price as
   `pricing: {price: "price_..."}` — a bare `price` argument is rejected ("unknown parameter:
   price. Did you mean pricing?"). It also accepts `quantity`, `description`, `amount`,
   `period`, `discounts`, and inline `price_data`; use `price_data` (with `product` set) when
   the amount is a genuine one-off, so revenue still rolls up to the right product. Never
   create a standing catalog price to fake a total — e.g. don't mint a $6,000 price when the
   deal is 4 × the $1,500 workshop; that's `quantity: 4`.
   - **Line item = what they bought. Memo = what's included.** Keep the line item to the offer
     name as it appears in the catalog (`1:1 Claude Workshop`) and put scope detail in the
     invoice-level `description` (the "Memo"). The line item renders in a narrow column and a
     long string wraps badly; the memo has room to breathe. So: memo carries participant
     counts, session structure, delivery format, coverage period. It should not restate
     discount math or installment arithmetic — that belongs in the proposal, not the bill.
   - Set `period` on multi-month work so revenue lands in the right month.
5. **Verify the built invoice** with `GetInvoicesInvoice` before showing Shaw the link — confirm
   the total, that there's exactly one line item (a stray pending invoice item silently attaches
   itself and inflates the bill), and that `payment_method_types` came through.
6. **Finalize** with `PostInvoicesInvoiceFinalize` once Shaw says go. This locks the invoice and
   triggers Stripe to email the hosted invoice link to the customer.

The `finalize_invoice` response includes a hosted invoice URL (`url` field). Always include this in the reply to Shaw, plus the dashboard URL (see URL patterns below).

### Payment methods

**Default every invoice to `["us_bank_account", "card", "link"]`, in that order.** ACH first is
real money on a five-figure engagement — card runs ~2.9% + 30¢ (~$520 on $18,000) against ACH
capped at $5 — and ordering nudges bank transfer without blocking anything.

Trim the rest of the account's default list (Klarna, Cashapp): consumer BNPL options read oddly
on a B2B bill. **Link is not one of those** — it's Stripe's saved-credential accelerator, so a
payer who already has it confirms instead of retyping card or bank details. It shortens
time-to-payment and costs nothing in seriousness, so it stays on. (An earlier version of this
skill lumped Link in with the BNPL options and silently trimmed it; Shaw caught it and set the
three-method list above as the standing default.)

### Computing days_until_due

Shaw's policy is **due ~7 days before the session** — compute from the session date rather than
defaulting to net-14, and if the session is too near for that, say so instead of silently picking
a longer term. When no session is booked yet (participants still TBD on a group deal), net-7 from
send is the fallback.

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

### Creation is the commit point (drafts are locked too)

**Through this connector, a draft invoice is write-once in every part.** Not the invoice
(`PostInvoicesInvoice` absent — no changing due date, memo, or payment methods), not the line
items (`PostInvoiceitemsInvoiceitem` and `DeleteInvoiceitemsInvoiceitem` both absent, as are the
`PostInvoicesInvoiceLines*` operations), and nothing can be deleted. `PostInvoiceitems` creates;
it does not edit.

This skill previously claimed line items were "fully featured" and editable. They aren't, and the
wrong claim is expensive in a specific way: believing a description is fixable later licenses
writing one without checking it with Shaw first. On 7/30/26 that produced four invoices for a
single $4,500 deal — one for a too-long line item, one for a memo edit, one for a payment method —
each rebuild stranding a draft Shaw had to delete by hand, since the connector can't delete either.

Practical upshot: **the confirmation gate belongs before `PostInvoices`, not before finalize.**
Assemble the entire spec first — payer, line item text, memo text, quantity, amount, due date,
payment methods — show Shaw the strings that will actually render, and create only on his OK.
Treat `PostInvoices` the way you'd treat finalize: cheap to get right beforehand, irreversible
after. If Shaw changes any wording post-creation, the only path is a full rebuild plus manual
cleanup, so say that plainly rather than implying a quick edit is possible.

Two escape hatches worth knowing: drafts *are* fully editable in the dashboard via **Edit draft**
and delete cleanly from the ⋯ menu, so a one-field fix may be cheaper handed to Shaw than
rebuilt — offer both and let him pick. And if you create a price by mistake, deactivate it with
`PostPricesPrice` (`active: false`).

## Billing a multi-month engagement (installment plans)

When a deal is "$X per month for N months" — a retainer, a continuity offer, a phased engagement —
the instinct is a subscription. **Reach for N dated invoices instead.** It wins on every axis that
matters here, and it's the only route this connector can build end to end:

| | N dated invoices | Subscription |
|---|---|---|
| Land on exact due dates | yes | anchors to checkout date, or drifts |
| ACH available | yes | Stripe's payment-update link is **card-only** |
| Can overrun the term | no — there are exactly N | yes, needs a cancel date set by hand |
| Buildable via this connector | yes | no — dashboard only |

The ACH difference compounds across N installments, so the standard
`["us_bank_account", "card", "link"]` list matters more here than anywhere else — see
"Payment methods" above.

The only thing given up: the client pays N times instead of once. For a company that already pays
Stripe invoices without friction, that's not a real cost.

### Making it self-running

Create all N invoices up front, then let Stripe do the sending:

- `collection_method: send_invoice` and an explicit `due_date` per invoice.
- `auto_advance: true` plus **`automatically_finalizes_at`** on every invoice after the first.
  Finalization is the "issue and send" moment — it assigns the number, generates the PDF and hosted
  payment page, and emails the client. Scheduling it means invoices 2..N send themselves months
  later with no action from Shaw, while staying fully editable as drafts until they fire.
- Schedule each send ~a week before its due date, and **shift off weekends** — a Saturday send date
  is worth moving to the Friday.
- **Invoice 1 gets `auto_advance: false`.** With advancement on and no finalize time, Stripe picks a
  finalization time from the account's grace period and can email the client before Shaw has
  approved it. Create it inert, show Shaw the summary, then `PostInvoicesInvoiceFinalize` with
  `auto_advance: true` once he says go — that single call is what sends it.

### Two account settings this depends on

Neither is readable via the API, so ask Shaw to confirm both — and note they live on **different
tabs**, which is easy to get wrong:

| Setting | Where | Why it matters |
|---|---|---|
| **Send finalized invoices and credit notes to customers** | Settings → Billing → *Subscriptions and emails* | Without it, scheduled invoices finalize **silently** and the client never gets an email |
| **Send reminders if a *one-off* invoice hasn't been paid** | Settings → Billing → *Invoices* → Manage advanced invoicing features | Auto-chases unpaid invoices; add reminders before / on / after the due date |

The reminder setting has a near-identical twin — "Send reminders if a **recurring** invoice hasn't
been paid" — on the Subscriptions and emails tab. That one only governs subscription-generated
invoices (`billing_reason: subscription_cycle`). Invoices you create are `billing_reason: manual`,
so the **one-off** setting is the one that applies. Flipping the recurring toggle does nothing.

### Recording it downstream

One engagement billed in N installments is still **one** row in the Engagements DB, with `Price`
holding the contract value and `Paid Status` walking `Unpaid` → `Partial` → `Paid in Full`. Hand
the invoice IDs to the `engagements` skill for its Payment Schedule table.

## Payment links

For "create a Stripe link for X" — use `create_payment_link` with a price ID.

**A payment link can't carry a coupon.** There's no `discounts` parameter — only
`allow_promotion_codes`, which asks the customer to type a code, and a client who forgets it pays
list price. So a discount that must apply automatically has to live **in the price**: add a second
price at the discounted amount on the same product and point the link at it, leaving the list price
as the anchor. Keep the coupon for invoices, which do accept `discounts` directly.

Payment links also expose only a **relative** trial (`subscription_data.trial_period_days`), never
a fixed date — so "first charge on the 10th" drifts by however long the client waits to click.
Absolute `trial_end` exists on Checkout Sessions, which this connector can't create. Payment links are shareable and don't require a customer record. Good for: course/intensive checkouts, lead magnets with a paid tier, one-off offers Shaw wants to drop into a DM or post.

Confirm with Shaw before creating: which price, any quantity limits, where he plans to share it. Return the payment link URL when done.

## Reporting and lookups

When Shaw asks "did X pay", "how much is in my account", "what's my Stripe doing", reach for:

- **`retrieve_balance`** — current available + pending balance
- **`GetInvoices`** via `stripe_api_execute` — recent invoices with status (`paid`, `open`, `void`, `draft`, `uncollectible`) and full line items. Filter with the `customer` param if Shaw names a specific person. (There is no `list_invoices` tool.)
- **`list_payment_intents`** — actual successful payments (`status: succeeded`) vs. canceled attempts. Useful for verifying a charge actually went through.
- **`search_stripe_resources`** with `customers:email~"..."` — quick lookup for a specific person (there is no `list_customers` tool)

Most activity is one-off invoicing, but don't assert that the account has *no* subscriptions or
coupons — check if the question depends on it (see "Read billing mode live" above).

## URL patterns

These are stable Stripe dashboard patterns — useful for giving Shaw a clickable link to manage things.

- Invoice (dashboard): `https://dashboard.stripe.com/invoices/{invoice_id}`
- Customer (dashboard): `https://dashboard.stripe.com/customers/{customer_id}`
- Payment intent (dashboard): `https://dashboard.stripe.com/payments/{payment_intent_id}`
- Hosted invoice (customer-facing): returned in the `url` field on `finalize_invoice`

When Shaw asks for "the link to that invoice", he usually means the dashboard URL (so he can manage it), not the hosted one (which is for the customer to pay). If unclear, share both.

## Working pattern reminders

- **Confirm before creating, not just before finalizing.** Nothing on a draft can be edited or
  deleted through this connector, so `PostInvoices` is the commit point. Show Shaw the exact
  strings first.
- **Surface the live-mode caveat** when creating anything for a real customer — quick reminder, no need to belabor it.
- **Ask who's being billed.** Don't infer the payer from precedent (see "Confirm what only Shaw knows").
- **Don't create duplicate customers.** Email lookup first, every time.
- **Check the write op exists before promising the outcome.** One `stripe_api_details` call beats
  walking back a plan Shaw already approved.
- **When something is blocked by API limits** (void, update finalized invoice, subscriptions, Checkout Sessions), tell Shaw what the wall is and offer the dashboard workaround. Don't loop trying alternative API operations.
- **Prefer N dated invoices over a subscription** for monthly engagements — see the installment section.
- **Default to including dashboard links** in any summary — Shaw moves between Claude and the dashboard frequently.
