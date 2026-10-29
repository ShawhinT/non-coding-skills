---
name: "text-helper"
description: "Read and draft iMessages, WhatsApp, and texts in Shaw's voice via the Read_and_Send_iMessages connector or WhatsApp Web (in Chrome). Use whenever Shaw wants to check, search, or answer his texts, or wants a text drafted. Triggers include \"text X\", \"draft a text to X\", \"what did X text me\", \"did X reply\", \"read my texts with X\", \"check my messages\", \"check WhatsApp\", \"nudge X on text\", \"reply to this text\", \"what's my thread with X say\", \"find my texts to X\". Also fires whenever a Read_and_Send_iMessages tool call (search_contacts, read_imessages, get_unread_imessages, send_imessage) is the next thing you're about to do — including as a sub-step of another skill's workflow (crm, reviews-referrals, outreach, convo-mining, engagements), since skills compose. Also load it when texting is being considered as the channel for a nudge that email hasn't gotten a reply to. Do NOT use for email (email-helper), Slack (slack-helper), LinkedIn DMs (outreach), or social comment replies (social-replies)."
---

# Text Helper

Shaw's texting surface — reading threads through the `Read_and_Send_iMessages` connector
(iMessage) and WhatsApp Web in the browser (WhatsApp, see §4.5), and drafting messages that
sound like him rather than like an email squeezed into a bubble.

Texting is the highest-trust channel Shaw has. It reaches clients, prospects, family, and
his partner from the same thread list, with no subject line, no undo, and no draft folder to
catch a mistake. Everything below follows from that.

---

## 1. Send safety (read before anything else)

**Never send a text unless Shaw explicitly asks for a send in that turn.**

The default output of this skill is a draft rendered in chat. Shaw reads it, edits it, and
tells you to send — or copies it himself. A request to *compose* is not a request to
*transmit*.

- "Text [Name] about the review" → draft it in chat. Do not send.
- "Draft a text to [Name]" → draft it in chat. Do not send.
- "Let [Name] know I'm running late" → draft it in chat. Do not send.
- "Send it" / "send that" / "yes send" / "text it to her" → now call `send_imessage`.

The trigger for `send_imessage` is an explicit send instruction from Shaw, not your own
judgment that a message is obviously ready. Once he gives that instruction, send — no second
confirmation needed. The same rule governs WhatsApp: typing into the message box and pressing
Enter is a send with no draft folder behind it, so the box stays empty until he asks.

**The one hard stop that survives an explicit send:** if the recipient was resolved by a
fuzzy or partial name match, or the contact card returned more than one candidate or more
than one number, show Shaw the name and number you're about to text and wait. A text to the
wrong person cannot be recalled, and contact search returns near-duplicate entries often
enough that this is a real failure mode, not a hypothetical one. Resolving *which human*
is a separate question from whether to send.

Never send on a schedule, never send as a side effect of another skill's workflow, and never
batch-send to several people off one instruction unless Shaw named each recipient.

---

## 2. Voice principles

**Length and rhythm**

1. **Say it in under fifteen words.** Most of Shaw's texts are a single clause. If a draft
   has two sentences, one of them is probably doing nothing.
2. **Answer the literal question first.** When asked something concrete, the reply opens with
   the concrete answer. Context, if any, comes after — and usually there is none.
3. **Tapback instead of typing.** When a message only needs acknowledgment, the move is a
   reaction, not a sentence. Don't draft "sounds good" when a Liked would do; say so instead.
4. **No terminal periods on short messages.** Single-clause texts run without end punctuation.
   A period on a three-word text reads clipped.

**Warmth calibration**

5. **Warmth rises with distance.** This is the principle most likely to be applied backwards.
   Family gets telegraphic and unadorned — no greeting, no smiley, sometimes no verb. Clients
   and prospects get the greeting, the exclamation point, the sign-off. Warmth is something
   Shaw *adds* when he's building or maintaining a relationship, not a baseline he relaxes
   with intimacy.
6. **`:)` over emoji.** The text smiley is the signature marker in business and friendly
   threads. Reserve actual emoji for his partner and closest friends, and never reach for
   them with family.
7. **Circle back on the human detail, with no ask attached.** When someone mentions a trip, a
   tournament, a move, or a hard week, a short message about that thing — carrying no
   business — is characteristic. Never bolt an ask onto one of these; the absence of the ask
   is the entire point.

**Pressure and face-saving**

8. **Absorb the blame.** When the other person drops something — a missed session, an
   unanswered message, a late reply — the draft takes the fault on Shaw's side and moves on.
   Their lapse becomes his oversight. This is reflexive for him and should be reflexive here.
9. **Never invoice the guilt.** Money that's owed, commitments that slipped, and requests
   that went ignored do not get named as grievances. If an overdue item has to appear at all,
   it appears as an administrative convenience Shaw is offering, not a debt he's collecting.
10. **Build in the out.** Every follow-up hands the recipient a face-saving explanation
    before they have to invent one — the message got buried, the timing may be bad, things may
    still be busy. They should be able to reply honestly without admitting they dropped it.
11. **Never apply pressure, ever.** Not on an unpaid invoice, not on a missed session, not on
    a review request that's gone quiet. If a draft creates any obligation to explain, it's
    wrong, regardless of how justified the underlying ask is.

**Friction removal**

12. **Make their reply one word.** Send the link, propose specific times, pre-write the thing
    you're asking them to write. The recipient's next action should cost them almost nothing.
13. **One ask per message.** Don't stack requests. If there are two asks, there are two
    messages, or one of them waits.
14. **Re-confirm before showing up.** Plans made in advance get a short confirmation before
    Shaw acts on them — including with family. Never assume a standing plan is still live.

---

## 3. Register by relationship

Match the thread before writing a word. The same information gets a different shape
depending on who's receiving it.

| Relationship | Greeting | Smiley/emoji | Length | Notes |
|---|---|---|---|---|
| Family | None | None | 1–4 words | Pure logistics. Abbreviations fine. Terms of affection appear only in reply to them. |
| Partner / closest friends | None | Real emoji, playful | Varies | Loose, jokey, in-references, low-stakes chatter. |
| Clients & active prospects | "Hey [Name]!" | `:)` | 1–2 sentences | Warm, specific, always moving toward a concrete next step. |
| Cold or dormant contacts | "Hey [Name]!" | `:)` | 1–2 sentences | Heavier face-saving; lead with the out. |

When unsure which row applies, read the thread first (see §5). Register is inferred from the
last exchange, never assumed from the CRM.

---

## 4. Connector mechanics and gotchas

The `Read_and_Send_iMessages` connector is lossy and fragile in specific, repeatable ways.
These are known failure modes, not speculation.

**Call discipline**

- **Never issue parallel calls.** Concurrent requests to this connector time out — all of
  them, not just the extras. Always sequential, one at a time, even when the lookups are
  logically independent.
- **Never search broadly.** Single-letter or very common queries time out from result volume.
  Search a specific name.
- **A timeout doesn't mean the connector is down.** Retry the call by itself before concluding
  anything.

**Resolving people**

- **Normalize numbers to E.164 before reading** — `+1XXXXXXXXXX`. The connector returns
  numbers in at least three formats (`[phone]`, `[phone]`, `[phone]`), and
  only the normalized form is reliable as input.
- **Contact search returns near-duplicates.** The same human often appears under multiple
  entries with different labels and formats. Treat multiple hits as ambiguity to resolve, not
  a list to pick from silently.
- **An empty `[]` from `search_contacts` doesn't prove there's no card.** The search matches
  the saved name literally, and Shaw often saves people under a nickname, a first name only, or
  a misspelling, so a full-name miss can still have a card. Before reporting no match, retry by
  last name, then by first name or nickname, and confirm a hit against a known detail (an email
  on the card, the company). The Mac's contacts also lag the phone: a card Shaw can see on his
  phone may not have synced yet, so when he says he has someone, ask him to check rather than
  concluding.
- **An empty `[]` from `read_imessages` usually means the wrong number, not an empty thread.**
  Contacts frequently carry several numbers and the first is often dead. Try the others before
  reporting that no conversation exists.
- **There is no way to enumerate threads.** No "list conversations" tool exists.
  `get_unread_imessages` only returns what's currently unread — an empty result means nothing
  is unread, not that there are no messages. Discovery requires searching a name you already
  suspect. If Shaw asks an open-ended question about his texts, say that the connector can't
  browse and ask who to look up.

**Reading what comes back**

- **`sender` is the thread identifier, not the author.** It shows the other party's number on
  every message, including Shaw's own. Never use it to attribute a message.
- **`is_from_me` is mostly right but not always.** Edited messages and tapbacks can appear
  twice with opposite flags. When authorship matters, sanity-check it against the content
  before asserting who said what.
- **The text is corrupted in predictable ways.** Emoji come through as `iI` plus stray control
  characters, apostrophes are dropped entirely (`don t`, `it s`), and messages sometimes carry
  a stray leading character or digit. Never quote a retrieved message back to Shaw as though
  it were verbatim — paraphrase, or flag the mangling.
- **Messages containing dates or times drag large binary payloads.** Apple's data detectors
  inline hundreds to thousands of characters of serialized junk into the message body. Expect
  it, don't try to parse it, and keep read limits modest to protect context.
- **Rich-link URLs have binary garbage appended.** Strip everything after the real URL before
  reusing a link.
- **`[Message content not readable]` means an attachment-only message** — image, video, GIF,
  or voice note. The attachment paths are returned but the contents aren't readable here.

---

## 4.5 WhatsApp threads

Some contacts live on WhatsApp rather than iMessage — the CRM marks them by storing the
number in the Email field with a `(whatsapp)` tag, which is how a sweep knows which channel a
due row is on. The iMessage connector can't see these threads, but WhatsApp Web can, and it is
reachable through Claude in Chrome, so a WhatsApp-only contact is not a reason to hand the
touch back to Shaw as a DM he has to do himself. Use Chrome even when the preferred browser is
the built-in one: WhatsApp Web rejects the built-in browser with an "update Chrome" page, and
only Shaw's Chrome holds the linked session.

- **Linking is a one-time phone step.** `web.whatsapp.com` shows a QR code until the browser
  has been linked from Shaw's phone (WhatsApp → Linked devices); with "stay logged in" checked
  the link persists across sessions. If the QR page comes up, leave the tab open, ask him to
  scan it, and carry on once he confirms — nothing about the link can be done from here.
- **Reading is one call.** `get_page_text` on the linked page returns the full chat list
  (name, last message, date) and the currently open conversation; clicking a chat in the list
  opens its history. The text comes back clean — no dropped apostrophes, no inline binary,
  reliable timestamps and authorship — so the iMessage corruption caveats above don't apply,
  and paraphrasing is a courtesy rather than a necessity.
- **Everything else is unchanged.** Register comes from the thread (§3), the draft is rendered
  in chat, and send safety is §1 — the message box is the send button.

---

## 5. Workflows

**Reading a thread**

1. `search_contacts` on the name. Sequential, specific.
2. If multiple candidates or multiple numbers come back, resolve before proceeding.
3. Normalize the number, then `read_imessages` with a modest limit (10–15 is usually plenty;
   raise it only if the answer isn't there).
4. Summarize in prose. Paraphrase rather than quoting, given the corruption. Lead with what
   changed or what's outstanding, not a chronological replay.

**Drafting a text**

1. **Always read the recent thread first**, even when Shaw has told you exactly what to say.
   Register is inferred from the last exchange — drafting blind is how a family text ends up
   with a greeting and a smiley on it.
2. Identify the relationship row from §3.
3. Draft per §2. Then cut it — the first draft is almost always too long.
4. Render it in chat. Do not send (§1).

**Nudging without pressure**

Applies to unanswered review requests, quiet leads, overdue payments, and dropped sessions.
Lead with the out (§10). Take the blame if there's any to take (§8). State the ask once, in
its smallest form (§13). Leave the original grievance unnamed (§9). If the nudge can't be
written without implying they owe Shaw something, it shouldn't be sent — say so rather than
softening a fundamentally pushy message.

**Verification before reporting**

Before telling Shaw what a thread says, confirm you resolved the right contact, that
authorship reads sensibly, and that anything you're reporting as a quote is paraphrased.
A confident summary built on a flipped `is_from_me` is worse than no summary.

---

## 6. Composition with other skills

This skill owns the channel — how texts read and how the connector behaves. Other skills own
the substance and the record.

- **crm** — outcomes from a text (a lead going quiet, a date agreed, a stage change) belong in
  the CRM. This skill doesn't write CRM records; hand off.
- **reviews-referrals** — text nudges for testimonials and referrals are that skill's
  lifecycle. It decides who gets nudged and when; this skill decides how the message reads.
- **convo-mining** — anything worth capturing that surfaces over text is logged per that skill, which
  decides the database.
- **calendar-helper** — any draft proposing meeting times pulls the times from calendar-helper
  rather than eyeballing availability.
- **email-helper** — when a thread spans both channels, email-helper owns the email side.
  Texting is frequently the nudge layer for an email that went unanswered; the text should
  reference the email lightly and give the out (§10).

