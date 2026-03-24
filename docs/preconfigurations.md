# Preconfigurations

Ianuacare now ships production-oriented adapters and a vendor-agnostic stack factory.

## Available adapters

### Auth

- `CognitoUserRepository` (`ianuacare.infrastructure.auth`) for Cognito access tokens.

### Storage

- `PostgresDatabaseClient` (`ianuacare.infrastructure.storage`) for JSON payload persistence.
- `S3BucketClient` (`ianuacare.infrastructure.storage`) for blob/object storage.

### AI provider

- `TogetherAIProvider` (`ianuacare.ai.providers`) for Together chat inference.

### Cache and encryption

- `CacheClient` + `InMemoryCacheClient` (`ianuacare.infrastructure.cache`)
- `RedisCacheClient` (`ianuacare.infrastructure.cache.redis`)
- `EncryptionService` + `NoOpEncryption` (`ianuacare.infrastructure.encryption`)
- `KMSEncryptionService` (`ianuacare.infrastructure.encryption.kms`)

### Configuration and logging

- `EnvConfigService` (`ianuacare.core.config`) reads `IANUA_*` environment variables.
- `StructuredLogger` (`ianuacare.core.logging`) emits JSON logs with context fields.

## Generic factory

Use `create_stack()` to wire the framework without vendor lock-in:

```python
from ianuacare import (
    InMemoryBucketClient,
    InMemoryDatabaseClient,
    NLPModel,
    AIProvider,
    UserRepository,
    create_stack,
)

provider = AIProvider()
model = NLPModel(provider, "clinical")

stack = create_stack(
    auth_repository=UserRepository(),
    database=InMemoryDatabaseClient(),
    bucket=InMemoryBucketClient(),
    models={"nlp": model},
    default_model_key="nlp",
)

# stack.pipeline, stack.auth_service, stack.writer, stack.orchestrator
```

For production, pass concrete adapters (Cognito/Postgres/S3/Redis/KMS) instead of in-memory ones.
