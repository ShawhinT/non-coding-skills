// Pull every reactor and commenter for a list of posts, via LinkedIn's legacy
// Voyager REST endpoints. Same auth as the feed API: the csrf-token header is
// the JSESSIONID cookie value.
//
// Run on any linkedin.com page (the recent-activity page is convenient).
//
// Set window.__POSTS first — every post in the analytics window, not just this
// week's (reactions carry no date, so walking each post is the only way to see
// everyone who engaged):
//   window.__POSTS = window.__feed.map(r => ({ id: r.id, ugc: r.ugc, date: r.date }))
// window.__feed comes from linkedin-post-analytics/scripts/scrape-feed-api.js.
// Keep `ugc`: a post whose counts are keyed by its ugcPost urn serves its
// reactions and comments only under that urn, and the activity urn returns none.
//
// Resumable, like enrich-candidates.js: a 28-day window runs past
// javascript_tool's ~45-second limit in one call. Paste this file once, then
// re-run `JSON.stringify(await window.__scrapeEngagers(5))` until `remaining`
// is 0. Each finished post is saved before the next one starts, so a timeout or
// a tab drop loses at most the post in flight.
//
// Full rows land on window.__engagers (keyed by post id), and one row per
// person (with the posts they engaged on) on window.__engagerPeople — both also
// in localStorage under __aba_* keys. Dump them in slices; the whole set will
// truncate javascript_tool's output.

window.__engagers = window.__engagers && !Array.isArray(window.__engagers)
  ? window.__engagers : JSON.parse(localStorage.getItem('__aba_engagers') || '{}');

window.__scrapeEngagers = async (limit = 5) => {
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  if (!csrf) return { error: 'No JSESSIONID cookie — are you logged in?' };
  const POSTS = window.__POSTS;
  if (!Array.isArray(POSTS) || !POSTS.length) return { error: 'Set window.__POSTS = [{id, ugc, date}, ...] first' };

  const headers = {
    'csrf-token': csrf,
    'x-restli-protocol-version': '2.0.0',
    'accept': 'application/vnd.linkedin.normalized+json+2.1'
  };
  const pause = ms => new Promise(r => setTimeout(r, ms));

  // MiniProfile entities carry the name, headline and vanity slug. They arrive
  // in included[] and are referenced by entityUrn from the reaction/comment.
  const indexProfiles = (included) => {
    const map = {};
    (included || []).forEach(e => { if (/MiniProfile$/.test(e.$type || '')) map[e.entityUrn] = e; });
    return map;
  };
  const person = (p) => p ? {
    name: ((p.firstName || '') + ' ' + (p.lastName || '')).trim(),
    slug: p.publicIdentifier || '',
    headline: (p.occupation || '').slice(0, 90)
  } : null;

  const todo = POSTS.filter(p => !window.__engagers[p.id]).slice(0, limit);
  for (const post of todo) {
    const reactions = [], comments = [];

    // Reactions. No timestamp is available — attribute them to the post.
    for (let start = 0; start < 1000; start += 50) {
      const url = '/voyager/api/feed/reactions?count=50&q=reactionType&start=' + start +
                  '&threadUrn=' + (post.ugc ? 'urn%3Ali%3AugcPost%3A' + post.ugc : 'urn%3Ali%3Aactivity%3A' + post.id);
      const res = await fetch(url, { headers, credentials: 'include' });
      if (!res.ok) { reactions.push({ error: 'HTTP ' + res.status }); break; }
      const json = await res.json();
      const profiles = indexProfiles(json.included);
      const batch = (json.included || []).filter(e => /feed\.social\.Reaction$/.test(e.$type || ''));
      batch.forEach(r => { const p = person(profiles[r.actorUrn]); if (p) reactions.push(p); });
      if (batch.length < 50) break;
      await pause(250);
    }

    // Comments. These DO carry createdTime, which is what lets you catch
    // in-window comments on posts published before the window.
    for (let start = 0; start < 1000; start += 50) {
      const url = '/voyager/api/feed/comments?count=50&q=comments' +
                  '&sortOrder=REVERSE_CHRONOLOGICAL&start=' + start +
                  '&updateId=' + (post.ugc ? 'ugcPost%3A' + post.ugc : 'activity%3A' + post.id);
      const res = await fetch(url, { headers, credentials: 'include' });
      if (!res.ok) { comments.push({ error: 'HTTP ' + res.status }); break; }
      const json = await res.json();
      const profiles = indexProfiles(json.included);
      const batch = (json.included || []).filter(e => /feed\.Comment$/.test(e.$type || ''));
      batch.forEach(c => {
        const urn = c.commenter && c.commenter['*miniProfile'];
        const p = person(profiles[urn]);
        if (p) comments.push({ ...p, at: c.createdTime ? new Date(c.createdTime).toISOString() : null });
      });
      if (batch.length < 50) break;
      await pause(250);
    }

    window.__engagers[post.id] = { ...post, reactions, comments };
    try { localStorage.setItem('__aba_engagers', JSON.stringify(window.__engagers)); } catch (e) {}
    await pause(400);
  }

  // One row per person across all posts, carrying every post they engaged on.
  // Repeat engagement is the signal the tables sort on, so it is kept here
  // rather than re-derived later. Rebuilt each call from everything pulled so far.
  const people = {};
  Object.values(window.__engagers).forEach(p => {
    [...p.reactions.map(r => [r, 'reacted']), ...p.comments.map(c => [c, 'commented'])].forEach(([x, src]) => {
      if (!x || !x.slug) return;
      const q = people[x.slug] = people[x.slug] || { name: x.name, id: x.slug, headline: x.headline, sources: [], posts: [] };
      if (!q.sources.includes(src)) q.sources.push(src);
      if (!q.posts.includes(p.date)) q.posts.push(p.date);
    });
  });
  window.__engagerPeople = Object.values(people);
  try { localStorage.setItem('__aba_engagerPeople', JSON.stringify(window.__engagerPeople)); } catch (e) {}

  // Compare per-post counts against the totals LinkedIn shows on each post. An
  // exact match means the pull is complete; short means pagination stopped early.
  return {
    pulled: todo.map(p => { const e = window.__engagers[p.id]; return p.date + ' ' + e.reactions.length + '/' + e.comments.length; }),
    remaining: POSTS.filter(p => !window.__engagers[p.id]).length,
    people: window.__engagerPeople.length
  };
};
