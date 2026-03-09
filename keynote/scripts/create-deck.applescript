-- create-deck.applescript
-- Usage: osascript create-deck.applescript "/path/to/.claude/keynote/new-deck.key"
-- Creates a new Keynote document using the "talk-basic" theme and saves it. Path MUST contain ".claude/keynote".

on run argv
	if (count of argv) < 1 then
		error "Usage: osascript create-deck.applescript <output-path>"
	end if

	set filePath to item 1 of argv

	-- Resolve to absolute path
	set parentDir to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" 2>/dev/null && pwd || echo ''"
	if parentDir is "" then
		error "Parent directory does not exist for: " & filePath
	end if
	set fileName to do shell script "basename " & quoted form of filePath
	set filePath to parentDir & "/" & fileName

	-- Safety check: path must contain ".claude/keynote"
	if filePath does not contain ".claude/keynote" then
		error "Output path must be within a .claude/keynote directory. Got: " & filePath
	end if

	set savePath to POSIX file filePath

	tell application "Keynote"
		set newDoc to make new document with properties {document theme:theme "talk-basic"}
		save newDoc in savePath
		close newDoc
	end tell

	return "Created: " & filePath
end run
