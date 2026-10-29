// Shared building blocks for every scene. Runs synchronously at load so all
// CSS animations exist before render.py pauses and seeks them.

const ICON = {
  plus: '<path d="M12 4.5v15m7.5-7.5h-15"/>',
  projects: '<path d="M7.5 4h9M6 7h12"/><path d="M4 10h16l-1.5 8.3A2 2 0 0 1 16.53 20H7.47a2 2 0 0 1-1.97-1.7Z"/>',
  artifacts: '<path d="M9.2 3.6a.9.9 0 0 1 1.6 0l3.3 6a.9.9 0 0 1-.8 1.3H6.7a.9.9 0 0 1-.8-1.3Z"/><circle cx="7.4" cy="16.4" r="4"/><rect x="12.6" y="11.6" width="7.6" height="9" rx="1.6"/>',
  clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
  customize: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 13h18"/>',
  chevron: '<path d="m19.5 8.25-7.5 7.5-7.5-7.5"/>',
  up: '<path d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"/>',
  check: '<path d="m4.5 12.75 6 6 9-13.5"/>',
  folder: '<path d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z"/>',
  bolt: '<path d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"/>',
  doc: '<path d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"/>',
  chat: '<path d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z"/>',
  panel: '<rect x="3.75" y="4.5" width="16.5" height="15" rx="2.25"/><path d="M9 4.5v15"/>',
  filter: '<path d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75"/>',
  tray: '<path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"/>',
  search: '<path d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>',
  laptop: '<path d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25"/>',
  mic: '<path d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z"/>',
  stop: '<circle cx="12" cy="12" r="8.25"/><rect x="9.5" y="9.5" width="5" height="5" rx="1" fill="currentColor"/>',
  wave: '<path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4"/>',
  eyeoff: '<path d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"/>',
  listcheck: '<path d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"/>',
  arrowleft: '<path d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18"/>',
  checkcircle: '<path d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>',
  hand: '<path d="M10.05 4.575a1.575 1.575 0 1 0-3.15 0v3m3.15-3v-1.5a1.575 1.575 0 0 1 3.15 0v1.5m-3.15 0 .075 5.925m3.075.75V4.575m0 0a1.575 1.575 0 0 1 3.15 0V15M6.9 7.575a1.575 1.575 0 1 0-3.15 0v8.175a6.75 6.75 0 0 0 6.75 6.75h2.018a5.25 5.25 0 0 0 3.712-1.538l1.732-1.732a5.25 5.25 0 0 0 1.538-3.712l.003-2.024a.668.668 0 0 1 .198-.471 1.575 1.575 0 1 0-2.228-2.228 3.818 3.818 0 0 0-1.12 2.687M6.9 7.575V12m6.27 4.318A4.49 4.49 0 0 1 16.35 15m.002 0h-.002"/>',
  ban: '<path d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636"/>',
  kebab: '<path d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"/>',
  arrowupright: '<path d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25"/>',
  sliders: '<path d="M6 13.5V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 9.75V10.5"/>',
  code: '<path d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5"/>',
};

function icon(name, cls = '') {
  return `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">${ICON[name]}</svg>`;
}

// Sidebar: order and labels mirror the real claude.ai sidebar (captured 2026-09-30):
// nav block, Pinned, then "Chats and tasks". The real Scheduled section is left out on purpose.
// Chat titles are fake. `chats` is the list shown; `after` optionally crossfades to a
// second list at `afterAt` seconds (used when a new chat appears) so nothing reflows.
const DEFAULT_CHATS = ['Proposal for Lakeshore Dental', 'Q4 workshop agenda', "Summarize Tuesday's AI sync", 'Newsletter draft', 'Follow-up email to Dana', 'Workshop sign-up page copy'];
function sidebar({ active = 'new', chats = DEFAULT_CHATS, current = null, after = null, afterAt = 0, user = 'Shaw', plan = 'Max' } = {}) {
  const nav = (id, ic, label) => `<div class="nav ${active === id ? 'on' : ''}">${id === 'new' ? `<span class="newdot">${icon('plus')}</span>` : icon(ic)}${label}</div>`;
  const list = (items, cur) => items.slice(0, 6).map(n => `<div class="side-item ${n === cur ? 'on' : ''}"><span class="dot"></span><span class="nm">${n}</span></div>`).join('');
  const lists = after
    ? `<div class="chatlists"><div class="out" style="--d:${afterAt}s">${list(chats, current)}</div><div class="alt fade" style="--d:${afterAt}s">${list(after.chats, after.current)}</div></div>`
    : list(chats, current);
  return `
  <aside class="sidebar">
    <div class="brand"><span class="bl">${icon('panel')}Claude</span><div class="modes"><span class="on">${icon('chat')}</span><span>${icon('code')}</span></div></div>
    ${nav('new', 'plus', 'New')}
    ${nav('projects', 'projects', 'Projects')}
    ${nav('artifacts', 'artifacts', 'Artifacts')}
    ${nav('scheduled', 'clock', 'Scheduled')}
    ${nav('customize', 'customize', 'Customize')}
    <div class="nav more">${icon('chevron')}More</div>
    <div class="side-label">Pinned</div>
    <div class="side-item pin">${icon('projects')}<span class="nm">Client readouts</span></div>
    <div class="side-label row">Chats and tasks ${icon('filter')}</div>
    ${lists}
    <div class="account"><div class="av">${user[0]}</div>${user} <span class="plan">· ${plan}</span>${icon('chevron')}<span class="acct-ic">${icon('tray')}${icon('search')}</span></div>
  </aside>`;
}

// Cowork session chrome -------------------------------------------------------
// Top bar: laptop icon with a green "running" dot, title, chevron; panel toggle at right.
function sessionTopbar(title) {
  return `<div class="stopbar"><span class="lap">${icon('laptop')}<i></i></span>${title}${icon('chevron')}<span class="ptoggle">${icon('panel')}</span></div>`;
}
// Bottom composer used inside a session, with the "Manual" and model line under it.
function sessionComposer(inner = '') {
  return `<div class="scomp"><div class="scomp-box"><span class="plus">${icon('plus')}</span><div class="sfield">${inner || '<span class="ph">Write a message…</span>'}</div><span class="sicons">${icon('stop')}${icon('mic')}${icon('chevron')}</span></div><div class="sunder"><span>Manual</span><span class="smodel">Opus 5.5 <em>Medium</em></span></div></div>`;
}
// Floating right panel. Section order matches the real app: Progress, Outputs, Context.
function sessionPanel({ progress = todo(), outputs = '', connectors = '', skills = '', skillsAt = null }) {
  const sec = (title, body) => `<div class="psec"><div class="phead">${title}${icon('chevron')}</div><div class="pbody">${body}</div></div>`;
  const progSec = `<div class="psec"><div class="phead">Progress${icon('chevron').replace('<svg ', `<svg style="${progress.chevStyle}" `)}${progress.headExtra}</div><div class="pbody tbody">${progress.body}</div></div>`;
  const ctx = `${connectors ? `<div class="plabel">Connectors</div><div class="pchips">${connectors}</div>` : ''}${skills ? `<div class="plabel ${skillsAt === null ? '' : 'fade'}" style="--d:${skillsAt ?? 0}s">Skills</div>${skills}` : ''}`;
  return `<aside class="spanel">${progSec}${sec('Outputs', outputs)}${sec('Context', ctx)}</aside>`;
}
const connChip = (img, name, d) => `<span class="pchip fade" style="--d:${d}s"><img src="../shared/${img}" alt="">${name}</span>`;
const skillRow = (name, d) => `<div class="pskill fade" style="--d:${d}s"><span class="skic">${icon('doc')}</span>${name}</div>`;
const outRow = (name, meta, d, kind = 'PPT') => `<div class="pfile in" style="--d:${d}s"><span class="ic ${kind === 'MD' ? 'md' : ''}">${kind}</span><span>${name}<em>${meta}</em></span></div>`;
// Progress to-do list, modeled on the real Cowork panel (captured 2026-09-30, reference/20-progress-*):
// - The whole list is written first, rows added in quick succession.
// - Each item then goes pending (grey number) -> active (blue ring, "-ing" label) -> done
//   (filled blue check, struck-through label), with an "k of N" counter in the header.
// - When every item is done the Progress section collapses to its header; the next
//   request opens a fresh list.
// rounds: [{ at, collapseAt, items: [[label, activeLabel, start, done], ...] }]
// placeholder: show the empty-state line until the first list is written (new sessions).
function todo({ rounds = [], placeholder = false, gap = 0.2 } = {}) {
  const anim = (list) => list.filter(Boolean).join(', ');
  // Section open/close timeline, shared by the body, the chevron and the counter.
  const opens = [], closes = [];
  rounds.forEach(r => { opens.push(r.at); if (r.collapseAt != null) closes.push(r.collapseAt); });
  const startOpen = placeholder;
  const seq = [...opens.map(t => ['open', t]), ...closes.map(t => ['close', t])].sort((a, b) => a[1] - b[1]);
  const secAnim = (openK, closeK) => anim(seq.map(([k, t]) => `${k === 'open' ? openK : closeK} .35s var(--std) ${t}s forwards`));

  const rows = rounds.map((r, ri) => {
    const next = rounds[ri + 1];
    const goneAt = next ? next.at : null;
    return r.items.map(([label, active, start, done], i) => {
      const openAt = r.at + i * gap;
      const box = `<span class="box"><span class="num">${i + 1}</span>`
        + `<span class="ring" style="animation:${anim([`fadeIn .2s var(--out) ${start}s forwards`, `fadeOut .01s linear ${done + 0.25}s forwards`])}"></span>`
        + `<span class="tick" style="animation:fadeIn .25s var(--out) ${done}s forwards">${icon('check')}</span></span>`;
      const labels = `<span class="pl">`
        + `<span style="animation:fadeOut .15s linear ${start}s forwards">${label}</span>`
        + `<span style="opacity:0;animation:fadeIn .2s linear ${start}s forwards, fadeOut .15s linear ${done}s forwards">${active}</span>`
        + `<span class="struck" style="opacity:0;animation:fadeIn .2s linear ${done}s forwards">${label}</span></span>`;
      return `<div class="tgrow" style="animation:${anim([`rowOpen .35s var(--out) ${openAt}s forwards`, goneAt != null && `rowClose .01s linear ${goneAt - 0.02}s forwards`])}"><div class="tin"><div class="pstep">${box}${labels}</div></div></div>`;
    }).join('');
  }).join('');

  const ph = placeholder && rounds.length
    ? `<div class="tgrow open" style="animation:rowClose .25s var(--std) ${rounds[0].at}s forwards"><div class="tin"><div class="pempty">See task progress for longer tasks.</div></div></div>` : '';

  // "k of N" counter: one stacked span per value, each visible until the next check lands.
  const counts = rounds.map(r => {
    const n = r.items.length;
    const times = [r.at, ...r.items.map(it => it[3])];
    const end = r.collapseAt ?? null;
    return times.map((t, k) => {
      const until = k < n ? times[k + 1] : end;
      return `<span style="opacity:0;animation:${anim([`fadeIn .15s linear ${t}s forwards`, until != null && `fadeOut .15s linear ${until}s forwards`])}">${k} of ${n}</span>`;
    }).join('');
  }).join('');

  return {
    headExtra: `<span class="pcount">${counts}</span>`,
    chevStyle: `transform:rotate(${startOpen ? 0 : -90}deg);animation:${secAnim('chevOpen', 'chevClose')}`,
    body: `<div class="tgrow ${startOpen ? 'open' : ''}" style="animation:${secAnim('rowOpen', 'rowClose')}"><div class="tin">${ph}${rows}</div></div>`,
  };
}

// Types `text` into `el` one character at a time, starting at `start` seconds.
// Returns the time the last character lands.
function typeInto(el, text, start, cps = 26) {
  let t = start;
  const frag = [];
  for (const c of text) {
    frag.push(`<span class="ch" style="animation-delay:${t.toFixed(3)}s">${c === ' ' ? ' ' : c.replace('<', '&lt;')}</span>`);
    t += (c === ' ' ? 0.6 : 1) / cps + (',.'.includes(c) ? 0.12 : 0);
  }
  el.innerHTML = frag.join('');
  return t;
}

const CURSOR_SVG = `<svg class="cursor" viewBox="0 0 24 24"><path d="M5 3l14 7.5-6.2 1.6L10 18.5z" fill="#f0efec" stroke="#1a1a19" stroke-width="1.3" stroke-linejoin="round"/></svg>`;

// ---------- deck thumbnails ----------
// All sizes are in "slide units" relative to a 1600x900 slide, then scaled by `w`.
function slideFrame(w, cls, inner) {
  const k = w / 1600;
  return `<div class="${cls}" style="width:${w}px;height:${w * 9 / 16}px"><div style="width:1600px;height:900px;transform:scale(${k});transform-origin:0 0;position:absolute;left:0;top:0">${inner}</div></div>`;
}

// Generic first draft: what an un-onboarded assistant produces.
// ---------- layout-dependent positions ----------
// Measured after webfonts load, so cursor targets and toggle pills follow the real
// text metrics. render.py awaits document.fonts.ready after these callbacks are
// registered, so they run before any frame is captured.
const CURSOR_TIP = [7, 4]; // arrow tip offset inside the 34px cursor svg

// aim({c: '.lbl-cowork', s: '#send'}) sets --cx/--cy and --sx/--sy on the cursor.
function aim(targets) {
  document.fonts.ready.then(() => {
    const cur = document.querySelector('.cursor');
    for (const [k, sel] of Object.entries(targets)) {
      const r = document.querySelector(sel).getBoundingClientRect();
      cur.style.setProperty(`--${k}x`, `${r.x + r.width / 2 - CURSOR_TIP[0]}px`);
      cur.style.setProperty(`--${k}y`, `${r.y + r.height / 2 - CURSOR_TIP[1]}px`);
    }
  });
}

// Sizes each .toggle .pill[data-for] to sit exactly under its label.
function placePills() {
  document.fonts.ready.then(() => {
    document.querySelectorAll('.toggle').forEach(t => {
      const tr = t.getBoundingClientRect();
      t.querySelectorAll('.pill[data-for]').forEach(p => {
        const r = t.querySelector(p.dataset.for).getBoundingClientRect();
        p.style.left = `${r.x - tr.x}px`;
        p.style.width = `${r.width}px`;
      });
    });
  });
}
