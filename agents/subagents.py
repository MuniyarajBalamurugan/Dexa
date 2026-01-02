from google.adk.agents import Agent

from tools.agent_tools import *



system_agent = Agent(
    name="system_agent",
    model="gemini-2.0-flash",
    instruction="Handle system-level commands like volume, shutdown, restart, apps, utilities.",
    tools = [
    # 🔊 Sound
    mute_sound, increase_volume, decrease_volume,

    # 🌐 Web / Apps
    open_whatsapp, open_youtube, open_google, open_gmail,
    open_facebook, open_instagram, open_twitter, open_linkedin,
    open_github, open_gitlab, open_reddit, open_maps,
    open_wikipedia, open_stackoverflow,

    # 📂 Files / Folders
    open_d_drive, open_c_drive, open_downloads, open_documents,
    open_desktop, create_folder, delete_folder,
    create_file, delete_file, copy_file, move_file,

    # 🖥️ System Apps
    open_notepad, open_calculator, open_paint, open_cmd,
    open_task_manager, open_control_panel, open_file_explorer,
    open_edge, open_chrome, open_firefox, open_spotify,
    open_vlc, open_word, open_excel, open_powerpoint,
    open_settings,

    # 🔒 Power Controls
    lock_pc, shutdown_pc, restart_pc, sleep_pc,

    # 📸 Screenshots
    take_screenshot, take_screenshot_timestamp, take_region_screenshot,

    # ⌨️ Keyboard / Mouse
    type_text_anywhere, copy_text, paste_text, cut_text,
    undo_action, redo_action, press_enter, scroll_up,
    scroll_down, switch_window, close_window,
    minimize_windows, maximize_window, minimize_window,

    # 🎵 Media
    next_track, previous_track, play_pause,

    # 📋 Clipboard
    read_clipboard, clear_clipboard,

    # 🔋 System Info
    get_battery_status, get_cpu_usage, get_ram_usage, get_disk_usage,

    # 🌞 Brightness
    increase_brightness, decrease_brightness, get_brightness,
])