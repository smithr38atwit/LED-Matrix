from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class AppState:
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    active_display_id: str | None = None
