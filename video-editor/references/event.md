# Live Event Editorial Guide

Event recordings are talks, presentations, and live workshops — usually single-take, with an audience. The editorial problem has two layers:

1. **Structural overhead** — pre-talk warm-up, Q&A preambles, logistics tail. Large, easy to spot.
2. **Pacing** — inter-sentence pauses, filler clusters, restatements, slide-hunting, hedged non-answers. Small, pervasive, and collectively a large fraction of the runtime.

A common mistake is to make only the structural cuts and leave pacing untouched. That lands around 85–90% retention and an edit that feels slack. A well-edited live talk has both layers trimmed — expect roughly 55–70% retention for a typical event with Q&A.

## Core editorial principle

Protect **substantive** continuous speech — the actual explanation, example, or answer — but trim everything *around* it: filler, repeated false starts, dead air while the speaker finds a slide, and restated sentences where the second pass is cleaner than the first.

The speaker rarely retakes anything deliberately, but they often self-correct in real time: they'll say a sentence, pause, then restate it better. In a live talk this is *not* "elaboration" — it's an in-the-moment retake, and the first pass should be cut.

## Retention as a self-check

- Typical event with Q&A: **~55–70% retention**.
- Tight talk, little Q&A: up to ~80%.
- Long workshop with heavy pre/post overhead: down to ~20%.

**If your kept segments for a chunk exceed ~75% of the chunk runtime and the chunk is not pure demo/screenshare, you are almost certainly under-cutting pacing.** Re-scan for restatements, slide-hunting, and filler clusters before returning. A single "keep everything" segment for a 10-minute chunk is almost always wrong.

Exception: when the source is itself an already-edited cut (a second editorial pass over a rendered final), the filler a first pass removes is already gone, so much higher retention is normal. Absence of cuttable material is not under-cutting — don't force cuts to hit the range. The brief should state the second-pass context so chunk agents apply this exception deliberately.

## Pipeline parameters for events

Events are single-take live talks — a cadence between voiceover's tight sentence-by-sentence delivery and talking-head's multi-second retake pauses. Preprocess with the default `--silence-gap 0.35` (no override). Assemble with `--transcript` (for interior dead-air tightening) plus:

`assemble_edl.py --merge-gap 0.5 --lead-in 0.12 --tail-pad 0.20 --max-internal-gap 0.8`

- `--merge-gap 0.5` bridges natural speaking breaths so continuous speech stays whole, while still breaking at the longer pauses between thoughts.
- `--lead-in 0.12 / --tail-pad 0.20` give a live speaker's cuts a bit more room to breathe than voiceover's tight `0.08 / 0.15`, so trims don't feel clipped.
- `--max-internal-gap 0.8` matches this guide's "trim inter-sentence pauses longer than ~0.8 s" rule — interior pauses above that get closed, shorter ones stay for natural rhythm.

These are starting points. Raise `--max-internal-gap` toward `1.0` if the cut feels breathless; lower it toward `0.6` for a tighter edit.

## What to cut

### Structural overhead

#### Pre-talk (usually the first few minutes)

- Waiting for attendees ("while we wait", "give people a few minutes", "more people will join", "trickle in")
- Icebreakers unrelated to the talk ("drop in the chat where you're coming from")
- Tech checks ("can you hear me", "test test", "can you see my screen", "note taker", "will share the recording")
- Host intros and thank-yous ("welcome everyone", "thanks for joining", "calling in from...")
- Biographical tangents in the speaker's own self-intro — prior jobs, past projects, career anecdotes that don't establish authority for *this* talk. Credentials and current role belong; generic career narrative is filler.
  - **Does not apply to the host introducing the speaker.** A host saying "X was a principal engineer at Google and Microsoft, now teaches Y on Maven" is framing for the audience, not a self-intro tangent — keep it. Likewise, the speaker's own one-line credential statement ("I'm a software engineer, not an analyst, but I do data work") is positioning that sets up the thesis, not filler. Cut *extended* career narrative, not the establishing lines.

Structural cuts like these usually only apply in the first five minutes or so. Past that window, a line like "can you hear me" is probably a mid-talk tech issue worth keeping in context.

#### Q&A and chat-check preambles

Cut the meta-commentary *around* questions, not necessarily the questions themselves:

- "Let me go through the chat", "peek at the chat", "look at questions"
- "Raise your hand", "come off mute"
- "Feel free to drop questions", "drop it in the chat"
- "Any questions?", "good question", "great question" — when they're filler rather than answering a specific question

When the speaker actually engages with a question, protect the substantive answer.

When a mid-talk answer is being kept, the question read-out is part of the answer, not part of the meta. Trim the housekeeping around it ("I see we've got some questions in the chat", "great question", "I think David had a good answer") but keep the sentence where the speaker reads or restates the question — an answer whose question was trimmed lands as an orphaned non-sequitur, and restoring it later costs a parent-session lookup-and-revalidate pass.

#### Logistics tail — **end-of-talk only**

This rule applies **after the last substantive content**, not anywhere a plug-like phrase appears:

- Recording and follow-up ("share the recording", "send you the recording", "I'll email")
- Goodbyes ("that's all I've got", "thanks everyone", "see you next time")
- End-of-talk plugs and LinkedIn calls ("drop me a note on LinkedIn", "sign up at the link", "link in the chat")

When the brief drops the whole Q&A, the talk loses its recorded ending — the goodbye usually sits after the Q&A, inside this logistics tail. Check the tail for a short clean sign-off line ("thanks for joining… take care") and offer it as a splice-on outro directly after the last content block; ending cold on the final takeaway is the alternative. Surface this choice in the Step 0.5 brief rather than deciding silently.

#### **Mid-talk product pitch — KEEP**

A product/course pitch delivered as a planned section mid-talk (typical placement: right before Q&A) is **event content, not overhead**. Viewers of a live-talk recording expect the offer pitch as part of the event. Keep the full pitch — pricing, guarantees, promo codes, bonuses — even though the phrases overlap with the "plugs" list above. The "plugs" rule applies to the *tail*, not mid-talk.

Trim only the meta-asides inside a mid-talk pitch:
- Hard-expiry timers directed only at the live audience ("this offer expires in 72 hours")
- "For people watching the recording..." parentheticals
- Redundant value restatements where the same dollar figure is repeated

### Pacing cuts

These are the small, pervasive cuts that distinguish a tight edit from a slack one. Every chunk, including middle chunks, needs a pacing pass.

#### Restatement / in-the-moment retake

If the speaker says essentially the same sentence twice in a row (e.g., *"AI app needs needs. So for mcp, the AI app needs MC client..."* after already defining it cleanly), cut the weaker pass — usually the second, unless it adds a new noun, number, or example. A live speaker restating within ~15s is self-correcting, not elaborating. This is the single largest pacing bucket — do not skip it.

In Q&A, the same pattern stretches out to 20–30s. A hedged or rambling first answer ("I'm not sure. So…") is often followed, once the speaker has organized their thought, by a cleaner restatement that covers the same ground. Treat these the same way: the later pass renders the earlier one redundant, so cut the weaker take even when both are substantive and on-topic. Protecting a Q&A answer means keeping the *content* of the answer, not every attempt at delivering it — last-take-wins applies inside Q&A just as it does in the talk body.

A single continuous Q&A answer can also sprawl without retaking — the speaker stays on one point but re-illustrates it through parallel comparisons ("with A…, with B…, also with A…"), analogy chains, or stacked personal-experience anecdotes. The first illustration carries the substance; the parallel extensions re-deliver rather than advance. An answer that runs past ~60s on a single topic usually contains one such sprawl. The substantive pass — the actual information or opinion that answers the question — typically fits in 15–30s. Parallel reframes, "another way to think about it" passes, and personal-reflection codas ("that was scary at first… turned out to be a good thing… made me more X") don't add information. Keep the substantive pass; cut the reframes and codas that follow.

#### Slide-hunting / lost-thread

When the speaker pauses to navigate slides or search the screen and verbally narrates the search, cut the search out:

- "Let me go back. Here. Uh,"
- "Uh, let's see. Okay. Adoption."
- "I think I have it pulled up here actually. Uh, let's see."
- "Here we have, here we have..." (screen-switch dead air)

Cut from the last substantive word of the prior sentence to the first substantive word of the restart.

During an active demo — screenshare, code walkthrough, live tool use — on-topic narration *is* the content, even when phrasing sounds navigational ("let's see…", "uv run main py", "and now this tells the model…"). The distinction is operational: slide-hunting is the speaker recovering a lost thread; demo narration is the speaker driving the demo forward. Keep the running commentary; cut only genuine dead air or a search-for-slide.

#### Hedged non-answers in Q&A

If the speaker's first clause is an explicit hedge, cut the hedge and any silence attached to it:

- "Uh, that's a good question. I'm not sure. [silence] So..."
- "I don't know. [silence] But maybe..."

Keep from the first substantive clause. **If the entire answer is a hedge with no substance, cut the whole answer.** The "protect rambling answers" principle only applies when substance follows the hedge.

#### Inter-sentence pauses and filler clusters

- Trim inter-sentence pauses longer than ~0.8s down to a tight gap.
- Cut clusters of filler words: repeated "uh", "um", "you know", doubled words ("needs needs", "I woke up with, I woke up with"), false starts that restart mid-word.

Aim for sub-second gaps between kept segments during continuous speech.

#### Speaker-state asides

Cut asides about the speaker's physical state or apologies for interruptions, even mid-talk:

- "Excuse me, I woke up with a sore throat..."
- "Sorry, my voice is going..."
- Any 2+ second aside that doesn't advance the topic

"Personality" in this guide means on-topic conversational seams — not health disclaimers or apologies.

## What to protect

- Substantive continuous speech on the talk's subject — the actual explanation.
- The answer to a question (after any hedge is trimmed), even if the question was rambling.
- Specific examples, demos, numbers, stories, product-pitch details — the unique content the audience showed up for.
- On-topic conversational seams that give the talk its personality.

## Sub-agent guidance

Each chunk sub-agent should make **two passes**:

1. **Structural pass.** Scan for structural phrases (pre-talk, Q&A preamble, end-of-talk logistics). Large, high-confidence cuts.
2. **Pacing pass.** Within each kept region, scan for restatements, slide-hunting, hedged non-answers, long inter-sentence pauses, and filler clusters. These are smaller but collectively the bigger source of over-keeping.

Before returning, compute retention for your chunk. If it's above ~75% and the chunk isn't pure demo, go back and look harder for pacing cuts — you are almost certainly returning a slack edit.

Flag rather than cut only when genuinely ambiguous. "When in doubt, keep" is the wrong default — the more common failure mode is leaving pacing untouched, not over-cutting.

## Q&A pair review gate (interactive; runs before assembly)

The chunk pass protects each answer's *substance*, but it cannot decide *which whole questions belong in the published recording* — that call depends on the audience and the video's purpose, not on take quality. Some pairs are near-always noise on replay (a viewer asking "will you share the recording?", an off-topic personal ask, a re-ask of something already covered), and the editor wants to prune them as whole units before importing to Final Cut. So for any event with a Q&A portion, the pipeline pauses after the dedup pass and before Step 6 assembly to enumerate the pairs and let the user prune them. Skip only when the event has no Q&A or the user waives it.

1. **Extract the pairs.** Spawn a Sonnet sub-agent over the *kept* Q&A segments (the Q&A chunks' entries in `all_segments_validated.json`) plus the word-level transcript. It writes `<project_dir>/chunks/qa_pairs.json`: a list of `{"id", "start", "end", "asker", "question_summary", "answer_gist", "suggested_action": "keep"|"drop", "reason"}`. `start`/`end` bound the whole pair — from the question read-out through the end of the answer — on real segment boundaries, so a dropped pair maps straight to a drop range. `asker` is a name only if the transcript or chat names it, else `null`. The agent sets `suggested_action` per the drop candidates below.

2. **Present and wait.** Show the user a skimmable table — `# | time | asker | question | 🟢 keep / 🔴 drop + reason` — and ask which to drop. This is a real pause: do not assemble until they answer. (Include the 🟢/🔴 recommendation column by default; drop it for a neutral list if the user prefers to decide every pair from scratch.)

3. **Apply.** Append the user's chosen pairs' `{start, end, reason}` to `<project_dir>/chunks/dedup_drops.json` (Step 6 removes everything in that file), then assemble. The drop ranges land on segment boundaries, so no re-validation is needed. Assembly and FCPXML are cheap, so if the user changes their mind they can edit `dedup_drops.json` and re-run Step 6 without re-editing chunks.

### Whole-pair drop candidates

Trimming the *meta around* a question (see "Q&A and chat-check preambles" above) is different from dropping a *whole* pair. Some pairs, even with a clean substantive answer, rarely earn their place on replay — flag these as suggested drops (the human still decides):

- **Logistics / housekeeping asks** — "will you share the recording?", "will you send the slides?", "is this recorded?". The answer is identical each time and belongs in a follow-up email, not the video. These recur because different attendees ask live throughout — flag every instance.
- **Off-topic or personal asks** — internship/hiring requests, "how can I contact you?", questions aimed at the speaker personally rather than the topic. Interesting live, dead weight on replay.
- **Re-asks of an already-answered question** — a later attendee asks what the talk or an earlier answer already covered; the repeat adds nothing.
- **Pure preamble/transition pairs** — "let me check the chat… no questions yet", "happy to stick around for another 30 minutes", "any other questions?" with no real question attached.

Everything else — a substantive, on-topic question with a real answer — defaults to keep. The gate exists to prune the housekeeping and off-topic pairs an automatic pass leaves in, not to thin genuine content. Suggest, don't decide.
