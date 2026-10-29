---
name: event-finder
description: Find upcoming in-person events on Eventbrite for Shaw to attend, ranked by how close they are to Frisco/Plano and by topic (AI first, then tech, then general business networking). Use whenever Shaw asks to find events, meetups, or networking opportunities, e.g. "find AI events in DFW", "what's happening on Eventbrite next month", "any good networking events near me", "events to go to this quarter", "where can I meet founders/CEOs in person", or names a city plus a topic and a time window. Also fires for prospecting-by-showing-up requests like "where should I be in person to meet my ICP" when the answer is local events. Do NOT use for creating or promoting Shaw's own events (Luma pages → conversion-copy, outreach) or for online-only webinars.
---

# Event Finder

Find in-person Eventbrite events in a window, score them on two axes, and hand Shaw a short ranked list he can act on.

## Defaults (override with whatever Shaw says)

- **Home base:** Frisco/Plano. Distance is measured from lat 33.085, lon -96.81 (Legacy area).
- **Window:** today through 3 months out. Resolve "today" in America/Chicago, not UTC.
- **Topic priority:** AI is the best match, then tech/startup, then general business networking.
- **Area:** Frisco and Plano first, then the wider DFW area.
- **Format:** in-person only. Drop online events.

## Why the browser, not search

Web search results for Eventbrite are months stale, because search engines cache old listing pages. A WebFetch of eventbrite.com returns 405. Live data only comes from loading Eventbrite in a real browser. Use the session's preferred browser if its tools work. If they don't (built-in browser tools missing or unreachable), fall back to Claude in Chrome. Read that browser's skill first.

## Method

1. **Open one Eventbrite tab** on any search URL, e.g. `https://www.eventbrite.com/d/tx--plano/ai/`. This puts the page on the eventbrite.com origin so same-origin `fetch` works.

2. **Crawl from inside the page with `scripts/crawl.js`.** Paste the whole file into the browser's JavaScript tool, after setting the `CONFIG` block (locations, slugs, dates, pages per query). The script works like this:
   - Every search page embeds `window.__SERVER_DATA__` JSON. The script fetches the search pages directly and parses that JSON from `search_data.events.results`. That JSON gives venue, lat/lon, dates, tags and the online flag, which is much richer and faster than scraping cards.
   - It runs **in the background** and returns immediately. A single awaited crawl of about 80 pages takes 2–3 minutes and blows the 45-second JavaScript timeout. Poll with `EF.status()` every 30–60 seconds until it reports done.
   - The default config covers 3 locations × 7 slugs × 4 pages, about 84 fetches, and yields about 350 unique in-person events. Results are ranked by relevance, so 4 pages per query is enough. Deeper pages are mostly noise.

3. **Score and read out with `EF.rank()` and `EF.page(cat, start, n)`.**
   - `EF.rank()` labels each event AI, Tech or Biz using keyword regexes over the name, summary and tags. It also computes distance from home.
   - JavaScript tool output truncates at about 1,000 characters, so read results in slices of 12–15 compact lines with `EF.page('AI', 0, 15)`, `EF.page('AI', 15, 15)`, and so on.
   - Use `EF.detail([ids])` (also sliced) to get start time, venue and summary for the shortlist only.

4. **Judge relevance, don't trust the regex.** Topic slugs like `tech` or `ai` seem to return broad result sets, and keywords misfire. For example, "Algo Trading with AI" and an "AI" travel-agent MLM both match the AI pattern, while kids' STEM days and PMP trainings match Tech. Read titles and summaries and drop:
   - consumer and kids events
   - certification trainings
   - MLM and "build wealth" pitches
   - investing or trading pitches
   - Spanish-only events, unless Shaw asks for them
   
   Weight events whose audience is business leaders or founders, since that is Shaw's ICP, above builder hack nights. Treat invite-only exec summits as high value.

5. **Close the tab** you opened.

## Output

Reply in chat, since Shaw is often on mobile. Keep it scannable:

- Open with one line on what was searched: count, window, and that online events were excluded.
- Use 3–4 short groups:
  - **AI near you**
  - **AI elsewhere in DFW**
  - **Tech/startup near you**
  - **Business networking near you** (only the strongest few)
- Give each group 3–6 bullets in this format: `[Title](https://www.eventbrite.com/e/<id>) — date, time, venue/city`, plus a few words on why it fits if that isn't obvious.
- Flag anything happening **today or tomorrow**.
- End with a one-line **pick**: the 2–3 events with the best value, clustered on the same day or area when possible, because Shaw prefers back-to-back over scattered.
- Add one caveat line when it's true: events beyond about 6 weeks out are sparse because organizers post late, so a re-run in a month will surface more.
- Offer next steps in one line: put the list in a sheet, or add picks to the calendar (calendar-helper).

Do not register Shaw for anything or click "Get tickets". That submits a form with his personal data, so ask first.
