from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_display_manager, get_runtime_state
from backend.app.models.api import HealthResponse
from backend.app.services.manager import DisplayManager
from backend.app.services.state import AppState

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health(
    runtime: AppState = Depends(get_runtime_state),
    manager: DisplayManager = Depends(get_display_manager),
) -> HealthResponse:
    now = datetime.now(UTC)
    uptime_seconds = int((now - runtime.started_at).total_seconds())
    status = manager.get_status()
    return HealthResponse(uptime_seconds=uptime_seconds, active_display_id=status.active_display_id)
