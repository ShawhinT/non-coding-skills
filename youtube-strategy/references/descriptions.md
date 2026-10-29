# Descriptions

The YouTube description is a growth + conversion surface, not metadata. Treat it the way you treat a title: the top earns the click-through to the *next* action, and every line respects the avatar's time.

**Shaw's published descriptions are the voice source** — `description-examples.md` holds recent ones. Read them before drafting; when they disagree with anything below, they win. For a fresh pull, `curl` the watch page and parse `shortDescription` from the embedded JSON.

## Structure (top-down)

Draft in this order. Each block is short; the chapters carry the detail.

1. **Business CTA — first line, above the fold.** The single most valuable line of the description is the one visible before "...more". Spend it on the channel's conversion goal (Shaw's 1:1 / team AI workshops for $10M+ companies), not on a synopsis. Current wording: `🤝 Your team not maximizing AI? I run 1:1 and team Claude workshops for companies doing $10M+ per year: https://aibuilder.academy/yt/<video-id>` — the `/yt/<video-id>` path attributes leads to the video, so leave `<video-id>` as an obvious marker until the upload exists.
2. **Two-sentence summary, derived from the title and the hook — not from the body.** Sentence one is the viewer's problem in the words the video itself uses (the intro usually says it outright; take it from the transcript). Sentence two restates the title's promise as an outcome — *"Here, I walk through how you can get Claude to do this for you (reliably)"* — at the same altitude as the title. The how belongs to the chapters.
3. **Primary resource link** — only when the video is *about* a repo, doc, or download (`My Skills Repo: <url>`).
4. **References** — only for sources the video actually cites, as a plain numbered list (`References` / `[1] <url>`). Don't add background links the video never mentions.
5. **Chapters** — timestamps with concrete names (see below).

**Deliver it as a file.** Write the final description to `~/Downloads/<video-slug>_description.txt` and give Shaw the path, along with showing it in chat. Copying from the terminal breaks the line breaks and spacing, so the file is what he actually pastes into YouTube. When he asks for revisions, update that same file.

## Principles

These came from comparing a generated draft to Shaw's final edit. Each is a *why*, not a rule.

- **Business goal before recap.** The fold is conversion real estate. A viewer who already clicked the video doesn't need a synopsis at the top — they need the next step toward becoming a customer. The summary can wait one line.
- **Compress; don't duplicate the chapters.** If a chapter is named "Demo: create-handout-doc skill", the summary doesn't also need "(turning a slide deck into a handout doc)". Redundancy reads as padding.
- **Plain and direct, one emoji.** The 🤝 on the CTA line (plus a second CTA line if there's a lead magnet) is the only emoji. The summary is plain, confident prose — no jokes, asides, or exclamation points. A draft with "plenty of them in 🙌" and emoji section headers was rejected as off-tone; the published examples read like a sharp abstract, not a social post.
- **Real URLs, never invented titles or `[link]` placeholders.** A bare clickable URL is worth more than a polished label that's actually a guess. If you don't have the real link, ask for it or leave an obvious `<paste link>` marker — don't dress a placeholder up as finished copy.
- **Link the durable resource, not the marketing page.** Prefer the docs overview (`platform.claude.com/docs`) over an announcement/news page (`anthropic.com/news`). Docs stay useful; announcements age.
- **Concrete artifact names in chapter titles.** "Demo: create-handout-doc skill" beats "Demo: Building a Skill Live" — more searchable, more honest, sets a clearer expectation. Name the specific thing built, not the generic activity.

## Chapters

- **Chapters are the video's outline, not a topic index of the transcript** — the places a viewer would jump to rewatch or replicate. On a tutorial that's a parent chapter followed by numbered steps (`Demo: …` → `Step 1: …`); side tips and asides fold into the step they occur in, and a short sign-off doesn't get a chapter. Get the outline first, then find timestamps for it.
- Shaw's chapter line format is `label - X:XX` (e.g. `Intro - 0:00`): label first, then a spaced hyphen, then the timestamp. Labels stay short and slide-like (`The Promise`, `The Domino`), not sentence-length descriptions.
- First chapter must be `0:00` (YouTube requires it to enable chapter UI).
- Minimum ~10s apart; at least three chapters.
- Name the concrete thing covered, not the abstract activity.
- Group multi-part sections by naming, not nesting (YouTube chapters are flat): `Step 1: ...`, `Step 2: ...` reads as a sub-sequence without needing indentation.
- **Derive timestamps from the video itself, never from memory of the edit.** Transcribe the final render (the video-editor skill's `transcribe.py`; output is `{"words": [{"word", "start", "end"}]}` in seconds) and locate each section's opening phrase for a word-accurate speech start. Timeline math from an earlier EDL drifts the moment the editor makes one more pass in Final Cut.
- **On slide-driven talks, verify each boundary visually with ffmpeg before finalizing.** A viewer who clicks a chapter should land on that chapter's slide, not the tail of the previous one — and slides often change a few seconds before or after the spoken transition. Two tools: extract the frame at each candidate time (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 -vf scale=640:-1 f.jpg`) and read it; scene-detect a window around it (`ffmpeg -ss <t-8> -t 12 -i video.mp4 -vf "select='gt(scene,0.08)',metadata=print:file=-" -an -f null -`) to find the exact slide-change moment. When the slide reveal and the speech start disagree, snap the chapter to whichever comes first. Caveat: soft fades between mostly-white slides can slip under scene detection — when a window comes back empty, fall back to eyeballing extracted frames. On talks that cut between a full-frame camera shot and slides, scene detection also fires on every camera cut, so a hit isn't proof of a slide change — read the frames to tell them apart. On screen recordings the boundary is where the screen resets to the step's starting state (a blank chat, a fresh page), which often comes a few seconds after the spoken transition. Bonus: frame checks catch render glitches (e.g. a stray slide flashing for a few frames at a cut) worth flagging to the editor.

## When in doubt

Prefer the description that:
- Puts the conversion CTA before the synopsis
- Uses a real URL over a descriptive placeholder
- Names the specific artifact over the generic activity
- Matches the published examples over sounding clever
