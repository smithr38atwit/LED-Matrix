from fastapi import APIRouter

from backend.api.displays import router as displays_router
from backend.api.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(displays_router, prefix="/displays", tags=["displays"])
