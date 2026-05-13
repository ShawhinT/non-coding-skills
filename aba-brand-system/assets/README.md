# Logo files

Bundled with this skill so it has no external dependencies. Reference these in HTML deliverables with a relative path from your output file to wherever you copy them, or paste their contents inline if you need a single-file deliverable.

| File | Purpose | When to use |
|---|---|---|
| `logo-wide-dark.png` | Wide wordmark, dark variant | **Default.** Use on the dark `#010413` site background. Render at `height: 54px` in the navbar. |
| `logo-wide-light.png` | Wide wordmark, light variant | Only when the background is light (off-brand for ABA itself but useful in mixed-brand decks). |
| `logo-square-dark-192.png` | Square mark, 192px, dark variant | Footer (40×40 rounded), chip avatars, dark-background slides. |
| `logo-square-dark-512.png` | Square mark, 512px, dark variant | Higher-resolution use — app icons, large social graphics. |
| `logo-square-light-192.png` | Square mark, 192px, light variant | Same as above but on light backgrounds. |
| `favicon-32x32.png` | 32×32 favicon | Browser tab icon. |

## Conventions

- **The site is dark, so the dark-variant logo is the default.** Reach for light-variant only when explicitly designing for a light surface.
- **Square mark in the navbar** is paired with the wordmark text in Manrope 700: `<img> [40px] + <span>AI Builder Academy</span>`. The wide wordmark replaces both.
- **Footer logo** is the 192px square mark, rendered at 40×40 with `border-radius: 8px`.
- **Never** stretch, recolor, drop a shadow on, or overlay the logo. If you need it on a busy photo, put it on a dark/light flat surface first.

## "Taught at" / partner logos

The site shows a marquee of partner wordmarks (Google, Microsoft, Meta, AWS, NCSL, CEI, Matson, etc.) **inverted to white at 40% opacity**:

```css
filter: brightness(0) invert(1);
opacity: 0.4;
```

Don't bundle partner logos with this skill — pull them from the live site or the user's `assets/logos/` folder when needed.
