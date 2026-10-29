
import json

from app import technique_search


def test_bm25_search_success(client, tmp_path, monkeypatch):
    # Create a small dataset with several techniques.
    techniques = [
        {
            "technique_id": "T1566.001",
            "name": "Spearphishing Attachment",
            "description": "Phishing using a malicious attachment",
            "url": "https://attack.mitre.org/techniques/T1566/001/",
        },
        {
            "technique_id": "T1000",
            "name": "Network Discovery",
            "description": "Attackers inspect network devices",
            "url": "https://example.com/network",
        },
        {
            "technique_id": "T2000",
            "name": "Command Execution",
            "description": "Attackers execute system commands",
            "url": "https://example.com/command",
        },
        {
            "technique_id": "T3000",
            "name": "File Collection",
            "description": "Attackers collect local files",
            "url": "https://example.com/files",
        },
    ]

    file_path = tmp_path / "bm25_techniques.json"
    file_path.write_text(
        json.dumps(techniques),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        technique_search,
        "DATA_FILE",
        file_path,
    )

    response = client.get(
        "/api/techniques/bm25",
        params={"query": "phishing attachment"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "phishing attachment"
    assert data["total_matches"] >= 1
    assert data["results"][0]["technique_id"] == "T1566.001"
    assert data["results"][0]["bm25_score"] > 0


def test_bm25_search_empty_query(client, technique_data):
    response = client.get(
        "/api/techniques/bm25",
        params={"query": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty"


def test_bm25_search_no_match(client, technique_data):
    response = client.get(
        "/api/techniques/bm25",
        params={"query": "xyzunknownterm"},
    )

    assert response.status_code == 200
    assert response.json()["total_matches"] == 0
    assert response.json()["results"] == []
