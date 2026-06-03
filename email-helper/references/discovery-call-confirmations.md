# Discovery Call Confirmations

The reply Shaw sends after a lead books an intro/discovery call via Calendly. Goes out
same-day, primes the live conversation, and keeps the call from starting cold.

This file owns the **threading mechanics** for that reply. The **template, question bank, and
question selection** live in the Discovery Call SOP — the single source of truth for
discovery-call content. (The SOP's page ID is catalogued in `notion-helper/SKILL.md` →
"Event-Type SOPs.")

Read this file *and* the Discovery Call SOP before drafting any "they just booked a discovery
call" reply.

---

## When it fires

A new email from `notifications@calendly.com` lands in the business inbox with subject
`New Event: <name> - <time> - <event type>`. The event type is a discovery-style call —
`ABA Intro Call`, `AI Transformation`, or `1:1 Claude Workshop (Discovery)`; the Discovery Call
SOP holds the canonical alias list, and they all resolve to one call type.

This is the canonical signal for a brand-new direct booking. The intake is orchestrated by
**CRM Workflow 7 (Discovery Call Intake)** — when Workflow 7 reaches its confirmation-email
step it invokes this skill. You may also be invoked directly when Shaw asks for the
confirmation reply.

---

## Threading mechanics

- **Reply to the Calendly notification thread** — pass the notification's `messageId` as
  `replyToMessageId`. The whole exchange (booking → confirmation → live thread with the lead)
  stays in one place.
- **If the lead came in through the contact form or an existing sales thread**, reply there
  instead so the relationship context carries.
- **`to:` is the invitee's email**, not `notifications@calendly.com`. Pull the invitee email
  from the notification body.
- **Subject:** keep the Calendly subject prefixed with `Re:` (e.g., `Re: New Event: [Lead Name] -
  05:00pm Tue, May 5, 2026 - ABA Intro Call`).
- Business inbox is `u/1` — see "Gmail accounts and the `u/` path" in SKILL.md.
- No em dashes in the drafted email — see "Punctuation" under Voice in SKILL.md.

---

## Template and question selection

Both live in the **Discovery Call SOP**, below its `---` divider. Draft from there — don't keep
a second copy here that can drift. The SOP's drafting note covers the default question pair for
low-info leads and how to swap one or both when the Calendly intake form was populated.

---

## Principle: only paraphrase what they actually said

An earlier version of this template included a second sentence after `Thanks for setting this
up!` — something like `Happy to give more guidance on this.` That sentence works *only* when
there's a stated reason in the intake form to acknowledge ("you want help with X — happy to
give more guidance"). When intake is blank, it reads as filler and gets cut.

Generalizes: the optional acknowledgement sentence in any template should react to something
concrete the person said. If there's nothing concrete, drop the sentence rather than padding
with a generic version.
