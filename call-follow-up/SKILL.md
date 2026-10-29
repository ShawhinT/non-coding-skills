---
name: "call-follow-up"
description: Process the Follow-up sections Shaw jots on his ABA Calls and ABA Trainings pages after calls. Route each open bullet to where it belongs (the next call page, an ABA task, a CRM Next Contact date, or the email task), then cross off what's handled. Works over any window Shaw names, like yesterday's calls, last week's, a specific date range, or one named call. Use whenever Shaw says "do yesterday's call follow-up", "call follow-up for last week", "follow-up for the [Name] call", "what did I jot down after my calls", "carry this to next week's call", "what's still open from this week's calls", or "clean up my follow-up sections". The morning scheduled task also runs it for the previous day. Do NOT use for drafting the follow-up emails themselves (the email task and email-helper own those) or for pre-call research (meeting-prep).
---

# Call Follow-up

After a call, Shaw writes terse bullets under the page's `## Follow-up` heading. Some are
content for the follow-up email, some are things to raise next time, some are his own to-dos,
and some are already done by the time anyone looks. A separate email task handles the email.
This skill handles the rest: it gets each bullet to the place Shaw will see it when it matters,
then crosses it off so the page shows only what's still open.

Load `notion-helper` before any Notion read or write, `email-helper` before any Gmail search, and
`crm` before touching a CRM row. They hold the connector quirks and conventions this skill relies on.

## Scope

The window comes from the request:

| Request | Window |
|---|---|
| "yesterday's call follow-up" or no window given | Yesterday |
| "last week's", "the last week" | The past 7 days, up to yesterday |
| "this week's" | Monday of this week up to now |
| A date or range | That date or range |
| A named call ("the [Name] call") | That one page |

Dates are in Shaw's local time (Central). Filter Notion on explicit ISO dates, since its
relative date filters resolve in UTC.

Read call pages from both ABA Calls and ABA Trainings. Skip `❌` pages (the call never happened)
and anything under Demo (Synthetic Data). On each page, read the `## Follow-up` section. Skip
bullets that are already crossed off (`~~…~~`) and empty bullets. Use Call Notes only for
context, never as items to route.

## Mode

- **Preview**: read, classify, and report what you *would* write. Write nothing.
- **Write**: make the writes, verify them, cross off, and report what landed.

Use the mode the caller names. In an interactive run with no mode given, preview first and write
once Shaw approves. Shaw's corrections to the preview override this skill's routing for that run.

## 1. Classify each open bullet

Ask what the bullet *is*, then route it:

| Bullet is… | Example | Route |
|---|---|---|
| Content for the follow-up email | "Send review link", "PS playbooks zip", "FU email" | **Leave for the email task.** Don't draft it. Cross it off once sent mail confirms the email went out |
| Something to raise or check at the next call | "[Person] to try skill sharing", "Ask [Person 2] about product training" | **Carry forward** to the next call page with that person or company |
| Shaw's own action, not an email | "Individual follow-ups with attendees next week" | **ABA task** |
| Scheduling that will come out of an ongoing conversation | "Connect with [Person] for scheduling follow-ups", "BAMFAM" | **Set the person's `Next Contact`** in the CRM instead of making a task. Their normal cadence takes it from there |
| Already done | Intro sent, hold on the calendar, the next page already has the bullet | **Cross off** once confirmed |
| An idea phrased as a question, or unclear | "Create one-pager case study?", "Nov 11 workshop" | **Ask Shaw** in the report's closer. Write nothing |

The owner decides the route, so read carefully: "[Person] to try X" is [Person]'s, while "Reach out
to [Person 2]" is Shaw's.

**Check whether it's done before routing.** Many bullets are already finished by the time this
runs. Look in sent mail (`get_thread`, never a search snippet), the calendar, the destination
page, and the CRM row's Notes. Routing finished work just gives Shaw noise to clear.

**Don't connect pages by coincidence.** If a bullet is unclear, ask about it. Never fill in its
meaning from another page that happens to share a date or keyword. (10/14/26: [Person]'s "Nov 11
workshop" got linked to an unrelated [Company] workshop on 11/11 that wasn't even happening.)

## 2. Write (write mode only)

**Carry forward.** Find the next ABA Calls or ABA Trainings page after now with the same person,
Friend, or Company. A call later today counts. Add the bullet under that page's `## Call Notes`,
which is where Shaw keeps things to raise. First check whether an equivalent bullet is already
there, since Shaw often adds them himself in different words. Write in his voice, a name then a
short prompt:
- `[Person]: rerun normalize-pto (backfill + transitions)?`
- `Product team training? ([Person 2], else [Person 3])`

If there's no next page yet, write nothing and leave the bullet open. Report it as waiting, so
a later run over a wider window can pick it up once the page exists.

**ABA task.** Follow `notion-helper` → Core Workflow. Use a short, action-first title. Date it
from the bullet ("next week" means next Monday); otherwise use the next working day. The body is
a single `<mention-page>` link back to the source call page.

**Next Contact.** Change only that field on the person's CRM row. Follow `crm`'s
one-person-one-touch rule: if a sibling row (Friends, Reviews/Referrals) already has a live
date, ask Shaw instead of writing.

**Cross off.** Wrap the bullet's exact text in `~~ ~~` with `update_content`, one call per page.
Cross off an item only after its route has landed and been verified, or after it's confirmed
done. An item that's merely assumed done stays open. Cross off child bullets individually.

When a bullet was an ask and the answer has come back (directions requested, a date confirmed,
a figure sent), log the answer under that bullet on the call page before crossing it off,
rather than on the event, CRM, or engagement page it relates to. The Follow-up section is where
Shaw and later runs look when acting on the item next, so an answer filed anywhere else reads
as still missing.

**Verify.** A batched `update_content` can partly fail while still reporting success. Re-fetch
every edited page and confirm each change before reporting it.

## 3. Report

Format with `skimmable-summary`. Title: `Call Follow-up — <window>`. Stat line:
`{N} pages · {c} carried · {t} tasks · {d} crossed off · {q} for you`.

Sections, in order:
- ↪️ Carried forward: `Add '<bullet>' to [<destination>](url)`, then the source page. In preview
  this is phrased as a proposal. Prefix waiting items with ⏳. Empty: "Nothing to carry forward."
- 📌 New tasks: [task](url) with its date and source. Empty: "No new tasks."
- 📇 Next Contact: [person](url), old date → new date. Empty: "No date changes."
- ✉️ Left for the email task: page and a short gist of its email items not yet confirmed sent.
  Empty: "Nothing pending for email."
- ✅ Crossed off: page, what was confirmed, and how. Empty: "Nothing crossed off."
- 🔴 Needs Your Attention [closer]: unclear bullets and ideas phrased as questions, one
  decision-ready question each.

In write mode, end with a `✓ Verification` line: how many pages were re-fetched and how many
writes were confirmed.
