# Review Track — Approval, Publish, Decline

Statuses touched: `Form Submitted` → `Approved` → `Published`, and `Declined`. What counts
as approval (form permission, "yes go ahead", client's own version, trivial-edit
short-circuit) is SOP policy — don't re-derive it here.

## 1. Apply approval

**Trigger:** an unambiguous "yes, go ahead", the client returning their own clean version, or
form permission counting as approval per the SOP.

1. `notion-update-page` (update_properties): Review Status → `Approved`. Notes line with the
   approval date. Clear Next Contact (no FU pending).
2. Reshape the body: replace `## Drafts` (all variants) with a clean `## Testimonial`
   section containing only the approved quote + attribution (`update_content`). Keep
   `## Form Response` intact below as historical record.
3. Client edits: apply them; re-confirm only if the change is substantive (trivial edits
   promote directly per the SOP). Anonymity requests: anonymize the attribution (keep
   seniority + broad sector, strip name/company/narrowing specialty), don't drop the quote.
4. **Don't schedule a referral on-ramp here.** The ask is made at the Results call, which
   its own dated ABA task carries — nothing about it is scheduled from this row. If the
   review track has no pending touch, hand the next touch back to the CRM record: set its
   Next Contact per its nurture cadence, strip the `Next touch owned by Reviews/Referrals`
   pointer.

Ambiguous replies (conditional yes, permission questions, substantive edits) do NOT
auto-advance — surface them as decisions.

## 2. Publish

**Trigger:** Shaw says the quote is live (website, sales letter, LinkedIn, deck, etc.).
Publishing itself is always Shaw's action.

1. Review Status → `Published`. Notes line with the date + surface(s).
2. `Published` is terminal for the review track. The referral ask rides the Results call and
   its own ABA task, so nothing schedules it here — hand the touch back to the CRM record:
   set its Next Contact per its nurture cadence, strip the `Next touch owned by
   Reviews/Referrals` pointer.
3. Post-publish is the highest-goodwill moment for the referral ask — if the Results call is
   far out, surface the option to make the ask sooner. Don't move it silently.

## 3. Decline (review track)

**Trigger:** an active decline, or no response after the final FU per the SOP cadence.

1. Review Status → `Declined`. Notes line with the reason (active vs. ghosted post-FU3).
2. Clear Next Contact.
3. **Hand the touch back or route it forward.** If the referral track is viable (Shaw may
   still want a referral ask despite a declined review — his call, surface it), the row can
   keep the touch with a future Next Contact. Otherwise the CRM record takes ownership back:
   set its Next Contact per its own cadence, strip the pointer from its Notes. A person
   scheduled nowhere reads as handled and isn't.
