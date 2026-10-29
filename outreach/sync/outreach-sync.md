# Outreach Sync

Running a *sync* on a live campaign: check for new replies and registrations across every channel, then move each contact one step forward. Triggered by "sync the outreach", "check for replies", "who registered", "did anyone respond", "move the outreach forward".

The core idea: **the tracker defines the campaign — read it before you sync.** Don't hardcode a funnel. Four signals in the tracker tell you how *this* campaign works:

- **Status options** = the funnel / state machine. Their order is the path a contact travels (an event promo might be `Replied → Registered → Share Ask Sent → Shared → Added to CRM`; a research-call campaign might be `Replied → Call Booked → Completed`). You advance contacts along *these* statuses, whatever they are.
- **Medium options** = which reply channels are in play. `Email` → sweep Gmail; `LinkedIn` → sweep the DM inbox; `Text` → you can't read texts, so ask Shaw what came in.
- **The page's scripts / "DM Logic"** = the decision tree and the exact copy for each move. Use them verbatim (pick the personalization + variation to fit; adapt only channel wrapping like an email greeting/sign-off). Don't write custom copy — Shaw will redirect you to the page scripts if you do.
- **The campaign goal/context** (top of the page) = the *conversion event* (register, book a call, reply-yes) and its **source of truth** (an event guest list, a booking calendar, a form). Pull that source first; the tracker and Gmail are not authoritative for who converted.

## The loop

1. **Read the campaign definition** (statuses, mediums, scripts, goal) from the tracker + page.
2. **Pull the conversion source of truth**, filtered to *actual* conversions, and reconcile against the tracker — mark only those not already at the conversion status.
3. **Sweep each active reply channel** (per the Medium options in use) for new inbound — see Channel sweeps below.
4. **For each contact with a new signal, advance one step** along the campaign's own funnel and fire the matching page script.
5. **Log and set/clear Next Contact** by behavior (see below).
6. **Refresh any on-page summary** (a segment legend, a counts dashboard) so the at-a-glance view stays true.

**Count the unsent backlog before drafting new rungs.** A row whose last note ends in "drafted, not sent" is not waiting on you for a decision, it's waiting on a send — and every rung queued behind it is scheduled off a date that hasn't started counting. Surface the backlog as its own number before adding to it, because a sync that drafts forward over an unsent batch reports progress the campaign hasn't made.

## Behavior → movement

The specific status labels come from the campaign; the *pattern* is constant. Read the signal, then set the campaign's corresponding status:

- **Converted** (hit the conversion event): set the conversion status. If the funnel has a post-conversion ask (share/repost, refer, a next step), fire it and set that status too; predraft the ask so Shaw can send.
- **Warm** (positive reply, a question, "is this legit?", "hopefully I can make it"): set the reply status, respond using the page's reply script, and set a follow-up date so they resurface. Confirm the FU date with Shaw and set it uniformly across the batch so they surface together in the CRM sweep.
- **Cold** (declines, "already doing it"): set the reply status and fire the campaign's salvage ask if it has one (e.g. "know anyone who'd want this?").
- **Replied-but-cold next-touch override.** When an FU1 nudge already went out but the reply went cold without a register, queue the cold-salvage template for the *next* touch slot instead of the default FU2 — advance Next Contact and note the swap rather than firing a second hard nudge.
- **Ball in their court** (they reply promising to re-initiate — "I'm on vacation, let me try this and come back to you"): warm, but terminal for cadence purposes. Clear Next Contact and don't queue an FU. They've already committed to the next move, so a nudge asks a question they've answered; the reply itself is the follow-up. Distinguish this from a plain positive reply, which leaves the next move with Shaw and *does* earn a date.
- **Terminal** (every message that applies to them has been sent): clear Next Contact so they drop out of the sweep. Drafted is not sent — an unsent message *is* the next touch, and a row cleared on one looks exactly like a row that finished, so nothing surfaces it again. If they graduate to a real conversation, use the campaign's hand-off status (e.g. `Added to CRM`) and follow the CRM skill's promotion rule.

Three rules that keep the log honest:
- **Any state you wrote is a claim with an expiry — re-read it before you report it.** Writes get reverted and Shaw sends without telling you, so a row you set an hour ago may not say what you think. Read it back from the tracker rather than from your own record of having written it — and when a send turns out to have happened, check the conversion source too, not just the note.
- **Record the actual reply channel**, even when it differs from the row's Medium — someone emailed the ask may reply on LinkedIn. Note it in Notes.
- **Draft, never send.** Predraft share-asks in the row body and draft email/DM replies for Shaw; only advance the "sent" statuses (`Share Ask Sent`, `Shared`) once he confirms he sent.

## Channel sweeps

**Conversion source** — filter to real conversions before reading (an unfiltered list mixes in invited-but-not-registered people and inflates the count). Match to tracker rows by email where the source carries one, else by **name tokens** (first + last; display names vary — "Will"/"William", "Dr." prefixes — so match shared tokens, not exact strings). Platform mechanics for Luma: `../events/luma-guest-list.md`.

**Gmail** — one search over the send window (`in:inbox newer_than:Nd`, N = days since the asks went out). Separate campaign replies from unrelated inbound. Read the full thread with `get_thread` before logging — snippets truncate and mislead, and they also *normalize* text rather than merely cutting it: Gmail strips periods out of abbreviations in a snippet, so `(i.e.` renders as `(ie` and reads as drift that isn't there. Diffing sent-vs-drafted off a snippet manufactures false positives as readily as it hides real ones.

**LinkedIn DMs** — LinkedIn has two message inboxes and a Sales Nav-sourced campaign will have threads in both: a DM sent from Sales Navigator lives in the Sales Nav inbox (`/sales/inbox/`) and never appears in LinkedIn messaging, and the reverse holds too. Neither inbox knows about the other, so an empty sweep of one is evidence you read the wrong inbox, not that the message was never sent — sweep both, and match each row to whichever inbox holds its thread. Message search is no substitute: it misses live recent threads, so a nil result proves nothing.

Sending splits the same way. A thread belongs to the tool it was started from, and the next rung sent from the other one opens a *second* thread rather than continuing the first. The recipient usually still sees one conversation; what breaks is the sender's own view of the sequence. Send each rung where that person's history already is.

Within an inbox: don't open profiles one by one, and don't sweep the whole inbox. The tracker already names who's been contacted, and only those threads can carry a campaign reply, so pull that set first and let its size decide how much inbox you read. The messaging inbox is recency-sorted, so any reply floats to the top with the *contact* as the last sender, while un-replied asks show a **"You:"** prefix on the snippet. So: scan the inbox and flag every thread whose latest snippet is **not** "You:" — those are the replies. When the contacted set fits inside the first render, that one read is the entire sweep. When it doesn't:
- The list virtualizes (~10–20 rendered). Scroll the conversation-list container and click **"Load more conversations"** to load the whole campaign-day cluster — a reply sent the same day as the asks can sit *buried among* them, not just at the very top.
- Virtualization recycles aggressively — in a single DOM snapshot most rows can be blank, so a one-shot scrape silently misses threads. Scroll back to the top and accumulate names into a persistent object across small scroll steps. Because the inbox is recency-sorted, every reply since the asks went out floats into the top today→campaign-start cluster — a clean read of *that window* is sufficient.
- One tab, sequentially — the browser policy in SKILL.md.

Cross-reference the already-marked rows too: a thread ending in "You:" where that message is a *reply to their reply* (not the original ask) is already-handled activity — log it, don't re-draft.

## Rate limits

Notion rate-limits bulk property updates; pacing and retry guidance live in `notion-helper`.
