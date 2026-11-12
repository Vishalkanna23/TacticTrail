
from fastapi.testclient import TestClient

from app import main as main_module

client = TestClient(main_module.app)


def test_pgvector_search(monkeypatch):
    def mock_search(query, top_k):
        assert query == "stealing passwords"
        assert top_k == 5

        return [
            {
                "technique_id": "T1110",
                "name": "Brute Force",
                "description": "Password guessing",
                "url": "https://attack.mitre.org/techniques/T1110/",
                "similarity_score": 0.85,
            }
        ]

    monkeypatch.setattr(main_module, "search_pgvector", mock_search)

    response = client.get(
        "/api/techniques/pgvector",
        params={"query": "stealing passwords"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_matches"] == 1
    assert data["results"][0]["technique_id"] == "T1110"


def test_pgvector_empty_query():
    response = client.get(
        "/api/techniques/pgvector",
        params={"query": "   "},
    )

    assert response.status_code == 400
