# Surface: Meeting Transcripts

For a call that's already happened — a 30-minute sales call, a 1:1 training, a group workshop. The
shape of the work is identical across them; only the amount of reading changes.

Load the file for every database you're extracting for before step 3. Once the read starts, the bar
you're holding is whatever you loaded.

## 1. Find the transcript

`google-drive-helper` owns this — a Meet Doc usually titled
`[Name] / Shaw - [Type] - YYYY/MM/DD HH:MM TZ - Transcript`, though group sessions title themselves
less predictably. Search on the parts that hold: the trailing `- Transcript` and the date. Check
`fileSize` only to tell a real transcript from a no-show stub — a stub is ~1 KB, and anything
meaningfully above that is real. There's no upper bound worth checking.

Drive only holds Meet calls. A session held elsewhere has its transcript on its own ABA Calls /
Trainings page, in one of two forms: a Notion `<meeting-notes>` block (read with `include_transcript`),
or a transcript file Shaw attached under the page's `## Transcript` heading — a Zoom `.vtt` export,
typically. An attached file fetches as a `notion-file-block://` reference; `notion-get-file-download-urls`
turns it into a short-lived signed URL you can download from. Any of the three homes means the page
has its transcript.

**Who is on the call decides whether there is anything to mine.** Clients, prospects and workshop
participants talk about their own work, which is what these databases are for. Peers — other
consultants, trainers, networking contacts — mostly interview Shaw about his business, and all four
databases gate them out: Q&A and Wins on the relationship, ABA Q&A on whether a buying decision or a
referral partnership is live, Pain Points on whether the cost transplants. Check the speaker gates before reading rather than after; a good conversation with
nothing fileable in it is the expected outcome, not a failed extraction.

## 2. Stage it locally, verbatim

Pull the full text into a file in the working directory, without routing it through your own
output — re-emitting a transcript to write it out is the one step here that can silently corrupt
the verbatim text everything downstream rests on. An oversized connector read already persists to a
local file and returns the path; that copy is byte-exact. It is an envelope, though, not the
transcript — a Drive read lands as JSON with the text in a field, a Notion `<meeting-notes>` fetch as
a whole page with the transcript inside a `<transcript>` tag, a Zoom `.vtt` as numbered cues with
timestamps around each `Name: text` line. Pull it out with a script rather than
by hand, and write the derived plain-text copy your readers take line numbers from in that same
script: hand-extraction is the same corruption risk as re-emitting, just one step later. Note the
size, the line count, and the exact speaker-label format. Then verify each extracted quote against
the staged file before it reaches a proposal — a one-character slip inside a blockquote is
invisible in review and permanent once filed.

**Check whether the transcript has speaker labels before staging.** A Meet Doc prefixes every turn
with a name; a Notion `<meeting-notes>` block emits bare turn-separated lines, and adjacent turns
are sometimes merged or transposed so a reply appears above the question it answers. Unlabeled,
attribution is an inference from register — Shaw teaches and explains, participants describe their
own work — so ask each reader for a speaker *and* a confidence, and resolve the low-confidence ones
against the session page or batch them to Shaw instead of guessing.

Labels can also be present and wrong. Participants sharing one room and one microphone collapse into
whichever name the tool picked, so every turn from that room carries it — confidently, and with
nothing to signal the merge. Count the distinct labels against the people the session page says were
there before trusting any of them; when they disagree, the labelled transcript is really an unlabeled
one for those speakers, and the register-plus-confidence rule applies to every turn they own.

Transposition matters most for the disqualifiers that turn on who spoke first. Wins' "the speaker
claims it, not Shaw" is the one that bites: a participant's reaction sitting below Shaw's version of
the same observation may have come first, and cutting it as Shaw's framing throws away a real win —
so where order decides the row, read the neighbouring turns rather than trusting the seam.

## 3. Size the read to the transcript

Budget roughly 20 KB (~5K tokens) per reader. Under that, read it in one pass yourself — most
30-minute calls land here, and splitting them buys nothing but seams.

Over it, fan out one subagent per ~20 KB window with ~15% overlap, because an item straddling a
boundary vanishes otherwise. Give each agent the inclusion bar for **every** target database and
demand structured output: which database the item belongs to, a three-word title, the verbatim text,
the speaker label of whoever said it, and the **absolute** line number (tell each agent its offset;
they report relative numbers otherwise).

## 4. If you fanned out, verify the empty stretches

Any window returning few or no items gets a second agent whose only job is that window, told to be
*more* inclusive and to report what the stretch actually consists of. This distinguishes "extraction
failed" from "Shaw was talking / someone was screen-sharing" — different problems, indistinguishable
from a low count alone. Parallelization is the main source of error here, which is why it earns a
verification pass that a single-pass read doesn't need.

## 5. Dedupe on the payload, then apply the rules

Same item from two agents is one row — but match on the *body* text, not the title. Two agents
reading the same exchange routinely disagree about where it starts, one of them sweeping in a
preceding sentence, so they produce different titles while reproducing the same substance nearly
verbatim. A title key leaves those in; a body key catches them.

Then trim leading and trailing bleed — demo narration that drifted onto the front, the next activity
that drifted onto the end — and apply the three row-rules from SKILL.md plus each database's own
bar.

## 6. Sweep the set mechanically before you present it

Two checks cost nothing and catch what reading closely still misses at volume:

- **Any item attributed to Shaw** is either his own question to the client or a mis-attribution.
  Resolve it rather than writing it.
- **Any body under a sentence or two** is almost always a bare confirmation or a shrug ("That's my
  guess. unique users."). Read those before keeping them.

## 7. Present for review

Per SKILL.md — tier substantive vs thin, say what you'd drop and why, expect roughly a fifth to be
cut.

## Sessions with more than one participant

A group training has several distinct speakers, so carry each item's speaker label through to its
own `Person` / `Asker` — the field is per-row, not per-session, and one engagement covering six
people is still six different names.

Occasionally a participant answers another participant rather than Shaw. That's still a row worth
keeping, with the answerer named in the provenance line so the body isn't read as Shaw's words.
