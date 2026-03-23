---
name: openapi-spec-generator
description: >-
  Generate and validate OpenAPI 3.1 specifications for Flask API endpoints.
  Use when creating or updating endpoints, documenting contracts, or writing Swagger/OpenAPI docs.
---

# OpenAPI Spec Generator

Generates and maintains OpenAPI 3.1 specs for every API endpoint.

## Workflow

### Step 1 — Scan the Endpoint
Read:
- Endpoint module: `app/api/<resource>.py` (or equivalent blueprint)
- Route registration: app factory / blueprint registry
- Schema/serializer: request and response models
- Tests: `tests/integration/api/test_<resource>.py` (for examples)

### Step 2 — Generate Path Spec

Create `specs/api/paths/<resource>.yml` following project template.

Key requirements:
- Every action gets its own operationId (camelCase: `listPatients`, `createInvoice`)
- All parameters documented with type, required flag, and description
- All response codes: 200/201, 400, 401, 403, 404, 422, 500 as relevant
- At least one example per response
- Bearer auth on every operation

### Step 3 — Generate/Update Schemas

For each response model, ensure a schema exists in `specs/api/schemas/<model>.yml`.

**Python → OpenAPI Type Mapping**:

| Python | OpenAPI type | format |
|-----------|-------------|--------|
| `string` | `string` | — |
| `integer` | `integer` | `int64` |
| `float` / `Decimal` | `number` | `float` |
| `boolean` | `boolean` | — |
| `date` | `string` | `date` |
| `datetime` | `string` | `date-time` |
| `dict` | `object` | — |
| `list[T]` | `array` | + `items` |
| enum | `string` | + `enum: [values]` |

**Nullable fields**: add `nullable: true` for columns that allow NULL.
**Required fields**: include in `required:` array only non-nullable fields without defaults.

### Step 4 — Register in Root Document

Add the path reference to `specs/api/openapi.yml`:

```yaml
paths:
  /patients:
    $ref: "./paths/patients.yml#/patients"
  /patients/{id}:
    $ref: "./paths/patients.yml#/patient_by_id"
```

Add any new tags to the `tags:` section.

### Step 5 — Validate

```bash
python scripts/validate_openapi.py
```

## Authentication Pattern

All protected API endpoints should declare Bearer token auth:

```yaml
security:
  - bearerAuth: []
```

The `bearerAuth` scheme is defined in `specs/api/openapi.yml` components.

## Standard Error Responses

Always use `$ref` to shared error schemas:

```yaml
"401":
  description: Missing or invalid Bearer token
  content:
    application/json:
      schema:
        $ref: "../schemas/error.yml#/Error"
      example:
        code: "bad_credentials"
"422":
  description: Validation errors
  content:
    application/json:
      schema:
        $ref: "../schemas/error.yml#/ValidationError"
```

## Reference Files

- Root spec: [specs/api/openapi.yml](../../../specs/api/openapi.yml)
- Error schemas: [specs/api/schemas/error.yml](../../../specs/api/schemas/error.yml)
- Template: [specs/templates/api-spec-template.md](../../../specs/templates/api-spec-template.md)
- Type mapping reference: [reference.md](reference.md)
