import os
import requests
import openai
import time
import uuid

# CONFIGURATION
ELEVENLABS_API_KEY = "sk_4a7e2e6fd7e46745fe7307b11c4efaf3be20f0bf524454fd"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # replace with your cloned voice ID
OPENAI_API_KEY = "your-openai-api-key"  # ← REPLACE with your real OpenAI key

# AUDIO FILE NAME
recorded_wav = "user_input.wav"

def record_voice():
    print("🎙️ Listening... Speak into the mic (Ctrl+C to stop)")
    os.system(f"ffmpeg -f avfoundation -i ':0' -t 5 -y {recorded_wav} > /dev/null 2>&1")

def transcribe_audio():
    print("📝 Transcribing...")
    result = os.popen(f"whisper {recorded_wav} --model tiny --language en --fp16 False --output_format txt").read()
    transcript_file = recorded_wav.replace(".wav", ".txt")
    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as f:
            return f.read().strip()
    return ""

def chat_with_gpt(prompt):
    print("🤖 Generating reply...")
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an emotional personal assistant named SelfSync. Reply with expressive tone."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def speak_emotionally(text):
    print("🗣️ Speaking with emotion...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.75,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        output_mp3 = f"reply_{uuid.uuid4()}.mp3"
        with open(output_mp3, "wb") as f:
            f.write(response.content)
        os.system(f"afplay {output_mp3}")
        os.remove(output_mp3)
    else:
        print("❌ ElevenLabs error:", response.text)

if __name__ == "__main__":
    while True:
        record_voice()
        user_text = transcribe_audio()
        if not user_text:
            print("⚠️ No speech detected. Try again.\n")
            continue
        print(f"👤 You said: {user_text}")
        reply = chat_with_gpt(user_text)
        print(f"🤖 SelfSync replies: {reply}")
        speak_emotionally(reply)
        time.sleep(1)