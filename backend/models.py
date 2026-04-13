from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DisplayStability(str, Enum):
    stable = "stable"
    experimental = "experimental"
    broken = "broken"
    test_only = "test_only"


class DisplayControlAction(str, Enum):
    start = "start"
    stop = "stop"
    switch = "switch"


class ErrorResponse(BaseModel):
    code: str = Field(description="Stable error code identifier")
    message: str = Field(description="Human-readable summary")
    details: dict[str, Any] | None = Field(default=None, description="Optional structured context")


class HealthResponse(BaseModel):
    status: str = Field(default="ok", examples=["ok"])
    uptime_seconds: int = Field(ge=0, description="Seconds since backend startup")
    active_display_id: str | None = Field(default=None)


class DisplayInfo(BaseModel):
    id: str = Field(description="Stable display identifier used in API paths")
    name: str = Field(description="Human-friendly display name")
    module_path: str = Field(description="Python module path or script location")
    stability: DisplayStability = Field(description="Display readiness classification")
    supports_control: bool = Field(description="Whether display is intended to be startable")
    notes: str | None = Field(default=None)


class DisplayListResponse(BaseModel):
    displays: list[DisplayInfo]
    active_display_id: str | None = None


class DisplayControlRequest(BaseModel):
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Display-specific startup parameters. Validation is registry-driven.",
    )


class DisplayControlResponse(BaseModel):
    action: DisplayControlAction
    target_display_id: str
    previous_display_id: str | None = None
    active_display_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message: str
