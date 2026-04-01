# Follow-Up Rules & Drafting Guidance

Apply these rules during CRM review or whenever Shaw mentions a lead's status.

---

## Contact form lead cadence

For any inbound contact form lead (ABA Contact, ABB, etc.), follow this cadence regardless of
what was discussed in the reply (pricing, call offer, info, etc.):

| Step | Timing | Template |
|---|---|---|
| Initial reply | Same day as form submission | — |
| FU #1 | 2–3 days after initial reply, no response | Short direct question: *"Did you get a chance to look at this?"* |
| FU #2 (final) | 2 weeks after initial reply, no response | One-liner, no greeting, no sign-off: *"Have you given up on this?"* |

**FU #2 formatting:** This is literally just the single line "Have you given up on this?" — no "Hey [Name],"
no sign-off, no "-Shaw". Just the question by itself. It's intentionally blunt and short.

After FU #2 with no response, stop following up.

## B2B pipeline follow-ups

| Situation | Trigger |
|---|---|
| Booking link sent or time proposed, no response | ~3 days since `Last Contact?` |
| Outline/proposal sent (`Outline Sent`), no response | ~5 days since `Last Contact?` |
| Notes contain an explicit future FU date (e.g. "FU in April") | That date has arrived or passed |

## When NOT to draft a follow-up

- Lead is LinkedIn-only (no email to draft to)
- Notes contain a future FU date that hasn't arrived yet
- Status is `Closed` or `Lost`
- Lead responded recently and conversation is active

---

## How to draft follow-ups

**Default behavior: create Gmail drafts directly.** Do not present draft options to Shaw for
review unless the situation is genuinely ambiguous (e.g., unclear whether to follow up at all,
or unclear tone for a sensitive deal). For routine follow-ups, just draft them in Gmail and
report what was drafted in the summary.

1. Read the full Gmail thread to understand tone and context
2. Draft a short, casual reply in the existing thread — match Shaw's voice (direct, friendly, low-pressure)
3. **Self-check before finalizing:** verify the last sentence is a question, not a statement.
   If it ends with "let me know," "happy to help," or any passive closer, rewrite it as a question.
4. Create the draft using `gmail_create_draft` with the `threadId` of the existing thread.
   For Gmail formatting details (HTML structure, emoji reaction handling), see the **email-writer** skill's Gmail Technical Notes.
5. Update the lead's CRM Notes to reflect the follow-up: e.g. `FU (3/18).`
6. Call it out clearly in the summary report under **"Follow-ups due"**

**Never create a replacement draft without deleting the old one first.** If a draft needs to be
redone (e.g., wrong formatting, wrong template), ask Shaw to delete the old draft before creating
a new one. Creating two drafts in the same thread causes a real problem: when the email is sent,
Gmail sees the unsent draft as a "duplicate" message in the thread and hides the actually-sent
email by default. The recipient gets it fine, but Shaw can't see it in his sent view without
expanding hidden messages — which looks broken and is confusing.

**Always end follow-ups with a question, not a statement.** Questions create a response obligation;
statements and commands ("let me know", "happy to help") are easy to ignore. Examples:
- Good: *"Did you get a chance to look at this?"*
- Good: *"Is this still something you're interested in?"*
- Bad: *"Let me know if you have any questions."*
- Bad: *"Happy to help if you need anything."*

---

## Tone guidance from observed examples

- Contact form FU #1: *"Did you get a chance to look at this?"*
- Contact form FU #2: *"Have you given up on this?"* (no greeting, no sign-off — just this one line)
- Scheduling: *"Would [day] at [time] work?"* or *"Is [tomorrow] a bad time?"*
- Casual re-engagement: *"Is [tomorrow] a bad time? Happy to work around your schedule if you think this is worth pursuing :)"*
- Never pushy; always leave the door open

---

## Lead source context for drafting

When drafting follow-ups or replies, adjust approach based on the lead's source:

- **ABB** (Bootcamp alums) — warm relationship; Shaw already knows them. Tone is peer-level,
  casual. They may be interested as a client, a partner, or just staying in touch — don't assume.
- **ABA Contact** (inbound contact form) — interested but cold; they reached out but have no
  prior relationship. Tone is friendly but slightly more structured. Follow the contact form
  cadence strictly.
- **YouTube / Organic** — they know Shaw's content but haven't worked with him. Warmer than
  cold outreach but still need to build trust. Reference shared context where possible.
- **LinkedIn** — often exploratory; may be looking for partnership, consulting, or just networking.
  Clarify intent early rather than assuming they want training.
- **Personal** — existing relationship. Match whatever tone the relationship has.
