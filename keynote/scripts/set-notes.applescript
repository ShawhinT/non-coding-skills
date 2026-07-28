-- set-notes.applescript
-- Usage: osascript set-notes.applescript "/path/to/deck.key" 1 "Presenter note text" [--close]
-- Sets the presenter notes on a single slide. Use \n in the text for line breaks
-- (pass it from the shell as an ANSI-C string, e.g. $'line 1\nline 2').

on run argv
	if (count of argv) < 3 then
		error "Usage: osascript set-notes.applescript <deck-path> <slide-number> <note-text> [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set slideNum to (item 2 of argv) as integer
	set noteText to item 3 of argv
	set closeAfter to helpers's parseCloseFlag(argv)

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		set theDoc to helpers's docForPath(filePath)
		set presenter notes of slide slideNum of theDoc to noteText
		save theDoc
		if closeAfter then close theDoc
	end tell

	return "Set presenter notes on slide " & slideNum
end run
