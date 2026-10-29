---
name: "convo-mining"
description: "Mines Shaw's conversational records — meeting transcripts and client Slack channels — into structured Notion databases: what people asked, what they struggled with, and what results they reported. Load it whenever something someone said needs capturing, whenever a transcript or a channel needs mining, and before any read or write against them. Triggers: \"log this Q&A\", \"log this objection\", \"log this pain point\", \"log this win\", \"mine the transcript\", \"pull the questions from today's call\", \"what came up in the workshop\", \"extract the Q&A\", \"what did X ask\", \"any repeats\", \"that quote was gold\". Also fires when a training or sales call wraps, when someone reports a result, when a Slack sweep surfaces a question or a complaint, and whenever another skill (slack-helper, meeting-prep, engagements, sfc-helper, reviews-referrals) needs a database schema or the capture procedure. Do NOT use for drafting the answer or the post itself — the surface's own skill governs voice."
---

# Convo Mining

Turns conversational records into structured, verbatim rows in Notion.

Someone says something once, in a call or a channel, and then it's gone. Captured, it compounds —
as renewal evidence, as content raw material, as the signal that a topic has graduated into a skill
or a training module, and as a curriculum grounded in what people are actually stuck on rather than
what seems useful. That's why capture is half the job, not an afterthought.

Two surfaces today, three target databases. Both lists are meant to grow, and the structure below is
what lets them grow without a rewrite.

---

## How This Skill Is Organized

Everything true regardless of surface or target lives in this file. Everything specific to one
surface or one database lives in its own file.

**Surfaces — how to read a record:**

| Surface | Use when | File |
|---|---|---|
| Meeting transcript | A call already happened — sales call, 1:1 training, group workshop | `references/surfaces/transcripts.md` |
| Slack | A client channel needs sweeping, or one message needs capturing live | `references/surfaces/slack.md` |

**Databases — what a row is:**

| Database | Captures | File |
|---|---|---|
| 💬 Q&A | A question about AI someone asked and the answer Shaw gave | `references/databases/qa.md` |
| 🏷️ ABA Q&A | A question or objection about ABA's own offer, and Shaw's answer | `references/databases/aba-qa.md` |
| 💢 Pain Points | A pain, doubt, or frustration someone expressed | `references/databases/pain-points.md` |
| 🏆 Wins | A result or outcome someone reported from AI work | `references/databases/wins.md` |

**Load every database file you intend to extract for before the read starts — not just the surface
file.** A run that opens `transcripts.md` and `qa.md` but never opens `pain-points.md` produces Q&A
rows only and looks like it succeeded. Reading the record is the expensive step, you get one pass at
it, and the bar you're holding while you read is whatever you loaded beforehand. This is the most
likely way for this skill to fail quietly.

Adding a database later means adding a row to the table above and a file next to the others.
Nothing else in this file should need to change.

---

## The Shared Spine

Every target database carries these properties, with the same meaning and the same rules. Only the
title property's name and the database-specific fields differ — those live in the database files.

| Property | Type | How to fill it |
|---|---|---|
| *(title)* | Title | **Three words max.** A topic label, not a sentence — "Skills vs Obsidian", "Self-training burden", "MCP connector setup". It's an index entry; the body carries the detail |
| Date | Date | The date it was **said**, not the date you captured it |
| Source | Select | `Slack` / `Training` / `Call` / `Upwork` |
| Source Link | URL | Where it was said — see the table below |
| Person | Text | Whoever actually said it. On a forwarded or relayed message that's the original speaker, not the forwarder; in a group engagement it's the participant, not the payer |
| Company | Relation → Companies | The account the speaker belongs to — what lets the company page show everything its people asked, struggled with, and won. Empty for a solo client, a friend, a lone lead whose company has no row yet, or someone with no company |
| CRM | URL | The speaker's **own** record — their row in Clients (Nurture) or Active Leads, or their Friends row. Most participants at a client company have none, and that's correct: `Company` carries them. This link matters most when there is no company (a solo client, a partner, a friend, a lone lead), because it's then the only record the moment attaches to. Never point it at the buyer's row on a participant's behalf |

| Source | Source Link points at |
|---|---|
| Slack | The permalink in **Shaw's** workspace (`aibuilderacademy.slack.com/archives/...`) — never the client-workspace link, which he can't open |
| Training | The ABA Trainings page for the session — Notion-native, and it carries the pre-call research and the transcript |
| Call | The ABA Calls page for the call |
| Upwork | The job posting's own URL |

`Source` names the database the session page lives in: a page in ABA Calls is `Call`, a page in
ABA Trainings is `Training` — so a client check-in or weekly sync whose page sits in ABA Calls is
`Call`. Read it off the Source Link rather than judging the relationship: a value derived from where
the link points stays consistent across runs and can be audited and repaired mechanically, while a
judgment call drifts. Whether the speaker is someone Shaw sells or delivers to is a separate
question, answered by each database's gates, not by this field.

**Not every source is a conversation.** A question can arrive in writing from someone who never
spoke to Shaw — most often an Upwork posting, whose asks he answers in a proposal. Two spine rules
bend there and nowhere else: `Person` holds the role rather than a name (`Upwork client (President
& Controller)`), since there is no identified speaker; and the answer is Shaw's written reply
rather than a transcribed one, so it is already clean prose. Everything else holds, and the
provenance line carries the difference — say the answer was written rather than given live, and
whether the client ever replied. The verbatim rule still binds on the *question*: quote the posting
as written. `upwork` owns when this capture happens.

**The three-word cap is the clustering mechanism.** Similar items naturally get similar titles, and
that prefix collision *is* how repeats become visible — there's no topic tag, by design. If a title
needs more than three words, it's usually two rows.

**Name the row after what the speaker said, never after the reply.** The reply is the crisper half —
it arrives already resolved into a clean phrase, where the utterance is hedged and half-finished — so
it exerts a constant pull on the title. Following it breaks the clustering: two people raising the
same thing get different titles whenever Shaw answered them differently, and the repeat stops being
visible, which is the one thing the title exists to do.

**Bodies are verbatim.** Each database has its own body template, but all of them blockquote what
was actually said and add one italic line of provenance. The paraphrase lives in the title; the body
is the primary source, and that's what makes a row reusable as content, as an FAQ entry, or as the
seed of a skill.

---

## Five Rules That Decide What a Row Is

**A row is one concept, not one topic.** Merge two extracted items only to undo a tooling artifact —
a duplicate returned by overlapping chunks, or a sentence split across a seam. Never merge because
two items are *related*. Three items circling one theme is a cluster, and clusters are how you
notice something has graduated into a skill or a training module. Collapse them into one row and
you've destroyed the signal these databases exist for. A rapid follow-up ("and is that the system
prompt?") is its own concept and its own row.

The rule has an edge, and splitting past it is the more common error. It protects items voiced as
separate moments; it does not license breaking one continuous statement into its parts. When someone
states a cost and then qualifies it in the same breath — the complaint, then the reason it bites —
that qualifier is the same concept elaborating itself, and it belongs in the one row's body. The
test is whether each half would still be legible as a row with the other deleted.

**Store raw, clean on the way out.** Auto-transcripts mangle proper nouns — Claude becomes "clot" or
"cloud", Obsidian becomes "bsidian", context rot becomes "context broad". Don't fix any of it at
capture. Both Claude and Shaw can read through it, and the garble only bites when a quote *leaves*
the database into a post or a newsletter — which is a one-quote fix at publish time, not a
whole-corpus cleanup on the chance it's needed. Never smooth disfluency either; the "I mean" and the
half-finished sentence are what make a pull-quote sound like a person.

**An open loop is not a row.** "We can revisit that" or "it'll come together at the end" means the
thing is still pending — an agenda item for the next check-in, not a record. The same holds for a
request that happens to draw a long reply ("are you going to send us that dashboard?"): answer
length can never rescue something that was only ever a to-do. Surface these to Shaw as loose ends
instead of filing them. The mirror image points the other way: a cost that hasn't landed yet — a
leader planning around a report's upcoming leave — is forward planning, not a pain.

**Independent recurrence is signal, and no pass may prune it.** The dedup test compares one
speaker's descriptions of one thing inside one record. Across records it inverts: a second person
asking the same question, or the same argument surfacing in an unrelated conversation weeks later,
is convergence — evidence the thing is real and lands, which is what makes it worth a post, a page,
or a skill. Never cut a row for duplicating one from another record, another speaker, or another
surface. This binds hardest on any pass that removes rows rather than adds them: prune a cluster to
a single row and nothing survives to show it was ever a cluster, so the signal isn't weakened, it's
destroyed.

**A row has to outlive the moment it was captured in.** Each database measures that differently,
which is why the same utterance can qualify in one and not the other. Pain Points asks whether the
cost outlives the session, so friction the session itself generated is a support ticket rather than
a record. Q&A asks whether anyone would ask it again, so a question the session provoked still earns
a row — the next trainee will provoke it too. ABA Q&A asks whether the next buyer would ask or raise
it before signing.

---

## Routing: Sort by What the Utterance Is

Q&A, ABA Q&A, Pain Points, and Wins do different jobs, and the same exchange can legitimately earn
rows in more than one.

**Route on what the utterance is, not on whether Shaw answered it.** A question reaching for
information about AI — tools, technique, adoption — is a Q&A row. A question or objection about
ABA's own offer — scope, format, process, proof, prerequisites, price, whether to buy — is an ABA
Q&A row. A pain, doubt, or frustration is a Pain Point — and Shaw's reply rides along in that row's
response section when he gave one. A reported result or outcome — something that worked, saved
time, shipped, or changed how someone works — is a Win. Answer presence used to decide this, back
when Pain Points could only hold the utterance; it no longer does.

**Route on what the asker reached for, not on what the answer covered.** Shaw often answers an AI
question with how his engagement handles it. The pitch doesn't make it an ABA Q&A row, and his
adoption methodology stays in Q&A unless the question is about how ABA's engagement runs it.

Objections are the case worth naming, because they rarely announce themselves. A challenge to price
or value is obvious. A competitive comparison in a buying context — "how is this different from
Copilot?", "why not just build it ourselves?" — is the same thing wearing a question's clothes, and
the reply is a displacement argument worth filing as one: ABA Q&A, `Kind: Objection`. The identical
comparison from a trainee learning the tool is just a Q&A question; the buying context is what makes
it an objection. A doubt that ABA's engagement will work is an objection too; a doubt that AI will
work for their team stays a Pain Point.

**An objection gets one row, not two.** File it in ABA Q&A only — a second copy in Pain Points or
Q&A reads as a second person raising it. (10/11/26: one budget objection had been filed in both
Q&A and Pain Points.)

The mirror trap for Wins is the before/after: a cost the speaker no longer carries is the
evidence half of a win, not a standing pain — `wins.md` carries the rule.

When an utterance genuinely belongs to two databases — a Win and a Q&A, say — write both. When you're unsure whether it
belongs anywhere, that's the exclusion bar talking — see below.

---

## Check What's Already Captured

A record can be mined twice — a scheduled task and a hand-run session, hours apart, neither aware of
the other. The cost isn't the wasted read. It's that duplicate rows are indistinguishable from
**independent recurrence**, the one signal these databases exist to detect — and the rule that
recurrence may never be pruned means nothing downstream will ever clean them up. A second copy of one
person's question becomes permanent evidence that two people asked it.

So check before the read, and check **per database**: a record mined into Q&A may be absent from Pain
Points, and the reverse. Match on the bare page ID normalized out of `Source Link` (strip dashes,
lowercase) rather than the URL string, which varies by host, slug, and query params — and filter
inside the query rather than scanning returned rows, since a partial page of a large table reads
exactly like a clean one. A guard that finds nothing looks identical whether it works or is broken,
so confirm it against a record you know is there before trusting a negative — drawn from the same
database, since a `Source Link` that exists in one table can legitimately be absent from another.

---

## One Pass, Many Targets

Reading the record is the expensive part. Extracting one artifact type and coming back for the
others later doubles the cost and guarantees drift — the second pass judges by a subtly different
bar than the first, and the two halves of one conversation end up inconsistent in a way nobody will
ever catch.

So every reader — you, or each subagent in a fan-out — carries the full routing spec and returns
**typed** items: which database each belongs to, alongside the extraction itself. Dedupe, route, and
apply the per-database bars afterward.

---

## Gotcha: Resolve the Company First, the Person Second

Rows in Clients (Nurture) and Active Leads are named after *people*, so searching them for a
company name returns nothing, and searching the speaker's own name fails whenever they aren't a
buyer. Resolve the account instead: query **Companies**
(`collection://[page-id]`) by `Domain` (the speaker's email domain)
or `Name`, and set `Company` to that page. The company page's people relations then tell you
whether the speaker has a row of their own — set `CRM` only if they do. A speaker with no
Companies row is a solo client (Clients row → `CRM`), someone in the non-lead network (Friends
row → `CRM`), or a lone lead whose company hasn't earned a row yet (Active Leads row → `CRM`).
Don't create the company row from here: it comes with a purchase or a second person in the
pipeline, and `crm` owns that step.

Faster still for a call: the **ABA Trainings / ABA Calls page** for that session usually names the
company and the participants in its body, already resolved. Read the session page before querying
anything.

**Group purchases split the speaker from the buyer.** One buyer can hold seats for several people,
so the participant who spoke is frequently not the person on any CRM row. That's exactly what
`Person` is for — fill it from who spoke; `Company` from where they work; `CRM` only from a row
that is actually theirs.

`Company` is a relation, set by passing an array with the Companies page URL. `CRM` is a plain
URL, so it takes a single link and can point into Clients (Nurture), Active Leads, or Friends.

## Gotcha: Notion Auto-Linkifies Filenames

Anything domain-shaped becomes a hyperlink on save — `Claude.md` silently turns into a link to
`http://Claude.md`, and so do `example.io` and `config.sh`. These bodies are full of filenames, so
backtick them before writing. Backticked text is exempt, and it reads better anyway.

---

## Present for Review Before Writing

Whatever the surface, tier the extracted items as substantive vs thin and say which you'd drop and
why.

**Err toward exclusion.** A marginal row is more expensive than a missed one, and the asymmetry is
not close. These tables are read by filtering and clustering, so every weak row degrades every
future read of them, permanently — nothing downstream prunes. A missed moment costs far less: Shaw
was in the conversation, the review names every exclusion with its reason, and a wrong cut is one
word from him to reverse. Recurrence does the rest — the same cost voiced again in a later record
is the signal these tables exist for, so a topic that matters comes back on its own.

The operative test is **if the row needs an argument, it isn't a row.** A genuine row announces
itself: the utterance is the evidence, and the three-word title writes itself. When you find
yourself building a case for why something qualifies — reasoning past a disqualifier, justifying
from surrounding context rather than from what was said, arguing that a thin item is thin *but* —
that construction is the finding. Drop it and name it in the exclusion list.

**The thin pile is a rescue pool, not a reject pile.** Tiering is the first of two passes and judges
each item alone. The second asks, of everything tiered thin: is this the only utterance in the
record carrying that cost? If it is, and it clears the bar on its own words, promote it. If
promoting it takes an argument, it fails the test above — let it recur instead. If something
stronger already carries it, cut it and fold the detail into the surviving row's provenance line,
where the texture survives without inflating the count. This pass only ever adds, so it can't reach an item that already cleared the bar, and it
never resurrects one that failed a disqualifier outright.

It compares one speaker's descriptions of one thing within one record, never across records — see
the recurrence rule above.

It also can't run during extraction: a reader working one window can't know whether a sibling three
windows away carries the same cost. Readers hand up a generous thin pile with reasons attached
rather than adjudicating it.

**A criterion Shaw introduces mid-run applies to everything already written.** When he draws a new
line on one batch, the batches that landed before it were judged by the old bar and are now wrong —
say so and offer to re-apply it, rather than starting the next batch clean and leaving a silent
inconsistency in the database.

**When you notice a pattern across rows — a repeat, a cluster, an utterance that reveals a gap in
delivery — surface it.** Nobody else is reading these databases looking for that.
