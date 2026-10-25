import importlib
import logging
import sys

import app as app_module
import config


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


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db.example.test")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_NAME", "TESTDB")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/test/db")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")

    cfg = importlib.reload(config)
    assert cfg.DB_HOST == "db.example.test"
    assert cfg.DB_PORT == 5433
    assert cfg.DB_NAME == "TESTDB"
    assert cfg.DB_USER == "test_user"
    assert cfg.DB_PASSWORD_SECRET_NAME == "dts/test/db"
    assert cfg.LOG_LEVEL == "DEBUG"
    assert cfg.PORT == 9090

    monkeypatch.undo()
    importlib.reload(config)


def test_db_dsn_resolves_secret_by_name(monkeypatch):
    calls = []
    monkeypatch.setattr(
        app_module,
        "get_db_password",
        lambda name: calls.append(name) or "fake-placeholder-password",
    )
    dsn = app_module.db_dsn(
        {
            "DB_USER": "test_user",
            "DB_HOST": "db.example.test",
            "DB_PORT": 1433,
            "DB_NAME": "TESTDB",
            "DB_PASSWORD_SECRET_NAME": "dts/it-asset-inventory/db",
        }
    )

    assert calls == ["dts/it-asset-inventory/db"]
    assert "fake-placeholder-password" in dsn


def test_logs_to_stdout():
    app = app_module.create_app({"TESTING": True})
    assert all(isinstance(handler, logging.StreamHandler) for handler in app.logger.handlers)
    assert all(handler.stream is sys.stdout for handler in app.logger.handlers)
