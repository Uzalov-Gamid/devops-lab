import os
from typing import Any

import psycopg
from fastapi import FastAPI, Response, status
from redis import Redis


app = FastAPI(title="DevOps Lab API", version="0.1.0")


def postgres_dsn() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "devops_lab")
    user = os.getenv("POSTGRES_USER", "devops")
    password = os.getenv("POSTGRES_PASSWORD", "devops")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def check_postgres() -> bool:
    try:
        with psycopg.connect(postgres_dsn(), connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select 1")
                cursor.fetchone()
        return True
    except Exception:
        return False


def check_redis() -> bool:
    try:
        client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), socket_connect_timeout=2)
        return bool(client.ping())
    except Exception:
        return False


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "devops-lab", "status": "running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response) -> dict[str, Any]:
    checks = {
        "postgres": check_postgres(),
        "redis": check_redis(),
    }
    is_ready = all(checks.values())
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"ready": is_ready, "checks": checks}

