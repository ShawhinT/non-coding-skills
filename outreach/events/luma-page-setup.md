# Luma Page Setup

Setting up a Luma event page, usually by cloning an existing event in the same series. The copy itself (title, description blocks) is conversion-copy's job (`channel-event-pages.md`). This file covers making the page match that copy and how the editor behaves. The editor UI changes often, so the mechanics are kept here where a UI change only means fixing one file.

## Clone an existing event, don't build up from scratch

When a series already has a live event, that event is the spec. The new page should match it exactly. That means the same registration questions in the same order, with the same required flags, plus the same description, capacity and settings. After that, apply only the changes for this event (partner, city, date, anything the hub page lists as event-specific). Questions left over from a duplicated page are wrong even if they look harmless. If there are extra questions or the order differs, the page doesn't match the template. Check this before calling the page done. The series' canonical question list and description usually live on its Notion campaign hub page, so read that first.

## Editor mechanics

Work in the manage view (`luma.com/event/manage/<evt-id>`). Use DOM reads to check state. Screenshots lag behind toggles and saves.

- **Description.** The editor is Tiptap. Set the whole body in one go instead of typing it in:
  `document.querySelector('.tiptap.ProseMirror').editor.commands.setContent(html, true)`
  Then click **Update Event**. Nothing is saved until you do.
- **Registration questions.** To delete one: Edit → trash icon → confirm Delete. To add one: Add Question → pick the type (Options, Text, …) → fill it in.
- **Required toggle.** Set it from inside the question dialog with
  `const s = dialog.querySelector('[role=switch]'); if (!s.checked) s.click();`
  Then read `checked` back to confirm it changed.
- **Order.** Drag-to-reorder doesn't work here: the drag selects text instead of moving the question. To fix the order, delete the out-of-place questions and re-add them in sequence. They're appended to the end, so re-add in the order they should finally appear.
