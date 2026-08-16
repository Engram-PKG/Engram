# Personal Digital Twin

An AI that answers questions from your own data — email, chat, notes, docs,
calendar — instead of general knowledge, and can act on your behalf (e.g.
send an email) with your confirmation first.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design and
[CONTRIBUTING.md](CONTRIBUTING.md) for coding standards and branch strategy.

## Project layout

```
frontend/    static HTML/CSS/JS app (served by nginx in docker-compose)
backend/     FastAPI app, Alembic migrations, Celery worker
docker-compose.yml
env.example  copy to .env and fill in before running
```

## Running locally

```
cp env.example .env      # fill in ANTHROPIC_API_KEY etc. as needed
docker compose up --build
```

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000 (docs at http://localhost:8000/docs)
- Backend health check: http://localhost:8000/api/v1/health

## Backend without Docker

```
cd backend
python -m venv .venv && .venv\Scripts\activate   # or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Requires a reachable Postgres (with the `pgvector` extension) and Redis —
either run `docker compose up db redis`, or point `DATABASE_URL`/`REDIS_URL`
at your own instances.

## Status

Foundation/scaffolding stage: project structure, Docker setup, and the API
skeleton are in place. Connectors, real auth, retrieval, and chat are not
implemented yet — endpoints return `501 Not Implemented` as placeholders.
See `ARCHITECTURE.md` for the phased build-out plan.
