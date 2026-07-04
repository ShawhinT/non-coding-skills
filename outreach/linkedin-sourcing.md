# LinkedIn Sourcing

Use this workflow when Phase 2 of the outreach flow calls for sourcing from Shaw's LinkedIn network. The core insight: LinkedIn's connections page search only filters by name — to find connections by role or title, you need to use the main LinkedIn search bar with a 1st-degree filter.

## Prerequisites

- Chrome tools must be enabled (Claude in Chrome MCP)
- Shaw must be logged into LinkedIn in Chrome

If Chrome tools aren't available, tell Shaw to enable them at Settings → Desktop app → Computer use, and to be logged into LinkedIn.

## Plan your search queries

A single search term misses most of the network. You need multiple queries because people describe the same role in wildly different ways. For an analytics-focused search, a good query set looks like:

**Leadership tier:**
- "analytics director"
- "head of analytics"
- "VP data analytics"
- "chief data officer"

**Manager tier:**
- "analytics manager"
- "data science manager"

**IC tier:**
- "data analyst"
- "senior data analyst"

**Location-specific (the geo hack):**
- "analytics dallas" — Adding a city name to the keyword is more reliable than LinkedIn's geo filter URL parameters, which sometimes map to the wrong location.

Run the highest-seniority queries first. Stop adding queries once you've hit the target volume.

**When sourcing founders/owners, search by *functional and board titles too* — they often don't say "founder."** A founder/owner query set:

- Core: "founder", "co-founder", "cofounder" (no hyphen finds different people), "CEO", "owner", "president"
- Functional (esp. technical/product founders): "CTO", "CPO", "Chief AI Officer", "founder CTO"
- Board / ownership (founders who stepped back but still own): "executive chairman", "chairman", "managing partner", "general partner"
- Builder language (AI-native founders): "building", "entrepreneur", "startup"

`CEO`-type terms have a **long tail** — page deep (LinkedIn caps people search at ~10 pages/query). Watch new-adds-per-page: a drop usually means *overlap* with prior queries, not exhaustion — confirm before stopping a core term early. Note which query surfaced each lead (tag it) so you can tell diversifiers from duplicates. Pure variants ("cofounder" vs "co-founder") often 100% overlap — drop them fast.

## Execute the searches

For each search query:

### Navigate to the search

```
https://www.linkedin.com/search/results/people/?keywords=<URL-encoded-query>&network=%5B%22F%22%5D&origin=FACETED_SEARCH
```

The `network=%5B%22F%22%5D` parameter filters for 1st-degree connections. This is equivalent to clicking the "1st" filter button on the People search results.

To paginate, append `&page=N`.

### 3-tab pipelining (overlap the load waits)

LinkedIn content loads asynchronously (~2-3s). Don't pay that wait serially. Open a **3-tab pool** and, in one `browser_batch`, navigate all three to different query pages; by the time you cycle back to extract, the first has loaded. Navigate-batch → extract-batch, three pages per round. Pace gently — rapid concurrent profile/search hits on one account risk a throttle or flag. (Subagents can't help here: one browser, one logged-in session.)

### Extract via JavaScript — key on the `• 1st` degree badge

LinkedIn's CSS classes are obfuscated, and the old "View [name]'s profile" link text is **stale** — don't rely on it. Each result card's anchor text contains the degree badge (`• 1st`); mutual-connection links don't. Filter on that:

```javascript
const byUrl = {};
[...document.querySelectorAll('a')].forEach(a => {
  if (!a.href || !a.href.includes('/in/')) return;
  const url = a.href.split('?')[0];
  const t = a.textContent.replace(/\s+/g, ' ').trim();
  (byUrl[url] = byUrl[url] || {url, texts: []}).texts.push(t);
});
const out = [];
Object.values(byUrl).forEach(r => {
  const card = r.texts.find(t => /•\s*1st/.test(t));   // result card only
  if (!card) return;
  const name = r.texts.filter(t => !/•/.test(t)).sort((a,b)=>a.length-b.length)[0] || '';
  let h = (card.split(/•\s*1st/)[1] || '')
    .split(/\d+[KM]?\s*followers|mutual connection|Visit my website|is a mutual/)[0]
    .replace(/Message/g,'').trim();
  out.push({name, url, headline: h.slice(0,150)});
});
```

The headline carries the role, company (`@`/`at`/`Current:`), and often the AI/industry signal — enough for free-stage scoring.

### Accumulate to localStorage, exfiltrate via the DOM

Two truncation traps: the `javascript_tool` return truncates at ~1,130 chars, and `get_page_text` targets `<article>`/`<main>` (sometimes grabbing a promoted post). Beat both:

1. **Accumulate, don't return.** Have the extractor merge results into `localStorage` (dedup by URL, tag with the query) and return only `{added, total}` — tiny, never truncated. This survives across pages/queries (localStorage persists; `window` globals don't). You can run the 3 tabs' accumulators in one `browser_batch` since each return is small.
2. **Exfiltrate by injecting into `<main>`.** When done, write the whole store as delimited text (use sentinels like ` ~REC~ ` / ` ~F~ ` so headlines with spaces parse cleanly) into `document.querySelector('main').innerHTML`, then read it with `get_page_text` — which returns ~25KB cleanly (far past the JS-eval cap). Dump in halves if larger. Save that to `raw/<campaign>_leads_raw.json` via a small Python parser.

For reading individual **profile/activity pages** (e.g. checking recent posts), use a **self-waiting** extractor — `javascript_tool` supports top-level `await`, so poll until the feed loads instead of guessing a fixed wait:

```javascript
(async()=>{let t='';for(let i=0;i<12;i++){const m=document.querySelector('main');
  t=m?m.innerText.replace(/\s+/g,' ').trim():''; if(t.length>300) break;
  await new Promise(r=>setTimeout(r,400));} return t.slice(0,1400);})()
```

### Save after each round

Persist after each round of pages — never accumulate only in context. The localStorage store is the durable buffer; flush it to `raw/` periodically and at the end.

### Pagination

Each search page shows 10 results. Increment the `page` parameter to continue. The page text will tell you the total: "Currently on the page X of Y search result pages."

## Common pitfalls

- **Don't use the connections page search** (`/mynetwork/invite-connect/connections/`). It only searches by name, not title. Always use the main search bar or direct URL.
- **Don't trust LinkedIn's geo URL parameter** (`geoUrn`). It sometimes maps to the wrong city. The "city name in keyword" hack is more reliable.
- **Don't try `read_page` with `filter: interactive`** on search results. It returns nothing useful for LinkedIn search pages. Use JavaScript extraction instead.
- **Don't keep everything in context**. Write to a file after every page. At 100+ leads, you will lose data otherwise.
- **Expect heavy overlap across searches**. The same person surfaces in "analytics director," "analytics manager," and "data analyst" searches. Always deduplicate by URL.
- **Some leads will have "Unknown" locations**. The page text gets truncated or the person hasn't listed a location. Keep these — Shaw can filter later.

## When sourcing leaders: typical seniority ordering

Not required, but a useful default when ranking within a segment:

1. C-level (Chief, CDO, CAO)
2. VP
3. Head of / Global Head
4. Senior Director
5. Director
6. Manager / Lead
7. Senior Analyst
8. Analyst / IC

This is just one example segmentation — segments depend on the campaign. See the main SKILL.md for segment design.
