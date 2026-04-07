# Video Editor Skill

Edit YouTube videos (slides + voiceover) by analyzing raw recordings, proposing cuts, and generating FCPXML project files for Final Cut Pro. **Never render or overwrite original video files.**

## Output Directory

**All outputs go in `<session_cwd>/claude-edits/`.** This is the working directory of the Claude Code session (NOT the skill directory). Create this directory if it doesn't exist. This keeps analysis files, EDLs, and FCPXML files separate from the user's source material. Nothing is ever written next to or on top of original video files.

**Important:** Since scripts run from the skill directory (for `uv run`), always pass `--output-dir <session_cwd>/claude-edits/` explicitly to every script. Never rely on the script's default output directory.

Output structure:
```
<session_cwd>/claude-edits/
    <video_stem>_analysis.json      # Phase 1 output
    <video_stem>_edl.json           # Phase 2 output
    <video_stem>_edit.fcpxml        # Phase 3 output
    <video_stem>_transcript.json    # Raw transcript
```

## Tools Required
- `ffmpeg` / `ffprobe` — video metadata, silence detection, audio extraction
- AssemblyAI API — verbatim word-level transcription with disfluencies preserved (primary)
- Python `xml.etree` — FCPXML generation (no extra deps)

## Configuration
- AssemblyAI API key: `.env` file in the skill directory (`~/.claude/skills/video-editor/.env` with `ASSEMBLYAI_API_KEY=...`)
- Scripts run via `uv run` from the skill directory (`~/.claude/skills/video-editor/`)

## Workflow

All commands below are run from the skill directory via `cd ~/.claude/skills/video-editor`. Always pass `--output-dir` pointing to `<session_cwd>/claude-edits/` so outputs land in the user's working directory, not the skill folder.

### Phase 1: Analyze
Run the analysis script on the video file:
```bash
cd ~/.claude/skills/video-editor
uv run scripts/analyze.py <video_path> --output-dir <session_cwd>/claude-edits/
```
This produces `<video_stem>_analysis.json` in the output directory with:
- Video metadata (duration, resolution, codec, framerate, audio info)
- Silent segments (threshold: -30dB, minimum duration: 1.5s)
- Per-segment audio levels
- AssemblyAI transcription with word-level timestamps (verbatim, disfluencies preserved)

Present a human-readable summary to the user.

### Phase 2: Propose Edits

**Step 1:** Run the edit proposal script to generate a draft EDL and review document:
```bash
cd ~/.claude/skills/video-editor
uv run scripts/propose_edits.py <session_cwd>/claude-edits/<stem>_analysis.json --output-dir <session_cwd>/claude-edits/
```
This produces:
- `<stem>_edl.json` — Draft EDL with keep/cut segments
- `<stem>_review.md` — Human-readable edit review

The script handles mechanical editing work in 5 passes:
1. Utterance segmentation (split by gaps >0.6s)
2. Take detection (repeated starts → keep last complete version)
3. Filler removal (surgical sub-clip splits around "um", "uh", "like", etc.)
4. Incomplete sentence trimming (trailing fillers/conjunctions)
5. Silence normalization (consistent 0.3–0.8s gaps)

**Step 2:** Read the review document (`<stem>_review.md`) and refine the EDL:
- Check all ⚠️ flagged decisions (uncertain repeats, borderline cuts)
- Verify unique content wasn't incorrectly grouped with repeated takes
- For content you're unsure about, keep it (let the user decide)
- Update `<stem>_edl.json` with any corrections

**Step 3:** Present a summary to the user:
- Total duration: original → edited
- Retention percentage
- Number of segments
- Notable cuts (long repeated sections, etc.)
- Any flagged decisions that need human review

### Phase 3: Generate FCPXML
Run the FCPXML generator:
```bash
cd ~/.claude/skills/video-editor
uv run scripts/generate_fcpxml.py <session_cwd>/claude-edits/<stem>_analysis.json <session_cwd>/claude-edits/<stem>_edl.json --output-dir <session_cwd>/claude-edits/
```
This produces an FCPXML v1.11 file that:
- References original video files (non-destructive)
- Maps each kept segment to a `<clip>` in the timeline spine
- Applies volume adjustments via `<adjust-volume>` elements
- Targets -16 LUFS for YouTube spoken word
- Imports into Final Cut Pro (File > Import > XML) or DaVinci Resolve

## File Structure
```
scripts/
    analyze.py          # Phase 1: ffprobe + silence detection + AssemblyAI transcription
    transcribe.py       # AssemblyAI API helper (verbatim mode with disfluencies)
    propose_edits.py    # Phase 2: mechanical edit proposal (5-pass pipeline)
    generate_fcpxml.py  # Phase 3: EDL → FCPXML conversion
references/
    editing-principles.md   # Shaw's editing style preferences
    fcpxml-format.md        # FCPXML structure reference
```
