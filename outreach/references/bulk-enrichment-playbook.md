# Bulk Enrichment Playbook

Use this for lists of 10+ contacts that need company name and size added.

## Phase 1: Parallel Haiku Agents (WebSearch)

### Setup
- Split contacts into **batches of 10**
- Launch **all batches in a single message** as parallel Agent tool calls
- Use **model: haiku** — sufficient for research, significantly cheaper than Sonnet

### Per-Agent Instructions
Each agent receives:
1. A list of 10 contacts (name, title, location, linkedin_url)
2. Title-hint parsing instructions
3. The size ranges
4. A strict "CSV only" output instruction

See `batch-agent-prompt.md` for the exact prompt template.

### Title Hint Parsing (tell agents to do this first)
Before searching, scan each contact's title for embedded company names:
- `@ CompanyName` → company = CompanyName
- `at CompanyName` → company = CompanyName
- `- CompanyName` at end of title → company = CompanyName
- `Director at Accenture Strategy` → company = Accenture
- `Data Science Manager at Toyota Financial Services` → company = Toyota Financial Services

If found, skip the profile search and go straight to a size lookup.

### Expected Accuracy
- ~87% success rate from WebSearch alone
- Failures are mostly: common names with multiple LinkedIn profiles, profiles with no public employer, or people who've changed jobs recently

## Phase 2: Chrome Cleanup Pass

After aggregating Phase 1 results, collect all rows where `company_size` is `Unknown`.

For each Unknown:
1. Navigate to their LinkedIn profile in Chrome
2. Read page text to find current employer
3. Search for that employer's size
4. Update the row

See `chrome-profile-lookup.md` for the full Chrome workflow.

Combined accuracy after both phases: ~99%.

## Aggregating Results

After all agents complete:
1. Collect CSV blocks from each agent response
2. Combine in original contact order
3. Write to output file: `outputs/<campaign>_leads_with_company_size.csv`
4. Check for any remaining `Unknown` values → queue for Phase 2

## Output Format

```csv
name,title,location,linkedin_url,company,company_size
```

Do not include `tier` or other columns from the input — keep the output clean and focused on what was enriched.
