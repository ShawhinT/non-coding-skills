# Calibrating the estimator against real usage

The estimate has two error sources. Calibrate them separately — one is cheap and
exact, the other needs real session data.

- **Error A — tokenizing visible text.** How well does `chars / CHARS_PER_TOKEN`
  match the true token count of a chunk of text? Fixable exactly and for free.
- **Error B — the OVERHEAD constant.** The invisible system+tools+skills payload per
  call. This is the big one, and the only way to pin it is to compare full-session
  estimates to what the account actually got billed.

## Experiment A — fix chars-per-token (free, exact, do this first)

Ground truth for token counts is Anthropic's `count_tokens` endpoint — it returns the
exact input token count for a given payload and costs nothing.

1. Grab 5–10 representative text chunks from real chats: a couple of the user's messages,
   a couple of assistant replies, a web-fetch result, a Notion dump. Aim for variety
   (prose, code, JSON) since density differs.
2. For each chunk, get the exact count:
   ```bash
   curl https://api.anthropic.com/v1/messages/count_tokens \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-opus-4-8","messages":[{"role":"user","content":"<CHUNK>"}]}'
   ```
   (Requires a standard API key. The returned `input_tokens` minus a small fixed
   message overhead ≈ the chunk's true tokens.)
3. Compute `chars / true_tokens` for each chunk and average. That average is your
   calibrated `--cpt`. Typical result lands near 3.5–4.0.

Result: the visible-transcript half of the estimate is now essentially exact.

## Experiment B — measure OVERHEAD directly (Cowork is NOT API-billed)

Important reality check learned 2026-07: Cowork/Claude-app sessions run under the
subscription, not the API account. They do **not** appear in the Console usage page,
so there is no billed ground truth to fit against. The Console-comparison approach
only works if you're replicating turns through the API directly — which we can't do
faithfully without Cowork's exact system+tools payload.

So measure OVERHEAD by its **components** instead, using the free `count_tokens`
endpoint on the scaffolding text you *can* get at:

1. **Skills list (measurable exactly).** Extract the description block from every
   installed `SKILL.md` frontmatter, concatenate, and `count_tokens` it. Measured
   result: ~34 skills ≈ 10k tokens for the trimmed disk text; the live injected list
   runs larger (fuller descriptions + plugin/system skills) — scale up ~30% to ~13k.
2. **System prompt (estimate).** The Cowork system prompt isn't on disk verbatim, but
   it's large and fairly stable — budget ~18–20k tokens.
3. **Tool schemas (estimate).** The deferred tool-name list plus loaded schemas —
   budget ~5–7k tokens.

Sum → OVERHEAD ≈ 35–45k. The default is 38k. This can't be pinned to the token
because pieces 2–3 aren't exposed and nothing bills these chats, but the components
bound it well, and for relative triage anything in this band gives the same verdict.

The single most direct measurement, when the user is present, is their own `/context`
reading (SKILL.md Step 0): it prints every scaffolding category as a real token count.
Sum system prompt + system tools + **active** MCP/connector schemas + memory + skills.
**Do not add the "MCP tools (deferred)" line** — that pool is names-only and fetched on
demand, not resident, so it isn't re-read per call; folding it into OVERHEAD can overstate
cost several-fold on connector-heavy setups.

If Anthropic ever surfaces a real Cowork token meter, revisit: back OVERHEAD out via
`OVERHEAD ≈ (actual_input − estimated_visible_input) / turns` across a few chats of
different lengths (Experiment A already nails the visible term).

## Realistic agentic validation (2026-07) — 5 experiments

Beyond the toy prose test, we validated against realistic tool-using conversations —
real agentic loops through the Messages API (exact billing) plus an exact-tokenization
pass over this actual session's transcript. Results and the fixes they forced:

- **Tool rounds are separate API calls.** The real session was ~120 calls, not ~16
  user turns. Input cost scales with call count (each re-reads the overhead). The skill
  must emit one `assistant_toolcall`+`tool` pair per tool round — the biggest
  structural undercount if missed.
- **Per-role cpt, exact-measured on real content:** user 3.0, assistant-prose 2.9,
  assistant_toolcall 2.1, tool-result 2.25. Real chats are denser than textbook prose
  (markdown, tables, numbers, code). Lands within ±1.4% per role on the real transcript.
- **Tool-call framing.** Billed tokens exceed visible content by ~65 tokens/round
  (tool_use structure + stop tokens), invisible to char counts. A per-round constant
  closed a consistent ~6-8% cost undercount; dense-JSON agentic output went from ~-45%
  to near-0.
- **Cache warmth dominates realized cost.** The same short chat billed $0.086 cold vs
  $0.023 warm (3.7x). Hence the skill reports a band, not a point.

Net validated accuracy on agentic chats: input tokens within ~5-6%, list cost within
~5-8%. Output is the least-precise piece but a minor cost share. Plenty for triage.

## The cache model — validated end-to-end (2026-07)

We ran a real cached multi-turn conversation through the Messages API and compared
exact billed usage to the estimator. Findings:

- **Token counts: ±0.3%.** The overhead + growing-context + per-role-cpt model
  reproduces actual input/output token counts almost exactly.
- **List cost: ±0.7%.** Essentially exact.
- **Cache-adjusted cost — COLD start: <1% error** after adding the 1.25x cache-write
  premium. This is the case the script models: turn 1 pays to *write* the scaffolding
  to cache; later turns *read* it at 10%.
- **Cache-adjusted cost — WARM start: the script reads ~3x high.** A second run 60s
  later found the scaffolding *still cached* from the first run (turn 1 was a cache
  read, not a write), so actual cost was far lower.

Takeaway: the cache-adjusted number is a **conservative (cold-start) estimate** — it
assumes you pay the write premium every conversation. Real cost floats between that and
an all-reads *floor*, depending on how warm the cache is when the chat starts. Ephemeral
cache lives ~5 min (1 hr on the extended tier).

This matters for Cowork specifically: the scaffolding (system + tools + skills) is
*identical* across every conversation, so back-to-back chatting keeps the cache warm and
real cost drifts toward the floor — below the estimate. Erring high is the safe
direction for a spend-awareness tool, so this is fine; just don't treat the cache-adj
figure as a hard number. list price = absolute ceiling (no caching); cache-adj =
conservative realistic; warm floor = all reads.

## What "good enough" looks like

The goal is decision-support, not accounting. If the calibrated estimate lands within
~20–30% of billed cost consistently, it's doing its job: the user can tell a $0.05 chat
from a $2 chat and decide whether the model tier matched the value. Chasing tighter
than that isn't worth the effort.
