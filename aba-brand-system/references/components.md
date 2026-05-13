# ABA Components — Annotated HTML

Drop-in component snippets. Each one uses raw HTML + inline styles or CSS variables from `colors_and_type.css`. No framework required. The page assumes a `body` with `background: #010413` (or `--aba-base-100`) and `color: white`.

To use these in a page, include the CSS variables file first:

```html
<link rel="stylesheet" href="colors_and_type.css">
<!-- or paste the :root { ... } block inline -->
```

---

## Buttons

All buttons are **full pills** (`border-radius: 32px`), Manrope 700, no shadow, color-only hover.

```html
<!-- Primary CTA (the canonical button on the site) -->
<button style="background:#087CA7;color:white;border:none;border-radius:32px;
               padding:14px 28px;font-family:'Manrope';font-weight:700;
               font-size:15px;cursor:pointer">
  Book intro call →
</button>

<!-- Outline (secondary forms, e.g. contact "Send") -->
<button style="background:transparent;color:white;border:1px solid rgba(255,255,255,0.3);
               border-radius:32px;padding:14px 28px;font-family:'Manrope';
               font-weight:700;font-size:15px;cursor:pointer">
  Send
</button>

<!-- Neutral (OAuth, "Continue with Google") -->
<button style="background:oklch(27% 0.041 260.031);color:white;
               border:1px solid oklch(27% 0.041 260.031);border-radius:32px;
               padding:10px 18px;font-family:'Manrope';font-weight:600;
               font-size:13px;cursor:pointer">
  Continue with Google
</button>
```

**Sizes:** `btn-lg` → `padding:14px 28px; font-size:15px`. Default → `padding:10px 20px; font-size:14px`. Don't go smaller than this on CTAs.

**Hover:** primary lightens ~12% (`color-mix(in srgb, #087CA7 88%, white)`). Outline shows a subtle `bg:rgba(255,255,255,0.05)`. No transform, no shadow.

---

## Header / Nav

```html
<nav style="display:flex;align-items:center;justify-content:space-between;
            padding:14px 24px;background:#010413;max-width:80rem;margin:0 auto">
  <!-- Logo -->
  <a style="display:flex;align-items:center;gap:10px;text-decoration:none">
    <img src="assets/logo-square-dark-192.png"
         style="width:36px;height:36px;border-radius:6px">
    <span style="font-family:'Manrope';font-weight:700;font-size:14px;color:white">
      AI Builder Academy
    </span>
  </a>

  <!-- Center nav links -->
  <div style="display:flex;gap:24px;align-items:center">
    <a style="font-family:'Libre Franklin';font-size:14px;font-weight:500;
              color:rgba(255,255,255,0.9);text-decoration:none">Events</a>
    <a style="font-family:'Libre Franklin';font-size:14px;font-weight:500;
              color:rgba(255,255,255,0.9);text-decoration:none">Courses</a>
    <a style="font-family:'Libre Franklin';font-size:14px;font-weight:500;
              color:rgba(255,255,255,0.9);text-decoration:none">Services</a>
  </div>

  <!-- Right CTA -->
  <button style="background:#087CA7;color:white;border:none;border-radius:32px;
                 padding:10px 18px;font-family:'Manrope';font-weight:700;
                 font-size:13px;cursor:pointer">
    Get in touch
  </button>
</nav>
```

The wide-wordmark variant uses `<img src="logo-wide-dark.png" style="height:54px">` in place of the square mark + text.

---

## Hero

```html
<section style="padding:80px 24px 64px;max-width:80rem;margin:0 auto;
                position:relative;text-align:center">
  <!-- Radial glow behind -->
  <div style="position:absolute;inset:0;
              background:radial-gradient(ellipse 60% 50% at 50% 40%,
                                          rgba(8,124,167,0.12) 0%,
                                          transparent 70%);
              pointer-events:none"></div>

  <!-- Eyebrow -->
  <div style="position:relative;font-family:'Manrope';color:#087CA7;
              font-size:13px;font-weight:600;letter-spacing:0.2em;
              text-transform:uppercase;margin-bottom:20px">
    Transform your business
  </div>

  <!-- H1 with highlighted phrase -->
  <h1 style="position:relative;font-family:'Manrope';font-weight:800;
             font-size:clamp(40px,5vw + 16px,60px);letter-spacing:-0.02em;
             line-height:1.1;margin:0 0 20px;color:white">
    AI Lets Small Teams Do
    <span style="position:relative;display:inline-block;padding:0 0.06em">
      <span style="position:absolute;inset:auto 0 0.03em 0;height:0.25em;
                   background:rgba(8,124,167,0.9);z-index:-1"></span>
      Big Things.
    </span>
  </h1>

  <!-- Subhead -->
  <p style="position:relative;font-size:18px;color:rgba(255,255,255,0.6);
            max-width:42rem;margin:0 auto 32px;line-height:1.6">
    Stop researching AI tools. Start handing off work to them.
  </p>

  <!-- Primary CTA -->
  <button style="position:relative;background:#087CA7;color:white;border:none;
                 border-radius:32px;padding:16px 32px;font-family:'Manrope';
                 font-weight:700;font-size:15px;cursor:pointer">
    Book intro call →
  </button>
</section>
```

---

## Pain card

```html
<!-- Default state -->
<div style="background:rgba(238,99,82,0.07);border:1px solid rgba(238,99,82,0.2);
            border-radius:16px;padding:24px;transition:all 200ms">
  <h3 style="font-family:'Manrope';font-weight:700;font-size:18px;
             color:#EE6352;margin:0 0 8px">
    You've been burned before.
  </h3>
  <p style="margin:0;font-size:14px;color:rgba(255,255,255,0.5);line-height:1.55">
    Spent $50K and three months on AI consulting that generated little ROI.
  </p>
</div>

<!-- Hover state: bg-error/14, border-error/40 -->
<!-- background:rgba(238,99,82,0.14);border-color:rgba(238,99,82,0.4); -->
```

**Grid pattern.** Pain cards use a 1/4/6 grid progression on mobile/`md:`/`lg:` to center an odd 5th card. Example:

```html
<div style="display:grid;grid-template-columns:1fr;gap:16px">
  <!-- on md+: grid-template-columns: repeat(4, 1fr) -->
  <!-- on lg+: grid-template-columns: repeat(6, 1fr) with cards spanning 2 cols -->
  ... pain cards ...
</div>
```

---

## Service / Training card

The "ladder" cards (1:1 Workshop / Team Workshop / Done-For-You). Includes a 16:9 gradient thumbnail with a single white outline icon centered.

```html
<div style="background:oklch(20% 0.042 265.755);
            border:1px solid oklch(27% 0.041 260.031);
            border-radius:16px;overflow:hidden;width:320px;
            transition:all 200ms">
  <!-- Gradient thumbnail with single icon -->
  <div style="aspect-ratio:16/9;
              background:linear-gradient(135deg,#087CA7 0%,rgba(8,124,167,0.4) 100%);
              display:flex;align-items:center;justify-content:center">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
         stroke="white" stroke-width="1.5" stroke-linecap="round"
         stroke-linejoin="round" opacity="0.9">
      <!-- icon path from icons.md -->
      <path d="..."/>
    </svg>
  </div>

  <!-- Body -->
  <div style="padding:24px;display:flex;flex-direction:column;gap:12px">
    <!-- Duration badge (Mono) -->
    <span style="background:#087CA7;color:white;padding:4px 12px;
                 border-radius:32px;font-family:'JetBrains Mono';
                 font-size:11px;align-self:flex-start">
      90 min
    </span>

    <h3 style="font-family:'Manrope';font-weight:800;font-size:18px;margin:0;color:white">
      1:1 Workshops
    </h3>

    <p style="margin:0;font-size:14px;color:rgba(255,255,255,0.5);line-height:1.55">
      Live session on your highest-leverage workflow. Walk out with one AI skill
      running on your real work.
    </p>

    <div style="font-size:14px;font-weight:600;color:rgba(255,255,255,0.8);margin-top:4px">
      Starting at $1,500
    </div>

    <!-- Lime mono CTA link -->
    <a style="font-family:'JetBrains Mono';color:#8FC93A;font-size:12px;
              margin-top:6px;text-decoration:none">
      Book intro call →
    </a>
  </div>
</div>
```

**Gradient variants for the thumbnail tile:**

- Workshop (primary) → `linear-gradient(135deg, #087CA7 0%, rgba(8,124,167,0.4) 100%)`
- Team (mixed) → `linear-gradient(135deg, #087CA7 0%, #519872 100%)`
- DFY (warm) → `linear-gradient(135deg, #D19C1D 0%, #519872 100%)`

These are **the only multi-color gradients in the system**, and only inside thumbnail tiles.

---

## Testimonial card

```html
<div style="background:rgba(0,15,40,0.5);border:1px solid rgba(255,255,255,0.08);
            border-radius:16px;padding:32px">
  <!-- Decorative serif curly-quote, primary-blue, oversize -->
  <div style="font-family:Georgia,serif;font-size:64px;color:rgba(8,124,167,0.8);
              line-height:0.8;margin-bottom:-8px">&ldquo;</div>

  <p style="margin:0 0 20px;font-size:15px;line-height:1.6;
            color:rgba(255,255,255,0.7)">
    In one session, we automated a task that was taking me 20 hours.
    Shaw doesn't just show tools — he helps you build systems I can extend
    across the business.
  </p>

  <!-- Attribution with primary-blue dash + name + role -->
  <div style="display:flex;align-items:flex-start">
    <div style="width:32px;height:1px;background:rgba(8,124,167,0.4);
                margin:10px 12px 0 0"></div>
    <div>
      <div style="font-family:'Manrope';font-weight:600;font-size:14px;color:white">
        [Client Name]
      </div>
      <div style="font-size:13px;color:rgba(255,255,255,0.4)">
        Founder, [Company]
      </div>
    </div>
  </div>
</div>
```

---

## Badges (chips)

Pill-shaped, **JetBrains Mono 11px**. The mono font is what tells you it's a data badge, not prose.

```html
<!-- Duration / default → primary blue -->
<span style="background:#087CA7;color:white;padding:4px 10px;border-radius:32px;
             font-family:'JetBrains Mono';font-size:11px;font-weight:500">
  90 min
</span>

<!-- Free → lime + black text -->
<span style="background:#8FC93A;color:black;padding:4px 10px;border-radius:32px;
             font-family:'JetBrains Mono';font-size:11px;font-weight:500">
  Free
</span>

<!-- Paid price → goldenrod -->
<span style="background:#D19C1D;color:white;padding:4px 10px;border-radius:32px;
             font-family:'JetBrains Mono';font-size:11px;font-weight:500">
  $275
</span>

<!-- "Coming Soon" / "Half Day" → primary blue (same as duration) -->
```

### Live-event dot row

```html
<div style="display:flex;align-items:center;gap:6px">
  <span style="width:10px;height:10px;background:#8FC93A;border-radius:50%"></span>
  <span style="font-family:'JetBrains Mono';font-size:11px;color:#8FC93A;
               letter-spacing:0.02em">
    LIVE TUE, MAY 5
  </span>
</div>
```

---

## Inputs

```html
<!-- Standard text field — underline / soft style -->
<div>
  <label style="display:block;font-size:13px;color:rgba(255,255,255,0.6);
                margin-bottom:4px">
    Email <span style="color:rgba(255,255,255,0.3)">(required)</span>
  </label>
  <input type="email" placeholder="[email]"
         style="width:100%;background:transparent;
                border:1px solid rgba(255,255,255,0.2);border-radius:8px;
                color:white;padding:10px 14px;font-family:'Libre Franklin';
                font-size:14px;outline:none">
</div>

<!-- Focused state → border:1px solid #087CA7 -->

<!-- OTP box -->
<input maxlength="1"
       style="width:48px;height:56px;
              background:oklch(20% 0.042 265.755);
              border:1px solid oklch(27% 0.041 260.031);border-radius:8px;
              text-align:center;color:#087CA7;font-family:'JetBrains Mono';
              font-size:22px;outline:none">
```

---

## FAQ accordion

```html
<!-- Closed -->
<div style="border:1px solid rgba(255,255,255,0.08);border-radius:12px;
            padding:16px 20px;display:flex;justify-content:space-between;
            align-items:center;cursor:pointer">
  <div style="font-family:'Manrope';font-weight:600;font-size:15px;color:white">
    Do I need to be technical?
  </div>
  <div style="color:rgba(255,255,255,0.4);font-size:20px">+</div>
</div>

<!-- Open -->
<div style="border:1px solid rgba(255,255,255,0.08);border-radius:12px;
            padding:16px 20px">
  <div style="display:flex;justify-content:space-between;align-items:center;
              cursor:pointer">
    <div style="font-family:'Manrope';font-weight:600;font-size:15px;color:white">
      What's the time commitment?
    </div>
    <div style="color:rgba(255,255,255,0.4);font-size:20px">×</div>
  </div>
  <p style="margin:10px 0 0;font-size:14px;color:rgba(255,255,255,0.5);
            line-height:1.55">
    The 1:1 Workshop is one 90-minute session plus a 30-minute check-in
    seven days later. You walk out with a working AI skill on day one.
  </p>
</div>
```

---

## Footer

```html
<footer style="border-top:1px solid rgba(255,255,255,0.1);margin-top:64px">
  <div style="padding:40px 24px;max-width:80rem;margin:0 auto">
    <div style="display:grid;grid-template-columns:1fr;gap:40px">
      <!-- on md+: grid-template-columns: 1fr 1fr 1fr -->

      <!-- Col 1: Logo + signature + socials -->
      <div>
        <a style="display:flex;align-items:center;gap:12px;text-decoration:none">
          <img src="assets/logo-square-dark-192.png"
               style="width:40px;height:40px;border-radius:8px">
          <span style="font-family:'Manrope';font-weight:600;font-size:18px;color:white">
            AI Builder Academy
          </span>
        </a>
        <p style="font-family:'JetBrains Mono';font-size:12px;
                  color:rgba(255,255,255,0.4);margin:16px 0 0">
          Built with 🥖 by
          <span style="text-decoration:underline;color:rgba(255,255,255,0.5)">
            Shaw Talebi
          </span>
        </p>
        <div style="display:flex;gap:16px;margin-top:16px;color:rgba(255,255,255,0.4)">
          <!-- Social icons go here (see icons.md) -->
        </div>
      </div>

      <!-- Col 2: Two link stacks (uppercase tracked) -->
      <div style="display:flex;gap:40px">
        <div style="display:flex;flex-direction:column;gap:8px">
          <a style="font-family:'Libre Franklin';font-size:12px;font-weight:500;
                    text-transform:uppercase;letter-spacing:0.04em;
                    color:rgba(255,255,255,0.5);text-decoration:none">Events</a>
          <!-- ... Courses, Services, Contact ... -->
        </div>
        <div style="display:flex;flex-direction:column;gap:8px">
          <a style="font-family:'Libre Franklin';font-size:12px;font-weight:500;
                    text-transform:uppercase;letter-spacing:0.04em;
                    color:rgba(255,255,255,0.5);text-decoration:none">Privacy</a>
          <!-- ... Terms, Support ... -->
        </div>
      </div>

      <!-- Col 3: Newsletter -->
      <div style="display:flex;flex-direction:column;gap:12px">
        <span style="font-family:'Manrope';font-size:14px;font-weight:700;
                     text-transform:uppercase;letter-spacing:0.04em;color:white">
          Stay in the loop
        </span>
        <div style="display:flex;gap:8px">
          <input placeholder="Your email"
                 style="padding:8px 12px;font-size:14px;border-radius:6px;
                        outline:none;flex:1;
                        background:oklch(20% 0.042 265.755);
                        border:1px solid oklch(27% 0.041 260.031);
                        color:white;max-width:12rem">
          <button style="padding:8px 14px;font-size:12px;font-weight:700;
                         color:white;border-radius:32px;background:#087CA7;
                         border:none;cursor:pointer">
            Subscribe
          </button>
        </div>
        <p style="font-family:'JetBrains Mono';font-size:11px;
                  color:rgba(255,255,255,0.3);margin:0">
          Free. No spam. Unsubscribe anytime.
        </p>
      </div>
    </div>

    <!-- Copyright row -->
    <p style="text-align:center;font-size:12px;margin:40px 0 0;
              padding-top:24px;border-top:1px solid rgba(255,255,255,0.05);
              color:rgba(255,255,255,0.3)">
      © 2026 AI Builder Academy. All rights reserved.
    </p>
  </div>
</footer>
```

---

## Logo marquee (social proof)

Logos inverted to white at 40% opacity, scrolling horizontally on a 90s loop, with left/right linear-fade masks.

```html
<style>
  @keyframes marquee {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
  }
  .marquee {
    overflow: hidden;
    mask-image: linear-gradient(to right,
                                transparent 0%,
                                black 10%,
                                black 90%,
                                transparent 100%);
  }
  .marquee-track {
    display: flex;
    gap: 64px;
    width: max-content;
    animation: marquee 90s linear infinite;
  }
  .marquee img {
    height: 28px;
    filter: brightness(0) invert(1);
    opacity: 0.4;
    transition: opacity 200ms;
  }
  .marquee img:hover { opacity: 0.8; }
</style>

<div class="marquee">
  <div class="marquee-track">
    <img src="logo-google.svg" alt="Google">
    <img src="logo-microsoft.svg" alt="Microsoft">
    <!-- ... duplicate the row of logos so the loop seams cleanly ... -->
  </div>
</div>
```

---

## Card-on-hover behavior (shared)

All cards share this transition. Apply via class or inline:

```css
.aba-card {
  transition: border-color 200ms, box-shadow 200ms;
}
.aba-card:hover {
  border-color: rgba(8,124,167,0.5);
  box-shadow: 0 10px 25px -5px rgba(8,124,167,0.08);
}
```

No `transform`, no `scale`, no lift. Just a tinted border + a faint primary-tinted glow.
