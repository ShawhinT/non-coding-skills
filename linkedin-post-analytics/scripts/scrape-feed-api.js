// LinkedIn Post Analytics — Voyager feed API (complete + exact)
// Run via javascript_tool on https://www.linkedin.com/in/me/recent-activity/all/
//
// Why this exists: the analytics dashboard (scrape-*.js) caps at the top ~50 posts
// by a metric and mixes lifetime vs window counts. This calls LinkedIn's own
// internal GraphQL feed with the page's credentials and returns EVERY original
// post with exact numImpressions / numLikes / numComments / numShares, dated
// precisely from the activity-ID timestamp. Not capped. No age-string parsing.
//
// Window: set window.__START / window.__END ("YYYY-MM-DD") before running.
// Defaults to the trailing 28 days.
//
// PAGINATION IS TOKEN-BASED. `start` alone does nothing — you must pass the
// paginationToken from the previous response. If the request 404s, the queryId
// hash has rotated: open the recent-activity page, scroll/click "Show more
// results" while reading network requests, grab the live
// voyagerFeedDashProfileUpdates.<hash> and set window.__QID.
//
// Reposts of OTHER people's content come back with no SocialActivityCounts
// (null impressions) and are filtered out — they aren't your posts.
//
// The trailing IIFE MUST be awaited. javascript_tool serializes an un-awaited
// Promise as `{}` — no error, just an empty object, so the run looks like it
// returned nothing when it actually succeeded. The `await` below is
// load-bearing; keep it if you adapt or inline this script.

await (async () => {
  const END = window.__END || new Date().toISOString().slice(0,10);
  const startMs = window.__START ? Date.parse(window.__START + 'T00:00:00') : (Date.now() - 28*864e5);
  const endMs   = Date.parse(END + 'T23:59:59');
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  const prof = (document.documentElement.innerHTML.match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/) || [])[0];
  const qid  = window.__QID || 'voyagerFeedDashProfileUpdates.<queryId-hash>';
  if (!csrf || !prof) return JSON.stringify({ error: 'missing csrf or profileUrn — open /in/me/recent-activity/all/ while logged in' });

  const tsOf = id => Number(BigInt(id) >> 22n);             // activity ID -> creation ms
  const sani = t => t.replace(/https?:\/\/\S+/g, '[url]').replace(/[^\w\s.,!?'\-:;@#]/g, '').replace(/\s+/g, ' ').trim();
  const acc = {};

  const fetchPage = async (start, token) => {
    let v = '(count:20,start:' + start + ',profileUrn:' + prof.replace(/:/g, '%3A');
    if (token) v += ',paginationToken:' + encodeURIComponent(token);
    v += ')';
    const res = await fetch('/voyager/api/graphql?variables=' + v + '&queryId=' + qid, {
      headers: { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0', 'accept': 'application/vnd.linkedin.normalized+json+2.1' },
      credentials: 'include'
    });
    const j = await res.json();
    const inc = j.included || [];
    const counts = {};
    inc.forEach(e => {
      if (/SocialActivityCounts$/.test(e.$type || '')) {
        const m = (e.entityUrn || '').match(/urn:li:activity:(\d+)/);
        if (m) counts[m[1]] = { re: e.numLikes, co: e.numComments, sh: e.numShares, im: e.numImpressions };
      }
    });
    inc.forEach(e => {
      if (!/Update$/.test(e.$type || '')) return;
      const bu = (e.metadata && e.metadata.backendUrn) || e.entityUrn || '';
      const m = bu.match(/urn:li:activity:(\d+)/); if (!m) return;
      const id = m[1], c = counts[id] || {};
      const comm = (e.commentary && e.commentary.text && e.commentary.text.text) ? sani(e.commentary.text.text).slice(0, 80) : '';
      // Format = whichever component is populated under `content`. Cheap to grab
      // here and usually the sharpest single explanatory variable in the split,
      // so it ships on every row rather than being re-derived by eye later.
      const ct = e.content || {};
      const media = ct.imageComponent ? 'image' : ct.linkedInVideoComponent ? 'video'
                  : ct.articleComponent ? 'article' : ct.documentComponent ? 'document' : 'text';
      acc[id] = { id, ts: tsOf(id), isReshare: !!e.resharedUpdate, media, im: c.im ?? null, re: c.re ?? null, co: c.co ?? null, sh: c.sh ?? null, preview: comm };
    });
    // next-page token lives in the response metadata
    return (((((j.data || {}).data || {}).feedDashProfileUpdatesByMemberShareFeed || {}).metadata) || {}).paginationToken || null;
  };

  let token = null, start = 0;
  for (let i = 0; i < 12; i++) {
    token = await fetchPage(start, token);
    start += 20;
    const ids = Object.keys(acc);
    if (!ids.length) break;
    const oldest = Math.min(...ids.map(k => acc[k].ts));
    if (oldest < startMs || !token) break;
  }

  // Original posts only (have impressions), inside the window
  let rows = Object.values(acc).filter(r => r.im != null && r.ts >= startMs && r.ts <= endMs);
  rows.forEach(r => {
    r.date = new Date(r.ts).toISOString().slice(0, 10);
    r.eng = (r.re || 0) + (r.co || 0) + (r.sh || 0);
    r.er = r.im > 0 ? +(((r.eng) / r.im) * 100).toFixed(2) : 0;   // (reactions+comments+shares)/impressions
  });
  rows.sort((a, b) => b.ts - a.ts);
  try { localStorage.setItem('__feedData', JSON.stringify(rows)); } catch (e) {}
  window.__feed = rows;

  // Output is just a summary — the full rows can exceed tool limits.
  // Dump in slices, capping preview length: it is the previews, not the row
  // count, that blows the output budget.
  //   JSON.stringify(window.__feed.slice(0,10).map(r => [r.date,r.er,r.im,r.re,r.co,r.sh,r.media,r.id,r.preview.slice(0,50)]))
  const byMedia = Object.entries(rows.reduce((o, r) => { (o[r.media] = o[r.media] || []).push(r.er); return o; }, {}))
    .map(([k, v]) => [k, v.length, +(v.reduce((a, b) => a + b, 0) / v.length).toFixed(2)]);
  return JSON.stringify({
    count: rows.length,
    window: [new Date(startMs).toISOString().slice(0, 10), END],
    byMedia,   // [format, n, avg engagement rate %]
    note: 'rows saved to window.__feed and localStorage.__feedData — dump in slices of ~10 with previews capped to ~50 chars'
  });
})();
