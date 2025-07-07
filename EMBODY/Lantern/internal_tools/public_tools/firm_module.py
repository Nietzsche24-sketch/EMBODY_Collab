from pydub.utils import mediainfo
import os

def inspect_audio(filepath):
    try:
        info = mediainfo(filepath)
        duration_sec = float(info.get("duration", 0))
        sample_width = int(info.get("bits_per_sample", 16))
        channels = int(info.get("channels", 2))
        frame_rate = int(info.get("sample_rate", 44100))
        file_size_kb = os.path.getsize(filepath) / 1024

        score = 100
        issues = []

        if duration_sec < 1:
            score -= 40
            issues.append("File too short")
        if file_size_kb < 10:
            score -= 30
            issues.append("File size unusually small")
        if channels < 1:
            score -= 20
            issues.append("No audio channels detected")

        status = (
            "✅ Healthy" if score >= 90 else
            "⚠️ Issues Detected" if score >= 60 else
            "❌ Likely Damaged"
        )

        metadata = {
            "📁 File": filepath,
            "🔊 Channels": channels,
            "🎚️ Sample Width": f"{sample_width} bits",
            "📈 Frame Rate": f"{frame_rate} Hz",
            "⏱️ Duration": f"{duration_sec:.2f} seconds",
            "📦 File Size": f"{file_size_kb:.1f} KB",
            "💯 Score": f"{score}/100",
            "📌 Status": status,
        }

        if issues:
            metadata["🛠️ Suggestions"] = "; ".join(issues)

        return metadata

    except Exception as e:
        return {"❌ Error": f"Could not inspect {filepath}: {e}"}
