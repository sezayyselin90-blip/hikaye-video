#!/usr/bin/env python3
"""
English TTS Audio Generator: Generates voiceover audio using ElevenLabs
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

def parse_english_scenario(txt_path: str) -> list:
    """Parse English scenario file into scenes"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    scenes = []
    scene_pattern = r'\[SCENE (\d+)\] \((\d+)s\)\nSpeaker: (.+?)\nText: (.+?)\nVisual:'

    matches = re.finditer(scene_pattern, content, re.DOTALL)
    for match in matches:
        scene_id = int(match.group(1))
        duration = int(match.group(2))
        speaker = match.group(3).strip()
        text = match.group(4).strip()

        scenes.append({
            'scene_id': scene_id,
            'duration': duration,
            'speaker': speaker,
            'text': text
        })

    return scenes

def generate_tts_audio(text: str, voice_id: str, output_path: str) -> bool:
    """Generate TTS audio using ElevenLabs"""
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        print("  ⚠️  ElevenLabs API key not found")
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"  ✗ ElevenLabs error: {response.status_code}")
            return False

    except Exception as e:
        print(f"  ✗ TTS error: {e}")
        return False

def main():
    scenario_path = "scripts/hikaye_13min_full.txt"
    voice_id = "AIJ0ViCZ83NSXLNIERjD"  # Warm agent voice

    if not Path(scenario_path).exists():
        print(f"Error: {scenario_path} not found!")
        return

    print("📖 Parsing English scenario...")
    scenes = parse_english_scenario(scenario_path)
    print(f"✓ Found {len(scenes)} scenes\n")

    print("🎙️ Generating TTS audio with ElevenLabs...")
    print(f"   Voice: Warm Agent (Soothing American Assistant)")
    print(f"   Voice ID: {voice_id}\n")

    audio_dir = "audio_english"
    Path(audio_dir).mkdir(exist_ok=True)

    success_count = 0
    for scene in scenes:
        scene_id = scene['scene_id']
        text = scene['text']
        output_path = f"{audio_dir}/scene_{scene_id:03d}.mp3"

        print(f"[SCENE {scene_id:02d}] {text[:50]}...", end=' ')

        if generate_tts_audio(text, voice_id, output_path):
            print("✓")
            success_count += 1
        else:
            print("✗")

    print(f"\n✓ Generated {success_count}/{len(scenes)} audio files")

    # Save metadata
    metadata = {
        "voice_id": voice_id,
        "voice_name": "Warm Agent (Soothing American Assistant)",
        "language": "English",
        "scenes": scenes,
        "audio_dir": audio_dir
    }

    with open("metadata_audio_english.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 80)
    print("✅ ENGLISH AUDIO GENERATION COMPLETE!")
    print("=" * 80)
    print(f"\n🎵 Audio files: {audio_dir}/")
    print(f"📋 Metadata: metadata_audio_english.json")
    print(f"\nTotal scenes: {len(scenes)}")
    print(f"Successfully generated: {success_count}/{len(scenes)}")

if __name__ == "__main__":
    main()
