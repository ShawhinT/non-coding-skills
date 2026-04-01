# Non-Coding Skills

Claude Code skills for personal (non-coding) workflows.

Resources
- [How I Automated My Work with Claude Code](https://youtu.be/XLilQNKy7mk)
- [How to Automate Anything with Claude]

## How to Use

These are personal skills built for my specific workflows. Using them as-is probably won't be as helpful to you as they are to me. However, the value is in the patterns and ideas. 

Two ways I'd recommend using this repo:
1. **Browse for inspiration** — Read through the skills to see what's possible. If you're new to skills, this is a good way to understand the kinds of non-coding workflows you can automate with Claude.
2. **Use as a starting point** — If a skill here is close to something you need, give it to Claude as a starting point and have it adapt the skill to your unique workflow.

## Skills

| Skill | Description | Surface | Dependencies |
|-------|-------------|---------|--------------|
| **linkedin-post-writer** | Draft LinkedIn posts in a consistent writing style | Any | None |
| **validate-saas-idea** | Validate startup or product ideas through systematic market research | Any | Web search |
| **skill-updater** | Update and repackage existing skills on Claude.ai | Claude.ai | None |
| **email-writer** | Draft emails in a consistent voice and style | Any | Gmail MCP |
| **3-way-intro** | Draft three-way email introductions between leads and consultants | Any | Gmail MCP |
| **executive-briefing** | Generate a daily briefing by pulling tasks from Notion databases | Any | Notion MCP |
| **notion-research-documentation** | Search Notion, synthesize findings, and create research documentation | Any | Notion MCP |
| **business-strategy** | Strategic thinking partner for business decisions | Any | Notion MCP, web search |
| **crm** | Read, update, and manage a CRM in Notion; cross-reference Gmail for activity | Any | Notion MCP, Gmail MCP |
| **outreach-campaign** | Set up and manage outreach campaigns, track contacts and responses | Any | Notion MCP, Gmail MCP |
| **pre-call-research** | Research prospects before sales calls | Any | Notion MCP, Gmail MCP, web search |
| **training-proposal** | Draft training proposals and outlines from unstructured notes | Claude Code | Python, PDF tooling |
| **linkedin-lead-gatherer** | Gather leads from LinkedIn via browser automation | Claude Code | Chrome tool |
| **keynote** | Read, create, and modify Apple Keynote presentations | Claude Code | macOS, Keynote app |



## Install

The simplest option is to just paste a skill's GitHub URL into any Claude conversation. Since this is a public repo, Claude can fetch the content and adapt it for you (no installation needed).

```
https://github.com/ShawhinT/non-coding-skills/tree/main/3-way-intro
```

If you're using Claude Code and want a skill installed permanently:

```bash
# From GitHub
claude skill add https://github.com/ShawhinT/non-coding-skills/tree/main/3-way-intro

# Or clone and add locally
git clone https://github.com/ShawhinT/non-coding-skills.git
claude skill add /path/to/non-coding-skills/3-way-intro
```
