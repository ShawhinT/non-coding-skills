---
name: "meeting-prep"
description: "Prep Shaw for an upcoming meeting — a discovery call, a paid 1:1 Claude Workshop, a post-session or nurture check-in, a multi-session engagement wrap-up, a partner/channel call, or a recurring client sync. Use whenever Shaw asks to prep for a meeting or call, do pre-call research, or gather context before any conversation — \"prep for my call with X\", \"meeting prep for X\", \"do pre-call research for X\", \"I have a call with X today\", \"what should I bring up at the X sync\", or any reference to preparing for an upcoming meeting. Also trigger when Shaw mentions a person's name alongside a scheduled call; even casual mentions like \"call with X later\" or \"meeting with X, what should I know?\" count. Also invoked by CRM Workflow 7 (Discovery Call Intake) to create and populate the ABA Calls page for a freshly-booked discovery call. Covers prospects, clients, past clients, and partners."
---

# Meeting Prep

Get Shaw ready for an upcoming meeting so meeting time goes to the things only the other people can share — their world, their pain points, their decisions. Web research, CRM data, and past session notes handle the factual background; the meeting handles everything else.

This skill is a **router**, not a content store. It owns the *mechanics* of prep — finding the person, deciding what the meeting needs, pulling the CRM record, reading Gmail, web research, and writing to the call page. The *content* of each call type — its question bank, its tone, what the brief should emphasize — lives in that call type's event-type SOP. This skill points at the SOP; it does not restate it.

## What the meeting needs

Decide this first: it sets *what* gets written, and the call type then sets *how*.

- **A brief** — a first or occasional conversation: discovery, check-in, wrap-up, partner. Walking in without the background means spending the meeting re-treading it, so the page gets a research brief and prioritized questions. This is the full Workflow below.
- **Agenda suggestions** — a recurring meeting with a standing agenda. See "Recurring meetings."
- **A delivery session** — anything on the ABA Trainings page: a 1:1 Claude Workshop, a team workshop, office hours. A brief on the Trainings page, plus the Pre-session prep and Agenda its SOP calls for. See "Delivery sessions."

### Recurring meetings

A weekly retainer sync or standing team call already has its prep in the agenda. A Person/Company/Read brief on someone Shaw talks to every Tuesday restates what he knows, and Prioritized Questions compete with the agenda. Leave the page's existing structure as you found it — whatever sections it carries are the format — and leave the agenda to Shaw.

The tell is cadence, not call type. What changed since last week still matters; it lands under the page's Call Notes, filtered, for Shaw to promote into the agenda and refine. For a Fractional AI Department weekly sync, `references/weekly-sync-frac-ai.md` covers what to gather and what earns a line.

### Delivery sessions

The page's `Call Type` (1:1 Claude Workshop, Team Workshop, Office Hours — read the current options off the data source) picks the delivery SOP; a team workshop scoped to one function runs on that SOP's function-specific spoke. The SOP decides what the page needs, so don't carry 1:1 mechanics onto a group session. Intake sheets are per offer — the link below is the 1:1 sheet; a team workshop's responses live in their own Drive sheet, found by the client's name.

Run the Workflow below with the brief on the ABA Trainings page, then add a **Pre-session** checklist after the brief's `---` divider. This is the prep Shaw runs through 24 hours before the session. For a 1:1 Claude Workshop, include:

```
Pre-session
- [Intake responses (Sheet)](https://docs.google.com/spreadsheets/d/[sheet-id]/edit)
- Rank use cases best (high impact, high probability of success) to worst (low impact, low probability of success)
- Send agenda 24-hr before
```

Then add the standard **Agenda** section from the matching SOP. The Pre-session + Agenda block goes after the research brief, separated by a `---` divider.

## The five call types

Each maps to an event-type SOP. SOPs aren't hardcoded by ID — find the matching SOP on the SOPs page (its ID is in the SOPs row of `notion-helper/SKILL.md` → "Other Key Pages"; fetch it and match child pages by title), then read it when prepping.

- **Discovery Call** — pre-sale conversation with a lead. Discovery-focused. The brief goes on an ABA Calls page. SOP: *Discovery Call*.
- **1:1 Claude Workshop** (and other delivery sessions) — the paid 1:1 delivery session, or a team workshop / office hour on the ABA Trainings page. The brief goes on the Trainings page and is paired with Pre-session prep and an Agenda (see "Delivery sessions" above). SOP: per the page's `Call Type` — *1:1 Claude Workshop*, *Team Workshop* (or its function-specific spoke), *Office Hours*.
- **Check-in Call** — a relational touchpoint with a client or warm lead. The base *Check-in Call* SOP carries the shared Setup, relational call bank, and post-call mechanics, plus the current list of variant spokes and what triggers each; read it to pick the spoke, since the set changes as offers change. The spoke governs the brief and the question bank. The brief goes on an ABA Calls page.
- **Wrap-up Call** — end of a *group / multi-session training engagement*, days-to-weeks after it wraps, with company contacts (champion, buyer, leadership). Recommendations + the 4Rs. The brief goes on an ABA Calls page. SOP: *Wrap-up Call*.
- **Partner / Channel Call** — a call with someone who is *not* a lead or client: a partner, channel, affiliate, or subcontractor (see `crm/SKILL.md` → "The Friends database" for what each type means), from the first exploratory conversation through every working sync after it. The other side is a peer splitting client and delivery, not a buyer, so the brief sources from the **Friends record** rather than the CRM. The brief goes on an ABA Calls page. SOP: *Partner Call*.

### These five vs. the `Call Type` property

The ABA Calls database carries a `Call Type` select that does **not** use these names one-for-one.
Set it when creating a page:

| This skill's type | `Call Type` value |
|---|---|
| Discovery Call | `Intro Call` |
| Check-in Call | `Check-in` |
| Wrap-up Call | `Wrap-Up` |
| Partner / Channel Call | `Partner` |
| 1:1 Claude Workshop | *(ABA Trainings — no Call Type on ABA Calls)* |

The table maps this skill's vocabulary onto the property — it is not the full option set, and
that set isn't fixed. Shaw retunes it in Notion as the work changes, so read `Call Type`'s
current options off the data source rather than a copy kept here. A page still needs its
`Call Type` set even when no brief is written.

Values outside the table get no brief by default, and the reason is never the name — it's that
something else already did the brief's job: an intake form collected the answers, or a standing
agenda holds the prep (see "Recurring meetings" above). The exception is a page that already carries a
`Pre-Call Research` heading. That's a request for one; fill it from whatever record exists —
the Friends row, the last email thread, the text history — at the same 1-2 sentence discipline.

## Key Locations

Canonical Notion IDs for the main databases live in `notion-helper/SKILL.md` → "Main Databases." Event-type SOPs aren't hardcoded by ID — discover them on the SOPs page (its ID is in the SOPs row of `notion-helper/SKILL.md` → "Other Key Pages"; fetch it and match child pages by title). CRM-specific sub-databases (Active Leads, Clients Nurture) and the Gmail account are documented in `crm/SKILL.md`. The key resources are:

- **Active Leads database** — CRM entries with status, notes, email, source
- **Clients (Nurture) database** — past clients with engagement history, check-in cadence, and expansion signals
- **Friends database** — the non-lead network (partners, channels, affiliates, subcontractors, friends), with deal-structure state in each record's Context. Documented in `crm/SKILL.md`
- **ABA Calls database** — call pages where pre-call briefs and notes live (Discovery, Check-in, Wrap-up, Partner)
- **ABA Trainings database** — delivery sessions (1:1 workshops, trainings, engagements) with session content and notes
- **Engagements database** — won-deal project ledger; a client's engagement row links the ABA Trainings pages that hold prior session context
- **Gmail** — shaw@aibuilder.academy, where all email threads with leads and clients live

## Workflow

### 1. Find the person and determine call type

Search the Active Leads database, the Clients (Nurture) database, **and the Friends database** for the person's name — and search by company name and email domain too, since a colleague may be the one on file. Pull their email, status, source, and notes. Also search the ABA Calls and ABA Trainings databases for any existing pages with this person's name — past calls and delivery sessions are essential context.

Searching only the two CRM tables is the easy miss: a partner or channel contact is *deliberately* not in either, so a CRM-only sweep returns nothing and the person reads as brand new when there may be a Friends record carrying the whole history of the arrangement.

Determine the call type from what the call *is*, cross-checked against where the person sits:

- **A lead in Active Leads, early-stage / pre-sale** → **Discovery Call**.
- **A delivery session** (there's an ABA Trainings page, an engagement row, or Shaw describes it as the workshop itself) → **1:1 Claude Workshop**, or the team/office-hours SOP its `Call Type` names.
- **A client in Clients (Nurture)**, and the call is a post-session or periodic nurture touch → **Check-in Call** (client context). The base *Check-in Call* SOP's Variants and Trigger sections decide which spoke; read what fired the call (a dated task, a `Next Contact` date, a BAMFAM booking) rather than inferring the spoke from elapsed time, which misreads any call that landed off its intended schedule.
- **A lead in Active Leads with a check-in on the calendar** (warm but not converted — often pre-booked off a discovery call) → **Check-in Call** (lead nurture context) → *Check-in Call (Lead Nurture)*. No 4Rs, no engagement to pull from.
- **The end of a group / multi-session training engagement**, with company contacts → **Wrap-up Call**.
- **A contact in the Friends database**, or someone whose own business could plausibly deliver what Shaw sells, or a call Shaw frames as exploring a partnership → **Partner / Channel Call**. A firm that sells adjacent services is a partner candidate before it's a lead; if there's a real chance the conversation is about splitting client and delivery, prep it as a partner call even when a sale is also possible.
- **Found in both Active Leads and Clients** → the Clients entry takes precedence. They're a past client, not a prospect.

If the call type is genuinely ambiguous, or the person isn't in any database and Shaw hasn't pointed you to a source, ask rather than assuming. A call can also be *two* types at once — most often a partner call that might become a client conversation. Prep the partner framing and note the other possibility in the Read rather than forcing a single label.

### 2. Find or create the call page

Search the ABA Calls database (or ABA Trainings, for a 1:1 Claude Workshop) for the person's name. This is where the pre-call brief will go.

- **Invoked by CRM Workflow 7 (Discovery Call Intake):** create the ABA Calls page and link it bidirectionally with the CRM record, without asking first. In the Workflow 7 flow, this skill is the **single creator** of that page — Workflow 7 does not also create it, so it never gets made twice.
- **Invoked any other way:** if there's no page yet, ask Shaw before creating one.

**Properties to set on a new ABA Calls page** (schema refactored 9/18/26): `Name`, `Date`,
`Email`, `Call Type` (map it via the table above), `Company` (relation → Companies — match on the
attendee's email domain against the Companies `Domain` field), `CRM` (url of the person's Active
Leads *or* Clients page), and `Friend` (relation → Friends) on a partner/channel call, where the
Friends record is the source anyway. `Company` is a dual relation, so setting it also populates
`Calls` on the Companies row — that is what keeps the account-level call history complete without
anyone maintaining a list by hand.

### 3. Check for previous call notes

If the CRM notes reference earlier calls, or earlier ABA Calls / ABA Trainings pages exist for this person, read them. Previous call context is valuable — it means this isn't a cold conversation and you should understand what was discussed before so Shaw doesn't re-tread old ground. For client calls, the engagement row's linked ABA Trainings pages are the canonical record of what Shaw actually delivered. When those pages link call transcripts (Google Docs), read the transcripts, not just the page notes — for results-driven calls like wrap-ups and check-ins, the honest per-use-case numbers and quotable lines live in the transcript, while the notes only carry the gist.

### 4. Pull the Gmail thread

Search Gmail for messages to/from the person's email address. Read the full thread. Email exchanges often contain context that the CRM notes compress out — tone, specific asks, how they described their situation in their own words.

**Load `email-helper` → "Gmail Technical Notes" before concluding a thread is missing, stale, or complete.** That file already documents the two ways this step fails, and both are invisible in the result you get back: `search_threads` truncates a thread's message list, so the newest messages silently disappear; and the live conversation routinely lives in a thread whose subject is about something else entirely. A prep run that skips those notes will read "no recent email" off a search result and brief Shaw as though the last touch was weeks ago. (8/3/26: an entire close-out exchange and the reply that booked the call were sitting inside a thread titled for a proposal from six weeks earlier.)

**Notes are a compression, so verify the load-bearing claims against the source.** CRM and page notes exist to be terse, which means they state conclusions where the email stated something hedged — "they chose another vendor" for an email that said only "we've decided to move in a different direction." A brief written off the notes inherits the assertion without the evidence behind it, and the failure is not academic: Shaw may repeat the confident version to the person who wrote the careful one. When a claim will shape how he opens — who won, what they committed to, why they passed — read the message it came from and use their actual words. Where the notes turn out to overstate, that's worth flagging back to Shaw, since the CRM will keep briefing off it.

### 5. Web search the company and everyone on the call

Do a quick web search on the company and on **every named attendee**, not just the primary contact. You're looking for:

- **Company**: what they do, approximate size, business model, anything notable (acquisitions, funding, industry position). A few sentences, not a report.
- **Each person**: role, title, brief career background. Just enough so Shaw knows who he's talking to without asking anyone to walk through their resume.

On a group call, who the contact chooses to bring is itself a signal — an IT or security lead, an ops/process owner, a finance gatekeeper, or a senior sponsor each tells you what the conversation is really about. Pull each attendee's email and name from the calendar event, and don't let Shaw walk in cold on anyone in the room. (For a 1:1 call this is just the one person.)

**A new invite's attendee list doesn't tell you who was on the last call.** Reading a change in the room is high-value — a commercial lead appearing means they're moving to paper, an ops lead means they're testing feasibility — but the comparison only works against who was *actually* there, not against who was on the previous invite. People get added by a forwarded link or a mid-call "let me pull someone in," and none of that shows up on the original event. Before calling anything an escalation or a swap, check the invite *thread* in Gmail for the prior call, since a re-sent link often reveals a cc who never appeared as a calendar attendee. A confidently wrong staffing read is worse than none: Shaw may walk in and reference a first meeting the person was already on.

When you state someone's role, get it from the primary source — open and read their actual profile (usually LinkedIn). Titles pulled from search-result snippets, conference posts, or the search engine's own summary are point-in-time and drift; a role you saw in a two-year-old event blurb may be stale or belong to a different person who shares the name. LinkedIn is gated and JavaScript-rendered, so `web_fetch` comes back as an empty shell — use the Chrome browser tools (`navigate` then `get_page_text`) to read the page for real. **A browser tool reporting itself unavailable is worth one retry before you fall back** — the extension drops connection transiently and usually reconnects on the next call, so accepting the first failure trades a confirmed title for a search-engine guess. This matters most in an unattended scheduled run, where nobody is around to notice the brief quietly downgraded to "couldn't confirm." And read the role *body*, not just the headline title: what someone actually does day to day (their function) matters more for the call than their HR title, and the two often diverge — a "Director of X" whose work is really go-to-market, or vice versa. Characterizing someone from the title alone is how you produce a confident block that's quietly wrong. If you can only match a person by an email handle and can't open a profile to confirm, say "couldn't confirm role" rather than borrowing a plausible-looking title.

Don't try to draw deep conclusions from web research. The goal is factual background, not analysis. Insights about their pain points, goals, and motivations are for the call itself.

### 6. Write the brief to the call page

**First, check whether the page already carries a complete, current brief — if it does, don't regenerate it.** This skill can run against the same page more than once: CRM Workflow 7 writes the brief at booking, and a morning call-research sweep can hit the same page again hours later. When the Pre-Call Research and Prioritized Questions are already present and still accurate, leave them in place and report the page as ready. Only refresh a section when something material changed since it was written — a new email thread, a reschedule, an added attendee, a corrected role, or — for a 1:1 Claude Workshop — a newly-submitted intake form (the page's use-case list and Read call depend on it, so a stale "intake not submitted" line is a strong signal to re-check the responses Sheet). Reproducing near-identical content wastes effort and risks clobbering hand-edits Shaw made on the page; this restraint is what makes a scheduled or repeat run safe.

**An ABA Calls page opens with `## Context`, above the brief.** That section is not yours to
regenerate — it carries the durable intake facts (business, topics, audience, size, how they heard
about Shaw) that used to be database properties before the 9/18/26 refactor. Write it when
creating a page from fresh intake answers; otherwise leave it alone and add the brief beneath it.
`crm/references/context-sections.md` governs what goes inside.

Do not confuse it with the **Context from prior touchpoints** block *inside* Pre-Call Research
below — that one is this-call prep and is disposable. `## Context` is what is still true at the
next call. Two things named Context on one page is a known trap; the durability test is what
separates them.

Write the pre-call brief directly to the person's call page in Notion. The brief has two sections:

**Pre-Call Research** — short blocks, glanceable before a call. Each block is **1-2 sentences flat** — no bullet lists of details, no quoted excerpts, no stacked interpretive paragraphs. If a block is growing into a sub-document, you've over-researched the page; compress.

- **Person**: who they are, their role, and background. On a multi-person call, give each additional attendee their own short block (name, role, and why they're likely in the room) held to the same 1-2 sentence discipline — for a 1:1 this is just the single block.
- **Company**: what the company does, size, anything notable
- **From emails**: what the email exchange revealed — what they asked for, how they described their situation, any signals worth noting
- **Read**: a one-line take on what the research adds up to — the angle Shaw should walk in with, or the tension worth probing live. Skip if there's nothing useful to say.
- **Context from prior touchpoints** (client check-ins and lead check-ins): for clients, what Shaw covered in prior sessions and where things left off (pull from ABA Trainings pages on the Engagements row); for leads, what came up in the discovery call and any prior conversations.

The brief exists to be glanced at before a call, not studied. If something can be said in one sentence, don't use two.

**On a partner call the brief follows the *Partner Call* SOP's Pre-call research step**, which adds the prior touchpoint's outcome, Shaw's settled positions pulled forward from the Friends record, and the other side's unagreed assumptions. When the deal structure is still open, say so in the Read and name the live options; the questions then aim at closing that gap.

**Prioritized Questions** — the matching event-type SOP's question bank sets the frame (usually an opener or two about why this matters to them); the rest come from what they've already told you. Anything the person wrote before the call — a reply to the pre-call email, intake free text, a "wants to discuss" list — is the richest source, because it's their agenda in their own words. Turn each thing they raised into a follow-up one level deeper than what they wrote: what they mean by a term they used, a concrete recent example, the number behind a claim, where the tool they chose fell short, the thing they mentioned in motion. Group follow-ups under the topic they came from. The Read is where these should point — a question that wouldn't change after reading their email came from the bank, not the research. Use the fewest questions that cover what matters; there's no target count, and each extra one dilutes the focus. Skip the annotation when the question speaks for itself.

When there's nothing firsthand — you only know them through someone else — the right set is the plainest arc that gets them talking: what they built, why, how it works today. Sharp questions need the plain answers first; asking one cold makes the person defend a thing they haven't described yet.

**Where a call page carries an agenda, it's a running order — not a second copy of the brief.** The lines are bare: the phase, nothing else. Per-line explanations and time boxes restate what Prioritized Questions already says and go stale the moment the call moves. When the questions *are* the middle of the call, the agenda points at them rather than reproducing them — a line like `What? Why? How?` carries the arc, and the questions section holds the wording. (A 1:1 Claude Workshop agenda is the exception: it's a fixed SOP template, so it comes over verbatim.)

After writing to Notion, let Shaw know it's ready. He'll review it there and follow up with questions in chat — for example, if the brief mentions an unfamiliar industry term, he'll ask about it and you can discuss. The brief is a starting point for conversation, not a finished deliverable.

**Delivery sessions:** after the brief, add the Pre-session checklist and Agenda (see "Delivery sessions" above).

### 7. Add Call Notes section

Add a `Call Notes` section immediately after `Prioritized Questions`. Leave it blank — this is where Shaw will capture live notes during the call.

The organizer owns the transcript. When the event was created from someone else's account, Shaw's auto-transcription doesn't run on it, so the section opens with a bare reminder bullet — `‼️ Transcribe meeting` — above the blank space. Read the organizer off the calendar event rather than inferring it from who booked or who leads the relationship; a client contact who sends the invite is the common case. The bullet stays bare — naming whose invite it was explains something Shaw already knows.

### 8. Add follow-up section

Add a `Follow-up` section at the bottom of the call page (after `Call Notes`) with a blank space for Shaw to fill in during/after the call. This is where next steps, action items, and proposals go.

## Question banks live in the SOPs

This skill used to carry the question banks inline. They now live in the event-type SOPs — one bank per call type — so there's a single source of truth and the banks evolve with the SOPs. To pick the prioritized questions in Step 6, find the matching SOP on the SOPs page (see "Key Locations" above) and select from its bank. For check-ins, the base *Check-in Call* SOP carries the shared relational question bank, while *Check-in Call (1:1 Claude Workshop)* carries the 4Rs agenda. The same goes for the 4Rs framework referenced by the Check-in and Wrap-up SOPs — those SOPs link the canonical 4Rs Framework page; don't restate it here.

## Principles

**Research the overhead, not the insights.** The purpose of pre-call research is to cover the things that don't need to be discussed on the call — company background, person's role, what's already been said in emails. The call is for everything that can't be discovered through web search or talking to AI chatbots: their actual experience, their pain points, their goals in their own words.

**Don't over-signal your research.** The brief is for Shaw's eyes, not the prospect's. But the suggested questions should still feel natural and curious — not like "I already know you have 300 employees, so let's talk about team training." Let the other person share context on their own terms.

**Keep questions open-ended.** Good questions invite the person to share their world. Avoid leading questions that presume an answer or push toward a specific offering. If a question sounds like it's setting up a sales pitch, reframe it or drop it.

**Confirm the outcome, not the mechanism.** A call page's prep notes often record who was supposed to do something — "[Person] owns the company-wide invite." That's an assumption captured at planning time, not a requirement. When you check the item, check whether the thing happened: the invite exists, the room is booked, the questions got asked. A deliverable met by a different route than the page guessed is still met, and reporting it as a gap sends Shaw chasing a problem that isn't there.

The same restraint governs anything you couldn't find. "Couldn't confirm" is the honest output when a search comes back empty; "didn't happen" is a positive claim and needs a positive check behind it. This matters most in an unattended scheduled run, where nobody is around to catch a confident negative before it lands in the report as an action item.

