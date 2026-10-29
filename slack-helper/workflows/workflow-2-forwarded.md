# Workflow 2: Reading a Forwarded Message

This is the gotcha that will otherwise cost you the whole answer, so it gets its own workflow.

**The symptom:** a message comes back from the connector as literally nothing but
`Forwarded message from <Name> (https://<client>.slack.com/archives/...)`. The text is empty. The
suggestion to "use slack_read_thread to read the original" is a dead end — the original lives in
the *client's* workspace, where the connector has no install, and every attempt returns
`channel_not_found`. Searching `from:<Name>` also returns nothing, for the same reason.

This is common and will keep happening: a client champion sees a question in their internal channel
and forwards it into the shared channel. That's the intended flow. The content is genuinely
visible to Shaw in Slack — it's the API that strips it.

**The fix — read it through Chrome**, where Shaw is already logged in:

1. Do **not** navigate to the `aibuilderacademy.slack.com/archives/...` permalink. It serves a
   "Launching AI Builder Academy… you will be redirected" interstitial and no content.
2. Navigate instead to the web client: `https://app.slack.com/client/<team-id>/<channel_id>`
3. The client hydrates asynchronously. `get_page_text` immediately after navigating often returns
   "No text content found" — that's the app still booting, not a failure. Call `read_page` first
   (which works earlier), or simply call `get_page_text` again.
4. `get_page_text` on the loaded client returns the full channel including the forwarded body,
   attributed to the original author with a `From <Client> | <time>` footer.

Attachments, file shares, and canvas posts fail the same way and take the same fix.

Leave the tab open if Shaw may want to reply by hand; mention that you did.
