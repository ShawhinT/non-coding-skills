-- populate-deck.applescript
-- Usage: osascript populate-deck.applescript "/path/to/.claude/keynote/deck.key" "/path/to/slides.json"
-- Reads a JSON file, creates slides with specified masters, populates text fields.
-- Processes in batches of 5 slides (open/save/close) to avoid AppleEvent timeouts.
-- Path MUST contain ".claude/keynote".
--
-- JSON format:
-- [
--   {"master": "Title", "title": "...", "subtitle": "...", "body": "", "author": "Your Name"},
--   {"master": "Title Only", "title": "...", "subtitle": "...", "body": "bullet 1\nbullet 2"},
--   {"master": "Section", "title": "Section Name"},
--   ...
-- ]
--
-- Notes:
-- - Slide 1 (the default slide) is reused for the first entry and set to the requested master.
-- - Additional slides are appended.
-- - For Title layout: "author" sets the footer (text item 1); "body" is ignored.
-- - For Title Only: "body" creates a freeform text box below the subtitle.
-- - For Section: only "title" is used (center text).
-- - For Blank: no text items are set.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript populate-deck.applescript <deck-path> <json-path>"
	end if

	set filePath to item 1 of argv
	set jsonPath to item 2 of argv

	-- Resolve deck path to absolute
	set filePath to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" && echo \"$(pwd)/$(basename " & quoted form of filePath & ")\""

	-- Safety check
	if filePath does not contain ".claude/keynote" then
		error "Output path must be within a .claude/keynote directory. Got: " & filePath
	end if

	-- Resolve JSON path to absolute
	set jsonPath to do shell script "cd \"$(dirname " & quoted form of jsonPath & ")\" && echo \"$(pwd)/$(basename " & quoted form of jsonPath & ")\""

	-- Parse JSON using shell (extract fields for each slide)
	set slideCountStr to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(len(data))\" " & quoted form of jsonPath
	set totalSlides to slideCountStr as integer

	if totalSlides < 1 then
		error "JSON file contains no slides."
	end if

	-- Phase 1: Create all slides with correct masters
	set fileRef to (POSIX file filePath) as alias
	tell application "Keynote"
		with timeout of 300 seconds
			open fileRef
			set theDoc to front document

			-- Set master for slide 1
			set masterName1 to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[0].get('master','Title Only'))\" " & quoted form of jsonPath
			set base slide of slide 1 of theDoc to master slide masterName1 of theDoc

			-- Create remaining slides
			if totalSlides > 1 then
				repeat with i from 2 to totalSlides
					set masterNameI to do shell script "python3 -c \"import json,sys; data=json.load(open(sys.argv[1])); print(data[" & (i - 1) & "].get('master','Title Only'))\" " & quoted form of jsonPath
					make new slide at end of slides of theDoc with properties {base slide:master slide masterNameI of theDoc}
				end repeat
			end if

			save theDoc
			close theDoc
		end timeout
	end tell

	-- Phase 2: Populate text in batches of 5
	set batchSize to 5
	set batchStart to 1

	repeat while batchStart ≤ totalSlides
		set batchEnd to batchStart + batchSize - 1
		if batchEnd > totalSlides then set batchEnd to totalSlides

		-- Pre-extract all field data for this batch (outside Keynote tell block)
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
								-- Title layout: item 1 = footer/author, item 2 = big title, item 3 = subtitle
								if titleField is not "" then
									set object text of text item 2 to titleField
								end if
								if subtitleField is not "" then
									set object text of text item 3 to subtitleField
								end if
								if authorField is not "" then
									set object text of text item 1 to authorField
								end if
							else if item1Y > 300 then
								-- Section layout: item 1 = center text
								if titleField is not "" then
									set object text of text item 1 to titleField
								end if
							else
								-- Title Only layout: item 1 = title, item 2 = subtitle
								if titleField is not "" then
									set object text of text item 1 to titleField
								end if
								if subtitleField is not "" then
									set object text of text item 2 to subtitleField
								end if
								if bodyField is not "" then
									-- No body placeholder — create a freeform text box
									make new text item with properties {object text:bodyField, position:{72, 300}, width:1130, height:600}
								end if
							end if
						end if
						-- itemCount = 0 means Blank layout — nothing to set
					end tell
				end repeat

				save theDoc
				close theDoc
			end timeout
		end tell

		set batchStart to batchEnd + 1
	end repeat

	return "Populated " & totalSlides & " slides from JSON."
end run
