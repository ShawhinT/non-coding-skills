# Company Size Ranges

Standard ranges used for ABA outreach enrichment:

| Range | Label |
|-------|-------|
| 1–50 | `1-50` |
| 51–200 | `51-200` |
| 201–1,000 | `200-1000` |
| 1,001–5,000 | `1000-5000` |
| 5,001–10,000 | `5000-10000` |
| 10,001+ | `10000+` |

## Edge Cases

- **Freelance / self-employed / consultant** → `1-50`
- **Founder/co-founder of a startup with no listed headcount** → search the company name + "employees" or "team size"; if truly unfindable, use `1-50`
- **Subsidiary** → use the parent company's headcount (e.g., Mailgun is part of Sinch; use Sinch's count)
- **Non-profit** → treat the same as any company; use total staff count
- **Government agency** → use total agency headcount (e.g., NJ Transit ~12,000 → `10000+`)
- **University** → use total staff/faculty count
- **Unknown / profile hidden** → use `Unknown`
