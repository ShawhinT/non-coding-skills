---
name: google-drive-helper
description: Navigate Shaw's Google Drive (aibuilder.academy workspace) — search, read file contents, navigate known folders, and avoid the connector's quirks. Use whenever Shaw asks to find a file in Drive, read a Google Doc/Sheet/Slide/PDF, look in a specific folder, pull form responses, locate something he uploaded, or do anything Drive-adjacent. Triggers include "find X in my drive", "what's in the forms folder", "read this doc", "pull the responses for X", "is X in my drive", "search drive for X", "do I have a file about X". Even casual mentions like "where's that proposal I wrote", "the spreadsheet I made last week", or "look in Drive" should fire this skill. Also trigger when Shaw shares a Drive URL and asks to read it. Do NOT use for file *organization* (moving, renaming, batch operations).
---

# Google Drive Helper

Reference for navigating Shaw's Google Drive — finding files, reading contents, and avoiding the connector's footguns. Load it, then act based on the request.

## Workspace

The Drive connector is wired to Shaw's **aibuilder.academy** account only (the ABA business workspace). Files owned by other accounts (Shaw's personal Gmail, clients, collaborators) only surface when they've been explicitly shared into the aibuilder.academy workspace — those show up in search with `sharedWithMeTime` populated. There's no way to list arbitrary contents of folders owned by other accounts; only individually shared files are reachable.

When linking back to Shaw, use the `viewUrl` returned by the API. Don't hand-rewrite URLs.

## Known Folders

Hardcoded folder IDs Shaw uses regularly. When asked about content in any of these, search by `parentId =` directly instead of doing a fuzzy title search.

| Folder | ID | What's inside |
|---|---|---|
| `forms` | `[drive-folder-id]` | Google Forms (intake, testimonial, feedback, etc.). Some entries are shortcuts to Forms shared in from elsewhere. |
| `sheets` | `[drive-folder-id]` | Linked response sheets for the forms above. |

When Shaw says "the forms folder" or "my response sheets," use the IDs above directly.

## Tool Cheatsheet

| Need | Tool |
|---|---|
| Find files by query | `search_files` (Drive query syntax) |
| Recently touched | `list_recent_files` |
| File metadata only | `get_file_metadata` |
| Read content as text | `read_file_content` |
| Download as bytes (base64) | `download_file_content` |
| Permissions | `get_file_permissions` |
| Create new file | `create_file` |
| Copy file | `copy_file` |

## Connector Quirks (have actually bitten)

1. **`mimeType = 'application/vnd.google-apps.form'` returns nothing.** The mimeType filter doesn't work for Forms specifically. Fall back to title-based search (`title contains 'form' or title contains 'intake' or ...`) or filter by the known forms folder's `parentId`.
2. **Forms can't be read or downloaded.** `read_file_content` rejects Forms ("unsupported mime type") and `download_file_content` errors internally. To see form questions or responses, open the linked response sheet in the `sheets` folder.
3. **No deep-link to individual form responses.** Without a Forms-specific MCP, the per-respondent edit URL isn't reachable — only the form's `#responses` summary URL. Tell Shaw this and offer the response-sheet row instead.
4. **Shortcuts vs. files.** The `forms` folder contains both real Forms (`application/vnd.google-apps.form`) and shortcuts (`application/vnd.google-apps.shortcut`). Shortcuts point to files shared into the workspace from elsewhere. When listing, surface both; when reading, resolve to the target ID first.
5. **Title search is case-insensitive but returned titles preserve case.** Don't echo a casing different from the file's actual name.
6. **Files that aren't shared in aren't reachable.** If a folder's `parentId` lookup returns empty but you saw the folder ID in metadata earlier, it's likely owned by another account and only individual files are shared — not the whole folder. Stop and tell Shaw rather than guessing.

## Search Query Syntax

`search_files` uses Drive's query language. Combine clauses with `and`, `or`, `not`, parentheses. String values must be single-quoted.

| Clause | Example |
|---|---|
| Title contains | `title contains 'invoice'` |
| Title exact | `title = 'My Doc'` |
| MIME type | `mimeType = 'application/vnd.google-apps.spreadsheet'` (works for most types — not Forms; see Quirks) |
| Folder | `parentId = '<folder_id>'` — use `'root'` for top-level My Drive |
| Fulltext | `fullText contains 'OAuth'` (matches title or body) |
| Owner | `owner = 'me'` or `owner = '[email]'` |
| Shared | `sharedWithMe = true` |
| Date | `modifiedTime > '2025-01-01T00:00:00Z'` |

When the mimeType filter misbehaves, batch keyword variants:
`title contains 'form' or title contains 'survey' or title contains 'intake' or title contains 'feedback' or title contains 'application'`

## Common Workflows

### "Find me X" (general lookup)
1. If Shaw names a known folder (forms, sheets), go straight to `parentId =` — don't fuzzy search the whole Drive.
2. Otherwise: title-based search first. Add `fullText contains` as a fallback if title hits nothing.
3. Return 5-10 hits. If >25, narrow before returning everything.

### "What does X say?" (read content)
1. Try `read_file_content` first — handles Docs, Sheets, Slides, PDFs, Office formats.
2. If the connector rejects the mime type (Forms, video, audio, images), use `download_file_content` for bytes. For Forms specifically, jump to the linked response sheet instead.
3. Quote sparingly. Don't dump full files.

### "Pull responses for the X form"
1. Look in the `sheets` folder for a sheet whose title is `<form name> (Responses)`.
2. `read_file_content` on the sheet — questions are columns, responses are rows.
3. The form itself can't be read directly; the response sheet is the canonical source.

### "Where's that file I [made / shared / opened] last week?"
`list_recent_files` with `orderBy: 'lastModifiedByMe'` or `'recency'`. Faster than searching.

### "What's in the [folder name] folder?"
- Known folder → use the hardcoded ID.
- Unknown folder → `title = '<folder name>' and mimeType = 'application/vnd.google-apps.folder'` to find the folder ID, then `parentId = '<id>'`.
- If `parentId =` returns empty for a folder that *should* have contents, the folder is likely owned by another account and not actually accessible — flag this to Shaw.

## Linking Back to Shaw

When sharing a file:
- **Google native (Doc/Sheet/Slide)**: use the `viewUrl` from the API.
- **Form**: `https://docs.google.com/forms/d/<id>/edit` — append `#responses` to land on the responses tab.
- **Folder**: `https://drive.google.com/drive/folders/<id>`

Always copy the URL the API returns; don't hand-craft.

---

If a question hits a quirk not listed here (new error, unexpected mime type behavior), surface it to Shaw rather than guessing. The connector is undocumented in places.
