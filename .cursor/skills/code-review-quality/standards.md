# Code Quality Standards Reference

Concrete thresholds and metrics for the code-review-quality skill.

## Size Limits

| Unit | Max Lines | Action if exceeded |
|------|-----------|-------------------|
| Method | 15 | Extract to private methods |
| Class | 200 | Split by responsibility (SRP) |
| Route handler | 15 | Move logic to service object |
| Migration | — | One concern per migration file |
| Test case | 25 | Split into multiple tests |

## Complexity

- **Cyclomatic complexity**: max 8 per function
- **Nested conditionals**: max 2 levels deep
- **Method arguments**: max 5 (use keyword args or value objects)

## Test Coverage

| Scope | Minimum |
|-------|---------|
| Overall project | 80% |
| Per file | 70% |
| New code in PR | 80% |
| Critical paths (auth, payments) | 95% |

## Database

### Query Rules
- Always use `includes`/`preload` when iterating associations
- Avoid `select *` in scopes — specify columns
- Use `find_each` for large dataset iteration (not `all.each`)
- Use `insert_all`/`upsert_all` for bulk inserts (not `each { create }`)

### Index Requirements
- Foreign keys must have indexes
- Columns used in `where`, `order`, or `group` must have indexes
- Composite indexes: order matters (most selective column first)

## Flask Conventions

### Routes
```python
# Good: thin endpoint
@bp.post("/patients")
def create_patient():
    payload = CreatePatientSchema.model_validate(request.get_json() or {})
    result = patient_service.create(payload)
    return jsonify(result), 201

# Bad: fat endpoint
@bp.post("/patients")
def create_patient():
    data = request.json
    # validation + db + external calls + formatting all mixed here
    ...
```

### Services
```python
class CheckAutomaticAssignments:
    def __init__(self, repo):
        self.repo = repo

    def call(self, user_id: int) -> None:
        surveys = self.repo.list_eligible_surveys(user_id=user_id)
        for survey in surveys:
            self.repo.assign_user_survey(user_id=user_id, survey_id=survey.id)
```

### Models
```python
# Good: persistence-centric model
class PatientStep(Base):
    __tablename__ = "patient_steps"
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def overdue(self) -> bool:
        return self.due_at is not None and self.due_at < datetime.now(timezone.utc)

# Bad: external side effects in ORM model methods
# -> move to a service/worker
```

## Security Thresholds

| Risk | Threshold | Action |
|------|-----------|--------|
| Bandit high issues | 0 | Block merge |
| pip-audit CVEs | 0 | Block merge |
| npm audit high/critical | 0 | Block merge |
| Unencrypted PII fields | 0 | Immediate fix |
| Missing authorization | 0 | Block merge |
