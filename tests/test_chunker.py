
import pytest

from app.ingestion.chunker import chunk_pages


def test_chunker_preserves_document_and_page():
    pages = [
        {
            "document": "security.pdf",
            "page": 5,
            "text": "ABCDEFGHIJ",
        }
    ]

    chunks = chunk_pages(pages, chunk_size=6, overlap=2)

    assert len(chunks) == 2
    assert chunks[0]["text"] == "ABCDEF"
    assert chunks[1]["text"] == "EFGHIJ"
    assert chunks[0]["document"] == "security.pdf"
    assert chunks[1]["page"] == 5


def test_chunker_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_pages(
            [{"document": "test.pdf", "page": 1, "text": "abc"}],
            chunk_size=5,
            overlap=5,
        )
