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
    monkeypatch.setenv("DB_NAME", "TESTDB")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/visitor-register/test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")
    try:
        cfg = importlib.reload(config)
        assert cfg.DB_HOST == "db.example.test"
        assert cfg.DB_PORT == 5555
        assert cfg.DB_NAME == "TESTDB"
        assert cfg.DB_USER == "test_user"
        assert cfg.DB_PASSWORD_SECRET_NAME == "dts/visitor-register/test"
        assert cfg.LOG_LEVEL == "DEBUG"
        assert cfg.PORT == 9090
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_config_defaults(monkeypatch):
    for name in ("DB_PASSWORD_SECRET_NAME", "LOG_LEVEL", "PORT"):
        monkeypatch.delenv(name, raising=False)
    try:
        cfg = importlib.reload(config)
        assert cfg.DB_PASSWORD_SECRET_NAME == "dts/visitor-register/db"
        assert cfg.LOG_LEVEL == "INFO"
        assert cfg.PORT == 8080
        assert not hasattr(cfg, "DB_PASSWORD")
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_db_dsn_resolves_secret_by_name(monkeypatch):
    seen = {}

    def fake_lookup(secret_name):
        seen["name"] = secret_name
        return "fake-placeholder"

    monkeypatch.setattr(app_module, "get_db_password", fake_lookup)
    dsn = app_module.db_dsn(
        {
            "DB_USER": "u",
            "DB_HOST": "h",
            "DB_PORT": 1433,
            "DB_NAME": "n",
            "DB_PASSWORD_SECRET_NAME": "dts/visitor-register/db",
        }
    )
    assert seen["name"] == "dts/visitor-register/db"
    assert dsn == "mssql://u:fake-placeholder@h:1433/n"
