from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_usage_endpoint():
    response = client.get("/usage")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "TacticTrail"
    assert "keyword" in data["available_search_methods"]
    assert "bm25" in data["available_search_methods"]
    assert "semantic" in data["available_search_methods"]