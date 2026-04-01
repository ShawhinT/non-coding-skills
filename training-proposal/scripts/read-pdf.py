"""Extract text from a PDF file and print to stdout.

Usage: uv run python read-pdf.py /absolute/path/to/proposal.pdf
"""

import sys
import os

from pypdf import PdfReader


def extract_text(pdf_path):
    """Extract and print all text from a PDF."""
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            if i > 0:
                print(f"\n--- Page {i + 1} ---\n")
            print(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python read-pdf.py <path-to-pdf-file>")
        sys.exit(1)

    pdf_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(pdf_path):
        print(f"Error: file not found: {pdf_path}")
        sys.exit(1)

    extract_text(pdf_path)
