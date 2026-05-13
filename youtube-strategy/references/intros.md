# Intros (Ed Lawrence-style hooks)

How to write the opening 10 seconds of a video. The hook is the contract. If it doesn't land in those 10 seconds, the rest of the script doesn't matter.

## The Ed Lawrence pattern

Three lines. ~25 words total. Under 10 seconds when spoken. Each line is a complete idea, increasingly short, exiting on a confident promise. Each line earns the next.

### Three-beat structures

The skeleton is always pain → reframe → promise, but the opening move varies:

**Pain mirror → reframe → promise** (most universal)
> You've been using Claude every day. You can tell you're scratching the surface.
> It's not your prompts. It's not the model. You're missing one thing.
> Here's what it is.

**Proof → curiosity → curation**
> I've delegated 15 hours of my week to Claude.
> Not from better prompts. From one specific thing.
> If you only learn one thing about Claude, learn this.

**Curation frame** (when the avatar is already overwhelmed)
> There's a thousand ways to use Claude.
> But if you're a busy founder, only one of them matters.
> Let me show you what it is.

**Pain stab → reframe → promise** (when the avatar is self-blaming)
> Most people who try Claude get lost in the first week.
> It's not because they're bad at it.
> They're missing one thing — and that's what we're fixing today.

The "not X, not Y, it's Z" rhythm is Ed's signature for line 2. Builds tension, lands the hammer, exits on the verdict. Use beats and pauses on camera to recover the rhythm if a line gets condensed for spoken flow.

## Filter check

Every line of the hook must pass the visualize / falsify / unsignable filter from `conversion-copy`. That's the canonical home for the line-by-line filter. Don't restate it here — just enforce it.

The most common line-1 failure: brand-voice abstractions ("Claude is powerful", "AI is transformative"). Three filter ✗'s. Anthropic's homepage could open with the same line.

The fix: anchor line 1 in something the avatar has *actually done* themselves — used it, paid for it, sat with it.

## Iteration logistics

This matters and isn't intuitive: **iterate the first line alone before iterating on the full hook.**

Why: the first line carries the most weight. It has to anchor in real customer language and pass all three filter questions. Once it's locked, lines 2 and 3 fall into place faster because they're now reacting to a fixed anchor.

Order of operations:
1. Lock the title and angle first
2. Generate 8-10 candidate line-1's, each grounded in a different customer-language source. Annotate with ✓/✗ on each filter question.
3. Recommend top picks with reasoning, let Shaw pick.
4. Once line 1 is locked, generate 2-3 full hook variants — each with a different line-2 move (elimination triple-beat, self-blame reframe, curation play).
5. Shaw picks. Tighten on delivery (where to pause, where to push).

Rough number of variants is the lever. Do 3 variants when the angle is well-defined; do 8-10 when the line is failing and you're hunting for the right anchor.

## Customer-language sourcing (where to pull from)

Hooks fail when the language is invented. They land when it's real. Before drafting line 1 candidates, pull verbatim language from:

1. **ABA Calls** (Notion database) — sales call notes have the actual phrases prospects used. Search for terms like the topic of the video, "scratching the surface", "where to start", "feel behind", "overwhelmed".
2. **Workshop intake form responses** (Google Drive — `1:1 Claude Workshop - Intake (Responses)`) — the most detailed source. Each response includes how clients describe their actual workflows, time on task, and what they want freed up. Read 5-10 entries before drafting.
3. **Testimonial form responses** (Google Drive — `1:1 Claude Workshop - Testimonial Form (Responses)`) — post-engagement language; useful for outcome framing.
4. **Workshop one-pager** (Notion — `1:1 Claude Workshop`) — the offer's own avatar/pain language. Already filter-tested copy.

Pull at minimum 3 verbatim phrases before generating. Quote the source for each candidate so Shaw can audit the grounding.

Real examples (from one session):
- [Lead Name] (sales call): *"Last 4 month it was a good email summary tool, just scratching the surface"*
- [Lead Name] (sales call): *"Spending evenings with AI"* / *"Using it but feel behind. FOMO"*
- [Lead Name] (intake): script he built *"sometimes works sometimes it doesn't"*
- [Client Name] (testimonial): *"stitching outputs together, switching between tools"*

These are the building blocks of line 1.

## What line 1 needs to do

- **Mirror the avatar's actual experience.** Not "you've heard X is powerful" — "you've been using X for months and Y still happens."
- **Anchor in something the avatar has done, paid for, or felt** — past behavior is more defensible than claimed feelings.
- **Avoid brand-voice abstraction.** No "powerful," "transformative," "unleash," "supercharge," "revolutionary."
- **Earn line 2.** End on something that creates a question line 2 answers.

## What line 2 needs to do

- **Sharpen the diagnosis.** Name what's actually missing or what the real fix is.
- **Use Ed's "not X, not Y, it's Z" pattern when possible** — gives delivery a triple-beat punch.
- **Stay short.** Line 2 is usually shorter than line 1.

## What line 3 needs to do

- **Promise the fix without giving it away.** "Here's what it is." / "Let me show you." / "I'll walk you through it."
- **Be the shortest line.** Sets up the cold-open-to-content transition cleanly.

## Time and word target

- **~25 words total** across all three lines
- **Under 10 seconds spoken**
- **Line 1 is the longest, line 3 is the shortest** (the rhythm narrows)

## Output format

```
**Topic:** <one-sentence restatement>
**Avatar:** <pulled from current Q strategy page>
**Customer language sources used:** <which calls, intake responses, etc.>

**Line 1 candidates** (10 options, mixed angles):

1. <Line>
   - Source: <verbatim quote or composite>
   - Filter: ✓ visualize ✓ falsify ✓ unsignable
2. ...

**Top picks for line 1:** <2-3 + reasoning>

[Once line 1 is locked, then:]

**Full hook variants** (3 options, different line-2 moves):

A — <line-2 move name>
> <Line 1>
> <Line 2>
> <Line 3>

B — ...

**Top pick:** <1 + reasoning>
```

## Common failure modes

- **Drafting line 1 from imagination.** It always sounds like a brand wrote it. Pull from the call notes first.
- **Trying to perfect the full hook before line 1 is anchored.** Lines 2 and 3 will keep shifting with the angle. Lock line 1 first.
- **Stacking too many filter questions in line 2.** "Not your prompts, not the model, not the temperature, not the system prompt..." reads as overwritten. Two beats, then the verdict.
- **Ending line 3 with a question that has no payoff.** Line 3 is the contract — it promises the fix.
