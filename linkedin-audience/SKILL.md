---
name: "linkedin-audience"
description: Weekly ICP sweep of Shaw's LinkedIn audience. Pull everyone who reacted, commented, voted, followed, viewed his profile, newly connected in a window, or sent a pending invite, qualify them against the ABA ICP page in Notion using LinkedIn's own data (current role, company headcount, HQ country, connection degree — no Apollo), and return two tables in chat — Tier 1 people at companies that match the ICP and Tier 2 people at adjacent companies, each row marked DM or Connect — plus which of the week's new connections are worth a DM. Use whenever Shaw asks who in his audience fits the ICP, "run the sweep", "any prospects this week", "who showed up that I should connect with", "who's worth following up with from LinkedIn", "any interesting new connections", "look at my connection requests", or when the LinkedIn sales motion page needs its weekly list. Do NOT use for post performance metrics or reach analysis (linkedin-post-analytics), and do not produce audience lists, cross-channel breakdowns, or dashboards.
---

# LinkedIn audience — the weekly ICP sweep

One job: turn a week of LinkedIn activity into a short list of people worth contacting. Everything in the pipeline exists to feed that list; anything that doesn't feed it is not part of the deliverable.

**Requires Chrome tools** (Claude in Chrome): `navigate`, `javascript_tool`, and `computer` for the one page that still needs real scrolling.

## Run it through subagents

The sweep is two kinds of work: hundreds of mechanical calls (signal pulls, enrichment, inbox and Notion lookups) and a few minutes of judgment at the end (who is worth Shaw's time). Done in one context, the mechanical work fills it with tool output, and the judgment — the only part Shaw sees — gets made with what's left. So delegate the mechanical phases to subagents and keep the main thread for scoring and writing.

Each subagent gets a self-contained brief (which script, which tab, which localStorage keys to write) and returns a short summary — counts, completeness checks, anything that failed — never row dumps. The data stays in the browser's `__aba_*` keys, where the next phase reads it. Phases that touch different pages can run in parallel (the Notion context pull alongside the LinkedIn pulls); phases that drive the same tab run one after another. The main thread then reads only the filtered survivors and the in-motion context, and scores them.

## The deliverable

Two tables and one short list, in chat, nothing else:

**Tier 1 — ICP companies.** The company meets every company criterion on the ICP page.
**Tier 2 — adjacent companies.** The company misses one criterion: just outside the size band, or a neighbouring type or vertical.

The tiers describe the company, not the person. Who at the company counts is the page's call (see below); when it admits any role, role only orders the rows.

| Person | Role | Company | Size | Engaged | Next | Profile |
|---|---|---|---|---|---|---|

- *Role* is the current position title, not the headline.
- *Company* is the name plus a three-word description and the HQ city, e.g. "[Company] — litigation law firm ([City])". The description comes from the company's own tagline or About text, condensed.
- *Size* is LinkedIn's employee count for the company.
- *Engaged* is single words from {reacted, commented, voted, followed, viewed, connected, invited}, comma-separated if several. When someone engaged on more than one post, add the post count (`reacted ×6`), and list repeat engagers first within a tier — someone who keeps showing up across posts is a warmer lead than one reaction. Among equals, senior seats (founder, executive, whoever owns AI) go above individual contributors.
- *Next* is the move the degree allows: **DM** for 1st-degree, **Connect** for 2nd/3rd, **Accept + DM** for a pending invite. Group each tier's rows by it, Accept + DM and DMs first — the groups are different work (a message now vs. a request that has to be accepted first), and Shaw works them as separate batches.
- *Profile* is a link. Followers arrive as opaque `ACoAA…` member URNs rather than vanity slugs; they open fine.

If a tier is empty, say so in one line. Empty is a finding about the week, not a failure of the sweep.

**New connections worth a DM** — every person who connected this week is a live relationship in a way a reactor isn't (they just said yes to Shaw), so this section answers, for all of them, whether a DM is worth sending. One line each for those who are: what they do and why they're worth it — a non-buyer at a company outside the tiers, an investor or firm serving PE/VC portfolios (a route to portfolio intros), a likely referral or channel partner, someone at Anthropic. Then one line accounting for the rest by reason (already in a DM thread or in Notion, no current position, company far off the ICP), so Shaw can see the list was walked rather than skimmed. Anyone already in a tier table isn't repeated here.

## Read the ICP before scoring — the whole page

The ICP lives on the ABA ICP page in Notion (find it by title; it moves between quarters). Fetch the page in full with `notion-fetch` before scoring anyone. A search highlight is not the page: it truncates, and one sweep qualified against a snippet that had dropped "US-based" from the first line and produced four wrong rows. The page owns who qualifies, and this skill carries no criteria of its own: the size bounds and how soft their edges are, which verticals count and which are adjacent, and whether role gates at all are read from the page each run. The strategy behind the sweep changes by quarter — one aimed at closing buyers gates on the avatar seats the page defines, one aimed at building relationships admits anyone at the right company — and a criterion copied into this file would keep enforcing last quarter's strategy after the page has moved on. If the page is silent on something the sweep needs (a size tolerance, whether role matters), ask rather than assume the stricter reading.

## Pipeline

Order matters: cheap filters run before expensive ones, and the expensive step is the per-person enrichment.

Start each sweep by clearing the per-run `__aba_*` keys in localStorage — engagers, engagerPeople, voters, followers, connected, invites, enriched, dms. The scripts persist there so a run can resume after a tab drop, and they read it back on load, so a previous sweep's voters and enrichment records are still present and merge silently into this one's candidates. Keep `__aba_orgs`: it is a cache of company records, and reusing it across sweeps saves a call per employer.

### 1. Pull the seven raw signals

- **Reacted / commented** — `scripts/scrape-engagers.js`, run in batches of a few posts until `remaining` is 0 (a full window overruns the ~45-second tool limit, the same constraint as enrichment), over **every post in the analytics window** (the trailing 28 days the post-analytics report covers), not just the posts published this week. Reactions carry no timestamp, so the only way to see everyone who engaged is to walk each post's full list; restricting to this week's posts misses everyone who reacted this week to an older post, which is usually where the biggest posts' audiences are. The post list, with each post's `ugc` urn, comes from `linkedin-post-analytics/scripts/scrape-feed-api.js`; that skill owns the Voyager auth and the feed pull, so borrow rather than reimplement. Pass `ugc` through: a post whose counts are keyed by its ugcPost urn also serves its reactions and comments only under that urn. Per-post counts should match the numbers LinkedIn shows on each post. Strip Shaw's own replies.
- **Voted** — a poll's voters are not in its reactions or comments; LinkedIn shows them only to the author, in the poll's "N votes" dialog. `scripts/scrape-poll-voters.js` pages the endpoint behind that dialog, option by option, rather than scrolling it: the dialog stops loading the moment a page comes back short, and LinkedIn withholds the odd voter, so a 30-voter tab can freeze at 9 however far it is scrolled. A tab may come back one or two under its count for the same reason; a whole page missing means the pull is incomplete.
- **Followed** — `scripts/walk-followers.js` on the followers page. It pages the list newest-first and dates each person through the memberRelationship endpoint, stopping at the first connection older than the window. This replaces the old notification-feed join: nearly every follower who matters is a connection (connecting auto-follows), and the same call returns the degree the table needs.
- **Connected** — `scripts/recent-connections.js`. New 1st-degree connections with exact connection dates, from the endpoint behind the connections page (the page itself lazy-loads and won't page by script). Walk-followers only sees a connection if they still follow and stops at the first older connection it meets, so it isn't a complete record of who connected this week; this is.
- **Invited** — `scripts/pending-invites.js`. People who sent Shaw a connection request he hasn't answered. They reached out first, so they're the warmest strangers in the pool, but the queue is large and mostly far from the ICP — check each sender's own location against the sweep's geography before enriching anyone, since that one cheap lookup clears most of the backlog. Profile lookups are rate-limited; the script's header has the pacing.
- **Viewed** — `scripts/scrape-viewers.js` on the Premium profile-views page. The list virtualizes and ignores scripted scrolling, so drive real scrolls from the tool layer and harvest between them; stop when the oldest harvested row is past the window, not when the count stops moving. Private viewers surface as "Someone at X" and cannot be named — count them, don't chase them.

Followers, connections and viewers stay on the sweep's own window (the trailing 7 days); engagers and voters cover the analytics window; invites cover the whole pending backlog, since a request stays live until Shaw answers it. Union the seven into one candidate list, carrying every source a person appeared in. Profile id alone will not dedupe it: LinkedIn hands back two id forms for the same person — followers and connections arrive as opaque `ACoAA…` member URNs (so those two dedupe directly), engagers and viewers as vanity slugs — so anyone who both followed and viewed enters twice under different keys. The ids can't be reconciled before enrichment, so carry the duplicates through and merge on name plus current company once step 2 has resolved both, unioning their sources onto one row. Skip it and the same person appears twice in a Tier table, which overstates the week's yield and spends a contact twice.

### 2. Enrich from LinkedIn, in that order

`scripts/enrich-candidates.js`, run in batches of ~20 until `remaining` is 0 — javascript_tool times out around 45 seconds, and each person costs up to three calls. Per person: current position from `positionGroups`, company record (headcount, HQ, industries, tagline) from the organization endpoint, degree from `memberRelationship`. A headline pre-filter drops people with no employer to qualify — students, job-seekers, self-described freelancers — before any call is spent on them; anyone ambiguous goes through.

Positions, not headlines. A headline advertises a function and often names no employer; the current position names the company, and the company record gives the size. One sweep's standout follower by headline ("[Big Co] Partner | [Big Co] AI Transformation Lead") was, by position, founder of a two-person company. Current means open-ended: someone whose positions have all ended has no employer to qualify, however recent or impressive the last one was.

### 3. Filter, then score

`window.__inBand(min, max)` applies the criteria that need no judgment — US HQ, headcount inside the bounds — and hands back the survivors with everything the table needs. Pass the widest bounds the page allows, tolerance included, so a company just outside the core band survives to be scored as adjacent instead of vanishing here.

Score the survivors by reading, against the ICP page fetched before scoring: does the company match the type, vertical and core size band? All of them → Tier 1. One miss → Tier 2. More than one → out. A consultancy, agency or training shop that sells AI help is out on company type, however its people are titled, and so is anyone whose invite note is a pitch — a seller, not a lead; someone leading AI inside a qualifying company is in. Apply a role gate only if the page sets one.

The page states criteria; Shaw's Active Leads and Clients show what fit actually looks like. Read them before scoring, because the two drift apart — real deals have come through investor and referral chains, from companies headquartered abroad with a US presence, and above the page's size band. When a candidate resembles the pipeline but fails the page's letter, surface it with the reason rather than dropping it, and when they disagree in a way that keeps recurring, say so — the page is what should change. IT services shops, MSPs and dev shops are usually partners rather than buyers: route their people to the new-connections section as referral or channel contacts instead of out.

### 4. Drop anyone already in motion — last, by person and by company

Remove anyone Shaw is already working with, and anyone at a company he already has a relationship with. A colleague of a client, a lead, or a Friend isn't a cold find: the relationship runs through the person Shaw already knows, and opening a second thread around them crosses it. The sources:

- Notion: Clients, Active Leads, Friends, the Companies database they link to, and every campaign's Outreach Tracker — finished campaigns too, since everyone in them has already been contacted.
- LinkedIn DMs: `scripts/dm-inbox.js` lists every 1:1 conversation back to a cutoff. A DM Shaw sent this morning is in no Notion page.

This runs after scoring, on the short list, because the company match needs the company enrichment resolves, and because Shaw works fast — people get DM'd the same day they show up. Match people on name, loosely (trackers store Sales Navigator lead ids, which never equal profile ids, and names carry credentials and emoji, e.g. "[Person], M.Ed."), and match companies on name.

### 5. Write the tables

Straight from the survivors. A `connected` row is someone Shaw connected with this week, not someone who discovered him through a post — it changes how he'd open the DM, so the Engaged column should show it. The new-connections section covers every `connected` row not already in a tier table, plus the partner-type rows routed there in step 3.

## What not to do

Don't build an artifact or dashboard — the tables are read once and acted on. Don't shuttle the full candidate list out of the browser; javascript_tool truncates output around 1,000 characters, so keep the data on `window` and localStorage and only export the qualified rows. Don't spend enrichment calls before the headline pre-filter, and don't score before fetching the page. Use namespaced `__aba_*` localStorage keys — LinkedIn keeps its own state there, and a bare key once collided with it.

## If something breaks

`linkedin-post-analytics/references/troubleshooting.md` covers the shared plumbing: un-awaited IIFEs returning `{}`, output truncation, tab-ID drift, and the stalled-scroll trap on the viewers page.

Per-person profile lookups hit a rate limit long before the other endpoints do: parallel calls draw 429s after a couple hundred and stay blocked for about a minute. Run them one at a time with a gap of a second or so, and when a 429 lands, stop, keep progress, and resume after a pause rather than retrying straight away.
