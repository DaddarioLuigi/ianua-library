---
name: incremental-implementation
description: >-
  Implement features incrementally using a test-first, Red-Green-Refactor cycle
  for Python/Flask backends and React/Next.js frontends.
---

# Incremental Implementation

Implements one task at a time following TDD: write failing tests, implement minimum code, refactor.

## Cycle (repeat per task/issue)

### 1. Setup
```bash
git checkout main && git pull origin main
git checkout -b feat/<issue-number>-<short-description>
```

### 2. Write Failing Tests (Red)
Write tests BEFORE implementation:
- Identify the smallest testable behavior
- Write the test describing expected behavior
- Run and confirm the test fails: `pytest <test_file>`
- Never write tests that pass without implementation code

### 3. Implement Minimum Code (Green)
- Write only the code needed to make tests pass
- No premature optimization
- No gold-plating (YAGNI)
- Follow project patterns: services for business logic, explicit auth checks for authorization

### 4. Refactor (while tests stay green)
Apply improvements:
- Extract methods >15 lines
- Remove duplication
- Improve naming
- Ensure single responsibility
- Run tests after each refactor: `pytest <test_file>`

### 5. Local Validation
Run this sequence before committing:

```bash
pytest tests/path/to/changed_test.py
pytest --cov=app --cov-fail-under=80
ruff check app tests
mypy app
bandit -r app
pnpm lint && pnpm typecheck && pnpm test
```

If Redis behavior changed, add targeted checks for key TTL, invalidation, and concurrency race conditions.

### 6. Commit (Conventional Commits)
```bash
cz commit
# or
git commit -m "feat(api): add patient search endpoint"
git commit -m "test(api): add endpoint integration coverage"
```

Max 200 lines of non-test code per commit. If larger, split into sub-tasks.

### 7. Push and Open PR
```bash
git push -u origin HEAD

gh pr create \
  --title "feat(pathways): add step position validation" \
  --body "Closes #42"
```

## Increment Size Rules

- **Max 200 lines** of non-test code per increment
- **Max 1 migration** per increment (multiple column additions are ok)
- If a task is too large → split into sub-tasks, create sub-issues

## Implementation Order (within a feature)

```
1. Migration → model test → model
2. Service test → service
3. Auth/permission test → auth rule
4. API integration test → route + handler
5. Frontend component test → component/page
6. E2E test
7. OpenAPI spec (if API endpoint)
```

## Common Patterns

**New Service**:
```python
class MyService:
    def __init__(self, repo):
        self.repo = repo

    def call(self, *, record_id: int) -> dict:
        # implement
        ...
```

**Permission Check**:
```python
def can_manage_record(user, record) -> bool:
    return user.is_admin or (user.is_manager and record.org_id == user.org_id)
```

**API Test**:
```python
def test_get_things_returns_ok(client, auth_headers):
    response = client.get("/api/v1/things", headers=auth_headers)
    assert response.status_code == 200
```
