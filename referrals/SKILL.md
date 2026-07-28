---
name: referrals
description: >-
  Manage Shaw's referral workflow — create rows in the Referrals database, follow up on
  referral asks, log names a referrer shares, hand new intros to the CRM, and trace referred
  leads back to their referrer. Use this skill whenever Shaw mentions a referral — "did [Referrer]
  send those names?", "follow up on the referral ask", "log this intro", "kick off a referral
  ask for X", "who owes me referrals?", "sweep the referrals", "X just intro'd me to Y",
  "thank X for the referral". Also fires when a wrap-up call or testimonial publish surfaces a
  referral opportunity, when a 3-way intro email lands in Gmail (subjects like "[Name] x Shaw"),
  or when a client says "I know some people who'd want this". Trigger words: referral, intro,
  three-way intro, warm intro, "know anyone who". Do NOT use for the SOP itself (sop-helper),
  generic CRM work (crm), or testimonial asks (testimonials).
---

# Referrals Skill

Manages the **Referrals** database in ABA (Master) — the tracker for turning happy clients
and warm contacts into new warm leads (the "Referrals" R of the 4Rs). Companion skill to the
[Referral Ask SOP](https://www.notion.so/[page-id]) — the SOP carries
cadence, status definitions, ask policy, and email templates. This skill carries the
mechanics: database IDs, payload shapes, the page-body format, and skill composition. When a
question is about *what to do or when*, the SOP answers it. When it's about *how to do it in
Notion / Gmail / payloads*, this skill answers it.

## Where Referrals Live

| Thing | ID / URL |
|---|---|
| Referrals database (page) | `[page-id]` |
| Referrals data source | `[page-id]` |
| Database URL | https://www.notion.so/[database-id] |
| Referral Ask SOP | `[database-id]` |

### Related databases (when linking from a Referrals row)

| DB | Data source ID | What it carries |
|---|---|---|
| CRM Active Leads | `[page-id]` | Where referred leads get created (Source = `Referral`) |
| Clients (Nurture) | `[page-id]` | Most referrers live here (past/current clients) |
| Archived Leads | `[page-id]` | Referrers who were never clients |
| Engagements | `[page-id]` | Paid project ledger |

## Schema Cheat Sheet

| Property | Type | Notes |
|---|---|---|
| Name | title | Referrer's full name. **One row per referrer**, not per referred person — a single referrer can produce many referrals, and those live in the page body |
| Email | email | Referrer's direct email |
| CRM | url | Plain URL of their page in Active Leads / Clients (Nurture) / Archived Leads |
| Engagement | relation | → Engagements DB. Only set when there's a paid engagement row |
| Status | select | `Not Asked` · `Asked` · `Names Given` · `Intro Made` · `Converted` · `Declined`. See the SOP for what each stage means. Status reflects the *furthest* stage reached across that referrer's referrals |
| Last Contact | date | Most recent referral-related touch (ask, FU, names received, intro thread reply) |
| Next Contact | date | When the next FU is due. Cadence policy lives in the SOP. Clear when nothing is pending |
| Notes | text | Terse activity log of dated events only, `(M/D)` format, append-only. No em dashes. Don't restate engagement context — the CRM and Engagement fields carry that |

## Standard Page Body Format

Every Referrals row body uses this structure:

```
## Referrals
- [Name] ([title], [company]) — [stage: named M/D / intro'd M/D / converted M/D] <mention-page url="<their Active Leads page>"/>
```

- `## Referrals` is the canonical header. One line per referred person, in the order they
  surface. This is why there's no "Referred Leads" property — a referrer can produce
  multiple referrals, and lines scale where properties don't.
- A referred person's line starts as plain text when their name is first given. Once the
  intro lands and CRM Workflow 3 creates their Active Leads page, replace the plain name
  with a `<mention-page>` link to that page. The body becomes the referrer → pipeline map.
- Anything else worth keeping (how the offer arose, context on who they know) goes *above*
  the `## Referrals` header, mirroring the CRM convention of pinning the growing list to the
  bottom.

## Core Workflows

### 1. Open an ask

**Trigger:** a high-goodwill moment per the SOP (wrap-up call, post-session check-in,
testimonial published, client names a win), a client offers referrals unprompted, or Shaw
says "kick off a referral ask for X".

1. **Find their CRM page URL** via `notion-search` (Clients (Nurture) first for paying
   clients, then Active Leads / Archived Leads).
2. **Find their Engagement**, if one exists (paid work only).
3. **Create the Referrals row** with `notion-create-pages` against data source
   `[page-id]`: Name, Email, CRM (plain URL), Engagement (JSON
   array of page URL, only if found), Status `Not Asked`, and body content with an empty
   `## Referrals` header. Note in Notes whether the referral was *offered* (they volunteered)
   or a *general ask* (unprompted) — this decides whether you skip the check-in on-ramp and go
   straight to the ask, not the cadence (the SOP runs one cadence either way).
4. **Hand off to `email-helper`** to draft the right touch — the SOP runs one sequence: open
   with the check-in on-ramp for a general ask, or go straight to the ask if it was offered or
   made on a live call.
5. **After Shaw confirms the email sent:** Status → `Asked`, Last Contact = send date,
   Next Contact per the SOP cadence. Drafts aren't touchpoints — never advance state on an
   unsent draft. On the check-in on-ramp the check-in is not the ask: on a confirmed check-in
   send, log it in Notes and update Last Contact, but keep Status `Not Asked` until the actual
   referral ask goes out.
6. **Take the next touch.** The referral sequence is now the live one, so this row owns the
   person's next outbound. Open the linked `CRM` record, clear its `Next Contact`, and append
   a pointer to its Notes: `Next touch owned by Referrals, due M/D.` Do the same on their
   Testimonials row if one exists. This applies from the first *sent* touch, including the
   check-in on-ramp — the on-ramp is outbound to the same person, so it owns the touch even
   while Status is still `Not Asked`. This step is what actually creates the state "One
   person, one next touch" describes; without it the convention never takes effect and the
   sweep's collision check (Workflow 5) is only a backstop for rows that predate it.

### 2. Log names

**Trigger:** the referrer replies with names ("you should talk to..."), mentions people on a
call, or Shaw relays them.

1. Status → `Names Given`. Last Contact = the date the names arrived.
2. Add one line per person under `## Referrals` (name, title/company if known, `named M/D`).
3. Hand off to `email-helper` for the next move per the SOP — draft the intro from the
   name/email they gave, or share the forwardable script if they'd rather send it themselves.
4. Set Next Contact for a nudge in case the intro doesn't land.

### 3. Intro lands → CRM handoff

**Trigger:** a 3-way intro email arrives (watch for `<Name> <> Shaw` subjects), or Shaw says
"X intro'd me to Y".

1. Hand the new person to **CRM Workflow 3** (add a new lead): Active Leads row with
   Source = `Referral`. Reply on the intro thread per the SOP (via `email-helper`).
2. On the Referrals row: Status → `Intro Made`, update the person's line under
   `## Referrals` to a `<mention-page>` link to their new Active Leads page (`intro'd M/D`).
3. From here the *lead's* journey is the CRM's job. This row only tracks the referrer
   relationship — don't duplicate the lead's pipeline activity here.

### 4. Convert / close out

**Trigger:** a referred lead closes, the referrer actively declines, or the cadence is
exhausted.

- **Converted:** Status → `Converted`, tag the person's line (`converted M/D`), and surface
  a thank-the-referrer prompt — this is also a high-goodwill moment for the *next* ask.
  Hand the thank-you note to `email-helper`.
- **Declined:** Status → `Declined`, clear Next Contact, add a Notes line with the reason.
  `Declined` is for an active no; a ghosted ask parks as dormant on silence rather than
  hitting `Declined` — see the SOP.
- **Hand the touch back** on either terminal outcome, and on a row that parks as dormant.
  Both `Converted` and `Declined` end this row's claim on the person's next outbound, so
  ownership returns to the CRM record: set its `Next Contact` per its own nurture cadence
  and strip the `Next touch owned by Referrals` pointer from its Notes. A dormant row counts
  too — parking on silence is exactly the case where the person would otherwise end up
  scheduled nowhere, which reads as handled and isn't.

### 5. Sweep — who needs a nudge?

**Trigger:** "any referrals due?", "sweep the referrals", "who owes me referrals?", or a CRM
Workflow 1 sync (referrals ride along the same pass, like campaign trackers).

1. Query the database default view (`notion-query-database-view`), then filter client-side on
   **Next Contact ≤ today for any non-terminal row** — `Not Asked`, `Asked`, and `Names Given`
   all qualify; only `Converted` and `Declined` are terminal. Status is the wrong filter here:
   the SOP deliberately parks a row at `Not Asked` through the whole check-in on-ramp (the
   check-in plus up to 2 check-in FUs), flipping to `Asked` only when the actual referral ask
   goes out. Filtering on `Asked` therefore skips every live on-ramp row. Next Contact is what
   says a row is due; Status only says which template to reach for.
2. **Reconcile against Gmail first.** Cross-reference Gmail for replies since Last Contact
   (`from:<email> OR to:<email>`) — a reply may have already advanced the stage. If it has
   (names given, or an intro landed), apply **Workflow 2** (log names) or **Workflow 3** (intro
   handoff) to advance the row *before* deciding on a nudge, so the sweep acts on current state,
   not stale Status. Gmail is the source of truth for whether the referrer moved; the row's
   `Status` can lag it.
3. **Check the sibling row before drafting.** For each due row, open the linked `CRM` record
   (and the person's Testimonials row, if any) and read its `Next Contact`. If another row is
   also live, the two databases are both about to contact the same person. What to do next
   depends on whether ownership is actually in question:
   - **Unambiguous — repair it.** If this row's own sequence is mid-cadence (an ask or
     on-ramp touch is out, FUs are running) and the sibling is just a stale date nobody took,
     that's drift from a row created before the take-ownership step existed, not a real
     decision. Blank the sibling, add the pointer, draft normally, and report the repair in
     the sweep summary.
   - **Ambiguous — surface it.** If both sequences are genuinely live and neither obviously
     started later, don't pick a winner; hand it to Shaw as a decision, per "One person, one
     next touch" in the crm skill.

   Once Workflow 1 step 6 is running on new rows, this check should mostly stop firing —
   treat a collision as a signal that a row predates the convention.
4. Surface per row: name, status, days since Last Contact, and which FU is next per the SOP.
   Hand each draft to `email-helper`.

## Composition with Other Skills

- **`email-helper`** — owns all email composition. Hand off the SOP template name + row
  context; it produces the draft. Every Gmail draft in these workflows goes through it.
- **`crm`** — owns the referred *lead* once an intro lands (Workflow 3 creates it; the lead's
  cadence lives on their Active Leads row, not here). Also owns the referrer's own client
  cadence: referral FUs don't reset the client record's Status or Notes. The next-touch *date*
  is a different matter — it's owned by one row at a time across both databases, per
  "One person, one next touch" in the crm skill. When a referral sequence is live it owns the
  touch and the client record's `Next Contact` stays blank; when the sequence parks or goes
  terminal, ownership hands back.
- **`testimonials`** — its post-publish nudge is a referral-ask trigger; when it fires,
  run Workflow 1 here.
- **`sop-helper`** — for edits to the Referral Ask SOP (cadence, templates, policy). Don't
  restate SOP content here; if policy needs to change, change it there.
- **`notion-helper`** — for ad hoc FU task pages in ABA when a referral action needs a dated
  reminder outside this database.

## Rules

- **Defer cadence, status meanings, ask policy, and email templates to the SOP.** This skill
  carries mechanics only. Single source of truth.
- **One row per referrer; referred people live in the body.** Never create a property or a
  separate row per referred person — the `## Referrals` body section is the ledger.
- **Append, never overwrite Notes.** Same `(M/D)` conventions as the CRM. No em dashes
  anywhere Shaw owns.
- **Drafts aren't touchpoints.** Only advance Status / Last Contact / Next Contact on sends
  and events that actually happened.
- **Don't duplicate the lead's pipeline here.** Once an intro is in Active Leads, this row
  only tracks the referrer relationship and the body link.
- **Offered vs. general ask changes where you start, not the cadence.** Note in Notes which
  one each ask is — an offered referral (or a live-call ask) skips the check-in on-ramp and
  goes straight to the ask, but the follow-up cadence is the same either way (per the SOP).
  [Referrer]/[Company] is the canonical offered case.
- **Notion + Gmail-via-email-helper only.** No calendar events, invoices, or other side
  effects from this skill.

## Quick Reference: Tools

Assume these are loaded via `tool_search` before first use.

| Need | Tool |
|---|---|
| Find a referrer's CRM page / Engagement | `notion-search` |
| Read a Referrals row | `notion-fetch` |
| Create a Referrals row | `notion-create-pages` |
| Update Status / properties / body | `notion-update-page` |
| Query the database for the sweep | `notion-query-database-view` |
| Check for replies / intro threads | Gmail `search_threads`, `get_thread` |
