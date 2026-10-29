// Everyone Shaw has a LinkedIn DM conversation with, newest first, back to a
// cutoff — the inbox half of the "already in motion" check.
//
// Run via javascript_tool on any linkedin.com page. Set window.__DM_DAYS first
// (default 60). Results land on window.__dms and localStorage.__aba_dms:
// one row per 1:1 conversation { name, headline, last, created, shawLast }.
// Group chats are skipped.
//
// The legacy /voyager/api/messaging/conversations endpoint returns 500. What
// works is the messenger GraphQL query the /messaging/ page itself uses:
//   messengerConversations (queryId below) with category INBOX, paged by
//   lastUpdatedBefore on the first call and nextCursor after that.
// The other queryId (messengerConversationsBySyncToken) returns only the
// latest 20 and won't page. If this one 400s/404s, the queryId has rotated:
// open /messaging/, read the live messengerConversations request from
// performance.getEntriesByType('resource'), and set window.__DM_QID. Print only
// the queryId — echoing the full URL gets blocked as cookie/query-string data.
//
// Accept header must be application/graphql. The mailbox is Shaw's own
// fsd_profile urn, resolved from /voyager/api/me. Only the Inbox folder is
// read; Other/Archived are not.
//
// Matching against candidates is by name, loosely, as with the Notion check.

await (async () => {
  const DAYS = window.__DM_DAYS || 60;
  const cutoff = Date.now() - DAYS * 864e5;
  const qid = window.__DM_QID || 'messengerConversations.9501074288a12f3ae9e3c7ea243bccbf';
  const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
  if (!csrf) return JSON.stringify({ error: 'No JSESSIONID cookie' });
  const H = { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0', 'accept': 'application/graphql' };

  const me = await fetch('/voyager/api/me', { headers: { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0' }, credentials: 'include' });
  const mailbox = (JSON.stringify(await me.json()).match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/) || [])[0];
  if (!mailbox) return JSON.stringify({ error: 'could not resolve own fsd_profile urn' });
  const myId = mailbox.split(':').pop();

  const out = [];
  let cursor = null, before = Date.now(), pages = 0;
  while (pages++ < 20) {
    let v = '(query:(predicateUnions:List((conversationCategoryPredicate:(category:INBOX)))),count:20,mailboxUrn:' +
            encodeURIComponent(mailbox);
    v += cursor ? ',nextCursor:' + encodeURIComponent(cursor) + ')' : ',lastUpdatedBefore:' + before + ')';
    const r = await fetch('/voyager/api/voyagerMessagingGraphQL/graphql?queryId=' + qid + '&variables=' + v,
                          { headers: H, credentials: 'include' });
    if (!r.ok) return JSON.stringify({ error: 'HTTP ' + r.status + ' — queryId may have rotated (see header)', pages, rows: out.length });
    const data = (await r.json()).data || {};
    const block = Object.values(data).find(x => x && Array.isArray(x.elements)) || {};
    const els = block.elements || [];
    if (!els.length) break;
    for (const c of els) {
      if (c.groupChat) continue;
      const other = (c.conversationParticipants || [])
        .map(p => (p.participantType || {}).member)
        .find(m => m && !JSON.stringify(m).includes(myId));
      if (!other) continue;
      const sender = JSON.stringify(((((c.messages || {}).elements || [])[0] || {}).sender) || '');
      out.push({
        name: `${(other.firstName || {}).text || ''} ${(other.lastName || {}).text || ''}`.trim(),
        headline: ((other.headline || {}).text || '').slice(0, 90),
        last: new Date(c.lastActivityAt).toISOString().slice(0, 10),
        created: c.createdAt ? new Date(c.createdAt).toISOString().slice(0, 10) : null,
        shawLast: sender.includes(myId)
      });
    }
    const oldest = Math.min(...els.map(c => c.lastActivityAt || Date.now()));
    if (oldest < cutoff) break;
    cursor = (block.metadata || {}).nextCursor || null;
    if (!cursor) { before = oldest; }
    await new Promise(r => setTimeout(r, 400));
  }

  window.__dms = out.filter(d => Date.parse(d.last) >= cutoff);
  try { localStorage.setItem('__aba_dms', JSON.stringify(window.__dms)); } catch (e) {}
  return JSON.stringify({ conversations: window.__dms.length, pages, oldest: window.__dms.length ? window.__dms[window.__dms.length - 1].last : null });
})();
