# Company Size Ranges

Standard ranges used for ABA outreach enrichment. **Fine low-end buckets matter:** the make-or-break distinction is usually *solo/micro (no team to train)* vs *real team (30+)*, and most ICP bands sit in the 30–500 zone — a coarse `1-50` bucket hides exactly the line you're filtering on.

| Range | Label |
|-------|-------|
| 1–10 | `1-10` |
| 11–30 | `11-30` |
| 31–50 | `31-50` |
| 51–200 | `51-200` |
| 201–500 | `201-500` |
| 501–1,000 | `501-1000` |
| 1,001–5,000 | `1001-5000` |
| 5,000+ | `5000+` |

The band that counts is campaign-specific (lock it at kickoff — e.g. ABA founders ≈ 10–1,000, sweet spot 50–200). Carry the bucket plus a confidence level so low-confidence guesses can be re-checked rather than filtered on blindly.

## Edge Cases

- **Freelance / self-employed / solo consultant** → `1-10` (usually a no-team disqualification, not just a size)
- **Fractional exec (e.g. "Fractional CFO at ClientCo")** → size their *own* practice, not the client — almost always `1-10`. See coherence validation in `company-size.md`.
- **Founder/co-founder of a startup with no listed headcount** → search the company name + "employees" or "team size"; if truly unfindable, mark `Unknown` (low confidence) and resolve in the browser — do NOT default to a mid bucket
- **Subsidiary** → use the parent company's headcount (e.g., Mailgun is part of Sinch; use Sinch's count)
- **Non-profit** → treat the same as any company; use total staff count
- **Government agency** → use total agency headcount (e.g., NJ Transit ~12,000 → `10000+`)
- **University** → use total staff/faculty count
- **Unknown / profile hidden** → use `Unknown`
