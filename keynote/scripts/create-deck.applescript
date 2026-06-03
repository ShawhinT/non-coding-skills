-- create-deck.applescript
-- Usage: osascript create-deck.applescript "/path/to/new-deck.key" [--close]
-- Creates a new Keynote document using the "talk-basic" theme. Refuses to overwrite an existing file.

on run argv
	if (count of argv) < 1 then
		error "Usage: osascript create-deck.applescript <output-path> [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set rawPath to item 1 of argv

	-- Resolve to absolute path (parent dir must exist)
	set parentDir to do shell script "cd \"$(dirname " & quoted form of rawPath & ")\" 2>/dev/null && pwd || echo ''"
	if parentDir is "" then
		error "Parent directory does not exist for: " & rawPath
	end if
	set fileName to do shell script "basename " & quoted form of rawPath
	set filePath to parentDir & "/" & fileName

	set closeAfter to helpers's parseCloseFlag(argv)

	-- Refuse to overwrite an existing deck
	set fileExists to do shell script "[ -e " & quoted form of filePath & " ] && echo yes || echo no"
	if fileExists is "yes" then
		error "Refusing to overwrite existing file: " & filePath & ". Delete it first or choose a different path."
	end if

	set savePath to POSIX file filePath

	tell application "Keynote"
		set newDoc to make new document with properties {document theme:theme "talk-basic"}
		save newDoc in savePath
		if closeAfter then close newDoc
	end tell

	return "Created: " & filePath
end run
