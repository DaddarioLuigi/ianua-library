# Planning Checklist

Use this checklist when decomposing a feature spec into implementation tasks.

## Pre-Planning Verification

- [ ] Spec exists in `specs/features/` with status `approved`
- [ ] All clarification questions answered
- [ ] No unresolved dependencies on other in-progress features
- [ ] Stakeholder has approved the spec (gdrive_url populated)

## Task Decomposition Checklist

For each task you create, verify:

- [ ] Task is atomic (single concern, single commit)
- [ ] Task is completable in 1-3 hours
- [ ] Task has clear acceptance criteria
- [ ] Task has at least one associated test requirement
- [ ] Task is ordered correctly (no circular dependencies)

## Domain Analysis Prompts

**Database**
- Does this require a new table? → Migration task first
- Does this add columns to existing tables? → Migration + Model update
- Does this change indexes? → Performance implications

**Authorization**
- Which roles can perform each action?
- Are there tenant/org-scoped restrictions?
- Are there role-specific exclusions?

**API Surface**
- Does this create new API endpoints? → OpenAPI spec task required
- Does this change response formats? → Breaking change? → Version bump

**Redis**
- Which keys are introduced or modified?
- Is TTL defined and justified?
- How is cache invalidation handled on write paths?

**Background Processing**
- Does this need async processing? → Job task
- Is it recurring? → Scheduler/Cron task
- Does it send notifications/emails? → worker + template tasks

**Frontend**
- Does this require new Next.js routes/pages?
- Is it SSR, SSG, ISR, or CSR?
- Are reusable React components/hooks needed?

**Internationalization**
- New user-facing strings? → i18n task for supported locales
- Date/time formatting? → Use frontend/backend locale-safe formatters

## Issue Labels Reference

| Label | When to use |
|-------|------------|
| `feature` | New functionality |
| `bug` | Defect fix |
| `refactor` | Code quality improvement |
| `test` | Test-only change |
| `docs` | Documentation only |
| `db` | Data model and migrations |
| `api` | API endpoints |
| `auth` | Authentication/authorization |
| `jobs` | Background jobs |
| `redis` | Cache and distributed primitives |
| `nextjs` | Frontend app router/pages |
| `flask` | Flask backend modules |
| `infra` | Infrastructure/CI/deploy |
