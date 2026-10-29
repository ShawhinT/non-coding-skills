# Q&A-database posts (cluster mode)

Turning the **💬 Q&A database** (owned by `convo-mining` — load it first for schema and query
mechanics) into short-form posts. Unlike mine-file mode, the input isn't one call's pre-mined
pairs — it's the whole database, and the unit of selection is the **repeat cluster**: the same
question surfacing across different people, clients, and surfaces. Questions and objections about
ABA's own offer live in ABA Q&A, not here — they're pre-call and sales-page material, not post clusters.

## Selecting what to post

- **Repetition is the demand signal, but count it two ways.** Raw times-asked ranks clusters for
  short-form volume — every variant of the question is its own post hook. Distinct askers ranks
  them for what deserves deeper content (blog, video) — six variants from one person is one
  signal; six people asking once is demand. Report both; they disagree in informative ways.
- **Weight the askers against the current avatar before trusting a cluster.** Who asked matters
  more than how often: clients asking mechanics post-purchase is onboarding material, not
  acquisition material, and LinkedIn engagement will overweight practitioner topics regardless.
  Cross-check against the current quarter's avatar (strategy page) before letting a cluster
  graduate up the funnel; the graduation signal is comments/DMs from ICP-shaped people, not
  impressions.

## Drafting

- **Draft via a subagent armed with `linkedin-voice` and the verbatim rows.** Query the cluster's
  rows for their page `url`s, then spawn one subagent whose prompt: loads `linkedin-voice` first,
  fetches the row bodies (verbatim `## Question` / `## Answer`), and returns the draft plus a
  **sourcing appendix** — which rows fed it, which quotes are verbatim, what was cleaned. The
  appendix is what lets you verify claims before the post ships; a draft without one is
  uncheckable.
- **Publish-time cleanup, per convo-mining's rules:** fix garbled proper nouns only inside quoted
  text (Claude ← "clot"), keep the human disfluency that makes a quote sound real, and anonymize
  every asker to a role ("an HR lead at a ~100-person company") — never a name or company.
- **Verify a count-based hook against the database.** "N people asked me X" must match the
  distinct-asker count, and the role words ("founders and execs") must match who the askers
  actually are — a couple of ops leads in the tally makes "founders" an overclaim. Check before
  staging, not after.

## Staging

Normal SFC conventions apply (`references/sfc-database.md`): dedupe both windows, ⬜ icon, and —
since this mode produces a finished draft — the copy goes on the page below a `---` divider,
with a few keyword-level provenance notes (cluster size, source rows) above it.
