import subprocess
import re
import socket

def get_current_wifi_windows():
    # get SSID
    result = subprocess.run("netsh wlan show interfaces", shell=True, capture_output=True, text=True)
    ssid = None
    for line in result.stdout.splitlines():
        if "SSID" in line and "BSSID" not in line:
            ssid = line.split(":", 1)[1].strip()
            break

    # get password (needs admin rights)
    pw = None
    if ssid:
        profile_cmd = f'netsh wlan show profile name="{ssid}" key=clear'
        profile_result = subprocess.run(profile_cmd, shell=True, capture_output=True, text=True)
        m = re.search(r"Key Content\s*:\s*(.*)", profile_result.stdout)
        if m:
            pw = m.group(1).strip()

    # get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
  
    return {"ssid": ssid, "password": pw, "local_ip": ip}


