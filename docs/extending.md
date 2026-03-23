# Extending Ianuacare

## Custom AI models

Subclass `BaseAIModel` and register instances in `Orchestrator`:

```python
from ianuacare.ai.base import BaseAIModel

class VisionModel(BaseAIModel):
    def run(self, payload: object) -> dict:
        # load image refs from payload, call your vision API, return structured output
        return {"labels": []}

orch = Orchestrator(
    DataParser(),
    {"vision": VisionModel(), "nlp": nlp_model},
    default_model_key="nlp",
)
```

Then set `RequestContext(..., metadata={"model_key": "vision"})` when routing to that model.

## Custom parsing

Subclass `DataParser` and override `_parse_impl` for schema validation, FHIR normalization, etc.:

```python
class FhirParser(DataParser):
    def _parse_impl(self, validated: object) -> dict:
        # return a normalized structure
        return {"resource": validated}
```

## Custom validation

Subclass `DataValidator` and override `_coerce_validated` or `validate` to integrate Pydantic/Marshmallow schemas and raise `ValidationError` with clear messages (avoid echoing PHI in error strings in production).

## Production storage

Implement `DatabaseClient` and `BucketClient` with your drivers (e.g. SQLAlchemy, boto3). Keep **collection names** and key conventions consistent with your retention and backup policies.

`Writer` uses blob keys of the form:

`{product}/{user_id}/{phase}/{request_id}`

Ensure `request_id` is set (automatically by `DataManager.collect()`).

## Authentication in API layers

Call `AuthService.authenticate()` on incoming tokens, then `authorize()` for the permission required by the endpoint (e.g. `pipeline:run`), then build `RequestContext` and call `Pipeline.run()`.

## Audit and compliance

- Treat `AuditService.log_event` as **operational** metadata: user id, product, event name, correlation ids.
- For regulatory audit trails, combine this with immutable storage and access controls outside this library.
