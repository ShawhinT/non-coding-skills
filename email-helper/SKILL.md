---
name: "email-helper"
description: "Draft emails in Shaw's voice, and research his Gmail — this skill covers both writing mail and reading it. Use it ANY time Claude is composing or about to compose an email (drafting, replying, forwarding, following up), and ANY time Claude is searching or reading threads to answer a question, verify a fact, or gather context. The trigger is the next tool call: if it is `create_draft`, `search_threads`, `get_thread`, or `label_thread`, this skill should have been invoked first, EVEN when another skill (crm, meeting-prep, outreach, engagements, notion-helper, etc.) is already running and the email step is part of its workflow — skills compose. Also trigger for \"draft a reply\", \"write an email to\", \"follow up with\"; for \"what did X say\", \"did I ever email X\", \"did X reply\", \"find the thread about Y\", \"search my email for\"; when Shaw shares a thread and asks what to say; or when he shares a Gmail thread link (`u/1`). Covers outreach, replies, follow-ups, declines, intros, and inbox research."
---

# Email Helper

Draft emails that match Shaw's voice. Before drafting, check whether the email falls into a known category (see `references/` directory) and read the relevant reference file.

This skill also owns read-only inbox research — searching and reading threads to answer a question or gather context, with no draft at the end. That work runs on **Gmail Technical Notes** below: search snippets are lossy, `search_threads` truncates a thread's message list, a thread's apparent latest message can be stale, and some mail hides under custom labels. Those are the failure modes that turn a research answer confidently wrong, so read that section before reporting what the inbox says.

## Reference Files

- `references/expert-network-replies.md` — Replies to ABA expert network newsletter respondents
- `references/call-follow-ups.md` — Post-call follow-up emails
- `references/three-way-intros.md` — Intros Shaw makes, connecting leads with his AI consultants (replying to an intro Shaw receives is the Inbound Intro SOP's, not this file's)
- `references/scope-declines.md` — Declining out-of-scope asks (coaching, tutoring, personal-project help) and redirecting to specific resources
- `references/brand-deal-declines.md` — Declining brand deal, sponsorship, and creator-partnership inquiries by handing them to [Contact] at [Company]
- `references/nudges.md` — Nudging a thread where Shaw's last email got no reply: how to pick the angle, real sends, and which closing line fits
- `references/client-troubleshooting-replies.md` — Email register for answering a client's technical question or how-do-I ask; the answer itself is `client-support`'s

---

## Handoff to conversion-copy

For emails whose job is conversion — closing a warm lead, reviving a ghost, post-call follow-ups that need a yes — use conversion-copy's `channel-emails.md`. This skill owns general voice, introductions, declines, scheduling, and ABA replies.

This handoff also fires on what *looks* like a simple reply but isn't: a **serious buyer raising friction**. The tell is two things at once — they signal real buying intent *and* they raise a question or objection. Signals include a pricing or "what would it take" question, a discount or negotiation ask, an objection (too expensive, not sure, need to check with the team), or a scope question (can we add X, can we shrink it). Answering these literally ("here's the price") leaves money on the table; route them to conversion-copy's `channel-emails.md`, which carries the pattern for holding value and advancing the deal. Pipeline state is the trigger, not the words — the same price question is conversion from a warm, evaluating lead and pure logistics from an already-closed client.

## Handoff to client-support

The mirror-image handoff fires on the other side of the sale: a client or workshop participant writing about their own Claude work, whether or not they asked anything. A how-do-I, an "it's not working," a "how do we QA what Claude makes?" and a status update on a check-in ("I've been piggybacking on the team's skills") all route the same way. The reply's content is `client-support`'s — which shape it takes (teach, triage, or a reframe plus a call), what goes in it, and whether the question has been answered before — and this skill owns how it lands as an email (`references/client-troubleshooting-replies.md`). The shape decision is the reason the handoff exists: a procedure written for a design-level question commits Shaw in writing to an approach he'd want to shape live, and the channel skill has no way to tell those questions apart.

---

## When another skill is already running

If you are already inside another skill's workflow (calendar-helper for a session, crm for a follow-up nudge, outreach for a batch send, engagements for a wrap-up, etc.) and the next thing to do is draft an email, invoke email-helper *before* composing — don't reach for `create_draft` directly. Skills compose; the parent skill stays in charge of its workflow, and email-helper owns voice, formatting, and Gmail mechanics for the specific email being drafted. Skipping this step is how plain-text drafts, broken bullets, and stale templates slip through.

## Voice

Shaw writes email like he talks — casual, direct, and warm. He sounds like a peer, not a brand. The energy is friendly efficiency: get to the point, be human about it, move things forward.

**Greeting.** "Hey [First Name]," for peers and warm contacts. "Hi [First Name]," for first-time contacts and more formal contexts. Never "Dear" or "Hello there."

Whether to include one at all is governed by *position in the thread*, not by what the recipient did. The email that opens a thread gets a greeting. Once they've replied and Shaw is replying back, the greeting goes — he's mid-conversation, and a greeting restarts something that's already running. Sign "-Shaw" on those.

Don't mirror the recipient here. People routinely open every message with "Hi Shaw," including their third reply in a same-day exchange; Shaw still drops his. The exception is a reply landing after a long gap, where the thread has gone cold enough that re-opening it is the honest read.

**Mirror register, not greetings.** The rule above is scoped to greetings. Length and register are a different matter, and they *are* mirrored. A busy executive — a CEO, C-suite, anyone writing from their phone between meetings — sends one-line, text-message-length messages, and Shaw matches that: very short lines, no scaffolding, no sign-off. A four-paragraph reply to a two-line message reads as more work than the exchange is worth, however warm it is, and it quietly asks the busiest person on the thread to read the most. Based on a real send ([Person], 8/12/26): he wrote two lines from Bali; Shaw's entire reply was two lines with no sign-off.

**Closeness is its own axis, and it runs the opposite way from warmth.** Mirroring reads the *thread*; this reads the *relationship*, and the two are set independently — a busy friend gets both. The closer Shaw is to someone, the less scaffolding the email carries: an offer he's already described to them in person doesn't get re-explained, the reason for writing doesn't get stated, and the sign-off relaxes ("Talk soon" over "Cheers"). Warmth is what he *adds* for clients, prospects, and cold contacts — not a baseline he relaxes with friends. `text-helper` carries the same gradient for texts, in a sharper form, and its framing is worth borrowing: this is the principle most likely to be applied backwards.

Read closeness off shared history, not off a database: meeting in person, an unprompted share, a reciprocal free offer, a mutual scene. A row in the Notion Friends DB confirms it, but its absence proves nothing — plenty of Shaw's friends were never filed. The reliable tell that a draft has the axis wrong is that everything the recipient would cut is something both parties already know.

**Opening line.** "Thanks for reaching out!" is the default for a genuine inbound — someone Shaw hasn't been talking to who wrote in. Don't vary it for variety's sake.

"Thanks for the reply!" is *not* a default. It's for the first reply back from someone after a long gap, and even then Shaw often skips it. Mid-thread it's dead weight: acknowledgment scaffolding belongs at the start of a conversation, not in the middle of one. Same instinct as the greeting — by the time you're a few messages deep, lead with the substance.

A reaction is not an acknowledgment. Thanking someone for replying acknowledges *that* they wrote; a reaction answers *what* they wrote, and that is how Shaw opens a reply: one or two words that match their energy ("Awesome!", "All good!", "No budget necessary!"), then the substance. He is mirroring their message, so the reaction survives mid-thread where the greeting and the thanks don't. Skip it only when their message gives nothing to react to.

The same holds for a post-call opener reacting to a win they described: name the outcome for them in one clause and move on. Retelling their own anecdote back to them (the numbers, the client, the mechanics) spends a paragraph proving Shaw listened, and it reads as a transcript rather than a reaction. "Love that the client-delivery-hub skill is making an impact for you and your clients" is the whole reaction; the story behind it is theirs to tell. ([Person], 10/14/26.)

"Hope things are going well!" opens a fresh thread to someone Shaw knows but hasn't written to in months — one line that acknowledges the gap, then straight to substance. On cold sends, active threads, and recent contacts it stays banned as filler (see "Shaw never pads for length"). Based on real sends ([Person], [Person] / [Company], 8/26/26).

**Paragraphs.** One idea per paragraph. 1-2 sentences each. Lots of white space. Emails should feel light on mobile.

**Sign-off.** "Thanks again, Shaw" for more formal contexts. "Cheers, Shaw" for peer-level. "-Shaw" for quick replies. No sign-off in active back-and-forth threads.

**Tone markers.** `:)` is the default for a first contact and anything formal. An emoji is fine in a reply or nudge to someone Shaw has gone back and forth with (`😅` on a bump to a client whose inbox he knows is a mess, `🍕🗽` on a "have fun in NYC"), because the register follows the relationship, and a warm thread earns a warmer marker. One per email max, usually near the end. No bold, no headers, no visible formatting — the email should look plain even though it's sent as HTML.

*Exception: proposal/offer follow-ups.* In emails whose body lists the shape of a deal as bullets (format, platform, investment), bold the leading category label on each bullet — e.g. `**1:1 Claude Workshops** (3-4 participants): ...`, `**Virtual live sessions** via Google Meet`, `**Total investment**: $4,500-$6,000`. The labels work as scan-anchors over distinct deal facets, while the rest of the email stays plain. Bold only the label, not the value or the trailing clause. In `create_draft`, use HTML `<b>` inside the `<li>` (plain Markdown `**...**` doesn't render). See the Discovery Call SOP (post-call FU Variant A) for the template.

*Exception: skill bullets.* In emails whose bullets recommend skills to build (session follow-ups, skills roadmaps, next-step lists), bold the skill name inside each bullet — e.g. `Build a **meeting-prep** skill by doing your pre-call news run with Claude once, then telling it to turn that into a skill`. Skill names stay lowercase kebab-case. The bold makes the list scan as a set of named things to build, which is what the reader comes back to the email for. Same HTML mechanic as above: `<b>` inside the `<li>`.

**Punctuation.** Never use em dashes (`—`) in drafted emails. Use a period, a comma, or split into two sentences. Shaw doesn't use them and they read as AI-written.

**Numerals.** Shaw writes numbers as digits, not words: "$1,500" not "fifteen hundred", "4 groups" not "four", "5-10 hr/wk". Spelled-out numbers read as AI-written.

**Soft asks.** When the ask could read as an imposition — changing a plan the other person already offered, asking a favor, proposing something they didn't bring up — float it rather than request permission: `Maybe we can try virtual to save you the drive.` not `Would you be up for doing it virtually?`. The hedge lets them take it or leave it; a direct question puts a yes/no on their plate. Same instinct as the no-oriented `Would you be opposed to a coffee chat?` — both lower the cost of declining, which is what makes them easy to say yes to.

### Proposing time options

When the email proposes specific call times (rather than offering a Calendly link), the format depends on whether you're offering a menu or a single time. For *which* times to pick, see calendar-helper's "Picking times to propose."

**Shared conventions (apply to both formats):**

- **Compressed times.** `2PM` not `2:00 PM`.
- **Don't say "e-meet".** Use "(virtually) meet" or just "meet".

#### Multi-option list (initial proposals, multiple options)

Use when offering a menu of times — typically the first proposal in a thread, where the recipient is choosing from your availability.

- **Abbreviated weekday + date, bolded.** `**Tues, May 12**`, `**Wed, May 13**`, `**Thurs, May 14**`. One line per day.
- **Ranges over enumerated slots.** When availability is a contiguous window, write the window: `11AM-1PM, 3:30PM-6:30PM`, not `11AM, 12PM, 3:30PM, 4:30PM, 5:30PM`. Enumerate discrete times only when the open slots are actually scattered. A range says "pick anything in here" and reads lighter than a menu of artificial hour marks.
- **Timezone label.** Shaw is Central — when the recipient's zone is unknown or different, the label rides on the times themselves (`**Wed, Sep 2**: 8AM PT`), not as an `All CT:` prefix on the ask line; a bare `8AM` looks unfinished, and the prefix costs the ask line a clause it doesn't need. Label once per line, after the last time. Drop the label entirely when the recipient is known-local; it's one more thing to read. (Based on a real send: [Person], 8/26/26.)
- **Include an escape hatch closer.** Something like `Let me know what works best or if another time works better :)` — gives the recipient permission to counter-propose. When the recipient has been hard to pin down (a busy partner, a thread that took several nudges to get a yes), make the fallback the Calendly link instead: `If not, here's my full availability: <link>`. The list still does the work for someone who picks from email, and the link means a miss on all three doesn't cost another round trip. ([Person], 10/14/26.)

Example (multi-day):

> Would any of these times next week work?
>
> - **Tues, May 12**: 2PM, 3PM, 4PM CT
> - **Wed, May 13**: 2PM, 3PM, 4PM CT
> - **Thurs, May 14**: 11AM, 3PM, 4PM CT
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
- **Drop the escape hatch.** No "let me know if another time works better." The brevity is the point; the recipient can still counter-propose without being invited to. This covers a time Shaw is *asking* about. When he has already acted on it (sent the invite, booked the slot) without the recipient picking, close with a short out ("Let me know if that doesn't work."): they never got a turn to say no, and the line gives them one.
- **Drop the `:)`.** Skip the tone marker on tight nudges — it softens what should land as a direct ask.
- **Opener.** When this is a nudge on an unanswered email, the bumping line and the angle come from `references/nudges.md`.

**On a coffee chat or peer catch-up, propose one time and anchor it on what worked before.**
When the other person has already narrowed the window ("next week is slammed, but I'm free
Wed-Friday the week of the 3rd"), a multi-day menu re-opens a decision they've mostly made.
Pick a single slot inside their window, and reuse the time-of-day from your last meeting with
them — if the previous chat landed at 10AM, offer 10AM. It's a time you both already know
works, so it needs no negotiating. Based on a real send ([Person], 7/27/26): he offered Wed-Fri,
Shaw replied `All good! How does Friday (Aug 7) at 10AM sound?`, matching the 10AM of their
prior chat. Note this is the *opposite* default from a busy exec you're trying to book cold,
where the menu is what lowers friction; here the relationship already carries it.

Example (FU after a multi-option proposal went unanswered):

> Hi [First Name],
>
> Just wanted to follow up.
>
> Would Thurs (May 14) at 4PM ET work?
>
> -Shaw

#### When the next step is a call, propose the time — don't promise to send one

A reply that says "I'll reach out next week to get something on the calendar" spends a message and moves nothing: the recipient waits, then has to respond to a second email that asks what this one could have. Name a specific time instead, so the thread's next message is either a yes or a counter.

This holds for any call or meeting — a check-in, a session, a first conversation, a wrap-up, a reschedule — not just re-engagement. Read "check-in," "catch up," or "connect" in a nurture thread as a *call*, which is what the CRM cadence means by it too; a reply treating it as an email touchpoint answers a question nobody asked.

**Convert to the recipient's timezone when they're senior or abroad.** Shaw is Central and labels times `CT` by default, but doing the conversion on their behalf removes the step most likely to stall a reply. Based on a real send ([Person] / [Company], 8/12/26): he is in Australia and proposed "the week commencing 31 August"; Shaw replied `How does Wed, Sep 2 at 8AM Sydney time sound?` — one time, already converted, inside the window he named.

---

## Principles

### Every email has a purpose and ends with a clear next step.

This is the single most important principle. Every email Shaw sends moves the conversation somewhere — a question, a link, a redirect, a booking. Even a decline points to an alternate path. If an email just acknowledges without moving forward, it's not done yet.

**The exception is a closer.** Some replies exist to close a loop, not open the next one: confirming an approved edit, a "got it, done," a final sign-off. Here the resolved loop *is* the purpose, so don't manufacture a CTA to satisfy this rule. A clean confirmation that it's handled is complete on its own. A give is not a manufactured CTA, though: when a client's update exposes an easy next step they may not know about (a feature that does what they're planning by hand, a shortcut to the thing they described), one line pointing at it is the value of replying at all, and it rides inside the closer without turning it into an ask. Based on a real send ([Person] / [Company], 10/21/26): her "all good for now" got the confirmation plus "You can even share it directly within the Claude desktop app."

This means: one CTA per email, not two. If someone's message is vague, ask one clarifying question rather than guessing. If the answer is "no" or "not now," redirect them somewhere useful. A nudge — Shaw's last email got no reply — is written from the message it's chasing, not from a stock line: reread what that message asked, then send whatever makes replying easiest now. Nudges get shorter and more direct each time, never re-pitch, and each one on a thread takes a different angle from the last, because a repeated line reads as a sequence firing rather than a person writing. Nothing gets re-attached by default: the offer is one scroll up, and re-dropping the link reads as automated. Re-link only when it genuinely saves the recipient work: a busy exec, a high-stakes ask, or a long thread where scrolling back is a real cost. Read `references/nudges.md` before drafting one — it carries the angles Shaw reaches for, with real sends, and which closing line fits.

When an email genuinely must carry more than one action for the recipient, enumerate them rather than burying them in prose: announce the count ("Here are a couple of follow-ups:") and number the asks. The one-CTA rule exists to keep the ask visible; explicit enumeration is how visibility survives when a second ask is unavoidable. Inside each item, state any already-done work in past tense ("I updated the calendar invite to 9-10:30AM PT") so the item leads with what's settled and ends with the recipient's part.

**A nudge has two shapes, and nothing in between.** The *standard* nudge is a greeting, the bumping line, the ask, and the sign-off, each as its own paragraph even when each is one sentence; running the bump and the ask together into one paragraph visually loads the email and reads as one dense thought instead of a light touch. The *tight* nudge is a single line with no greeting and at most a `-Shaw`: the question stands on its own because the thread already carries everything else. A greeting stacked on a fused two-sentence body is neither shape and reads as neither. Which one fits is a nudges.md call (see its "Two shapes"); the "Single time inline" example above shows the standard shape.

### The template is the prior; the recipient's memory is the update.

A template or SOP line is the right starting point because it encodes what has worked before. It is not the email. The recipient has read everything Shaw has sent them; the drafter has not, because every draft starts in a fresh context. So the line that comes to mind first is the one most likely already sitting in their inbox, and a template that passes every voice rule still reads as a sequence once the person has seen the same shape twice. People notice this, and it costs replies.

Before drafting any repeat touch (a nudge, a check-in, a close, a follow-up to someone Shaw has written before), read what they have already received: sent mail to them across threads, not just the live one, and for a team engagement to their colleagues, who compare notes. Then update the prior against it. How far it moves depends on how much they've seen. A first email to a new lead is the template nearly verbatim. A fourth touch to a client who has read three stock lines gets rewritten until it could only have been written to them, today.

The levers Shaw pulls to do the updating: the subject line on a fresh thread (`Are you a Claude Power User yet?` over a third `Checking in`), a light read on their current situation in place of the status question (`I suspect the inbox might still be a disaster, so just bumping this up 😅`), a specific give, a different question, a dated return instead of an open door (`I'll check back in next month :)`), humor. The update comes from their reality, not from invention: when the standard line is true (the next call is already booked, so "Looking forward to our call in a couple of weeks" is the honest close), it stays.

### Answer their ask first; anything you're adding comes after.

When a reply is triggered by a direct request — "send me times," "what's the price," "can you take a look?" — that answer is the first thing in the body. Whatever else the email carries is yours, not theirs, and follows it.

Ordering is a separate axis from length. An email can pass every brevity test and still bury the recipient's answer behind a request of your own, which reads as being handled rather than helped. When a second item genuinely belongs in the same email, "Also –" is the hinge: it marks the shift from their business to yours. When that second item is lighter than the first — a nicety, an aside, a standing offer rather than a parallel ask — it goes in a P.S. instead of a paragraph, so the body stays one ask and the aside reads as the afterthought it is. Based on real sends ([Person], 10/21/26: "P.S. Let me know about that GoHighLevel meetup in Dallas; I'd love to swing by :)"; [Person], 10/20/26: "PS Let me know if you get stuck building any of the skills").

### Mirror the inbound's order when they raised several things.

When someone's email carries more than one item — resources they sent, a next step to book, an aside at the end — the reply walks them in the order they were raised. The reader checks the reply against their own message, so a reordering by Shaw's sense of what's settled or important reads as scattered even when every item is answered. Their last, lighter item lands last, or in a P.S. when it sits off the main thread of the email. "Answer their ask first" above covers the single-ask case; this is the same instinct for a multi-item one.

### Shaw never pads for length.

If an email can be 3 lines, it's 3 lines. The length should match what the situation actually requires, not what feels "complete." Personalization is earned — react to what someone said or did, not who they are. Skip filler like "Hope you're doing well!" and go straight to the substance. When the email answers a direct question — especially pricing — the answer is the first line. Cut the "Happy to..." or "Great question..." preamble and lead with the substance; the warmth can come after, if at all.

**Warm threads compress hardest.** When the recipient already has full context (you just talked, the deal is live, the next step was already agreed), don't restate it. "Happy to put together the 2 proposals we discussed" is padding when the recipient is the one who asked for the proposals — the email's whole job is the ask, so get to it. Subject lines follow the same logic: `Call Wednesday?` beats `[Company] Training Proposals - Call Wednesday?` because the relationship already carries the topic. Reserve descriptive subjects for cold or context-free sends.

**Send what's settled; the rest is a call.** A call page's Follow-up section and the transcript are Shaw's to-do list, not the email's body. Most of what's on that list gets handled on the next call or later, so transcribing it produces an email that commits him in writing to plans still being shaped: a date for the next session, a format nobody has picked, what he'll bring, a step the recipient hasn't agreed to. The email carries what is already settled and the one thing the recipient needs to act on now; anything still being decided stays off the page, and a bullet that only restates something both sides have confirmed (an accepted invite, a time already agreed) gets cut. The same goes for the reason behind an ask: the recipient sat through the call where it came up, so "could you send over an updated org chart?" is the whole item, and naming the new hire who prompted it, or spelling out what the working session will cover, reads as a transcript of a conversation they were in. Explain an ask only to someone who wasn't on the call. When the next step is deciding the plan itself, don't write the decision as a menu of options for them to pick from. Ask for a short call to work it out: one line of intent, one ask. Based on real sends ([Person], [Person], 10/14/26), where a two-option scheduling menu became "Do you have 15 minutes this week to discuss the best way to do this?"

**Re-engagement and catch-up asks are 2-3 lines.** When the goal is just to reconnect — a check-in outreach to a quiet lead or past client, a "want to catch up?" nudge — keep it to a warm line plus a single low-friction ask. Don't recap the relationship history or re-list the paths or options you discussed last time; the low effort is what makes it easy to say yes. (For a revival that carries a real pitch — closing or reviving a warm lead with an offer — that's conversion-copy's domain; see its `channel-emails.md`.)

**Name the specific reason to meet, not a generic one.** When you state why you want to talk or what you'll bring, pull the concrete thing from their context rather than a placeholder. "I'd love to continue the conversation on rolling out Claude across your portfolio companies" beats "I'd love to continue the conversation and share a few insights." The specific material is almost always already sitting in the thread or the CRM notes, so use it. This is conversion-copy's "specific beats vague" applied to everyday email; see that skill for the deeper treatment.

**The line budget after a bulleted list is two.** In an email whose substance is a bulleted list (a roadmap, a set of recommendations, next steps), the bullets carry the weight and the prose around them is scaffolding. The shape: greeting, one opener, one line setting up the list, the bullets, then exactly two lines — the payoff the list adds up to, and a sign-off or CTA. That budget is spoken for, so anything else worth saying (a resource link, a caveat, a pointer) goes in a P.S. rather than squeezing in a third line. The bullets themselves can run long; it's the connective prose that has to stay thin. Based on a real send ([Person], 7/29/26).

**Absorb the constraint; don't narrate the derivation.** When work went into a choice — a timezone that clears four locations, a date that leaves enough prep time — the email carries the *result*, not the reasoning. "Here are some timezone-safe times" does the job that a sentence naming each location spends a line on. Explanatory sentences are the hardest padding to catch because they feel like substance; the test is whether the recipient needs the reasoning in order to act, and they almost never do. Same instinct as labeling times in the zone of whoever has to act on them: do the work, don't show it.

**Default to 3 sections in the body, never more than 5.** Body sections = the distinct ideas or asks between the opener and the wrap-up. When an email starts feeling heavy, reach for compression: fuse the opener and the reaction into one sentence, drop a forced compliment, trim parentheticals the reader doesn't need. These are tools to pull when the email is dense, not rules to apply every time.

### Write to the context the thread carries, not the context you have.

Shaw's conversations often span channels, and the thread a message lands in decides what it can assume. Same conversation, same moment, two different messages.

A message continuing an existing thread inherits everything said in it, so it can be a single line with no setup. A message opening a new thread inherits nothing: the recipient meets it cold, so it has to establish where the conversation came from and name what it's asking about, even when that feels redundant to the sender.

This bounds compression. "Shaw never pads for length" cuts what's redundant with context the recipient already has; on a fresh thread, none of it is. The tell that a draft has it backwards is an opener responding to something the reader can't see, or an ask pointing at a decision made somewhere else.

When a conversation moves channels, both messages get sent: the old thread gets the short handoff, so the question is answered where it was asked, and the new thread carries the substance.

Based on a real send ([Person], 9/16/26).

### Don't brief the reader on their own world.

The recipient knows their org, their people, and their priorities better than Shaw does, so anything that explains their world back to them is padding with a whiff of being managed: where the ask came from internally ("coming out of yesterday's AI sync"), why they're the recipient ("since both teams report to you"), or what their own colleague does ("plus [Person], who's supporting the marketing engine work" — just "(plus [Person])"). When an ask originated with a stakeholder, attribute it to the person, not the meeting: "Yesterday, [Person] mentioned..." — the meeting is internal machinery the reader wasn't in. Spend the freed lines on what the recipient gets out of the ask (e.g. "we'll go through 1-3 marketing-specific use cases"). Based on real sends ([Person], [Person] / [Company], 8/26/26).

### State the problem; don't prescribe the fix when they own it.

When you're surfacing something the recipient controls — an unpaid invoice, a missing approval, a stalled handoff inside their own org — the fact *is* the message. Adding what they should do about it ("might be worth nudging accounting") narrates a route they already own, and to a senior person it reads as being managed through their own company.

The bare fact is also what gets acted on, because it leaves them the whole decision rather than one option to evaluate. Based on a real send ([Person], 8/12/26): the draft gave the invoice number, the amount, and a suggestion to chase accounting; Shaw sent one line — `Payment hasn't come through yet` — and he replied `I'll make sure that happens.`

### Acknowledge the inbound, don't engage it.

When an email is triggered by something the recipient submitted — a form, a scorecard, a comment — but the *content* of that submission isn't what the email is about, the acknowledgment still belongs in the opener. `Thanks for submitting the AI Scorecard for [Company]!` names the honest reason Shaw is in their inbox, in one clause, without touching a single answer they gave.

The failure mode is over-correcting. Told the submission isn't the point, the instinct is to cut it entirely — but the email still has to explain why it exists, so the specific reference gets swapped for a vague one (`Thanks for stopping by my site this week`) that's worse on every axis. "Don't worry about X" means don't build the email on X, not don't mention it.

Based on a real send ([Person] / [Company], 8/10/26), where the submitter turned out to be a peer rather than a prospect: Shaw's sent version opened on the submission and moved straight past it.

### Earn the ask with a frame when the recipient is hard to reach.

Reflecting someone's situation back to them is a good default. It shows you read what they wrote, and it costs nothing. But when the email also carries an ask *and* the recipient is slow to reply, the mirror spends the message without giving them anything — it agrees with them and stops.

Lead instead with something they didn't already have: a named concept, a pattern you've seen across other clients, a read on where their situation is headed. Give before you ask. The frame is what earns the reply, not the credential that follows it.

Based on a real send ([Person] / [Company], 7/30/26), a contact who had been hard to get replies from. The draft mirrored his own words back ("costs land well before the gains do, especially when the spend is spread across teams and tools"); Shaw replaced it with a frame plus a forecast — *"Costs usually rise in the early days as people learn how to apply the tech to their work (what I call 'Ignorance Tax'), but should be temporary"* — ahead of the same ask.

### Downgrade a correction, don't announce it.

Any correction carries an implicit accusation: if you're clarifying, the reader failed to get it the first time. Announcing it sharpens that. Treat "Just to be clear," "To clarify," "Actually," and "As I mentioned" as red flags — if a draft opens with one, you're pointing at the reader's mistake rather than fixing it. The repair isn't a set phrase. Usually the opener can just go, and the corrected fact stands on its own; sometimes a light "BTW:" carries it. What matters is that the correction reads as incidental, not as a point being made.

### Dissolve a stated blocker in their words, don't comment on your intent.

When someone says they want the thing but names an obstacle — no budget, no time, not the right quarter — the reply's job is to remove the obstacle, not to explain your position on it. Reach for their own phrasing and negate it: "I don't have budget to hire you" answers to `No budget necessary!`. Using their words is what makes it land as settled rather than argued; a paraphrase reads like a counterproposal.

The failure mode is answering the *frame* instead of the blocker. A draft that says "no pitch intended" or "I wasn't trying to sell you" names the sales dynamic in order to deny it, which keeps it alive for the reader and makes the email about Shaw's intentions rather than their concern. Same instinct as downgrading a correction: don't narrate the meta, just make the obstacle stop mattering, then move to the ask.

Based on a real send ([Person], 7/31/26). He replied "Would love to chat but I don't have budget to hire you - my job is roll out AI tools ;-)". The draft opened `Ha, no pitch intended.`; Shaw sent `No budget necessary! Always happy to chat.` and went straight to the Calendly link.

### Lead with the forward motion when delivering a no.

When the answer is no — a decline, a "this one won't work," any bad news — Shaw doesn't front-load the rejection. He folds the reason into a subordinate "While [reason]," clause and resolves the sentence on what's next: *"While this role has to be in person, I'll definitely reach out with other opportunities :)"*. Skip the generic politeness scaffolding — an "Unfortunately" up front, a "but" pivot, an apology. That register is the internet's default for rejection emails, and it lands harsher because it makes the no the main event. The warmth comes from leading with the path forward, not from softening the no.

Clause order is the whole mechanism, and it's easy to invert: everyday polite-decline writing runs "While [the nice thing], [the no]", which lands the reader on the door closing. Shaw's shape is the reverse — the no rides inside the "While," clause and the sentence resolves on the positive. Before finishing any decline, check what the final clause lands on. Based on a real send ([Person] / [Company], 9/2/26): *"While I'm fully focused on growing AI Builder Academy right now, the instructor model sounds like a great opportunity"*, closing on *"Wishing you and the [Company] team continued success :)"*.

When the no is about *scope* — someone outside the business wanting coaching, tutoring, or one-off technical help — the forward motion is a redirect to a specific resource, and the pattern for finding one is in `references/scope-declines.md`. Read it before drafting that reply.

The same principle governs correcting your own mistake. Own the error in one clause ("I misunderstood [Person]'s email"), then describe the new arrangement on its own merits — what it is and what the recipient gets — without re-describing the superseded version. Restating the old plan ("not the 30-min session I mentioned") re-anchors the reader on the error and makes the change read as something to re-approve rather than an upgrade. Where possible, tie the value to something the recipient already knows ("we'll walk through the 4-step framework I covered in the all-hands, but tailored to your specific work").

### Confirm and proceed on an agreed expansion, don't re-poll.

When a warm or already-closed client has effectively agreed to a next step and only the format or price needs a green light, state the options and price plainly and close on a ready-to-move line ("Happy to move forward either way :)"). Don't reopen the decision by asking which option is "more valuable," and don't hedge the bigger option with caveats like "that might be overkill" — asking the client to re-evaluate, or second-guessing your own offer, stalls a deal that was already moving. Confirming the price *is* the forward motion here; the client picks from a confident menu, not an open question. (For a lead who hasn't committed yet — real buying intent plus a live objection — that's conversion-copy's `channel-emails.md`; this principle is for the client who's already in.)

### Frame a format's built-in trait as a benefit, not a caveat.

Every option carries structural traits — an office hour is a group setting, a longer workshop is a bigger time commitment. Present the trait as an upside for the buyer rather than a disclaimer: the office hour's group nature becomes "others from your team are welcome to join too," not "office hours are really meant for groups, so this might be the wrong fit." The facts are identical; leading with the benefit reads as confidence in the offer, while leading with the limitation plants a doubt the recipient wasn't going to raise on their own.

### Re-derive a template line's rationale for a new audience.

Template lines encode the context they were written for, and the encoded rationale silently stops making sense when the audience changes. "So we can jump right into onboarding Claude" fits someone who knowingly booked a workshop; for a client who just learned their session changed, the honest benefit is "so I can better understand your use case(s)". Before reusing a line outside its home context, re-derive the benefit from the recipient's frame — the words should answer why this helps *them*, not restate the workflow's internal purpose.

### Find and read the actual thread before drafting.

Shaw's description of what to say is the intent, not the context — the email carries the context. Drafting from his summary alone yields a reply that's on-message but blind to what the person actually wrote. Locate the thread and read it with `get_thread` first; build the draft from their words. If a search comes back empty, search harder (name variants like Jon/John, subject keywords, `u/2`) rather than drafting from the description — the inbound almost always exists.

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

This isn't scoped to templates and batches. Before any reply, including a 2-line ack, search sent mail for the *analogous moment* — a win report, a yes, an apology for a slow reply — not just the same workflow. Shaw's register in those small sends is distinctive and mostly undocumented, so his past replies in that moment are the voice reference; a draft written without one tends to carry scaffolding his real sends don't.

**When there are multiple candidates, the newest one wins.** Shaw actively refines templates over time — step names get shortened, framings get tightened, links move around. An email from two weeks ago may already be stale. Sort candidates by date and anchor on the most recent instance; only fall back to older examples to fill in structure the newest one happens to be missing.

The reference files cover stable, long-lived patterns; sent mail covers everything else. (Both sit below the SOP in priority — when a workflow has an SOP template, that wins; see "Check Notion SOPs" below.)

### Check Notion SOPs for templated workflows.

Most recurring email patterns are codified as canonical templates inside the Notion SOPs — that's the single source of truth. When the email Shaw is asking for fits one of these workflows, draft from the SOP template rather than from scratch or from a reference file.

SOPs parent page: `[page-id]`. Fetch it, find the SOP whose workflow matches the email you're drafting, and read that SOP. Don't work from a remembered list of which SOP holds which template — SOPs are added, split, renamed, and re-variant'd constantly, so any such list is stale the moment it's written.

Inside an SOP, email templates sit below a `---` divider, stacked and separated by `---`. Each carries a `Subject:` line with an italic `*(annotation)*` naming the template and when it's sent, a `**Context**:` line above it saying when to use that variant, and the verbatim body in a fenced block. When a step has more than one template they're stacked as Variant A / B / C — match the *variant*, not just the SOP, since variants differ by situation (one proposal vs. several, resources vs. proposal, next call booked vs. not).

**Source priority: SOP first, then sent mail, then from scratch.** When a workflow has an SOP template, that's the source of truth — draft from it. Sent mail is the fallback: use it to fill in the current specifics the SOP leaves open (phrasing, links, structure the template doesn't pin down) and for ad hoc patterns that have no SOP at all, anchoring on the most recent same-variant send. Draft from scratch only when neither exists.

Match the *variant*, not just the recipient: a sent example only helps if it actually contains the block you're drafting. If you're adding a follow-up-questions list and the sent confirmation had none, or proposal bullets and the example was resources-only, go to the SOP for that block rather than reconstructing it from memory — improvising a structured block (numbered questions, proposal bullets) from scratch is how off-looking formatting and padded, invented copy slip in.

When a recent send diverges from the SOP, flag it so `sop-helper` can reconcile them. The SOP is meant to stay the current source of truth, so a divergence is a signal to update the SOP — not a reason to quietly abandon it.

---

## Calendly Links and When to Use Them

Shaw keeps one Calendly event per *kind* of call, and the kind is a judgment this skill owns:

- **Intro call** — corporate / team training inquiries ("my company," "my team," "our organization"), and anything vague that doesn't fit below.
- **1:1 Claude Workshop discovery** — an individual looking for a hands-on Claude session.
- **Check-in / catch-up** — booked-relationship calls: check-ins with existing clients (e.g. a post-workshop check-in agreed at the session but not booked) and catch-ups with select qualified leads ([Person], 8/19/26).
- **Client-specific page** — a retainer client usually has a booking page of its own, made so anyone at the company can grab time without going through the champions; it goes to champions and participants alike, and a client champion is not the busy-exec case: the link, not a list of times, is the default for them too ([Person] / [Company], 10/21/26).
- **Coffee chat** — peer-to-peer (founder-to-founder, fellow consultant, mutual contact, no commercial intent).

The URL itself is never written from memory. Slugs get renamed and retired, and a dead link lands as an invalid page with no error on Shaw's side, so this file doesn't carry them. Take the link from the newest sent email that offered the same kind of call: to the same client or domain first (`from:me to:<domain> calendly.com`), then to anyone. The newest send is the live slug by construction, since Shaw's own sends switch over the moment he changes an event. When no prior send of that kind exists, ask Shaw for the link rather than guessing a slug.

### When to offer Calendly vs. propose specific times

**Default: offer the Calendly link.** It's the lowest-friction path for most people and lets them self-serve.

**Exception: propose specific times in the email when the person who has to act on it is a senior leader, exec, or otherwise very busy person.** They often won't click through to Calendly — clicking a link, reviewing times, and booking is more friction than picking from a list in their inbox. They prefer to operate in email. Examples: CEOs, C-suite execs, well-known investors.

The exception follows whoever is booking, not whoever the call is with. When the exec has handed scheduling to an EA, the EA is the one acting on the email, and an EA works from calendars all day, so the link is the lower-friction path again: send the Calendly link to the EA, and keep the standard escape hatch. ([Person] / [Company], 10/26/26: times drafted for her EA were replaced with the 30-min link.) Specific times are for the exec who is booking themselves.

When proposing specific times manually, see calendar-helper's "Picking times to propose" for which times to pick, and "Proposing time options" under Voice above for how to format them — including "When the next step is a call, propose the time," which governs replies that would otherwise promise to follow up later.

**Phrasing the link.** Introduce it as a question or a soft offer, not an instruction: `Any of these times work?`, `If it's helpful, happy to hop on a call to walk through X`, `If not, here's my full availability` — not `Grab any time that works here:`. The question keeps it an offer the recipient can decline, and it matches the ask that heads the multi-option list, so the same voice carries whether the times are in the email or behind the link. The link rides as anchor text on the phrase that names the call ("a call", "my full availability"), never as a bare URL after the sentence ([Person] and [Person], 10/21/26; [Person], 10/16/26).

**The escape hatch.** A Calendly link closes on Shaw's standard line:

> `If not, let me know, and we can figure something else out :)`

The line answers the ask sitting directly above it, so it refers back with "If not" rather than restating it; "If no time works" repeats "times work" two lines apart. It's the link-based sibling of the multi-option list's closer, and it does the same job — the link shows finite availability, so the line says the availability isn't the constraint. Note the SOPs carry an older variant ("just shoot me an email, and we'll get something scheduled"); the line above is current, and the divergence is worth flagging to `sop-helper`.

**When Shaw dictates a line, use his words.** If his instruction contains the phrasing he wants — even loosely, even mid-sentence — that phrasing wins over any template line from an SOP or a reference file. A template is what to reach for when he *hasn't* specified; reaching for one anyway silently overwrites a decision he already made. Tighten his wording into email voice if it needs it, but keep the words.

His words are the payload, not the whole email. A dictated line is usually the gist of what the email has to carry, said in a hurry; it isn't a claim that the email is one line long. Write the email around it the way he would have: the reaction to what they said, his line, then whatever close the situation needs.

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

**`search_threads` caps a thread at 5 messages, keeping the oldest and dropping the newest.** The cap is hard rather than approximate, and it is silent — a genuine 5-message thread and a truncated 40-message thread are identical in the response. Because it drops from the *new* end, the message most likely missing is the one that decides whether a reply is needed at all: the reschedule, the acceptance, the answer to the question you asked. Verified 8/12/26 across two unrelated threads, one 8 messages and one 6, both of which returned exactly the oldest 5.

So the trigger is behavioral, not observational: **never draft, date, or write a claim about a thread from a search result.** Call `get_thread` first, every time — `MINIMAL` format is enough for the message list, and it's one call. Counting messages in the response is not a workable check, because every thread of five or more looks the same from the outside. (8/12/26: a draft told a client team a meeting time was still open and a session was 60 minutes, both contradicted by messages 6-8 of an 8-message thread.)

The staleness cuts both ways: it hides inbound replies *and* your own sends. A search result showing no message from you today is not evidence you didn't send one, so confirm with `get_thread` before writing "not sent" into a report or a database Note. (8/1/26: a referral FU that went out at 14:22 was reported to Shaw as never sent, off a search result that stopped at the previous message.)

The check is scoped by what you're about to *say about the thread*, not by what workflow you're in. Drafting workflows remember it because the draft depends on the thread; incidental findings skip it — a thread noticed while verifying something else, then flagged as "unanswered" in a closing summary, never gets the re-read. Any claim about a thread's state that reaches Shaw (a flag, a summary line, a "want me to reply?") earns the same `get_thread` check as a draft, because a wrong "unanswered" costs him the same either way. (8/11/26: a reschedule ask spotted while verifying sends was flagged as unanswered off a 5-message search result; the full thread showed Shaw had already replied and rebooked the same day.)

**Exact-subject searches are a tertiary tool.** Use `subject:"..."` filters only when looking for a specific template instance — e.g., "find the most recent 'Tomorrow's 1:1 Session' I've ever sent, to anyone, so I can match its structure." Never use exact-subject filters as the primary way to surface context with a particular person.

### Filing a thread into a label

Filing is two calls, not one: `label_thread` to add the label, then one `unlabel_thread` removing both `INBOX` and `UNREAD`. There is no archive tool — archiving *is* removing the `INBOX` label, and stopping after the first call leaves a labeled thread still sitting in the inbox, which isn't what "file it" means. Clearing `UNREAD` rides in the same call because a filed thread is a handled thread, and a handled thread shouldn't show as new in its label.

**Read the label off the relationship, not off the taxonomy.** The labels are a nested hierarchy (`aba/clients/<client>`, `aba/leads`, `aba/contact form`, `aba/partnerships`, `aba/expert-network`, `aba/events`, `networking/<org>`, `services/<vendor>`), and choosing from the names alone produces plausible-but-wrong picks — a calendar invite from a client contact reads as `aba/events` just as easily as `aba/clients/<client>`. Look instead at what *sibling* threads with that person or org already carry: an org Shaw works with has a filing history, and a new thread joins it rather than starting a new category. `search_threads` returns `labelIds` on every message, so the answer is usually already sitting in the search you ran to find the email. This is the same signal the Chrome fallback below mines from `tr.zA` rows — Shaw's own filing says what a relationship *is* faster than reading any single thread in it.

When no sibling thread exists, that's a genuinely new relationship. Surface the closest existing label and ask rather than inventing one.

**`label_thread` takes label IDs, not display names**, so `list_labels` comes first to resolve the name. Both calls return a bare `{}` on success, which says nothing about what actually changed — confirm with `get_thread` at `METADATA_ONLY`, which returns `labelIds` and little else. Neither `INBOX` nor `UNREAD` should remain.

### The calendar is a channel — check it before drafting anything about timing.

Shaw reschedules by sending an updated invite rather than an email, deliberately: the invite already renders the new date, time, and Meet link, so a second email announcing "moved it to Friday" is inbox noise he'd rather not send. The consequence for drafting is that **the calendar routinely runs ahead of the email thread.** A thread that reads as an unresolved scheduling negotiation may already be settled, with the settlement visible only as an event's changed start time and its attendees' response statuses.

So before drafting any reply that proposes, confirms, or references a time, read the event itself (`list_events` over the relevant window). Acceptances and declines count as answers: an attendee who accepted the moved invite has responded, even though they never wrote back. So has one whose "Accepted:" notification is sitting in the inbox looking like a see-and-file item.

This composes with "The live thread wins" — the live record of a scheduling decision often isn't a thread at all. (8/12/26: a draft re-proposed Friday 2PM PT to a client team when Shaw had already moved the recurring event to exactly that slot the night before, and one attendee had already accepted.)

### Reading threads the Gmail MCP can't see

The connected Gmail MCP is scoped to one inbox and search hits sometimes miss threads filtered into custom labels — most commonly contact-form submissions in `shawhintalebi@gmail.com` that get auto-labeled `stv/Website/contacts` and never land in the main inbox view. If the CRM notes (or any other source) reference an email exchange but `search_threads` comes back empty, fall back to Claude in Chrome:

1. Open Gmail at `https://mail.google.com/mail/u/2/#search/<keyword>` for the non-ABA business account (`shawhintalebi@gmail.com`), or `u/1` for the ABA business account. Pick the account based on where the thread should live (contact form → `u/2`; ABA outbound sales → `u/1`).
2. Read the results list with `javascript_tool` — not `get_page_text`. See below.
3. Click into the thread you want.
4. *Now* `get_page_text` works: an opened thread renders inline, so one call returns the whole body.
5. Treat what you read like normal email context: extract goals, asks, pain points, then move on.

**A results list and an opened thread need different tools.** `get_page_text` targets article-like content — which an opened thread is and a results list isn't. The list is a virtualized grid, so text extraction returns a few lines of chrome (`1–40 of 40`, `Conversations`) and not one actual row. `read_page` does see the rows, but Gmail's label sidebar dominates the accessibility tree and burns ~13k characters before the first result. Pull the rows as structured data instead:

```js
Array.from(document.querySelectorAll('tr.zA')).map(r => ({
  from: r.querySelector('.yW span[email]')?.getAttribute('email') || '',
  name: r.querySelector('.yW span')?.innerText || '',
  subj: r.querySelector('.bog')?.innerText || '',
  snip: (r.querySelector('.y2')?.innerText || '').slice(0, 150),
  date: r.querySelector('.xW span')?.getAttribute('title') || '',
  labels: Array.from(r.querySelectorAll('.av,.at')).map(e => e.innerText).join('|')
}))
```

`tr.zA` is one conversation row. The `labels` field is the quiet win — it surfaces Shaw's own filing (`stv/lead connections`, `stv/networking`, `stv/collabs/*`), which often says what a relationship *is* faster than reading any single thread in it. This also scales: one call returns 40 rows of sender, subject, snippet, date, and labels, which is usually enough to decide what's worth opening at all.

Reach for this only when the MCP comes back empty for a thread that other evidence says exists. The MCP is faster and quieter for everything else.

### Drafting with `create_draft`

The Gmail MCP tool `create_draft` accepts `to`, `subject`, `body` (plain text), `htmlBody` (HTML), and `replyToMessageId`. Use `htmlBody` whenever the message has paragraphs, links, or any structure — Gmail's plain text mode auto-wraps lines at ~78 characters, inserting hard line breaks mid-sentence. In HTML, use `<div>` tags for paragraphs, `<div><br></div>` for blank lines between them, and `<ul><li>` (bullets) or `<ol><li>` (numbered) for lists — a real list tag, never markers you type by hand. Text dashes and typed `1.`/`2.` don't become a list; typed numbers dropped into separate `<div>`s (with `<div><br></div>` between them) render as loose, widely-spaced standalone lines, which is exactly what makes an enumerated ask look off.

**Write raw tags in `htmlBody`, never HTML entities.** The `htmlBody` parameter takes real markup, so the angle brackets go in as literal `<` and `>`. Escaping them (`&lt;div&gt;`) doesn't get decoded anywhere along the way — the entities survive into the message body and the recipient sees the tags as visible text. Nothing in the API response flags this: `create_draft` returns a normal success either way, and `list_drafts` doesn't return the body, so there's no way to verify the render through the connector. That makes it a silent failure Shaw catches by opening the draft. The habit that prevents it is to write markup the way you'd write it in an HTML file and never reach for an entity for a structural tag (7/31/26: a draft to a new contact went out with `&lt;div&gt;` throughout and had to be recreated, leaving a duplicate for Shaw to trash by hand).

**Never set a font, size, or color on the `htmlBody`.** Don't wrap it in a `<div style="font-family:…;font-size:…;color:…">` or put inline `style` font rules on any element. Those overrides force the message into a non-default font (e.g. Arial) that renders visibly different from Shaw's normal sends, and he'll flag it on sight. Use only structural tags — `<div>`, `<br>`, `<ul>`/`<li>`, `<b>`, `<a href>` — and let Gmail apply the inbox's own default font. The email should *look plain even though it's sent as HTML* (see Voice → Tone markers); a font/style wrapper is exactly the visible formatting that rule forbids.

**Links.** Every URL sent through the Gmail connector comes back rewritten as `https://www.google.com/url?q=…&source=gmail&ust=…&sa=E` — applied server-side at message creation, identically for bare text, `<a href>` with the URL as anchor text, `<a href>` with different anchor text, and every domain including Google's own, in the stored draft and the delivered message alike (verified 9/20/26). There is no known fix from inside the connector: don't restructure a draft to dodge it, and don't tell Shaw one exists. The links resolve correctly, so the cost is cosmetic. Whether the recipient sees a URL or anchor text is therefore a presentation choice:
- **Anchor text** when a word carries the meaning better than the URL (e.g., "Claude desktop app", "intake form", "a call", "my full availability").
- **The full URL** when Shaw's pattern for that send shows it in full (a Google Form). Keep it inside `htmlBody` either way — a plain-text-only body is the one case that makes the wrapper worse, since with no HTML part the redirect URL becomes the visible text.
- **Inline the link, don't pedestal it.** In a short informational share, fold the link into the sentence with plain anchor text ("in this article", "this doc") rather than setting the doc title on its own line — and merge what the link covers into that same sentence instead of a separate trailing "here's what's in it" line. One inline-linked sentence carries the whole share; a titled link line plus a description line reads as two ideas where Shaw sends one. (Composes with "Shaw never pads for length.")
- **Sharing one of Shaw's skills** — link the skill's file in the aba-plugins GitHub dist (`https://github.com/ShawhinT/aba-plugins/blob/main/dist/<skill-name>.skill`), not a Drive folder. The repo is the canonical, always-current copy; a Drive pointer goes stale and makes the recipient hunt. The exception is a client-specific skill shipped inside the client's shared Drive folder: there the Drive folder *is* the canonical copy, so link the skill's folder (based on a real send: [client-skill] / [Company], 10/6/26).

**Attachments.** `create_draft` takes attachments as base64 inside the tool call, which is impractical for
anything past a small file (a 108 KB PDF is ~144 KB of encoded text). For a local file of real size, write the
body as if it's attached and tell Shaw, in the summary, which file to drag in before sending. The limit here is
cost, not a tested connector cap (10/24/26).

**Threading.** To attach the draft to an existing thread (most follow-ups, all CRM nudges), pass `replyToMessageId` set to the most recent message ID in that thread — find it via `get_thread`. Omit `replyToMessageId` to start a fresh thread. The reply subject should be the original subject prefixed with `Re:` (e.g., `Re: [Person] / Shaw - Check-in`). Pick the thread per "The live thread wins" above — don't reply on a stale template-named thread when the actual conversation has moved elsewhere. Meeting follow-ups are the exception and open a fresh thread — see `references/call-follow-ups.md` → "Threading and batch" for the rule and the subject lines.

**Verify drafts with `list_drafts` after creating.** `create_draft` returns `{id, messageId, threadId}`, and the `id` has matched the draft's real ID in recent use (verified across 6 drafts, 8/21/26) — `messageId` is the handle `trash_message` needs for cleanup. What the response can't prove is persistence: a returned ID looks the same whether or not the draft actually saved, and silent failures have happened (7/28/26: two of three drafts silently failed, and every draft link in the summary was dead). So after drafting, call `list_drafts`, match on recipient, and confirm the draft exists before reporting it or linking `#drafts/<id>`.

**A threaded draft is effectively immutable — recreate rather than update.** `update_draft` has no `replyToMessageId` parameter, so editing a reply strips its threading: the draft detaches into a brand-new thread and the original stays behind as a duplicate. Nothing in the response signals this. When a threaded draft needs different wording, create a fresh one with `replyToMessageId`, then trash the stale copy yourself with `trash_message` on its messageId from `list_drafts` (verified working on drafts, 8/21/26). `update_draft` is safe only on drafts that were never threaded to begin with.

Before trashing any draft, check whose it is. `list_drafts` returns everything in the account,
including drafts Shaw is composing himself, and one he's mid-edit on looks identical in metadata
to a stale copy of yours. The tells are the body and the timestamp: text that diverges from what
you wrote, or a `date` newer than your own `create_draft` call, means it's his working copy.
Leave it and say so — the stakes are higher now that cleanup is a direct `trash_message` call. (8/1/26: a half-written
reply of Shaw's, ending mid-sentence on "However,", was nearly listed as cleanup.)

**List spacing.** When a `<ul>` follows a line of text, attach it directly — no `<div><br></div>` between the text and the opening `<ul>`, and none between the closing `</ul>` and the next line. HTML `<ul>` already renders with its own top/bottom margin; adding blank-line divs doubles the gap. This is also why a short list of questions or asks goes inside one `<ul>`/`<ol>` with its `<li>`s back-to-back — not hand-numbered `<div>`s separated by `<div><br></div>`, which is the loose, spaced-out look that reads as off.

**Line spacing mirrors the source.** Lines that sit on consecutive lines in the source template, with no blank line between them, stay in back-to-back `<div>`s. A two-line couplet like `If it rings true, just reply "yes, go ahead".` / `If not, happy to tweak :)` is one unit, not two paragraphs. Reserve `<div><br></div>` for where the template actually has a blank line; inserting one between paired lines visually loads the email and Shaw flags it. A blank line next to a list is the exception. Plain-text templates put one above and below a bulleted list because that's the only way plain text can separate a list from surrounding prose. HTML doesn't need it: `<ul>` carries its own top and bottom margin, so reproducing the template's blank line stacks two gaps. When the neighboring block is a list, the List spacing rule wins and the blank line doesn't transfer.

**Inline quotes (testimonials, pull-quotes).** Render the quote as `<i>...</i>`, with the attribution on the next line via a single `<br>`, also italic. Don't use `<blockquote>`: Gmail renders it inconsistently (stray indent bar, broken spacing) and Shaw flags it on sight. The connector can't produce the clean gray-bar blockquote, so he adds that by hand if he wants it. (The reviews-referrals skill's polish-framework points here for the testimonial case.)

**Plain text `*word*` means bold, not italic.** When reading sent emails via the Gmail API, the plain text body renders bold text as `*word*`. When reproducing this formatting in HTML drafts, use `<b>` tags, not `<i>`.

### Gmail emoji reactions break thread replies

When Shaw reacts to an email with an emoji, Gmail creates a new message in the thread. Replying after a reaction (via `replyToMessageId`) breaks the rendering. When the last message in a thread is a reaction, create a fresh thread with a descriptive subject line instead of replying to the existing one. This rule overrides "the live thread wins" — if the live thread ends in a reaction, fall back to a fresh thread.

Note this is a *rendering* problem, not a visibility one. A reaction doesn't hide anything from `get_thread`, and it isn't why messages go missing from a search result — that's the 5-message cap above. Diagnosing a missing message as "the emoji broke the thread" points at the wrong fix.

### Calendly notification threads

Discovery-call confirmations reply *inside* the Calendly notification thread so the booking context carries. The gotcha: set `to:` to the **invitee's email pulled from the notification body**, never `notifications@calendly.com` — that address is a no-reply relay and the lead never sees the message. Exception: if the lead came in through the contact form or a sales thread, reply there instead so the relationship context carries.

### Squarespace contact-form threads

The `shawhintalebi.com` contact form forwards to `u/2` from `[email]`, with the actual sender's name and email in the body. Gmail's Reply button parses that real email out of the body and pre-fills it as the recipient — so click Reply on the thread to keep everything threaded under `Form Submission - Contact Page`. Composing a new email instead loses the thread and breaks future CRM cross-referencing.

**Reply mechanics.** Reply in the u/2 thread (via Chrome — click Reply on the Squarespace message) and **CC `shaw@aibuilder.academy`**. This keeps the thread clean in the `shawhintalebi` (non-ABA) inbox while ensuring the ABA business inbox has a copy. Do NOT create a standalone draft in the business inbox — that loses the thread and the CC link.

**The ABA cc is scoped to contact-form business, not to the u/2 inbox.** It exists so an inquiry ABA will actually work belongs to ABA's records. A reply whose whole job is to route the inquiry *away* — a brand-deal hand-off to [Contact] (`references/brand-deal-declines.md`) — produces nothing for ABA to file, and the extra cc puts a second Shaw address on a thread he's exiting. On those, [Contact] is the only cc. Ask what the reply does with the inquiry, not which inbox it's sitting in.

**Calendly link selection.** See "Calendly Links and When to Use Them" above for which kind of call fits and where the link comes from.

---

## Batch Outreach Workflow

When drafting the same template for multiple recipients, create one draft first and let Shaw review and edit it. Analyze the diff (subject line, formatting, link placement, etc.) and apply those changes to the remaining drafts. This avoids multiplying mistakes across a batch.
