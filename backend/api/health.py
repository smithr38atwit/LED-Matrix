from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from backend.dependencies import get_runtime_state
from backend.models import HealthResponse
from backend.state import AppState

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health(runtime: AppState = Depends(get_runtime_state)) -> HealthResponse:
    now = datetime.now(UTC)
    uptime_seconds = int((now - runtime.started_at).total_seconds())
    return HealthResponse(uptime_seconds=uptime_seconds, active_display_id=runtime.active_display_id)
