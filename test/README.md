# Test Directory

This directory is a centralized test entrypoint for project-wide validation.

## Structure
- `test/backend/`: API contracts, retrieval quality checks, MCP checks
- `test/smoke/`: critical-path smoke runner
- `test/performance/`: load-testing assets
- `test/conftest.py`: shared Python path setup for backend app imports

## Run

```bash
pytest test -q
```

Smoke run:

```bash
python test/smoke/run_smoke.py
```

If dependencies are missing:

```bash
pip install -r backend/requirements.txt
```
