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

## Behavior → movement

The specific status labels come from the campaign; the *pattern* is constant. Read the signal, then set the campaign's corresponding status:

- **Converted** (hit the conversion event): set the conversion status. If the funnel has a post-conversion ask (share/repost, refer, a next step), fire it and set that status too; predraft the ask so Shaw can send.
- **Warm** (positive reply, a question, "is this legit?", "hopefully I can make it"): set the reply status, respond using the page's reply script, and set a follow-up date so they resurface. Confirm the FU date with Shaw and set it uniformly across the batch so they surface together in the CRM sweep.
- **Cold** (declines, "already doing it"): set the reply status and fire the campaign's salvage ask if it has one (e.g. "know anyone who'd want this?").
- **Replied-but-cold next-touch override.** When an FU1 nudge already went out but the reply went cold without a register, queue the cold-salvage template for the *next* touch slot instead of the default FU2 — advance Next Contact and note the swap rather than firing a second hard nudge.
- **Terminal** (reached a *leaf* of the campaign's outreach logic tree — no further scripted step exists): clear Next Contact so they drop out of the sweep. Every branch has a leaf, not just the conversion one: a registrant who's been sent the share/repost ask *and equally* a "no" who's been sent the referral/"know anyone?" salvage ask have both run the sequence to its end — clear both. The leaf is campaign-defined, so read it off the campaign page's logic tree rather than hardcoding one status. If they graduate to a real conversation, use the campaign's hand-off status (e.g. `Added to CRM`) and follow the CRM skill's promotion rule.

Two rules that keep the log honest:
- **Record the actual reply channel**, even when it differs from the row's Medium — someone emailed the ask may reply on LinkedIn. Note it in Notes.
- **Draft, never send.** Predraft share-asks in the row body and draft email/DM replies for Shaw; only advance the "sent" statuses (`Share Ask Sent`, `Shared`) once he confirms he sent.

## Channel sweeps

**Conversion source** — filter to real conversions before reading (an unfiltered list mixes in invited-but-not-registered people and inflates the count). Harvest the (usually virtualized) list into a set, then match to tracker rows by **name tokens** (first + last; display names vary — "Will"/"William", "Dr." prefixes — so match shared tokens, not exact strings). Platform mechanics for Luma: `luma-guest-list.md`.

**Gmail** — one search over the send window (`in:inbox newer_than:Nd`, N = days since the asks went out). Separate campaign replies from unrelated inbound. Read the full thread with `get_thread` before logging — snippets truncate and mislead.

**LinkedIn DMs** — don't open profiles one by one. The messaging inbox is recency-sorted, so any reply floats to the top with the *contact* as the last sender, while un-replied asks show a **"You:"** prefix on the snippet. So: scan the inbox and flag every thread whose latest snippet is **not** "You:" — those are the replies. Three gotchas:
- The list virtualizes (~10–20 rendered). Scroll the conversation-list container and click **"Load more conversations"** to load the whole campaign-day cluster — a reply sent the same day as the asks can sit *buried among* them, not just at the very top.
- Virtualization recycles aggressively — in a single DOM snapshot most rows can be blank (seen once: 100 of 160 rows recycled to empty), so a one-shot scrape silently misses threads. Don't trust one read: scroll back to the top and accumulate names into a persistent object across small scroll steps. Because the inbox is recency-sorted, every reply since the asks went out floats into the top today→campaign-start cluster — a clean read of *that window* is sufficient, and you needn't render every older thread.
- One sequential tab only; never run parallel Chrome agents (the extension serves one connection).

Cross-reference the already-marked rows too: a thread ending in "You:" where that message is a *reply to their reply* (not the original ask) is already-handled activity — log it, don't re-draft.

## Rate limits

Notion's collection API rate-limits hard during a sync — space property updates (~9–11 per burst) and expect 429s that need 30–200s waits.
