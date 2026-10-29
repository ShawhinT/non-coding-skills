# Sales Navigator: working with a saved lead list

Getting the leads out of a saved list and turning rows into structured
records, and building or trimming a list in the first place. Sales
Navigator's list view is noticeably less reliable than its search — most of
what follows exists because the UI reports things that aren't true. Plumbing
(browser, API auth, encoding) is in `api-access.md`.

## A pasted URL is a view, not a scope decision

A Sales Nav link usually carries `page=N`, a `sortOrder`, and often a
`spotlight=` (recently posted, changed jobs). Those describe what was on
screen when the link was copied, not which leads to take. Strip `spotlight`
and `page` before extracting, take the whole list, and if the tracker is
empty and the link pointed at a subset, confirm scope before seeding — the
cheap question beats stranding the rest of a validated list.

## Confirm the real count first

The header's "Total results" can show roughly double the real list (it has
read 92 on a 34-lead list and 243 on a 120-lead list), and the pager's page
count drifts between renders. Computing a page count from either walks you
off the end into empty pages. Get the real number from the list API's
`paging.total` (`api-access.md`, list-contents call) — one call, and it also
confirms no spotlight is applied (`spotlightParam:(selectedType:ALL)`) when a
spotlight tab's count coincidentally matches what you extracted.

## Extracting

**Paginate by clicking the pager, not by URL.** A `?page=N` deep link renders
an empty list ("No leads in this list") regardless of what the list holds.
Click the pager buttons (`aria-label="Page 2"`), and stop when the pager stops
offering a next page.

**Allow 8–10s per page.** At 4–5s the table is half-rendered and rows are
silently missing — there is no error, just a short list.

**One settled pass, not repeated passes.** Re-renders serve slightly different
row sets, so unioning several passes inflates the result past the list's real
size while still missing people. Take one settled pass. To reach names the pass
didn't cover (page boundaries drift), flip `sortOrder` and take one settled
pass of that — cheaper and correct. The same flip surfaces a row you need to
act on that the current order keeps at the bottom of the page.

**Read rows from the DOM.** Per `<tr>`: the lead link is
`a[href*="/sales/lead/"]`, the company link (when there is one) is
`a[href*="/sales/company/"]`, and the numeric company id is in that href.
Strip `.a11y-text` before reading the row text, or names come back
triplicated ("Select X X X Second-degree connection…").

## Parsing a row

After stripping, a row reads `Name · 2nd · N List · Title Company Location`.

- **Name** is everything before ` 2nd `.
- **Company** comes from the company link's text, not from parsing — then
  split title from location around it. Use `lastIndexOf(company)`, not
  `indexOf`: the company name often appears inside the title as well
  ("Vice President, Customer Success at [Company] · [Company] · Austin"), and
  `indexOf` truncates the title mid-phrase.
- **`(+N)` after a company** means concurrent positions — strip it from the
  column value, keep the fact in the row's Context. The named company may not
  be the one they actually run, which matters for any company-level
  criterion.
- **`Add Account` in place of a company** means no company record. Leave
  size blank. Blank is *unresolved*, not small — an owner with no linked
  company page can be running several venues or locations, and the title
  text alone can't tell you.

Bulk selection in the list view should match rows by name text, never by
position: the row order is not stable between renders.

## Public profile URLs

The tracker's LinkedIn column defaults to the public `/in/` URL (the rule and
its one exception live in `../campaign/tracker-setup.md`). The list view
doesn't expose it, but the profile API does
(`api-access.md`, public-URL call): loop the deduped lead ids with ~1s spacing
and store `flagshipProfileUrl`. Thirty-odd leads resolve in about half a
minute. Rows already holding an `/in/ACoAA…` member id (followers, ad-hoc
adds) resolve through `GET /voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=<ACoAA id>`
→ `publicIdentifier`. A loop of ~90 outruns the extension's 45s call limit
but keeps running in the page — cache results on `window`, then poll.

## Writing to a list

Creating a list and filling it goes through the API; the UI fights automation
badly enough that it is not the cheaper path.

- **Create:** `POST /sales-api/salesApiLists` with
  `{name, listType:"LEAD", role:"OWNER", description}`. The response carries
  the new list id.
- **Rename or re-describe:** `POST /sales-api/salesApiLists/<listId>` with
  `{patch:{$set:{name, description}}}` → 204. (A real `PATCH` verb is a 400,
  and an `x-http-method-override` header is a 500 — it is a POST carrying a
  patch body.)
- **Add leads:** `POST /sales-api/salesApiLeads?action=bulkSaveByMembers` with
  `{entities:[...], lists:["<listId>"]}`.
- **Remove leads:** `POST /sales-api/salesApiListEntities?action=bulkDeleteFromLists`
  with `{entities:[...], lists:["<listId>"], doUnsaveEntities:false}`. The
  `false` keeps the people in My Saved Leads and removes them only from this
  list — the reversible choice, and the one to default to.

Entities are `urn:li:fs_salesProfile:(<leadId>,NAME_SEARCH,<token>)`. The
third component is a search-context token and **is not validated** — a
placeholder works — so a lead id alone is enough to save or remove someone,
and ids from an old extract stay usable. Batch 14-16 per call, ~1s apart, and
read `entityCount` off the list afterwards to confirm the count landed.

**Don't build a list through the create dialog.** Its fields are React
controlled inputs: a programmatic value assignment updates the DOM but not the
component state, so the button stays disabled or the *stale* value is what
gets submitted, and keystrokes are dropped once a field sits at its
`maxLength` (75 for name, 350 for description). Both failure modes produce a
list that looks right on screen and is wrong in the POST body. Create through
the API and the problem doesn't arise; if a dialog is unavoidable, type into
empty fields only and verify against the request that actually went out.

## Handing off

Loading rows into the Notion tracker is `../campaign/tracker-setup.md`
("Seeding from a lead list"). Validating the size band is `headcount.md`.
Sending connection requests to the list is `connecting.md`. Building the
search that feeds a list is `search.md`.
