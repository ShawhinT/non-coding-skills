# Video Editor Skill

Edit YouTube videos (slides + voiceover) by analyzing raw recordings, proposing cuts, and generating FCPXML project files for Final Cut Pro / DaVinci Resolve. Non-destructive — never renders or overwrites original video files.

See `SKILL.md` for the full workflow Claude follows.

## Prerequisites

- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) for dependency management
- `ffmpeg` and `ffprobe` on your `PATH`
- An [AssemblyAI](https://www.assemblyai.com/) API key (used for verbatim transcription)

## Setup

1. **Install as a Claude Code skill** by placing this folder at `~/.claude/skills/video-editor/`:
   ```bash
   cp -r video-editor ~/.claude/skills/video-editor
   cd ~/.claude/skills/video-editor
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure your API key:**
   ```bash
   cp .env.example .env
   # then edit .env and paste your AssemblyAI key
   ```

## Usage

Once installed, just ask Claude Code things like:
- "Edit `~/Videos/raw-take.mp4` using the video-editor skill"
- "Analyze this recording and propose cuts"

Claude will run the three-phase workflow (analyze → propose edits → generate FCPXML) and write all outputs to `<your-cwd>/claude-edits/`. Import the resulting `.fcpxml` into Final Cut Pro via **File → Import → XML**.

## Files

```
SKILL.md            # instructions Claude follows
scripts/            # analyze, transcribe, propose_edits, generate_fcpxml
references/         # editing principles + FCPXML format reference
.env.example        # template for API keys
```
