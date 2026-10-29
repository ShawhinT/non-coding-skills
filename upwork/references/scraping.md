# Scraping Upwork with the Chrome tools

Read this before writing any browser JavaScript for an Upwork sweep. Every item here cost real
calls to discover.

## Setup

Upwork search requires Shaw's login, so use the Chrome tools against his session rather than
WebFetch. `tabs_context_mcp{createIfEmpty:true}` first, then `navigate`. Close the tab with
`tabs_close_mcp` when the sweep is done.

## The two traps

**`get_page_text` returns only the first job tile.** On a 50-result search page it hands back one
posting's full text and silently drops the other 49. It looks like it worked. Use
`javascript_tool` against the DOM instead.

**`javascript_tool` truncates its result at roughly 1000 characters.** No error, no warning —
just `[TRUNCATED]` at the end of whatever you were reading. This is the single biggest time sink
in this workflow. The fix is to keep state in `window.*` on the page and page through it in
small, tightly-formatted chunks. Build the compact triage line first (about 90 characters per
posting, so ~11 fit in one call), and pull full descriptions only for the survivors, two at a
time.

Because state lives on the page, **navigating away wipes it.** Capture everything you need from a
search page — including the job IDs — before moving to the next query.

## Extraction

Job tiles are `article.job-tile`. The fields hang off `data-test` attributes:

```js
window.__all = Array.from(document.querySelectorAll('article.job-tile')).map(t => {
  const g = s => { const e = t.querySelector(s); return e ? e.innerText.trim() : null; };
  const a = t.querySelector('a[href*="/jobs/"]');
  return {
    title: a ? a.innerText.trim() : g('h2'),
    url:   a ? a.getAttribute('href') : null,
    type:  g('[data-test="job-type-label"]'),      // "Hourly: $50.00 - $150.00"
    budget:g('[data-test="is-fixed-price"]'),
    spent: g('[data-test="total-spent"]'),
    loc:   g('[data-test="location"]'),
    posted:g('[data-test="job-pubilshed-date"]'),  // sic — Upwork's typo, not ours
    desc:  (g('[data-test="UpCLineClamp JobDescription"]') || '').replace(/\s+/g, ' ')
  };
});
window.__all.length;
```

Then filter and page, keeping each returned line short:

```js
const KEEP = /(train|workshop|upskill|enable|adoption|coach|onboard|consult).{0,90}(our team|our staff|our company|employees|executives|leadership|our organization|managers)|((our team|our staff|employees|executives|leadership|managers).{0,90}(train|workshop|upskill|adoption))/i;
const DROP = /developer|engineer needed|data annotat|labeling|voice actor|transcri/i;
window.__hits = window.__all.map((j,i) => ({...j, i}))
  .filter(j => KEEP.test(j.title + ' ' + j.desc) && !DROP.test(j.title));

window.__pg = (a,b) => window.__hits.slice(a,b).map(j =>
  `${j.i}|${j.title.slice(0,55)}|${(j.type||j.budget||'').replace(/Hourly: |Fixed price|\$|\.00/g,'')}|${(j.spent||'').replace(/\s|spent/g,'')}|${(j.loc||'').replace(/Location\s*/,'').slice(0,10)}`
).join('\n');

window.__d = idx => idx.map(i => i + ':' + window.__all[i].desc.slice(0,420)).join('\n\n');

window.__hits.length + '/' + window.__all.length;
```

Call `window.__pg(0,11)`, `window.__pg(11,22)` … to triage, then `window.__d([3,7])` two at a
time for the ones worth reading. Tune the keep/drop patterns per query — a broad query like
"AI training for our team" needs a much stricter filter than "claude training".

Grab the job IDs before navigating away:

```js
[0,3,28,34].map(i => i + ':' + window.__all[i].url.match(/~[0-9a-z]+/)[0]).join('\n');
```

A job ID resolves to `https://www.upwork.com/jobs/~<id>` — short, stable, and the right thing to
put in a deliverable. The full slugged URLs from the search page are long and carry
`<span class="highlight">` fragments from the search term.

## The client block

Only on the job detail page. This is the qualification payload:

```js
const b = document.querySelector('[data-test="AboutClientUser"],[data-test="about-client-container"]');
const d = document.querySelector('[data-test="Description"],.description');
'CLIENT: ' + (b ? b.innerText.replace(/\s+/g,' ')
    .replace(/About the client|Payment method verified|Phone number verified|Rating is.*?reviews/g,'') : '?').slice(0,280)
+ '\nDESC: ' + (d ? d.innerText.replace(/\s+/g,' ').slice(0,500) : '?');
```

A populated block reads like:

```
United States  9:27 AM  18 jobs posted  67% hire rate, 1 open job  $49K total spent
21 hires, 2 active  $42.75 /hr avg hourly rate paid  1,043 hours
Mid-sized company (10-99 people)  Member since Mar 18, 2024
```

Company-size bands seen so far: `Small company (2-9 people)`, `Mid-sized company (10-99 people)`.
Individual accounts have no band at all. Note the band tops out at 99, so it can't confirm the
upper half of a 51–200 gate on its own — pair it with outside research when the company is
identifiable.

The detail page also carries the full description, where the search tile truncates. That full
text is usually where a company names itself.

## Cost

A sweep of four queries at 50 results each, plus client blocks on a dozen survivors, runs roughly
40–50 browser calls. Most of that is the 1000-character cap. Budget accordingly, and prefer
narrowing the in-browser filter over pulling more text into context.
