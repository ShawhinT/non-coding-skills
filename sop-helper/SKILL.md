---
name: sop-helper
description: >
  Create, update, and reference Shaw's standard operating procedures (SOPs) in Notion. Use this
  skill whenever Shaw wants to turn a process into an SOP, update an existing SOP, or pull up
  an SOP to reference or walk through. Triggers include: "write an SOP for X", "document the
  process for X", "turn this into an SOP", "capture this workflow", "update the SOP for X",
  "fix the launch SOP", "where's the SOP for X", "pull up the SOP for X", "walk me through the
  SOP", or any reference to the SOPs page. Also trigger when Shaw describes a repeatable
  workflow (launch sequence, event run-of-show, research-call process) and says "let's save
  this" or "this should be written down" — that almost always means a new SOP. Casual mentions
  like "I keep redoing this, make it an SOP" or "we need a playbook for X" should trigger this
  skill. Do NOT use for one-off tasks — those go through `notion-helper`. SOPs are for
  repeatable processes, not single to-dos.
---

# SOP Helper Skill

Shaw's SOP manager. Use this skill to capture repeatable processes, update existing SOPs, and
pull them up on demand. The goal is a tight, checklist-style reference library that Shaw (and
future Claude runs) can actually use — not an over-engineered process manual.

This skill is scoped to Shaw's SOPs Notion page. For ad hoc tasks, follow-ups, or one-off
reminders, defer to `notion-helper`. If the request is "document this process so I can repeat
it," it's an SOP.

---

## Where SOPs Live

All SOPs are child pages under the **SOPs** parent page in Shaw's ABA (Master) workspace.

| Thing | ID / URL |
|---|---|
| SOPs parent page | `[page-id]` |
| URL | https://www.notion.so/SOPs-[page-id] |
| Parent (ABA Master) | `[page-id]` |

The parent page is organized by category headers. As of this writing:

- **Acquisition** — course launch (free), course launch (paid), course validation (paid), event
  promo, research calls
- **Delivery** — new course, new event

Some categories are just header bullets without child pages yet (placeholders for SOPs Shaw
hasn't written). A few are real child pages — currently **Post Event** and **Event Series** sit
under Delivery.

When creating a new SOP, add it under the right category heading. If there's no obvious
category fit, surface that to Shaw and suggest either extending an existing category or adding
a new one — don't silently drop it at the bottom.

---

## Format Conventions (match what's already there)

Shaw's existing SOPs are minimal and practical. Match that style — don't impose a heavier
template unless Shaw asks for one.

### Structure of a typical SOP

A bare SOP has two sections:

1. **A checklist of steps** (no header, just bullets). Nesting is fine for sub-steps. Language
   is short and action-first — "ID target audience", not "Identify the target audience for the
   campaign."
2. **Email/message templates** at the bottom, separated from the steps by a `---` divider.
   Multiple templates are stacked with `---` between each one. Use fenced code blocks
   (```plain text``` or similar) for templates that need to be copied verbatim.

That's it. No Purpose, Scope, Owner, Last Updated, Version, Revision History — unless Shaw
specifically asks. The existing SOPs don't have them and Shaw has made clear he wants tight
reference docs, not compliance artifacts.

### Example skeleton

```
- Step 1
- Step 2
  - Sub-step
  - Sub-step
- Step 3
<mention-page url="https://www.notion.so/<related-page-id>"/>

---

Subject: <email subject>

<email body>

---

Subject: <second email subject>

<second email body>
```

### Style notes

- **Short, imperative bullets.** "Export slides as PDF", not "The slides should be exported to
  PDF format."
- **Link to other Notion pages with `<mention-page url="..."/>`** — not Markdown `[text](url)`.
  This creates a proper live reference.
- **Inline links to external tools** (Canva, Calendly, Drive, etc.) use Markdown links.
- **Preserve Shaw's shorthand.** He uses "FU" for follow-up, "ID" as a verb for identify, etc.
  Don't expand these.
- **Keep nesting shallow** — two levels deep is usually enough. Three is a code smell.

---

## Core Workflow: Creating a New SOP

The typical trigger is Shaw describing a process he just did (or is about to do again) and
saying "let's save this" or "make this an SOP." Your job is to extract the repeatable core,
not transcribe the conversation.

### Step 1: Search first to avoid duplicates

Before creating anything, use `notion-search` scoped to the SOPs page (or the workspace) with
the SOP's likely title and a few keywords. If something close already exists, stop and surface
it — ask if Shaw wants to update the existing SOP or create a new one alongside it. The goal
is one SOP per process, not a shelf full of near-duplicates.

Search example: for "course launch", search `"course launch"` and look for hits under the
SOPs page. Also check the Acquisition/Delivery bullets on the parent page — some category
items may be placeholder entries that should be promoted to real pages rather than duplicated.

### Step 2: Draft the SOP before creating the page

Draft the SOP content in the conversation first (or just assemble it mentally before calling
`notion-create-pages`). The goal is a checklist Shaw could follow next time without rereading
the original context. Extract:

- **Discrete, ordered steps** — strip out anything that was specific to the one-off case
  (specific dates, the specific person's name, last week's numbers)
- **Sub-steps where useful** — if a step has real substructure (e.g., "create event page on
  Luma" with 6 specific things to fill in), nest them
- **Any templates** — if the process involves sending emails or messages, lift them out and
  put them in the template section at the bottom

If Shaw's description is thin (he just said "research calls, make an SOP"), ask one or two
targeted questions before drafting. Don't invent a process he hasn't described.

### Step 3: Pick the right category

Match against the existing headers on the SOPs parent page (Acquisition / Delivery / etc.).
If the SOP doesn't obviously fit, ask Shaw which bucket or whether a new category is needed.

### Step 4: Create the page under the SOPs parent

Use `notion-create-pages` with the SOPs page as the parent:

```json
{
  "parent": {"page_id": "[page-id]", "type": "page_id"},
  "pages": [{
    "properties": {"title": "<SOP title>"},
    "content": "<checklist + templates, in Notion-flavored Markdown>"
  }]
}
```

Then update the SOPs parent page (`notion-update-page` with `command: "update_content"`) to
add a link to the new SOP under the right category header. If there's already a placeholder
bullet for this SOP (e.g., `- Course launch (free)` under Acquisition), replace the bullet
text with a `<mention-page>` to the new SOP instead of adding a duplicate line.

### Step 5: Confirm back to Shaw

Keep it brief: the SOP title, which category it went under, and a link. Don't re-summarize the
steps — he just told you them.

---

## Updating an Existing SOP

Triggers: "update the SOP for X", "fix the event SOP", "the launch SOP is out of date", or any
time Shaw describes a change to how he does something that's already documented.

### Step 1: Find the SOP

Use `notion-search` or fetch the SOPs parent page and locate the child page. Read it fully
before editing — you want to make a targeted change, not a rewrite.

### Step 2: Make a targeted edit

Use `notion-update-page` with `command: "update_content"` and a search-and-replace that
touches only the relevant section. For small changes (adding a step, fixing a template), this
is much safer than rewriting the whole page.

If Shaw is asking for a larger rewrite ("redo the event SOP, it's stale"), confirm scope
before doing it — a big rewrite risks losing useful detail he doesn't remember is there.

### Step 3: Don't add revision metadata

Shaw's SOPs don't track "last updated" or version history. Don't add it unless he asks.

---

## Retrieving / Walking Through an SOP

Triggers: "where's the SOP for X", "pull up the launch SOP", "walk me through the post-event
SOP", "what do I need to do after an event."

### If Shaw wants the reference

Fetch the page, then return a short response with a link to the SOP and, if helpful, the top-
level checklist. Don't dump the whole page unless asked.

### If Shaw wants to be walked through it

Fetch the page and step through the checklist conversationally — one step at a time, waiting
for Shaw to confirm each is done before moving to the next. This turns the SOP into an
interactive runbook.

### If no SOP exists

Say so plainly, and offer to draft one from what he describes.

---

## Maintenance: Keeping the SOP Library Tidy

Not every interaction needs this, but if Shaw asks to "clean up the SOPs page" or it's
obviously drifting:

- **Promote placeholders.** If category bullets exist without child pages (e.g., "course
  launch (paid)"), flag them and offer to stub out or draft real SOPs.
- **Merge near-duplicates.** If two SOPs cover overlapping ground, propose a merge before
  doing it.
- **Flag stale content.** If an SOP references tools or pages that no longer exist, surface
  it — but don't auto-delete.

The rule: propose, don't silently restructure. Shaw's SOP page is load-bearing for his
business; changes should be intentional.

---

## Rules and Preferences

- **SOPs are for repeatable processes, not one-off tasks.** If it's going to happen once, it's
  a `notion-helper` task. If Shaw will do it again and wants a reference, it's an SOP.
- **Match the existing minimal format** — checklist + templates at the bottom. No Purpose /
  Scope / Owner / Version sections unless explicitly requested.
- **Always search first** to avoid creating duplicates.
- **Use `<mention-page url="..."/>` for internal Notion links**, Markdown for external ones.
- **Preserve Shaw's shorthand** ("FU", "ID") — don't expand it.
- **Keep nesting shallow** (two levels max unless the structure really needs more).
- **Categorize under existing headers** (Acquisition, Delivery) or ask before adding a new
  one.
- **Link from the parent page.** After creating an SOP, update the SOPs parent page so the
  new SOP is reachable via its category header — replacing a placeholder bullet if one
  exists.
- **Propose, don't silently restructure.** The SOP library is load-bearing; big edits need
  confirmation.
- **Notion-only.** This skill doesn't create calendar events, iOS Reminders, or anything
  outside Notion.

---

## Quick Reference: Notion Tools

Assume these are loaded via `tool_search` before first use:

| Need | Tool |
|---|---|
| Find an SOP by keyword | `notion-search` |
| Read the SOPs page or a specific SOP | `notion-fetch` |
| Create a new SOP page | `notion-create-pages` |
| Edit an SOP's content or properties | `notion-update-page` |
