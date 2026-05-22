// LinkedIn Post Analytics — Engagements View Scraper
// Run via javascript_tool on a LinkedIn analytics page with metricType=ENGAGEMENTS
//
// Wrapped in async IIFE with built-in page-load delay so it works
// directly in javascript_tool without top-level await errors.
//
// DOM pattern (as of mid-2026):
//   Same selectors as impressions view, but standalone numbers mean different things.
//   In engagements view, standalone numbers are: [reactions, totalEngagements]
//   "totalEngagements" is LinkedIn's all-up engagement count for the post —
//   reactions + comments + reposts + clicks/saves/other interactions. It is
//   NOT the repost count. Treating it as reposts is the most common failure
//   mode for this skill (see references/troubleshooting.md).
//
//   Text-containing metrics: "X comments", "X reposts". A "X reposts" span
//   only appears when LinkedIn chooses to surface it — most posts don't have
//   one even when reposts > 0. The only reliable way to get a per-post repost
//   count is to navigate to the post page itself.

(async () => {
  await new Promise(r => setTimeout(r, 3000));

  // Sanitize preview text — strip URLs and special chars that can trigger
  // Chrome tool content filters ([BLOCKED: Cookie/query string data])
  const sanitize = (text) =>
    text.replace(/https?:\/\/\S+/g, '[url]').replace(/[^\w\s.,!?'"\-:;()@#]/g, '');

  const allLinks = document.querySelectorAll('main li > a[href*="/feed/update/"]');
  const data = [];

  allLinks.forEach(link => {
    const li = link.closest('li');
    const allSpans = li.querySelectorAll('span');
    const spanTexts = Array.from(allSpans).map(s => s.innerText.trim()).filter(t => t);

    const postText = Array.from(allSpans).find(s => s.innerText.length > 80);
    const preview = postText ? sanitize(postText.innerText.substring(0, 50)) : 'N/A';

    const metricSpans = spanTexts.filter(t =>
      t.length < 30 && (/^[\d,]+$/.test(t) || /^\d+\s+(comment|repost)/i.test(t))
    );

    let reactions = 0, comments = 0, repostsShown = null, totalEng = 0;
    const commentMatch = metricSpans.find(m => /comment/i.test(m));
    const repostMatch = metricSpans.find(m => /repost/i.test(m));
    if (commentMatch) comments = parseInt(commentMatch);
    if (repostMatch) repostsShown = parseInt(repostMatch);

    const nums = metricSpans.filter(m => /^[\d,]+$/.test(m)).map(n => parseInt(n.replace(/,/g, '')));
    if (nums.length >= 1) reactions = nums[0];
    // The second standalone number is LinkedIn's totalEngagements metric.
    // Do NOT treat it as reposts.
    if (nums.length >= 2) totalEng = nums[1];

    data.push({ preview, reactions, comments, repostsShown, totalEng });
  });

  // Format output. We report LinkedIn's totalEngagements directly — this is
  // the correct numerator for engagement rate (totalEng / impressions).
  const sumEng = data.reduce((s, d) => s + d.totalEng, 0);

  let out = `${data.length} posts | ${sumEng.toLocaleString()} total engagements (LinkedIn metric)\n`;
  out += `Note: totalEng includes reactions + comments + reposts + clicks/saves/other.\n`;
  out += `Repost counts are not reliable from this view — visit the post page for ground truth.\n\n`;

  out += `TOP 20 BY TOTAL ENGAGEMENTS:\n`;
  data.slice(0, 20).forEach((d, i) => {
    const repostNote = d.repostsShown !== null ? ` (${d.repostsShown} reposts shown)` : '';
    out += `${i + 1}. [${d.totalEng} eng] ${d.reactions}r / ${d.comments}c${repostNote} — "${d.preview}"\n`;
  });

  out += `\nBOTTOM 10:\n`;
  data.slice(-10).forEach((d, i) => {
    out += `${data.length - 9 + i}. [${d.totalEng} eng] ${d.reactions}r / ${d.comments}c — "${d.preview}"\n`;
  });

  return out;
})();
