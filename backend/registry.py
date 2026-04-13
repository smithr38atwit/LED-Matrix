from backend.models import DisplayInfo, DisplayStability


def list_displays() -> list[DisplayInfo]:
    """Return all known displays from the current repository surface.

    This is intentionally static in Step 2 so endpoint contracts can stabilize
    before adding the full DisplayRegistry/DisplayManager runtime in later steps.
    """

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
