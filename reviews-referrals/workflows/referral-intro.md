# Referral Track — Intro, Convert, Close

Statuses touched: Referral Status `Asked` → `Intro Made` → `Converted` / `Declined`,
plus parking as dormant.

## 1. Intro lands → CRM handoff

**Trigger:** a 3-way intro email arrives (watch for `<Name> <> Shaw` subjects), or Shaw says
"X intro'd me to Y".

1. Hand the new person to **CRM Workflow 3** (add a new lead): Active Leads row, Source =
   `Referral`, linked to their company. An intro to a colleague at the referrer's own company
   is still a lead row, under the company that already exists. Reply on the intro thread per the SOP (via `email-helper`).
2. On this row: Referral Status → `Intro Made`; upgrade the person's ledger line to a
   `<mention-page>` link to their new Active Leads page (`intro'd M/D`).
3. From here the *lead's* journey is the CRM's job — this row tracks only the referrer
   relationship. Don't duplicate the lead's pipeline activity here.
4. Send the referrer a one-line update at each later status flip (Intro Made, Converted,
   and especially a declined lead) so they hear back win or lose — per the SOP.

## 2. Convert

**Trigger:** a referred lead closes.

1. Referral Status → `Converted`; tag the ledger line (`converted M/D`).
2. Surface a thank-the-referrer prompt — this is also a high-goodwill moment for the *next*
   ask. Hand the note to `email-helper`.

## 3. Decline / park

- **Declined** is an active no only: Referral Status → `Declined`, clear Next Contact,
  Notes line with the reason. A ghosted ask parks as dormant on silence instead (per the
  SOP) — Notes it, clear Next Contact, revive on a reply or new goodwill moment.
- **Hand the touch back** on any terminal or parked outcome where the review track is also
  settled: the row stops owning the person's next outbound, so the CRM record takes it —
  set its Next Contact per its nurture cadence, strip the `Next touch owned by
  Reviews/Referrals` pointer from its Notes. Parking is exactly the case where a person
  otherwise ends up scheduled nowhere.
