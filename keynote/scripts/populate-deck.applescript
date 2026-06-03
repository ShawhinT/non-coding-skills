-- populate-deck.applescript
-- Usage: osascript populate-deck.applescript "/path/to/deck.key" "/path/to/slides.json" [--force] [--close]
-- Reads a JSON file, sets master layouts, and populates text fields.
-- Processes in batches of 5 slides (open/save/close) to avoid AppleEvent timeouts.
-- DESTRUCTIVE: refuses to run on a deck with >1 slide unless --force is passed.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript populate-deck.applescript <deck-path> <json-path> [--force] [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set jsonPath to helpers's resolvePath(item 2 of argv)
	set closeAfter to helpers's parseCloseFlag(argv)

	set forceMode to false
	repeat with a in argv
		if (contents of a) is "--force" then set forceMode to true
	end repeat

	helpers's saveIfOpen(filePath)
	helpers's backupDeck(filePath)

	-- Parse JSON
	set slideCountStr to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(len(data))\" " & quoted form of jsonPath
	set totalSlides to slideCountStr as integer
	if totalSlides < 1 then error "JSON file contains no slides."

	-- Destructive-action guardrail
	set fileRef to (POSIX file filePath) as alias
	tell application "Keynote"
		open fileRef
		set theDoc to front document
		set existingSlides to count of slides of theDoc
		close theDoc saving no
	end tell

	if existingSlides > 1 and not forceMode then
		error "Refusing to populate deck with " & existingSlides & " existing slides (would clobber edits). A backup was created. Re-run with --force to override, or use set-slide-text/add-slides to edit incrementally."
	end if

	-- Phase 1: Create all slides with correct masters
	set fileRef to (POSIX file filePath) as alias
	tell application "Keynote"
		with timeout of 300 seconds
			open fileRef
			set theDoc to front document

			set masterName1 to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[0].get('master','Title Only'))\" " & quoted form of jsonPath
			set base slide of slide 1 of theDoc to master slide masterName1 of theDoc

			if totalSlides > 1 then
				repeat with i from 2 to totalSlides
					set masterNameI to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & (i - 1) & "].get('master','Title Only'))\" " & quoted form of jsonPath
					make new slide at end of slides of theDoc with properties {base slide:master slide masterNameI of theDoc}
				end repeat
			end if

			save theDoc
			-- Always close between phases to release locks; phase 2 reopens.
			close theDoc
		end timeout
	end tell

	-- Phase 2: Populate text in batches of 5
	set batchSize to 5
	set batchStart to 1

	repeat while batchStart ≤ totalSlides
		set batchEnd to batchStart + batchSize - 1
		if batchEnd > totalSlides then set batchEnd to totalSlides

		set batchTitles to {}
		set batchSubtitles to {}
		set batchBodies to {}
		set batchAuthors to {}

		repeat with i from batchStart to batchEnd
			set idx to i - 1
			set end of batchTitles to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & idx & "].get('title',''), end='')\" " & quoted form of jsonPath
			set end of batchSubtitles to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & idx & "].get('subtitle',''), end='')\" " & quoted form of jsonPath
			set end of batchBodies to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & idx & "].get('body',''), end='')\" " & quoted form of jsonPath
			set end of batchAuthors to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & idx & "].get('author',''), end='')\" " & quoted form of jsonPath
		end repeat

		set fileRef to (POSIX file filePath) as alias
		tell application "Keynote"
			with timeout of 300 seconds
				open fileRef
				set theDoc to front document

				repeat with i from batchStart to batchEnd
					set batchIdx to i - batchStart + 1
					set titleField to item batchIdx of batchTitles
					set subtitleField to item batchIdx of batchSubtitles
					set bodyField to item batchIdx of batchBodies
					set authorField to item batchIdx of batchAuthors

					tell slide i of theDoc
						set itemCount to count of text items

						if itemCount ≥ 1 then
							set item1Pos to position of text item 1
							set item1Y to item 2 of item1Pos

							if item1Y > 900 then
								if titleField is not "" then set object text of text item 2 to titleField
								if subtitleField is not "" then set object text of text item 3 to subtitleField
								if authorField is not "" then set object text of text item 1 to authorField
							else if item1Y > 300 then
								if titleField is not "" then set object text of text item 1 to titleField
							else
								if titleField is not "" then set object text of text item 1 to titleField
								if subtitleField is not "" then set object text of text item 2 to subtitleField
								if bodyField is not "" then
									make new text item with properties {object text:bodyField, position:{72, 300}, width:1130, height:600}
								end if
							end if
						end if
					end tell
				end repeat

				save theDoc
				-- Close between batches to release locks; reopened next iteration.
				-- After the final batch, leave it open unless --close was passed.
				if batchEnd < totalSlides or closeAfter then close theDoc
			end timeout
		end tell

		set batchStart to batchEnd + 1
	end repeat

	return "Populated " & totalSlides & " slides from JSON."
end run
