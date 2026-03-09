-- delete-slides.applescript
-- Usage: osascript delete-slides.applescript "/path/to/.claude/keynote/file.key" "3,5,10-15,20"
-- Deletes specified slides from a Keynote file. File MUST be in a .claude/keynote directory.
-- Accepts comma-separated slide numbers and ranges (e.g. "3,5,10-15,20").
-- Slides are deleted from highest to lowest to preserve numbering.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript delete-slides.applescript <keynote-file-path> <slide-numbers>" & linefeed & "Examples: \"3,5,10\" or \"10-15\" or \"3,5,10-15,20\""
	end if

	set filePath to item 1 of argv
	set slideSpec to item 2 of argv

	-- Resolve to absolute path
	set filePath to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" && echo \"$(pwd)/$(basename " & quoted form of filePath & ")\""

	-- Safety check: file must be in a .claude/keynote directory
	if filePath does not contain ".claude/keynote" then
		error "File must be within a .claude/keynote directory. Got: " & filePath
	end if

	-- Parse slide spec into a sorted list of unique slide numbers using shell
	set slideNumbers to do shell script "echo " & quoted form of slideSpec & " | tr ',' '\\n' | while read spec; do if echo \"$spec\" | grep -q '-'; then start=$(echo \"$spec\" | cut -d'-' -f1); finish=$(echo \"$spec\" | cut -d'-' -f2); seq $start $finish; else echo \"$spec\"; fi; done | sort -rn | uniq"

	-- Convert to AppleScript list
	set slideList to paragraphs of slideNumbers

	set fileRef to (POSIX file filePath) as alias

	set deletedCount to 0

	tell application "Keynote"
		open fileRef
		set theDocument to front document
		set slideCount to count of slides of theDocument

		-- Delete slides from highest number to lowest (to preserve indices)
		repeat with slideNumStr in slideList
			set slideNum to slideNumStr as integer
			if slideNum > 0 and slideNum ≤ slideCount then
				delete slide slideNum of theDocument
				set deletedCount to deletedCount + 1
			end if
		end repeat

		set remainingCount to count of slides of theDocument

		save theDocument
		close theDocument
	end tell

	return "Deleted " & deletedCount & " slides. Remaining: " & remainingCount & " slides."
end run
