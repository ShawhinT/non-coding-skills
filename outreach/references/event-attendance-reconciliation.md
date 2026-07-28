# Event Attendance Reconciliation

Turning a finished Zoom event into a segmented attendee list. This is the mechanics half of the
**Post Event** SOP's "Send Follow-ups to attendees" step — the SOP owns the process and the policy
calls; this file owns the brittle parts.

The core problem: **the Zoom participant export usually has no emails.** Guests join without
authenticating, so Zoom records only a display name. Every attendee must be matched to a registrant
by name, which is fuzzy, error-prone, and where all the time goes. Fix it at the source when you can
(see Prevention at the bottom).

Related: `luma-guest-list.md` (pulling the registration list), `tracker-setup.md` (tracker schema),
`outreach-sync.md` (advancing status once outreach starts).

## Inputs

| File | Where | Carries |
|---|---|---|
| Luma guest CSV | Luma → Guests → Export | registrants, emails, `utm_source`, `approval_status`, `created_at` |
| Zoom participant CSV | Zoom → Reports → Usage → participants | display name, join/leave times, duration |
| Zoom chat log | recordings folder, `*RecordingnewChat.txt` | self-intros, questions, LinkedIn URLs |
| Recording transcript | recordings folder, `*.cc.vtt` | session structure / segment boundaries |

The chat log and transcript live alongside the MP4 in Shaw's Drive recordings folder
(`_ABA/events-recordings/<date>_<event-slug>/`). He may only mention the transcript — **look for the
chat log too**, it is usually the higher-value file.

**`approval_status` gates everything.** `approved` = actually registered. `invited` = sent a Luma
invite and never converted; these are not registrants and must be excluded from every denominator.
A single invite blast can more than double the row count (July 2026: 552 rows, 262 of them invites).

## Reconciling attendance

### 1. Collapse Zoom rows into people

One person yields multiple rows when they drop and rejoin. Group by normalized display name, then
**sum durations** and take the **max leave time**.

### 2. Match display names to registrants

Run a ladder, cheapest first, and hand whatever falls through to manual review:

1. Exact normalized name
2. Token-set match (handles reordering, middle names)
3. Email local-part, and the "smashed" full name (`[firstlast]` → `[first last]`)
4. Last name + first initial, **only when it resolves to exactly one registrant**
5. Manual review of the remainder against the guest list

Expect roughly a third to reach manual review. Display names in the wild: first name only (`[First]`),
company name (`[Company]-[Region] [Person]`, or a registrant literally named `[COMPANY]`), device
names (`[FIRST]'s iPad`), initials (`[M] ([Person])`), handles (`[handle]`).

### 3. Normalization traps

Both of these cost a full debugging cycle in July 2026:

- **Curly apostrophes vanish under NFKD→ASCII.** `[Person] DBA PC's iPhone` normalizes to
  `[person] dba pcs iphone`, not `...pc s iphone`. Normalize `'` → `'` *before* the NFKD pass, or
  derive override keys from the actual normalizer output rather than by hand.
- **Stripping parentheticals can empty a name.** `[M] ([Person])` → `[m]`. Keep the parenthetical
  as a fallback match key instead of discarding it.

### 4. Dedupe by matched registrant, not by display name

**The one that silently corrupts the headcount.** A person can appear under two different display
names in the same meeting — [Person] joined once as `[Company]` and once as
`[Person] ([Company])`. Deduping on display name counted him twice.

After matching, collapse on registrant email. Then check the inverse: if two display names map to the
same registrant, confirm it is a rejoin and not a bad match. That check is what exposed
`[First] D ([handle])` as a *different person* from `[FIRST MIDDLE LAST]`, who had his own row.

### 5. Exclusions

- **AI notetaker bots** — `read.ai meeting notes`, Otter, Fathom. Drop before counting.
- **The host.** Shaw appears in both the Zoom log and (often) the guest list. Exclude from
  registrations and attendance.

### 6. Duplicate registrations

Same person, two emails — usually a re-register on event day. Detect by normalized name across the
guest list (5 of 290 in July 2026). They inflate the registration denominator; report unique people.

## Deriving session boundaries from the transcript

Needed when segmenting on *when* someone left rather than how long they stayed — a late joiner who
sat through the whole back half logs fewer minutes than someone who joined early and bailed, so
duration ranks them backwards.

1. **Recording start = the filename's GMT stamp.** `GMT20260724-145811_Recording.cc.vtt` → 14:58:11
   UTC → 09:58:11 local. VTT cue offsets are relative to this.
2. **Find the structural cues** by grepping the VTT for wrap/transition language
   (`wrap up`, `let's jump into`, `Q&A`, `questions`, `demo`).
3. **Convert offset → absolute** and bucket attendees on their max leave time.

July 2026 worked example: `01:00:37` ("I think we can wrap up here… happy to stick around another 30
minutes") → **10:58:48**, the bonus-Q&A boundary. `00:46:17` ("let's just wrap up here and do a Q&A")
→ **10:44:28**, end of presentation.

**Sanity-check against the leave-time histogram** — a real boundary shows up as a cliff. 41 of 107
attendees left in the ten minutes around 10:58.

Recutting on leave time moved 29 of 90 people, 28 of them upward.

## Mining the chat log

Format is tab-delimited `HH:MM:SS\tDisplay Name:\tmessage`, with **continuation lines for wrapped
messages** — append unprefixed lines to the previous message or you will truncate the long ones.
Timestamps are relative to recording start.

Worth extracting per attendee: opening geo/role intro (Shaw asks for these), questions asked,
volunteered LinkedIn/YouTube URLs, and total message count. For attendees who registered with a
personal email this is often the *only* source of role and company.

It can also resolve identities the guest list cannot — an unregistered attendee posting their own
LinkedIn URL, or a self-intro confirming a shaky match (`[Person]` → "Germany, CEO of my own
digital agency" corroborating a `@[email-domain]` registrant named [Person 2]).

Match chat display names through the same normalizer used for the participant CSV.

## Writing the tracker

Schema conventions live in `tracker-setup.md`. Two mechanics specific to this job:

- **Bulk writes need subagent fan-out.** 90+ single-page property updates are slow sequentially.
  Split into chunks of ~16, write each to its own JSON file, and dispatch one subagent per chunk with
  instructions to call `notion-update-page` sequentially (see `batch-agent-prompt.md`). Six parallel
  agents cleared 96 rows in about 90 seconds with no rate limiting.
- **Renaming a Select vocabulary takes three passes** — ALTER to the union, retag every row, then
  ALTER to drop the retired options. Restating a Select's options replaces the entire set including
  colors, so carry existing colors forward verbatim. Full detail in `notion-helper`.

## Report honestly

Some attendees are unrecoverable — generic display names (`User`, `Guest`, `Zoom user`, `Client`),
silent in chat, no guest-list match. Count them in total attendance, exclude them from any
source or segment breakdown, and **list them explicitly**. 10 of 107 in July 2026.

Same for match confidence: flag medium/low-confidence matches on the row itself rather than
presenting them as settled.

## Prevention

Turn on Zoom registration or authentication for the event so attendees carry emails. That removes
this entire file's worth of work. It is a *pre*-event setting — it belongs in the Event Series SOP,
not Post Event.
