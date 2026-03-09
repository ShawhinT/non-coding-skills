-- add-slides.applescript
-- Usage: osascript add-slides.applescript "/path/to/.claude/keynote/deck.key" "Title Only" 3
-- Opens deck, adds <count> slides using the named master layout, saves, closes.
-- Path MUST contain ".claude/keynote".

on run argv
	if (count of argv) < 3 then
		error "Usage: osascript add-slides.applescript <deck-path> <master-name> <count>"
	end if

	set filePath to item 1 of argv
	set masterName to item 2 of argv
	set slideCount to (item 3 of argv) as integer

	-- Resolve to absolute path
	set filePath to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" && echo \"$(pwd)/$(basename " & quoted form of filePath & ")\""

	-- Safety check: path must contain ".claude/keynote"
	if filePath does not contain ".claude/keynote" then
		error "Output path must be within a .claude/keynote directory. Got: " & filePath
	end if

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		open fileRef
		set theDoc to front document

		set theMaster to master slide masterName of theDoc
		repeat slideCount times
			make new slide at end of slides of theDoc with properties {base slide:theMaster}
		end repeat

		set totalSlides to count of slides of theDoc

		save theDoc
		close theDoc
	end tell

	return "Added " & slideCount & " slides with master \"" & masterName & "\". Total slides: " & totalSlides
end run
