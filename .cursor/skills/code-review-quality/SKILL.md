---
name: code-review-quality
description: >-
  Review implemented code for quality, readability, maintainability, performance,
  and security following project standards. Use when reviewing a pull request,
  performing a refactoring pass, doing a code quality audit, or when asked to
  improve code quality, identify technical debt, or optimize existing code.
---

# Code Review & Quality

Systematic review producing actionable, prioritized feedback.

## Review Checklist

Run through each category. For each finding, note severity and location.

### Readability
- [ ] Method names express intent (verb + noun for actions)
- [ ] No method longer than 15 lines — extract if longer
- [ ] No class longer than 200 lines — split by responsibility
- [ ] No deeply nested conditionals (max 2 levels) — use guard clauses
- [ ] Complex logic has a comment explaining *why*, not *what*
- [ ] No "magic numbers" — extract to named constants or enums

### Maintainability
- [ ] Single Responsibility: one reason to change per class/method
- [ ] DRY: no duplicated business logic (but don't over-abstract)
- [ ] Follows project patterns: services for business logic, explicit auth policies, reusable UI components
- [ ] No logic in Flask routes beyond validation/orchestration/response
- [ ] No raw SQL strings unless justified and parameterized
- [ ] Correct module boundaries by domain (`api`, `services`, `repos`, `ui`)

### Testability
- [ ] Dependencies are injectable (not hardcoded inside methods)
- [ ] Side effects isolated in service objects
- [ ] No direct `datetime.now()` without timezone awareness
- [ ] No `rand` without seed — use deterministic alternatives in tests
- [ ] Coverage >80% on new code (`pytest --cov`)

### Performance
- [ ] No N+1 queries — use `includes`, `preload`, or `eager_load`
- [ ] New DB queries on associated records use proper indexes
- [ ] Bulk operations use ORM/native bulk APIs where appropriate
- [ ] Expensive operations (file processing, external API calls) in background jobs
- [ ] No synchronous HTTP calls in request handlers
- [ ] Redis keys have TTL/invalidation strategy and avoid hot-key abuse

### Security (Healthcare Critical)
- [ ] No PII in logs — no `logger.info user.email` etc.
- [ ] Request schema validation enforced on all mutating endpoints
- [ ] Authorization check in every protected endpoint
- [ ] No user-controlled SQL fragments
- [ ] No `send()` or `eval()` with user input
- [ ] Sensitive attributes encrypted at rest
- [ ] Webhook signatures verified before processing

### Stack-Specific
- [ ] Flask blueprints/services structure is respected
- [ ] Next.js components/pages follow app-router conventions
- [ ] Redis usage has key naming, TTL, and safe invalidation
- [ ] API responses are JSON with proper status codes and stable error schema

## Severity Levels

Use these prefixes when reporting findings:

| Severity | Label | Meaning |
|----------|-------|---------|
| Must fix | `[CRITICAL]` | Bug, security issue, or broken functionality — blocks merge |
| Should fix | `[MAJOR]` | Significant quality issue — fix before or shortly after merge |
| Consider | `[MINOR]` | Improvement opportunity — nice to have |
| Note | `[NOTE]` | Observation for future reference, no action required |

## Output Format

For each finding:
```
[SEVERITY] path/to/file.py:line_number
Issue: what is wrong and why it matters
Fix: concrete code suggestion
```

Example:
```
[CRITICAL] app/api/patients.py:23
Issue: Missing authorization check — authenticated user can access foreign tenant data
Fix: Enforce policy check before query and scope by current tenant

[MAJOR] app/services/surveys/assignments.py:45
Issue: N+1 query — related surveys loaded inside loop
Fix: Eager load relationships or fetch in a single query before iteration

[MINOR] app/services/patient_steps.py:78
Issue: Method is 28 lines and mixes validation + side effects
Fix: Split into `validate_input` and `send_completion_notification`
```

## Additional Standards

See [standards.md](standards.md) for detailed metrics and thresholds.
