# Workflow 3: Answering a Question

**Never send without explicit approval.** Draft, show Shaw the draft, wait for a clear yes, then
hand it over with `slack_send_message_draft` — the connector cannot post into a Slack Connect
channel, so Shaw sends it himself (see Delivering a Message in SKILL.md). This holds even when the
answer is obvious and even when Shaw asked you to "handle it" — posting under his name in a paid
client channel is his call every time.

- **Reply in-thread**, not to the channel. Pass `thread_ts` = the parent message's `ts`. Client
  channels stay readable only if question threads stay threaded.
- **Address the asker by name** when the question was forwarded — the person who asked isn't the
  person who posted it, and naming them ("as [Person] noticed") closes that loop.
- If the answer needs more than a paragraph or genuinely needs live back-and-forth, say so and
  offer to take it to the weekly sync instead of writing an essay in Slack.

## The answer itself

The content of the answer is owned by the `client-support` skill: which shape it takes (teach,
triage with a multiple-choice question, or a one-line reframe plus taking it live), what goes in it
(the honest short answer, a small numbered set of options phrased as "good when", the tradeoff that
says when the thing stops working, the tie-back to what they observed), and the look-up of past
answers in the Q&A database so a repeat question gets the answer Shaw already gave. Invoke it
before drafting; its `references/anchors.md` has the real sends.

What's Slack-specific is the register, and it's one rule: deliver the content, then stop. No
sign-off, no "hope that helps", no call offer unless the question genuinely needs live
back-and-forth, in which case the weekly sync is the offer, per the bullet above. Avoid
bullet-list dumps with no ordering logic, hedging that never resolves, and answers that restate the
question before answering it.

This register is for *replies*. An outbound post to the channel runs on a different register — see
`workflow-5-broadcast.md`.
