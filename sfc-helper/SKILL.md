---
name: "sfc-helper"
description: "Strategy-aware LinkedIn content ideation for Shaw's SFC pipeline. Works from a pre-mined Q&A file (the workhorse 'mine-file' mode), the Q&A database (repeat clusters), a single existing SFC page, or a proven post being repurposed to another channel: audits the idea against the backlog, turns it into hooks on request, and on approval stages it as an SFC database page. Use whenever Shaw wants LinkedIn post ideas, asks 'what should I post', wants to plan or fill his content calendar, wants hooks for a specific post idea, wants a painful post drafted from the qa_pairs file, or wants to turn strategy/analytics findings into scheduled posts. Trigger even when he doesn't say 'SFC' (e.g. 'brainstorm posts', 'plan my week of content'). Do NOT use for drafting the full text of one post (use linkedin-voice) or analyzing past performance (use linkedin-post-analytics); this is the ideation and scheduling layer between them. Also schedules LinkedIn or 🔴 YT Community posts and files post images out of Downloads."
---

# SFC Helper

Turn Shaw's strategy, pre-mined call material, and post analytics into staged LinkedIn content — ending in SFC database pages he can act on. This is the ideation layer: it decides *what* to post and *why*, maps it to the strategy, and stages it. It does not write the finished post copy and it does not pull analytics — it composes with two sibling skills for those.

## How this skill composes with others

- **`linkedin-post-analytics`** produces the numbers (the top/bottom split analysis, what's working). Pull its latest findings as an input; don't recompute them here.
- **`sfc-helper`** (this skill) takes the raw material (a pre-mined Q&A file, the Q&A database, an existing SFC page, or a proven post) → audits it against the backlog → (optionally) turns it into hooks → stages it as an SFC page.
- **`linkedin-voice`** drafts the full post text in Shaw's voice. That hand-off is the only thing this skill doesn't own — everything up to the copy is sfc-helper's. When Shaw wants a post written out, hand off to `linkedin-voice`.

Keeping these boundaries clean is the point: the SFC page holds Shaw's own unstructured notes on the idea, and the copy gets written later (often the morning of) so it's fresh.

## Four modes: mine-file, Q&A-database, single page, and repurpose

The skill runs in one of four modes depending on the raw material Shaw brings. **Mine-file mode** is the workhorse — a painful post straight from a pre-mined Q&A file — and has its own self-contained procedure in `references/transcript-posts.md` (audit first, pick for pain, anchor on the verbatim quote, close the edit loop). **Q&A-database mode** mines the 💬 Q&A database itself for repeat clusters (the same question asked across clients and surfaces) and drafts from the verbatim rows via a `linkedin-voice`-armed subagent — procedure in `references/qa-database-posts.md`. The other two are below.

### Single-page mode: developing one existing SFC page

Shaw often points at **one existing SFC page** and wants to develop just that post — "how many hooks for this idea?", "give me hooks for this", "draft this one":

- Fetch the page, work from the notes already on it, and stay scoped to that one idea.
- **A blank or thin page isn't a blocker — fill the context yourself before asking.** Search the workspace first: sibling posts on the topic, strategy notes, and recent call transcripts usually already hold the substance (Shaw's own phrasing, real numbers, the original angle — and often a recent sibling post the new one must differentiate from). Interview Shaw only when that search comes up empty: research costs him nothing, questions cost his attention.
- **The page title is the hook direction; the body is the payoff.** Anchor hooks to the title's framing and make sure they pay off into the options/points already noted on the page (this is `linkedin-voice`'s hook rule — read it). If the page has no hooks yet, answer the literal question plainly ("zero so far") before offering to add some.
- **When Shaw brings his own hook, sharpen it — don't replace it with a from-scratch menu.** If he proposes a direction ("a bold statement that AI-native businesses outperform"), your job is to refine and pressure-test *his* angle: offer 2–3 tight variations of it and name the one risk it carries (e.g. an analogy whose real-world timescale undercuts the urgency he's going for), so he can choose with eyes open. The generated menu is for when he asks "give me hooks," not when he already has one.
- **When Shaw asks for a hook menu, run `linkedin-voice`'s Hook process rather than improvising a shorter one.** That process owns the format (10 candidates, split 5 in Shaw's voice / 5 in named creators' voices, presented as two labeled sections) as well as the craft. Read it and generate against it — a menu of generic, concept-led restatements of the nugget is worse than none. These hooks are a **menu of directions**, not finished copy; when he picks one, hand it back to `linkedin-voice` for the full draft. `linkedin-voice` owns hook craft — read it, don't duplicate it here.
- **On approval, draft and write it in.** When he picks a hook and says draft it, hand off to `linkedin-voice`, then append the chosen hook + full draft to the page body *below* his existing notes (use `insert_content` at the end, don't replace) and keep the ⬜ icon. The draft goes below a `---` divider under his notes, as plain paragraphs — the same convention as repurpose pages. The divider is the boundary the schedulers read (everything below it ships), so angle notes and reminders stay above it and only post copy goes below.

### Repurpose mode: re-running a proven post on another channel

Sometimes the input is neither a mined Q&A file nor an existing page — it's **post analytics**. Shaw picks his best-performing posts (via `linkedin-post-analytics`) and wants them staged to run again on another channel, usually **YT Community**. This mode skips the ideation half entirely: the page carries only the *exact original copy*, because the post already proved itself and only needs re-placing.

- **The selection is analytics-driven**, so there's no ideation to do — just re-place proven copy. Still dedupe against the backlog (see `references/sfc-database.md`), and still propose the lineup and wait for approval before creating pages.
- **Screen the CTA before you rank, not after.** A post's close is part of what you're re-running, so a strong engagement rate can belong to copy that cannot ship — and none of what disqualifies it is visible in the metrics. A CTA for an event that has already happened can't run as written — but that's a flag, not a veto. The call is Shaw's, and staging it as a placeholder he'll reframe himself is a normal outcome, because the page is his draft surface. Screening sorts candidates into ships-as-is and needs-a-decision; it doesn't drop them. Name which end is dead and let him choose. An on-platform link (`lnkd.in`) has to become a direct URL once the post leaves LinkedIn. And an ask already scheduled on the *target* channel is a campaign-sequencing conflict, not a copy fix — two versions of the same ask days apart spends the audience twice. Read each candidate's ending first; ranking by rate and checking the close afterwards produces a shortlist you then throw away.
- **Set `Channel` to the target** (e.g. `YT Community`), not the default LinkedIn — here the channel switch is the whole point.
- **Icon: 🔴 for YT Community pages, not ⬜.** The icon encodes the channel at a glance — ⬜ marks queued LinkedIn posts (the ⬜ convention in `references/sfc-database.md` is LinkedIn-only), 🔴 marks YT Community pages.
- **Carry over the verbatim copy.** Pull each post's exact text from LinkedIn via the `linkedin-post-analytics` feed API (the `commentary.text.text` field) and put it on the page as plain paragraphs, exactly as it ran. Notes can't recreate a post that won on its specific wording.
- **Verify reconstructed copy against the source.** When `javascript_tool` truncates a long post and you rebuild the text from overlapping slices, diff your reconstruction against the original *in the page* before writing it to Notion — compare for equality and report the first differing index, rather than eyeballing the seams. Silently corrupted copy is the one failure this mode can't absorb: it reads as fine on inspection, and the entire premise is that the exact wording is what won.
- **Flag the media.** Copy alone isn't the whole post — check each source post's `content` for an `imageComponent` (or video/document) and pin a prominent note on the pages that have one (`> 📷 Includes an image — pull it from the original before publishing`). Text-only posts get no note; skipping this silently strips the post's visual. A poll is the same problem in another shape: its question and options aren't in `commentary.text.text` but in `content.pollComponent` (`question.text`, `pollOptions[].option.text`), and a poll re-run without them is just a lead-in. Stage them the way the target channel will take them, so the page is paste-ready: a YT Community text poll has no question field, so the question goes inside the copy block as its last line, and a **Poll** block beneath holds the options only, one per line.
- **Edits are substitutions, never rewrites.** Verbatim copy can carry things that break on re-run: dated event details, `lnkd.in` shortlinks that should be direct URLs off-LinkedIn, a "my channel" plug that's redundant on the channel itself. Swapping or deleting those is mechanical — the sentences around them don't change. Anything that would require *writing* a new sentence is not an edit: pin a note above the copy and let Shaw decide. That includes framing aimed at the wrong audience (e.g. buyer language on a channel where most people were handed a seat) — the most tempting rewrite, and the one that spends the post's proof. Adapted copy reads like it was generated, which is the exact thing re-running a winner is meant to avoid.
- **Dates follow whatever cadence Shaw names** (e.g. MWF starting today).
- **When Shaw says to actually schedule a staged YT Community page** — put it in the
  YouTube composer and schedule it for its date — follow
  `references/yt-community-scheduling.md`. It's the execution procedure (text prep, media
  handling, and the browser mechanics that are non-obvious), learned from real runs.

## Scheduling a staged LinkedIn page

When Shaw says to actually put a ⬜ LinkedIn page into the composer or schedule it, follow
`references/linkedin-scheduling.md` — the LinkedIn counterpart of the YT Community
procedure above: getting the copy in with its spacing intact, handling the page's media,
the schedule dialog, and closing the loop on the row.

## Strategy is the backbone

Every idea has to serve Shaw's actual go-to-market. Read `references/strategy.md` for the distilled version (avatar, the barbell model, the comment habit).

**Whenever the task involves laying out or rescheduling a week — not just picking ideas — also read `references/scheduling-principles.md`.** It governs volume, reach/engagement alternation, tee-up spacing, merge/split, format, and CTA handling, and it supersedes any cadence advice found elsewhere.

Also read the live source of truth before proposing — it evolves:

- **LinkedIn Strategy** page (Notion): `[page-id]`
- **Current quarter avatar** (Q2 2026 strategy): `[page-id]`

If those pages have shifted since `references/strategy.md` was written, trust the pages and flag the drift.

The backlog cross-reference — read a row's status from its Date, dedupe against the upcoming-Sunday backlog plus the last ~4 weeks, and check hook freshness before committing — is canonical in `references/sfc-database.md` and inlined into the mine-file procedure in `references/transcript-posts.md`. Run it in every mode before creating or rescheduling a page.

## Post assets on disk (Claude Code on Shaw's Mac only)

A LinkedIn post's graphic is built by `graphic-builder`; this skill owns where the finished file lives — and the same home holds every other asset a post carries: event photos, email screenshots, flyers. When running locally in Claude Code on Shaw's machine, the permanent home is:

```
~/Documents/_stv/_content/_SFC/sfc/<year>/<category>/<slug>/
  <slug>.html
  <slug>.png
  assets/          ← only when the HTML references external logo files
```

`<category>` is one of the existing topical folders under the year: `aba`, `ai-coding`, `ai-education`, `ai-takes`, `content-creation`, `entrepreneurship`, `events-and-workshops`, `misc`. Pick the one that matches the post's subject (a Builder Log about building an MCP server went under `ai-coding`); ask only if none fits. `<slug>` is a kebab-case name for the post's idea, matching the SFC page title where practical.

Exploration and unused variants never go here — `graphic-builder` keeps those in a scratch folder under `~/Downloads/` and deletes them once the winner is filed. This path exists only on Shaw's Mac: in a Desktop, Cowork, or web session, hand the rendered file back to Shaw instead of trying to write it there.

**Cleaning post assets out of `~/Downloads` means filing them, not trashing them** — even once the post is scheduled or live, the folder tree is the archive of what ran. A photo or screenshot carries no hint of its post, so identify each one first: view it, then match it to an SFC page by date and content (a page's `[Email screenshot]` placeholder, an event name visible in a photo). Propose the file → post → folder mapping, and name a guess as a guess. Photos keep their camera filenames inside a slug folder named for the post. Move with the shell rather than the Trash — restoring from the Trash is blocked from the sandbox, so a mistaken trash can't be undone from here. macOS screenshot names contain a narrow no-break space before AM/PM, so address them with a glob.

## Principles

- **Anonymize client material.** Never name a client or individual in a post idea. "a cybersecurity CEO," "a VC firm's CFO," "a policy director" — never the real name or company.
- **Verify numbers before they go in a post.** The big lesson from past sessions: a quantified claim has to be a real, attributable before/after, and you must distinguish a *manual baseline → AI* result from *first-AI-run → refined-skill*. If the manual baseline wasn't captured, say so and frame the number honestly (e.g., "~1 hour, her estimate"), or flag it to confirm. Don't inflate or conflate.
- **The page is Shaw's, and it holds two things.** An SFC page body carries his own unstructured notes on the idea — raw, keyword-level, written to jog his own memory — and, below a `---` divider, the final post copy. Nothing else. He writes either half himself as often as you do, so read what's on a page as authored rather than as an empty slot: a body that looks thin or trails off mid-sentence is his draft in progress. Add to it by appending; never restate his notes in your own words, and never overwrite a body you didn't write. The one thing this skill hands off is the post copy itself, which is `linkedin-voice`'s job.

  "Nothing else" is the part that gets violated. Two things reliably feel like value and aren't. **Your open questions** — a checklist of unresolved items converts your uncertainty into Shaw's task, and most of what lands on such a list is either something you could have decided yourself or something you could have asked him in one line. If a decision genuinely needs him, ask it in the message, not in the margin of his page. **The directions you rejected** — a record of hooks and angles that lost is conversation residue; the decision is already made, and preserving it lengthens the page without making the post easier to write. Both feel like diligence in the moment and read as clutter a week later, which is the only moment that counts.
- **Build on Shaw's angle, don't override it.** When Shaw arrives with his own hook or framing, refine and stress-test it rather than substituting your own idea-led menu. Pressure-testing means naming the one real weakness (a shaky analogy, an over-claimed number, a buried payoff) and offering tighter variants of *his* direction — he keeps authorship, you sharpen the edge.
- **Carry a take on a story.** A thesis stated on its own reads as opinion in a vacuum; the same point told through something that actually happened to a client reads as concrete and earned. When an idea is a belief, look for the real story that proves it — the 🏆 Wins database (`collection://[database-id]`) is the first place to look, since each row is a before→after in the person's own words. Going the other way, when mining a win, ask what bigger idea it's evidence for. The story is the vehicle; the moral is the post.
- **Lead with ore, not packaging.** Surface what people actually said and realized — quoted pains, aha moments, vivid specifics, honest numbers — not finished post packages with audience labels. Shaw tells the story; your job is to hand him the genuinely valuable raw material.
- **One post, one role.** Each idea targets the sponsor or the champion, not both. Posts that try to serve everyone serve no one (that's the dead "abstract analogy" middle).
- **Propose first, create on approval.** Present the idea or lineup and wait for Shaw's go-ahead before creating or rescheduling any SFC page. This is a propose-first skill.
