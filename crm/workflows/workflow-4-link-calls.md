# Workflow 4: Link Call Notes to CRM Lead Page

Use when Shaw asks to connect a lead's CRM page to their call notes, or proactively when adding
call history to a lead's page for easy reference.

The goal is to embed `<mention-page>` links in the body of the lead's CRM page so Shaw can
click through to the full call notes without having to search for them.

## Step 1 — Search ABA Calls for the lead

Search the ABA Calls database (page ID: `1f25f2e2-6be9-804f-847b-d26f36563dd0`) for the lead's
name. Also search by company name or email domain — calls are sometimes filed under the company
name rather than the individual (e.g., "LeadsOnline" instead of "Travis White").

## Step 2 — Fetch each matching call page

Fetch each result to confirm it's the right person and get the call date from the `Date` property.

## Step 3 — Update the CRM lead page content

Use `replace_content` to add one line per call, formatted as:

```
Date: <mention-page url="https://www.notion.so/{page-id}"/>
```

Each call should be its own paragraph (a separate line in the content string). For example, a
lead with two calls would look like:

```
Feb 12: <mention-page url="https://www.notion.so/3055f2e26be980f590dff39d567a8c75"/>
Feb 17: <mention-page url="https://www.notion.so/30a5f2e26be9809ca9a6c76a32d8a1e7"/>
```

Use the short month + day format (e.g., "Jan 9", "Feb 17") to match how dates appear elsewhere
in the CRM. Order calls chronologically.

If the lead's CRM page already has content, preserve it and append the new call links.
