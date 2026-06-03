-- insert-image.applescript
-- Usage: osascript insert-image.applescript "<deck-path>" <slide-number> "<image-path>" "<position>" [width] [--close]
-- Inserts an image onto a slide.
--
-- <position>: bottom-right, bottom-left, top-right, top-left, center, or "x,y" (canvas is 1920x1080).
-- [width] optional, default 500. Height auto-scales.
--
-- IMPORTANT: width is passed as a creation property. Setting it after creation has been observed to corrupt the .key file.

on run argv
	if (count of argv) < 4 then
		error "Usage: osascript insert-image.applescript <deck-path> <slide-number> <image-path> <position> [width] [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set slideNum to (item 2 of argv) as integer
	set imagePath to helpers's resolvePath(item 3 of argv)
	set posArg to item 4 of argv

	set imgWidth to 500
	if (count of argv) ≥ 5 then
		try
			set imgWidth to (item 5 of argv) as integer
		end try
	end if

	set closeAfter to helpers's parseCloseFlag(argv)

	-- Parse explicit "x,y" outside the Keynote tell block (where `text items` would shadow).
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
	set imgRef to POSIX file imagePath

	tell application "Keynote"
		open fileRef
		set theDoc to front document
		set sw to width of theDoc
		set sh to height of theDoc

		set margin to 80
		set approxH to imgWidth * 0.5

		if posArg is "bottom-right" then
			set posX to sw - imgWidth - margin
			set posY to sh - approxH - margin
		else if posArg is "bottom-left" then
			set posX to margin
			set posY to sh - approxH - margin
		else if posArg is "top-right" then
			set posX to sw - imgWidth - margin
			set posY to margin
		else if posArg is "top-left" then
			set posX to margin
			set posY to margin
		else if posArg is "center" then
			set posX to (sw - imgWidth) / 2
			set posY to (sh - approxH) / 2
		else if explicitX is not missing value then
			set posX to explicitX
			set posY to explicitY
		else
			error "Invalid position. Use bottom-right/bottom-left/top-right/top-left/center or 'x,y'."
		end if

		tell slide slideNum of theDoc
			make new image with properties {file:imgRef, position:{posX, posY}, width:imgWidth}
		end tell

		save theDoc
		if closeAfter then close theDoc
	end tell

	return "Inserted image on slide " & slideNum & " at " & posArg
end run
