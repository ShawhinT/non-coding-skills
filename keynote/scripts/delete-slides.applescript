-- delete-slides.applescript
-- Usage: osascript delete-slides.applescript "/path/to/file.key" "3,5,10-15,20" [--close]
-- Deletes specified slides from a Keynote file.
-- Slides are deleted from highest to lowest to preserve numbering.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript delete-slides.applescript <keynote-file-path> <slide-numbers> [--close]" & linefeed & "Examples: \"3,5,10\" or \"10-15\" or \"3,5,10-15,20\""
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set slideSpec to item 2 of argv
	set closeAfter to helpers's parseCloseFlag(argv)

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	-- Parse slide spec into a sorted list of unique slide numbers using shell
	set slideNumbers to do shell script "echo " & quoted form of slideSpec & " | tr ',' '\\n' | while read spec; do if echo \"$spec\" | grep -q '-'; then start=$(echo \"$spec\" | cut -d'-' -f1); finish=$(echo \"$spec\" | cut -d'-' -f2); seq $start $finish; else echo \"$spec\"; fi; done | sort -rn | uniq"

	set slideList to paragraphs of slideNumbers
	set fileRef to (POSIX file filePath) as alias
	set deletedCount to 0

	tell application "Keynote"
		set theDocument to helpers's docForPath(filePath)
		set slideCount to count of slides of theDocument

		repeat with slideNumStr in slideList
			set slideNum to slideNumStr as integer
			if slideNum > 0 and slideNum ≤ slideCount then
				delete slide slideNum of theDocument
				set deletedCount to deletedCount + 1
			end if
		end repeat

		set remainingCount to count of slides of theDocument

		save theDocument
		if closeAfter then close theDocument
	end tell

	return "Deleted " & deletedCount & " slides. Remaining: " & remainingCount & " slides."
end run
