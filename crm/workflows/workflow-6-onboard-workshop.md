# Workflow 6: Onboard Workshop Participant

Use when a new participant books or is accepted for a 1:1 Claude Workshop (free lead-gen
session or paid) and needs to be set up in the system.

Onboarding has two halves. The **session setup** — ABA Trainings page, daily Precall/FU tasks,
the bidirectional FU link, welcome + pre-session emails, pre-call research — is owned by the
**1:1 Claude Workshop SOP**. That SOP is the single source of truth; follow it rather than
re-deriving the steps here (they drift otherwise). This workflow owns only the **CRM side**:
resolving which record tracks them. The two halves connect via a `## Calls` link on that record.

## 1. Run the 1:1 Claude Workshop SOP for the session setup

Follow the 1:1 Claude Workshop SOP (`notion-helper` discovers it at runtime by fetching the
SOPs page and matching on title — no hardcoded ID). In order, it covers: the ABA Trainings session
page (`collection://[page-id]`, `Name` = `"[First Name] - 1:1 Claude
Workshop"`, `Date` = session date), the two ABA daily tasks (`Precall - [First Name]` the day
before and `FU - [First Name]` the day after, both with the ✉️ icon), the bidirectional FU link
under the session page's **Next steps**, the welcome email (desktop app + intake), pre-call
research, and the pre-session agenda email 24h out. Every email routes through **email-helper**.

**Free vs paid.** The SOP is written for the paid session. For a *free* 1:1 workshop, run the
same steps but **skip the two paid-only ones — the Stripe invoice and the engagement row**.
There's no engagement to track until they buy — and no assumption that they're a lead; step 2
resolves where they're tracked. (The free workshop is still a designed feeder: note any
employer/team expansion signals on the session page so a paid opportunity isn't missed.)

Do **not** link the session anywhere other than the spots the SOP prescribes — in particular not
the stale April "Free Claude Automation Workshop 1:1" parent page (a one-off round page, not a
living index).

## 2. Resolve the CRM record

A free workshop is a *session*, not a pipeline stage — it doesn't decide where someone is
tracked. So the first move is finding the record that already owns the relationship, not
creating one. Search **Active Leads, Clients (Nurture), Friends, Archived Leads, and every
campaign tracker** by name fragment *and* email domain, with a global `notion-search` as a
backstop — see "A clean search in one database only proves absence *there*" in `SKILL.md`.

**They already have a record** → update it in place. Log the booking in Notes, move
`Next Contact` to the session date, and link the ABA Trainings session page under `## Calls`.
This is the common case for collab-driven free workshops, which go to people already sitting in
Friends as a `Channel` or `Partner`. Adding an Active Lead alongside that record forks the person
into two live `Next Contact` dates with two syncs independently drafting at them — the exact
failure "one person, one next touch" exists to prevent. If the existing record is a genuinely
poor fit for what the relationship has become, that's a **retype or a move**, not a second row;
surface it to Shaw rather than resolving it by creating.

**Nobody has a record** → create an Active Lead in
`collection://[page-id]`. Pull the name, email, and timeline from the
Calendly booking and any Gmail threads. Status: `Booked Call`.

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
session pages are the pattern to follow.
