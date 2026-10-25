def test_list_courses(client):
    resp = client.get("/courses")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 3


def test_get_one(client):
    resp = client.get("/courses/TR-101")
    assert resp.status_code == 200
    assert resp.get_json()["course_id"] == "TR-101"


def test_missing_returns_404(client):
    assert client.get("/courses/does-not-exist").status_code == 404
