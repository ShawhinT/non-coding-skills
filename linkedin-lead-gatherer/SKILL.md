---
name: linkedin-lead-gatherer
description: >
  Gather leads from LinkedIn by searching 1st-degree connections matching specific criteria (role, seniority, location, industry).
  Use this skill whenever Shaw asks to find people on LinkedIn, pull connections matching a profile, build a lead list,
  gather contacts for outreach, find people for discovery calls, or anything involving searching through LinkedIn connections.
  Even casual mentions like "check my LinkedIn for analytics people" or "who do I know at mid-sized companies" should trigger this skill.
  Requires Chrome tools (Claude in Chrome) to be enabled.
---

# LinkedIn Lead Gatherer

This skill walks you through systematically extracting leads from a user's LinkedIn network. The core insight is that LinkedIn's connections page search only filters by name — to find connections by role or title, you need to use the main LinkedIn search bar with a 1st-degree filter.

## Prerequisites

- Chrome tools must be enabled (Claude in Chrome MCP)
- User must be logged into LinkedIn in Chrome

If Chrome tools aren't available, tell the user to enable them at Settings → Desktop app → Computer use, and that they need to be logged into LinkedIn.

## The Workflow

### 1. Clarify the target profile

Before touching LinkedIn, nail down:
- **Role keywords**: What titles/functions are you looking for? (e.g., "analytics director", "head of data", "data analyst")
- **Seniority preference**: Leaders first, then managers, then ICs? Or a specific level?
- **Location priority**: Is there a preferred metro area? (e.g., DFW)
- **Volume needed**: How many leads? This determines how many search queries and pages to scrape.
- **Exclusions**: Anyone to skip? (prior outreach, specific companies, etc.)

### 2. Plan your search queries

A single search term misses most of the network. You need multiple queries to get good coverage because people describe the same role in wildly different ways. For an analytics-focused search, good query sets look like:

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

### 3. Set up a working file

Don't try to keep 100+ leads in your context window. Create a JSON file to accumulate leads as you go:

```
/sessions/<session>/leads_raw.json
```

Write a small Python helper to add leads (deduplicating by URL) and report the running count. This pays for itself immediately — you'll be adding leads from 10+ pages across multiple searches.

### 4. Execute the searches

For each search query:

#### Navigate to the search
```
https://www.linkedin.com/search/results/people/?keywords=<URL-encoded-query>&network=%5B%22F%22%5D&origin=FACETED_SEARCH
```

The `network=%5B%22F%22%5D` parameter filters for 1st-degree connections. This is equivalent to clicking the "1st" filter button on the People search results.

To paginate, append `&page=N`.

#### Wait for the page to load
Always wait 2-3 seconds after navigation. LinkedIn's content loads asynchronously.

#### Extract profile URLs via JavaScript
This is the most reliable extraction method. LinkedIn's CSS class names are obfuscated random strings, so don't try to use semantic selectors like `.search-result`. Instead, filter all `<a>` tags:

```javascript
const allLinks = [...document.querySelectorAll('a')];
const seen = new Set();
const profiles = allLinks
  .filter(a => a.href && a.href.includes('/in/')
    && a.textContent.includes('View')
    && a.textContent.includes('profile'))
  .map(a => {
    const url = a.href.split('?')[0];
    const name = a.textContent.replace(/View.*profile/,'').trim();
    return { name, url };
  })
  .filter(p => {
    if (seen.has(p.url)) return false;
    seen.add(p.url);
    return true;
  });
JSON.stringify(profiles);
```

This works because LinkedIn wraps each person's name in a link whose text includes "View [Name]'s profile" and whose href contains `/in/`. Splitting on `?` strips tracking parameters to get a clean profile URL.

#### Get titles and locations
The JavaScript extraction gives you names and URLs but not titles or locations. For those, read the `main` element's `innerText` via JavaScript:

```javascript
const main = document.querySelector('main');
const text = main ? main.innerText : '';
const lines = text.split('\n').filter(l => l.trim().length > 0);
lines.slice(0, 150).join('\n');
```

This returns the full text of all search results on the page, including names, titles, locations, and mutual connections. Parse it to fill in the title and location fields for each lead.

Note: `get_page_text` sometimes grabs a promoted article instead of the search results (it targets `<article>` elements). The JavaScript `main.innerText` approach is more reliable for search pages.

**Run both JavaScript calls in parallel** (URL extraction + page text) to save time. You can parse the text output to match titles/locations to the names you extracted.

#### Save after each page
Append the extracted leads to your working file after each page. Don't accumulate across multiple pages before saving — if something goes wrong, you lose everything.

#### Pagination
Each search page shows 10 results. Move to the next page by incrementing the `page` parameter in the URL.

The page text will tell you how many total pages exist: "Currently on the page X of Y search result pages."

### 5. Deduplicate and triage

After collecting from all queries, the same people will appear across multiple searches. Deduplicate by LinkedIn URL.

Then triage by location. Tag each lead as:
- **Tier 1**: Target metro area (e.g., for DFW check keywords like dallas, fort worth, plano, irving, frisco, allen, mckinney, carrollton, roanoke, arlington)
- **Tier 2**: Same state / nearby (e.g., Austin, San Antonio, Houston for Texas)
- **Tier 3**: Everywhere else

Within each tier, sort by seniority:
1. C-level (Chief, CDO, CAO)
2. VP
3. Head of / Global Head
4. Senior Director
5. Director
6. Manager / Lead
7. Senior Analyst
8. Analyst / IC

### 6. Apply exclusions

Ask the user if there's anyone to remove:
- People they've already spoken to or reached out to
- Companies with too many duplicates (keep only the best one)
- Geographic regions to exclude entirely
- Anyone else for any reason

### 7. Output the final list

Generate a clean markdown table saved to the outputs folder, organized by tier with seniority sorting within each tier. Include: name, title, location, and LinkedIn URL.

Also keep the raw JSON file — it's useful for future filtering or pushing to a CRM/Notion.

## Common pitfalls

- **Don't use the connections page search** (`/mynetwork/invite-connect/connections/`). It only searches by name, not by title or keyword. Always use the main search bar or direct URL.
- **Don't trust LinkedIn's geo URL parameter** (`geoUrn`). It sometimes maps to the wrong city. The "city name in keyword" hack is more reliable.
- **Don't try `read_page` with `filter: interactive`** on search results. It often returns nothing useful for LinkedIn search pages. Use JavaScript extraction instead.
- **Don't keep everything in context**. Write to a file after every page. At 100+ leads, you will lose data otherwise.
- **Expect heavy overlap across searches**. The same person surfaces in "analytics director," "analytics manager," and "data analyst" searches. Always deduplicate by URL.
- **Some leads will have "Unknown" locations**. This happens when the page text gets truncated or the person hasn't listed a location. Keep these — the user can filter them later.
