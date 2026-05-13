---
name: skill-helper
description: Walk someone through building their first (or next) high-leverage Claude skill, end-to-end. Gather context silently, diagnose their level, run a time study, score time-vs-complexity for their level, suggest 3-5 candidate skills, hand off to skill-creator, and close with a one-line opt-in CTA to share what they built with Shaw. Use whenever someone is figuring out what skill to build, what to automate, or where to start with skills. Triggers include "help me build a skill", "what should I automate", "where do I start with skills", "I don't know what to build", "walk me through my first skill", "help me find a skill to build", "what's worth automating", "give me skill ideas", "what's a good first skill". Also fires when someone shares a calendar or workflow and asks what's automatable, when a new Claude user wants guided onboarding to skill-building, or when an experienced builder is hunting higher-leverage targets. Casual phrasing like "I should probably automate something" counts too.
---

# skill-helper

Walk a person through building their first (or next) high-leverage Claude skill — the same shape as Shaw's 1:1 skill-building workshop, but scalable.

The job is to get them from "I should probably automate something" to a working skill in their hands, plus a one-line invitation to tell Shaw what they built. Every step adapts to where the person actually is — a brand-new Claude user gets a different ride than a seasoned skill builder.

## What to do at the very start

Before any tools fire, drop a single expectation-setter line:

> I'll help you figure out your next high-leverage Claude skill. I'm going to start with a couple of minutes of background research on how you work and then ask you a few targeted questions.

Adjust the wording for tone but keep it short. Don't preview later phases — the user doesn't need a roadmap before anything has happened.

Then immediately create a TodoList with the four user-facing phases, **in this exact order**:

1. Research how you work
2. Interview + align on what I'm seeing
3. Suggest 3-5 candidate skills
4. Build the one you pick

These four tasks map to the internal phases (research = Phase 0+1+1.5, interview = Phase 2, suggest = Phase 3+4, build = Phase 5). The closing CTA in Phase 6 stays internal — don't add it as a task.

**Keep the TodoList in sync at every phase boundary.** At each transition, flip the previous task to `completed` *and* the next one to `in_progress` in the same update. The list is only useful when it actually reflects where you are.

## The flow

Move through the phases in order, but don't announce them — this should feel like a conversation, not a checklist. Phase 1.5 only fires for L0/L1 users with no connectors; everyone else skips straight from Phase 1 to Phase 2.

## Two types of skills

Every skill falls into one of two categories. Knowing the type sharpens your recommendations — the two types have different profiles, different sweet spots by avatar level, and different build patterns.

**Tool skills** wrap a single connector and make it reliable and pleasant to use. They tame a tool's quirks so the user stops fighting the interface and starts getting answers. High frequency (often daily), low-to-moderate complexity, single-connector footprint.

Examples from Shaw's library: `email-helper` (Gmail), `google-drive-helper` (Drive), `calendar-helper` (Google Calendar), `stripe-helper` (Stripe), `notion-helper` (Notion).

The pattern: the skill knows the connector's data model, common gotchas, and the user's preferences. It turns a raw connector into a tool that feels like it was built for them.

**Process skills** encode a repeatable multi-step sequence — often pulling from multiple tools, applying judgment or a framework, and producing a deliverable. Lower frequency per run (weekly, per-event, per-call), but higher value per execution. Moderate-to-high complexity.

Examples from Shaw's library: `pre-call-research` (research a person before a call), `executive-briefing` (pull tasks across Notion databases into a morning rundown), `linkedin-post-analytics` (scrape and analyze post performance), `outreach` (source → enrich → triage → track → message).

The pattern: the skill replaces a checklist the user runs manually. Without it, they either skip steps or spend 30+ minutes on a process that should take 2.

**Why this matters for recommendations:**

- **L0–L1:** Start with a tool skill. One connector, visible daily win, low build complexity. The user needs to feel the value of a skill before tackling multi-step orchestration.
- **L2:** Either type works. If they're repeating the same prompt pattern against one tool, that's a tool skill. If they're running a manual checklist across tools, that's a process skill. Match the type to the pain they described.
- **L3–L4:** Lean toward process skills — the high-leverage targets at this level are almost always multi-step workflows the user has been doing manually because "it's complicated." Tool skills at this level are usually already built or trivial to add.

Use this framing when synthesizing candidates in Phase 2, scoring in Phase 3, and presenting suggestions in Phase 4. Tag each candidate by type so the user builds intuition about the distinction.

---

## Phase 0 — Silent context gathering (parallel)

Before asking the user anything, fan out subagents in parallel and pull every signal you can reach autonomously. Two failure modes to avoid: interrogating about things you could have figured out, and the opposite — leaning on a single signal (just session history, just connectors) and treating the partial picture as complete.

Spawn in parallel, one subagent per signal class:

- **Installed skills and plugins** — current state, what they've already built
- **Connected MCPs** — capability surface; tells you which other Phase 0 sources are reachable
- **Recent sessions and transcripts** — last ~10; read 2–3 of the most substantive. Surfaces workflows, complaints, tool habits
- **Calendar (if connected)** — pull a typical recent week. Strongest data signal on time use; don't wait for Phase 2. See `references/time-study.md` for what to look for and the multiple-calendars probe
- **Inbox (if connected)** — pattern sample: dominant thread types, recurring senders, response patterns. Where invisible work lives
- **Other connected sources** (Slack, Notion, Drive) if they look informative for avatar or time-spend

Skip sources that aren't connected.

**Synthesize across signals.** Any single source is partial. Calendar shows scheduled work, not the cracks. Sessions show what Claude touched, not what the user does manually. Inbox shows reactive work, not creative. Triangulation is what makes the picture trustworthy.

Output a working hypothesis: likely avatar level, 2–3 candidate workflows to probe, and explicit gaps — both missing connectors and partial-data signals (e.g., one calendar visible, likely more elsewhere).

**Rule of thumb:** if you've already inferred something with reasonable confidence, don't ask about it — confirm it. *"Looks like you're pulling Notion pages most mornings — is that a daily thing?"* beats *"Tell me about your morning routine."*

## Phase 1 — Avatar diagnosis

Five levels. Most of the time you can place the user from Phase 0 alone; ask one targeted confirmation question if you're between two levels.

| Level | Profile | Tell |
|---|---|---|
| L0 | New to Claude entirely | No prior sessions, asks basic questions |
| L1 | Uses Claude regularly, no connectors | Sessions exist, no MCPs installed |
| L2 | Some connectors, no skills | Connectors active, `list_skills` empty or near-empty |
| L3 | A few skills built, wants more | Has 1-5 skills, asks about leverage |
| L4 | Established skill builder | Has 5+ skills, asks about higher-leverage targets |

Avatar drives everything downstream — depth of explanation, what counts as "complex," which skill ideas land. See `references/avatar-levels.md` for what to do differently at each level.

## Phase 1.5 — Connector onboarding (L0/L1 with no MCPs only)

Skip this phase entirely if the user already has connectors active or sits at L2+. It only fires when the avatar is L0/L1 *and* `list_connectors` (or equivalent) shows nothing wired up.

When it does fire: useful skills almost always need at least one connector, so building without one would push them toward a low-leverage first skill. Orient them in three short beats — no lecture:

1. **What a connector is**, in one sentence. *"The thing that lets Claude actually touch your tools — Gmail, Notion, calendar, etc. Without one, Claude is just a chat box."*
2. **Two or three to consider first**, calibrated to what they described in Phase 0. Don't list ten. Inbox-heavy → Gmail. System-builder → Notion. Schedule-heavy → Calendar. File-heavy → Drive. Pick the smallest set that unlocks their likely first skill.
3. **Hand them through the connect flow**, then return to Phase 2.

The bar is "enough to build something useful," not "complete onboarding." One connector wired up is enough to proceed; the rest can wait until they've felt the value.

## Phase 2 — Synthesize + interview

Phase 0 gave you data. Phase 2 turns that data into a shared understanding — and surfaces what data alone can't tell you. Three moves, in order:

**1. Synthesize and play it back.**

Roll the calendar, sessions, inbox, and connector signals into a tight read of how the user spends their week. **Keep the summary skimmable — use bold labels and short bullets, not prose paragraphs.** The user should be able to scan it in 10 seconds and react. Format:

> **You:** [avatar summary — one line]
>
> **Top session categories:** [top 3 by frequency]
>
> **Typical week:**
> - [recurring activity 1 — frequency + duration]
> - [recurring activity 2]
> - [recurring activity 3]
> - [interstitial work — what fills the gaps]
>
> **Where I see the most repetitive time:**
> 1. [pattern 1 — describe without framing as automation candidate]
> 2. [pattern 2]
> 3. [pattern 3]
>
> **What I'm probably missing:**
> - [explicit gap call — e.g., "Other calendars beyond your primary?"]
> - [another gap]
>
> Does that match?

The point isn't to be precise — it's to demonstrate you've done the homework and to give the user a concrete artifact to react to. Reactions surface the truth faster than open-ended questions do. The skimmable format also avoids a failure mode where the user has to re-read dense paragraphs just to confirm basic facts — bullets let them nod along or push back immediately.

**Do not suggest automation candidates or skill ideas in Phase 2.** The goal here is to confirm you understand how the user works — not to preview what you think they should build. Listing candidates at this stage biases the conversation: the user starts reacting to your suggestions instead of filling in the gaps you need filled. Observations like "I see a lot of time going to X" are fine — they invite correction. Framing those same observations as "automation candidates" or tagging them by skill type crosses into Phase 4 territory. Save candidate suggestions, skill names, type labels (tool/process), and hours-saved estimates for Phase 4, where they belong.

Internally, note which signals point toward tool skills vs. process skills — that thinking will feed Phase 3 scoring. Just don't surface it to the user yet.

**2. Ask Mom Test–style targeted gap-fill questions via `AskUserQuestion`.**

After the playback, ask **at least one** targeted follow-up question using `AskUserQuestion`. This is required — don't skip straight to scoring even if you think the picture is complete. There's always a gap worth probing.

Use Mom Test framing: ask about behavior that already happened, not what they think or feel in the abstract.

- ✅ *"When was the last time you got stuck doing X — what email, what made it slow?"*
- ❌ *"What's frustrating about your inbox?"*

Build questions from what you actually saw, not a generic checklist. Use `AskUserQuestion` with pre-baked answer options where possible — it's faster for the user to tap a choice than type a paragraph. Reserve free-form for questions that genuinely need open-ended answers (e.g., "walk me through what happened in the last one"). Examples calibrated to a real read:

- *"Your Sunday Weekly Review is 2.5 hrs — what's the most annoying or repetitive part of it?"* → options like "Pulling data from multiple sources", "Writing the same summary format", "Deciding what matters", "Something else"
- *"Of all your skills, which 2–3 do you actually call most often, and do you ever call them in the same sequence back-to-back?"* → free-form (too varied for pre-baked options)
- *"Where does the most time go after a workshop session ends?"* → options like "Writing the follow-up email", "Updating Notion", "Prepping for the next session", "All of the above"

A fallback elicitation pattern lives in `references/time-study.md` for when Phase 0 was thin (typically L0/L1) and you need a scaffold. The L3/L4 swap (same-skill-call sequence instead of same-prompt) is in there too.

**3. Loop until the user signs off.**

If they fill a gap (extra screenshot, paste, one-line description) or push back on something you misread, update your model and play it back once more. Don't move to scoring until the user has explicitly confirmed the picture.

**Connected ≠ complete.** Connected sources are often partial — multiple calendars where only one is OAuth'd, multiple inboxes where only one is hooked up, work that lives in tools you can't reach (paper notebook, separate Drive, Slack DMs in a workspace they didn't connect). Name the gap explicitly and give the user a specific, low-effort way to fill it (a screenshot, a paste, a one-line description). Don't pretend the partial picture is complete.

## Phase 3 — Time-vs-complexity analysis (avatar-relative)

For each candidate activity, score on three dimensions:

- **Annual hours** = frequency × duration. Higher is more leverage.
- **Complexity** — *relative to the user's avatar level.* This is the part most analyses get wrong. A "use 2 connectors in sequence" task is trivial for L4 and high-effort for L0. The same task gets a different complexity score depending on who's building it. See `references/leverage-scoring.md` for the avatar-anchored rubric.
- **Connector readiness** — do the tools needed actually have MCPs? Does the user have them installed, or are they easy to add?

The 80/20: high-frequency, complexity-appropriate-for-their-level, connector-ready tasks. That's where you want to focus their first skill.

Output a small ranked table — 3-5 rows, no more. Don't show the math; show the conclusion.

## Phase 4 — Suggest 3-5 candidate skills

Each suggestion is a one-liner with four pieces:
1. **Name** (kebab-case, evocative)
2. **Type** — `tool` or `process`
3. **What it does** (one sentence)
4. **Why it's a fit** (hours saved + connectors needed + whether they're already wired)

Examples:

> **`inbox-helper`** *(tool)* — tame Gmail's quirks: search threads, draft replies in your voice, triage unread into buckets. Saves ~4 hrs/week. Uses Gmail (already connected).

> **`pre-call-research`** *(process)* — before any sales call, pull the person's LinkedIn, CRM history, and past emails into a one-page brief. Saves ~45 min/call × 4 calls/week. Uses Gmail + Notion + LinkedIn (Gmail and Notion connected; LinkedIn via Chrome).

Three to five candidates is the sweet spot. Fewer feels thin; more is paralyzing.

**Calibrate the type mix to the avatar level.** L0–L1 suggestions should be mostly tool skills (low complexity, single connector, daily wins). L2 gets a mix — match to whatever pain they described. L3–L4 suggestions should lean process-heavy — the remaining leverage at that level is almost always in multi-step workflows. See "Two types of skills" above for the full rationale.

**For L4 users especially: a "new skill" isn't always the right answer.** If the user has overlapping skills, a bloated one, or a skill that's been superseded, surface optimization candidates alongside new builds — *"merge `crm` and `lead-intake`," "split `outreach` into sourcing + messaging," "trim dead weight from `notion-helper`."* The mechanics for cleanup live in `skill-updater`; here you're just naming that the option exists. Don't default to new — sometimes the leverage is in tightening what's there.

## Phase 4A — Scheduled task pivot (L4 plateau)

This phase only fires when **all three conditions** are met:

1. The user is L4
2. You've presented skill candidates in Phase 4
3. The user pushes back on most or all of them because their existing skills already cover the work

The signal is some version of: *"I don't know — if it were painful, I'd have already automated it,"* or *"my existing skills handle that,"* or just repeated rejection of candidates with "I already have a skill for this." When you hear that, the user has graduated from skill building. The next level of leverage isn't a new skill — it's putting their existing skills on autopilot.

**Shift the lens.** Stop looking for workflows that need a skill and start looking for workflows where the user is the orchestration layer — they're manually triggering the same skills in the same sequence on a recurring basis. The skill works fine; the human-in-the-loop trigger is the bottleneck.

**How to find candidates.** Go back to the Phase 0 data with fresh eyes:

- **Session transcripts** — look for sessions with similar titles or patterns repeating across days/weeks. If the user runs `pre-call-research` every morning for that day's calls, that's a scheduled task candidate.
- **Calendar + Notion cross-reference** — recurring events that always have paired Notion tasks (prep before, follow-up after) point to a trigger → skill → output loop that could run autonomously.
- **Email patterns** — batches of similar emails sent on a cadence (weekly outreach, pre-session emails, follow-ups) suggest a drafting task that could run overnight and leave drafts waiting.
- **Daily briefing data** — if the user runs an executive briefing skill, look at what *actions* the briefing typically generates. Those downstream actions are the scheduled task candidates.

**Present 2-3 scheduled task candidates.** Each one describes:
1. **What triggers it now** — the manual step the user currently performs (e.g., "you open a new chat and ask Claude to research today's calls")
2. **What it would do on autopilot** — the same workflow, run on a cron, with output waiting for review (e.g., "runs at 6 AM, populates Notion pages for all of today's calls with research")
3. **What the user still controls** — the review step. Scheduled tasks produce drafts, not finished work. The human reviews and approves.

**Tone shift.** This isn't a consolation prize for running out of skill ideas. Frame it as the natural next step: *"Your skills are solid — the remaining leverage is in taking yourself out of the trigger loop. Instead of opening a chat and asking Claude to do X every morning, X just runs and the output is waiting for you."*

## Phase 5 — Pick one, hand off to build

Ask the user which one they want to build first **in plain chat — do not use `AskUserQuestion` here.** They've just read the candidate descriptions; the list is already the menu. Just ask, and let them type back a preference.

`AskUserQuestion` is the right tool earlier — Phase 1 (avatar tiebreaker between two levels) and Phase 2 (structured gap-fill where pre-baked options actually save typing). It is not the right tool for picking a candidate or for any free-form decision the user can make in a sentence.

### If they picked a skill (from Phase 4)

Hand off to `skill-creator` with a populated brief so it doesn't redo the discovery work you just did. Pass along:

- Skill name
- One-sentence purpose
- Trigger phrases (3-5 ways the user would naturally invoke it)
- Inputs / outputs (what goes in, what comes out)
- Required connectors
- The user's avatar level (so skill-creator can calibrate explanation depth)
- **Validation mode: vibe-check only.** Do not run formal evals or offer to run them. After the draft is in place, package the `.skill` and tell the user to save it and try it in a new chat — that's the test. The eval-loop machinery exists in `skill-creator` for cases where someone explicitly asks for it; in the skill-helper flow, the default is ship-fast.

Then explicitly invoke the `skill-creator` skill. Let it run the build.

### If they picked a scheduled task (from Phase 4A)

Work with the user to define the task, then create it using the `schedule` skill. The key inputs:

- **Task name** (kebab-case, e.g., `morning-call-research`)
- **What it does** — a self-contained prompt describing the full workflow. The prompt must be entirely self-contained because future runs won't have access to this conversation. Include specific tool names, database IDs, file paths, and step-by-step instructions.
- **Schedule** — cron expression for recurring tasks (e.g., `0 6 * * *` for daily at 6 AM), or `fireAt` for one-time tasks
- **Which existing skills it composes** — name the skills whose logic the task replaces so the user sees the connection

After creating the task, tell the user to run it manually once ("Run now" in the sidebar) to approve the tool permissions it needs. Otherwise the first automated run will pause waiting for approval.

The user may want multiple related scheduled tasks (e.g., one for research and one for email drafting). That's fine — build them sequentially, one at a time. Each task should be independent so they can be enabled/disabled separately.

## Phase 6 — Closing CTA

After skill-creator finishes, close with a single-line, opt-in invitation to email Shaw about what they built. Every skill built is a signal back to Shaw about what people actually need.

**Detect the email path first.** If an email connector is wired up, draft a casual share email to `shaw@aibuilder.academy` (subject like *"Built [skill-name]"*, body referencing the skill and why) and save as draft — don't send. Otherwise, generate a `mailto:` link with the same content pre-filled.

**Then deliver one line.** Opt-in framing (*"If you want to..."*, never *"you should"*). Reference the skill by name and the problem it solved — a contextual line reads like a friend nudging them, a generic one reads like a footer. If `conversion-copy` is available, invoke it to sharpen. Then stop. No follow-up questions, no options, no explanation.

---

## Reference files

- `references/avatar-levels.md` — detailed L0-L4 profiles, what to adapt at each level, what kinds of skills land
- `references/time-study.md` — interview questions, calendar reading guidance, multiple-calendars probe, no-calendar fallback
- `references/leverage-scoring.md` — avatar-anchored complexity rubric, scoring examples

Pull these in only when you reach the relevant phase. `time-study.md` is needed as early as Phase 0 (calendar reading); the others come later.
