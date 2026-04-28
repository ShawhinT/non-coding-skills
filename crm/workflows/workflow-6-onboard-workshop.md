# Workflow 6: Onboard Workshop Participant

Use when a new participant is accepted for a free 1:1 Claude Workshop (or similar delivery
session) and needs to be set up in the system.

This workflow creates three things and connects them:

1. **ABA Trainings page** — the session page where pre-session prep and call notes will live.
   Create it in the ABA Trainings database (`collection://[database-id]`),
   not as a child page of the workshop parent. Set `Name` to `"[First Name] - 1:1 Claude Workshop"`
   and `Date` to the session date. Link it on the workshop parent page's Sessions section as a
   `<mention-page>`, matching the format of existing entries.

2. **CRM entry** — an Active Lead in `collection://[page-id]`.
   Pull the participant's name, email, and timeline from Gmail threads and the workshop parent
   page. Use Source: `ABB`, Status: `Booked Call`. Notes should log the timeline in short
   `(M/D)` format (e.g., `Applied to 1:1 Claude Workshop (4/4). Accepted (4/4). Booked Thu
   Apr 16 session (4/9).`). Set `Last Contact?` to the most recent touchpoint date. In the page
   body, add a `## Calls` section linking to the ABA Trainings page.

3. **Link the ABA Trainings page on the workshop parent** — add the new page as a `<mention-page>`
   in the Sessions section of the workshop parent page (e.g., "Free Claude Automation Workshop
   1:1"). It should appear alongside the other session links, not as a child page.

(Database IDs live in `notion-helper/SKILL.md` → "Main Databases.")

## Reference: existing participants to match

Look at how prior participants are set up — their CRM entries, ABA Trainings pages, and links
on the workshop parent page are the pattern to follow.
