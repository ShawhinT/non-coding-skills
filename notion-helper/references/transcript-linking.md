# Linking Meet transcripts to call pages

A batch-style page-freshness workflow that keeps dated pages current, the way `crm` keeps the
pipeline current. Run on-demand today ("link the recent transcripts"); written to be
**idempotent** so it can later run unattended on a schedule.

Google Meet auto-saves each call's transcript to Drive. This workflow attaches the transcript to
its matching ABA Calls (sales) or ABA Trainings (delivery) page, so the link lives on the page
and anything that reads the page later — `meeting-prep`, the daily briefing — picks it up
for free.

The *find* isn't this skill's job: it lives in `google-drive-helper` ("Find the transcript for a
call"). This workflow owns the **match + Notion write** — don't restate the Drive query here,
call it.

## Two homes for a transcript

Drive is not the only place a transcript lands, and that shapes what "done" means for a page:

- **Meet calls** → Google auto-saves a Doc to Drive; this workflow links it onto the page.
- **Everything else** (Zoom, phone, in-person) → Shaw records it himself with **Notion's built-in
  transcription tool**, which lives on the page as a `<meeting-notes>` block.

So a page carrying a `<meeting-notes>` block is already captured and needs nothing from this
workflow. Treating that block as "missing a transcript" produces a nagging false positive that
recurs on every run — the call is on the page, just not as a Drive link. Skip those pages the same
way you'd skip one that already has a `docs.google.com` URL.

For each call page that still needs a transcript (a single named call, or — for a batch run —
recent ABA Calls / ABA Trainings pages with neither a `docs.google.com` link nor a
`<meeting-notes>` block):

1. **Derive the key** — person/company name from the page title, date from the page's `Date`
   property.
2. **Find the transcript** via `google-drive-helper`. If it returns more than one for that day,
   disambiguate with the matching Google Calendar event's start time.
3. **Link it** — append a `## Transcript` line to the page body with the transcript's Drive
   `viewUrl` as a **plain external Markdown link**
   (`[Transcript](https://docs.google.com/document/d/...)`), *not* `<mention>` (that syntax
   is for internal Notion pages; a Google Doc isn't one). Use the `update_content`
   search-and-replace pattern from SKILL.md → "Linking pages on an existing task".
4. **Stay idempotent** — skip any page already carrying either form of transcript. This is what
   makes a future scheduled run safe to repeat.
5. **Report** the pages linked, and surface any transcript with no confident page match instead of
   guessing.

## Reading an empty result

An empty Drive search is ambiguous, and the right report depends on which case it is. Check the
page before writing it up as a miss:

- **Page icon is ❌** (no-show) — nothing was said, so there's nothing to link. Meet still emits a
  ~1 KB stub for these; don't link it. Not a problem, don't flag it.
- **Page body shows a non-Meet link** (Zoom, a dial-in) — no Drive transcript will ever exist.
  Permanently absent, not pending. If it also has no `<meeting-notes>` block, that's worth a
  mention so Shaw can add one; otherwise it's done.
- **A Meet call, held, and still nothing** — this is the real miss. Recording or transcription
  probably wasn't on.

When several pages come back empty in the same run, check whether transcripts are landing
*anywhere* recently before reporting N individual misses. A change in the plumbing is one story,
and writing it up as four unrelated absences buries the actual cause.

Only forward-looking calls have transcripts — transcription started May 2026, so pages before
that stay notes-only.
