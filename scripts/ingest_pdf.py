
import argparse
from pathlib import Path

from app.ingestion.chunker import chunk_pages
from app.ingestion.document_store import save_document_chunks
from app.ingestion.embedder import embed_chunks
from app.ingestion.pdf_parser import extract_pdf_pages


def ingest_pdf(pdf_path: Path) -> int:
    """Process a PDF and store its embeddings in PostgreSQL."""

    # Step 1: Extract PDF pages
    pages = extract_pdf_pages(pdf_path)

    if not pages:
        raise ValueError("PDF contains no extractable text")

    # Step 2: Split pages into chunks
    chunks = chunk_pages(
        pages,
        chunk_size=800,
        overlap=100,
    )

    # Step 3: Generate ONNX embeddings
    embedded_chunks = embed_chunks(chunks)

    # Step 4: Save chunks to PostgreSQL
    saved_count = save_document_chunks(embedded_chunks)

    return saved_count


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a PDF into TacticTrail"
    )

    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to a PDF document",
    )

    args = parser.parse_args()

    count = ingest_pdf(args.pdf_path)

    print(f"Successfully saved {count} chunks")
    print(f"Document: {args.pdf_path.name}")


if __name__ == "__main__":
    main()
