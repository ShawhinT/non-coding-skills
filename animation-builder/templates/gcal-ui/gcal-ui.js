// Google Calendar week-view builder for the scheduling demo. Loads after gcal-data.js.
//
//   buildApp(document.querySelector('.app'), {
//     duration: 4,                 // seconds; must equal render.py --duration
//     week: 0,                     // week shown at t=0 (0..2)
//     on: ['ravi'],                // teammates whose calendars are on at t=0 (viewer always on)
//     toggles: [{ id: 'claire', at: 1.6 }],   // checkbox clicks, in order
//     flips: [{ week: 1, at: 2.4 }],           // "next week" clicks
//     cursorStart: '#chk-ravi' | [x, y],      // where the cursor sits at t=0
//     cursorEnd: '#chk-claire' | null,         // optional idle target after the last action
//   })
//
// Every state change is a step animation keyed off `--d`, so render.py can seek it exactly.
// Event layout follows Calendar's cascade: overlapping chips are assigned columns by start
// time; each chip spans from its column to the right edge and later columns sit on top.

const HOUR = 53, COL = 209.7, GUTTER = 65, GRID_START = 4, GRID_END = 21;   // grid shows 4 AM–9 PM
const DOW = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const svg = (d, extra = '') => `<svg viewBox="0 0 24 24" ${extra}>${d}</svg>`;
const P = {
  burger: '<path d="M3 6h18M3 12h18M3 18h18" stroke-linecap="round"/>',
  left: '<path d="M15 5l-7 7 7 7" stroke-linecap="round" stroke-linejoin="round"/>',
  right: '<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21" stroke-linecap="round"/>',
  help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01" stroke-linecap="round"/>',
  gear: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" stroke-linejoin="round"/>',
  chev: '<path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round"/>',
  chevUp: '<path d="M6 15l6-6 6 6" stroke-linecap="round" stroke-linejoin="round"/>',
  cal: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4" stroke-linecap="round"/>',
  checkCircle: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5" stroke-linecap="round" stroke-linejoin="round"/>',
  grid9: '<circle cx="5" cy="5" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="19" cy="19" r="2"/>',
  plus: '<path d="M12 5v14M5 12h14" stroke-linecap="round"/>',
  people: '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3.3 2.6-5 5.5-5s4.9 1.7 5.5 5M15.5 5.3a3.2 3.2 0 0 1 0 5.4M17 14.2c2.2.4 3.4 2 3.8 4.8" stroke-linecap="round"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5" stroke-linecap="round" stroke-linejoin="round"/>',
  insight: '<path d="M4 18l5-6 4 3 7-9M15 6h5v5" stroke-linecap="round" stroke-linejoin="round"/>',
};
const ICON = (name, cls = '') => svg(P[name], `class="${cls}"`);

// Google Calendar product logo: blue rounded tile, white page, blue day number.
function calendarLogo(n) {
  return `<svg class="logo" viewBox="0 0 40 40"><rect width="40" height="40" rx="9" fill="#1a73e8"/><rect x="6" y="9" width="28" height="25" rx="4" fill="#fff"/><rect x="6" y="9" width="28" height="4" fill="#fff"/><text x="20" y="29" text-anchor="middle" font-family="Roboto, Arial" font-size="17" font-weight="500" fill="#1a73e8">${n}</text></svg>`;
}
// Right-rail Google apps (Keep, Tasks, Contacts, Maps) as simple colored marks.
const RAIL = [
  `<svg class="ri" viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2z" fill="#fbbc04"/><rect x="9" y="19.5" width="6" height="2.5" rx="1" fill="#f29900"/></svg>`,
  `<svg class="ri" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#4285f4"/><path d="M7.5 12.5l3 3 6-6.5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  `<svg class="ri" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4.2" fill="#1a73e8"/><path d="M4 20c.8-4.2 3.8-6.5 8-6.5s7.2 2.3 8 6.5z" fill="#1a73e8"/></svg>`,
  `<svg class="ri" viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z" fill="#34a853"/><circle cx="12" cy="9" r="2.6" fill="#fff"/></svg>`,
];

// ---- time formatting (Calendar style: "9am", "9:30am", "12pm") ----
function tm(h) {
  const hh = Math.floor(h), mm = Math.round((h - hh) * 60);
  const ap = hh >= 12 && hh < 24 ? 'pm' : 'am';
  const h12 = ((hh + 11) % 12) + 1;
  return `${h12}${mm ? ':' + String(mm).padStart(2, '0') : ''}${ap}`;
}
function range(s, e) {
  const a = tm(s), b = tm(e);
  const sa = a.slice(-2), sb = b.slice(-2);
  return sa === sb ? `${a.slice(0, -2)} – ${b}` : `${a} – ${b}`;
}
function hourLabel(h) { const h12 = ((h + 11) % 12) + 1; return `${h12} ${h >= 12 ? 'PM' : 'AM'}`; }
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const sameDay = (a, b) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

// ---- top bar ----
function topbar() {
  return `<div class="topbar">
    <div class="tb-left">
      ${ICON('burger', 'ic burger')}
      ${calendarLogo(TODAY.getDate())}
      <span class="wordmark">Calendar</span>
      <span class="pill today-btn">Today</span>
      <span class="nav"><span class="arr" id="prev"><span class="hover"></span>${ICON('left')}</span><span class="arr" id="next"><span class="hover" id="next-hover"></span>${ICON('right')}</span></span>
      <span class="title" id="title">${MONTHS[WEEK0.getMonth()]} ${WEEK0.getFullYear()}</span>
    </div>
    <div class="tb-right">
      <span class="icbtn">${ICON('search')}</span><span class="icbtn">${ICON('help')}</span><span class="icbtn">${ICON('gear')}</span>
      <span class="pill view-pill">Week ${ICON('chev')}</span>
      <span class="seg"><div class="on">${ICON('cal')}</div><div>${ICON('checkCircle')}</div></span>
      <span class="apps">${ICON('grid9')}</span>
      <span class="gpill"><span class="gword">Google</span><span class="avatar">S</span></span>
    </div>
  </div>`;
}

// ---- sidebar ----
function miniMonth(weekIdx) {
  const first = new Date(WEEK0.getFullYear(), WEEK0.getMonth(), 1);
  const start = addDays(first, -first.getDay());
  const selStart = addDays(WEEK0, weekIdx * 7);
  let cells = ['S', 'M', 'T', 'W', 'T', 'F', 'S'].map(d => `<div class="dow">${d}</div>`).join('');
  for (let i = 0; i < 42; i++) {
    const d = addDays(start, i);
    const cls = [d.getMonth() !== first.getMonth() ? 'other' : '', sameDay(d, TODAY) ? 'today' : '', weekIdx !== 0 && sameDay(d, selStart) ? 'sel' : ''].join(' ');
    cells += `<div class="${cls}">${d.getDate()}</div>`;
  }
  return `<div class="mini"><div class="mhead"><span>${MONTHS[first.getMonth()]} ${first.getFullYear()}</span><span class="arrows">${svg(P.left)}${svg(P.right)}</span></div><div class="mgrid">${cells}</div></div>`;
}
function insights(weekIdx) {
  const s = addDays(WEEK0, weekIdx * 7), e = addDays(s, 6);
  const mon = MONTHS[s.getMonth()].slice(0, 3).toUpperCase();
  const hrs = VIEWER_WEEKS[weekIdx].reduce((a, b) => a + (b.end - b.start), 0);
  return `<div class="insights"><div class="range">${mon} ${s.getDate()} – ${e.getDate()}, ${s.getFullYear()}</div><div class="hrs">${hrs % 1 ? hrs.toFixed(1) : hrs} hr in meetings (avg: 8.1 hr)</div><div class="bar" style="width:${Math.max(40, Math.min(220, hrs / 12 * 220))}px"></div><div class="more">${ICON('insight')}More insights</div></div>`;
}
function calRow(id, label, color, state, d) {
  // state: 'on' | 'off' | 'pending' (turns on at d seconds)
  const cls = state === 'pending' ? 'cal-row pending' : 'cal-row';
  const onStyle = state === 'off' ? 'style="opacity:0"' : '';
  return `<div class="${cls}" id="chk-${id}" style="--c:${color};--d:${d}s"><span class="hl"></span><span class="box"><span class="off"></span><span class="on" ${onStyle}>${ICON('check')}</span></span><span class="lbl">${label}</span></div>`;
}
function sidebar(opts, toggleAt) {
  const others = PEOPLE.map(p => {
    const st = opts.on.includes(p.id) ? 'on' : (toggleAt[p.id] != null ? 'pending' : 'off');
    return calRow(p.id, p.name, p.color, st, toggleAt[p.id] || 0);
  }).join('');
  return `<div class="side"><div class="side-scroll" id="side-scroll">
    <div class="create">${ICON('plus', 'plus')}Create${ICON('chev', 'chev')}</div>
    <div id="mini-slot">${miniMonth(opts.week)}</div>
    <div class="side-label">Meet with...</div>
    <div class="search-people">${ICON('people')}Search for people</div>
    <div class="row-head"><span>Booking pages</span><span class="acts">${ICON('plus')}</span></div>
    <div class="row-head"><span>Time Insights</span><span class="acts">${ICON('chevUp')}</span></div>
    <div id="insights-slot">${insights(opts.week)}</div>
    <div class="row-head"><span>My calendars</span><span class="acts">${ICON('chevUp')}</span></div>
    <div class="cal-list">${calRow('me', VIEWER.name, VIEWER.color, 'on', 0)}${calRow('bday', 'Birthdays', '#33b679', 'on', 0)}${calRow('tasks', 'Tasks', '#4285f4', 'on', 0)}</div>
    <div class="row-head"><span>Other calendars</span><span class="acts">${ICON('plus')}${ICON('chevUp')}</span></div>
    <div class="cal-list">${others}${calRow('holidays', 'Holidays in United States', '#0b8043', 'on', 0)}</div>
    <div style="height:20px"></div>
  </div></div>`;
}

// ---- event layout (cascade) ----
function layoutDay(evs) {
  // evs: [{start,end,...}] for one day. Returns [{ev, col, ncols}].
  const sorted = evs.slice().sort((a, b) => a.start - b.start || (b.end - b.start) - (a.end - a.start));
  const out = []; let cluster = [], colEnds = [], clusterEnd = -1;
  const flush = () => { const n = colEnds.length; for (const o of cluster) o.ncols = n; out.push(...cluster); cluster = []; colEnds = []; clusterEnd = -1; };
  for (const ev of sorted) {
    if (cluster.length && ev.start >= clusterEnd) flush();
    let c = colEnds.findIndex(e => e <= ev.start);
    if (c < 0) { c = colEnds.length; colEnds.push(ev.end); } else colEnds[c] = ev.end;
    clusterEnd = Math.max(clusterEnd, ev.end);
    cluster.push({ ev, col: c });
  }
  if (cluster.length) flush();
  return out;
}
function chip(ev, col, ncols, color) {
  const top = (ev.start - GRID_START) * HOUR, h = (ev.end - ev.start) * HOUR;
  const left = (col / ncols) * (COL - 10);
  const width = COL - 10 - left;
  const one = h < 42;
  const inner = one ? `<div class="t">${ev.title}, ${tm(ev.start)}</div>` : `<div class="t ${h >= 80 ? 'wrap' : ''}">${ev.title}</div><div class="tm">${range(ev.start, ev.end)}</div>`;
  return `<div class="ev ${one ? 'one' : ''} ${ev.tent ? 'tent' : ''}" style="top:${top}px;height:${h - 1}px;left:${left + 2}px;width:${width}px;--c:${color};z-index:${col + 1}">${inner}</div>`;
}
function eventState(weekIdx, ids) {
  const data = buildWeek(weekIdx);
  const colorOf = id => id === 'me' ? VIEWER.color : PEOPLE.find(p => p.id === id).color;
  let html = '';
  for (let d = 0; d < 7; d++) {
    const evs = [];
    for (const id of ids) for (const e of data[id]) if (e.day === d) evs.push({ ...e, color: colorOf(id) });
    const laid = layoutDay(evs);
    html += `<div style="position:absolute;left:${d * COL}px;top:0;width:${COL}px;height:${(GRID_END - GRID_START) * HOUR}px">${laid.map(o => chip(o.ev, o.col, o.ncols, o.ev.color)).join('')}</div>`;
  }
  return html;
}
function alldayRows(weekIdx, ids) {
  const rows = [];
  for (const b of ALLDAY[weekIdx] || []) {
    if (!b.span) continue;
    if (b.holiday) rows.push({ ...b, color: '#0b8043' });
    else for (const id of b.ids) if (ids.includes(id)) rows.push({ ...b, color: PEOPLE.find(p => p.id === id).color });
  }
  return rows;
}

// One full week view (header, all-day row, grid with per-state event layers).
function weekView(weekIdx, states, opts) {
  const start = addDays(WEEK0, weekIdx * 7);
  let head = '';
  for (let d = 0; d < 7; d++) {
    const day = addDays(start, d);
    head += `<div class="dcol ${sameDay(day, TODAY) ? 'is-today' : ''}"><div class="dow">${DOW[d]}</div><div class="dnum">${day.getDate()}</div></div>`;
  }
  // all-day banners: one layer per visibility state (banner count grows as people are added)
  const maxRows = Math.max(1, ...states.map(s => alldayRows(weekIdx, s.ids).length));
  const alldayH = 10 + maxRows * 26;
  const allday = states.map((s, i) => {
    const rows = alldayRows(weekIdx, s.ids);
    const next = states[i + 1];
    const anim = [i > 0 ? `appear .01s step-end ${s.at}s forwards` : '', next ? `vanish .01s step-end ${next.at}s forwards` : ''].filter(Boolean).join(', ');
    return `<div class="evstate" style="${i > 0 ? 'opacity:0;' : ''}${anim ? 'animation:' + anim : ''}">` +
      rows.map((b, r) => `<div class="banner ${b.holiday ? 'holiday' : ''}" style="--c:${b.color};left:${GUTTER + b.span[0] * COL + 2}px;width:${(b.span[1] - b.span[0] + 1) * COL - 6}px;top:${6 + r * 26}px">${b.title}</div>`).join('') + `</div>`;
  }).join('');
  let acols = '';
  for (let d = 0; d < 7; d++) acols += `<div class="acol" style="left:${GUTTER + d * COL}px"></div>`;

  // grid chrome
  const gridH = (GRID_END - GRID_START) * HOUR;
  let lines = '';
  for (let h = GRID_START; h <= GRID_END; h++) {
    const y = (h - GRID_START) * HOUR;
    lines += `<div class="hline" style="top:${y}px"></div>`;
    if (h > GRID_START && h < GRID_END) lines += `<div class="hlabel" style="top:${y}px">${hourLabel(h)}</div>`;
  }
  for (let d = 0; d <= 7; d++) lines += `<div class="vline" style="left:${GUTTER + d * COL}px"></div>`;
  const evLayers = states.map((s, i) => {
    const next = states[i + 1];
    const anim = [i > 0 ? `appear .01s step-end ${s.at}s forwards` : '', next ? `vanish .01s step-end ${next.at}s forwards` : ''].filter(Boolean).join(', ');
    return `<div class="evstate" style="${i > 0 ? 'opacity:0;' : ''}${anim ? 'animation:' + anim : ''}">${eventState(weekIdx, s.ids)}</div>`;
  }).join('');
  const nowH = TODAY.getHours() + TODAY.getMinutes() / 60;
  const todayIdx = Math.round((TODAY - start) / 864e5);
  const now = (todayIdx >= 0 && todayIdx < 7) ? `<div class="nowline" style="top:${(opts.nowAt - GRID_START) * HOUR}px;left:${GUTTER + todayIdx * COL}px;width:${COL}px"></div>` : '';
  const gridTop = 100 + alldayH + 1;
  return `<div class="weekview" data-week="${weekIdx}">
    <div class="head">${head}</div><div class="gmt">GMT-05</div>
    <div class="allday" style="height:${alldayH}px">${acols}${allday}</div>
    <div class="gridwrap" style="top:${gridTop}px"><div class="grid" style="height:${gridH}px">${lines}<div class="cols" style="height:${gridH}px">${evLayers}</div></div>${now}</div>
    <div class="scrollbar" style="top:${gridTop + 8}px;height:${Math.round((1002 - gridTop) * 0.62)}px"></div>
  </div>`;
}

// ---- cursor ----
const CURSOR_SVG = `<svg class="cursor" viewBox="0 0 24 24"><path d="M5 3l14 7.5-6.2 1.6L10 18.5z" fill="#1a1a19" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>`;
const TIP = [6, 3];
function centerOf(target) {
  if (Array.isArray(target)) return target;
  const r = document.querySelector(target).getBoundingClientRect();
  return [r.x + r.width / 2, r.y + r.height / 2];
}
// Builds a keyframe timeline: travel to each target, arriving 0.35s before `at`, click at `at`.
function cursorKeyframes(steps, startXY, duration) {
  const kf = [];
  const pct = t => `${Math.max(0, Math.min(100, t / duration * 100)).toFixed(3)}%`;
  let pos = startXY;
  kf.push(`0% { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) }`);
  let lastT = 0;
  for (const s of steps) {
    const arrive = s.at - 0.35, leave = Math.max(lastT, arrive - s.travel);
    if (leave > lastT) kf.push(`${pct(leave)} { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) }`);
    pos = s.xy;
    kf.push(`${pct(arrive)} { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) }`);
    if (s.click) {
      kf.push(`${pct(s.at)} { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) scale(1) }`);
      kf.push(`${pct(s.at + 0.06)} { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) scale(.88) }`);
      kf.push(`${pct(s.at + 0.14)} { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) scale(1) }`);
      lastT = s.at + 0.14;
    } else lastT = arrive;
  }
  kf.push(`100% { transform: translate(${pos[0] - TIP[0]}px, ${pos[1] - TIP[1]}px) }`);
  return kf.join('\n');
}

// ---- app ----
function buildApp(root, opts) {
  opts = Object.assign({ week: 0, on: [], toggles: [], flips: [], cursorStart: [1100, 600], cursorEnd: null, nowAt: 11.9, duration: 4 }, opts);
  const toggleAt = {}; for (const t of opts.toggles) toggleAt[t.id] = t.at;

  // visible-id states over time (toggles only; flips reuse the final id set)
  const states = [{ at: 0, ids: ['me', ...PEOPLE.filter(p => opts.on.includes(p.id)).map(p => p.id)] }];
  for (const t of opts.toggles) states.push({ at: t.at, ids: [...states[states.length - 1].ids, t.id] });
  const finalIds = states[states.length - 1].ids;

  // week views: the initial week carries the toggle states; flipped weeks carry the final set
  const flipSeq = [{ week: opts.week, at: 0 }, ...opts.flips];
  const views = flipSeq.map((f, i) => {
    const next = flipSeq[i + 1];
    const st = i === 0 ? states : [{ at: 0, ids: finalIds }];
    let v = weekView(f.week, st, opts);
    const anim = [i > 0 ? `appear .01s step-end ${f.at}s forwards` : '', next ? `vanish .01s step-end ${next.at}s forwards` : ''].filter(Boolean).join(', ');
    return v.replace('class="weekview"', `class="weekview" style="${i > 0 ? 'opacity:0;' : ''}${anim ? 'animation:' + anim : ''}"`);
  }).join('');

  root.innerHTML = topbar() + sidebar(opts, toggleAt) + `<div class="card">${views}</div>` +
    `<div class="rail">${RAIL.join('')}${ICON('plus', 'plus')}</div>` + CURSOR_SVG;

  // mini-month + insights swap on flips
  if (opts.flips.length) {
    const wrap = (html, i, at, nextAt) => {
      const anim = [i > 0 ? `appear .01s step-end ${at}s forwards` : '', nextAt != null ? `vanish .01s step-end ${nextAt}s forwards` : ''].filter(Boolean).join(', ');
      return `<div class="slot-layer" style="${i > 0 ? 'opacity:0;' : ''}${anim ? 'animation:' + anim : ''}">${html}</div>`;
    };
    const ms = document.getElementById('mini-slot'), is = document.getElementById('insights-slot');
    ms.innerHTML = flipSeq.map((f, i) => wrap(miniMonth(f.week), i, f.at, flipSeq[i + 1]?.at)).join('');
    is.innerHTML = flipSeq.map((f, i) => wrap(insights(f.week), i, f.at, flipSeq[i + 1]?.at)).join('');
  }

  // sidebar scrolled so the full "Other calendars" list is visible (as in the recording)
  const sc = document.getElementById('side-scroll');
  sc.style.top = `${Math.min(0, 1016 - sc.offsetHeight)}px`;

  // hover highlights: checkbox rows get a faint pill while the cursor is on them; the next
  // arrow gets its circle. Both fade with step timing around the click.
  const steps = [];
  for (const t of opts.toggles) steps.push({ at: t.at, sel: `#chk-${t.id}`, click: true, travel: 0.45, hl: `#chk-${t.id} .hl` });
  for (const f of opts.flips) steps.push({ at: f.at, sel: '#next', click: true, travel: 0.9, hl: '#next-hover' });
  steps.sort((a, b) => a.at - b.at);
  if (opts.cursorEnd) steps.push({ at: opts.duration + 0.35, sel: opts.cursorEnd, click: false, travel: 0.6 });
  for (const s of steps) if (s.hl) {
    const el = document.querySelector(s.hl);
    el.style.animation = `appear .01s step-end ${(s.at - 0.35).toFixed(2)}s forwards, vanish .01s step-end ${(s.at + 0.5).toFixed(2)}s forwards`;
  }
  document.fonts.ready.then(() => {
    for (const s of steps) s.xy = centerOf(s.sel);
    const start = centerOf(opts.cursorStart);
    const style = document.createElement('style');
    style.textContent = `@keyframes cur { ${cursorKeyframes(steps, start, opts.duration)} }\n.cursor { animation: cur ${opts.duration}s cubic-bezier(.4,0,.2,1) forwards; }`;
    document.head.appendChild(style);
  });
}
