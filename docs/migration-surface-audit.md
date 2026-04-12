# Migration Surface Audit

This document is the step 1 audit for the LED Matrix roadmap: audit and prepare the migration surface.

It records which parts of the current repository are active, which are worth carrying into the first managed-runtime version, and which should stay out of scope for the MVP. It is intentionally descriptive rather than architectural. The current Flask runtime remains unchanged after this audit.

## Objective

Make the repository legible before backend and frontend migration work starts.

## Current Runtime Summary

- [main.py](../main.py) starts the current Flask app in debug mode on port 5000.
- [web/**init**.py](../web/__init__.py) builds the Flask app and registers the current blueprint.
- [web/views.py](../web/views.py) discovers displays by listing every top-level `.py` file in `web/displays` and launches the selected script with `Popen(["python3", script_path])`.
- Only one child process is tracked at a time through the in-memory `CURRENT_PROCESS` global in [web/views.py](../web/views.py).
- Deployments are currently rsync-based through [.vscode/tasks.json](../.vscode/tasks.json).
- Raspberry Pi setup still depends on [rgb-matrix.sh](../rgb-matrix.sh) and an external install of the hzeller RGB matrix library.

## Important Temporary Constraint

The current Flask UI still exposes every top-level Python file in `web/displays`, including deferred and test-only scripts. This audit defines the intended MVP surface, but step 1 does not change the current launcher behavior.

## Display Classification

| Display                                                                       | Status              | MVP Role          | Notes                                                                                                                                                                         |
| ----------------------------------------------------------------------------- | ------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [web/displays/weather.py](../web/displays/weather.py)                         | Active              | Keep              | Actively used. Depends on Open-Meteo, `icons/weather-icons.bmp`, and hardcoded location/matrix settings.                                                                      |
| [web/displays/text_scroll.py](../web/displays/text_scroll.py)                 | Active              | Keep              | Actively used. Good candidate for migration once matrix config and font path are centralized.                                                                                 |
| [web/displays/meetings.py](../web/displays/meetings.py)                       | Inactive but viable | Keep with caveats | Google Calendar display. Not used currently, but worth preserving. Needs OAuth file handling cleanup and removal of interactive `input()` loop before unattended runtime use. |
| [web/displays/sports_display.py](../web/displays/sports_display.py)           | Experimental        | Defer             | ESPN integration and logo assets exist, but implementation is incomplete for MVP use. Hardcoded Houston filter, fragile assumptions, and no real score rendering.             |
| [web/displays/news.py](../web/displays/news.py)                               | Broken              | Exclude           | Incomplete scraper with missing imports and no matrix rendering path.                                                                                                         |
| [web/displays/test.py](../web/displays/test.py)                               | Test-only           | Exclude           | Console loop only. Useful only as a process-control smoke test.                                                                                                               |
| [web/displays/sports_display_test.py](../web/displays/sports_display_test.py) | Test-only           | Exclude           | Developer harness, not a production display.                                                                                                                                  |

## Asset And External Dependency Classification

| Surface                                               | Status                       | Used By                                       | Notes                                                                          |
| ----------------------------------------------------- | ---------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| [icons/weather-icons.bmp](../icons/weather-icons.bmp) | Required                     | `weather.py`                                  | Required for the retained weather display.                                     |
| [icons/sport_logos_24x24](../icons/sport_logos_24x24) | Deferred                     | `sports_display.py`, `sports_display_test.py` | Keep for future sports work, but not part of the MVP migration surface.        |
| `rpi-rgb-led-matrix/fonts/7x13.bdf`                   | Required external dependency | `text_scroll.py`, `meetings.py`               | Font path is hardcoded and must be centralized in a later configuration step.  |
| `rpi-rgb-led-matrix/fonts/9x15.bdf`                   | Required external dependency | `weather.py`                                  | External font dependency for weather display.                                  |
| `credentials.json`                                    | Required external secret     | `meetings.py`                                 | Not stored in the repo. User-managed on the Raspberry Pi or local workstation. |
| `token.json`                                          | Generated external secret    | `meetings.py`                                 | OAuth token generated at runtime and not stored in the repo.                   |
| Open-Meteo API                                        | Active external dependency   | `weather.py`                                  | No secret required, but location is hardcoded today.                           |
| ESPN scoreboard API                                   | Deferred external dependency | `sports_display.py`                           | Relevant only if sports display returns to scope.                              |

## Operational Files And Migration Relevance

| File                                        | Status                                  | Why It Matters                                                                                      |
| ------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [main.py](../main.py)                       | Migration reference                     | Captures current app entrypoint and debug-server assumptions.                                       |
| [web/**init**.py](../web/__init__.py)       | Migration reference                     | Shows the current Flask app factory and placeholder config usage.                                   |
| [web/views.py](../web/views.py)             | Critical migration reference            | Defines the current display discovery and subprocess lifecycle model that later steps must replace. |
| [pyproject.toml](../pyproject.toml)         | Active dependency source                | Current Python dependency definition for the uv-based workflow introduced in step 2.                |
| [uv.lock](../uv.lock)                       | Active lockfile                         | Pinned dependency resolution for reproducible local and Raspberry Pi syncs.                         |
| [.vscode/tasks.json](../.vscode/tasks.json) | Active workflow                         | Shows the current rsync deployment flow and the lingering dev/prod target ambiguity.                |
| [rgb-matrix.sh](../rgb-matrix.sh)           | Active Raspberry Pi bootstrap reference | Documents hardware-library installation expectations that later setup docs must preserve.           |
| [README.md](../README.md)                   | Active documentation                    | Must describe the audited MVP surface instead of treating all displays as equivalent.               |

## Recommended MVP Surface For Later Steps

The first managed-runtime migration should treat these displays as the intended MVP surface:

- [web/displays/weather.py](../web/displays/weather.py)
- [web/displays/text_scroll.py](../web/displays/text_scroll.py)
- [web/displays/meetings.py](../web/displays/meetings.py)

The user confirmed that only weather and text scroll are still in regular use today. Meetings remains worth preserving as a migration candidate, but it should not drive MVP parity decisions until its runtime model is cleaned up.

## Known Blockers Carried Forward

- Display discovery is file-based and currently treats every top-level Python file in `web/displays` as runnable.
- Display lifecycle is controlled by a single in-memory `CURRENT_PROCESS` variable in [web/views.py](../web/views.py).
- Flask runs in debug mode and is not a durable service model for Raspberry Pi operation.
- Matrix options, font paths, asset paths, coordinates, and team selections are hardcoded inside individual scripts.
- Secrets and OAuth material for meetings are manual, local files.
- Deployment still assumes manual rsync and occasional SSH/tmux usage.

## Local Work Completed By This Audit

- Classified the current display surface.
- Identified which assets and external dependencies are part of the MVP.
- Marked the current Flask/process model as migration reference rather than future architecture.
- Updated repository guidance to point future work at this audit.

## Raspberry Pi Work Still Owned By The User

- Keep the external matrix library installed and working on the Pi.
- Preserve any local secrets or OAuth files needed for retained displays.
- Perform hardware verification for retained displays on the actual matrix.

## Validation Checklist

- Every top-level file in `web/displays` has one status bucket and rationale.
- The audit separates retained, deferred, broken, and test-only displays.
- Required assets and external files are listed explicitly.
- Current operational assumptions are documented without changing runtime behavior.

## Handoff To Implementation Agent

If you start step 2, step 3, step 5, or step 6, use this document and [docs/display-inventory.yaml](./display-inventory.yaml) as the source of truth for what belongs in the migration surface.

Do not begin by expanding the display list. Start from the retained displays, then treat deferred or excluded displays as follow-up work only if the user explicitly reopens scope.
