from pathlib import Path

from backend.app.models.api import DisplayInfo, DisplayStability
from backend.app.services.manager import DisplayManager
from backend.app.services.persistence import RuntimeStateStore
from backend.app.services.registry import DisplayRegistry


class _FakeProcess:
    _next_pid = 1000

    def __init__(self, *_args, **_kwargs) -> None:
        type(self)._next_pid += 1
        self.pid = type(self)._next_pid
        self.returncode = None

    def poll(self):
        return self.returncode

    def terminate(self) -> None:
        self.returncode = 0

    def wait(self, timeout: float | None = None) -> int:
        return 0

    def kill(self) -> None:
        self.returncode = -9


class _TestRegistry(DisplayRegistry):
    def _build_default_displays(self) -> list[DisplayInfo]:
        return [
            DisplayInfo(
                id="weather",
                name="Weather",
                module_path="displays/active/weather.py",
                stability=DisplayStability.stable,
                supports_control=True,
            ),
            DisplayInfo(
                id="news",
                name="News",
                module_path="displays/active/news.py",
                stability=DisplayStability.broken,
                supports_control=False,
            ),
        ]


def _build_manager(tmp_path: Path) -> DisplayManager:
    project_root = Path.cwd()
    store = RuntimeStateStore(tmp_path / "state.json")
    registry = _TestRegistry(project_root=project_root)
    return DisplayManager(registry=registry, state_store=store, project_root=project_root)


def test_manager_keeps_single_active_display(monkeypatch, tmp_path: Path) -> None:
    # Arrange
    monkeypatch.setattr("backend.app.services.manager.subprocess.Popen", _FakeProcess)
    manager = _build_manager(tmp_path)

    # Act
    first = manager.start_display("weather")
    second = manager.start_display("weather")

    # Assert
    assert first.active_display_id == "weather"
    assert second.active_display_id == "weather"
    assert first.active_pid == second.active_pid


def test_manager_stop_is_idempotent_when_nothing_running(tmp_path: Path) -> None:
    # Arrange
    manager = _build_manager(tmp_path)

    # Act
    stopped = manager.stop_display("weather")

    # Assert
    assert stopped.active_display_id is None
    assert stopped.active_pid is None


def test_manager_persists_last_selected_display(monkeypatch, tmp_path: Path) -> None:
    # Arrange
    monkeypatch.setattr("backend.app.services.manager.subprocess.Popen", _FakeProcess)
    manager = _build_manager(tmp_path)

    # Act
    manager.start_display("weather")
    manager.stop_display("weather")

    # Assert
    restored = _build_manager(tmp_path).get_status()
    assert restored.active_display_id is None
    assert restored.last_selected_display_id == "weather"
