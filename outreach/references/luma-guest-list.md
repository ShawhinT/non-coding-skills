# Luma Guest List

Pulling the authoritative registration list for a Luma event — the "who actually registered" source of truth for an event-promo sync. The reconcile-and-advance logic lives in `outreach-sync.md`; this file is just the Luma mechanics, which are brittle and platform-specific (isolated here so a UI change is a one-file fix).

## Fastest, most reliable: export the CSV

The Guests tab has an **Export** action that downloads a complete CSV — one row per registrant with `name, first_name, last_name, email, created_at, approval_status, utm_source, has_joined_event`, and more.

**Don't trust `has_joined_event`.** It is wrong in both directions — for the July 2026 event it missed 32 registrants who demonstrably attended and flagged 18 who never appeared in the Zoom log. For actual attendance, reconcile against the Zoom participant export per `event-attendance-reconciliation.md`. `utm_source` has its own limit: the tag travels when someone forwards the link, so it attributes the *click*, not the relationship. This is the **authoritative, complete** source and the preferred way to reconcile: it carries every registrant (no pagination cap), gives you emails for exact matching, and the `utm_source` column attributes each registration to a channel for free. When Shaw can drop the export in, use it — reconcile by matching the tracker's emails against the CSV (exact, unambiguous), falling back to name-token matching only for rows without an email.

Two failure modes of the in-browser methods that the CSV avoids — and why an in-browser negative is never proof someone didn't register:
- **The DOM list caps at ~50 rows.** It renders only the ~50 most-recent approved guests and does not load more on scroll (page height stops growing; the admin API 401s from the page context because auth lives on a different domain). Fine for a spot-check of recent sign-ups, useless for a full reconcile.
- **The search box silently misses registrants.** Searching a name — or even the exact email — of someone genuinely registered can return zero results (confirmed 2026-07-20: a registrant present in the CSV returned nothing for both name and email searches). A search miss is inconclusive, not a "no".

Use the DOM/search approach below only as a fallback when no export is available, and treat its negatives as inconclusive.

## Get to the Going-only guest list

*Fallback only — prefer the CSV export above; use this when no export is available.*

1. Open the public event page (`luma.com/<slug>`) while signed in as host. It shows a **Manage** button ("You have manage access for this event").
2. Click Manage → it opens the host view at `luma.com/event/manage/<evt-id>/…`. Grab the `evt-…` id from the URL.
3. Go to `luma.com/event/manage/<evt-id>/guests?fs=approved`. The **`?fs=approved`** filter is essential: it restricts to **Going** registrants. The default (unfiltered) guests view interleaves a large **Invited** pool — people invited via Luma who have *not* registered — so reading it makes invited-not-registered people look registered. Filter first, always.

The "Going N" chip shows the true registrant count; use it to know when you've loaded everyone.

## Harvest the list (it's virtualized)

The guest list renders only ~10–15 rows at a time and recycles them on scroll, and the accessibility tree is huge and duplicated — so read `innerText`, not the a11y tree, and accumulate across scrolls rather than reading once.

Reliable approach (via the Chrome `javascript_tool`):
- Find the scroll container (the tallest element with `overflow-y: auto/scroll` whose `scrollHeight > clientHeight`) and scroll *it*, not the window.
- After each small scroll step, parse `document.body.innerText`, pair each line matching an email regex with the preceding non-email line as the name, and store `email → name` in a `Map` (dedupes automatically).
- Stop when the Map size stabilizes across several steps, or matches the "Going N" chip.
- Keep each scroll+harvest step small. A long loop with many `setTimeout` waits in a single call can exceed the tool's ~45s execution limit and time out — do a few steps per call, accumulating on a `window.__…` object across calls, rather than one giant loop. (Also remember to `await` the async IIFE, or the tool returns `{}`.)

Output `name | email` pairs. The host's own row appears in the list — exclude it.

## Match to the tracker

Match guests to tracker rows by name tokens (first + last), not exact strings — display names vary ("Will" vs "William", honorific prefixes like "Dr.", single-name handles). Act only on rows **not already at the Registered status**, then hand back to the sync loop for advancing status + predrafting the share-ask.
