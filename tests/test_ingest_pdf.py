from scripts import ingest_pdf


def test_ingest_pdf_pipeline(monkeypatch, tmp_path):
    pdf_path = tmp_path / "security.pdf"

    pages = [
        {
            "document": "security.pdf",
            "page": 1,
            "heading": "Credential Access",
            "text": "Brute force attacks",
        }
    ]

    monkeypatch.setattr(
        ingest_pdf,
        "extract_pdf_pages",
        lambda path: pages,
    )

    monkeypatch.setattr(
        ingest_pdf,
        "chunk_pages",
        lambda data, chunk_size, overlap: data,
    )

    monkeypatch.setattr(
        ingest_pdf,
        "embed_chunks",
        lambda chunks: chunks,
    )

    monkeypatch.setattr(
        ingest_pdf,
        "save_document_chunks",
        lambda chunks: len(chunks),
    )

    result = ingest_pdf.ingest_pdf(pdf_path)

    assert result == 1
