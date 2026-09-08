#!/usr/bin/env python3
"""
Audio & Image Fetcher: Generates English voiceover and AI images
using ElevenLabs and Fal.ai APIs for each scene.
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
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "TxGEqnHWrfWFTfGW9XjX")
ELEVENLABS_LANGUAGE = os.getenv("ELEVENLABS_LANGUAGE", "en")
FAL_KEY = os.getenv("FAL_KEY")

def load_scenes(scenes_path: str = "scenes.json") -> dict:
    with open(scenes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_voiceover(text: str, scene_id: int, voice_id: str = ELEVENLABS_VOICE_ID, speaker: str = None) -> bool:
    """Generate English voiceover with character-specific voice"""
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_key_here":
        speaker_label = f" ({speaker})" if speaker else ""
        print(f"  ⚠️  ElevenLabs API key not configured (simulating scene_{scene_id}.mp3{speaker_label})")
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
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        # Debug first request
        if scene_id == 1:
            import json as json_module
            print(f"  🔧 DEBUG - ElevenLabs Request:")
            print(f"     URL: {url}")
            print(f"     Headers: xi-api-key={ELEVENLABS_API_KEY[:10]}..., Content-Type=application/json")
            print(f"     Payload: {json_module.dumps(payload, indent=6)}")

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        output_path = f"output/audio/scene_{scene_id}.mp3"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True

    except requests.exceptions.HTTPError as e:
        speaker_label = f" ({speaker})" if speaker else ""
        print(f"  ⚠️  ElevenLabs HTTP Error {e.response.status_code} (scene_{scene_id}{speaker_label})")
        print(f"     URL: {e.response.url}")
        print(f"     Response: {e.response.text}")
        return False
    except Exception as e:
        speaker_label = f" ({speaker})" if speaker else ""
        print(f"  ⚠️  ElevenLabs error (scene_{scene_id}{speaker_label}): {e}")
        return False

def generate_image(prompt: str, scene_id: int) -> bool:
    """Generate images using Fal.ai Flux-dev API"""
    if not FAL_KEY or FAL_KEY == "your_fal_key_here":
        print(f"  ⚠️  Fal.ai API key not configured (simulating scene_{scene_id}.png)")
        output_path = f"output/images/scene_{scene_id}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        img = Image.new('RGB', (1920, 1080), color=(73, 109, 137))
        img.save(output_path)
        return True

    try:
        url = "https://fal.run/fal-ai/flux/dev"
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "image_size": "landscape_16_9",
            "num_inference_steps": 25,
            "guidance_scale": 3.5
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()

        result = response.json()

        # Try multiple response formats - Fal.ai returns different structures
        img_url = None
        if "images" in result and len(result["images"]) > 0:
            # New format: {"images": [{"url": "..."}]}
            img_url = result["images"][0].get("url")
        elif "image" in result:
            # Legacy format: {"image": {"url": "..."}}
            if isinstance(result["image"], dict) and "url" in result["image"]:
                img_url = result["image"]["url"]
            elif isinstance(result["image"], str):
                # Direct URL string
                img_url = result["image"]

        if not img_url:
            print(f"  ⚠️  Unexpected response from Fal.ai (scene_{scene_id})")
            print(f"     Response: {result}")
            return False

        img_response = requests.get(img_url, timeout=30)
        img_response.raise_for_status()

        output_path = f"output/images/scene_{scene_id}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(img_response.content)

        return True

    except requests.exceptions.HTTPError as e:
        print(f"  ⚠️  Fal.ai HTTP Error {e.response.status_code} (scene_{scene_id})")
        print(f"     URL: {e.response.url}")
        print(f"     Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"  ⚠️  Fal.ai error (scene_{scene_id}): {e}")
        return False

def fetch_all_assets():
    """Generate audio and visual assets for all scenes"""
    print("📦 Loading scene data...")

    # Debug: Show what API keys are configured
    print("\n🔍 Debug - API Configuration:")
    print(f"   ELEVENLABS_API_KEY: {'✓ Set' if ELEVENLABS_API_KEY and ELEVENLABS_API_KEY != 'your_elevenlabs_key_here' else '✗ Not set'}")
    print(f"   ELEVENLABS_VOICE_ID: {ELEVENLABS_VOICE_ID}")
    print(f"   ELEVENLABS_LANGUAGE: {ELEVENLABS_LANGUAGE}")
    print(f"   FAL_KEY: {'✓ Set' if FAL_KEY and FAL_KEY != 'your_fal_key_here' else '✗ Not set'}")
    print()

    scenes_data = load_scenes()
    scenes = scenes_data['scenes']
    character_desc = scenes_data['character_description']
    characters = scenes_data.get('characters', {})

    print(f"✓ Loaded {len(scenes)} scenes\n")
    print(f"🎨 Characters: {character_desc}\n")

    if characters:
        print("🎙️  Multi-Character Voices:")
        for char_name, char_info in characters.items():
            voice_name = char_info.get('voice_name', 'Unknown')
            print(f"  • {char_name}: {voice_name}")
        print()

    for scene in scenes:
        scene_id = scene['scene_id']
        voiceover = scene['voiceover_text']
        image_prompt = scene['image_prompt']
        speaker = scene.get('speaker', 'Narrator')

        print(f"📍 Scene {scene_id}/{len(scenes)}:")

        # Get voice for speaker
        voice_id = ELEVENLABS_VOICE_ID
        if characters and speaker in characters:
            voice_id = characters[speaker].get('voice_id', ELEVENLABS_VOICE_ID)

        print(f"  🎤 Generating voiceover ({speaker})...")
        generate_voiceover(voiceover, scene_id, voice_id=voice_id, speaker=speaker)

        print(f"  🖼️  Generating image...")
        generate_image(f"{character_desc}. {image_prompt}", scene_id)

        time.sleep(1)
        print()

    print("✓ All assets ready!")
    print(f"  - Audio files: output/audio/scene_*.mp3 (multi-character)")
    print(f"  - Image files: output/images/scene_*.png")

if __name__ == "__main__":
    fetch_all_assets()
