# Per-Prospect Scripting & Channel Formats

Downstream of tracker setup: turning the base script + personalization menu into a ready-to-send message on **every** row, then drafting the sends.

## The per-prospect loop

For each row: read its page-body **Context** → pick the single best-fit `{Personalization}` menu option **verbatim** → write the finished script into the row's page body as a `plain text` code block → add a one-line italic note.

**Pick the opener from the live thread, not just Context.** Context is a snapshot from when the row was sourced; the DM or text thread is the current state of the relationship — a recent call, an unanswered ask in either direction, a ghost, a role change. Read it before choosing an option (LinkedIn via the Chrome sweep under Browser policy, texts via `text-helper`). The thread also surfaces rows that should wait, such as one where Shaw's last message is an open, sensitive ask.

**The note is a closed set, not a summary.** It may contain three things: which script and slot the copy came from, what was swapped and for what, and a live pre-send warning. Nothing else. "Recording the option **and why**" is the same unbounded-slot bug this file warns about two sections down — "why" has no wrong answer, so it drifts from one clause on row 1 to a sourcing audit on row 40 (a real one ran 150 words: where a stat came from, which seat it mirrored, how the sent version differed from the draft). The rationale is worth *thinking*; it isn't worth writing on the row. It goes in chat, where Shaw can act on it while it's live.

```
*Scripts 2 M2, [Company]/QBR win — he owns sales as well as ops.*
```

Never in the note: an instruction back to Shaw ("revert if you'd rather", "Shaw's call"), a re-litigation of a campaign-page decision, or a ranking of this prospect against others.

Shaw fills in the specifics (the literal "X", any tweaks) himself. **Pick the option; don't rewrite it** — rewording an opener he's about to edit is wasted work and he'll correct it.

**Re-check `disqualified.md` at the top of the loop, not only before enrichment.** A row that's already sourced, enriched and tracked still gets read once more against the anti-ICP before you write copy for it — cutting at draft time costs one skipped row; cutting at send time costs a judgment call per message with the drafting work already spent.

**The exception is a line the row's own data falsifies.** A script's audience qualifier ("for ops leaders at midsized B2B SaaS companies") is a claim about the recipient, so wherever a segment is broader than its qualifier the template contradicts some rows outright — and a prospect who reads that he isn't the person being described is a harder no than one who was never written to. Adapt that clause to what Context actually says, record the swap in the italic note, raise the mismatch with Shaw directly, and fix it on the campaign page: a qualifier narrower than its segment's filter is a page-level bug, and patching it row by row hides it. This covers claims the data falsifies and nothing else — copy you'd merely word differently still goes out verbatim.

**A variable slot specified as a preference will drift across a batch.** "Prefer the short form", "follow their function", "keep it natural" — each reads fine on one row and produces something different on the fortieth, because a preference has no wrong answer to check against. Specify each slot instead as either a **transformation** (the shape the output takes — `<function> <rank>s`, never an "of" construction) or a **closed set** (the three or four values allowed, plus an instruction not to invent a fifth). Both are checkable per row; a preference isn't. A slot still phrased as a preference is a page-level bug of the same kind as a too-narrow qualifier — fix the campaign page and draft from the fixed version, rather than exercising your own taste forty times and handing Shaw forty edits.

**Write the row even when its script is identical to its neighbours'.** The row body is where Shaw sends from, so a script delivered only in chat isn't delivered. Personalization is what varies between rows; the write is not optional when it doesn't.

## The campaign page is the script; row bodies are copies

Row bodies hold a *copy* of the campaign page's script, written once and often drafted from days later. Copies drift: a subject line gets edited on the page and the rows keep the old one, or a new row gets written from a neighbouring row instead of from the page. **Diff the row against the campaign page's script for its segment before drafting from it.** The page wins.

The corollary matters more than the rule: **when one row disagrees with the rest of the batch, the outlier may be the correct one.** Resolve the disagreement against the page, not by normalizing to the majority — a stale line copied into thirty rows still loses to the one row that matches the source. Treat any within-batch inconsistency as a reason to re-read the page, not as noise to smooth over.

## Thread state → opener

The menu lives on the campaign page, inside the script's code block, as a numbered list under `{Personalization}` — one option per line, so each row can record `option N`. A script whose personalization slot is empty or unnumbered is the page-level bug described above: propose the menu before drafting rows.

Which option fits is decided by the most recent real exchange in the thread. Segment only supplies the default when the thread is silent.

| Thread shows | Opener |
|---|---|
| Shaw owes them (an unanswered offer, a call he agreed to and never booked) | Name it and make the invite the make-good: "I completely dropped the ball on X. But this might be a good way to make up for it." |
| They went quiet on Shaw (ghosted asks or invites) | "Wanted to keep you in the loop." — no warmth the thread doesn't support |
| A fresh change they'd expect him to notice (new role, venture, move) | "Congrats on …!" or the specific detail. A stale announcement he never answered doesn't qualify — use "been a while" |
| Saw them recently (event, call) | "Great catching up at X!" |
| Real past exchange, gone stale, no loose ends | "It's been a while, hope things are going well!" |
| Never messaged | No opener line; add a clause to the ask ("…and thought of you") |
| Live thread with an agreed next step | Fold it into the ask ("Would be a good opportunity to catch up") and drop the greeting and sign-off |

A specific detail Shaw would actually say beats the generic option — specificity is the point of the slot. When the thread is empty, segment sets the default: ABB alum → "been a while"; met in person → "great catching up"; never met → no opener.

## Drafting follow-up & salvage templates

The campaign page holds the final script copy; this is how to draft the follow-up and salvage templates from scratch so they start right.

- **Follow-up nudges inherit the Ask's personalization.** Draft FU1/FU2 to open inline — `Hey {Name}, just wanted to follow up.` — not a standalone `Hey {Name},` line, and with no sign-off, since they land in an existing thread. Only the name varies per person.
- **FU copy is segment- and following-agnostic.** One FU body serves the whole list; `Has Following?` only changes the post-registration ask (repost vs. who-else-do-you-know), so don't spin per-person FU variants — personalize the name, nothing else.
- **Give the "replied-but-cold" case its own template.** Someone who replied then went quiet without registering is neither a fresh non-responder nor a hard "no." Draft a name-opener salvage — a pass-along + open-door note. Reserve an "Of course!"-style opener for a direct reply to a "thanks"; use the name opener when re-initiating after silence.

## One campaign, multiple channels — the `Medium` column

Contacts split into **Email / LinkedIn DM / Text**, tracked in the tracker's `Medium` column. The channel changes the script format:

- **LinkedIn DM / Text:** plain-text code block, **raw visible link** (you can't hyperlink text in LinkedIn).
- **Email:** needs three extra things — (1) an **email address in Context**, (2) a `**Subject:**` line at the top of the block, (3) a **hyperlinked CTA** `[→ Secure your spot](url)` instead of the raw link. Keep it in the `plain text` code block anyway (Shaw copy-pastes it); the markdown link is the source of truth, and the real hyperlink gets built in the Gmail draft.

Converting a DM row to an email row = add the email to Context, add the subject line, swap the raw link for the markdown-link CTA, set `Medium = Email`.

## Subject-line register matches the send type

- **Personal 1:1 email** (warm alum/contact): plain, personal — "You're invited". NOT a benefit headline.
- **Broadcast / newsletter promo**: the benefit headline — "Get 20 hours back" — belongs here, on the mass send (e.g. the campaign's newsletter/ABN event-promo pages), not the 1:1s.

Defer the actual craft to conversion-copy; the reusable point is that **register differs by send type** — don't reuse a newsletter subject on a 1:1.

## Email-address sourcing waterfall

Context usually only carries emails for alumni. Source the rest cheapest-first:

1. **Kit** — alumni, via cohort tags (ABB1–8): `list_tags` → `list_subscribers_for_tag`, match by first name within the cohort. Delegate to a subagent to keep context clean.
2. **Gmail search** — recipient pair (`to:`/`from:` the name, or the company/domain); also confirms the address is current and surfaces any prior thread.
3. **🧊 Archived Leads DB** (sub-page of the CRM) — where lost/aged leads live; Shaw will point you here.
4. **Active Leads** — current pipeline.
5. **Ask Shaw.**

Watch for **stale addresses** — an archived-lead email can predate the person's current company. Flag it, don't silently use it.

## Gmail draft mechanics (defer to email-helper, but it bites)

- Build the body with `<div>` for lines and `<div><br></div>` for blank lines. **Never `<p>`** — its default top/bottom margins insert unwanted blank lines before the greeting and inside the signature, and Shaw flags it on sight. The sign-off ("Cheers," / "Shaw") is two back-to-back `<div>`s.
- CTA as a hyperlink: `<a href="url">→ Secure your spot</a>` (anchor text, URL hidden). Preserve the campaign's UTM (`?utm_source=dm`, etc.); Shaw says per channel whether to change it.
- **Draft, never send.** Prepare drafts; Shaw sends and reports back. `create_draft` can't edit an existing draft, so **draft one, get Shaw's edit, diff it, then apply the diff to the whole batch** — one review before the batch, not after.
- **When drafting is split across parallel agents, have each agent fetch the script from the campaign page itself** rather than pasting the copy into their prompts. Pasting feels safer and is the opposite: it converts one unverified assumption into N identical errors and removes the only thing fan-out gives you free — independent reads that disagree when something's wrong. A prompt-literal guarantees nothing in the batch will ever contradict you.
- **Once a batch is handed off, Shaw may start sending at any moment.** Drafts are shared mutable state, not your workspace. Batch-wide edits after handoff race his sends: some drafts will already be gone, and any that ship mid-edit go out in the pre-edit form. Re-read the mailbox immediately before dispatching edit work and expect the set to have shrunk. For a small fix, amend the campaign page and tell him rather than mutating drafts under him — a one-character change is rarely worth the race.
- **A draft that has vanished was almost certainly sent, not deleted.** Check sent mail before reporting loss or re-creating it.

## Logging the sends

Once Shaw confirms a batch went out, log per SKILL.md's "Logging a batch send."
