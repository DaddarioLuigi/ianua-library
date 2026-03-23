# Ianuacare

**Ianuacare** is a Python library for building **healthcare** products that need a consistent
**data pipeline**: authenticate users, validate input, persist artifacts, run **AI inference**
behind a stable abstraction, and record **audit events** without mixing protected health
information (PHI) into logs.

## Goals

- **Composable**: inject storage clients, models, and validators for each product.
- **Typed**: Python 3.12+ type hints throughout; friendly to static analysis.
- **Safe by design**: audit helpers emphasize **no PHI in log payloads**; callers remain
  responsible for encryption and access control in production.

## Contents

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | Components, relationships, data flow |
| [Getting started](getting-started.md) | Install, minimal example |
| [API reference](api-reference.md) | Public classes and methods |
| [Extending](extending.md) | Custom models, storage, validation |

## Repository layout

- **Package**: `src/ianuacare/`
- **Tests**: `tests/unit/`, `tests/integration/`
- **This documentation**: `docs/`

## License

MIT (see project README).
