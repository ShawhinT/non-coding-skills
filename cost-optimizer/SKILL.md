---
name: cost-optimizer
metadata:
  author: Shaw Talebi (aibuilder.academy)
  source: https://github.com/ShawhinT/aba-plugins
description: >-
  Estimate the token usage and dollar cost of the CURRENT conversation, then
  translate it into a break-even wage (effective hourly cost) so the user can judge
  whether the task was worth it. Use whenever the user asks what a conversation cost,
  how many tokens it used, "was this worth it", "what's the break-even wage",
  "effective hourly cost", "run the cost estimate", "/cost", "estimate the
  tokens", or any end-of-conversation cost check. Also fire when the user is weighing
  the value they got against what a task cost. Produces an estimate (not a billed
  figure) with list-price and cache-adjusted cost, plus a break-even wage;
  model-tier suggestions are only a forward-looking note since the desktop app
  can't switch models mid-conversation. Do NOT use for pulling real historical
  usage from the Anthropic Console (that's a manual export) or for pricing
  questions unrelated to the current chat.
---

# Token Cost Estimator

The user wants a fast, end-of-conversation gut-check: roughly how many tokens did this
chat burn, what did it cost, and — the real point — was it worth it? The answer they care about is a break-even
wage: the effective hourly cost of having Claude do the task, so they can compare it
to what their own time is worth. This skill closes that feedback loop.

## First: which billing surface is this?

Before anything else, determine how this session is billed — it changes what the final
number *means* and which Optimize levers are real:

- **Subscription surface** (Claude desktop app, Cowork, claude.ai chat): the session runs
  under the user's subscription, not per-token metering. The figure you produce is a
  **hypothetical "what this would have cost via the API"**, translated into usage-limit
  impact. Models can't be switched mid-conversation, so tier advice is forward-looking
  only, and Optimize levers must be actionable in the app (skills, connector hygiene,
  fresh chats, model/effort settings for the *next* chat).
- **API billing** (typical Claude Code CLI, or any session on an API key): the figure is
  a **real bill** — it lands on the Console usage page. Model switching is available
  (`/model`), and Claude Code levers are in scope: `/clear`, starting fresh sessions per
  task, tightening subagent configuration, and `/context`/`/cost` where available.

Tell-tales: the environment/system prompt usually says which surface is running.
Claude Code CLI defaults to API billing (unless authenticated via a subscription plan);
desktop/Cowork/claude.ai are subscription. Sections below are written from the
subscription framing — where you're on API billing, read "hypothetical figure" as
"actual cost" and widen the Optimize palette accordingly.

## The one honest limitation — say it once, plainly

You cannot read the *cumulative* billed token count from inside a conversation — the harness
exposes no running total across all the API calls a session made. So this is a **calibrated
estimate**, good for relative "worth it or not" triage, **not** an invoice number. Don't imply otherwise.

What the harness *does* expose is the **`/context` command** — a live readout of the *current*
context's composition (system prompt, system tools, connector/MCP tool schemas, memory, the message
transcript, and free space). It's a snapshot of one call's input, not a cumulative bill, but it hands
you the two softest inputs to the whole estimate as real numbers instead of guesses: the fixed
per-call overhead and the current transcript size. Only the user can run `/context` — it's a client
command, not a tool you can invoke — so ask for it up front (Step 0).

Crucially (subscription surfaces): **Cowork/Claude-app sessions run under the user's subscription, not their API
account.** They are NOT metered per-token and do NOT appear in the Anthropic Console
usage page — so there is no per-conversation bill to reconcile against, and marginal
cost per chat is effectively zero. What this skill reports is a **hypothetical
"what this would have cost via the API"** figure. That's still the right signal for
the user's actual goal — judging whether a task deserved the model tier / thinking effort
it got — it just isn't an accounting number. Don't send the user to the Console for a real
total; it won't be there. (On API billing this paragraph inverts: the estimate approximates
a real charge, and the Console *is* the authoritative reconciliation point.)

Two things drive the estimate, and one is invisible:
1. **The visible transcript** — user turns, your replies, tool calls, and tool
   *results*. You can see all of this and size it.
2. **The scaffolding** — the system prompt, every tool schema, and the user's
   skills list. These silently reload on *every* turn and usually **dominate** the
   cost. You can't see them, so we model them with one calibrated `OVERHEAD`
   constant (tokens per API call).

## How to run it

Do the estimate with the bundled script so the math is deterministic and the
calibration knobs live in one place. Don't do the arithmetic by hand.

### Step 0 — Open with the user, then ask for a `/context` reading

This is the skill's opening move — before building any transcript, tell the user in one friendly
line what's about to happen, and ask them to run `/context` so the estimate rests on real numbers
instead of guesses. Lead with something close to:

> "Let's analyze this conversation to estimate its usage cost and look for ways to trim it. To help
> me get a sharper number, run `/context` and tell me when you see the breakdown — it drops your real
> context sizes into the chat so I'm not guessing the overhead."

`/context` is the one real meter available, and only the user can run it (it's a client command, not
a tool you can invoke). Running it inserts the breakdown into the conversation on its own — the user
just runs it and sends a quick "done" so you get a turn to read what appeared. Then pin the two
numbers the estimate otherwise softens:

- **`--overhead`** = the *resident* scaffolding re-read on every call: system prompt + system tools +
  **active** connector/MCP tool schemas + memory + skills. Sum those categories and pass the total to
  `--overhead`. Exclude **Free space** and **Messages** (Messages is the transcript, handled in Step 1).
  - **Deferred-tools trap — the easiest way to overstate cost several-fold.** `/context` usually lists
    a large **"MCP tools (deferred)"** category (can be 100k+ tokens on a setup with many connectors).
    Those are *not* resident: only the tool *names* are loaded, and each schema is fetched on demand, so
    they are NOT re-read every call. Leave the deferred pool out of `--overhead` — count only the *active*
    tool schemas. (Its size is still worth quoting as an Optimize lever: disabling unused connectors
    shrinks what could load and keeps that pool from ever becoming resident.)
- **Current transcript size** = the Messages figure — a real anchor for how big the visible conversation
  has grown. Sanity-check your char-count transcript (Step 1) against it; if your eyeballed sum is far
  under the reported Messages tokens, your tool-result estimates are probably low — raise them.

If the breakdown doesn't land in the chat or the user skips it (e.g. a scheduled run with no user
present), fall back to the default `--overhead` and the eyeballed transcript — the estimate still
works, just less grounded. Offer it, don't block on it.

### Step 1 — Build the transcript JSON

Walk the current conversation in order and write `/tmp/cost_transcript.json`. For
each message, record its role and an estimated **character** count (eyeball each
message's length — precision here doesn't matter much; the per-role ratios and
calibration absorb the slop):

```json
{
  "model": "opus",
  "messages": [
    {"role": "user",               "chars": 210},
    {"role": "assistant_toolcall", "chars": 300},
    {"role": "tool",               "chars": 5200},
    {"role": "assistant_toolcall", "chars": 280},
    {"role": "tool",               "chars": 1800},
    {"role": "assistant",          "chars": 4300}
  ]
}
```

CRITICAL — count **every tool-call round as its own API call.** Each time you call a
tool, the model made a separate request that re-processed the entire context. A single
"turn" that used 5 tools is *6 API calls*, not 1, and input cost scales with call
count (each re-reads the ~38k overhead). Collapsing tool rounds into one turn is the
single biggest way to undercount — a real agentic session is often 40-120 calls, not
the handful of user turns. So emit one `assistant_toolcall` + `tool` pair per tool
round, then a final `assistant` for the closing text reply.

Roles (each tuned to how that content actually tokenizes — validated on real chats):
- `user` — the user's messages. Input context on later calls.
- `assistant` — your PROSE replies with no tool call. Output this call, then context.
- `assistant_toolcall` — an assistant step that **makes one or more tool calls**. Its
  chars = your text + the tool-call arguments (the JSON you emit). These tokenize dense
  and carry extra billed framing, handled by the skill. One per tool round.
- `tool` — a tool **result** returned to you (web-fetch page, file read, Notion/Gmail
  dump). Input-only but often **huge** — a couple of web fetches can dwarf the visible
  chat, and they're frequently where the cost actually went. Never skip them.

Set `"model"` to the model that ran this session (from the system prompt / env).

### Step 2 — Fetch live pricing, then run the script

No prices are stored in this skill or its script — pricing has one source of truth,
Anthropic's docs. Fetch the current rates for the session's model (USD per million
tokens, input and output) from
https://platform.claude.com/docs/en/about-claude/pricing — a cheap web fetch — and pass
them explicitly via `--in-price`/`--out-price`. If web access isn't available on this
surface, use your best knowledge of current rates and say plainly that the figures are
from memory, not the live page.

Run the bundled `scripts/estimate.py` from this skill's own directory. Resolve the path at
runtime — locate the directory this SKILL.md loaded from and run the script relative to it
(plugin installs land in a cache directory, never a fixed path):

```bash
python3 <this-skill's-directory>/scripts/estimate.py \
    /tmp/cost_transcript.json --model opus --in-price 5 --out-price 25
```

(`--model` is a display label; the fetched prices are what drive the math.)

It prints input/output tokens (with a fresh-vs-cached split), total tokens, and both
a **list-price** and a **cache-adjusted** cost. The cache-adjusted number is the one
to lead with — after turn 1 the scaffolding is cached at ~10%, so realistic cost is
far below sticker.

### Step 2.5 — Subagents are separate meters (and often the bulk of the cost)

If the session spawned subagents (Agent tool, workflows), their API calls happen outside
the visible transcript and the main-loop estimate misses them entirely. Two traps, both
validated on a real 7-agent extraction session:

- **Don't take reported "subagent_tokens" at face value.** Task notifications report a
  footprint-style number, not cumulative billed input. On the validation run the
  notifications summed to ~1.7M tokens while proper modeling gave ~20M+ cumulative input —
  the subagents were ~90% of the session's true cost, and trusting the reported figure
  produced a 6-7x undercount.
- **Model each subagent like the main loop:** its own transcript JSON with one
  `assistant_toolcall` + `tool` pair per tool round (the notification's `tool_uses` count
  anchors the round count), the spawn prompt as the `user` message, and a smaller
  `--overhead` (~18000 — subagents don't carry the skills list). Agents with high tool-use
  counts (80-120 rounds) are the expensive ones: every round re-reads a growing context.
  Sum the per-agent results with the main loop before quoting a total.

Also watch for **re-emission**: an agent that saves fetched content to disk via Write is
re-emitting those bytes as *output* (5x input price). Reading 175KB of transcripts is cheap;
writing them back out is not — flag it as an Optimize lever (have agents copy/stream via
shell instead of Write when the content passed through a tool result).

**Sanity-check against observable effort before presenting.** The strongest bogosity
detector isn't in the math — it's whether the dollar figure is plausible for how hard the
session visibly worked. Count total tool rounds (main loop + every subagent's `tool_uses`
from its notification); on a top-tier model an agentic round runs very roughly $0.05–0.25
cache-adjusted. If your estimate implies far less per round (a long multi-agent session
coming out at a few dollars), assume an unmodeled meter — usually subagents — and re-model
before presenting, rather than letting the user catch it.

### Step 3 — Present the result

Two parts, in a fixed order: a short readout, then three bullets with nothing after them.

**The readout (1-2 short paragraphs, conversational — not a report).** Cover: est.
tokens (total, and note it's input-heavy — agentic chats are dominated by re-reading
the overhead across many tool-call rounds); the cost as a RANGE (the script prints a
warm-cache floor and a cold-start figure, and real cost lands in that band — the same
chat validated 3.7x more expensive cold than warm; list price is the ceiling); and one
line on where the cost actually went (usually the retrieval loop, not output). On a
subscription surface, say once that the session runs under the subscription, so this is a
hypothetical API figure, not a bill —
then translate it to what subscribers actually spend: **usage limits** (session + weekly,
shared across claude.ai, Desktop, and Claude Code). The same drivers drain both, so every
Optimize move below also stretches limits, and Settings > Usage in the app is the one real
meter that exists. If an "is this normal" anchor helps: enterprise Claude Code usage
averages ~$13/developer per active day, with 90% of users under $30/day (as of 2026-07).

**Then exactly three bullets, and nothing after the third one:**

- **Estimated cost:** ~$X
- **Estimated break-even wage:** ~$Y/hour
- **Recommendation:** Keep *or* Optimize — <one concrete change>

Nothing follows the third bullet — no trailing caveat, no "hope this helps." The bullets
are the scannable takeaway the user asked for; burying them under a closing paragraph defeats
the point. Put every caveat in the readout above them instead.

**The recommendation bullet** is a verdict, not a discussion. **Keep** means the task
earned its setup — same model and thinking effort next time, full stop. **Optimize** means
the next run should be cheaper, and you name exactly ONE concrete change — the single
highest-leverage one, not a menu. Every candidate must be actionable on the surface the
user is actually on: in the desktop app that means no hooks, `/clear`, or subagent
configs; on Claude Code (API billing) those levers ARE in play — `/clear` or a fresh
session per task, `/model` to switch tiers immediately, and trimming subagent
configuration all join the palette below. The desktop palette:

- **Lower model tier** — pick a cheaper model in the model selector next chat; re-run the
  script with the cheaper tier's fetched rates to quote the saving.
- **Lower effort / thinking off** — both live in the app's model settings. Thinking tokens
  bill as output and can run tens of thousands per request, so this lever is bigger than it
  looks. Not available on Fable, which always uses extended thinking — there the lever is a
  tier downgrade.
- **A skill (new or updated)** — the desktop mechanism for both *delegation* and
  *preprocessing*, since those are just standing instructions to Claude. A skill can hand
  over stable context upfront (schemas, workflows, IDs, site structure) so future runs skip
  the repeated research, and it can encode retrieval discipline — "grep the log instead of
  reading it whole", "fetch, summarize, drop the raw dump" — so big tool results never
  bloat the context.
- **Conversation & connector hygiene** — start a fresh chat per task (every tool call
  re-reads the whole transcript, so long chats cost superlinearly, and auto context
  management burns extra usage); batch related asks into one message; disable unused
  connectors in Search & tools (they're token-heavy scaffolding — this literally shrinks
  the `OVERHEAD` constant). If a `/context` reading is on hand, quote the actual connector/MCP
  tool-schema share (often the largest scaffolding category) so "disable unused connectors" lands
  as a concrete number — "your loaded connectors are ~N tokens re-read every call" — not just advice.

The cache-adjusted number is a *conservative cold-start* figure (it assumes the
scaffolding is written to cache once this conversation, the 1.25x write premium). The user's
scaffolding is identical across chats, so back-to-back use keeps the cache warm and real
cost runs *below* the cold-start estimate — present cache-adj as "about this or a bit
less." Accuracy vs. real API billing: tokens within ~5%, list-price cost within ~5-8%;
output on very short chats is the noisiest piece but a minor share. One known
undercount: extended-thinking tokens bill as output but are invisible in the transcript —
on high-effort settings or always-thinking models (Fable), the real output figure runs
higher than the estimate; say so rather than silently absorbing it.

A good shape:

> This chat ran ~6M tokens across ~60 API calls, almost all input — each tool round
> re-read the ~38k-token scaffolding plus a growing transcript, while output was tiny.
> So the drafting was cheap; the retrieval loop is where it went. On Opus that's
> ~$3.50–$4.16 cache-adjusted (list ceiling ~$31). By hand — the reconcile, ~10 drafts,
> an SOP edit, 7 DB updates — this is ~2 hours, so it cost about $2 per hour of your time
> it replaced.
>
> - **Estimated cost:** ~$4
> - **Estimated break-even wage:** ~$2/hour
> - **Recommendation:** Optimize — mostly retrieval and formatting, no hard reasoning; run it on Sonnet next time (~$1.10 cache-adj at Sonnet's rates).

## The break-even wage — this is the payload

The number only matters if it drives a decision, and in the Claude desktop app (Cowork)
you **can't switch models mid-conversation** — so "you should've used a cheaper model" is
advice the user can't act on for the chat that just ran. The worth-it signal is therefore not
a model nudge but an **effective hourly cost**: what the task cost divided by how long it
would have taken the user to do by hand.

**Break-even wage = estimated cost ÷ estimated manual-time-equivalent (in hours).**

Read it as: "as long as your time is worth more than $Y/hour, letting Claude do this pays
off." It's interpretable at a glance with no knowledge of tokens or model tiers, and since
the effective rate usually lands at a couple of dollars an hour, the verdict is almost
always "worth it" — the metric's job is to make that concrete, not to second-guess it.

**Estimating the manual time** is the one input you have to reason about, and the softest
number in the readout. Do it bottom-up: decompose the conversation into its concrete
deliverables (each reconcile pass, each drafted email, each doc edit, each batch of DB
updates), assign a rough "how long would a person take" to each, and sum. Be transparent
that it's a gut estimate. Offer to ground it by timing one real comparable task, so future
runs anchor to a measured number instead of a guess.

**Be conservative: assume a fast human, and quote the wage as an upper bound.** The
break-even wage will be met with skepticism — a reader's instinct is to attack the manual-time
guess ("I'd have done that faster"), and a wage built on a slow-human estimate collapses under
that critique. So price the manual work as a fast, competent person doing it briskly (the low
end of the hours range), exclude rigor a human would realistically skip (nobody
character-verifies 186 quotes by hand), and present the result as "at most ~$Y/hour." A
conservative wage that still clears the bar is persuasive; an optimistic one invites the
whole estimate to be dismissed. When the hours are genuinely uncertain, the range you give
should be driven by fast vs. very-fast — not fast vs. thorough.

**Model tier is a secondary, forward-looking note only.** You can still observe that the
work was mostly retrieval/formatting (Haiku or Sonnet territory) versus genuine hard
reasoning (Opus/Fable earned it), but frame it as a default for a *future* chat or a
scheduled task's next run — never as a fix for the conversation that just happened.
Re-running the script with the cheaper tier's rates gives the concrete "what a cheaper
tier would cost next time" comparison. Be honest both ways: if Opus was the right call, say so.
This judgment is what feeds the **Recommendation** bullet (Keep vs. Optimize) in the readout.

## Calibration (how the estimate gets trustworthy)

V1 ships with reasonable defaults, but the `OVERHEAD` constant is a guess and a setup
with many skills/connectors makes it large. Calibrate against real numbers — the knobs are
at the top of `estimate.py` and overridable via CLI:

- `--overhead N` — tokens of system+tools+skills per call. **Tune this first**; it
  moves the answer the most. Raise it until estimates match observed cost. The most direct
  calibration is the user's own `/context` reading (Step 0): sum every category except Messages,
  Free space, and the deferred MCP-tools pool (names-only, not resident), and pass that as
  `--overhead` — the constant measured rather than fitted.
- `--cpt N` — characters per token (default 3.7). Lower = denser text = more tokens.
  Fable 5, Opus 4.7+, and Sonnet 5 use a newer tokenizer that produces ~30% more tokens
  for the same text — start near 2.8 when estimating those models.
- `--cache-read N` — cached-input price multiplier (default 0.10).

The calibration experiment the user runs to fit these is described in `references/calibration.md`.
Read it when the user wants to tune the constants against actual API/Console data.

## Notes

- No prices are stored anywhere in this skill. The pricing source of truth is
  https://platform.claude.com/docs/en/about-claude/pricing — fetch it fresh each run
  (Step 2) and pass the rates via `--in-price`/`--out-price`. This also picks up
  time-limited rates (intro pricing, changes) automatically, with nothing to keep in sync.
- This estimates **one conversation**. It does not sum across a day or reconcile a
  bill — for that, the Console usage export is authoritative.
- Further reading (all as of 2026-07-13): [cost management](https://code.claude.com/docs/en/costs)
  (Claude Code-centric — translate its levers to desktop as above),
  [usage & length limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work),
  [usage-limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices),
  and [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  — the one-line rationale behind every recommendation here: keep the context to the
  smallest set of high-signal tokens.
