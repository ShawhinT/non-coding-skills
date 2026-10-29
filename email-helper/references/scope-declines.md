# Scope Declines

Replies to someone who wants real help that Shaw doesn't sell — 1:1 coaching, tutoring, mentorship, ad hoc technical guidance on a personal project. The ask is legitimate and often well-researched; it just isn't the business. The job of the email is to close the loop warmly and leave the person better off than a "no thanks" would.

Read this file before drafting any reply that declines an out-of-scope ask.

---

## When to Use

Fires when all of these hold:

- The person is **not a client** and has no active engagement
- What they want is **outside the offer** — individual coaching, tutoring, career advice, a one-off technical consult on their own project
- There is **no team, budget, or company** behind the ask

The last one is usually what settles it, and it often only surfaces on the second email. [Person]'s first message looked like a lead: a real technical problem, an explicit request for rates and engagement structure. His second message closed the door on its own — *"This is a personal project, just for me, no team or other people involved."* Wait for that signal before declining; a solo founder asking about rates is a lead, not a scope decline.

### Not this file

**A serious buyer raising friction** → conversion-copy's `channel-emails.md`. The tell is buying intent *plus* an objection: a pricing pushback, a discount ask, a scope negotiation. That person is in the pipeline and the email's job is to advance the deal.

The two look similar on the surface because both involve someone questioning fit. The difference is direction: a buyer with an objection wants to find a way *in*, and this person wants something Shaw doesn't sell at any price. Route on pipeline state, not on wording.

---

## The Shape

Four moves, in order. Usually 5 short paragraphs total.

1. **Standard opener.** `Thanks for your reply!` (or `Thanks for reaching out!` on a first contact). Don't get creative here.
2. **Name who you serve, and let the no fall out of it.** Not "I don't do that" but "I'm focused on X, so Y isn't the best fit." The decline reads as a consequence of a real focus rather than a rejection of them, and it's true, which is why it works.
3. **Redirect to something concrete.** See "Picking the Redirect" below. This is the CTA — it's what keeps the email from being a dead end.
4. **Conditional door-open.** `If this ever grows beyond a personal project, feel free to reach back out :)` — ties the door-open to the specific condition that would make them a fit, so it's an honest invitation rather than a pleasantry.

Then `Cheers, Shaw`.

### What to avoid

The generic rejection register: an `Unfortunately` up front, a `but` pivot, an apology for not helping. That's the internet's default and it lands harsher, because it makes the no the main event. (Same principle as "Lead with the forward motion when delivering a no" in SKILL.md.)

Also skip hedging the focus statement. "I may not be the best fit" is fine; "I'm probably not the right person, though I'd love to help if I could" reopens a door you just closed and invites a negotiation.

### Precedents

| Date | Person | Ask | The line |
|---|---|---|---|
| Apr 2026 | [Person] | Tutoring until he finds a job | *"I'm focused on training Founder-CEOs and SMB teams, so I may not be the best fit as a tutor. What types of roles are you looking for? Maybe I can recommend some alternative resources."* |
| May 2026 | [Person] | Independent AI project help, post-grad | *"I've refocused to helping businesses with AI transformation, so the content is more..."* |
| Jul 2026 | [Person] | Technical guidance on a personal trading system | *"I'm focused on helping companies roll out AI across their teams, so 1:1 technical guidance on a single use case isn't the best fit for how I work."* |

Note the Apr 2026 reply got a *question* instead of an immediate resource ("What types of roles are you looking for?") because his ask was too vague to redirect on. Asking one clarifying question is a valid substitute for the redirect when you genuinely can't tell what would help — Shaw sent the actual playlist a week later once he knew.

---

## Picking the Redirect

**Match the specificity of the redirect to the effort they put in.** This is the rule that separates a useful decline from a brush-off:

- Two lines of context → one playlist or the channel generally
- A detailed problem description → 2-3 named videos with links

[Person] sent a 280-line architecture document. A reply saying "check out my YouTube channel" would have read as a brush-off of work he clearly spent hours on. Three named videos, each mapped to a specific failure in his system, made the decline land as help.

**Diagnose the problem behind the stated question.** When they've shared enough detail, the highest-value thing in the reply is often not an answer to what they asked. [Person]'s headline question was a storage-design question ("should per-ticker context live in a column on the parent row?"). His actual problem, visible three sections down, was that his deduplication layer was unreliable and he had no way to measure whether any fix helped. So the redirect led with evals — the thing he didn't ask for and needed most.

This costs one careful read of their attachment. It's the difference between a reply they skim and one they act on.

**Never invent a video title or URL.** A plausible-sounding title that 404s is worse than a generic channel link. Verify every link with the procedure below before it goes in a draft.

---

## Finding the Right Videos

Shaw's catalog is 90+ videos and there's no clean machine-readable index of it. Most obvious approaches are dead ends, so go straight to the one that works.

### What works

YouTube's **channel-scoped search**, driven through Chrome, one topic at a time:

```
https://www.youtube.com/@ShawhinTalebi/search?query=<term>
```

Navigate there, then scrape the results:

```js
await new Promise(r => setTimeout(r, 3000));
for (let i = 0; i < 6; i++) {
  window.scrollTo(0, document.body.scrollHeight);
  await new Promise(r => setTimeout(r, 500));
}
const out = [], seen = new Set();
document.querySelectorAll('a[href*="/watch?v="]').forEach(a => {
  const h = a.getAttribute('href') || '';
  const id = (h.split('v=')[1] || '').split('&')[0];
  if (!id || seen.has(id)) return;
  let t = (a.getAttribute('title') || '').trim();
  if (!t) {
    const card = a.closest('ytd-video-renderer, yt-lockup-view-model');
    if (card) {
      const el = card.querySelector('#video-title, a[title], h3 span');
      t = (el && (el.getAttribute && el.getAttribute('title') || el.textContent) || '').trim();
    }
  }
  if (t && t.length > 6 && !/^\d+:\d+$/.test(t)) {
    seen.add(id);
    out.push(t + ' || https://youtu.be/' + id);
  }
});
out.join('\n');
```

Run it once per topic — 4-6 searches covers most diagnoses. Useful query terms: `context`, `agents`, `memory`, `evaluate`, `RAG`, `embeddings`, `prompt`, `fine-tuning`.

To confirm what a video actually covers before recommending it, open the watch page and read the description:

```js
const d = document.querySelector('#description-inline-expander') || document.querySelector('meta[name="description"]');
String(d.innerText || d.getAttribute('content') || '').slice(0, 1600);
```

### What doesn't work (don't retry these)

- **The channel RSS feed** (`youtube.com/feeds/videos.xml?channel_id=...`) — blocked by robots.txt via WebFetch.
- **WebFetch on the channel page** — returns Shaw's bio and channel metadata, no video titles.
- **The `/videos` grid** — virtualizes aggressively and only ever renders about 3 cards regardless of scrolling; a long scroll loop times out the CDP call.
- **curl or any script-based fetch** — out of bounds under the web content restrictions, regardless of what WebFetch returned.

Skipping straight to channel search saves roughly 8 tool calls of dead ends.

### Don't cache a topic-to-video index here

Tempting, but Shaw publishes often enough that a hardcoded list goes stale, and a stale link is worse than a live search — it produces confident, wrong recommendations. Keep the method, not the answers.

---

## Draft Mechanics

Nothing unusual, but two things specific to this pattern:

- **A list of 2-3 videos goes in a real `<ul>`**, with each title as the anchor text of an `<a href>` rather than a bare URL. Titles carry the meaning; raw YouTube URLs are noise. Attach the `<ul>` directly to the line introducing it with no `<div><br></div>` between them.
- **Reply on the existing thread** with `replyToMessageId`, since these are almost always a reply to an inbound ask rather than a fresh send.

---

## Example

**Context:** [Person] reached out via the ABA contact form about a real-time SEC filing analysis system, attached a detailed architecture doc, and clarified in a follow-up that it's a solo personal project with no team.

> Hi [First Name],
>
> Thanks for your reply!
>
> I'm focused on helping companies roll out AI across their teams, so 1:1 technical guidance on a single use case isn't the best fit for how I work.
>
> That said, these 3 videos should help with what you described:
>
> - [Context Engineering Explained (5 Practical Tips)](https://youtu.be/zKHSpwayPBU)
> - [How to Evaluate (and Improve) Your LLM Apps](https://youtu.be/-sL7QzDFW-4)
> - [Text Embeddings, Classification, and Semantic Search](https://youtu.be/sNa_uiqSlJo)
>
> If this ever grows beyond a personal project, feel free to reach back out :)
>
> Cheers,
> Shaw
