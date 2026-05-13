# Leverage scoring

The job: take the activities surfaced in the time study and rank them by *how good a first (or next) skill they'd make for this specific user*. Three dimensions, scored fast, no false precision.

The thing most analyses get wrong: complexity is treated as absolute. It isn't. A two-connector orchestration is trivial for L4 and intimidating for L0. The same task gets a different complexity score depending on who's building it. This rubric anchors complexity to the user's avatar level.

---

## Pre-screen — Type A vs Type B work

Before scoring, classify each candidate. Some recurring activities look like time sinks but are actually craft — automating them destroys the value. Others are pure execution and the user just wants the answer.

- **Type A — execution work.** Just needs to get done. User judgment isn't the value-add — the output is. *Examples: updating a balance sheet from Stripe + bank data, drafting a follow-up email after a call, generating a status digest, logging a call to Notion.* These are pure automation candidates. Score them.
- **Type B — clarity work.** The doing IS the value. The user needs mental contact with the work for reflection, learning, or strategic clarity. *Examples: weekly strategic review, customer call notes (writing them is how the user processes), planning sessions, writing they consider "thinking on the page."* If the entire activity is Type B, drop it from the candidate list. If only parts are Type B, score the Type A pieces (data pulls, formatting, scaffolding) and leave the thinking manual.

**The screen in practice.** A user's Sunday "Weekly Review" might cover strategy, calendar, email, Notion pages, and finances. The strategy pass and calendar review are Type B — the user is making contact with their week. The balance sheet update is Type A — pure data shuffle. Surface the balance sheet as a candidate; leave the rest alone.

When in doubt, ask the user directly: *"If a skill could do this for you and hand you the result, would that feel like a win — or would you feel like you missed something?"* If they'd feel like they missed something, it's Type B.

---

## The three dimensions

### 1. Annual hours (frequency × duration)

How much time does this activity cost the user per year?

Quick math: minutes per occurrence × occurrences per week × 50 weeks ÷ 60 = annual hours.

| Annual hours | Score |
|---|---|
| < 25 | Low |
| 25 – 100 | Medium |
| 100 – 300 | High |
| > 300 | Very high |

Anything in "Low" probably isn't worth a skill — too little leverage. The sweet spot is Medium-High. "Very high" is great if complexity matches.

### 2. Complexity (anchored to user's avatar level)

Score complexity on a 1-5 scale, but the scale shifts with the user's level. The same task can be a 2 for L4 and a 4 for L0. Use this table:

| Complexity score | L0 / L1 means | L2 means | L3 / L4 means |
|---|---|---|---|
| **1 — Trivial** | Single-prompt skill, no connectors, fixed output | Single connector, single tool | Already have the connectors, mostly orchestration |
| **2 — Easy** | Single connector, simple prompt | Two connectors, simple chaining | Multi-connector with clear logic |
| **3 — Moderate** | Two connectors with light logic | Multi-step with branching, but well-defined | Composes existing skills, novel orchestration |
| **4 — Hard** | Multi-connector, branching logic, requires new connector setup | Complex chaining, judgment calls, custom output | Cross-system with state, requires new patterns |
| **5 — Hard for this person** | Anything they'd struggle to even describe | Anything that requires building skills they haven't built before | Genuinely novel territory — meta-skills, agentic loops |

**The 80/20 target is complexity 2-3 for the user's level.** Lower is too small to feel valuable; higher risks the build stalling out.

### 3. Connector readiness

Three states:

| State | Meaning |
|---|---|
| **Ready** | All required connectors are already installed and connected |
| **One install away** | Required connectors exist as MCPs but aren't installed yet (low friction) |
| **Gap** | A required tool doesn't have a usable MCP, or requires meaningful custom work |

Strongly favor **Ready** for the first skill. **One install away** is fine if the user is L1+ and the connector is high-value across other future skills. **Gap** disqualifies a candidate from being the first skill — flag it as "later."

---

## Putting it together

Each candidate gets a one-line summary. Don't show the user the rubric or the scores — show the conclusion.

Internally, you're looking for the activity that maximizes:

> Annual hours, *given* complexity is appropriate for the user's level, *and* connector state is Ready (or One install away with a strong reason).

If two candidates tie, prefer the one that:
1. Solves a *recurring weekly* pain (not monthly) — visible wins build momentum
2. Has output the user can show someone else (a digest, a doc, a Slack post) — easier to feel the value
3. Composes well with future skills (lays groundwork)

---

## Scoring examples

### Example A — L1 user, Gmail + calendar in their life, no connectors set up

Candidate: *Morning email triage*
- Annual hours: ~190 (45 min/day × 5 days × 50 weeks)
- Complexity for L1: 2 (single connector, simple prompt — once Gmail is set up)
- Connector readiness: One install away (Gmail)
- **Verdict:** strong first skill. The required connector install is the right kind of friction — installing Gmail is a multiplier for everything else they'll build.

### Example B — L3 user, has Notion + Slack + Calendar connected, 3 skills already built

Candidate: *Weekly client roll-up — pull last week's calls from Notion, status from Slack, route into a draft email*
- Annual hours: ~50 (1 hr/week)
- Complexity for L3: 3 (multi-connector, well-defined logic)
- Connector readiness: Ready
- **Verdict:** good fit. Lower hours but compounds with their existing skills, and they have the chops.

### Example C — L0 user, just installed Claude this week

Candidate: *Inbox triage with Gmail*
- Annual hours: ~190
- Complexity for L0: 4 (single connector but requires connector install, which is intimidating at L0)
- Connector readiness: One install away
- **Verdict:** wrong first skill. Push them toward something complexity-2 for L0 — a "summarize this PDF in plain English" or "draft a thank-you note from these bullet points" skill. Build connector confidence first; come back to inbox later.

### Example D — L4 user

Candidate: *Meta-skill that routes incoming requests to the right existing skill based on intent*
- Annual hours: hard to estimate directly, but unlocks every other skill
- Complexity for L4: 3 (orchestration over existing infrastructure)
- Connector readiness: Ready (just calls existing skills)
- **Verdict:** strong target. L4s should be building leverage on their leverage.

---

## Quick mental check

Before recommending: ask yourself *"would this user feel proud to demo this skill to a friend in 60 seconds?"* If no, it's the wrong target — too small, too abstract, or too narrow.
