# Environment Matrix

| Environment | Purpose | DB Target | Chroma Target | Docs Access | Auth |
|---|---|---|---|---|---|
| Dev | Local feature development | Local/Shared MySQL read-only | Local path `.chroma` | Open | Optional |
| Stage | Integration and QA | Staging MySQL read-only | Persistent volume | Token gated | Required |
| Prod (On-Prem) | Enterprise runtime | Production MySQL read-only | Persistent on-prem storage | Token gated | Required |

