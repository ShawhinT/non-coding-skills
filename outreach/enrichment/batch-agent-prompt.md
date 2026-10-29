# Batch Agent Prompt Template

One prompt per parallel web-search agent in the bulk pass (`company-size.md`). Replace `[CONTACT LIST]` with that batch's 10 contacts. The bucket list below mirrors `size-ranges.md` — keep them in sync.

---

```
For each of the 10 contacts below, find their current employer and estimate
the company's employee count. Return results as CSV rows.

Size ranges to use (pick exactly one per contact):
- 1-10
- 11-30
- 31-50
- 51-200
- 201-500
- 501-1000
- 1001-5000
- 5000+
- Unknown (only if truly unfindable — never guess a mid bucket)

Freelance / self-employed / solo consultant → 1-10.
Fractional exec ("Fractional CFO at ClientCo") → size their own practice, not the client.
Subsidiary → use the parent's headcount.

**Title hint parsing (do this first — saves unnecessary searches):**
If the contact's title contains the company name, use it directly:
- "@ CompanyName" → employer is CompanyName
- "at CompanyName" → employer is CompanyName
- "Director at [Company]" → employer is [Company]
- "Data Science Manager at [Company]" → employer is [Company]

**For contacts without a title hint:**
Search "[name] [title] [location] LinkedIn employer" or
"[name] [partial title] company" to find their current employer.

Contacts:
[CONTACT LIST FORMAT:]
1. [Name] | [Title] | [Location] | [LinkedIn URL]
2. ...

Return ONLY a CSV block with no extra text, explanation, or commentary:
```csv
name,company,company_size
Person Name,Company Name,51-200
```
```

---

## Notes

- "Return ONLY a CSV block" matters — without it, agents append explanations that make aggregation harder.
- The LinkedIn URL in the contact list disambiguates common names.
- Batches of exactly 10 keep per-agent cost predictable. Failures cluster on entries with no location and no title hint ("Director, Unknown").
