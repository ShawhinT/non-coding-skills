// Pull a poll's complete voter list by paging the endpoint behind its
// "N votes" dialog (author-only view).
//
// Poll votes are not reactions or comments, so scrape-engagers.js never sees
// them. LinkedIn shows the voter list only to the poll's author, in a dialog
// with one tab per option.
//
// Why page the endpoint instead of scrolling the dialog: the dialog asks for
// 10 voters at a time and stops loading as soon as a page comes back short.
// LinkedIn withholds some voters (a page of 10 arrives as 9), so a tab with 30
// voters can stop at 9 and no amount of scrolling moves it. The endpoint itself
// keeps answering for later start indexes; only the dialog's loader gives up.
//
// The request can't be built from scratch — it carries page-instance headers
// and an actor binding — so borrow a real one and replay it per option.
//
// Usage (on https://www.linkedin.com/feed/update/urn:li:activity:<poll id>/):
//   1. Run this file once, BEFORE opening the dialog. It installs a fetch
//      wrapper that keeps the dialog's own pagination request.
//   2. Open the dialog: click the "N votes" link under the poll with `computer`,
//      by coordinate read off a screenshot (a scripted .click() and a ref click
//      both fail to open it).
//   3. Scroll the list once with `computer` (~10 ticks) on a tab holding more
//      than 10 voters, so the dialog fires one pagination request.
//   4. `await window.__sweepPoll('<label>')` — pages every option from index 0
//      until a page comes back empty, and returns per-option counts.
//      Compare them with the numbers on the tabs: a tab may be short by the
//      voters LinkedIn withholds, never by a whole page.
//
// If no tab holds more than 10 voters, no pagination request ever fires and
// __sweepPoll says so. Every tab is then fully rendered already: click through
// the tabs and call window.__harvestVotes('<option>') on each instead.
//
// Voters land on window.__voters (keyed by /in/ id, vanity slug or ACoAA urn)
// and localStorage.__aba_voters. Feed them into the candidate union with
// source 'voted'. Headlines come back empty from the endpoint; enrichment
// supplies the current position, which is what the table uses anyway.

(() => {
  window.__voters = window.__voters || JSON.parse(localStorage.getItem('__aba_voters') || '{}');
  const save = () => { try { localStorage.setItem('__aba_voters', JSON.stringify(window.__voters)); } catch (e) {} };

  // 1. Keep the dialog's own pagination request (url, headers, body).
  if (!window.__pollFetch) {
    window.__pollFetch = window.fetch;
    window.__pollReq = null;
    window.fetch = function (u, o) {
      const url = typeof u === 'string' ? u : (u && u.url) || '';
      if (/rsc-action\/actions\/pagination/.test(url) && o && typeof o.body === 'string' && /pollOptionId/.test(o.body)) {
        window.__pollReq = {
          url, body: o.body,
          headers: o.headers instanceof Headers ? Object.fromEntries(o.headers.entries()) : o.headers
        };
      }
      return window.__pollFetch.apply(this, arguments);
    };
  }

  const dialog = () => {
    const h = [...document.querySelectorAll('h1,h2,h3')].find(e => /^Votes$/.test(e.innerText.trim()));
    let m = h;
    while (m && !(m.querySelectorAll('a[href*="/in/"]').length && /\d+\s*\n/.test(m.innerText))) m = m.parentElement;
    return m;
  };

  // Option ids are not in the DOM; they sit in the React props of the dialog.
  // Collect every id minted alongside the poll (same leading digits) and let
  // the endpoint sort them out — an id that isn't an option returns no voters.
  const optionCandidates = (pollId) => {
    const d = dialog(); if (!d) return [];
    const found = new Set(), seen = new WeakSet();
    const scan = (o, depth) => {
      if (!o || depth > 7) return;
      if (typeof o === 'string') { (o.match(/\d{19}/g) || []).forEach(x => found.add(x)); return; }
      if (typeof o !== 'object' || seen.has(o) || o instanceof Node) return;
      seen.add(o);
      let n = 0;
      for (const k in o) {
        if (/^(return|_owner|stateNode|alternate|sibling|child)$/.test(k)) continue;
        if (n++ > 60) break;
        try { scan(o[k], depth + 1); } catch (e) {}
      }
    };
    [d, ...d.querySelectorAll('*')].forEach(el => Object.keys(el).forEach(k => {
      if (k.startsWith('__reactFiber')) {
        let f = el[k];
        for (let i = 0; i < 6 && f; i++) { scan(f.memoizedProps, 0); scan(f.memoizedState, 0); f = f.return; }
      } else if (k.startsWith('__reactProps')) scan(el[k], 0);
    }));
    return [...found].filter(x => x !== pollId && x.slice(0, 9) === pollId.slice(0, 9));
  };

  const page = async (optionId, start) => {
    const c = window.__pollReq, b = JSON.parse(c.body);
    b.clientArguments.payload.pollOptionId = optionId;
    b.clientArguments.payload.startIndex = start;
    const r = await window.__pollFetch(c.url, { method: 'POST', headers: c.headers, body: JSON.stringify(b), credentials: 'include' });
    if (!r.ok) return { error: 'HTTP ' + r.status };
    // The response is a React server-component stream. Each voter is a profile
    // url followed by text nodes shaped [null,"<text>",null]; the first is the name.
    const rows = (await r.text()).split('https://www.linkedin.com/in/').slice(1).map(p => {
      const id = decodeURIComponent(p.split(/[\/"\\]/)[0]);
      const texts = [...p.matchAll(/\[null,"((?:[^"\\]|\\.)+)",null\]/g)].map(m => m[1]);
      return { id, name: (texts[0] || '').trim() };
    });
    return { rows };
  };

  window.__sweepPoll = async (label = 'poll') => {
    if (!window.__pollReq) return JSON.stringify({ error: 'No pagination request captured — scroll a tab with more than 10 voters, or use __harvestVotes per tab if none has that many' });
    const payload = JSON.parse(window.__pollReq.body).clientArguments.payload;
    const options = [...new Set([payload.pollOptionId, ...optionCandidates(payload.pollId)])];
    const counts = {};
    for (const opt of options) {
      const got = {};
      for (let start = 0; start < 2000; start += payload.pageSize || 10) {
        const res = await page(opt, start);
        if (res.error) { counts[opt] = res.error; break; }
        if (!res.rows.length) break;          // an empty page is the end; a short one is not
        res.rows.forEach(r => { got[r.id] = r; });
        await new Promise(r => setTimeout(r, 300));
      }
      const n = Object.keys(got).length;
      if (!n) continue;                       // not an option of this poll
      counts[opt] = n;
      Object.values(got).forEach(r => {
        const v = window.__voters[r.id] = window.__voters[r.id] || { id: r.id, source: 'voted', name: r.name, degree: '', headline: '', polls: [] };
        if (!v.name) v.name = r.name;
        v.polls = v.polls || [];
        if (!v.polls.includes(label)) v.polls.push(label);
        v.option = label + ':' + opt;
      });
    }
    save();
    return JSON.stringify({ perOption: counts, pollTotal: Object.values(counts).filter(Number.isFinite).reduce((a, b) => a + b, 0), votersSoFar: Object.keys(window.__voters).length });
  };

  // Fallback for polls where every tab fits on one page: read the open tab.
  window.__harvestVotes = (option) => {
    const d = dialog();
    if (!d) return JSON.stringify({ error: 'Votes dialog not open' });
    const idOf = a => (a.getAttribute('href').match(/\/in\/([^\/?]+)/) || [])[1];
    let inTab = 0;
    new Set([...d.querySelectorAll('a[href*="/in/"]')].map(idOf)).forEach(() => inTab++);
    d.querySelectorAll('a[href*="/in/"]').forEach(a => {
      const id = idOf(a);
      if (!id || window.__voters[id]) return;
      // The row is the largest ancestor that still holds links to this one
      // person only. A fixed number of parent hops overshoots into the option
      // tabs and reads a tab label as the name.
      let row = a;
      while (row.parentElement && d.contains(row.parentElement) &&
             new Set([...row.parentElement.querySelectorAll('a[href*="/in/"]')].map(idOf)).size === 1) row = row.parentElement;
      const lines = (row.innerText || '').split('\n').map(s => s.trim()).filter(Boolean);
      const first = lines[0] || '';
      window.__voters[id] = {
        id, option, source: 'voted',
        name: first.replace(/\s*[•·].*$/, ''),
        degree: (first.match(/[•·]\s*(1st|2nd|3rd\+?)/) || [])[1] || '',
        headline: (lines[1] || '').slice(0, 100)
      };
    });
    save();
    return JSON.stringify({ inTab, votersSoFar: Object.keys(window.__voters).length });
  };

  return JSON.stringify({ installed: true, dialogOpen: !!dialog(), requestCaptured: !!window.__pollReq });
})();
