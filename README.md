# LED Matrix Controller

![demo image](https://github.com/smithr38atwit/smithr38atwit.github.io/blob/main/public/project_images/led_matrix.png)

This repository contains the codebase for controlling a **64x32 RGB LED matrix**. The project includes Python scripts for running various displays on the LED matrix and a web application for managing which display is shown.

> **Note:** This project is a **work in progress**

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

- **Dynamic Displays** - python scripts to render various animations and custom content on the LED matrix.
  - Weather display: shows current temperature and weather conditions
  - Text scroll display: utility for scrolling custom messages
  - Meeting sign: syncs with google calendar and displays next scheduled meeting time and current meeting status
- **Web-based Control** - FastAPI backend endpoints for switching between display modes, and a planned React UI interface.

---

## Technologies Used

This project leverages the following technologies:

- **Languages**:
  - Python
  - JavaScript/HTML/CSS (planned)
- **Frameworks and Libraries**:
  - FastAPI
  - React (planned)
  - [RGB Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix)
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
   uv venv .venv --python 3.11 --system-site-packages
   source .venv/bin/activate
   uv sync
   ```

3. Run the installer script for the RGB Matrix Bonnet library and follow the prompts:

   ```bash
   sudo bash rgb-matrix.sh
   ```

### Usage

1. Run the Python display scripts directly:
   ```bash
   uv run python displays/active/weather.py
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
  - Meeting sign
- FastAPI backend controller.

### Upcoming Features:

- Web interface using **React**.
- Expanded library of display animations and effects.
