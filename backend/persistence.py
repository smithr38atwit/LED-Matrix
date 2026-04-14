import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class PersistedRuntimeState:
    active_display_id: str | None = None
    last_selected_display_id: str | None = None


class RuntimeStateStore:
    def __init__(self, state_file: Path):
        self._state_file = state_file

    def load(self) -> PersistedRuntimeState:
        if not self._state_file.exists():
            return PersistedRuntimeState()

        try:
            raw = json.loads(self._state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return PersistedRuntimeState()

        if not isinstance(raw, dict):
            return PersistedRuntimeState()

        return PersistedRuntimeState(
            active_display_id=raw.get("active_display_id"),
            last_selected_display_id=raw.get("last_selected_display_id"),
        )

    def save(self, state: PersistedRuntimeState) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")
