<!--
CANONICAL FORMAT REFERENCE (not a real proposal).
This file demonstrates every structural/formatting pattern a proposal can use.
It carries NO real copy. For the actual wording and content to start from, clone
the most recent live proposal of the matching offering type under
~/Documents/_stv/_ABA/proposals/. Use THIS file only to get the
table shapes, table classes, spacers, page breaks, and table math right.
Each <!-- ... --> note explains the pattern on the line(s) below it; delete all
notes in a real proposal.
-->

# <Offering> - <Client>

<!-- Prepared line: italic, includes the date. Always present, right under H1. -->
*Prepared on <Month D, YYYY> by Shaw Talebi, PhD*

---

## Overview
<!-- Heading is "Overview" or "Syllabus" (either is fine, match the cloned base). -->

<!--
Syllabus block is RAW HTML, not a markdown table.
- <tr class="spacer"> inserts the gap that separates the title/instructor group
  from the dates/logistics group.
- Use TBD for any unknown value (renders highlighted red in the PDF).
- Row set is flexible: include the rows that apply (Date(s), Session Time(s),
  Duration, Location, Participants, Prerequisites). Escape & as &amp;.
- Duration row mirrors the engagement shape, e.g. "4 sessions (90 min each)"
  or "1 session (3.5 hours total)".
-->
<table class="syllabus">
<tr><td><strong>Training Title:</strong></td><td><Title></td></tr>
<tr><td><strong>Instructor(s):</strong></td><td>Shaw Talebi</td></tr>
<tr class="spacer"><td colspan="2"></td></tr>
<tr><td><strong>Date(s):</strong></td><td>TBD</td></tr>
<tr><td><strong>Duration:</strong></td><td><N sessions (90 min each)></td></tr>
<tr><td><strong>Location:</strong></td><td><Remote (Zoom) / Microsoft Teams / in-person></td></tr>
</table>

---

<!-- OPTIONAL prose sections. Include the ones the engagement needs, drop the rest. -->

## Engagement Goal
<!-- Numbered list of concrete outcomes the client walks away with. -->

By the end of the engagement:

1. <Outcome one.>
2. <Outcome two.>
3. <Outcome three.>

---

## Sessions

<!--
SESSION HEADERS come in two shapes. Pick one per proposal:
  (A) Multi-session:        ### Session N: <Title> (90 min)
  (B) Single session, parts: ### Part 1: <Title> (90 min)  /  ### Part 2: ...
Non-session items (Intake Form, etc.) use a plain ### header with no duration.
-->

<!-- Non-session item example (no billed duration): -->
### Intake Form *(submitted 7 days before kickoff)*

<One or two sentences on what it captures.>

<!--
Timed-segment pattern: bold section name + italic duration, nested bullets for
subtopics. The segment durations MUST sum to the session's stated duration.
-->
### Session 1: <Title> (90 min)

- **<Section name>** *(15 min)*
    - <Subtopic>
    - <Subtopic>

- **<Section name>** *(75 min)*
    - <Subtopic>

<!--
OPTIONAL / unbilled segment: mark it clearly. It is EXCLUDED from the session
duration math and from both Investment totals. Not the same as an "Included"
line item (see Investment notes).
-->
- **Optional Q&A** *(15 min, after the session)*

---

<!-- Repeat sessions, separated by --- rules. -->
### Session 2: <Title> (90 min)

- **<Section name>** *(15 min)*
    - <Subtopic>

- **<Section name>** *(75 min)*
    - <Subtopic>

---

<!-- OPTIONAL: extra deliverables / logistics, when relevant. -->

### Additional Deliverables

- <Deliverable, e.g. a post-engagement debrief or one-page memo.>

---

## Logistics

- **Prerequisites:** <accounts/tools participants need.>
- **Scheduling:** <how sessions get booked.>

<!-- Force the Investment table onto its own page. -->
<div class="page-break"></div>

## Investment

<!--
TWO table shapes. Use the SIMPLE 3-column form when every line is distinct.
Use the QTY form when a line repeats N times at one unit price (collapse it).

Total math, two independent axes:
  - Total Duration = sum of EVERY stated Duration cell, INCLUDING `Included`
    rows that have a real duration. Only `n/a`-duration rows are skipped.
    Optional/unbilled segments above are NOT line items, so they never count.
  - Total Price = sum of the dollar rows only; `Included` adds $0.
Use consistent unit formatting across rows. Use "n/a" for an empty cell (never a dash).
-->

<!-- SIMPLE form: -->
| Session | Duration | Price |
|---|---|---|
| Session 1: <Title> | 90 min | $X,XXX |
| Session 2: <Title> | 90 min | $X,XXX |
| **Total** | **N hours** | **$XX,XXX** |

<!--
QTY form (collapses repeats as `N | $total ($unit ea)`), with an `Included`
deliverable and an `n/a` duration cell:

| Item | Duration | Qty | Price |
|---|---|---|---|
| <Repeated session> | 90 min | 4 | $20,000 ($5,000 ea) |
| <Bundled deliverable> | 30 min | 1 | Included |
| <No-duration deliverable> | n/a | n/a | Included |
| **Total** | **N hours** | | **$XX,XXX** |
-->

<!--
DISCOUNT row (green, italic): list line items at full price, add a plain
Subtotal row with the full price, then subtract. The Total reflects the
discounted price.

| Subtotal | | $X,XXX |
| <span style="color: #2E7D32">*Discount*</span> | | <span style="color: #2E7D32">*-$X,XXX*</span> |
-->

### Payment terms
<!--
Bold label + parenthetical timing. Common variants:
- **Full payment** (no less than) 24 hours before the first session
- **Initial 50% payment** (no less than) 7 days before Session 1
- **Final 50% payment** (no more than) 14 days after the final session
Always close with the payment method line below.
-->
- **<Payment label>** (<timing qualifier>) <when>
- **Payment method:** Stripe invoice, payable by direct deposit, debit card, or credit card
