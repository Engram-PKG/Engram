# Project Structure

One line per file. Update this alongside any change that adds, removes, or
repurposes a file — treat it as part of the diff, not an afterthought.

## Root

| File | What it is |
|---|---|
| `README.md` | Setup instructions and project overview — start here |
| `ARCHITECTURE.md` | System design, data flow, connector rollout phasing, deployment options |
| `CONTRIBUTING.md` | Branch strategy, commit style, coding standards, the safety-critical confirm-before-action rule |
| `PROJECT_STRUCTURE.md` | This file |
| `docker-compose.yml` | Orchestrates the `db`, `redis`, `backend`, `worker`, and `frontend` containers |
| `env.example` | Template for the real `.env` — copy it, never commit the real one |
| `.gitignore` | Excludes `.env`, caches, venvs, and DB volume data from git |
| `.env` | Real secrets/config — gitignored, not committed |

## `backend/`

| File | What it is |
|---|---|
| `Dockerfile` | Multi-stage build — build tools only in the builder stage, slim non-root runtime image |
| `.dockerignore` | Excludes tests/caches/venvs from the built image |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Adds pytest/ruff/mypy/httpx on top of `requirements.txt` |
| `pyproject.toml` | ruff/mypy/pytest configuration |
| `alembic.ini` | Alembic migration-runner config |
| `alembic/env.py` | Wires Alembic to the app's `Settings` and SQLAlchemy metadata |
| `alembic/script.py.mako` | Template new migrations are generated from |
| `alembic/versions/c61825e56a8d_init.py` | Initial migration — creates `users` and `memory_items` tables |
| `alembic/versions/.gitkeep` | Keeps the otherwise-empty `versions/` folder tracked by git |

### `backend/app/`

| File | What it is |
|---|---|
| `main.py` | FastAPI entrypoint — CORS setup, mounts the `/api/v1` router |
| `core/config.py` | `Settings` — env vars for DB/Redis URLs, secrets, OAuth client IDs, CORS origins |
| `db/base.py` | SQLAlchemy declarative `Base` |
| `db/session.py` | Async engine/session factory + the `get_db()` FastAPI dependency |
| `models/user.py` | `User` table (id, email, hashed password) |
| `models/memory_item.py` | `MemoryItem` table — the core ingested-content model; includes the pgvector embedding column |
| `schemas/user.py` | Pydantic request/response shapes for `User` |
| `api/v1/router.py` | Aggregates every endpoint router under `/api/v1` |
| `api/v1/endpoints/health.py` | `GET /health` — liveness check |
| `api/v1/endpoints/auth.py` | Signup/login (stub — real logic lands Sprint 2) |
| `api/v1/endpoints/connectors.py` | Connector list/connect/disconnect (stub — Sprints 2-6) |
| `api/v1/endpoints/memory.py` | Memory search/listing (stub — Sprints 7-8) |
| `api/v1/endpoints/chat.py` | Chat + agentic actions (stub — Sprints 9 and 11) |
| `api/v1/endpoints/graph.py` | Knowledge graph data (stub — Sprint 10) |
| `workers/celery_app.py` | Celery app wired to Redis, plus a `ping` smoke-test task |
| every other `__init__.py` | Empty — just marks its folder as a Python package |

### `backend/tests/`

| File | What it is |
|---|---|
| `test_health.py` | Confirms `GET /api/v1/health` returns `200 {"status": "ok"}` |

## `frontend/`

Static HTML/CSS/JS. All "AI" behavior below is currently mocked with hardcoded
data — see `ARCHITECTURE.md` and the sprint roadmap for when each page gets
wired to the real backend.

| File | What it is |
|---|---|
| `index.html` | Public marketing/landing page |
| `login.html` / `signup.html` | Auth forms (mocked until Sprint 2) |
| `connectors.html` | Connect-your-sources onboarding step + connector management |
| `building.html` | Simulated "twin is being built" onboarding screen |
| `dashboard.html` | Logged-in home — stats, recent activity, latest reflection |
| `chat.html` | Conversation with the twin (canned replies until Sprint 9) |
| `timeline.html` | Chronological feed of indexed memories |
| `graph.html` | Knowledge graph visualization (hardcoded demo dataset until Sprint 10) |
| `search.html` | Memory search (mocked until Sprint 8) |
| `reflection.html` | AI-surfaced pattern insights |
| `settings.html` | Profile / privacy / notifications / twin-behavior / danger-zone tabs |
| `css/style.css` | Global tokens, marketing sections, auth forms |
| `css/dashboard.css` | App-shell layout — sidebar rail, topbar, cards |
| `css/chat.css` | Chat-specific layout |
| `css/connector.css` | Connector card grid + permission-consent modal |
| `css/animation.css` | Keyframes — ambient particles, twin-thread, progress ring |
| `css/responsive.css` | Breakpoints |
| `js/app.js` | `DT` module — page interactivity/state (forms, filters, mocked chat/search/settings logic) |
| `js/animation.js` | `DTAnim` module — canvas/SVG decorative animation (twin-thread, ambient field, graph render) |
| `assets/icons/`, `assets/images/`, `assets/videos/` | Empty — scaffolding for assets not yet added; icons are currently inline SVG/emoji |
