-- add-slides.applescript
-- Usage: osascript add-slides.applescript "/path/to/deck.key" "Title Only" 3 [--close]
-- Opens deck, adds <count> slides using the named master layout, saves.

on run argv
	if (count of argv) < 3 then
		error "Usage: osascript add-slides.applescript <deck-path> <master-name> <count> [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set masterName to item 2 of argv
	set slideCount to (item 3 of argv) as integer
	set closeAfter to helpers's parseCloseFlag(argv)

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		set theDoc to helpers's docForPath(filePath)

		set theMaster to master slide masterName of theDoc
		repeat slideCount times
			make new slide at end of slides of theDoc with properties {base slide:theMaster}
		end repeat

		set totalSlides to count of slides of theDoc

		save theDoc
		if closeAfter then close theDoc
	end tell

	return "Added " & slideCount & " slides with master \"" & masterName & "\". Total slides: " & totalSlides
end run
