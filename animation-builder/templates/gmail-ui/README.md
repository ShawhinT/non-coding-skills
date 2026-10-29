# gmail-ui kit

Gmail (light) Drafts view + compose window, for demos where Claude's output is a Gmail draft.
Matched to `reference/` captures (2026-10-12) and scaled ~1.45x so the body reads on a projector.
Roboto stands in for Google Sans; the message body is Arial, as in real Gmail.

Copy `gmail-ui.css`, `gmail-ui.js` and `gmail.png` into `<video>/assets/src/shared/` next to the
claude-ui kit (it reuses that kit's captions, cursor and keyframes). See `scene-example.html`.

`gmail({ rows, draft, openAt, user })`
- `rows`: Drafts-list rows `{sub, snip, tm}`, newest first. Each shows the red "Draft" label.
- `draft`: `{to, cc, subject, body, hlTo, hlCc}`. `body` is HTML; use `<ul>` for bullets and `<a>` for
  links. Highlights are seconds: `hlTo`/`hlCc` tint a recipient row, `<li class="gm-li hl" style="--h:Ns">`
  or `<a class="hl" style="--h:Ns">` tint a line or link. With no `cc`, the To row shows "Cc Bcc", which
  is how a missing CC reads at a glance.
- `openAt`: null = compose open from t=0; a number = row 0 hovers just before and the window opens then.

Gmail's connector can't attach files, so put documents in the body as Drive links rather than as
attachment chips.
