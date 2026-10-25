import importlib

import pytest

import app as app_module
import config

FAKE_PASSWORD = "fake-test-password"


@pytest.fixture
def reload_config(monkeypatch):
    yield lambda: importlib.reload(config)
    monkeypatch.undo()
    importlib.reload(config)


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_config_from_env(monkeypatch, reload_config):
    monkeypatch.setenv("DB_HOST", "db.example.test")
    monkeypatch.setenv("DB_PORT", "15433")
    monkeypatch.setenv("DB_NAME", "desks")
    monkeypatch.setenv("DB_USER", "desk_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/test/db")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")
    cfg = reload_config()
    assert cfg.DB_HOST == "db.example.test"
    assert cfg.DB_PORT == 15433
    assert cfg.DB_NAME == "desks"
    assert cfg.DB_USER == "desk_user"
    assert cfg.DB_PASSWORD_SECRET_NAME == "dts/test/db"
    assert cfg.LOG_LEVEL == "DEBUG"
    assert cfg.PORT == 9090


def test_config_defaults(monkeypatch, reload_config):
    for name in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD_SECRET_NAME", "LOG_LEVEL", "PORT"):
        monkeypatch.delenv(name, raising=False)
    cfg = reload_config()
    assert cfg.DB_HOST == ""
    assert cfg.DB_USER == ""
    assert cfg.DB_PASSWORD_SECRET_NAME == "dts/desk-booking/db"
    assert cfg.LOG_LEVEL == "INFO"
    assert cfg.PORT == 8080
    assert not hasattr(cfg, "DB_PASSWORD")


def test_db_dsn_resolves_secret_by_name(monkeypatch):
    seen = []

    def fake_lookup(name):
        seen.append(name)
        return FAKE_PASSWORD

    monkeypatch.setattr(app_module, "get_db_password", fake_lookup)
    dsn = app_module.db_dsn(
        {
            "DB_USER": "u",
            "DB_PASSWORD_SECRET_NAME": "dts/desk-booking/db",
            "DB_HOST": "h",
            "DB_PORT": 1433,
            "DB_NAME": "n",
        }
    )
    assert seen == ["dts/desk-booking/db"]
    assert dsn == "mssql://u:" + FAKE_PASSWORD + "@h:1433/n"


def test_create_app_does_not_resolve_secret(monkeypatch):
    def fail(name):
        raise AssertionError("secret lookup must be lazy")

    monkeypatch.setattr(app_module, "get_db_password", fail)
    client = app_module.create_app({"TESTING": True}).test_client()
    assert client.get("/healthz").status_code == 200
