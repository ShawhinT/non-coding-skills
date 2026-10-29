# Workflow 4: Log it via convo-mining

Do this for every substantive question — same turn as the answer, not "later." A message can
also carry a pain point with no question attached: a client naming a blocker, or a champion relaying
a colleague's complaint. Same rule, same turn. Which database each one lands in is convo-mining's
call, not this skill's.

**The capture databases, their schemas, and the routing between them are owned by `convo-mining`.**
Load it, plus the reference file for each database you're writing to. None of its databases is Slack-only
— training and sales-call material lands in the same tables, which is what makes a repeat spanning a
Slack thread and a training call visible at all. Keeping one copy of the schema is why it lives
there and not here.

Only the Slack-specific parts belong in this skill:

| Field | Slack value |
|---|---|
| `Source` | `Slack` |
| `Source Link` | The permalink in **Shaw's** workspace (`aibuilderacademy.slack.com/archives/...`). Never the client-workspace link — he can't open it |
| `Asker` | The person who actually asked. On a forwarded message that's the original author, not the champion who forwarded it |
