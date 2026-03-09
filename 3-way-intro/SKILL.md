---
name: 3-way-intro
description: Draft and send three-way email introductions between a new lead and one or more of your AI consultant contacts. Use this skill whenever a new lead is mentioned, a contact form submission comes in, or someone is looking for an AI consultant — especially phrases like "intro", "connect these two", "draft an intro for", or when a person's name + need is provided. Always use this skill for intro email drafting tasks, even if the user doesn't explicitly say "three-way intro".
---

# Three-Way Intro Skill

## Purpose
Draft and save Gmail drafts introducing new leads to AI consultant partners. The goal is to match leads with the right consultants based on their needs.

---

## Step 1: Gather Lead Info

Extract from the conversation (or ask if missing):
- **Name** (first name used in email)
- **Email address**
- **Their need** — what are they building or looking for?

---

## Step 2: Identify Which Consultants to Intro

The user will specify which consultants to include. Refer to the roster below for their details.

If the user says "all consultants" or "the usual ones", use all entries from the roster.

---

## Consultant Roster

> ✏️ Replace the entries below with your actual consultant contacts.

### [Consultant Name]
- **Title:** [e.g. CEO]
- **Company:** [Company Name]
- **Description:** [One sentence describing what their firm does]
- **Email:** [consultant@example.com]

### [Consultant Name]
- **Title:** [e.g. Founder]
- **Company:** [Company Name]
- **Description:** [One sentence describing what their firm does]
- **Email:** [consultant@example.com]

---

## Step 3: Draft the Emails

Write **one email per consultant**. Use this exact template — do NOT change the first line or last three lines:

---

**Subject:** `[Lead First Name] <> [Consultant First Name]`

Hey folks,

I wanted to connect you two because I see the potential for a fruitful collaboration.

[Lead Name], meet [Consultant Name]. [He's/She's/They're] the [Title] of [Company], [description of what they do].

[Consultant Name], meet [Lead Name]. [He's/She's/They're] [brief description of who they are and what they're building/looking for].

Hope you two get a chance to connect :)

Cheers,
[Your Name]

---

**Rules:**
- "Hey folks," — always exactly this, never change it
- "Hope you two get a chance to connect :)" — always exactly this, never change it
- Keep each person's blurb to 1–2 sentences max
- Frame the lead's blurb as their specific need/opportunity (from the consultant's perspective)
- Use `<>` in the subject line (e.g. `Alex <> Jordan`)

---

## Step 4: Look Up Consultant Emails (if needed)

If a consultant's email isn't in the roster above, search Gmail:
```
[Consultant Name] from:me
```
Look at recent threads to find their reply-to address.

---

## Step 5: Save as Gmail Drafts

Use the `Gmail:gmail_create_draft` tool for each email:
- **to:** `[lead email], [consultant email]`
- **subject:** `[Lead] <> [Consultant]`
- **body:** the drafted email

Confirm to the user once all drafts are saved, and flag if any consultant email was uncertain.

---

## Example (Reference)

**Lead:** Alex Chen (alex.chen@example.com) — building an AI-driven equity and derivatives investment platform, looking for a technical AI consultant.

**Output draft for Jordan:**

> Subject: Alex <> Jordan
>
> Hey folks,
>
> I wanted to connect you two because I see the potential for a fruitful collaboration.
>
> Alex, meet Jordan. He's the CEO of [Consultant Company], an organization specializing in building AI and LLM projects for clients.
>
> Jordan, meet Alex. He's building an AI-driven equity and derivatives investment platform and is looking for a technical AI consultant to bring it to life.
>
> Hope you two get a chance to connect :)
>
> Cheers,
> [Your Name]
