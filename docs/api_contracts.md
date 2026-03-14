# API Contracts (v1)

## REST Endpoints
- `GET /api/v1/health`
- `POST /api/v1/query`
- `POST /api/v1/query/stream`
- `POST /api/v1/schema/refresh`
- `GET /api/v1/runs/{run_id}`

## MCP Tool Endpoints
- `POST /api/v1/mcp/tools/generate_sql`
- `POST /api/v1/mcp/tools/execute_readonly_sql`
- `POST /api/v1/mcp/tools/refresh_schema_index`
- `POST /api/v1/mcp/tools/get_table_catalog`

## MCP Resource Endpoints
- `GET /api/v1/mcp/resources/schema/catalog`
- `GET /api/v1/mcp/resources/schema/table/{table_name}`
- `GET /api/v1/mcp/resources/run/{run_id}/trace`

## Documentation Routes
- `/openapi.json`
- `/docs`
- `/redoc`

