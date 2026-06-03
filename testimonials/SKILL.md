---
name: testimonials
description: >-
  Manage Shaw's testimonial workflow — create rows in the Testimonials database, polish form submissions into pull-quotes, advance status through the lifecycle (Asked → Form Submitted → Approved → Published), and surface rows that need a follow-up nudge. Use this skill whenever Shaw mentions a testimonial — "did the client approve?", "polish their response", "draft a testimonial from a form submission", "kick off testimonial asks for a team", "check which testimonials are stuck", "publish a client's quote on the site", "process the new form submissions". Also fires when a training wraps and a testimonial ask should be queued, or when Shaw says he's ready to publish. Trigger words: testimonial, pull-quote, review, social proof, form response from a client. Do NOT use for the SOP itself (sop-helper), generic CRM work (crm), pre-call context (pre-call-research), or referral asks (the Referral Ask SOP covers that).
---

# Testimonials Skill

Manages the **Testimonials** database in ABA (Master) and handles the polish step
that turns raw form responses into pull-quotes. Companion skill to the
[Testimonial Ask SOP](https://www.notion.so/[page-id]) —
the SOP carries cadence, status definitions, email templates, and policy decisions.
This skill carries the mechanics: database IDs, payload shapes, polish framework,
and skill composition. When a question is about *what to do or when*, the SOP
answers it. When it's about *how to do it in Notion / Drive / payloads*, this skill
answers it.

## Where Testimonials Live

| Thing | ID / URL |
|---|---|
| Testimonials database (page) | `[page-id]` |
| Testimonials data source | `[page-id]` |
| Database URL | https://www.notion.so/[database-id] |
| Testimonial Ask SOP | `[database-id]` |

### Form response sheets (Google Drive)

Both forms share the same 4-question spine: Before → Impact → Peer recommendation
("Worth it?") → Permission. The 1:1 form is per-individual; the ABA Training form
is for group/team trainings (phrasing nods to "the team" and "the business").

| Form | Form ID | Response sheet ID | Columns |
|---|---|---|---|
| 1:1 Claude Workshop - Testimonial | `[form-id]` | `[sheet-id]` | Timestamp · Name · Before our session, where were you spending time you didn't want to spend? · What impact did the 1:1 session have on your time and work? · If someone in your exact role asked "is this worth it?" What would you tell them? · Can I share your story publicly? |
| ABA Training - Testimonial | `[form-id]` | `[sheet-id]` | Timestamp · Name · How was the team using AI before we worked together? · What impact did the training have on the business? · If a peer at another company asked you "is this worth it?" — what would you tell them? · Can I share your story publicly? |

**Public form URLs** (what gets pasted into client emails — not the response sheet):

- 1:1 Claude Workshop: `[form-url]`
- ABA Training: *(public URL TBD — pull from a recent send when needed)*

The `Form` column on the Testimonials row tracks the response sheet URL (so Shaw can jump to submissions). The `forms.gle/` URL above is what gets dropped into the initial ask email body via `email-helper`.

### Related databases (when linking from a Testimonials row)

| DB | Data source ID | What it carries |
|---|---|---|
| CRM Active Leads | `[page-id]` | Open leads (pre-conversion) |
| Clients (Nurture) | `[page-id]` | Past/current paying clients |
| Archived Leads | `[page-id]` | Disqualified / non-pursuit (incl. freebies, friends) |
| Engagements | `[page-id]` | Paid project ledger |

## Schema Cheat Sheet

| Property | Type | Notes |
|---|---|---|
| Name | title | Person's full name. One row per person (multiple per company is fine — e.g. several trainees from the same company) |
| Email | email | Person's direct email |
| CRM | url | Plain URL field — paste the URL of their page in any of the three CRM databases. No relation, no title sync; the URL itself is the link |
| Engagement | relation | → Engagements DB. Only set when there's a paid engagement row |
| Status | select | `Not Asked` · `Asked` · `Form Submitted` · `Approved` · `Published` · `Declined`. See the SOP for what each stage means and when to advance |
| Last Contact | date | Most recent testimonial-related touch (initial ask, FU, approval reply, etc.) |
| Next Contact | date | When to send next FU. Clear when no FU is pending (e.g. after Approved or Declined) |
| Form | url | Link to the response sheet of the form they were sent |
| Notes | text | Terse activity log of dated events only. Dates in parens, e.g. `Initial ask (5/13). FU1 sent (5/27). FU2 due (6/3).` No em dashes anywhere (use commas, colons, or split sentences). Don't restate biographic or engagement context — the `Engagement` and `CRM` fields carry that. |

Status options are listed for the SQL; cadence and meaning live in the SOP — don't
restate them.

## Core Workflows

### 1. Open a new testimonial ask

**Trigger:** a training wrapped (paid or unpaid). Shaw says "open a testimonial ask
for [Name]", "queue a testimonial for [the team I just trained]", or "kick off
testimonials for the cohort I just finished".

**Steps:**

1. **Find their CRM page URL.** Search Notion by name (`notion-search`). They might
   be in Active Leads, Clients (Nurture), or Archived Leads — use whichever shows
   them. For paying clients, check Clients (Nurture) first; for freebies / friends /
   archived, expect Archived Leads.
   - **Multi-attendee engagements.** When the engagement covers a team (group
     training, multi-attendee 1:1s), individual attendees usually don't have their
     own CRM rows. Every attendee's Testimonials row points to the same CRM page:
     the payer/champion's Clients (Nurture) record. Examples: a pair of attendees
     from one company all point to the payer's page; a four-person team all point to
     that company's shared team page.
2. **Find their Engagement, if one exists.** Search the Engagements DB by name.
   Engagements only exist for paid work — unpaid sessions don't have a row, leave
   the relation empty.
3. **Create the Testimonials row** with `notion-create-pages` against data source
   `[page-id]`:
   - `Name` (title)
   - `Email`
   - `CRM` — the URL pasted directly (no JSON array — it's a plain URL field)
   - `Engagement` — JSON array with the page URL, only if an Engagement was found
   - `Status` — `Not Asked` initially (flip to `Asked` after the email goes out)
   - `Form` — URL per the table above. Default to the 1:1 Claude Workshop form for
     individual workshops; pick ABA Training form for group/team trainings.
4. **Hand off to `email-helper`** to send the Initial Ask per the SOP. Pass the
   Testimonials row URL and the Form URL as context.
5. **After the email sends:** update the row — `Status` → `Asked`,
   `Last Contact` = today, `Next Contact` = today + 3.

### 2. Process a form submission

This is the meatiest workflow. **Trigger:** Shaw says "polish X's testimonial",
"X submitted the form", "draft a testimonial from the new form responses", or
"process today's form submissions".

**Steps:**

1. **Read the form response sheet** via the Drive `read_file_content` tool on the
   sheet ID. The sheet returns Markdown — first row is headers, subsequent rows are
   responses. Find the row by matching the `Name` column.
2. **Pull the verbatim response.** Note the values for Before / Impact / Worth It /
   Permission.
3. **Polish into 3 variants** per `references/polish-framework.md`. The framework
   covers voice rules, attribution per permission level, and worked examples.
4. **Update the Testimonials row** via `notion-update-page`:
   - `Status` → `Form Submitted`
   - `Last Contact` = the form's Timestamp date (not today — that's when they
     submitted)
   - Append to the page body: a `## Form Response` section with the verbatim, and a
     `## Drafts` section with the 3 polished variants. Use `insert_content`.
5. **Hand off to `email-helper`** to send the Approval Ask with whichever variant
   Shaw picks. Pass the chosen polished version + the Notes context.

### 3. Apply approval

**Trigger:** client replies "yes, go ahead" or Shaw says "X approved [their
testimonial]".

**Steps:**

1. `notion-update-page` (update_properties): `Status` → `Approved`. Add a Notes line
   with the approval date.
2. Reshape the body to lead with the approved version. Use `update_content` to
   replace the `## Drafts` section (with all 3 variants) with a clean `## Testimonial`
   section containing only the approved variant + attribution. Keep the
   `## Form Response` verbatim section intact below as historical record.
3. If the client made edits to the polished version, apply their edits and
   re-send for approval — stay in `Form Submitted` until they say yes to the final
   form.

### 4. Publish

**Trigger:** Shaw says "I published X's quote on the website", "the testimonial is
live", or "added their quote to the landing page".

**Steps:**

1. `notion-update-page`: `Status` → `Published`.
2. Update Notes with the publication date and the surface(s): website, sales letter,
   LinkedIn, newsletter, deck, proposal, social post, etc.
3. **Post-publish nudge:** the SOP notes that this is the highest-goodwill moment
   for a Referral Ask. Surface this to Shaw — either offer to create a
   `FU - [Name] (referral)` task in ABA via `notion-helper`, or just suggest he run
   the referral ask flow. Don't create the task silently; surface and confirm first.

### 5. Decline cleanup

**Trigger:** client actively declines, OR Shaw says "X never replied after FU3,
mark them declined" (the SOP's end-of-cadence outcome).

**Steps:**

1. `notion-update-page`: `Status` → `Declined`. Clear `Next Contact`.
2. Add a Notes line with the reason (active decline vs. ghosted post-FU3).

### 6. Sweep — who needs a nudge?

**Trigger:** "what testimonials need a follow-up?", "any testimonials due today?",
"sweep the testimonials DB", "what's stale in testimonials?".

**Steps:**

1. Query the Testimonials default view (`notion-query-database-view` on the database
   URL with the default view's `?v=` query string — fetch the database once to get
   the view URL if you don't have it).
2. Filter client-side: rows where `Status` is in (`Asked`, `Form Submitted`) AND
   `Next Contact` ≤ today.
3. **Group by FU stage** using the SOP cadence (don't restate the numbers — look them
   up if you need them):
   - `Asked` + Next Contact past, days since Last Contact maps to FU1 / FU2 / FU3
     per the SOP cadence
   - `Form Submitted` + Next Contact past → approval-ask follow-up needed
4. Surface to Shaw per row: name, current status, days since Last Contact, which FU
   stage is due. Then hand each off to `email-helper` for the appropriate FU draft
   per the SOP template.

## Polish Framework

→ See [references/polish-framework.md](references/polish-framework.md)

The HOW of turning raw form responses into pull-quotes. Includes the 3-variant
default, voice rules, attribution by permission level, and worked examples.

## Composition with Other Skills

- **`email-helper`** — owns all email composition. This skill hands off the polished
  testimonial + the relevant SOP template name; email-helper produces the draft.
- **`google-drive-helper`** — reads form response sheets. Use `read_file_content` on
  the sheet ID; responses are keyed by the `Name` column.
- **`conversion-copy`** — invoke when a quote is high-leverage (landing page hero,
  sales letter open) and needs sharper polish than the default 3-variant pass.
- **`crm`** — when the CRM page URL isn't already on the row, defer to `crm` to find
  the right page (Active Leads / Clients (Nurture) / Archived Leads).
- **`engagements`** — when an Engagement exists but isn't linked, defer to
  `engagements` to find it.
- **`sop-helper`** — for edits to the Testimonial Ask SOP itself (adding a new
  template variant, changing cadence, etc.). Don't restate SOP content here; if a
  policy needs to change, change it in the SOP.
- **`notion-helper`** — for the post-publish referral-ask reminder task. This skill
  doesn't create ad hoc tasks directly.

## Rules

- **Defer cadence, status meanings, and email templates to the SOP.** This skill
  carries mechanics. If a process question can't be answered from this file, the
  SOP has it. Single source of truth — don't duplicate.
- **Defer email composition to email-helper.** Hand off the polished testimonial
  + the SOP template name as context; let email-helper produce the draft.
- **Polish from real submissions only.** Don't invent testimonials. The pre-drafted
  FU2 case (where no form submission exists) pulls from call notes / Engagement
  Results, not from imagination.
- **Status flips and body updates are atomic.** When advancing to Form Submitted /
  Approved / Published, update both properties AND body together — don't leave the
  row inconsistent.
- **Honor permission level.** The form's Permission column dictates attribution.
  "Name only" means no role/company in the published quote. "Name, role, and
  company" is the full attribution. Default to less-rather-than-more if a permission
  level is ambiguous.
- **No em dashes in notes or polished quotes.** Shaw's voice rule. Use commas,
  colons, or split sentences. Em dashes are fine only in raw verbatim quotes
  (preserved as the client wrote them); every surface Shaw owns — notes, polished
  variants, attribution lines — drops them.
- **Notion + Drive only.** This skill doesn't create calendar events, iOS reminders,
  Stripe invoices, or other side effects. Side effects compose via the other skills
  listed above.

## Quick Reference: Tools

Assume these are loaded via `tool_search` before first use.

| Need | Tool |
|---|---|
| Find a page (CRM, Engagement) | `notion-search` |
| Read a Testimonials row or related page | `notion-fetch` |
| Create a Testimonials row | `notion-create-pages` |
| Update Status / properties / body | `notion-update-page` |
| Query the database for the sweep | `notion-query-database-view` |
| Read a form response sheet | Drive `read_file_content` |
| Search Drive for a form / sheet by name | Drive `search_files` |
