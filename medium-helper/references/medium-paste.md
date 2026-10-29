# Pasting into Medium's editor

Medium's editor (`.postArticle-content` contenteditable) listens for `paste` and converts HTML into
its own `graf` blocks. A synthetic `ClipboardEvent` with `text/html` set is accepted exactly like a
real paste. Typing the body with the `type` action works but is slow and drops heading levels;
`form_input` does nothing on a contenteditable.

## Sequence (Chrome, tab already on `medium.com/new-story`)

1. `left_click` the Title placeholder, `type` the title.
2. `left_click` the body placeholder ("Tell your story…") so `document.activeElement` is the
   editor.
3. `javascript_tool`:

```js
const html = `...full article HTML...`;
const dt = new DataTransfer();
dt.setData('text/html', html);
dt.setData('text/plain', html.replace(/<[^>]+>/g, ''));
const evt = new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true});
const target = document.activeElement;
const r = target.dispatchEvent(evt);
({tag: target.tagName, cls: target.className, dispatched: r, defaultPrevented: evt.defaultPrevented});
```

Expected result: `cls` contains `postArticle-content`, `dispatched: false`,
`defaultPrevented: true`. If `cls` is something else the click missed the editor — click again and
re-run; the editor only pastes into the focused element.

4. Verify structure:

```js
const el = document.querySelector('.postArticle-content');
Array.from(el.querySelectorAll('h1,h2,h3,h4,p,figure,hr')).slice(0,15)
  .map(e => e.tagName + '.' + e.className.split(' ').slice(0,3).join('.') + ': ' + e.textContent.slice(0,60)).join('\n')
```

The title should be `H3.graf--h3.graf--leading` (Medium's title class), the subtitle `H4`, section
headings `H3`, sub-headings `H4`. Medium autosaves ("Saved" appears next to "Draft" in the header);
the tab URL becomes `https://medium.com/p/<id>/edit` — that is the link to report.

## Tag → Medium block

| Paste this | Medium shows |
|---|---|
| `<h4>` as the first element | subtitle (gray, under the title) |
| `<h1>` | big section heading (the "T" large option) |
| `<h2>` | small sub-heading (the "t" small option) |
| `<p>` | paragraph |
| `<strong>` / `<em>` | bold / italic |
| `<ul><li>` | bulleted list |
| `<hr>` | section divider (the three dots) |
| `<a href>` | link |
| `<blockquote>` | quote |

Don't paste `<h1>` for the title — the Title field is separate and pasting a second H1 creates a
duplicate heading in the body. Don't paste `<img>` with external URLs; Medium drops or breaks them.
Images are uploaded through the "+" menu, which is Shaw's step.

## Building the HTML from Notion markdown

Notion's fetch returns markdown with escaped characters (`\$`, `\{`, `\}`). Unescape them. Notion's
bold-heading style `### **Good Idea 1: Sell First**` → `<h2>Good Idea 1: Sell First</h2>` (drop the
bold; the heading is already bold). A line that is only `…` is a divider Shaw uses between the intro
block and the body — render it as `<hr>` or drop it; both are fine.

Placeholders: anything in braces (`\{image\}`, `\{sales over time\}`, `\{Bad approach: …\}`) is a
note to self about a figure that doesn't exist yet. One italic paragraph each,
`<p><em>[IMAGE: sales over time]</em></p>`, same wording. Keep them in order; they are the to-do list
for section 3 of the skill.
