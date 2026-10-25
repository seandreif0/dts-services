def test_list_expenses(client):
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/expenses/EX-5501")
    assert resp.status_code == 200
    assert resp.get_json()["claim_id"] == "EX-5501"


def test_missing_returns_404(client):
    assert client.get("/expenses/does-not-exist").status_code == 404
