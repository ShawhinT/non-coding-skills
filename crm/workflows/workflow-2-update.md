# Workflow 2: Update a Lead

Use when Shaw shares new info about a lead (reply received, call happened, proposal sent, etc.).

1. Fetch the lead's current Notion page to read existing notes and properties
2. Cross-reference before writing — compare what Shaw said against the existing notes. Shaw
   often recaps recent activity as context alongside a genuinely new update (e.g. "I responded
   to [Lead Name]" might refer to something already logged). If the activity looks like it's already
   captured in the notes, confirm with Shaw before appending (e.g. "Looks like your reply to
   [Lead Name] on 3/30 is already in the CRM — anything new to add?"). Only append entries that
   represent new information not yet in the log.
3. Determine what changed: new activity, status change, or both
4. Update properties:
   - Append to Notes (never overwrite)
   - Update `Last Contact?` to today's date if a new touchpoint occurred
   - Update `Next Contact` to the next planned touchpoint — use cadence defaults from
     `references/follow-up-guidance.md` (e.g., reply sent → +2–3 days; proposal sent → +2 days;
     call scheduled → the call date; explicit future FU date → that date; marked Lost → +6 weeks
     unless context suggests a longer window). Never leave it blank for an active lead or
     stale in the past. For `Closed` leads about to graduate via Workflow 5, skip — Workflow 5
     sets `Next Contact` on the new Clients record.
   - Update `Status` if the pipeline stage has advanced
5. Prompt for follow-up email — If the update includes a call or meeting that happened today
   (or yesterday), ask Shaw whether he'd like a follow-up email drafted. If yes, use the
   email-helper skill's call follow-up reference (`references/call-follow-ups.md`) to draft it.
   If Shaw already requested a follow-up email as part of the same message, skip the prompt and
   draft it directly. When you draft the email, do NOT also bump `Status`, `Last Contact?`, or
   `Next Contact` to reflect the email's send — drafts aren't touchpoints. Step 4's CRM update
   should reflect only what actually happened (e.g., the call). The drafted email's send-state
   gets picked up later, either when Shaw confirms send or on the next Workflow 1 sync. See
   "Drafts aren't touchpoints" in SKILL.md.
6. Confirm the update to Shaw with a brief summary
