import importlib

import app as app_module
import config


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db.example.test")
    monkeypatch.setenv("DB_PORT", "5555")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/expense-lookup/test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")
    try:
        cfg = importlib.reload(config)
        assert cfg.DB_HOST == "db.example.test"
        assert cfg.DB_PORT == 5555
        assert cfg.DB_NAME == "testdb"
        assert cfg.DB_USER == "test_user"
        assert cfg.DB_PASSWORD_SECRET_NAME == "dts/expense-lookup/test"
        assert cfg.LOG_LEVEL == "DEBUG"
        assert cfg.PORT == 9090
        assert not hasattr(cfg, "DB_PASSWORD")
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_db_dsn_resolves_secret_by_name(monkeypatch):
    calls = []

    def fake_get_secret(name, region=None):
        calls.append(name)
        return "fake-placeholder"

    monkeypatch.setattr(app_module.secret_store, "get_secret", fake_get_secret)
    cfg = {
        "DB_USER": "u",
        "DB_HOST": "h",
        "DB_PORT": 1433,
        "DB_NAME": "n",
        "DB_PASSWORD_SECRET_NAME": "dts/expense-lookup/db",
    }
    assert app_module.db_dsn(cfg) == "mssql://u:fake-placeholder@h:1433/n"
    assert calls == ["dts/expense-lookup/db"]
