---
name: outreach
description: >
  Run 1:1 outreach campaigns end-to-end — sourcing the list, enriching it, triaging into segments,
  setting up a Notion tracker, drafting templates, sending, and logging responses. Use this skill
  whenever Shaw is building a list of people to reach out to, setting up outreach tracking, or
  crafting the messages themselves. Triggers include: "find people on LinkedIn", "pull my connections",
  "build a lead list", "enrich this CSV", "look up where these people work", "get company sizes",
  "set up outreach", "create an outreach table", "add people to the outreach list", "who have I
  reached out to", "update outreach", "write me an outreach message", "draft a DM template", or any
  time Shaw shares a batch of names he's reaching out to. Also casual phrasing like "check my LinkedIn
  for analytics people", "I texted these 5 people", "add them to the list", "what should I say to
  these people". Covers workshops, events, research calls, partnerships, and any 1:1 outreach initiative.
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

- **Deduplicate enrichment targets.** If 5 people work at Toyota, look up Toyota's size once.
- **Extract before searching.** Titles often contain companies ("PM at Figma"). Parse these before any web search.
- **Batch web searches** into parallel Haiku agents (~10 per agent), or a Workflow with structured output (agents read the lead file by index range and return validated rows — cleaner aggregation).
- **Chrome is last resort** — sequential and rate-limited. Reserve for the smallest possible set of unresolved unknowns.
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
| [Person] | [linkedin-url] | Already reached out, not interested |
| [Person] | [linkedin-url] | Already have a contact at [Company] |

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

### 4. Triage into segments

Deduplicate by LinkedIn URL (or email, or whatever's unique). Then group by segment.

Segments are how Shaw prioritizes the list. The scheme varies by campaign:
- **Relationship proximity:** met in person → met virtually → have their email
- **Seniority × location:** DFW leaders → DFW managers → DFW ICs → non-DFW leaders → ...
- **Channel:** existing DMs → LinkedIn-only → cold email

Apply `disqualified.md` as part of triage. Present the triaged list to Shaw as a manual checkpoint before any further enrichment or tracker setup.

### 5. Set up the tracker

Once the list is confirmed, build the Notion tracker → see **`tracker-setup.md`** for the inline-database schema, segment legend, and page placement.

### 6. Draft templates

Each campaign needs templates — typically one per segment, sometimes per channel (text / email / LinkedIn DM). Start with the **warmest segment first** to establish the core pitch, then adapt outward. Draft one at a time so Shaw can react and steer before the next.

Save finalized templates to the campaign page in code blocks for easy copy-paste.

For writing craft specifically:
- **Voice, tone, email mechanics (HTML, Gmail threading)** → defer to **email-helper**
- **Message craft — hooks, CTAs, personalization, reply friction** → defer to **conversion-copy** (specifically `channel-outreach.md`)

This skill owns the operational side (who, when, which segment); message skills own the words.

### 7. Send, log, review

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

---

## Relationship to other skills

- **CRM skill** — owns Notes format and pipeline-level lead management, including the promotion process. When an outreach contact graduates (books a call, asks about pricing), add them to the CRM and follow the CRM skill's "Promotion to main CRM" rule — the tracker entry becomes a historical breadcrumb (`Added to CRM` status, `Next Contact` cleared) while the main CRM owns ongoing touchpoints.
- **email-helper** — owns Shaw's voice, Gmail mechanics, reply/intro/decline templates.
- **conversion-copy** — owns message craft for conversion-focused copy. `channel-outreach.md` specifically covers cold-outreach DMs.
- **notion-helper** — adjacent; owns ad-hoc Notion creation outside structured campaigns.
