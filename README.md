# LED Matrix Controller

![demo image](https://github.com/smithr38atwit/smithr38atwit.github.io/blob/main/public/project_images/led_matrix.png)

This repository contains the codebase for controlling a **64x32 RGB LED matrix**. The project includes Python scripts for running various displays on the LED matrix and a web application for managing which display is shown.

> **Note:** This project is a **work in progress**

The current migration audit for the repository surface lives in [docs/migration-surface-audit.md](docs/migration-surface-audit.md). Use that file as the source of truth for which displays are active, deferred, broken, or test-only.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Roadmap](#roadmap)

---

## Features

- **Dynamic Displays**: Python scripts to render various animations and custom content on the LED matrix.
  - Weather display: active display for current temperature and conditions
  - Text scroll display: active utility for scrolling custom messages
  - Meeting sign: retained as a migration candidate, but not currently in regular use
- **Web-based Control**: A web application to easily switch between different display modes.

Current display surface status:

- MVP migration candidates: weather, text scroll, meetings
- Deferred or experimental: sports display
- Broken or test-only: news, test, sports display test

The current Flask UI still lists every top-level Python file in `web/displays`. That is a known temporary limitation and not the intended long-term display registry behavior.

---

## Technologies Used

This project leverages the following technologies:

- **Languages**:
  - Python
  - JavaScript (planned)
  - HTML
  - CSS
- **Frameworks and Libraries**:
  - Flask (for the current web application)
  - React (planned for future migration of the web app)
  - [RGB Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix) (for controlling LED matrix with Raspberry PI)
- **Hardware**
  - Raspberry Pi 3B
  - [64x32 RGB LED Matrix](https://www.adafruit.com/product/2278)
  - [RGB Matrix Bonnet](https://www.adafruit.com/product/3211) and other accessories from Adafruit

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Adafruit RGB Matrix hardware and dependencies
- A Raspberry Pi
- Node.js and npm (for future React updates)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/smithr38atwit/LED-Matrix.git
   cd LED-Matrix
   ```

2. Set up the Python environment:

   ```bash
   python3 -m pip install uv
   uv venv .venv --python 3.11
   source .venv/bin/activate
   uv sync
   ```

3. On the Raspberry Pi, run the installer script for the RGB Matrix Bonnet library and follow the prompts:

   ```bash
   sudo bash rgb-matrix.sh
   ```

4. On the Raspberry Pi, recreate the environment with access to system site packages so the venv can import the system-installed `rgbmatrix` module:

```bash
rm -rf .venv
uv venv .venv --python 3.11 --system-site-packages
source .venv/bin/activate
uv sync
```

The uv-managed environment is the source of truth for pure Python dependencies. The `rgbmatrix` module and related native/system packages are still installed separately by `rgb-matrix.sh`.

### Usage

1. Run the Python display scripts directly:
   ```bash
   uv run python web/displays/weather.py
   ```

**OR**

1. Start the backend controller (FastAPI):

   ```bash
   uv run python main.py
   ```

2. Access backend docs in your browser at `http://localhost:5000/docs` and run display control requests.

---

## Roadmap

### Current Features:

- Python display scripts for animations and content rendering.
  - Weather display
  - Text scroll display
  - Meeting sign as a retained migration candidate
- FastAPI backend control plane with docs-driven API workflow.

### Upcoming Features:

- Migration of the web application to **React**.
- Replacement of the current Flask process launcher with a managed backend runtime.
- Expanded library of display animations and effects.
