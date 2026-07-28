---
name: pre-call-research
description: Do pre-call research for an upcoming call — a discovery call, a paid 1:1 Claude Workshop, a post-session or nurture check-in call, or a multi-session engagement wrap-up call. Use this skill whenever Shaw asks to prep for a call, do pre-call research, or gather context before any conversation — including phrases like "do pre-call research for X", "prep for my call with X", "I have a call with X today", "what should I do to prepare for X's call", or any reference to preparing for an upcoming call. Also trigger when Shaw mentions a specific person's name alongside a scheduled call. Even casual mentions like "call with X later" or "meeting with X, what should I know?" should trigger this skill. Also invoked by CRM Workflow 7 (Discovery Call Intake) to create and populate the ABA Calls page for a freshly-booked discovery call. Covers prospects, active clients, and past clients alike.
---

# Pre-Call Research

Gather the "overhead" context for an upcoming call so Shaw can spend call time on the things only the other person can share — their world, their pain points, their personal experience. Web research, CRM data, and past session notes handle the factual background; the call handles everything else.

This skill is a **router**, not a content store. It owns the *mechanics* of prep — finding the person, determining the call type, pulling the CRM record, reading Gmail, web research, and writing the brief to the call page. The *content* of each call type — its question bank, its tone, what the brief should emphasize — lives in that call type's event-type SOP. This skill points at the SOP; it does not restate it.

## The four call types

Each maps to an event-type SOP. SOPs aren't hardcoded by ID — find the matching SOP on the SOPs page (see `notion-helper/SKILL.md` → "Event-Type SOPs" for how to discover them), then read it when prepping.

- **Discovery Call** — pre-sale conversation with a lead. Discovery-focused. The brief goes on an ABA Calls page. SOP: *Discovery Call*.
- **1:1 Claude Workshop** — the paid 1:1 delivery session. The brief goes on an ABA Trainings page and is paired with a Pre-session checklist and Agenda (see "Training pages" under Step 6). SOP: *1:1 Claude Workshop*.
- **Check-in Call** — a relational touchpoint with a client or warm lead, in one of three contexts: (1) *after a 1:1 session* — the ~1-week post-workshop 4Rs call (Results, Reviews, Referrals, Resells), SOP: *Check-in Call (1:1 Claude Workshop)*; (2) a periodic client nurture check-in (4Rs not forced), SOP: *Check-in Call (Client Nurture)*; (3) a lead nurture check-in — warm but not-yet-converted, often pre-booked off a discovery call (no 4Rs, no engagement context yet), SOP: *Check-in Call (Lead Nurture)*. Identify which from CRM status and recency. The brief goes on an ABA Calls page. The shared Setup, relational call bank, and post-call mechanics live in the base *Check-in Call* SOP; each spoke above adds its own context.
- **Wrap-up Call** — end of a *group / multi-session training engagement*, days-to-weeks after it wraps, with company contacts (champion, buyer, leadership). Recommendations + the 4Rs. The brief goes on an ABA Calls page. SOP: *Wrap-up Call*.

## Key Locations

Canonical Notion IDs for the main databases live in `notion-helper/SKILL.md` → "Main Databases." Event-type SOPs aren't hardcoded by ID — discover them on the SOPs page (see `notion-helper/SKILL.md` → "Event-Type SOPs" for how). CRM-specific sub-databases (Active Leads, Clients Nurture) and the Gmail account are documented in `crm/SKILL.md`. The key resources are:

- **Active Leads database** — CRM entries with status, notes, email, source
- **Clients (Nurture) database** — past clients with engagement history, check-in cadence, and expansion signals
- **ABA Calls database** — call pages where pre-call briefs and notes live (Discovery, Check-in, Wrap-up)
- **ABA Trainings database** — delivery sessions (1:1 workshops, trainings, engagements) with session content and notes
- **Engagements database** — won-deal project ledger; a client's engagement row links the ABA Trainings pages that hold prior session context
- **Gmail** — shaw@aibuilder.academy, where all email threads with leads and clients live

## Workflow

### 1. Find the person and determine call type

Search both the Active Leads database and the Clients (Nurture) database for the person's name. Pull their email, status, source, and notes. Also search the ABA Calls and ABA Trainings databases for any existing pages with this person's name — past calls and delivery sessions are essential context.

Determine the call type from what the call *is*, cross-checked against where the person sits:

- **A lead in Active Leads, early-stage / pre-sale** → **Discovery Call**.
- **A paid 1:1 delivery session** (there's an ABA Trainings page, an engagement row, or Shaw describes it as the workshop itself) → **1:1 Claude Workshop**.
- **A client in Clients (Nurture)**, and the call is either ~1 week after a 1:1 session or a periodic nurture touch → **Check-in Call** (client context). Use recency to tell the two sub-contexts apart: a recently-ended 1:1 session means the post-session 4Rs context → *Check-in Call (1:1 Claude Workshop)*; 6+ weeks out means the relational nurture context → *Check-in Call (Client Nurture)*.
- **A lead in Active Leads with a check-in on the calendar** (warm but not converted — often pre-booked off a discovery call) → **Check-in Call** (lead nurture context) → *Check-in Call (Lead Nurture)*. No 4Rs, no engagement to pull from.
- **The end of a group / multi-session training engagement**, with company contacts → **Wrap-up Call**.
- **Found in both Active Leads and Clients** → the Clients entry takes precedence. They're a past client, not a prospect.

If the call type is genuinely ambiguous, or the person isn't in any database and Shaw hasn't pointed you to a source, ask rather than assuming.

### 2. Find or create the call page

Search the ABA Calls database (or ABA Trainings, for a 1:1 Claude Workshop) for the person's name. This is where the pre-call brief will go.

- **Invoked by CRM Workflow 7 (Discovery Call Intake):** create the ABA Calls page and link it bidirectionally with the CRM record, without asking first. In the Workflow 7 flow, this skill is the **single creator** of that page — Workflow 7 does not also create it, so it never gets made twice.
- **Invoked any other way:** if there's no page yet, ask Shaw before creating one.

### 3. Check for previous call notes

If the CRM notes reference earlier calls, or earlier ABA Calls / ABA Trainings pages exist for this person, read them. Previous call context is valuable — it means this isn't a cold conversation and you should understand what was discussed before so Shaw doesn't re-tread old ground. For client calls, the engagement row's linked ABA Trainings pages are the canonical record of what Shaw actually delivered. When those pages link call transcripts (Google Docs), read the transcripts, not just the page notes — for results-driven calls like wrap-ups and check-ins, the honest per-use-case numbers and quotable lines live in the transcript, while the notes only carry the gist.

### 4. Pull the Gmail thread

Search Gmail for messages to/from the person's email address. Read the full thread. Email exchanges often contain context that the CRM notes compress out — tone, specific asks, how they described their situation in their own words.

### 5. Web search the company and everyone on the call

Do a quick web search on the company and on **every named attendee**, not just the primary contact. You're looking for:

- **Company**: what they do, approximate size, business model, anything notable (acquisitions, funding, industry position). A few sentences, not a report.
- **Each person**: role, title, brief career background. Just enough so Shaw knows who he's talking to without asking anyone to walk through their resume.

On a group call, who the contact chooses to bring is itself a signal — an IT or security lead, an ops/process owner, a finance gatekeeper, or a senior sponsor each tells you what the conversation is really about. Pull each attendee's email and name from the calendar event, and don't let Shaw walk in cold on anyone in the room. (For a 1:1 call this is just the one person.)

When you state someone's role, get it from the primary source — open and read their actual profile (usually LinkedIn). Titles pulled from search-result snippets, conference posts, or the search engine's own summary are point-in-time and drift; a role you saw in a two-year-old event blurb may be stale or belong to a different person who shares the name. LinkedIn is gated and JavaScript-rendered, so `web_fetch` comes back as an empty shell — use the Chrome browser tools (`navigate` then `get_page_text`) to read the page for real. And read the role *body*, not just the headline title: what someone actually does day to day (their function) matters more for the call than their HR title, and the two often diverge — a "Director of X" whose work is really go-to-market, or vice versa. Characterizing someone from the title alone is how you produce a confident block that's quietly wrong. If you can only match a person by an email handle and can't open a profile to confirm, say "couldn't confirm role" rather than borrowing a plausible-looking title.

Don't try to draw deep conclusions from web research. The goal is factual background, not analysis. Insights about their pain points, goals, and motivations are for the call itself.

### 6. Write the brief to the call page

**First, check whether the page already carries a complete, current brief — if it does, don't regenerate it.** This skill can run against the same page more than once: CRM Workflow 7 writes the brief at booking, and a morning call-research sweep can hit the same page again hours later. When the Pre-Call Research and Prioritized Questions are already present and still accurate, leave them in place and report the page as ready. Only refresh a section when something material changed since it was written — a new email thread, a reschedule, an added attendee, a corrected role, or — for a 1:1 Claude Workshop — a newly-submitted intake form (the page's use-case list and Read call depend on it, so a stale "intake not submitted" line is a strong signal to re-check the responses Sheet). Reproducing near-identical content wastes effort and risks clobbering hand-edits Shaw made on the page; this restraint is what makes a scheduled or repeat run safe.

Write the pre-call brief directly to the person's call page in Notion. The brief has two sections:

**Pre-Call Research** — short blocks, glanceable before a call. Each block is **1-2 sentences flat** — no bullet lists of details, no quoted excerpts, no stacked interpretive paragraphs. If a block is growing into a sub-document, you've over-researched the page; compress.

- **Person**: who they are, their role, and background. On a multi-person call, give each additional attendee their own short block (name, role, and why they're likely in the room) held to the same 1-2 sentence discipline — for a 1:1 this is just the single block.
- **Company**: what the company does, size, anything notable
- **From emails**: what the email exchange revealed — what they asked for, how they described their situation, any signals worth noting
- **Read**: a one-line take on what the research adds up to — the angle Shaw should walk in with, or the tension worth probing live. Skip if there's nothing useful to say.
- **Context from prior touchpoints** (client check-ins and lead check-ins): for clients, what Shaw covered in prior sessions and where things left off (pull from ABA Trainings pages on the Engagements row); for leads, what came up in the discovery call and any prior conversations.

The brief exists to be glanced at before a call, not studied. If something can be said in one sentence, don't use two.

**Prioritized Questions** — select **3-4 questions max** from the **matching event-type SOP's question bank** — the ones that fill the biggest gaps after the research. The SOP owns the bank and the tone for that call type; don't keep a copy here. More than 3-4 and the brief stops being a focusing tool and becomes a checklist. Each question gets a one-line note explaining why it's high-leverage for this specific person; skip the annotation when the question speaks for itself.

After writing to Notion, let Shaw know it's ready. He'll review it there and follow up with questions in chat — for example, if the brief mentions an unfamiliar industry term, he'll ask about it and you can discuss. The brief is a starting point for conversation, not a finished deliverable.

**Training pages (ABA Trainings):** When the brief is for a 1:1 Claude Workshop (written to an ABA Trainings page rather than ABA Calls), add a **Pre-session** checklist after the brief's `---` divider. This is the prep Shaw runs through 24 hours before the session. Include:

```
Pre-session
- [Intake responses (Sheet)](https://docs.google.com/spreadsheets/d/[sheet-id]/edit)
- Rank use cases best (high impact, high probability of success) to worst (low impact, low probability of success)
- Send agenda 24-hr before
```

Then add the standard **Agenda** section from the 1:1 Claude Workshop SOP. The Pre-session + Agenda block goes after the research brief, separated by a `---` divider.

### 7. Add Call Notes section

Add a `Call Notes` section immediately after `Prioritized Questions`. Leave it blank — this is where Shaw will capture live notes during the call.

### 8. Add follow-up section

Add a `Follow-up` section at the bottom of the call page (after `Call Notes`) with a blank space for Shaw to fill in during/after the call. This is where next steps, action items, and proposals go.

## Question banks live in the SOPs

This skill used to carry the question banks inline. They now live in the event-type SOPs — one bank per call type — so there's a single source of truth and the banks evolve with the SOPs. To pick the prioritized questions in Step 6, find the matching SOP on the SOPs page (see `notion-helper/SKILL.md` → "Event-Type SOPs" for how to discover them) and select from its bank. For check-ins, the base *Check-in Call* SOP carries the shared relational question bank, while *Check-in Call (1:1 Claude Workshop)* carries the 4Rs agenda. The same goes for the 4Rs framework referenced by the Check-in and Wrap-up SOPs — those SOPs link the canonical 4Rs Framework page; don't restate it here.

## Principles

**Research the overhead, not the insights.** The purpose of pre-call research is to cover the things that don't need to be discussed on the call — company background, person's role, what's already been said in emails. The call is for everything that can't be discovered through web search or talking to AI chatbots: their actual experience, their pain points, their goals in their own words.

**Don't over-signal your research.** The brief is for Shaw's eyes, not the prospect's. But the suggested questions should still feel natural and curious — not like "I already know you have 300 employees, so let's talk about team training." Let the other person share context on their own terms.

**Keep questions open-ended.** Good questions invite the person to share their world. Avoid leading questions that presume an answer or push toward a specific offering. If a question sounds like it's setting up a sales pitch, reframe it or drop it.
