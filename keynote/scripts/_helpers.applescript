-- _helpers.applescript
-- Shared helpers for the keynote skill scripts.
-- Loaded by each script via:
--   set helpers to load script POSIX file ((do shell script "dirname " & quoted form of (POSIX path of (path to me))) & "/_helpers.applescript")
--
-- Exported handlers:
--   resolvePath(p)        — turn a relative or absolute path into a fully-resolved absolute path
--   parseCloseFlag(argv)  — true if argv contains "--close"
--   saveIfOpen(filePath)  — if Keynote has the deck open, save it (commits user's unsaved edits)
--   backupDeck(filePath)  — copy the deck to <deck-dir>/.keynote-skill/backups/<name>.<timestamp>.key

on resolvePath(p)
	return do shell script "cd \"$(dirname " & quoted form of p & ")\" && echo \"$(pwd)/$(basename " & quoted form of p & ")\""
end resolvePath

on parseCloseFlag(argv)
	repeat with a in argv
		if (contents of a) is "--close" then return true
	end repeat
	return false
end parseCloseFlag

on saveIfOpen(filePath)
	tell application "Keynote"
		if not running then return
		repeat with d in documents
			try
				if (POSIX path of (file of d as alias)) is filePath then
					save d
					return
				end if
			end try
		end repeat
	end tell
end saveIfOpen

on backupDeck(filePath)
	-- Copy the deck to .keynote-skill/backups/<name>.<timestamp>.key, then
	-- prune older backups for this deck so only the 3 most recent remain.
	do shell script "
deckPath=" & quoted form of filePath & "
deckDir=$(dirname \"$deckPath\")
deckName=$(basename \"$deckPath\" .key)
backupDir=\"$deckDir/.keynote-skill/backups\"
mkdir -p \"$backupDir\"
ts=$(date +%Y%m%d-%H%M%S)
if [ -e \"$deckPath\" ]; then
  cp -R \"$deckPath\" \"$backupDir/${deckName}.${ts}.key\"
  cd \"$backupDir\" && ls -1t \"${deckName}\".*.key 2>/dev/null | tail -n +4 | while read f; do rm -rf \"$f\"; done
fi
"
end backupDeck
