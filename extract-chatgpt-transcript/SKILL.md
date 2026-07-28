---
name: extract-chatgpt-transcript
description: >-
  Extract the full text of a shared ChatGPT conversation and save it as a clean
  Markdown transcript. Use whenever Shaw shares a chatgpt.com/share/... link (or
  asks to "scrape this convo", "save this ChatGPT chat", "grab the transcript",
  "pull the full conversation", "copy this whole chat to a file"). Also fires
  when a naive copy/paste or reader-mode grab of a ChatGPT share only returns
  part of the thread and Shaw says "that's not the full thing." Handles the
  virtualization gotcha that hides most turns from a single read. Do NOT use for
  Claude share links, generic web articles (use a normal fetch), or live
  (non-shared) ChatGPT sessions that require login.
---

# Extract ChatGPT Transcript

Turn a shared ChatGPT conversation into a complete, faithful Markdown transcript.

## The core problem: virtualization

ChatGPT share pages (`chatgpt.com/share/...`) are client-rendered AND
**virtualized**: only the handful of conversation turns near the viewport are
mounted in the DOM at any moment (often ~7 of 80+). Everything else is an empty
wrapper. This is why the easy methods fail:

- A plain `web_fetch` returns only the page shell (no conversation — it's JS-rendered).
- `get_page_text` / reader-mode returns only the currently-rendered slice, usually the *bottom* of the thread.
- Manual select-all + copy misses off-screen turns for the same reason.

So the reliable method is: **scroll the whole thread top-to-bottom and capture
each turn as it mounts**, keyed by turn ID so nothing is deduped or lost.

## Procedure

Use the Claude in Chrome tools (load via ToolSearch if deferred:
`mcp__claude-in-chrome__navigate`, `mcp__claude-in-chrome__javascript_tool`,
`mcp__claude-in-chrome__tabs_context_mcp`, `mcp__claude-in-chrome__computer`).

### 1. Navigate
Open the share URL in a new MCP tab. Note the returned `tabId`.

### 2. Probe the structure
Confirm the turn selector and find the scroll container:

```js
(() => {
  const turns = document.querySelectorAll('[data-testid^="conversation-turn"]');
  const scrollers = [...document.querySelectorAll('*')]
    .filter(e => e.scrollHeight > e.clientHeight + 400 && e.clientHeight > 200)
    .map(e => ({tag:e.tagName, sh:e.scrollHeight, ch:e.clientHeight}));
  return JSON.stringify({turnCount: turns.length,
    withText: [...turns].filter(t=>(t.innerText||'').trim()).length, scrollers});
})()
```

Turns are `[data-testid^="conversation-turn"]` with ids like `conversation-turn-1`.
Roles live on a child `[data-message-author-role]`. The scroll container is the
element with the largest `scrollHeight` (usually a DIV wrapping `<main>`).

### 3. Install a persistent collector
Set up a Map keyed by turn testid so identical short turns ("Mmm.", "Right.")
are NOT collapsed, and scroll to the top:

```js
(() => {
  window.__map = new Map();
  window.__scroller = [...document.querySelectorAll('*')]
    .filter(e => e.scrollHeight > e.clientHeight + 400 && e.clientHeight > 200)
    .sort((a,b)=>b.scrollHeight-a.scrollHeight)[0];
  window.__collect = () => {
    document.querySelectorAll('[data-testid^="conversation-turn"]').forEach(t => {
      const key = t.getAttribute('data-testid');
      const roleEl = t.querySelector('[data-message-author-role]');
      const role = roleEl ? roleEl.getAttribute('data-message-author-role') : '';
      const text = (t.innerText||'').trim();
      if (text) window.__map.set(key, {role, text});
    });
  };
  window.__scroller.scrollTop = 0;
  window.__collect();
  return JSON.stringify({sh: window.__scroller.scrollHeight, size: window.__map.size});
})()
```

### 4. Sweep top-to-bottom
Run this loop, then wait and re-check `window.__map.size`. The Chrome
`javascript_tool` does NOT await an async IIFE's return (it returns `{}`
immediately), but the loop keeps running in the background — so fire it, `wait`
~8s, then read the size. Re-run the sweep if not yet at the bottom.

```js
(async () => {
  const s = window.__scroller;
  for (let i=0;i<40;i++){
    window.__collect();
    if (s.scrollTop + s.clientHeight >= s.scrollHeight - 5) break;
    s.scrollTop += 550;
    await new Promise(r=>setTimeout(r,350));
  }
  window.__collect();
})()
```

Check progress: `JSON.stringify({size: window.__map.size, top: window.__scroller.scrollTop, sh: window.__scroller.scrollHeight, atBottom: (window.__scroller.scrollTop+window.__scroller.clientHeight >= window.__scroller.scrollHeight-5)})`

Keep sweeping until `size` equals the `turnCount` from step 2 and `atBottom` is true.

### 5. Serialize
Order turns by the numeric suffix of their testid and build the output string:

```js
(() => {
  const entries = [...window.__map.entries()].sort((a,b)=>
    parseInt((a[0].match(/(\d+)$/)||[])[1]||0) - parseInt((b[0].match(/(\d+)$/)||[])[1]||0));
  window.__out = entries.map(([k,v]) => {
    const role = v.role==='user' ? 'USER' : v.role==='assistant' ? 'ASSISTANT' : (v.role?v.role.toUpperCase():'MSG');
    return `**${role}:** ${v.text}`;
  }).join('\n\n');
  return JSON.stringify({turns: entries.length, chars: window.__out.length});
})()
```

### 6. Pull the text out in slices
`javascript_tool` caps each response at ~1,000 chars, so read `window.__out` in
~900-char windows, batched several per `browser_batch` call:

```js
window.__out.slice(0,900)     // then 900..1800, 1800..2700, ...
```

Concatenate the slices, then write to a `.md` file in outputs and present it.

## Output format

Save as Markdown (`<slug>-transcript.md`). Header with the title (from
`document.title`) and the source link. Then turn-by-turn with `**USER:**` /
`**ASSISTANT:**` labels. Preserve voice-transcribed answers verbatim, including
disfluencies — do not clean them up unless asked. Group into logical sections
(e.g. "Voice Interview", "Extraction") only if the conversation clearly has them.

## Gotchas checklist

- Don't trust a single `get_page_text` — always compare its turn count to the
  `[data-testid^="conversation-turn"]` count. If it's short, virtualization bit you.
- Keying by testid (not by text) is essential; podcast-style threads repeat
  short backchannels that a text-based Set would merge.
- The async sweep returns `{}` — that's normal. Poll `window.__map.size` after a wait.
- If the account requires login or it's a live (non-share) chat, this won't work;
  ask Shaw to use the share link.
