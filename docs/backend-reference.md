# Backend Reference

This is the single source of truth for the current backend runtime.

## Entry Points

- API server: `main.py`
- App factory and lifespan: `backend/app/main.py`

## Core Components

- Routes: `backend/app/api`
- Dependency wiring: `backend/app/dependencies.py`
- Services: `backend/app/services`
  - `registry.py`: explicit display catalog and metadata
  - `manager.py`: start/stop/switch lifecycle, single-active invariant, and startup restore of the last selected controllable display
  - `persistence.py`: runtime state persisted at `runtime/state.json`
  - `errors.py`: display control domain errors
  - `state.py`: app-scoped runtime container

## API Endpoints

- `GET /health`
  - Returns backend status and current active display.
- `GET /displays`
  - Lists known displays and active display ID.
- `POST /displays/{display_id}/start`
  - Starts requested display if controllable.
- `POST /displays/{display_id}/stop`
  - Stops requested display if active.
- `POST /displays/{display_id}/switch`
  - Switches active display to requested target.

Common API error codes:

- `display_not_found`
- `display_not_controllable`

## Display Surface

- Production-intent: `displays/active`
- Non-production/test harnesses: `displays/experimental`

Current status by display ID:

- Stable: `weather`, `text_scroll`
- Experimental: `meetings`, `sports_display`
- Non-controllable: `news`, `sports_display_test`, `test`

## Test Strategy (Regression Guardrails)

Tests focus on intent, not implementation details:

- API intent tests: success/failure contract and control flow behavior
- Manager intent tests: single-active invariant, idempotent stop, and startup restore behavior

Run all tests:

```bash
uv run pytest -q
```
