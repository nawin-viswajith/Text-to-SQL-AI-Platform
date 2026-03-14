# LangGraph Reflexion Flow

1. `context_check`:
   - If DB is connected -> `rag_retrieval`
   - If disconnected -> `sql_generation` (generic fallback mode)
2. `rag_retrieval` -> `sql_generation`
3. `sql_generation` -> `sql_safety_validate`
4. `sql_safety_validate`:
   - Pass -> `execution`
   - Fail -> `reflexion_analyzer`
5. `execution` -> `reflexion_analyzer` (or `finish` when disconnected fallback)
6. `reflexion_analyzer`:
   - Schema mismatch + retries available -> `schema_updater`
   - Else -> `finish`
7. `schema_updater`:
   - Success -> `rag_retrieval`
   - Failure -> `finish`
8. `finalize`

