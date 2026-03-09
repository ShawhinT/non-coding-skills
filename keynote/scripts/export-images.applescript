-- export-images.applescript
-- Usage: osascript export-images.applescript "/path/to/file.key" "/path/to/output-dir"
-- Exports all slides as PNG images

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript export-images.applescript <keynote-file-path> <output-directory>"
	end if

	set filePath to item 1 of argv
	set outputDir to item 2 of argv

	-- Resolve to absolute path
	set filePath to do shell script "cd \"$(dirname " & quoted form of filePath & ")\" && echo \"$(pwd)/$(basename " & quoted form of filePath & ")\""

	-- Create output directory if it doesn't exist
	do shell script "mkdir -p " & quoted form of outputDir

	set fileRef to POSIX file filePath
	set outputFolder to POSIX file outputDir

	tell application "Keynote"
		set wasRunning to running

		open fileRef

		set theDocument to front document
		set docName to name of theDocument

		-- Export as images
		export theDocument to file outputFolder as slide images with properties {image format:PNG, skipped slides:false}

		set slideCount to count of slides of theDocument

		close theDocument saving no

		if not wasRunning then
			quit
		end if
	end tell

	-- List exported files
	set fileList to do shell script "ls -1 " & quoted form of outputDir & "/*.png 2>/dev/null || echo '(no files found)'"

	return "Exported " & slideCount & " slides from " & docName & " to " & outputDir & linefeed & fileList
end run
