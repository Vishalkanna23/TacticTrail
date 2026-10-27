
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_invalid_technique():
    response = client.get(
        "/api/techniques/T999999/explain"
    )

    assert response.status_code == 404

def test_valid_technique(monkeypatch):

    def fake_generate_answer(question, evidence):
        return "This is a test explanation."

    monkeypatch.setattr(
        "app.main.generate_answer",
        fake_generate_answer
    )

    response = client.get(
        "/api/techniques/T1566.001/explain"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["technique_id"] == "T1566.001"
    assert data["answer"] == "This is a test explanation."
    assert "attack.mitre.org" in data["source"]

