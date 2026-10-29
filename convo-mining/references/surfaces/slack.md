# Surface: Slack

Shaw's embedded client channels (`#ext-<client>-ai-builder-academy`) and any channel he's been added
to inside a client workspace. `slack-helper` owns reading and posting mechanics — forwarded
messages, thread reading, the connector's quirks. This file covers what happens to what you find.

Two modes: capture one thing as it happens, or sweep a channel for everything that's accumulated.

## Mode A: Log a single item

For something answered or said live. Do it the same turn, not "later."

1. Read the session page (ABA Trainings / ABA Calls) or the engagement for the two relations — see
   the client-lookup gotcha in SKILL.md.
2. Write the row: three-word title, verbatim body, `Source: Slack`, and a Source Link that is the
   permalink in **Shaw's** workspace (`aibuilderacademy.slack.com/archives/...`). A
   `<client>.slack.com` link is unreachable for him and returns `channel_not_found` for you.
3. If this rhymes with rows already in the database, say so. Nobody else is reading these looking
   for repeats.

## Mode B: Sweep a channel

For a channel that's accumulated activity since the last pass — the same operation as mining a
transcript, on a different kind of record.

Read the channel, then walk it in one pass holding the bar for every target database. Most of what
comes back is noise: joins, renames, Slackbot notices, and file-upload stubs dominate any channel's
history, and a new channel is almost entirely that.

Three Slack-specific things change what you extract:

**An empty message text is not an empty message.** Forwarded content, files, canvases, and
attachments all come back blank through the connector. A blank message adjacent to real discussion
is usually the thing being discussed — resolve it via `slack-helper` before deciding there's nothing
there.

**The speaker is the original author, not the forwarder.** A champion forwarding a colleague's
message, or quoting them inline, produces a row whose `Person` is the colleague. Name the relay in
the provenance line instead. This is where a lot of the best pain-point material comes from, and
attributing it to the forwarder destroys the record.

**A message can carry both a question and a pain.** Slack compresses more into one message than
speech does — a single paragraph often contains a request, a complaint, and a question. Apply the
routing rule in SKILL.md per concept, not per message.

## Fields

| Field | Slack value |
|---|---|
| `Source` | `Slack` |
| `Source Link` | The permalink in Shaw's workspace. Never the client-workspace link |
| `Person` / `Asker` | The original author, not the forwarder |
| `Date` | The date the message was posted, not the date you swept |
