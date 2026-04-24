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

## Execute the searches

For each search query:

### Navigate to the search

```
https://www.linkedin.com/search/results/people/?keywords=<URL-encoded-query>&network=%5B%22F%22%5D&origin=FACETED_SEARCH
```

The `network=%5B%22F%22%5D` parameter filters for 1st-degree connections. This is equivalent to clicking the "1st" filter button on the People search results.

To paginate, append `&page=N`.

### Wait for the page to load

Always wait 2-3 seconds after navigation. LinkedIn's content loads asynchronously.

### Extract profile URLs via JavaScript

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

This works because LinkedIn wraps each person's name in a link whose text includes "View [Name]'s profile" and whose href contains `/in/`. Splitting on `?` strips tracking parameters.

### Get titles and locations

The URL extraction gives you names and URLs but not titles or locations. For those, read the `main` element's `innerText`:

```javascript
const main = document.querySelector('main');
const text = main ? main.innerText : '';
const lines = text.split('\n').filter(l => l.trim().length > 0);
lines.slice(0, 150).join('\n');
```

This returns the full text of all search results on the page. Parse it to fill in the title and location fields for each lead.

Note: `get_page_text` sometimes grabs a promoted article instead of search results (it targets `<article>` elements). The JavaScript `main.innerText` approach is more reliable.

**Run both JavaScript calls in parallel** (URL extraction + page text) to save time.

### Save after each page

Append to `raw/<campaign>_leads_raw.json` after each page. Don't accumulate across multiple pages before saving — if something goes wrong, you lose everything. A small Python helper that deduplicates by URL and reports the running count pays for itself immediately.

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
