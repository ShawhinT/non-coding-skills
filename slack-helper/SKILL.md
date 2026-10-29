---
name: "slack-helper"
description: "Run Shaw's embedded client Slack channels — the async support surface of the Fractional AI Department retainer. Sweep channels for new questions, unpack forwarded messages the connector strips to nothing, draft answers and outbound posts in Shaw's voice, and get every Q&A and pain point logged (the databases are owned by `convo-mining`). Use whenever Shaw mentions Slack at all, even in passing: \"anything happening in slack\", \"any new questions\", \"what did X ask\", \"read that thread\", \"can you read the forwarded message\", \"draft a reply to this\", \"log this Q&A\", \"who's asked what this week\". Also fires for outbound posts to a client channel (an intro, an announcement, a heads-up to the whole org), whenever a client question needs an answer or a record, and whenever a Slack tool call (slack_read_channel, slack_search_public_and_private, slack_read_thread, slack_send_message_draft) is the next thing you're about to do. Do NOT use for LinkedIn, email, or internal chat unrelated to client support."
---

# Slack Helper

Runs Shaw's embedded client Slack channels — the async support surface of the **Fractional AI
Department** retainer.

The offer promises "unlimited async access to Shaw — shared company Slack channel, answered within
1 business day." That promise is the whole reason this skill exists, and it sets the standard: a
question sitting unanswered past one business day is a missed deliverable, not an inbox item.

**Every question is three things at once** — a deliverable being delivered, evidence of value for
the renewal conversation, and raw material for content and future skills. That's why answering is
only half the job. The other half is logging it to Notion. A question answered in Slack and never
recorded is worth exactly one answer; recorded, it compounds.

---

## Workspace Facts

| Thing | Value |
|---|---|
| Workspace | AI Builder Academy — `aibuilderacademy.slack.com` |
| Team ID | `[team-id]` |
| Shaw's user ID | `[user-id]` |
| [Company] — champions | `#ext-[company]-ai-builder-academy` → `[channel-id]` ([Person], [Person 2], [Person 3]) |
| [Company] — org-wide | `#ai-community` → `[channel-id]` ([Company]'s own channel, whole company) |

Client channels are **Slack Connect**, which is a paid feature. The workspace has been on a Pro
trial; if external channels suddenly vanish or go read-only, check the plan before debugging
anything else.

**Channel names are ad hoc, and a client is not one channel.** There's no naming convention to
infer from — `#ext-[company]-ai-builder-academy` is just what that one happened to get called.
A client typically has at least two surfaces: the small channel with the champions, and the
client's own org-wide channel that Shaw was invited into, which carries none of ABA's naming.
Resolve them with `slack_search_channels` and read the member list before drawing any conclusion
about reach. Finding no questions in the champions channel means the champions had no questions;
the org-wide channel is where the org actually asks.

---

## Workflows

Read the file for the workflow you're running. Each is self-contained.

| Workflow | Trigger | File |
|---|---|---|
| 1. Sweep for New Activity | "anything happening in Slack?", "check Slack", "any new questions", scheduled sweeps | `workflows/workflow-1-sweep.md` |
| 2. Reading a Forwarded Message | A message comes back with empty `Text`; "can you read the forwarded message"; any file, attachment, or canvas post | `workflows/workflow-2-forwarded.md` |
| 3. Answering a Question | A client question needs a reply; "draft a reply to this", "answer this in Slack" (answer content per `client-support`) | `workflows/workflow-3-answering.md` |
| 4. Log it via convo-mining | Anything convo-mining captures came up — a question answered, an objection, a pain point, a result — same turn, not "later" | `workflows/workflow-4-log-qa.md` |
| 5. Posting to a Client Channel | An outbound post rather than a reply: intro, announcement, heads-up to the whole org | `workflows/workflow-5-broadcast.md` |

Workflows 3 and 4 run as a pair — an answer that never gets logged is half the job. Workflow 5 is
the one that isn't a reply, and it runs on a different register; don't reach for the answer voice
in Workflow 3 when writing a broadcast.

---

## Gotchas Worth Remembering

- **Empty message text ≠ empty message.** Forwarded content, files, and attachments all come back
  blank. See Workflow 2.
- **Cross-workspace links are unreachable.** Any `https://<client>.slack.com/...` URL will return
  `channel_not_found`. Don't retry it; go to Chrome.
- **Slack permalinks redirect to a launcher.** Use `app.slack.com/client/<team>/<channel>`.
- **The web client needs a moment to hydrate.** A first empty `get_page_text` is a timing artifact.
- **Sweep results are mostly noise.** Joins, renames, and Slackbot notices dominate a new channel.
- **Never post without explicit approval**, and never treat "handle Slack for me" as standing
  permission to send. This covers replies and broadcasts alike — see Delivering a Message for how
  a message actually leaves.

---

## Delivering a Message

Client channels are Slack Connect, and the connector cannot post into them. `slack_send_message`
fails with `mcp_externally_shared_channel_restricted` every time — approval doesn't change that,
and neither does retrying. The delivery path is `slack_send_message_draft`, which places the text
in that channel's compose box for Shaw to send himself. Wherever a workflow file says to send with
`slack_send_message`, this is the step it means.

The practical consequence is that you can never report a message as sent — you hand Shaw a draft
and he decides. Say so plainly when you hand it over; a draft described as sent is a client
message he thinks went out and didn't.

Approval still comes first, and for the reason it always did: a draft sitting in his Slack is one
click from being public, so it should only ever be text he has already agreed to. Only one draft
can exist per channel, so an existing one has to be cleared before a new one will land.
