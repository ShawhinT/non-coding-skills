# Review Track — Ask & Form Processing

Statuses touched: `Not Asked` → `Asked` → `Form Submitted`. Approval and beyond live in
`testimonial-approve.md`. Cadence and templates live in the Testimonial Ask SOP.

## 1. Open a review ask

**Trigger:** a training wrapped (paid or unpaid), an engagement was just created (placeholder
rows for every participant open at engagement creation — `engagements/workflow-1-create.md`
owns that step), or Shaw says "open a testimonial ask for [Name]" / "kick off testimonials
for the cohort".

Placeholder rows: partial names fine (tag with company, e.g. `[Person] ([Company])`), Email can
be blank, Review Status stays `Not Asked` until the ask actually goes out. Fill in details
when the participant list arrives.

1. **Find where they belong.** Their company in Companies (by email domain, then name) →
   `Company`; or their Friends row, for someone in the non-lead network → `Friend`. Then
   their **own** CRM row, if they have one (`notion-search` Clients (Nurture), Active Leads,
   Archived Leads) → `CRM`. Most session participants have a company and no CRM row of their
   own; that is the normal shape, not a gap to fill by pointing `CRM` at the buyer.
2. **Find their Engagement** (paid work only; otherwise leave the relation empty).
3. **Create the row** (`notion-create-pages` against the data source in SKILL.md): Name,
   Email, Company or Friend (JSON array), CRM (plain URL, only their own row), Engagement
   (JSON array, only if found), Review Status `Not Asked`, Referral Status `Not Asked`. The properties in SKILL.md's cheat sheet are the full set;
   the connector rejects the whole create if a key it doesn't know is passed.
   **Seed a `## Context` section in the body in the same call** — a row created blank stays
   blank, and the guidance has nowhere to land months later when the ask finally goes out.
   Two bullets are enough at creation: the channel the person replies on with its evidence,
   and the win from the session a review ask would anchor on (pull it from the training page
   or transcript). Everything else accretes as the tracks run. Shape per
   `../crm/references/context-sections.md`. A placeholder row with no session yet gets the
   heading and a single bullet naming what's still unknown.
4. **Hand off to `email-helper`** for the Initial Ask per the SOP (training-specific variant
   if one exists). Pass the row URL + the `forms.gle` URL for the training type (1:1 form for
   individual workshops, ABA Training form for group/team).
5. **After the send:** Review Status → `Asked`, Last Contact = send date, Next Contact per
   the SOP cadence.
6. **Take the next touch.** Open the sibling record (the `CRM` row, or the `Friend` row),
   clear its Next Contact, append to its Notes: `Next touch owned by Reviews/Referrals, due
   M/D.` This is what makes "one person, one next touch" real — without it the sweep's
   collision check is only a backstop. A participant with no sibling record skips this step.

## 2. FU stages

The sweep (`sync.md`) detects due rows and maps days-since-Last-Contact to FU1-FU3 per the
SOP cadence. Every FU send: Last Contact = send date, Next Contact per the SOP, Review
Status stays `Asked`. Any non-terminal reply restarts the cadence. Post-FU3 silence and
active declines → `testimonial-approve.md` § Decline.

## 3. Process a form submission

**Trigger:** detected by the sync reconcile, or Shaw says "polish X's testimonial" /
"process today's form submissions". A submission ends the FU cadence — process it, never
nudge past it.

1. **Read the response sheet** (Drive `read_file_content` on the sheet ID; rows keyed by the
   Name column). Pull the verbatim Before / Impact / Worth It / Permission.
2. **Polish into 3 variants** per `references/polish-framework.md` (voice rules, attribution
   by permission level, worked examples).
3. **Update the row** (atomic): Review Status → `Form Submitted`, Last Contact = the
   submission Timestamp (not today), and append to the body a `## Form Response` section
   with the verbatim + a `## Drafts` section with the 3 variants (`insert_content`).
4. **Hand off to `email-helper`** for the Approval Ask (fresh thread, "Your testimonial")
   with the chosen variant.

Orphan submissions (no matching row): match against the full database including terminal
rows first — a hit on a `Published`/`Declined` row means it's already handled. Only a name
appearing nowhere is a true orphan: surface it, then open a row via §1.

## 4. Pre-drafted testimonials (FU2 path)

**First confirm there's no form submission** (run the sync reconcile or read the sheet
directly) — a submitted form supersedes a pre-draft.

Ground the Before/After in primary records:

- **Intake form** — via `google-drive-helper`; the time-spend columns are the quantified
  before-state.
- **Session + check-in pages** — the person's ABA Trainings / ABA Calls pages
  (`notion-search` for "[Name] - 1:1 Claude Workshop" / "[Name] - Check-in").
- **Transcripts** — Meet Recordings folder in Drive; highest fidelity. Read *their* lines,
  not just Shaw's.

The check-in is where you learn whether the build stuck — draft to what's true there. If
results are thin or no intake exists, go approach/mindset-focused or hold the ask.

**Every beat traces to something the client actually said.** Two drift modes: inventing the
half they never stated (they gave the before but not the after → keep the after
qualitative), and amplifying their language ("so nice to have" ≠ "such a relief"). If your
draft carries a stronger claim or feeling than the source, pull back.

**Save the sent pre-draft on the row:** after the FU2 goes out, append the exact sent quote
(read from sent mail — Shaw tightens on the way out) as `## Pre-Drafted (FU2, sent M/D)`.
A "yes, go ahead" then promotes straight to Approved without reconstructing the quote.
