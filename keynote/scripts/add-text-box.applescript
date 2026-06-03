-- add-text-box.applescript
-- Usage: osascript add-text-box.applescript "<deck-path>" <slide-number> "<text>" "<position>" [width] [font] [size] [--close]
-- Adds a freeform text box to a slide.
--
-- <text>:     use \n (literal backslash-n) to separate lines; each becomes its own line in the box.
-- <position>: bottom-right, bottom-left, top-right, top-left, center, or "x,y" (canvas is 1920x1080).
-- [width]     optional, default 560.
-- [font]      optional PostScript font name (e.g. Menlo-Bold). If omitted, the theme default is kept.
-- [size]      optional point size, default 32.
--
-- IMPORTANT: text items must be created INSIDE a `tell <slide>` block and the creation
-- properties MUST include `height` — omitting it (or using `make new text item at end of slide`)
-- throws `AppleEvent handler failed (-10000)`. This is a creation-structure problem, NOT a
-- special-character/Unicode problem. font/size are set on `object text` AFTER creation.

on run argv
	if (count of argv) < 4 then
		error "Usage: osascript add-text-box.applescript <deck-path> <slide-number> <text> <position> [width] [font] [size] [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set slideNum to (item 2 of argv) as integer
	set rawText to item 3 of argv
	set posArg to item 4 of argv

	set closeAfter to helpers's parseCloseFlag(argv)

	-- Collect optional positional args (items 5+), skipping the --close flag.
	set opts to {}
	if (count of argv) ≥ 5 then
		repeat with i from 5 to (count of argv)
			set a to item i of argv
			if a is not "--close" then set end of opts to a
		end repeat
	end if

	set boxWidth to 560
	set theFont to missing value
	set theSize to 32
	if (count of opts) ≥ 1 then
		try
			set boxWidth to (item 1 of opts) as integer
		end try
	end if
	if (count of opts) ≥ 2 then set theFont to (item 2 of opts)
	if (count of opts) ≥ 3 then
		try
			set theSize to (item 3 of opts) as integer
		end try
	end if

	-- Convert literal "\n" (backslash + n) into real newlines. Done OUTSIDE the Keynote tell
	-- block, where `text items` would refer to slide objects instead of string parts.
	set boxText to my replaceText(rawText, "\\n", (ASCII character 10))

	-- Count lines for height estimation / placement.
	set AppleScript's text item delimiters to (ASCII character 10)
	set lineCount to (count of text items of boxText)
	set AppleScript's text item delimiters to ""
	if lineCount < 1 then set lineCount to 1
	set boxHeight to (lineCount * theSize * 1.6) as integer
	if boxHeight < (theSize * 2) then set boxHeight to (theSize * 2) as integer

	-- Parse explicit "x,y" outside the Keynote tell block.
	set explicitX to missing value
	set explicitY to missing value
	if posArg contains "," then
		set AppleScript's text item delimiters to ","
		set posParts to text items of posArg
		set AppleScript's text item delimiters to ""
		if (count of posParts) = 2 then
			set explicitX to (item 1 of posParts) as integer
			set explicitY to (item 2 of posParts) as integer
		end if
	end if

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	set fileRef to (POSIX file filePath) as alias

	tell application "Keynote"
		open fileRef
		set theDoc to front document
		set sw to width of theDoc
		set sh to height of theDoc

		set margin to 80

		if posArg is "bottom-right" then
			set posX to sw - boxWidth - margin
			set posY to sh - boxHeight - margin
		else if posArg is "bottom-left" then
			set posX to margin
			set posY to sh - boxHeight - margin
		else if posArg is "top-right" then
			set posX to sw - boxWidth - margin
			set posY to margin
		else if posArg is "top-left" then
			set posX to margin
			set posY to margin
		else if posArg is "center" then
			set posX to (sw - boxWidth) / 2
			set posY to (sh - boxHeight) / 2
		else if explicitX is not missing value then
			set posX to explicitX
			set posY to explicitY
		else
			error "Invalid position. Use bottom-right/bottom-left/top-right/top-left/center or 'x,y'."
		end if

		-- Tested creation pattern: inside the slide's tell block, with `height` in the
		-- creation properties. Style is applied to `object text` afterward.
		tell slide slideNum of theDoc
			set newItem to make new text item with properties {object text:boxText, position:{posX, posY}, width:boxWidth, height:boxHeight}
			if theFont is not missing value then set font of object text of newItem to theFont
			set size of object text of newItem to theSize
		end tell

		save theDoc
		if closeAfter then close theDoc
	end tell

	return "Added text box on slide " & slideNum & " at " & posArg & " (" & lineCount & " line(s))"
end run

-- Replace every occurrence of `find` in `src` with `repl`. Kept outside any Keynote tell block.
on replaceText(src, findStr, repl)
	set AppleScript's text item delimiters to findStr
	set parts to text items of src
	set AppleScript's text item delimiters to repl
	set out to parts as text
	set AppleScript's text item delimiters to ""
	return out
end replaceText
