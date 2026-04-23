---
name: workshop-use-case-researcher
description: >
  Research and brainstorm practical use case ideas for custom AI workshops and training proposals.
  Use this skill whenever Shaw is preparing a workshop, training session, or proposal for a client
  and needs to identify relevant use cases for a specific audience. Triggers include: "brainstorm
  use cases", "what use cases should I cover", "help me prep the workshop for [company]",
  "I need use case ideas for [role/audience]", "research topics for the training", "what should
  I demo", or any reference to building out a custom workshop or training proposal. Also trigger
  when Shaw mentions a specific client engagement where the deliverable is a training session,
  workshop, or enablement program. Even casual mentions like "what should I teach them" or
  "I need to figure out the use cases for this one" should trigger this skill.
---

# Workshop Use Case Researcher

Shaw delivers custom AI workshops for organizations. Each engagement has a different audience
(role, seniority, industry), different tools (M365 Copilot, Claude, ChatGPT, etc.), and different
adoption maturity. This skill helps research and brainstorm practical, demo-able use cases
tailored to that specific context.

The goal: produce a tight shortlist of use case ideas — each grounded in a real business problem,
backed by reference links, and scoped to what's actually possible with the client's tool stack.

---

## Phase 1: Gather Context

Before any research, assemble everything known about this engagement. The quality of use cases
depends entirely on how well you understand the audience's daily work, pain points, and tools.

### Step 1: Check Notion for existing context

Look for the client in the ABA Calls database (page ID: `[database-id]`).
If a call record exists, fetch it — the call notes typically contain:
- What the audience does day-to-day
- Current tool access and adoption level
- What they can't do today that they should be doing
- Stated goals and pain points
- Any specific use case directions already discussed

Also check the Active Leads database via the CRM skill if relevant — there may be email threads
or pipeline context that adds detail.

### Step 2: Identify gaps and ask Shaw

After reviewing available context, assess what you still need to know. The essential context for
good use case research is:

- **Company & industry** — What does the company do? What sector? What's unique about their work?
- **Audience role** — What is the specific job function? (e.g., "product managers in cell therapy R&D" is much better than "employees")
- **Daily workflows** — What does this audience actually spend their time on? What are the 5-6 recurring tasks that eat their week?
- **Tool stack** — What AI tools do they have access to? What's the specific product/version?
- **Adoption maturity** — Are they brand new, dabbling, or already using AI daily? What have they tried so far?
- **Pain points** — What's frustrating, slow, or manual about their current work?
- **Goals** — What does the client or their leadership want to get out of this?
- **Session format** — How long is the session? How many use cases needed? Is it demo-heavy or discussion-heavy?

If any of these are unclear from the Notion context, ask Shaw directly. He often has additional
insights about where to research — specific platforms, communities, or content sources that are
especially relevant for this particular audience. Ask for these explicitly:

> "Before I start researching, are there any specific sources you think would be especially
> relevant for this audience? For example, specific communities, YouTube channels, learning
> platforms, industry publications, or people who cover this role?"

Present a brief research plan before kicking off. Shaw should approve or adjust before you
spend tokens on broad searches.

---

## Phase 2: Research

### Research plan structure

Based on the context gathered, design a research plan with 2-4 parallel threads. The specific
threads depend on the engagement — don't default to a fixed set. Instead, choose threads based
on what will yield the most relevant results for this audience and tool stack.

Common thread types (pick what's relevant, not all of them):

- **Role-specific AI adoption** — How are people in this role actually using AI today? Search
  for practitioner content: courses, talks, blog posts, newsletters by people in this role
  sharing their workflows. Shaw may point you to specific sources (e.g., Maven for PMs,
  specific YouTube channels for engineers, industry Slack communities).

- **Tool capabilities audit** — What can the client's specific tool stack actually do today?
  Go to the official documentation and recent feature announcements. Don't rely on general
  knowledge — tools change fast. Search for the tool name + recent features/capabilities.

- **Industry/domain context** — What's unique about this company's industry that shapes how
  the audience works? For regulated industries (biotech, finance, healthcare), there are
  specific constraints and workflows that generic AI use cases won't address.

- **Broad web / practitioner stories** — Search for real examples of people in similar roles
  using AI. Look for blog posts, podcast episodes, newsletter issues, and articles that
  describe specific workflows, not just tool lists.

### Depth over breadth

A common failure mode is shallow research — running a few web searches and skimming the
snippets without actually reading the content. To avoid this:

- When a search result looks promising, use `web_fetch` to read the actual page. Snippets
  are often too compressed to extract real workflow details.
- For tool capability research, go to the official docs and recent release blogs. Don't rely
  on third-party summaries which may be outdated or wrong.
- For practitioner content (courses, talks, podcasts), read the description, syllabus, or
  transcript to understand what specific workflows they're teaching — not just the title.
- Aim for at least 3-4 web_fetch calls per research thread to get real depth.

### What to extract from research

For each source, look for:
- **Specific workflows** — not "AI helps with research" but "upload 50 interview transcripts
  and get a themed synthesis in 30 minutes"
- **Time savings claims** — concrete before/after numbers that make the business case vivid
- **Tool-specific features** — which exact tool or feature enables the workflow
- **Relevance to this audience** — does this map to something the client's audience actually does?

---

## Phase 3: Synthesize

### Cross-reference research with context

Map what you found in research against the audience's actual daily work:
- Which use cases address a stated pain point?
- Which use cases are possible with the client's tool stack today?
- Which use cases will land with the audience's adoption maturity? (Don't propose agent
  architectures to people who haven't used chat yet.)

### Rank by these criteria

1. **Business problem clarity** — Can you articulate the specific daily pain this solves in
   one sentence that the audience would nod at?
2. **Tool feasibility** — Is this actually doable with their specific tools today?
3. **Demo-ability** — Can Shaw show this live in 10-15 minutes?
4. **Wow-to-effort ratio** — Does this feel impressive relative to how simple it is to do?
5. **Complexity ramp** — The final set should progress from simple to complex.

---

## Phase 4: Output

### First pass: Tight shortlist

Present 5 use case ideas in this exact format:

```
**1. [3-Word Label]** — [One sentence describing what the audience does with the tool to solve a specific problem.]
- [Link title (Source)](URL)
- [Link title (Source)](URL)
- [Link title (Source)](URL)
```

No descriptions on the links. No extra commentary between items. Keep it scannable.

Shaw will pick the top 3 (or however many he needs). Only then expand.

### Second pass: Expanded use cases (on request)

When Shaw picks his top choices, expand each one with:
- **The business problem** — 2-3 sentences grounding it in the audience's specific daily work
- **Prerequisites** — What needs to be true for this demo to work (licenses, data, files)
- **Demo steps** — Numbered list, as few steps as possible (aim for 4-5), each one an
  action Shaw performs live

Order the final set from simplest to most complex so the workshop narrative ramps up.

---

## Failure modes to watch for

- **Shallow research** — Skimming search snippets instead of fetching and reading actual pages.
  Fix: use web_fetch on promising results. Read the actual content.
- **Feature-first thinking** — Describing what the tool does instead of what problem it solves.
  Fix: always lead with the business problem. "Researcher agent" is not a use case. "Compress
  6 hours of competitive analysis into 30 minutes" is.
- **Overfitting to generic roles** — Proposing the same use cases you'd give any audience.
  Fix: ground every use case in something specific to this company, industry, or role.
- **Ignoring adoption maturity** — Proposing advanced workflows to beginners, or basic
  features to power users. Fix: calibrate to where the audience actually is.
- **Skipping the context phase** — Jumping straight to research without understanding the
  audience. Fix: always do Phase 1 first. The 10 minutes spent gathering context saves
  hours of wasted research.
