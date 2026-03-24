# Getting started

## Requirements

- Python **3.12+**

## Install

From the repository root:

```bash
pip install -e ".[dev]"
```

## Minimal example

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
    data_manager=DataManager(),
    validator=DataValidator(),
    writer=writer,
    orchestrator=Orchestrator(
        DataParser(),
        {"nlp": nlp},
        default_model_key="nlp",
    ),
    audit_service=AuditService(db),
)

ctx = RequestContext(
    User("u1", "clinician", ["pipeline:run"]),
    "my-product",
    metadata={"model_key": "nlp"},
)
packet = pipe.run({"text": "example input"}, ctx)
print(packet.inference_result)
```

## Run tests

```bash
pytest

# With coverage (matches CI expectations)
pytest --cov=ianuacare --cov-report=term-missing
```

## Lint and types

```bash
ruff check src tests
mypy src
```

## Next steps

- Read [API reference](api-reference.md) for class details.
- Read [Preconfigurations](preconfigurations.md) for production-ready adapters.
- Read [Extending](extending.md) to add custom models and validation.
