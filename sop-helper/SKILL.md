---
name: sop-helper
description: >
  Create, update, and reference Shaw's standard operating procedures (SOPs) in Notion. Use
  whenever Shaw wants to turn a process into an SOP, update an existing one, or pull up an SOP
  to reference or walk through. Triggers: "write/update/fix the SOP for X", "document this
  process", "turn this into an SOP", "where's the SOP for X", "walk me through the SOP", or
  any reference to the SOPs page. Also trigger when Shaw describes a repeatable workflow and
  says "let's save this" or "this should be written down", or casual phrasings like "I keep
  redoing this, make it an SOP" or "we need a playbook for X". Also load at the start of any
  SOP-adjacent reasoning — proposing template edits, comparing sent mail to existing templates,
  or sketching SOP changes. Don't wait for the actual edit; if you're reasoning about what an
  SOP should say, the skill should already be loaded. Do NOT use for one-off tasks — those go
  through `notion-helper`. SOPs are for repeatable processes, not single to-dos.
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

The parent page is organized by category headers. As of this writing (confirm against the live
page — titles drift as SOPs are added, split, or renamed):

- **Acquisition** — Discovery Call, Testimonial Ask, Referral Ask, AI Rollout Audit Call,
  Event Series, Post Event
- **Delivery** — 1:1 Claude Workshop, Group Claude Workshop, Wrap-up Call, and the **Check-in
  Call family**: a shared base (**Check-in Call** — Setup, call bank, post-call mechanics) plus
  three spokes carrying the agenda + templates — **Check-in Call (1:1 Claude Workshop)**
  (post-session 4Rs), **Check-in Call (Client Nurture)** (periodic; 4Rs not forced), and
  **Check-in Call (Lead Nurture)** (warm lead; no 4Rs)
- **Resources** — reference pages rather than process SOPs (e.g. The 4Rs Framework, The
  Hormozi Content Framework); SOPs link to these instead of restating them

The call/session SOPs follow a consistent **Trigger → Setup → Pre-call research → Call →
Post-call** structure; delivery/acquisition SOPs follow their own order.

All the entries above are real child pages. A category may also carry placeholder header
bullets for SOPs Shaw hasn't written yet — promote those to real pages rather than
duplicating them.

When creating a new SOP, add it under the right category heading. If there's no obvious
category fit, surface that to Shaw and suggest either extending an existing category or adding
a new one — don't silently drop it at the bottom.

---

## Format Conventions (match what's already there)

Shaw's existing SOPs are minimal and practical. Match that style — don't impose a heavier
template unless Shaw asks for one.

### Structure of a typical SOP

An SOP opens with a one-line **`**Context**:`** statement, then a **chronological spine of
process steps**, followed by templates. Read top to bottom, it's the workflow in order.

- **A `**Context**:` line comes first** — one sentence defining what the thing is and when it
  happens (e.g. "a discovery call is any (free) initial call with a lead to discuss whether
  ABA's offerings would be a good fit"). It sits above the first step, as its own line, not as
  a bullet.
- **Top-level bullets are the steps**, in the order they happen — bold the step name. For a
  call or engagement SOP the established shape is **Trigger → Setup → Pre-call research →
  Call → Post-call**; other processes follow whatever their natural workflow order is.
- **Detail nests under the step it belongs to.** Reference material — question banks, "what
  the brief should cover" lists, policy notes — are sub-bullets of the step that uses them,
  not standalone top-level sections. A question bank used in the call lives under the Call
  step.
- **Edge cases are handled inline**, as a sub-bullet of the step where they come up — not
  collected into a dangling "Edge cases" section at the end.
- **A `**Helpful Links**` section** sits near the bottom, before the templates: the related
  Notion databases/pages and external tools this SOP touches.
- **Email/message templates last**, below a `---` divider, stacked with `---` between each.
  Each template is: a `Subject:` line carrying an italic `*(annotation)*` that says what the
  email is and when it's sent, and a fenced ```plain text``` block with the verbatim body. A
  `**Context**:` line can sit above the `Subject:` line to carry one-line adaptation rules
  (e.g. when to drop the greeting, which words to swap) — this keeps the body clean of
  bracketed guidance. A `*Drafting note:*` inside the fence is optional, used only when it
  carries something the body and context line don't: provenance ("based on real send to X,
  5/27/26"), non-obvious policy, or a cross-skill pointer. Don't add boilerplate suffixes
  like "Always draft via email-helper" — that's a system-level rule, not template content.
- **When one step needs more than one template** (e.g. a follow-up that differs by
  situation), stack them as **Variant A / Variant B**. Each variant gets its own
  `**Context**:` line saying when to use it.

Keep bullets short and action-first — "ID target audience", not "Identify the target audience
for the campaign." No Purpose, Scope, Owner, Last Updated, Version, or Revision History
sections — unless Shaw specifically asks. He wants tight reference docs, not compliance
artifacts.

### Example skeleton

````
**Context**: one sentence — what this is and when it happens

- **Trigger** — what kicks this process off
- **Setup**
	- Sub-step (e.g. create the page in <mention-page url="..."/>, link the record)
	- Sub-step
- **Step in the middle**
	- Detail / reference material used at this step
	- Edge case: handled inline, where it comes up
- **Final step**
**Helpful Links**
- <mention-page url="https://www.notion.so/<related-database-or-page-id>"/>
- [External tool](https://example.com)

---
Subject: <email subject> *(what it is — when it's sent)*
```plain text
<email body>
```
---
**Context**: when to use this variant
Subject: <subject> *(... — Variant A, <short label>)*
```plain text
<email body>
```
---
**Context**: when to use this variant
Subject: <subject> *(... — Variant B, <short label>)*
```plain text
<email body>
```
````

### Style notes

- **Short, imperative bullets.** "Export slides as PDF", not "The slides should be exported to
  PDF format."
- **Link Notion pages *and databases* with `<mention-page url="..."/>`** — not Markdown
  `[text](url)`. Link them inline at the step that touches them (the database a page gets
  created in, the record it links to), and also collect them under **Helpful Links**.
  External tools (Canva, Calendly, Drive) use Markdown links.
- **Preserve Shaw's shorthand.** He uses "FU" for follow-up, "ID" as a verb for identify, etc.
  Don't expand these.
- **Keep nesting shallow** — two levels deep is usually enough. Three is a code smell.

---

## What belongs in an SOP

### SOP vs. skill — the dividing line

An SOP and its companion skill split the work. The **SOP owns intent, policy, and content** —
the *what* and *why*, written so a human with no Claude access could follow it: the process
steps, the policy decisions (Shaw's business rules), canonical email templates, question
banks, edge cases, helpful links. The **skill owns execution** — the *how*: tool calls,
database IDs, payload shapes, the orchestration wiring between skills.

Single source of truth: if a fact lives in the SOP, the skill references it ("do step 3 per
the Discovery Call SOP") rather than restating it. Hard mechanics — IDs, payloads, codepoints
— live in exactly one place: the skill. When drafting or editing an SOP, keep mechanics out of
it; if you notice mechanics that have crept in, propose moving them to the owning skill.

### Codify only what's real

SOP content — edge cases, templates, question banks — must come from things Shaw has actually
experienced or sent. Don't invent edge cases to look thorough, and don't write a template from
imagination. Ground templates in real sent emails; ground edge cases in cases that actually
came up. If there's nothing real to codify for a section yet, leave it out rather than padding
it — an empty space is honest, an invented one is misleading.

### Cross-reference: email-helper

SOP-stored email templates are consumed by `email-helper` when drafting standard emails
(pre-call, post-event, kickoff, follow-up, testimonial asks). Keep templates in plain text
with `-` dashes — `email-helper` handles HTML conversion (bullets, links) when generating the
draft. Don't encode HTML in the SOP template itself.

**Maintenance loop.** When Shaw sends an edited version of a templated email, propose updating
the SOP template to match — otherwise future drafts start from a stale base.

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
- **Match the structure** — a chronological spine of steps, edge cases and reference material
  nested inline, Helpful Links, then templates (see Format Conventions). No Purpose / Scope /
  Owner / Version sections unless explicitly requested.
- **Keep mechanics in the skill, not the SOP** — the SOP owns process, policy, and content;
  IDs and payloads live in the companion skill (see What belongs in an SOP).
- **Codify only what's real** — never invent edge cases, templates, or question banks; ground
  them in things Shaw has actually experienced or sent.
- **Always search first** to avoid creating duplicates.
- **Use `<mention-page url="..."/>` for internal Notion links** (pages and databases),
  Markdown for external ones.
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
