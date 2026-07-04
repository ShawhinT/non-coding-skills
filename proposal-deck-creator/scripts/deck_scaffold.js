/*
 * Proposal Deck scaffold (pptxgenjs).
 *
 * Copy this file next to your work, fill in the three slide bodies, and run:
 *   npm install pptxgenjs react-icons react react-dom sharp
 *   node deck_scaffold.js
 *   python <pptx-skill>/scripts/rezip.py <Output>.pptx
 * Then render + visual-QA via the pptx skill.
 *
 * It pre-wires: the ABA proposal palette, a fresh-shadow helper (pptxgenjs
 * mutates option objects in place, so never share one shadow object), a
 * react-icons -> PNG rasterizer, and a shared eyebrow+title header.
 * Read references/design-conventions.md before changing colors or layout.
 */
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaUserTie, FaUsers, FaLaptopCode, FaRocket, FaSyncAlt, FaChartLine, FaShieldAlt, FaCheckCircle } = require("react-icons/fa");

// ---- palette (see aba-brand-system + design-conventions.md) ----
const CERULEAN = "087CA7";   // brand primary, the one accent
const GREEN    = "6BA329";    // secondary audience accent / "Case study" tag
const GOLD      = "B07D12";   // goldenrod text (warning), "Example" tag
const GOLD_ICON = "D19C1D";   // brighter goldenrod for icons/graphics
const INK       = "0B0E1A";   // headings / near-black (never pure #000)
const BODY      = "454A57";   // body text
const MUTE      = "7A7F8C";   // captions / muted
const PAGE      = "FAFAF7";   // light page background (not pure white)
const CARD      = "FFFFFF";
const BORDER    = "E4E6E2";
const TINT_BLUE = "EAF3F8", TINT_GREEN = "F1F6E9", TINT_YELLOW = "FBF3DE";

const FONT = "Roboto"; // honor the client's font convention; else a safe sans (Arial/Calibri)
const W = 13.333, MX = 0.7, GAP = 0.3;

const makeShadow = () => ({ type: "outer", color: "000000", blur: 7, offset: 3, angle: 90, opacity: 0.10 });

async function icon(IconComponent, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(IconComponent, { color: "#" + color, size: String(size) }));
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

// eyebrow + title  OR  title + subtitle — never all three (pass null for the unused one)
function header(slide, eyebrow, title, subtitle) {
  if (eyebrow) slide.addText(eyebrow.toUpperCase(), { x: MX, y: 0.5, w: W - 2 * MX, h: 0.3, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: CERULEAN, charSpacing: 2 });
  slide.addText(title, { x: MX, y: 0.82, w: W - 2 * MX, h: 0.7, margin: 0, fontFace: FONT, fontSize: 34, bold: true, color: INK });
  if (subtitle) slide.addText(subtitle, { x: MX, y: 1.52, w: W - 2 * MX, h: 0.4, margin: 0, fontFace: FONT, fontSize: 16, color: BODY });
}

function card(slide, pres, x, y, w, h, fill) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill || CARD }, line: { color: BORDER, width: 1 }, shadow: makeShadow() });
}

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "W", width: 13.333, height: 7.5 });
  pres.layout = "W";
  pres.author = "Shaw Talebi, AI Builder Academy";

  // Preload audience + stage icons (color goes on icons, not text).
  const ic = {
    exec: await icon(FaUserTie, CERULEAN), champ: await icon(FaUsers, GREEN), tech: await icon(FaLaptopCode, GOLD_ICON),
    rocket: await icon(FaRocket, CERULEAN), sync: await icon(FaSyncAlt, CERULEAN), chart: await icon(FaChartLine, GREEN),
    shield: await icon(FaShieldAlt, GOLD_ICON), check: await icon(FaCheckCircle, GREEN),
  };

  // ---- Slide 1: Executive summary ----
  const s1 = pres.addSlide(); s1.background = { color: PAGE };
  header(s1, "AI Builder Academy  ·  Proposal for [Client]", "Executive summary", null);
  // TODO: purpose band (TINT_BLUE) + What / Why / Outcomes cards. See structure-patterns.md.

  // ---- Slide 2: The impact ----
  const s2 = pres.addSlide(); s2.background = { color: PAGE };
  header(s2, "The impact", "Proven results across three audiences", null);
  // TODO: three audience cards (ic.exec/champ/tech), each with CASE STUDY (GREEN) / EXAMPLE (GOLD) tagged items.
  // See impact-slide-patterns.md.

  // ---- Slide 3: Transformation roadmap ----
  const s3 = pres.addSlide(); s3.background = { color: PAGE };
  header(s3, "AI transformation roadmap", "The path to becoming an AI-native org", null);
  // TODO: Activation / Adoption / Expansion stage cards + warning-yellow Foundation bar (TINT_YELLOW, ic.shield, GOLD label).

  await pres.writeFile({ fileName: "Proposal-Deck.pptx" });
  console.log("written");
})();
