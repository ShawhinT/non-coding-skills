# Sales Navigator: sending connection requests

Working a saved lead list into blank connection requests. Plumbing is in
`api-access.md`. This is an action under Shaw's name on his account — it runs
only on his explicit instruction for a specific list, and the pace is his call
too; say the account-risk piece once if it's worth saying, then do what he
asked.

## The fast path is the list row, not the profile

Every row in a saved list has an overflow at the far right whose menu holds
**Connect** directly. That keeps the whole batch on one page — no navigation,
~4s per lead — and its invite modal is a plain in-page dialog that scripts can
see. Going lead-by-lead through public profiles works, but is several times
slower and its modal is invisible to the DOM (below). Use the list.

Widen the viewport if the overflow column isn't rendered (`resize_window`
to ~1600 wide); at narrow widths the table drops its trailing columns.

## Selectors

The overflow is discoverable only by class — it has no text and no
`aria-label`, so a probe that filters on either will report that no per-row
action exists. Name it explicitly:

| Thing | Selector |
|---|---|
| The row's `···` trigger | `tr button.artdeco-dropdown__trigger` (last cell) |
| The Connect item, once the menu is open | the `.artdeco-dropdown__item` in `.artdeco-dropdown__content-inner` whose text is `Connect` — see below, matching it is not obvious. Absent has three meanings, also below |
| The invite dialog | `[role="dialog"]` whose text contains "Send invitation" |
| Send | the dialog's button with text `Send Invitation`; leave the optional message empty for a blank request |

**The menu item's text is not `Connect`.** Every `.artdeco-dropdown__item`
carries hidden a11y text, so the item's `textContent` reads
`"Connect Send connection request to [Person]."`. An exact `=== 'Connect'`
test therefore matches nothing, and the whole run logs as "no Connect" for
every lead — which reads exactly like a list where everyone is already
pending. Match the leaf node and climb back to the item:

```js
const leaf = [...document.querySelectorAll('.artdeco-dropdown__content-inner *')]
  .find(e => e.children.length === 0 && e.textContent.trim() === 'Connect' && e.offsetParent);
const connect = leaf && leaf.closest('.artdeco-dropdown__item');
```

(A class named `.list-detail__connect-option` was documented here until 9/7/26
and no longer exists in the page — a selector on it returns an empty list.)

**Query the Connect item document-wide, not inside the row.** The open menu
renders inside the `<tr>` on some pages and portaled to the document root on
others. A row-scoped query silently reports "no Connect" for every lead on a
page where it's portaled. Only one menu is open at a time, so the
document-wide query above, filtered on `offsetParent`, is unambiguous.

**Open the trigger with a full pointer sequence.** A bare `.click()` opens
the container with zero children. Dispatch `pointerdown`, `mousedown`,
`pointerup`, `mouseup`, `click` at the element's centre; the same helper works
for the Connect item and the Send button.

## Pacing the run as a loop

Run it as a background loop on `window` (see `api-access.md`, "Long loops"):
per row, open → Connect → Send → next, logging a result per name.

**Poll for each element; never sleep a fixed interval.** The menu populates
asynchronously, and at a flat 1.5s the container is present with zero children
— indistinguishable from the degradation failure below, and it logs as a skip.
Poll at ~300ms up to ~3s for the Connect item, again for the dialog, and again
for the dialog to close after Send. Polling took 200 leads at ~2s each with no
misses; the same loop on fixed waits lost its first rows.

Two more things make the loop fail quietly if not handled:

- **The menu degrades after ~15–20 open/close cycles** — the trigger reports
  `aria-expanded="true"` but the container renders empty, and everything
  after that logs as "no Connect". It happened at 1.2s and at 4–8s spacing
  alike, so it's page state, not speed. Reload every 15–20 rows.
- **Rows at the bottom of a page may not open a menu at all**
  (virtualization). Flip `sortOrder` so they land at the top of page 1, or
  handle the stragglers on a fresh load.

Stop the loop if the dialog text mentions a weekly invitation limit.

## Verify against the API, never the click log

The loop's log records what it *tried*; it will claim sends that didn't land
and skips that were selector bugs. The truth is the list-contents call
(`api-access.md`) — one request for the whole list, before and after. It also
shows invitations that were already out before the run started, which the log
has no way to know.

**Read `pendingInvitation` together with `degree`, never alone.** A false
`pendingInvitation` has two opposite meanings, and the field goes false the
moment someone *accepts*:

| `degree` | `pendingInvitation` | What it means |
|---|---|---|
| 2 | true | Invite is out, waiting. |
| 1 | false | **Accepted.** The invite landed — count it as a success. |
| 2 | false | Genuinely not sent. This is the only real failure. |

On the 9/7/26 seg-2 run, five people accepted within minutes of the send, so
the bare pending count read as 191/200 and the first failure list named nine
people when only four had actually failed. Diff on the pair, and report
accepts separately from misses.

## An absent Connect item has three meanings

Only the first two are "skip":

1. **Already pending** — an invite is out. Confirm against the API, not the menu.
2. **Already connected** (`degree` 1) — nothing to send.
3. **LinkedIn does not offer Connect for this person at all.** The row is
   `degree` 2 with no pending invite, and the menu simply has no Connect item —
   a follow-first or restricted profile. Retrying the row is futile; it fails
   identically every pass. Four of 200 landed here on 9/7/26.

Case 3 is not a skip, it is an unreached lead. Try the public-profile fallback
below, and when that also fails, **record it on the tracker row** rather than
letting it vanish into a log — a line in the row's Context (`⚠️ Connection
request could not be sent — LinkedIn offers no Connect option on this profile
(M/D).`) is what keeps it from being silently counted as sent. Report the count
to Shaw with the names.

## Public-profile fallback

For a lead whose row won't cooperate, the public profile (`lead-lists.md`,
public-URL harvest) works but costs more per person:

- Two layouts. Some profiles show **Connect** as the primary pill; follow-first
  profiles show **Follow** and put Connect under the `···` next to it.
- The "Add a note?" modal there renders outside the page DOM — invisible to
  JS and to the accessibility tree — so its buttons take coordinate clicks
  after a screenshot. "Send without a note" for a blank request.
- Confirm by re-reading the profile's top card for `Pending`.

## Afterwards

Log the batch on the tracker per SKILL.md ("Logging a batch send") — the send
date, the campaign's ask name in Notes, and a uniform `Next Contact` for
everyone who got the same ask.
