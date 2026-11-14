
from pathlib import Path

import pymupdf


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """Extract PDF pages with text, headings and page numbers."""

    pdf_path = Path(pdf_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    pages = []
    current_heading = None

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            blocks = page.get_text("dict")["blocks"]

            text_parts = []
            candidates = []

            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    spans = line["spans"]

                    line_text = "".join(
                        span["text"] for span in spans
                    ).strip()

                    if not line_text:
                        continue

                    text_parts.append(line_text)

                    # Identify possible headings using font sizes
                    max_font_size = max(
                        span["size"] for span in spans
                    )

                    candidates.append(
                        (max_font_size, line_text)
                    )

            if not text_parts:
                continue

            # The largest text is a heading candidate
            if candidates:
                largest_size = max(
                    size for size, _ in candidates
                )

                for size, text in candidates:
                    if (
                        size == largest_size
                        and len(text) <= 100
                    ):
                        current_heading = text
                        break

            pages.append(
                {
                    "document": pdf_path.name,
                    "page": page_number,
                    "heading": current_heading,
                    "text": "\n".join(text_parts),
                }
            )

    return pages
