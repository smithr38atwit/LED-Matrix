from fastapi import APIRouter, Depends, HTTPException, status

from backend.dependencies import get_runtime_state
from backend.models import (
    DisplayControlAction,
    DisplayControlRequest,
    DisplayControlResponse,
    DisplayListResponse,
    ErrorResponse,
)
from backend.registry import list_displays
from backend.state import AppState

router = APIRouter()


@router.get("", response_model=DisplayListResponse)
def get_displays(runtime: AppState = Depends(get_runtime_state)) -> DisplayListResponse:
    return DisplayListResponse(displays=list_displays(), active_display_id=runtime.active_display_id)


@router.post(
    "/{display_id}/start",
    response_model=DisplayControlResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def start_display(
    display_id: str,
    request: DisplayControlRequest,
    runtime: AppState = Depends(get_runtime_state),
) -> DisplayControlResponse:
    _ = request
    display_map = {display.id: display for display in list_displays()}

    if display_id not in display_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        )

    target = display_map[display_id]
    if not target.supports_control:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                code="display_not_controllable",
                message="Display is registered but not controllable in backend yet",
                details={"display_id": display_id},
            ).model_dump(),
        )

    previous = runtime.active_display_id
    runtime.active_display_id = display_id
    return DisplayControlResponse(
        action=DisplayControlAction.start,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=runtime.active_display_id,
        message="Contract stub: runtime manager wiring arrives in a later step.",
    )


@router.post(
    "/{display_id}/stop",
    response_model=DisplayControlResponse,
    responses={404: {"model": ErrorResponse}},
)
def stop_display(display_id: str, runtime: AppState = Depends(get_runtime_state)) -> DisplayControlResponse:
    display_ids = {display.id for display in list_displays()}
    if display_id not in display_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        )

    previous = runtime.active_display_id
    if runtime.active_display_id == display_id:
        runtime.active_display_id = None

    return DisplayControlResponse(
        action=DisplayControlAction.stop,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=runtime.active_display_id,
        message="Contract stub: runtime manager wiring arrives in a later step.",
    )


@router.post(
    "/{display_id}/switch",
    response_model=DisplayControlResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def switch_display(
    display_id: str,
    request: DisplayControlRequest,
    runtime: AppState = Depends(get_runtime_state),
) -> DisplayControlResponse:
    _ = request
    display_map = {display.id: display for display in list_displays()}

    if display_id not in display_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        )

    target = display_map[display_id]
    if not target.supports_control:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                code="display_not_controllable",
                message="Display is registered but not controllable in backend yet",
                details={"display_id": display_id},
            ).model_dump(),
        )

    previous = runtime.active_display_id
    runtime.active_display_id = display_id
    return DisplayControlResponse(
        action=DisplayControlAction.switch,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=runtime.active_display_id,
        message="Contract stub: runtime manager wiring arrives in a later step.",
    )
