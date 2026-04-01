---
name: crm
description: >
  Use this skill whenever Shaw mentions leads, contacts, sales pipeline activity, or anything
  CRM-related — even casually. Triggers include: "check my CRM", "update the CRM", "any updates
  on leads?", "add this person to the CRM", "review my pipeline", "follow up with X", "cross-reference
  Gmail", "did anyone respond?", "ABA contact form", or any mention of a specific lead's name in a
  sales context. Also triggers when Shaw shares new contact form submissions or inbound emails that
  look like potential leads. Use this skill proactively — if a conversation touches leads or sales
  activity, consult this skill before responding.
---

# CRM Skill

Shaw runs a B2B AI enablement sales pipeline. This skill governs how to read, update, and act on
his CRM in Notion, cross-reference Gmail for new activity, check call notes in Notion, add new leads,
and proactively draft follow-up emails when the rules indicate one is due.

---

## Key Locations

| Resource | Location |
|---|---|
| CRM page | Notion page ID: `21031c0a-4375-48cb-833d-4b355d70e5ee` |
| Active Leads database | Data source: `collection://c527d3fd-e4af-4c9d-8a5d-979a954ee5c9` |
| ABA Calls database | Notion page ID: `1f25f2e2-6be9-804f-847b-d26f36563dd0` |

**Gmail account:** `you@yourdomain.com` (all outbound sales activity lives here)

---

## Active Leads Database Schema

| Field | Type | Notes |
|---|---|---|
| Name | Title | Full name |
| Email | Text | Email address |
| Source | Multi-select | `LinkedIn`, `Organic`, `YouTube`, `Personal`, `ABB`, `ABA Contact` |
| Status | Multi-select | `Pending Call`, `Booked Call`, `Outline Sent`, `Closed`, `Lost` |
| Last Contact? | Date | Date of most recent touchpoint |
| Notes | Text | Short chronological log (see format below) |

### Notes Format

Short, comma-separated, date-stamped **pipeline actions only**. Never write full sentences.
Notes should record *what happened* in the sales process — not details about the lead's business,
team, tech stack, budget, or call content. That context lives in the ABA Calls page and doesn't
need to be duplicated here.

**Good examples:**
- `Warm outreach (3/4). FU (3/11). Asked about individual training (3/12). Replied about ABA (3/13).`
- `ABA contact form (3/16). Replied, offered call (3/16).`
- `Call on 3/13. Not right now. FU in April.`
- `Call w/ Marco & Lud (3/27). Sending proposal (3/28).`

**Bad example (too much context):**
- `Call w/ Marco & Lud (3/27). SumUp growth analytics, small team, already using MCP + agents. $2k L&D budget/person. Sending proposal (3/28).`

**Rules:**
- Always append new entries; never overwrite existing notes
- Use `(M/D)` date format
- Common shorthands: `FU` = follow up, `ABA` = AI Builder Academy, `ABB` = AI Builders Bootcamp
- Only include: outreach actions, call dates, proposal/outline sent, follow-ups, responses, status changes
- Do NOT include: company details, team size, tech stack, budget info, call discussion topics
- When other stakeholders are involved in a deal (e.g. a second contact on the thread), mention them
  by name so future sessions have context without re-reading the full email chain.
  Example: `Jordan (jordan.k@acmecorp.example.com) responded, evaluating proposals (3/17).`

---

## Sales Pipeline Stages

```
Contact → Book Call → Attend Call → Send Outline/Proposal → Closed
```

Status should reflect the furthest confirmed stage reached:
- **Pending Call** — call link sent or time proposed, awaiting confirmation
- **Booked Call** — call confirmed on calendar
- **Outline Sent** — proposal/outline sent after call
- **Closed** — deal won
- **Lost** — explicitly not moving forward

---

## Workflows

Read the relevant workflow file before executing. Each contains step-by-step instructions.

| Workflow | Trigger | File |
|---|---|---|
| 1. Review & Cross-Reference CRM | Shaw asks to review leads, check for updates, or audit the pipeline | `workflows/workflow-1-review.md` |
| 2. Update a Lead | Shaw shares new info about a lead (reply received, call happened, proposal sent) | `workflows/workflow-2-update.md` |
| 3. Add a New Lead | Shaw shares a new contact form submission, inbound email, or new lead | `workflows/workflow-3-add-lead.md` |
| 4. Link Call Notes to CRM Lead Page | Shaw asks to connect a lead's CRM page to their call notes from ABA Calls | `workflows/workflow-4-link-calls.md` |

---

## References

Read these when the workflow requires follow-up assessment or email drafting.

| Reference | Contents | File |
|---|---|---|
| Follow-Up Guidance | Follow-up cadences, drafting rules, tone guidance, lead source context | `references/follow-up-guidance.md` |

---

## ABA Calls — Fetching Call Notes

When deeper context is needed on a lead (e.g., what was discussed on a call, what their org situation is):

1. Search Notion for the lead's name within the ABA Calls database
2. Also search by company name or email domain — calls are sometimes filed under the company
   name rather than the individual
3. Fetch the matching page to read call notes
4. Use that context to inform CRM updates, proposal framing, or follow-up tone

Call notes often contain: org context, budget/mandate clarity, audience size, stated next steps,
and Shaw's own follow-up intentions.

To link call notes directly in the lead's CRM page for easy access, see **Workflow 4**.

---

## Key Principles

- **Always read before writing** — fetch the lead's current Notion page before making any updates
- **Append, never overwrite** — notes are a chronological log; always add to the end
- **Match Shaw's voice** — short, direct, friendly; no corporate filler
- **Don't over-follow-up** — respect the cadence limits; after FU #2 on contact form leads, stop
- **Update Last Contact? on every touchpoint** — keep this field current so follow-up timing is accurate
- **Default to action** — when follow-ups are due, create Gmail drafts directly rather than presenting options
