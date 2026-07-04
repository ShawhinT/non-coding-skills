# Workflow 6: Onboard Workshop Participant

Use when a new participant books or is accepted for a 1:1 Claude Workshop (free lead-gen
session or paid) and needs to be set up in the system.

Onboarding has two halves. The **session setup** — ABA Trainings page, daily Precall/FU tasks,
the bidirectional FU link, welcome + pre-session emails, pre-call research — is owned by the
**1:1 Claude Workshop SOP**. That SOP is the single source of truth; follow it rather than
re-deriving the steps here (they drift otherwise). This workflow owns only the **CRM side**:
the Active Lead record. The two halves connect via a `## Calls` link on the CRM page.

## 1. Run the 1:1 Claude Workshop SOP for the session setup

Follow the 1:1 Claude Workshop SOP (`notion-helper` discovers it at runtime by fetching the
SOPs page and matching on title — no hardcoded ID). In order, it covers: the ABA Trainings session
page (`collection://[page-id]`, `Name` = `"[First Name] - 1:1 Claude
Workshop"`, `Date` = session date), the two ABA daily tasks (`Precall - [First Name]` the day
before and `FU - [First Name]` the day after, both with the ⭕ icon), the bidirectional FU link
under the session page's **Next steps**, the welcome email (desktop app + intake), pre-call
research, and the pre-session agenda email 24h out. Every email routes through **email-helper**.

**Free vs paid.** The SOP is written for the paid session. For a *free* 1:1 workshop, run the
same steps but **skip the two paid-only ones — the Stripe invoice and the engagement row**. A
free participant is a lead, not yet a paying client, so there's no engagement to track until
they buy. (The free workshop is still a designed feeder: note any employer/team expansion
signals on the session page so a paid opportunity isn't missed.)

Do **not** link the session anywhere other than the spots the SOP prescribes. Earlier guidance
here pointed at a "Free Claude Automation Workshop 1:1" parent page's Sessions list — that was a
one-off April-round page, not a living index, so don't add new bookings to it.

## 2. Create the CRM Active Lead

Create an Active Lead in `collection://[page-id]`. Pull the name,
email, and timeline from the Calendly booking and any Gmail threads. Status: `Booked Call`.

**Source:** infer it from how they came in and how Shaw knows them — `ABB` for bootcamp alums,
`ABA Discovery Call` for a direct Calendly booking with no prior relationship, `Personal` for
someone Shaw knows personally, `YouTube` / `LinkedIn` / etc. as the signal indicates. If it's
genuinely unclear, **ask Shaw** rather than guessing or defaulting to one.

Notes: log only the trigger in short `(M/D)` format (e.g., `Booked 1:1 Claude Workshop 6/12 via
Calendly (6/7).`) — see the Notes Format rules in `SKILL.md`. Set `Last Contact?` to the booking
date and `Next Contact` to the session date. In the page body, add a `## Calls` section linking
the ABA Trainings session page.

## Reference: existing participants to match

Look at how [Client Name] and [Client Name] are set up — their CRM entries and ABA Trainings
session pages are the pattern to follow. (Ignore any links to the stale April parent page.)
