# Workflow 3: Add a New Lead

Use when Shaw shares a new contact form submission, inbound email, or new lead from any source.

This workflow assumes the inbound *is* a lead. When it arrived through a form rather than a
conversation, confirm that first — see SKILL.md → "Inbound isn't automatically a lead." Solo
founders and peers show up in the same inbox as real prospects, and neither belongs in Active
Leads.

## Required fields to populate

- `Name` — full name
- `Email` — from the contact form or email header
- `Source` — infer from context. Website paths: `ABA Contact` = aibuilder.academy contact form, `ABA Discovery Call` = direct Calendly booking on aibuilder.academy (no contact form first), `Homepage Contact` = shawhintalebi.com contact form. Other defaults: `ABB` for bootcamp alums, `LinkedIn`/`YouTube` for inbound from those channels, `Personal` for warm contacts.
- `Last Contact?` — date of initial contact
- `Next Contact` — when to follow up next, per cadence defaults in
  `references/follow-up-guidance.md`. Common cases: inbound contact form reply → +2–3 days
  (FU #1); call booked → the call date; call link sent, awaiting confirmation → +2 days.
  Always populate — leaving this blank causes the lead to go silent in Workflow 1's sync.
- `Notes` — first entry, e.g. `ABA contact form (3/16). Replied, offered call (3/16).`
- `Status` — only set if the lead has clearly reached a pipeline stage (e.g. a call link was sent → `Pending Call`, a call was booked → `Booked Call`). If the lead just submitted a contact form and received a reply with info or pricing, leave Status **blank** — do not default to `Pending Call`
- `Company` — the account, when it has a row. Look the company up in Companies (`collection://[page-id]`) by email domain, then by name, and link it if it's there. If it isn't, check Active Leads and Clients for someone else at the same domain: a colleague intro'd at an account already in the pipeline — a second decision-maker, a VP the buyer looped in — gets their own lead row, and that second row is what earns the company one. Create it then (Name, Domain, Website, Relationship `Prospect`, a two-bullet `## Context`), link both people, and backfill `Company` on the first person's ABA Calls pages and mined rows. With no one else there, leave `Company` blank and put the company in the lead's `Role:` line as plain text with its site; SKILL.md → "Companies, people, and who gets a CRM row" has the threshold. Also blank for a solo operator.

**Create the page under:** data source `[page-id]`

After creating, confirm the Notion page was created and summarize the fields set.

## When the new lead came from a Calendly booking

A Calendly booking for a **discovery call** is handled end-to-end by **Workflow 7 (Discovery
Call Intake)** — if you're creating this lead, you're most likely being called *by* Workflow 7.
Workflow 7 owns the ABA Calls page, the FU task, the pre-call brief, and the same-day
confirmation email; this workflow's job is just the Active Leads record (Source =
`ABA Discovery Call` for a direct booking). Don't draft the confirmation email here —
Workflow 7's Step 5 handles it via email-helper.

## When the new lead came from a campaign tracker

If the contact already exists in a campaign tracker (Workshop Outreach, ABA Lead Generation, etc.), promote them after the CRM record is created:

- Add `Added to CRM` to the tracker entry's Status
- Clear `Next Contact` on the tracker entry
- Append `Added to CRM (M/D).` to the tracker Notes

The tracker entry stays for historical context but stops driving touchpoints — the main CRM
owns the cadence going forward. See SKILL.md → "Promotion to main CRM" for the rationale.

## When the new lead came from a Homepage Contact form

If the source is `Homepage Contact` (shawhintalebi.com contact form), the original submission lives in u/2 (`shawhintalebi@gmail.com`), not the ABA inbox. When drafting a reply as part of this workflow:

- Follow the Squarespace threading instructions in `email-helper` → "Squarespace contact-form threads": reply in the u/2 thread via Chrome (click Reply), CC `shaw@aibuilder.academy`
- Use the Calendly link mapping in that same section to pick the right link based on the lead's ask (corporate training → `ai-transformation`, individual workshop → `claude-workshop-discovery`, general/vague → `aba-intro-call`)
- Do NOT create a standalone draft in the business inbox — that loses the thread
