from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from backend.app.api import router as api_router
from backend.app.services.manager import DisplayManager
from backend.app.services.persistence import RuntimeStateStore
from backend.app.services.registry import DisplayRegistry
from backend.app.services.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI):
    project_root = Path(__file__).resolve().parent.parent.parent
    registry = DisplayRegistry(project_root=project_root)
    state_store = RuntimeStateStore(project_root / "runtime" / "state.json")
    manager = DisplayManager(registry=registry, state_store=state_store, project_root=project_root)

    app.state.runtime = AppState(registry=registry, manager=manager)
    try:
        yield
    finally:
        manager.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        title="LED Matrix Control API",
        description=(
            "Backend control plane for LED matrix displays. "
            "Use this API via /docs to list displays and control active display state."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(api_router)

    return app


app = create_app()
