# Three-Way Intros

Patterns for drafting three-way email introductions between a new lead and one or more of Shaw's AI consultant partners. The goal is to match leads with the right consultants based on their needs.

Read this file before drafting any three-way intro email.

---

## When to Use

Shaw mentions a new lead, a contact form submission, or someone looking for an AI consultant — especially phrases like "intro", "connect these two", "draft an intro for", or when he provides a person's name + need and says to connect them with his consultants.

---

## Lead Info Needed

Extract from the conversation (or ask Shaw if missing):
- **Name** (first name used in email)
- **Email address**
- **Their need** — what are they building or looking for?

Shaw will specify which consultants to include. If he says "all consultants" or "the usual ones", use all from the roster below.

---

## Consultant Roster

> **Template — fill in with real consultant details locally.** Do NOT commit real names, companies, or emails to this public repo.

### [Consultant 1]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

### [Consultant 2]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

### [Consultant 3]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

### [Consultant 4]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

### [Consultant 5]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

### [Consultant 6]
- **Title:** [Title]
- **Company:** [Company]
- **Description:** [One-line description of what they do]
- **Email:** [email]

---

## Template

Write **one email per consultant**. Do NOT change the first line or last three lines — they are fixed.

**Subject:** `[Lead First Name] <> [Consultant First Name]`

```
Hey folks,

I wanted to connect you two because I see the potential for a fruitful collaboration.

[Lead Name], meet [Consultant Name]. [He's/She's/They're] the [Title] of [Company], [description of what they do].

[Consultant Name], meet [Lead Name]. [He's/She's] [brief description of who they are and what they're building/looking for].

Hope you two get a chance to connect :)

Cheers,
Shaw
```

**Rules:**
- "Hey folks," — always exactly this, never change it
- "Hope you two get a chance to connect :)" — always exactly this, never change it
- Keep each person's blurb to 1–2 sentences max
- Frame the lead's blurb as their specific need/opportunity (from the consultant's perspective)
- Use `<>` in the subject line (e.g. `[Lead First] <> [Consultant First]`)

---

## Gmail Draft Setup

Use `create_draft` for each email (these are fresh threads, no thread workaround needed):
- **to:** `[lead email], [consultant email]`
- **subject:** `[Lead First Name] <> [Consultant First Name]`
- **body:** the drafted email

If a consultant's email isn't in the roster, search Gmail for `[Consultant Name] from:me` and look at recent threads to find their reply-to address.

Confirm to Shaw once all drafts are saved, and flag if any consultant email was uncertain.

---

## Example

**Lead:** [Lead Name] ([email]) — building an AI-driven equity and derivatives investment platform, looking for a technical AI consultant.

**Output draft for [Consultant]:**

> Subject: [Lead First] <> [Consultant First]
>
> Hey folks,
>
> I wanted to connect you two because I see the potential for a fruitful collaboration.
>
> [Lead First], meet [Consultant First]. He's the [Title] of [Company], [one-line description of what they do].
>
> [Consultant First], meet [Lead First]. He's building an AI-driven equity and derivatives investment platform and is looking for a technical AI consultant to bring it to life.
>
> Hope you two get a chance to connect :)
>
> Cheers,
> Shaw
