---
name: email-writer
description: >
  Draft emails in Shaw's voice and style. Use this skill whenever Shaw asks to write, draft,
  compose, or reply to an email, including phrases like "draft a reply", "write an email to",
  "respond to this", "send them a message", "follow up with", or any reference to composing
  email. Also trigger when Shaw shares an email thread and asks what to say, or when creating
  Gmail drafts as part of a workflow. Even casual requests like "shoot them an email" or
  "write back to X" should trigger this skill. This skill covers all email types: outreach,
  replies, follow-ups, declines, introductions, three-way intros, and scheduling.
---

# Email Writer

Draft emails that match Shaw's voice. Before drafting, check whether the email falls into a known category (see `references/` directory) and read the relevant reference file.

## Reference Files

- `references/expert-network-replies.md` — Replies to ABA expert network newsletter respondents
- `references/call-follow-ups.md` — Post-call follow-up emails
- `references/three-way-intros.md` — Three-way intro emails connecting leads with Shaw's AI consultants

---

## Handoff to conversion-copy

For emails whose job is conversion — closing a warm lead, reviving a ghost, post-call follow-ups that need a yes — use conversion-copy's `channel-emails.md`. This skill owns general voice, introductions, declines, scheduling, and ABA replies.

---

## Voice

Shaw writes email like he talks — casual, direct, and warm. He sounds like a peer, not a brand. The energy is friendly efficiency: get to the point, be human about it, move things forward.

**Greeting.** "Hey [First Name]," for peers and warm contacts. "Hi [First Name]," for first-time contacts and more formal contexts. Never "Dear" or "Hello there."

**Opening line.** "Thanks for reaching out!" (inbound) or "Thanks for your reply!" (responding). This is a consistent pattern — don't vary it for variety's sake.

**Paragraphs.** One idea per paragraph. 1-2 sentences each. Lots of white space. Emails should feel light on mobile.

**Sign-off.** "Thanks again, Shaw" for more formal contexts. "Cheers, Shaw" for peer-level. "-Shaw" for quick replies. No sign-off in active back-and-forth threads.

**Tone markers.** `:)` not emoji. One per email max, usually near the end. No bold, no headers, no visible formatting — the email should look plain even though it's sent as HTML.

---

## Principles

### Every email has a purpose and ends with a clear next step.

This is the single most important principle. Every email Shaw sends moves the conversation somewhere — a question, a link, a redirect, a booking. Even a decline points to an alternate path. If an email just acknowledges without moving forward, it's not done yet.

This means: one CTA per email, not two. If someone's message is vague, ask one clarifying question rather than guessing. If the answer is "no" or "not now," redirect them somewhere useful. Follow-ups get shorter and more direct each time — never re-pitch, just nudge.

### Shaw never pads for length.

If an email can be 3 lines, it's 3 lines. The length should match what the situation actually requires, not what feels "complete." Personalization is earned — react to what someone said or did, not who they are. Skip filler like "Hope you're doing well!" and go straight to the substance.

### Infer templates from sent mail, don't just use reference files.

Not every recurring email pattern lives in `references/`. Shaw often runs ad hoc campaigns — like emailing multiple speakers for an event series — where he's sending the same structure to each person but it's not worth codifying as a permanent template. When Shaw asks to draft an email and points to examples or the email is clearly part of a batch (same subject pattern, same recipients list, same stage of a workflow), search his sent mail for similar recent emails and use those as the template. Match structure, formatting, tone, links, and CTAs exactly.

**When there are multiple candidates, the newest one wins.** Shaw actively refines templates over time — step names get shortened, framings get tightened, links move around. An email from two weeks ago may already be stale. Sort candidates by date and anchor on the most recent instance; only fall back to older examples to fill in structure the newest one happens to be missing.

The reference files cover stable, long-lived patterns; sent mail covers everything else.

---

## Gmail Technical Notes

### Drafting with `create_draft`

The Gmail MCP tool `create_draft` accepts `to`, `subject`, `body` (plain text), and `htmlBody` (HTML). It does NOT currently accept a `threadId` or `contentType` parameter, so every draft created this way starts a fresh thread. Use `htmlBody` whenever the message has paragraphs, links, or any structure — Gmail's plain text mode auto-wraps lines at ~78 characters, inserting hard line breaks mid-sentence. In HTML, use `<div>` tags for paragraphs, `<div><br></div>` for blank lines between them, and `<ul><li>` for bullet points (text dashes render as plain text, not actual bullets).

**Plain text `*word*` means bold, not italic.** When reading sent emails via the Gmail API, the plain text body renders bold text as `*word*`. When reproducing this formatting in HTML drafts, use `<b>` tags, not `<i>`.

### Replying on an existing thread (Chrome workaround)

`create_draft` cannot attach a draft to an existing thread, so any reply that needs to land on the original thread (most follow-ups, all CRM nudges, post-call replies) must be authored through the Gmail UI via Claude in Chrome. This is a workaround until the connector restores `threadId` support — when it returns, prefer the API path.

The recipe:

1. **Use the right Gmail account.** `shaw@aibuilder.academy` lives at `https://mail.google.com/mail/u/2/#inbox`. Other indices belong to personal accounts.
2. **Find the thread.** In the Gmail search bar, run `to:<email> subject:"<original subject>"`. Click the result to open it.
3. **Click Reply.** Then click into the body area below the recipient line to place the cursor.
4. **Type the body.** Match the voice and structure you'd produce for an API draft.
5. **Hyperlinks.** Type the anchor text inline (e.g., `here`), select it with `shift+Left` N times, press `cmd+K`, paste the URL, and press Return — Return commits the link reliably.
6. **After the link applies, click back into the body to advance the cursor.** Do NOT press Right or Tab — those move focus to the "..." trimmed-content toggle below the body, and the next keystrokes get silently swallowed instead of appearing in the email.
7. **Verify before handing back.** Zoom into the relevant lines (`computer.zoom`) to confirm punctuation, spacing, and that the link is hyperlinked rather than pasted as raw URL.

Gmail auto-saves the draft as you type. Leave it in Drafts for Shaw to send unless told otherwise.

### Gmail emoji reactions break thread replies

When Shaw reacts to an email with an emoji, Gmail creates a new message in the thread. If you reply via `threadId` (when that path is available again) or scroll past the reaction in Chrome and reply on the original message, the rendering breaks. When the last message in a thread is a reaction, create a fresh thread with a descriptive subject line instead of replying to the existing one.

---

## Batch Outreach Workflow

When drafting the same template for multiple recipients, create one draft first and let Shaw review and edit it. Analyze the diff (subject line, formatting, link placement, etc.) and apply those changes to the remaining drafts. This avoids multiplying mistakes across a batch.
