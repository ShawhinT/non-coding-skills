---
name: "client-support"
description: "Reply to a client or workshop participant about their own Claude work, in Shaw's voice: a how-do-I, an \"it's not working\" report, a request for tips, a \"pick your brain\" on quality or process (how do we QA what Claude makes), a question in a check-in, office-hour thread, or client Slack channel, or a check-in reply with no question in it (a status update on what they've built). The trigger is who is writing, not whether they asked something. The channel skill (email-helper, slack-helper) owns delivery and register; the answer's content, the choice between teaching, triaging, and taking it live, and the look-up of past answers live here. Fires before create_draft or slack_send_message_draft on any such reply, and when prepping answers for an office hour. Not for buyer objections, pricing, or scope (conversion-copy), scheduling replies (email-helper), or logging the exchange afterward (convo-mining)."
---

# Client Support

Shaw's engagements put him in front of a lot of people at once: leaders, managers, individual
contributors, and everything from first-week Claude users to people already shipping skills. He
checks in with them constantly, and the check-ins surface questions and progress reports. This
skill is how those get answered: the trigger is who is writing, someone Shaw delivers to, about
their own Claude work, not whether their message contains a question. A status update with nothing
asked gets a lighter reply: a one-line reaction to what they built and an optional offer of live
help. The next lever is for the call, not the email. The skill owns the *content* of the
answer: which shape the reply takes, what goes
in it, and where to look before writing it. The channel skill it composes with owns everything about
*delivery*: `email-helper` for greeting, sign-off, threading, and HTML; `slack-helper` for threads,
approval, and the no-sign-off register of a client channel.

The job is not to be exhaustive. Shaw's answers are short because the person on the other end has
to act on them this week, and because the engagement includes live time where the long version
belongs. A reply that reads as a knowledge-base article has usually answered a question nobody
asked.

## Before writing

**Read the question, then find who's asking.** The asker's role and level set the register and the
shape more than the question's words do. Their CRM or Reviews/Referrals row, the engagement, and
the session notes say what they've built so far and what they're trying to do; their past rows in
the `convo-mining` databases show what they've asked, struggled with, and won before. Someone asking "how do I"
wants a procedure. Someone asking "should we" or "can we control" wants a stance and a pointer, and
usually prefers to see it together rather than read it.

**Check whether it's been answered.** Every question Shaw answers is logged by `convo-mining` into
the Q&A database (`references/databases/qa.md` in that skill has the schema and ID). Search it by
topic before drafting: a repeat question gets the answer Shaw already gave, adapted to this asker,
rather than a fresh improvisation that drifts from the first. The Troubleshooting SOP under
Resources on the SOPs page holds known symptom → fix pairs for platform issues; check it when the
question is "it won't turn on" rather than "how should I".

**Check what they already have.** The cheapest procedure routes through an existing conversation,
an existing skill, or a connector they've already set up. Knowing those exists is what lets the
answer say "go back to the chat where you did this" instead of "start by...".

## Pick the shape

Three shapes, chosen by how specific the question is and how big the answer would be. Picking
before drafting matters: a teaching reply to a vague complaint guesses, a triage reply to a clear
one stalls, and a full procedure for a design-level question commits Shaw in writing to an approach
he'd want to shape live.

**Teach** when the problem is clear enough to prescribe against and small enough to fit in a few
steps. The reply carries a procedure the person can run this week and ends at a named skill.

**Triage** when the complaint is vague ("hit or miss", "a struggle", "not great"). Advice against a
guess is wasted, so the reply asks a multiple-choice question, three or four options plus
"something else?", and gives no advice yet. The options do double duty: they name the failure modes
so the person can recognize theirs, and they teach the vocabulary for the next exchange.

**Frame it, then take it live** when the question is clear but design-level: how should we QA what
Claude produces, how do we structure this workflow, what should the next phase look like. A good
answer needs their artifact or process in front of you. The reply gives a one-line reframe that
shows the question was understood, one principle that settles the direction, and a call offer with
times. No procedure. Based on a real send ([Person], 10/17/26): the question was how to use
Claude to QA client decks faster; the reply reframed it ("going beyond 'Can Claude do X?' to 'Can
Claude do X well?'"), stated the stance on human-in-the-loop, and offered a 30-min call. A drafted
version with a three-step deck-qa procedure was replaced with that.

## What goes in the answer

**Open with a short ack when they sent substance, then normalize.** "Great use case!", "Glad it's
going well!", "Thanks for sharing, this is super helpful." The next line frames the difficulty as a
property of the work, not of the person: "This friction is a normal part of the learning process",
"expect lots of iteration since teaching voice and style is hard." Never adjudicate "is it me?"
either way, even kindly; a verdict on their ability keeps the email about them instead of the work.

**One sentence naming the mechanism.** Before any tips, one line that says what kind of solution
this is: "Use the same 4-step approach", "The best solution here is to build a skill that teaches
Claude what X looks like", "The trick is starting with smaller asks that roll up." The frame is what
they reuse after the tips are spent. An analogy (delegating to a new hire) is optional; the
mechanism is not.

**Lead with the honest short answer, including "it depends."** Say what it depends on in the same
breath. When the answer has levels or options, give them as a small numbered set with a bolded
label each, phrased as *good when <condition>* rather than as a rule, and name the tradeoff: the
reason Shaw's answers land is that they say when the thing stops working ("use this sparingly
because these instructions get added to every new conversation and can confuse Claude").

**Tips are procedures, not diagnoses, and they end at a named skill.** "The fix is context" tells
them what's wrong; "have Claude read past announcements and draft a new one, go back and forth
until it sounds good, have it distill your style into reusable principles, tell it to create a
company-email-writer skill" tells them what to do Monday. Sequence the steps, start with the
smallest version of the task, escalate, close on the skill. Include the diff loop explicitly, since
it's what makes the skill compound: each time they use it, tell Claude to compare its draft to what
they actually sent and update the skill.

**Route through what they already have.** "Go to one of your existing conversations where you did
this and ask it to create a skill", "ground the draft by searching your Gmail", "connect Claude to
your documentation so you don't have to copy/paste context in." The lower the prep cost, the more
likely the procedure happens.

**Human in the loop is a stance, not a concession.** When the question is about quality or trust
in what Claude produces, Shaw's position is consistent: keep a person reviewing anything that
ultimately reaches a customer (decks, emails), and let Claude take the recurring, routine work
around it. The goal is making the review faster, not removing it. State it in one line and move on.

**Bound the advice when you'd need to see the artifact.** "I'd have to see the HTML file to give
more specific advice", "you may need to disconnect and reconnect it", "let me know what you see so I
can troubleshoot." Accurate scope keeps the tip from overpromising and invites the thing you need
next.

**Reroute a wrong hypothesis; don't rebut it.** When they propose a fix that won't help (voice mode
for a content problem, more prompt nuance for what should be a skill), answer with the better path
and never mention theirs. The frame does the rerouting; a rebuttal reads as correction.

**Tie it back to what they observed.** If they described a symptom, point at the part of the answer
that explains their symptom. That's what makes the reply read as written to them.

## Calibrate to the asker

The same question gets a different answer by who's asking, and the record is what fills this
section in, not a taxonomy. What the real sends support so far:

- An individual contributor asking how to do their own work gets the procedure, scoped to one task,
  starting small. The 4-step skill framework is the spine, and the named skill is the finish line.
- A leader raising a policy or control concern (file access, data handling, what the team is allowed
  to do) gets the fact and the control that governs it, with an offer to look at it together, in a
  P.S. or a short reply rather than a procedure. Based on a real send ([Person], 6/16/26):
  Cowork file access was the concern; the reply pointed at the desktop app's enterprise
  configuration and offered to walk through it.
- A group gets per-person labels: bold the name or the use case, one item each, so each reader finds
  theirs.
- Someone early and frustrated gets the normalization line first and a smaller ask than they were
  attempting; someone already shipping skills gets the next lever (connectors, scheduled tasks, the
  diff loop) and no basics.

Add to this list from sends that worked, with the date, not from what seems plausible.

## Live help is the escape hatch, and sometimes the answer

Inside an engagement the live surfaces are the office hour and the weekly sync; outside one, a
30-min call. Which to offer depends on the shape and the asker. A booked session gets a preview and a
deferral ("We'll cover this tomorrow"). A design-level question gets the call as the primary answer,
per the third shape. A group is asked whether they want an office hour before times are proposed;
a menu asks them to coordinate teammates before they've said yes. An individual gets the link or
the times directly. Check the calendar before promising "the next office hour": if none is booked,
the offer has to carry the booking.

## Shape and register by channel

The content above is channel-independent. The register is not, and the channel skill owns it; the
one-line deltas that matter for an answer:

- **Email** (per `email-helper`): 6-10 lines for a teach reply; numbered list when the steps are a
  sequence, bullets with bold category labels when the items are parallel; skill names bold,
  lowercase kebab-case; the closer is a loop, not a CTA ("Let me know how it goes :)", or the open
  door inside an engagement), carrying the email's one `:)`. Mid-thread: no greeting, sign "-Shaw".
  A resource link goes in a P.S.
- **Slack** (per `slack-helper`): same content, then stop. No sign-off, no "hope that helps", no call
  offer unless the question genuinely needs live back-and-forth, in which case say so and offer the
  weekly sync instead of writing an essay in the thread. Reply in-thread; address the asker by name
  when the question was forwarded.

## After sending

The exchange is logged by `convo-mining` (Q&A, and Pain Points when the question carried a
frustration). That log is what makes the next answer to the same question faster and consistent,
so it's part of answering, not a separate chore.

## References

- `references/anchors.md`: the real sends behind each shape and principle, verbatim, with what each
  one shows. Read it before drafting; the shapes are easier to see than to describe.
