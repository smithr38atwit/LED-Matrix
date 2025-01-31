import sys
import time

from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Setup LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 2
options.hardware_mapping = "adafruit-hat"
MATRIX = RGBMatrix(options=options)

image_file_1 = "sport_logos_24x24/nfl_logos/NE.bmp"
image_file_2 = "sport_logos_24x24/nfl_logos/KC.bmp"
image_1 = Image.open(image_file_1)
image_2 = Image.open(image_file_2)
MATRIX.SetImage(image_1.convert("RGB"), 4, 1)
MATRIX.SetImage(image_2.convert("RGB"), 36, 1)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    MATRIX.Clear()
    sys.exit(0)
