// Scheduling-demo data: the viewer (Shaw, Central time) plus a fictional sales org
// ("Meridian Cyber", two teams) spread over London / New York / San Francisco.
// Busy blocks are generated deterministically (seeded) so every render is identical, and
// the self-test (`node gcal-data.js`) confirms that no 90-minute slot inside business hours
// is free for everyone in any of the three weeks.
// All times are expressed in the VIEWER's zone (CT), as Google Calendar displays shared
// calendars; each person's local working window is shifted into CT by `off` (hours ahead of CT).

// Google Calendar event palette (chip background).
const PALETTE = {
  tomato:    '#d50000', flamingo: '#e67c73', tangerine: '#f4511e', banana: '#f6bf26',
  sage:      '#33b679', basil:    '#0b8043', peacock:   '#039be5', blueberry: '#3f51b5',
  lavender:  '#7986cb', grape:    '#8e24aa', graphite:  '#616161', cobalt: '#4285f4',
};

// Week 0 = Sun 2026-10-04 (today is Wed Oct 7). Weeks 1 and 2 follow.
const WEEK0 = new Date(2026, 9, 4);
const TODAY = new Date(2026, 9, 7);
const VIEWER = { name: 'Shaw Talebi', color: '#2a8fde', off: 0 };   // sampled from the recording

// off = hours ahead of CT (local = CT + off).  London = +6, New York = +1, San Francisco = -2.
const PEOPLE = [
  { id: 'ravi',   name: 'Ravi Mehta',      team: 'New Business', city: 'London',        off: +6, color: PALETTE.grape },
  { id: 'claire', name: 'Camille Dubois',   team: 'New Business', city: 'London',        off: +6, color: PALETTE.flamingo },
  { id: 'owen',   name: 'Owen Fitzgerald', team: 'New Business', city: 'New York',      off: +1, color: PALETTE.tangerine },
  { id: 'felix',  name: 'Felix Nakamura',  team: 'New Business', city: 'San Francisco', off: -2, color: PALETTE.banana },
  { id: 'marcus', name: 'Marcus Hale',     team: 'Account Mgmt', city: 'New York',      off: +1, color: PALETTE.basil },
  { id: 'sofia',  name: 'Sofia Alvarez',   team: 'Account Mgmt', city: 'New York',      off: +1, color: PALETTE.graphite },
  { id: 'tom',    name: 'Tom Lindqvist',   team: 'Account Mgmt', city: 'San Francisco', off: -2, color: PALETTE.lavender },
  { id: 'jenna',  name: 'Jenna Okafor',    team: 'Account Mgmt', city: 'San Francisco', off: -2, color: PALETTE.tomato },
];

// Realistic-sounding titles so the chips read as a working sales team's week.
const TITLES = [
  'Pipeline review', 'Discovery call: Halvorsen Re', 'Weekly 1:1', 'Deal desk sync', 'Demo prep',
  'QBR: Meridian Logistics', 'Forecast call', 'Renewal: Castellan Group', 'Sales standup', 'Proposal walkthrough',
  'Territory planning', 'Enablement: new pricing', 'Customer call: Brightline', 'Follow-up: Ardent Health',
  'Partner intro', 'Focus time', 'Contract review', 'Onboarding: SDR cohort', 'Account planning',
  'Exec sponsor sync', 'Comp plan Q&A', 'Negotiation prep', 'Marketing handoff', 'Broker lunch',
  'Underwriting sync', 'Submission review', 'Portfolio check-in', 'Renewal strategy', 'Client training',
];

const SEED = (typeof process !== 'undefined' && process.env && process.env.SEED) ? Number(process.env.SEED) : 0;   // reshuffles every generated week

// Small seeded PRNG so the generated weeks never change between renders.
function rng(seed) {
  let s = seed >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

// All-day blockers (rendered as banners in the all-day row). day: 0=Sun..6=Sat.
// Borrowed in shape from the real situation (a conference for half the group, an offsite the
// week after, an OOO), renamed. `ids` lists who is blocked; `span` is [firstDay, lastDay].
const ALLDAY = {
  0: [
    { title: 'Holidays in United States', span: null },                        // none this week
  ],
  1: [
    { title: 'Columbus Day', span: [1, 1], holiday: true },
    { title: 'RiskWorld 2026', span: [2, 4], ids: ['ravi', 'owen', 'marcus', 'jenna'] },
  ],
  2: [
    { title: 'Sales offsite: Account Mgmt', span: [1, 3], ids: ['marcus', 'sofia', 'tom', 'jenna'] },
    { title: 'OOO', span: [1, 3], ids: ['claire'] },
    { title: 'Client event: Lloyd\'s', span: [4, 4], ids: ['ravi'] },
  ],
};

// Soft (flexible) and tentative events. Soft ones can move; tentative ones are invitations the
// person hasn't accepted, which Calendar draws as outlined chips. Everything else is hard.
const SOFT = ['Focus time', 'Lunch', '[HOLD] Pipeline review', 'Optional: product roadmap', 'Admin time', '[HOLD] Deal prep', 'Inbox + CRM'];

// One person's timed busy blocks for one week → [{day 1-5, start, end (CT), title, soft, tent}].
// Local window 8:30–18:00 shifted by `off`. ~50% filled with 30/45/60/90-min meetings and gaps,
// so each column reads as a normal busy week rather than a solid slab.
function personWeek(p, weekIdx, idx) {
  const r = rng(idx * 7919 + weekIdx * 104729 + 17 + SEED);
  const out = [];
  const winStart = 8.5 - p.off, winEnd = 18 - p.off;   // local 8:30–18:00 → CT
  const blockedDays = new Set();
  for (const b of ALLDAY[weekIdx] || []) if (b.ids && b.ids.includes(p.id)) for (let d = b.span[0]; d <= b.span[1]; d++) blockedDays.add(d);
  for (let d = 1; d <= 5; d++) {
    if (blockedDays.has(d)) continue;
    let t = winStart + [0, 0.5, 1, 1.5][Math.floor(r() * 4)];
    const lunch = 12 - p.off + (r() < 0.5 ? 0 : 0.5);
    let hadLunch = false;
    while (t < winEnd - 0.5) {
      if (!hadLunch && t >= lunch - 0.25) {
        if (r() < 0.75) out.push({ day: d, start: lunch, end: lunch + 1, title: 'Lunch', soft: true });
        t = Math.max(t, lunch + 1); hadLunch = true; continue;
      }
      if (r() < 0.42) { t += [0.25, 0.5, 0.5, 0.75, 1][Math.floor(r() * 5)]; continue; } // open gap
      const dur = [0.5, 0.5, 0.75, 1, 1, 1.5][Math.floor(r() * 6)];
      const end = Math.min(t + dur, winEnd);
      if (end - t >= 0.5) {
        const k = r();
        if (k < 0.18) out.push({ day: d, start: t, end, title: SOFT[Math.floor(r() * SOFT.length)], soft: true });
        else out.push({ day: d, start: t, end, title: TITLES[Math.floor(r() * TITLES.length)], tent: k < 0.32 });
      }
      t = end + (r() < 0.5 ? 0 : 0.25);
    }
  }
  return out;
}

// Viewer's own weeks, grounded on Shaw's real Oct 2026 calendar (shape, times and density
// copied from the reference recording; every name and company swapped for a fictional one).
const VIEWER_WEEKS = [
  [ { day: 0, start: 11, end: 12, title: 'ABA' },
    { day: 1, start: 9, end: 11, title: 'Weekly Review (Strategy, Cal, Email, Notion, Finances)' },
    { day: 1, start: 11.5, end: 12, title: 'Priya / Shaw' },
    { day: 1, start: 12, end: 12.5, title: 'Meridian Cyber / ABA - Weekly AI Sync' },
    { day: 2, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 2, start: 9, end: 12, title: 'Claude Code Workshop with Brightline - Dallas' },
    { day: 2, start: 12, end: 13, title: 'Meridian Cyber (Product Advisory)' },
    { day: 2, start: 13.5, end: 14, title: 'Lena / Shaw' },
    { day: 2, start: 14, end: 14.5, title: 'Theo / Shaw - Follow-up' },
    { day: 2, start: 17.5, end: 18, title: 'ABA' },
    { day: 3, start: 9.5, end: 10.5, title: 'Notion + Email' },
    { day: 3, start: 15, end: 15.5, title: 'Noah / Shaw - Claude SMB Workshop' },
    { day: 4, start: 7, end: 7.5, title: 'Notion + Email' },
    { day: 4, start: 12, end: 12.5, title: 'Liam / Shaw - Check-in' },
    { day: 4, start: 14.5, end: 15, title: 'Cole / Shaw' },
    { day: 4, start: 15, end: 15.5, title: 'Dev / Shaw - Coffee Chat' },
    { day: 4, start: 15.5, end: 16, title: 'Caleb / Shaw - Coffee Chat' },
    { day: 4, start: 16, end: 16.5, title: 'Drew / Shaw - Coffee Chat' },
    { day: 5, start: 7, end: 7.5, title: 'Notion + Email' },
    { day: 5, start: 8, end: 8.5, title: 'Theo / Shaw' },
    { day: 5, start: 12, end: 12.5, title: 'Nora / Shaw' },
    { day: 5, start: 13.5, end: 14, title: 'Carter / Shaw - Check-in' },
    { day: 5, start: 15.5, end: 17, title: 'Diego / Shaw - 1:1 Claude Workshop' },
    { day: 6, start: 8, end: 10, title: 'SFC' } ],
  [ { day: 0, start: 8.5, end: 10.5, title: 'Weekly Review (Strategy, Cal, Email, Notion, Finances)' },
    { day: 1, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 1, start: 14, end: 15, title: '[HOLD] Theo / Shaw' },
    { day: 2, start: 9, end: 10.5, title: 'Sales / AI Builder Academy [Shaw] - Claude Workshop' },
    { day: 2, start: 13.5, end: 14, title: 'Theo / Shaw' },
    { day: 2, start: 16.5, end: 17, title: 'Meridian Cyber / ABA - Weekly AI Sync' },
    { day: 3, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 3, start: 11, end: 12, title: 'Podcast recording' },
    { day: 4, start: 10, end: 11, title: 'Coffee chat' },
    { day: 4, start: 14, end: 15.5, title: 'Proposal review' },
    { day: 5, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 5, start: 13, end: 14, title: 'Content planning' },
    { day: 5, start: 17.5, end: 18.5, title: 'Ezra / Shaw' },
    { day: 6, start: 8, end: 10, title: 'SFC' } ],
  [ { day: 0, start: 8.5, end: 10.5, title: 'Weekly Review (Strategy, Cal, Email, Notion, Finances)' },
    { day: 1, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 1, start: 15, end: 16, title: 'Weekly review' },
    { day: 2, start: 10, end: 10.5, title: 'Check-in: Castellan' },
    { day: 2, start: 16.5, end: 17, title: 'Meridian Cyber / ABA - Weekly AI Sync' },
    { day: 3, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 3, start: 15, end: 18.5, title: 'North Texas Innovation Pitch Competition' },
    { day: 4, start: 10, end: 10.5, title: 'Rhys / Shaw' },
    { day: 4, start: 13, end: 14.5, title: 'Workshop: Lakeshore' },
    { day: 4, start: 17, end: 20, title: 'Dallas Meetup at Legacy Hall' },
    { day: 5, start: 8, end: 8.5, title: 'Notion + Email' },
    { day: 6, start: 8, end: 10, title: 'SFC' } ],
];

// Everyone's timed blocks for a week, keyed by person id ('me' for the viewer).
const VIEWER_SOFT = /^(Notion \+ Email|ABA|Weekly [Rr]eview|\[HOLD\]|SFC|Content planning|Coffee chat)/;
// The puzzle's answers: one 90-min slot per week inside the cross-zone window (10:30–12:00 CT)
// where nobody has a hard conflict, but the listed people keep a soft one (a focus block, a lunch,
// an invite they haven't accepted). Everyone else's hard events in that window are removed.
// Week 0 is the current week and deliberately has no answer.
const ANSWERS = {
  1: [{ day: 5, start: 10.5, soft: ['felix', 'sofia', 'ravi'] }],       // Fri Oct 16
  2: [{ day: 5, start: 10.5, soft: ['marcus', 'tom'] }],                // Fri Oct 23
};
function carve(weekIdx, data) {
  for (const a of ANSWERS[weekIdx] || []) {
    const end = a.start + 1.5;
    for (const id of Object.keys(data)) {
      const hit = e => e.day === a.day && e.start < end && e.end > a.start;
      if (a.soft.includes(id)) {
        data[id] = data[id].map(e => hit(e) && !e.soft && !e.tent ? { ...e, tent: true } : e);
        if (!data[id].some(hit)) {   // nothing there: give them a flexible block so the slot isn't visibly open
          const k = a.soft.indexOf(id);
          const inj = [{ start: a.start, end: a.start + 1, title: 'Focus time', soft: true },
                       { start: a.start + 0.5, end: a.start + 1.5, title: 'Lunch', soft: true },
                       { start: a.start + 0.25, end: a.start + 1.25, title: 'Optional: product roadmap', soft: true }][k % 3];
          data[id].push({ day: a.day, ...inj });
        }
      } else {
        data[id] = data[id].filter(e => !hit(e) || e.soft || e.tent);
        if (id !== 'me') data[id] = data[id].filter(e => !hit(e));   // keep the viewer's own soft blocks
      }
    }
  }
  return data;
}
function buildWeek(weekIdx) {
  const data = { me: VIEWER_WEEKS[weekIdx].map(e => VIEWER_SOFT.test(e.title) ? { ...e, soft: true } : e) };
  PEOPLE.forEach((p, i) => { data[p.id] = personWeek(p, weekIdx, i + 1); });
  return carve(weekIdx, data);
}

// Availability of one person at a 15-min step: 'off' (outside their working day or an all-day
// banner), 'hard', 'soft' (flexible meeting or unaccepted invite), or 'free'.
function stateAt(weekIdx, data, id, d, t) {
  const p = id === 'me' ? VIEWER : PEOPLE.find(x => x.id === id);
  const ws = 8.5 - p.off, we = 18 - p.off;
  if (t < ws - 0.5 || t >= we + 0.5) return 'off';
  const edge = t < ws || t >= we;   // 30-min stretch at either end: possible, but a favor
  for (const b of (ALLDAY[weekIdx] || [])) if (b.ids && b.ids.includes(id) && d >= b.span[0] && d <= b.span[1]) return 'off';
  let st = edge ? 'soft' : 'free';
  for (const e of data[id]) if (e.day === d && e.start < t + 0.25 && e.end > t) {
    if (!e.soft && !e.tent) return 'hard';
    st = 'soft';
  }
  return st;
}
// Classifies every 90-min slot (Mon–Fri, 15-min steps, 6:00–18:00 CT) for the given people:
// 'perfect' (everyone free), 'soft' (only flexible conflicts), or blocked. Returns the non-blocked ones.
function slots(weekIdx, ids, minutes = 90) {
  const data = buildWeek(weekIdx), len = minutes / 60, out = [];
  for (let d = 1; d <= 5; d++) for (let t = 6; t + len <= 18; t += 0.25) {
    let soft = [];
    let blocked = false;
    for (const id of ids) {
      for (let x = t; x < t + len - 1e-9; x += 0.25) {
        const st = stateAt(weekIdx, data, id, d, x);
        if (st === 'off' || st === 'hard') { blocked = true; break; }
        if (st === 'soft' && !soft.includes(id)) soft.push(id);
      }
      if (blocked) break;
    }
    if (!blocked) out.push({ day: d, start: t, kind: soft.length ? 'soft' : 'perfect', soft });
  }
  return out;
}
// Legacy helper kept for the stack-scene pacing check: first perfect slot or null.
function commonSlot(weekIdx, ids, minutes = 90) { return slots(weekIdx, ids, minutes).find(s => s.kind === 'perfect') || null; }

if (typeof module !== 'undefined') {
  module.exports = { PALETTE, WEEK0, TODAY, VIEWER, PEOPLE, ALLDAY, buildWeek, commonSlot, slots };
  if (require.main === module) {
    const ids = ['me', ...PEOPLE.map(p => p.id)];
    const DN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const fmt = h => { const hh = Math.floor(h), mm = Math.round((h - hh) * 60); return `${((hh + 11) % 12) + 1}:${String(mm).padStart(2, '0')}${hh < 12 ? 'am' : 'pm'}`; };
    for (let w = 0; w < 3; w++) {
      const all = slots(w, ids), n = Object.values(buildWeek(w)).reduce((a, b) => a + b.length, 0);
      const perfect = all.filter(s => s.kind === 'perfect'), soft = all.filter(s => s.kind === 'soft');
      console.log(`week ${w}: ${n} events | perfect 90-min slots: ${perfect.length} | soft-only: ${soft.length}`);
      for (const s of soft) console.log(`   ${DN[s.day]} ${fmt(s.start)}–${fmt(s.start + 1.5)}  only conflicts: ${s.soft.join(', ')}`);
      for (const s of perfect) console.log(`   PERFECT ${DN[s.day]} ${fmt(s.start)}`);
    }
    for (let w = 0; w < 3; w++) {
      let k = 1; while (k <= PEOPLE.length && commonSlot(w, ['me', ...PEOPLE.slice(0, k).map(p => p.id)])) k++;
      console.log(`week ${w}: no perfect slot once ${k} teammates are on`);
    }
  }
}
