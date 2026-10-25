import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "LOG_FILE": str(tmp_path / "visitor-register.log")})
    return app.test_client()
