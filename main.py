import asyncio
import os
import speech_recognition as sr
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from agents.agent import voice_agent
from utils.voice_output import speak
from utils.log import add_log
import threading
import socket
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Set your Google API Key
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY not found. Check your .env file.")

os.environ["GOOGLE_API_KEY"] = api_key
# Wake word
WAKE_WORD = os.getenv("WAKE_WORD", "DEXA")

# ---------- LISTENERS ---------- #
async def text_listener(runner, user_id, session_id, stop_event):
    print("⌨️ Text mode enabled. Type your command (or 'exit' to quit).")

    while not stop_event.is_set():
        text = input("You: ").strip()
        if text.lower() == "exit":
            stop_event.set()
            break

        if not text:
            continue

        # Send text to AI
        content = types.Content(role="user", parts=[types.Part(text=text)])
        events = runner.run(user_id=user_id, session_id=session_id, new_message=content)

        for event in events:
            if event.is_final_response():
                response = (
                    event.content.parts[0].text
                    if event.content and event.content.parts
                    else "<no response>"
                )
               
                print(" Agent Response:", response)
                speak(response)




async def tcp_listener(runner, user_id, session_id, stop_event, host='0.0.0.0', port=5000):
    import socket
    import asyncio

    print(f"Starting TCP listener on {host}:{port}...")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen()

    loop = asyncio.get_running_loop()
    print(" Waiting for Android client to connect...")
    client_sock, addr = await loop.run_in_executor(None, server_sock.accept)
    print(f"Connected by {addr}")

    client_sock.setblocking(False)

    async def handle_client():
        while not stop_event.is_set():
            try:
                data = await loop.sock_recv(client_sock, 1024)
                if not data:
                    print(" Client disconnected")
                    break

                text = data.decode("utf-8").strip()
                print(f" Received TCP message: {text}")

                add_log("REMOTE",text)

                # --- Safe runner call to prevent tool errors ---
                try:
                    content = types.Content(role="user", parts=[types.Part(text=text)])
                    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)

                    for event in events:
                        if event.is_final_response():
                            response = (
                                event.content.parts[0].text
                                if event.content and event.content.parts
                                else "<no response>"
                            )
                            print(" Agent Response:", response)
                            add_log("RESPONSE",response)
                            speak(response)

                            # Send response back to client
                            await loop.sock_sendall(client_sock, (response + "\n").encode("utf-8"))

                except Exception as e:
                    # Catch function-calling/tool errors here
                    response = "Sorry, I cannot perform that action right now."
                    print(f"⚠️ Runner Error: {e}")
                    await loop.sock_sendall(client_sock, (response + "\n").encode("utf-8"))

            except (BlockingIOError, ConnectionResetError):
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"⚠️ TCP Error: {e}")
                break

    try:
        await handle_client()
    finally:
        print(" Closing TCP connection")
        client_sock.close()
        server_sock.close()
        print(" TCP listener stopped.")
async def mic_listener(runner, user_id, session_id, stop_event):
    recognizer = sr.Recognizer()
    wakeword_enabled = os.getenv("WAKE_WORD_ENABLED", "1") == "1"
    wake_word = os.getenv("WAKE_WORD", "DEXA")

    print(f"Listening... Wake word mode = {wakeword_enabled} (word='{wake_word}')")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while not stop_event.is_set():
            print(" Say something...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                text = recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                 

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f" Speech API error: {e}")
                continue

            


            if wakeword_enabled:
                words = text.split()
                if not (words and words[0] == wake_word):
                    continue
                command = " ".join(words[1:]).strip()
            else:
                command = text

            print(f" Command: {command}")
            add_log("LOCAL",command)

            content = types.Content(role="user", parts=[types.Part(text=command)])
            events = runner.run(user_id=user_id, session_id=session_id, new_message=content)

            for event in events:
                if event.is_final_response():
                    response = (
                        event.content.parts[0].text
                        if event.content and event.content.parts
                        else "<no response>"
                    )
                    print(" Agent Response:", response)
                    add_log("RESPONSE",response)
                    speak(response)


# ---------- MAIN ---------- #
async def main(stop_event, tcp_enabled=True, mic_enabled=False, wake_word_enabled=True, wake_word="alexa"):
    session_service = InMemorySessionService()
    user_id = "user1"
    session_id = "session1"
    session_service.create_session(app_name="agent_app", user_id=user_id, session_id=session_id)
    runner = Runner(agent=voice_agent, app_name="agent_app", session_service=session_service)

    tasks = []

    # Start TCP listener if enabled
    if tcp_enabled:
        tcp_task = asyncio.create_task(tcp_listener(runner, user_id, session_id, stop_event))
        tasks.append(tcp_task)

    # Start mic listener if enabled
    if mic_enabled:
        mic_thread = threading.Thread(target=lambda: asyncio.run(
            mic_listener(runner, user_id, session_id, stop_event)
        ))
        mic_thread.start()

    # Keep main alive until stop_event is set
    try:
        while not stop_event.is_set():
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass

    print(" Assistant stopped.")

    # Wait for mic thread to finish if started
    if mic_enabled:
        mic_thread.join()

    # Cancel TCP tasks if running
    for task in tasks:
        task.cancel()



if __name__ == "__main__":
    stop_event = asyncio.Event()

    # allow Ctrl+C to stop gracefully
    def handle_sigint(sig, frame):
        print("Ctrl+C detected. Stopping assistant...")
        stop_event.set()

    signal.signal(signal.SIGINT, handle_sigint)

    asyncio.run(main(stop_event))
