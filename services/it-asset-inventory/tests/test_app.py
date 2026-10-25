def test_list_assets(client):
    resp = client.get("/assets")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/assets/LT-88213")
    assert resp.status_code == 200
    assert resp.get_json()["asset_tag"] == "LT-88213"


def test_missing_returns_404(client):
    assert client.get("/assets/does-not-exist").status_code == 404
