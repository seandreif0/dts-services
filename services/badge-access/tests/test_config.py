import importlib

import config


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db.example.internal")
    monkeypatch.setenv("DB_PORT", "5555")
    monkeypatch.setenv("DB_NAME", "BADGE_TEST")
    monkeypatch.setenv("DB_USER", "svc_user")
    monkeypatch.setenv("DB_PASSWORD_SECRET_NAME", "dts/badge-access/test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9090")
    try:
        importlib.reload(config)
        assert config.DB_HOST == "db.example.internal"
        assert config.DB_PORT == 5555
        assert config.DB_NAME == "BADGE_TEST"
        assert config.DB_USER == "svc_user"
        assert config.DB_PASSWORD_SECRET_NAME == "dts/badge-access/test"
        assert config.LOG_LEVEL == "DEBUG"
        assert config.PORT == 9090
        assert not hasattr(config, "DB_PASSWORD")
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_config_defaults(monkeypatch):
    for name in ("DB_HOST", "DB_USER", "DB_PASSWORD_SECRET_NAME", "LOG_LEVEL", "PORT"):
        monkeypatch.delenv(name, raising=False)
    try:
        importlib.reload(config)
        assert config.DB_HOST == ""
        assert config.DB_USER == ""
        assert config.DB_PASSWORD_SECRET_NAME == "dts/badge-access/db"
        assert config.LOG_LEVEL == "INFO"
        assert config.PORT == 8080
    finally:
        monkeypatch.undo()
        importlib.reload(config)
