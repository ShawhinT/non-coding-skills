// Event Finder crawler — paste into the browser JS tool on any eventbrite.com page.
// Starts a background crawl and returns immediately. Then call:
//   EF.status()            -> progress / done
//   EF.rank()              -> classify + distance; returns counts per category
//   EF.page(cat, start, n) -> compact lines "mi|MM-DD HH:MM|city|title|id" (cat: 'AI'|'Tech'|'Biz'|'all')
//   EF.detail([ids])       -> "id|time|venue|summary" for a shortlist
// Output from the JS tool truncates near ~1000 chars: read in slices of 12-15.

const CONFIG = {
  locations: ['tx--frisco', 'tx--plano', 'tx--dallas'],
  slugs: ['ai', 'artificial-intelligence', 'tech', 'startups', 'science-and-tech--events', 'business--networking', 'networking'],
  start: '2026-10-15',   // set to today (America/Chicago)
  end: '2027-01-15',     // default: +3 months
  pagesPerQuery: 4,
  home: [33.085, -96.81], // Frisco/Plano (Legacy)
};

window.EF = (() => {
  const S = { cfg: CONFIG, ev: {}, log: [], done: false, ranked: [] };

  async function getServerData(path) {
    const h = await fetch(path).then(r => r.text());
    const i = h.indexOf('__SERVER_DATA__ = ') + 18;
    let s = h.slice(i, h.indexOf('</script>', i));
    const k = s.indexOf('};\n'); // JSON is followed by more JS; cut at the first top-level close
    s = k > 0 ? s.slice(0, k + 1) : s.slice(0, s.lastIndexOf('}') + 1);
    return JSON.parse(s);
  }

  async function crawl() {
    const c = S.cfg, D = `start_date=${c.start}&end_date=${c.end}`;
    for (const loc of c.locations) for (const q of c.slugs) {
      for (let p = 1; p <= c.pagesPerQuery; p++) {
        try {
          const ev = (await getServerData(`/d/${loc}/${q}/?${D}&page=${p}`)).search_data.events;
          for (const e of [...ev.results, ...(ev.promoted_results || [])]) {
            if (e.is_online_event) continue;
            const v = e.primary_venue || {}, a = v.address || {};
            const r = S.ev[e.id] ||= {
              id: String(e.eventbrite_event_id || e.id), n: e.name, d: e.start_date, t: e.start_time,
              c: a.city, v: v.name, lat: +a.latitude, lon: +a.longitude, u: e.url,
              tags: (e.tags || []).map(t => t.display_name).join('/'), s: (e.summary || '').slice(0, 160), q: [],
            };
            if (!r.q.includes(q)) r.q.push(q);
          }
          S.log.push(`${loc}/${q}/${p}:${ev.results.length}/${ev.pagination.page_count}`);
          if (p >= ev.pagination.page_count) break;
        } catch (err) { S.log.push(`${loc}/${q}/${p}:ERR ${String(err.message).slice(0, 40)}`); break; }
      }
    }
    S.done = true;
  }

  const miles = (lat, lon) => {
    const [h0, h1] = S.cfg.home, R = 3959, r = x => x * Math.PI / 180;
    const h = Math.sin(r(lat - h0) / 2) ** 2 + Math.cos(r(lat)) * Math.cos(r(h0)) * Math.sin(r(lon - h1) / 2) ** 2;
    return Math.round(2 * R * Math.asin(Math.sqrt(h)));
  };
  const AI = /\bAI\b|A\.I\.|artificial intel|chatgpt|claude|\bLLM|machine learning|genai|generative|agentic|\bagents?\b|automation/i;
  const TECH = /\btech|software|startup|cyber|\bdata\b|developer|saas|innovation|\bIT\b|engineer|product manag|venture|founder|digital|pitch/i;
  const BIZ = /network|business|entrepreneur|chamber|leader|professional|ceo|executive|sales|marketing|b2b|mixer|owner/i;

  function rank() {
    S.ranked = Object.values(S.ev).filter(e => e.d >= S.cfg.start && e.d <= S.cfg.end).map(e => {
      const txt = `${e.n} ${e.s} ${e.tags}`;
      const cat = AI.test(txt) ? 'AI' : TECH.test(txt) ? 'Tech' : BIZ.test(txt) ? 'Biz' : '';
      return { ...e, cat, mi: miles(e.lat, e.lon) };
    }).filter(e => e.cat).sort((a, b) => a.mi - b.mi || a.d.localeCompare(b.d));
    const counts = {}; S.ranked.forEach(e => counts[e.cat] = (counts[e.cat] || 0) + 1);
    return JSON.stringify(counts);
  }

  const idOf = e => (e.u.match(/(\d+)$/) || [])[1] || e.id;
  const page = (cat = 'all', start = 0, n = 14, maxMi = 99) =>
    S.ranked.filter(e => (cat === 'all' || e.cat === cat) && e.mi <= maxMi).slice(start, start + n)
      .map(e => `${e.mi}|${e.d.slice(5)} ${e.t}|${(e.c || '').slice(0, 10)}|${e.n.slice(0, 45)}|${idOf(e)}`).join('\n');
  const detail = ids => ids.map(i => { const e = S.ranked.find(x => idOf(x) === i) || {};
    return `${i.slice(-4)}|${e.t}|${(e.v || '').slice(0, 30)}|${(e.s || '').slice(0, 90)}`; }).join('\n');
  const status = () => `${S.done ? 'DONE' : 'running'} events=${Object.keys(S.ev).length} pages=${S.log.length} last=${S.log.slice(-2).join(' ')}`;

  crawl();
  return { S, rank, page, detail, status };
})();
'crawl started — poll EF.status()';
