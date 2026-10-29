# Sales Navigator: validating the headcount band

Checking a saved list against the campaign's company-size band. Plumbing is in
`api-access.md`; getting the rows out is `lead-lists.md`.

## The band

The campaign's filter set is an external record — its own page in the campaign
hub (e.g. "Sales Nav Filters"). Read the band off that page rather than
hardcoding one; it changes per campaign.

A saved list built from a Sales Nav filter set is usually correct on the
measure the filter uses (member count), and the full pass below is cheap enough
— a few minutes for a 120-lead list — that it's the default; there is no need
to spot-check first. When it comes back with zero out-of-band leads, that's the
filter having held, not the pass having failed.

**That trust does not extend to a filtered search.** Search-side company
filters — headcount, company type — leak badly enough to return companies
orders of magnitude outside the band, and public companies under a Privately
Held filter, with no concurrent-position artifact to explain it. So on a search
the validation pass is load-bearing rather than confirmatory: resolve every
company against the API before any company-level criterion is applied, and
treat a clean result as evidence you checked, not as the filter having worked.

## Two headcounts — a lead is in band if either one is

LinkedIn carries two headcounts per company, and they disagree often:

- **Declared size** — the range the company set on its page (`11-50`,
  `51-200`, …). Self-reported, coarse, often stale; a 143-member company can
  sit at `2-10`, and a 64-member holding company at `1001-5000`.
- **Associated members** — the count of LinkedIn profiles listing the company
  as current employer. Continuous, moves monthly; undercounts industries whose
  staff aren't on LinkedIn.

The Sales Nav headcount filter tracks **associated members**, so a filtered
list is consistent with that number and drifts to about half in band when
judged on the declared range alone. Neither is the truth — they are two proxies
for the same thing — so the standing rule is: **a lead is in band if either
measure is; only leads out of band on both get parked.** Don't ask which
measure to use. Report both numbers per lead so the disagreements stay visible;
a lead that passes on one and fails on the other is expected, not a reason to
re-check.

## Reading a company's headcount

The company API (`api-access.md`) returns both numbers in one call —
`employeeCountRange` is the declared size and `employeeCount` the member
count, verified identical to the public `/company/<id>/about/` page. Loop over
the deduped company ids as a background loop. The public About page (poll for
the `Company size` text) remains the fallback if the endpoint ever changes
shape.

- **Absence is not zero and not failure.** A record can carry a declared size
  with no member count, or neither. Leave no-data leads unresolved rather than
  cutting them — a no-data account passing a headcount filter is the likelier
  leak than a wrong number, since there was nothing for the filter to test.
- Leads whose row shows `Add Account` have no company at all; count them as
  no-data.

## The pass

Cheapest work first, so the expensive step runs on the smallest set:

1. **Free filters** — cut on role/title from the extract alone. Non-buyers (a
   conference director, a search-firm practice lead, a founder-in-residence at
   a VC) are cuttable at zero cost; validating their companies is wasted work.
   Cut only what the headline makes unmistakable — anything ambiguous stays.
2. **Dedupe by company** — one lookup per company, not per lead.
3. **Check the cache** — company → declared size + member count → date checked,
   kept across campaigns. Segments of one campaign and successive campaigns
   overlap heavily.
4. **Validate** the remainder via the company API loop.
5. **Split** into in-band (either measure) / out-of-band (both measures) /
   no-data, and write both numbers back to the cache. Report both measures per
   lead so Shaw can see where they disagree.

## Parking out-of-band leads

Out-of-band leads go to Shaw's parked list, **Disqualified** (`Add to another
list`, then `Remove`), rather than a bare `Remove` — the parked list is the
exclusion memory, since removed leads reappear the next time the saved search
runs and get re-validated from scratch. The `Remove` dialog's default, "remove
from this list only", keeps the lead saved and in the parked list; the other
option unsaves them everywhere. In the `Add to another list` dropdown the list
names are leaf `<span>`s, not buttons — click the last span whose text is the
list name, and confirm by the count in parentheses ticking up.

## Cross-source disagreement

If a filter was applied by Sales Nav, re-check it *in Sales Nav* — not in an
aggregator. Crunchbase, ZoomInfo and PitchBook measure different populations on
different refresh cycles, so a disagreement tells you the sources differ, not
that the filter failed; and their coarse buckets (`101-250`) can't adjudicate a
boundary at 200 anyway. The generic enrichment pattern for lists that didn't
come from Sales Nav is `../enrichment/company-size.md`.
