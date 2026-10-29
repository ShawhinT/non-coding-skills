# Channel: Cold Outreach / DMs

Cold emails and LinkedIn DMs to people who don't know Shaw — partnerships, research calls, podcast pitches, event invites, offer pitches. Warm contacts → `channel-emails.md`. Campaign orchestration (sourcing, enrichment, trackers, logging) → the `outreach` skill; this file owns the message.

Lock before drafting: the target cohort, the specific shared need, the lowest-friction next step, and which playbook fits.

## Shared principles

A new playbook that violates one of these needs an explicit argument for why.

1. **Target a tight cohort, not a broad list.** "VPs of marketing at B2B SaaS companies who've hired in the last 90 days" gives you a shot; "marketers" doesn't. A tight cohort lets one message hit many recipients; a broad list forces generic slop.
2. **First line = preview text = opens.** What you avoid matters more than what you use: "I hope this email finds you well," "thanks for connecting," "I'd love to add you to my network" are instant deletes. Two ways to escape the template read: a reference specific to *them*, or disarming honesty about being cold ("I know this is random, but…").
3. **Personalization never disappears — it moves.** Bespoke outreach personalizes to the individual (their post, their news); scaled outreach personalizes to the cohort (a problem statement so specific it reads as "this person knows my job"). Generic copy to a generic list is the one unforgivable combination.
4. **Three to five lines.** Longer and they read two lines and archive.
5. **The CTA is a permission ask, not a meeting ask.** "Quick 15-minute call?" is the most-used and least-effective CTA in cold outreach — the ask is too big for zero trust. In ascending order: reply-only ("worth me sending a 2-minute Loom? just reply 'yes'") → one-click → low-time ("worth a 10-min chat? if not, no worries") → a call, only after they've reciprocated.

## Choosing a playbook

| Condition | Advice-frame | Uptown method |
|---|---|---|
| List size | Tens | Hundreds+ (e.g. 200 requests/wk) |
| Per-prospect research | Affordable (30 sec–5 min) | Not affordable — cohort does the targeting |
| Per-prospect hook | Yes (their post, their news) | No — shared cohort pain instead |
| Optimizing for | Hit rate per message | Split-testable reply data on a fixed template |
| Trust posture | Value before pitch | Upfront "pitch slap" — name who you are and why |

Shaw's per-prospect scripting workflow in `outreach` (templated base script + personalization menu) is a middle position: Uptown-style body, advice-frame opener. Don't mix playbooks mid-campaign — editing a scaled template per send destroys the test data; templating a bespoke message wastes the research.

## Playbook: Advice-frame (Harry Dry / Ryan's "1000 replies")

**Proven in:** small-batch cold email where each message could be hand-researched. AndCo's advice email saw 65% CTR and 55% reply rate vs. <5% for typical pitch emails.

Lead with a genuine observation or question and offer something useful before asking for anything. This only works if you're actually willing to help whether or not they buy — Ryan's test: *"Find 100 people you can help. Offer to help them for free. Blow them away."* If the draft wouldn't pass that, rewrite it.

Personalization costs 30 seconds, not 30 minutes: one specific thing from their latest post, recent company news, or about page.

**Structure:** subject ("[First name] — one question" / "Your post about X") → opener referencing them → the observation or offer → reply-only CTA → "— Shaw". DMs drop the subject and run shorter.

**Worked example — cold DM to a founder who posted about being the bottleneck:**

> Saw your post last week about being the bottleneck for every deliverable. That Friday night review hell is literally why I stopped doing client delivery myself.
>
> I work with owner-operators on exactly that problem — usually shave 10–15 hours a week off the review cycle in the first month.
>
> Want me to send a 3-minute Loom of how it worked for the last client in your shoes? No call — just tell me if it's useful.
>
> — Shaw

## Playbook: The Uptown method (pattern-disrupt / "pitch slap")

**Proven in:** Sales Navigator campaigns at ~200 connection requests/week against cohorts filtered for active LinkedIn users. Their pharmacy-tech campaign: ~3,000 requests → 35% accepted → 219 replies → 49 positive → 24 meetings → 11 closed → ~$400k in under 6 months. These are the seller's own case studies — treat the numbers as directional; the structural logic is what transfers.

The philosophy: the most respectful cold message names the elephant — who you are and why you're writing — instead of manufacturing fake warmth. The template stays rigid *on purpose*; one skeleton with one variable slot produces clean split-test data.

**Three sentences:**
1. **Pattern disrupt + problem statement.** "I know this is random, but I'm chatting with [role] who [specific pain]." The disrupt earns the open; the problem statement is both the personalization and the thesis you're testing.
2. **The "at a high level" line.** "At a high level, we [do X via Y] — typically [quantified result]."
3. **CTA mirroring sentence one.** "Would it be all right if I shared a few ideas to [the exact problem you named]?" People skim, so the problem appears first and last.

> I know this is random, but I'm chatting with pharmacy leaders who see technician payroll climbing as script volume grows. At a high level, we help pharmacies deploy AI agents to help prescription data entry, fax processing, and insurance workflows — typically saving $300–500k in technician wages. Would it be all right if I shared a couple ideas to keep your technicians focused on patient-facing work instead of being glued to a screen?

Only the problem statement and mechanism line are custom per campaign; everything else is scaffold. Split-test the **problem statement only**, every 1–2 weeks early on, then freeze the winner. Pain tied to *revenue* outperformed pain tied to activity. Silence means targeting or messaging is off — if the cohort is confirmed right, change the message.

**Follow-up ladder:** M2 "forgot to mention" (proof point + CTA) → M3 bare nudge ("Thoughts, [FirstName]?") → M4 loose breakup (reframe to a different pain, then an explicit out: "seems like my timing is off… let me know if I'm completely off base"). Cadence: ~4 messages month one, ~3 more across year one, ~4/year ongoing.

**Adding playbooks:** same template — source and proven context (with an honesty note on evidence quality), the discriminating "best when" conditions added to the chooser, structure, what to test. Check new playbooks against the shared principles rather than rewriting them.

## Follow-ups (both playbooks)

A follow-up is a lighter touch than the message before it — the ladder should feel like it's winding down, not repeating.

- **The first follow-up carries the proof.** Don't "just check in" — that adds pressure without a reason. Move the credibility line from the original ask into the nudge ("this is the same framework I've taught to 30+ leaders 1:1").
- **Don't re-drop a link already in the thread.** It's one scroll up; repeating reads as automated. Re-include only when it's a fresh CTA and the earlier one has scrolled away.
- **Each rung gets terser.** The last nudge is a one-liner tied to a deadline ("we go live Friday") — drop the greeting and sign-off in a familiar thread.
- **The last touch changes the angle and gives an out.** A fast no frees the list for people who'll say yes.

## Voice cues

Casual, first-name basis, "— Shaw" as the only sign-off, no signature block. If a batch template has a {merge field}, it should require real research to fill — otherwise it's a form letter in costume. (In the Uptown method the cohort-level problem statement satisfies this by construction, but both custom slots still have to sound like Shaw, not a SaaS homepage.)
