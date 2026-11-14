
from fastapi.testclient import TestClient

from app import main as main_module

client = TestClient(main_module.app)


def test_ask_returns_document_citations(monkeypatch):
    results = [
        {
            "document": "NIST.SP.800-61r3.pdf",
            "page": 12,
            "heading": "Incident Response",
            "chunk_id": 25,
            "text": "Incident response involves preparation.",
            "similarity_score": 0.85,
        }
    ]

    monkeypatch.setattr(
        main_module,
        "search_documents",
        lambda question, top_k: results,
    )

    monkeypatch.setattr(
        main_module,
        "generate_answer",
        lambda question, evidence: (
    "Incident response requires preparation "
    "[NIST.SP.800-61r3.pdf, page 12]."
),
    )

    response = client.post(
        "/ask",
        json={"question": "Explain incident response"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "preparation" in data["answer"]
    assert data["citations"] == [
        "[NIST.SP.800-61r3.pdf, page 12]"
    ]
    assert data["sources"][0]["page"] == 12


def test_ask_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 400

def test_ask_blocks_unverified_citation(monkeypatch):
    results = [
        {
            "document": "NIST.SP.800-61r3.pdf",
            "page": 12,
            "heading": "Incident Response",
            "chunk_id": 25,
            "text": "Incident response involves preparation.",
            "similarity_score": 0.85,
        }
    ]

    monkeypatch.setattr(
        main_module,
        "search_documents",
        lambda question, top_k: results,
    )

    monkeypatch.setattr(
        main_module,
        "generate_answer",
        lambda question, evidence: (
            "NIST recommends preparation "
            "[NIST.SP.800-61r3.pdf, page 99]."
        ),
    )

    response = client.post(
        "/ask",
        json={"question": "Explain incident response"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "could not produce" in data["answer"]
    assert "page 99" not in data["answer"]
    assert data["citations"] == [
        "[NIST.SP.800-61r3.pdf, page 12]"
    ]

def test_ask_blocks_answer_without_citations(monkeypatch):
    results = [
        {
            "document": "NIST.SP.800-61r3.pdf",
            "page": 17,
            "heading": "Incident Response",
            "chunk_id": 52,
            "text": "Organizations should document incident response procedures.",
            "similarity_score": 0.78,
        }
    ]

    monkeypatch.setattr(
        main_module,
        "search_documents",
        lambda question, top_k: results,
    )

    # Simulate Gemini forgetting to include citations
    monkeypatch.setattr(
        main_module,
        "generate_answer",
        lambda question, evidence: (
            "Organizations should document incident response procedures."
        ),
    )

    response = client.post(
        "/ask",
        json={"question": "Explain incident response procedures"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "could not produce" in data["answer"]
    assert data["citations"] == [
        "[NIST.SP.800-61r3.pdf, page 17]"
    ]
