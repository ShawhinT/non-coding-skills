#!/usr/bin/env python3
"""
Token & cost estimator for a single Cowork/Claude conversation.

The model running the skill can see the visible transcript (user turns, its own
replies, tool calls, and tool results) but NOT the raw system prompt, tool
schemas, or skills list that silently reload on every turn. Those are the
"scaffolding" and they dominate cost. We estimate them with a single calibrated
OVERHEAD constant.

Two numbers come out:
  - list price:  what the raw token counts would cost at sticker rates
  - cache-adj:   the realistic cost, accounting for prompt caching

NOTE: Cowork sessions run under the subscription, not the API account, so these
figures are a HYPOTHETICAL "what this would cost via the API" — a value/efficiency
signal for model & effort decisions, not a bill. See SKILL.md.

Validated 2026-07 against a real cached API conversation: total-token error +0.3%,
list-cost error +0.7%, cache-cost error <1% after the fixes below.

Usage:
  python estimate.py transcript.json --in-price X --out-price Y
                                     [--model opus]   (display label only)
                                     [--overhead 38000]
                                     [--cpt N]        (uniform override; else per-role)

No pricing table is stored here. Fetch the live USD-per-million-token rates from
https://platform.claude.com/docs/en/about-claude/pricing and pass them via
--in-price/--out-price (see SKILL.md Step 2).
"""

import argparse, json, math, sys

# ---- Calibration knobs -------------------------------------------------------
# Per-ROLE chars/token, measured via count_tokens on claude-opus-4-8 (2026-07).
# Prose (user/assistant replies) ~3.3-3.4; tool results are JSON/code/tables and
# run much denser ~2.3. Using one blended number mis-sizes both output (pure prose)
# and tool-heavy input, so we split by role.
CPT_BY_ROLE = {
    "user": 3.0,              # human messages. Real chats: markdown/links/numbers,
                              # denser than clean prose. (exact-tokenized on real data)
    "assistant": 2.9,         # model PROSE replies (no tool calls). Denser than pure
                              # prose because of tables, numbers, inline code.
    "assistant_toolcall": 2.1,# model output that INCLUDES TOOL CALLS. Tool-call JSON
                              # content tokenizes ~2.1 (exact-measured); the per-call
                              # framing on top is added separately (FRAMING_TOKENS below).
    "tool": 2.25,             # tool RESULTS returned to the model (dense JSON/code)
}
CPT_FALLBACK = 2.7

# Each tool-call round carries billed tokens beyond its visible content: the tool_use
# structure (id/name/type) + response stop tokens, present in both the output AND when
# the block is re-read as context. Char counts can't see these. Measured ~65/round on
# agentic runs; adding it closed a consistent ~6-8% cost undercount.
FRAMING_TOKENS_PER_TOOLCALL = 65

OVERHEAD   = 38000    # system + tool schemas + skills list, per API call.
                      # Component-measured: skills ~10-13k, system ~18-20k, tools ~5-7k.
                      # Can't be pinned exactly (payload not exposed; not API-billed).

CACHE_READ  = 0.10    # cached input billed at 10% of input price
CACHE_WRITE = 1.25    # cache CREATION billed at 125% of input price (the write premium).
                      # Modeling this fixed a ~14% underestimate of cache-adj cost.
# -----------------------------------------------------------------------------

PRICING_URL = "https://platform.claude.com/docs/en/about-claude/pricing"


def toks(chars, role, override=None):
    cpt = override if override else CPT_BY_ROLE.get(role, CPT_FALLBACK)
    return math.ceil(chars / cpt)


def estimate(messages, in_price, out_price, overhead,
             cpt_override=None, cache_read=CACHE_READ, cache_write=CACHE_WRITE):
    total_input = 0        # cumulative input tokens across all API calls (list basis)
    visible_input = 0      # cross-turn sum of prior_context ONLY (overhead-excluded)
    total_output = 0
    fresh_input = 0        # cache-miss input (billed at write premium in cached mode)
    cached_input = 0       # cache-read input

    prior_context = 0
    seen_by_cache = 0
    first_call = True

    for m in messages:
        t = toks(m["chars"], m["role"], cpt_override)
        if m["role"] == "assistant_toolcall":
            t += FRAMING_TOKENS_PER_TOOLCALL
        if m["role"].startswith("assistant"):   # "assistant" or "assistant_toolcall"
            call_input = overhead + prior_context
            total_input += call_input
            visible_input += prior_context
            total_output += t
            if first_call:
                fresh_input += call_input
                first_call = False
            else:
                cached = overhead + seen_by_cache
                fresh = prior_context - seen_by_cache
                cached_input += cached
                fresh_input += fresh
            seen_by_cache = prior_context + t
        prior_context += t

    list_cost = total_input / 1e6 * in_price + total_output / 1e6 * out_price
    # Cache-adjusted: in a cached session, "fresh" tokens are written to cache once
    # at the 1.25x creation premium, then re-read at 10%. Output is never cached.
    # Cold-start realistic: pay the 1.25x write once, read the rest at 10%.
    cache_cost = (
        fresh_input / 1e6 * in_price * cache_write
        + cached_input / 1e6 * in_price * cache_read
        + total_output / 1e6 * out_price
    )
    # Warm floor: cache already hot from a prior chat, so ALL input reads at 10%,
    # no write premium. Real cost lands between this floor and cache_cost depending
    # on how warm the cache is when the conversation starts (validated: same chat
    # varied 3.7x with cache warmth).
    warm_floor = total_input / 1e6 * in_price * cache_read + total_output / 1e6 * out_price
    return {
        "total_input_tokens": total_input,
        "visible_input_tokens": visible_input,
        "total_output_tokens": total_output,
        "fresh_input_tokens": fresh_input,
        "cached_input_tokens": cached_input,
        "list_cost": list_cost,
        "cache_cost": cache_cost,
        "warm_floor": warm_floor,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--model", default=None)
    ap.add_argument("--overhead", type=float, default=OVERHEAD)
    ap.add_argument("--cpt", type=float, default=None, help="uniform chars/token override")
    ap.add_argument("--cache-read", type=float, default=CACHE_READ)
    ap.add_argument("--cache-write", type=float, default=CACHE_WRITE)
    ap.add_argument("--in-price", type=float, default=None)
    ap.add_argument("--out-price", type=float, default=None)
    args = ap.parse_args()

    with open(args.transcript) as f:
        data = json.load(f)

    model = (args.model or data.get("model") or "unknown").lower()
    if args.in_price is None or args.out_price is None:
        sys.exit(
            "Missing --in-price/--out-price. This script stores no pricing table — "
            f"fetch the live rates (USD per million tokens) from {PRICING_URL} "
            "and pass both flags."
        )
    in_price, out_price = args.in_price, args.out_price

    r = estimate(data["messages"], in_price, out_price, args.overhead,
                 args.cpt, args.cache_read, args.cache_write)

    ti, to = r["total_input_tokens"], r["total_output_tokens"]
    print(f"Model:            {model}  (${in_price}/M in, ${out_price}/M out)")
    print(f"Turns (calls):    {sum(1 for m in data['messages'] if m['role'].startswith('assistant'))}")
    print(f"Input tokens:     {ti:,}  (cumulative across turns)")
    print(f"  fresh:          {r['fresh_input_tokens']:,}")
    print(f"  cached:         {r['cached_input_tokens']:,}")
    print(f"  visible-only:   {r['visible_input_tokens']:,}  (overhead-excluded; calibration anchor)")
    print(f"Output tokens:    {to:,}")
    print(f"Total tokens:     {ti+to:,}")
    print(f"List-price cost:  ${r['list_cost']:.3f}   (ceiling: no caching)")
    print(f"Cache-adj cost:   ${r['cache_cost']:.3f}   (cold start, conservative)")
    print(f"Warm-cache floor: ${r['warm_floor']:.3f}   (cache already hot)")
    print(f">> realistic range ${r['warm_floor']:.3f} - ${r['cache_cost']:.3f}")
    print("JSON " + json.dumps(r))


if __name__ == "__main__":
    main()
