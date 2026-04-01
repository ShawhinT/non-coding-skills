---
name: pre-call-research
description: Do pre-sales call research for an upcoming call. Use this skill whenever Shaw asks to prep for a call, do pre-call research, or gather context before a sales conversation — including phrases like "do pre-call research for X", "prep for my call with X", "I have a call with X today", or any reference to preparing for an upcoming sales call. Also trigger when Shaw mentions a specific person's name alongside a scheduled call. Even casual mentions like "call with X later" or "meeting with X, what should I know?" should trigger this skill.
---

# Pre-Call Research

Gather the "overhead" context for an upcoming sales call so Shaw can spend call time on the things only the other person can share — their world, their pain points, their personal experience. Web research and CRM data handle the factual background; the call handles everything else.

## Key Locations

This skill relies on the same data sources as the CRM skill. See `mnt/.claude/skills/crm/SKILL.md` for the canonical Notion IDs and Gmail account. The key resources are:

- **Active Leads database** — CRM entries with status, notes, email, source
- **ABA Calls database** — call pages where pre-call briefs and notes live
- **Gmail** — you@yourdomain.com, where all email threads with leads live

## Workflow

### 1. Find the person in the CRM

Search the Active Leads database for the person's name. Pull their email, status, source, and notes. The notes are a chronological log of pipeline activity — they tell you what's happened so far (outreach dates, call history, proposals sent, etc.).

If the person isn't in the CRM, Shaw may point you to a different data source. Ask rather than assuming.

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

**Pre-Call Research** — three short blocks:
- **Company**: 1-2 sentences on what the company does, size, and anything notable
- **Person**: 1-2 sentences on who they are, their role, and background
- **From emails**: 1-2 sentences on what the email exchange revealed — what they asked for, how they described their situation, any signals worth noting

Less is more. If something can be said in one sentence, don't use two. The brief exists to be glanced at before a call, not studied.

**Prioritized Questions** — select from the question bank below based on what gaps remain after the research. Each question gets a one-line note explaining why it's high-leverage for this specific person given what we already know. Skip questions that the research already answers, and skip reasoning annotations when the question speaks for itself.

After writing to Notion, let Shaw know it's ready. He'll review it there and follow up with questions in chat — for example, if the brief mentions an unfamiliar industry term, he'll ask about it and you can discuss. The brief is a starting point for conversation, not a finished deliverable.

### 7. Add follow-up section

Add a `Follow-up` section at the bottom of the call page with a blank space for Shaw to fill in during/after the call. This is where next steps, action items, and proposals go.

## Question Bank

These are Shaw's standard discovery questions for sales calls. Don't use all of them — pick the ones that fill the most gaps given what the pre-call research already uncovered.

1. Why are you looking for AI training?
2. What have you tried so far?
3. What do you want to be able to do that you can't today?
4. What does your team do?
5. What are your goals?
6. What tools/AI do you use now?
7. What's been the hardest part?
8. Why do you even bother? Why is this important?
9. If this were working really well, what would be different?

## Principles

**Research the overhead, not the insights.** The purpose of pre-call research is to cover the things that don't need to be discussed on the call — company background, person's role, what's already been said in emails. The call is for everything that can't be discovered through web search or talking to AI chatbots: their actual experience, their pain points, their goals in their own words.

**Don't over-signal your research.** The brief is for Shaw's eyes, not the prospect's. But the suggested questions should still feel natural and curious — not like "I already know you have 300 employees, so let's talk about team training." Let the other person share context on their own terms.

**Keep questions open-ended.** Good questions invite the person to share their world. Avoid leading questions that presume an answer or push toward a specific offering. If a question sounds like it's setting up a sales pitch, reframe it or drop it.
