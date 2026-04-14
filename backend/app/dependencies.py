from fastapi import Request

from backend.app.services.manager import DisplayManager
from backend.app.services.registry import DisplayRegistry
from backend.app.services.state import AppState


def get_runtime_state(request: Request) -> AppState:
    runtime = getattr(request.app.state, "runtime", None)
    if runtime is None:
        runtime = AppState()
        request.app.state.runtime = runtime
    return runtime


def get_registry(request: Request) -> DisplayRegistry:
    runtime = get_runtime_state(request)
    if runtime.registry is None:
        raise RuntimeError("Display registry not initialized")
    return runtime.registry


def get_display_manager(request: Request) -> DisplayManager:
    runtime = get_runtime_state(request)
    if runtime.manager is None:
        raise RuntimeError("Display manager not initialized")
    return runtime.manager
