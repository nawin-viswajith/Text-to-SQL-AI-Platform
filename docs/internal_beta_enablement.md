# Internal Beta Enablement Notes

## Audience
- Internal analysts
- Data engineering reviewers
- Product stakeholders

## Access Checklist
- Ensure API and frontend are reachable in staging.
- Provide read-only MySQL credentials for beta environment.
- Share API auth token for protected routes when required.

## Core Test Flows
- Submit NL query and validate generated SQL.
- Confirm query results render in split-view dashboard.
- Validate reflexion behavior on schema mismatch prompts.
- Validate MCP tool calls for catalog and RAGAS evaluation.

## Feedback Template
- Prompt used:
- Expected output:
- Actual output:
- Severity:
- Suggested improvement:

## Known Constraints
- Non-read-only SQL is blocked by policy.
- RAGAS may run in fallback mode depending on runtime dependencies.
- Docs and API access are gated in production mode.

