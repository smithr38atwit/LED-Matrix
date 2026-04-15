from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api import router as api_router
from backend.app.dependencies import (
    get_display_manager,
    get_registry,
    get_runtime_state,
)
from backend.app.models.api import DisplayInfo, DisplayStability
from backend.app.services.errors import (
    DisplayNotControllableError,
    DisplayNotFoundError,
)
from backend.app.services.state import AppState


@dataclass
class _Status:
    active_display_id: str | None


class _FakeRegistry:
    def __init__(self) -> None:
        self._displays = {
            "weather": DisplayInfo(
                id="weather",
                name="Weather",
                module_path="displays/active/weather.py",
                stability=DisplayStability.stable,
                supports_control=True,
            ),
            "news": DisplayInfo(
                id="news",
                name="News",
                module_path="displays/active/news.py",
                stability=DisplayStability.broken,
                supports_control=False,
            ),
        }

    def list_displays(self) -> list[DisplayInfo]:
        return list(self._displays.values())

    def get_display(self, display_id: str) -> DisplayInfo:
        display = self._displays.get(display_id)
        if display is None:
            raise DisplayNotFoundError(display_id)
        return display


class _FakeManager:
    def __init__(self, registry: _FakeRegistry) -> None:
        self.registry = registry
        self.active_display_id: str | None = None

    def get_status(self) -> _Status:
        return _Status(active_display_id=self.active_display_id)

    def start_display(self, display_id: str, params: dict | None = None) -> _Status:
        display = self.registry.get_display(display_id)
        if not display.supports_control:
            raise DisplayNotControllableError(display_id)
        self.active_display_id = display_id
        return self.get_status()

    def stop_display(self, display_id: str | None) -> _Status:
        if display_id is None or display_id == self.active_display_id:
            self.active_display_id = None
        return self.get_status()

    def switch_display(self, display_id: str, params: dict | None = None) -> _Status:
        return self.start_display(display_id=display_id, params=params)


def _build_test_client() -> TestClient:
    app = FastAPI()
    app.include_router(api_router)

    registry = _FakeRegistry()
    manager = _FakeManager(registry)
    runtime_state = AppState(started_at=datetime.now(UTC), registry=registry, manager=manager)

    app.dependency_overrides[get_registry] = lambda: registry
    app.dependency_overrides[get_display_manager] = lambda: manager
    app.dependency_overrides[get_runtime_state] = lambda: runtime_state

    return TestClient(app)


def test_health_reports_service_ok() -> None:
    # Arrange
    client = _build_test_client()

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert isinstance(payload["uptime_seconds"], int)


def test_displays_lists_inventory_and_no_active_initially() -> None:
    # Arrange
    client = _build_test_client()

    # Act
    response = client.get("/displays")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["active_display_id"] is None
    ids = {display["id"] for display in payload["displays"]}
    assert {"weather", "news"}.issubset(ids)


def test_start_unknown_display_returns_not_found() -> None:
    # Arrange
    client = _build_test_client()

    # Act
    response = client.post("/displays/unknown/start", json={"params": {}})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "display_not_found"


def test_start_non_controllable_display_returns_conflict() -> None:
    # Arrange
    client = _build_test_client()

    # Act
    response = client.post("/displays/news/start", json={"params": {}})

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "display_not_controllable"


def test_start_switch_and_stop_follow_operator_intent() -> None:
    # Arrange
    client = _build_test_client()

    # Act
    start = client.post("/displays/weather/start", json={"params": {}})
    switch = client.post("/displays/weather/switch", json={"params": {}})
    stop = client.post("/displays/weather/stop")

    # Assert
    assert start.status_code == 200
    assert start.json()["active_display_id"] == "weather"
    assert switch.status_code == 200
    assert switch.json()["active_display_id"] == "weather"
    assert stop.status_code == 200
    assert stop.json()["active_display_id"] is None
