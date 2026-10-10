
import requests
import sounddevice as sd
import numpy as np
import pyttsx3
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
RECORD_SECONDS = 5
API_URL = "http://127.0.0.1:8000/ask"

print("Loading speech recognition model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8",
)


def speak(text: str):
    text = str(text).strip()

    if not text:
        print("No text available to speak.")
        return

    print(f"\nLeadPilot: {text}")
    print("DEBUG: Starting Windows speech engine...")

    engine = None

    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("volume", 1.0)
        engine.setProperty("rate", 135)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

        print("DEBUG: Speech playback completed.")

    except Exception as error:
        print(f"DEBUG: Text-to-speech failed: {error}")

    finally:
        if engine is not None:
            del engine


def listen() -> str:
    print(f"\nListening for {RECORD_SECONDS} seconds...")

    try:
        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        audio = np.squeeze(audio)

        segments, _ = model.transcribe(
            audio,
            language="en",
            vad_filter=True,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        print(f"You: {text or '[No speech detected]'}")
        return text

    except Exception as error:
        print(f"DEBUG: Audio or transcription error: {error}")
        return ""


def ask_leadpilot(question: str) -> str:
    try:
        print("DEBUG: Sending question to API...")

        response = requests.post(
            API_URL,
            json={"query": question},
            timeout=180,
        )
        response.raise_for_status()

        answer = response.json().get("answer", "").strip()

        print("DEBUG: API response received.")
        return answer or "Sorry, I couldn't retrieve an answer."

    except requests.RequestException as error:
        print(f"DEBUG: API error: {error}")
        return (
            "I'm having trouble connecting to LeadPilot "
            "right now. Please try again."
        )


def main():
    speak(
        "Hello! LeadPilot is ready. "
        "Ask me a question. Say stop or exit to finish."
    )

    while True:
        question = listen()

        if not question:
            print("No question detected. Listening again.")
            continue

        command = question.lower().strip().rstrip(".!?")

        if command in {"stop", "exit", "quit", "goodbye"}:
            speak("Goodbye! Thanks for talking with LeadPilot.")
            break

        answer = ask_leadpilot(question)
        speak(answer)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVoice session stopped.")
