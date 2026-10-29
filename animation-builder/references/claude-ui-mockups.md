# Claude UI mockups (product demo videos)

Use this when the deliverable recreates the Claude app (claude.ai / Cowork / Customize) as an
animated walkthrough: a cursor clicks through real-looking screens while captions name each step.
It extends the B-roll workflow in SKILL.md to multi-scene videos of 1–2 minutes.

The audience knows the real app, or soon will. Every guessed detail reads as fake the moment they
open Claude themselves, so the job is fidelity first and design second.

---

## Principles

### 1. Copy the real thing; never reconstruct it from memory

Every visible gap in the first drafts of the reference project came from a guess: weight,
font, panel order, icon shapes, how the to-do list behaves. Each one was fixed by looking.

- **Capture before you build.** Screenshot each screen and each key interaction in the live
  app, then read computed styles with JS: font family, size, weight, `font-variation-settings`,
  colors, radii, spacing, section order. Save captures to `<video>/reference/NN-screen-*.png`
  so later passes compare against the same source.
- **Compare side by side and iterate.** Snap the mockup at the same moment (`scripts/snap.py`),
  put it next to the capture, list the differences, fix, re-snap. Budget up to 4 passes per screen.
- **Match the mode the video depicts.** If the story is Cowork, every reference comes from
  Cowork. Chat-mode captures mislead (different composer, sidebar, layout) and should be deleted.
  Keep only what a pre-switch frame needs.
- **Copy behavior, not just appearance.** How state changes over time is part of the UI:
  - Switching modes changes the whole screen, not only the toggle highlight.
  - The to-do list is generated first, then items progress in order.
  - Short tasks get no list at all.
  - "Connected" is implied by a Disconnect button, not a badge.

  Watch a real run from send to finish before animating one.
- **Order and structure are fidelity too.** Sidebar sections, panel sections and nav items appear
  in the real order with the real labels. If a section can't be shown faithfully, drop it rather
  than show it wrong or out of order.
- **Show each output where it actually lands.** If Claude's work ends up in another app (a Gmail
  draft, a Drive file, a CRM record), cut to a mock of that app (`templates/gmail-ui/`, or build
  one per `third-party-ui-mockups.md`) instead of inventing an in-thread preview card. Cowork
  doesn't render one, and the audience will look for it. Cut back to Claude for the next round
  of feedback, so the video alternates Claude → app → Claude.
- **Connectors only do what the real connector does.** Before showing a permissions page or a
  permission prompt, check the provider's MCP docs for the real tool names and limits, and write
  the story around them. For example, HubSpot's write tool is `manage_crm_objects`, not "Create
  task", and Gmail drafts can't carry attachments, so a file goes in as a Drive link.
- **Interaction realism matters as much as visuals.** Cursor targets land on real controls, pages
  change the way the app changes them, and a permission prompt only appears if the permissions
  shown earlier in the video would cause it.

### 2. Typography and assets

- **Match measured weights, not named weights.** Claude's text runs lighter than "regular"
  (variable weight 360). The wrong weight is the first thing that reads as off.
- **Serif for Claude, sans for the interface.** Claude's responses and the greeting are serif;
  user messages, controls and labels are sans.
- **When the real font is proprietary, offer choices.** Render 3–5 full versions with different
  stand-ins (only the font lines differ) plus a stacked comparison still, and let the person pick.
  Don't decide for them. In the reference project they chose Newsreader for serif and Inter
  for sans.
- **Icons come from an icon font (Anthropicons), so there are no SVGs to copy.** Zoom into the
  real sidebar, redraw each glyph as a 24px stroke SVG, and match its size relative to the
  adjacent text (≈1.4× the text size). Generic Heroicons look visibly wrong here.
- **Logos are vector, always.** Use `claude-color.svg`; a small colormapped PNG goes jagged
  when scaled. Align a mark beside display text to the text's cap-height center, not its box
  center. A serif line box includes descender space, so box-centering sits the mark low.
- **Scale for the projector consistently.** Derive one layout factor from the capture width
  (the kit uses 1.25× from a 1536px-wide viewport; type runs ~1.3×) and apply it everywhere
  rather than eyeballing individual elements.

### 3. Captions are part of the UI

- Style them like the app: the same corner radius as the composer and panels (14px), not a pill.
- One caption on screen at a time; crossfade between them.
- Each caption names the step the viewer is watching, in short imperative phrasing:
  - "Switch from Chat to Cowork"
  - "Make sure your connectors are set up"
  - "Explain the task to Claude like a new hire"
- Bring a caption in slightly before its action, as the cursor heads to the control, and hold it
  long enough to read (≥2.5s).
- Never cover the composer or the content the caption describes; raise it when a bottom composer
  is on screen.
- To label the steps of a framework (e.g. the 4-step skill loop), open each step with one
  **dark caption card** in the caption slot ("Step 1: Do it once", with the number in the accent
  colour), shown once and then replaced by the normal white captions. A persistent corner chip
  was rejected: it competes with the UI the whole time and adds nothing after the first glance.

### 4. Pacing teaches the interface

- **Navigation is slow; interactions are quick.** When the cursor moves to a new screen, give the
  audience time to take it in: a deliberate move, a dwell on each page (2–4s), and a hover over
  what matters. Clicks and page changes stay snappy, like the real app.
- **Compress waiting honestly.** Long agent work is sped up with a visible "Sped up 10x" label.
- **Time state changes to activity.** A to-do item completes when its matching activity line
  appears, not on an arbitrary beat.

### 5. The story is a real workflow with invented data

- Mine the user's real work for the workflow's shape: deliverable type, metrics, cadence, and
  the tools involved.
- Replace every person, company and number with fake ones. The presenter's own name and plan
  are fine.
- Show the habit, not just the result (this is the 4-step framework the workshops teach):
  1. **Do it once:** delegate the task, then give two rounds of feedback. Voice first ("too long,
     match my email to X") and missing context second ("you left out Y, it's in Drive") reads as
     a natural progression.
  2. **Distill into skill:** turn the result into a skill and save it.
  3. **Use it:** in a fresh session, ask in plain language with no `/skill`. Claude loads the
     skill on its own; highlight the "loaded skill" line and the panel's Skills row and caption
     that it happened automatically. That's the point of the step.
  4. **Improve it:** in that same session, spot a gap in the output, give feedback, then say
     "Update the skill based on this session." Show the skill-update card with a one-line diff.
     No separate thread for the update.
- When the story's punchline is output in the presenter's voice, build the "good" version from
  their real examples (e.g. read their sent emails with the Gmail connector) and keep its
  structure, openers and sign-offs. A generic short-and-punchy version reads as too thin, and
  as not them.
- Keep scenes consistent with each other. If the connectors scene shows tools set to "Needs
  approval", the later permission prompt is earned. If it showed "Always allow", cut the prompt.
  Having the user click "Always allow" in that first prompt is what lets later runs (Steps 3–4)
  skip it.
- When a narrative choice is open, build both and let the person compare. Example: two
  final-card wordings. Alternate clips go in `assets/alt/` and are assembled into a second MP4.

### 6. Working with the live app

- Send sub-agents to capture, and state what they're authorized to do. The default is read-only:
  no toggles, connects, disconnects, saves or OAuth. Send prompts or save skills only when the user
  says so.
- Ask for one harmless test task that exercises the feature being mocked: a multi-step task for
  progress lists, a skill create-and-save for the skill flow.
- Report everything a capture run created in the user's account (sessions, skills, files) so they
  can delete it. Never delete on their behalf.
- Some states are hard to reach in a browser. Cowork's toggle needed its hidden radio input
  clicked by script, and the panel can sit offscreen. Say what was approximated rather than
  inventing it silently.
- Blur or replace personal info that appears in captures: emails, workspace names, real chat titles.

---

## Build workflow

1. **Copy the kit.** Copy `templates/claude-ui/` into `<video>/assets/src/shared/`. Scenes link
   `../shared/claude-ui.css` and `../shared/claude-ui.js`. Per-video content goes in its own file,
   like `example-deck.*`; the engine files stay generic.
2. **One scene per folder.** Use `assets/src/NN-name/NN-name.html`, starting from
   `scene-starter.html`. Split a long beat into separate scenes, like the switch, the connectors
   check and typing, so each can be retimed and re-rendered alone.
3. **Change shared components once.** The sidebar, panel, to-do list, composer and captions are
   builders in `claude-ui.js` / classes in `claude-ui.css`. A layout fix goes there, never into
   individual scenes.
4. **Time the send from the typing, not by hand.** `typeInto` returns when its last character
   lands; put the send press at least 0.5s after that. When retiming a scene later, recompute the
   cursor keyframes from those seconds rather than regex-shifting the numbers already in the file.
   Blind shifts here missed the `B+x` to-do times and rescaled a `100%` keyframe, which kept a
   cursor on screen.
5. **Never hardcode click coordinates.** Use `aim({k: selector})` for the cursor's `--kx/--ky`
   variables and `placePills()` for toggle highlights. Both measure after webfonts load, so font
   or size changes don't break clicks.
6. **Snap, compare, render.** Snap key moments with `scripts/snap.py`, compare against
   `reference/`, then render each scene with `render.py`.
7. **Assemble.** Run `scripts/assemble.sh [out.mp4] [N=alt-clip.mp4 ...]` from the video folder.
   Crossfade offsets come from each clip's real duration, so retiming a scene needs no offset
   math.
8. **Verify every click.** Extract a frame at each click with
   `ffmpeg -ss <t> -i clip.mp4 -frames:v 1` and confirm the cursor is on target. Look at one frame
   per changed scene.

### Kit reference (`templates/claude-ui/claude-ui.js`)

| Builder / helper | What it gives you |
|---|---|
| `sidebar({active, chats, current, after, afterAt, user, plan})` | Real-order sidebar with account row; `after`/`afterAt` swaps the chat list mid-scene with no blank row |
| `sessionTopbar(title)`, `sessionComposer()`, `sessionPanel({progress, outputs, connectors, skills, skillsAt})` | Cowork session view with the floating right panel (Progress → Outputs → Context) |
| `todo({placeholder, rounds:[{at, collapseAt, items:[[label, activeLabel, startAt, doneAt]]}]})` | Real to-do behavior: list appears first, items pending → active ("-ing" label) → done, "N of M" counter, collapse |
| `connChip`, `skillRow`, `outRow` | Context-panel connector chips, skills rows, output files |
| `typeInto(el, text, start, cps)` | Per-character typing as seekable CSS animations |
| `aim({...})`, `placePills()`, `CURSOR_SVG` | Self-measuring cursor targets and toggle highlights |
| `icon(name)`, `ICON` | Stroke icons redrawn to match Anthropicons; add new glyphs here |
| `slideFrame(w, cls, inner)` | Scales a 1600×900 slide layout to thumbnail size for in-chat file previews |

---

## Measured snapshot: claude.ai dark mode, 2026-09-30

Perishable. Claude's UI changes often, so re-capture and diff before trusting any of these.

- **Colors**
  - backgrounds: `#151515` page, `#1b1b1a` sidebar, `#20201f` composer
  - text: `#f0efec` primary, `#c3c2b7` secondary, `#898781` muted
  - send button: `#c6613f` with a white arrow
  - "New" badge: blue `#6da7ec` text on `rgba(3,36,81,.75)`
- **Type** (real px, before scaling)
  - sidebar and body 14px, wght 360; toggle and model picker 13px; section labels 13px
  - badges 12px, wght 460
  - composer input 15px
  - Claude responses: serif 16px / 24px, wght 360
  - greeting: serif 38px, wght 290, `opsz` 48
  - "Claude" wordmark: serif 20px, wght 500
- **Composer:** radius 14, padding 8.
  - Chat/Cowork toggle: darker track; the active pill has a 1px `rgba(255,255,255,.1)` border.
  - Cowork adds a Beta badge, drops the voice button, and shows a "Project · Manual · Output" row
    and an "Active" task list.
- **Sidebar order:** New, Projects, Artifacts, Scheduled, Customize, More, then Pinned, then
  "Chats and tasks" with a filter icon. The account row has a chevron plus download and search
  icons. (The reference video drops the Scheduled section on request.)
- **Session view:**
  - top bar: laptop icon with a green dot, title and chevron, blue panel button
  - your message in a faint bubble; Claude's narration in serif
  - tool activity as plain grey lines ("Loaded tools, used Google Drive integration"), not boxes
  - bottom composer: "Write a message…", with "Manual" and the model name below it
- **Right panel:** a floating grey card in the order Progress → Outputs → Context. Context shows
  Connectors as rounded chips and Skills as a list. Outputs shows a count ("Outputs 5") and plain
  grey file icons.
- **To-do list**
  - before work: "See task progress for longer tasks."
  - pending: faint grey circle with a grey number
  - active: thin blue ring `#3987E5`, with the label switched to an "-ing" form
  - done: filled blue circle with a dark check, label struck through in grey
  - "N of M" on the header line
  - once everything is done, collapses to "Progress ›"
  - inline chat line: "Updated tasks, …"
- **Skill save:** a "SKILL PROPOSAL" label above a card with `/name`, a "new" tag, a description,
  "Content ›", and Dismiss/Save buttons. After Save it collapses to "✓ Saved as /name ›".
- **Customize → Connectors**
  - header: serif "Customize" title, tabs Skills / Connectors / Plugins, a Yours | Discover
    switch, search, filter, and a white "+ Add" button
  - Yours: a table (Connector / Type / Status) with a check mark for each connected tool
  - detail page:
    - "← Your connectors" back link, Disconnect button and ⋮ menu
    - "Prompt suggestions"
    - "Tool permissions", grouped into read-only and write tools
    - three-way controls per tool (allow / ask (hand) / block)
