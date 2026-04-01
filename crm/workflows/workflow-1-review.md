# Workflow 1: Review & Cross-Reference CRM

Use when Shaw asks to review leads, check for updates, or audit the pipeline.

## Step 1 — Fetch all Active Leads

Search the Active Leads data source to get all current records with their properties.

## Step 2 — Cross-reference Gmail for each lead

For each lead with an email address, search Gmail:
```
from:<email> OR to:<email>
```
Look for any messages newer than the lead's `Last Contact?` date.

**Skip Gmail search for:**
- LinkedIn-only contacts (email field contains a LinkedIn URL)
- Leads with Status `Lost` (unless Shaw asks)

## Step 3 — Check ABA Calls if relevant

If a lead has had a call (Status is `Booked Call` or beyond), search Notion for their name under
the ABA Calls database to pull call notes for deeper context on their situation, goals, and next steps.

## Step 4 — Assess follow-up needs

Apply the follow-up rules (see `references/follow-up-guidance.md`) to flag which leads need action.

## Step 5 — Produce a summary report

Present findings in this format:

```
**Updates found:**
- [Name] — [what changed / new Gmail activity detected] → [recommended action]

**Follow-ups due:**
- [Name] — [reason] → Draft created in Gmail ✓

**Looks up to date:**
- [Name], [Name], [Name]...

**Skipped (LinkedIn-only or no email):**
- [Name], [Name]...
```
