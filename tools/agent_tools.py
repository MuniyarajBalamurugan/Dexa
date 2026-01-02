import pyautogui
import os
import webbrowser
import subprocess
import datetime
import shutil
import time
import ctypes
import psutil
import pyperclip
import screen_brightness_control as sbc

# -------------------------------------
# 🔊 System Sound
# -------------------------------------
def mute_sound():
    pyautogui.press("volumemute")
    return "Sound muted."

def increase_volume():
    pyautogui.press("volumeup", presses=5)
    return "Volume increased."

def decrease_volume():
    pyautogui.press("volumedown", presses=5)
    return "Volume decreased."

# -------------------------------------
# 🌐 Web / Apps
# -------------------------------------
def open_whatsapp():
    os.system("start whatsapp://")
    return "WhatsApp opened."

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "YouTube opened."

def open_google():
    webbrowser.open("https://www.google.com")
    return "Google opened."

def open_gmail():
    webbrowser.open("https://mail.google.com")
    return "Gmail opened."

def open_facebook():
    webbrowser.open("https://www.facebook.com")
    return "Facebook opened."

def open_instagram():
    webbrowser.open("https://www.instagram.com")
    return "Instagram opened."

def open_twitter():
    webbrowser.open("https://twitter.com")
    return "Twitter opened."

def open_linkedin():
    webbrowser.open("https://www.linkedin.com")
    return "LinkedIn opened."

def open_github():
    webbrowser.open("https://github.com")
    return "GitHub opened."

def open_gitlab():
    webbrowser.open("https://gitlab.com")
    return "GitLab opened."

def open_reddit():
    webbrowser.open("https://reddit.com")
    return "Reddit opened."

def open_maps():
    webbrowser.open("https://maps.google.com")
    return "Google Maps opened."

def open_wikipedia():
    webbrowser.open("https://wikipedia.org")
    return "Wikipedia opened."

def open_stackoverflow():
    webbrowser.open("https://stackoverflow.com")
    return "StackOverflow opened."

# -------------------------------------
# 📂 Files / Folders
# -------------------------------------
def open_d_drive():
    os.startfile("D:\\")
    return "D: drive opened."

def open_c_drive():
    os.startfile("C:\\")
    return "C: drive opened."

def open_downloads():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(path)
    return "Downloads opened."

def open_documents():
    path = os.path.join(os.path.expanduser("~"), "Documents")
    os.startfile(path)
    return "Documents opened."

def open_desktop():
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    os.startfile(path)
    return "Desktop opened."

def create_folder(path: str):
    os.makedirs(path, exist_ok=True)
    return f"Folder created at {path}"

def delete_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
        return f"Deleted folder: {path}"
    return "Folder not found."

def create_file(path: str, content: str = ""):
    with open(path, "w") as f:
        f.write(content)
    return f"File created at {path}"

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
        return f"Deleted file: {path}"
    return "File not found."

def copy_file(src: str, dest: str):
    shutil.copy(src, dest)
    return f"Copied file from {src} to {dest}"

def move_file(src: str, dest: str):
    shutil.move(src, dest)
    return f"Moved file from {src} to {dest}"

# -------------------------------------
# 🖥️ System Apps
# -------------------------------------
def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return "Notepad opened."

def open_calculator():
    subprocess.Popen(["calc.exe"])
    return "Calculator opened."

def open_paint():
    subprocess.Popen(["mspaint.exe"])
    return "Paint opened."

def open_cmd():
    subprocess.Popen(["cmd.exe"])
    return "Command Prompt opened."

def open_task_manager():
    subprocess.Popen(["taskmgr.exe"])
    return "Task Manager opened."

def open_control_panel():
    subprocess.Popen(["control.exe"])
    return "Control Panel opened."

def open_file_explorer():
    subprocess.Popen(["explorer.exe"])
    return "File Explorer opened."

def open_edge():
    subprocess.Popen(["msedge.exe"])
    return "Edge opened."

def open_chrome():
    subprocess.Popen(["chrome.exe"])
    return "Chrome opened."

def open_firefox():
    subprocess.Popen(["firefox.exe"])
    return "Firefox opened."

def open_spotify():
    subprocess.Popen(["spotify.exe"], shell=True)
    return "Spotify opened."

def open_vlc():
    subprocess.Popen(["vlc.exe"], shell=True)
    return "VLC opened."

def open_word():
    subprocess.Popen(["winword.exe"], shell=True)
    return "Word opened."

def open_excel():
    subprocess.Popen(["excel.exe"], shell=True)
    return "Excel opened."

def open_powerpoint():
    subprocess.Popen(["powerpnt.exe"], shell=True)
    return "PowerPoint opened."

def open_settings():
    subprocess.Popen(["start", "ms-settings:"], shell=True)
    return "Windows Settings opened."

# -------------------------------------
# 🔒 Power Controls
# -------------------------------------
def lock_pc():
    ctypes.windll.user32.LockWorkStation()
    return "PC locked."

def shutdown_pc():
    os.system("shutdown /s /t 1")
    return "Shutting down."

def restart_pc():
    os.system("shutdown /r /t 1")
    return "Restarting."

def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "Sleep mode."

# -------------------------------------
# 📸 Screenshots
# -------------------------------------
import os
import pyautogui
from datetime import datetime

def take_screenshot():
    try:
        # Define folder for screenshots
        folder = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        os.makedirs(folder, exist_ok=True)

        # Filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(folder, f"screenshot_{timestamp}.png")

        # Take the screenshot
        screenshot = pyautogui.screenshot()

        # Save to file
        screenshot.save(path)

        if os.path.exists(path):
            return f"Screenshot successfully saved at: {path}"
        else:
            return f"Screenshot failed to save at: {path}"

    except Exception as e:
        return f"Error taking screenshot: {e}"


def take_screenshot_timestamp():
    folder = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
    os.makedirs(folder, exist_ok=True)
    filename = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
    path = os.path.join(folder, filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved at {path}"

def take_region_screenshot(x1: int, y1: int, x2: int, y2: int) -> str:
    """Takes a screenshot of the region defined by (x1,y1) top-left and (x2,y2) bottom-right."""
    import pyautogui, datetime, os
    
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"screenshot_{timestamp}.png")

    image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    image.save(filename)

    return f"Region screenshot saved as {filename}"


# -------------------------------------
# ⌨️ Keyboard / Mouse Automation
# -------------------------------------
def type_text_anywhere(text: str):
    pyautogui.typewrite(text)
    return f"Typed: {text}"

def copy_text():
    pyautogui.hotkey("ctrl", "c")
    return "Copied text."

def paste_text():
    pyautogui.hotkey("ctrl", "v")
    return "Pasted text."

def cut_text():
    pyautogui.hotkey("ctrl", "x")
    return "Cut text."

def undo_action():
    pyautogui.hotkey("ctrl", "z")
    return "Undo."

def redo_action():
    pyautogui.hotkey("ctrl", "y")
    return "Redo."

def press_enter():
    pyautogui.press("enter")
    return "Pressed Enter."

def scroll_up():
    pyautogui.scroll(500)
    return "Scrolled up."

def scroll_down():
    pyautogui.scroll(-500)
    return "Scrolled down."

def switch_window():
    pyautogui.hotkey("alt", "tab")
    return "Switched window."

def close_window():
    pyautogui.hotkey("alt", "f4")
    return "Closed window."

def minimize_windows():
    pyautogui.hotkey("win", "d")
    return "All windows minimized."

def maximize_window():
    pyautogui.hotkey("win", "up")
    return "Window maximized."

def minimize_window():
    pyautogui.hotkey("win", "down")
    return "Window minimized."

# -------------------------------------
# 🎵 Media Controls
# -------------------------------------
def next_track():
    pyautogui.press("nexttrack")
    return "Next track."

def previous_track():
    pyautogui.press("prevtrack")
    return "Previous track."

def play_pause():
    pyautogui.press("playpause")
    return "Play/Pause toggled."

# -------------------------------------
# 📋 Clipboard Tools
# -------------------------------------
def read_clipboard():
    text = pyperclip.paste()
    return f"Clipboard: {text}" if text else "Clipboard empty."

def clear_clipboard():
    pyperclip.copy("")
    return "Clipboard cleared."

# -------------------------------------
# 🔋 System Status
# -------------------------------------
def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Not charging)'}"
    return "Battery info not available."

def get_cpu_usage():
    return f"CPU: {psutil.cpu_percent()}%"

def get_ram_usage():
    ram = psutil.virtual_memory()
    return f"RAM: {ram.percent}% ({ram.used // (1024*1024)} MB used)"

def get_disk_usage(drive: str) -> str:
    """Get disk usage for a specific drive (e.g., 'C:/')."""
    usage = psutil.disk_usage(drive)
    return f"Disk {drive}: {usage.percent}% used ({usage.used // (1024**3)}GB/{usage.total // (1024**3)}GB)"

# -------------------------------------
# 🌞 Brightness Control
# -------------------------------------
def increase_brightness():
    sbc.set_brightness(min(100, sbc.get_brightness()[0] + 10))
    return "Brightness increased."

def decrease_brightness():
    sbc.set_brightness(max(0, sbc.get_brightness()[0] - 10))
    return "Brightness decreased."

def get_brightness():
    return f"Brightness: {sbc.get_brightness()[0]}%"
