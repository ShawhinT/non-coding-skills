---
name: client-docs
description: Draft ABA's formal client-facing documents — proposals, statements of work (SOW, the signable contract version of an accepted proposal), and proposal decks. Fire whenever Shaw asks to draft, revise, or send a proposal, SOW, contract, engagement outline, pricing quote, or scope for a client, even when he names no format ("draft a proposal for X", "write the SOW", "update [Client]'s proposal"). The default proposal format is the branded PDF document; build a slide deck only when he asks for a deck or slides ("proposal deck", "put the proposal in slides"). Also covers training outlines, workshop syllabi, bootcamp outlines, course proposals, session agendas, curriculum design, and reading existing .pdf proposals or SOWs for reference. All documents branded under AI Builder Academy (ABA). Do NOT use for cover emails (email-helper), sales letters (sales-letter-writer), or one-pagers (conversion-copy).
---

# Client Docs Skill

Draft, edit, and convert the formal documents Shaw sends consulting clients: **proposals** (pre-sale scoping), **SOWs** (the signable contract), and **proposal decks** (the slide form of a proposal, built only on request). Proposals and SOWs share one PDF pipeline, voice, and set of formatting conventions; decks have their own guide (see Proposal Decks below). All documents are branded under **AI Builder Academy (ABA)**.

A plain "proposal" request means the PDF document. Only build a deck when Shaw explicitly asks for slides.

## Workflow

1. **Gather info** from the user (or unstructured notes)
2. **Draft markdown** following the example proposal structure
3. **User reviews/edits** the markdown
4. **Convert to PDF** using the bundled pipeline

## Reading Existing Documents

When the user wants to reference a past proposal or SOW:

- **PDF files**: Extract text with the read-pdf script:
  ```bash
  cd ~/.claude/skills/client-docs/scripts && uv run python read-pdf.py /path/to/proposal.pdf
  ```
- **.pages files**: Most past proposals have a PDF version alongside the .pages file. Use the PDF with read-pdf.py.

Past proposals live in `~/Documents/_stv/_ABA/proposals/<client>/`. Past SOWs live in `~/Documents/_stv/_ABA/sow/<client>/`.

## Updating an Existing Proposal

When the user wants to revise a draft, read the existing markdown, make targeted changes, and re-save. Don't regenerate from scratch.

When you change a value that appears in more than one place — durations, session counts, titles, structural terms — update every instance: the syllabus Duration field, session headers, the Investment table rows, the Total, and payment terms. Numeric totals especially must reconcile (the sum of session durations equals the stated total). A priced document loses trust the moment the arithmetic doesn't add up, so re-check the math after any duration or pricing edit.

## Drafting a Proposal

**First, find the best base to start from.** Before writing anything, look across *all* client folders under `~/Documents/_stv/_ABA/proposals/`, not just the current client's, and pick the **most recent proposal of the same offering type** to use as the template. The newest proposal of a given type carries the latest copy refinements (wording, structure, section names), so starting there beats both the current client's older draft and the content-free `references/proposal-format-reference.md` (which is for format, not copy).

To do this:
1. Rank the candidates for that offering type by the `Prepared on` date *inside* each file. Do not rank by file mtime: editing an old proposal for any reason floats it to the top and silently hands you a stale base. Run this from the proposals root, swapping the variant token:

```bash
for f in */*1on1*.md; do d=$(grep -m1 '^\*Prepared on' "$f" | sed 's/^\*Prepared on //; s/ by .*//'); echo "$(date -j -f '%B %d, %Y' "$d" '+%Y-%m-%d' 2>/dev/null) $f"; done | sort -r
```

   Variant tokens: `1on1` (1:1 and 2:1 workshops), `fractional` (ongoing retainers), `team` (cohort/group rollouts), `partner` (offering menus for a partner to resell, see Partner Proposals below). The token matches across naming eras, since current files are `ai-proposal_<client>_<variant>.md`, older ones `ai-training-outline_<client>_<variant>`, and descriptive ones still carry the word (e.g. `team-claude-workshops_[client-slug]-bdr-sa.md`).

2. Take the top result as the base, with two exclusions. Skip files with `example` in the name (illustrative templates, not live proposals). Skip anything whose offering doesn't actually match once you open it. If the glob returns nothing or suspiciously few hits, the offering may predate the token convention: fall back to `ls */*.md` and identify the type by reading titles.
3. Read that file, then adapt it to the new client: swap names, participant groupings, delivery method, dates, and pricing. Preserve its refined copy unless the new engagement calls for different wording. Rewrite the H1 to the standard `AI Enablement - <Client>` (older bases carry offering-specific titles like `1:1 Claude Workshops - [Company]`), or `AI Partnership - <Client>` for a partner proposal.

Confirm the chosen base with the user if it's ambiguous which prior proposal is the closest match.

**The latest proposal can lag what Shaw actually teaches.** Agendas evolve in the slides before they reach a proposal, so a session agenda copied from the base may already be stale. When drafting a session agenda, check the most recent delivered deck for that format under `~/Documents/Presentations/Slides/ABA/clients/<client>/` (read it with the `keynote` skill) and build the agenda from its slide flow. If unsure which deck is current, ask.

**Other agent platforms.** Some clients can't use Claude (e.g. a Microsoft shop on Copilot Cowork). The agenda and framework stay the same since the principles are tool-agnostic. Swap the tool name throughout (titles, steps, prerequisites, licenses) and confirm the platform supports what the agenda promises, such as skills and connectors. Anything Claude-specific, like the ABA Skill Library, may not carry over.

Gather these details from the user (ask for anything missing):

- **Client name**
- **Training title**
- **Number of sessions** and **duration per session**
- **Delivery method** (e.g., Microsoft Teams, Zoom, in-person)
- **Topics per session** (or general themes to flesh out)
- **Pricing**: standard hourly and per-session rates, the retainer's founding-rate ladder, and the in-engagement Additional Services rates live in `references/pricing.md`. Read it before pricing anything. Ask the user which rate tier applies to each session.
- **Discount** — When a discount applies (volume, founding client, group), list sessions at full standard-rate prices, then a plain `Subtotal` row with the full price, then a discount row in green: `| <span style="color: #2E7D32">*Discount*</span> | | <span style="color: #2E7D32">*-$X*</span> |`. The Total row reflects the discounted price. The subtotal makes the full price visible, so the reader sees what the discount is worth instead of having to add up the rows.
- **Dates** (or TBD)

**Structure:** Engagements can be multiple sessions or a single session with multiple parts (using `### Part 1:`, `### Part 2:`). The syllabus Duration field should reflect this (e.g., "1 session (3.5 hours total)" or "4 sessions (90 min each)").

**Proposal sets (the default).** Most clients get three proposals at once, one per tier, so the buyer picks a starting point instead of a yes/no on one scope:

- `1on1`: entry point. A few 1:1s for key leaders (usually 3, so the volume rate applies).
- `team`: the same 1:1s plus an all-hands and 1-2 function workshops, each with its follow-up office hour.
- `fractional`: the 3-month retainer.

Each is a standalone document in the client folder with the same `Prepared on` date, built from the newest base of its own variant. Facts the three share (participant names, unit prices, discount wording, agenda copy) must read identically, so when one is edited, check whether the change applies to its siblings. Worked examples: `[client-slug]/` and `[partner-slug]/`. Write a single proposal only when Shaw asks for one specific offering.

**Flexible-scope pricing (count or timing undecided).** When the engagement's exact scope is still open, don't pin a single headline Total. Price by building block: an Investment table that lists each unit (a workshop, a 1:1 prep, a follow-up) at its unit price, followed by two anchored *example scopes*, a smaller and a larger configuration, each with its own reconciled Total. Two anchors let the reader infer the in-between cost without you enumerating every option. If a unit price hinges on a term that could be read two ways (per-team vs per-session), define that term in plain language right before the table (e.g. "a *team* is a function. a *group* is a scheduled session of that team."). See `[client-slug]/team-claude-workshops_[client-slug]-bdr-sa.md` for the worked example.

**Next phases (optional, buyer-driven).** A proposal usually scopes one recommended starting offering. When the buyer asks to see offerings beyond that starting point (e.g. wanting unit prices to bring to a leadership conversation), add a short "Next phases" section after the Investment listing the other offerings at unit prices, one line each. Keep them out of the Investment Total, they're context, not priced scope. Only include when asked, not as a default.

**Partner proposals (the recipient resells rather than buys).** Sometimes the company Shaw is writing to isn't the client. It's a partner bundling ABA's workshops into engagements with *their* customers. The document is a menu of what they can sell, not a scope for one engagement, and that changes four things:

- **The offerings section replaces the single engagement.** List each offering under its own `###` header with the price in the header (e.g. `### 1:1 Claude Workshops (<unit price> each)`), each carrying its own outcomes and session agenda. There is no one Engagement Goal, since each offering has its own.
- **The syllabus describes a category of participant, not named people.** `Offering:` replaces `Training Title:`, participants read as roles at the partner's customer accounts, and dates are "TBD, scheduled per customer engagement".
- **Flexible-scope pricing is the default here,** not the exception. Per-customer scope is unknowable at signing, so price by building block with two example scopes as anchors.
- **Surface the margin question rather than guessing it.** Whether the listed prices are the partner's cost (they mark up) or list price to the end customer (Shaw pays a referral cut) is a business decision Shaw makes, and it rarely comes up on the call. List the standard rates as-is and flag the open question to him instead of inventing a partner discount.

See `[partner-slug]/ai-proposal_[partner-slug]_partner.md` for the worked example.

Two sources, two jobs:
- **Content/copy** comes from the most recent live proposal of the matching offering type (the "find the best base" step above). Clone its wording and structure.
- **Format/structure** is defined once in `references/proposal-format-reference.md`, a content-free skeleton that demonstrates every pattern with inline notes: both syllabus headings, the spacer row, multi-session vs single-session-with-parts headers, timed segments, optional/unbilled segments, the page break, both Investment table shapes (simple 3-column and Qty-column collapse `N | $total ($unit ea)`), `Included` and `n/a` cells, the green discount row, and the payment-term variants. Consult it whenever you're unsure how a structural element should be written. It is the fallback base when no live proposal of the needed type exists yet.

**Filename convention.** Save to: `~/Documents/_stv/_ABA/proposals/<client>/ai-proposal_<client>_<variant>.md`. The H1 title is `AI Enablement - <Client>` (e.g. `# AI Enablement - [Client]`).

- `<variant>`: `1on1` | `team` | `fractional` | `partner`. When a client has only one offering, still include the variant that fits (e.g. `ai-proposal_[client-slug]_1on1.md`). A `partner` proposal takes the H1 `AI Partnership - <Client>` instead, since "AI Enablement" names an engagement and the document is a collaboration.
- One convention for both the source `.md` and the built `.pdf` (the PDF inherits the basename), and it's also the client-facing name Shaw sends. No separate internal vs client naming.
- **Do not track versions.** No `_v2`/`_v3` suffixes and no date suffixes. When a proposal is revised, edit and rebuild the same file in place.
- `<client>` is kebab-case (e.g. `[client-slug]`); the folder uses the same client slug.

Legacy proposals use the older `ai-training-outline_<client>...` prefix and some are named descriptively (e.g. `team-claude-workshops_[client-slug]-bdr-sa.md`). Leave those as-is. The discovery step globs all `.md` rather than a fixed prefix, so mixed names coexist fine.

Tell the user to review the markdown before PDF generation.

## Statements of Work

A SOW is the contract version of an accepted proposal. The proposal sells the engagement; the SOW defines the binding terms the client signs. Draft one when a client has accepted a proposal and Shaw asks for the SOW. Same pipeline, voice, and conventions as proposals, with these differences:

- **One shared stylesheet.** SOWs render with the same `style.css` as proposals (US Letter, 1 inch side margins, 10.5pt body, 22/15pt bold headings, spaced paragraphs). There is no SOW-specific styling beyond the classes the SOW markup uses (`.signatures`).

- **Location and name.** Save to `~/Documents/_stv/_ABA/sow/<client>/ai-sow_<client>_<variant>.md`, using the same client slugs and variant tokens as proposals. The H1 is `Statement of Work - <Client>`. The contract id (`SOW-NNN`, numbered per client) lives in the Overview's Engagement row, not the filename. All other proposal file rules apply: one basename for `.md` and `.pdf`, client-facing name, revise in place with no version suffixes.
- **Two content sources.** Engagement-specific sections (Objectives, Services, Fees & payment, guarantees) derive from the accepted proposal: its Engagement Goal becomes Objectives, What's Included becomes the Services table, Investment and Payment terms become the installment table. The legal sections (Out of scope, Responsibilities, IP & confidentiality, General terms, Signatures) carry over from the most recent live SOW nearly verbatim; find it under the sow root the same way you find a proposal base (rank by `Prepared on` date). Structural patterns unique to SOWs (numbered sections, parties Overview, installment table, signature block) are demonstrated in `references/sow-format-reference.md`.
- **Numbered sections with cross-references.** H2s are numbered (`## 2. Services`) and the body refers to them ("Section 2", "Section 7"). Adding, removing, or reordering a section silently breaks these, so re-check every cross-reference after any structural edit.
- **Objectives are directional, not obligations.** Metric targets from the proposal's goals enter the SOW as shared goals with an explicit disclaimer: services are complete when the Section 2 items are delivered, and targets are not a condition of payment. Never let an outcome metric read as a performance obligation. Two habits follow from this. State targets without baseline readings ("daily use reaches 75% of monthly active users", not "75% ... (65% at signing)"): a number pinned to signing day invites a before-and-after scorecard on work whose value isn't the delta. And frame them as "a starting point ... expected to evolve by mutual agreement", not "may be adjusted", so evolution reads as the plan rather than an escape hatch.
- **Commitments stay as loose as the work allows.** Where a clause can bind Shaw without buying the client anything real, prefer the looser form: prior consent rather than prior *written* consent on subcontracting, sessions that "may be moved to another week or combined with a later session" rather than only rescheduled. Reserve hard formality for the clauses that protect delivery or payment.
- **Leave payment mechanics out.** No preferred payment method and no tax language. Shaw invoices for services, works from a W-9, and pays his own taxes, so a "fees are exclusive of applicable taxes" line only creates a question that the Independent contractor clause already answers. Keep the Fees paragraph to who receives the invoice and the no-travel-expenses note.
- **Warrant the services, not the model.** Shaw sells his work, not Claude's output, so the warranty clause draws that line in plain language: "Claude's outputs are not guaranteed to be accurate or complete. Client is responsible for reviewing AI-assisted work before relying on it." Avoid the lawyer register ("provided without warranty"). The professional-and-workmanlike warranty on ABA's own services stays.
- **Lead lists with their framing, including the process line.** A section whose body is a bulleted list opens with one line that both frames the list and carries any process note, then the bullets close the section. A sentence stranded after a list reads as an afterthought.
- **No standalone Out of scope section.** A one-line catch-all under the Services table does the job: "Anything not listed above is out of scope. Additions can be agreed at any time in writing; email suffices." An enumerated exclusion list mostly restates what the Services table already implies. Note the amendment mechanism stays written (email), even though scope gets discussed on recurring calls: a verbal agreement as the amendment path is the ambiguity a contract exists to remove.
- **Pricing appears once.** The Services table has no Price column (`Service | Qty | Duration`). Money lives only in Fees & payment as an installment table whose rows sum to the bold Total. A discount is a green italic note in the Total row's Due cell (e.g. `Founding client rate (50% off <list price>)`), not a separate row, because the installments already reflect the discounted amounts.
- **Contract register relaxes the sentence rules.** Semicolons joining coordinated legal clauses are normal here ("at any time; email suffices"), unlike proposals. Em dashes stay banned. Defined terms in the raw-HTML Overview table need curly quotes as entities (`&ldquo;ABA&rdquo;`) since raw HTML skips the smart-quotes pass.
- **Verify before PDF:** installments sum to the Total; dates agree everywhere they appear (Overview term, Delivery paragraph, session date ranges, installment due dates); service quantities match the term (a 13-week term means 13 weekly sessions); cross-references point at the right sections; the discount math in the Total note reconciles with the proposal's pricing.
- **Audit page breaks in the built PDF, not just the markdown.** Read the generated PDF and look for a heading or table split from its content: a table whose first row sits alone on the previous page, a section header with one orphaned bullet under it. Fix by inserting `<div class="page-break"></div>` before that section, then rebuild and re-read, since each break shifts everything after it and can create a new orphan downstream. A split between two paragraphs of the same section is fine and not worth forcing; only chase breaks that separate a heading or table from its body. Manual breaks are tuned to the current content, so re-audit after any edit that changes length.

## Proposal Decks

When Shaw asks for the proposal in slide form ("proposal deck", "put the proposal in slides", a client requesting a deck), read `deck/guide.md` and follow it start to finish. It is a research-first workflow (scope, mine real case studies, confirm with Shaw, then build) that composes with the `aba-brand-system` and `pptx` skills and uses `deck/deck_scaffold.js` as the pptxgenjs starter. The Voice & Style and PDF sections below do not apply to decks; everything deck-specific lives in the `deck/` folder.

## Voice & Style

A proposal is a spec, not a pitch. The deal sells itself through clear structure; persuasion belongs in the cover email and the live conversation. Write to define what happens, and cut anything whose job is to convince or impress. Drafting in this voice up front saves the user from stripping it down later.

- **Compress to the outcome.** State the result; don't explain the mechanism inside it. "Each participant builds one skill relevant to their work" beats "three skills built live (12 total), drawn from the intake form, plus one built as homework."
- **One idea per sentence.** Any punctuation that fuses two clauses into one breath (em-dash, semicolon, comma-splice) is a signal to split into two sentences or cut the trailing clause. A period is almost always the fix. (Shaw reliably edits these out.)
- **No em dashes or en dashes, anywhere.** Not in prose, not in headers, not as table placeholders. Shaw strips them from nearly every proposal because they read as AI-authored, so write without them from the start. Replace a prose em dash with a period, comma, or colon. Write number ranges with a hyphen ("2-3 skills", "3-4 participants"), not an en dash. Use "n/a" for an empty Investment-table cell, not "—".
- **Cut rationale and framing.** A well-ordered agenda argues for itself. Don't narrate why it's structured that way ("no demos here, those come later") or add an "Our Approach" essay. Meta-commentary reads as insecurity about the structure. *One sanctioned exception:* a short "Why this matters" block under the Engagement Goal is fine when Shaw asks for it. It's a judgment call he makes by feel, not a default, so don't add it unprompted. When included, keep it to ~2 bullets framing the entry-point offering as the wedge (executives gain the AI mental model to build strategy, champions drive adoption through social proof), drawn from Shaw's roadmap language. Don't let it grow into an essay.
- **The client is the hero, not the instructor.** Demote yourself as the actor, promote the team as the one who acts and benefits. You get the work verbs (instruct, demo); they get the outcome verbs (learn, build, share). Prefer "skills the team can build" over "skills to build," and "Instructor builds…" over "I build…".
- **Don't tally or label-inflate.** Counts ("12 skills!") and marketing terms ("done-for-you") signal salesmanship and quietly commit you to numbers. Promise the minimum you can stand behind.
- **Name things plainly.** Calm, true nouns over benefit-reaching labels: "Onboarding Claude to [Company]" over "Delegating Work to Claude for Teams."
- **Say each thing once.** If info already lives in its natural place (the table, the body), don't echo it in the overview or repeat structural prefixes ("Session 1:") that the ordering already conveys. The same goes for price: when the Total and payment terms already state it, a per-month restatement adds nothing.
- **State capacity as a pool over the term.** "Up to 13 training sessions over the 3-month term" beats "up to one per week" plus a sentence explaining that timing is flexible. The pool already implies the flexibility, so the clause is redundant.
- **Examples illustrate, they don't scope.** For open-ended deliverables (e.g. infrastructure builds), give one inline line of short, representative example names with the "not a scope of work" footnote. A bulleted list of client-tailored builds reads like a commitment to work nobody has scoped yet.
- **Spend words only where they're load-bearing.** Ruthless on adjectives, precise on commitments and logistics. Hard constraints like "filled out no later than 7 days prior" or "30-minute debrief" earn their length because they protect delivery.

Rhythm: short, present-tense, subject-verb-object declaratives. Modest active voice. No stacked "which/that" clauses.

## Converting to PDF

Before converting, verify:

- Each session's timed segments sum to its stated duration.
- The Investment table reconciles to the headline **Total** on both axes, and the two axes are independent:
    - **Total Duration** = the sum of every stated duration in the Duration column, including rows priced **Included**. An `Included` deliverable with a real duration (e.g., a 30-min Check-In Call) is committed delivery time, so its minutes count toward the Total hours even though it contributes nothing to the price. Only rows with no stated duration (`n/a`) are skipped.
    - **Total Price** = the sum of the dollar rows only. `Included` rows contribute nothing to the price.
    - Worked example: 3 x 90-min workshops + a 30-min Included Check-In Call = **5 hours total** at the same workshop price (not 4.5 hours). The 4.5-hour answer is the classic mistake: don't drop an Included row's duration from the Total.
- **Genuinely optional segments** (e.g., "optional 15-min Q&A after the session") are the only thing excluded from both the Total duration and price. "Optional" means the client can decline it. It is not the same as "Included" (committed, no extra charge). The same duration reads identically in the session header, the Investment row, and the Total.
- Titles, durations, and structural terms read identically everywhere they appear.
- **Capacity-style scope can't be summed either.** When quantities are "up to N" or "unlimited" (fractional trainings, office hours), there is no committed total, so leave the Total Duration cell blank rather than inventing a figure.
- **A duration range can't be summed.** Shaw often describes a format loosely ("60-90 min session plus a 30-60 min office hour"), which reads fine in prose but leaves the Total unreconcilable. Resolve the range in the Investment table by splitting it into the concrete rows the range was covering (an all-hands at 60 min and a function workshop at 90 min, each with its own follow-up length), and keep the range in the offering description where it belongs. Don't average the range or quietly pick an endpoint.

After the user approves the markdown:

```bash
cd ~/.claude/skills/client-docs/scripts && uv run python md-to-pdf.py /path/to/outline.md
```

The PDF is created in the same directory as the markdown file, with the same base name (`.md` → `.pdf`).

## Formatting Notes

These conventions aren't obvious from the example alone — follow them for correct PDF rendering:

- Syllabus uses HTML `<table class="syllabus">` with `<tr class="spacer">` to separate title/instructor from dates/logistics (not a markdown table)
- Use `TBD` for unknown dates/times — it gets highlighted in red in the PDF
- Each session's timed segments should add up to the session duration
- Session content uses: `- **Section** *(15 min)*` with nested bullets for subtopics
- Use `---` horizontal rules between sessions
- Use `<div class="page-break"></div>` before the Investment section to force a page break
- Inline HTML like `<span style="color: #2E7D32">` works inside markdown table cells for colored text (e.g., discount rows)
- For an asterisk note under a session (a caveat about how a segment works), wrap it in `<p class="footnote">...</p>`. The `.footnote` class in `style.css` renders it ~20% smaller and gray, so it reads as a subordinate note rather than body copy
- Investment table goes at the end with a bold **Total** row — use consistent unit formatting across all rows
- Prepared-by line format: `*Prepared on <date> by Shaw Talebi, PhD*` (italicized, includes date)
- Payment terms go after the Investment table as a `### Payment terms` subsection with bold bullet labels. Close it with `- **Payment method:** Stripe invoice, payable by direct deposit, debit card, or credit card`, since corporate buyers routing a proposal through approval need to know how it gets paid
- Supplementary price lists (e.g. Additional Services in a fractional proposal: 1:1 and team workshop rates plus a "Custom AI build | Scoped per project | Quoted per project | 25% off" row) go last, after Guarantees and Payment terms, so the committed scope and its terms read as one block
