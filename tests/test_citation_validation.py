
from app.ingestion.citation_validation import (
    find_unverified_citations,
)


def test_detects_unverified_document_page():
    sources = [
        {
            "document": "NIST.SP.800-61r3.pdf",
            "page": 17,
        }
    ]

    answer = (
        "NIST recommends incident response planning "
        "[NIST.SP.800-61r3.pdf, page 17]. "
        "It also discusses another topic "
        "[NIST.SP.800-61r3.pdf, page 99]."
    )

    result = find_unverified_citations(answer, sources)

    assert result == [
        "[NIST.SP.800-61r3.pdf, page 99]"
    ]


def test_allows_verified_document_citations():
    sources = [
        {
            "document": "NIST.SP.800-61r3.pdf",
            "page": 17,
        }
    ]

    answer = (
        "Incident response requires planning "
        "[NIST.SP.800-61r3.pdf, page 17]."
    )

    result = find_unverified_citations(answer, sources)

    assert result == []
