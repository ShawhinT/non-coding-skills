# Workflow 2: Status Transitions

**Triggers:**
- First session of an engagement happens (Sold → Active)
- Last session of an engagement happens (Active → Delivered)
- A refund is issued (any status → Refunded)
- An engagement stalls 30+ days with no booked next step (Active → On Hold)
- "Mark X as delivered" / "Wrap up X's engagement" / "X just had their first session"

**Goal:** Flip Status to reflect the engagement's true state, and fill in any related fields
(End Date on Delivered, 4Rs at wrap).

---

## Status Flips

### Sold → Active

**Detection signals:**
- A new ABA Trainings page is created for this client (means the first session is on the
  calendar or just happened)
- Shaw says "X had their first session" / "X started"

**Steps:**
1. Fetch the engagement row
2. Update `Status` to `Active`
3. If `Start Date` is blank, set it to the date of the first session
4. Run **Workflow 3** in the same pass to add the new ABA Trainings page to the Sessions body
   section

### Active → Delivered

**Detection signals:**
- The last scheduled session in the engagement body has occurred
- Shaw says "X is done" / "wrap up X"
- For team workshops: all attendees have completed their sessions

**Steps:**
1. Fetch the engagement row
2. Update `Status` to `Delivered`
3. If `End Date` is blank, set it to the date of the last session
4. Update each linked Clients (Nurture) row — **but only hand a person off to nurture if this
   was their *last* open engagement.** Before flipping, check that row's `Engagements` for others
   still in `Sold`/`Active`:
   - **No other open engagements** → set `Status` to `Nurturing` (the client enters the quarterly
     check-in rhythm) and `Next Contact` ~3 months out per CRM follow-up guidance.
   - **Other engagements still open** (a re-up already sold, a concurrent project, near-term
     sessions still on the calendar) → keep `Status` at `Active` and set `Next Contact` to the
     next real touchpoint (the next scheduled session or call), not ~3 months out. CRM Status
     tracks the *account relationship*, not this one engagement, so a single Delivered project
     doesn't put the whole account into nurture while other work is still live.
5. Surface the 4Rs prompt to Shaw — ask whether to fill them in now (during the wrap call) or
   defer. Don't auto-fill 4Rs without Shaw's input.

### Any → Refunded

**Detection signals:**
- A refund is issued in Stripe (or Shaw says "I refunded X")
- The engagement is cancelled before delivery completes

**Steps:**
1. Fetch the engagement row
2. Update `Status` to `Refunded`
3. Update `Paid Status` to `Refunded` (or `Partial` if a partial refund)
4. Append a dated note under the `**Notes**` block inside `## Context`: `Refunded $X (M/D). [Reason if known.]`
   (Notes lives inside Context, not as its own H2 — don't create a `## Notes` section.)
5. Update the linked Clients (Nurture) row's `Status` to `Churned` if no other active
   engagements; otherwise leave as-is.

### Active → On Hold

**Detection signals:**
- 30+ days since last session with no booked next step
- Client explicitly pauses ("we need to pause for a few months")
- Shaw says "put X on hold"

**Steps:**
1. Fetch the engagement row
2. Update `Status` to `On Hold`
3. Append a dated note under the `**Notes**` block inside `## Context`: `On hold (M/D). [Reason.]`
4. Update the linked Clients (Nurture) row's `Next Contact` to a re-engagement date (Shaw's
   discretion — typically 30-60 days out)

### On Hold → Active

When delivery resumes:
1. Update `Status` back to `Active`
2. Append a dated note: `Resumed (M/D).`
3. Run **Workflow 3** to link the next session

---

## Filling in 4Rs at Wrap

When transitioning to Delivered, prompt Shaw for each R. Use `update_content` to replace each
`_TBD at wrap_` placeholder.

### Results

Concrete outcome from the engagement. Format as a short paragraph or bullet list. Examples:

```
- Built and deployed 3 Claude skills (email triage, weekly report draft, customer onboarding).
- Estimated 8-10 hrs/week saved.
- CEO using Claude daily for strategic prep.
```

### Re-up

Status of follow-on conversation:

```
Declined Intensive — happy with current scope. Will revisit Q3.
```
or
```
Re-upped into 30-Day Intensive (E024) on 5/15.
```

### Referrals

Names + outcomes:

```
Referred 2 contacts: [Person] (booked discovery 5/20), [Person 2] (sent intro email 5/22, no reply).
```

### Reviews

Testimonial status + content or page link:

```
Testimonial captured — see [linked doc](url) or:
> "Shaw's workshop saved me 10 hours a week. The skill we built is still running 6 months later."
> — [Client Name], Founder, Acme Co
```

If declined or pending: `Testimonial declined.` or `Testimonial pending — sent draft for review (M/D).`

---

## Update Pattern

Always use the explicit property update pattern:

```json
{
  "page_id": "<engagement-page-id>",
  "command": "update_properties",
  "properties": {"Status": "Delivered", "date:End Date:start": "2026-05-06"}
}
```

For body updates (4Rs), use `update_content` with exact-string `old_str` matching the placeholder.
