# API reference

Public symbols are re-exported from `ianuacare` (`from ianuacare import ...`).

## Domain models

### `User`

- `user_id: str`
- `role: str`
- `permissions: list[str]`

### `RequestContext`

- `user: User`
- `product: str`
- `metadata: dict` — use for **non-PHI** routing keys (e.g. `model_key`).

### `DataPacket`

Mutable pipeline state:

- `raw_data`, `parsed_data`, `validated_data`, `processed_data`, `inference_result`
- `metadata: dict` — includes `request_id`, `product`, `user_id` after `DataManager.collect()`.

## Exceptions (`IanuacareError`)

- `IanuacareError` — base; has `message` and `code`.
- `AuthenticationError`, `AuthorizationError`, `ValidationError`, `OrchestrationError`, `InferenceError`, `StorageError`.

## Auth

### `UserRepository`

- `get_user_by_token(token: str) -> dict` — raises `KeyError` if unknown.
- `register_token(token, user_dict)` — convenience for tests.

### `AuthService`

- `authenticate(token: str) -> User` — raises `AuthenticationError`.
- `authorize(user: User, required_permission: str) -> None` — raises `AuthorizationError`.
- `build_context(user, *, product, metadata=...)` — builds `RequestContext`.

## Pipeline

### `DataManager`

- `collect(input_data, context: RequestContext) -> DataPacket`

### `DataValidator`

- `validate(packet: DataPacket) -> DataPacket` — sets `validated_data`; raises `ValidationError` if `raw_data` is missing (unless `allow_none_raw=True`).

### `Pipeline`

- `run(input_data, context: RequestContext) -> DataPacket` — full pipeline.

## Orchestration

### `DataParser`

- `parse(packet: DataPacket) -> DataPacket` — default copies `validated_data` → `parsed_data`; override `_parse_impl` for custom parsing.

### `Orchestrator`

- `execute(packet, context) -> DataPacket` — parse, select model, run inference, set `processed_data` and `inference_result`.
- `_select_model(context, packet) -> str` — uses `context.metadata["model_key"]`, `packet.metadata["model_key"]`, `default_model_key`, or a single registered model.

## AI

### `BaseAIModel` (abstract)

- `run(payload: Any) -> Any` — implement in subclasses.

### `AIProvider`

- `infer(model_name: str, payload: Any) -> dict` — default echoes payload; replace with HTTP/SDK calls.

### `NLPModel`

- `run(payload) -> Any` — delegates to `provider.infer(model_name, payload)`.

## Storage

### Protocols

- `DatabaseClient`: `write(collection, record) -> dict`, `fetch_all(collection) -> list`
- `BucketClient`: `upload(key, content) -> dict`, `download(key) -> Any`

### Implementations

- `InMemoryDatabaseClient`, `InMemoryBucketClient`

### `Writer`

- `write_raw(packet, context) -> dict`
- `write_processed(packet, context) -> dict`
- `write_result(packet, context) -> dict`
- `write_log(message, context) -> dict` — **message must not contain PHI**.

Raises `StorageError` on failure.

## Audit

### `AuditService`

- `log_event(event_name: str, context: RequestContext, details: dict | None) -> None`

Writes to collection `audit_events`. **Do not** put PHI in `details`.

## Config

### `ConfigService`

- `get(key, default=None) -> Any`
- `set(key, value)` — for tests/dynamic config.
