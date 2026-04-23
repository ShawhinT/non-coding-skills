// LinkedIn Post Analytics — Impressions View with Post Type Categorization
// Run via javascript_tool on a LinkedIn analytics page with metricType=IMPRESSIONS
//
// Wrapped in async IIFE so the built-in page-load delay works without
// top-level await errors in javascript_tool.
//
// Extends the base impressions scraper with heuristic post type classification
// and aggregated stats by type. Useful for content strategy analysis.

(async () => {
  await new Promise(r => setTimeout(r, 3000));

  const sanitize = (text) =>
    text.replace(/https?:\/\/\S+/g, '[url]').replace(/[^\w\s.,!?'"\u201C\u201D\u2018\u2019\u2014\-:;()@#]/g, '');

  // Curated lists with number hooks ("10 YouTube channels that...") are Shaw's
  // highest-ceiling format — they drive massive reposts and have long shelf lives.
  // Check for this pattern before other types.
  function categorizePost(preview) {
    const ft = preview.toLowerCase();
    if (/^\d+\s/.test(ft) && (ft.includes('channel') || ft.includes('tool') ||
        ft.includes('resource') || ft.includes('website') || ft.includes('app') ||
        ft.includes('project') || ft.includes('that will') || ft.includes('that keep')))
      return 'curated-list';
    if (ft.includes('believe') || ft.includes('disagree') || ft.includes('opinion') ||
        ft.includes('here is something') || ft.includes('hot take') || ft.includes('controversial'))
      return 'opinion';
    if (ft.includes('i pay') || ft.includes('i spent') || ft.includes('i use') ||
        ft.includes('my ') || ft.includes("i'm ") || ft.includes('i learned') ||
        ft.includes('side hustle') || ft.includes('$'))
      return 'personal';
    if (ft.includes('workshop') || ft.includes('free') || ft.includes('register') ||
        ft.includes('event') || ft.includes('bootcamp') || ft.includes('closing') ||
        ft.includes('promo') || ft.includes('download') || ft.includes('guide'))
      return 'promo';
    if (ft.includes('youtube') || ft.includes('video') || ft.includes('watch') ||
        ft.includes('course'))
      return 'video-bridge';
    return 'educational';
  }

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

    let reactions = 0, comments = 0, reposts = 0, impressions = 0;
    const commentMatch = metricSpans.find(m => /comment/i.test(m));
    const repostMatch = metricSpans.find(m => /repost/i.test(m));
    if (commentMatch) comments = parseInt(commentMatch);
    if (repostMatch) reposts = parseInt(repostMatch);

    const nums = metricSpans.filter(m => /^[\d,]+$/.test(m)).map(n => parseInt(n.replace(/,/g, '')));
    if (nums.length >= 2) { reactions = nums[0]; impressions = nums[1]; }
    else if (nums.length === 1) { impressions = nums[0]; }

    const type = categorizePost(preview);
    const totalEng = reactions + comments + reposts;
    data.push({ preview, reactions, comments, reposts, impressions, type, totalEng });
  });

  // Aggregate by type
  const byType = {};
  data.forEach(d => {
    if (!byType[d.type]) byType[d.type] = { count: 0, impr: 0, eng: 0 };
    byType[d.type].count++;
    byType[d.type].impr += d.impressions;
    byType[d.type].eng += d.totalEng;
  });

  const totalImpr = data.reduce((s, d) => s + d.impressions, 0);

  let out = `${data.length} posts | ${totalImpr.toLocaleString()} total impressions\n\n`;

  out += `BY TYPE:\n`;
  Object.entries(byType).sort((a, b) => b[1].impr - a[1].impr).forEach(([type, stats]) => {
    const avgImpr = Math.round(stats.impr / stats.count);
    out += `  ${type}: ${stats.count} posts | ${stats.impr.toLocaleString()} impr (avg ${avgImpr.toLocaleString()}) | ${stats.eng} eng\n`;
  });

  out += `\nTOP 10:\n`;
  data.slice(0, 10).forEach((d, i) => {
    out += `${i + 1}. ${d.impressions.toLocaleString()} impr [${d.type}] | ${d.reactions}r/${d.comments}c/${d.reposts}rp "${d.preview}"\n`;
  });

  out += `\nBOTTOM 5:\n`;
  data.slice(-5).forEach((d, i) => {
    out += `${data.length - 4 + i}. ${d.impressions.toLocaleString()} impr [${d.type}] "${d.preview}"\n`;
  });

  return out;
})();
