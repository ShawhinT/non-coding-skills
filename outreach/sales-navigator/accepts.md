# Sales Navigator: detecting accepted connection requests

Sales Nav-specific. A campaign sourced elsewhere needs its own accept check;
this one reads the saved list.

## The signal

Open the list sorted by **Outreach activity**, descending
(`/sales/lists/people/<listId>?sortCriteria=OUTREACH_ACTIVITY&sortOrder=DESCENDING`),
one tab, in whichever browser `api-access.md` names for this
environment. The sort returns only leads with outreach activity —
the invited set — and each row carries two agreeing signals: the degree badge
(`1st` once connected, `2nd` before) and the activity label (`Invitation
accepted` vs `Invitation sent`). Require both.

Ignore the "X minutes ago" text. It reflects the latest activity of any kind
(a DM you sent updates it too), and rows also carry a "last active" presence
line that a loose match picks up instead. Time isn't needed: the tracker is
the memory.

## Join on the lead ID, not the name

Each row's link holds the lead ID (`/sales/lead/ACwAA…`), and the tracker's
`LinkedIn` field stores the same ID (`../campaign/tracker-setup.md`). Diff on
it. Names carry prefixes, credentials and presence text ("Chef [Person]",
"[Person], Ph.D., PE") that make string matching unreliable. Where a row
holds a public `/in/` URL instead, the join has nothing to match — fall back to
names for that run, then fix the field, because every later sweep hits the same
wall.

## Procedure

1. Read from the top and stop early. Accepting is fresh activity, so
   accepts form one contiguous block above every invitation still sitting
   unanswered: the first `Invitation sent` row below that block ends it,
   and everything past it is wasted reads. A newly sent batch is fresh
   activity too and crowns the list above older accepts, so skip any
   leading run of `Invitation sent`, take the accepted run under it, then
   stop at the next `Invitation sent`. Go by labels and contiguity, not
   timestamps. Per row: lead ID, name, degree, label. (25 rows per page;
   page only if the accepted block reaches the bottom.)
2. Keep rows with `1st` + `Invitation accepted`.
3. Query the tracker for rows already at `Accepted`; anyone from step 2 not
   in that set is new.
4. Set `Status = Accepted` on the new rows and hand off to per-prospect
   scripting for Msg 1. Leave `Last Contact` empty — nothing has been sent.
5. **Set `Next Contact` to the next day.** An accept is an opened door, and
   Msg 1 goes out the day after it lands — so the accept itself schedules the
   DM. This is the one place `Next Contact` gets a date before anything has
   been sent: everywhere else it points at a follow-up to something already
   out, but here it points at the first message. Without it the row carries a
   `Status` and no date, and the CRM sweep (`Next Contact <= today`) never
   surfaces it — the accept goes cold in a view Shaw is not reading.

   **Only for accepts that have not been DM'ed yet.** Once Msg 1 goes out,
   `Next Contact` belongs to the message ladder and is set from the cadence,
   not from this rule — overwriting it with "tomorrow" drags a lead who is on
   M2 back to the top of the sweep. And a blank `Next Contact` on an
   already-DM'ed row is a decision someone made (a polite no, a closed
   ladder); per `notion-helper`, blank is intentional and never backfilled.
   Filter on Notes: `Accepted (M/D).` alone is in scope, anything carrying
   `DM'ed` is not.

Per-row extraction, run in the page:

```js
[...document.querySelectorAll('tr')].filter(r => /Invitation/.test(r.innerText)).map(r => {
  const a = r.querySelector('a[href*="/sales/lead/"]');
  return {
    id: (a?.getAttribute('href') || '').match(/lead\/([^,?]+)/)?.[1],
    name: (a?.innerText || '').split('\n')[0].trim(),
    deg: (r.innerText.match(/\b(1st|2nd|3rd)\b/) || [])[1],
    accepted: /Invitation accepted/.test(r.innerText),
  };
})
```
