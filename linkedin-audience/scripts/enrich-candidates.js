// Enrich a candidate list from LinkedIn alone: current role and company,
// company headcount / HQ / tagline, and connection degree. No Apollo.
//
// Run via javascript_tool on any linkedin.com page. Input is
// window.__CANDIDATES = [{ name, id, headline, source }, ...] where `source`
// is one of reacted / commented / followed / viewed (a person can carry
// several — pass a "sources" array or join with "+"). `id` may be a vanity slug
// or an ACoAA… member URN, but only the URN works everywhere: positionGroups
// takes either, the degree endpoint takes the URN alone. The URN is harvested
// out of the positionGroups response and reused, so mixed id forms are fine on
// the way in.
//
// Three endpoints, all legacy Voyager, all cheap:
//   /voyager/api/identity/profiles/<id>/positionGroups
//       -> Position entities; the one without timePeriod.endDate is current.
//          MiniCompany entities carry universalName (the company slug).
//   /voyager/api/organization/companies?q=universalName&universalName=<slug>
//       -> staffCount, staffCountRange, headquarter, industries, tagline,
//          description. This is where size and geography come from.
//   /voyager/api/voyagerRelationshipsDashMemberRelationships/urn:li:fsd_memberRelationship:<ACoAA…>
//       -> *connection (1st, with createdAt) or DISTANCE_n. 403s on a slug.
//
// Don't reach for /identity/profiles/<id> or /networkinfo as a fallback — both
// are 410 Gone. See linkedin-post-analytics/references/troubleshooting.md.
//
// A headline pre-filter runs first so the expensive calls hit ~40% of the
// list. It only removes people with no employer to qualify (students,
// job-seekers, self-described freelancers); anyone ambiguous goes through.
//
// Resumable: progress lives on window.__enriched and localStorage under
// namespaced __aba_* keys (a bare key collided with LinkedIn's own state once).
// Call with a limit and re-run until `remaining` is 0 — javascript_tool times
// out on a full 150-person pass.
//
//   window.__CANDIDATES = [...]; then paste this file; then re-run
//   `JSON.stringify(await window.__enrich(20))` until remaining is 0.

window.__enriched = window.__enriched || JSON.parse(localStorage.getItem('__aba_enriched') || '{}');
window.__orgs     = window.__orgs     || JSON.parse(localStorage.getItem('__aba_orgs') || '{}');

window.__enrich = async (limit = 20) => {
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  const H = { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0',
              'accept': 'application/vnd.linkedin.normalized+json+2.1' };
  const pause = ms => new Promise(r => setTimeout(r, ms));

  const OUT = /\b(student|aspiring|undergrad|intern|freelancer?|self[- ]employed|open to work|seeking)\b|bachelor of|i want to be/i;

  const todo = (window.__CANDIDATES || []).filter(c => !window.__enriched[c.id]).slice(0, limit);

  for (const c of todo) {
    if (OUT.test(c.headline || '')) {
      window.__enriched[c.id] = { ...c, skipped: 'headline' };
      continue;
    }
    const rec = { ...c };
    try {
      // current position
      const pr = await fetch('/voyager/api/identity/profiles/' + encodeURIComponent(c.id) + '/positionGroups',
                             { headers: H, credentials: 'include' });
      if (pr.ok) {
        const raw = await pr.text();
        // The member URN, harvested here because this response is the only
        // cheap place it appears. The degree endpoint below 403s on a vanity
        // slug and accepts only this ACoAA… form — followers already arrive
        // as URNs, so without this every engager and viewer loses its degree.
        rec.urn = (raw.match(/ACoAA[A-Za-z0-9_-]+/) || [])[0] || (/^ACoAA/.test(c.id) ? c.id : '');
        const j = JSON.parse(raw); const inc = j.included || [];
        const mc = {}; inc.filter(e => /MiniCompany$/.test(e.$type || '')).forEach(m => mc[m.entityUrn] = m.universalName);
        const pos = inc.filter(e => /\.Position$/.test(e.$type || ''));
        // Current = an open-ended position. No fallback to pos[0]: when every
        // position has ended, the person has no employer to qualify, and an old
        // job read as current puts them at a company they left years ago.
        // Several open-ended positions are common (a day job plus a board seat,
        // a side business, a conference). The first one returned is not the
        // main one, so prefer the position whose company the headline names —
        // that's the employer the person leads with — then the latest start.
        const open = pos.filter(p => !(p.timePeriod && p.timePeriod.endDate));
        const hl = (c.headline || '').toLowerCase();
        const started = p => { const d = (p.timePeriod || {}).startDate || {}; return (d.year || 0) * 12 + (d.month || 0); };
        const cur = open.find(p => p.companyName && hl.includes(p.companyName.toLowerCase().replace(/,? (llc|inc\.?|ltd\.?)$/, '')))
                 || open.sort((a, b) => started(b) - started(a))[0];
        if (!cur) { window.__enriched[c.id] = { ...rec, skipped: 'no current position' }; await pause(180); continue; }
        rec.title = cur ? cur.title : '';
        rec.company = cur ? cur.companyName : '';
        rec.companySlug = (cur && mc[cur['*company'] || cur.companyUrn]) || '';
      }
      await pause(180);

      // company record (cached per slug — many candidates share employers)
      if (rec.companySlug) {
        if (!window.__orgs[rec.companySlug]) {
          const cr = await fetch('/voyager/api/organization/companies?q=universalName&universalName=' + encodeURIComponent(rec.companySlug),
                                 { headers: H, credentials: 'include' });
          if (cr.ok) {
            const j = await cr.json();
            const o = (j.included || []).find(e => /organization\.Company$/.test(e.$type || '')) || {};
            const hq = o.headquarter || {};
            window.__orgs[rec.companySlug] = {
              name: o.name || '', staff: o.staffCount ?? null,
              range: o.staffCountRange ? [o.staffCountRange.start, o.staffCountRange.end ?? null] : null,
              country: hq.country || '', city: hq.city || '',
              industries: (o.industries || []).slice(0, 2),
              tagline: (o.tagline || '').slice(0, 100),
              description: (o.description || '').replace(/\s+/g, ' ').slice(0, 200)
            };
          }
          await pause(180);
        }
        Object.assign(rec, { org: window.__orgs[rec.companySlug] || null });
      }

      // degree — keyed on the member URN resolved above, never on the slug
      const rr = await fetch('/voyager/api/voyagerRelationshipsDashMemberRelationships/urn%3Ali%3Afsd_memberRelationship%3A' + encodeURIComponent(rec.urn || c.id),
                             { headers: H, credentials: 'include' });
      if (!rr.ok) rec.degree = '?';
      if (rr.ok) {
        const j = await rr.json(); const u = (j.data || {}).memberRelationshipUnion || {};
        if (u['*connection']) {
          const conn = (j.included || []).find(e => /fsd_connection/.test(e.entityUrn || ''));
          rec.degree = '1st'; rec.connectedAt = conn && conn.createdAt ? new Date(conn.createdAt).toISOString().slice(0, 10) : null;
        } else {
          const m = JSON.stringify(u).match(/DISTANCE_(\d)/);
          rec.degree = m ? m[1] + (m[1] === '2' ? 'nd' : 'rd') : '3rd+';
        }
      }
      await pause(180);
    } catch (e) { rec.error = String(e).slice(0, 80); }
    window.__enriched[c.id] = rec;
  }

  try {
    localStorage.setItem('__aba_enriched', JSON.stringify(window.__enriched));
    localStorage.setItem('__aba_orgs', JSON.stringify(window.__orgs));
  } catch (e) {}

  const all = Object.values(window.__enriched);
  return {
    done: all.length,
    remaining: (window.__CANDIDATES || []).length - all.length,
    skipped: all.filter(r => r.skipped).length,
    orgs: Object.keys(window.__orgs).length
  };
};

// First-pass filters that need no judgment. Everything that survives goes to
// the ICP scoring step, which is done by reading, not by regex.
// min and max come from the ICP page each run (its tolerance included) — no
// defaults here, so a band copied from an old page can't keep filtering.
// Headcount is LinkedIn's member count; the declared range is the fallback
// only when that count is missing.
window.__inBand = (min, max) => {
  if (!(min > 0 && max > min)) throw new Error('__inBand(min, max): pass the size bounds from the ICP page');
  return Object.values(window.__enriched)
  .filter(r => !r.skipped && r.org)
  .filter(r => r.org.country === 'US')
  .filter(r => r.org.staff != null ? (r.org.staff >= min && r.org.staff <= max)
                                    : (r.org.range && r.org.range[0] <= max && (r.org.range[1] ?? Infinity) >= min))
  .map(r => ({ name: r.name, id: r.id, title: r.title, company: r.org.name, staff: r.org.staff,
               city: r.org.city, tagline: r.org.tagline, description: r.org.description,
               engaged: r.source, degree: r.degree, connectedAt: r.connectedAt || '' }));
};

JSON.stringify(await window.__enrich(20));
