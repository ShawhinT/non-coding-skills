# Context Sections

How to write the `## Context` section of a record's page body. These conventions are not
CRM-specific: they apply to any Notion record that carries one, including Reviews/Referrals
rows, Engagements, and **ABA Calls pages** (added 9/18/26, when that database's Calendly-form
properties were retired into page bodies).

**On an ABA Calls page, `## Context` sits above `## Pre-Call Research`, and the two divide by
durability.** Context holds what is still true at the *next* call — intake answers, the
business, the audience, how they found Shaw. Pre-Call Research holds disposable prep for *this*
call — the Read, the fresh email thread, the questions. Without that line the two sections
collide, because both answer "what do we know going in."

One consequence worth stating: a fact that appears in both is not a defect to clean up. The
9/18/26 migration deliberately left duplicated phrasing inside Pre-Call Research rather than
let an agent reword Shaw's research prose. Duplication there ages out on its own; a bad
clause-level rewrite does not. The general form, for any migration that moves content
into Context: **remove whole lines, never clauses.** A standalone line that now duplicates a
Context bullet can go; a clause sitting inside a sentence Shaw wrote stays, because removing it
means rewriting his sentence, and whoever is doing the migration is the worst-placed person to
judge whether the rewrite still says what he meant. Expect the split to favor clauses — in the
9/18/26 pass only 4 of 21 candidate removals were clean lines — which is why "de-duplicate the
body while you're in there" is a much larger ask than it sounds, and worth quoting back before
agreeing to it. The skill that owns the record decides *which* sections exist and what
sits alongside Context; this file governs what goes *inside* it.

A Context section exists to be scanned in the two minutes before Shaw acts on the record. Every
rule below follows from that.

**Context is a bullet list, not prose.** Prose paragraphs and `###` subheadings defeat the
purpose: a wall of well-organized paragraphs takes longer to scan than the transcript it was
summarizing. **Bold the label that opens each bullet** — `**Role:**`, `**Arrangement (7/30):**`,
`**Open items:**` — so the eye lands on structure. That is not the same thing as a bolded
pseudo-header sitting above a paragraph, which is the failure mode to avoid: the bold belongs
*inside* the bullet, as its label. Reference record:
[Person](https://app.notion.com/p/[page-id]).

**A bullet is a fragment, not a sentence.** The keep-filter below decides *which* facts survive;
this decides how each one is written, and a record can pass the filter and still read as prose.
The tell is a clause that draws the conclusion for him — "owns the reps who would take the
training, **so he controls both the use cases and attendance**" — or that thinks out loud —
"**presumably** owns the other sales team. Which team he covers is still unconfirmed", where
`[Person] — co-addressee, silent. Team? unconfirmed` says the same thing. State the fact and
stop; he draws the implication faster than he reads yours. The full check list is under
"Writing page bodies" in `notion-helper`, which governs every page body in the workspace.

**The filter: keep what Shaw could not reconstruct by opening the linked source page.** For a
CRM record that's the call page; for a Reviews/Referrals row it's the call page, the form
response, or the sent thread. Nearly everything durable was said somewhere else, so origin isn't
the test — the test is whether he'd have to open that page to act. Shaw's own positions,
rationale, and arguments are recap: the *conclusion* stays in Context, the reasoning behind it
stays on the source page. He already knows why he holds his own positions, and re-litigating
them in Context is what makes a record read as a transcript.

Shape:

1. **Contact lines** — LinkedIn, phone, email. On records where the channel matters (anywhere an
   ask or a nudge gets sent), say which channel the person actually replies on and what the
   evidence is; a channel nobody has tested is a guess, and a dead one is why records go stale.
2. **One `Role:` line** — title, company (linked to its Companies row when it has one, otherwise plain text with its site), size, and what they sell, in a clause. The
   relevance to Shaw is why the line is there, not extra text to add: "what they sell and why it
   matters" invites a second sentence arguing the first. Not accolades, office lists,
   subsidiaries, or prior employers; that's recoverable from LinkedIn and changes nothing about
   the next conversation.
3. **Stakeholder lines**, one per person — `Name (Role): email — what they control, short read`.
   A person row lists the colleagues who matter to *their* thread (an EA who owns the
   calendar, a co-decision-maker); the full stakeholder map for the account lives on the
   Companies page's Context, written once rather than on every person row.
4. **Durable state** — the arrangement, the constraints, the figures quoted. Nest sub-bullets
   under a label when one heading genuinely has parts (`**Constraints:**` with three beneath it).
   Nesting for legibility is good; group by topic freely.
5. **`Open items:`** last, as a nested list.

**Newest does not go first.** The shape above is the order, and within it a record reads as a
picture of the relationship rather than a changelog — durable facts at the top, the pending
decision at the bottom under `Open items`. Leading with the latest conclusion inverts that and
buries the facts the conclusion rests on.

**`Open items` means an owner and a next action.** Not open questions, not unknowns, not
analysis, and not anything a linked source page or a `Next Contact` date already implies — a
booked session does not need a line announcing it's booked. "[Person] + [Person 2] owe a preferred
configuration, ball is in their court" is an open item. "The margin has never been named" is an
unknown, and belongs in the `Arrangement:` line if anywhere. "Free 1:1 set for 8/15" is already
legible from the linked call page.

**Date-stamp figures and negotiable terms, nothing else.** `**Quoted (7/30):**` and
`**Arrangement (7/30):**` carry dates because a stale price or a shifted deal shape is
expensive to get wrong. Constraints, role, contact, and stakeholder lines don't. Dating every
line turns Context into a version history of the record rather than a picture of the
relationship — which is exactly how the section bloats.

**A figure is dated from when it was quoted, not when it was agreed.** The date answers "how
stale is this number," and a price starts aging the moment it goes in front of someone —
whether they accept it that day or three weeks later. So a $6,000 engagement proposed 5/29 and
closed 6/3 reads `**Engagement (5/29):**`, with the close date inside the line if it's worth
keeping. `**Arrangement:**` follows the same logic: date it from when the shape was proposed,
not ratified. The two dates often coincide, which is why the convention only shows its value on
the records where they don't.

**Where the quote date genuinely isn't recorded, leave the label undated and say so inside the
line** — `no quote date on record`. That reads as a known gap; a guessed date reads as fact.
Before concluding it's unrecorded, check the linked call page and the outbound proposal email,
because "Shaw to send proposal" on a call page means the call is *not* the quote date.

**No length ceiling.** Length falls out of the filter rather than being budgeted. A record with
twelve things that survive it gets twelve bullets; most land well under. When a section feels
long, apply the filter harder — don't trim to a number.
