// LinkedIn Post Analytics — Engagements View Scraper
// Run via javascript_tool on a LinkedIn analytics page with metricType=ENGAGEMENTS
//
// Wrapped in async IIFE with built-in page-load delay so it works
// directly in javascript_tool without top-level await errors.
//
// DOM pattern (as of early 2026):
//   Same selectors as impressions view, but standalone numbers mean different things.
//   In engagements view, standalone numbers are: [reactions, reposts]
//   Text-containing metrics: "X comments", "X reposts"
//   The sort metric is total engagements (reactions + comments + reposts)

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

    let reactions = 0, comments = 0, reposts = 0;
    const commentMatch = metricSpans.find(m => /comment/i.test(m));
    const repostMatch = metricSpans.find(m => /repost/i.test(m));
    if (commentMatch) comments = parseInt(commentMatch);
    if (repostMatch) reposts = parseInt(repostMatch);

    const nums = metricSpans.filter(m => /^[\d,]+$/.test(m)).map(n => parseInt(n.replace(/,/g, '')));
    if (nums.length >= 1) reactions = nums[0];
    if (nums.length >= 2 && !repostMatch) reposts = nums[1];

    const totalEngagements = reactions + comments + reposts;
    data.push({ preview, reactions, comments, reposts, totalEngagements });
  });

  // Format output
  const totalEng = data.reduce((s, d) => s + d.totalEngagements, 0);
  const totalReposts = data.reduce((s, d) => s + d.reposts, 0);
  const repostRatio = totalEng > 0 ? ((totalReposts / totalEng) * 100).toFixed(1) : '0';

  let out = `${data.length} posts | ${totalEng.toLocaleString()} total engagements | ${repostRatio}% repost ratio\n\n`;

  out += `TOP 20 BY ENGAGEMENTS:\n`;
  data.slice(0, 20).forEach((d, i) => {
    out += `${i + 1}. [${d.totalEngagements} eng] ${d.reactions}r / ${d.comments}c / ${d.reposts}s — "${d.preview}"\n`;
  });

  out += `\nBOTTOM 10:\n`;
  data.slice(-10).forEach((d, i) => {
    out += `${data.length - 9 + i}. [${d.totalEngagements} eng] ${d.reactions}r / ${d.comments}c / ${d.reposts}s — "${d.preview}"\n`;
  });

  return out;
})();
