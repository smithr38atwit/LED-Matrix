#!/usr/bin/env python

import sys

sys.path.append(".")

import os.path
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import UTC, datetime
from signal import SIGINT, SIGTERM, signal

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Setup LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 2
options.hardware_mapping = "adafruit-hat"
MATRIX = RGBMatrix(options=options)

# Color Constants
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
WHITE = (200, 200, 200)

# Thread variables
message = "No upcoming events"
in_meeting = False
manual_override = False
stop = threading.Event()


def display_message():
    """
    Displays meeting time/status on LED Matrix
    """
    canvas = MATRIX.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
    text_color = graphics.Color(*WHITE)
    pos = canvas.width - 2

    while not stop.is_set():
        # Message/Color
        if in_meeting:
            outline_color = graphics.Color(*RED)
        else:
            outline_color = graphics.Color(*GREEN)

        canvas.Clear()
        # Text
        len = graphics.DrawText(canvas, font, pos, 20, text_color, message)
        pos -= 1
        if pos + len < 1:
            pos = canvas.width

        # Outline
        graphics.DrawLine(canvas, 0, 0, 63, 0, outline_color)
        graphics.DrawLine(canvas, 63, 0, 63, 31, outline_color)
        graphics.DrawLine(canvas, 0, 0, 0, 31, outline_color)
        graphics.DrawLine(canvas, 0, 31, 63, 31, outline_color)

        time.sleep(0.04)
        canvas = MATRIX.SwapOnVSync(canvas)
    MATRIX.Clear()


def get_next_event():
    """
    Retrieves next calendar event
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.now(UTC).isoformat()[:-6] + "Z"  # 'Z' indicates UTC time; [:-6] cuts out TZ offset data
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                eventTypes="default",
                timeMin=now,
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return None

        # Filter out all day events
        events = list(filter(lambda event: "dateTime" in event["start"], events))
        return events[0]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def meeting_loop():
    global message, in_meeting, manual_override
    while not stop.is_set():
        if manual_override:
            time.sleep(1)
            continue

        event = get_next_event()
        if not event:
            message = "No upcoming events"
            in_meeting = False
        else:
            start = event["start"]["dateTime"]
            start = datetime.fromisoformat(start)
            if start.date() == datetime.now().date():
                start_time = start.strftime("%-I:%M")
                end_time = event["end"]["dateTime"]
                end_time = datetime.fromisoformat(end_time).strftime("%-I:%M")
                now = datetime.now().isoformat()
                in_meeting = event["start"]["dateTime"] <= now <= event["end"]["dateTime"]

                if in_meeting:
                    message = f"In a meeting: {start_time} - {end_time}"
                else:
                    message = f"Next meeting: {start_time} - {end_time}"
            else:
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day_name = days[start.weekday()]
                message = f"Next meeting: {day_name}"
                in_meeting = False
            for _ in range(60):  # Check for new events every minute
                if stop.is_set() or manual_override:
                    break
                time.sleep(1)


def manual_override_loop():
    global in_meeting, manual_override, message
    while not stop.is_set():
        user_input = input("Enter command (busy, free, auto, stop): ").strip().lower()
        match user_input:
            case "busy":
                manual_override = True
                in_meeting = True
                message = "Busy"
            case "free":
                manual_override = True
                in_meeting = False
                message = "Available"
            case "auto":
                manual_override = False
            case "stop":
                stop.set()
                sys.exit(1)
            case _:
                print("Invalid command")


def handle_exit(sig, frame):
    stop.set()
    sys.exit(1)


def main():
    signal(SIGINT, handle_exit)
    signal(SIGTERM, handle_exit)

    with ThreadPoolExecutor() as executor:
        futures: list[Future] = []
        futures.append(executor.submit(meeting_loop))
        futures.append(executor.submit(display_message))
        futures.append(executor.submit(manual_override_loop))

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
