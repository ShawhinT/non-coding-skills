# Animation Techniques

Patterns for the common animation types that show up in talking-head scripts. Each pattern is a starting point — adjust durations and easing to taste.

## 1. Morph (icon A → icon B)

Two layers, stacked. A is visible at start; B fades up and replaces it.

```css
.state-a { animation: stateOut 3.6s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
.state-b { animation: stateIn  3.6s cubic-bezier(0.4, 0, 0.2, 1) infinite; opacity: 0; }

@keyframes stateOut {
  0%, 22%   { opacity: 1; transform: scale(1); }
  33%, 94%  { opacity: 0; transform: scale(0.85); }
  100%      { opacity: 1; transform: scale(1); }
}
@keyframes stateIn {
  0%, 22%   { opacity: 0; transform: scale(0.85) translateY(8px); }
  36%, 94%  { opacity: 1; transform: scale(1) translateY(0); }
  100%      { opacity: 0; transform: scale(0.85) translateY(8px); }
}
```

**When to use:** any "X becomes Y" callout in a script ("the tool becomes the employee", "manual becomes automated", etc.).

## 2. Build-in (staggered fade-up)

Multiple elements appear in sequence — boxes in a flow chart, labels in a list, points being made.

```css
.item { opacity: 0; animation: fadeUp 3.6s ease-out infinite; }
.item:nth-child(1) { animation-delay: 0.0s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.4s; }
.item:nth-child(4) { animation-delay: 0.6s; }

@keyframes fadeUp {
  0%, 5%   { opacity: 0; transform: translateY(8px); }
  20%, 94% { opacity: 1; transform: translateY(0); }
  100%     { opacity: 0; transform: translateY(8px); }
}
```

Stagger between 100–250ms. Faster reads as "all at once," slower reads as "narration sync."

**Holding the final state matters.** The reader needs ~2 seconds to absorb a 4-element flow. The keyframe above holds from 20% to 94% — that's ~2.6 seconds at a 3.6s total. Don't cut the hold short.

**When to use:** "4-step process" boxes, "three things to remember" bullets, label stacks (✓ Knows / ✗ Doesn't know columns).

## 3. Draw-on (curve, line, underline)

Use SVG `stroke-dasharray` + `stroke-dashoffset` to animate a path being drawn.

```html
<svg viewBox="0 0 400 200" width="400" height="200">
  <path d="M 20 150 Q 100 50 200 80 T 380 60"
        fill="none"
        stroke="currentColor"
        stroke-width="3"
        stroke-linecap="round"
        pathLength="100"
        class="draw" />
</svg>
```

```css
.draw {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw 3.6s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
@keyframes draw {
  0%, 10%  { stroke-dashoffset: 100; }
  50%, 94% { stroke-dashoffset: 0; }
  100%     { stroke-dashoffset: 100; }
}
```

Using `pathLength="100"` lets you treat the path as 0–100 regardless of its actual length — much easier than computing the real length.

**When to use:** drawing a curve in an "effort/output over time" chart, animating an arrow between two boxes, underlining a phrase as the VO emphasizes it.

## 4. Side-by-side comparison

Two columns appear simultaneously (or stagger one before the other). Keep them visually distinct — usually a ✓ column and an ✗ column.

```html
<div class="cols">
  <div class="col yes">
    <div class="col-header">✓ Knows</div>
    <ul>
      <li class="item">The world</li>
      <li class="item">Experience</li>
      <li class="item">Skills</li>
    </ul>
  </div>
  <div class="col no">
    <div class="col-header">✗ Doesn't know</div>
    <ul>
      <li class="item">Your business</li>
      <li class="item">Your industry</li>
      <li class="item">Your way</li>
    </ul>
  </div>
</div>
```

Animate the column headers in first, then stagger the list items. Use color to differentiate (green/lime for ✓, coral/red for ✗) — but only on the icon and header, not the body text, or it reads as alarming.

## 5. Effort/output curve

A specific case of draw-on: a line that drops below baseline then rises above. Show a horizontal baseline first, then draw the curve over it.

```html
<svg viewBox="0 0 600 240">
  <!-- Baseline (drawn instantly or fades in early) -->
  <line x1="0" y1="120" x2="600" y2="120"
        stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="4 4" />

  <!-- Curve: small bump up (onboarding cost), drop below (payoff), rise -->
  <path d="M 0 120 Q 80 80 160 100 T 320 200 Q 460 200 600 60"
        fill="none" stroke="var(--primary)" stroke-width="4"
        stroke-linecap="round" pathLength="100" class="draw-slow" />
</svg>
```

Slow the draw so the eye can track it — ~1.5s of actual drawing inside a 3.6s clip.

## 6. Counting up / metric reveal

A number that animates from 0 → final value. Most reliable approach: build the digit changes manually as keyframes rather than using JS counters (the render pipeline pauses JS via animation pause, so CSS is more predictable).

For a single number flip:

```css
.metric {
  font-variant-numeric: tabular-nums;
  animation: metricGrow 3.6s ease-out infinite;
}
@keyframes metricGrow {
  0%      { content: "0"; }
  20%     { content: "23"; }
  40%     { content: "67"; }
  60%, 94%{ content: "100"; }
  100%    { content: "0"; }
}
```

Or, for a clean reveal without the count-up, just fade the final number in. That's almost always better — count-ups feel cheesy outside specific contexts.

## Common mistakes to avoid

- **Holding too briefly.** B-roll is meant to be paused on. Your destination state should hold for at least 1.5–2 seconds.
- **Animating too many things at once.** If three elements move simultaneously, the eye picks one and misses the others. Stagger by 100–200ms.
- **Big rotation/scale moves.** A 90° rotate or a 1.5× scale punches above the talking head and pulls focus. Stay subtle.
- **Loops that snap.** If the clip will loop in the editor, make the end state visually identical to the start state (or fade out completely at 100%). The starter template handles this with the `94%–100%` reset.
- **Forgetting to test the render.** Sometimes a CSS animation behaves differently when seeked deterministically vs played in real time. Always render and watch the MP4 before declaring done.

## Per-element vs whole-scene animations

Two valid patterns:

1. **One animation per element** (the starter template). Each element has its own keyframe driving its in/out. Composable, predictable.
2. **One scene-wide timeline.** Use a single keyframe `@keyframes scene` on a parent, with `transform` and `opacity` affecting children via descendant selectors and CSS variables. More compact but harder to debug.

Default to pattern 1 unless the scene has many elements with tightly choreographed timing.
