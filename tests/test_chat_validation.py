
from fastapi.testclient import TestClient

from app import main as main_module

client = TestClient(main_module.app)


def test_chat_blocks_unverified_ids(monkeypatch):
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

    monkeypatch.setattr(
        main_module,
        "generate_answer",
        lambda question, evidence: (
            "Attackers use T1110, T1003 and T1078."
        ),
    )

    response = client.post(
        "/chat",
        json={"question": "How do attackers steal passwords?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "could not verify" in data["answer"]
    assert "T1003" not in data["answer"]
    assert "T1078" not in data["answer"]
    assert data["sources"][0]["technique_id"] == "T1110"


def test_chat_allows_verified_ids(monkeypatch):
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

    monkeypatch.setattr(
        main_module,
        "generate_answer",
        lambda question, evidence: "T1110 is Brute Force.",
    )

    response = client.post(
        "/chat",
        json={"question": "Explain brute force"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "T1110 is Brute Force."
