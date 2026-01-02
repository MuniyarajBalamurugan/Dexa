from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "source", "log")
os.makedirs(LOG_DIR, exist_ok=True)

def add_log(source, command):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"report_{today}.txt"
    filepath = os.path.join(LOG_DIR, filename)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, "a+", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ({source}) {command}\n")
