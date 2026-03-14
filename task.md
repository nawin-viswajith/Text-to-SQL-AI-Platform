# Enterprise Text-to-SQL Platform - Business Execution Checklist

## How to Use
- Mark each checkbox as work is completed.
- Treat each week as a business delivery unit with measurable outcomes.
- Do not move to the next week until the current week exit gate is complete.

## Week 1
- [ ] Plan: Program kickoff and foundation alignment.
- [ ] Subtopic: Confirm business goals, MVP scope, and internal beta success criteria.
- [ ] Subtopic: Assign owners for Backend/AI, Frontend, Data/Infra, QA.
- [ ] Subtopic: Approve architecture baseline and governance model.
- [ ] KPI: Project charter signed by stakeholders.
- [ ] Exit Gate: Sprint 1 backlog approved and prioritized.

## Week 2
- [x] Plan: Delivery foundation setup.
- [x] Subtopic: Bootstrap repo structure for backend, frontend, infra, docs.
- [x] Subtopic: Configure CI skeleton and environment matrix (dev/stage/on-prem prod).
- [ ] Subtopic: Create initial risk register and mitigation owners.
- [ ] KPI: CI executes baseline pipeline without failures.
- [ ] Exit Gate: Phase 0 sign-off completed.

## Week 3
- [x] Plan: Core backend skeleton (part 1).
- [x] Subtopic: Stand up FastAPI service with health and docs routes.
- [x] Subtopic: Define v1 contracts for query, stream, schema refresh, run retrieval.
- [x] Subtopic: Create initial AgentState schema.
- [x] KPI: API starts successfully in dev and returns health status.
- [ ] Exit Gate: Core API contracts reviewed by team.

## Week 4
- [x] Plan: Core backend skeleton (part 2).
- [x] Subtopic: Add MySQL read-only connector and execution service shell.
- [x] Subtopic: Add LangSmith trace hooks and run metadata capture.
- [x] Subtopic: Create initial unit test harness for backend nodes/services.
- [x] KPI: End-to-end mocked query flow runs with trace ID.
- [ ] Exit Gate: Sprint demo approved by tech lead.

## Week 5
- [x] Plan: Schema intelligence (part 1).
- [x] Subtopic: Implement schema metadata ingestion from MySQL information schema.
- [x] Subtopic: Store DDL, columns, indexes, row count metadata in ChromaDB.
- [x] Subtopic: Define schema refresh process and operational triggers.
- [ ] KPI: Schema docs indexed for all target tables.
- [ ] Exit Gate: Metadata quality validated on seed dataset.

## Week 6
- [x] Plan: Schema intelligence (part 2).
- [x] Subtopic: Implement retrieval and ranking for schema context (top-k).
- [ ] Subtopic: Add retrieval telemetry and quality metrics logging.
- [ ] Subtopic: Build integration tests for schema retrieval.
- [ ] KPI: Target relevance quality achieved on benchmark prompts.
- [ ] Exit Gate: Phase 2 completion sign-off.

## Week 7
- [x] Plan: Safe SQL generation controls.
- [x] Subtopic: Implement SQL generation node with schema-grounded prompting.
- [x] Subtopic: Add SQL policy validator (SELECT-only + denylist).
- [x] Subtopic: Enforce default/max LIMIT policy.
- [ ] KPI: Unsafe SQL leakage rate is zero in test suite.
- [ ] Exit Gate: Security review for SQL policy passed.

## Week 8
- [x] Plan: Explain and execution safety.
- [x] Subtopic: Add EXPLAIN pre-check before execution.
- [x] Subtopic: Add execution node output schema (rows, columns, timing).
- [ ] Subtopic: Build tests for valid generation and guarded execution.
- [ ] KPI: Stable query execution on baseline scenarios.
- [ ] Exit Gate: Phase 3 acceptance criteria met.

## Week 9
- [x] Plan: Reflexion loop (part 1).
- [x] Subtopic: Implement error classifier for schema mismatch and non-retryable errors.
- [x] Subtopic: Implement reflexion analyzer routing decisions.
- [x] Subtopic: Add retry counters and retry budget policy.
- [ ] KPI: Errors classified correctly by category in tests.
- [ ] Exit Gate: Reflexion decision logic approved.

## Week 10
- [x] Plan: Reflexion loop (part 2).
- [x] Subtopic: Implement schema updater and ChromaDB refresh on mismatch.
- [x] Subtopic: Wire retry path back to retrieval/generation/execution.
- [x] Subtopic: Add run audit logs for each retry attempt.
- [ ] KPI: Schema mismatch auto-recovery succeeds in target cases.
- [ ] Exit Gate: Phase 4 completion demo approved.

## Week 11
- [x] Plan: MCP and developer tooling (part 1).
- [x] Subtopic: Implement MCP tool endpoints (generate_sql, execute_readonly_sql).
- [x] Subtopic: Implement auth and request governance for external clients.
- [ ] Subtopic: Add contract tests for MCP tool schemas.
- [ ] KPI: External client can call tools successfully in stage.
- [ ] Exit Gate: MCP API review passed.

## Week 12
- [x] Plan: MCP and developer tooling (part 2).
- [x] Subtopic: Implement MCP resources (schema catalog, table context, run trace).
- [x] Subtopic: Add rate limiting and deterministic response behavior.
- [x] Subtopic: Publish developer-facing API usage docs.
- [ ] KPI: MCP reliability target met in stage tests.
- [ ] Exit Gate: Phase 5 sign-off complete.

## Week 13
- [x] Plan: UI MVP foundation.
- [x] Subtopic: Set up React + Vite + Tailwind 4 + Framer Motion baseline.
- [ ] Subtopic: Implement dashboard layout shell and routing.
- [x] Subtopic: Apply Deep Space Noir design system tokens.
- [ ] KPI: UI shell fully responsive desktop/mobile.
- [ ] Exit Gate: UI baseline approved by product/design.

## Week 14
- [x] Plan: UI query workflow.
- [x] Subtopic: Implement NL input panel and query submit workflow.
- [x] Subtopic: Implement SQL preview and status messaging.
- [x] Subtopic: Integrate sync query API response rendering.
- [ ] KPI: Users can submit NL query and see SQL output.
- [ ] Exit Gate: Core user path validated internally.

## Week 15
- [x] Plan: UI results and timeline.
- [x] Subtopic: Build animated data table output panel.
- [x] Subtopic: Build run timeline and reflexion notes visualization.
- [x] Subtopic: Integrate streaming query events.
- [ ] KPI: Full split-view experience works with live backend.
- [ ] Exit Gate: Internal UX walkthrough passed.

## Week 16
- [x] Plan: UI stabilization and beta prep.
- [x] Subtopic: Add frontend error handling and loading states.
- [ ] Subtopic: Add interaction tests for query lifecycle.
- [ ] Subtopic: Prepare internal beta enablement notes.
- [ ] KPI: Internal beta-ready UI quality baseline achieved.
- [ ] Exit Gate: Phase 6 beta launch approval.

## Week 17
- [ ] Plan: Enterprise hardening (security).
- [ ] Subtopic: Implement RBAC baseline and role-based API access.
- [ ] Subtopic: Integrate secrets handling for on-prem runtime.
- [ ] Subtopic: Expand audit logging coverage for all critical operations.
- [ ] KPI: Security checklist passes baseline controls.
- [ ] Exit Gate: Security gate approval complete.

## Week 18
- [ ] Plan: Enterprise hardening (operations).
- [ ] Subtopic: Build observability dashboards and alerting.
- [ ] Subtopic: Define backup/recovery runbook.
- [ ] Subtopic: Run load/performance tests and tune bottlenecks.
- [ ] KPI: Stage reliability target (99.5% success) achieved.
- [ ] Exit Gate: Operational readiness sign-off.

## Week 19
- [ ] Plan: UAT preparation.
- [ ] Subtopic: Finalize UAT scenarios with business users.
- [ ] Subtopic: Prepare release checklist and rollback strategy.
- [ ] Subtopic: Freeze change scope for release branch.
- [ ] KPI: UAT environment and scripts fully ready.
- [ ] Exit Gate: UAT kickoff approved.

## Week 20
- [ ] Plan: UAT execution (part 1).
- [ ] Subtopic: Execute UAT functional scenarios.
- [ ] Subtopic: Track defects by severity and owner.
- [ ] Subtopic: Prioritize and patch P1/P2 issues.
- [ ] KPI: No blocker defects open at week close.
- [ ] Exit Gate: UAT wave 1 completed.

## Week 21
- [ ] Plan: UAT execution (part 2).
- [ ] Subtopic: Re-test patched defects and regression suite.
- [ ] Subtopic: Validate retry/recovery and safety controls with users.
- [ ] Subtopic: Confirm production runbook with support team.
- [ ] KPI: UAT pass rate meets sign-off threshold.
- [ ] Exit Gate: Business acceptance received.

## Week 22
- [ ] Plan: Production readiness.
- [ ] Subtopic: Final performance validation and resilience checks.
- [ ] Subtopic: Verify monitoring, alerting, and incident response flow.
- [ ] Subtopic: Conduct rollback rehearsal.
- [ ] KPI: Go-live checklist at 100% completion.
- [ ] Exit Gate: Go-live authorization granted.

## Week 23
- [ ] Plan: Production release.
- [ ] Subtopic: Deploy to on-prem production.
- [ ] Subtopic: Perform smoke tests and critical path validation.
- [ ] Subtopic: Start hypercare monitoring window.
- [ ] KPI: Zero P1 incidents during first 48 hours.
- [ ] Exit Gate: Release marked stable.

## Week 24
- [ ] Plan: Post-launch stabilization and handoff.
- [ ] Subtopic: Close residual defects and optimize performance.
- [ ] Subtopic: Publish executive launch report with KPIs.
- [ ] Subtopic: Create next-quarter roadmap from production learnings.
- [ ] KPI: Hypercare success and operational handoff completed.
- [ ] Exit Gate: Program phase closure approved by stakeholders.


