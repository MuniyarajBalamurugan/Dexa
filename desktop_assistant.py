import asyncio
import threading
import os
import socket
import customtkinter as ctk
import qrcode
from PIL import Image
import main  # your main.py
from utils.wifi_config import get_current_wifi_windows
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64
import json

# ---------------- GLOBALS ----------------
wake_word = os.getenv("WAKE_WORD", "DEXA")
wake_word_enabled = True
assistant_thread = None
stop_event = threading.Event()
qr_photo = None

# DES key/IV (must be 8 bytes)
DES_KEY = b'8bytekey'
DES_IV = b'12345678'

# ---------------- HELPERS ----------------
def update_status(msg, color="white"):
    status_label.configure(text=msg, text_color=color)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def encrypt_des(text: str) -> str:
    cipher = DES.new(DES_KEY, DES.MODE_CBC, DES_IV)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def generate_ip_qr(qrdata):
    json_str = json.dumps(qrdata)
    encrypted_str = encrypt_des(json_str)

    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(encrypted_str)
    qr.make(fit=True)
    img = qr.make_image(fill="blue", back_color="white")
    img = img.resize((150, 150))
    return ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))

def on_qr_click(event):
    ip = get_local_ip()
    ctk.CTkMessageBox.show_info(title="System IP", message=f"IP for TCP: {ip}")

# ---------------- Agent Functions ----------------
def run_agent():
    os.environ["WAKE_WORD_ENABLED"] = "1" if wake_word_enabled else "0"
    os.environ["WAKE_WORD"] = wake_word

    tcp_state = tcp_switch.get()
    mic_state = mic_switch.get()

    if not tcp_state and not mic_state:
        update_status("⚠ At least one mode must be ON. Defaulting to Mic.", "orange")
        mic_state = True
        mic_switch.select()

    asyncio.run(main.main(stop_event, tcp_enabled=tcp_state, mic_enabled=mic_state,
                          wake_word_enabled=wake_word_enabled, wake_word=wake_word))

def start_agent():
    global assistant_thread, stop_event
    if assistant_thread and assistant_thread.is_alive():
        return
    stop_event.clear()
    assistant_thread = threading.Thread(target=run_agent, daemon=True)
    assistant_thread.start()
    update_status("Assistant running", "green")
    start_button.configure(text="⏹ Stop Assistant", fg_color="#e74c3c", command=stop_agent)

def stop_agent():
    global assistant_thread, stop_event
    stop_event.set()
    update_status("Assistant stopped", "red")
    start_button.configure(text="▶ Start Assistant", fg_color="#2ecc71", command=start_agent)

def change_wake_word():
    global wake_word
    new_word = wake_word_entry.get().strip()
    if new_word:
        wake_word = new_word
        os.environ["WAKE_WORD"] = wake_word
        update_status(f"Wake word changed to '{wake_word}'", "blue")

def toggle_wake_word():
    global wake_word_enabled
    wake_word_enabled = wake_word_switch.get()
    if wake_word_enabled:
        update_status(f"Wake word enabled: '{wake_word}'", "green")
    else:
        update_status("Wake word disabled (listening to all speech)", "orange")

# ---------------- UI ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("✨ Desktop Assistant ✨")
root.geometry("450x650")
root.resizable(False, False)

# Title
ctk.CTkLabel(root, text="✨ AI Voice Assistant ✨", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

# Start Button
start_button = ctk.CTkButton(root, text="▶ Start Assistant", command=start_agent, height=40, corner_radius=20, fg_color="#2ecc71")
start_button.pack(pady=10)

# Mode Frame
mode_frame = ctk.CTkFrame(root, corner_radius=10)
mode_frame.pack(padx=40, pady=10, fill="x")
ctk.CTkLabel(mode_frame, text="Mode Selection", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

# ---------------- MIC ----------------
mic_switch = ctk.CTkSwitch(mode_frame, text="Mic Mode", command=lambda: toggle_container(mic_switch, mic_container))
mic_switch.select()
mic_switch.pack(anchor="w", padx=20, pady=5)

mic_container = ctk.CTkFrame(mode_frame, corner_radius=10, fg_color="#2c3e50", height=0)
mic_container.pack(anchor="w", padx=20, fill="x", pady=5)
mic_container.pack_propagate(False)

wake_word_entry = ctk.CTkEntry(mic_container, placeholder_text="Enter wake word...", width=200)
wake_word_entry.pack(pady=5)
change_wake_word_btn = ctk.CTkButton(mic_container, text="Change Wake Word", command=change_wake_word, height=35, corner_radius=20)
change_wake_word_btn.pack(pady=5)
wake_word_entry.insert(0, wake_word)
wake_word_switch = ctk.CTkSwitch(mic_container, text="Enable Wake Word", command=toggle_wake_word)
wake_word_switch.select()
wake_word_switch.pack(pady=5)

# ---------------- APP ----------------
tcp_switch = ctk.CTkSwitch(mode_frame, text="App Connection (TCP)", command=lambda: toggle_container(tcp_switch, app_container))
tcp_switch.pack(anchor="w", padx=20, pady=5)

app_container = ctk.CTkFrame(mode_frame, corner_radius=10, fg_color="#34495e")
app_container.pack(anchor="w", padx=20, fill="x", pady=5)
app_container.pack_propagate(False)

qr_label = ctk.CTkLabel(app_container, text="")
qr_label.bind("<Button-1>", on_qr_click)
qr_label.pack(pady=5)


# ---------------- Status ----------------
status_label = ctk.CTkLabel(root, text="Assistant not running", font=ctk.CTkFont(size=14))
status_label.pack(pady=15)

# ---------------- Animation Function ----------------
def toggle_container(switch, container):
    target_height = 160 if switch.get() else 0
    current_height = container.winfo_height()
    step = 100 if target_height > current_height else -100

    def animate():
        nonlocal current_height
        while (step > 0 and current_height < target_height) or (step < 0 and current_height > target_height):
            current_height += step
            if current_height < 0:
                current_height = 0
            container.configure(height=current_height)
            root.update()
        container.configure(height=target_height)
        # Populate content if App mode
        if switch == tcp_switch and switch.get():
            qrdata = get_current_wifi_windows()
            global qr_photo
            qr_photo = generate_ip_qr(qrdata)
            qr_label.configure(image=qr_photo)
            ip_label.configure(text=f"IP: {ip}")

    threading.Thread(target=animate).start()

# ---------------- Initial display ----------------
toggle_container(mic_switch, mic_container)
toggle_container(tcp_switch, app_container)

root.mainloop()
