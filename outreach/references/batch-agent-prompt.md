# Batch Agent Prompt Template

Use this prompt for each parallel Haiku agent in Phase 1 bulk enrichment. Replace `[CONTACT LIST]` with the 10 contacts for that batch.

---

```
For each of the 10 contacts below, find their current employer and estimate
the company's employee count. Return results as CSV rows.

Size ranges to use (pick exactly one per contact):
- 1-50
- 51-200
- 200-1000
- 1000-5000
- 5000-10000
- 10000+

**Title hint parsing (do this first — saves unnecessary searches):**
If the contact's title contains the company name, use it directly:
- "@ CompanyName" → employer is CompanyName
- "at CompanyName" → employer is CompanyName
- "Director at Accenture Strategy" → employer is Accenture
- "Data Science Manager at Toyota Financial Services" → employer is Toyota Financial Services

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
Person Name,Company Name,10000+
```
```

---

## Notes on Prompt Effectiveness

- The "Return ONLY a CSV block" instruction is critical — without it, agents add lengthy explanations that make aggregation harder
- Including the linkedin_url in the contact list helps agents find the right person when names are common
- Batches of exactly 10 keep token usage predictable (~55-65k tokens per agent)
- Agents reliably handle contacts where the company is in the title; failures mostly come from "Director, Unknown" type entries with no location or title hints
