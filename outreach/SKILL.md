---
name: "outreach"
description: "Run 1:1 outreach campaigns end-to-end — sourcing the list, enriching it, triaging into segments, setting up a Notion tracker, drafting templates, sending, and logging responses. Use this skill whenever Shaw is building a list of people to reach out to, setting up outreach tracking, or crafting the messages themselves. Triggers include: \"find people on LinkedIn\", \"pull my connections\", \"build a lead list\", \"enrich this CSV\", \"get company sizes\", \"clean a Sales Nav lead list\", \"set up outreach\", \"create an outreach table\", \"add people to the outreach list\", \"who have I reached out to\", \"update outreach\", \"sync the outreach\", \"who registered\", \"write me an outreach message\", \"draft a DM template\", or any time Shaw shares a batch of names he's reaching out to. Also casual phrasing like \"check my LinkedIn for analytics people\", \"I texted these 5 people\", \"what should I say to these people\". Covers workshops, events, research calls, partnerships, reshare asks (lead getters), and any 1:1 outreach initiative.\n"
---

# Outreach

This skill runs Shaw's outreach campaigns end-to-end. Two halves of the same workflow: **build the list**, then **work the list**. A campaign is a coherent outreach push with a clear audience and goal — a workshop, an event, a research-call batch, a partnership push.

## Which file for which ask

The folders follow the phases of the flow below. **Find the row for the ask and read that file before loading any tool** — it names the source, the browser, and the mechanics; this file carries the principles that apply across all of them.

| The ask | Read |
|---|---|
| Planning a campaign, choosing channels, "where should leads come from" | `strategy/acquisition-playbook.md` |
| Sourcing from Shaw's LinkedIn network by role or title | `sourcing/linkedin-search.md` |
| Sourcing from a **Sales Navigator search** — filters, keywords, pulling the results | `sales-navigator/search.md` |
| A saved **Sales Navigator** lead list — extracting it, parsing rows, getting public profile URLs, creating or updating one | `sales-navigator/lead-lists.md` (+ `sales-navigator/api-access.md` for browser and API plumbing) |
| Auditing a Sales Nav list against the headcount band, or any company-level criterion | `sales-navigator/headcount.md` |
| Sending connection requests to a Sales Nav list | `sales-navigator/connecting.md` |
| Who accepted a connection request from a Sales Nav list | `sales-navigator/accepts.md` |
| Adding company / size to a list; resolving unknowns; sizing the company someone actually leads | `enrichment/company-size.md` (+ `enrichment/batch-agent-prompt.md` for the bulk pass, `enrichment/size-ranges.md` for the buckets) |
| Building the Notion tracker and campaign page | `campaign/tracker-setup.md` |
| Per-row scripts, email-vs-DM formats, follow-up templates, Gmail drafts | `campaign/per-prospect-scripting.md` |
| Syncing a live campaign — replies, registrations, "move it forward" | `sync/outreach-sync.md` |
| Reviewing a DM campaign's numbers | `sync/linkedin-benchmarks.md` |
| Setting up or cloning a Luma event page | `events/luma-page-setup.md` |
| Who registered for a Luma event | `events/luma-guest-list.md` |
| Post-event attendee follow-up from a Zoom export | `events/event-attendance-reconciliation.md` |

## Browser policy

Two browsers are available and the choice is per task, not a default: the **built-in browser** for Sales Navigator work (each read returns the page title with the data, so a mis-navigation is self-evident rather than silently mislabeled, and its DOM reads stay current where the extension's screenshots lag and its batch calls time out); the **Chrome extension** for LinkedIn search sourcing, profile lookups, and DM sweeps, where Shaw's signed-in session lives. **That split assumes Claude Desktop, whose built-in browser is signed in. In Claude Code the built-in browser is Playwright and is NOT signed into LinkedIn — it redirects to `/sales/login` and returns an empty DOM rather than an error — so every LinkedIn task there, Sales Navigator included, runs in the Chrome extension** (`sales-navigator/api-access.md`, Browser). This is a standing instruction and overrides the app's preferred-browser default. Whichever browser: **one tab, sequentially**. Concurrent tabs have tripped LinkedIn's rate limiting, and parallel agents against the extension crash it (it serves one connection) — parallelism is for web-search agents only. A single sequential agent reliably finishes 10–18 lookups; chain batches of ~15.

## The tracker's fields are CRM-owned

The tracker's `Last Contact`, `Next Contact`, `Status`, and `Notes` are CRM-owned: outreach decides who's in the campaign and which step they're on, `crm` defines what the fields mean and how far out dates go. Read `crm/references/follow-up-guidance.md` before writing any of them, in any phase — not just at send-and-log.

## General principle: confirm before creating

Before committing to anything structural — a pipeline plan, a tracker schema, a segment scheme, a template direction — use the AskUserQuestion tool to present the plan and get Shaw's sign-off. Assumptions on shape are easy to get wrong and tedious to undo. A quick confirmation saves rework.

## Acquisition strategy layer

Before the pipeline comes the channel question. `strategy/acquisition-playbook.md` holds the strategy frames — the Core Four channel map, Dream 100 (borrowed audiences), owned-vs-rented traffic, and awareness-stage message matching. Read it when planning a new campaign, choosing channels, or diagnosing where leads should come from; it informs Kickoff alignment, not the run itself. For lead magnets, the canonical guidance is Shaw's Notion **Lead Magnet Guidance** page (linked from that file) — don't reinvent it.

## Pipeline design principles

Every campaign is a sequence of **(enrich → filter) cycles** using progressively more expensive tools on a shrinking candidate set. For any piece of information you need about a candidate, try these in order — only falling back to the next when the previous can't resolve:

```
1. Extract from data you already have (free)
2. Web search with cheap-tier agents in parallel (cheap)
3. Browser profile lookup (expensive)
4. Ask the user (most expensive)
```

This pattern is fractal:
- **Pipeline level:** the entire campaign is enrich → filter cycles, cheapest first
- **Stage level:** within "get company names," first extract from titles (free), then web search the remainder (cheap), then the browser for the unknowns (expensive)
- **Decision level:** within "should we include this person," first check automated criteria, then enriched data, then ask Shaw

### Kickoff alignment (do this FIRST, before any research)

The most important thing to lock at the start of every campaign — get explicit sign-off on all of it:

1. **The wide net.** What's the starting pool — who do we cast for and how (which source, which search terms)? This is the top of the funnel; agree on it before scraping a single name.
2. **The non-negotiables.** In most campaigns these are **role and company size** — the two axes that actually gate. Everything else (industry, AI-interest, location) is *scored/flexible*, not a hard cut. State the role bar (must own/lead or be budget-authority C-suite — decide explicitly whether hired C-suite counts, or founders/owners only) and the **size band** (e.g. 10–1,000 employees). LinkedIn carries two headcounts per company (declared range and member count) that disagree often; the standing rule is that a lead is in band if *either* one is — don't ask which measure to use (see `sales-navigator/headcount.md`, "Two headcounts").
3. **The anti-ICP.** Ask *"who looks like a fit but isn't actually a buyer?"* and write it down. This is easy to miss and expensive to discover late — last time the realization that "AI-native builders/teachers are peers, not customers" surfaced mid-run and inverted the entire ranking. Decide exclusions up front.
4. **The weights.** If scoring, set component weights now (role + size dominate; flexible factors weigh less). Don't let weighting emerge through iteration.
5. **Seed `disqualified.md` from the CRM — first.** Pull **Clients (Nurture)** and **Active Leads** from the Notion CRM and exclude anyone already a client or in the active pipeline *before* scoring or enriching them. Don't leave CRM dedup to the end.
6. **Sanity-check the channel.** Is the warm network even the right well? An audience-saturated network (e.g. an AI educator's connections are ~half AI builders) will surface mostly anti-ICP under role-based search. Sourcing is often the binding constraint, not scoring — consider adopter/industry-oriented terms with the peer-exclusion baked in, or a different source entirely.

Then classify each criterion by evaluation cost (free / cheap / expensive / manual), sequence cheapest first, and present the pipeline to Shaw before starting.

### A sourced row is a position, not a person

Every attribute derived from a sourced row — employer, headcount, industry,
seniority, tenure — belongs to whichever *position* matched the filter, and
people list many at once. Picking the position that best fits the avatar is
the wrong instinct: the on-avatar-sounding one is usually the volunteer seat,
the fractional engagement or the side LLC, because that is where the
impressive title goes. Resolve the **primary** position first, and treat the
row's company as a claim — headcount especially, which has to be resolved on
the employer rather than on whatever page the position pointed at, or umbrella
and product pages report a fraction of the real organization. The position's
own description also settles what a title means in its industry, which a
keyword cannot: "Technical Director" runs a camera in broadcast and a
formulation lab in chemicals.

**Run the anti-ICP as a filter step, not just a kickoff decision.** Vendors,
agencies, consultancies and firms selling what the offer teaches are cheap to
identify and expensive to discover late, and they cluster densely enough to
dominate a list that never checked. A company's own LinkedIn `description`
usually settles operator-versus-vendor in one call — spend it on every company
before the list ships.

### Filtering discipline (when to cut vs. keep)

- **Cut early only on cheap + unambiguous signals.** If role or size is unmistakable from the headline alone — an obvious solopreneur/freelancer/one-person shop, an obvious employee at a mega-corp, a clear non-buyer (IC, student, ex/aspiring founder) — drop them at the free stage; there's no value enriching them.
- **Keep everything ambiguous or unknown → enrich → filter on facts.** A fuzzy headline, a title that could be founder-or-staff, or a *missing* value is NOT grounds for cutting. Carry them through enrichment and disqualify only once you have the data.
- **Never filter on a field until it's fully populated.** A missing company size is not "out of band" — it's unknown. Resolve it for everyone (web → browser) before applying any size cut. Err toward keeping the unknown until disqualified by real data.
- **A deferred cut is still a cut.** When Shaw parks a filter decision for a later phase ("add them all, filter at send time"), resurface it at that phase with the candidates named — inheriting the deferral silently as "everyone" skips a decision he explicitly kept.

### Scoring & gating (for larger lists)

When a list is big enough to rank rather than hand-pick:

- **Score, don't prematurely disqualify.** Give each prospect a score from weighted components (e.g. role + size + fit). Soft criteria move the score; they don't eliminate.
- **Gate the *expensive* step on the *cheap* score.** Run the costly enrichment/inspection only on candidates already scoring well on the free/cheap dimensions — so you never spend browser time or per-profile lookups on someone who's clearly off-avatar.
- Set weights at requirements time (see Kickoff alignment). Role + size are the non-negotiable axes; flexible factors are scored but never the sole gate.

### Enrichment efficiency

- **Deduplicate enrichment targets.** If 5 people work at [Company], look up [Company]'s size once.
- **Extract before searching.** Titles often contain companies ("PM at Figma"). Parse these before any web search.
- **Batch web searches** into parallel Haiku agents (~10 per agent), or a Workflow with structured output (agents read the lead file by index range and return validated rows — cleaner aggregation).
- **The browser is last resort** — sequential and rate-limited (see Browser policy above). Reserve it for the smallest possible set of unresolved unknowns.
- **Finish the field before filtering on it.** When a filter depends on company size, run web search *then* a browser cleanup pass on every remaining "unknown" — get to zero unknowns before any size cut. A second web pass is not a substitute for the browser pass.
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

LinkedIn is the default source for cold/warm prospect lists → **`sourcing/linkedin-search.md`** (Chrome extension).
For a saved **Sales Navigator lead list** — extracting it, validating headcount, sending connection requests — the `sales-navigator/` folder (built-in browser on Desktop, Chrome extension in Claude Code — see Browser policy): **`sales-navigator/lead-lists.md`** to get the rows out, **`headcount.md`** to validate the band, **`connecting.md`** to work it, **`accepts.md`** to see who connected.

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

Enrichment runs between sourcing and triage when a filter depends on data you don't have yet. The most common case is company size — see **`enrichment/company-size.md`** for the decision tree (1–9 contacts → browser direct; 10+ → parallel web-search agents + browser cleanup).

**Resolve the field fully before filtering on it.** For company size: web-search pass, then browser cleanup on every "unknown" until none remain — *then* apply the size band. A missing value is not out-of-band; keep unknowns until real data disqualifies them. And validate **coherence** — the company you sized must be the one they own/lead, not an employer or client (see `enrichment/company-size.md`).

Other enrichments follow the same pattern: extract → web search → browser → ask.

**Verify a criterion against the source that defines it.** When a filter was applied by a platform against its own data, re-check it *in that platform*, not in a proxy. Aggregators (Crunchbase, ZoomInfo, PitchBook) measure different populations on different refresh cycles, so a disagreement tells you the two sources differ — not that the filter failed — and their coarse buckets (`101-250`) can't adjudicate a boundary at 200 anyway. Reach for them only where the defining source has no record, and label what comes back as a different measurement. The cheap proxy is only cheap when it answers the same question.

#### Warmth enrichment (before segmenting a warm-network campaign)

For any campaign that segments by relationship proximity, the segment assignment is only as good as the relationship data behind it. Don't guess warmth from headlines — pull it from the actual record:

- **DM-history sweep (LinkedIn).** For each prospect, read the existing DM thread and classify: `they_reached_out` / `replied` (Shaw initiated, they responded) / `ghosted` (Shaw messaged, no reply) / `never_messaged`. This directly drives segment and send-order, surfaces ready-made openers ("great connecting at X", "congrats on the new role"), and flags who to send *last* (prior ghosts). Run it as one sequential agent in the Chrome extension over ~15 names per batch (Browser policy above), read-only — never touch a compose box.
- **Cross-check Kit cohort tags.** Query Kit for ABB/cohort tags (`list_tags` → `list_subscribers_for_tag`, match by email/first name) to catch alumni the LinkedIn data won't show. Alumni are the warmest segment (paying past customers) and their alum status overrides soft exclusions — e.g. an ABB alum who'd otherwise be cut as "too technical" stays in. Log that override as a principle in `disqualified.md`.
- **Met-in-person is Shaw's knowledge.** DM history and tags won't reveal in-person meetings — ask Shaw, and re-segment when he says "I've met X."

#### Reusing a prior campaign's shortlist as a source

A recent same-ICP campaign's `FINAL_shortlist` is often the cheapest well for a new one — but **treat it as stale, not verified**. People change jobs and the original scrape had coherence errors, so re-verify role / company / size / location before loading (a fresh parallel web-search pass catches out-of-band sizes, job changes, and scrambled company↔person data). Also re-check inherited enrichment: a prior campaign's `geo` field mislabeled US people as non-US last time — verify geo from the headline/company rather than trusting the inherited value.

#### LinkedIn scraping gotchas

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

Once the list is confirmed, build the Notion tracker → see **`campaign/tracker-setup.md`** for the inline-database schema, segment legend, and page placement.

### 6. Draft the scripts

A campaign has a **base script** — usually one core message with a `{Personalization}` **menu** of numbered opener options (e.g. 1 = "it's been a while", 2 = "great catching up at X", 3 = "congrats on the new role", 4 = "this seemed relevant"). Draft the base warmest-segment-first, one at a time, so Shaw can steer.

Then produce a **per-prospect script for every row** — this is the real deliverable, not just one template per segment:
- Read the prospect's page-body **Context** and their live DM/text thread, pick the **single best-fit menu option verbatim**, and drop the finished script into that row's page body. Shaw fills the specifics (the literal "X", any tweaks) himself — do NOT reword the opener he's going to edit.
- Keep it in a **`plain text` code block** for copy-paste. Don't un-fence it to rich text (Shaw reverts that).
- Add a one-line italic note above the block recording which option and why.

The details — how the thread picks the opener, the **email-vs-DM format split**, the `Medium` column, subject-line register, email-address sourcing, and Gmail draft mechanics — live in **`campaign/per-prospect-scripting.md`**. Read it before scripting a mixed-channel campaign.

**Shaw's DM register — voice lives here, not in the message skills.** Campaign DMs and every later rung sound like Shaw texting, not like structured conversion copy: about 3 short lines; no-oriented asks ("Opposed to…?"); assertion over hedging ("this is NOT a sales call" beats "no pitch, I promise"); one warm give to close (a P.S., an emoticon) so the message ends by offering rather than defending. Draft any new rung — a follow-up, a variant, a rung the campaign didn't plan — from the campaign's existing scripts' register. `conversion-copy` still supplies general conversion principles and structure, but once a thread exists, a message that breaks register reads as a different (automated) sender.

For writing craft specifically:
- **Voice, tone, email mechanics (HTML `<div>` spacing, Gmail threading)** → defer to **email-helper**
- **Message craft — hooks, CTAs, personalization, subject register, reply friction** → defer to **conversion-copy** for principles and structure (specifically `channel-outreach.md`, which carries named playbooks — the bespoke advice-frame play and the high-volume Uptown method — with a chooser for which fits the campaign); DM voice and register are governed here
- **Follow-up ladder — proof carried into the first nudge, no re-dropped in-thread links, progressively terser rungs** → defer to **conversion-copy** (`channel-outreach.md`, Follow-ups)

This skill owns the operational side (who, when, which segment, which channel) and Shaw's DM voice; message skills own conversion principles and structure.

### 7. Send, log, review

**Syncing a live campaign.** When Shaw asks to check for replies, reconcile registrations, or "move the outreach forward," you're running a *sync*: sweep every reply channel and the conversion source, then advance each contact one step along the campaign's own funnel. The campaign's shape — its funnel stages, its channels, its scripts — is defined by the tracker's Status/Medium options and the page scripts, not hardcoded, so read it before acting. Full sweep→classify→advance loop: `sync/outreach-sync.md`.

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

**Logging a batch send.** When Shaw says "sent all" (or reports a batch), read the sent messages before writing anything down. A batch of per-row variants is assembled by hand, so what went out is not guaranteed to be what was drafted, and the log inherits any mismatch — the row records a variant nobody received, and the next rung gets drafted from it. One pass over the inbox settles both questions at once: that the batch went, and which version each person got. Then for every row that went out set:
- **Last Contact** = send date.
- **Notes** = the ask, using the campaign's own step name — `Ask sent (M/D).` Append replies (`Replied, bringing a friend (7/13).`). Channel lives in the `Medium` column, not Notes; add `via LinkedIn DM` / `via text` in Notes only when one batch mixes channels and it's worth disambiguating.
- **Next Contact** = the date of the next planned touchpoint. **Defer to the CRM skill**, which owns this field's semantics and cadence defaults (`crm/references/follow-up-guidance.md`). It is not an FU1 flag: it's a rolling pointer that advances as the sequence progresses, holding FU1 today, FU2 once FU1 goes out, a booked call date, or a re-engagement date. **Read campaign-wide FU dates off the Promo Calendar** rather than inventing them, and set the date uniformly across everyone who got *the same ask* — a single day's send often mixes several scripts, and the batch for follow-up purposes is the ask, not the send date.
- **An accept schedules the DM — `Next Contact` = the next day.** When someone
accepts a connection request (or otherwise opens the door without being written to
yet), Msg 1 goes out tomorrow, so set the date the moment the accept is logged. This
is the one case where `Next Contact` is set before anything has been sent: elsewhere
it points at a follow-up to a message already out, here it points at the first one.
Skip it and the row carries a `Status` and no date, which the CRM sweep
(`Next Contact <= today`) never surfaces — the warmest lead in the campaign goes cold
in a view nobody reads. Applies only until Msg 1 actually goes out; after that the
cadence owns the field. Sales Nav mechanics: `sales-navigator/accepts.md`.
- **Whether someone gets a date at all is a judgment call, and blank is a legitimate answer.** Per the CRM skill, a blank `Next Contact` is assumed intentional and is never backfilled. Ask what a follow-up would actually say: an ask with something to say yes to (a call, a coffee chat, a favour) earns a nudge, because silence means "not yet." A message that sorts people — a reply-with-a-letter diagnostic, a multiple-choice qualifier — is self-sorting, and nudging just asks the same question twice. Which asks earn a follow-up varies by campaign; confirm the split with Shaw when a batch mixes both.

**The row body carries no send state.** Log the send in the properties above and leave the body's
rung headings alone — `## M3`, never `## M3 — due 9/15, drafted (not sent)`. Which rungs went out
is already in `Notes` and `Last Contact`, and a body that also claims it has to be kept in sync by
hand forever. It won't be: in the Sep 2026 tracker roughly 75 of 106 worked rows still read
"drafted (not sent)" for messages sent days earlier, because logging updates properties and
nothing updates the body. That isn't cosmetic — `sync/outreach-sync.md` counts the unsent backlog
off that exact phrase, so stale headings inflate the backlog and depress the campaign page's
funnel numbers.

Two things the body owes in exchange: when the sent wording differed from the draft, replace the
block with what actually went out (the body is then the only record of it, since `Notes` holds
dates and not text); and delete a draft the send superseded — a never-to-be-sent M2 sitting under
a reply is noise that the next drafting pass will read as live.

**The tracker's date and notes fields are CRM-owned** — outreach *sets* them, the CRM skill *defines* them. Where this file and the CRM skill disagree about what a field means, the CRM skill wins.

**One date field on the tracker; mirror later touches, don't add columns.** The tracker holds a single `Next Contact` — resist adding a second date column for FU2 and beyond. The field *advances*: when FU1 goes out it moves to the FU2 date rather than needing a new column. The Promo Calendar holds the campaign-wide schedule of FU rounds; `Next Contact` points at whichever one is next for that person. Each scheduled round should also be **mirrored into an ABA task** (`✉️` icon — it's an email send, body = a `<mention-page>` link back to the campaign page) so it actually surfaces in Shaw's daily briefing — Promo Calendar pages don't feed the briefing on their own. See `notion-helper` for the mirror mechanics.

**Draft, never send.** Shaw sends himself and reports back; your job is to prepare Gmail drafts (`create_draft`), then log once he confirms. `create_draft` can't edit an existing draft, so **draft ONE, let Shaw edit it, diff his version, then apply the diff to the rest of the batch** — don't mass-create before he's reviewed one. The review catches what your own verification structurally cannot: re-reading your drafts confirms they match your intent, never that your intent was right. A wrong subject line, a stale script, or the wrong segment's opener survives every self-check you can run and dies the instant Shaw opens draft #1.

**Notion bulk updates rate-limit.** Pace batch logging per `notion-helper`, which owns connector mechanics.

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

**Benchmarking campaign health.** For high-volume LinkedIn DM campaigns, compare the funnel (acceptance → reply → positive → meeting) against `sync/linkedin-benchmarks.md` during status reviews — it includes the diagnostic logic for which stage to fix when a number is off. The benchmarks are external (Uptown's) until Shaw's own campaign data replaces them.

**Already-handled activity — check before you draft.** When Shaw says people "replied," his first move is often to answer them live himself. Before drafting a reply, read the actual thread (the LinkedIn DM, or Gmail) to see whether he's already responded. When he has, the deliverable is *logging the exchange* (advance Status — `Replied` / `Registered` / `Share Ask Sent` — and append a Notes line), not a duplicate draft. Reading the thread also tells you what they actually said, which is what makes the log accurate (e.g. "signed up" → Registered; "already doing that, no register" → Replied only).

**Draft replies from the campaign's own templates, not from scratch — even when the reply doesn't fit cleanly.** The campaign page has a reply script for each branch (`No`, `Soft No`, `Registered`, etc.); map the incoming message to the nearest one and run it as the base. A decline that carries a *counter-ask* (they pass but pitch their own thing, propose a swap, offer to help) still runs the `No` template as written, then hinges the closing support-offer line ("any way I can support you") into the counter-ask. Reserve bespoke copy for when no template is close — a fully custom draft is the exception, not the reflex.

**Confirming registrations (event campaigns).** The authoritative "who registered" source is the event's own guest list, not the tracker or Gmail — pull it, reconcile against the tracker, and mark only those not already registered, predrafting the campaign's "Registered" share-ask (the repost ask if `Has Following?` = Yes, the "who else do you know" variation if No; rotate the No-Following variation across rows). Luma pull mechanics: `events/luma-guest-list.md`; the reconcile-and-advance logic is part of `sync/outreach-sync.md`.

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

After an event the attendee list *is* the lead list — but it has to be built before it can be worked. Process and policy live in the **Post Event** SOP (`sop-helper`); the mechanics live in `events/event-attendance-reconciliation.md`. Read that file before touching a Zoom export.

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
- **notion-helper** — adjacent; owns ad-hoc Notion creation outside structured campaigns, the connector mechanics this file defers to, and the standard for **what a page body may contain** ("Writing page bodies"). Read it before writing any row body, not only when a connector call misbehaves.
