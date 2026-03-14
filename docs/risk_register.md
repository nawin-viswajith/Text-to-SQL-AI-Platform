# Initial Risk Register

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R1 | Schema drift causes query failures | High | Reflexion analyzer + schema updater + retry budget |
| R2 | Unsafe SQL generation | High | SQL denylist, SELECT-only enforcement, LIMIT hardening |
| R3 | Slow responses on large tables | Medium | EXPLAIN check, default LIMIT, index metadata in retrieval |
| R4 | On-prem connectivity constraints | High | Early environment validation and health checks |
| R5 | External client abuse of MCP tools | Medium | API token in prod + rate limiting |

