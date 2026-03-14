# Architecture Overview

## Core Runtime
- Frontend sends natural language question to FastAPI.
- FastAPI invokes `QueryOrchestrator`, which runs the reflexion workflow.
- Workflow steps:
  1. Context check
  2. RAG schema retrieval
  3. SQL generation
  4. SQL safety validation
  5. MySQL execution
  6. Reflexion analyzer
  7. Schema updater (conditional)
  8. Finalize
- ChromaDB stores schema metadata for retrieval.
- Retrieval supports `MMR` reranking for better schema diversity.
- MySQL access is read-only via SQL policy and executor.
- RAGAS scoring can evaluate runs and log metrics.
- LangSmith hooks capture workflow events, retrieval diagnostics, and evaluation metrics.

## Security and Reliability
- Read-only SQL policy with denylist and SELECT-only enforcement.
- Automatic LIMIT policy to avoid unbounded scans.
- Retry path only for schema mismatch failures.
- MCP tool endpoints protected by API auth in production and rate limited.
