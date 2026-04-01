---
name: outreach-campaign
description: >
  Set up and manage outreach campaigns for Shaw. Use this skill whenever Shaw is doing 1:1 outreach
  to a list of people — whether for workshops, events, research calls, partnerships, or any initiative
  where he's reaching out individually and tracking responses. Triggers include: "set up outreach",
  "track my outreach", "create an outreach table", "add people to the outreach list", "who have I
  reached out to", "update outreach", "write me an outreach message", "draft a DM template", or any
  time Shaw shares a batch of names/contacts he's reaching out to. Also trigger when Shaw is building
  a campaign page with outreach templates and wants a tracker alongside it, or when he's crafting the
  actual messages he'll send. Even casual mentions like "I texted these 5 people", "add them to the
  list", or "what should I say to these people" in an outreach context should trigger this skill.
---

# Outreach Campaign Skill

Shaw regularly runs outreach campaigns — reaching out 1:1 to people for workshops, events, research
calls, partnerships, and other initiatives. Each campaign follows a similar pattern: a Notion page
with context about the campaign, an inline tracker database, a segment legend, message templates,
and the outreach messages themselves.

This skill handles both sides: crafting the outreach messages and templates, and the operational
tracking of who was contacted and how they responded.

## General principle: confirm before creating

Throughout this skill — whether setting up a database, drafting templates, or structuring a
campaign page — use the AskUserQuestion tool to present your plan before executing it. Shaw
would rather approve a quick summary than undo work that went in the wrong direction. This is
especially important for anything structural (database columns, status options, page placement)
where assumptions are easy to get wrong and changes are tedious to make after the fact.

## How Shaw's outreach campaigns work

Shaw organizes outreach by **segments** — groups that share a common trait like relationship
proximity, seniority, location, or channel. The exact segmentation varies by campaign, but the
principle is the same: prioritize the warmest or highest-value segments first and work outward.

Examples from past campaigns:

- **Free workshop outreach:** Segment 1 = met in person, Segment 2 = met on virtual call, Segment 3 = have their email
- **Event series outreach:** Segments 1-6 based on seniority (Leader/Manager/IC) crossed with location (DFW/non-DFW)

The status options are also campaign-specific. A workshop campaign might track `Replied`, `Applied`,
`Selected`. An event outreach might track `Booked call`, `Pending Call`. Design the statuses to
match the campaign's pipeline — what are the meaningful milestones someone moves through?

## Setting up a new campaign tracker

When Shaw asks to create or set up an outreach tracker, follow this process:

### 1. Understand the campaign context

Before creating anything, figure out:
- What's the campaign for? (workshop, event, research calls, etc.)
- Where should the tracker live? (which Notion page)
- What are the segments? (how is Shaw grouping his outreach list)
- What status milestones matter? (what progression does a contact go through)
- What contact info is Shaw tracking? (email, phone, LinkedIn, platform like WhatsApp/iMessage)

If Shaw has already described this in conversation or on the Notion page, extract it from there
rather than asking redundant questions.

### 1b. Confirm the plan before creating anything

Use the AskUserQuestion tool to present the proposed database structure for Shaw to approve
before building it. This avoids unnecessary rework — things like superfluous status options,
wrong column names, or incorrect placement are much easier to fix before creation than after.

Present something like:
- **Columns:** Name, Segment, Contact, Status, Last Contact, Notes
- **Segment options:** 1 = [description], 2 = [description], ...
- **Status options:** [only the milestones that matter]
- **Placement:** inline table under [section name]

This confirmation step applies any time there's ambiguity about the structure. If Shaw has
already been very explicit about exactly what he wants, it's fine to just build it — use
judgment on when to ask vs. when to act.

### 2. Create the inline database

Create the database as an **inline table** on the campaign's Notion page. Shaw prefers inline
databases over full-page databases — they live right in the flow of the page content alongside
templates, context, and legends.

Use `notion-create-database` with the `parent` set to the page ID, then if it doesn't appear
inline, use `notion-update-data-source` with `is_inline: true`.

**Standard columns** (adapt names and options per campaign):

| Column | Type | Purpose |
|---|---|---|
| Name | Title | Contact's full name |
| Segment | Select | Numbered options (just the number — keep it clean) |
| Contact | Rich text | How Shaw reached them: email address, phone, "iMessage", "WhatsApp", "LinkedIn DM", etc. |
| Status | Multi-select | Campaign-specific milestones only — no "Sent" or "No response" (that's what blank means) |
| Last Contact | Date | Date of most recent touchpoint |
| Notes | Rich text | Chronological log of actions (see Notes format below) |

Additional columns may make sense depending on the campaign (e.g., Company Size, LinkedIn URL,
topic-specific checkboxes). Add them when the campaign context calls for it.

Status options should only represent meaningful forward progress — if blank already
communicates the default state (e.g., "message sent, no reply yet"), there's no need
for a status for it.

### 3. Add a segment legend

After the database, add a simple reference table so Shaw (and future Claude sessions) can quickly
decode what the numbers mean:

```
| Segment | Description |
|---------|-------------|
| 1       | Met in person |
| 2       | Met on a virtual call |
| 3       | Have their email |
```

Use `notion-update-page` with `update_content` to insert the table after the database.

### 4. Place it in the right spot on the page

Look for cues on the page about where the tracker should go. Shaw sometimes leaves placeholders
like `{Add outreach database here}`. If there's a natural section for it (e.g., an "Outreach"
heading), place it there.

## Adding contacts

When Shaw shares names to add to the tracker, create pages in the database's data source using
`notion-create-pages`. Extract as much info as possible from what Shaw provides:

- **Name** — always required
- **Segment** — infer from context (Shaw usually specifies which segment)
- **Contact** — email address, phone number, or platform name (iMessage, WhatsApp, LinkedIn DM)
- **Status** — only set if the person has already hit a milestone (e.g., they already replied)
- **Last Contact** — set to today's date if Shaw just reached out, or the date he mentions
- **Notes** — initial entry if there's activity to record

Shaw often adds contacts in batches. Handle them all in a single `notion-create-pages` call.

## Updating contacts

When Shaw reports activity (someone replied, applied, was selected, etc.):

1. Find the contact's page in the database
2. Update their Status and Last Contact date
3. Append to Notes (never overwrite)

### Notes format

Use the same format as the CRM skill — read the Notes Format section in the CRM skill for the
full guide. In short: short, comma-separated, date-stamped actions. Always append, never overwrite.

**Example:** `Emailed (3/30). Replied, asked to spectate (3/30). Replied: no spectating, will send YT video (3/30).`

## Reviewing campaign status

When Shaw asks how the outreach is going or wants a status check, fetch all entries from the
tracker and summarize:

```
**Replies received:**
- [Name] — [brief context from notes]

**Awaiting response:**
- [Name], [Name], [Name]...

**Next steps:**
- [Any follow-ups due or next segments to activate]
```

Cross-reference Gmail if Shaw asks for updates — search for each contact's email to find new
replies that haven't been logged yet. Update the tracker with anything new found.

## Crafting outreach messages

Each campaign typically needs templates — one per segment and sometimes per channel (text, email,
newsletter). The templates share a core pitch adapted for the audience and medium.

When drafting templates, start with the warmest segment first to establish the core pitch, then
adapt outward to colder segments. Draft one at a time so Shaw can react and steer before the
next one — his feedback on the first template shapes the rest.

Save finalized templates to the campaign page in code blocks so they're easy to copy-paste.

For voice, tone, and email-specific details (HTML formatting, Gmail threading, etc.), defer to
the **email-writer skill** — it's the source of truth for how Shaw sounds in writing.

## Relationship to other skills

- **Notes format:** Defer to the **CRM skill** — it's the single source of truth for how Shaw writes notes.
- **Email drafting and voice:** Defer to the **email-writer skill** for Shaw's writing style and Gmail mechanics.
- **Lead management:** If a contact becomes a sales lead (books a call, asks about pricing), they
  should also be added to the CRM. The outreach tracker is campaign-level; the CRM is pipeline-level.
  A person can exist in both.
