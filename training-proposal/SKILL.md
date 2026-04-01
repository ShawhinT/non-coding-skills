---
name: training-proposal
description: Draft AI training proposals and outlines from unstructured notes, convert markdown proposals to branded PDF, read existing .pdf proposals for reference. Covers client proposals, training outlines, workshop syllabi, bootcamp outlines, course proposals, session agendas, curriculum design, pricing quotes, and scoping.
---

# Training Proposal Skill

Draft, edit, and convert training proposals for consulting clients.

## Workflow

1. **Gather info** from the user (or unstructured notes)
2. **Draft markdown** following the example proposal structure
3. **User reviews/edits** the markdown
4. **Convert to PDF** using your preferred pipeline (see Converting to PDF section)

## Reading Existing Proposals

When the user wants to reference a past proposal:

- **PDF files**: Use a PDF text extraction tool to read the content
- **.pages files**: Most past proposals have a PDF version alongside the .pages file. Use the PDF version.

## Updating an Existing Proposal

When the user wants to revise a draft, read the existing markdown, make targeted changes, and re-save. Don't regenerate from scratch.

## Drafting a Proposal

Gather these details from the user (ask for anything missing):

- **Client name**
- **Training title**
- **Number of sessions** and **duration per session**
- **Delivery method** (e.g., Microsoft Teams, Zoom, in-person)
- **Topics per session** (or general themes to flesh out)
- **Pricing** — define your standard rates (e.g., a rate for prepared content like lectures and webinars, and a lower rate for no-prep sessions like workshops and office hours). Calculate each session price as `duration_hours × hourly_rate`. Ask the user which rate tier applies to each session.
- **Discount** — When a discount applies, list sessions at full standard-rate prices and add a discount row in green: `| <span style="color: #2E7D32">*Discount*</span> | | <span style="color: #2E7D32">*-$X*</span> |`. The Total row reflects the discounted price.
- **Dates** (or TBD)

**Structure:** Engagements can be multiple sessions or a single session with multiple parts (using `### Part 1:`, `### Part 2:`). The syllabus Duration field should reflect this (e.g., "1 session (3.5 hours total)" or "4 sessions (90 min each)").

> **Note:** Add your own reference examples to a `references/` directory to guide the formatting and structure of proposals.

Save to a consistent location for your client files (e.g., `clients/<client>/ai-training-outline_<client>.md`).

Tell the user to review the markdown before PDF generation.

## Converting to PDF

After the user approves the markdown, convert it using your preferred markdown-to-PDF tool. Options include:

- A custom Python script using libraries like `weasyprint` or `pdfkit`
- Pandoc with a LaTeX template
- A VS Code extension like "Markdown PDF"

> **Note:** If you want branded PDFs, you'll need to set up your own conversion pipeline with your logo and styles.

## Formatting Notes

These conventions ensure consistent, professional-looking proposals:

- Syllabus uses HTML `<table class="syllabus">` with `<tr class="spacer">` to separate title/instructor from dates/logistics (not a markdown table)
- Use `TBD` for unknown dates/times — consider highlighting these in the PDF
- Each session's timed segments should add up to the session duration
- Session content uses: `- **Section** *(15 min)*` with nested bullets for subtopics
- Use `---` horizontal rules between sessions
- Use `<div class="page-break"></div>` before the Investment section to force a page break
- Inline HTML like `<span style="color: #2E7D32">` works inside markdown table cells for colored text (e.g., discount rows)
- Investment table goes at the end with a bold **Total** row
- Prepared-by line format: `*Prepared on <date> by [Your Name]*` (italicized, includes date)
- Payment terms go after the Investment table as a `### Payment terms` subsection with bold bullet labels
