# Call Follow-Ups

Patterns for following up after a research call, expert network sync, or discovery call. These emails confirm alignment, provide next steps, and keep momentum.

Read this file before drafting any post-call follow-up. The named follow-up templates — and their drafting notes — live in their Notion SOPs (single source of truth). This file owns only what no single SOP carries: the cross-cutting **Structure**, the general fallback template, and two formatting nuances that aren't in the SOP notes. Everything else is a pointer; draft the actual template from the SOP.

---

## Read the transcript before drafting

For any post-call follow-up, read the meeting transcript, not just the Notion Call Notes. The transcript lives in Drive, titled like `[Name] x Shaw - ... - Transcript`; find it by searching the recipient's name. The Notion notes are a lossy summary — the shareable substance lives in the transcript: the framework or roadmap Shaw walked through on screen, the client's pains in their own words, and the one thing they explicitly asked to pick up next time. Drafting from the notes alone yields a generic nudge that misses what would actually land. This is the call-FU parallel to SKILL.md's "Find and read the actual thread before drafting" — the transcript is to a post-call FU what the Gmail thread is to a reply.

---

## Structure

Shaw's call follow-ups tend to follow this shape, though the specifics vary by type:

1. **Warm opener** — "Really enjoyed our call yesterday!" (or similar). Always genuine, never filler.
2. **Reaction** — One sentence showing Shaw was present (skip for proposal follow-ups; go straight to value).
3. **Value / recap** — The useful thing: an outline, a resource, agreed next steps. The meat of the email.
4. **Closing** — Match to the situation: "What do you think?" when you need a reply to move forward; an open door ("Let me know if any questions or blockers come up :)") when the next meeting is already booked.

**Sign-off:** "Cheers, Shaw" (these are warm, peer-level relationships post-call).

---

## What to give: explicit items first, else the artifact you showed

First look for explicit follow-up items — resources the client asked for, or next steps Shaw promised, whether listed on the Notion call page or surfaced in the transcript. Those drive the follow-up.

When there's no obvious item to hand off, the framework, roadmap, or diagram Shaw walked through live is the natural high-value give: attach that artifact and keep the body short rather than re-explaining it in prose bullets. The "resource" needn't be an external link or a formal one-pager — the thing shown on screen is the resource.

Either way, lead the short body with a diagnostic line that mirrors the client's situation back in Shaw's framework (e.g. "most of your org is still at Stage 1, i.e., they need the aha moment"). That one sentence proves you listened and frames the offer at once — it's the highest-leverage line in the email.

---

## Named templates — draft from the SOP

Each of these lives, with its full drafting note, in a Notion SOP. Don't keep a second copy of the rules here. See SKILL.md "Check Notion SOPs for templated workflows" for the SOP→template map. Quick index:

- **Workshop/Talk follow-up** → Event Series SOP ("talk follow-up").
- **Proposal follow-up** → Discovery Call SOP (post-call FU Variant A). The deal-shape bullets bold the leading category label as scan-anchors — see SKILL.md Voice → "Exception: proposal/offer follow-ups" for that rule and its HTML mechanic.
- **Post-workshop / post-training follow-up** → 1:1 Claude Workshop SOP ("1:1 Session Follow-up").
- **Check-in / multi-ask follow-up** → Check-in Call (1:1 Claude Workshop) spoke (Variant A); lighter nurture-recap version in Check-in Call (Client Nurture) spoke (Variant B). *Wrap-up nuance not in the SOP:* for a **conditional next touchpoint** (next call is real but gated on the recipient doing X first — aligning a stakeholder, filling a form, reviewing the proposal), name the dependency in plain language, then propose one specific time anyway as a forcing function rather than open-ended "let me know when you're ready." Pattern: "Let's do another call after you [dependency]. How does [day] ([Mon DD]) look for you?" See SKILL.md "Single time inline" for the date format.

---

## Template: General Call Follow-Up

**When to use:** The fallback skeleton for any call with no dedicated SOP template — research, informal coffee chat, etc. For discovery calls, use the Discovery Call SOP's two post-call FU variants instead.

**Subject line:** "Call follow-up"

**One next step → keep it prose:**

```
Hey [First Name],

Really enjoyed our call [yesterday/on Thursday/etc.]!

[COMPLIMENT — one sentence reacting to something specific from the call]

[VALUE — the one resource, agreed next step, or info you promised to send]

[CLOSING QUESTION — one question to move things forward]

Cheers,
Shaw
```

**Two or more next steps → use bullets (the session-FU shape).** When the call leaves more than one concrete thing to hand off (book this, set up that, try this skill), put them in a short verb-first bulleted list instead of threading them through paragraphs. Buried action items are the failure mode — the reader should see the asks at a glance.

```
Hey [First Name],

Really enjoyed our [call/coffee chat] [yesterday/on Thursday/etc.]!

Here are a couple of next steps:
- [Verb-first action, e.g. Book the 1:1 here (link)]
- [Verb-first action, e.g. Set up the some-skill skill with this prompt for Claude: "..."]

[Open-door close, e.g. Let me know if any questions come up :)]

Cheers,
Shaw
```

Cap at ~3 bullets, each starting with a verb; skill names lowercase kebab-case and bolded. One CTA still leads — the extra bullets are gives (resources), not competing asks.

---

## Threading and batch

- **Threading:** reply on the existing thread per SKILL.md "Drafting with `create_draft`"; fresh thread when the live thread ends in a reaction per SKILL.md "Gmail emoji reactions break thread replies." Subject: "Call follow-up" for first/standalone calls, "Check-in Follow-up" for subsequent touchpoints in an ongoing engagement.
- **Batch:** see SKILL.md "Batch Outreach Workflow" — one consistent template, present it to Shaw before creating drafts, only customize the name + compliment + status-quo parenthetical.
