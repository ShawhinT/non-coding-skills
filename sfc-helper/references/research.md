# Researching client transcripts for content

The freshest, least-generic ideas come from what clients actually said in sessions. Mine the last ~2 weeks.

## Where to look

- **Clients (Nurture)** data source: `[page-id]`. Query it for current clients (Status Active / Nurturing / Expansion).
- Each client's CRM page has a `## Calls` section linking **ABA Calls** (sales/check-in calls) and **ABA Trainings** (delivery sessions). Fetch those with `notion-fetch` and `include_transcript=true`.
- Transcripts are frequently linked **Google Docs**, not inline — read them with the Google Drive `read_file_content` tool using the doc ID. (The Drive read tool and the file Read tool see different filesystems; for very large transcripts, search/slice rather than dumping the whole thing.)

## On-avatar vs off-avatar

Bias toward clients that match the avatar (50–200-person tech/financial-services companies, team engagements): the strongest examples in past runs were a cybersecurity SaaS CEO, a VC firm's CFO/COO, a cyber-analytics ops lead, and an auction-SaaS chairman. Solo professionals or individuals on personal budgets (e.g. a surgeon, a think-tank director) can still yield a *great quantified win* worth using anonymized, but their company shape isn't the ICP — use them for proof, not as the avatar.

## Use subagents — one per client

Spawn the client research in parallel. Template for each subagent:

> You are mining recent client call transcripts for LinkedIn content ideas for Shaw (AI Builder Academy). Read only.
> CLIENT: <name, company, one-line context>. Past two weeks ≈ <dates>.
> Use `notion-fetch` to: (1) open the CRM page <url> and read its `## Calls` section; (2) fetch the linked ABA Calls / ABA Trainings pages dated in the window with `include_transcript=true`; read the Google Doc transcripts via the Drive tool.
> EXTRACT content ideas, not a summary: specific pains in the client's own words (quote), governance/security/adoption struggles, quantified wins, objections, vivid stories.
> RETURN 5–10 candidate LinkedIn angles. For each: a working hook (1 line), audience (Sponsor / Champion), the supporting quote/insight, and post type. ANONYMIZE — no client or individual names.

## Turning research into ideas

Cluster the returned angles, dedupe across clients (the same theme often recurs — that's a signal it's strong), and map each to the barbell. Watch for the gold: a governance struggle (sponsor reach + sets up the Audit), a quantified before/after (champion proof), a recurring pain across multiple clients (high-confidence thesis).
