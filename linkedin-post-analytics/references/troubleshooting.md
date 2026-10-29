# Troubleshooting

Common problems encountered when scraping LinkedIn analytics, and how to fix them. These are all things that came up during real sessions — not theoretical edge cases.

## Scraper returns 0 posts

**Cause:** The page hasn't finished rendering. LinkedIn's analytics page loads asynchronously — the post cards render after the initial page load.

**Fix:** The scripts include a built-in 3-second delay, so this should be rare. If it still happens, run the scraper again — the page may need extra time on slow connections. If retrying doesn't help, the page structure may have changed or the URL is wrong. Verify the URL has all four parameters (`startDate`, `endDate`, `metricType`, `timeRange`).

## Shares / reposts look suspiciously high

**Cause:** The engagements view's third column is LinkedIn's **totalEngagements** metric — reactions + comments + reposts + clicks + saves + other interactions — *not* the repost count. Earlier versions of this skill mislabeled that number as "reposts," producing absurd outputs like "167 shares" on a post that actually had 1 repost (the other 165 were clicks, saves, etc.). If your output shows reposts much larger than reactions for several posts, you've hit this.

**Fix:** The current `scrape-engagements.js` reports the number as `totalEng`, not `reposts`. If you need a true repost count for a specific post, navigate to the post page (`https://www.linkedin.com/feed/update/urn:li:activity:<id>/`) and read the count from the social-counts row at the bottom of the post body. There is no way to get reliable per-post repost counts from the analytics dashboard in bulk.

## Engagement rate over 100% or wildly out of range

**Cause:** Almost always one of two things: (a) reaction/comment counts on the dashboard are lifetime totals while impressions are window-specific, so an old post that received a few hundred impressions during the window will combine its lifetime engagement with a tiny denominator; or (b) the scraper misinterpreted the engagements-view third column (see above).

**Fix:** Filter to posts whose age span (e.g., "2w", "3d") falls inside the analytics window. Posts marked "1mo" or older were created before the window opened. For (b), make sure you're using the current `scrape-engagements.js` that reports `totalEng` rather than fabricating a `reposts` value.

Watch the age *unit* when you filter: LinkedIn writes months as `mo` and minutes as `m`. A regex that lists `m` before `mo` will truncate `10mo` to `10m` and treat a 10-month-old post as 10 minutes old — it then passes the window filter and detonates the rate. Order alternations `mo|yr|s|m|h|d|w`. See the dedicated entry below.

## Numbers look wrong but not absurdly so

**Cause:** You're running the wrong scraper variant for the current view. The impressions scraper interprets `nums[1]` as impressions; the engagements scraper interprets it as totalEngagements. Mismatching the scraper to the view silently swaps these.

**Fix:** Check the `metricType` in the current URL and make sure you're using the matching scraper. The URL in the tab context from `tabs_context_mcp` will show you which view you're on.

## Post text shows "N/A"

**Cause:** Some posts (reshares, image-only, or very short text posts) don't have a span with `innerText.length > 80`.

**Fix:** Lower the threshold to 40-50 characters, or fall back to grabbing the first substantial span. For image-only posts, there simply won't be preview text — that's expected.

## Tab ID errors or "tab not found"

**Cause:** Tab IDs change between sessions and can change when tabs are opened/closed.

**Fix:** Always call `tabs_context_mcp` before running `javascript_tool` to get the current tab ID. Never hardcode tab IDs from a previous scrape.

## read_page exceeds character limits

**Cause:** LinkedIn's analytics dashboard is too large for `read_page` or `get_page_text` — both return the full page content including navigation, sidebar, and all post card HTML.

**Fix:** This is the whole reason the skill uses `javascript_tool` instead. Don't try to use `read_page` on the analytics page — go straight to `javascript_tool` with the scraping scripts.

## LinkedIn UI structure has changed

**Cause:** LinkedIn periodically updates their frontend. The selectors (`main li > a[href*="/feed/update/"]`) or the span structure may change.

**Fix:** Use `javascript_tool` to inspect the current structure:
```javascript
document.querySelector('main').innerHTML.substring(0, 3000)
```
This gives you enough HTML to identify the new pattern. Look for the post links (they'll still contain `/feed/update/`) and work backwards to find the new container structure. Also dump the raw spans for a single post card and verify what each number actually means before trusting the scraper output:
```javascript
const li = document.querySelector('main li');
Array.from(li.querySelectorAll('span')).map(s => s.innerText.trim()).filter(t => t && t.length < 80);
```

## Data is capped at ~50 posts

**Cause:** LinkedIn only renders the top ~50 posts per page load, sorted by the selected metric. This is a LinkedIn limitation, not a scraper bug.

**Fix:** Note the cap in your analysis. For date ranges that would have more than 50 posts, you're seeing the top 50 only. If you need comprehensive data, break the date range into smaller chunks (e.g., month by month) and scrape each separately. Be aware that month-by-month scraping may still miss posts that aren't in the top 50 for any individual month.

## Matching posts across the two views

**Cause:** Preview text shown on each card is truncated, and the truncation point can differ slightly between views. Using "first N characters of preview" as a join key sometimes fails — especially when the truncation point lands inside a word.

**Fix:** Extract the activity ID from the post's `href` (`/feed/update/urn:li:activity:<id>/`) and use that as the join key. It's stable, unique, and identical across views.

## Output blocked by Chrome content filter

**Cause:** The Chrome tool's content filter sometimes blocks scraper output with `[BLOCKED: Cookie/query string data]`. This happens when post preview text contains URLs, query strings, or character sequences that look like cookies or tracking parameters.

**Fix:** The scripts now sanitize preview text by stripping URLs and special characters before output. If you still hit this, strip preview text more aggressively — drop quotes, hashes, and parentheses — or return numbers only and cross-reference previews manually. One non-obvious trigger: returning `location.href` (or anything containing the analytics URL's query string) from `javascript_tool` trips this filter too. Don't echo the URL back — return only the data you need.

## Age unit: months ("mo") read as minutes ("m")

**Cause:** The post age in the byline ("... posted this • 10mo") uses `mo` for months and `m` for minutes. A unit-matching regex that lists `m` before `mo` matches the `m` branch first, so `10mo` is captured as `10m`. The post then looks 10 minutes old instead of 10 months old, slips past a "created in the last N days" window filter, and its lifetime engagement gets divided by a small window impression count — producing a garbage (often chart-topping) engagement rate.

**Fix:** Order the alternation so longer units win: `mo|yr|s|m|h|d|w`. Treat `now`, `Nh`, `Nm` (minutes), `Nd`, and `Nw` as in-window; treat `Nmo` and `Nyr` as out-of-window. The bundled scrapers already parse age this way and store it on each row — sanity-check by dumping the distinct ages (`[...new Set(rows.map(r => r.age))]`) and confirming you see no bare `m` values you actually meant as months.

## Data disappears after navigating between the two views

**Cause:** Scraping impressions then engagements means navigating to a second URL. Navigation reloads the page and wipes every `window.*` global, so a result stashed in `window.__impr` on the first page is gone by the time you scrape the second.

**Fix:** Persist each view's result to `localStorage` (the bundled scrapers write `__imprData` and `__engData`), then read both keys back and merge by activity ID after the second scrape. `localStorage` survives same-origin navigation; `window` globals do not.

## Voyager feed API returns 400 / nothing

**Cause:** Either the legacy `identity/profileUpdatesV2` endpoint (dead — returns 400) was used, or the GraphQL `queryId` hash has rotated and no longer matches.

**Fix:** Use the GraphQL endpoint `voyager/api/graphql?variables=(...)&queryId=voyagerFeedDashProfileUpdates.<hash>`. If it 404s, capture a fresh hash: on `/in/me/recent-activity/all/`, start `read_network_requests` filtered to `graphql`, scroll and click "Show more results" to trigger a real feed request, and copy the live queryId into `window.__QID` before running the scraper.

## Identity: the `ACoAA…` member URN is the key, not the page and not the slug

**Cause:** LinkedIn has been moving identity off both places it used to be readable. Two symptoms, one root:

- `scrape-feed-api.js` returns `missing csrf or profileUrn` — your *own* profile URN is no longer in the recent-activity page HTML, so the regex over `document.documentElement.innerHTML` finds nothing even though you're logged in.
- A per-person endpoint 403s — `voyagerRelationshipsDashMemberRelationships` (the degree lookup) rejects a vanity slug. It accepts only the opaque `ACoAA…` member URN. Followers already arrive as URNs, so this fails precisely on the slug-keyed rows: engagers and profile viewers, i.e. every genuinely inbound person in a sweep.

**Fix:** resolve the URN, then call. For your own, `/voyager/api/me` returns it. For anyone else, `positionGroups` still accepts either id form and its response carries the person's `ACoAA…` urn, so one call yields the URN and the current position together — resolve it there and key the record on the URN from then on. Both bundled scripts now do this.

Don't reach for the old profile endpoints to bridge the gap: `identity/profiles/<id>` and `identity/profiles/<id>/networkinfo` are **410 Gone**, so a fallback chain built on them fails twice and looks like an auth problem. `positionGroups` under the same path prefix still works, which is what makes the 410s surprising — the prefix surviving is not evidence the endpoint did.

The general lesson for any new Voyager endpoint: assume the URN is the identity key and that a slug is a convenience the endpoint may not honor. Resolve once when you build the work list rather than discovering it mid-batch.

## Voyager pagination not advancing (same posts repeat)

**Cause:** The endpoint ignores `start` as an offset. Incrementing `start` alone returns the same first page.

**Fix:** Pass the `paginationToken` from each response (`data.data.feedDashProfileUpdatesByMemberShareFeed.metadata.paginationToken`) into the next request's variables. `scrape-feed-api.js` already threads this; page until the oldest post predates the window.

## Feed DOM only shows ~5 posts / "Show more" does nothing

**Cause:** The recent-activity feed virtualizes — only ~5 post nodes are mounted at once — and the "Show more results" button doesn't fire on a synthetic `.click()` or dispatched mouse events.

**Fix:** Don't scrape the feed DOM for completeness. Call the Voyager API (`scrape-feed-api.js`), which returns every post regardless of what's rendered.

## javascript_tool output is truncated

**Cause:** The full row set (all posts in a month, with previews) can exceed the tool's output limit, so the JSON gets cut off mid-string.

**Fix:** Don't return the whole array. Persist it (the feed scraper writes `window.__feed` and `localStorage.__feedData`) and dump it in slices: `JSON.stringify(window.__feed.slice(0,10))`, then `slice(10,20)`, etc. Same trick for any large in-page computation.

Preview text, not row count, is what actually blows the budget — a row is a handful of small numbers plus a string that can run 100+ characters. Cap the preview in the projection rather than shrinking the slice: `.map(r => [r.date, r.er, r.im, r.re, r.co, r.sh, r.media, r.id, r.preview.slice(0,50)])` reliably fits ~10 rows, where the same 10 rows at full preview length truncate.

## javascript_tool returns `undefined` (bare top-level `return`)

**Cause:** `javascript_tool` runs with REPL semantics — it returns the value of the last *expression*, and a top-level `return` statement throws in that context, so the tool silently yields `undefined` instead of your result. This bites when you inline or adapt a scraper by hand instead of pasting it whole, because the bundled scripts' output lives inside `return` statements.

**Fix:** Keep the `(async () => { ... })()` wrapper (the bundled `scrape-feed-api.js` already has it) so the `return`s sit inside a function and the IIFE itself is the trailing expression. If you paste only a fragment, either restore the wrapper or end with a bare expression (e.g. `JSON.stringify(result)`) rather than `return ...`. The wrapper is necessary but not sufficient — see the next entry for the `await` it also needs.

## javascript_tool returns `{}` (un-awaited async IIFE)

**Cause:** An `async` IIFE evaluates to a *Promise*, and `javascript_tool` serializes an un-awaited Promise as `{}`. There's no error and no timeout — the call looks like it ran and returned an empty object, so the natural next move is to re-run it or start debugging the scrape logic, when in fact the scrape already succeeded and its result is sitting in `window.__feed`.

This is the twin of the entry above and they pull in opposite directions: that one tells you to keep the `(async () => {...})()` wrapper, which is correct, but the wrapper alone still yields `{}`.

**Fix:** Await it — `await (async () => { ... })();`. Verified directly: `(async () => 42)()` returns `{}` while `await (async () => 42)()` returns `42`. The bundled `scrape-feed-api.js` now ships with the `await`; keep it when adapting or inlining the script. If you hit a `{}` from a script you've already run, don't re-run it — read the result back out of `window.__feed` / `localStorage.__feedData` first.

## javascript_tool times out at 45s on a long walk

**Cause:** `javascript_tool` is capped around 45 seconds (`CDP sendCommand "Runtime.evaluate" timed out after 45000ms`). Any per-person walk over the Voyager endpoints runs past that long before it finishes: a week of followers (~70 people, a relationship lookup each, plus "show more" waits) or a full enrichment pass (~150 people at ~2.5s each) both take minutes. The timeout kills the *call*, not the page — the script usually keeps running to completion, so re-running it doubles the work and can double-count.

**Fix:** Start long walks **detached** and poll, which is the one case where the un-awaited IIFE above is correct rather than a bug. Accumulate into a global the script owns, flip a done flag at the end, and return a literal immediately:

```js
window.__out = []; window.__done = false;
(async () => { /* ... push into window.__out ... */ window.__done = true; })();
'started'
```

Then poll from separate calls — `await new Promise(r => setTimeout(r, 35000)); JSON.stringify({done: window.__done, n: window.__out.length})` — until the flag flips. Read the flag and the count together: a count that has stopped moving is indistinguishable from a walk still waiting on a page load. Per-script `limit` parameters (as on `enrich-candidates.js`) chunk around the same cap, but the detached pattern generalizes to any walk, including the ones that page a list and so can't be resumed from an index.

## Chrome connection drops mid-analysis ("Browser connection is unavailable")

**Cause:** The extension connection can drop between calls. Reconnecting hands you a *new tab* with a new ID and a fresh page, so every `window.*` global from the scrape is gone — `window.__feed` included. The natural reflex is to re-navigate and re-run full pagination.

**Fix:** Re-navigate to `/in/me/recent-activity/all/`, then read the rows back from `localStorage.__feedData` before re-scraping. `localStorage` is scoped to the origin, not the tab, so it outlives the drop even though the tab doesn't — re-paginating the feed API is usually wasted work.

The catch: this only helps if the write actually happened. `scrape-feed-api.js` persists to `localStorage.__feedData`, but an inlined or hand-adapted copy of the script easily drops that line while keeping the `window.__feed` assignment — leaving nothing to rehydrate from at exactly the moment you need it. When adapting the script, keep the `localStorage.setItem`; it costs one line and it's the only copy of the data that survives the tab.

## A scrolled list stops growing — and you believe it

**Cause:** LinkedIn lazy-loads its long lists (profile viewers, followers, notifications) as you scroll. Two very different situations produce an identical signal — the item count holding steady across iterations. Either the list is genuinely exhausted, or the loader never fired and the page is sitting on whatever it rendered first. A scrape loop that stops on "count didn't change" cannot tell them apart, so it reports a partial pull as a complete one.

This is worse than a crash, because it yields a plausible number rather than an error. A profile-viewer pull that stalled at 30 entries was reported as "LinkedIn caps the list at 30 and three days"; scrolled properly the same list returned 60 entries across the full seven days, and the missing half contained the most senior people in it. Every downstream conclusion was drawn from the truncated set.

**Fix:** Stop on a *boundary*, not on a plateau. Page until you see an item that is provably outside the window you asked for — an age string older than the range, a date past the cutoff — and treat "the count stopped moving" as a symptom to investigate rather than a terminating condition. If you must stop without reaching a boundary, say so in the output: report it as "the first N I could load," never as the total.

The usual cause of the stall is the scroll itself. `window.scrollTo(...)` and setting `element.scrollTop` move the viewport but do **not** trigger LinkedIn's infinite-scroll loader — it listens for real user scroll events. From `javascript_tool` alone the list will plateau forever. Drive the scrolling from the tool layer instead (`computer` with `action: "scroll"`), and use `javascript_tool` only to harvest what has rendered. Because these lists also virtualize — nodes are unmounted once they leave the viewport — harvest incrementally into an accumulator between scrolls rather than reading the DOM once at the end.
