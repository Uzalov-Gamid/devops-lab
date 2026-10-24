# DevOps Lab

Small infrastructure lab for a backend service. The project shows how to run a FastAPI app with PostgreSQL, Redis, nginx, health checks, Docker Compose, and GitHub Actions CI.

## Stack

- FastAPI + Uvicorn
- PostgreSQL 16
- Redis 7
- nginx reverse proxy
- Docker Compose
- pytest and GitHub Actions

## Architecture

```text
browser -> nginx:8080 -> api:8000
                    |-> PostgreSQL
                    |-> Redis
```

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open:

- API through nginx: http://localhost:8080
- Health endpoint: http://localhost:8080/health
- Readiness endpoint: http://localhost:8080/ready

## Local tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## What this MVP demonstrates

- Backend containerization
- Docker Compose service wiring
- App, database, cache, and reverse proxy separation
- Liveness (`/health`) and readiness (`/ready`) checks, both covered by tests
- Non-root runtime image without test dependencies
- CI pipeline for tests and a Docker image smoke test

