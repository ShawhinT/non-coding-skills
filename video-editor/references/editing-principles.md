# Editing Principles

Shaw's YouTube videos are educational/technical content (slides + voiceover). The editing style should preserve the natural, thoughtful pacing of a teacher explaining concepts.

## Core Philosophy
- **Conservative:** when in doubt, keep it — but "conservative" means preserving *substantive* content, not preserving failed takes. Raw recordings with multiple takes commonly contain 50-80% cuttable material; removing all of it is expected, not aggressive.
- The goal is a clean rough cut, not a polished final product
- Preserve the speaker's natural rhythm and personality
- Educational content needs breathing room — don't make it "punchy"

## What to Cut
1. **Extended silences** (>2s): Reduce to ~0.8s, but never remove all silence
2. **False starts:** Speaker begins a thought, stops, and restarts
3. **Repeated content:** When the same idea appears multiple times — whether word-for-word, rephrased, or as a vague-then-specific pair — keep only the last version. This includes the surrounding silence. If the speaker tried something several times and then moved on to a different topic entirely, cut all attempts.
4. **Pre/post-roll dead air:** Keep 1s before first word, 1s after last word
5. **Filler words:** "um", "uh", "like", "you know", "so", "and so", "and then"
6. **Obvious mistakes:** Coughing, phone notifications, "let me start over"

## What to Keep
- All substantive content, even if imperfect
- Natural pauses between thoughts (up to ~2s)
- Deliberate emphasis pauses
- Transitions between topics
- Any content you're unsure about — let the user decide

## Audio Guidelines
- Target loudness: -16 LUFS (YouTube spoken word standard)
- Normalize volume across segments
- Don't apply compression or EQ — that's for the final edit

## Timing Rules
- Never cut mid-word or mid-sentence
- Find natural pause points (end of phrase, breath)
- Minimum segment length: 0.25s (avoid jarring micro-cuts)
- When reducing silence, keep at least 0.3s gap between speech segments
- Ground every segment boundary in word-level timestamps: each kept segment must start at the preceding kept word's start time (or slightly before), and end 0.25s after the last kept word's end timestamp to preserve the natural audio tail — but never overlapping the next kept segment's first word

## Filler Word Removal
Fillers should be **surgically removed** via sub-clips, not left in because the surrounding content is good. The `propose_edits.py` script handles this automatically, but when reviewing:
- When a filler appears mid-sentence, the script creates two sub-clips: before and after the filler
- Standalone fillers ("um", "uh") are always cut
- "Like" is only cut when used as a filler, not when it means "such as" or "similar to"
- Filler bigrams ("you know", "and so", "and then") are treated as a unit
- Sub-clips shorter than 0.25s are merged with adjacent segments rather than kept standalone

## Within-Segment Repeated Takes
Back-to-back restarts with <1s gaps are common in multi-take recordings. Speakers often restart a sentence 2-5 times before completing it. The script detects these by:
- Looking for matching first 3+ substantive words across nearby utterances
- Using text similarity (>0.5) to catch rephrased attempts
- Always keeping the **last complete version** of a repeated take
- When the last take appears incomplete (much shorter than others), falling back to the second-to-last

During review, verify that segments flagged with borderline similarity (0.4–0.6) are genuinely repeated takes and not unique content that happens to start similarly.

## Incomplete Sentences
Sentences trailing off into "um", "and", "so" without completing a thought should be trimmed. Common patterns:
- "...and then, um" → trim "and then, um"
- "...so, like, the" → trim "so, like, the"
- Trailing conjunctions with no following clause

The script trims these automatically, but only when the trailing words are clearly incomplete — it won't trim a sentence ending with "and" if that's part of a list ("apples and").

## Expected Retention
Use these ranges to calibrate whether the edit is too aggressive or too conservative:
- **Multi-take recordings** (speaker restarts frequently): **30–45%** retention
- **Single-take recordings** (clean delivery, minimal restarts): **70–90%** retention
- **Mixed recordings** (some sections clean, some with many takes): **50–65%** retention
- If retention falls outside these ranges, review the cuts — the script may be over-cutting unique content or under-cutting repeated takes
