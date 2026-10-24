import pytest
from fastapi.testclient import TestClient

from app import main


client = TestClient(main.app)


@pytest.fixture
def set_checks(monkeypatch: pytest.MonkeyPatch):
    def _set(postgres: bool, redis: bool) -> None:
        monkeypatch.setattr(main, "check_postgres", lambda: postgres)
        monkeypatch.setattr(main, "check_redis", lambda: redis)

    return _set


def test_ready_when_all_dependencies_are_up(set_checks) -> None:
    set_checks(postgres=True, redis=True)
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"ready": True, "checks": {"postgres": True, "redis": True}}


@pytest.mark.parametrize(("postgres", "redis"), [(False, True), (True, False), (False, False)])
def test_ready_returns_503_when_a_dependency_is_down(set_checks, postgres: bool, redis: bool) -> None:
    set_checks(postgres=postgres, redis=redis)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"ready": False, "checks": {"postgres": postgres, "redis": redis}}


def test_postgres_dsn_uses_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "6543")
    monkeypatch.setenv("POSTGRES_DB", "lab")
    monkeypatch.setenv("POSTGRES_USER", "app")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")
    assert main.postgres_dsn() == "postgresql://app:secret@db:6543/lab"
