# Tracker Setup (Notion)

Use this when Phase 5 of the outreach flow calls for creating a tracker. Shaw's campaigns live on Notion pages with an **inline** database for the tracker, a segment legend, templates, and context — all on one page.

## Before creating anything: confirm the plan

Use AskUserQuestion to present the proposed schema before building it. Rework on structural things (column names, status options, placement) is tedious. Present something like:

- **Columns:** Name, Segment, Contact, Status, Last Contact, Notes
- **Segment options:** 1 = [description], 2 = [description], ...
- **Status options:** [only the milestones that matter]
- **Placement:** inline table under [section name]

If Shaw has already been very explicit about exactly what he wants, it's fine to just build it — use judgment.

## Create the inline database

Use `notion-create-database` with `parent` set to the page ID. If the table doesn't render inline, follow with `notion-update-data-source` setting `is_inline: true`. Shaw prefers inline databases over full-page databases — they live in the flow of the page alongside context, legends, and templates.

### Standard columns

Adapt names and options per campaign:

| Column | Type | Purpose |
|---|---|---|
| Name | Title | Contact's full name |
| Segment | Select | Numbered options — just the number, keep it clean |
| Contact | Rich text | How Shaw reached them: email, phone, "iMessage", "WhatsApp", "LinkedIn DM" |
| Status | Multi-select | Campaign-specific milestones only |
| Last Contact | Date | Date of most recent touchpoint |
| Notes | Rich text | Chronological log of actions (see Notes format in CRM skill) |

Additional columns when the campaign calls for them: Company, Company Size, LinkedIn URL, Location, topic-specific checkboxes.

### Status options

**Only meaningful forward progress.** If blank already communicates the default ("message sent, no reply yet"), there's no status for it. No `Sent`, no `No response`.

Campaign-specific examples:
- **Workshop outreach:** Replied, Applied, Selected
- **Event outreach:** Booked Call, Pending Call
- **Research calls:** Replied, Scheduled, Completed

## Add a segment legend

After the database, add a simple reference table so Shaw (and future Claude sessions) can decode the numbers:

```
| Segment | Description |
|---------|-------------|
| 1       | Met in person |
| 2       | Met on a virtual call |
| 3       | Have their email |
```

Use `notion-update-page` with `update_content` to insert the table after the database.

## Place it in the right spot

Look for cues on the page about where the tracker goes. Shaw sometimes leaves placeholders like `{Add outreach database here}`. If there's a natural section (e.g., an "Outreach" heading), use that.

## Common segment schemes

Pick the one that matches how Shaw wants to prioritize:

- **Relationship proximity** — met in person → met virtually → have their email → cold
- **Seniority × location** — DFW leaders → DFW managers → DFW ICs → non-DFW leaders → ...
- **Channel** — existing DMs → LinkedIn-only → cold email
- **Heat tier** — warm intros → known but not close → cold

The number of segments matches the number of distinct message templates Shaw will write.
