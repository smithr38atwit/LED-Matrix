from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.app.services.manager import DisplayManager
from backend.app.services.registry import DisplayRegistry


@dataclass
class AppState:
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    registry: DisplayRegistry | None = None
    manager: DisplayManager | None = None
