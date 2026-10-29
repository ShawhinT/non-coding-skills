// New followers for a window, dated by the memberRelationship API.
//
// Run via javascript_tool on
//   https://www.linkedin.com/mynetwork/network-manager/people-follow/followers/
//
// LinkedIn dates followers nowhere in the UI, but nearly every follower who
// matters is also a connection (connecting auto-follows), and the
// memberRelationship endpoint returns a connection's createdAt. So: page the
// followers list (newest first), look each one up, and stop at the first
// connection older than the window. That call also returns the degree, which
// the deliverable needs anyway.
//
// Non-connection followers can't be dated this way. They keep flowing into
// the candidate list until the stop condition fires, and are dated as
// "in window" by position. In practice that tail is students, job-seekers and
// freelancers; if it ever isn't, the notifications feed is the fallback.
//
// Set window.__WINDOW_DAYS first (default 7). Results land on window.__followers
// and in localStorage.__aba_followers. Keys are namespaced — LinkedIn keeps its
// own state in localStorage and a bare key like __co collides with it.
//
// The IIFE is awaited: an un-awaited async IIFE serializes as {}.

await (async () => {
  const DAYS = window.__WINDOW_DAYS || 7;
  const cutoff = Date.now() - DAYS * 864e5;
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  if (!csrf) return JSON.stringify({ error: 'No JSESSIONID cookie' });
  const H = { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0',
              'accept': 'application/vnd.linkedin.normalized+json+2.1' };

  // Followers list rows: name + headline + /in/<id> link. The id is usually an
  // opaque ACoAA… member URN rather than a vanity slug; every Voyager endpoint
  // used here accepts either form.
  const readList = () => {
    const seen = {}, order = [];
    document.querySelectorAll('main a[href*="/in/"]').forEach(a => {
      const id = (a.getAttribute('href').match(/\/in\/([^\/?]+)/) || [])[1];
      if (!id || seen[id]) return;
      let row = a; for (let i = 0; i < 6 && row.parentElement; i++) row = row.parentElement;
      // Presence badges render as text ("Status is online", "Status is reachable")
      // ahead of the name; drop them or they become the person's name and break
      // the name-based dedupe later.
      const lines = (row.innerText || '').split('\n').map(s => s.trim()).filter(s => s && !/^Status is /.test(s));
      if (!lines.length || /^(Follow|Following|Message)$/.test(lines[0])) return;
      const headline = lines.find(s => s !== lines[0] && s.length > 3 &&
        !/^•|^Follow|^Following$|^Message$|followers?$/.test(s)) || '';
      seen[id] = { name: lines[0], id, headline: headline.slice(0, 120) };
      order.push(id);
    });
    return order.map(k => seen[k]);
  };

  const relationship = async (id) => {
    const r = await fetch('/voyager/api/voyagerRelationshipsDashMemberRelationships/urn%3Ali%3Afsd_memberRelationship%3A' + id,
                          { headers: H, credentials: 'include' });
    if (!r.ok) return { degree: '?', connectedAt: null };
    const j = await r.json();
    const u = (j.data || {}).memberRelationshipUnion || {};
    if (u['*connection']) {
      const c = (j.included || []).find(e => /fsd_connection/.test(e.entityUrn || ''));
      return { degree: '1st', connectedAt: c && c.createdAt ? c.createdAt : null };
    }
    const m = JSON.stringify(u).match(/DISTANCE_(\d)/);
    return { degree: m ? m[1] + (m[1] === '2' ? 'nd' : 'rd') : '3rd+', connectedAt: null };
  };

  const out = [];
  let stop = false;
  for (let page = 0; page < 15 && !stop; page++) {
    const rows = readList();
    for (const p of rows.slice(out.length)) {
      const rel = await relationship(p.id);
      if (rel.connectedAt && rel.connectedAt < cutoff) { stop = true; break; }
      out.push({ ...p, ...rel, source: 'followed' });
      await new Promise(r => setTimeout(r, 200));
    }
    if (stop) break;
    const more = [...document.querySelectorAll('button')].find(b => /show more/i.test(b.innerText || ''));
    if (!more) break;
    more.click();                                   // a real .click() works on this page
    await new Promise(r => setTimeout(r, 1800));
  }

  window.__followers = out;
  try { localStorage.setItem('__aba_followers', JSON.stringify(out)); } catch (e) {}
  return JSON.stringify({
    inWindow: out.length,
    connections: out.filter(p => p.degree === '1st').length,
    undated: out.filter(p => !p.connectedAt).length,
    stoppedOn: stop ? 'connection older than window' : 'end of list / page cap'
  });
})();
