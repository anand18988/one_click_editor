from pathlib import Path
from datetime import datetime
import json

import sys

if getattr(sys, "frozen", False):
    BASE = Path(sys.executable).resolve().parent
else:
    BASE = Path(__file__).resolve().parent

STATUS_FILE = BASE / "status.json"

def _load():
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except:
            pass

    return {
        "status": "",
        "progress": 0,
        "log": []
    }


def _save(data):
    STATUS_FILE.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


# ----------------- ADD THIS FUNCTION -----------------
def reset():
    _save({
        "status": "",
        "progress": 0,
        "log": []
    })
# -----------------------------------------------------


def set_status(text):
    data = _load()
    data["status"] = text
    _save(data)


def update_progress(value):
    data = _load()
    data["progress"] = value
    _save(data)


def log(text):
    now = datetime.now().strftime("%H:%M:%S")

    line = f"{now}  {text}"

    print(line)

    data = _load()
    data["log"].append(line)
    _save(data)