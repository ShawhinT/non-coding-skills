# Event Attendance Reconciliation

Turning a finished Zoom event into a segmented attendee list. This is the mechanics half of the **Post Event** SOP's "Send Follow-ups to attendees" step — the SOP (`sop-helper`) owns the process and policy calls; this file owns the brittle parts.

The core problem: **the Zoom participant export usually has no emails.** Guests join without authenticating, so Zoom records only a display name, and every attendee has to be matched to a registrant by name — fuzzy, error-prone, and where all the time goes. Prevent it when you can: turning on Zoom registration or authentication is a *pre*-event setting (Event Series SOP) that removes this whole file's worth of work.

Related: `luma-guest-list.md` (the registration list), `../campaign/tracker-setup.md` (tracker schema, including the post-event columns), `../sync/outreach-sync.md` (advancing status once outreach starts).

## Inputs

| File | Where | Carries |
|---|---|---|
| Luma guest CSV | Luma → Guests → Export | registrants, emails, `utm_source`, `approval_status`, `created_at` |
| Zoom participant CSV | Zoom → Reports → Usage → participants | display name, join/leave times, duration |
| Zoom chat log | recordings folder, `*RecordingnewChat.txt` | self-intros, questions, LinkedIn URLs |
| Recording transcript | recordings folder, `*.cc.vtt` | session structure / segment boundaries |

The chat log and transcript sit alongside the MP4 in Shaw's Drive recordings folder (`_ABA/events-recordings/<date>_<event-slug>/`). He may only mention the transcript — **look for the chat log too**; it is usually the higher-value file.

## Rules

- **`approval_status` gates everything.** `approved` = registered. `invited` = sent a Luma invite and never converted — not a registrant, excluded from every denominator. An invite blast can more than double the row count.
- **Collapse Zoom rows into people first.** One person yields multiple rows when they drop and rejoin: group by normalized display name, sum durations, take the max leave time.
- **Match with a ladder, cheapest first,** handing the remainder to manual review: exact normalized name → token-set match (reordering, middle names) → email local-part and the "smashed" full name (`janedoe` → `jane doe`) → last name + first initial *only when it resolves to exactly one registrant* → manual review against the guest list. Budget for roughly a third reaching manual review.
- **Dedupe by matched registrant, not display name.** The same person can appear under two display names in one meeting (a company name, then `Name (Company)`); deduping on display name counts them twice. Collapse on registrant email, then check the inverse — two display names mapping to one registrant is either a rejoin or a bad match, and that check is what catches two different people with similar names.
- **Exclude notetaker bots** (read.ai, Otter, Fathom) and **the host** from both registrations and attendance.
- **Duplicate registrations** (same person, two emails — usually a re-register on event day) inflate the denominator. Detect by normalized name across the guest list; report unique people.
- **Segment on *when* someone left, not how long they stayed.** A late joiner who sat through the back half logs fewer minutes than an early joiner who bailed, so duration ranks them backwards.
- **Report honestly.** Some attendees are unrecoverable — generic display names (`User`, `Guest`, `Zoom user`), silent in chat, no guest-list match. Count them in total attendance, exclude them from source and segment breakdowns, and list them explicitly. Flag medium/low-confidence matches on the row rather than presenting them as settled.

## Gotchas

- **Curly apostrophes vanish under NFKD→ASCII** (`PC's iPhone` → `pcs iphone`, not `pc s iphone`). Normalize `'` → `'` *before* the NFKD pass, or derive override keys from the actual normalizer output rather than by hand.
- **Stripping parentheticals can empty a name** (`M (Jane D)` → `m`). Keep the parenthetical as a fallback match key instead of discarding it.
- **Display names in the wild:** first name only, a company name, a device name (`[FIRST NAME]'s iPad`), initials with a parenthetical, a handle. Expect all of them.
- **Chat-log continuation lines.** The format is tab-delimited `HH:MM:SS\tDisplay Name:\tmessage`, and wrapped messages continue on unprefixed lines — append those to the previous message or you truncate the long ones. Timestamps are relative to recording start. Run chat display names through the same normalizer as the participant CSV.

## Session boundaries from the transcript

Needed for the leave-time segmentation above. Recording start is the filename's GMT stamp (`GMT20260724-145811_Recording.cc.vtt` → 14:58:11 UTC); VTT cue offsets are relative to it. Grep the VTT for wrap/transition language (`wrap up`, `let's jump into`, `Q&A`, `questions`, `demo`), convert offset → absolute, and bucket attendees on max leave time. **Sanity-check against the leave-time histogram** — a real boundary shows up as a cliff.

## Mining the chat log

Worth extracting per attendee: the opening geo/role intro (Shaw asks for these), questions asked, volunteered LinkedIn/YouTube URLs, and message count. For attendees who registered with a personal email this is often the *only* source of role and company, and it can resolve identities the guest list can't — an unregistered attendee posting their own URL, or a self-intro corroborating a shaky match.

## Writing the tracker

Schema conventions, including the post-event behavioural columns, live in `../campaign/tracker-setup.md`. Bulk writes of 90+ rows are slow sequentially — split into chunks of ~16 and dispatch one subagent per chunk, each calling `notion-update-page` sequentially. Renaming a Select vocabulary takes three passes (ALTER to the union, retag, ALTER to drop the retired options) and restating a Select's options replaces the whole set including colors — full detail in `notion-helper`.
