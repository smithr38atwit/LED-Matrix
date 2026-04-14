from pathlib import Path

from backend.errors import DisplayNotFoundError
from backend.models import DisplayInfo, DisplayStability


class DisplayRegistry:
    def __init__(self, project_root: Path):
        self._project_root = project_root
        self._displays = self._build_default_displays()
        self._display_map = {display.id: display for display in self._displays}

    def list_displays(self) -> list[DisplayInfo]:
        return list(self._displays)

    def get_display(self, display_id: str) -> DisplayInfo:
        display = self._display_map.get(display_id)
        if display is None:
            raise DisplayNotFoundError(display_id)
        return display

    def resolve_script_path(self, display_id: str) -> Path:
        display = self.get_display(display_id)
        return self._project_root / display.module_path

    def _build_default_displays(self) -> list[DisplayInfo]:
        return [
            DisplayInfo(
                id="text_scroll",
                name="Text Scroll",
                module_path="web/displays/text_scroll.py",
                stability=DisplayStability.stable,
                supports_control=True,
                notes="CLI args supported for text/color/speed",
            ),
            DisplayInfo(
                id="weather",
                name="Weather",
                module_path="web/displays/weather.py",
                stability=DisplayStability.stable,
                supports_control=True,
                notes="Uses Open-Meteo and icon assets",
            ),
            DisplayInfo(
                id="sports_display",
                name="Sports Display",
                module_path="web/displays/sports_display.py",
                stability=DisplayStability.experimental,
                supports_control=True,
                notes="Kept for migration parity, known behavior gaps",
            ),
            DisplayInfo(
                id="meetings",
                name="Meetings",
                module_path="web/displays/meetings.py",
                stability=DisplayStability.experimental,
                supports_control=True,
                notes="Requires Google credentials and daemonization refinements",
            ),
            DisplayInfo(
                id="news",
                name="News",
                module_path="web/displays/news.py",
                stability=DisplayStability.broken,
                supports_control=False,
                notes="Retained for now; currently incomplete",
            ),
            DisplayInfo(
                id="sports_display_test",
                name="Sports Display Test",
                module_path="web/displays/sports_display_test.py",
                stability=DisplayStability.test_only,
                supports_control=False,
                notes="Retained non-production test script",
            ),
            DisplayInfo(
                id="test",
                name="Test",
                module_path="web/displays/test.py",
                stability=DisplayStability.test_only,
                supports_control=False,
                notes="Retained non-production test script",
            ),
        ]
