# Call Follow-Ups

Patterns for following up after a research call, expert network sync, or discovery call. These emails confirm alignment, provide next steps, and keep momentum.

Read this file before drafting any post-call follow-up email. Most named follow-up templates now live in their Notion SOPs (single source of truth) — this file owns the cross-cutting **Structure**, the general fallback template, threading, and batch mechanics, and points to the SOP for each codified template.

---

## Structure

Shaw's call follow-ups tend to follow this shape, though the specifics vary by follow-up type:

1. **Warm opener** — "Really enjoyed our call yesterday!" (or similar). Always genuine, never filler.
2. **Reaction** — One sentence showing Shaw was present. This takes different forms depending on context: for talk/event follow-ups where someone pitched an idea, use "Loved your [concise 3-4 word description]." For post-training or post-workshop follow-ups, a genuine reaction to how the session went works better (e.g., "I'm glad we were able to make it through a full loop of the framework"). For proposal follow-ups, skip this entirely and go straight to the value.
3. **Value / recap** — Provide something useful: a talk outline, a resource, a summary of what was agreed, or suggestions for next steps. This is the meat of the email.
4. **Closing** — Match the closing to the situation:
   - **Need a reply to move forward** (talk direction, proposal review): "What do you think?"
   - **Next meeting already booked**: open door — "Let me know if any questions or blockers come up :)"
   - **Multi-ask check-in FU**: one-line gracious wrap-up — see Check-in / Multi-Ask Follow-Up template for the two variants (forward-looking vs reciprocity).

**Sign-off:** "Cheers, Shaw" (these are warm, peer-level relationships post-call).

---

## Workshop/Talk Follow-Up

**When to use:** After a call where Shaw and an event-series partner agreed on a talk topic. Confirms the direction and shares a narrative outline structure.

**Template lives in the Event Series SOP** (below the `---` divider, "talk follow-up"). Draft from there — the SOP's drafting note covers the personalization rules: keep the compliment to a 3-4 word reaction to their *idea* (not their credentials), and name their specific domain in the status-quo parenthetical. The talk outline is a bulleted list — one of the allowed exceptions to the "no bullet points" rule.

---

## Proposal Follow-Up

**When to use:** After a discovery/sales call where the next step is sending a proposal or outline PDF.

**Template lives in the Discovery Call SOP** as Variant A of the post-call FU. Draft from there.

**Key principle:** Keep the email body short. The proposal PDF carries the detail — don't re-explain workshop content, use cases, or session breakdowns in the email. The bullets just convey the shape of the deal (format, delivery, price) before the recipient opens the attachment.

**Optional P.S. line:** If the recipient mentioned needing supporting docs for internal approval (e.g., a CV for L&D submission), add a `P.S.` noting the extra attachment.

---

## Template: General Call Follow-Up

**When to use:** The fallback skeleton for a sales or research call with no dedicated SOP template. For discovery calls specifically, use the Discovery Call SOP's two post-call FU variants (proposal vs. resources) instead.

**Subject line:** "Call follow-up"

```
Hey [First Name],

Really enjoyed our call [yesterday/on Thursday/etc.]!

[COMPLIMENT — one sentence reacting to something specific from the call]

[VALUE — recap of agreed next step, resource, or info you promised to send]

[CLOSING QUESTION — one question to move things forward]

Cheers,
Shaw
```

---

## Post-Workshop/Post-Training Follow-Up

**When to use:** After Shaw has delivered a 1:1 workshop or training session — recap what was covered, suggest what to build next, point to the upcoming check-in.

**Template lives in the 1:1 Claude Workshop SOP** ("Call follow-up", below the `---` divider). Draft from there.

**Key principles:**
- Frame next steps as *suggestions*, not a committed plan. Peer tone, not PM tone.
- Cap at ~3 items. Even if the session notes list more, pick the highest-leverage ones.
- Every bullet starts with a verb: Create, Improve, Build, Try, Keep improving.
- Skill names are lowercase kebab-case and bolded: *slack-helper*, *finance-reporting*, *weekly-summary*. Never Title Case or camelCase.
- No session reaction line — go straight from the warm opener to the suggestions intro. (Shaw dropped the reaction line in his most recent sends; if session notes have a standout moment worth calling out, it can be fused into the opener.)
- No "What do you think?" — the check-in is already on the calendar, so use an open door instead of forcing a reply.
- Include the P.S. with the skill-helper Google Drive link.

**Examples of what suggestion bullets look like (from real sent emails):**
- "Improve the *ssc-lbo-model* skill by manually reviewing its output and giving Claude feedback"
- "Create a *calendar-helper* skill based on the existing chat where Claude helped you prioritize your week"
- "Create a *slack-helper* skill by having Claude research your Slack channels so it can navigate them more effectively in the future"

---

## Check-in / Multi-Ask Follow-Up

**When to use:** After a subsequent touchpoint in an ongoing engagement — a post-session check-in, or any post-engagement call carrying multiple distinct asks (next steps + review + referral).

**Template lives in the Check-in Call SOP** as Variant A of the post-call FU (Variant B is the lighter nurture-recap version). Draft from there.

**Key principles:**

- **Section labels match the content.** Use *Next Steps* when committing to action, *New skill ideas* when offering options. Same shape, different label.
- **Cap at 3 body sections by default, 5 max.** See SKILL.md "Shaw never pads for length."
- **Skill bullets describe what Claude does** — "*fireflies* skill to have Claude help with workflows involving meeting transcripts" beats "Fireflies skill (auto-extract action items)." Verb- and value-first, not feature-first. Skill names are always lowercase kebab-case and bolded. Only relevant when the section is skill suggestions.
- **Proposal sections pull the headlines inline.** When one of the asks is "share the outline" or "send the proposal," that section should use the Proposal Follow-Up bullet pattern — format, scope, investment — not just gesture at the attachment. The body has to be readable without opening the PDF. When the call notes prescribe a specific starting point ("start with rev function, pick 3 teams"), prefer surfacing it as flexibility ("can be company-wide or function-wide e.g. RevOps only") over pre-committing the recipient.
- **The wrap-up matches whether the next touchpoint is locked in.** Pick one:
  - **Next touchpoint scheduled:** "Thanks again for taking the time to go through this with me. Looking forward to our [call/session] [when]."
  - **No next touchpoint scheduled:** "Thanks again for taking the time to go through this with me. Please let me know if there's ever any way I can support you or [Company]."
  - **Conditional next touchpoint** (next call is real but gated on the recipient doing X first — aligning with a stakeholder, filling out a form, reviewing the proposal): name the dependency in plain language, then propose one specific time anyway as a forcing function. Don't default to open-ended "let me know when you're ready" — it slows the deal and puts scheduling work on the recipient. Pattern: "Let's do another call after you [dependency]. How does [day] ([Mon DD]) look for you?" See SKILL.md "Single time inline" for the date format.

---

## Threading Rules

- **Default:** Reply on the existing email thread — see SKILL.md "Drafting with `create_draft`" for the `replyToMessageId` mechanics.
- **Emoji-reaction fallback:** See SKILL.md "Gmail emoji reactions break thread replies" — fresh thread when the live thread ends in a reaction.
- **Subject line:** "Call follow-up" for first/standalone calls. "Check-in Follow-up" for subsequent touchpoints in an ongoing engagement (e.g., 30-day check-ins after a prior workshop). Same convention whether threaded or fresh.

---

## Batch Follow-Ups

When following up with multiple people after calls (e.g., after a day of back-to-back research calls):

- **Use a consistent template.** Don't force variation across recipients. The same structure with swapped personalization is better than 5 different email styles.
- **Only customize:** the greeting name, the compliment line, and the status quo parenthetical in the outline.
- **Present the template to Shaw first** before creating drafts, so he can approve the structure and tweak wording. Then batch-create all drafts at once.
