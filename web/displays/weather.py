import time
from datetime import datetime

import openmeteo_requests
import pandas as pd
import requests_cache
from PIL import Image
from retry_requests import retry
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Weather Codes
WEATHER_CODE_MAP = {
    0: "clear",
    1: "partly_cloudy",
    2: "partly_cloudy",
    3: "partly_cloudy",
    45: "fog",
    48: "fog",
    51: "drizzle",
    53: "drizzle",
    55: "drizzle",
    56: "drizzle",
    57: "drizzle",
    61: "rain",
    63: "rain",
    65: "rain",
    66: "rain",
    67: "rain",
    71: "snow",
    73: "snow",
    75: "snow",
    77: "snow",
    80: "rain",
    81: "rain",
    82: "rain",
    85: "snow",
    86: "snow",
    95: "thunder_storms",
    96: "thunder_storms",
    99: "thunder_storms",
}

# Color Constants
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
WHITE = (200, 200, 200)

# Setup LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 2
options.hardware_mapping = "adafruit-hat"

MATRIX = RGBMatrix(options=options)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=60)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
OPENMETEO = openmeteo_requests.Client(session=retry_session)
URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 42.8015,
    "longitude": -70.9898,
    "current": ["temperature_2m", "is_day", "weather_code"],
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "mph",
    "precipitation_unit": "inch",
    "timezone": "America/New_York",
}


# Thread variables
STOP = False
TIME = None
TEMP = None
IS_DAY = None
WEATHER_CODE = None


def load_icons():
    tile_height = 16
    tile_width = 16

    img = Image.open("icons/weather-icons.bmp")
    img_width, img_height = img.size

    day_icons = []
    night_icons = []
    icon_names = [
        "clear",
        "partly_cloudy",
        "cloudy",
        "fog",
        "rain",
        "drizzle",
        "thunder_storms",
        "snow",
        "windy",
    ]
    for top in range(0, img_height, tile_height):
        for left in range(0, img_width, tile_width):
            # Define the box to crop
            right = min(left + tile_width, img_width)
            bottom = min(top + tile_height, img_height)

            # Crop the image to the tile
            icon = img.crop((left, top, right, bottom))
            if left == 0:
                day_icons.append(icon)
            else:
                night_icons.append(icon)

    day_icons = dict(zip(icon_names, day_icons))
    night_icons = dict(zip(icon_names, night_icons))
    return day_icons, night_icons


def display_weather(day_icons, night_icons):
    canvas = MATRIX.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("rpi-rgb-led-matrix/fonts/9x15.bdf")
    text_color = graphics.Color(*WHITE)
    pos = canvas.width - 1

    while not STOP:
        canvas.Clear()

        # Weather
        weather = WEATHER_CODE_MAP[WEATHER_CODE]
        if IS_DAY:
            icon = day_icons[weather]
        else:
            icon = night_icons[weather]
        MATRIX.SetImage(icon.convert("RGB"), 1, 1)

        # Temperature
        temp_str = f"{TEMP}°F"
        graphics.DrawText(canvas, font, 25, 14, text_color, temp_str)

        # time.sleep(0.04)
        canvas = MATRIX.SwapOnVSync(canvas)
    MATRIX.Clear()


def main():
    global TIME, TEMP, IS_DAY, WEATHER_CODE, STOP

    responses = OPENMETEO.weather_api(URL, params=PARAMS)
    response = responses[0]
    current = response.Current()

    TIME = datetime.fromtimestamp(current.Time())  # .strftime("%I:%M %p")
    TEMP = round(current.Variables(0).Value())
    IS_DAY = int(current.Variables(1).Value())
    WEATHER_CODE = int(current.Variables(2).Value())

    print(f"Current time {TIME}")
    print(f"Current temperature_2m {TEMP}")
    print(f"Current is_day {IS_DAY}")
    print(f"Current weather_code {WEATHER_CODE}")

    day_icons, night_icons = load_icons()
    try:
        display_weather(day_icons, night_icons)
        while not STOP:
            time.sleep(1)
    except KeyboardInterrupt:
        STOP = True
        MATRIX.Clear()


if __name__ == "__main__":
    main()
