# "Coming up" pre-roll

A ~30 s teaser of lines from later in the video, prepended to the edit with a "Coming up" title. Its job is the first 30 seconds of retention: make the viewer care about the people, then leave a question open that only the full video answers. It is a story, not a highlight reel.

Build it after the editorial brief is approved (Step 0.5), so you know what survives the main cut. Use the AssemblyAI word transcript for all line-finding and timing; use speaker labels (e.g. a Zoom VTT) only to know who is talking.

## Research process

Shaw makes the editorial calls; Claude's job is to give him a strong pool to choose from and assemble fast. Expect several rounds. Each round narrows.

1. **Mine by register, in parallel.** Spawn one sub-agent per register, each prompted differently: *funny*, *insightful*, *pain / struggle / negative emotion*, and (for guest videos) *traction / credibility*. One generalist pass returns safe, flat lines; register-specific prompts find the lines with energy. Each agent returns 8–15 candidates with exact words, speaker, and AssemblyAI in/out. If Shaw calls a pool weak, re-mine that register with a sharper prompt rather than padding the list.
2. **Topic sweeps on request.** When a beat needs material ("every snippet where [Guest] talks about the app's success"), run a sweep for that one topic and return every hit, not a curated few. Shaw builds micro-arcs from the raw list.
3. **Write candidates as a skimmable table plus JSON.** One row per line: number, register, speaker, exact words, duration. JSON underneath with in/out times for Claude. No prose paragraphs per clip.
4. **Propose arcs, not just lists.** Offer two or three sequences with different shapes (e.g. before/after, underdog) and a one-line rationale each. Shaw picks an arc, then dictates the order beat by beat ("open on X, then Y, then give me options for what comes next").
5. **Use exactly what he names.** When he picks specific lines, add only those. Don't add other lines from the same register to be thorough.
6. **Preview renders stay short.** Review MP4s run 30–45 s. Multiple versions mean multiple short files, not one long reel.
7. **Subtract to test.** When a version feels off, try it with the weakest beat removed before adding anything. Removing two good jokes made the [Guest] pre-roll work.

## Editorial judgment: telling a story in 30 seconds

The [Guest] pre-roll, as shipped:

| Beat | Line | Job |
|---|---|---|
| Stakes, left open | "Last time it burned about 300,000 tokens. We'll see what it does this time." | Opens a loop the video closes |
| Who this is | "First month it had 20 users. Last month I had 1,800 recurring users and I had 700 new users." | Credibility as a mini before/after |
| The question | "So what did you do that made it so popular?" | Says the viewer's question aloud |
| The humble answer | "I think I just made something that people wanted to use." | Answers without bragging |
| The struggle | "I just spent a weekend going back and forth with Claude, and then that weekend turned into 2 weeks." | Honesty; the viewer recognises it |
| The permission | "It's not because I'm very good at coding… I'm just more willing to interface with these kind of technologies." | "You could do this too" |
| The thesis | "As long as it's physically possible for a computer to display the information you want, you can get there eventually." | Ends on a line that lands |

Principles behind it:

- **Open a loop and don't close it.** Lead with the stakes and withhold the result. The 200K-token payoff was cut from the pre-roll on purpose; the viewer stays to find it out.
- **Credibility through numbers, said by the guest.** A specific progression (20 → 1,800) beats any adjective. Let the guest say it; the host frames, the guest proves.
- **Pair a question with its answer.** A spoken question gives the sequence a conversational rhythm, and the viewer hears their own question asked.
- **Arc from proof to permission.** Success, then the struggle behind it, then why the viewer can do it too. The underdog shape makes the guest relatable rather than impressive.
- **End on a thesis line,** a sentence that works as a standalone quote. Not a joke, not a question.
- **Every line must make sense with no context.** Drop lines that depend on what's on screen or on an earlier setup ("it's never played this card game before", "locally, not globally"), however good they are in place.
- **Jokes are optional.** A funny line only stays if it moves the arc. Out-of-context jokes (highballs in Japan, White Monsters) stall it; cut them first.
- **Fast.** About 11 cuts in 30 s, 1–6 s each. Split a slow speaker's sentence into fragments and jump-cut between them ("last time" / "it burned about 300,000 tokens"). Keep information, drop connective words.

## Cut points

AssemblyAI word times locate a line; they are not acoustic boundaries. When words run together, AssemblyAI stretches one word's end to meet the next word's start. That hides real pauses and makes outs run long.

- Snap each in/out to the quietest 10 ms frame by RMS, searching a little past the neighbouring transcript words.
- Split out any pause over ~0.2 s inside a clip, found by RMS, not by transcript gaps.
- When a clip's first word is fused to the word before it, either drop it ("So we'll see" → "We'll see") or back up to include the whole lead-in phrase ("like, oh, what did you do"). Never start mid-word. Note which in the cut list.
- Quantize to the timeline frame rate.
- Verify by re-transcribing the preview render with AssemblyAI and checking for stray or clipped words at each seam.

## Deliverable

Editable, not printed. Prepend the pre-roll cuts to the main EDL as their own segments; `generate_fcpxml.py` keeps segment order, so they become separate spine clips from the source media. Render the title as a ProRes 4444 alpha MOV and place it with Step 8 at start 0, with its duration equal to the pre-roll's total length. The preview MP4 is only for review.

Title look: "Coming up" lower left in the channel font (Manrope Bold, white, accent underline), fading in at ~0.3 s. No show name.
