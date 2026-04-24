# Workflow 4: Link Call & Session Notes to CRM Lead Page

Use when connecting a lead's or client's CRM page to their sales call notes and/or delivery
session pages — either directly on request, or as part of Workflow 1's sync pass.

The goal is to embed `<mention-page>` links in the body of the lead's CRM page so Shaw can
click through to the full notes without having to search for them. A single lead may have
sales calls (ABA Calls) and delivery sessions (ABA Trainings) — both belong linked on the
CRM page. See SKILL.md's "Three Databases Show Up During CRM Work" section for the
distinction, and `notion-helper/SKILL.md` for database IDs.

## Principle: full rewrite, not append

Always rewrite the **full ordered list** of call links using `replace_content`. Never append
just the newest call. Appending means older calls that were never linked stay invisible
forever — which is how entire threads of context get dropped (e.g., an AI at Work Calls entry
from January that predates the lead entering the main pipeline).

Rewriting the full list every time is cheap and guarantees multi-call leads stay in sync.

## Step 1 — Gather all call pages for the person

Search broadly across every database that might hold relevant pages:

1. **ABA Calls** — sales calls (discovery, follow-ups, proposal reviews)
2. **ABA Trainings** — delivery sessions: 1:1 workshops, trainings, ongoing engagements
3. **Related call databases** — e.g., AI at Work Calls. Older research calls often belong
   linked too, because they're the earliest context Shaw has on the person.
4. **Search variations** — name, email, company name, and email domain. Pages are sometimes
   filed under company name ("[Company]" instead of "[Person]", "[Company]" instead of
   "[Person]"), and stakeholders get cc'd from the same domain.

Database IDs live in `notion-helper/SKILL.md` → "Main Databases."

## Step 2 — Fetch and confirm

Fetch each candidate page to confirm it's the right person and to pull the call date from
the `Date` property.

## Step 3 — Rewrite the CRM page content

Use `replace_content` to write the full ordered list. One line per call, formatted as:

```
Date: <mention-page url="https://www.notion.so/{page-id}"/>
```

Each call is its own paragraph (separate line). Use short month + day format (e.g., "Jan 9",
"Feb 17") and order calls chronologically. Example for a lead with three calls:

```
Jan 29: <mention-page url="https://www.notion.so/[page-id]"/>
Mar 27: <mention-page url="https://www.notion.so/[page-id]"/>
Apr 15: <mention-page url="https://www.notion.so/[page-id]"/>
```

If the CRM page has other body content beyond call links (notes, scratchwork), preserve it
by including it in the `replace_content` payload alongside the refreshed call list.
