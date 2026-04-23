# Non-Coding Skills

Agent skills for (non-coding) business workflows.

Resources
- [How I Automated My Work with Claude Code](https://youtu.be/XLilQNKy7mk)
- [How to Automate Anything with Claude (4-Step Framework)](https://youtu.be/FSOvLgS4xvc)
- [How I Taught Claude To Edit My YouTube Videos](https://youtu.be/wmIO2rs-AIs)

> **Want help building (AI) skills for your team?** [AI Builder Academy](https://aibuilder.academy/) helps small teams do big things with AI.

## How to Use

These are personal skills built for my specific workflows. Using them as-is probably won't be as helpful to you as they are to me. However, the value is in the patterns and ideas. 

Two ways I'd recommend using this repo:
1. **Browse for inspiration** — Read through the skills to see what's possible. If you're new to skills, this is a good way to understand the kinds of non-coding workflows you can automate with Claude.
2. **Use as a starting point** — If a skill here is close to something you need, give it to Claude as a starting point and have it adapt the skill to your unique workflow.

## Skills

| Skill | Description | Surface | Dependencies |
|-------|-------------|---------|--------------|
| **conversion-copy** | Draft/sharpen conversion copy (landing pages, DMs, sales emails) via Harry Dry's 3-question filter | Any | None |
| **four-rs-framework** | Advisor for Results/Re-up/Referrals/Reviews decisions on client engagements | Any | None |
| **linkedin-post-writer** | Draft LinkedIn posts in a consistent writing style | Any | None |
| **sales-letter-writer** | Draft long-form sales letters and one-pagers using Hormozi's $100M Offers principles | Any | None |
| **validate-saas-idea** | Validate startup or product ideas through systematic market research | Any | Web search |
| **workshop-use-case-researcher** | Research practical use cases for custom AI workshops and training proposals | Any | Web search |
| **email-writer** | Draft emails in a consistent voice and style (including three-way intros, follow-ups, etc.) | Any | Gmail MCP |
| **executive-briefing** | Generate a daily briefing by pulling tasks from Notion databases | Any | Notion MCP |
| **notion-helper** | Create ad hoc tasks, follow-ups, and reminders across Notion databases | Any | Notion MCP |
| **notion-research-documentation** | Search Notion, synthesize findings, and create research documentation | Any | Notion MCP |
| **sop-helper** | Create, update, and reference standard operating procedures in Notion | Any | Notion MCP |
| **business-strategy** | Strategic thinking partner for business decisions | Any | Notion MCP, web search |
| **crm** | Read, update, and manage a CRM in Notion; cross-reference Gmail for activity | Any | Notion MCP, Gmail MCP |
| **outreach-campaign** | Set up and manage outreach campaigns, track contacts and responses | Any | Notion MCP, Gmail MCP |
| **pre-call-research** | Research prospects before sales calls | Any | Notion MCP, Gmail MCP, web search |
| **skill-updater** | Update and repackage existing skills on Claude.ai | Claude.ai or Desktop | None |
| **linkedin-lead-gatherer** | Gather leads from LinkedIn via browser automation | Claude Code or Cowork | Chrome tool |
| **linkedin-post-analytics** | Pull and analyze LinkedIn post performance from the creator analytics dashboard | Claude Code or Cowork | Chrome tool |
| **keynote** | Read, create, and modify Apple Keynote presentations | Claude Code or Cowork | macOS, Keynote app |
| **training-proposal** | Draft training proposals and outlines from unstructured notes | Claude Code or Cowork | Python, PDF tooling |
| **video-editor** | Analyze raw recordings, propose cuts, and generate FCPXML for Final Cut Pro | Claude Code or Cowork | Python, ffmpeg, AssemblyAI API |



## Install

The simplest option is to just paste a skill's GitHub URL into any Claude/AI conversation. Since this is a public repo, Claude can fetch the content and adapt it for you (no installation needed).

```
https://github.com/ShawhinT/non-coding-skills/tree/main/email-writer
```

If you're using Claude Code and want a skill installed permanently:

```bash
# From GitHub
claude skill add https://github.com/ShawhinT/non-coding-skills/tree/main/email-writer

# Or clone and add locally
git clone https://github.com/ShawhinT/non-coding-skills.git
claude skill add /path/to/non-coding-skills/email-writer
```
