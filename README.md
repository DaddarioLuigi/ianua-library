# Ianuacare

Healthcare-oriented **Python** library for data pipelines and AI inference: authentication, validation, orchestration, audit-friendly logging, and pluggable storage.

## Install

```bash
pip install -e ".[dev]"
```

## Documentation

See the [`docs/`](docs/) folder: [index](docs/index.md), [architecture](docs/architecture.md), [getting started](docs/getting-started.md), [API reference](docs/api-reference.md), [extending](docs/extending.md).

## Quick example

```python
from ianuacare import (
    AIProvider,
    AuditService,
    DataManager,
    DataParser,
    DataValidator,
    InMemoryBucketClient,
    InMemoryDatabaseClient,
    NLPModel,
    Orchestrator,
    Pipeline,
    RequestContext,
    User,
    Writer,
)

db = InMemoryDatabaseClient()
bucket = InMemoryBucketClient()
writer = Writer(db, bucket)
provider = AIProvider()
nlp = NLPModel(provider, "clinical-nlp-v1")
pipe = Pipeline(
    DataManager(),
    DataValidator(),
    writer,
    Orchestrator(DataParser(), {"nlp": nlp}, default_model_key="nlp"),
    AuditService(db),
)
ctx = RequestContext(User("u1", "clinician", ["pipeline:run"]), "ianuacare-demo")
packet = pipe.run({"text": "example"}, ctx)
```

## License

MIT
