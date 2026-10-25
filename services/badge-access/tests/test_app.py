def test_list_badges(client):
    resp = client.get("/badges")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/badges/B-1001")
    assert resp.status_code == 200
    assert resp.get_json()["badge_id"] == "B-1001"


def test_missing_returns_404(client):
    assert client.get("/badges/does-not-exist").status_code == 404
