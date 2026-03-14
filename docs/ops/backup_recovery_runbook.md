# Backup and Recovery Runbook

## Backup Scope
- MySQL production database (managed by DBA policy)
- Chroma persistent volume (`CHROMA_PATH`)
- Application config snapshots

## Backup Cadence
- MySQL: daily full + hourly incremental
- Chroma metadata volume: daily snapshot
- Config and runbooks: per release

## Recovery Steps
1. Restore MySQL to last known good state.
2. Restore Chroma snapshot.
3. Run `POST /api/v1/schema/refresh` to validate index consistency.
4. Execute smoke tests (`test/smoke/run_smoke.py`).
5. Validate dashboard API and critical query flows.

## Recovery Validation
- Health endpoint returns 200.
- Query endpoint returns valid safe SQL.
- MCP catalog and RAGAS endpoints return successful contracts.

