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


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_db_dsn_resolves_secret_by_name(fake_secret):
    from app import db_dsn

    cfg = {
        "DB_USER": "u",
        "DB_HOST": "h",
        "DB_PORT": 1433,
        "DB_NAME": "n",
        "DB_PASSWORD_SECRET_NAME": "dts/badge-access/db",
    }
    assert db_dsn(cfg) == "mssql://u:fake-test-password@h:1433/n"
    assert fake_secret == ["dts/badge-access/db"]
