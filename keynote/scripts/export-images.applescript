-- export-images.applescript
-- Usage: osascript export-images.applescript "/path/to/file.key" "/path/to/output-dir" [--all-stages] [--close]
-- Exports all slides as PNG images. --all-stages emits one PNG per build stage
-- (each animation step), e.g. to rebuild a slide track synced to a talk recording.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript export-images.applescript <keynote-file-path> <output-directory> [--all-stages] [--close]"
	end if

	set helpers to load script (POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.scpt"))

	set filePath to helpers's resolvePath(item 1 of argv)
	set outputDir to item 2 of argv
	set closeAfter to helpers's parseCloseFlag(argv)
	set allStages to (argv contains "--all-stages")
	helpers's saveIfOpen(filePath)

	do shell script "mkdir -p " & quoted form of outputDir

	set fileRef to POSIX file filePath
	set outputFolder to POSIX file outputDir

	tell application "Keynote"
		set wasRunning to running

		set theDocument to helpers's docForPath(filePath)
		set docName to name of theDocument

		export theDocument to file outputFolder as slide images with properties {image format:PNG, skipped slides:false, all stages:allStages}

		set slideCount to count of slides of theDocument

		if closeAfter then
			close theDocument saving no
			if not wasRunning then quit
		end if
	end tell

	set fileList to do shell script "ls -1 " & quoted form of outputDir & "/*.png 2>/dev/null || echo '(no files found)'"

	return "Exported " & slideCount & " slides from " & docName & " to " & outputDir & linefeed & fileList
end run
