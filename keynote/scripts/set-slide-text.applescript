-- set-slide-text.applescript
-- Usage: osascript set-slide-text.applescript "/path/to/.claude/keynote/deck.key" 1 "Title" "Subtitle" "Body text"
-- Sets text on a single slide. Pass "" for unused fields.
-- Path MUST contain ".claude/keynote".
--
-- Layout detection (talk-basic theme):
--   Title layout:      item 1 at y>900 (footer), item 2 (big title), item 3 (subtitle)
--   Section layout:    item 1 at y>300 (center text)
--   Title Only layout: item 1 at y<200 (title), item 2 (subtitle), no body — body created via make new text item

on run argv
	if (count of argv) < 5 then
		error "Usage: osascript set-slide-text.applescript <deck-path> <slide-number> <title> <subtitle> <body>"
	end if

	set filePath to item 1 of argv
	set slideNum to (item 2 of argv) as integer
	set titleText to item 3 of argv
	set subtitleText to item 4 of argv
	set bodyText to item 5 of argv

	-- Resolve to absolute path
	set filePath to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" && echo \"$(pwd)/$(basename " & quoted form of filePath & ")\""

	-- Safety check
	if filePath does not contain ".claude/keynote" then
		error "Output path must be within a .claude/keynote directory. Got: " & filePath
	end if

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		open fileRef
		set theDoc to front document

		tell slide slideNum of theDoc
			set itemCount to count of text items

			if itemCount < 1 then
				-- Blank layout - nothing to set
			else
				-- Detect layout by checking y-position of text item 1
				set item1Pos to position of text item 1
				set item1Y to item 2 of item1Pos

				if item1Y > 900 then
					-- Title layout: item 1 = footer/author (y~934), item 2 = big title (y~203), item 3 = subtitle (y~569)
					if titleText is not "" then
						set object text of text item 2 to titleText
					end if
					if subtitleText is not "" then
						set object text of text item 3 to subtitleText
					end if
					if bodyText is not "" then
						-- bodyText doubles as author/footer for Title layout
						set object text of text item 1 to bodyText
					end if
				else if item1Y > 300 then
					-- Section layout: item 1 = center text (y~357)
					if titleText is not "" then
						set object text of text item 1 to titleText
					end if
				else
					-- Title Only layout: item 1 = title (y~85), item 2 = subtitle (y~187)
					if titleText is not "" then
						set object text of text item 1 to titleText
					end if
					if subtitleText is not "" then
						set object text of text item 2 to subtitleText
					end if
					if bodyText is not "" then
						-- No body placeholder exists — create a freeform text box
						set newItem to make new text item with properties {object text:bodyText, position:{72, 300}, width:1130, height:600}
					end if
				end if
			end if
		end tell

		save theDoc
		close theDoc
	end tell

	return "Set text on slide " & slideNum
end run
