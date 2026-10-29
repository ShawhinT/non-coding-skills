// Pending received connection invitations — the whole backlog — with each
// sender's own location.
//
// Run via javascript_tool on any linkedin.com page (the invitation manager is
// a natural home: /mynetwork/invitation-manager/received/).
//
// Two passes, because they cost very differently:
//
//   1. await window.__pullInvites()        — one call per 100 invites.
//   2. await window.__locateInvites()      — one profile call per person;
//      re-run until `remaining` is 0 (javascript_tool times out ~45s).
//
// Pass 1: the invitationViews endpoint returns every pending invite, newest
// first. Page and newsletter invites ride the same endpoint
// (invitationType ORGANIZATION / CONTENT_SERIES); only PENDING are people.
// sentTime is epoch ms. No window applies: an invite stays live until Shaw
// acts on it, so an old one is as workable as yesterday's.
//
// Pass 2: the sender's location comes from identity/dash/profiles with the
// WebTopCardCore decoration (its Geo entities). The older
// identity/profiles/{slug} endpoint returns 410. Profile lookups are rate
// limited: four in parallel drew 429s after ~200 calls and stayed blocked for
// a minute; sequential at ~1.3s sustained well over 150. On a 429 the pass
// stops and keeps its progress — wait a minute and re-run.
//
// Results: window.__invites and localStorage.__aba_invites. Each row:
// { t, name, headline, slug, msg, loc }. `msg` is the invite note — a pitch
// there marks a seller. `slug` is a vanity id, so invite rows dedupe against
// engagers/viewers directly and against followers/connections after
// enrichment, like the other sources.

window.__invites = window.__invites || JSON.parse(localStorage.getItem('__aba_invites') || '[]');

const __abaHeaders = () => {
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  return { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0',
           'accept': 'application/vnd.linkedin.normalized+json+2.1' };
};

window.__pullInvites = async () => {
  const H = __abaHeaders();
  const known = Object.fromEntries(window.__invites.map(x => [x.slug, x]));
  const out = [];
  for (let start = 0; start < 1000; start += 100) {
    const r = await fetch(`/voyager/api/relationships/invitationViews?q=receivedInvitation&start=${start}&count=100&includeInsights=true`,
                          { headers: H, credentials: 'include' });
    if (!r.ok) return { error: r.status, pulled: out.length };
    const inc = (await r.json()).included || [];
    const prof = Object.fromEntries(inc.filter(e => /MiniProfile$/.test(e.$type || '')).map(e => [e.entityUrn, e]));
    const invs = inc.filter(e => /\.Invitation$/.test(e.$type || ''));
    for (const v of invs.filter(v => v.invitationType === 'PENDING')) {
      const p = prof[v['*fromMember']] || {};
      if (!p.publicIdentifier) continue;
      const prev = known[p.publicIdentifier] || {};
      out.push({ t: v.sentTime, name: `${p.firstName || ''} ${p.lastName || ''}`.trim(),
                 headline: p.occupation || '', slug: p.publicIdentifier,
                 msg: v.message || '', loc: prev.loc });
    }
    if (invs.length < 100) break;
    await new Promise(r => setTimeout(r, 400));
  }
  window.__invites = out.sort((a, b) => b.t - a.t);
  localStorage.setItem('__aba_invites', JSON.stringify(window.__invites));
  return { pending: out.length, oldest: new Date(Math.min(...out.map(x => x.t))).toISOString().slice(0, 10) };
};

window.__locateInvites = async (budgetMs = 38000, gapMs = 1300) => {
  const H = __abaHeaders();
  const t0 = Date.now();
  let done = 0, limited = false;
  for (const x of window.__invites.filter(x => !x.loc)) {
    if (Date.now() - t0 > budgetMs) break;
    const r = await fetch(`/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=${encodeURIComponent(x.slug)}` +
                          `&decorationId=com.linkedin.voyager.dash.deco.identity.profile.WebTopCardCore-19`,
                          { headers: H, credentials: 'include' });
    if (r.status === 429) { limited = true; break; }
    const inc = r.ok ? ((await r.json()).included || []) : [];
    x.loc = inc.filter(e => /\.Geo$/.test(e.$type || '')).map(e => e.defaultLocalizedName).join(' / ') || '?';
    done++;
    await new Promise(r => setTimeout(r, gapMs));
  }
  localStorage.setItem('__aba_invites', JSON.stringify(window.__invites));
  return { done, limited, remaining: window.__invites.filter(x => !x.loc).length };
};

// After both passes: filter on location against the sweep's geography, e.g.
//   const ok = /United States|Canada|United Kingdom|Germany|France|…/;
//   window.__invites.filter(x => ok.test(x.loc))
// Match country names, not loose words — "Greater Bengaluru Area" is not a
// US metro.
