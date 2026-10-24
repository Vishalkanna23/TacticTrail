
import json

import pytest

from app import technique_search


@pytest.fixture
def technique_data(tmp_path, monkeypatch):
    # Create a small temporary dataset for testing
    data = [
        {
            "technique_id": "T1566.001",
            "name": "Spearphishing Attachment",
            "tactics": ["Initial Access"],
            "description": "Phishing using a malicious attachment",
            "url": "https://attack.mitre.org/techniques/T1566/001",
        }
    ]

    file_path = tmp_path / "techniques.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    # Make the search function use our test dataset
    monkeypatch.setattr(technique_search, "DATA_FILE", file_path)


def test_valid_technique(client, technique_data):
    response = client.get("/api/techniques/T1566.001")

    assert response.status_code == 200
    assert response.json()["technique_id"] == "T1566.001"
    assert response.json()["name"] == "Spearphishing Attachment"


def test_invalid_technique(client, technique_data):
    response = client.get("/api/techniques/T9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Technique ID not found"


def test_missing_dataset(client, tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(technique_search, "DATA_FILE", missing_file)

    response = client.get("/api/techniques/T1566.001")

    assert response.status_code == 503
