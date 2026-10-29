# Scheduling YT Community Posts

Repurpose mode ends with a staged 🔴 SFC page; this file is the execution layer that ships
it. Use it when Shaw says to schedule (or post) a YT Community page — it covers pulling the
copy off the page, prepping media, and driving the YouTube composer via the Claude in Chrome
tools. Distilled from real runs, including one Shaw demonstrated by hand — the details below
exist because the obvious routes failed.

## Inputs

- **The SFC page.** The post copy is everything below the `---` divider (older pages: a
  fenced code block) — use it verbatim. Pinned blockquote notes above it (📷 media, ⚠️ stale/mismatched copy) are production
  instructions, not content. When a note says the page is the same post as a LinkedIn page,
  that page's copy is what ships — sync this page to it if they've drifted, then type.
- **Date** comes from the page's `Date` property; **time** from Shaw (his standing pattern
  so far: 10:00 AM CT). Scheduling is publishing — if he hasn't named the date/time
  exactly, confirm before the final click.

## Prep the text

- Keep proven copy **verbatim** — it won on its wording. The edits that are safe to make
  without asking are the ones the page notes call for, plus one standing rule: drop any
  "My channel: <link>" plug (the audience is already on the channel; lnkd.in links look
  off there).
- **Resolve lnkd.in shortlinks** by navigating to them — LinkedIn's interstitial ("this
  link will take you to a page that's not on LinkedIn") prints the destination URL.
- **If a link points to one of Shaw's own videos, attach the video instead of pasting the
  URL.** A native attachment renders the real thumbnail, title, and view count. Adjust the
  closing line to point at the card ("You can watch the full session here 👇") and skip any
  image — the card is the visual. The attach itself is Shaw's step (see Media).
- **Verify what landed in the composer.** After typing, read the composer back
  (`#contenteditable-root`), normalize `\n\n\n` to `\n\n`, and compare it to the page's copy
  for equality, reporting the first differing index. Typing is as silent about dropped
  characters as a truncated slice is, and a screenshot confirms the text is *there*, not that
  it is identical.
- Notes may *suggest* reframing for the YT audience; surface those as options rather than
  silently rewriting a proven post.

## Media

**Video: hand off one step.** The composer's Video picker is a cross-origin Google Picker
iframe; browser-automation clicks, typing, and scrolling don't reach it (keystrokes fall
through to the page, where `/` opens YouTube's search). So prep everything else — copy typed
and verified, date and time set in the schedule panel — then ask Shaw to click **Video** →
pick the named video → **Schedule**, and verify the Scheduled tab once he confirms.

**Image Shaw supplies as a file** (e.g. in a connected folder): stage it into the session and
call `file_upload` with the *staged* path (the device path and the outputs folder are
rejected) on the composer's image input — the one inside
`ytd-backstage-multi-image-select-renderer`, not the masthead's search-by-image input. This
uploads the original at full quality. The first upload can open a preview-crop editor:
keep the image with **Save Preview**, since its Cancel removes the image. After an upload
the Post button can stay disabled until the text gets an input event; type and delete a
character to wake it.

**Several images go in one file at a time.** Handing the dropzone input several files at once
shows every thumbnail but registers only the last upload, and YouTube then rejects the whole
post. Upload the first file to the dropzone input, then each further one to the single-file
input inside the add-image tile (`#add-image-button-container`), waiting for its thumbnail
before the next. That input is re-created after every upload, so `find` it again each time.
Wait until Post is no longer greyed out before opening the schedule menu: grey means an
upload is still in flight.

**Image that exists only on the LinkedIn post: save the original, then upload it as a
supplied file.** Open the post (`linkedin.com/feed/update/urn:li:activity:<id>/`) and click
the photo — the viewer loads the full-resolution version, where the feed holds only a
downscaled one. In that tab, `fetch` the image's src and save the blob to Downloads through an
`<a download>` click, then list the folder to confirm it landed. Chrome lets a tab trigger
one scripted download and silently blocks the rest, so take each image from a fresh tab. A
saved original keeps its full size and shape; any screenshot-based route crops it to the
viewport and recompresses it.

## Compose

Go straight to **`youtube.com/@ShawhinTalebi/posts`** — the composer ("Post an update to
your fans") is at the top. (`youtube.com/post_dashboard` 404s; studio.youtube.com is a
detour.) Click the placeholder text, then type the copy, attach media, and screenshot to
confirm everything looks right.

**Confirm focus before every type call, in the composer and in each poll field.** Read
`document.activeElement` and check it is the field you mean (`#contenteditable-root` for the
post text, an `input` with placeholder "Add option" for a poll option) — and make the check
throw, so a batched sequence stops instead of typing anyway. Keystrokes sent with focus
elsewhere don't vanish: they run as YouTube's keyboard shortcuts, which can navigate off
the page and discard the draft. The page also hydrates slowly, so a first click on the
placeholder can land before the composer is live; wait and click again rather than typing.

A poll re-run uses **Text poll**, which has no question field: the poll's question goes as
the last line of the post text, and each option goes in its own field. Click each field by
coordinate from a fresh screenshot — a click by `find` ref does not reliably focus these
inputs — and run the focus check above before typing into it.

## Schedule

1. Dropdown arrow next to **Post** → **Schedule post**.
2. Sanity-check the timezone label (e.g. `(GMT-0500) Local Time` = Central in summer)
   against the requested time before trusting it.
3. **Date:** click the field, click the day in the calendar — then verify the field text shows the intended date before moving on. A click that lands a hair off selects the neighboring day (has happened in a real run: aimed 19, got 18).
4. **Time:** the option list is a Polymer overlay whose 96 options are ordinary light-DOM
   elements that ignore synthetic mouse input — typing sets nothing, a drag near the list
   dismisses it, and a click on a visible option (by coordinate or accessibility ref)
   closes the list without selecting. Drive it through the DOM instead. Click the field to
   open the list, then with `javascript_tool`:
   ```js
   const mb = [...document.querySelector('ytd-date-time-picker-renderer')
     .querySelectorAll('tp-yt-paper-menu-button')][1];   // 0=date, 1=time, 2=timezone
   const opts = [...mb.querySelector('[role=listbox]').querySelectorAll('[role=option]')];
   const norm = s => s.replace(/\s+/g, ' ').trim();
   opts.find(o => norm(o.textContent) === '10:00 AM').click();   // 15-min steps from 12:00 AM
   ```
   The field updates and the list closes on its own; screenshot to confirm it stuck.
   Rendered text is never the text you typed or read — collapse every whitespace run before
   comparing. Option labels use a non-breaking space between the time and the meridiem, and
   `innerText` on the composer adds a newline per block, so a blank line reads back as
   `\n\n\n`. Normalize both sides and compare programmatically, not by eye.
5. Click **Schedule**, then verify in the **SCHEDULED** tab — the entry reads "Scheduled
   for <date>, <time> (local time)". Do this per post, before composing the next one. A
   rejected post fails quietly: the composer stays put with a small red "We weren't able to
   add your post" line under the media, and from a scrolled viewport it looks like it went
   through. An entry in the tab is the only confirmation; reload the page if the tab hasn't
   picked it up.

## Close the loop

Report back with the verified date/time. Flip the page's icon from 🔴 to ✅ — a scheduled
post is done as far as the SFC calendar is concerned, and the icon is how Shaw reads that at
a glance. Record the slot in the page's `Time` property, and
if what was scheduled differs from the page's `Date`, update that too — the row should match
what is live. Close the tabs you opened.
