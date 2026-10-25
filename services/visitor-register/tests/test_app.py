def test_list_visitors(client):
    resp = client.get("/visitors")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/visitors/V-3001")
    assert resp.status_code == 200
    assert resp.get_json()["visit_id"] == "V-3001"


def test_missing_returns_404(client):
    assert client.get("/visitors/does-not-exist").status_code == 404
