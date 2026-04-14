#!/usr/bin/env python3
"""
Simple text scrolling display for 32x64 RGB LED matrix.
Usage: python text_scroll.py --text "Hello" --color "255,0,0" --text "World" --color "0,255,0"
"""

import argparse
import sys
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


def parse_color(color_string):
    """
    Parse color string into RGB tuple.

    Args:
        color_string: String in format "R,G,B" (e.g., "255,0,0")

    Returns:
        tuple: (R, G, B) values
    """
    try:
        parts = color_string.split(",")
        if len(parts) != 3:
            raise ValueError("Color must have 3 components (R,G,B)")

        r, g, b = [int(x.strip()) for x in parts]

        # Validate range
        if not all(0 <= val <= 255 for val in [r, g, b]):
            raise ValueError("Color values must be between 0 and 255")

        return (r, g, b)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid color format: {color_string}. Use format 'R,G,B' (e.g., '255,0,0')") from e


def scroll_text(matrix, text_blocks, speed=0.04):
    """
    Scroll multiple text blocks with individual colors across the LED matrix continuously.

    Args:
        matrix: RGBMatrix instance
        text_blocks: List of tuples [(text, (r, g, b)), ...]
        speed: Scroll speed in seconds (default: 0.04, lower = faster)
    """
    offscreen_canvas = matrix.CreateFrameCanvas()

    # Load font
    font = graphics.Font()
    font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")

    # Calculate width for each text block and total width
    block_info = []
    total_width = 0

    for text, color in text_blocks:
        text_width = sum([font.CharacterWidth(ord(c)) for c in text])
        block_info.append(
            {
                "text": text,
                "color": graphics.Color(color[0], color[1], color[2]),
                "width": text_width,
                "start_offset": total_width,
            }
        )
        total_width += text_width

    # Start position (right edge of display)
    x_pos = matrix.width

    # Print info
    print(f"Scrolling {len(text_blocks)} text block(s):")
    for i, (text, color) in enumerate(text_blocks, 1):
        print(f"  Block {i}: '{text}' (RGB: {color})")
    print("Press Ctrl+C to stop")

    try:
        while True:
            offscreen_canvas.Clear()

            # Draw each text block at its calculated position
            for block in block_info:
                block_x = x_pos + block["start_offset"]
                graphics.DrawText(offscreen_canvas, font, block_x, 20, block["color"], block["text"])

            # Move text left
            x_pos -= 1

            # Reset position when all text fully scrolls off left edge
            if x_pos + total_width < 0:
                x_pos = matrix.width

            # Swap canvas
            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

            # Control scroll speed (smaller = faster)
            time.sleep(speed)

    except KeyboardInterrupt:
        print("\nStopping text scroll...")
        matrix.Clear()


def main():
    """Main entry point for CLI execution."""
    parser = argparse.ArgumentParser(
        description="Scroll text on a 32x64 RGB LED matrix with multiple colored blocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single text block (default white)
  python text_scroll.py --text "Hello World!"
  
  # Single text block with custom color
  python text_scroll.py --text "Hello" --color "255,0,0"
  
  # Multiple text blocks with different colors
  python text_scroll.py --text "Hello" --color "255,0,0" --text "World" --color "0,255,0"
  
  # Mix of colored and default blocks
  python text_scroll.py --text "Red" --color "255,0,0" --text " White " --text "Blue" --color "0,0,255"
  
  # Custom scroll speed
  python text_scroll.py --text "Fast!" --color "255,255,0" --speed 0.02
        """,
    )

    parser.add_argument(
        "--text", action="append", dest="texts", type=str, help="Text block to display (can be used multiple times)"
    )

    parser.add_argument(
        "--color",
        action="append",
        dest="colors",
        type=str,
        help="RGB color for the preceding text block in format 'R,G,B' (e.g., '255,0,0' for red). If omitted, white is used.",
    )

    parser.add_argument(
        "--speed", type=float, default=0.04, help="Scroll speed in seconds (default: 0.04, lower = faster)"
    )

    args = parser.parse_args()

    # Validate that at least one text block is provided
    if not args.texts:
        print("Error: At least one --text argument is required", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Build text blocks with colors
    text_blocks = []
    colors = args.colors or []

    for i, text in enumerate(args.texts):
        # Validate text is not empty
        if not text or text.strip() == "":
            print(f"Error: Text block {i+1} cannot be empty", file=sys.stderr)
            sys.exit(1)

        # Use provided color or default to white
        if i < len(colors) and colors[i]:
            try:
                color = parse_color(colors[i])
            except ValueError as e:
                print(f"Error in color for text block {i+1}: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            color = (255, 255, 255)  # Default white

        text_blocks.append((text, color))

    # Setup LED matrix configuration
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.gpio_slowdown = 2
    options.hardware_mapping = "adafruit-hat"

    try:
        matrix = RGBMatrix(options=options)
        scroll_text(matrix, text_blocks, args.speed)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
