# Polish Framework

How to turn a raw form response into a pull-quote.

The job is to keep the client's voice and core meaning while sharpening for impact:
lead with the quantified win, cut filler, no em dashes (Shaw's voice rule). The
polished version should always be identifiable as the client's own thought — just
tightened. If a polished quote sounds like a brand wrote it, it's overcooked; pull
back toward the verbatim.

## Presenting a quote inline in an email

The polished or pre-drafted quote often goes straight into an email: the FU2
pre-drafted ask and the approval ask both drop the quote inline. There it renders
as *italicized* quote text with the attribution on its own line directly beneath
it, no blank line between them. Don't wrap it in an HTML blockquote. Gmail renders
`<blockquote>` inconsistently (stray indent bar, broken spacing) and Shaw flags it
on sight; the Gmail connector can't produce the clean gray-bar look, so if he
wants it he adds it by hand after the draft.

The `>` blockquote styling in the worked examples below is documentation
formatting for this file only, not the shape the quote takes in an email. See the
email-helper skill for the htmlBody mechanics.

## The 3-variant default

When polishing a fresh form submission, produce three variants. Each pulls a
different angle out of the same source material and serves a different surface.

### Variant 1 — Punchy / outcome-first

**For:** landing page card, sales letter hero, above-the-fold pull-quote.
**Format:** Before → After → Impact arc, 1–3 sentences. Pull each beat from a
specific form column: Before from "Before our session", After from the "Impact"
field, and the closing Impact line from the "Worth It" column (NOT the Impact
field). The Worth-It column carries the peer-rec language that lands hardest as
the close; the Impact field's outcome description is the middle "After" beat.

**Example ([Client Name]):**

> "I came in with a manual hiring workflow that was eating my week: copying contracts, cross-checking NDAs, swapping out parameters. Shaw and I built a Claude skill on the call itself that gave me ~3 hours back every week. The bigger win: I left with a clear framework for deciding what to automate as a skill, what to vibe-code as software, and what to keep doing by hand."

### Variant 2 — Short pull-quote

**For:** social posts, hero one-liners, deck slides, email signatures.
**Format:** 1–2 sentences. Boil it down to the single sharpest line.

**Example ([Client Name]):**

> "Shaw and I built a Claude skill on the call that automated my hiring workflow. ~3 hours back every week, and a sharper way of thinking about what to automate next."

### Variant 3 — Thinking-partner angle

**For:** long-form sales pages, case studies, proposals. Surfaces both the
deliverable (the skill / outcome) AND the meta-value (the framework / mental model).
**Format:** 2–4 sentences. Lead with deliverable, end with framework.

**Example ([Client Name]):**

> "Two things I walked away with: a Claude skill we built live on the call that automated the manual parts of my hiring process (~3 hours a week back), and Shaw's framework for deciding when a task should become a Claude skill, when it should become a vibe-coded product, and when it should stay manual."

## What each form field gives you

The 4-question spine — same in both the 1:1 Workshop form and the ABA Training
form, just phrased per-individual vs. per-team:

| Form column | What it yields in the polished version |
|---|---|
| **Before** (pain / context) | The opening hook. Sets the "before" state, makes the reader feel the problem. The more specific, the better — pull sub-steps from call notes if the form answer is thin (e.g., [Client Name]'s form said "manual hiring process" but the call notes had the actual sub-steps: copy contract, cross-check NDA, swap params, send via Google e-sig). |
| **Impact** (outcome) | The middle / pivot. Lead with the quantified win when present — hours saved per week, % improved, $ value, time-compression ratio. Numbers convert. |
| **Worth It?** (peer rec) | Often the strongest one-line testimonial material. Frequently becomes Variant 2 on its own — pull the cleanest sentence. |
| **Permission** | Dictates attribution. See "Permission levels" below. |

For the ABA Training form, the questions are framed at the team/business level
instead of the individual. Same polish framework, just keep the language
team/company-scoped ("the team", "across the business") rather than ("I", "my work").

## Voice rules

- **No em dashes.** Use colons, periods, or split sentences. Em dashes read as
  AI-written and aren't Shaw's natural punctuation. *(Em dashes inside verbatim
  raw responses are fine — only the polished output needs to lose them.)*
- **Lean toward maximum verbatim.** A polished quote should mostly be the client's
  own words, lightly stitched. Tighten for flow (drop a dangling "and", cut
  "actually" or "I have to say"), but don't paraphrase. If your output uses
  different words than the form response, you've gone too far, pull back toward
  the verbatim. Don't invent metaphors they wouldn't use, don't add corporate
  clichés ("game-changer", "next level", "needle-mover"), and don't add claims
  they didn't make.
- **Avoid self-promotional intensifiers.** Words like "just one", "only",
  "somehow" frame the work as faster or more impressive than the reader would
  infer on their own. The quantified win does the work; the framing should be
  peer-voiced, not pitch-voiced. *"In just one 90-minute session"* reads as a
  pitch; *"In our 90-minute session"* lands the same fact peer-to-peer.
- **Lead with the quantified win when present.** "~3 hours back every week" beats
  "saved me a lot of time". If there's a number, pull it forward. If you have a
  hedged phrasing ("under an hour") and the call notes have a tighter one
  ("in minutes"), use the tighter. The polish step is where to push for precision,
  not where to hedge.
- **Each number keeps its own claim shape.** A one-time win (built in 3 hours instead
  of a 4-5 day HubSpot project) and a recurring cost (the 4 days blocked every month
  for reporting) are different claims; merging them into one line overstates what the
  client said. Same with saved vs. on track to save: if the time isn't fully recovered
  yet, the quote says roadmap, not result. When two similar numbers show up in the
  source material, go back to the transcript to check what each one actually measures.
- **Vary the opener across concurrently published quotes.** Quotes land side by side
  on the homepage, so if every one starts "Working with Shaw..." the wall reads
  templated. Rotate the framing ("Working with Shaw", "After a 1:1 session", "In our
  session") and check the openers of the other live quotes before finalizing a new one.
- **Cut filler.** Phrases like "Honestly,", "I have to say,", "All in all,",
  "Truly,", "To be frank," — delete. Same with most "really" / "very" intensifiers.
- **One beat per idea.** If a closing sentence ("More importantly, X") already
  lands the impact, an earlier bridge sentence that previews the same ground is
  usually cuttable. Let the closer carry the impact; don't pre-state it.
- **Match attribution to permission level.** See below.
- **Pull from call notes ONLY when the form is genuinely thin.** If the form has
  substantive answers, lean on them verbatim. Adding texture from call notes the
  client didn't surface themselves reads as inserted, not as theirs. When the form
  is genuinely thin (one-liners with no texture), pull specific sub-steps from
  call notes: if the form says "manual hiring process," the call notes likely say
  what specifically (copying contracts, cross-checking NDAs, etc.), that
  specificity goes into Variant 1.

## Permission levels

Form field "Can I share your story publicly?" controls how the polished version
gets attributed:

| Permission level (form answer) | Attribution |
|---|---|
| No / Decline | Don't share. Flip the row Status to `Declined` and stop. |
| Yes, anonymous | `— [Role from client's self-ID] + generic industry descriptor` (e.g. `— People leader, mid-size [industry] SaaS`). See "Anonymous attribution research" below. |
| First name only | `— [First Name]` |
| Name only | `— [Client Name]` |
| Name + role | `— [Client Name], Founder & Principal` |
| Name + role + company | `— [Client Name], Founder & Principal, [Company]` |
| + photo / video | Same as above + visual asset. Flag to Shaw that he needs to source the photo/video. |

Default to **less-rather-than-more** if a permission level is ambiguous. Better to
under-share than over-share. When in doubt, check with Shaw or send a confirming
email before publishing.

### Anonymous attribution research

When permission is "Yes, anonymous" (or any free-text variant that grants
publish-permission but blocks name/company), build the descriptor in two parts:

1. **Role.** Pull from the client's own self-ID in the form, usually their "Worth
   It" answer ("If you're a People leader..." → "People leader").
2. **Industry descriptor.** Web-search the company for size + segment. Aim broad
   enough that the company isn't identifiable: "mid-size [industry] SaaS"
   works (hundreds of companies fit), "[narrow industry niche] platform"
   doesn't (~3 named players in that segment basically IDs them). Default shape:
   `[size]-[adjective] [industry] [SaaS / platform / firm]`.

Confirm the descriptor in the approval ask. Free-text permission answers
("Yes, but keep it anonymous") aren't standard form options, so the client may
have a different attribution shape in mind.

## The pre-drafted arc (FU2 path)

Pre-drafted quotes follow **Before -> After -> Lasting impact**, usually 3 sentences,
anchored on the single clearest win. Don't pack multiple wins into one quote; breadth
belongs only when breadth is itself the story (a client whose win is a stack of
net-new processes). The third beat looks forward: what's now repeatable, or where
this is heading.

When the wins are new capabilities rather than time saved, close on capability
expansion, not efficiency. "We now have processes that simply didn't exist before
and a roadmap to keep expanding" lands harder than another hours-saved line, and it
matches how clients describe the shift themselves ("we could have done it, but we
never did"). Marginal-gains framing undersells exactly the engagements worth quoting.

## Worked examples

### [Client Name] — form submission, 3 variants, Variant 1 approved verbatim

**Raw form response:**

- *Before:* "repetitive/manual parts of the hiring process."
- *Impact:* "It concretely sped a few things up!"
- *Worth It:* "This was time well spent! I got two concrete things out of this—(1) I got ~3 hours per week back, because of a Claude skill that Shaw and I built together quickly just on the call itself, and (2) I got from Shaw's AI-wisdom a good way of deciding—is this task automatable by a Claude skill, by a software product which I can vibe-code, or I should continue to do this manually."
- *Permission:* Name + role + company

**Polished (Variant 1, approved by [Client Name] via email thread 5/27):**

> "I came in with a manual hiring workflow that was eating my week: copying contracts, cross-checking NDAs, swapping out parameters. Shaw and I built a Claude skill on the call itself that gave me ~3 hours back every week. The bigger win: I left with a clear framework for deciding what to automate as a skill, what to vibe-code as software, and what to keep doing by hand."
> — [Client Name], Founder & Principal, [Company]

**Notes on the move:**

- Pulled specific hiring sub-steps (contracts, NDAs, swap params) from the call
  page (those weren't in the form response itself — texture from the engagement
  context).
- Used "~3 hours back" as the lead quantified win.
- "The bigger win:" replaces an em dash that would've split the sentence.
- Closed with [Client Name]'s framework — the secondary win he described.

### [Client Name] — verbatim was strong, light tightening, form consent

**Raw Worth It answer (full):**

> "If you're already using AI but feel like it's not fully leveraged or is scattered across tools, this is absolutely worth it. Shaw doesn't just show tools—he helps you build systems. It's especially valuable for founders who want to move from experimenting with AI to actually operationalizing it across their work."

**Polished (compressed for impact, approved on form consent — no separate approval
email):**

> "In one session, we automated a task that was taking me 20 hours. Shaw doesn't just show tools, he helps you build systems I can extend across the business."
> — [Client Name], Founder, [Company]

**Notes on the move:**

- Verbatim was clear but long for a pull-quote (74 words → 28 words).
- Pulled the "20 hours" quantified win from the Impact answer (not in the Worth It).
- Kept [Client Name]'s strongest phrase — "doesn't just show tools, he helps you build
  systems" — almost verbatim, just removed the em dash.
- Status went Form Submitted → Approved without a separate approval email because
  [Client Name]'s form Permission answer was "Yes — name, role, and company" — explicit
  consent covered the publish. Notes captured this for the record.

### [Client Name] — no form submitted, pre-drafted from call notes (FU2 path)

[Client Name] never filled out the form. Shaw pre-drafted the testimonial from the
engagement page Results section, anchored on call notes from 4/15 (3-week financial
project → 1 hour, email time cut in half). Sent as the initial ask via the FU2
pre-drafted template (per the SOP). [Client Name] reviewed and approved.

**Polished (sent inline in the ask email):**

> "Before working with Shaw, I was spending my nights and weekends trying to self-learn AI. I was using Claude, but I didn't feel like I was maximizing it for my work. One session with him and a week of applied work later, I've turned a 3-week financial project into a 1-hour job, cut my email time in half, and built skills across our business that I didn't have time to even think about before."
> — [Client Name], Co-founder & CEO, [Company]

**Notes on the move:**

- No raw form to anchor on — built entirely from call notes.
- Before/After structure with 1–2 quantified wins is the formula for the pre-drafted
  path ([Client Name]'s worked because it named the "3-week project → 1 hour" win + "cut
  email time in half").
- Status went Asked → Approved directly, skipping Form Submitted, since no form
  submission existed. Notes captured "pre-drafted path."

This is the canonical example of the FU2 pre-drafted variant working as the
initial-ask path for a busy exec.

## When to lean on conversion-copy

The default 3-variant pass is enough for most quotes. Invoke `conversion-copy`
when:

- The quote is going on a landing page hero or sales letter open (high-leverage
  surface — every word counts).
- You need to compress significantly — verbatim is 100+ words and you need a
  ~30-word version that still hits.
- You want A/B variants for testing different angles or different audiences.
- The Worth It language is weak and needs a rewrite that goes further than light
  tightening (still within voice and meaning, but more shaped).

For most testimonials, this skill's 3-variant default is the right altitude.
