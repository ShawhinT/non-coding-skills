# Troubleshooting

Common problems encountered when scraping LinkedIn analytics, and how to fix them. These are all things that came up during real sessions — not theoretical edge cases.

## Scraper returns 0 posts

**Cause:** The page hasn't finished rendering. LinkedIn's analytics page loads asynchronously — the post cards render after the initial page load.

**Fix:** The scripts include a built-in 3-second delay, so this should be rare. If it still happens, run the scraper again — the page may need extra time on slow connections. If retrying doesn't help, the page structure may have changed or the URL is wrong. Verify the URL has all four parameters (`startDate`, `endDate`, `metricType`, `timeRange`).

## Numbers look wrong or nonsensical

**Cause:** You're running the wrong scraper variant for the current view. The impressions scraper interprets `nums[1]` as impressions; the engagements scraper interprets it as reposts. If you run the impressions scraper on an engagements-sorted page (or vice versa), you'll misattribute metrics.

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
This gives you enough HTML to identify the new pattern. Look for the post links (they'll still contain `/feed/update/`) and work backwards to find the new container structure.

## Data is capped at ~50 posts

**Cause:** LinkedIn only renders the top ~50 posts per page load, sorted by the selected metric. This is a LinkedIn limitation, not a scraper bug.

**Fix:** Note the cap in your analysis. For date ranges that would have more than 50 posts, you're seeing the top 50 only. If you need comprehensive data, break the date range into smaller chunks (e.g., month by month) and scrape each separately. Be aware that month-by-month scraping may still miss posts that aren't in the top 50 for any individual month.

## Engagement numbers don't add up

**Cause:** LinkedIn's total engagement count sometimes includes interaction types beyond reactions, comments, and reposts (e.g., clicks, follows). The scraped reactions + comments + reposts may be less than the total engagement figure LinkedIn shows.

**Fix:** Accept this as a known discrepancy. The scraped metrics are still useful for relative comparisons — even if the absolute totals don't match LinkedIn's aggregates perfectly.

## Output blocked by Chrome content filter

**Cause:** The Chrome tool's content filter sometimes blocks scraper output with `[BLOCKED: Cookie/query string data]`. This happens when post preview text contains URLs, query strings, or character sequences that look like cookies or tracking parameters.

**Fix:** The scripts now sanitize preview text by stripping URLs and special characters before output. If you still hit this, the simplest workaround is to remove preview text entirely from the output and return numbers only — the metrics are what matter for analysis, and you can cross-reference post previews manually if needed.
