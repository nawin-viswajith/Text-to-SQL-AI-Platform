# Enterprise Text-to-SQL Platform

Enterprise-grade Text-to-SQL platform with reflexion retries, schema-aware RAG, MCP tools/resources, and a split-view operator dashboard.

## Features

### AI / Orchestration
- LangGraph-style reflexion workflow:
  - `context_check`
  - `rag_retrieval`
  - `sql_generation`
  - `sql_safety_validate`
  - `execution`
  - `reflexion_analyzer`
  - `schema_updater` (conditional retry)
  - `finalize`
- Retry policy:
  - Auto-retry only for schema mismatch errors.
  - Bounded retries (`max_retries`, default 2).
- SQL safety controls:
  - `SELECT`-only enforcement.
  - DDL/DML denylist.
  - LIMIT hardening (default and max cap).
  - `EXPLAIN` pre-check before execution.

### Retrieval / RAG
- ChromaDB schema index for DDL and metadata (columns, indexes, row counts).
- Retrieval strategies:
  - `mmr` (default) for diversity-aware reranking.
  - `similarity` for top-ranked retrieval.
- Retrieval diagnostics returned in query responses.
- In-memory fallback store when Chroma is unavailable.

### Evaluation / Observability
- Optional per-query RAGAS scoring (`run_ragas=true`).
- Dedicated RAGAS evaluation API endpoint.
- Fallback lexical scoring mode when full RAGAS runtime is unavailable.
- LangSmith integration for:
  - run lifecycle trace IDs
  - node event logging
  - retrieval diagnostics logging
  - metric feedback logging (RAGAS/fallback scores)
- HTTP audit middleware with request IDs and latency logging.

### API / MCP
- FastAPI backend with OpenAPI docs.
- REST endpoints for query, streaming, schema refresh, run retrieval, and evaluation.
- MCP tool/resource endpoints with:
  - production auth gating
  - optional RBAC role gating (`RBAC_ENABLED=true`)
  - sliding-window rate limiting

### Frontend
- React + Vite + Tailwind 4 + Framer Motion dashboard.
- Split-view UX:
  - natural language query input
  - SQL preview + reflexion notes
  - animated results table
  - LangGraph timeline events
- Deep Space Noir visual style tokens.

## Tech Stack

- Backend: Python, FastAPI, LangGraph, LangChain, LangSmith
- Data: MySQL (read-only), ChromaDB
- Evaluation: RAGAS
- Frontend: React, Vite, Tailwind 4, Framer Motion
- Ops: Docker, GitHub Actions CI

## Project Structure

```text
backend/
  app/
    api/v1/
    core/
    db/
    graph/
    mcp/
    observability/
    rag/
    schemas/
    services/
    tests/
frontend/
  src/
docs/
infra/
```

## Quick Start (Local)

### 1) Prerequisites

- Python 3.11+
- Node.js 20+ (22 recommended)
- npm
- MySQL instance with read-only credentials

### 2) Configure Environment

Copy `.env.example` values into your shell or environment manager and set:
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- optional tracing/eval flags (`LANGSMITH_*`, `RAGAS_*`)

### 3) Run Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4) Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:5173`  
Backend default URL: `http://localhost:8000`

## Quick Start (Docker Compose)

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:4173`

## API Documentation

- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`
- ReDoc: `http://localhost:8000/redoc`

Production note:
- When `APP_ENV=prod`, docs are gated by `X-Docs-Token`.
- API/MCP are gated by `X-Api-Token`.

## REST Endpoints

- `GET /api/v1/health`
- `POST /api/v1/query`
- `POST /api/v1/query/stream` (SSE)
- `POST /api/v1/schema/refresh`
- `GET /api/v1/runs/{run_id}`
- `POST /api/v1/evaluate/ragas`

## Query Controls

`POST /api/v1/query` supports:
- `max_retries`
- `retrieval_strategy` (`mmr` or `similarity`)
- `retrieval_fetch_k`
- `mmr_lambda`
- `run_ragas`
- `reference_answer`

Response includes:
- generated `safe_sql`
- query `result`
- `retrieval_diagnostics`
- optional `ragas_scores`
- node `events`

## MCP Contracts

### Tool Endpoints
- `POST /api/v1/mcp/tools/generate_sql`
- `POST /api/v1/mcp/tools/execute_readonly_sql`
- `POST /api/v1/mcp/tools/refresh_schema_index`
- `POST /api/v1/mcp/tools/get_table_catalog`
- `POST /api/v1/mcp/tools/evaluate_ragas`

### Resource Endpoints
- `GET /api/v1/mcp/resources/schema/catalog`
- `GET /api/v1/mcp/resources/schema/table/{table_name}`
- `GET /api/v1/mcp/resources/run/{run_id}/trace`

## Testing and Validation

```bash
cd backend
python -m compileall app
pytest app/tests -q
```

Centralized test suite directory:

```bash
pytest test -q
```

Smoke test:

```bash
python test/smoke/run_smoke.py
```

If `pytest` is not installed, run:

```bash
pip install -r requirements.txt
```

## Important Notes

- The app is designed for read-only MySQL access.
- Schema indexing requires reachable MySQL metadata tables.
- RAGAS may run in fallback mode depending on local runtime/dependency availability.
- LangSmith logging is controlled by `LANGSMITH_TRACING` and related env vars.
