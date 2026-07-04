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

**First, find the best base to start from.** Before writing anything, look across *all* client folders in your proposals directory, not just the current client's, and pick the **most recent proposal of the same offering type** to use as the template. The newest proposal of a given type carries the latest copy refinements (wording, structure, section names), so starting there beats both the current client's older draft and the content-free `references/format-reference.md` (which is for format, not copy).

To do this:
1. List the proposal folders and their `.md` files with timestamps. Filenames vary: most follow `ai-training-outline_<client>_<variant>.md` (variant `_1on1`/`_team`, version `_v2`), but some are named descriptively after the offering (e.g. `team-claude-workshops_acme.md`). Glob *all* proposal markdown, not a single prefix: `ls -lt **/*.md`. Read the offering type from filename keywords (`team`/`cohort` vs `1on1`/`1:1`) or by opening the file. Don't filter on the `ai-training-outline_` prefix, or you'll silently miss the most recent base when it was renamed.
2. Match on offering type: a 1:1/2:1 workshop request should clone the most recent `_1on1` outline (e.g., [Company A]'s was the freshest when drafting [Company B]'s), a cohort/team rollout the most recent `_team`, and so on.
3. Read that file, then adapt it to the new client: swap names, participant groupings, delivery method, dates, and pricing. Preserve its refined copy unless the new engagement calls for different wording.

Confirm the chosen base with the user if it's ambiguous which prior proposal is the closest match.

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

**Flexible-scope pricing (count or timing undecided).** When the engagement's exact scope is still open, don't pin a single headline Total. Price by building block: an Investment table that lists each unit (a workshop, a 1:1 prep, a follow-up) at its unit price, followed by two anchored *example scopes*, a smaller and a larger configuration, each with its own reconciled Total. Two anchors let the reader infer the in-between cost without you enumerating every option. If a unit price hinges on a term that could be read two ways (per-team vs per-session), define that term in plain language right before the table (e.g. "a *team* is a function. a *group* is a scheduled session of that team."). See the most recent flexible-scope proposal for a worked example.

Two sources, two jobs:
- **Content/copy** comes from the most recent live proposal of the matching offering type (the "find the best base" step above). Clone its wording and structure.
- **Format/structure** is defined once in `references/format-reference.md`, a content-free skeleton that demonstrates every pattern with inline notes: both syllabus headings, the spacer row, multi-session vs single-session-with-parts headers, timed segments, optional/unbilled segments, the page break, both Investment table shapes (simple 3-column and Qty-column collapse `N | $total ($unit ea)`), `Included` and `n/a` cells, the green discount row, and the payment-term variants. Consult it whenever you're unsure how a structural element should be written. It is the fallback base when no live proposal of the needed type exists yet.

Save to: `<proposals-directory>/<client>/ai-training-outline_<client>.md`

When a client gets multiple offering variants or revisions, suffix the filename — variant first, then version: `ai-training-outline_<client>_<variant>.md` (e.g., `_team`, `_1on1`), and `_v2`, `_v3` for major revisions (e.g., `ai-training-outline_acme_team_v2.md`). Shaw sometimes renames a proposal to a descriptive, offering-led name (e.g. `team-claude-workshops_acme.md`). That's fine, and it's why the discovery step globs all `.md` rather than a fixed prefix.

Tell the user to review the markdown before PDF generation.

## Voice & Style

A proposal is a spec, not a pitch. The deal sells itself through clear structure; persuasion belongs in the cover email and the live conversation. Write to define what happens, and cut anything whose job is to convince or impress. Drafting in this voice up front saves the user from stripping it down later.

- **Compress to the outcome.** State the result; don't explain the mechanism inside it. "Each participant builds one skill relevant to their work" beats "three skills built live (12 total), drawn from the intake form, plus one built as homework."
- **One idea per sentence.** Any punctuation that fuses two clauses into one breath (em-dash, semicolon, comma-splice) is a signal to split into two sentences or cut the trailing clause. A period is almost always the fix. (Shaw reliably edits these out.)
- **No em dashes or en dashes, anywhere.** Not in prose, not in headers, not as table placeholders. Shaw strips them from nearly every proposal because they read as AI-authored, so write without them from the start. Replace a prose em dash with a period, comma, or colon. Write number ranges with a hyphen ("2-3 skills", "3-4 participants"), not an en dash. Use "n/a" for an empty Investment-table cell, not "—".
- **Cut rationale and framing.** A well-ordered agenda argues for itself. Don't narrate why it's structured that way ("no demos here, those come later") or add an "Our Approach" essay. Meta-commentary reads as insecurity about the structure.
- **The client is the hero, not the instructor.** Demote yourself as the actor, promote the team as the one who acts and benefits. You get the work verbs (instruct, demo); they get the outcome verbs (learn, build, share). Prefer "skills the team can build" over "skills to build," and "Instructor builds…" over "I build…".
- **Don't tally or label-inflate.** Counts ("12 skills!") and marketing terms ("done-for-you") signal salesmanship and quietly commit you to numbers. Promise the minimum you can stand behind.
- **Name things plainly.** Calm, true nouns over benefit-reaching labels: "Onboarding Claude to [Company]" over "Delegating Work to Claude for Teams."
- **Say each thing once.** If info already lives in its natural place (the table, the body), don't echo it in the overview or repeat structural prefixes ("Session 1:") that the ordering already conveys.
- **Spend words only where they're load-bearing.** Ruthless on adjectives, precise on commitments and logistics. Hard constraints like "filled out no later than 7 days prior" or "30-minute debrief" earn their length because they protect delivery.

Rhythm: short, present-tense, subject-verb-object declaratives. Modest active voice. No stacked "which/that" clauses.

## Converting to PDF

Before converting, verify:

- Each session's timed segments sum to its stated duration.
- The Investment table reconciles to the headline **Total** on both axes, and the two axes are independent:
    - **Total Duration** = the sum of every stated duration in the Duration column, including rows priced **Included**. An `Included` deliverable with a real duration (e.g., a 30-min Check-In Call) is committed delivery time, so its minutes count toward the Total hours even though it contributes nothing to the price. Only rows with no stated duration (`n/a`) are skipped.
    - **Total Price** = the sum of the dollar rows only. `Included` rows contribute nothing to the price.
    - Worked example: 3 x 90-min workshops + a 30-min Included Check-In Call = **5 hours total** at the same workshop price (not 4.5 hours). The 4.5-hour answer is the classic mistake: don't drop an Included row's duration from the Total.
- **Genuinely optional segments** (e.g., "optional 15-min Q&A after the session") are the only thing excluded from both the Total duration and price. "Optional" means the client can decline it. It is not the same as "Included" (committed, no extra charge). The same duration reads identically in the session header, the Investment row, and the Total.
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
- For an asterisk note under a session (a caveat about how a segment works), wrap it in `<p class="footnote">...</p>`. The `.footnote` class in `style.css` renders it ~20% smaller and gray, so it reads as a subordinate note rather than body copy
- Investment table goes at the end with a bold **Total** row — use consistent unit formatting across all rows
- Prepared-by line format: `*Prepared on <date> by Shaw Talebi, PhD*` (italicized, includes date)
- Payment terms go after the Investment table as a `### Payment terms` subsection with bold bullet labels
