# Per-Prospect Scripting & Channel Formats

Downstream of tracker setup (Phase 6): turning the base script + personalization menu into a ready-to-send message on **every** row, then drafting the sends. Learned in depth on the July 2026 ABA event-promo campaign.

## The per-prospect loop

For each row: read its page-body **Context** → pick the single best-fit `{Personalization}` menu option **verbatim** → write the finished script into the row's page body as a `plain text` code block → add a one-line italic note recording the option + why.

Shaw fills in the specifics (the literal "X", any tweaks) himself. **Pick the option; don't rewrite it** — rewording an opener he's about to edit is wasted work and he'll correct it.

## Segment → default opener

| Segment | Default opener |
|---|---|
| 1 — ABB alum | "It's been a while, hope things are going well!" |
| 2 — met in person | "Great catching up at X!" |
| 3 — met virtually | judgment (see below) |
| 4 — never met | "This seemed relevant to you so I thought I'd share." |

- **Seg 3 is a judgment call** on the actual thread: recent call → "great catching up"; warm but aged → "it's been a while"; one-sided or ignored pitch → "seemed relevant".
- **A recent role change overrides the segment** → "Congrats on the new role/venture!" is the strongest wedge, valid even for never-met, and it cleanly resets a prior ghost.
- Mid-campaign **re-segmentation** happens (Shaw moves people 3→4). Re-default the opener to option 4, but keep strong specific hooks (role-change congrats) regardless of segment, and flag anyone with genuine prior contact so Shaw can keep the warm opener if he wants.

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

## Logging the sends

Once Shaw confirms a batch went out, log per the SKILL.md "Logging a batch send" rules: `Last Contact` = send date, `Notes` = `Ask sent (M/D).` (append replies), `Next Contact` = the FU1 date from the campaign's Promo Calendar, uniform across the batch. Expect Notion 429s on bulk updates; batch ~9–11 per message.
