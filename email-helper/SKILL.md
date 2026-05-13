---
name: email-helper
description: >
  Draft emails in Shaw's voice and handle any email-adjacent task. Use this skill ANY time
  Claude is composing or about to compose an email — drafting, replying, forwarding, or
  following up. The trigger is the next tool call: if it is `create_draft`, this skill
  should have been invoked first, EVEN when another skill (calendar-helper, crm, outreach,
  engagements, notion-helper, etc.) is already running and the email is one step in its
  workflow — skills compose. Also trigger for phrases like "draft a reply", "write an email
  to", "respond to this", "follow up with", or any reference to composing email; when Shaw
  shares an email thread and asks what to say; or when sharing a link to a Gmail thread
  (Shaw's account uses `u/2` — see Gmail Technical Notes). Casual requests like "shoot them
  an email" count too. Covers outreach, replies, follow-ups, declines, intros, and
  scheduling.
---

# Email Helper

Draft emails that match Shaw's voice. Before drafting, check whether the email falls into a known category (see `references/` directory) and read the relevant reference file.

## Reference Files

- `references/discovery-call-confirmations.md` — Pre-call reply after a lead books an intro call via Calendly
- `references/expert-network-replies.md` — Replies to ABA expert network newsletter respondents
- `references/call-follow-ups.md` — Post-call follow-up emails
- `references/three-way-intros.md` — Three-way intro emails connecting leads with Shaw's AI consultants

---

## Handoff to conversion-copy

For emails whose job is conversion — closing a warm lead, reviving a ghost, post-call follow-ups that need a yes — use conversion-copy's `channel-emails.md`. This skill owns general voice, introductions, declines, scheduling, and ABA replies.

---

## When another skill is already running

If you are already inside another skill's workflow (calendar-helper for a session, crm for a follow-up nudge, outreach for a batch send, engagements for a wrap-up, etc.) and the next thing to do is draft an email, invoke email-helper *before* composing — don't reach for `create_draft` directly. Skills compose; the parent skill stays in charge of its workflow, and email-helper owns voice, formatting, and Gmail mechanics for the specific email being drafted. Skipping this step is how plain-text drafts, broken bullets, and stale templates slip through.

## Voice

Shaw writes email like he talks — casual, direct, and warm. He sounds like a peer, not a brand. The energy is friendly efficiency: get to the point, be human about it, move things forward.

**Greeting.** "Hey [First Name]," for peers and warm contacts. "Hi [First Name]," for first-time contacts and more formal contexts. Never "Dear" or "Hello there."

**Opening line.** "Thanks for reaching out!" (inbound) or "Thanks for your reply!" (responding). This is a consistent pattern — don't vary it for variety's sake.

**Paragraphs.** One idea per paragraph. 1-2 sentences each. Lots of white space. Emails should feel light on mobile.

**Sign-off.** "Thanks again, Shaw" for more formal contexts. "Cheers, Shaw" for peer-level. "-Shaw" for quick replies. No sign-off in active back-and-forth threads.

**Tone markers.** `:)` not emoji. One per email max, usually near the end. No bold, no headers, no visible formatting — the email should look plain even though it's sent as HTML.

**Punctuation.** Never use em dashes (`—`) in drafted emails. Use a period, a comma, or split into two sentences. Shaw doesn't use them and they read as AI-written.

### Proposing time options

When the email proposes specific call times (rather than offering a Calendly link), the format depends on whether you're offering a menu or a single time. For *which* times to pick, see calendar-helper's "Picking times to propose."

**Shared conventions (apply to both formats):**

- **Compressed times.** `2PM` not `2:00 PM`.
- **Don't say "e-meet".** Use "(virtually) meet" or just "meet".

#### Multi-option list (initial proposals, multiple options)

Use when offering a menu of times — typically the first proposal in a thread, where the recipient is choosing from your availability.

- **Abbreviated weekday + date, bolded.** `**Tues, May 12**`, `**Wed, May 13**`, `**Thurs, May 14**`. One line per day.
- **Include an escape hatch closer.** Something like `Let me know what works best or if another time works better :)` — gives the recipient permission to counter-propose.

Example:

> Would any of these times next week work? All ET:
>
> - **Tues, May 12**: 2PM, 3PM, 4PM
> - **Wed, May 13**: 2PM, 3PM, 4PM
> - **Thurs, May 14**: 11AM, 3PM, 4PM
>
> Let me know what works best or if another time works better :)

#### Single time inline (follow-ups, concise nudges)

Use when suggesting one specific time inline — typically a follow-up where you're narrowing the original menu, or any reply where keeping the email concise matters. Shaw's pattern is to pick one time from his earlier proposal rather than re-propose the full list.

- **Parenthetical date, plain text.** `Thurs (May 14)` — not bold, no comma. The bold + comma format is reserved for the multi-option list above.
- **Drop the escape hatch.** No "let me know if another time works better." The brevity is the point; the recipient can still counter-propose without being invited to.
- **Drop the `:)`.** Skip the tone marker on tight nudges — it softens what should land as a direct ask.

Example (FU after a multi-option proposal went unanswered):

> Hi [First Name],
>
> Just bumping this up.
>
> Would Thurs (May 14) at 4PM ET work?
>
> -Shaw

---

## Principles

### Every email has a purpose and ends with a clear next step.

This is the single most important principle. Every email Shaw sends moves the conversation somewhere — a question, a link, a redirect, a booking. Even a decline points to an alternate path. If an email just acknowledges without moving forward, it's not done yet.

This means: one CTA per email, not two. If someone's message is vague, ask one clarifying question rather than guessing. If the answer is "no" or "not now," redirect them somewhere useful. Follow-ups get shorter and more direct each time — never re-pitch, just nudge.

**Follow-up paragraph breaks.** On tight follow-ups, break the bumping line, the question/ask, and the sign-off into separate paragraphs even when each is one sentence. Running them together visually loads up the email; splitting them keeps the brevity legible. The "Single time inline" example above shows the pattern.

### Shaw never pads for length.

If an email can be 3 lines, it's 3 lines. The length should match what the situation actually requires, not what feels "complete." Personalization is earned — react to what someone said or did, not who they are. Skip filler like "Hope you're doing well!" and go straight to the substance.

**Default to 3 sections in the body, never more than 5.** Body sections = the distinct ideas or asks between the opener and the wrap-up. When an email starts feeling heavy, reach for compression: fuse the opener and the reaction into one sentence, drop a forced compliment, trim parentheticals the reader doesn't need. These are tools to pull when the email is dense, not rules to apply every time.

### Read the full thread before drafting a follow-up.

Search snippets are lossy — they cut off mid-sentence and routinely miss the substantive parts of a message (proposed times, attached outlines, specific questions asked). Before drafting any follow-up or reply, fetch the full sent message body with `get_thread`, not just the search snippet. What was already proposed in the prior message directly shapes what the follow-up should say: narrow a previously-offered menu rather than re-opening the ask, reference a specific question that was raised, etc. Drafting from a snippet leads to vague nudges that ignore the live state of the conversation.

### Infer templates from sent mail, don't just use reference files.

Not every recurring email pattern lives in `references/`. Shaw often runs ad hoc campaigns — like emailing multiple speakers for an event series — where he's sending the same structure to each person but it's not worth codifying as a permanent template. When Shaw asks to draft an email and points to examples or the email is clearly part of a batch (same subject pattern, same recipients list, same stage of a workflow), search his sent mail for similar recent emails and use those as the template. Match structure, formatting, tone, links, and CTAs exactly.

**When there are multiple candidates, the newest one wins.** Shaw actively refines templates over time — step names get shortened, framings get tightened, links move around. An email from two weeks ago may already be stale. Sort candidates by date and anchor on the most recent instance; only fall back to older examples to fill in structure the newest one happens to be missing.

The reference files cover stable, long-lived patterns; sent mail covers everything else.

### Check Notion SOPs for templated workflows.

Some recurring email patterns are codified as part of larger operational SOPs in Notion (e.g., delivery sessions, post-event sends, kickoffs, structured follow-ups, testimonial asks). When the email Shaw is asking for fits one of these workflows, check the SOPs page first before drafting from scratch.

SOPs parent page: `[page-id]`. SOP-backed email types currently include:

- Post Event (slides + recording, recording link)
- 1:1 Claude Workshop (pre-session agenda, follow-up, testimonial asks)
- Group Claude Workshop

When both an SOP template and recent sent mail exist, prefer sent mail — Shaw refines templates by editing on the way out, so the most recent send is the most current source. Flag the divergence so `sop-helper` can update the SOP to match.

---

## Calendly Links and When to Use Them

Pick the right Calendly link based on what the lead is asking for:

| Inquiry type | Calendly link |
|---|---|
| Corporate / team AI training | `[calendar-link] |
| 1:1 Claude Workshop (individual) | `[calendar-link] |
| Coffee chats with friends, colleagues, founders, peers | `[calendar-link] |
| General intro / doesn't fit above | `[calendar-link] |

Default to `ai-transformation` when the lead mentions "my company," "my team," "our organization," or any language suggesting a group training need. Default to `claude-workshop-discovery` for individuals looking for a hands-on Claude session. Default to `coffee-chat` when the conversation is peer-to-peer (founder-to-founder, fellow consultant, mutual contact, no commercial intent). Use `aba-intro-call` when the ask is vague or doesn't fit elsewhere.

### When to offer Calendly vs. propose specific times

**Default: offer the Calendly link.** It's the lowest-friction path for most people and lets them self-serve.

**Exception: propose specific times in the email when the recipient is a senior leader, exec, or otherwise very busy person.** They often won't click through to Calendly — clicking a link, reviewing times, and booking is more friction than picking from a list in their inbox. They prefer to operate in email. Examples: CEOs, C-suite execs, well-known investors, and anyone whose calendar is gatekept by an EA.

When proposing specific times manually, see calendar-helper's "Picking times to propose" for which times to pick, and "Proposing time options" under Voice above for how to format them.

---

## Gmail Technical Notes

### Gmail accounts and the `u/` path

Shaw is signed into multiple Gmail accounts in the same browser, and each one is addressed by a `u/N` index in the URL:

- `u/2` — `shaw@aibuilder.academy` — the **business inbox**. All ABA outbound sales activity, the connected Gmail MCP tool, and the canonical destination for thread links.
- `u/1` — `shawhintalebi@gmail.com` — **personal inbox**. This is where the contact form on `shawhintalebi.com` lands (Squarespace forwards submissions here, not to the business address).
- `u/0` — other personal account.

When pasting a Gmail link into chat or Notion, always use:

`https://mail.google.com/mail/u/2/#inbox/<threadId>`

The `u/2` path opens the business inbox. Using `u/0` or `u/1` will open the wrong account and the link will fail to resolve the thread. This applies to thread links AND individual message links (`/<messageId>`).

### Searching Gmail for context

When you need conversation context with a specific person — an upcoming session, a stalled lead, what was last agreed in a back-and-forth — anchor the search on the relationship, not on the subject. Subject lines drift over time (Shaw might use "Tomorrow's 1:1 Session" one week and "Tomorrow's Session" the next), so a search filtered to one exact subject silently misses anything that drifted. Search by recipient pair first (`to:[email] OR from:[email]`, optionally with `newer_than:30d` to keep it tight), then read the freshest threads to find the live conversation.

**The live thread wins.** The most recent thread with the person — regardless of its subject — is where the current conversation actually lives. Reschedules, agenda updates, blockers, and BAMFAM commitments all land in whatever thread happened to be open at the time, not in a thread named after the template. When deciding which thread to reply on, pick the live conversation (subject to the emoji-reaction fallback below), not the template-named thread.

**Exact-subject searches are a tertiary tool.** Use `subject:"..."` filters only when looking for a specific template instance — e.g., "find the most recent 'Tomorrow's 1:1 Session' I've ever sent, to anyone, so I can match its structure." Never use exact-subject filters as the primary way to surface context with a particular person.

### Reading threads the Gmail MCP can't see

The connected Gmail MCP is scoped to one inbox and search hits sometimes miss threads filtered into custom labels — most commonly contact-form submissions in `shawhintalebi@gmail.com` that get auto-labeled `stv/Website/contacts` and never land in the main inbox view. If the CRM notes (or any other source) reference an email exchange but `search_threads` comes back empty, fall back to Claude in Chrome:

1. Open Gmail at `https://mail.google.com/mail/u/1/#search/<keyword>` for the personal account, or `u/2` for the business account. Pick the account based on where the thread should live (contact form → `u/1`; outbound sales → `u/2`).
2. Click the result to open the thread.
3. Use `get_page_text` to read the full body in one call — Gmail renders the entire thread inline.
4. Treat what you read like normal email context: extract goals, asks, pain points, then move on.

Reach for this only when the MCP comes back empty for a thread that other evidence says exists. The MCP is faster and quieter for everything else.

### Drafting with `create_draft`

The Gmail MCP tool `create_draft` accepts `to`, `subject`, `body` (plain text), `htmlBody` (HTML), and `replyToMessageId`. Use `htmlBody` whenever the message has paragraphs, links, or any structure — Gmail's plain text mode auto-wraps lines at ~78 characters, inserting hard line breaks mid-sentence. In HTML, use `<div>` tags for paragraphs, `<div><br></div>` for blank lines between them, and `<ul><li>` for bullet points (text dashes render as plain text, not actual bullets).

**Threading.** To attach the draft to an existing thread (most follow-ups, all CRM nudges, post-call replies), pass `replyToMessageId` set to the most recent message ID in that thread — find it via `search_threads` or `get_thread`. Omit `replyToMessageId` to start a fresh thread. The reply subject should be the original subject prefixed with `Re:` (e.g., `Re: [Name] / Shaw - Check-in`). Pick the thread per "The live thread wins" above — don't reply on a stale template-named thread when the actual conversation has moved elsewhere.

**List spacing.** When a `<ul>` follows a line of text, attach it directly — no `<div><br></div>` between the text and the opening `<ul>`, and none between the closing `</ul>` and the next line. HTML `<ul>` already renders with its own top/bottom margin; adding blank-line divs doubles the gap.

**Plain text `*word*` means bold, not italic.** When reading sent emails via the Gmail API, the plain text body renders bold text as `*word*`. When reproducing this formatting in HTML drafts, use `<b>` tags, not `<i>`.

### Gmail emoji reactions break thread replies

When Shaw reacts to an email with an emoji, Gmail creates a new message in the thread. Replying after a reaction (via `replyToMessageId`) breaks the rendering. When the last message in a thread is a reaction, create a fresh thread with a descriptive subject line instead of replying to the existing one. This rule overrides "the live thread wins" — if the live thread ends in a reaction, fall back to a fresh thread.

### Squarespace contact-form threads

The `shawhintalebi.com` contact form forwards to `u/1` from `[email]`, with the actual sender's name and email in the body. Gmail's Reply button parses that real email out of the body and pre-fills it as the recipient — so click Reply on the thread to keep everything threaded under `Form Submission - Contact Page`. Composing a new email instead loses the thread and breaks future CRM cross-referencing.

**Reply mechanics.** Reply in the u/1 thread (via Chrome — click Reply on the Squarespace message) and **CC `shaw@aibuilder.academy`**. This keeps the thread clean in the personal inbox while ensuring the business inbox has a copy. Do NOT create a standalone draft in the business inbox — that loses the thread and the CC link.

**Calendly link selection.** See "Calendly Links and When to Use Them" above for the full link table and selection logic.

---

## Batch Outreach Workflow

When drafting the same template for multiple recipients, create one draft first and let Shaw review and edit it. Analyze the diff (subject line, formatting, link placement, etc.) and apply those changes to the remaining drafts. This avoids multiplying mistakes across a batch.
