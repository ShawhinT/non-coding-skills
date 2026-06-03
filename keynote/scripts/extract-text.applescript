-- extract-text.applescript
-- Usage: osascript extract-text.applescript "/path/to/file.key" [--close]
-- Extracts slide text and presenter notes from a Keynote file.

on run argv
	if (count of argv) < 1 then
		error "Usage: osascript extract-text.applescript <keynote-file-path> [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set closeAfter to helpers's parseCloseFlag(argv)
	helpers's saveIfOpen(filePath)

	set fileRef to POSIX file filePath
	set output to ""

	tell application "Keynote"
		set wasRunning to running

		open fileRef
		set theDocument to front document
		set docName to name of theDocument
		set output to output & "=== " & docName & " ===" & linefeed & linefeed

		set slideCount to count of slides of theDocument

		repeat with i from 1 to slideCount
			set theSlide to slide i of theDocument
			set output to output & "--- Slide " & i & " of " & slideCount & " ---" & linefeed

			if skipped of theSlide then
				set output to output & "(skipped)" & linefeed & linefeed
			else
				set textItems to every text item of theSlide
				set itemIndex to 0
				repeat with ti in textItems
					set itemIndex to itemIndex + 1
					set textContent to object text of ti
					if textContent is not "" then
						if itemIndex is 1 then
							set output to output & "Title: " & textContent & linefeed
						else
							set output to output & "Text: " & textContent & linefeed
						end if
					end if
				end repeat

				set theNotes to presenter notes of theSlide
				if theNotes is not "" then
					set output to output & "Notes: " & theNotes & linefeed
				end if

				set output to output & linefeed
			end if
		end repeat

		if closeAfter then
			close theDocument saving no
			if not wasRunning then quit
		end if
	end tell

	return output
end run
