# Third-party UI mockups (Google Calendar, Slack, Notion, …)

`claude-ui-mockups.md` holds the principles for recreating a real app on screen: copy, don't
reconstruct; fidelity before design; captions and pacing. This file adds what changed when the
product was someone else's (Google Calendar, Oct 2026) and the user had a screen recording of
the exact interaction they wanted mimicked.

## Measure from the recording first

A recording from the user's own machine shows their theme, zoom, account layout and the real
interaction order. Mine it before (or alongside) sending an agent to the live app:

```bash
ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=nw=1 ref.mov
ffmpeg -y -i ref.mov -vf "fps=1/2,scale=1280:-1" frames/f_%02d.png     # contact sheet, every 2s
ffmpeg -y -ss 0.5 -i ref.mov -frames:v 1 -update 1 00-start.png         # full-res stills at key moments
```

Then read geometry off a full-res still with a few pixel scans (PIL): walk a row inside the grid
for gray pixels to get the vertical dividers and column pitch, walk a column in an empty day for
the hour lines, scan for the sidebar's edge, and sample colors at known points (chip, now-line,
backgrounds). Twenty lines of Python gave sidebar width, gutter, column pitch (209.7px), hour
pitch (53px), and the real chip blue in one pass. Crop zoomed regions (top bar, sidebar rows, a
day header, overlapping chips) and look at them; that is where radii, weights and spacing come
from.

A live-capture agent is still worth sending: it reads computed styles (font sizes, weights,
exact hex values) that pixels can't give, and it sees states the recording doesn't show (the
dropdown, the person chip, hover). Give it the usual read-only authorization and expect it to
take a while; the recording-derived build should not wait for it. When its spec arrives, diff
against the kit and patch the deltas (here: chip radius 6 not 8, label weight 500, two colors).

## Interaction fidelity comes from the recording

The user's recording shows *how they do it*: in the scheduling demo, calendars were added by
clicking checkboxes under "Other calendars" one at a time, then "›" to flip weeks. The live app
offers a fancier path ("Search for people"), but it also needs sharing permissions and renders
a different sidebar state. Mimic what the recording does unless the user says otherwise; it is
what they will recognise, and it sidesteps states the mockup would have to invent.

## State-layer animations for UIs that reflow

Real apps re-layout when data arrives: adding a calendar narrows every overlapping chip in the
column, the all-day row grows, counts change. Fading individual elements in can't show that.
Render **one complete layer per visible state** (people 0..k on, week w shown) and step between
layers with `opacity` keyframes using `step-end` timing at the action times:

```js
// layer i appears at states[i].at and leaves when the next state arrives
const anim = [i > 0 ? `appear .01s step-end ${s.at}s forwards` : '',
              next ? `vanish .01s step-end ${next.at}s forwards` : ''].filter(Boolean).join(', ');
```

A few hundred chips per layer times eight layers is fine for Chromium. The same pattern handles
week flips (one layer per week), the mini-month's selected day and any text that changes with
the view. Everything stays a CSS animation, so `render.py` seeks it exactly.

**Stacking gotcha:** an element that must always paint on top (the red now-line) cannot live
inside the layered container. Layers with opacity animations create stacking contexts, so its
`z-index` only competes inside its own layer. Place it as a sibling of the layer stack.

**Checkbox toggles** are two stacked boxes (unchecked outline, colored fill with a check), the
"on" one `opacity: 0` with an `appear` step at the click time. Hover highlights (the gray pill on
a sidebar row, the circle behind "›") fade in 0.35s before the click and out 0.5s after.

## Cursor timelines from action times

Generate the cursor keyframes from the list of actions rather than hand-writing percentages:
for each action, travel to the target's measured center arriving 0.35s before `at`, hold, then a
0.88 scale pulse over 0.14s at `at`. Targets are measured after `document.fonts.ready` (as in
`aim()`), so font or layout changes never break a click. Start each scene's cursor at the
previous scene's last target so the cut is seamless.

## Hard cuts between scenes of the same screen

Scenes that are the same UI in successive states join with straight cuts (ffmpeg concat with
`-c copy` is enough), not the 0.4s crossfades `assemble.sh` uses for B-roll between unrelated
clips. Before rendering, verify the static layout is pixel-identical across scenes by reading
`getBoundingClientRect` for a couple of fixed elements in each; a slot whose height was derived
from `offsetHeight` moved the sidebar 10px between scenes 4 and 5 and was invisible in any
single snapshot.

## Render the app, not the browser

Render at 1920×1080 with the app filling the frame, no tab strip or bookmarks bar, unless the
cut must match a real recording that has them. The editor can frame it; a faked bookmarks bar
is one more thing to get wrong.

## Fonts for Google products

Google Sans / Google Sans Text are proprietary and not installed. Roboto 400/500 from Google
Fonts (`@import` in the kit CSS) is the closest free match and what Calendar itself used before
Google Sans Text; `render.py` waits for `networkidle`, so webfonts load before the first frame.

## Ops gotchas

- macOS screen recordings are named `Screen Recording 2026-10-07 at 11.58.43 AM.mov` with a
  **U+202F narrow no-break space** before "AM". Pasted paths fail with "No such file"; use a
  glob (`mv ./Screen*.mov …`).
- A recording still sitting in `/var/folders/…/TemporaryItems/` (the screenshot-UI holding area)
  is not readable from the shell (`Operation not permitted`). Ask for it to be moved into the
  project's `reference/` folder.
- Save frames, crops and the measured spec under `<video>/reference/` so later passes compare
  against the same source.

## Scheduling demo, Oct 2026 (worked example)

`templates/gcal-ui/` is the kit that came out of this. `gcal-data.js` carries a fictional sales
org in three time zones with a seeded generator, soft/tentative flags, authored `ANSWERS`, and a
self-test; `gcal-ui.js` builds the app from `buildApp(root, {week, on, toggles, flips, cursorStart,
duration})`. The storyboard that drove it (beats, decisions, answers) is a good shape to copy.

## Gmail drafts, Oct 2026 (worked example)

`templates/gmail-ui/` came from a client sales demo, where every email Claude drafted was
shown in Gmail rather than in the Claude thread. It was captured from a live throwaway draft
(Chrome, Drafts list → compose window; tell the user to discard the test draft afterwards). The
video cuts Claude → Gmail → Claude around each round of feedback.
