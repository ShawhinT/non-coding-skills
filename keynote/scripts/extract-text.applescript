-- extract-text.applescript
-- Usage: osascript extract-text.applescript "/path/to/file.key" [--positions] [--close]
-- Extracts slide text and presenter notes from a Keynote file.
-- --positions also prints each text item's {x, y} and width, so you can match
-- the layout of an existing deck when adding or restyling elements.

on run argv
	if (count of argv) < 1 then
		error "Usage: osascript extract-text.applescript <keynote-file-path> [--positions] [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set closeAfter to helpers's parseCloseFlag(argv)
	set showPos to false
	repeat with a in argv
		if (contents of a) is "--positions" then set showPos to true
	end repeat
	helpers's saveIfOpen(filePath)

	set fileRef to POSIX file filePath
	set output to ""

	tell application "Keynote"
		set wasRunning to running

		set theDocument to helpers's docForPath(filePath)
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
						set posTag to ""
						if showPos then
							try
								set p to position of ti
								set posTag to "{" & (item 1 of p) & ", " & (item 2 of p) & "} w=" & (width of ti) & " "
							end try
						end if
						if itemIndex is 1 then
							set output to output & posTag & "Title: " & textContent & linefeed
						else
							set output to output & posTag & "Text: " & textContent & linefeed
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
