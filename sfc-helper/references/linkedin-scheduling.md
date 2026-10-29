# Scheduling LinkedIn Posts

The execution layer for a ⬜ LinkedIn page: use it when Shaw says to stage, paste, or
schedule one in the LinkedIn composer. It covers pulling the copy off the page, getting it
into the composer intact, setting the slot, and closing the loop on the SFC row.

## Inputs

- **The SFC page, fetched fresh.** Shaw edits the copy right up to the moment he asks, so
  an earlier read in the same conversation is stale. Use the copy verbatim; anything on the
  page that isn't post copy (notes, pinned blockquotes) is production context, not content.
  The copy is everything below the `---` divider (older pages: a fenced code block).
  Numbered items can come back as Notion list blocks that read as all `1.` — type each
  item's real position into the composer.
- **Date** from the page's `Date` property; **time** from Shaw. Scheduling is publishing —
  "paste it in" means stop with the composer filled, and the Schedule click waits for an
  exact date and time from him.

## The row matches what's live

The page is the record of what ran, so the composer and the page carry the same text. If
you spot a typo while staging, fix it on the page as well as in the composer (and say so),
or leave both alone and flag it — a fix made only in the composer leaves the record wrong.

## Media is part of the post

An image, video, or document on the page ships with the post. If you can't attach it from
where you're running, the final click waits: tell Shaw the composer is staged text-only and
let him attach it or say to go without. A text-only schedule of a post that was drafted
with a visual is a different post.

## Compose

Click **Start a post** on the feed to open the composer. The **Add collaborators** button
sits nearby; collaborators aren't tags.

**Blank lines don't survive a plain-text paste.** The editor is a rich-text
(ProseMirror) field that turns every newline into a paragraph and drops the empty ones, so
copy pasted as text arrives as one unbroken wall. Paste it as HTML instead, with an
explicit empty paragraph between each paragraph of copy:

```js
const ed = document.querySelector('[contenteditable="true"]');
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const html = paras.map(esc).map(t => `<p>${t}</p>`).join('<p><br></p>');
const dt = new DataTransfer();
dt.setData('text/html', html); dt.setData('text/plain', paras.join('\n\n'));
ed.focus();
ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
```

**Verify what landed, by count and by text.** Read the editor's `<p>` elements back: N
paragraphs of copy should give 2N−1 paragraphs with N−1 empty, and the non-empty ones
should equal the page's paragraphs. A screenshot shows that text is there, not that the
spacing or wording is identical. Select the editor by attribute, not class — its class
names change.

**Tags.** A `-Name` in the copy is Shaw's placeholder for an @mention. Paste the copy
around it, then type each tag as `@` + name so the typeahead resolves it — pasted text
never becomes a mention. The typeahead lags a keystroke; if results look stale, delete and
retype the last character. Orgs often have duplicate or personal look-alike pages, so pick
the real one (follower count, via company search in a *separate* tab — navigating the
composer's tab discards the draft). If no page exists, leave the name as plain text and say
so. Mentions render the page's full name; update the page copy to match.

## Schedule

1. Clock icon next to **Post** opens the schedule dialog.
2. **Date:** select the field's contents and type `m/d/yyyy`.
3. **Time:** typing the time opens a dropdown of 15-minute options; click the matching
   option — the typed text alone isn't committed.
4. Read the "Posting at <day>, <date>, <time>" line under the fields before confirming;
   it's the dialog's own statement of what it understood.
5. **Confirm** returns to the composer, where **Post** has become **Schedule**. Click it
   and look for the "Post scheduled" toast.

## Close the loop

Report the verified date and time. Flip the page's icon from ⬜ to ✅ — a scheduled post is
done as far as the SFC calendar is concerned — record the slot in `Time`, and update `Date`
if what was scheduled differs from the page.
