import signal
import sys
import time

running = True


def signal_handler(sig, frame):
    global running
    running = False
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    x = 0
    while running:
        print(f"Running for {x} second{'' if x == 1 else 's'}")
        x += 1
        time.sleep(1)
