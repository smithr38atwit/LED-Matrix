import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from backend.errors import DisplayNotControllableError
from backend.persistence import PersistedRuntimeState, RuntimeStateStore
from backend.registry import DisplayRegistry


@dataclass
class DisplayRuntimeStatus:
    active_display_id: str | None
    last_selected_display_id: str | None
    active_pid: int | None
    last_exit_code: int | None


class DisplayManager:
    def __init__(
        self,
        registry: DisplayRegistry,
        state_store: RuntimeStateStore,
        project_root: Path,
        stop_timeout_seconds: float = 5.0,
    ):
        self._registry = registry
        self._state_store = state_store
        self._project_root = project_root
        self._stop_timeout_seconds = stop_timeout_seconds

        self._process: subprocess.Popen | None = None
        self._active_display_id: str | None = None
        self._last_selected_display_id: str | None = None
        self._last_exit_code: int | None = None

        self._load_persisted_state()

    def get_status(self) -> DisplayRuntimeStatus:
        self._refresh_process_state()
        return DisplayRuntimeStatus(
            active_display_id=self._active_display_id,
            last_selected_display_id=self._last_selected_display_id,
            active_pid=self._process.pid if self._process else None,
            last_exit_code=self._last_exit_code,
        )

    def start_display(self, display_id: str, params: dict[str, Any] | None = None) -> DisplayRuntimeStatus:
        self._refresh_process_state()

        display = self._registry.get_display(display_id)
        if not display.supports_control:
            raise DisplayNotControllableError(display_id)

        # Idempotent start when target display is already running.
        if self._active_display_id == display_id and self._process and self._process.poll() is None:
            return self.get_status()

        if self._process and self._process.poll() is None:
            self.stop_display(self._active_display_id)

        script_path = self._registry.resolve_script_path(display_id)
        command = self._build_command(script_path=script_path, params=params or {})
        self._process = subprocess.Popen(
            command,
            cwd=str(self._project_root),
            stdout=None,
            stderr=None,
        )

        self._active_display_id = display_id
        self._last_selected_display_id = display_id
        self._last_exit_code = None
        self._save_state()
        return self.get_status()

    def stop_display(self, display_id: str | None) -> DisplayRuntimeStatus:
        self._refresh_process_state()

        # Idempotent stop when nothing is running.
        if not self._process:
            return self.get_status()

        if display_id and self._active_display_id != display_id:
            return self.get_status()

        process = self._process
        process.terminate()
        try:
            process.wait(timeout=self._stop_timeout_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=self._stop_timeout_seconds)

        self._last_exit_code = process.returncode
        self._process = None
        self._active_display_id = None
        self._save_state()
        return self.get_status()

    def switch_display(self, display_id: str, params: dict[str, Any] | None = None) -> DisplayRuntimeStatus:
        self.stop_display(self._active_display_id)
        return self.start_display(display_id=display_id, params=params)

    def shutdown(self) -> DisplayRuntimeStatus:
        """Stop the active display when the backend process is shutting down."""
        return self.stop_display(self._active_display_id)

    def _refresh_process_state(self) -> None:
        if not self._process:
            return

        exit_code = self._process.poll()
        if exit_code is None:
            return

        self._last_exit_code = exit_code
        self._process = None
        self._active_display_id = None
        self._save_state()

    def _build_command(self, script_path: Path, params: dict[str, Any]) -> list[str]:
        command: list[str] = [sys.executable, str(script_path)]

        for key, value in params.items():
            if key == "args" and isinstance(value, list):
                command.extend(str(item) for item in value)
                continue

            flag = f"--{key.replace('_', '-')}"

            if isinstance(value, bool):
                if value:
                    command.append(flag)
                continue

            if isinstance(value, list):
                for item in value:
                    command.extend([flag, str(item)])
                continue

            command.extend([flag, str(value)])

        return command

    def _load_persisted_state(self) -> None:
        persisted = self._state_store.load()
        # A process cannot be safely reconstructed on restart, so only restore intent.
        self._active_display_id = None
        self._last_selected_display_id = persisted.last_selected_display_id or persisted.active_display_id
        self._last_exit_code = None
        self._save_state()

    def _save_state(self) -> None:
        self._state_store.save(
            PersistedRuntimeState(
                active_display_id=self._active_display_id,
                last_selected_display_id=self._last_selected_display_id,
            )
        )
