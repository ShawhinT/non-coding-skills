# Transcript-based posts (mine-file mode)

The workflow for turning a **pre-mined Q&A file** into a single LinkedIn post. This is the transcript-based path: the input isn't an existing SFC page, it's a dated `YYYY-MM-DD-qa_pairs.txt` from the **SFC Content Mining** project — verbatim asker-question / Shaw-answer pairs pulled from recent call transcripts, grouped by theme and ordered as LinkedIn raw material. The ore is already dug; there's no live client research or analytics to run.

**Trigger:** Shaw points at the file ("new post", "pick a painful idea from the qa_pairs file and draft it"). Work straight from the file — this mode is self-contained and shouldn't send you bouncing to other procedures.

## The steps

- **Read the file efficiently.** The Q&A file is grouped by theme under `#### THEME` headers. Grep those headers first to see the map, then read only the **2–3 themes you'll actually mine** rather than dumping the whole transcript file into context.
- **Cross-reference the backlog first — and make the audit conclusive before investing in hooks or a draft.** An idea that fails the audit shouldn't get a hook, let alone a draft, so settle this up front. Query the SFC table view and check two windows (canonical rules in `references/sfc-database.md`):
  - **Topic overlap.** Read status from the Date — a past-dated row is posted, a future-dated row on the upcoming-Sunday backlog is parked. Is this idea already parked, or posted in the **last ~4 weeks**? If it's parked, rebrief *that* page instead of drafting a fresh one. A matching topic posted **more than ~4 weeks ago is fair game** to rerun — recycle it.
  - **Hook freshness (~past week).** Look at the hooks on the last several posts and don't repeat an opener shape or mechanism (concede-then-pivot, anon story-lead, number+stakes, listicle) you've used in that window — consecutive posts should each feel fresh.
- **Pick for pain, not coverage.** Only after the audit clears the idea: scan for the one that's contrarian, widely felt, and ties back to a thesis in the strategy (adoption != transformation, agencies are back, the intern frame). One sharp pain beats a balanced survey.
- **Anchor the draft on the verbatim quote.** The file's answers are Shaw's actual words. Build the post around the real line ("engineers are not typing as much but the SDLC...is the same"); don't paraphrase it away, the quote is the proof. Hand the draft itself to `linkedin-voice` (it writes the full text in Shaw's voice) and match the machinery to the format: a take gets no list or footer, a teaching post gets the listicle.
- **Close the loop after Shaw edits.** When he revises the draft, diff his version against yours and infer the voice principles behind each change. Present them as a short list, let him pick which ones stick, then feed only those into the voice skill via `skill-updater`. This is how the voice compounds: every edited post makes the next draft start closer.
