---
name: spec-driven-planning
description: >-
  Plan feature implementation from technical specs in the /specs folder
  for Flask backend, Next.js frontend, and Redis-backed capabilities.
---

# Spec-Driven Planning

Decomposes a feature spec into an ordered, atomic implementation plan with GitHub issues.

## Workflow

### Step 1 — Load the Spec
Read the feature spec from `specs/features/<name>.md`.
If the spec doesn't exist yet, guide the user to create one using `specs/templates/feature-spec-template.md`.

### Step 2 — Analyze Scope
Identify all affected areas:
- **Models**: new models, fields/associations, migrations needed
- **Services**: domain/application services
- **Authorization**: permission rules and role checks
- **API**: Flask blueprints/endpoints and serializers
- **Frontend**: React/Next.js pages, components, data fetching
- **Jobs**: background processing requirements
- **Redis**: cache keys, invalidation, TTL, pub/sub, locks, rate limits
- **Tests**: unit, integration, E2E

### Step 3 — Clarification Loop
Before decomposing, ask targeted questions (max 3-4 at a time):
- "Serve una nuova tabella o solo campi su entità esistenti?"
- "Quali ruoli possono usare la feature e con quali limiti?"
- "Ci sono endpoint nuovi o modifiche breaking alle API?"
- "La feature usa Redis? Se sì: chiavi, TTL, invalidazione e fallback?"
- "Sono richiesti job async/scheduler?"
- "Ci sono requisiti specifici per SSR/CSR in Next.js?"

Iterate until scope is clear. Update the spec if clarifications reveal new requirements.

### Step 4 — Decompose into Tasks
Create atomic tasks following this implementation order:

```
1. Migration (if new table/columns)
2. Model (validations, relations, indexes)
3. Service objects (business logic)
4. Auth/permission rules
5. Flask route + schema + serializer
6. Redis contracts (keys, TTL, invalidation)
7. Next.js page/components/hooks
8. Background jobs/workers
9. Unit tests
10. Integration/API tests
11. E2E tests
12. OpenAPI spec (if API endpoint)
13. i18n keys
```

Each task must be:
- Completable in 1-3 hours
- Independently testable
- Described with clear acceptance criteria

### Step 5 — Create GitHub Issues
For each task, create a GitHub issue:

```bash
gh issue create \
  --title "[feat] <task description>" \
  --label "feature,<domain>" \
  --milestone "<sprint>" \
  --body "$(cat <<'EOF'
## Context
Spec: specs/features/<name>.md

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests passing with >80% coverage

## Technical Notes
- Models: ...
- Migration: yes/no
- Breaking changes: yes/no
EOF
)"
```

Domain labels: `api`, `auth`, `db`, `jobs`, `infra`, `ui`, `redis`, `nextjs`, `flask`

### Step 6 — Output Summary
Present the implementation plan as an ordered checklist with:
- Issue numbers
- Estimated complexity (S/M/L)
- Dependencies between tasks

## Reference Files
- Spec template: [specs/templates/feature-spec-template.md](../../../specs/templates/feature-spec-template.md)
- Planning checklist: [planning-checklist.md](planning-checklist.md)
