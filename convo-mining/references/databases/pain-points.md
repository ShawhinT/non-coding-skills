# 💢 Pain Points

Pain points, doubts, and negative emotions expressed by customers and prospects. One row per
utterance, verbatim in the body.

**Database:** `https://app.notion.com/p/[database-id]`
**Data source:** `collection://[page-id]`

## Schema

Shared-spine properties behave exactly as SKILL.md describes, including `Person` under that name.
Three properties are specific to this database:

| Property | Type | Note |
|---|---|---|
| Pain Point | Title | The spine's title property. Three words max |
| Type | Select | `Pain` / `Doubt` / `Frustration` |
| Avatar | Select | `Founder/CEO` (no boss on the org chart) / `Leader` (has reports, or heads a function) / `IC`. One value only — see the ladder below |

**Type:**

- `Pain` — something costing them now
- `Doubt` — unsure it will work
- `Frustration` — venting with no clear ask

**Objections don't live here.** Since 10/11/26 a stated reason not to buy — or a doubt that ABA's
engagement will work — goes to ABA Q&A with `Kind: Objection`; `aba-qa.md` carries the rule. A
`Doubt` here is about AI or the speaker's own team. A peer, partner, or friend on a free session
voicing a view of Shaw's offer is neither — nothing was being decided — so the same words are a
`Pain` about their own work or nothing at all.

The distinction that matters most in practice is `Pain` vs `Frustration`: a concrete cost that's
blocking something is `Pain` even when it's expressed emotionally. `Frustration` is for an utterance
with no actionable shape — real feeling, nothing to fix.

The word that defeats this test is "hate." "One of the things that I hate he keeps doing and I have
to tell him all the time" is `Pain` — the feeling is loud, but it recurs and there is something to
fix. "I need to get better at that," about his own time management, is `Frustration` — equally felt,
no mechanism to act on. Before leaving a row typed `Frustration`, check that nothing in it could be
fixed.

**Avatar** tracks whoever is named in `Person`, not whoever is paying — a founder relaying his
data-entry clerk's morning produces an `IC` row. That's what lets the same pain read differently by
segment; the reason a founder hesitates isn't the reason an IC does.

**One value, and the most senior one wins.** The ladder is `Founder/CEO` > `Leader` > `IC`.

- `Founder/CEO` — nobody above them on the org chart: founders and co-founders, owners, CEOs, a
  president who runs the company. A co-founder counts even when another co-founder holds the CEO
  title.
- `Leader` — two tests, in order. **Primary:** has direct reports — an exec, a senior manager, or a
  people manager; a C-suite title below the CEO (CFO, COO, CAIO) lands here. **Fallback:** no formal
  reports, but heads a function and directs other people's work in it — a director of finance, or a
  head of recruiting who brings in contractors. At fifty to two hundred people a department is
  frequently one person, and that person is still a `Leader`.
- `IC` — executes inside a function someone else owns.

(Until 10/17/26 there was a fourth value, `Exec`; it was folded into `Founder/CEO` for CEOs and
`Leader` for everyone else, and no row carries it any more.)

**Leave it blank when the record doesn't say.** A title is evidence; a role in the session is not.
"Office manager" means reports in some firms and none in others, and someone described only as a
workshop participant has told you nothing about their org scope. Blank reads as the open question it
is and stays filterable, where a guessed `IC` is invisible and propagates. Surface the name to Shaw
instead — he usually settles it in one word.

**The rung comes from the person's job, not a side venture.** Someone employed as an IC who also
runs a side project or solo business is an `IC`, even when every row is about the side project —
the segment these tables cut is who the buyer-side reader is at work, and a founder title on a
personal venture would file them alongside people who run companies.

**Read what the tables already say about this person before writing.** All three databases share
this scheme, so a name usually has history: query it and you get the Avatar already in use, and
often more than that. Three things follow. A value that's already consistent settles the field
without asking. A value that *disagrees* with itself across tables is a real inconsistency — raise
it once and fix every row, rather than silently inheriting the majority, which is how a wrong value
survives thirty rows. And prior rows are a fact-check on the extraction itself: a win reported as
someone's first is contradicted by their earlier rows, and on a garbled transcript that contradiction
is often the only way to catch a mis-attribution.

That query replaces a flag, and this is where per-row uncertainty gets resolved rather than
forwarded. Where it genuinely can't settle a field, batch what's left into one question covering
every affected row — not a flag per row, which turns a review into a quiz.

## Body template

```markdown
## Pain Point

> <verbatim utterance, blockquoted, unsmoothed>

*<one italic line of provenance: where it was said, who relayed it, what surrounded it>*

## Response

<Shaw's reply, verbatim, formatting preserved — omit this heading entirely when he gave none>
```

**The response section is optional, on every type.** Include it whenever Shaw answered; leave it off
when he didn't. The pain is what the row exists for and it stands alone — one nobody responded to is
a complete row, not a broken one. But where he did answer, that reply is the rebuttal, and on a
`Doubt` it's the half you actually reach for when writing a sales page or prepping a call.
Capturing only the doubt would throw it away.

## What clears the bar

Two gates, in order. The first asks about the speaker, the second about the utterance.

**Is the speaker doing real work?** A role inside an organization — at any level — or a business
with real customers. Level and headcount are both irrelevant: an intern at a fifty-person firm
passes, and so does a company of one with customers and revenue. What fails is someone still trying
to *reach* the work — a student, or someone early enough in building a practice that there's no
organization and no customer base behind them. Their costs are real; they just aren't the costs this
database collects.

**Does the pain survive transplant?** These rows are raw material for selling to companies of fifty
to two hundred people, so the test is whether someone at that size would recognize the pain as their
own. Email volume, adoption stalling, tool cost, permission anxiety, unreachable executives, bad
legacy data — all transfer. Landing your first clients, having no income yet, positioning your own
practice — none do. One speaker routinely produces both, which is why this is a gate on the
utterance and not on the person: "I have a terrible case of the squirrels" is any overloaded
operator, and "everything is kind of backloaded since it's a monthly fee" is nobody but a company of
one.

Past both gates, an utterance earns a row if it names something the speaker experiences as a cost, a
risk, a blocker, or a reason to hesitate — about their work, about AI and tooling, or about ABA
itself. Phrasing doesn't have to be negative; understatement counts, and so does a hedge.

**Relayed pain counts, and the speaker is the person who felt it.** A champion quoting a colleague
("she said training on her own has been a challenge") produces a row whose `Person` is the
colleague, with the relay named in the provenance line. That's the same rule the spine applies to
forwarded Slack messages, and it matters here because a lot of the best material arrives
second-hand from an internal advocate.

**The pain has to be one they carry.** Applying the spine's durability rule here: two shapes name
something real and neither survives the session that produced it.

- **Friction the session created.** A connector that isn't logged in, a hallucinated name in the
  sheet being built live, a usage limit hit because two heavy tasks were running. The test is
  whether it would have happened with Shaw not on the call. What a session *reveals* still counts —
  someone stalling on "this is actually quite hard" when asked to state criteria he has never had to
  articulate has a standing problem the exercise exposed. What a session *generates* is a support
  ticket.
- **What they want, not what it costs.** "It's not like I want to automate the whole thing, but
  ideally I'd look at 50% less profiles" specifies a solution. Design input is high signal for the
  build and belongs in the session notes; it names no cost. The same utterance shape is a perfectly
  good Q&A row, which is why this test is local to this database.

The corollary: product friction counts when they brought it with them. "I tried to do this in
January and it was so painful that I just gave up" and "the struggle to edit Google Docs" are
standing experiences that predate the session.

**Doesn't clear it:** generic industry complaint with no personal stake, Shaw's own framing of a
client's problem, a logistics gripe about scheduling, and anything that is really an open loop or a
to-do rather than a pain.

## What this database is for

- **Copy raw material.** Buyer-side language for landing pages, sales letters, and hooks. A line
  the customer actually said outperforms anything written for them, which is why the body stays
  unsmoothed.
- **Offer design.** Repeated pains across clients are the strongest signal for what to build,
  package, or price next.
- **Doubt handling.** `Doubt` rows are pre-call prep and sales-page FAQ, grounded in what people
  actually hesitate over rather than what seems likely. Objections to the offer itself are in ABA Q&A.
- **Delivery signal.** A pain from an active client is a retainer problem showing up early. Surface
  those rather than just filing them.
