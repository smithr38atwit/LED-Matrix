from fastapi import Request

from backend.state import AppState


def get_runtime_state(request: Request) -> AppState:
    runtime = getattr(request.app.state, "runtime", None)
    if runtime is None:
        runtime = AppState()
        request.app.state.runtime = runtime
    return runtime
