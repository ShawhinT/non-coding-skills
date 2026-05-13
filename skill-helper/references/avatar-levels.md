# Avatar levels

Five levels along the Claude-skill-builder spectrum. Place the user from Phase 0 signals first; ask one targeted question only if you're stuck between two adjacent levels.

The point of the avatar isn't labeling the user — it's calibrating *how you talk*, *what you assume*, and *which skill ideas land*. A great L0 conversation looks nothing like a great L4 conversation.

---

## L0 — New to Claude entirely

**Tells:** No prior sessions. Asks foundational questions ("what's a connector?", "what's a skill?"). Often arrived because someone told them to try this.

**How to talk:** Slow down. Define "connector" and "skill" in one sentence each the first time you use them. No jargon-as-shorthand. Avoid the phrase "MCP" — say "tool integration."

**What to assume:** They don't know what's possible yet. Their "what's worth automating" instincts will be off, because they don't know what Claude can do. Lean heavier on *your* suggestions; lean lighter on asking *them* what they want.

**Skills that land — almost always tool skills:**
- A single tool skill built on whatever connector got wired up in Phase 1.5 — `gmail-helper`, `notion-helper`, `calendar-helper`. The user needs to feel the daily win of a skill that tames one tool before anything else.
- Things they can demo to a friend in under a minute.
- If no connector yet: a zero-connector utility like "summarize this PDF in plain English."

**Skills that don't land yet:**
- Process skills (multi-step, multi-tool) — too much orchestration before they trust the building blocks.
- Anything where the value depends on existing infrastructure they haven't built.

---

## L1 — Uses Claude regularly, no connectors

**Tells:** Sessions exist. No MCPs installed. Uses Claude as a chat tool, maybe occasional file work.

**How to talk:** Skip the basics on Claude itself. Connector orientation happens in Phase 1.5 — don't repeat it here.

**What to assume:** They have intuitions about what's repetitive in their work. They just haven't connected the dots between "Claude" and "actually doing the thing." Their first skill is often a wedge built on whatever got connected in Phase 1.5.

**Skills that land — tool skills, same as L0:**
- A single tool skill tied to whichever connector got wired up in Phase 1.5 — `gmail-helper`, `notion-helper`, `slack-digest`. The skill should *demand* the connector; that's what makes it stick.
- Pick the connector with the lowest setup friction relative to value.

---

## L2 — Some connectors, no skills

**Tells:** Active connectors. `list_skills` empty or has 0-1 skills. They're using Claude + connectors as a souped-up chat tool but haven't crossed into automation.

**How to talk:** They get the building blocks. Skip definitions. The unlock here is the *concept of a skill itself* — that they can package a workflow and give it a name, and Claude will run it consistently. Most L2s have the right ingredients and just haven't seen the recipe.

**What to assume:** They've felt the pain of repeating the same prompt structure. Ask about workflows where they've found themselves typing roughly the same instructions multiple weeks in a row. That's the skill.

**Skills that land — either type, matched to pain:**
- **Tool skill** if the pain is a single connector they fight with daily — repeated preambles, awkward queries, working around the same quirks every time. Formalize that into a helper.
- **Process skill** if the pain is a manual checklist they run weekly — a repeated prompt sequence across 1-2 connectors. The win is *consistency*: always do X, in this order, with this output format.
- The first skill should formalize an existing habit, not introduce a new one. Don't suggest something fancier than what they're already doing manually.

---

## L3 — A few skills built, wants more

**Tells:** Has 1-5 skills. Asks about leverage, asks "what should I build next." Comfortable with skill-creator.

**How to talk:** Peer-to-peer. Skip onboarding. Spend the conversation on diagnosis — what's their highest-friction recurring task that *isn't* already a skill, and why hasn't it become one yet? Often the answer reveals an under-used connector or a workflow they've been doing manually because "it's complicated."

**What to assume:** They have taste. They know what a good skill feels like. The friction is identifying the next-best target, not building it.

**Skills that land — process skills start to dominate:**
- **Process skills** are the natural next step — multi-connector orchestrations they've been doing manually because the wiring felt fiddly. Think `pre-call-research`, `weekly-client-rollup`, `outreach-triage`. The value is replacing a manual checklist with a single invocation.
- Skills that compose with their existing tool skills (e.g., `executive-briefing` calls their existing `notion-helper` and `calendar-helper` under the hood).
- **Tool skills** still land if there's a connector they use daily but haven't wrapped yet — but most L3s have already built the obvious ones.

**What to flag:**
- Watch for over-engineering. L3s sometimes want to build the most clever skill, not the most useful one.

---

## L4 — Established skill builder

**Tells:** 5+ skills. Talks about skills like infrastructure. Asks about higher-leverage targets, second-order effects, skill composition.

**How to talk:** Strategy session, not walkthrough. They don't need scaffolding — they need pushback and a fresh angle. Be willing to challenge their framing.

**What to assume:** They've already built the obvious stuff. The remaining leverage is in: skills that compose other skills, skills that target higher-stakes / lower-frequency work, skills for parts of their work they've been ignoring because "it's too messy to automate."

**Skills that land — almost entirely process skills (and meta-skills):**
- **Process skills** targeting strategic, high-stakes work — `weekly-strategic-review`, `quarterly-planning`, `client-engagement-wrap`. The remaining leverage at L4 is in multi-step workflows the user has been doing manually because "it's too messy to automate."
- **Meta-skills** that orchestrate existing tool and process skills — a morning routine that chains `executive-briefing` → `inbox-triage` → `calendar-review`.
- Skills that capture judgment they currently hold in their head and want to externalize.
- **Optimization candidates** — merging two overlapping skills, splitting a bloated one, trimming dead weight. Sometimes the leverage is in tightening existing skills rather than building new ones. The mechanics live in `skill-updater`.

**The L4 plateau — when skill candidates stop landing.**

Some L4 users have genuinely covered their workflow. Every candidate you suggest, they already have a skill for. They'll say some version of *"if it were painful, I'd have already automated it"* or just reject candidates one by one. This isn't a failure of the skill-helper — it's a signal that the user has graduated from skill building.

The unlock at this point is **scheduled tasks**: taking the skills they already have and removing the human from the trigger loop. The user is still manually opening a chat every morning to run `pre-call-research` for today's calls, or triggering `email-helper` five times to draft follow-ups. The skills work perfectly — the bottleneck is that the user is the cron job.

When you hit this wall, pivot to Phase 4A in SKILL.md. Look for repeating session patterns, recurring Notion tasks that trigger the same skill sequence, and email batches that go out on a cadence. The output is 2-3 scheduled task candidates, not skill candidates.

**What to flag:**
- Push back if they're building skill #6 in a category where they already have 3. Ask what they're avoiding — and consider whether a merge/split is a better move than another build.
- Watch for the plateau signal. Don't keep pushing skill ideas when the user is telling you they've already covered the ground. Pivot to scheduled tasks — that's where the remaining leverage lives.

---

## When you're between two levels

Ask one question. Examples:

- Between L0 and L1: *"Have you used Claude before this conversation? Even casually?"*
- Between L1 and L2: *"Any connectors set up — Gmail, Notion, Slack, anything like that?"*
- Between L2 and L3: *"How many skills have you built so far?"*
- Between L3 and L4: *"What's the most ambitious skill you've shipped?"*

One question. Don't quiz them.
