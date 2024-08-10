import os
from subprocess import Popen

from flask import Blueprint, redirect, render_template, request, url_for

views = Blueprint("views", __name__)

DISPLAYS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "displays")
CURRENT_PROCESS: Popen = None


@views.route("/")
def home():
    scripts = [f for f in os.listdir(DISPLAYS_DIR) if f.endswith(".py")]
    selected_script = CURRENT_PROCESS.args[1] if CURRENT_PROCESS else None
    return render_template("base.html", scripts=scripts, selected_script=selected_script)


@views.route("/run", methods=["POST"])
def run_script():
    global CURRENT_PROCESS
    script_name = request.form["script"]
    script_path = os.path.join(DISPLAYS_DIR, script_name)

    if CURRENT_PROCESS:
        CURRENT_PROCESS.terminate()
    if os.path.exists(script_path):
        CURRENT_PROCESS = Popen(["python3", script_path])
    return redirect(url_for("views.home"))


@views.route("/stop", methods=["POST"])
def stop_script():
    global CURRENT_PROCESS
    if CURRENT_PROCESS:
        CURRENT_PROCESS.terminate()
        CURRENT_PROCESS = None
    return redirect(url_for("views.home"))
