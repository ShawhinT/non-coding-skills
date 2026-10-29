# Workflow 1: Sweep for New Activity

The default answer to "anything happening in Slack?"

1. `slack_search_public_and_private` with `after:YYYY-MM-DD`, `sort: "timestamp"`,
   `include_context: false`. Use the last few days unless Shaw names a window.
2. Run two more searches for what's directed at Shaw, because each finds what the other misses.
   `to:me after:YYYY-MM-DD` returns DMs, where he is the recipient. A keyword search on his
   mention token (`<@USER_ID>`, with the ID from Workspace Facts in `SKILL.md`) returns @mentions
   in channels and threads, where the recipient is the channel rather than him.
3. **Filter the noise ruthlessly.** Slack's own signal-to-noise here is terrible — joins, channel
   renames, Slackbot trial nags, and "X was added to this channel" all come back as results.
   None of it is activity. Report what a person actually said.
4. Any result with **empty `Text`** is not an empty message — it's a forwarded message, a file, or
   an attachment the connector couldn't render. Go to Workflow 2 before reporting it.
5. Read the channel around anything interesting (`slack_read_channel`) to get thread context, and
   `slack_read_thread` where a thread exists.

**Reporting:** multi-item sweeps use the `skimmable-summary` house format. A single item doesn't —
just say what it is. Always distinguish "needs an answer" from "setup noise" explicitly; the point
of the sweep is to spare Shaw from reading the noise himself.
