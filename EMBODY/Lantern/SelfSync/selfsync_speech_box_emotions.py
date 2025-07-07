import requests
import json
import os

# === ElevenLabs API Settings ===
ELEVEN_API_KEY = "sk_1eeb4f175a3ba0bce00815704fadfbc786c2ddf54b67ac9a"  # your real key
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

def speak_emotionally(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # this matches Rachel
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        os.system("afplay output.mp3")  # Mac playback
    else:
        print("❌ ElevenLabs Error:", response.status_code, response.text)


# === Run Test ===
if __name__ == "__main__":
    test_lines = [
        "Hey, it's me. How are you doing today?",
        "I'm here if you need to talk."
    ]

    for line in test_lines:
        speak_emotionally(line)