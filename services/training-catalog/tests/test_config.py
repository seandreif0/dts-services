import importlib

import pytest

import app as app_module
import config


@pytest.fixture
def reload_config_after_monkeypatch(monkeypatch):
    yield
    monkeypatch.undo()
    importlib.reload(config)


def test_config_reads_environment(monkeypatch, reload_config_after_monkeypatch):
    monkeypatch.setenv("DB_HOST", "db.example.internal")
    monkeypatch.setenv("DB_PORT", "1444")
    monkeypatch.setenv("DB_NAME", "TESTDB")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/test/db")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")

    importlib.reload(config)

    assert config.DB_HOST == "db.example.internal"
    assert config.DB_PORT == 1444
    assert config.DB_NAME == "TESTDB"
    assert config.DB_USER == "test_user"
    assert config.DB_PASSWORD_SECRET_NAME == "dts/test/db"
    assert config.LOG_LEVEL == "DEBUG"
    assert config.PORT == 9090


def test_config_defaults(monkeypatch, reload_config_after_monkeypatch):
    for name in (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD_SECRET_NAME",
        "LOG_LEVEL",
        "PORT",
    ):
        monkeypatch.delenv(name, raising=False)

    importlib.reload(config)

    assert config.PORT == 8080
    assert config.LOG_LEVEL == "INFO"
    assert config.DB_PASSWORD_SECRET_NAME == "dts/training-catalog/db"
    assert config.DB_HOST == ""
    assert not hasattr(config, "DB_PASSWORD")


def test_db_dsn_uses_secret_lookup(secret_lookups):
    cfg = {
        "DB_HOST": "db.example.internal",
        "DB_PORT": 1444,
        "DB_NAME": "TESTDB",
        "DB_USER": "test_user",
        "DB_PASSWORD_SECRET_NAME": "dts/test/db",
    }

    dsn = app_module.db_dsn(cfg)

    assert secret_lookups == ["dts/test/db"]
    assert "fake-password-for-tests" in dsn
