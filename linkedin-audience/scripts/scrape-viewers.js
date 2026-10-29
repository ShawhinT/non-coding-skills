// Harvest the "Who's viewed your profile" list (Premium).
//
// Run on https://www.linkedin.com/analytics/profile-views/ AFTER setting the
// date filter (14 days is the shortest option above a week — there is no 7).
//
// This script does NOT scroll. LinkedIn's infinite-scroll loader ignores
// window.scrollTo and element.scrollTop, so scrolling has to be driven from the
// tool layer with `computer` { action: "scroll" }. The list also virtualizes —
// offscreen rows are unmounted — so rows must be accumulated as they render.
//
// Usage:
//   1. Run this file once. It installs window.__harvest() and returns a first count.
//   2. Alternate: computer scroll down ~10 ticks, wait ~2s, call window.__harvest().
//   3. Stop when __harvest() reports an entry older than your window (`oldest`),
//      NOT when the count stops changing — a stalled loader looks identical to a
//      finished list. See linkedin-post-analytics/references/troubleshooting.md.
//   4. Read results from window.__pv; dump in slices to avoid output truncation.

(() => {
  window.__pv = window.__pv || {};

  window.__harvest = () => {
    const main = document.querySelector('main');
    if (!main) return { error: 'No <main> — wrong page?' };

    // Anchor on the "Viewed Nd ago" leaf, then walk up to the row container.
    const stamps = [...main.querySelectorAll('*')].filter(
      el => el.children.length === 0 && /^Viewed .{1,22} ago$/.test(el.textContent.trim())
    );

    stamps.forEach(stamp => {
      let row = stamp;
      for (let i = 0; i < 5 && row.parentElement; i++) row = row.parentElement;

      const link = row.querySelector('a[href*="/in/"]');
      const lines = row.innerText.split('\n').map(s => s.trim()).filter(Boolean);
      const name = lines[0];
      const when = stamp.textContent.trim().replace('Viewed ', '').replace(' ago', '');

      const headline = lines.find(s =>
        s !== name && s.length > 3 &&
        !/^•|^Viewed|mutual connection|^Message$|^Connect$|^Follow$|^Search$|^Accept$|^Pending$|^Status is/.test(s)
      ) || '';

      // Anonymous viewers have no profile link — they show as "Someone at X" or
      // a job-title-and-industry string. Keep them: they are the gap between
      // what you can name and what the panel's headline total counts.
      const url = link ? link.getAttribute('href').replace(/\?.*/, '') : null;
      const key = url || ('anon:' + name + '|' + when);

      if (!window.__pv[key]) {
        window.__pv[key] = { name, when, url, named: !!url, headline: headline.slice(0, 90) };
      }
    });

    const rows = Object.values(window.__pv);
    try { localStorage.setItem('__pvData', JSON.stringify(rows)); } catch (e) {}

    return {
      total: rows.length,
      named: rows.filter(r => r.named).length,
      anonymous: rows.filter(r => !r.named).length,
      oldest: rows.length ? rows[rows.length - 1].when : null
    };
  };

  return JSON.stringify(window.__harvest());
})();
