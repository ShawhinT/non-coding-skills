# ABA — event / sponsor slide composition

Load this when building an **event or sponsor slide**: a single 16:9 slide that promotes a live event and usually gets handed to a partner to drop into *their* deck (sponsor spotlight, webinar promo, conference slide). The universal tokens in `SKILL.md` still apply; this file covers what makes this surface different from a scroll-stopping social still or a web hero.

The job of the slide is narrow: **convert a room's attention into a scan/registration.** It is seen from across a room, briefly, often while someone talks. Design backward from the scan — everything else is support.

## Why it's its own surface

It borrows the still's display-type rules but breaks two of `infographic-composition.md`'s conventions on purpose:

- **A QR + "scan to register" is legitimate here.** The still guide bans CTA buttons because a feed image isn't clickable. A QR *is* the actionable element, so its microcopy is functional, not a web-style pill CTA.
- **A centered bottom footer is legitimate here.** The still convention is a quiet corner URL signature. A sponsor slide is a title/hero surface where the brand *is* the point, so a centered `[square mark]  aibuilder.academy` footer (optionally over a 1px `rgba(255,255,255,0.08)` divider) reads as intentional, not as chrome.

## Layout — split, QR as co-hero

Default is a two-column split on the `#010413` canvas:

- **Left (~58%):** the message stack — eyebrow (optional), headline, a `FREE` lime tag + one-line descriptor, a "Led by" block, and the date/time/location. One Cerulean accent does the chromatic work (e.g. the number in the headline); the lime `FREE` tag is the defined "free/available" token, not a second accent.
- **Right (~42%):** the QR as a white card, vertically centered. This is the biggest single element after the headline.

A centered-QR-hero variant (QR dead-center, text above/below) scans even better in a room but shrinks the message; reach for split when the slide also has to carry a title, presenter, and logistics.

## The QR is the conversion element

- **Large.** Size it to scan from the back rows — err bigger. It's a co-hero, not a footnote.
- **On a `#FFFFFF` card.** QR scanners choke on codes over dark or textured backgrounds, so this is the one place raw white is correct even though the brand otherwise bans pure `#fff`. Dark modules (`#010413`/near-black) on white.
- **Verify it decodes before shipping.** Generate with error-correction H, then actually decode the rendered code (`opencv` `QRCodeDetector` or `pyzbar`) and confirm the string — including the UTM. A pretty QR that doesn't scan fails the only job.
- **Every event link carries its channel UTM** (`?utm_source=…`) so registrations attribute back to this slide.

## Match the registration cover

If the event has a Luma/registration cover, the slide should read as the *same campaign*: reuse its title wording, its subhead ("Live workshop & Q&A"), its "Led by" treatment, and its logistics. Consistency between the slide and the page the scan lands on is worth more than a cleverer headline. Pull the event's real palette/wording from the cover rather than inventing parallel copy.

## Presenter headshot

Mirror the cover's circular avatar next to the "Led by / Name / Title" block:

- **Face-centered crop with headroom** — leave space above the hair; a too-tight crop that clips the hairline is the most common miss. Include a little shoulder, like a cover portrait.
- Mask to a clean circle (supersample the alpha for a smooth edge), and on the dark canvas add a subtle ring (`box-shadow: 0 0 0 4px rgba(255,255,255,0.10)`), not a hard border.
- Ask for a **high-res source** (≥1000px square). Extracting the face from an existing cover PNG works only as a low-res fallback and will look soft on a projector.

## Location / platform line

Echo the cover's "Hosted live from: …". For an online event, a small line under the date — a video-camera icon (Heroicons outline) + "Hosted live on Zoom" — does it. The platform's own brand color on its name (Zoom blue `#2D8CFF`) is an allowed product brand-mark, not a second accent, same rule as depicting Claude coral or Stripe purple.

## Accuracy small print

Get the timezone label right: US Central is **CT/CDT in summer**, not CST. Prefer the neutral "CT" unless the event is in winter. Same care for the date's weekday.

## Build + export pipeline

Custom fonts (Manrope, Libre Franklin, JetBrains Mono) won't be installed on a partner's machine, so a **full-bleed image beats native text boxes** for a handed-off slide — it renders identically everywhere. Recommended path:

1. **Design in HTML/CSS** with the ABA fonts loaded from Google Fonts, at a fixed 1920×1080 stage. Use flex spacers to balance blocks (e.g. equal space above/below the "Led by" section) and measure element bounding boxes to confirm no overflow rather than eyeballing.
2. **Render to PNG** with headless Chromium (Playwright) at `device_scale_factor: 2` for a crisp 3840×2160.
3. **QR** via Python `qrcode` (ecc H, dark-on-white), embedded base64; decode-verify as above.
4. **Wrap into PPTX** with `pptxgenjs`: set `p.layout = "LAYOUT_WIDE"` (13.333×7.5 in) *before* adding the slide, then one `addImage({ path, x:0, y:0, w:13.333, h:7.5 })`. Validate with the `pptx` skill's `validate.py`.

Deliver both the PNG (universal drop-in) and the PPTX (editable container for the partner's deck).

Minimal skeleton (drop the base64 blobs and full CSS for brevity):

```python
# qr.png: qrcode ERROR_CORRECT_H, fill="#010413", back="#FFFFFF"; then decode-verify
# head.png: face-centered square crop -> resize -> circular alpha mask
# slide.html: split layout, ABA fonts, images embedded as base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1920,"height":1080}, device_scale_factor=2)
    pg.goto("file:///.../slide.html"); pg.wait_for_timeout(1200)
    pg.screenshot(path="slide.png", clip={"x":0,"y":0,"width":1920,"height":1080})
    b.close()
```

```js
// pptxgenjs: full-bleed 16:9
const p = new pptxgen(); p.layout = "LAYOUT_WIDE";
const s = p.addSlide(); s.background = { color: "010413" };
s.addImage({ path: "slide.png", x: 0, y: 0, w: 13.333, h: 7.5 });
p.writeFile({ fileName: "event-slide.pptx" });
```

## Reference artifact

`assets/example-event-slide.png` — a shipped split-layout event slide (eyebrow + benefit headline, `FREE` + descriptor, headshot + "Led by," date/time + Zoom location, centered footer, QR-hero card). Copy its structure before inventing a new one.

## Checklist before shipping an event slide

1. ☐ QR is large, on `#FFFFFF`, and its rendered form decodes to the correct UTM link.
2. ☐ Title/subhead/"Led by"/logistics match the registration cover.
3. ☐ Headshot has headroom (hair not clipped), circular with a subtle ring on dark.
4. ☐ Location line present; platform name in its own brand color, one Cerulean accent otherwise.
5. ☐ Timezone label correct (CT/CDT in summer), weekday correct.
6. ☐ No overflow (measure boxes); blocks balanced with spacers.
7. ☐ Delivered as PNG **and** validated PPTX (`LAYOUT_WIDE`, full-bleed image).
