// New 1st-degree connections for a window, with exact connection dates.
//
// Run via javascript_tool on any linkedin.com page (the connections page is a
// natural home: /mynetwork/invite-connect/connections/).
//
// The connections page UI lazy-loads and ignores scripted scrolling, but the
// Voyager endpoint behind it returns connections newest-first with createdAt,
// 40 per call. Page until the oldest connection is past the window.
//
// ids come back as ACoAA… member URNs — the same form walk-followers.js
// produces — so the two sources dedupe on id directly. `slug` (vanity) is kept
// for building profile links.
//
// Set window.__WINDOW_DAYS first (default 7). Results land on window.__connected
// and in localStorage.__aba_connected. The IIFE is awaited: an un-awaited async
// IIFE serializes as {}.

await (async () => {
  const DAYS = window.__WINDOW_DAYS || 7;
  const cutoff = Date.now() - DAYS * 864e5;
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  if (!csrf) return JSON.stringify({ error: 'No JSESSIONID cookie' });
  const H = { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0',
              'accept': 'application/vnd.linkedin.normalized+json+2.1' };

  const out = [];
  for (let start = 0; start < 400; start += 40) {
    const r = await fetch('/voyager/api/relationships/dash/connections' +
      '?decorationId=com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-16' +
      '&count=40&q=search&sortType=RECENTLY_ADDED&start=' + start,
      { headers: H, credentials: 'include' });
    if (!r.ok) return JSON.stringify({ error: 'HTTP ' + r.status, start });
    const inc = (await r.json()).included || [];
    const profiles = {};
    inc.filter(e => /Profile$/.test(e.$type || '')).forEach(p => profiles[p.entityUrn] = p);
    const conns = inc.filter(e => /Connection$/.test(e.$type || ''));
    if (!conns.length) break;
    for (const c of conns) {
      const p = profiles[c['*connectedMemberResolutionResult'] || c.connectedMember] || {};
      out.push({
        id: (p.entityUrn || '').split(':').pop(),
        slug: p.publicIdentifier || '',
        name: ((p.firstName || '') + ' ' + (p.lastName || '')).trim(),
        headline: (p.headline || '').slice(0, 120),
        connectedAt: c.createdAt, degree: '1st', source: 'connected'
      });
    }
    if (Math.min(...conns.map(c => c.createdAt)) < cutoff) break;
    await new Promise(r => setTimeout(r, 400));
  }

  const inWindow = out.filter(p => p.connectedAt >= cutoff)
                      .sort((a, b) => b.connectedAt - a.connectedAt);
  window.__connected = inWindow;
  try { localStorage.setItem('__aba_connected', JSON.stringify(inWindow)); } catch (e) {}
  return JSON.stringify({ inWindow: inWindow.length, fetched: out.length });
})();
