
def test_valid_keyword(client, technique_data):
    response = client.get("/api/techniques/search?keyword=phishing")
    assert response.status_code == 200
    assert response.json()["total_matches"] == 1


def test_empty_keyword(client, technique_data):
    response = client.get("/api/techniques/search?keyword=")
    assert response.status_code == 400


def test_unknown_keyword(client, technique_data):
    response = client.get("/api/techniques/search?keyword=xyznonexistent")
    assert response.status_code == 200
    assert response.json()["results"] == []



def test_keyword_search_ranking(client, technique_data, monkeypatch, tmp_path):
    import json

    from app import technique_search

    test_data = [
        {
            "technique_id": "T1000",
            "name": "Command Execution",
            "description": "Attackers may use phishing emails.",
            "url": "https://attack.mitre.org/techniques/T1000"
        },
        {
            "technique_id": "T2000",
            "name": "Phishing",
            "description": "Attackers use phishing emails.",
            "url": "https://attack.mitre.org/techniques/T2000"
        }
    ]

    test_file = tmp_path / "ranking_test.json"
    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    monkeypatch.setattr(technique_search, "DATA_FILE", test_file)

    response = client.get("/api/techniques/search?keyword=phishing")

    assert response.status_code == 200

    results = response.json()["results"]

    assert len(results) == 2
    assert results[0]["technique_id"] == "T2000"
    assert results[0]["relevance_score"] == 12

    assert results[1]["technique_id"] == "T1000"
    assert results[1]["relevance_score"] == 2
