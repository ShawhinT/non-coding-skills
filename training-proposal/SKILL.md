---
name: training-proposal
description: Draft AI training proposals and outlines from unstructured notes, convert markdown proposals to branded PDF, read existing .pdf proposals for reference. Covers client proposals, training outlines, workshop syllabi, bootcamp outlines, course proposals, session agendas, curriculum design, pricing quotes, and scoping for AI Builder Academy (ABA).
---

# Training Proposal Skill

Draft, edit, and convert AI training proposals for Shaw's consulting clients. All proposals are branded under **AI Builder Academy (ABA)**.

## Workflow

1. **Gather info** from the user (or unstructured notes)
2. **Draft markdown** following the example proposal structure
3. **User reviews/edits** the markdown
4. **Convert to PDF** using the bundled pipeline

## Reading Existing Proposals

When the user wants to reference a past proposal:

- **PDF files**: Extract text with the read-pdf script:
  ```bash
  cd ~/.claude/skills/training-proposal/scripts && uv run python read-pdf.py /path/to/proposal.pdf
  ```
- **.pages files**: Most past proposals have a PDF version alongside the .pages file. Use the PDF with read-pdf.py.

Keep past proposals in a consistent location, organized by client (one folder per client).

## Updating an Existing Proposal

When the user wants to revise a draft, read the existing markdown, make targeted changes, and re-save. Don't regenerate from scratch.

When you change a value that appears in more than one place — durations, session counts, titles, structural terms — update every instance: the syllabus Duration field, session headers, the Investment table rows, the Total, and payment terms. Numeric totals especially must reconcile (the sum of session durations equals the stated total). A priced document loses trust the moment the arithmetic doesn't add up, so re-check the math after any duration or pricing edit.

## Drafting a Proposal

Gather these details from the user (ask for anything missing):

- **Client name**
- **Training title**
- **Number of sessions** and **duration per session**
- **Delivery method** (e.g., Microsoft Teams, Zoom, in-person)
- **Topics per session** (or general themes to flesh out)
- **Pricing** — Shaw's standard rates: **$2,500/hr** for prepared content (lectures, webinars, custom sessions), **$1,000/hr** for no-prep (workshops, office hours). For custom sessions, calculate price as `duration_hours × hourly_rate`. Ask the user which rate tier applies to each session.

  Recurring session formats have go-to flat rates (round numbers, not strict `duration × rate`). Short and done-for-you sessions are priced as packaged minimums:

  | Session type | Standard rate |
  |---|---|
  | All-hands kickoff (short, prepared) | $2,500 flat |
  | Cohort breakout / done-for-you live build (~90 min) | $5,000 |
  | Office hour / follow-up (~30 min, no-prep) | $1,000 |

  Note the 90-min done-for-you build is a premium over the `$2,500/hr` prepared rate, and short sessions use a flat minimum rather than a prorated hourly figure. These are starting points to confirm with the user, not fixed outputs.
- **Discount** — When a discount applies, list sessions at full standard-rate prices and add a discount row in green: `| <span style="color: #2E7D32">*Discount*</span> | | <span style="color: #2E7D32">*-$X*</span> |`. The Total row reflects the discounted price.
- **Dates** (or TBD)

**Structure:** Engagements can be multiple sessions or a single session with multiple parts (using `### Part 1:`, `### Part 2:`). The syllabus Duration field should reflect this (e.g., "1 session (3.5 hours total)" or "4 sessions (90 min each)").

Follow the structure in the reference examples and adapt to match the client's needs:
- `references/example-proposal.md` — Acme Corp: multi-session engagement with lecture and breakout sessions
- `references/example-proposal-techstart.md` — TechStart: single session with 2 parts, discount row, upfront payment
- `references/example-proposal-globex.md` — Globex: cohort onboarding engagement with non-session sections (Intake Form, Logistics/Prerequisites, Additional Deliverables) and a Qty-column Investment table that collapses repeated sessions (`N | $total ($unit ea)`) and uses `Included` for no-charge items

Save to a consistent location for your client files (e.g., `clients/<client>/ai-training-outline_<client>.md`).

When a client gets multiple offering variants or revisions, suffix the filename — variant first, then version: `ai-training-outline_<client>_<variant>.md` (e.g., `_team`, `_1on1`), and `_v2`, `_v3` for major revisions (e.g., `ai-training-outline_globex_team_v2.md`).

Tell the user to review the markdown before PDF generation.

## Voice & Style

A proposal is a spec, not a pitch. The deal sells itself through clear structure; persuasion belongs in the cover email and the live conversation. Write to define what happens, and cut anything whose job is to convince or impress. Drafting in this voice up front saves the user from stripping it down later.

- **Compress to the outcome.** State the result; don't explain the mechanism inside it. "Each participant builds one skill relevant to their work" beats "three skills built live (12 total), drawn from the intake form, plus one built as homework."
- **One idea per sentence.** Any punctuation that fuses two clauses into one breath (em-dash, semicolon, comma-splice) is a signal to split into two sentences or cut the trailing clause. A period is almost always the fix. (Shaw reliably edits these out.)
- **No em dashes or en dashes, anywhere.** Not in prose, not in headers, not as table placeholders. Shaw strips them from nearly every proposal because they read as AI-authored, so write without them from the start. Replace a prose em dash with a period, comma, or colon. Write number ranges with a hyphen ("2-3 skills", "3-4 participants"), not an en dash. Use "n/a" for an empty Investment-table cell, not "—".
- **Cut rationale and framing.** A well-ordered agenda argues for itself. Don't narrate why it's structured that way ("no demos here, those come later") or add an "Our Approach" essay. Meta-commentary reads as insecurity about the structure.
- **The client is the hero, not the instructor.** Demote yourself as the actor, promote the team as the one who acts and benefits. You get the work verbs (instruct, demo); they get the outcome verbs (learn, build, share). Prefer "skills the team can build" over "skills to build," and "Instructor builds…" over "I build…".
- **Don't tally or label-inflate.** Counts ("12 skills!") and marketing terms ("done-for-you") signal salesmanship and quietly commit you to numbers. Promise the minimum you can stand behind.
- **Name things plainly.** Calm, true nouns over benefit-reaching labels: "Onboarding Claude to Globex" over "Delegating Work to Claude for Teams."
- **Say each thing once.** If info already lives in its natural place (the table, the body), don't echo it in the overview or repeat structural prefixes ("Session 1:") that the ordering already conveys.
- **Spend words only where they're load-bearing.** Ruthless on adjectives, precise on commitments and logistics. Hard constraints like "filled out no later than 7 days prior" or "30-minute debrief" earn their length because they protect delivery.

Rhythm: short, present-tense, subject-verb-object declaratives. Modest active voice. No stacked "which/that" clauses.

## Converting to PDF

Before converting, verify:

- Each session's timed segments sum to its stated duration.
- The Investment table durations and quantities reconcile to the headline **Total** (both hours and price).
- **Optional or unbilled segments** (e.g., "optional 15-min Q&A after the session") are excluded from billed durations and the Total. The same duration reads identically in the session header, the Investment row, and the Total.
- Titles, durations, and structural terms read identically everywhere they appear.

After the user approves the markdown:

```bash
cd ~/.claude/skills/training-proposal/scripts && uv run python md-to-pdf.py /path/to/outline.md
```

The PDF is created in the same directory as the markdown file, with the same base name (`.md` → `.pdf`).

## Formatting Notes

These conventions aren't obvious from the example alone — follow them for correct PDF rendering:

- Syllabus uses HTML `<table class="syllabus">` with `<tr class="spacer">` to separate title/instructor from dates/logistics (not a markdown table)
- Use `TBD` for unknown dates/times — it gets highlighted in red in the PDF
- Each session's timed segments should add up to the session duration
- Session content uses: `- **Section** *(15 min)*` with nested bullets for subtopics
- Use `---` horizontal rules between sessions
- Use `<div class="page-break"></div>` before the Investment section to force a page break
- Inline HTML like `<span style="color: #2E7D32">` works inside markdown table cells for colored text (e.g., discount rows)
- Investment table goes at the end with a bold **Total** row — use consistent unit formatting across all rows
- Prepared-by line format: `*Prepared on <date> by Shaw Talebi, PhD*` (italicized, includes date)
- Payment terms go after the Investment table as a `### Payment terms` subsection with bold bullet labels
