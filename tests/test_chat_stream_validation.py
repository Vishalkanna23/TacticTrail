
from fastapi.testclient import TestClient

from app import main as main_module

client = TestClient(main_module.app)


def test_chat_stream_blocks_unverified_ids(monkeypatch):
    techniques = [
        {
            "technique_id": "T1110",
            "name": "Brute Force",
            "description": "Password guessing attacks.",
            "url": "https://attack.mitre.org/techniques/T1110/",
        }
    ]

    # Mock semantic search
    monkeypatch.setattr(
        main_module,
        "search_semantic",
        lambda question, top_k: techniques,
    )

    # Mock Gemini streaming
    def fake_stream(question, evidence):
        yield "Attackers use T1110 and T10"
        yield "78 to gain access."

    monkeypatch.setattr(
        main_module,
        "stream_answer",
        fake_stream,
    )

    # Call the real FastAPI endpoint
    response = client.post(
        "/chat/stream",
        json={"question": "Explain password attacks"},
    )

    assert response.status_code == 200

    answer = response.text

    assert "T1110" in answer
    assert "T1078" not in answer
    assert "unsupported MITRE" in answer


def test_chat_stream_allows_verified_ids(monkeypatch):
    techniques = [
        {
            "technique_id": "T1110",
            "name": "Brute Force",
            "description": "Password guessing attacks.",
            "url": "https://attack.mitre.org/techniques/T1110/",
        }
    ]

    monkeypatch.setattr(
        main_module,
        "search_semantic",
        lambda question, top_k: techniques,
    )

    def fake_stream(question, evidence):
        yield "T1110 is "
        yield "a brute force technique."

    monkeypatch.setattr(
        main_module,
        "stream_answer",
        fake_stream,
    )

    response = client.post(
        "/chat/stream",
        json={"question": "Explain brute force"},
    )

    assert response.status_code == 200
    assert response.text == "T1110 is a brute force technique."

