import requests
import time
import sys

from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

font_color = 0xFFFFFF
timezone_info = [-4, "EDT"]
# the name of the sports you want to follow
sport_name = ["football", "baseball", "hockey"]
# the name of the corresponding leages you want to follow
sport_league = ["nfl", "mlb", "nhl"]
# the team names you want to follow
# must match the order of sport/league arrays
# include full name and then abbreviation (usually city/region)
TEAMS = [
    ("New England Patriots", "NE"),
    ("Boston Red Sox", "BOS"),
    ("Boston Bruins", "BOS"),
    ]
SPORT_URLS = [f"https://site.api.espn.com/apis/site/v2/sports/{sport_name[i]}/{sport_league[i]}/scoreboard" 
              for i in range(len(sport_name))]

# Setup LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 2
options.hardware_mapping = 'adafruit-hat'
MATRIX = RGBMatrix(options=options)


def get_info(url, team):
    names = []
    scores = []
    info = {}
    playing = False

    data = requests.get(url).json()
    info["league"] = data["leagues"][0]["slug"]
    for event in data["events"]:
        # check for your team playing
        # team[0]
        if "Houston Texans" not in event["name"]:
            continue

        playing = True

        info["dateTime"] = event["status"]["type"]["shortDetail"]
        info["status"] = event["status"]["type"]["state"]
        for competition in event["competitions"]:
            for competitor in competition["competitors"]:
                # index indicates home vs. away
                names.append(competitor["team"]["abbreviation"])
                scores.append(competitor["score"])
        break

    return names, scores, info, playing


def display_scores(names, scores, info):
    file_source = f'sport_logos_24x24/{info["league"]}_logos/'
    home_logo = Image.open(file_source + f"{names[0]}.bmp").convert('RGB')
    away_logo = Image.open(file_source + f"{names[1]}.bmp").convert('RGB')

    double_buffer = MATRIX.CreateFrameCanvas()
    img_size = 24

    # let's scroll
    ypos1, ypos2 = 0, 0
    try:
        while True:
            double_buffer.Clear()
            ypos1 += 1
            ypos2 += 1
            if (ypos1 + img_size > double_buffer.height):
                ypos1 = 0
            if (ypos2 - img_size > double_buffer.height):
                ypos2 = 0
            
            double_buffer.SetImage(home_logo, 4, -ypos1)
            double_buffer.SetImage(home_logo, 4, -ypos2 + img_size + 6)
            double_buffer.SetImage(away_logo, 36, -ypos1)
            double_buffer.SetImage(away_logo, 36, -ypos2 + img_size + 6)

            double_buffer = MATRIX.SwapOnVSync(double_buffer)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    names, scores, info, playing = get_info(SPORT_URLS[0], TEAMS[0])
    print("Names:\n", names)
    print("Scores:\n", scores)
    print("Info:\n", info)
    print("Playing:\n", playing)

    if playing:
        display_scores(names, scores, info)