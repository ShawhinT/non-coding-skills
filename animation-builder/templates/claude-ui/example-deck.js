// Example per-video content: deck thumbnails for the 'client readout' demo.
// Content, not engine: copy and rewrite per video. Uses slideFrame() from claude-ui.js.

function plainSlides(w) {
  const bar = (x) => `<div style="height:22px;background:#c9c9c4;border-radius:4px;width:${x}px;margin:26px 0"></div>`;
  return [
    slideFrame(w, 'plain', `<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px"><div style="font-size:92px;font-weight:700;color:#222">Ridgeline Analytics</div><div style="font-size:58px;color:#555">September Update</div><div style="width:420px;height:10px;background:#3b73c8"></div></div>`),
    slideFrame(w, 'plain', `<div style="padding:110px 130px"><div style="font-size:84px;font-weight:700;color:#222;margin-bottom:40px">Agenda</div>${bar(900)}${bar(760)}${bar(980)}${bar(640)}${bar(820)}</div>`),
    slideFrame(w, 'plain', `<div style="padding:110px 130px"><div style="font-size:84px;font-weight:700;color:#222;margin-bottom:50px">Usage Data</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px">${Array.from({length: 16}, (_, i) => `<div style="height:90px;background:${i < 4 ? '#3b73c8' : '#e2e2dd'}"></div>`).join('')}</div></div>`),
  ];
}

// Generic v2 after round-1 feedback: leads with daily use, 3 slides, still unbranded.
function plainSlidesV2(w) {
  const bar = (x) => `<div style="height:22px;background:#c9c9c4;border-radius:4px;width:${x}px;margin:26px 0"></div>`;
  return [
    slideFrame(w, 'plain', `<div style="padding:110px 130px"><div style="font-size:84px;font-weight:700;color:#222">Daily Use: 57%</div><div style="font-size:52px;color:#555;margin-top:20px">Goal: 75%</div><div style="display:flex;gap:40px;align-items:flex-end;height:330px;margin-top:40px"><div style="width:200px;height:190px;background:#9db6dd"></div><div style="width:200px;height:250px;background:#3b73c8"></div></div></div>`),
    slideFrame(w, 'plain', `<div style="padding:110px 130px"><div style="font-size:84px;font-weight:700;color:#222;margin-bottom:50px">Usage Data</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px">${Array.from({length: 16}, (_, i) => `<div style="height:90px;background:${i < 4 ? '#3b73c8' : '#e2e2dd'}"></div>`).join('')}</div></div>`),
    slideFrame(w, 'plain', `<div style="padding:110px 130px"><div style="font-size:84px;font-weight:700;color:#222;margin-bottom:40px">Next Steps</div>${bar(880)}${bar(720)}${bar(940)}</div>`),
  ];
}

// ABA-branded readout: what the skill produces.
function abaSlides(w, client, month, from, to) {
  const title = `<div style="position:absolute;inset:0;padding:120px 130px;display:flex;flex-direction:column;justify-content:center">
      <div class="eyebrow" style="font-size:34px">${client} · ${month} readout</div>
      <h1 style="font-size:124px;line-height:1.02;margin-top:40px">Daily use is at ${to}%.<br><span style="color:rgba(255,255,255,0.5)">Goal is 75%.</span></h1>
      <div class="mono" style="font-size:30px;margin-top:60px">AI Builder Academy · Fractional AI Department</div></div>`;
  const chart = (() => {
    const H = 520, bx = (v, x, lbl, c) => `<div style="position:absolute;left:${x}px;bottom:150px;width:260px;height:${H * v / 100}px;background:${c};border-radius:12px 12px 0 0"></div><div style="position:absolute;left:${x}px;bottom:${150 + H * v / 100 + 20}px;width:260px;text-align:center;font-family:Manrope;font-weight:800;font-size:64px">${v}%</div><div class="mono" style="position:absolute;left:${x}px;bottom:90px;width:260px;text-align:center;font-size:32px">${lbl}</div>`;
    return `<div style="position:absolute;inset:0"><div class="eyebrow" style="position:absolute;left:130px;top:100px;font-size:32px">Seats using Claude daily</div>
      ${bx(from, 380, 'August', 'rgba(255,255,255,0.18)')}${bx(to, 760, 'September', 'var(--aba-primary)')}
      <div style="position:absolute;left:300px;right:300px;bottom:${150 + H * 0.75}px;border-top:4px dashed var(--aba-lime)"></div>
      <div class="mono" style="position:absolute;right:130px;bottom:${150 + H * 0.75 - 20}px;font-size:32px;color:var(--aba-lime)">Goal 75%</div></div>`;
  })();
  const next = `<div style="position:absolute;inset:0;padding:110px 130px"><div class="eyebrow" style="font-size:32px">Next month</div>
      <h2 style="font-size:84px;margin:36px 0 50px">Three moves to reach 75%</h2>
      ${['Office hours split into beginner and advanced', 'Sales team training on Oct 21', 'Scheduled tasks for every adopted user'].map((t, i) => `<div style="display:flex;gap:36px;align-items:baseline;font-size:50px;margin:30px 0;color:rgba(255,255,255,0.85)"><span class="mono" style="font-size:40px;color:var(--aba-overlay)">0${i + 1}</span>${t}</div>`).join('')}</div>`;
  return [slideFrame(w, 'slide', title), slideFrame(w, 'slide', chart), slideFrame(w, 'slide', next)];
}

