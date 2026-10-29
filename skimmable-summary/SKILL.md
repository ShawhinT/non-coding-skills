---
name: skimmable-summary
description: "Shaw's house format for any multi-item summary, digest, briefing, status report, roundup, or a staged plan/roadmap he'll skim. Use whenever Claude presents several items across categories — scheduled-task reports, \"give me a rundown,\" \"catch me up on X,\" \"summarize my inbox/Slack/calendar/leads/pipeline,\" research roundups, sync results. Render as: a dated H1, a one-line count dashboard, emoji-headed sections with one-sentence linked items, every section always shown with an empty-state line, and a \"🔴 Needs Your Attention\" action closer. This is the DEFAULT presentation for digests to Shaw — apply it even when he doesn't name a format, and especially when he asks to make something \"easier to skim,\" \"more scannable,\" or \"match my format.\" When a task supplies its own section map, keep this frame with those sections. Do NOT use for single facts, one-item lookups, conversational replies, code, or long-form prose (reports, essays, letters, docs)."
---

# Skimmable Summary

This is Shaw's house style for turning a pile of gathered information into something he can
read in ten seconds. The job of a summary is to answer two questions before any detail:
*how much is here* and *what needs me*. Everything below serves that.

The format is a fixed **frame** with a swappable **middle**. The frame — title, count
dashboard, the rules for items, and the action closer — never changes. The middle sections
are whatever the situation calls for. So a calendar digest, a CRM sync, and a "catch me up
on Slack" all look like siblings even though their sections differ.

## When this applies (and when it doesn't)

Use it for any digest of **multiple items across categories** that Shaw will skim — whether
he asks for a format or not. It's the default.

Don't use it for a single fact, a one-item lookup, a normal conversational reply, code, or
long-form prose (a report, essay, letter, or doc). Forcing a dashboard onto a one-line
answer is worse than not having one. If you're unsure, ask whether the reader would scan or
read it — scan means use this; read means don't.

One artifact beyond after-the-fact digests takes this frame too: a **plan or roadmap** Shaw
will skim. Its sections are the stages or phases, its items are considerations and
next-actions, and it ends with the same 🔴 closer for what he has to decide next. It passes
the scan test, so it's in — the frame doesn't only describe *what happened*, it works for
*what's ahead*. What still stays out is genuine read-me-through prose: a staged roadmap is in,
a narrative report of the same plan is not.

## The frame

```
# <Title> — <Weekday, Mon D>

<count · count · count>

🔵 <Section A>
- <one-sentence item, name → source link>
- <empty-state line>

🔵 <Section B>
- …

🔴 Needs Your Attention
- <linked name — short context clause — **one decision-ready question?**>
- ✅ Nothing needs attention
```

Top to bottom: a dated **title**, a one-line **count dashboard**, the **informational
sections** (the record — what happened, what's due, what's coming), and the **action closer**
last. The closer is always the final section, because the last thing Shaw reads should be the
thing he has to act on.

## The rules (these never change)

These hold no matter what the sections are. They're what make every summary feel the same.

- **Title is a dated H1.** `# <Name> — <Weekday, Mon D>`. No emoji in the title — the
  sections carry the emoji.
- **Stat line is a one-line dashboard.** Counts joined by ` · `, on its own line, with a
  blank line above and below it. This is the "how much is here / how much needs me" read.
  Pick 3-5 counts that matter for this summary; always include the count of items in the
  closer (e.g. `… · 1 for you`).
- **One sentence per item, most important thing first.** Lead with the name or the action —
  the thing Shaw scans for — then the context. No padding, no second clause that could be
  cut. If a line needs two sentences, it's two items or it's too detailed.
- **Names are links, never bold.** Each person/record/item hyperlinks to its source (Notion
  page, Gmail draft, calendar event, message). The summary is a launchpad; Shaw clicks
  through for depth. Bolding names instead of linking them is the most common miss. Links
  point to a source that *exists* — in a plan or roadmap the items are considerations and
  next-actions with no underlying record, so they stand on their own rather than getting a
  fabricated link. The never-bold part still holds; use ⚠️ to flag judgment calls inline.
- **Closer items are asks, not findings.** Every 🔴 item reads: linked name → short context
  clause → **the one concrete question**, bolded, at the end of the line. The question is
  decision-ready — answerable in one sentence ("send the nudge?", "book it for next week?",
  "which convention should both follow?"). The diagnosis that *led* to the question belongs
  in the record sections or the brief context clause, never as the payload — a finding
  description that leaves Shaw to derive the ask himself defeats the closer's purpose. If an
  item can't be phrased as a question (or a direct approval ask), it's an FYI, not an
  attention item: move it to a record section. Bolding the question is the one deliberate
  exception to the never-bold rule — bold marks the ask, and only the ask.
- **The closer is scope-bounded to this summary's domain.** In a system of specialized
  syncs, an adjacent signal you happened to notice while gathering data belongs to whichever
  report owns that domain, not to this one. Surfacing it here produces the same ask in two
  reports and dilutes the closer's signal. If an item wouldn't have been found by this
  summary's own sources, it isn't a closer item — leave it out.
- **Every section always renders, with an explicit empty-state line.** A quiet day must read
  as cleanly as a busy one — never drop a section just because it's empty. The empty-state is
  one short line (see each component for its wording).
- **Record first, action last.** Informational sections up top; the 🔴 closer at the bottom.
  Never make Shaw hunt through the record to find what he has to do.

## Delivery (pull, not push)

The summary is a pull artifact: it renders in the surface Shaw will open himself — the chat
reply, or a scheduled run's final report. It is never the body of a notification, in full or
in part. A digest pushed to a phone defeats the format — nothing is clickable there, and a
daily push trains skim-blindness on the one channel that exists to interrupt.

On a scheduled run: a clean run — empty closer, nothing failed — sends no notification at
all; Shaw pulls the report up when he wants it. Only when the 🔴 closer has items, or the run
itself failed, send a one-line ping so he knows to open the run — title + count ("Engagement
Sync: 2 need you"), never the content. A task's own prompt may tighten this further (e.g.
always silent); it never loosens it back to pushing the summary.

## Marker legend (fixed meaning)

Markers are a visual vocabulary — they only work if they mean the same thing every time.

- 🔴 needs you (the action closer; also as an inline prefix on an item that needs review)
- ⚠️ caution / judgment-call flag
- ✅ / ✓ clean / done / verified
- ⏭️ skipped
- 📌 due
- 📅 upcoming / on the calendar
- 🧹 cleanup chore

Section-topic emoji (🏫 trainings, 📞 calls, ✏️ changes, etc.) are free to fit the domain —
the legend above is only for the status markers that recur across summaries.

## House conventions (locked, so every summary matches)

- **Bullets:** `-` (hyphen). Not `*`, not `•`.
- **Section headers:** bold emoji + label — `🔵 **Section**`. Not plain, not `##` markdown
  headings.
- **Action closer is named** `🔴 Needs Your Attention` **only when it has items.** When empty, the whole section collapses to the single line `✅ Nothing needs attention` — no header, no bullets.
- **Closer empty-state is exactly** `✅ Nothing needs attention`.
- **Stat line** is plain counts joined by ` · ` — no per-count emoji.

## Components (opt-in building blocks)

Most summaries are just sections + the closer. A few need extra pieces. These are named so a
task can ask for them by name:

- **`[closer]`** — the `🔴 Needs Your Attention` section. Always present, always last. One
  line per item needing Shaw's input, each shaped per the asks-not-findings rule: linked
  name — context clause — **bolded decision-ready question**. Empty-state: collapse the
  whole section to the single line `✅ Nothing needs attention` (no header, no bullets).
- **`[consolidated-link-line]`** — when several items share one kind of follow-up link (e.g.
  Gmail drafts to review), collapse them into one line inside the closer rather than a link
  per item: `Review drafts: [Name](url), [Name](url)`.
- **`[verification-footer]`** — for data-integrity work (syncs, reconciliations), a final
  `✓ Verification: …` line stating what was cross-checked and how many writes were made. This
  sits below the closer as evidence the run was self-audited.
- **`[table-section]`** — when the body is ranked or tabular data (e.g. a leaderboard) that a
  per-line list would flatten, render that one section as a markdown table instead of
  bullets. The frame (title, stat line, closer) still wraps it.
- **`inline-marker`** — prefix an item in a record section with 🔴 or ⚠️ when it also needs
  attention, then roll the same item up (with its reason) in the closer. The prefix lets the
  record section scan on its own; the closer collects the asks.

## Section-map contract (for codified tasks)

A scheduled task or workflow shouldn't restate any of the rules above — it should point here
and declare only **its sections**. That keeps the house style in one place: change it here,
every task inherits it. Restating format rules inside a task prompt does worse than
duplicate — it invites drift and makes it likely the renderer pattern-matches the inlined
spec instead of loading this skill at all. Declare sections, nothing more.

A task declares, in order, each section as: **emoji + label · what populates it ·
empty-state line**, plus which **stat-line tokens** to show and any **components** it uses.
For example, a task's entire report spec can be:

```
Format per the skimmable-summary skill. Stat line: "N due · N updated · N ahead · N for you".
Sections, in order:
- 📌 Due today — items due now (name → source); empty: "✅ Nothing due today."
- ✏️ Updated — records changed this run; empty: "No changes this run."
- 📅 Coming up — calls/sessions on the calendar; empty: "Nothing on the calendar."
- 🔴 Needs Your Attention [closer] — decisions/messages/flags.
Components: [verification-footer].
```

Everything else — the dated title, spacing, linking, one-sentence items, always-render
empty states, the closer's empty-state wording — comes from the skill.

## Default body (ad hoc, no section map)

When Shaw asks for a summary with no predefined sections ("catch me up on the Acme thread,"
"summarize what came in overnight"), don't invent a rigid taxonomy. Group the items into 2-4
natural emoji-headed buckets, informational first, and end with the 🔴 closer. The frame and
rules still apply; you're just choosing sensible sections on the fly. A reasonable default
for "what happened" content is something like 🆕 New / 🔄 Updates / 🔴 Needs Your Attention.

## Authority

This is the default presentation for any multi-item digest to Shaw, scheduled or ad hoc —
apply it even when he doesn't name a format. When a task supplies its own section map, keep
this frame and use those sections (the map wins on *which* sections, the skill wins on *how*
they're rendered). It composes with content skills: they gather and decide the data, this
skill only shapes the final summary. It never applies to prose documents, single facts, or
code.

## Worked example

```
# CRM Sync — Thu, Jun 11

3 due · 5 updated · 2 ahead · 1 for you

📌 **Due today**
- [[Client Name]](https://notion.so/…) — catch-up reply is a week overdue → [draft](https://mail.google.com/…)

✏️ **Updated**
- [[Person]](https://notion.so/…) — stage moved Outline Sent → Negotiating.

📅 **Coming up**
- Fri Jun 12 — [[Client Name]](https://notion.so/…) (1:1 Claude Workshop, 11:30 CT).

🔴 **Needs Your Attention**
- [[Person]](https://notion.so/…) — wants 3 grouped 1:1s — **approve the updated scope before I send?**

✓ Verification: clean — cross-checked Stripe, ABA Calls, and Nurture; 5 writes made.
```

On a fully clean run the same report ends with the closer collapsed to one line — no header:

```
✅ Nothing needs attention
```
