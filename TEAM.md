# Team Roles & Sprint Plan

> **Project:** Engram — Personal Digital Twin
> **Team Lead:** Aditya
> **Team Members:** Yashi, Avinash
> **Goal:** Industry-ready, production-deployable product — not a college demo.

---

## Who Does What — Roles at a Glance

| Person | Official Role | One-Line Summary |
|---|---|---|
| **Aditya** | Team Lead · AI & Backend Engineer | Owns the intelligence layer — RAG pipeline, Claude integration, agentic actions, DevOps, and all final code review |
| **Yashi** | Backend & Data Engineer · Project Architect | Designed the entire project architecture from scratch; owns all connectors, the ingestion pipeline, database models, and background workers |
| **Avinash** | Frontend & UI Engineer | Owns the complete frontend — all pages, the design system, animations, and wiring every page to the live backend API |

> Each person's role is scoped so that in a job interview or portfolio review,
> they can speak in depth about a distinct, self-contained system — not just
> "I did some backend stuff."

---

## Detailed Role Descriptions

### Aditya — Team Lead · AI & Backend Engineer

**Responsibilities:**
- Final say on all architecture decisions and PR merges into `main`
- Sprint planning, backlog grooming, and milestone tracking
- Implements the entire **AI intelligence layer**:
  - Embedding pipeline (chunking, embedding calls, storing vectors in pgvector)
  - RAG retrieval logic — semantic + hybrid search, result ranking with citations
  - Claude integration — prompt engineering, response synthesis with source citations
  - Agentic action loop — tool definitions, Claude tool-use API, draft-and-confirm safety layer
  - Weekly reflection generation (scheduled Celery task)
- Owns **DevOps and production deployment**:
  - CI/CD pipeline (GitHub Actions)
  - Production Docker hardening, environment secrets management
  - Monitoring, structured JSON logging, health checks
  - Final production deployment to cloud (VPS or Fly.io/Render)
- **Code review** — reviews and approves all PRs from Yashi and Avinash before merge

**What Aditya can say in an interview:**
> "I led a 3-person team building a production AI product. I personally designed and implemented the full RAG pipeline — embedding chunks, storing vectors in pgvector, and building the retrieval logic that feeds Claude with cited context. I also built the agentic tool-use loop where the AI can draft emails or calendar events, but nothing executes on a live account without explicit user confirmation. I handled all DevOps — Docker, CI/CD with GitHub Actions, structured logging, and cloud deployment."

---

### Yashi — Backend & Data Engineer · Project Architect

**Responsibilities:**
- **Designed and built the entire project foundation** (Sprint 0) — Docker stack, FastAPI skeleton, all API endpoint stubs, database models with pgvector, Alembic migrations, and all project documentation (`README`, `ARCHITECTURE`, `CONTRIBUTING`, `PROJECT_STRUCTURE`)
- Owns **Authentication & User Management** end-to-end:
  - Real JWT-based login/signup
  - Secure password hashing (bcrypt)
  - Auth middleware protecting all private routes
  - Token refresh logic
- Owns the **Connector Framework** — the base OAuth flow and polling infrastructure all connectors share
- Implements every **data source connector**: Gmail, Google Calendar, Google Drive, Notion, Slack, and manual file uploads (PDF, voice, WhatsApp exports)
- Owns the **Ingestion Pipeline** — the assembly line that turns raw connector data into searchable memory:
  - Normalization (each source → standard `MemoryItem` shape)
  - Celery task design for background processing with retry logic
  - `SyncJob` tracking for incremental polling
- Owns **all new database models and Alembic migrations** for connectors, ingestion, and graph data
- Owns the **Knowledge Graph data model** — entity and edge tables in Postgres

**What Yashi can say in an interview:**
> "I architected and bootstrapped the entire project from scratch — I wrote the full system design document, set up Docker orchestration across 5 services, defined the FastAPI structure, created the database models with pgvector, and wrote all project documentation before the team started building. I then owned the backend data layer: I built the connector framework with OAuth 2.0 flows for Gmail, Google Calendar, Notion, and Slack, and designed the ingestion pipeline that normalizes raw data, dispatches Celery background tasks for enrichment, and stores it all for AI retrieval. I also implemented the full authentication system with JWT and bcrypt."

---

### Avinash — Frontend & UI Engineer

**Responsibilities:**
- Owns the **complete frontend** across all sprints — as each backend feature lands, Avinash wires the corresponding page to real API data instead of mocked data
- Owns the **design system** — color tokens, typography, spacing, component consistency, responsive layout, and all CSS across every page
- Owns all **page-level interactivity and animations**:
  - Canvas/SVG animations (`animation.js`, `animation.css`)
  - Micro-interactions, hover effects, transitions
  - Knowledge graph canvas visualization (force-directed layout)
- Takes ownership of all **12 HTML pages** including polish, accessibility, and mobile responsiveness:
  - Landing page, Login, Signup
  - Dashboard, Chat, Search, Timeline
  - Graph, Connectors, Building/Onboarding
  - Reflection, Settings
- Implements the **Action Confirmation UI** — inline draft cards in chat with Confirm/Cancel
- Manages the **nginx configuration** for frontend serving and Content Security Policy headers

**What Avinash can say in an interview:**
> "I owned the entire frontend of an AI personal assistant product. I built and maintained 12 pages including a real-time streaming chat interface, a canvas-rendered knowledge graph visualization with force-directed layout, and a multi-tab settings panel — all in vanilla HTML/CSS/JS with no framework, which gave me deep control over performance and animations. Throughout the project my responsibility was to progressively wire each page from mocked data to live API responses as backend features were delivered, including auth flows, SSE streaming for chat, semantic search results, and the agentic action confirmation cards."

---

## Sprint Plan

> **Sprint length:** 2 weeks each. &nbsp; ✅ = Done &nbsp;|&nbsp; ⬜ = Not Started
>
> **Sprint Owner** = the one person accountable for that sprint's delivery.
> Tasks within the sprint are still distributed by role — but the owner drives it to Done.
>
> **Rotation logic:** Sprint owner always matches the primary skill needed.
> Back-to-back is allowed when the work is continuous in the same domain.

| Sprint | Focus | Owner | Domain |
|---|---|---|---|
| Sprint 0 | Foundation & Architecture | **Yashi** ✅ | Backend/Architecture |
| Sprint 1 | CI/DevOps Setup | **Aditya** | DevOps |
| Sprint 2 | Authentication | **Yashi** | Backend |
| Sprint 3 | Google Connectors | **Yashi** | Data/Connectors |
| Sprint 4 | Frontend: Auth & Connectors UI | **Avinash** | Frontend |
| Sprint 5 | Notion, Slack + Ingestion Pipeline | **Yashi** | Data/Connectors |
| Sprint 6 | Embedding & LLM Enrichment | **Aditya** | AI |
| Sprint 7 | Semantic Search & Memory API | **Aditya** | AI/Backend |
| Sprint 8 | Frontend: Search, Timeline & Dashboard | **Avinash** | Frontend |
| Sprint 9 | Manual Upload & Knowledge Graph Data | **Yashi** | Data/Backend |
| Sprint 10 | RAG Chat & Graph API | **Aditya** | AI/Backend |
| Sprint 11 | Frontend: Chat, Graph & Reflection UI | **Avinash** | Frontend |
| Sprint 12 | Agentic Actions & Reflections | **Aditya** | AI |
| Sprint 13 | Security, Hardening & Production Deploy | **Aditya** | DevOps |

---

### Sprint 0 — Foundation & Architecture ✅
**Sprint Owner: Yashi** &nbsp;|&nbsp; *Domain: Backend / Architecture*

**Goal:** Deliver a complete, runnable project skeleton — Docker stack, database, API stubs, mocked frontend, and all team documentation — so every team member can clone the repo, run one command, and see the full app working before a single real feature is built.

**What Yashi does:** Yashi designs and documents the entire system before writing a line of application code. She writes `ARCHITECTURE.md` covering how the system layers fit together, how data flows from connector to AI response, and why each technology was chosen. She writes `README.md` with step-by-step local setup instructions, `CONTRIBUTING.md` with team coding standards and branch rules, and `PROJECT_STRUCTURE.md` mapping every file's purpose. She then builds the Docker Compose stack that wires all five services — PostgreSQL with the pgvector extension, Redis, the FastAPI backend, a Celery worker, and nginx — each with proper health checks so services start in the right order. She creates the FastAPI application structure with six API endpoint stubs (health, auth, connectors, memory, chat, graph) that return `501 Not Implemented` as placeholders, defines the first two database models (`User` and `MemoryItem` with a pgvector embedding column), runs the first Alembic migration to create those tables, and writes the one real working test — confirming that `GET /api/v1/health` returns `{"status": "ok"}`.

**What Avinash does:** Avinash builds all 12 frontend pages (landing, login, signup, dashboard, chat, search, timeline, graph, connectors, building/onboarding, reflection, settings), the complete CSS design system with color tokens, typography, spacing and layout utilities, and two JavaScript modules — `app.js` for all page interactivity and `animation.js` for canvas/SVG animations. All pages use hardcoded or mocked data at this stage; the real API connections happen in dedicated frontend sprints later. The goal here is that every screen the user will ever see exists visually from day one, so the team has a shared picture of the finished product.

**Definition of Done:** Anyone on the team clones the repo, copies `.env.example` to `.env`, runs `docker compose up --build`, and sees the full app at `http://localhost:8080` with all 12 pages navigable and the backend health check passing at `http://localhost:8000/api/v1/health`.

---

### Sprint 1 — CI/DevOps Setup ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: DevOps*

**Goal:** Make it impossible to merge broken code into `main`. Every pull request must automatically pass linting, type checking, and tests before Aditya can approve and merge it.

**What Aditya does:** Aditya sets up a GitHub Actions CI workflow that triggers on every pull request to `main`. The workflow runs four steps in sequence — `ruff check` and `ruff format` for linting and formatting, `mypy app` for type checking, and `pytest` for tests. If any step fails, the PR is blocked from merging. He also configures GitHub branch protection rules so that direct pushes to `main` are disabled, CI must pass, and at least one review (his) is required. Beyond CI, he commits a `.env.example` file documenting every required environment variable with safe default values, audits the existing Docker setup to confirm hot-reload volume mounts work correctly for local development, and pins all package versions in `requirements.txt` so the build is reproducible across all team members' machines.

**Definition of Done:** A team member opens a PR, makes a deliberate syntax error, and sees the CI pipeline fail and block the merge. They fix it, CI goes green, and only then can Aditya approve and merge.

---

### Sprint 2 — Authentication & User Management ⬜
**Sprint Owner: Yashi** &nbsp;|&nbsp; *Domain: Backend*

**Goal:** Real users can register, log in, receive JWT tokens, and stay authenticated. Every private API route rejects requests that don't carry a valid token.

**What Yashi does:** Yashi implements the complete authentication system. She creates `core/security.py` using `python-jose` for JWT signing and `passlib[bcrypt]` for password hashing. She replaces the `POST /auth/signup` stub with real logic: validate that the email isn't already taken, hash the password, insert the user row, and return an access token plus a refresh token. She does the same for `POST /auth/login` (verify password hash, return token pair) and adds `POST /auth/refresh` so the frontend can silently renew tokens before they expire. She writes a `get_current_user` FastAPI dependency that decodes the JWT, loads the user from the database, and raises a 401 if the token is missing, malformed, or expired — then applies that dependency to every private endpoint in the router. Finally she writes tests covering the happy path (signup, login, refresh) and all the failure cases (duplicate email, wrong password, expired token, missing token).

**Definition of Done:** A new user hits `POST /auth/signup`, gets a token, uses it on a protected endpoint and gets a 200. Using an expired or missing token on any protected endpoint returns 401. All auth tests pass in CI.

---

### Sprint 3 — Google Connectors (Gmail, Calendar, Drive) ⬜
**Sprint Owner: Yashi** &nbsp;|&nbsp; *Domain: Data / Connectors*

**Goal:** A user connects their Google account through an OAuth flow and their emails, calendar events, and Drive documents are automatically fetched, stored as `MemoryItem` rows, and kept in sync via a background Celery task that runs every 15 minutes.

**What Yashi does:** Yashi starts by creating two new database models — `ConnectorCredential` to securely store OAuth access and refresh tokens per user per connector, and `SyncJob` to track the last sync cursor or timestamp per connector so only new or changed data is fetched on subsequent runs. She writes a `BaseConnector` abstract class with `connect()`, `sync()`, and `disconnect()` methods plus shared token-refresh logic that all connectors inherit. She then implements the Google OAuth 2.0 flow: a redirect endpoint that sends the user to Google's consent screen with the correct scopes, and a callback endpoint that receives the authorization code, exchanges it for tokens, and stores them in `ConnectorCredential`. With OAuth working, she builds the Gmail connector — a full initial sync that fetches all email threads and parses sender, subject, body, and date into `MemoryItem` rows, plus an incremental sync Celery task that uses Gmail's `historyId` to fetch only messages that changed since the last run. She builds the same pattern for Google Calendar (using `updatedMin` for incremental sync) and Google Drive (exporting Google Docs as plain text, polling via `modifiedTime`). She adds the connector CRUD API endpoints (`GET /connectors`, `POST /connectors/connect`, `DELETE /connectors/disconnect`, `GET /connectors/{id}/status`) and writes tests for the Gmail and Calendar connectors using `respx` to mock the Google API HTTP calls.

**Definition of Done:** A user authenticates with Google, and within 15 minutes their emails and calendar events appear as rows in the `memory_items` table. The Celery beat scheduler runs incremental syncs automatically. Connector status endpoint returns last sync time and item count.

---

### Sprint 4 — Frontend: Auth & Connectors UI ⬜
**Sprint Owner: Avinash** &nbsp;|&nbsp; *Domain: Frontend*

**Goal:** Replace every mocked redirect in the login, signup, and connectors pages with real API calls. A brand-new user should be able to go from landing page all the way to a synced dashboard without any mocked behaviour.

**What Avinash does:** Avinash wires the login page to `POST /auth/login` — the form submits a real `fetch()` request, stores the returned JWT in `localStorage` on success, shows an inline error message on wrong credentials, and redirects to the dashboard. He does the same for the signup page connecting to `POST /auth/signup`, handling duplicate-email errors gracefully. He adds a token guard to every private page: on load, each page checks `localStorage` for a valid JWT and redirects to `/login.html` if it's missing or expired. He also adds automatic token refresh — when any API call returns a 401, the app silently calls `POST /auth/refresh` and retries the original request before showing an error to the user. On the connectors page he calls `GET /connectors` on load so each connector tile shows its real connected or disconnected state, and wires the "Connect" button to `POST /connectors/connect` which returns the Google OAuth URL — the frontend then redirects the user there. The building/onboarding page polls `GET /connectors/{id}/status` to show real-time sync progress and automatically redirects to the dashboard once the initial sync completes. Throughout, Avinash adds consistent loading skeleton states, error toast notifications, and empty state illustrations so the UI always communicates what's happening.

**Definition of Done:** A new user signs up, connects Gmail, watches the building screen show live sync progress, and lands on the dashboard — all using real API calls with no mocked data or hardcoded redirects.

---

### Sprint 5 — Notion & Slack Connectors + Ingestion Pipeline ⬜
**Sprint Owner: Yashi** &nbsp;|&nbsp; *Domain: Data / Connectors*

**Goal:** Add Notion and Slack as connected data sources. Build the ingestion pipeline — the assembly line that turns raw connector output into clean, structured, ready-to-embed `MemoryItem` rows — and wire all connectors through it.

**What Yashi does:** Yashi adds OAuth flows and connector implementations for Notion (fetching pages and database entries, using `last_edited_time` for incremental sync) and Slack (fetching messages from joined channels using cursor-based pagination). She then builds the shared ingestion pipeline that all connectors feed into. The first stage is a normalization layer — a pure `normalize(raw_item) -> MemoryItem` function for each connector type that produces a consistent shape regardless of source. She adds four new columns to `memory_items` via an Alembic migration (`category`, `entities`, `chunk_index`, `parent_id`) — these will be filled by Aditya's enrichment tasks in Sprint 6. She writes the Celery task orchestrator that chains the pipeline stages: normalize → enrich → chunk → embed, where the enrichment and embedding slots are currently placeholders that Aditya will fill in the next sprint. She adds retry logic with exponential backoff so transient API failures don't lose data, and logs permanently failed tasks to a `FailedJob` table for visibility. Tests cover both new connectors with mocked API responses and the normalization functions with known inputs.

**Definition of Done:** All five official connectors (Gmail, Calendar, Drive, Notion, Slack) are syncing. Every raw item passes through normalization and enters the ingestion chain. The pipeline is ready and waiting for Aditya's enrichment and embedding tasks.

---

### Sprint 6 — Embedding & LLM Enrichment ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: AI*

**Goal:** Every item that enters the ingestion pipeline gets tagged with meaningful categories and entities by Claude, split into correctly-sized chunks if it's long, and stored with a vector embedding that makes it semantically searchable.

**What Aditya does:** Aditya plugs two Celery tasks into the ingestion chain that Yashi built in Sprint 5. The first is the LLM enrichment task: for each incoming `MemoryItem`, it calls Claude with a structured prompt asking it to classify the item's category (email, meeting, document, note, certification, etc.), extract named entities (person names, organization names, topics), and note the sentiment. The results are written back to the `category` and `entities` columns. The second task handles text chunking and embedding: documents longer than 512 tokens are split into overlapping chunks so no context is lost at boundaries; each chunk becomes its own `MemoryItem` row with `chunk_index` and `parent_id` linking it back to the original. Then every chunk — whether a standalone short item or a piece of a longer document — is sent to an embedding API (Voyage AI or OpenAI's `text-embedding-3-small`) and the resulting 1536-dimensional vector is stored in the `embedding` column. Tests mock both the Claude API and the embedding API and assert that the correct fields are written to the database after each task runs.

**Definition of Done:** After a Gmail sync runs end to end, every email has a `category` and `entities` field populated by Claude. Emails longer than 512 tokens are split into chunks. Every chunk has a non-null vector in the `embedding` column. The full pipeline — normalize → enrich → chunk → embed — runs automatically without manual intervention.

---

### Sprint 7 — Semantic Search & Memory API ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: AI / Backend*

**Goal:** Expose the stored memory as a searchable API. A natural-language query should return the most relevant items ranked by semantic similarity, with optional filters to narrow by source, category, or date.

**What Aditya does:** Aditya implements the memory API endpoints that the frontend will rely on. The core is `GET /memory/search`: it embeds the incoming query text using the same embedding model used during ingestion, then runs a pgvector cosine similarity search (`<=>` operator) against all the user's stored embeddings, applies any optional filters (`category`, `source`, `date_range`), and returns ranked results with similarity scores. To improve recall for keyword-heavy queries, he adds hybrid search by combining the pgvector approximate nearest-neighbour results with a PostgreSQL `tsvector` full-text search using Reciprocal Rank Fusion (RRF) to merge the two ranked lists. He also implements `GET /memory/items` (a paginated, filterable, sortable list of all the user's memory items) and `GET /memory/items/{id}` (full content and metadata for a single item). Tests seed the database with known items and assert that searches return the expected items in the correct order.

**Definition of Done:** Searching `"my meeting with Priya about the project proposal"` returns the correct calendar event and related emails ranked at the top, even if those exact words don't appear verbatim in the stored content.

---

### Sprint 8 — Frontend: Search, Timeline & Dashboard ⬜
**Sprint Owner: Avinash** &nbsp;|&nbsp; *Domain: Frontend*

**Goal:** Replace all hardcoded data on the search, timeline, and dashboard pages with live API results. Every filter, sort, and pagination control must work against the real backend.

**What Avinash does:** Avinash wires the search page to `GET /memory/search` — typing in the search box triggers a debounced `fetch()` call, and results render with a source badge (Gmail, Notion, etc.), date, and a snippet with the matching text highlighted. He adds an empty state illustration for when there are no results. On the timeline page he calls `GET /memory/items` with pagination and renders a chronological feed grouped by date; the source filter chips at the top pass filter parameters to the API and re-fetch. He adds a "Load more" button or infinite scroll so long histories don't overwhelm the page. On the dashboard he fetches live stats — total memory count and breakdown by source — and populates the recent activity feed from the same endpoint. Throughout all three pages he adds loading skeleton states that display while data is fetching, and clear error messages if the API call fails.

**Definition of Done:** All three pages show the user's real ingested data. Filters change the API query and re-render results. Refreshing the page shows up-to-date data. No hardcoded content remains.

---

### Sprint 9 — Manual Upload & Knowledge Graph Data Layer ⬜
**Sprint Owner: Yashi** &nbsp;|&nbsp; *Domain: Data / Backend*

**Goal:** Users can upload their own files — PDFs, voice recordings, WhatsApp exports — directly without connecting an external service. Simultaneously, build the knowledge graph data model and start extracting entities from all stored memories.

**What Yashi does:** Yashi adds a file upload endpoint (`POST /connectors/upload`) that accepts multipart form data, validates the file type (PDF, audio, or plain text), and kicks off background processing. For PDFs she uses `PyMuPDF` (`fitz`) to extract clean text. For audio files she runs `faster-whisper` in a Celery task to produce a text transcript. For WhatsApp export `.txt` files she writes a parser that reads the date-sender-message format and splits it into individual `MemoryItem` rows. All three file types then flow through the same ingestion pipeline built in Sprints 5 and 6 — normalize, enrich, chunk, embed. She adds `GET /connectors/uploads` to list a user's upload history with filename, status, and item count. She also builds the knowledge graph data model: two new tables, `Entity` (storing unique people, organizations, and topics with their type and the user they belong to) and `GraphEdge` (storing relationships between entities — the relation type, strength, and the memory item the relationship was observed in). She writes a Celery task that runs on every newly enriched `MemoryItem`, calls Claude to extract entities and the relationships between them, and upserts the results into those tables. Tests cover the PDF extractor, the WhatsApp parser, the upload endpoint, and the entity extraction task with a mocked Claude response.

**Definition of Done:** A user uploads a PDF; within minutes its content appears in the timeline with embeddings and entity tags. The `entities` and `graph_edges` tables are being populated automatically as all existing and new memory items are processed.

---

### Sprint 10 — RAG Chat & Knowledge Graph API ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: AI / Backend*

**Goal:** The AI chat is live and answers questions using the user's own data with cited sources. The knowledge graph API serves real entity and relationship data.

**What Yashi does (supporting):** Yashi creates the `ConversationThread` and `ChatMessage` database models and migration — threads belong to a user and store a title and creation time; messages store their role (user or assistant), content, and a list of cited `memory_item_id` values that the AI used to generate the response.

**What Aditya does:** Aditya implements the full RAG pipeline as an API endpoint. When a user sends a message to `POST /chat/threads/{id}/messages`, the endpoint embeds the query, retrieves the top-k most relevant memory items using the search logic from Sprint 7, constructs a Claude prompt that includes the retrieved context with clear source labels, instructs Claude to cite which sources it used, and streams Claude's response back to the client token-by-token using Server-Sent Events so the user sees a live typing effect. The completed message (user turn and assistant turn) is stored in the database with the cited source IDs. He also implements `POST /chat/threads` to create a new conversation, `GET /chat/threads` to list all past conversations with title and last-message preview, and the knowledge graph API endpoints — `GET /graph/nodes`, `GET /graph/edges` (returning the full entity graph as JSON), and `GET /graph/nodes/{id}` (returning all memory items connected to a specific entity). Tests mock the Claude API and assert that the prompt sent to Claude contains the retrieved context and that the SSE stream produces the correct event structure.

**Definition of Done:** A user asks "What did I discuss about my internship in my Notion docs?" and receives a coherent, cited answer pulled from their real Notion data, streamed in real time. The graph API returns the user's real entity network.

---

### Sprint 11 — Frontend: Chat, Graph & Reflection UI ⬜
**Sprint Owner: Avinash** &nbsp;|&nbsp; *Domain: Frontend*

**Goal:** Wire the chat, knowledge graph, reflection, and settings pages to live APIs. Chat must stream token-by-token in real time. The graph must render the user's real entity network interactively.

**What Avinash does:** Avinash replaces the canned chat replies with a real `EventSource` SSE connection — as Claude's response streams in, tokens append to the message bubble in real time giving a natural typing feel. He wires the conversation rail on the left to `GET /chat/threads` so past conversations load on page open and a click restores the thread history. Below each AI response he renders source citation chips showing which connector (Gmail, Notion, etc.) and item the answer drew from. On the graph page he replaces the hardcoded demo dataset by fetching from `GET /graph/nodes` and `GET /graph/edges` and re-renders the force-directed canvas layout with real entity data — he tunes the physics so the graph handles real-world sizes without becoming a tangled mess. Clicking any node opens a side panel that calls `GET /graph/nodes/{id}` and lists all the memories connected to that entity. On the reflection page he fetches from `GET /reflections` to render the user's real weekly insights, and wires the "Generate Now" button to `POST /reflections/generate`. On the settings page he connects all tabs — profile update, password change, and the danger-zone account-deletion flow — to their respective backend endpoints. He also adds strict Content Security Policy headers to the nginx config and removes any `eval()` usage from the JavaScript modules.

**Definition of Done:** Chat streams real AI answers with source citations. The graph page shows the user's real entity network; clicking a person node reveals their connected memories. Settings changes persist to the database.

---

### Sprint 12 — Agentic Actions & Reflections ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: AI*

**Goal:** The twin can take real actions — drafting emails or creating calendar events — but nothing executes on any external account without the user explicitly clicking Confirm. Reflections generate automatically every Sunday.

**What Aditya does:** Aditya implements the Claude tool-use agentic loop. He defines three tools as Claude tool-use schemas — `draft_email` (compose an email given to, subject, and body), `create_calendar_event` (create an event given title, time, and attendees), and `search_memory` (run an internal search if Claude needs more context). When a user sends a message that implies an action, the multi-turn loop runs: Claude detects the intent, calls the appropriate tool, the backend prepares a draft without executing anything, and returns the draft to the user for review. Only when the user calls `POST /chat/threads/{id}/actions/confirm` with the action ID does the backend actually send the email or create the calendar event using the stored OAuth tokens. Calling `POST /chat/threads/{id}/actions/cancel` discards the draft with no external effect. Aditya also builds the reflection system: a Celery beat task scheduled for every Sunday at midnight queries the last seven days of memory items, calls Claude with a structured prompt asking for themes, accomplishments, recurring people, and open loops, stores the result as a `Reflection` row, and makes it accessible via `GET /reflections`, `GET /reflections/{id}`, and an on-demand `POST /reflections/generate` endpoint.

**What Yashi does (supporting):** Yashi adds the `send_email()` and `create_event()` action functions that reuse the stored OAuth tokens from the Sprint 3 connectors, and creates the `Reflection` database model and Alembic migration.

**What Avinash does (supporting):** Avinash renders the action draft card inline in the chat thread — a styled card showing the email subject and body (or event details) with clearly labelled "Confirm" and "Cancel" buttons. Clicking Confirm calls the confirm endpoint; Cancel calls cancel.

**Definition of Done:** A user types "Email Avinash a summary of what we discussed about the project timeline." The twin finds the relevant memories, drafts the email, shows it in the chat. The user clicks Confirm and the email sends. Clicking Cancel does nothing. Every Sunday a new reflection appears automatically.

---

### Sprint 13 — Security, Hardening & Production Deployment ⬜
**Sprint Owner: Aditya** &nbsp;|&nbsp; *Domain: DevOps*

**Goal:** The product is hardened against abuse and accidental data leaks, and is running live on a real HTTPS domain with automated deployments and daily database backups.

**What Aditya does:** Aditya adds rate limiting using `slowapi` middleware — the `/chat` endpoint is capped at 30 requests per minute per user and `/memory/search` at 60, preventing API cost abuse. He replaces all `print` statements with `structlog`, which emits structured JSON logs carrying `user_id`, `request_id`, and `duration_ms` on every request so logs are machine-queryable. He enhances the health check endpoint to actively verify that the database, Redis, and a Celery worker heartbeat are all reachable, returning a degraded status if any component is down rather than a misleading 200. He adds a `gitleaks` step to the GitHub Actions CI workflow so any PR that accidentally includes a secret (API key, password) is blocked before it merges. He creates a `docker-compose.prod.yml` that removes `--reload`, adds memory and CPU resource limits per container, and injects secrets via Docker secrets instead of a plain `.env` file. He sets up a GitHub Actions CD pipeline that triggers on every merge to `main`: it builds the Docker images, pushes them to a container registry, SSHs into the production VPS, pulls the new images, runs `alembic upgrade head` to apply any pending migrations, and smoke-tests `GET /health` before marking the deployment successful. He configures Caddy as a reverse proxy in front of the stack for automatic TLS via Let's Encrypt — `/api/*` proxies to the FastAPI backend and `/` proxies to the nginx frontend. Finally he sets up a daily `pg_dump` cron job that uploads the compressed backup to object storage (Backblaze B2 or S3) and configures UptimeRobot to ping `/health` every minute and send an alert if it goes down.

**What Yashi does (supporting):** Yashi encrypts the stored OAuth `access_token` and `refresh_token` values in `ConnectorCredential` using `cryptography.Fernet` before they are written to the database, and decrypts them on read — so even if the database were compromised, the raw tokens would not be exposed.

**What all three members do:** Once the production deployment is live, all three team members run through the complete user journey independently — sign up, connect Gmail, wait for sync, search memories, have a chat, confirm an agentic action, and view a generated reflection — and report any bugs before calling the sprint done.

**Definition of Done:** The product is live at a real HTTPS URL. Any team member can send a PR, see CI run, merge it, and watch the CD pipeline deploy the change to production automatically within minutes. Database backups run daily. An uptime alert fires if the product goes down.

---

## Full Sprint Schedule

| Sprint | Focus | Owner | Weeks |
|---|---|---|---|
| Sprint 0 | Foundation & Architecture | **Yashi** ✅ | Done |
| Sprint 1 | CI/DevOps Setup | **Aditya** | Wk 1–2 |
| Sprint 2 | Authentication | **Yashi** | Wk 3–4 |
| Sprint 3 | Google Connectors | **Yashi** | Wk 5–6 |
| Sprint 4 | Frontend: Auth & Connectors UI | **Avinash** | Wk 7–8 |
| Sprint 5 | Notion, Slack + Ingestion Pipeline | **Yashi** | Wk 9–10 |
| Sprint 6 | Embedding & LLM Enrichment | **Aditya** | Wk 11–12 |
| Sprint 7 | Semantic Search & Memory API | **Aditya** | Wk 13–14 |
| Sprint 8 | Frontend: Search, Timeline & Dashboard | **Avinash** | Wk 15–16 |
| Sprint 9 | Manual Upload & Knowledge Graph Data | **Yashi** | Wk 17–18 |
| Sprint 10 | RAG Chat & Graph API | **Aditya** | Wk 19–20 |
| Sprint 11 | Frontend: Chat, Graph & Reflection UI | **Avinash** | Wk 21–22 |
| Sprint 12 | Agentic Actions & Reflections | **Aditya** | Wk 23–24 |
| Sprint 13 | Security, Hardening & Production Deploy | **Aditya** | Wk 25–26 |

**Total:** ~26 weeks (6.5 months) to a fully production-ready, industry-quality product.
