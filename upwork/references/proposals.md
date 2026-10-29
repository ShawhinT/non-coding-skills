# Drafting the Proposal

Everything Phase 2 needs that isn't the loop itself. Read this before extracting questions, not
after — the proof-sourcing rules change what you look for while reading the posting.

---

## The letter

A posting worth applying to was written by someone who spent real effort specifying what they
want, and who is now reading 20 to 50 replies. Both halves matter: they will read a long letter,
and they will read it fast. The shape that survives both is a short body over a long answers
block, so the skim gets the recommendation and the careful reader gets everything.

**First, let the posting choose the shape.** Many postings list what a proposal must contain.
That list *is* the body's structure, in its order: the buyer wrote it, and they read every reply
against it, so a letter organized any other way makes them do the matching. The five beats below
are the default for a posting that specifies nothing — and even then, beats that the posting's own
asks already cover get folded into those asks rather than repeated.

When a posting's asks exceed what the letter can hold, the required-contents list wins the body and
everything else (screening questions, extra detail) goes below the divider or into a separate
application field.

**Body** — five beats, roughly 300 to 350 words:

1. **Hook.** The direct answer to whatever the posting is actually anxious about — which is
   something to locate in their text, never a default to apply. It is usually written down
   somewhere: a "definition of success" section, a line about what they want to be able to do
   afterwards, a sentence naming what went wrong last time. Read for the sentence they'd have
   deleted last. Feasibility is rarely it; a posting drawing dozens of proposals and live
   interviews has no doubt anything is possible. And an opener that concedes a point in order to
   take it back ("yes, but…") argues with itself in the two lines that matter most.
2. **Recommendation.** The concrete shape of the engagement: what happens, in what order, how
   long. This is the only place structure beats prose.
3. **Social proof.** Volume first ("I've run 35+ of these in the past year"), then the typical
   outcome, then three specific wins as bullets.
4. **Links.** Two, maximum. One video that matches the buyer's avatar, one page of client
   results. More than two reads as a content dump.
5. **CTA.** A Calendly link phrased as a question, closing on the escape hatch. `email-helper`
   owns both conventions.

**Then a divider and `ANSWERS TO YOUR QUESTIONS`**, one short block per question in posting order,
each under a bolded label. This is where the letter earns the bid: nobody else answers the
questions, and a buyer who wrote a careful spec notices.

Two structural notes worth holding:

- **Proof sits next to the claim it backs, not clumped at the end.** If the letter claims skills
  make work durable across a team, the client who built an internal skill library belongs in that
  paragraph, not in the bullet list four beats later.
- **The answers block can reference the body.** "That's what we set up in the session with the
  Director of Finance above" is stronger than repeating her story, and it makes the two halves
  read as one argument rather than a letter with an appendix.

**Lead with the answer, not the credential.** The opener that wins is the one doing the buyer's
work for them — a real read on their problem, given away before anything is asked. Opening on
volume or client names instead is the move every other bidder makes.

---

## Extracting the questions

**Most postings contain no question marks at all.** Every ask arrives phrased as a stated need —
"Claude Team: administration, seats, and how the plan differs from individual use," "we'd want
your read on the practical options." The extraction job is converting needs into questions, and
it is worth doing explicitly rather than in your head, because the numbered list is what Shaw
dictates against.

Sweep for four kinds of ask, in posting order:

- **Listed coverage areas.** Usually bulleted, usually the bulk of them.
- **The buried real question.** Often one paragraph deep in the middle, phrased as context rather
  than a request. It is almost always the one that decides the bid.
- **The framing question.** "What's possible, what isn't, where the real limits are" — the thing
  they'd say the whole engagement is for.
- **Logistics.** Availability, rate, timeline, location constraints.

Return them numbered and nothing else. Say plainly that the posting had no literal questions, so
Shaw knows the list is a reading rather than a transcription and can correct it.

**Screening questions live behind Apply.** Upwork lets clients attach questions that render only
on the application page, never the public posting. Flag this every time; you cannot see them.

---

## Pulling the proof

Three databases, three different jobs. Always query; never reconstruct from memory.

**A database row is a summary, not the event.** Wins rows, CRM notes and scraped site copy are all
written after the fact and drift from what happened — a Wins row can flatly contradict the email
Shaw sent the next morning, and a page of testimonials read in bulk will merge one client's result
onto another's name. Neither announces itself as wrong. So before a claim about *what happened in a
session* reaches a buyer, confirm it against the primary record: the thread in Gmail, or the
transcript. A misattributed client result is the one error in a proposal that can't be walked back
on the call.

| Need | Source | Notes |
|---|---|---|
| A verbatim client outcome | 🏆 Wins, `collection://[page-id]` | Filter on `Avatar` to match the buyer. Bodies carry the unsmoothed quote and a Context line saying what produced it. Schema and capture rules live in `convo-mining` |
| A quotable testimonial | Reviews/Referrals, `collection://[page-id]` | `Review Status = Published` or `Approved` only. `reviews-referrals` owns the lifecycle |
| A volume count | 🏫 ABA Trainings, `collection://[page-id]` | Rows are named by offer, so filter on the title, not just `Call Type` |

### Choosing which wins

Match the buyer on **avatar and use case, in that order**. A finance leader's win lands harder
with a President and Controller than a more impressive win from an engineering leader.

The strongest possible proof is a published testimonial whose *before-state* mirrors the posting's
present tense. When one exists, it does more work than any three wins, and the rest of the letter
should be built around it.

Reserve two or three wins you don't use. They're what the interview is for, and a client whose
situation matches structurally (multi-location books against a multi-location buyer) is worth
holding even when the headline number is smaller.

### Counting rules

Counts are the easiest thing in a proposal to overstate by accident:

- **Exclude future-dated rows**, rows from a different offer, and internal or family sessions.
- **Round down.** A "35+" that's true beats a "38" that needs a caveat.
- **Sessions and people are different numbers.** A 2:1 session is one session and two people. Say
  which one you're claiming.
- **Check when the database starts.** A count that's true "in the past year" but actually
  concentrated in five months is a stronger claim stated the second way, and equally honest.

### Anonymity is per client, not a blanket rule

Some clients are named publicly on aibuilder.academy; others appear on the same page anonymized by
role and industry. The published testimonial is the authority. A client anonymized there stays
anonymized everywhere, including in a proposal a stranger reads, and including the company name in
passing. Check the site before naming anyone.

### Every claim carries a source

Deliver the proposal with a table mapping each claim to the row that backs it, so Shaw can defend
any of them on the call. Anything you couldn't source — a detail he supplied verbally that the
record contradicts, a number he'd know but you can't verify — gets flagged as unsourced rather
than quietly included. That flag is the deliverable's most useful line.

---

## Upwork submission mechanics

Five things about the platform that shape the letter itself:

- **The proposal box is plain text, and caps at 5,000 characters.** Markdown does not render — no
  bold, no headers, no tables — so structure comes from line breaks, capitals, and a divider. The
  cap is the bigger constraint: it decides what the letter can carry, so check the draft's length
  early rather than writing to fit and trimming after. Deliver the file unwrapped, since hard line
  breaks survive the paste and shred the formatting.
- **Application questions are separate fields with their own budgets.** A posting's "you will be
  asked to answer" questions render only on the application page and don't spend the letter's
  5,000 characters. Answer them so they complement the letter rather than repeat it — the client
  reads both side by side.
- **The rate is a separate form field**, and on an hourly post it wants an hourly number. Leaving
  price out of the letter costs nothing, but the field is the first thing the client sees and the
  thing they filter on.
- **External links can be redacted**, and moving a client off-platform before a contract exists
  is against Upwork's terms. A scheduling link for an interview is the gray part of that rule
  rather than the clearly-prohibited part, but it's their judgment, not Shaw's. Always offer the
  fallback: drop the link, offer to find a time, send it once they reply in Upwork Messages.
- **The client block is context for the letter, not just the sweep.** A brand-new account with no
  spend history, a stale last-viewed date, and someone already interviewing is worth saying out
  loud so Shaw can price his effort accordingly.

---

## The rate gap

Phase 1's standing finding is that Upwork buyers pay far below ABA's rates — clients with real
spend history average $37 to $48/hr paid, against a $1,500 workshop and a ~$6K entry contract. So
on almost every posting worth applying to, Shaw's real pricing will sit several multiples above
the advertised band. This is structural. Don't rediscover it each time, and don't let it silently
shape the letter.

Compute the effective hourly (package total ÷ hours proposed) and state it against their band.
Then lay out the three plays rather than choosing for him:

- **Bid the real number.** Honest and consistent. Most likely filtered before anyone reads.
- **Bid at the top of their band, real structure in the letter.** Gets read. But a band-rate field
  above a package several times larger reads as bait once the buyer does the arithmetic.
- **Bid at the top of their band, no figures in the letter, free intro call as the only ask.**
  Weakest answer to "what's your rate," strongest at getting the call.

The third is usually right, and the reason is worth saying: the buyer asked for a rate, but what
they want to know is whether Shaw is worth an hour. A free call answers that better than a number,
and the 1:1 workshop is an attraction offer rather than the thing revenue is optimized on.

Whichever he picks, the letter and the rate field have to tell the same story.
