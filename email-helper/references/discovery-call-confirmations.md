# Discovery Call Confirmations

The reply Shaw sends after a lead books an intro/discovery call via Calendly. Goes out same-day, primes the live conversation, and keeps the call from starting cold.

Read this file before drafting any "they just booked an ABA Intro Call" reply.

---

## When it fires

A new email from `notifications@calendly.com` lands in the business inbox with subject `New Event: <name> - <time> - <event type>`. The event type is typically `ABA Intro Call` or another discovery-style call.

This is the canonical signal for a brand-new direct booking — same one Workflow 3 in `crm/SKILL.md` uses to add the lead.

---

## Threading mechanics

- **Reply to the Calendly notification thread** — pass the notification's `messageId` as `replyToMessageId`. The whole exchange (booking → confirmation → live thread with the lead) stays in one place.
- **`to:` is the invitee's email**, not `notifications@calendly.com`. Pull the invitee email from the notification body.
- **Subject:** keep the Calendly subject prefixed with `Re:` (e.g., `Re: New Event: [name] - 05:00pm Tue, May 5, 2026 - ABA Intro Call`).

---

## Template

```
Hi [First Name],

Thanks for setting this up!

Here are a couple of follow-up questions to help us get the most out of our time together.
- [Question 1]
- [Question 2]

Talk soon,
```

The Gmail signature renders Shaw's name. Don't add a separate `Shaw` line.

---

## Picking the two questions

Pull from the Sales Discovery question bank in `pre-call-research/SKILL.md`. Don't restate them here — single source of truth.

**Default pair** when the Calendly intake form was blank (no business description, no stated reason for booking):

- *Why are you looking for AI training right now?*
- *What have you tried so far?*

These two surface the trigger and the starting point — the two things that most shape how the live call should go.

**When intake fields are populated** (business description, audience, topics of interest, etc.), swap one or both questions for ones that fill the biggest gaps the form didn't already cover. If they said "I run a 50-person consulting firm and I want my team to use Claude better" — don't ask "what do you want to be able to do" because they basically told you. Ask the deeper one: *what's been the hardest part?* or *what have you tried so far?*

---

## Principle: only paraphrase what they actually said

An earlier version of this template included a second sentence after `Thanks for setting this up!` — something like `Happy to give more guidance on this.` That sentence works *only* when there's a stated reason in the intake form to acknowledge ("you want help with X — happy to give more guidance"). When intake is blank, it reads as filler and gets cut.

Generalizes: the optional acknowledgement sentence in any template should react to something concrete the person said. If there's nothing concrete, drop the sentence rather than padding with a generic version.
