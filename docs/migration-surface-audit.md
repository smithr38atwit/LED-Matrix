# Migration Surface Audit

This document records the current migration surface after Flask removal and backend restructuring.

## Objective

Keep the repository legible while the FastAPI backend and managed display runtime continue to evolve.

## Current Runtime Summary

- [main.py](../main.py) starts the FastAPI backend.
- [backend/app/main.py](../backend/app/main.py) builds the app and initializes runtime services.
- [backend/app/api/displays.py](../backend/app/api/displays.py) exposes display start, stop, and switch endpoints.
- [backend/app/runtime/manager.py](../backend/app/runtime/manager.py) enforces one active display and subprocess lifecycle.
- [backend/app/runtime/registry.py](../backend/app/runtime/registry.py) provides explicit display registration.
- Deployments remain rsync-based through [.vscode/tasks.json](../.vscode/tasks.json).
- Raspberry Pi setup still depends on [rgb-matrix.sh](../rgb-matrix.sh).

## Display Classification

| Display             | Status              | MVP Role          | File                                                                                            |
| ------------------- | ------------------- | ----------------- | ----------------------------------------------------------------------------------------------- |
| weather             | Active              | Keep              | [displays/active/weather.py](../displays/active/weather.py)                                     |
| text_scroll         | Active              | Keep              | [displays/active/text_scroll.py](../displays/active/text_scroll.py)                             |
| meetings            | Inactive but viable | Keep with caveats | [displays/active/meetings.py](../displays/active/meetings.py)                                   |
| sports_display      | Experimental        | Defer             | [displays/active/sports_display.py](../displays/active/sports_display.py)                       |
| news                | Broken              | Exclude           | [displays/active/news.py](../displays/active/news.py)                                           |
| sports_display_test | Test-only           | Exclude           | [displays/experimental/sports_display_test.py](../displays/experimental/sports_display_test.py) |
| test                | Test-only           | Exclude           | [displays/experimental/test.py](../displays/experimental/test.py)                               |

## Assets And External Dependencies

| Surface                                                                                   | Status                       | Used By                             |
| ----------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------- |
| [displays/assets/weather/weather-icons.bmp](../displays/assets/weather/weather-icons.bmp) | Required                     | weather                             |
| [displays/assets/sports/logos_24x24](../displays/assets/sports/logos_24x24)               | Deferred                     | sports_display, sports_display_test |
| `rpi-rgb-led-matrix/fonts/7x13.bdf`                                                       | Required external dependency | text_scroll, meetings               |
| `rpi-rgb-led-matrix/fonts/9x15.bdf`                                                       | Required external dependency | weather                             |
| `credentials.json` and `token.json`                                                       | Required external secrets    | meetings                            |

## Operational Files And Migration Relevance

| File                                                                  | Status                   | Why It Matters                              |
| --------------------------------------------------------------------- | ------------------------ | ------------------------------------------- |
| [main.py](../main.py)                                                 | Active entrypoint        | Launches FastAPI backend.                   |
| [backend/app/main.py](../backend/app/main.py)                         | Active runtime bootstrap | App factory and lifespan wiring.            |
| [backend/app/runtime/manager.py](../backend/app/runtime/manager.py)   | Active display lifecycle | Start, stop, and switch process control.    |
| [backend/app/runtime/registry.py](../backend/app/runtime/registry.py) | Active display catalog   | Explicit display metadata and script paths. |
| [pyproject.toml](../pyproject.toml)                                   | Active dependency source | uv-managed dependency definitions.          |
| [uv.lock](../uv.lock)                                                 | Active lockfile          | Pinned reproducible dependency graph.       |
| [README.md](../README.md)                                             | Active documentation     | User-facing run and control guidance.       |

## Known Gaps Carried Forward

- Some displays still rely on hardcoded paths and values.
- Meetings display still has interactive OAuth flow constraints.
- Sports and news displays remain non-MVP quality.

## Handoff

Use this audit and [docs/display-inventory.yaml](./display-inventory.yaml) as the current source of truth for retained vs deferred display surface.
