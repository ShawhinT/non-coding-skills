// LinkedIn Post Analytics — Impressions View Scraper
// Run via javascript_tool on a LinkedIn analytics page with metricType=IMPRESSIONS
//
// Wrapped in async IIFE with built-in page-load delay so it works
// directly in javascript_tool without top-level await errors.
//
// DOM pattern (as of early 2026):
//   Each post is an <li> inside <main> containing an <a href="/feed/update/...">
//   Metrics are short <span> elements (< 30 chars) matching number patterns
//   In impressions view, standalone numbers are: [reactions, impressions]
//   Text-containing metrics: "X comments", "X reposts"
//
// NOTE: This view does NOT reliably surface repost counts. Always pair with
// the engagements view scraper to get repost data.

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

    // Filter to metric-bearing spans only
    const metricSpans = spanTexts.filter(t =>
      t.length < 30 && (/^[\d,]+$/.test(t) || /^\d+\s+(comment|repost)/i.test(t))
    );

    let reactions = 0, comments = 0, reposts = 0, impressions = 0;
    const commentMatch = metricSpans.find(m => /comment/i.test(m));
    const repostMatch = metricSpans.find(m => /repost/i.test(m));
    if (commentMatch) comments = parseInt(commentMatch);
    if (repostMatch) reposts = parseInt(repostMatch);

    const nums = metricSpans.filter(m => /^[\d,]+$/.test(m)).map(n => parseInt(n.replace(/,/g, '')));
    if (nums.length >= 2) { reactions = nums[0]; impressions = nums[1]; }
    else if (nums.length === 1) { impressions = nums[0]; }

    const totalEng = reactions + comments + reposts;
    const engRate = impressions > 0 ? ((totalEng / impressions) * 100).toFixed(1) : '0';

    data.push({ preview, reactions, comments, reposts, impressions, totalEng, engRate });
  });

  // Format output
  const totalImpr = data.reduce((s, d) => s + d.impressions, 0);
  const totalEng = data.reduce((s, d) => s + d.totalEng, 0);
  const avgEngRate = totalImpr > 0 ? ((totalEng / totalImpr) * 100).toFixed(2) : '0';

  let out = `${data.length} posts | ${totalImpr.toLocaleString()} total impressions | ${totalEng.toLocaleString()} total engagements | ${avgEngRate}% avg eng rate\n\n`;

  out += `TOP 20 BY IMPRESSIONS:\n`;
  data.slice(0, 20).forEach((d, i) => {
    out += `${i + 1}. ${d.impressions.toLocaleString()} impr | ${d.engRate}% eng | ${d.reactions}r/${d.comments}c/${d.reposts}s — "${d.preview}"\n`;
  });

  out += `\nBOTTOM 10:\n`;
  data.slice(-10).forEach((d, i) => {
    out += `${data.length - 9 + i}. ${d.impressions.toLocaleString()} impr | ${d.engRate}% eng — "${d.preview}"\n`;
  });

  return out;
})();
