---
name: video-editor-v3
description: Edit a single video for Shaw's YouTube channel by transcribing it, planning cuts with a multi-agent pipeline, writing an EDL JSON, and generating an FCPXML project file for Final Cut Pro. Use when the user asks to edit a video, cut a voiceover, or produce an FCPXML from a raw recording. Never renders or overwrites the original video file.
---

# Video Editor Skill (v3)

Edit a single video by reading the audio, producing a word-level transcript, planning cuts with a multi-agent pipeline, and emitting both an Edit Decision List (EDL) and an FCPXML project file for Final Cut Pro. **Never render or overwrite the original video file.**

## Input

The caller provides:

- `source_file` (required) — absolute path to the source video file.
- `video_type` (required) — `voiceover`, `talking-head`, or `event`. Selects the editorial reference.
- `parent_file` (optional) — absolute path to the parent video. Defaults to `source_file`.
- `transcript_path` (optional) — path to a word-level transcript JSON shaped `{"words": [{"word", "start", "end"}, ...]}`. If absent, Step 0 generates one via AssemblyAI.
- `source_duration` (optional, seconds) — if absent, probe via `ffprobe`.
- `project_root` (optional) — directory under which the `claude-edits/` scaffold is created. Defaults to the per-video draft folder (see below), NOT the raw folder or the current working directory.

## Output directory

**Shaw's channel SOP (default):** edits live under `2-drafts/`, never in `1-raw/` (raw holds only source media). Each video gets its own folder `2-drafts/<video-name>/` containing `claude-edits/` (this skill's artifacts) alongside `shaw-edits/`, optional `assets/`, and the eventual `<video-name>_draft.mp4`. So `project_root` = `…/_YouTube/2-drafts/<video-name>/`. Derive `<video-name>` from the raw folder name (e.g. raw `1-raw/agentcon-2026/` → draft `2-drafts/agentcon-2026/`); create the draft folder if it doesn't exist. If a `claude-edits/` for that video already exists from a prior pass, write the new run to `claude-edits-v2/`, `-v3/`, … (the channel keeps versioned passes). The FCPXML references source media by absolute `file://` path, so the project folder can sit in `2-drafts` while the media stays in `1-raw` — the two need not be colocated.

**Project naming SOP:** pass `--project-name <video-name>_draft` (e.g. `agentcon-2026_draft`) to the FCPXML step so the event/project label inside Final Cut matches the channel's `<video-name>_draft.mp4` convention. Name the output file `edit.fcpxml` as usual; it's the `--project-name` value that shows up in FCP.

All artifacts go in `<project_root>/claude-edits/`. Create the folder if missing. Nothing is ever written next to or on top of the source video.

```
<project_root>/claude-edits/
    transcript.json               # Step 0
    segments.json                 # Step 1
    chunks/
        chunks.json               # Step 2 manifest
        chunk_N.json              # Step 2 (segments per chunk)
        chunk_N.txt               # Step 2 (human-readable)
        chunk_N_segments.json     # Step 3 (per-chunk keep segments)
        all_segments_validated.json  # Step 4
        dedup_context.txt         # Step 5b input
        dedup_drops.json          # Step 5b output
    edl.json                      # Step 6 (final EDL)
    edit.fcpxml                   # Step 7 (Final Cut Pro project)
```

Below, `<project_dir>` refers to `<project_root>/claude-edits/`.

## Tools required

- `ffmpeg` / `ffprobe` — video probing (duration + format metadata for FCPXML).
- AssemblyAI API — verbatim word-level transcription with disfluencies preserved.
- `uv` — runs the Python scripts.

## Configuration

- **AssemblyAI API key** — place a `.env` file in the skill directory (`video-editor-v3/.env`) containing `ASSEMBLYAI_API_KEY=...`. The skill ships without a `.env`; the caller must supply one.
- All scripts run from the skill directory: `<skill_dir>` = the install path of the `video-editor-v3` skill. Prefix each command below with `cd <skill_dir> && ` or invoke from that directory.

## EDL schema

```json
{
  "source_file": "<source_file>",
  "parent_file": "<parent_file>",
  "source_duration": <float seconds>,
  "segments": [
    {"start": <float seconds>, "end": <float seconds>},
    ...
  ]
}
```

- Segments are time ranges to **keep** — everything outside is cut.
- Chronological, non-overlapping, clamped to `[0, source_duration]`.
- Timestamps to 4 decimal places, aligned to word boundaries (never cut mid-word).

## Routing — which editorial guide to follow

Pick the reference file(s) based on `video_type`:

- `voiceover` → `video-editor-v3/references/voiceover.md`
- `talking-head` → `video-editor-v3/references/talking-head.md` **and** `video-editor-v3/references/voiceover.md` (talking-head layers on the voiceover core; sub-agents must read both)
- `event` → `video-editor-v3/references/event.md`

The reference file tells you what to cut, what to protect, and how to think about the content type. This SKILL.md only describes the **type-agnostic mechanical pipeline** — anything that varies by video type lives in the routed reference, not here. That includes: editorial judgment (what to cut/protect), **pacing-parameter overrides** for the scripts (e.g. `preprocess.py --silence-gap`, the `assemble_edl.py` knobs), and any **extra pipeline step** a type needs (e.g. the event Q&A review gate). Where a step's parameters or sequence depend on the type, the step below points to the reference rather than naming a type — so read the routed reference before running the pipeline and apply the parameters and steps it specifies. If you're adding type-specific guidance, it belongs in the reference file, never in a step description here.

## Pipeline

Create `<project_dir>` (`<project_root>/claude-edits/`) before Step 0. Run each step from the skill directory so `uv run` resolves the environment.

### Step 0 — Transcribe (skip if `transcript_path` is provided)

```
uv run scripts/transcribe.py <source_file> --output-dir <project_dir>
```

Writes `<project_dir>/<video_stem>_transcript.json` (the script names the file after the video stem). Set `transcript_path` to that output path for downstream steps.

If `source_duration` was not provided, probe it now:

```
ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 <source_file>
```

### Step 0.5 — Confirm the editorial brief with the user

Before Step 1, confirm the brief with the user in one short message. Skim the transcript first so the questions are specific (length, structure, obvious cut candidates) rather than generic. Cover:

- **Video type** — `voiceover` vs `talking-head` vs `event`. Confirm or correct the routed reference; flag if the transcript looks like a hybrid. `talking-head` is scripted on-camera delivery with multi-second pauses between retake attempts (vs `voiceover`'s tight sentence-by-sentence cadence); if the brief mentions reading from a script in front of a camera, route talking-head.
- **Output destination** — confirm `<project_root>/claude-edits/` and the FCPXML project name (auto-generated names like `<video_stem>_edit` rarely match what the user wants in Final Cut).
- **Editorial intensity** — minimum cuts, standard pacing, or aggressive trim. The reference files default to standard pacing; a "minimum cuts" brief overrides them.
- **Audience and narrative priority** — who is this for, and how self-explanatory must the result be? For a non-expert audience (e.g. business users), transitions, topic introductions, and a term's first definition are load-bearing and must survive even an aggressive cut — "aggressive" then means *remove drafts and redundancy*, not *remove connective tissue*. Pass this to the chunk agents so "tight" is never read as "skip the narrative scaffolding."
- **Mandatory drops or keeps** — sponsor reads, dead segments, specific stories the user wants protected. Resolve any rough timestamps against the transcript so the brief carries word-boundary numbers. (Don't resolve *which individual Q&A questions* to cut here if a routed reference defines a review gate for that — e.g. `event.md` enumerates the pairs for the user to prune later. Here just confirm whether the Q&A stays in at all.)
- **Anything you noticed in the transcript** — flag specific moments (tech-check, mispronunciation, abandoned tangent, verbal directives like "scratch previous line") and ask whether to cut. The transcript almost always contains a judgment call the caller's initial request didn't anticipate. When surfacing ambiguous moments to the user, paste a raw transcript window (timestamps + verbatim words), not a Claude paraphrase — the framing of the question determines the answer.

Recommend a default for each item so the user can answer "ok" rather than write paragraphs. The user's response is the editorial brief that gets passed verbatim into chunk sub-agents (Step 3) and the dedup pass (Step 5b) — the existing rule that an explicit brief overrides conflicting generic rules depends on this step having actually happened.

### Step 1 — Preprocess transcript

Convert the word-level transcript into segment-level JSON. Segments are groups of consecutive words split at silence gaps (default 0.35s), preserving every word via concatenated text.

```
uv run scripts/preprocess.py <transcript_path> -o <project_dir>/segments.json
```

The default `--silence-gap` is `0.35`. If the routed reference specifies a different value for its type, use that — the reference carries the value and the rationale.

Output: `{"segments": [{"text", "start", "end"}, ...]}`. Prints `{n_words, n_segments, total_chars}` to stdout.

### Step 2 — Partition segments into content-aligned chunks

Spawn an **Opus sub-agent** (`model: "opus"`) to decide chunk boundaries editorially. Equal-duration windows mishandle videos with uneven content density (a 45-minute abandoned demo that wants one chunk, a 5-minute takeaways block that wants its own).

Pass the Opus sub-agent:

1. Path to `segments.json` from Step 1.
2. Path to `scripts/split_chunks.py` (the helper it will call).
3. Target chunk count: **8–10 chunks** — but sizes need not be equal.
4. Output directory: `<project_dir>/chunks`.

Tell the sub-agent to:

1. Read `segments.json` fully (paginate with `offset`/`limit`).
2. Identify content-aligned boundaries. Useful cues: `grep` for transition phrases ("demo time", "let's walk through", "key takeaways", explicit editor notes).
3. Assign each chunk a **title** and **rationale** (1–2 sentences describing what's in the chunk and what editorial policy fits). Both fields are mandatory.
4. Emit all chunk files in a single call:

   ```
   echo '{"chunks":[{"id":0,"start_seg_idx":0,"end_seg_idx":N,"title":"...","rationale":"..."}, ...]}' \
       | uv run scripts/split_chunks.py <project_dir>/segments.json <project_dir>/chunks
   ```

   The script validates indices cover `[0, n_segments-1]` contiguously, writes `chunks.json`, `chunk_N.json`, and `chunk_N.txt`. Prints the manifest.

5. Return the manifest to the parent session.

### Step 3 — Dispatch chunk sub-agents in parallel

For each chunk in `chunks.json`, spawn a Sonnet sub-agent (`model: "sonnet"`). Pass each:

1. Path to its `chunk_N.json` and `chunk_N.txt`.
2. The chunk's `title` and `rationale` from `chunks.json` — without this framing, a sub-agent seeing 45 minutes of debugging might preserve it as instructional content.
3. `source_duration` for the full video.
4. The full editorial rules from the routed reference file (`voiceover.md` or `event.md`).
5. **The editorial brief from the dispatch prompt, verbatim, if one was provided** — overrides any generic rule that conflicts. When the brief drops a structural block, content immediately adjoining that block (promo tails, preamble, wrap-ups) falls under the drop as well.
6. The `<transcript_path>` and the path to `scripts/transcript_lookup.py` (the word-level lookup tool — see below).
7. The output format below.

Each sub-agent returns a JSON array of **keep segments** for its chunk:

```json
[
  {"start": <float>, "end": <float>, "reason": "<brief note>"},
  ...
]
```

Sub-agents write to `<project_dir>/chunks/chunk_<id>_segments.json`. If Write is unavailable in the sub-agent, collect the JSON from the text response and write it from the parent session.

Run sub-agents in parallel wherever the API allows.

#### Word-level trimming inside a segment (head-trim / internal restart)

The chunk files carry only segment-level `start`/`end` and the concatenated `text`. A segment can therefore contain a **fused take** — a false start, a repeated opening, or a throat-clear bridging two attempts — that the silence-gap splitter never broke apart (filler vocalizations like "ahem"/"um" are transcribed as zero-gap words, so no gap ever crosses the split threshold). The agent can *see* the repeat in the `text` but the segment object gives it no timestamp for where the clean take begins.

Resolve this with `scripts/transcript_lookup.py` — a pure-data tool (no take detection, no trimming) that returns ground-truth word timings so the agent cuts at a real boundary instead of guessing:

```
# words (with gap_before) overlapping a segment you suspect is fused
uv run scripts/transcript_lookup.py <transcript_path> --start <seg_start> --end <seg_end>

# every occurrence of a repeated opening, with exact start times
uv run scripts/transcript_lookup.py <transcript_path> --phrase "hey everyone i'm shaw"
```

Tell each sub-agent, as a **required end-of-pass sweep**: for every kept segment whose `text` repeats its own opening phrase, or opens/closes on a stutter, call `transcript_lookup.py` over that segment, then **head-trim** (move `start` forward) or **tail-trim** (move `end` back) to the boundary of the last clean take — `--phrase` returns the candidate occurrences; keep the last. A repeated `Hey everyone, I'm Shaw … Hey everyone, I'm Shaw` should start at the second occurrence's `match_start`.

**Guardrail (relaxed, narrowly):** the standing rule is *do not invent timestamps*. The one exception: a `start`/`end` may be set to a word boundary **retrieved from `transcript_lookup.py`**. Never type a timestamp you did not read from the tool, the chunk file, or `chunks.json`. Step 4 still snaps every value to the nearest real word boundary, so a tool-sourced number is safe and a hand-typed one cannot survive — that check is a boundary snap, not editorial judgment.

#### Narrative-continuity self-check (before returning)

Per-segment judgment optimizes each clip for take-quality and uniqueness; nothing downstream verifies that the surviving **sequence** still explains the topic. Before returning, read your keep list end-to-end in order, as the viewer will hear it, and look for the breaks that local judgment cannot see:

- a term used before it is introduced (its first definition got cut),
- a section that starts with no transition (the bridge lived only in a take you dropped),
- an examples block with no payoff line (the synthesis that says what they *meant* got cut), or
- the same beat stated twice (two clean takes of one idea both survived).

Fixing the first three usually means **adding a keep back** — restoring a transition, definition, or synthesis segment you cut. Only the chunk pass can do this: Step 4 (validate), Step 5 (dedup), and Step 6 (assemble) can only *remove* and *stitch*, never restore. Editing for a coherent narrative rather than a notes file is the whole point of this step — a tight cut that a first-time viewer can't follow is a failed cut, not an aggressive one.

### Step 4 — Validate timestamps

Agents produce timestamps from memory and hallucinated timestamps are a common failure mode. Snap every `start`/`end` to a real word boundary before stitching.

```
uv run scripts/validate_segments.py <project_dir>/chunks <transcript_path> \
    -o <project_dir>/chunks/all_segments_validated.json
```

Snaps to nearest word start/end via `bisect`, drops zero-length segments, sorts chronologically. Prints `{n_segments, snaps, retention_pct}`.

### Step 5 — Stitch boundaries and global dedup

Catches cross-chunk duplicates that per-chunk editors cannot see.

**5a — Boundary stitching.** For each pair of adjacent chunks, spawn a stitching sub-agent that reads the last ~30 s of chunk N and first ~30 s of chunk N+1 as human-readable text, and decides whether any segments across the seam are duplicates. Fallback heuristic: if any pair across the boundary shares a long substantive word prefix or has high similarity, cut the earlier one.

**5b — Global dedup pass.** First build the context file:

```
uv run scripts/build_dedup_context.py \
    <project_dir>/chunks/all_segments_validated.json <transcript_path> \
    -o <project_dir>/chunks/dedup_context.txt
```

Then spawn a dedup sub-agent (Sonnet). Pass it:

- The path to `dedup_context.txt` (one segment per line with `[idx NNN | start-end]` prefix).
- The editorial brief from the dispatch prompt, verbatim, if one was provided — dedup should also drop content the brief excludes.
- Instructions to output a JSON list of `{start, end, reason}` entries to drop, written to `<project_dir>/chunks/dedup_drops.json`.
- A continuity lens alongside the dedup mandate: reading the full sequence in order, flag any *cross-chunk* break — a term used before it is introduced, a section starting with no transition, an examples block with no payoff — back to the parent session. This pass can only *remove*, so it cannot fix a break itself; surface it so the parent can re-dispatch the relevant chunk (which still can restore the missing keep).

> **Reference-inserted steps.** A routed reference may define an extra step that runs here, before assembly — e.g. `event.md` specifies an interactive **Q&A pair review gate** that pauses to let the user prune whole question/answer pairs. Consult the routed reference and run any step it inserts (its output feeds `dedup_drops.json`, which Step 6 already consumes) before continuing.

### Step 6 — Assemble the final EDL

```
uv run scripts/assemble_edl.py \
    <project_dir>/chunks/all_segments_validated.json \
    <project_dir>/chunks/dedup_drops.json \
    --source-file <source_file> --parent-file <parent_file> --source-duration <source_duration> \
    --transcript <transcript_path> \
    -o <project_dir>/edl.json
```

Removes dedup drops, merges segments with small gaps, tightens interior dead air, applies lead-in/tail pad, drops sub-second keeps, clamps, and validates the schema before writing. Prints `{edl, n_segments, n_internal_splits, retention_pct}`.

Four knobs control how aggressively the assembler stitches, tightens, and pads: `--merge-gap` (merge two adjacent kept segments separated by less than this many seconds), `--lead-in` (audio padding before each segment), `--tail-pad` (after), and `--max-internal-gap` (split a kept segment wherever an interior word-gap exceeds this many seconds). The defaults `0.3 / 0.08 / 0.15 / 0.6` are the type-agnostic starting point (tuned on voiceover). The routed reference specifies the override values for its type and the rationale — use those when editing that type.

**Interior dead-air tightening.** Merge/pad only close gaps *between* kept segments; a breath or thinking-pause *inside* a multi-sentence keep range survives untouched, and the viewer hears it as dead air. Pass `--transcript` so the assembler splits each kept range at interior word-gaps over `--max-internal-gap`, dropping the silence while landing every cut on a real word boundary. This automates a human editor's single most common tightening move — closing pauses inside otherwise-good takes — so `n_internal_splits` will normally be well above zero on a real edit. Omitting `--transcript` reverts to the old between-segment-only behavior. Raise `--max-internal-gap` toward `1.0` if the cut starts to feel clipped/breathless, lower it toward `0.4` for tighter pacing.

Check `retention_pct` against the expected range in the routed reference file. If out of range, revisit the cuts (drop more in `dedup_drops.json`, or re-dispatch a chunk) and re-run the assembler — do not ship a misaligned edit.

### Step 7 — Generate FCPXML

```
uv run scripts/generate_fcpxml.py <project_dir>/edl.json -o <project_dir>/<name>.fcpxml --project-name <name>
```

Pass `--project-name` with the FCPXML project label confirmed in Step 0.5 — otherwise the event and project inside the XML auto-name after the source video stem (e.g., `C0392_edit`), which rarely matches what the user wants in Final Cut. Use the same `<name>` for both the output filename and the `--project-name` flag.

Produces FCPXML v1.11 that:

- References the original video file (non-destructive — no re-encoding).
- Maps each kept segment to an `<asset-clip>` on the timeline spine.
- Probes format (width/height/fps) from `source_file` via `ffprobe`.
- Imports into Final Cut Pro (File → Import → XML) or DaVinci Resolve.

Prints `{fcpxml, n_clips, timeline_duration_s, source_duration_s}`.

### Step 8 — Place overlay assets (optional)

Use when the script has `[CARD]` / `[ANIMATION]` callouts and the corresponding MP4s already exist (built via `animation-builder` or supplied by the user). Places each MP4 on lane 1 above the spine. Works on either the freshly-generated FCPXML (Step 7) or a hand-edited FCPXML the user produced in Final Cut.

**Placement is a Claude judgment task, not a phrase-match arithmetic.** The script and the transcript diverge (the user ad-libs, restates, skips, reorders mid-recording). The "right" timeline position for each overlay depends on cadence, breath, where the spine cut landed, the energy of the spoken line, and how the line relates to the on-screen beat — none of which a deterministic Python rule can decide from a single trigger phrase. So in this skill, a Claude sub-agent reads the script + transcript + spine and decides timeline positions; the Python emitter just translates those decisions into valid FCPXML. (Same pattern as Step 3 chunk sub-agents: judgment in Claude, structure in Python.)

**Step 8a — Dispatch a placement sub-agent (Sonnet).**

Pass it:

1. Path to the **script text** (the user's editorial intent — typically a Notion doc fetched as plain text, or pasted into the prompt). If the user hasn't supplied a script, ask for one before dispatching — without it the sub-agent is doing phrase-match again, defeating the point.
2. Path to the word-level transcript JSON (`{"words":[{"word","start","end"},...]}` — recorded reality).
3. Path to the existing FCPXML (so it can read the spine and know what survived the cut).
4. List of asset MP4 absolute paths, in script order. Filenames carry editorial intent — `2-card-mindset_shift.mp4` corresponds to the "mindset shift" beat in the script; `7-animation-calendar_timesinks.mp4` corresponds to the "calendar / time sinks" beat.
5. The instruction: for each asset, decide the timeline `start` (seconds) where the overlay belongs *over the spoken content*, and optionally a `duration` (seconds) when the editorial slot wants a different length than the asset's natural render.

The sub-agent's prompt should emphasize:

- **Match each asset to a script beat by name, then locate that beat in the transcript** to get word-level timestamps. The script tells you "what's the intended idea here"; the transcript tells you "when (and whether) it actually got said." Reconcile divergences (skipped sections, restated lines, ad-libs) explicitly.
- **Translate from source time to timeline time** using the spine map (each spine `<asset-clip>` has `start` = source-in and `offset` = timeline-position). `timeline_t = clip.offset + (source_t - clip.start)` for a source time inside that clip. The sub-agent can write a few lines of inline Python for this.
- **Overlays land *over* the spoken content, not at its leading edge.** A card should appear during the new section's opening line, not at the cut from the previous section. An animation should build during the words it's illustrating, not before them. The exact position is the sub-agent's call — informed by what's natural to read at playback distance, not by a constant offset.
- **`duration` only when the slot wants it.** Default is the asset's render length. Override only when the talking-head section is tighter than the asset (trim it) or wants an emphasis hold longer than the asset (extend; FCP holds the final frame).

Output format — write to `<project_dir>/placements.json`:

```json
{
  "placements": [
    {"asset": "/abs/path/.../2-card-mindset_shift.mp4", "start": 52.3, "duration": 4.0},
    {"asset": "/abs/path/.../3-animation-effort_curve.mp4", "start": 78.4},
    …
  ]
}
```

No `phrase`, no `kind`, no `lead_in` — those were the old phrase-match scheme. The sub-agent has already accounted for all of that when picking `start`.

**Step 8b — Emit the FCPXML.**

```
uv run scripts/place_overlays.py <existing.fcpxml> <project_dir>/placements.json -o <project_dir>/<name>_overlays.fcpxml
```

The emitter probes each asset shape via ffprobe, declares a `<format>` resource per unique (width, height, fps) combination, finds the primary spine clip containing each `start` position, and inserts the overlay as a connected `<asset-clip lane="1">` nested inside that host clip in DTD-correct position. Prints one line per overlay (`tl=<seconds> dur=<seconds>`) and flags any placement that fell outside every spine clip (likely a sub-agent timestamp error — re-dispatch or hand-correct that entry).

**Placing overlays against a rendered MP4 (not an FCPXML).** If the source is a flat cut — the editor handed you an MP4, the cut originated outside this skill, or the upstream FCPXML's spine and the rendered MP4 have drifted apart — pass the media file directly as the first argument. The emitter detects `.mp4` / `.mov` / `.mkv` / `.m4v` and auto-wraps it as a single-spine sequence before placing overlays:

```
uv run scripts/place_overlays.py <cut>.mp4 <project_dir>/placements.json -o <project_dir>/<name>_final.fcpxml
```

The reason this matters: FCPXML durations are frame-aligned rationals like `19134115/30000s` that look like arbitrary numerators. A single transposed digit produces a project that's sub-second-off — small enough to look right at a glance, large enough to drift every overlay placement past its VO line. The emitter's wrapper computes those rationals via `to_frame_str`; bypassing it by hand-authoring a wrapper FCPXML re-introduces the typo class. Reach for the script, not the keyboard.

See `references/fcpxml-format.md` ("Connected Clips and Lanes", "DTD Content Order", "Mixed Formats") for the structural rules the emitter enforces.

**Redaction (on request only).** When the user asks to obscure something visible on screen — emails, PII, keys — follow **`references/redaction.md`**: exposure mapping, patch/blur design, the still-image→ProRes-alpha detour (the emitter takes video assets only), spine micro-cuts, and FCPXML round-trip gotchas all live there. Never run it as a default step.

### Step 7-alt — Dual-source picture-in-picture (rare)

When the shoot has **two recordings of the same talk** — e.g. a speaker camera plus a separate screen/slides capture — and you want one full-screen as the main show with the other as a synced PiP inset (usually keeping the *better* recording's audio), use `make_pip_fcpxml.py` **instead of** Step 7. This path is uncommon; the full workflow — audio-sync discovery, the emitter, the FCP transform coordinate system, and verification — lives in **`references/picture-in-picture.md`**. Read it before running.

## Output

The final deliverables are `<project_dir>/edl.json` and `<project_dir>/edit.fcpxml` (plus `<name>_overlays.fcpxml` if Step 8 ran). Report all relevant paths, the segment count, and the retention percentage to the user.
