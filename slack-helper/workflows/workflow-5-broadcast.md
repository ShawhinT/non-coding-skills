# Workflow 5: Posting to a Client Channel

Broadcasts run on a different register than answers. An answer is a deliverable being delivered to
the person who asked. A broadcast to a client's whole org is a relationship message, and most of
the audience never signed anything, never sat on a sales call, and doesn't know who Shaw is.

Approval rules are unchanged — draft, show Shaw, wait for a yes, then hand it over with
`slack_send_message_draft` for him to send (see Delivering a Message in SKILL.md).

## Principles

**Keep the engagement out of it.** Term dates, session counts, response-time SLAs, deliverable
lists, and pricing were sold to the champions, not to the org. Publishing them to a general channel
turns an introduction into a vendor announcement and invites the reader to audit the contract
instead of asking a question. Say what you're there to help with and leave the mechanics to the
people who bought them. "I'm working with the ops team to help you all leverage Claude in your
work" does the whole job; a 3-month term and a company-wide office hour date do not belong.

**Anchor on shared experience, not credentials.** "I did the all-hands training last month with
Claude Cowork" lands harder than any background line, because they were in the room. Reach for a
bio only when there's genuinely no shared moment to point at.

**Name why you're in the channel.** People notice a new name in a channel they've been in for
years. "[Person] recently added me here, so I wanted to drop a quick intro" costs one clause and
answers the question they'd otherwise be sitting with. Same instinct as the email voice's
"Acknowledge the inbound" — say the honest reason you're in front of them.

**Lower the bar to ask, twice.** Offer both the public tag and the DM. Some questions feel too
basic to ask in front of 90 colleagues, and the DM is where those go.

**Vague beats specific here.** This is the opposite of the usual "specific beats vague" default,
and it's deliberate: a broadcast's job is to open a door, not to commit Shaw to a schedule the org
will hold him to. "This will mostly be through team trainings" is right; enumerating the 13
trainings is not.

## Mechanics and register

- **Slack emoji shortcodes are in register.** `:grin:` fits a broadcast. This is a real divergence
  from the neighboring skills — `social-replies` is zero-emoji and `email-helper` allows only `:)`
  — so don't import their rule here.
- **Warm closers work.** "Looking forward to working with you all" is right for a broadcast, even
  though replies and email drop the sign-off.
- **`@channel` is appropriate for a genuine one-time announcement** like an intro, and almost never
  otherwise.
- Second person plural throughout — "you all," "your work." The message is to a group.

## Reference: the [Company] intro (sent 8/18/26)

Shaw's own text, after [Person] added him to [Company]'s general AI channel:

> Hey @channel! [Person] recently added me here, so I wanted to drop a quick intro.
>
> I'm Shaw (I did the all-hands training last month with Claude Cowork). I'm currently working with
> the ops team to help you all leverage Claude in your work. This will mostly be through team
> trainings, but if you ever have any questions about Claude or AI, feel free to tag me here or
> shoot me a DM.
>
> Looking forward to working with you all :grin:

Note what's absent: the retainer, the term, the 1-business-day SLA, the deliverable counts, the
dated first office hour, and any version of "no question is too basic." The warmth carries the
invitation; the specifics would have made it an announcement.
