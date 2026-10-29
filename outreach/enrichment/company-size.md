# Company Size Enrichment

Adding `company` and `company_size` to a lead list — the most common enrichment, and the pattern every other enrichment (industry, role verification, warm-intro paths) follows: **extract → web search → browser → ask**, cheapest first, on a deduplicated set of targets. Buckets are defined in `size-ranges.md`; use those labels everywhere, including in agent prompts.

## Decision tree

```
How many contacts need enrichment?
│
├── 1–9  → browser profile lookup, one at a time (see "Profile lookup")
│
└── 10+  → two phases
    ├── Phase 1: parallel web-search agents (see "Bulk pass")
    └── Phase 2: browser cleanup of every remaining Unknown
```

**Extract before searching.** A title that embeds the company (`@ [Company]`, `at [Company]`, `Director at [Company]`, `- CompanyName` at the end) skips the person lookup entirely — go straight to a size lookup. **Dedupe by company** before any lookup: five people at [Company] is one [Company] lookup.

## Resolve fully before filtering

When a size band comes next, drive `Unknown` to zero before cutting anyone on size: web-search pass, then a browser cleanup of every remaining unknown. Don't substitute a second web pass for the browser pass. A missing value is *unknown*, not *out of band* — only the clearly-out-of-band (obvious solo, obvious mega-corp, visible in the headline) may be dropped before enrichment.

**Verify a criterion against the source that defines it.** If a platform filter applied the criterion (a Sales Nav headcount band), re-check it *in that platform* — see `../sales-navigator/headcount.md`. Aggregators measure different populations on different refresh cycles, so a disagreement means the sources differ, not that the filter failed.

## Coherence: size the company they own or lead

The size attached to a row must belong to the company the person **owns or leads** — not an employer they're staff at, not a client they serve. This fails silently; check every enriched row:

- **Pure employee** — "GTM @ Stripe", "Director, Sales at X" with no ownership signal → the big company isn't theirs. Cut unless the campaign accepts budget-authority C-suite.
- **Fractional / advisory / consultant** — "CFO at ClientCo | Owner at MyAdvisory" → their led company is the advisory practice, almost always `1-10`. The client's headcount doesn't count.
- **Garbled or inflated web-search sizes** — confirm the number is for the right entity; a browser read of the actual current role settles it.

For large lists, a Workflow of structured-output agents that read the lead file by index and return `{led_company, led_role, led_company_size, is_decision_maker_with_team, coherence_note}` does this well. Surface judgment calls (hired C-suite vs founder, disputed facts) to Shaw; verify disputed ones in the browser.

## Bulk pass (10+ contacts)

- Split into **batches of 10** and launch all batches in one message as parallel Agent calls on the cheapest model tier — web research doesn't need more.
- Each agent gets: its 10 contacts (name, title, location, LinkedIn URL), the title-hint rule above, the bucket labels from `size-ranges.md`, and a strict CSV-only output instruction. Template: `batch-agent-prompt.md`.
- Aggregate CSV blocks in original contact order into `raw/<campaign>_leads_enriched.csv` with columns `name,title,location,linkedin_url,company,company_size`. Queue every `Unknown` for cleanup.

Web search alone lands roughly nine in ten; the misses are common names, hidden employers, and recent job changes. The browser cleanup closes nearly all of the rest.

## Profile lookup (1–9 contacts, or the cleanup pass)

One tab, sequentially — the browser policy in SKILL.md applies. For each profile, navigate to `linkedin.com/in/<slug>` and read the page text. The employer sits in the first few lines:

```
[Full Name]
[Title]
[Company Name] · [School or other org]
[Location]
```

Then search `"[Company] number of employees"` and map to a bucket. Edge cases: no employer shown → profile is private, between jobs, or freelance — mark `Unknown` or `Self-Employed` (`1-10`); a login wall means Shaw isn't signed in — stop and tell him; a redirected slug — confirm the landing URL is the person you meant. URL and identity gotchas are in SKILL.md under "LinkedIn scraping gotchas."
