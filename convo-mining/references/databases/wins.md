# 🏆 Wins

Results people report from AI work — time saved, output shipped, a capability unlocked, a change
in how someone works. One row per win, verbatim in the body. Any AI win from someone Shaw has
delivered to counts, whether or not ABA work caused it; attribution lives in the body, not a
property.

**Database:** `https://app.notion.com/p/[database-id]`
**Data source:** `collection://[page-id]`

## Schema

Shared-spine properties behave exactly as SKILL.md describes, including `Person` under that name.
Beyond the title, one property is specific to this database:

| Property | Type | Note |
|---|---|---|
| Win | Title | The spine's title property. Three words max |
| Avatar | Select | `Founder/CEO` / `Leader` / `IC`. Same scheme and same rules as Q&A, ABA Q&A, and Pain Points — one value, most senior wins, blank when the record doesn't say — so all four tables segment together |

No `Type` and no metric field, deliberately. The quantified bit stays verbatim in the body where
it can't drift from what was said, and the three-word title carries the topic.

## Body template

```markdown
## Win

> <verbatim utterance, blockquoted, unsmoothed>

*<one italic line of provenance: where it was said, who relayed it, what surrounded it>*

## Context

<what enabled it, when the record says: the skill, workflow, or session it traces to, one plain
line — omit this heading entirely when the record doesn't say>
```

**Context is where attribution lives.** Every win that clears the bar gets captured, whether or not
ABA work caused it, so there's no checkbox to tick — when a win traces to a session, a skill built
together, or retainer work, say so here in one line ("built in the 8/12 session", "the outreach
skill from the intensive"). A case-study or renewal filter is a read of this section, and an
omitted section honestly reports an unattributed win.

## What clears the bar

Two gates, in order. The first asks about the speaker, the second about the utterance.

**Is this someone Shaw has delivered to?** A client, a trainee, a workshop participant — anyone
inside or downstream of delivery. Everything this database feeds assumes that relationship: a
testimonial needs someone who worked with him, renewal evidence needs a retainer, and "what works"
needs a result his teaching can be read against. A peer or prospect describing results from their
own unrelated stack clears every utterance test below and still has nowhere to go — that is a good
coffee chat, not a win. This is why the attribution-agnostic rule above is narrower than it reads:
a *client's* win that ABA didn't cause still counts, because the relationship is what earns the
row, not the cause.

**The relationship has to predate the win.** The gate asks where someone stood when the result
landed, not where they stand by the end of the record. A first session is where this bites: the
participant becomes someone Shaw has delivered to partway through the very transcript being mined,
so everything they report from before it — however cleanly it clears realized, claimed, and
quantified — is a win their own stack earned. There is nothing for a testimonial, a renewal, or a
what-works read to attach to. Their wins start accruing at the *next* session; what a first session
yields is pain points and questions.

Past that gate, an utterance earns a row when the speaker reports a result that has landed — in
their work, their team's, or their numbers. Understatement counts, and so does a win relayed
second-hand (same rule as Pain Points: `Person` is whoever experienced it, the relay goes in the
provenance line).

**Realized, not forecast.** "This is going to save me hours" is enthusiasm about a future — the
spine's open-loop rule applies, and it's an agenda item for the next check-in, not a row. "It
saved me three hours Monday" is a win. The forecast coming true later is exactly what the next
session surfaces, and that later utterance is the row.

**Past tense is not the test — a landed result is.** Progress toward a result reports in the same
past tense a result does: a prototype built, customers shown, feedback collected, a phase moved on
to. All of it happened, and none of it is yet the time saved, the output shipped, or the changed way
of working. Ask what the speaker now has that they didn't have before; if the answer is a further
step rather than an outcome, the win is still ahead of them and the utterance is where they are, not
what they got.

**It has to outlive the session that produced it** — the spine's durability rule, pointed the
other way. A build compiling live on a call is Shaw's demo, not their win yet; the win is when it
holds up in their real work. What a session *reveals* still counts: "I've been doing this manually
for a year and it just did it in a minute" reports a realized comparison against their standing
workflow, even though the minute happened in-session.

**A win is a difference, so the record has to show both sides of it.** "It went well, it gave me
everything I needed, I'll keep using it" reports satisfaction and adoption: nothing says what the
work was like before or what changed because of it, so a testimonial, a renewal case, or a
what-works read has nothing to stand on. The before needn't be a number (a spreadsheet replaced, a
task they couldn't do at all) and it can come from elsewhere in the same record, but it can't be
assumed. When it's missing, the utterance is the opening for a follow-up question ("how long did
that take before?"): surface it to Shaw as a loose end, and the answer is the row.

**Praise is not a win.** "This is great, thanks so much" names no result. But praise that carries
one — "that would have taken me a week" — clears, and it's often the best pull-quote in the
record. Pure testimonial-shaped praise with no result attached belongs with `reviews-referrals`;
surface it to Shaw rather than filing it here.

**The speaker claims it, not Shaw.** Shaw summarizing the value delivered ("so that saved you
what, four hours?") is his framing — the row needs their words. An "exactly, yeah" after Shaw's
summary is thin; tier it and let review decide.

**A resolved pain is win evidence, not a pain row.** "I used to spend four hours on this; now
it's 20 minutes" carries a before and an after in one breath. The before is a cost the speaker no
longer carries, so it fails Pain Points' bar — keep it in the win's body, where it's the half that
makes the number land. Split it into a Pain Points row only if someone *still* carries that cost.

**Doesn't clear it:** aspiration ("I want to get to the point where…"), a description of what a
tool can do with no personal result attached, gratitude about session logistics, Shaw's own wins
told back to a client, and anything that is really an open loop or a to-do.

## What this database is for

- **Testimonial and case-study pipeline.** A win in the speaker's own words is the seed of a
  testimonial — hand strong ones to `reviews-referrals`, and quantified ones are case-study
  numbers with the quote already attached.
- **Renewal evidence.** Filter by client and you have the concrete value the retainer delivered —
  verbatim, dated, and linked to the session it happened in.
- **Content raw material.** Real wins from real practitioners are proof stories for LinkedIn,
  newsletter, and YouTube. Hand strong ones to `sfc-helper`.
- **What-works signal.** A cluster of wins around one skill, workflow, or training module is
  evidence of what to teach, build, and package next — the mirror image of Pain Points'
  offer-design signal.
