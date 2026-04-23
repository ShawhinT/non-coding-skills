# Workflow 3: Add a New Lead

Use when Shaw shares a new contact form submission, inbound email, or new lead from any source.

## Required fields to populate

- `Name` — full name
- `Email` — from the contact form or email header
- `Source` — infer from context (`ABA Contact` for website forms, `ABB` for bootcamp alums, etc.)
- `Last Contact?` — date of initial contact
- `Next Contact` — when to follow up next, per cadence defaults in
  `references/follow-up-guidance.md`. Common cases: inbound contact form reply → +2–3 days
  (FU #1); call booked → the call date; call link sent, awaiting confirmation → +2 days.
  Always populate — leaving this blank causes the lead to go silent in Workflow 1's sync.
- `Notes` — first entry, e.g. `ABA contact form (3/16). Replied, offered call (3/16).`
- `Status` — only set if the lead has clearly reached a pipeline stage (e.g. a call link was sent → `Pending Call`, a call was booked → `Booked Call`). If the lead just submitted a contact form and received a reply with info or pricing, leave Status **blank** — do not default to `Pending Call`

**Create the page under:** data source `[database-id]`

After creating, confirm the Notion page was created and summarize the fields set.
