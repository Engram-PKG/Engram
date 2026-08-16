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
```

## Running locally

Create a `.env` file in the project root (not committed) with the variables
below, then start the stack:

```
docker compose up --build
```

Variables read by `docker-compose.yml` and `backend/app/core/config.py`:

```
POSTGRES_USER=digitaltwin
POSTGRES_PASSWORD=changeme
POSTGRES_DB=digitaltwin
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@db:5432/<POSTGRES_DB>
REDIS_URL=redis://redis:6379/0
BACKEND_PORT=8000
FRONTEND_PORT=8080

SECRET_KEY=generate-a-real-secret
ANTHROPIC_API_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
SLACK_CLIENT_ID=
SLACK_CLIENT_SECRET=
NOTION_CLIENT_ID=
NOTION_CLIENT_SECRET=
```

All fields except `DATABASE_URL`/`REDIS_URL`/`SECRET_KEY` have safe defaults
or are optional — fill in only what you need (e.g. `ANTHROPIC_API_KEY` for
LLM calls, OAuth client id/secret pairs per connector you're building).

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
