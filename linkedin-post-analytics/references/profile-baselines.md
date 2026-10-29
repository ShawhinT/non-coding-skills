# Profile-level weekly series (viewers, followers, connection requests)

Post analytics answer "how did my posts do". Profile series answer "did something *off* LinkedIn send people to me" — e.g. a YouTube description CTA pointing at the profile. LinkedIn gives no source attribution for those visits, so the method is a pre-launch baseline plus lift during the test.

## Where each series comes from

Both analytics charts expose every data point as an `aria-label`, so a weekly series reads in one `javascript_tool` call — no hovering, no scrolling:

```js
[...document.querySelectorAll('[aria-label]')].map(e => e.getAttribute('aria-label')).filter(t => /\d{4}/.test(t))
```

- **Profile viewers** — `/analytics/profile-views/` (Premium), "Past 90 days". Labels read `Week from Sunday, Jul 19, 2026, 127. Viewers.` — already weekly. The last point is the in-progress week, and it can't be read as a partial count: on Sunday Oct 18 2026, the first day of its week, it already showed 100 viewers against a ~124 weekly median. Score only closed weeks.
- **New followers** — `/analytics/creator/audience/?timeRange=past_90_days`. Labels read `Tuesday, Jul 14, 2026, 19. New followers.` and the values are **cumulative** across the range, not per day. Difference them at week boundaries (Saturday to Saturday, to line up with the viewers' Sunday weeks); the first bucket is partial.
- **Connection requests** — no chart. Combine two Voyager calls (auth as in `linkedin-audience/scripts/recent-connections.js`):
  - new connections by `createdAt` — `relationships/dash/connections?q=search&sortType=RECENTLY_ADDED`
  - still-pending received invites by `sentTime` — `relationships/invitationViews?q=receivedInvitation`

  Their sum is the inbound proxy. An accepted outbound request becomes a connection indistinguishable from an inbound one, so pull pending sent invites (`relationships/sentInvitationViewsV2?invitationType=CONNECTION&q=invitationType`) to find outbound-campaign weeks, and exclude those weeks from the baseline. A campaign week can triple the count (93 vs a ~21 median), which is enough to fake any lift.

## Reading it

Use medians, not means: post virality drives spikes in all three series (one week ran 261 viewers against a ~124 median). Before calling an in-test spike a lift, check that week's post impressions. Size the expected effect up front. A source that adds ~40 visits a week is visible in viewers but sits inside the noise of requests and followers, and that difference decides which series the test is judged on. If the profile shows "Follow" rather than "Connect" to non-connections (creator mode), followers is the series a "connect" CTA actually moves.
