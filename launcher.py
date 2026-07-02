import json
import subprocess
import sys
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
import transcribe1


# -------------------------------------------------
# Paths
# -------------------------------------------------

import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

SETTINGS_FILE = BASE_DIR / "settings.json"
STATUS_FILE = BASE_DIR / "status.json"

# Reset status file when launcher starts
with open(STATUS_FILE, "w", encoding="utf-8") as f:
    json.dump({
        "status": "Waiting...",
        "progress": 0,
        "log": []
    }, f, indent=4)

# -------------------------------------------------
# Load Settings
# -------------------------------------------------

settings = {
    "blender": "",
    "editor": ""
}

if SETTINGS_FILE.exists():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings.update(json.load(f))
    except:
        pass

# -------------------------------------------------
# Save Settings
# -------------------------------------------------

def save_settings():

    settings["blender"] = blender_var.get()
    settings["editor"] = editor_var.get()

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

# -------------------------------------------------
# Browse Buttons
# -------------------------------------------------

def browse_blender():

    filename = filedialog.askopenfilename(
        title="Select Blender Executable",
        filetypes=[("Executable","*.exe")]
    )

    if filename:

        blender_var.set(filename)
        save_settings()


def browse_editor():

    folder = filedialog.askdirectory(
        title="Select One Click Editor Folder"
    )

    if folder:

        editor_var.set(folder)
        save_settings()


def browse_video():

    folder = filedialog.askdirectory(
        title="Select Video Folder"
    )

    if folder:

        video_var.set(folder)

# -------------------------------------------------
# Start Processing
# -------------------------------------------------


def start():

    save_settings()

    # Reset GUI
    status_var.set("Starting...")
    progress["value"] = 0

    log_box.configure(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.configure(state="disabled")

    # Reset status.json
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "status": "Starting...",
            "progress": 0,
            "log": []
        }, f, indent=4)

    start_button.config(state="disabled")

   
    def worker():
        try:
            transcribe1.main(
                blender_var.get(),
                editor_var.get(),
                video_var.get()
            )
        finally:
            root.after(
                0,
                lambda: start_button.config(state="normal")
    )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()
# -------------------------------------------------
# GUI
# -------------------------------------------------

root = tk.Tk()

root.title("One Click Video Editor")
root.geometry("900x650")
root.resizable(False, False)

# -------------------------------------------------
# Variables
# -------------------------------------------------

blender_var = tk.StringVar(value=settings["blender"])
editor_var = tk.StringVar(value=settings["editor"])
video_var = tk.StringVar()

status_var = tk.StringVar(value="Waiting...")

# -------------------------------------------------
# Blender
# -------------------------------------------------

tk.Label(
    root,
    text="Blender Executable"
).grid(row=0,column=0,padx=10,pady=10,sticky="w")

blender_frame = tk.Frame(root)
blender_frame.grid(row=0, column=1, sticky="w", padx=5)

tk.Entry(
    blender_frame,
    width=70,
    textvariable=blender_var
).pack(side="left")

tk.Button(
    blender_frame,
    text="Browse",
    command=browse_blender
).pack(side="left", padx=5)

# -------------------------------------------------
# One Click Editor
# -------------------------------------------------

tk.Label(
    root,
    text="One Click Editor"
).grid(row=1,column=0,padx=10,pady=10,sticky="w")

editor_frame = tk.Frame(root)
editor_frame.grid(row=1, column=1, sticky="w", padx=5)

tk.Entry(
    editor_frame,
    width=70,
    textvariable=editor_var
).pack(side="left")

tk.Button(
    editor_frame,
    text="Browse",
    command=browse_editor
).pack(side="left", padx=5)

# -------------------------------------------------
# Video Folder
# -------------------------------------------------

tk.Label(
    root,
    text="Video Folder"
).grid(row=2,column=0,padx=10,pady=10,sticky="w")

video_frame = tk.Frame(root)
video_frame.grid(row=2, column=1, sticky="w", padx=5)

tk.Entry(
    video_frame,
    width=70,
    textvariable=video_var
).pack(side="left")

tk.Button(
    video_frame,
    text="Browse",
    command=browse_video
).pack(side="left", padx=5)

# -------------------------------------------------
# Status
# -------------------------------------------------

tk.Label(
    root,
    text="Status",
    font=("Arial",10,"bold")
).grid(row=3,column=0,padx=10,pady=10,sticky="w")

status_label = tk.Label(
    root,
    textvariable=status_var,
    anchor="w",
    width=70,
    relief="sunken",
    bg="white"
)

status_label.grid(
    row=3,
    column=1,
    columnspan=2,
    sticky="ew",
    padx=5
)

# -------------------------------------------------
# Progress Bar
# -------------------------------------------------

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate",
    length=650
)

progress.grid(
    row=4,
    column=1,
    columnspan=2,
    pady=15
)

# -------------------------------------------------
# START Button
# -------------------------------------------------

start_button = tk.Button(
    root,
    text="START",
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    command=start
)

start_button.grid(
    row=5,
    column=1,
    pady=15
)

# -------------------------------------------------
# Log Window
# -------------------------------------------------

tk.Label(
    root,
    text="Live Log",
    font=("Arial",10,"bold")
).grid(row=6,column=0,padx=10,pady=10,sticky="nw")

log_box = ScrolledText(
    root,
    width=105,
    height=18
)

log_box.grid(
    row=6,
    column=1,
    columnspan=2,
    padx=5,
    pady=5
)

log_box.configure(state="disabled")
# -------------------------------------------------
# Refresh GUI from status.json
# -------------------------------------------------

def refresh_status():

    global process

    if STATUS_FILE.exists():

        try:

            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # -------------------------
            # Status
            # -------------------------

            status_var.set(
                data.get("status", "Waiting...")
            )

            # -------------------------
            # Progress
            # -------------------------

            progress["value"] = data.get(
                "progress",
                0
            )

            # -------------------------
            # Log Window
            # -------------------------

            lines = data.get("log", [])

            text = "\n".join(lines)

            current = log_box.get("1.0", tk.END).strip()

            if current != text:

                log_box.configure(state="normal")

                log_box.delete("1.0", tk.END)

                log_box.insert(
                    tk.END,
                    text
                )

                log_box.see(tk.END)

                log_box.configure(state="disabled")

        except Exception as e:

            print(e)

    # ------------------------------------
    # Check if process finished
    # ------------------------------------

  

    root.after(
        500,
        refresh_status
    )


# -------------------------------------------------
# Start Refresh Loop
# -------------------------------------------------
# Reset GUI
status_var.set("Waiting...")
progress["value"] = 0

log_box.configure(state="normal")
log_box.delete("1.0", tk.END)
log_box.configure(state="disabled")

refresh_status()

# -------------------------------------------------
# Run GUI
# -------------------------------------------------

root.mainloop()