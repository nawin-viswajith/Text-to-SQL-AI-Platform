# Enterprise Text-to-SQL Platform

This repository contains an enterprise-grade Text-to-SQL platform with:

- FastAPI backend with OpenAPI docs
- LangGraph-style reflexion workflow for SQL generation/retry
- MySQL read-only execution
- ChromaDB-backed schema retrieval with MMR reranking (fallback in-memory index)
- RAGAS evaluation endpoint and optional per-query scoring
- MCP-compatible tools and resources
- React + Vite + Tailwind + Framer Motion dashboard

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Docs

- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`
- ReDoc: `http://localhost:8000/redoc`

In production (`APP_ENV=prod`), docs routes require `X-Docs-Token`.
