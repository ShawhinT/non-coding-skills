# Talking-Head Editorial Guide

Scripted talking-head: Shaw reads from a written script in front of the camera and re-records each line until satisfied. The raw is a chain of takes — the **last take of each line is the keepable one**, and earlier attempts are drafts.

This is a subtype of voiceover. **First apply every rule in `voiceover.md`** — the core "last take wins" philosophy, the abandonment cues, the trim-don't-discard rules — all carry over. The notes below layer on top.

## The pipeline produces a handoff, not a finished cut

Aim for: takes intact, between-take cuts made, obvious drops applied. The editor will do the granular pacing work in FCP — subdividing fluent takes, tightening pauses, trimming pad — using the timeline scrubber. Calibrate against that goal. Pre-merging across natural pause points or over-padding clips destroys the editing surface area the human will use.

## What's different from voiceover

**1. Inter-take pauses are longer.** Pure voiceover is recorded sentence-by-sentence with tight pauses. On camera, the speaker looks up at the script, settles, then delivers — so the pause between two takes of the same line is commonly **2–10+ seconds**, not the tenths of a second you see in VO. The pauses within a continuous take run shorter, ~0.3–0.5 s at clause boundaries. The pipeline's merge threshold should sit comfortably between these ranges.

**2. Delivered structure ≠ scripted structure.** The speaker writes the script as bullets where each bullet is one intended beat, but delivery often diverges:
- Two scripted bullets may be delivered as one continuous take (no audible pause between them).
- One long scripted bullet may be delivered as 2–3 sub-utterances with natural breath pauses.
- The speaker revises on the fly — lines get added, removed, or reworded mid-recording.

The transcript is the only source of truth. The pipeline's job is to keep continuous takes intact and respect the obvious between-take pauses — not to match either the script or the editor's eventual FCP layout.

**3. Bridge-fragment trap.** When two adjacent kept segments are separated by **>1.0 s of silence**, they are almost never one continuous sentence — even when the script intends them as one. A real example: scripted *"But this isn't the main value of skills"* was delivered as `["But this"] — 1.47 s pause — ["isn't the main value of skills"]`. The "But this" fragment is stranded; drop it. The rule applies regardless of script intent: a >1 s mid-sentence pause makes the pre-pause fragment droppable.

This counters the voiceover rule "*takes span segment boundaries*" — that rule was written for the sub-second silences typical of VO. In talking-head, large gaps mean *separate takes*, not bridges.

**4. Analogy openers are load-bearing.** A sentence that opens an analogy and the sentence delivering the analogy's payoff are one rhetorical unit. Before dropping an apparent retake, check the next segment — if it's the analogy's *"and that's why…"* or *"have that same level of patience,"* the opener stays. Last-take-wins would otherwise drop the framing for a payoff that no longer makes sense.

**5. Speaker directives.** Verbal directives like *"scratch previous line"*, *"let me redo that"*, or *"actually, [reframe]"* are backward-looking, and their scope can be larger than the immediately-preceding fragment — sometimes covering a full alternate framing the speaker just developed. Surface them to Step 0.5 with raw transcript context spanning at least 30 s before and after the directive; don't have the chunk editor guess scope.

## AssemblyAI timing caveat

For fast soft-attack opening phrases ("A few weeks ago…", "And then…"), AssemblyAI commonly under-reports the word-**start** time by 100–300 ms. The tell is implausibly short reported durations for opening vowels (e.g., the letter "A" reported as 17 ms). This causes head-clipping when lead-in pads are anchored to a too-late timestamp.

## Recommended pipeline parameters

The script defaults are tuned for pure voiceover. For talking-head, pass these explicitly:

- `preprocess.py --silence-gap 0.20` — tighter splitting separates tight false-start/restart pairs that would otherwise fuse into one segment. Default 0.35 misses gaps in the 0.2–0.35 s range.
- `assemble_edl.py --merge-gap 1.0 --lead-in 0.12 --tail-pad 0.20` — `--merge-gap 1.0` sits above natural within-take breath pauses (~0.3–0.5 s) and well below inter-take pauses (~1.5 s+), so continuous takes stay whole and between-take pauses become clip boundaries. The tighter pads compensate for AssemblyAI timing slop without padding clips with dead air the editor would have to trim.

These are starting points. If the user reports clipped phrase heads, bump `--lead-in` toward 0.18. If between-take pauses are unusually short on a given recording, lower `--merge-gap` toward 0.6.

## Known limitation

False-start/restart pairs separated by **<0.20 s of silence** still fuse into a single transcript segment even with `--silence-gap 0.20`, and the chunk editor operates at segment granularity — it can drop a whole segment but cannot trim within one. Surfaced examples on this footage included `"thing that makes— the thing that makes…"` (0.19 s gap) and `"He was still using it. He was still using it for…"` (0.21 s gap). The current pipeline cannot remove just the abandoned half of these. Flag them in the final review and trim manually in FCP.

## Expected retention

Similar to voiceover — roughly a quarter to a little over half of the raw runtime. Talking-head scripts often run closer to the lower end because each line typically has 3–6 retake attempts on the raw, vs 1–3 for VO.
