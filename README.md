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

- **Dynamic Displays**: Python scripts to render various animations and custom content on the LED matrix.
  - Meeting sign: Syncs with google calendar and displays when your next scheduled meeting is and current meeting status
  - Weath display: Simple display which shows current temperature and weather conditions
- **Web-based Control**: A web application to easily switch between different display modes.

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
  - [RGB Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix) (for controlling LED matrix with Raspbeery PI)
- **Hardware**
  - Raspberry Pi 3B
  - [64x32 RGB LED Matrix](https://www.adafruit.com/product/2278)
  - [RGB Matrix Bonnet](https://www.adafruit.com/product/3211) and other accessories from Adafruit

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
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
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run installer script for RGB Matrix Bonnet library and follow prompts:
   ```bash
   sudo bash rgb-matrix.sh
   ```

### Usage

1. Run the Python display scripts directly:
   ```bash
   python scripts/display_example.py
   ```

**OR**

1. Start the web controller (if using the current Flask app):
   ```bash
   python main.py
   ```

2. Access the web app in your browser at `http://localhost:5000` and choose a display.

---

## Roadmap

### Current Features:
- Python display scripts for animations and content rendering.
  - Meeting sign
  - Weather display
- Flask-based web application for controlling the matrix.

### Upcoming Features:
- Migration of the web application to **React**.
- Expanded library of display animations and effects.
