# Sales Navigator: browser and API access

Shared plumbing for everything in this folder. The task files (`lead-lists.md`,
`headcount.md`, `connecting.md`) assume this is loaded.

## Browser

**Which browser depends on the environment — check before you start.**
"Built-in browser" resolves to different software in each, and only one of
them is signed into LinkedIn:

| Environment | Use | Why |
|---|---|---|
| **Claude Desktop** | the built-in browser | Signed in. Everything below applies as written. |
| **Claude Code** | the **Chrome extension** | Here "built-in" is Playwright, which is *not* signed into LinkedIn — it redirects to `/sales/login` and a DOM read returns an empty list rather than an error. Shaw's session lives in Chrome. Confirmed 9/7/26. |

In Chrome, read the DOM with `javascript_tool` (its reads are current, unlike
screenshots) and keep every call under ~40s — `Runtime.evaluate` times out at
45s. Long work goes in a background loop on `window` that you poll, per "Long
loops" below.

Either way, Sales Navigator work runs in **one tab, sequentially**, and this
overrides the app's preferred-browser default. Read the DOM (`get_page_text`
or a JS read) rather than screenshots, which can lag an action behind — in
either browser a read returns the page title alongside the data, so a
mis-navigation is self-evident rather than silently mislabeled. Concurrent
tabs have tripped LinkedIn's rate limiting; parallelism is for web-search
agents only.

## Same-origin API calls

Sales Navigator's own API is reachable with a same-origin `fetch` from any
Sales Nav page. The cookie jar does the auth; the `JSESSIONID` cookie value is
the `csrf-token` header:

```js
const csrf = (document.cookie.match(/JSESSIONID="?([^";]+)"?/) || [])[1];
fetch(url, { headers: { 'csrf-token': csrf, 'x-restli-protocol-version': '2.0.0' } });
```

**The `decoration` parameter must be percent-encoded — parens and commas
both.** `encodeURIComponent` is not enough: it leaves `(` and `)` untouched,
and the server answers `400` with no message. Write the encoded string
literally:

```
decoration=%28name%2CemployeeCount%2CemployeeCountRange%29
```

Restli complex keys in the *path* (`(profileId:...,authType:undefined,...)`)
stay unencoded — only the query-string decoration is encoded.

## Endpoints

| Need | Call |
|---|---|
| Company headcount, both measures | `GET /sales-api/salesApiCompanies/<companyId>?decoration=%28name%2CemployeeCount%2CemployeeCountRange%29` → `{name, employeeCountRange: "51-200", employeeCount: 181}`. `<companyId>` is the numeric id in a row's `/sales/company/<id>` link. |
| Public `/in/` URL for a lead | `GET /sales-api/salesApiProfiles/(profileId:<leadId>,authType:undefined,authToken:undefined)?decoration=%28entityUrn%2CfullName%2CflagshipProfileUrl%29`. `<leadId>` is the `ACwAA...` token before the comma in a row's `/sales/lead/<id>,NAME_SEARCH,...` link. |
| A saved list's real contents and count | `GET /sales-api/salesApiPeopleSearch?q=peopleSearchQuery&query=<q>&start=0&count=100&decoration=%28entityUrn%2CfullName%2Cdegree%2CpendingInvitation%29` where `<q>` is `(spotlightParam:(selectedType:ALL),doFetchSpotlights:true,doFetchHits:true,doFetchFilters:false,pivotParam:(com.linkedin.sales.search.LeadListPivotRequest:(list:urn%3Ali%3Afs_salesList%3A<listId>,sortCriteria:CREATED_TIME,sortOrder:DESCENDING)),list:(scope:LEAD,includeAll:false,excludeAll:false,includedValues:List((id:<listId>))))`. `paging.total` is the authoritative list size; `pendingInvitation` per element says whether an invite is already out. |

## Search vs saved list — different surface, different plumbing

Everything above assumes a **saved lead list**. A **filtered search** is a
separate surface and none of the list mechanics carry over:

- **Different endpoint.** `salesApiPeopleSearch` answers only for a list pivot;
  against a search it returns a bare `400`. A search is
  `GET /sales-api/salesApiLeadSearch?q=searchQuery&query=<q>&start=0&count=25&decorationId=com.linkedin.sales.deco.desktop.searchv2.LeadSearchResult-14`,
  where `<q>` is the `query` parameter copied straight off the search URL.
  `paging.total` is the real count; page in 25s until a short page comes back.
  Each element carries `fullName`, `geoRegion`, `degree` and
  `currentPositions[]` (`companyName`, `companyUrn`, `title`) — enough to skip
  the DOM entirely.
- **Different DOM.** Search results are list items, not a table, so the
  `<tr>`-per-lead read in `lead-lists.md` silently returns zero rows. Prefer the
  endpoint; when you must scrape, confirm the row container before writing a
  selector.
- **When an endpoint's shape is unknown, let the page tell you.** Hook `fetch`
  and `XMLHttpRequest.prototype.open` to record `salesApi` URLs, then click the
  pager. The app's own request — endpoint, decoration, and encoding — comes back
  exactly as the server expects it. Cheaper than guessing at a decoration.

**Decoration fields are validated, and an unknown one fails the whole call.**
The company endpoint accepts `name`, `employeeCount`, `employeeCountRange`,
`industry` and `description`; `websiteUrl`, `companyType` and `revenueRange` are
not fields and return `400` with no message naming the culprit. A `400` on a
decoration you extended is the new field, not the encoding — drop back to the
known-good set and add one field at a time.

## Long loops

A browser tool call times out around 45s, but a loop started in the page keeps
running. Start it without awaiting, store results on `window`, and poll a
counter — ~1s between calls; ~120 companies take about three minutes. Watch
`window.__done`-style progress rather than re-issuing the loop: re-issuing
while the first is still running doubles the request rate.
