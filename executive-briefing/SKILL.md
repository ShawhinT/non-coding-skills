---
name: "executive-briefing"
description: "Generate Shaw's daily executive briefing by pulling today's tasks from his main Notion databases. Use this skill whenever Shaw asks for his daily briefing, rundown, what's on his plate, what he has going on today, or anything about reviewing his scheduled tasks for the day. Triggers include: \"give me my briefing\", \"what do I have today\", \"daily rundown\", \"executive briefing\", \"what's on my plate\", \"what's scheduled today\", \"morning briefing\", \"what am I working on today\", or any reference to checking tasks across his Notion databases. Even casual mentions like \"what's today look like\" or \"run me through my day\" should trigger this skill."
---

# Executive Briefing Skill

Shaw organizes his work across several Notion databases. The first six are dated work
databases — pages with a `Date` property, scheduled for the day Shaw wants to act on them.
The last four are relationship databases (Active Leads, Clients (Nurture), Reviews/Referrals,
Friends) where each page has a `Next Contact` field; the briefing surfaces rows whose next
touch is due. Together they form a single daily picture of what's on Shaw's plate.

A relationship database earns a place here by carrying a live `Next Contact`, not by holding
leads. Friends is the case that makes the distinction visible: nobody in it is a prospect, but
partners, channels, and affiliates have next touches that go stale exactly like a lead's — and
a next-touch date nothing sweeps is worse than no date at all, because it reads as scheduled.
When a new database starts carrying `Next Contact`, it belongs in this briefing.

The briefing is a snapshot of what's due now — not a project management tool. No overdue
items from prior days, no upcoming items beyond today's window, no backlog.

---

## Databases in Scope

The canonical database catalog (IDs, icons, descriptions) lives in `notion-helper/SKILL.md`
under "Main Databases." The Today / Tomorrow **view URLs** this briefing runs on live here, in
the "View URLs" section below. This skill queries **all main databases**:

Dated work:

- 🎓 **ABA** — tasks, launches, outreach, partnerships, events
- 🏫 **ABA Trainings** — delivery sessions (1:1 workshops, trainings, ongoing engagements)
- 👨‍🏫 **ABA Calls** — sales calls (notes, prep, scheduling)
- 📹 **LFC** — YouTube videos
- 📅 **SFC** — LinkedIn posts, YT community posts, social shares
- 🗞️ **ABN** — newsletter editions, email blasts

Follow-ups due (filtered by `Next Contact`):

- 💼 **Active Leads** — pipeline rows where the next touch is due
- 🌱 **Clients (Nurture)** — active/nurturing client check-ins coming up
- 📝 **Reviews/Referrals** — testimonial asks and referral touches where the next nudge is due (both tracks live on one row; the row's live track is whichever its Notes say)
- 🫂 **Friends** — the non-lead network (partners, channels, affiliates, subcontractors, friends, family) where the next touch is due. `Type` is the field that says what the relationship is, so it belongs in the line

If a new database is added, update `notion-helper/SKILL.md` (catalog) and add its view rows to
the "View URLs" section below.

---

## View URLs

The precomputed server-side-filtered views this briefing runs on. Today views filter the
dated-work DBs on `Date is Today` and the relationship DBs on `Next Contact` due; Tomorrow views
mirror them one day forward. All are relative filters set in the Notion UI (the view DSL can't
write relative dates), so they update automatically each day.

**Which page ID a view URL uses is not uniform, so copy these rows rather than deriving them.**
The six dated views live on the database itself. Active Leads, Clients (Nurture), and
Reviews/Referrals point at their *source* database, which is why their Today and Tomorrow rows
carry different page IDs. Friends points at the database itself for both, so its two rows share
one ID — that is correct, not a copy-paste error to "fix."

### Today Views

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[page-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[page-id]` |
| Active Leads | `https://www.notion.so/[page-id]?v=[page-id]` |
| Clients (Nurture) | `https://www.notion.so/[page-id]?v=[page-id]` |
| Reviews/Referrals | `https://www.notion.so/[page-id]?v=[page-id]` |
| Friends | `https://www.notion.so/[page-id]?v=[page-id]` |

### Tomorrow Views

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[page-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[page-id]` |
| Active Leads | `https://www.notion.so/[page-id]?v=[page-id]` |
| Clients (Nurture) | `https://www.notion.so/[page-id]?v=[page-id]` |
| Reviews/Referrals | `https://www.notion.so/[page-id]?v=[page-id]` |
| Friends | `https://www.notion.so/[page-id]?v=[page-id]` |

(The Reviews/Referrals DB carries both the testimonial and referral tracks since the 8/7/26
merge, so referral touches now surface here naturally — the old standalone Referrals DB is
frozen and not queried.)

---

## Workflow

### Step 1: Resolve the date (in Shaw's current timezone), then query all databases

Stamp the dates in his zone — read it from the session context each run, since he travels;
default to `America/Chicago` if no timezone reminder is present. Substitute it for `<TZ>`:

```
TZ="<TZ>" date +%F                     # his local today
TZ="<TZ>" date -d tomorrow +%F         # his local tomorrow
TZ="<TZ>" date -d "next Monday" +%F    # a named day
date -u +%F                            # what the connector's relative filters treat as "today"
```

**Prefer the fast saved views — the precomputed Today/Tomorrow views are the default path,
and SQL is a rare fallback.** All ten databases have both a Today and a Tomorrow view (URLs in
the "View URLs" section above, which also explains why their page IDs don't follow one rule).
They're server-side filtered and quick.

**Pick the view set from one comparison: does UTC's date (`date -u +%F`) equal Shaw's local
today or his local tomorrow?** The connector resolves every view's relative filter
("today"/"Next day") in **UTC**, so which UTC calendar day it currently is decides which
precomputed view already points at the day you want. This holds for both today and tomorrow
briefings:

| Briefing for | UTC == local today (his daytime) | UTC == local tomorrow (his evening) |
|---|---|---|
| **Today** | **Today** views | explicit-date SQL fallback |
| **Tomorrow** | **Tomorrow** views | **Today** views (they already resolve to tomorrow) |

The case that's easy to miss: during Shaw's evening UTC has already rolled to his tomorrow,
so for a *tomorrow* briefing the **Today** views are the correct one-shot source — don't drop
to SQL. Only fall to SQL when the table sends you there (a today briefing in his evening) or
the target isn't today/tomorrow (a named weekday).

- **Fire the view queries in parallel — one batch, all the views you need.** `mode:view`
  queries are cheap; the parallel-timeout warning below is SQL-only and does not apply to
  views.
- **After reading a view, narrow its rows to the resolved day yourself** — dated: keep rows
  whose `Date` falls on the target date; relationship: keep rows whose `Next Contact` is on
  or before it. This makes the briefing correct no matter how tightly each view happens to be
  filtered (some carry a single "after today" rule that also lets later items through), so you
  never have to audit the views. The view rows already carry `url` (and status/notes for
  relationship rows), so you have everything Step 2 needs without re-querying.

**Fall back to explicit ISO dates** only when the table above sends you there (a today
briefing in his evening, or a named day that isn't today/tomorrow). Comparing the stored ISO
date strings is timezone-safe — plain text, matched literally, no relative-"today" resolution
in play. Query the data sources with `notion-query-data-sources` (SQL mode), IDs from
`notion-helper/SKILL.md` → "Main Databases":

- Dated work (6): `WHERE "date:Date:start" >= '<date>' AND "date:Date:start" < '<next-day>'`
- Relationship (4): `WHERE "date:Next Contact:start" <= '<date>'`

SQL gotchas, learned the hard way:

- **Cap parallel SQL queries at 4** (see `notion-helper` → "Connector quirks"). Up to 4
  `query_data_sources` calls batch fine; a 5th trips a 429. With ten databases, run them in
  batches of ≤4 with a brief gap, and wrap each in a retry-once — a throttled query recovers in
  ~30–60s. (SQL-only — `mode:view` queries batch freely.)
- **Select `url` and the display columns you'll show in the first query** — not just `Name`
  and the date. Re-querying a database just to pick up `url` for the links doubles the
  round-trips. Dated work: `SELECT "Name", "url", "date:Date:start"`. Relationship rows also
  grab `"Status"`, `"Notes"` (and `"date:Next Contact:start"`) so the Notes are in hand
  without a page fetch.
- Use the expanded SQL columns `date:Date:start` / `date:Next Contact:start` (bare `Date` /
  `Next Contact` errors with "no such column").
- Avoid `SELECT *` — some sources (ABA Calls) carry dozens of columns per row; list the
  columns you need.

Either way, everything downstream (Step 2 page fetch, Step 3 formatting) is identical — only
the resolved date and the date label in the output header change.

### Step 2: Fetch page content for each matching item

For each returned item, use `notion-fetch` with the page URL/ID to pull the page content.
This gives you the context needed to write a useful 1-2 sentence description. Fetch all
pages in parallel.

Also extract the page's `icon` attribute from the `<page>` tag in the fetch response
(e.g., `<page url="..." icon="✅">`). Shaw uses ✅ as the page icon to mark completed
tasks. If the icon is ✅, prepend it before the linked task name in the output. For any
other icon (or no icon), display the item normally with no prefix.

When summarizing page content:
- For ABA tasks: describe the specific action or deliverable
- For ABA Trainings: include the participant's name, session type (1:1 workshop, training,
  etc.), and any key context from session notes or prior prep
- For ABA Calls: include who the call is with, their company/role, and any key context
  from call notes or pre-call research
- For LFC items: describe the video topic and current stage (outline, scripting, filming, etc.)
- For SFC items: describe the post topic and whether draft copy exists
- For ABN items: describe the newsletter edition or email task
- For Active Leads: status (Booked Call, Outline Sent, etc.) and the most recent Note line
  so the next step is obvious
- For Clients (Nurture): status (Active, Nurturing, Expansion) and the most recent Note line
  — what's the next touch
- For Reviews/Referrals: the live track's status (Review Status: Asked, Form Submitted,
  Approved; or Referral Status: Asked, Intro Made) and what's owed (FU nudge, polish quote,
  publish, referral check-in, etc.) — the Notes say which track is live
- For Friends: the `Type` (Partner, Channel, Affiliate, Subcontractor, Friend, Family) and the
  most recent Note line — what the next touch is. `Type` matters more here than status does
  elsewhere, because it's what tells Shaw whether he's nudging a deal, an audience ask, or a
  catch-up. A Friends row's real state usually lives in its page body under `Arrangement:` and
  `Open items:`, so fetch the page when the Notes line alone doesn't say what's owed

The relationship-database rows (Active Leads, Clients (Nurture), Reviews/Referrals, Friends)
often have rich `Notes` columns in the query response itself — use those directly rather than
fetching each page, unless the row needs deeper context.

### Step 3: Present the briefing

Output as plain text, organized by database section. Format:

```
**🎓 ABA**
- [**Item name**](https://www.notion.so/page-id) — Brief context from page content.
- ✅ [**Item name**](https://www.notion.so/page-id) — Brief context from page content.

**🏫 ABA Trainings**
- [**Participant name**](https://www.notion.so/page-id) — Session type and key context.

**👨‍🏫 ABA Calls**
- [**Person name**](https://www.notion.so/page-id) — Key context from call notes.

**📹 LFC**
- [**Video title**](https://www.notion.so/page-id) — Topic and current stage.

**📅 SFC**
- [**Post title**](https://www.notion.so/page-id) — Post topic and draft status.

**🗞️ ABN**
- Nothing scheduled for today.

**💼 Active Leads**
- [**Lead name**](https://www.notion.so/page-id) — Status; next step from Notes.

**🌱 Clients (Nurture)**
- [**Client name**](https://www.notion.so/page-id) — Status; next touch from Notes.

**📝 Reviews/Referrals**
- [**Person name**](https://www.notion.so/page-id) — Live track + status; what's owed.

**🫂 Friends**
- [**Person name**](https://www.notion.so/page-id) — Type; next touch from Notes.
```

---

## Output Rules

- Only items due today (dated work + follow-ups whose Next Contact has arrived) — no
  overdue items from prior days, no upcoming items beyond today's window, no backlog
- Every section appears even if empty — show "Nothing scheduled for today." for empty sections
- Each item name is bold and linked to its Notion page URL
- Completed items (page icon ✅) get a ✅ prefix before the linked name; all others have no prefix
- Descriptions are 1-2 sentences max, pulled from the actual page content
- Keep the section order consistent: ABA → ABA Trainings → ABA Calls → LFC → SFC → ABN →
  Active Leads → Clients (Nurture) → Reviews/Referrals → Friends (dated work first, then
  follow-ups)
- No commentary, no prioritization advice, no suggestions — just the facts
- No widget/visualization — plain text only