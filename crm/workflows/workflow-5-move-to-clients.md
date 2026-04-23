# Workflow 5: Move Lead to Clients

Use when a deal closes and the lead should graduate from Active Leads to the Clients (Nurture) database.

## Step 1 — Fetch the lead's Active Leads record

Search the Active Leads data source for the lead by name. Fetch their full page to get all
current properties (Name, Email, Source, Notes, Last Contact?) and any page body content
(call note links, etc.).

## Step 2 — Create the client record

Create a new page in the Clients (Nurture) data source (`collection://[database-id]`)
with these fields:

- **Name** — carry over from lead
- **Email** — carry over from lead
- **Source** — carry over from lead
- **Status** — set to `Active` if the engagement is starting now, or `Nurturing` if it's already complete
- **Last Contact?** — carry over from lead
- **Next Check-in** — depends on Status. If `Active`, set to the date of the next scheduled
  training/session (the first delivery date for a new engagement). If `Nurturing` (engagement
  already complete), set ~3 months out from today for the quarterly outreach cadence.
- **Engagement Type** — infer from context: `1:1` for individual consulting, `Workshop` for team
  workshops, `Bootcamp` for bootcamp graduates who converted, `Ad Hoc Advisory` for anything else
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

## Step 5 — Confirm

Summarize what was created in Clients (Nurture) and remind Shaw to delete the old Active Leads entry.
