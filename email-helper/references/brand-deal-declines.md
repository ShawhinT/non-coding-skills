# Brand Deal Declines (Hand-off to [Contact] at [Company])

Replies to inbound brand deals, sponsorships, affiliate offers, and creator-partnership pitches — the ones that come in because of Shaw's audience rather than his consulting. Shaw doesn't do brand deals. His friend [Contact] runs [Company], a creator agency, so the standing move is to decline and cc [Contact] in the same email rather than send a dead-end no.

Read this file before drafting any reply to a partnership or sponsorship pitch.

---

## When to Use

An inbound (usually via the ABA contact form, sometimes a cold email or DM) where the sender wants to **buy access to Shaw's audience**: a sponsored video, a branded landing page, an affiliate or revenue-share deal, a "partnership" with a tool company, a newsletter placement, a product seeding.

The tell is what they're paying for. If they want Shaw's audience, it's this file. If they want Shaw's expertise for their own team, it's a normal lead. If it's an individual wanting coaching or help on a personal project, it's `scope-declines.md`.

**The second tell is who's asking.** The hand-off assumes there's a brand on the other end that [Contact] can actually transact with. When the inquiry comes from the company itself, a reply gives [Contact] a qualified inquirer whose own pitch is sitting right there in the quoted thread. When it comes from an agency or media buyer shopping rate cards for an unnamed "upcoming campaign," there's no brand behind it yet, so the intro hands [Contact] a middleman instead of a client. Those get no reply at all — classify as junk in triage, don't draft.

The tell is usually in the ask: a brand names itself and what it's launching; an intermediary asks for your rate card and media kit before naming anyone. *([Person], [Company], 7/28: "your audience would be a great fit for one of our upcoming campaigns," followed by a request for dedicated/integrated video rates and a media kit. No brand named — no reply.)*

**The third tell is the sender's address.** A real brand writes from its own domain. A launch or partnership pitch sent from a free personal address (gmail.com, outlook.com) fails the legitimacy gate even when it name-drops a real company and real employees — there's no verified brand contact for [Contact] to transact with. No reply, no [Contact] intro: classify as junk; Shaw blocks the sender. *([Company], 8/20/26: launch-marketing pitch from a personal gmail address — junked despite naming a real company.)*

Event sponsorships Shaw is *running* (like the [Partner] x ABA series) are the reverse direction and don't belong here.

---

## [Contact] / [Company]

- **[Contact]** — founder of [Company], `[email]`, site `[agency-url]`
- A platform with over 20,000 technical content creators to choose from
- Clients include [Client A], [Client B], [Client C], and [Client D]
- Also the person to talk to about a brand's AI visibility

Keep the client list current-ish but don't stress it; the names are there to establish that [Company] is real and operating at the inquirer's level.

---

## The Shape

Five short paragraphs. It's a decline and a three-way intro fused into one email.

1. **Greeting + standard opener.** `Hey [First Name],` then `Thanks for reaching out!`
2. **The no, with [Contact] as the resolution.** One sentence, `While` clause first, landing on the hand-off: `While I'm not taking on new partnerships right now, I wanted to connect you with [Contact] (cc'd), who might be a great option.` The no is never its own sentence — it's the subordinate half of the sentence that introduces [Contact]. (Same principle as "Lead with the forward motion when delivering a no" in SKILL.md.)
3. **[Contact]'s blurb.** Who he is, the scale of [Company], a few named clients. Add the AI-visibility line when the inquirer is a brand trying to get in front of technical audiences.
4. **`Hope you two get a chance to connect :)`** — verbatim, same closer as `three-way-intros.md`.
5. **`Cheers, Shaw`**

Note what's *absent*: no counter-offer, no "here's what I do instead," no pitch for training. Redirecting the inquiry is the whole job. Adding an ABA pitch turns a clean hand-off into a bait-and-switch.

---

## How This Differs From `three-way-intros.md`

Same closer, different mechanics — don't mix them up:

| | Three-way intro | Brand deal hand-off |
|---|---|---|
| Greeting | `Hey folks,` | `Hey [First Name],` |
| Recipients | both parties in `to:` | inquirer in `to:`, [Contact] in `cc:` |
| Thread | fresh send, subject `A <> B` | reply on the inbound thread |
| Direction | introduces each to the other | introduces [Contact] only |

[Contact] doesn't need an introduction to the inquirer because the quoted inbound is right there under the reply — he reads their own pitch in their own words, which beats any blurb. That's also why this stays a reply instead of becoming a fresh thread.

---

## Draft Mechanics

**The reply path follows the inbox the pitch landed in.** The Gmail MCP is scoped to `u/1` (`shaw@aibuilder.academy`) and can't see `u/2` at all, so the connector is only an option for pitches that arrived at the ABA address. Check the receiving inbox before reaching for a tool.

- **Landed in `u/1`** (`shaw@aibuilder.academy`) — draft with `create_draft`, passing `replyToMessageId` for the most recent message in the thread. Subject is the original prefixed with `Re:` (e.g. `Re: ABA Contact Form: [Name]`).
- **Landed in `u/2`** (`shawhintalebi@gmail.com`) — the connector can't reach it, so reply inline via Claude in Chrome: open the thread at `https://mail.google.com/mail/u/2/#inbox/<id>`, click Reply, add [Contact] to Cc, type the body. There is no draft to hand back for review, so the body is worth confirming with Shaw before it's typed.

Common to both:

- **`to:`** the inquirer's real address — for contact-form submissions that address is in the *body* of the notification, not the `From:` header.
- **`cc:`** `[email]` — and only [Contact]. No cc to `shaw@aibuilder.academy`, even on a `u/2` reply (see SKILL.md → Squarespace contact-form threads).
- Plain `<div>`/`<br>` structure, `[agency-url]` as plain text (Gmail linkifies it). In Chrome the body is typed directly, so structure it with real blank lines between paragraphs.
- **File the thread under `networking/[company]`** once the reply is out, not under the label the pitch landed in (`aba/contact form`, `aba/leads`). The hand-off changes what the thread *is*: it stops being an inquiry to ABA and becomes a referral Shaw made to [Company], so it belongs with [Contact]'s other threads. SKILL.md's sibling-label rule would otherwise pull it toward the inbox it arrived through, which is the wrong relationship.

---

## Example

**Context:** [Person] (Partnerships at [Company]) came in through the ABA contact form pitching a branded skills-library page and revenue share.

> Hey [First Name],
>
> Thanks for reaching out!
>
> While I'm not taking on new partnerships right now, I wanted to connect you with [Contact] (cc'd), who might be a great option.
>
> [Contact] is the founder of [Company] ([agency-url]), a platform with over 20,000 technical content creators to choose from, working with clients like [Client A], [Client B], [Client C], [Client D] and many more. If you are trying to figure out your brand's AI visibility, he is also the guy to speak with.
>
> Hope you two get a chance to connect :)
>
> Cheers,
> Shaw
