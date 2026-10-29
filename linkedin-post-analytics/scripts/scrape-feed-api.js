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
// Counts are keyed by one of TWO urns. Most posts key their
// SocialActivityCounts by urn:li:activity:<id>; some (scheduled posts among
// them) key by urn:li:ugcPost:<id>, reachable only through the update's
// *socialDetail. Joining on the activity urn alone silently drops those posts —
// once it dropped the month's top post. So join on activity first, then fall
// back to the ugcPost from socialDetail. A repost of someone else's content is
// identified by resharedUpdate, or by a socialDetail thread that points at a
// different activity (a repost with commentary) — not by missing counts; a row that still has no
// counts after both joins is reported in `unmatched` so a gap is visible
// rather than silent.
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
  const qid  = window.__QID || 'voyagerFeedDashProfileUpdates.<queryId-hash>';
  if (!csrf) return JSON.stringify({ error: 'no JSESSIONID cookie — are you logged in?' });

  // Own profile URN. LinkedIn has been removing identity from the rendered
  // HTML, so the scrape is the fast path and /voyager/api/me is the reliable
  // one. Ask the API rather than failing when the match comes up empty.
  let prof = (document.documentElement.innerHTML.match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/) || [])[0];
  if (!prof) {
    const me = await fetch('/voyager/api/me', {
      headers: { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0' }, credentials: 'include'
    });
    if (me.ok) prof = (JSON.stringify(await me.json()).match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/) || [])[0];
  }
  if (!prof) return JSON.stringify({ error: 'could not resolve profileUrn from page HTML or /voyager/api/me' });

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
    const counts = {}, votesBy = {};
    inc.forEach(e => {
      if (/SocialActivityCounts$/.test(e.$type || '')) {
        const m = (e.entityUrn || '').match(/urn:li:(?:activity|ugcPost):(\d+)/);
        if (m) counts[m[1]] = { re: e.numLikes, co: e.numComments, sh: e.numShares, im: e.numImpressions };
      }
      // Poll vote totals live on a separate PollSummary entity, not on the poll itself.
      if (/PollSummary$/.test(e.$type || '')) votesBy[e.entityUrn] = e.uniqueVotersCount ?? null;
    });
    inc.forEach(e => {
      if (!/Update$/.test(e.$type || '')) return;
      const bu = (e.metadata && e.metadata.backendUrn) || e.entityUrn || '';
      const m = bu.match(/urn:li:activity:(\d+)/); if (!m) return;
      const id = m[1];
      // socialDetail names the thread the counts belong to. A ugcPost thread is
      // this post under its other urn; an activity thread with a different id is
      // someone else's post that this one reshares with commentary.
      const sd = JSON.stringify(e['*socialDetail'] || e.socialDetail || '');
      const thread = sd.match(/fsd_socialDetail:\(urn:li:(activity|ugcPost):(\d+)/);
      const ugc = thread && thread[1] === 'ugcPost' ? thread[2] : null;
      const quotesOther = !!(thread && thread[1] === 'activity' && thread[2] !== id);
      // A plain repost (no commentary) can carry neither flag above: its thread
      // is the original's ugcPost, which reads exactly like this post's own
      // second urn. What gives it away is authorship — the update's actor is
      // the original author, and a header says it was reposted.
      const memberId = prof.split(':').pop();
      const actorStr = JSON.stringify(e.actor || '');
      const byOther = actorStr.length > 2 && !actorStr.includes(memberId);
      const repostHeader = /repost/i.test(JSON.stringify(e.header || ''));
      const c = counts[id] || (ugc && counts[ugc]) || {};
      const comm = (e.commentary && e.commentary.text && e.commentary.text.text) ? sani(e.commentary.text.text).slice(0, 80) : '';
      // Format = whichever component is populated under `content`. Cheap to grab
      // here and usually the sharpest single explanatory variable in the split,
      // so it ships on every row rather than being re-derived by eye later.
      const ct = e.content || {};
      const media = ct.imageComponent ? 'image' : ct.linkedInVideoComponent ? 'video'
                  : ct.articleComponent ? 'article' : ct.documentComponent ? 'document'
                  : ct.pollComponent ? 'poll' : 'text';
      // Poll votes are not reactions, comments or shares, so the rate below
      // excludes them. Carry the count so a poll can be read beside its rate.
      const votes = ct.pollComponent ? (votesBy[ct.pollComponent['*pollSummary']] ?? null) : null;
      acc[id] = { id, ugc, ts: tsOf(id), isReshare: !!e.resharedUpdate || quotesOther || repostHeader, byOther, media, votes, im: c.im ?? null, re: c.re ?? null, co: c.co ?? null, sh: c.sh ?? null, preview: comm };
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

  // Original posts only, inside the window. Reposts are dropped by flag; an
  // original with no counts after both joins is surfaced, not discarded.
  // Authorship check, with a guard: if the actor field ever stops naming your
  // own member id, byOther would flag every post and empty the report. On a
  // profile feed reposts are the minority, so a majority flagged means the check
  // is broken — drop it and say so rather than silently losing originals.
  const all = Object.values(acc);
  const authorCheck = all.filter(r => r.byOther).length <= all.length / 2;
  all.forEach(r => { if (authorCheck && r.byOther) r.isReshare = true; });
  const inWin = all.filter(r => !r.isReshare && r.ts >= startMs && r.ts <= endMs);
  const unmatched = inWin.filter(r => r.im == null).map(r => r.id);
  let rows = inWin.filter(r => r.im != null);
  rows.forEach(r => {
    const d = new Date(r.ts);   // browser-local date: an evening post must not land on tomorrow's UTC date
    r.date = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    r.eng = (r.re || 0) + (r.co || 0) + (r.sh || 0);
    r.er = r.im > 0 ? +(((r.eng) / r.im) * 100).toFixed(2) : 0;   // (reactions+comments+shares)/impressions
  });
  rows.sort((a, b) => b.ts - a.ts);
  try { localStorage.setItem('__feedData', JSON.stringify(rows)); } catch (e) {}
  window.__feed = rows;

  // Output is just a summary — the full rows can exceed tool limits.
  // Dump in slices, capping preview length: it is the previews, not the row
  // count, that blows the output budget.
  //   JSON.stringify(window.__feed.slice(0,10).map(r => [r.date,r.er,r.im,r.re,r.co,r.sh,r.media,r.votes,r.id,r.preview.slice(0,50)]))
  const byMedia = Object.entries(rows.reduce((o, r) => { (o[r.media] = o[r.media] || []).push(r.er); return o; }, {}))
    .map(([k, v]) => [k, v.length, +(v.reduce((a, b) => a + b, 0) / v.length).toFixed(2)]);
  return JSON.stringify({
    count: rows.length,
    window: [new Date(startMs).toISOString().slice(0, 10), END],
    byMedia,   // [format, n, avg engagement rate %]
    unmatched, // original posts in the window with no counts under either urn — should be empty
    authorCheck, // false = actor field no longer names you; reposts without commentary may show up as unmatched
    note: 'rows saved to window.__feed and localStorage.__feedData — dump in slices of ~10 with previews capped to ~50 chars'
  });
})();
