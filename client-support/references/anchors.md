# Anchors: real sends behind the shapes

Verbatim bodies of replies Shaw actually sent, grouped by the shape they show. Each entry names
what to take from it. Dates are M/D/YY; recipients are clients or workshop participants.

---

## Shape 1: Teach

### [Person] ([Company]), 6/29/26

Inbound: "I'm trying to make a skill to make emails sound more like me. But it hasn't really done a
great job yet. Any tips. Mostly for company announcement emails."

```
Use the same 4-step approach, but expect lots of iteration since teaching voice and style is hard.

Here's what I recommend:

1. Have Claude read past company announcement emails and have Claude draft a new announcement
2. Go back and forth until it sounds good (or just edit and send)
3. Have Claude reflect on the conversation to distill your style into reusable principles as opposed to ad hoc rules
4. Tell Claude to create a company-email-writer skill
5. Every time you use the skill, have Claude analyze the difference between its original draft and what you actually sent and update the skill accordingly

Let me know how it goes :)

P.S. You can check out my email-writer skill for inspiration here
```

Shows: the frame line ("same 4-step approach") with the difficulty normalized in the same sentence;
a numbered sequence that ends at a named skill; the diff loop as its own step; the loop closer; the
resource in a P.S.

### [Person] ([Company]), 9/17/26

Inbound: two use cases going badly (an HTML-to-PowerPoint conversion that burned all her tokens, and
client email drafts "much too wordy" and content-wrong), ending with "I can't decide if it's user
error" and "maybe I need to try using the voice feature instead now?"

```
This friction is a normal part of the learning process.

Both of these use cases are very doable with Claude. The trick is starting with smaller asks that eventually roll up into Claude taking more off your plate (just like if you were to delegate work to a new hire, you'd probably start small and simple to see how they do, then slowly give them more work).

Here are some tips for each use case:

- Client emails: start by just having Claude write one client email (even an easy one). Ask it to ground its draft in past similar emails by searching your Gmail. Then tweak its draft directly and tell it to analyze the difference. Repeat this for 2 more emails, increasing the complexity each time. Finally, at the end of that conversation, tell Claude to create a new client-emails skill.
- HTML to PPTX: I would have to see the HTML file to give more specific advice, but you could try making the ask smaller by going back and forth on just one slide. Once that looks good, try another. Then try the rest.

Also happy to work through these live. Would you, [Person], and [Person] want to do an "office hour" where we troubleshoot your use cases?

-Shaw
```

Shows: normalization first, with no verdict on "user error"; the mechanism ("start smaller, roll
up") with the new-hire analogy; one bullet per use case with a bold label; a procedure that routes
through Gmail and ends at a named skill; bounded advice where the artifact is missing; the voice
feature hypothesis rerouted by never mentioning it; the group asked whether they want an office hour
rather than handed times.

### [Person] ([Company]), 8/27/26 (day before a booked session)

Inbound: a long pre-session write-up of two tasks (speaker notes from presentation transcripts;
client email replies with a Gmail connector that wouldn't connect), with her current prompt pasted.

```
Thanks for sharing, [First Name]! This is super helpful.

A couple of quick thoughts on your two use cases:

1. Presentation notes: The easiest way to streamline this is to go to one of your existing conversations where you did this with Claude and ask it to create a new skill called speaker-notes. From there, you can refine it over time by having Claude use it on your next set of notes, giving it feedback when the voice isn't quite right, and updating the skill at the end of the conversation. (We'll cover this tomorrow)
2. Client emails: A skill is the right direction here too. We can troubleshoot the Gmail connector tomorrow. You may need to disconnect and reconnect it, and once that's working, this should get much faster. Ideally, we also connect Claude directly to your documentation, Loopio, and the wiki so you don't have to copy/paste context in. We can talk through that tomorrow too.

See you tomorrow :)

-Shaw
```

Shows: when a session is booked, the reply previews and defers ("We'll cover this tomorrow") rather
than teaching in full; routing through an existing conversation; a connector fix bounded to "you may
need to"; the long pasted prompt acknowledged and not engaged.

---

## Shape 2: Triage

### [Person], 5/27/26

Inbound: built an "OS" of markdown files, "hit or miss on quality of output... 3 steps forward, 2
steps back."

```
Storing context in a directory of markdown files is a powerful way to give Claude persistent context and codify SOPs.

When you say it's hit or miss on quality, what's going wrong?

1. Responses are low quality/too verbose
2. Claude is pulling in the wrong context
3. Claude doesn't follow the right process
4. Something else?

-Shaw
```

Shows: validate the approach in one line, then the multiple-choice question and nothing else. No
advice until the failure mode is named.

---

## Shape 3: Frame it, then take it live

### [Person] ([Company]), 10/17/26

Inbound: the deck-generation skill is "going well"; the friction point is now QA, which he sees as
the human-in-the-loop step they "can't entirely eliminate yet"; asks for suggestions on using Claude
to QA the decks faster, "happy to discuss this at our next checkpoint."

```
Thanks for the reply [First Name]! Sounds like you're going beyond "Can Claude do X?" to "Can Claude do X well?"

Keeping a human in the loop is usually a good idea for things that are ultimately consumed by customers (e.g. decks and emails). But that doesn't mean Claude can't help with much of the recurring, routine work.

Happy to hop on a call this week to walk through the best way to do this for your client deck use case.

Any of these times work?
[calendar-link]

-Shaw
```

Shows: the reframe as the ack; the stance on human-in-the-loop in one line, with the routine-work
counterweight; the call as the answer, with times. The draft this replaced prescribed a three-step
deck-qa procedure and offered the office hour as a closer; Shaw cut the procedure entirely. The
question was clear but design-level, and the right answer needed his decks and his QA list in front
of them.

### [Person] ([Company]), 8/28/26 (morning of the session)

Inbound: a last-minute use case, using Claude to flag client emails that need a follow-up; "Claude
flags every email from a client that hasn't received a response, even when a follow-up isn't
needed."

```
Great use case! We can definitely dig into this today.

The best solution here is to build a skill that teaches Claude what emails that need responding to look like. Today we'll talk about a simple 4-step framework for doing this and will have lots of time for Q&A to talk about your specific use cases.

Talk soon :)

-Shaw
```

Shows: the frame line alone ("build a skill that teaches Claude what X looks like"), then the live
session as the answer. Her implied hypothesis, "prompts with a bit more nuance", is rerouted to a
skill without being named.

---

## Status update (no question)

### [Person] ([Company]), 10/28/26

Inbound, replying to a post-workshop check-in: "I have been creating my own skills yes, for research
new companies and then contacts within those orgs."

```
Awesome use case! If it's helpful, happy to hop on another 1:1 call if you want to talk through additional skill ideas or leveling up existing ones :)
```

Shows: a one-line reaction, then the call as a soft offer; no tips or next lever in writing.
"another" because he'd already had a 1:1 with Shaw. The drafted version named a lever ("run the
research on a schedule"); Shaw cut it. Templates for this sequence live in the Team Workshop
Attendee Check-in SOP.

---

## Calibration: a leader's policy concern

### [Person] ([Company], CTO), 6/16/26

Context: a nudge on an unrelated ask, with the answer to a concern he'd raised on the call riding in
a P.S.

```
P.S. You mentioned Cowork's file access is a big concern for the team. It looks like you can control this through the Desktop app's configuration settings <link to the enterprise configuration article>. Happy to look at this together in case it's helpful :)
```

Shows: a leader's control question gets the fact, the control that governs it, and an offer to look
together. No procedure, no framework; two sentences.

---

## Slack register

Fragments `slack-helper` distilled from Shaw's replies in client channels, kept here so the answer
content stays in one place:

- Lead with the honest short answer, including "it depends", and say what it depends on in the same
  breath: *"The short answer is that it depends on the instructions."*
- Levels or options as a small numbered set with bolded labels, phrased as "good when <condition>".
- Name the tradeoff, not just the recommendation: *"use this sparingly because these instructions
  get added to all new conversations and can cause Claude to get confused."*
- Then stop. No sign-off, no "hope that helps."
