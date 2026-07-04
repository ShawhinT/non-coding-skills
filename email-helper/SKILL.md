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
  (Shaw's account uses `u/1` — see Gmail Technical Notes). Casual requests like "shoot them
  an email" count too. Covers outreach, replies, follow-ups, declines, intros, and
  scheduling.
---

# Email Helper

Draft emails that match Shaw's voice. Before drafting, check whether the email falls into a known category (see `references/` directory) and read the relevant reference file.

## Reference Files

- `references/expert-network-replies.md` — Replies to ABA expert network newsletter respondents
- `references/call-follow-ups.md` — Post-call follow-up emails
- `references/three-way-intros.md` — Three-way intro emails connecting leads with Shaw's AI consultants

---

## Handoff to conversion-copy

For emails whose job is conversion — closing a warm lead, reviving a ghost, post-call follow-ups that need a yes — use conversion-copy's `channel-emails.md`. This skill owns general voice, introductions, declines, scheduling, and ABA replies.

This handoff also fires on what *looks* like a simple reply but isn't: a **serious buyer raising friction**. The tell is two things at once — they signal real buying intent *and* they raise a question or objection. Signals include a pricing or "what would it take" question, a discount or negotiation ask, an objection (too expensive, not sure, need to check with the team), or a scope question (can we add X, can we shrink it). Answering these literally ("here's the price") leaves money on the table; route them to conversion-copy's `channel-emails.md`, which carries the pattern for holding value and advancing the deal. Pipeline state is the trigger, not the words — the same price question is conversion from a warm, evaluating lead and pure logistics from an already-closed client.

---

## When another skill is already running

If you are already inside another skill's workflow (calendar-helper for a session, crm for a follow-up nudge, outreach for a batch send, engagements for a wrap-up, etc.) and the next thing to do is draft an email, invoke email-helper *before* composing — don't reach for `create_draft` directly. Skills compose; the parent skill stays in charge of its workflow, and email-helper owns voice, formatting, and Gmail mechanics for the specific email being drafted. Skipping this step is how plain-text drafts, broken bullets, and stale templates slip through.

## Voice

Shaw writes email like he talks — casual, direct, and warm. He sounds like a peer, not a brand. The energy is friendly efficiency: get to the point, be human about it, move things forward.

**Greeting.** "Hey [First Name]," for peers and warm contacts. "Hi [First Name]," for first-time contacts and more formal contexts. Never "Dear" or "Hello there." Drop the greeting entirely on active back-and-forth threads — same rule that drops the sign-off. The reliable tell: mirror the recipient. If their last reply had no greeting and it's a same-day exchange, drop yours too and sign "-Shaw".

**Opening line.** "Thanks for reaching out!" (inbound) or "Thanks for your reply!" (responding). This is a consistent pattern — don't vary it for variety's sake.

**Paragraphs.** One idea per paragraph. 1-2 sentences each. Lots of white space. Emails should feel light on mobile.

**Sign-off.** "Thanks again, Shaw" for more formal contexts. "Cheers, Shaw" for peer-level. "-Shaw" for quick replies. No sign-off in active back-and-forth threads.

**Tone markers.** `:)` not emoji. One per email max, usually near the end. No bold, no headers, no visible formatting — the email should look plain even though it's sent as HTML.

*Exception: proposal/offer follow-ups.* In emails whose body lists the shape of a deal as bullets (format, platform, investment), bold the leading category label on each bullet — e.g. `**1:1 Claude Workshops** (3-4 participants): ...`, `**Virtual live sessions** via Google Meet`, `**Total investment**: $4,500-$6,000`. The labels work as scan-anchors over distinct deal facets, while the rest of the email stays plain. Bold only the label, not the value or the trailing clause. In `create_draft`, use HTML `<b>` inside the `<li>` (plain Markdown `**...**` doesn't render). See the Discovery Call SOP (post-call FU Variant A) for the template.

**Punctuation.** Never use em dashes (`—`) in drafted emails. Use a period, a comma, or split into two sentences. Shaw doesn't use them and they read as AI-written.

**Numerals.** Shaw writes numbers as digits, not words: "$1,500" not "fifteen hundred", "4 groups" not "four", "5-10 hr/wk". Spelled-out numbers read as AI-written.

### Proposing time options

When the email proposes specific call times (rather than offering a Calendly link), the format depends on whether you're offering a menu or a single time. For *which* times to pick, see calendar-helper's "Picking times to propose."

**Shared conventions (apply to both formats):**

- **Compressed times.** `2PM` not `2:00 PM`.
- **Don't say "e-meet".** Use "(virtually) meet" or just "meet".

#### Multi-option list (initial proposals, multiple options)

Use when offering a menu of times — typically the first proposal in a thread, where the recipient is choosing from your availability.

- **Abbreviated weekday + date, bolded.** `**Tues, May 12**`, `**Wed, May 13**`, `**Thurs, May 14**`. One line per day.
- **Ranges over enumerated slots.** When availability is a contiguous window, write the window: `11AM-1PM, 3:30PM-6:30PM`, not `11AM, 12PM, 3:30PM, 4:30PM, 5:30PM`. Enumerate discrete times only when the open slots are actually scattered. A range says "pick anything in here" and reads lighter than a menu of artificial hour marks.
- **Timezone label.** Shaw is Central — label times `CT` when the recipient's zone is unknown or different. Drop the label entirely when the recipient is known-local; it's one more thing to read.
- **Include an escape hatch closer.** Something like `Let me know what works best or if another time works better :)` — gives the recipient permission to counter-propose.

Example (multi-day):

> Would any of these times next week work? All CT:
>
> - **Tues, May 12**: 2PM, 3PM, 4PM
> - **Wed, May 13**: 2PM, 3PM, 4PM
> - **Thurs, May 14**: 11AM, 3PM, 4PM
>
> Let me know what works best or if another time works better :)

**Single-day proposals drop the bullet list.** When all proposed times fall on one day, a one-item bullet list reads heavier than it needs to. Tighten the ask and attach the bold date line directly under it with a line break (`<br>`, not a `<ul>` and not a separate paragraph):

> Any of these times work for Wednesday?
> **Wed, June 17**: 9:30AM, 11AM-1PM, 3:30PM-6:30PM
>
> Let me know what works best or if another time works better :)

Note the ask compresses too: `Any of these times work for Wednesday?` rather than `Would any of these times work? Here's my availability:`.

#### Single time inline (follow-ups, concise nudges)

Use when suggesting one specific time inline — typically a follow-up where you're narrowing the original menu, or any reply where keeping the email concise matters. Shaw's pattern is to pick one time from his earlier proposal rather than re-propose the full list.

- **Parenthetical date, plain text.** `Thurs (May 14)` — not bold, no comma. The bold + comma format is reserved for the multi-option list above.
- **Drop the escape hatch.** No "let me know if another time works better." The brevity is the point; the recipient can still counter-propose without being invited to.
- **Drop the `:)`.** Skip the tone marker on tight nudges — it softens what should land as a direct ask.
- **Opener.** Default to `Just wanted to follow up.` — that's Shaw's most-used FU opener by a wide margin. `Just wanted to check in.` is the alternate for warmer or relationship-anchored contexts (existing client, peer, anyone he's already in rhythm with). `Just bumping this up.` is rare; reach for it only on a thread that has already had a substantive FU and you're sending a one-line escalation, not another full follow-up.

Example (FU after a multi-option proposal went unanswered):

> Hi [First Name],
>
> Just wanted to follow up.
>
> Would Thurs (May 14) at 4PM ET work?
>
> -Shaw

---

## Principles

### Every email has a purpose and ends with a clear next step.

This is the single most important principle. Every email Shaw sends moves the conversation somewhere — a question, a link, a redirect, a booking. Even a decline points to an alternate path. If an email just acknowledges without moving forward, it's not done yet.

**The exception is a closer.** Some replies exist to close a loop, not open the next one: confirming an approved edit, a "got it, done," a final sign-off. Here the resolved loop *is* the purpose, so don't manufacture a CTA to satisfy this rule. A clean confirmation that it's handled is complete on its own.

This means: one CTA per email, not two. If someone's message is vague, ask one clarifying question rather than guessing. If the answer is "no" or "not now," redirect them somewhere useful. Follow-ups get shorter and more direct each time — never re-pitch, just nudge.

**Follow-up paragraph breaks.** On tight follow-ups, break the bumping line, the question/ask, and the sign-off into separate paragraphs even when each is one sentence. Running them together visually loads up the email; splitting them keeps the brevity legible. The "Single time inline" example above shows the pattern.

### Shaw never pads for length.

If an email can be 3 lines, it's 3 lines. The length should match what the situation actually requires, not what feels "complete." Personalization is earned — react to what someone said or did, not who they are. Skip filler like "Hope you're doing well!" and go straight to the substance. When the email answers a direct question — especially pricing — the answer is the first line. Cut the "Happy to..." or "Great question..." preamble and lead with the substance; the warmth can come after, if at all.

**Warm threads compress hardest.** When the recipient already has full context (you just talked, the deal is live, the next step was already agreed), don't restate it. "Happy to put together the 2 proposals we discussed" is padding when the recipient is the one who asked for the proposals — the email's whole job is the ask, so get to it. Subject lines follow the same logic: `Call Wednesday?` beats `[Company] Training Proposals - Call Wednesday?` because the relationship already carries the topic. Reserve descriptive subjects for cold or context-free sends.

**Re-engagement and catch-up asks are 2-3 lines.** When the goal is just to reconnect — a check-in outreach to a quiet lead or past client, a "want to catch up?" nudge — keep it to a warm line plus a single low-friction ask. Don't recap the relationship history, re-list the paths or options you discussed last time, or propose specific times; the low effort is what makes it easy to say yes. (For a revival that carries a real pitch — closing or reviving a warm lead with an offer — that's conversion-copy's domain; see its `channel-emails.md`.)

**Name the specific reason to meet, not a generic one.** When you state why you want to talk or what you'll bring, pull the concrete thing from their context rather than a placeholder. "I'd love to continue the conversation on rolling out Claude across your portfolio companies" beats "I'd love to continue the conversation and share a few insights." The specific material is almost always already sitting in the thread or the CRM notes, so use it. This is conversion-copy's "specific beats vague" applied to everyday email; see that skill for the deeper treatment.

**Default to 3 sections in the body, never more than 5.** Body sections = the distinct ideas or asks between the opener and the wrap-up. When an email starts feeling heavy, reach for compression: fuse the opener and the reaction into one sentence, drop a forced compliment, trim parentheticals the reader doesn't need. These are tools to pull when the email is dense, not rules to apply every time.

### Lead with the forward motion when delivering a no.

When the answer is no — a decline, a "this one won't work," any bad news — Shaw doesn't front-load the rejection. He folds the reason into a subordinate "While [reason]," clause and resolves the sentence on what's next: *"While this role has to be in person, I'll definitely reach out with other opportunities :)"*. Skip the generic politeness scaffolding — an "Unfortunately" up front, a "but" pivot, an apology. That register is the internet's default for rejection emails, and it lands harsher because it makes the no the main event. The warmth comes from leading with the path forward, not from softening the no.

### Find and read the actual thread before drafting.

Shaw's description of what to say is the intent, not the context — the email carries the context. Drafting from his summary alone yields a reply that's on-message but blind to what the person actually wrote. Locate the thread and read it with `get_thread` first; build the draft from their words. If a search comes back empty, search harder (alternate first-name spellings, subject keywords, `u/2`) rather than drafting from the description — the inbound almost always exists.

Search snippets are lossy — they cut off mid-sentence and routinely miss the substantive parts of a message (proposed times, attached outlines, specific questions asked). Before drafting any follow-up or reply, fetch the full sent message body with `get_thread`, not just the search snippet. What was already proposed in the prior message directly shapes what the follow-up should say: narrow a previously-offered menu rather than re-opening the ask, reference a specific question that was raised, etc. Drafting from a snippet leads to vague nudges that ignore the live state of the conversation.

### Confirming a calendar hold replies on the invite itself.

When Shaw says "reply to the hold/event" or wants to confirm a tentative time ("see if it's still a good time to check in"), the email goes *on the calendar invitation itself* — the Google Calendar message whose subject is the event title (e.g. `[HOLD] [Company] (Product) / Shaw - Check-in`), addressed to the event's guests. Don't route it to the most recent content/follow-up thread; "the live thread wins" doesn't apply here, because the invite is the canonical place to confirm timing and already renders the date, time, and Meet link inline. Find it with `from:me to:<guest> newer_than:Xd` or by the event title, and reply to that message.

Because the invite already shows the *when*, the body is a bare one-liner, not a formatted scheduling nudge: `Is this still a good time for a check-in?` + `-Shaw`. No greeting, no restating the date/time, no proposing alternatives, and only the event's guests on the recipient list (don't add a cc who isn't a guest). If they can't make it, *then* it becomes a reschedule and the normal time-proposing format applies.

### Check if it's already been sent before drafting.

Recurring templated emails (workshop welcome, pre-session agenda, post-call FU, testimonial ask) are easy to draft twice. Shaw is often a few days removed from sending the first one, and a "draft me an X for Y" request doesn't always mean Y hasn't already gotten X. The Notion task being open isn't proof the send hasn't happened either, since Shaw doesn't always check off tasks the moment they're done.

Before drafting any SOP-templated email, search sent mail for the recipient (`from:me to:<email> newer_than:30d`, or whatever window fits the template) and scan results for a thread whose content matches the template's intent.

If a match exists, don't draft. Reply with a one-line summary, the Gmail link to that thread (`https://mail.google.com/mail/u/1/#inbox/<threadId>`), and ask whether to reply on that thread with a nudge or draft something else instead. If no match, proceed normally.

The cost of drafting a duplicate is higher than the cost of one extra search.

### Infer templates from sent mail, don't just use reference files.

Not every recurring email pattern lives in `references/`. Shaw often runs ad hoc campaigns — like emailing multiple speakers for an event series — where he's sending the same structure to each person but it's not worth codifying as a permanent template. When Shaw asks to draft an email and points to examples or the email is clearly part of a batch (same subject pattern, same recipients list, same stage of a workflow), search his sent mail for similar recent emails and use those as the template. Match structure, formatting, tone, links, and CTAs exactly.

**When there are multiple candidates, the newest one wins.** Shaw actively refines templates over time — step names get shortened, framings get tightened, links move around. An email from two weeks ago may already be stale. Sort candidates by date and anchor on the most recent instance; only fall back to older examples to fill in structure the newest one happens to be missing.

The reference files cover stable, long-lived patterns; sent mail covers everything else.

### Check Notion SOPs for templated workflows.

Most recurring email patterns are codified as canonical templates inside the Notion SOPs — that's the single source of truth. When the email Shaw is asking for fits one of these workflows, draft from the SOP template rather than from scratch or from a reference file.

SOPs parent page: `[page-id]`. Each SOP carries its email templates below a `---` divider; SOPs are discovered via the SOPs page by matching the SOP title (see `notion-helper`) — reference SOPs by name, not by hardcoded ID. Which SOP carries which email templates:

- **Discovery Call** — confirmation email (reply inside the Calendly notification thread so context carries; `to:` is the invitee's email pulled from the notification body, *not* `notifications@calendly.com` — unless the lead came via the contact form or a sales thread, in which case reply there; fired by CRM Workflow 7); post-call FU (Variant A: with proposal/options, Variant B: resources).
- **1:1 Claude Workshop** — pre-session agenda, day-of nudge, call follow-up
- **Check-in Call** (base SOP + three spokes) — the follow-up templates live in specific spokes: post-call FU **Variant A** (post-session, multi-ask: next steps + review + referral) lives in **Check-in Call (1:1 Claude Workshop)**; the **"Checking in" outreach** and post-call FU **Variant B** (nurture recap) live in **Check-in Call (Client Nurture)** (**Check-in Call (Lead Nurture)** reuses those two templates). The **"Checking in" outreach** also serves the long-gap reconnect — a lapsed past client coming due after months (~6-12wk+); anchor it on one specific detail from the last conversation and acknowledge the gap (see CRM `follow-up-guidance.md` for the cadence ladder).
- **Wrap-up Call** — scheduling email, wrap-up follow-up, testimonial asks (Variants A and B)
- **Group Claude Workshop** — group kickoff, group feedback form, champion check-in invite
- **Event Series** — speaker hand-off, talk follow-up
- **Post Event** — slides + resources, recording link

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

- `u/1` — `shaw@aibuilder.academy` — the **business inbox**. All ABA outbound sales activity, the connected Gmail MCP tool, and the canonical destination for thread links.
- `u/2` — `shawhintalebi@gmail.com` — **non-ABA business inbox** (Shaw's personal-brand / `shawhintalebi.com` business, distinct from AI Builder Academy). This is where the contact form on `shawhintalebi.com` lands (Squarespace forwards submissions here, not to the ABA address).
- `u/0` — personal account.

When pasting a Gmail link into chat or Notion, always use:

`https://mail.google.com/mail/u/1/#inbox/<threadId>`

The `u/1` path opens the business inbox. Using `u/0` or `u/2` will open the wrong account and the link will fail to resolve the thread. This applies to thread links AND individual message links (`/<messageId>`).

### Searching Gmail for context

When you need conversation context with a specific person — an upcoming session, a stalled lead, what was last agreed in a back-and-forth — anchor the search on the relationship, not on the subject. Subject lines drift over time (Shaw might use "Tomorrow's 1:1 Session" one week and "Tomorrow's Session" the next), so a search filtered to one exact subject silently misses anything that drifted. Search by recipient pair first (`to:[email] OR from:[email]`, optionally with `newer_than:30d` to keep it tight), then read the freshest threads to find the live conversation.

**The live thread wins.** The most recent thread with the person — regardless of its subject — is where the current conversation actually lives. Reschedules, agenda updates, blockers, and BAMFAM commitments all land in whatever thread happened to be open at the time, not in a thread named after the template. When deciding which thread to reply on, pick the live conversation (subject to the emoji-reaction fallback below), not the template-named thread.

**Exact-subject searches are a tertiary tool.** Use `subject:"..."` filters only when looking for a specific template instance — e.g., "find the most recent 'Tomorrow's 1:1 Session' I've ever sent, to anyone, so I can match its structure." Never use exact-subject filters as the primary way to surface context with a particular person.

**Long threads overflow `get_thread` at `FULL_CONTENT`.** A thread with many messages (a months-long client/team chain) can blow past the response token limit and force a fallback. When all you need is the message list — dates, senders, subjects, and the latest message ID for `replyToMessageId` — call `get_thread` with `MINIMAL` format first; it returns the structure without the bodies. Reach for `FULL_CONTENT` only once you know the specific message whose body you actually need to read, or rely on `search_threads` snippets plus the CRM notes for the running context.

### Reading threads the Gmail MCP can't see

The connected Gmail MCP is scoped to one inbox and search hits sometimes miss threads filtered into custom labels — most commonly contact-form submissions in `shawhintalebi@gmail.com` that get auto-labeled `stv/Website/contacts` and never land in the main inbox view. If the CRM notes (or any other source) reference an email exchange but `search_threads` comes back empty, fall back to Claude in Chrome:

1. Open Gmail at `https://mail.google.com/mail/u/2/#search/<keyword>` for the non-ABA business account (`shawhintalebi@gmail.com`), or `u/1` for the ABA business account. Pick the account based on where the thread should live (contact form → `u/2`; ABA outbound sales → `u/1`).
2. Click the result to open the thread.
3. Use `get_page_text` to read the full body in one call — Gmail renders the entire thread inline.
4. Treat what you read like normal email context: extract goals, asks, pain points, then move on.

Reach for this only when the MCP comes back empty for a thread that other evidence says exists. The MCP is faster and quieter for everything else.

### Drafting with `create_draft`

The Gmail MCP tool `create_draft` accepts `to`, `subject`, `body` (plain text), `htmlBody` (HTML), and `replyToMessageId`. Use `htmlBody` whenever the message has paragraphs, links, or any structure — Gmail's plain text mode auto-wraps lines at ~78 characters, inserting hard line breaks mid-sentence. In HTML, use `<div>` tags for paragraphs, `<div><br></div>` for blank lines between them, and `<ul><li>` for bullet points (text dashes render as plain text, not actual bullets).

**Never set a font, size, or color on the `htmlBody`.** Don't wrap it in a `<div style="font-family:…;font-size:…;color:…">` or put inline `style` font rules on any element. Those overrides force the message into a non-default font (e.g. Arial) that renders visibly different from Shaw's normal sends, and he'll flag it on sight. Use only structural tags — `<div>`, `<br>`, `<ul>`/`<li>`, `<b>`, `<a href>` — and let Gmail apply the inbox's own default font. The email should *look plain even though it's sent as HTML* (see Voice → Tone markers); a font/style wrapper is exactly the visible formatting that rule forbids.

**Links: anchor text vs. bare URL.** Two cases:
- **Anchor text different from the URL** (e.g., "Claude desktop app", "intake form", "book a time [here]") — use `<a href>`. The compose view shows a `google.com/url?q=…` redirect on hover, but the recipient sees clean anchor text and Gmail resolves the link correctly on click.
- **Bare URL visible to the recipient** (e.g., a Calendly link, Google Form, or YouTube URL shown in full) — drop it as plain text inside the `<div>`, not wrapped in `<a href>`. Gmail still linkifies it on send, and skipping the anchor keeps the visible URL clean instead of replacing it with the Google redirect.

**Threading.** To attach the draft to an existing thread (most follow-ups, all CRM nudges, post-call replies), pass `replyToMessageId` set to the most recent message ID in that thread — find it via `search_threads` or `get_thread`. Omit `replyToMessageId` to start a fresh thread. The reply subject should be the original subject prefixed with `Re:` (e.g., `Re: [First Name] / Shaw - Check-in`). Pick the thread per "The live thread wins" above — don't reply on a stale template-named thread when the actual conversation has moved elsewhere.

**List spacing.** When a `<ul>` follows a line of text, attach it directly — no `<div><br></div>` between the text and the opening `<ul>`, and none between the closing `</ul>` and the next line. HTML `<ul>` already renders with its own top/bottom margin; adding blank-line divs doubles the gap.

**Line spacing mirrors the source.** Lines that sit on consecutive lines in the source template, with no blank line between them, stay in back-to-back `<div>`s. A two-line couplet like `If it rings true, just reply "yes, go ahead".` / `If not, happy to tweak :)` is one unit, not two paragraphs. Reserve `<div><br></div>` for where the template actually has a blank line; inserting one between paired lines visually loads the email and Shaw flags it.

**Inline quotes (testimonials, pull-quotes).** Render the quote as `<i>...</i>`, with the attribution on the next line via a single `<br>`, also italic. Don't use `<blockquote>`: Gmail renders it inconsistently (stray indent bar, broken spacing) and Shaw flags it on sight. The connector can't produce the clean gray-bar blockquote, so he adds that by hand if he wants it. (The testimonials skill's polish-framework points here for the testimonial case.)

**Plain text `*word*` means bold, not italic.** When reading sent emails via the Gmail API, the plain text body renders bold text as `*word*`. When reproducing this formatting in HTML drafts, use `<b>` tags, not `<i>`.

### Gmail emoji reactions break thread replies

When Shaw reacts to an email with an emoji, Gmail creates a new message in the thread. Replying after a reaction (via `replyToMessageId`) breaks the rendering. When the last message in a thread is a reaction, create a fresh thread with a descriptive subject line instead of replying to the existing one. This rule overrides "the live thread wins" — if the live thread ends in a reaction, fall back to a fresh thread.

### Squarespace contact-form threads

The `shawhintalebi.com` contact form forwards to `u/2` from `[email]`, with the actual sender's name and email in the body. Gmail's Reply button parses that real email out of the body and pre-fills it as the recipient — so click Reply on the thread to keep everything threaded under `Form Submission - Contact Page`. Composing a new email instead loses the thread and breaks future CRM cross-referencing.

**Reply mechanics.** Reply in the u/2 thread (via Chrome — click Reply on the Squarespace message) and **CC `shaw@aibuilder.academy`**. This keeps the thread clean in the `shawhintalebi` (non-ABA) inbox while ensuring the ABA business inbox has a copy. Do NOT create a standalone draft in the business inbox — that loses the thread and the CC link.

**Calendly link selection.** See "Calendly Links and When to Use Them" above for the full link table and selection logic.

---

## Batch Outreach Workflow

When drafting the same template for multiple recipients, create one draft first and let Shaw review and edit it. Analyze the diff (subject line, formatting, link placement, etc.) and apply those changes to the remaining drafts. This avoids multiplying mistakes across a batch.
