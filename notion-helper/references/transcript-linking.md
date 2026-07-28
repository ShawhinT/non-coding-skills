# Linking Meet transcripts to call pages

A batch-style page-freshness workflow that keeps dated pages current, the way `crm` keeps the
pipeline current. Run on-demand today ("link the recent transcripts"); written to be
**idempotent** so it can later run unattended on a schedule.

Google Meet auto-saves each call's transcript to Drive. This workflow attaches the transcript to
its matching ABA Calls (sales) or ABA Trainings (delivery) page, so the link lives on the page
and anything that reads the page later — `pre-call-research`, the daily briefing — picks it up
for free.

The *find* isn't this skill's job: it lives in `google-drive-helper` ("Find the transcript for a
call"). This workflow owns the **match + Notion write** — don't restate the Drive query here,
call it.

For each call page that needs a transcript (a single named call, or — for a batch run — recent
ABA Calls / ABA Trainings pages with no `## Transcript` link yet):

1. **Derive the key** — person/company name from the page title, date from the page's `Date`
   property.
2. **Find the transcript** via `google-drive-helper`. If it returns more than one for that day,
   disambiguate with the matching Google Calendar event's start time.
3. **Link it** — append a `## Transcript` line to the page body with the transcript's Drive
   `viewUrl` as a **plain external Markdown link**
   (`[Transcript](https://docs.google.com/document/d/...)`), *not* `<mention-page>` (that syntax
   is for internal Notion pages; a Google Doc isn't one). Use the `update_content`
   search-and-replace pattern from SKILL.md → "Linking pages on an existing task".
4. **Stay idempotent** — skip any page that already has a `## Transcript` link. This is what makes
   a future scheduled run safe to repeat.
5. **Report** the pages linked, and surface any transcript with no confident page match (or any
   page whose transcript isn't in Drive yet) instead of guessing.

Only forward-looking calls have transcripts — transcription started May 2026, so pages before
that stay notes-only.
