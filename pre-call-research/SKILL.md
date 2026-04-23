---
name: pre-call-research
description: Do pre-call research for an upcoming call — whether it's a sales discovery call, a post-engagement follow-up, or a long-term client check-in. Use this skill whenever Shaw asks to prep for a call, do pre-call research, or gather context before any conversation — including phrases like "do pre-call research for X", "prep for my call with X", "I have a call with X today", "what should I do to prepare for X's call", or any reference to preparing for an upcoming call. Also trigger when Shaw mentions a specific person's name alongside a scheduled call. Even casual mentions like "call with X later" or "meeting with X, what should I know?" should trigger this skill. Covers prospects, active clients, and past clients alike.
---

# Pre-Call Research

Gather the "overhead" context for an upcoming call so Shaw can spend call time on the things only the other person can share — their world, their pain points, their personal experience. Web research, CRM data, and past session notes handle the factual background; the call handles everything else.

This skill handles three call types, each with a different question bank and tone:

- **Prospect/sales call** — first-time or early-stage conversation with a lead. Discovery-focused.
- **Post-engagement follow-up** — days or weeks after a paid session (workshop, coaching, training). Homework review + the 4Rs (Results, Reviews, Referrals, Resells). The experience is fresh, so this is the best time to collect concrete outcomes and testimonials.
- **Long-term nurture check-in** — 6-12+ weeks since the last engagement. Genuine relationship check-in: hear their problems, see what's changed, surface expansion signals naturally. The 4Rs are not the focus here — the conversation should feel relational, not transactional.

## Key Locations

Canonical Notion IDs live in `notion-helper/SKILL.md` → "Main Databases." CRM-specific sub-databases (Active Leads, Clients Nurture) and the Gmail account are documented in `crm/SKILL.md`. The key resources are:

- **Active Leads database** — CRM entries with status, notes, email, source
- **Clients (Nurture) database** — past clients with engagement history, check-in cadence, and expansion signals
- **ABA Calls database** — call pages where pre-call briefs and notes live
- **ABA Trainings database** — delivery sessions (1:1 workshops, trainings, ongoing engagements) with session content and notes
- **Gmail** — [email], where all email threads with leads and clients live

## Workflow

### 1. Find the person and determine call type

Search both the Active Leads database and the Clients (Nurture) database for the person's name. Pull their email, status, source, and notes.

Based on where you find them, determine the call type:
- **Found in Active Leads** → this is a **prospect/sales call**. Use the Sales Discovery Question Bank.
- **Found in Clients (Nurture)** → check recency. If the last engagement ended within the past few weeks, this is a **post-engagement follow-up** (use the Post-Engagement Question Bank + 4Rs). If it's been 6+ weeks, this is a **long-term nurture check-in** (use the Nurture Check-In Question Bank).
- **Found in both** → the Clients entry takes precedence. They're a past client, not a prospect.

Also search the ABA Trainings database for delivery pages (1:1 workshops, trainings, ongoing engagements) with this person's name. These give you the content of what Shaw actually covered with them — essential context for any client call.

If the person isn't in either database, Shaw may point you to a different data source. Ask rather than assuming.

### 2. Find or create the call page

Search the ABA Calls database for the person's name. This is where the pre-call brief will go. If there's no page yet, ask Shaw before creating one.

### 3. Check for previous call notes

If the CRM notes reference earlier calls with this person, find those call pages in the ABA Calls database and read them. Previous call context is valuable — it means this isn't a cold conversation and you should understand what was discussed before so Shaw doesn't re-tread old ground.

### 4. Pull the Gmail thread

Search Gmail for messages to/from the person's email address. Read the full thread. Email exchanges often contain context that the CRM notes compress out — tone, specific asks, how they described their situation in their own words.

### 5. Web search the company and person

Do a quick web search on both the company and the individual. You're looking for:

- **Company**: what they do, approximate size, business model, anything notable (acquisitions, funding, industry position). A few sentences, not a report.
- **Person**: role, title, brief career background. Just enough so Shaw knows who he's talking to without asking them to walk through their resume.

Don't try to draw deep conclusions from web research. The goal is factual background, not analysis. Insights about their pain points, goals, and motivations are for the call itself.

### 6. Write the brief to the call page

Write the pre-call brief directly to the person's call page in Notion. The brief has two sections:

**Pre-Call Research** — short blocks, glanceable before a call:
- **Person**: 1-2 sentences on who they are, their role, and background
- **Company**: 1-2 sentences on what the company does, size, and anything notable
- **From emails**: 1-2 sentences on what the email exchange revealed — what they asked for, how they described their situation, any signals worth noting
- **Context from previous sessions** (client calls only): summary of what Shaw covered with them, what homework was assigned, and where things left off. Pull this from the ABA Trainings pages.

Less is more. If something can be said in one sentence, don't use two. The brief exists to be glanced at before a call, not studied.

**Prioritized Questions** — select from the question bank below based on what gaps remain after the research. Each question gets a one-line note explaining why it's high-leverage for this specific person given what we already know. Skip questions that the research already answers, and skip reasoning annotations when the question speaks for itself.

After writing to Notion, let Shaw know it's ready. He'll review it there and follow up with questions in chat — for example, if the brief mentions an unfamiliar industry term, he'll ask about it and you can discuss. The brief is a starting point for conversation, not a finished deliverable.

### 7. Add Call Notes section

Add a `Call Notes` section immediately after `Prioritized Questions`. Leave it blank — this is where Shaw will capture live notes during the call.

### 8. Add follow-up section

Add a `Follow-up` section at the bottom of the call page (after `Call Notes`) with a blank space for Shaw to fill in during/after the call. This is where next steps, action items, and proposals go.

## Question Banks

Use the question bank that matches the call type identified in Step 1. Don't use all questions from any bank — pick the ones that fill the most gaps given what the research already uncovered. Each question should get a brief tailored note explaining why it's relevant for this specific person.

### Sales Discovery (prospect/sales calls)

1. Why are you looking for AI training?
2. What have you tried so far?
3. What do you want to be able to do that you can't today?
4. What does your team do?
5. What are your goals?
6. What tools/AI do you use now?
7. What's been the hardest part?
8. Why do you even bother? Why is this important?
9. If this were working really well, what would be different?

### Post-Engagement Follow-Up (days/weeks after a paid session)

The goal is to review what they've done since the engagement and collect the 4Rs while the experience is fresh.

**Homework / progress review:**
- Walk me through what you built since last time.
- What tripped you up?

**4Rs** (collect at the end of every post-engagement call):
- **Results** — concrete "before → after" metrics. "What can you do now that you couldn't before, or what takes way less time?"
- **Reviews** — testimonial around time saved / clarity. "Would you share a quick testimonial — even a few sentences on what changed?"
- **Referrals** — tap their network. "Who else in your world would this help?"
- **Resells** — upsell to ongoing advisory or team rollout. "Would it make sense to keep going, or bring in other people from your team?"

### Long-Term Nurture Check-In (6-12+ weeks since last engagement)

The goal is a genuine relationship check-in — hear their problems, see what's changed, surface expansion signals naturally. This should feel relational, not transactional. The 4Rs are not the focus here.

1. How's it going? What have you been working on?
2. What's been the hardest part lately?
3. What problems are eating up your time right now?
4. Has anything changed since we last talked — new projects, new team members, new challenges?
5. Is there anything I can help with?

## Principles

**Research the overhead, not the insights.** The purpose of pre-call research is to cover the things that don't need to be discussed on the call — company background, person's role, what's already been said in emails. The call is for everything that can't be discovered through web search or talking to AI chatbots: their actual experience, their pain points, their goals in their own words.

**Don't over-signal your research.** The brief is for Shaw's eyes, not the prospect's. But the suggested questions should still feel natural and curious — not like "I already know you have 300 employees, so let's talk about team training." Let the other person share context on their own terms.

**Keep questions open-ended.** Good questions invite the person to share their world. Avoid leading questions that presume an answer or push toward a specific offering. If a question sounds like it's setting up a sales pitch, reframe it or drop it.
