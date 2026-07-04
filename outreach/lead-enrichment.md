# Lead Enrichment

Use this when the pipeline calls for adding fields to an existing list — most commonly `company` and `company_size`, but the pattern generalizes. Follows the pipeline design principles in SKILL.md: free → cheap → expensive → ask.

## Company size: decision tree

```
How many contacts need enrichment?
│
├── 1–9 contacts → Chrome profile lookup (most accurate)
│   └── See references/chrome-profile-lookup.md
│
└── 10+ contacts → Two-phase approach
    ├── Phase 1: Parallel Haiku agents with WebSearch (~87% accuracy)
    │   └── See references/bulk-enrichment-playbook.md
    └── Phase 2: Chrome cleanup pass for remaining Unknowns
        └── See references/chrome-profile-lookup.md
```

**Shortcut:** If a contact's title already embeds the company ("@ Mavenir", "at Affirm", "Director at Accenture"), skip the profile lookup and go directly to a size search. Deduplicate by company before searching — if 5 people work at Toyota, look up Toyota's size once.

## Resolve fully before filtering

If a size band (or any field-based filter) comes next, **drive "unknown" to zero before cutting anyone on that field.** Run Phase 1 (web search) then Phase 2 (Chrome cleanup) on every remaining unknown — do not skip Chrome by re-running web search. A missing value is *unknown*, not *out of band*; keep unknowns in the pool until real data disqualifies them. Only the clearly-out-of-band (obvious solo, obvious mega-corp, visible in the headline) may be dropped before enrichment.

## Coherence validation (own/led company vs. employer/client)

The size you attach must belong to the company the person **owns or leads** — not an employer they're staff at, and not a client they serve. This is a common, silent failure. Check each enriched row:

- **Pure employee** — "GTM @ Stripe", "Engineer at BigCo", "Director, Sales at X" with no ownership signal → the big company is *not theirs*; their decision-making authority is nil. Cut (unless the campaign accepts budget-authority C-suite — then keep CFO/COO/CEO-type roles).
- **Fractional / advisory / consultant** — "CFO at ClientCo | Owner at MyAdvisory" → their led company is the (often solo) advisory practice, NOT ClientCo. The client's headcount does not count.
- **Inflated/garbled web-search size** — verify the number is for the right entity; a Chrome read of the actual current role resolves disputes.

For lists big enough to automate, a parallel Workflow (structured-output agents that read the lead file by index and return `{led_company, led_role, led_company_size, is_decision_maker_with_team, coherence_note}`) does this well. Surface the judgment calls (hired C-suite vs founder, disputed facts) to Shaw; verify disputed ones via Chrome.

## Output format

```
name, title, location, linkedin_url, company, company_size
```

Size range definitions → `references/company-size-ranges.md`
Bulk agent prompt template → `references/batch-agent-prompt.md`

## Key facts

- Chrome reads current employer accurately ~99% of the time
- WebSearch alone misses ~13% (common names, private profiles, stale data)
- Haiku model is sufficient for WebSearch research — no need for Sonnet on bulk jobs
- Always verify Chrome is connected (`tabs_context_mcp`) before a Chrome pass

## Other enrichments

The same pattern — extract → web search → Chrome → ask — applies to any field:

- **Industry / domain:** usually extractable from company name + web search; Chrome only for the long tail
- **Role verification (is this still their title?):** Chrome is the only reliable source; batch these together
- **Mutual connections / warm-intro paths:** Chrome-only, expensive — reserve for the final short list

For anything not covered here, follow the fractal pattern: dedupe the enrichment targets, try the cheap path first, escalate as needed, checkpoint with Shaw before expensive passes.
