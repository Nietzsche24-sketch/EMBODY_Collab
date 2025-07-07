import requests

ELEVEN_API_KEY = "sk_9a7cd015789418be31920b05e2f66241490b5e7a3b5834b3"  # Your actual key

url = "https://api.elevenlabs.io/v1/voices"
headers = {
    "xi-api-key": ELEVEN_API_KEY
}

response = requests.get(url, headers=headers)

if response.ok:
    voices = response.json()["voices"]
    print("\n🔊 Available Voices:")
    for v in voices:
        print(f"- {v['name']} (ID: {v['voice_id']})")
else:
    print("❌ Failed to fetch voices:", response.text)