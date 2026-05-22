# Workflow 5: Move Lead to Clients

Use when a deal closes and the lead should graduate from Active Leads to the Clients (Nurture) database.

## Step 1 — Fetch the lead's Active Leads record

Search the Active Leads data source for the lead by name. Fetch their full page to get all
current properties (Name, Email, Source, Notes, Last Contact?) and any page body content
(call note links, etc.).

## Step 2 — Create the client record

Create a new page in the Clients (Nurture) data source (`collection://[page-id]`)
with these fields:

- **Name** — carry over from lead
- **Email** — carry over from lead
- **Source** — carry over from lead
- **Status** — set to `Active` if the engagement is starting now, or `Nurturing` if it's already complete
- **Last Contact?** — carry over from lead
- **Next Contact** — depends on Status. If `Active`, set to the date of the next scheduled
  session (the first delivery date for a new engagement) — and link the corresponding ABA
  Trainings page on the CRM page body so the touchpoint is legible as a session. If `Nurturing`
  (engagement already complete), set ~3 months out from today for the quarterly outreach cadence.
- **Engagement Type** — *(soft-deprecated — the canonical home for offer info is now the
  Engagement row's `Offer` property; see Step 5. Keep filling this in during the transition
  period so existing views don't break.)* Infer from context: `1:1` for individual consulting,
  `Workshop` for team workshops, `Bootcamp` for bootcamp graduates who converted, `Ad Hoc Advisory`
  for anything else.
- **Notes** — start fresh with a summary entry, e.g. `Moved from Active Leads (4/1). Workshop engagement.`

## Step 3 — Preserve history in the page body

The Notes property on the new client page is a fresh log starting from the move, but the lead's
Active Leads history should not be lost. Build the page body in this order:

1. A `Lead notes:` line followed by the full Active Leads Notes text, carried over verbatim.
2. A `---` horizontal divider.
3. The call note links (`<mention-page>` references) from the Active Leads page body, one per line.

Example:

```
Lead notes: <full Notes text from Active Leads, verbatim>

---

Jan 15: <mention-page url="..."/>
Apr 9: <mention-page url="..."/>
```

This keeps the short-log Notes property clean going forward while preserving the full sales
history one scroll away.

## Step 4 — Mark the move in Active Leads

Append to the lead's Active Leads Notes: `Moved to Clients (Nurture) (M/D).`

Shaw will manually delete the Active Leads entry — the Notion tools don't support page deletion.
Let Shaw know he can delete it.

## Step 5 — Create the engagement row

The won deal now needs a row in the Engagements DB so the project ledger has a record of this
work. Hand off to the `engagements` skill's `workflow-1-create.md`, passing:

- The new Clients (Nurture) page URL (for the `Client` relation)
- The offer name (canonical option from `engagements/references/offer-pricing.md`)
- The source (carry over from the lead)
- Start Date (first scheduled session, or today if kickoff is now)
- End Date (projected, if known)
- Stripe invoice ID if already issued (engagements workflow-4 can fill in Price + Paid Status)

Without this step, the deal closes into Nurture but the project ledger has no record — you'll
have no per-project view of revenue, sessions, outcomes, or wrap-up artifacts. The client's
quarterly nurture cadence still works, but every other engagement-level signal is missing.

## Step 6 — Confirm

Summarize what was created in Clients (Nurture) and the new Engagement row, and remind Shaw to
delete the old Active Leads entry.
