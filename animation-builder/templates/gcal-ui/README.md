# gcal-ui — Google Calendar week-view kit

Recreates Google Calendar's light Material 3 week view (Oct 2026) at 1920×1080 for product-demo
B-roll: a cursor clicks calendars on one at a time, the grid fills, weeks flip. Geometry and
colors were measured from a real screen recording and a live-app capture; see
`references/third-party-ui-mockups.md` for the method and `references/claude-ui-mockups.md`
for the fidelity principles.

## Files

- `gcal-ui.css` — layout engine (top bar, sidebar, grid card, right rail, chips, cursor). Colors
  and pitches are CSS variables at the top.
- `gcal-ui.js` — `buildApp(root, opts)` renders the whole app from data and turns every state
  change into a seekable CSS step animation. Event layout follows Calendar's cascade (later
  overlapping chips sit on top, offset right).
- `gcal-data.js` — the demo's cast and events. Seeded generator, soft/tentative flags, all-day
  blockers, authored `ANSWERS`, and a self-test: `node gcal-data.js`.
- `scene-starter.html` — one scene: copy to `src/NN-name/NN-name.html` with the kit in
  `src/shared/`.
- `interactive.html` — the same app as a standalone, clickable page (no render pipeline):
  calendar checkboxes, Today, ‹ ›, mini-month days and arrow keys are live; everything else
  is painted but inert. Fluid layout (columns fill the window, grid and sidebar scroll) so
  browser zoom behaves like the real app. Data is inlined, so a story change made in
  `gcal-data.js` has to be copied in. See SKILL.md § "Interactive demos".

## Using it

```
<video>/assets/src/shared/gcal-{data,ui}.js, gcal-ui.css
<video>/assets/src/01-my-week/01-my-week.html      ← from scene-starter.html
```

```js
buildApp(document.querySelector('.app'), {
  duration: 4,                 // seconds; must equal render.py --duration
  week: 0,                     // week shown at t=0 (0..2 relative to WEEK0)
  on: ['ravi'],                // calendars already on (viewer 'me' always is)
  toggles: [{ id: 'claire', at: 1.6 }],   // checkbox clicks, in order
  flips: [{ week: 1, at: 2.4 }],           // "›" clicks
  cursorStart: '#chk-ravi',    // selector or [x, y]; use the previous scene's last target
});
```

Each scene is one beat so the editor can retime it alone. Chain cursor positions scene to scene
and join the renders with straight cuts (`ffmpeg -f concat … -c copy`), not crossfades.

## Changing the story

Everything narrative lives in `gcal-data.js`: `PEOPLE` (names, teams, zones as hours ahead of
the viewer, colors from `PALETTE`), `VIEWER_WEEKS` (the viewer's own events, grounded on their
real weeks with names swapped), `ALLDAY` (conferences, offsites, OOO), `ANSWERS` (the slots that
should survive with only soft conflicts), `SEED`. After any change run `node gcal-data.js` and
confirm the printed claims still match the script: no perfect slot, the intended soft-only
answers, and how many teammates it takes before the first week closes (paces the stack scene).

## Fidelity notes (perishable, measured 2026-10-07)

Sidebar 282px; grid card at x 290–1846 with 24px radius; gutter 65px; columns 209.7px; hour
pitch 53px; day header 100px; chips radius 6, 12px text, 4px/8px padding, 1px white border;
unaccepted invites outlined (white fill, colored border and text); now-line `#db372d` 2px with
12px dot; grid lines `#dde3ea`; today `#0b57d0`; outlined buttons `#747775`; page `#f5f7fb`.
Fonts: Roboto stand-in for Google Sans Text.
