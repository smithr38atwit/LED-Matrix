from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api import router as api_router
from backend.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = AppState()
    yield


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
