import pytest

import app as app_module


@pytest.fixture(autouse=True)
def secret_lookups(monkeypatch):
    calls = []

    def fake_get_db_password(secret_name):
        calls.append(secret_name)
        return "fake-password-for-tests"

    monkeypatch.setattr(app_module, "get_db_password", fake_get_db_password)
    return calls


@pytest.fixture
def client():
    app = app_module.create_app({"TESTING": True})
    return app.test_client()
