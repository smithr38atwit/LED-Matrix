from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.dependencies import get_display_manager, get_registry
from backend.app.models.api import (
    DisplayControlAction,
    DisplayControlRequest,
    DisplayControlResponse,
    DisplayListResponse,
    ErrorResponse,
)
from backend.app.services.errors import (
    DisplayNotControllableError,
    DisplayNotFoundError,
)
from backend.app.services.manager import DisplayManager
from backend.app.services.registry import DisplayRegistry

router = APIRouter()


@router.get("", response_model=DisplayListResponse)
def get_displays(
    registry: DisplayRegistry = Depends(get_registry),
    manager: DisplayManager = Depends(get_display_manager),
) -> DisplayListResponse:
    status_state = manager.get_status()
    return DisplayListResponse(displays=registry.list_displays(), active_display_id=status_state.active_display_id)


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
    manager: DisplayManager = Depends(get_display_manager),
) -> DisplayControlResponse:
    previous = manager.get_status().active_display_id
    try:
        status_state = manager.start_display(display_id=display_id, params=request.params)
    except DisplayNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        ) from exc
    except DisplayNotControllableError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                code="display_not_controllable",
                message="Display is registered but not controllable in backend",
                details={"display_id": display_id},
            ).model_dump(),
        ) from exc

    return DisplayControlResponse(
        action=DisplayControlAction.start,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=status_state.active_display_id,
        message="Display manager started or confirmed running display.",
    )


@router.post(
    "/{display_id}/stop",
    response_model=DisplayControlResponse,
    responses={404: {"model": ErrorResponse}},
)
def stop_display(
    display_id: str,
    manager: DisplayManager = Depends(get_display_manager),
    registry: DisplayRegistry = Depends(get_registry),
) -> DisplayControlResponse:
    try:
        registry.get_display(display_id)
    except DisplayNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        ) from exc

    previous = manager.get_status().active_display_id
    status_state = manager.stop_display(display_id=display_id)

    return DisplayControlResponse(
        action=DisplayControlAction.stop,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=status_state.active_display_id,
        message="Display manager stopped display if it was active.",
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
    manager: DisplayManager = Depends(get_display_manager),
) -> DisplayControlResponse:
    previous = manager.get_status().active_display_id
    try:
        status_state = manager.switch_display(display_id=display_id, params=request.params)
    except DisplayNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="display_not_found", message="Unknown display id").model_dump(),
        ) from exc
    except DisplayNotControllableError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                code="display_not_controllable",
                message="Display is registered but not controllable in backend",
                details={"display_id": display_id},
            ).model_dump(),
        ) from exc

    return DisplayControlResponse(
        action=DisplayControlAction.switch,
        target_display_id=display_id,
        previous_display_id=previous,
        active_display_id=status_state.active_display_id,
        message="Display manager switched active display.",
    )
