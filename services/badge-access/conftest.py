import pytest

import app as app_module
from app import create_app


@pytest.fixture(autouse=True)
def fake_secret(monkeypatch):
    calls = []

    def fake_get_db_password(secret_name):
        calls.append(secret_name)
        return "fake-test-password"

    monkeypatch.setattr(app_module, "get_db_password", fake_get_db_password)
    return calls


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    return app.test_client()
