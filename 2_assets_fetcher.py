#!/usr/bin/env python3
"""
Ses ve Görsel İndirici: ElevenLabs ve Fal.ai API'lerini kullanarak
her sahne için ses ve görsel üretiyor.
"""

import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
FAL_KEY = os.getenv("FAL_KEY")

def load_scenes(scenes_path: str = "scenes.json") -> dict:
    with open(scenes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_voiceover(text: str, scene_id: int, voice_id: str = ELEVENLABS_VOICE_ID) -> bool:
    """ElevenLabs API ile ses üretiyor"""
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_key_here":
        print(f"  ⚠️  ElevenLabs API key ayarlanmadı (scene_{scene_id}.mp3 simüle ediliyor)")
        output_path = f"output/audio/scene_{scene_id}.mp3"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).touch()
        return True

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        output_path = f"output/audio/scene_{scene_id}.mp3"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True

    except Exception as e:
        print(f"  ⚠️  ElevenLabs hatası (scene_{scene_id}): {e}")
        return False

def generate_image(prompt: str, scene_id: int) -> bool:
    """Fal.ai (Flux-dev) API ile görsel üretiyor"""
    if not FAL_KEY or FAL_KEY == "your_fal_key_here":
        print(f"  ⚠️  Fal.ai API key ayarlanmadı (scene_{scene_id}.png simüle ediliyor)")
        output_path = f"output/images/scene_{scene_id}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        img = Image.new('RGB', (1920, 1080), color=(73, 109, 137))
        img.save(output_path)
        return True

    try:
        url = "https://api.fal.ai/v1/flux-dev"
        headers = {"Authorization": f"Key {FAL_KEY}"}
        payload = {
            "prompt": prompt,
            "image_size": {
                "width": 1920,
                "height": 1080
            },
            "num_inference_steps": 25,
            "guidance_scale": 3.5
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()

        result = response.json()
        if "image" in result and "url" in result["image"]:
            img_url = result["image"]["url"]
            img_response = requests.get(img_url, timeout=30)
            img_response.raise_for_status()

            output_path = f"output/images/scene_{scene_id}.png"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(img_response.content)

            return True
        else:
            print(f"  ⚠️  Fal.ai'den beklenmeyen yanıt (scene_{scene_id})")
            return False

    except Exception as e:
        print(f"  ⚠️  Fal.ai hatası (scene_{scene_id}): {e}")
        return False

def fetch_all_assets():
    """Tüm sahneler için ses ve görsel üretiyor"""
    print("📦 Sahne verileri yükleniyor...")
    scenes_data = load_scenes()
    scenes = scenes_data['scenes']
    character_desc = scenes_data['character_description']

    print(f"✓ {len(scenes)} sahne yüklendi\n")
    print(f"🎨 Karakter: {character_desc}\n")

    for scene in scenes:
        scene_id = scene['scene_id']
        voiceover = scene['voiceover_text']
        image_prompt = scene['image_prompt']

        print(f"📍 Sahne {scene_id}/{len(scenes)}:")

        print(f"  🎤 Seslendirme üretiliyor...")
        generate_voiceover(voiceover, scene_id)

        print(f"  🖼️  Görsel üretiliyor...")
        generate_image(f"{character_desc}. {image_prompt}", scene_id)

        time.sleep(1)
        print()

    print("✓ Tüm assetler hazır!")
    print(f"  - Ses dosyaları: output/audio/scene_*.mp3")
    print(f"  - Görsel dosyaları: output/images/scene_*.png")

if __name__ == "__main__":
    fetch_all_assets()
