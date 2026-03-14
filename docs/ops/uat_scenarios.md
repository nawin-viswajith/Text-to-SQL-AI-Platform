# UAT Scenarios

## Scenario 1: Standard Analytics Query
- Input: "Top 10 customers by revenue"
- Expectation: Safe SQL generated, results returned, timeline visible.

## Scenario 2: Schema Drift Recovery
- Input references missing column/table.
- Expectation: Reflexion triggers schema updater and retries within budget.

## Scenario 3: Policy Safety
- Input attempts write operation.
- Expectation: SQL blocked with policy error, no DB mutation.

## Scenario 4: MCP Contract
- Invoke `get_table_catalog` and `evaluate_ragas`.
- Expectation: Deterministic JSON contract responses.

