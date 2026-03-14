# API Contracts (v1)

## REST Endpoints
- `GET /api/v1/health`
- `POST /api/v1/query`
- `POST /api/v1/query/stream`
- `POST /api/v1/schema/refresh`
- `GET /api/v1/runs/{run_id}`
- `POST /api/v1/evaluate/ragas`

## MCP Tool Endpoints
- `POST /api/v1/mcp/tools/generate_sql`
- `POST /api/v1/mcp/tools/execute_readonly_sql`
- `POST /api/v1/mcp/tools/refresh_schema_index`
- `POST /api/v1/mcp/tools/get_table_catalog`
- `POST /api/v1/mcp/tools/evaluate_ragas`

## MCP Resource Endpoints
- `GET /api/v1/mcp/resources/schema/catalog`
- `GET /api/v1/mcp/resources/schema/table/{table_name}`
- `GET /api/v1/mcp/resources/run/{run_id}/trace`

## Documentation Routes
- `/openapi.json`
- `/docs`
- `/redoc`

## Access Control Headers
- `X-Api-Token`: API/MCP protection in production
- `X-Docs-Token`: docs protection in production
- `X-User-Role`: role context when `RBAC_ENABLED=true`

## Retrieval and Evaluation
- Query API supports retrieval strategy controls:
  - `retrieval_strategy`: `mmr` or `similarity`
  - `retrieval_fetch_k`: candidate pool size for reranking
  - `mmr_lambda`: relevance-vs-diversity tradeoff
- Query API can run optional RAGAS evaluation:
  - `run_ragas`: trigger evaluation
  - `reference_answer`: optional ground truth for correctness metric
