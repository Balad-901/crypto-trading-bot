# podcast/podcast_scanner.py

import os
import sys
import whisper
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm.summary_agent import summarize_and_score
from utils.influencer_detector import detect_influencers
from utils.topic_classifier import classify_topic
from memory.writer import save_memory_summary

# ✅ Fixed: Use working test MP3 instead of broken podcast
SAMPLE_AUDIO_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def download_sample_audio(output_path="test_audio.mp3"):
    if os.path.exists(output_path):
        return output_path

    print("⬇️ Downloading sample podcast...")
    response = requests.get(SAMPLE_AUDIO_URL)
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path

def transcribe_audio(file_path):
    print("🎙️ Transcribing with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def analyze_podcast(symbol="BTCUSDT"):
    audio_path = download_sample_audio()
    transcript = transcribe_audio(audio_path)

    summary, sentiment, _ = summarize_and_score(transcript)
    topic = classify_topic(summary)
    influencers, influencer_boost = detect_influencers(transcript)

    print(f"🎧 Podcast Summary: {summary[:100]}...")
    print(f"🧠 Topic: {topic} | Sentiment: {sentiment} | Influencers: {influencers}")

    save_memory_summary(
        symbol=symbol,
        summary=summary,
        sentiment=sentiment,
        topic=topic,
        extra={
            "influencers": influencers,
            "influencer_boost": influencer_boost,
            "source": SAMPLE_AUDIO_URL
        }
    )

# Run directly
if __name__ == "__main__":
    analyze_podcast()
