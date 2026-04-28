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

### Designing the pipeline at requirements time

Before any research begins:

1. Capture all filter criteria (title keywords, company size, location, seniority, exclusions)
2. Seed `disqualified.md` with known exclusions and disqualification principles
3. Classify each criterion by evaluation cost (free / cheap / expensive / manual)
4. Sequence stages cheapest first so each one shrinks the list before the next runs
5. Present the pipeline to Shaw before starting

### Enrichment efficiency

- **Deduplicate enrichment targets.** If 5 people work at Toyota, look up Toyota's size once.
- **Extract before searching.** Titles often contain companies ("PM at Figma"). Parse these before any web search.
- **Batch web searches** into parallel Haiku agents (~10 per agent).
- **Chrome is last resort** — sequential and rate-limited. Reserve for the smallest possible set of unresolved unknowns.

### Manual checkpoints

Place checkpoints **after automated filters have narrowed the list but before expensive enrichment**. Don't ask Shaw to review raw/unfiltered lists, and don't wait until the end for feedback — by then enrichment on cut candidates is already wasted. Shaw adds soft exclusions that no automation can know.

## Disqualification tracking (`disqualified.md`)

A living document created at campaign start and updated throughout the run. Its primary job is **intra-campaign efficiency**: when Shaw gives feedback mid-pipeline ("[Person]'s off the table"), it goes into `disqualified.md` immediately and applies to all remaining candidates — preventing wasted enrichment on people already cut.

Two sections:

**1. Disqualification principles** — general rules applied automatically at every stage:
- "Only one person per company per job level"
- "No one at companies < 50 or > 5000 employees"
- "Exclude anyone already in the Expert Calls DB"

Checked before any enrichment step. If a principle disqualifies someone, skip the enrichment.

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

Before touching any source, nail down:
- **Campaign context:** what's it for (workshop, event, research calls, partnerships)
- **Target profile:** role keywords, seniority preference, location priority, company size range, industry
- **Volume needed:** how many final leads? Work backward assuming ~80% attrition through filters.
- **Channels:** LinkedIn DM, email, text, mix
- **Segments:** how will you group outreach (warmest first)? Common patterns: relationship proximity (in-person / virtual call / email-only), seniority × location, channel.
- **Exclusions:** prior outreach, specific companies, geographic cuts

Then design the pipeline per the principles above — classify criteria by cost, sequence cheapest first. Seed `disqualified.md`. Present the plan to Shaw before executing.

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
- **Voice, tone, email mechanics (HTML, Gmail threading)** → defer to **email-writer**
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

- **CRM skill** — owns Notes format. Also owns pipeline-level lead management. If an outreach contact graduates (books a call, asks about pricing), add them to the CRM. Outreach tracker is campaign-level; CRM is pipeline-level. A person can exist in both.
- **email-writer** — owns Shaw's voice, Gmail mechanics, reply/intro/decline templates.
- **conversion-copy** — owns message craft for conversion-focused copy. `channel-outreach.md` specifically covers cold-outreach DMs.
- **notion-helper** — adjacent; owns ad-hoc Notion creation outside structured campaigns.
