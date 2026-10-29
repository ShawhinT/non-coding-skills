<!--
CANONICAL SOW FORMAT REFERENCE (not a real SOW).
This file demonstrates the structural patterns a Statement of Work uses beyond
the proposal patterns in proposal-format-reference.md. It carries NO real copy. For the
actual wording to start from, clone the most recent live SOW under
~/Documents/_stv/_ABA/sow/. Same pipeline and same style.css as
proposals. Each <!-- ... --> note explains the pattern below it; delete all
notes in a real SOW.
-->

# Statement of Work - <Client>

*Prepared on <Month D, YYYY> by Shaw Talebi, PhD*

---

## Overview

<!--
Syllabus block reused from proposals, but the rows name the PARTIES and TERM
(no spacer row). Defined terms get curly quotes as HTML entities
(&ldquo;ABA&rdquo;) because raw HTML skips the smart-quotes pass.
The SOW number lives in the Engagement row: <Offering> (SOW-NNN).
-->
<table class="syllabus">
<tr><td><strong>Engagement:</strong></td><td><Offering> (SOW-NNN)</td></tr>
<tr><td><strong>Provider:</strong></td><td>Shawhin Talebi Ventures LLC, d/b/a AI Builder Academy (&ldquo;ABA&rdquo;)</td></tr>
<tr><td><strong>Client:</strong></td><td><Legal entity name> (&ldquo;Client&rdquo;)</td></tr>
<tr><td><strong>Term:</strong></td><td><N months, start to end date></td></tr>
</table>

<!-- One-paragraph summary of the engagement, ending with the effectiveness
sentence (takes effect on last signature, expires at end of term unless
renewed in writing). -->
<One-paragraph engagement summary.>

---

<!--
NUMBERED H2 SECTIONS. The body cross-references them ("Section 2", "Section 6"),
so if a section is added or removed, every cross-reference must be re-checked.
Canonical order:
  1. Objectives  2. Services  3. Responsibilities  4. Fees & payment
  5. <Guarantee>  6. Intellectual property & confidentiality
  7. General terms  then unnumbered Signatures.
There is no standalone Out of scope section: a catch-all line inside Services
covers it (see below).
-->

## 1. Objectives

<!-- Goals cloned from the accepted proposal's Engagement Goal, plus the
directional-targets paragraph: targets are shared goals, not performance
obligations; services are complete when Section 2 is delivered. -->

## 2. Services

<!--
Markdown table, Service | Qty | Duration. No Price column: pricing lives only
in the Fees & payment section. Qty cells may be a number, `Unlimited`,
`Included`, or `As needed`. Directly under the table, one paragraph carries
the scoping process plus the out-of-scope catch-all (this replaces a
standalone Out of scope section). Follow with bold-label paragraphs
(**Delivery.**, **Transcripts & recordings.**) for delivery mechanics.
-->
| Service | Qty | Duration |
|---|---|---|
| <Recurring session> | 13 | 60 min |
| <Deliverable with no duration> | 3 | n/a |
| <Ongoing support line> | Unlimited | n/a |

<How services get scoped/prioritized.> Anything not listed above is out of scope. Additions can be agreed at any time in writing; email suffices.

## 4. Fees & payment

<!--
Installment table. Amounts sum to the bold Total. A discount is a green italic
note in the Total row's Due cell, not a separate row (the installments already
reflect the discounted amounts).
-->
| Installment | Amount | Due |
|---|---|---|
| 1 of N | $X,XXX | <date> |
| **Total** | **$XX,XXX** | <span style="color: #2E7D32">*<Rate note, e.g. Founding client rate (50% off $YY,YYY)>*</span> |

## 7. General terms

<!-- Bold-label paragraphs, one clause each: **Independent contractor.**,
**Publicity.**, **Warranties & liability.**, **Termination.**,
**Miscellaneous.** (governing law, entire agreement, survival). -->

---

## Signatures

<!--
Two borderless columns via table.signatures (style.css). Each cell: party
label, signature line, printed name with gray role, second line for date.
break-inside: avoid keeps the whole block on one page.
-->
<table class="signatures">
<tr>
<td>
<p class="sig-party">ABA</p>
<div class="sig-line"></div>
<p>Shawhin Talebi<br><span class="sig-role">Owner, Shawhin Talebi Ventures LLC</span></p>
<div class="sig-line"></div>
<p class="sig-role">Date</p>
</td>
<td>
<p class="sig-party">Client</p>
<div class="sig-line"></div>
<p><Signer name><br><span class="sig-role"><Title, Legal entity name></span></p>
<div class="sig-line"></div>
<p class="sig-role">Date</p>
</td>
</tr>
</table>
