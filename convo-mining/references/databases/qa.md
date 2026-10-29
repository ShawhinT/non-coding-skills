# 💬 Q&A

The record of every question someone asked Shaw and every answer he gave.

**Database:** `https://app.notion.com/p/[database-id]`
**Data source:** `collection://[page-id]`

## Schema

Shared-spine properties (`Date`, `Source`, `Source Link`, `Company`, `CRM`) behave exactly as
SKILL.md describes. Two names differ here:

| Property | Type | Note |
|---|---|---|
| Question | Title | The spine's title property. Three words max |
| Asker | Text | The spine's `Person` property, named for this database |
| Avatar | Select | `Founder/CEO` / `Leader` / `IC`. Same scheme and same rules as Pain Points, so the two tables segment together — one value, most senior wins, blank when the record doesn't say |

## Body template

```markdown
## Question

> <verbatim question text, blockquoted>

*<one italic line of provenance: where it was asked, who forwarded it, what was on screen>*

## Answer

<Shaw's answer, verbatim, formatting preserved>
```

## What clears the bar

Two gates, in order — the same shape Pain Points and Wins use. The first asks about the asker, the
second about the pair.

**Is the asker someone Shaw sells to or delivers to?** A client, a training or workshop attendee, a
prospect, an Upwork poster. Everything this database feeds runs on that relationship — renewal
evidence needs a retainer, curriculum needs someone being taught, and the content pipeline is aimed
at buyers. Anyone outside it fails however good the conversation is: a peer, partner, or networking
contact interviewing Shaw about how *he* runs his business produces answers none of the four jobs
below can use. `Source: Call` covers coffee chats and networking calls alongside intro calls, so the
source value is not the gate — the relationship is.

Past that gate, a pair earns a row if it would do work in one of the four jobs below. Ask what the
question was *reaching for*: if nobody would ever ask it again, there's nothing to reuse and nothing
to cluster with.

**Clears it:** a real question about AI, adoption, tooling, technique, workflow, or strategy —
including questions phrased as statements or hesitations when Shaw responds to them as questions.
Shaw's own methodology and point of view clear too, when a buyer draws them out: the adoption
roadmap, why bottom-up beats top-down, what makes a demo representative. That's his argument, and a
prospect pressing him is often where he states it most sharply. The carve-out is for the methodology
he sells, not for how he runs his own practice — course launches, audience building, and pricing his
own work belong to whoever asked.

**Doesn't:** session logistics, screen-share coordination, Shaw's own questions to the client, bare
confirmations, click-paths through a UI that will have moved by the time anyone reads the row (the
durable answer is the concept, not the sequence of clicks), and questions about someone else's
business — how to price their agency, what they should go study.

**Questions and objections about ABA's own offer belong in ABA Q&A** — scope, format, proof,
prerequisites, price, including objections shaped like comparison questions. Methodology stays here
unless the question is about how ABA's engagement runs it. See `aba-qa.md` and the routing section
in SKILL.md.

**Nothing already authored better elsewhere.** Shaw writes his ICP, offer ladder, and pricing
deliberately on his strategy page. A transcript of him reciting them is a worse copy of a document
that already exists — mangled by auto-transcription, frozen at one date, and certain to contradict
the real source the next time prices move. Ask where the best version of this answer lives; if it's
a page Shaw maintains, the row adds nothing and competes with it. This is why "what does the
fractional department cost?" fails while "why start with the executives?" passes: one is recitation,
the other is an argument he makes nowhere else in writing.

**Thinking out loud is not an answer.** An idea floated and not landed, a direction he's still
deciding on, "I'm building the plane while I'm flying it" — these read substantive because they
genuinely are interesting, but nothing was concluded, so there's no answer to reuse. Same family as
the deferral below.

**Session-bound exchanges don't outlive the session.** Two shapes. The micro-decision inside a live
build — "should I pull all three reports or just one?", "should I change the prompt or attach the
file?" — is unintelligible without the screen that was on share. The re-ask is someone restating
what was just answered to check they followed it: "just to summarize then…", "how does the pricing
work again?". Both are real moments; neither is a row. The first has no reader outside that hour,
the second is a weaker copy of a row written minutes earlier in the same record. That second test is
the ordinary within-record dedup, and it never licenses cutting a repeat across records.

**The thin pair that reads as substantive.** A request for a file or a follow-up — "are you going to
send us that dashboard?" — reliably draws a long, generous reply, and the *reply's* substance is
what fools an extractor into keeping it. Surface the request to Shaw as an action item instead.
Extractors weighing question and answer together reach the opposite conclusion, so state this
explicitly to every subagent you fan out.

**A deferral is not an answer.** "We can revisit that" or "it'll come together at the end" means the
question is still open — an agenda item for the next check-in, not a row.

## What this database is for

- **Renewal evidence.** Filter by client and you have a concrete list of what the retainer actually
  answered — far better than "we had some Slack conversations."
- **Content pipeline.** Real questions from real practitioners are the highest-signal source Shaw
  has for LinkedIn, newsletter, and YouTube. Hand strong ones to `sfc-helper`.
- **Skill and SOP detection.** When the same question shows up a third time it isn't a question
  anymore — it's a skill, a doc, or a training module. Watch for repeats *across* clients and
  surfaces; a repeat spanning a Slack thread and a training call is the strongest version of this
  signal, and it only shows up because everything lives in one table.
- **Training curriculum.** Topic clusters tell you what the next session should cover, grounded in
  what the team is actually stuck on.
