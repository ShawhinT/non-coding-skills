# Sales Navigator: sourcing from a search

Building a filtered people search and pulling its results. The search surface
is not the saved-list surface — different endpoint, different DOM, different
failure modes (`api-access.md`, "Search vs saved list"). Plumbing (browser,
API auth, encoding) is in `api-access.md`; this file is the query language.

## A filter the server doesn't recognize is ignored, not rejected

An unknown filter *type* or an unknown value *id* returns HTTP 200 and the
**unfiltered** count. Nothing warns you. A search you believe is scoped to
recent posters can quietly be a search of everyone, and every count and
conclusion downstream inherits that.

So a filter is not applied until you have watched the total move. Build the
query one filter at a time, checking `paging.total` after each, and keep the
before/after numbers — they are also the cheapest sanity check on whether a
filter means what you assumed. (`RECENTLY_POSTED_ON_LINKEDIN` reads as
plausible and is silently nothing; the real type is `POSTED_ON_LINKEDIN`.)

Exclusions fail the same way. `selectionType:EXCLUDED` is not honored on every
type: excluding `SENIORITY_LEVEL` returned the same people the include had, CXOs
and all. Watch the total drop, and spot-check a few results, before trusting a
negated filter.

## Filter vocabulary

Types and values go in `filters:List(...)` as
`(type:NAME,values:List((id:X,selectionType:INCLUDED)))`. Several values in
one `values:List(...)` are OR'd; `selectionType:EXCLUDED` negates.

| Type | Values |
|---|---|
| `RELATIONSHIP` | `F` 1st, `S` 2nd, `O` 3rd+ |
| `COMPANY_HEADCOUNT` | `A` 1-10, `B` 11-50, `C` 51-200, `D` 201-500, `E` 501-1000, `F` 1001-5000, `G` 5001-10000, `H` 10001+ |
| `SENIORITY_LEVEL` | `3` Entry, `4` Senior, `5` Manager, `6` Director, `7` VP, `8` CXO, `9` Partner, `10` Owner |
| `FUNCTION` | LinkedIn's function ids — `8` Engineering, `13` Information Technology, `15` Marketing, `18` Operations, `25` Sales |
| `YEARS_AT_CURRENT_COMPANY` | `1` <1yr, `2` 1-2, `3` 3-5, `4` 6-10, `5` >10 |
| `REGION` | a geo urn id — `103644278` is the United States |
| `POSTED_ON_LINKEDIN` | `RPOL` — posted in the past 30 days |

Treat anything not in this table as unverified until a count moves. The id
sets are LinkedIn's and drift; a value that stops filtering has been retired,
not mistyped.

## Keywords

`keywords:` searches the whole profile — headline, About, every position
description, past roles included. That breadth is the point and also the
risk: a phrase can match a job someone left a decade ago.

- **Quote every phrase.** Unquoted terms are tokenised and OR'd, which
  silently turns a phrase search into a search for any of its words —
  `department of one` returned 13,084 where `"department of one"` returned 59.
- **`OR` between quoted phrases works; wrapping the whole boolean in parens
  does not.** `("a" OR "b")` is accepted by the API but renders "something has
  gone wrong" in the Sales Navigator UI, so a URL built that way can't be
  handed to a human. Drop the outer parens — the count is identical.
- **Omit the `keywords:` key entirely when there is no keyword.** An empty
  value is a 400.
- Encode the value with parens percent-encoded (`%28`/`%29`); the structural
  parens of the query itself stay literal.

## Pulling the results

`salesApiLeadSearch` (`api-access.md`) pages in 25s or 50s. Two limits:

- **Paging stops at `start=2500`** with a bare 400, whatever `paging.total`
  says. A search larger than that is truncated, not sampled — narrow it
  (split by headcount band or region) if the tail matters.
- Each element carries `fullName`, `geoRegion`, `degree` and
  `currentPositions[]`. **`currentPositions` is a list because people hold
  several jobs at once** — see "A sourced row is a position, not a person" in
  `../SKILL.md` before deriving employer, company or headcount from it.

Long pulls belong in a loop started on `window` that you poll, ~650ms between
pages (`api-access.md`, "Long loops").

## Reproducible search URLs

The same query string works as `/sales/search/people?query=<query>`, which
lets a search be reopened in the UI or handed over. Build the URL from the
query *as the API takes it* — encoding it a second time double-escapes the
parens and the page fails to load.

## Handing off

Saving the results into a lead list is `lead-lists.md` ("Writing to a list").
Validating the size band is `headcount.md`. Sending connection requests is
`connecting.md`.
