# Initial Risk Register

| ID | Risk | Impact | Owner | Mitigation |
|---|---|---|---|---|
| R1 | Schema drift causes query failures | High | Data Platform Lead | Reflexion analyzer + schema updater + retry budget |
| R2 | Unsafe SQL generation | High | AI Engineer | SQL denylist, SELECT-only enforcement, LIMIT hardening |
| R3 | Slow responses on large tables | Medium | Backend Engineer | EXPLAIN check, default LIMIT, index metadata in retrieval |
| R4 | On-prem connectivity constraints | High | Infra Engineer | Early environment validation and health checks |
| R5 | External client abuse of MCP tools | Medium | Security Engineer | API token in prod + rate limiting |
