def test_list_desks(client):
    resp = client.get("/desks")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/desks/HQ-4-012")
    assert resp.status_code == 200
    assert resp.get_json()["desk_id"] == "HQ-4-012"


def test_missing_returns_404(client):
    assert client.get("/desks/does-not-exist").status_code == 404
