# Observability Dashboard Blueprint

## Dashboard 1: API Reliability
- Request rate by endpoint
- Success/error rate
- P95 latency
- 4xx/5xx trend

## Dashboard 2: Query Quality
- Query success vs error categories
- Retry rate and retry success rate
- Schema mismatch frequency
- RAGAS/fallback score trends

## Dashboard 3: MCP Usage
- Tool call volume by tool name
- Rate-limit events
- Auth failures

## Alerting Suggestions
- API error rate > 2% for 5 minutes
- P95 latency > 8s for 10 minutes
- Schema mismatch spike > baseline + 50%
- Consecutive refresh failures > 3

