import os
import random
import speech_recognition as sr
import pyttsx3

# === Customizable Mappings ===
COMMANDS = {
    "notes": "Notes",
    "safari": "Safari",
    "calculator": "Calculator",
    "selfsync": "/Users/peteryoussef/DevProjects/SelfSync",
    "finder": "Finder"
}

WAKE_RESPONSES = [
    "Welcome, Master Peter.",
    "At your command.",
    "Yes, Peter?",
    "I'm ready.",
    "How can I serve you?",
    "Awaiting orders."
]

# === Setup Text-to-Speech Engine ===
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # speaking speed

def say(text):
    engine.say(text)
    engine.runAndWait()

# === Transcription Function ===
def transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your command...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
        except:
            return ""

# === Command Execution ===
def execute(command):
    for keyword in COMMANDS:
        if keyword in command:
            phrase = keyword
            target = COMMANDS[keyword]
            response = random.choice(WAKE_RESPONSES)
            print(f"🧠 Heard: '{command}' → matched '{phrase}'")
            say(response)
            os.system(f"open -a \"{target}\"" if target.endswith(".app") or target in ["Notes", "Safari", "Calculator", "Finder"] else f"open \"{target}\"")
            return

    if "power off" in command:
        say("Powering down. Goodbye, Peter.")
        print("👋 SelfSync shutting down...")
        exit()

    print("❌ Sorry, I didn’t understand that command.")
    say("Sorry, I didn’t understand that.")

# === Looping Entry Point ===
if __name__ == "__main__":
    while True:
        spoken = transcribe()
        execute(spoken)