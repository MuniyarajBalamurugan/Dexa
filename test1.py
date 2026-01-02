import asyncio
import threading
import os
import socket
import customtkinter as ctk
import qrcode
from PIL import Image
import shutil
import main
from utils.wifi_config import get_current_wifi_windows
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64
import json
from tkcalendar import DateEntry
from pathlib import Path

# ---------------- GLOBALS ----------------
wake_word = os.getenv("WAKE_WORD", "DEXA")
wake_word_enabled = True
assistant_thread = None
stop_event = threading.Event()
qr_photo = None

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

# ---------------- Toast Function ----------------
def toast(msg, duration=2000, color="#2ecc71"):
    """Show a temporary toast message at the top of the window"""
    toast_label = ctk.CTkLabel(root, text=msg, fg_color=color, text_color="white",
                               corner_radius=10, font=ctk.CTkFont(size=14))
    toast_label.place(relx=0.5, rely=0.05, anchor="n")  # top center
    root.after(duration, toast_label.destroy)

# ---------------- Agent Functions ----------------
def run_agent():
    os.environ["TTS_ENABLED"] = '1' if voice_switch.get() else '0'
    os.environ["TTS_VOICE_INDEX"] = str(voice_var.get())
    os.environ["WAKE_WORD_ENABLED"] = "1" if wake_word_enabled else "0"
    os.environ["WAKE_WORD"] = wake_word

    tcp_state = tcp_switch.get()
    mic_state = mic_switch.get()

    if not tcp_state and not mic_state:
        update_status("⚠ At least one mode must be ON. Defaulting to Mic.", "orange")
        toast("⚠ At least one mode must be ON. Defaulting to Mic.", color="#e67e22")
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
    start_button.configure(text="⏹ Stop Assistant", fg_color="#e74c3c", hover_color="#c0392b", command=stop_agent)

def stop_agent():
    global assistant_thread, stop_event
    stop_event.set()
    update_status("Assistant stopped", "red")
    start_button.configure(text="▶ Start Assistant", fg_color="#2ecc71", hover_color="#27ae60", command=start_agent)

def change_wake_word():
    global wake_word
    new_word = wake_word_entry.get().strip()
    if new_word:
        wake_word = new_word
        os.environ["WAKE_WORD"] = wake_word
        update_status(f"Wake word changed to '{wake_word}'", "blue")
        toast(f"Wake word changed to '{wake_word}'", color="#3498db")

def toggle_wake_word():
    global wake_word_enabled
    wake_word_enabled = wake_word_switch.get()
    update_status(f"Wake word {'enabled' if wake_word_enabled else 'disabled'}", 
                  "green" if wake_word_enabled else "orange")
    toast(f"Wake word {'enabled' if wake_word_enabled else 'disabled'}", 
      color="#2ecc71" if wake_word_enabled else "#e67e22")

def download_log():
    date_str = log_date_entry.get_date().strftime("%Y-%m-%d")
    filename = f"source/log/report_{date_str}.txt"
    
    downloads_path = str(Path.home() / "Downloads")
    dest = os.path.join(downloads_path, f"report_{date_str}.txt")

    if os.path.exists(filename):
        shutil.copy(filename, dest)
        toast(f"Log downloaded: {dest}", color="#2ecc71")
    else:
        toast(f"No log file found for {date_str}", color="#e74c3c")

# ---------------- UI ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("✨ Desktop Assistant ✨")
root.geometry("650x780")
root.resizable(False, False)

# ---------------- Top Title ----------------
ctk.CTkLabel(root, text="✨ AI Voice Assistant ✨", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
start_button = ctk.CTkButton(root, text="▶ Start Assistant", command=start_agent, height=45, corner_radius=20,
                             fg_color="#2ecc71", hover_color="#27ae60")
start_button.pack(pady=10)

# ---------------- Mode Frame ----------------
mode_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#2c3e50")
mode_frame.pack(padx=40, pady=5, fill="x")
ctk.CTkLabel(mode_frame, text="Mode Selection", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=8)

# Mic Mode
mic_switch = ctk.CTkSwitch(mode_frame, text="Mic Mode", command=lambda: toggle_container(mic_switch, mic_container))
mic_switch.select()
mic_switch.pack(anchor="w", padx=20, pady=5)

mic_container = ctk.CTkFrame(mode_frame, corner_radius=10, fg_color="#34495e", height=0)
mic_container.pack(anchor="w", padx=20, fill="x", pady=5)
mic_container.pack_propagate(False)

wake_word_entry = ctk.CTkEntry(mic_container, placeholder_text="Enter wake word...", width=220)
wake_word_entry.pack(pady=5)
change_wake_word_btn = ctk.CTkButton(mic_container, text="Change Wake Word", command=change_wake_word, height=35, corner_radius=20)
change_wake_word_btn.pack(pady=5)
wake_word_entry.insert(0, wake_word)

wake_word_switch = ctk.CTkSwitch(mic_container, text="Enable Wake Word", command=toggle_wake_word)
wake_word_switch.select()
wake_word_switch.pack(pady=5)

# TCP Mode
tcp_switch = ctk.CTkSwitch(mode_frame, text="App Connection (TCP)", command=lambda: toggle_container(tcp_switch, app_container))
tcp_switch.pack(anchor="w", padx=20, pady=5)

app_container = ctk.CTkFrame(mode_frame, corner_radius=10, fg_color="#34495e")
app_container.pack(anchor="w", padx=20, fill="x", pady=5)
app_container.pack_propagate(False)

qr_label = ctk.CTkLabel(app_container, text="")
qr_label.bind("<Button-1>", on_qr_click)
qr_label.pack(pady=5)

# ---------------- Voice & Log Horizontal Frame ----------------
hl_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#2c3e50")
hl_frame.pack(padx=40, pady=15, fill="x", ipady=10)

# Voice Output
voice_frame = ctk.CTkFrame(hl_frame, corner_radius=10, fg_color="#2c3e50")
voice_frame.pack(side="left", fill="y", expand=True, padx=(0, 10), pady=10)
ctk.CTkLabel(voice_frame, text="🎤 Voice Output", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=8)

voice_switch = ctk.CTkSwitch(voice_frame, text="Enable Voice Output")
voice_switch.select()
voice_switch.pack(pady=5)

voice_var = ctk.IntVar(value=0)
gents_rb = ctk.CTkRadioButton(voice_frame, text="David (Male)", variable=voice_var, value=0)
ladies_rb = ctk.CTkRadioButton(voice_frame, text="Zira (Female)", variable=voice_var, value=1)

def update_voice_env():
    os.environ["TTS_VOICE_INDEX"] = str(voice_var.get())
    toast(f"Voice set to {'David' if voice_var.get()==0 else 'Zira'}", color="#3498db")

gents_rb.configure(command=update_voice_env)
ladies_rb.configure(command=update_voice_env)

def toggle_voice_options():
    if voice_switch.get():
        gents_rb.pack(pady=5)
        ladies_rb.pack(pady=5)
        os.environ["TTS_ENABLED"] = '1'
        toast("Voice Output enabled", color="#2ecc71")
    else:
        gents_rb.pack_forget()
        ladies_rb.pack_forget()
        os.environ["TTS_ENABLED"] = '0'
        toast("Voice Output disabled", color="#e74c3c")

voice_switch.configure(command=toggle_voice_options)
toggle_voice_options()

# Log Download
log_frame = ctk.CTkFrame(hl_frame, corner_radius=10, fg_color="#2c3e50")
log_frame.pack(side="left", fill="y", expand=True, padx=(10, 0), pady=10)
ctk.CTkLabel(log_frame, text="📄 Download Log File", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=8)

log_date_entry = DateEntry(log_frame, date_pattern="yyyy-MM-dd", width=12)
log_date_entry.pack(pady=5)

download_log_btn = ctk.CTkButton(log_frame, text="Download Log", command=download_log, height=35, corner_radius=20)
download_log_btn.pack(pady=5)

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
        if switch == tcp_switch and switch.get():
            qrdata = get_current_wifi_windows()
            global qr_photo
            qr_photo = generate_ip_qr(qrdata)
            qr_label.configure(image=qr_photo)

    threading.Thread(target=animate).start()

toggle_container(mic_switch, mic_container)
toggle_container(tcp_switch, app_container)

root.mainloop()
