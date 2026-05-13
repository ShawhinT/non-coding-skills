# Workflow 3: Link a Session or Call to an Engagement

**Triggers:**
- A new ABA Trainings page is created for an active client
- A new ABA Calls page is created for an active client (mid-engagement check-in, etc.)
- Shaw says "log [Person]'s session for X" / "add this call to E#### body"
- A session gets rescheduled and the body needs updating

**Goal:** Keep the engagement's `## Sessions` and `## Calls` body sections current as new
ABA Trainings and ABA Calls pages are created throughout delivery.

---

## Steps

### 1. Identify the target engagement

Given a client name + an ABA Trainings or ABA Calls page:

1. Find the client's Clients (Nurture) page (search by name/email)
2. Open the synced "Engagements" backlink property on the Nurture page — it lists all
   engagement rows for that client
3. If multiple engagements exist (re-ups), match by date proximity:
   - The session/call should fall between the engagement's Start Date and End Date
   - If ambiguous, ask Shaw which engagement it belongs to

### 2. Fetch the engagement page

Get the current body content. Pay attention to the exact format of existing entries so the new
line matches style:

```
- <mention-page url="..."/> (M/D — name)
```

For Sessions: annotation is `(M/D — attendee name)` or `(M/D — session label)`
For Calls: annotation is `(M/D — discovery / follow-up / check-in / etc.)`

### 3. Insert the new line in chronological position

Use `update_content` with `old_str` matching an adjacent existing line, and `new_str` containing
both lines (existing + new) in chronological order.

**Example — adding a new session between two existing ones:**

```
old_str:
- <mention-page url="https://www.notion.so/page-A"/> (Apr 21 — [Attendee 1])
- <mention-page url="https://www.notion.so/page-C"/> (Apr 24 — [Attendee 3])

new_str:
- <mention-page url="https://www.notion.so/page-A"/> (Apr 21 — [Attendee 1])
- <mention-page url="https://www.notion.so/page-B"/> (Apr 22 — [Attendee 2])
- <mention-page url="https://www.notion.so/page-C"/> (Apr 24 — [Attendee 3])
```

**Example — appending to the end of Sessions section:**

If the section currently reads:

```
## Sessions

_None yet — add as ABA Trainings pages get created._
```

Replace the placeholder text with the first session line:

```
old_str:
## Sessions

_None yet — add as ABA Trainings pages get created._

new_str:
## Sessions

- <mention-page url="..."/> (M/D — name)
```

### 4. Update related fields if applicable

- If this is the **first session** for an engagement currently in `Sold` status, run
  **Workflow 2** (Sold → Active) in the same pass.
- If this is the **last session**, ask Shaw whether to flip to Delivered now or wait until the
  session has occurred.
- If `Start Date` was blank and this is the first session being added, set Start Date to this
  session's date.

### 5. Handle reschedules

When a session moves to a different date:

1. Fetch the engagement body
2. Find the existing line for the rescheduled session
3. Replace it with the same mention-page but updated date annotation:

```
old_str:
- <mention-page url="https://www.notion.so/page-X"/> (Apr 22 — [Attendee] #1)

new_str:
- <mention-page url="https://www.notion.so/page-X"/> (May 6 — [Attendee], rescheduled from 4/22)
```

If the reschedule consolidates two previously-separate sessions into one (e.g., "[Attendee] #1" and
"[Attendee] #2" turn out to be the same session that just moved), remove the duplicate line entirely
in the same `update_content` call.

### 6. Confirm with Shaw

Reply with a one-line summary:

> Linked May 6 [Attendee] session to [E0003](url). Sessions section now has 5 entries.
