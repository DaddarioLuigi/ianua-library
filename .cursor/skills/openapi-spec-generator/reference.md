# OpenAPI Generator Reference

## File Locations

| File | Purpose |
|------|---------|
| `specs/api/openapi.yml` | Root document — info, servers, security, $ref paths |
| `specs/api/paths/<resource>.yml` | Per-resource endpoint definitions |
| `specs/api/schemas/<model>.yml` | Reusable model schemas |
| `specs/api/schemas/error.yml` | Standard error schemas |

## Naming Conventions

| Concept | Convention | Example |
|---------|-----------|---------|
| operationId | camelCase, verb+noun | `listPatients`, `createSession` |
| Tag | PascalCase, plural | `Patients`, `Sessions` |
| Schema name | PascalCase | `Patient`, `Session`, `ValidationError` |
| Path parameter | snake_case or id | `id`, `patient_id` |
| Query parameter | snake_case | `from`, `to`, `page` |

## Authentication

```yaml
# In openapi.yml components:
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer

# On each operation:
security:
  - bearerAuth: []
```

## Common Parameters

**Pagination**:
```yaml
parameters:
  - name: page
    in: query
    schema:
      type: integer
      minimum: 1
      default: 1
  - name: items
    in: query
    schema:
      type: integer
      minimum: 1
      maximum: 200
      default: 20
```

**Date range filter**:
```yaml
parameters:
  - name: from
    in: query
    schema:
      type: string
      format: date
    description: Start date (inclusive), defaults to 1 month ago
  - name: to
    in: query
    schema:
      type: string
      format: date
    description: End date (inclusive), defaults to tomorrow
```

**ID path parameter**:
```yaml
parameters:
  - name: id
    in: path
    required: true
    schema:
      type: integer
      format: int64
```

## Response Status Codes Reference

| Code | When |
|------|------|
| 200 | GET success, PATCH/PUT success |
| 201 | POST success (resource created) |
| 204 | DELETE success (no body) |
| 400 | Malformed request (invalid date format, etc.) |
| 401 | Missing or invalid Bearer token |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 422 | Validation errors on request body |
| 500 | Internal server error |

## Existing Schemas

Check if a schema already exists before creating a new one:
```bash
ls specs/api/schemas/
```

## Validation Script

Prefer a dedicated validation script:
```python
# scripts/validate_openapi.py
from openapi_spec_validator import validate_spec
import yaml

with open("specs/api/openapi.yml", "r", encoding="utf-8") as f:
    spec = yaml.safe_load(f)

validate_spec(spec)
print("OpenAPI spec is valid")
```
