"""Convert a markdown proposal to a branded PDF.

Usage: uv run python md-to-pdf.py /absolute/path/to/outline.md
Output: PDF created in the same directory with the same base name.

Note: Replace logo-square.png with your own logo and update the alt text below.
"""

import sys
import os
import re
import markdown
from markdown.extensions.toc import TocExtension
from weasyprint import HTML

# Resolve asset paths relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_CSS = os.path.join(SCRIPT_DIR, "style.css")
LOGO_PNG = os.path.join(SCRIPT_DIR, "logo-square.png")


def preprocess_markdown(md_content):
    """Ensure blank lines before list items that follow non-list lines.

    Standard markdown requires a blank line before the first list item
    when it follows a non-list line (e.g. a bold header). Without this,
    the parser treats the list as continuation of the paragraph.
    """
    lines = md_content.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i > 0 and re.match(r'\s*[-*]\s', line):
            prev = lines[i - 1]
            # Insert blank line if previous line is non-empty and not itself a list item
            if prev.strip() and not re.match(r'\s*[-*]\s', prev) and not re.match(r'\s*\d+\.\s', prev) and prev.strip() != '':
                result.append('')
        result.append(line)
    return '\n'.join(result)


def convert_md_to_pdf(md_file_path):
    """Convert a markdown file to a branded PDF."""
    # Derive output path
    base, _ = os.path.splitext(md_file_path)
    pdf_file_path = base + ".pdf"

    # Read markdown
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    md_content = preprocess_markdown(md_content)

    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=["extra", "smarty", TocExtension(permalink=True)],
    )

    # Highlight TBD in red
    html_content = html_content.replace("TBD", '<span class="tbd">TBD</span>')

    # Use file:// URI for the logo so weasyprint can resolve it
    logo_uri = f"file://{LOGO_PNG}"

    # Inject running elements for header/footer logos
    header_logo = f'''<div class="header-logo-element">
  <img src="{logo_uri}" alt="Logo">
</div>'''

    footer_logo = f'''<div class="footer-logo-element">
  <img src="{logo_uri}" alt="Logo">
</div>'''

    html_with_body = f"<body>{header_logo}{footer_logo}{html_content}</body>"

    # Use the script directory as base URL for resolving style assets
    base_url = f"file://{SCRIPT_DIR}/"

    HTML(string=html_with_body, base_url=base_url).write_pdf(
        pdf_file_path, stylesheets=[STYLE_CSS]
    )

    print(f"PDF created: {pdf_file_path}")
    return pdf_file_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python md-to-pdf.py <path-to-markdown-file>")
        sys.exit(1)

    md_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(md_path):
        print(f"Error: file not found: {md_path}")
        sys.exit(1)

    convert_md_to_pdf(md_path)
