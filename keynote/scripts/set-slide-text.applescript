-- set-slide-text.applescript
-- Usage: osascript set-slide-text.applescript "/path/to/deck.key" 1 "Title" "Subtitle" "Body" [--close]
-- Sets text on a single slide. Pass "" for unused fields.

on run argv
	if (count of argv) < 5 then
		error "Usage: osascript set-slide-text.applescript <deck-path> <slide-number> <title> <subtitle> <body> [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set slideNum to (item 2 of argv) as integer
	set titleText to item 3 of argv
	set subtitleText to item 4 of argv
	set bodyText to item 5 of argv
	set closeAfter to helpers's parseCloseFlag(argv)

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		set theDoc to helpers's docForPath(filePath)

		tell slide slideNum of theDoc
			set itemCount to count of text items

			if itemCount < 1 then
				-- Blank layout - nothing to set
			else
				set item1Pos to position of text item 1
				set item1Y to item 2 of item1Pos

				if item1Y > 900 then
					-- Title layout
					if titleText is not "" then set object text of text item 2 to titleText
					if subtitleText is not "" then set object text of text item 3 to subtitleText
					if bodyText is not "" then set object text of text item 1 to bodyText
				else if item1Y > 300 then
					-- Section layout
					if titleText is not "" then set object text of text item 1 to titleText
				else
					-- Title Only layout
					if titleText is not "" then set object text of text item 1 to titleText
					if subtitleText is not "" then set object text of text item 2 to subtitleText
					if bodyText is not "" then
						set newItem to make new text item with properties {object text:bodyText, position:{72, 300}, width:1130, height:600}
					end if
				end if
			end if
		end tell

		save theDoc
		if closeAfter then close theDoc
	end tell

	return "Set text on slide " & slideNum
end run
