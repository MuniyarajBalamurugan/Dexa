#voice_output.py
import pyttsx3
import os

def speak(text: str):
    """Convert text to speech."""
    
    # Check if TTS is enabled via environment variable (default: enabled)
    tts_enabled = os.getenv('TTS_ENABLED', '2')  # '1' = enabled, '0' = disabled
    if tts_enabled != '1':
        return  # Skip TTS if disabled

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Get voice index from environment variable, default to 0
    voice_index = int(os.getenv('TTS_VOICE_INDEX', 0))
    if voice_index < 0 or voice_index >= len(voices):
        voice_index = 0

    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()