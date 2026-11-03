
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_semantic_search_success(monkeypatch):
    def fake_search(query):
        return [
            {
                "technique_id": "T1110",
                "name": "Brute Force",
                "url": "https://attack.mitre.org/techniques/T1110/",
                "similarity_score": 0.85,
            }
        ]

    monkeypatch.setattr(
        "app.main.search_semantic",
        fake_search,
    )

    response = client.get(
        "/api/techniques/semantic",
        params={"query": "steal passwords"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "steal passwords"
    assert data["total_matches"] == 1
    assert data["results"][0]["technique_id"] == "T1110"


def test_semantic_search_empty_query():
    response = client.get(
        "/api/techniques/semantic",
        params={"query": "   "},
    )

    assert response.status_code == 400
