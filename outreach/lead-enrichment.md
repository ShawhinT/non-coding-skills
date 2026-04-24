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
