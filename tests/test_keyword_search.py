
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
