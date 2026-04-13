# FastAPI Backend Contract (Step 1)

This document defines the initial backend contract for replacing Flask with FastAPI.
It is intentionally strict about display lifecycle behavior so implementation can proceed in small, safe steps.

## Runtime Invariants

1. Exactly one display is active at a time.
2. Start and switch operations update active display ownership atomically from API perspective.
3. Stop is idempotent and safe when no display is active.
4. All existing display modules are retained and listed in registry metadata.
5. Non-production or broken displays remain visible but are marked as not controllable.

## Step 2 Endpoints

- GET /health
  - Returns backend health and active display id.
- GET /displays
  - Returns all known displays and active display id.
- POST /displays/{display_id}/start
  - Contract stub for setting active display state.
- POST /displays/{display_id}/stop
  - Contract stub for clearing active display state when target is active.
- POST /displays/{display_id}/switch
  - Contract stub for replacing active display state.

## Error Contract

Error payload shape:

- code: stable machine-friendly error id
- message: human-readable summary
- details: optional structured context

Known initial error codes:

- display_not_found
- display_not_controllable

## Docs-Driven Manual Testing Flow

1. Run backend service.
2. Open /docs in browser.
3. Call GET /displays and confirm inventory includes all current modules.
4. Call POST /displays/{display_id}/start for controllable display ids.
5. Call GET /health to verify active_display_id changes.
6. Call POST /displays/{display_id}/switch and verify active_display_id update.
7. Call POST /displays/{display_id}/stop and verify active_display_id clears.

## Out Of Scope For Steps 1 and 2

- Real subprocess lifecycle management
- Display parameter adapters and deep validation
- Persisted state restore on restart
- Authentication and frontend integration
