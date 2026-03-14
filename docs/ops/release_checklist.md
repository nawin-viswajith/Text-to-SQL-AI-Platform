# Release Checklist

- [ ] All required tests pass (`backend/app/tests` and `test/` suites).
- [ ] API docs validated against implemented endpoints.
- [ ] Security checks reviewed (auth, RBAC flag, SQL policy).
- [ ] MySQL read-only credentials verified in target environment.
- [ ] Chroma storage path verified and writable.
- [ ] Smoke tests executed post-deploy.
- [ ] Rollback plan and owner confirmed.

