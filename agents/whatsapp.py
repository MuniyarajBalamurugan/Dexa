import pyautogui
import time
from google.adk.agents import Agent

# 1. Open WhatsApp
def open_whatsapp():
    pyautogui.press("win")
    time.sleep(1)
    pyautogui.typewrite("WhatsApp")
    pyautogui.press("enter")

# 2. Search Contact
def search_whatsapp_contact(name: str):
    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)
    pyautogui.typewrite(name)
    time.sleep(1)
    pyautogui.press("enter")

# 3. Open Chat
def open_chat(name: str):
    search_whatsapp_contact(name)

# 4. Send Message
def send_message(message: str):
    pyautogui.typewrite(message)
    pyautogui.press("enter")

# 5. Send Emoji
def send_emoji(emoji: str):
    pyautogui.typewrite(emoji)
    pyautogui.press("enter")

# 6. Send File
def send_file(file_path: str):
    pyautogui.hotkey("ctrl", "o")
    time.sleep(1)
    pyautogui.typewrite(file_path)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")

# 7. Start Call
def start_call(call_type: str):
    if call_type == "video":
        pyautogui.hotkey("ctrl", "shift", "u")
    elif call_type == "voice":
        pyautogui.hotkey("ctrl", "u")

# 8. Read Recent Messages (OCR later)
def read_recent_messages():
    screenshot = pyautogui.screenshot(region=(200, 200, 600, 400))
    screenshot.save("recent_chat.png")
    return "Screenshot saved. Use OCR to read text."

# 9. Scroll Chat
def scroll_chat(direction: str, amount: int):
    for _ in range(amount):
        pyautogui.scroll(500 if direction == "up" else -500)

# 10. Close WhatsApp
def close_whatsapp():
    pyautogui.hotkey("alt", "f4")

# Agent definition
whatsapp_agent = Agent(
    name="whatsapp_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a WhatsApp Controller Agent.
    Handle tasks like opening WhatsApp, searching contacts, opening chats,
    sending messages, emojis, files, starting calls, reading messages (via OCR),
    scrolling chats, and closing WhatsApp. Always use tools to complete tasks automatically.
    """,
    tools=[
        open_whatsapp,
        search_whatsapp_contact,
        open_chat,
        send_message,
        send_emoji,
        send_file,
        start_call,
        read_recent_messages,
        scroll_chat,
        close_whatsapp
    ]
)
