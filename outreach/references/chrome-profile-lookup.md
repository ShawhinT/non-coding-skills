# Chrome Profile Lookup

Use this when you need to look up the current employer for individual LinkedIn profiles (1–9 contacts, or as a cleanup pass after bulk WebSearch enrichment).

## Prerequisites

Chrome must be connected. Always verify first:

```
1. ToolSearch: "select:mcp__claude-in-chrome__tabs_context_mcp"
2. Call: mcp__claude-in-chrome__tabs_context_mcp (createIfEmpty: true)
   → Must return a tabId, not a "not connected" error
```

If not connected: tell the user to open Chrome, ensure the Claude extension is running, and confirm they're logged into claude.ai with the same account.

## Step-by-Step

### 1. Load required tools
```
ToolSearch: "select:mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text"
```

### 2. For each profile

**Navigate:**
```
mcp__claude-in-chrome__navigate
  url: https://www.linkedin.com/in/[linkedin_slug]
  tabId: [tab_id]
```

**Read:**
```
mcp__claude-in-chrome__get_page_text
  tabId: [tab_id]
```

### 3. Parse the employer

The employer appears in the first ~5 lines of page text, immediately after the person's name and title. Pattern:

```
[Full Name]
[Title]
[Company Name] · [School or other org]
[Location]
```

Example:
```
[Full Name]
Sr. Manager, Cyber Analytics Platform
[Company Name] · [School]
Dallas-Fort Worth Metroplex
```
→ employer = **[Company Name]**

### 4. Look up company size

Once you have the employer name, search:
```
"[Company Name] number of employees"
```

Map the result to a size range per `company-size-ranges.md`.

## Processing Multiple Profiles

Process sequentially — one navigate → get_page_text cycle per profile, reusing the same tab. Do not open multiple tabs.

## Edge Cases

- **No employer shown**: Profile may be private, person is between jobs, or freelance. Mark company as `Unknown` or `Self-Employed` with size `1-50`.
- **LinkedIn login wall**: User needs to be logged in to Chrome. If you see a login page instead of a profile, stop and tell the user.
- **Profile redirects**: Some slugs redirect (e.g., old URL). The final URL in the tab context will show where you landed — confirm it matches.
