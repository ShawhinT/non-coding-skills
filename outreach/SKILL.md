---
name: outreach
description: >
  Run 1:1 outreach campaigns end-to-end — sourcing the list, enriching it, triaging into segments,
  setting up a Notion tracker, drafting templates, sending, and logging responses. Use this skill
  whenever Shaw is building a list of people to reach out to, setting up outreach tracking, or
  crafting the messages themselves. Triggers include: "find people on LinkedIn", "pull my connections",
  "build a lead list", "enrich this CSV", "look up where these people work", "get company sizes",
  "set up outreach", "create an outreach table", "add people to the outreach list", "who have I
  reached out to", "update outreach", "sync the outreach", "who registered",
  "write me an outreach message", "draft a DM template", or any
  time Shaw shares a batch of names he's reaching out to. Also casual phrasing like "check my LinkedIn
  for analytics people", "I texted these 5 people", "what should I say to
  these people". Covers workshops, events, research calls, partnerships, reshare asks
  (lead getters), and any 1:1 outreach initiative.
---

# Outreach

This skill runs Shaw's outreach campaigns end-to-end. Two halves of the same workflow: **build the list**, then **work the list**. A campaign is a coherent outreach push with a clear audience and goal — a workshop, an event, a research-call batch, a partnership push.

## General principle: confirm before creating

Before committing to anything structural — a pipeline plan, a tracker schema, a segment scheme, a template direction — use the AskUserQuestion tool to present the plan and get Shaw's sign-off. Assumptions on shape are easy to get wrong and tedious to undo. A quick confirmation saves rework.

## Pipeline design principles

Every campaign is a sequence of **(enrich → filter) cycles** using progressively more expensive tools on a shrinking candidate set. For any piece of information you need about a candidate, try these in order — only falling back to the next when the previous can't resolve:

```
1. Extract from data you already have (free)
2. Web search with Haiku agents in parallel (cheap)
3. Chrome profile lookup (expensive)
4. Ask the user (most expensive)
```

This pattern is fractal:
- **Pipeline level:** the entire campaign is enrich → filter cycles, cheapest first
- **Stage level:** within "get company names," first extract from titles (free), then web search the remainder (cheap), then Chrome the unknowns (expensive)
- **Decision level:** within "should we include this person," first check automated criteria, then enriched data, then ask Shaw

### Kickoff alignment (do this FIRST, before any research)

The most important thing to lock at the start of every campaign — get explicit sign-off on all of it:

1. **The wide net.** What's the starting pool — who do we cast for and how (which source, which search terms)? This is the top of the funnel; agree on it before scraping a single name.
2. **The non-negotiables.** In most campaigns these are **role and company size** — the two axes that actually gate. Everything else (industry, AI-interest, location) is *scored/flexible*, not a hard cut. State the role bar (must own/lead or be budget-authority C-suite — decide explicitly whether hired C-suite counts, or founders/owners only) and the **size band** (e.g. 10–1,000 employees).
3. **The anti-ICP.** Ask *"who looks like a fit but isn't actually a buyer?"* and write it down. This is easy to miss and expensive to discover late — last time the realization that "AI-native builders/teachers are peers, not customers" surfaced mid-run and inverted the entire ranking. Decide exclusions up front.
4. **The weights.** If scoring, set component weights now (role + size dominate; flexible factors weigh less). Don't let weighting emerge through iteration.
5. **Seed `disqualified.md` from the CRM — first.** Pull **Clients (Nurture)** and **Active Leads** from the Notion CRM and exclude anyone already a client or in the active pipeline *before* scoring or enriching them. Don't leave CRM dedup to the end.
6. **Sanity-check the channel.** Is the warm network even the right well? An audience-saturated network (e.g. an AI educator's connections are ~half AI builders) will surface mostly anti-ICP under role-based search. Sourcing is often the binding constraint, not scoring — consider adopter/industry-oriented terms with the peer-exclusion baked in, or a different source entirely.

Then classify each criterion by evaluation cost (free / cheap / expensive / manual), sequence cheapest first, and present the pipeline to Shaw before starting.

### Filtering discipline (when to cut vs. keep)

- **Cut early only on cheap + unambiguous signals.** If role or size is unmistakable from the headline alone — an obvious solopreneur/freelancer/one-person shop, an obvious employee at a mega-corp, a clear non-buyer (IC, student, ex/aspiring founder) — drop them at the free stage; there's no value enriching them.
- **Keep everything ambiguous or unknown → enrich → filter on facts.** A fuzzy headline, a title that could be founder-or-staff, or a *missing* value is NOT grounds for cutting. Carry them through enrichment and disqualify only once you have the data.
- **Never filter on a field until it's fully populated.** A missing company size is not "out of band" — it's unknown. Resolve it for everyone (web → Chrome) before applying any size cut. Err toward keeping the unknown until disqualified by real data.

### Scoring & gating (for larger lists)

When a list is big enough to rank rather than hand-pick:

- **Score, don't prematurely disqualify.** Give each prospect a score from weighted components (e.g. role + size + fit). Soft criteria move the score; they don't eliminate.
- **Gate the *expensive* step on the *cheap* score.** Run the costly enrichment/inspection only on candidates already scoring well on the free/cheap dimensions — so you never spend Chrome time or per-profile lookups on someone who's clearly off-avatar.
- Set weights at requirements time (see Kickoff alignment). Role + size are the non-negotiable axes; flexible factors are scored but never the sole gate.

### Enrichment efficiency

- **Deduplicate enrichment targets.** If 5 people work at [Company], look up [Company]'s size once.
- **Extract before searching.** Titles often contain companies ("PM at Figma"). Parse these before any web search.
- **Batch web searches** into parallel Haiku agents (~10 per agent), or a Workflow with structured output (agents read the lead file by index range and return validated rows — cleaner aggregation).
- **Chrome is last resort** — sequential and rate-limited. Reserve for the smallest possible set of unresolved unknowns.
- **Never run parallel subagents against Chrome.** The extension serves ONE connection; concurrent agents driving separate tabs crash it within a couple of lookups (confirmed 2026-07-06: 4 parallel DM-history agents → extension disconnected, 2 of 4 batches returned nothing). For browser work (DM sweeps, profile/follower checks), use ONE agent working sequentially in ONE tab (~1 min/lookup), chaining batches of ~15. Parallelism is for web-search agents only. A single long-running sequential agent reliably finishes 10–18 lookups.
- **Finish the field before filtering on it.** When a filter depends on company size, run web search *then* a Chrome cleanup pass on every remaining "unknown" — get to zero unknowns before any size cut. (Don't shortcut Chrome with a second web pass; last run that left 46 unresolved.)
- **Validate coherence: size must be for the company they own/lead**, not an employer or client. Watch for (a) pure employees — "GTM @ Stripe" means Stripe is not *their* company; (b) fractional/advisory/consultants — their led company is their own (often solo) practice, not the client they serve; (c) inflated or garbled web-search sizes. Verify role↔company↔size all refer to the same led entity.

### Manual checkpoints

Place checkpoints **after automated filters have narrowed the list but before expensive enrichment**. Don't ask Shaw to review raw/unfiltered lists, and don't wait until the end for feedback — by then enrichment on cut candidates is already wasted. Shaw adds soft exclusions that no automation can know.

## Disqualification tracking (`disqualified.md`)

A living document created at campaign start and updated throughout the run. Its primary job is **intra-campaign efficiency**: when Shaw gives feedback mid-pipeline ("[Person]'s off the table"), it goes into `disqualified.md` immediately and applies to all remaining candidates — preventing wasted enrichment on people already cut.

Two sections:

**1. Disqualification principles** — general rules applied automatically at every stage:
- "Exclude anyone already a client (Clients/Nurture) or in the active pipeline (Active Leads)" — **seed this from the CRM at kickoff, before scoring or enriching**
- "Exclude the anti-ICP" — the people who look like a fit but aren't buyers (decided at kickoff)
- "Only one person per company per job level"
- "No one obviously outside the size band (clear solopreneur, clear mega-corp employee)"

Checked before any enrichment step. If a principle disqualifies someone, skip the enrichment. (Soft/ambiguous size or fit is NOT disqualified here — that's scored and filtered on real data later.)

**2. Disqualified individuals** — people who *pass all automated criteria* but get cut for contextual reasons only Shaw knows:

| Name | LinkedIn URL | Reason |
|------|--------------|--------|
| [Person] | .../in/[linkedin-handle] | Already reached out, not interested |
| [Person] | .../in/[linkedin-handle] | Already have a contact at [Company] |

**Not for this table:** People who fail criteria filters (wrong role, wrong size). Those should be caught by automation — if they slip through, fix the filter.

When Shaw gives feedback like "no, X is off the table because Y":
1. Add them to `disqualified.md` immediately
2. Check if the reason implies a new principle ("already have someone at [Company]" → "one contact per company")
3. If so, add the principle and retroactively apply it before continuing

---

## The flow

### 1. Clarify the campaign and design the pipeline

Before touching any source, run the **Kickoff alignment** above (wide net · non-negotiables of role + size · anti-ICP · weights · CRM-seed `disqualified.md` · channel sanity-check). Plus:
- **Campaign context:** what's it for (workshop, event, research calls, partnerships)
- **Target profile:** role bar, seniority preference, location priority, **size band** (the hard one), industry (usually soft)
- **Anti-ICP:** who looks like a fit but isn't a buyer — decide and write down now
- **Volume needed:** how many final leads? Work backward assuming heavy attrition (a saturated network can attrit 95%+).
- **Channels:** LinkedIn DM, email, text, mix
- **Segments:** how will you group outreach (warmest first)? Common patterns: relationship proximity (in-person / virtual call / email-only), seniority × location, channel, fit tier.
- **Exclusions:** existing clients & active leads (from CRM), prior outreach, specific companies, geographic cuts

Then design the pipeline per the principles above — classify criteria by cost, sequence cheapest first. Present the plan to Shaw before executing.

**Drop a reproducible `recipe.md` in the campaign folder** capturing the agreed sequence (wide net → cheap filters → enrichment → hard filters → checkpoint → tracker → templates) so the run is repeatable and the next campaign can start from it.

### 2. Build the list

LinkedIn is the default source for cold/warm prospect lists → see **`linkedin-sourcing.md`** for the Chrome-based scraping workflow.

Other sources Shaw uses:
- CSV imports (past event attendees, conference lists)
- Contact form submissions
- Existing client/lead databases
- Batches Shaw shares directly in chat

Save raw leads to a working file so you don't keep 100+ people in context:

```
raw/<campaign>_leads_raw.json
```

### 3. Enrich (when the pipeline calls for it)

Enrichment runs between sourcing and triage when a filter depends on data you don't have yet. The most common case is company size — see **`lead-enrichment.md`** for the decision tree (1–9 contacts → Chrome direct; 10+ → parallel Haiku agents + Chrome cleanup).

**Resolve the field fully before filtering on it.** For company size: web-search pass, then Chrome cleanup on every "unknown" until none remain — *then* apply the size band. A missing value is not out-of-band; keep unknowns until real data disqualifies them. And validate **coherence** — the company you sized must be the one they own/lead, not an employer or client (see `lead-enrichment.md`).

Other enrichments follow the same pattern: extract → web search → Chrome → ask.

#### Warmth enrichment (before segmenting a warm-network campaign)

For any campaign that segments by relationship proximity, the segment assignment is only as good as the relationship data behind it. Don't guess warmth from headlines — pull it from the actual record:

- **DM-history sweep (LinkedIn).** For each prospect, read the existing DM thread and classify: `they_reached_out` / `replied` (Shaw initiated, they responded) / `ghosted` (Shaw messaged, no reply) / `never_messaged`. This directly drives segment and send-order, surfaces ready-made openers ("great connecting at X", "congrats on the new role"), and flags who to send *last* (prior ghosts). Run it as ONE sequential Chrome agent over ~15 names per batch (see the no-parallel-Chrome rule above), read-only — never touch a compose box.
- **Cross-check Kit cohort tags.** Query Kit for ABB/cohort tags (`list_tags` → `list_subscribers_for_tag`, match by email/first name) to catch alumni the LinkedIn data won't show. Alumni are the warmest segment (paying past customers) and their alum status overrides soft exclusions — e.g. an ABB alum who'd otherwise be cut as "too technical" stays in. Log that override as a principle in `disqualified.md`.
- **Met-in-person is Shaw's knowledge.** DM history and tags won't reveal in-person meetings — ask Shaw, and re-segment when he says "I've met X."

#### Reusing a prior campaign's shortlist as a source

A recent same-ICP campaign's `FINAL_shortlist` is often the cheapest well for a new one — but **treat it as stale, not verified**. People change jobs and the original scrape had coherence errors, so re-verify role / company / size / location before loading (a fresh parallel web-search pass catches out-of-band sizes, job changes, and scrambled company↔person data). Also re-check inherited enrichment: a prior campaign's `geo` field mislabeled US people as non-US last time — verify geo from the headline/company rather than trusting the inherited value.

#### LinkedIn scraping gotchas (learned 2026-07-06)

- **Followers vs connections:** a "Has Following?" check means the **intro card** (name/headline/location block, above About/Activity) shows "X followers". EVERY profile shows a follower count down in the Activity section — that does NOT count. Instruct the agent to read the intro line only, or it returns all-Yes.
- **Reconstructed URLs 404:** slugs rebuilt from a name can be wrong, especially with accents (`[linkedin-handle]`). Don't write a guessed URL — verify it resolves, or find the real one via 1st-degree people search.
- **Verify identity, not just name match:** a 1st-degree search can surface a same-name person at the wrong company. Confirm against a known signal (company, ABB email domain) before writing the URL.

### 4. Triage into segments

Deduplicate by LinkedIn URL (or email, or whatever's unique). Then group by segment.

Segments are how Shaw prioritizes the list, assigned from the **warmth enrichment** above (DM history + Kit tags + Shaw's in-person knowledge), not guessed. The scheme varies by campaign:
- **Relationship proximity:** ABB alumni → met in person → met virtually (warm DM thread) → cold
- **Seniority × location:** DFW leaders → DFW managers → DFW ICs → non-DFW leaders → ...
- **Channel:** existing DMs → LinkedIn-only → cold email

Apply `disqualified.md` as part of triage. Present the triaged list to Shaw as a manual checkpoint before any further enrichment or tracker setup.

### 5. Set up the tracker

Once the list is confirmed, build the Notion tracker → see **`tracker-setup.md`** for the inline-database schema, segment legend, and page placement.

### 6. Draft the scripts

A campaign has a **base script** — usually one core message with a `{Personalization}` **menu** of numbered opener options (e.g. 1 = "it's been a while", 2 = "great catching up at X", 3 = "congrats on the new role", 4 = "this seemed relevant"). Draft the base warmest-segment-first, one at a time, so Shaw can steer.

Then produce a **per-prospect script for every row** — this is the real deliverable, not just one template per segment:
- Read the prospect's page-body **Context**, pick the **single best-fit menu option verbatim**, and drop the finished script into that row's page body. Shaw fills the specifics (the literal "X", any tweaks) himself — do NOT reword the opener he's going to edit.
- Keep it in a **`plain text` code block** for copy-paste. Don't un-fence it to rich text (Shaw reverts that).
- Add a one-line italic note above the block recording which option and why.

The details — segment→opener defaults, the **email-vs-DM format split**, the `Medium` column, subject-line register, email-address sourcing, and Gmail draft mechanics — live in **`references/per-prospect-scripting.md`**. Read it before scripting a mixed-channel campaign.

For writing craft specifically:
- **Voice, tone, email mechanics (HTML `<div>` spacing, Gmail threading)** → defer to **email-helper**
- **Message craft — hooks, CTAs, personalization, subject register, reply friction** → defer to **conversion-copy** (specifically `channel-outreach.md`)
- **Follow-up ladder — proof carried into the first nudge, no re-dropped in-thread links, progressively terser rungs** → defer to **conversion-copy** (`channel-outreach.md`, Follow-ups)

This skill owns the operational side (who, when, which segment, which channel); message skills own the words.

### 7. Send, log, review

**Syncing a live campaign.** When Shaw asks to check for replies, reconcile registrations, or "move the outreach forward," you're running a *sync*: sweep every reply channel and the conversion source, then advance each contact one step along the campaign's own funnel. The campaign's shape — its funnel stages, its channels, its scripts — is defined by the tracker's Status/Medium options and the page scripts, not hardcoded, so read it before acting. Full sweep→classify→advance loop: `references/outreach-sync.md`.

**When Shaw adds contacts to the tracker,** extract everything inferable from what he provides:
- Name (required)
- Segment (infer from context; Shaw usually specifies)
- Contact (email, phone, iMessage, WhatsApp, LinkedIn DM)
- Status (only if they've already hit a milestone)
- Last Contact (today if just reached out, else the date Shaw mentions)
- Notes (initial entry if there's activity)

Handle batches in a single `notion-create-pages` call.

**When Shaw reports activity** (replied, applied, booked call):
1. Find the contact in the tracker
2. Update Status and Last Contact
3. **Append** to Notes — never overwrite

**Notes format:** defer to the **CRM skill** — single source of truth. In short: short, comma-separated, date-stamped actions, always append.

**Logging a batch send.** When Shaw says "sent all" (or reports a batch), for every row that went out set:
- **Last Contact** = send date.
- **Notes** = the ask, using the campaign's own step name — `Ask sent (M/D).` Append replies (`Replied, bringing a friend (7/13).`). Channel lives in the `Medium` column, not Notes; add `via LinkedIn DM` / `via text` in Notes only when one batch mixes channels and it's worth disambiguating.
- **Next Contact** = the FU1 date, set **uniformly across the whole batch** so they surface together in the CRM sweep. **Read the FU date off the campaign's Promo Calendar** (it already schedules FU1/FU2) rather than inventing one.

**One date field on the tracker; mirror later touches, don't add columns.** The tracker holds a single `Next Contact` (the FU1 flag) — resist adding a second date column for FU2 and beyond. Later follow-ups live as dated pages on the campaign's Promo Calendar, and each should also be **mirrored into an ABA task** (`⭕` icon, body = a `<mention-page>` link back to the campaign page) so it actually surfaces in Shaw's daily briefing — Promo Calendar pages don't feed the briefing on their own. See `notion-helper` for the mirror mechanics.

**Draft, never send.** Shaw sends himself and reports back; your job is to prepare Gmail drafts (`create_draft`), then log once he confirms. `create_draft` can't edit an existing draft, so **draft ONE, let Shaw edit it, diff his version, then apply the diff to the rest of the batch** — don't mass-create before he's reviewed one, or a formatting bug multiplies across every draft.

**Notion bulk-update reality.** The Notion collection API rate-limits hard during batch logging — do ~9–11 property updates per message and expect 429s that need 30–200s waits.

**Status review:** fetch all entries and summarize as:

```
**Replies received:**
- [Name] — [brief context]

**Awaiting response:**
- [Name], [Name], [Name]...

**Next steps:**
- [Follow-ups due or next segments to activate]
```

Cross-reference Gmail when Shaw asks for updates — search each contact's email for new replies not yet logged, then update the tracker.

**Already-handled activity — check before you draft.** When Shaw says people "replied," his first move is often to answer them live himself. Before drafting a reply, read the actual thread (the LinkedIn DM, or Gmail) to see whether he's already responded. When he has, the deliverable is *logging the exchange* (advance Status — `Replied` / `Registered` / `Share Ask Sent` — and append a Notes line), not a duplicate draft. Reading the thread also tells you what they actually said, which is what makes the log accurate (e.g. "signed up" → Registered; "already doing that, no register" → Replied only).

**Draft replies from the campaign's own templates, not from scratch — even when the reply doesn't fit cleanly.** The campaign page has a reply script for each branch (`No`, `Soft No`, `Registered`, etc.); map the incoming message to the nearest one and run it as the base. A decline that carries a *counter-ask* (they pass but pitch their own thing, propose a swap, offer to help) still runs the `No` template as written, then hinges the closing support-offer line ("any way I can support you") into the counter-ask. Reserve bespoke copy for when no template is close — a fully custom draft is the exception, not the reflex.

**Confirming registrations (event campaigns).** The authoritative "who registered" source is the event's own guest list, not the tracker or Gmail — pull it, match to tracker rows by name tokens, and mark only those not already registered, predrafting the campaign's "Registered" share-ask (the repost ask if `Has Following?` = Yes, the "who else do you know" variation if No; rotate the No-Following variation across rows). Luma-specific pull mechanics — the `?fs=approved` Going filter, getting the `evt-…` id via Manage, and the virtualized-list harvest — live in `references/luma-guest-list.md`; the reconcile-and-advance logic is part of the sync loop in `references/outreach-sync.md`.

---

## Campaign variant: repost / amplification asks (lead getters)

Some campaigns don't ask the prospect to *do* the thing (register, book a call) — they ask a well-connected contact to **amplify** it, i.e. reshare a specific live post. Run these as their own mini-campaign, not as the register funnel's tail:

- **It lives in its own tracker + scripts hub — go there directly.** The lead-getter list is a standalone Notion database with its own DM-scripts page (Ask/FU1/FU2), parallel to and *not* a segment of the campaign's main register-funnel Outreach Tracker. When asked to follow up or sync the lead getters, find that dedicated tracker/hub (search the workspace for "Lead Getters Tracker" / "DM Lead Getters") — the main tracker's segments won't contain them.
- **The ask points at a live artifact.** The CTA is a reshare of a specific post, so confirm that post is actually published before sending — if it isn't live yet, hold the asks until it is.
- **Its own funnel: Asked → Replied → Shared → No.** The tracker's Status options already carry `Shared` and `No`; a lead-getter tracker needs nothing more than Name, LinkedIn, Status, Medium, and a single date field.
- **Warmest-first, and let warmth collapse the message.** For a contact who already reshared unprompted or whom Shaw just saw in person, skip the value pitch entirely — a short, warm opener plus the link ("great seeing you at X — here's another post if you're open to sharing") outperforms the full ask. Reserve the fuller "here's what the workshop is / your audience would value it" ask for colder names.
- **An amplifier who already said yes but hasn't shared gets a warm check-in, not the cold "last nudge."** The FU2 "last nudge" template assumes no reply; for someone who already agreed, adapt it to acknowledge the yes ("still up for it? no pressure") so you don't re-pitch someone who's already on board. Note the adaptation in the row's italic annotation so Shaw can revert to the verbatim template if he prefers.
- **Verify the actual repost on the post before nudging, not the DM thread.** A reshare shows on the post's activity, not in the DM conversation, so the tracker can lag reality — glance at the post's reshares before sending a nudge to avoid chasing someone who already shared.

---

## Campaign variant: post-event attendee follow-up

After an event the attendee list *is* the lead list — but it has to be built before it can be worked. Process and policy live in the **Post Event** SOP (`sop-helper`); the mechanics live in `references/event-attendance-reconciliation.md`. Read that file before touching a Zoom export.

- **Attendance comes from the Zoom participant log, not Luma.** Luma's `has_joined_event` is wrong in both directions.
- **The Zoom export usually has no emails** — guests join unauthenticated — so every attendee is matched to a registrant by display name. Budget for it; roughly a third need manual review, and dedupe on the matched registrant rather than the display name.
- **`utm_source` attributes the click, not the relationship.** The tag travels on forwards; the campaign's own Outreach Tracker is ground truth for who was personally invited.
- **Segment on engagement, and prefer *when* someone left over *how long* they stayed** — duration ranks late joiners backwards. Segment definitions are per-event; agree them with Shaw rather than reusing the last event's.
- **Some attendees are unidentifiable.** Count them in total attendance, exclude them from breakdowns, list them explicitly, and don't chase them.

---

## Relationship to other skills

- **CRM skill** — owns Notes format and pipeline-level lead management, including the promotion process. When an outreach contact graduates (books a call, asks about pricing), add them to the CRM and follow the CRM skill's "Promotion to main CRM" rule — the tracker entry becomes a historical breadcrumb (`Added to CRM` status, `Next Contact` cleared) while the main CRM owns ongoing touchpoints.
- **email-helper** — owns Shaw's voice, Gmail mechanics, reply/intro/decline templates.
- **conversion-copy** — owns message craft for conversion-focused copy. `channel-outreach.md` specifically covers cold-outreach DMs.
- **notion-helper** — adjacent; owns ad-hoc Notion creation outside structured campaigns.
