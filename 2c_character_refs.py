#!/usr/bin/env python3
"""
Character Reference Generator: Creates consistent character reference images
Runs after 2_assets_fetcher.py generates initial images.
Generates focused character images for use in subsequent scenes.
Ensures character consistency across all video scenes (Premium mode).
"""

import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

FAL_KEY = os.getenv("FAL_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def load_scenes(scenes_path: str = "scenes.json") -> dict:
    with open(scenes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_character_first_scene(scenes: list, character: str) -> dict:
    """Find first scene where character appears"""
    for scene in scenes:
        if scene.get('speaker') == character:
            return scene
    return None

def generate_character_reference_image(character: str, description: str, scene_data: dict, scene_id: int) -> bool:
    """Generate focused character reference image using Fal.ai Flux Dev"""

    if not FAL_KEY or FAL_KEY == "your_fal_key_here":
        print(f"  ⚠️  Fal.ai key not configured")
        return False

    try:
        # Create character-focused prompt
        safety_instruction = "Clearly fictional character, no resemblance to real/famous people, illustration/animation style"
        character_prompt = f"{safety_instruction}. Close-up portrait of {character}: {description}. Character focus, professional headshot lighting."

        # Get scene's image prompt for context
        scene_image_prompt = scene_data.get('image_prompt', '')

        full_prompt = f"{character_prompt}. Scene context: {scene_image_prompt}"

        url = "https://fal.run/fal-ai/flux/dev"
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": full_prompt,
            "image_size": "landscape_16_9",
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": hash(character) % 10000  # Deterministic per character
        }

        print(f"  🎨 Generating {character} reference image...")
        response = requests.post(url, json=payload, headers=headers, timeout=120)

        if response.status_code != 200:
            print(f"  ⚠️  HTTP {response.status_code}: {response.text[:100]}")
            return False

        result = response.json()

        # Parse response
        img_url = None
        if "images" in result and len(result["images"]) > 0:
            img_url = result["images"][0].get("url")
        elif "image" in result:
            if isinstance(result["image"], dict) and "url" in result["image"]:
                img_url = result["image"]["url"]

        if not img_url:
            print(f"  ⚠️  No image URL in response")
            return False

        # Download image
        print(f"  ⬇️  Downloading reference image...")
        img_response = requests.get(img_url, timeout=30)
        img_response.raise_for_status()

        output_path = f"output/character_refs/{character.lower()}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(img_response.content)

        print(f"  ✓ Reference image saved")
        return True

    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        return False

def generate_all_character_refs():
    """Generate reference images for all unique characters"""
    print("👥 Character Reference Generator (Premium Mode)\n")

    scenes_data = load_scenes()
    scenes = scenes_data['scenes']
    characters = scenes_data.get('characters', {})
    char_description = scenes_data.get('character_description', '')

    # Find unique speakers
    unique_speakers = set()
    for scene in scenes:
        speaker = scene.get('speaker', 'Narrator')
        unique_speakers.add(speaker)

    unique_speakers = sorted(list(unique_speakers))

    if not unique_speakers:
        print("❌ No characters found in scenes")
        return

    print(f"Found {len(unique_speakers)} characters: {', '.join(unique_speakers)}\n")

    success_count = 0

    for character in unique_speakers:
        print(f"📌 {character}:")

        # Find first scene with this character
        first_scene = find_character_first_scene(scenes, character)
        if not first_scene:
            print(f"  ⚠️  No scenes found for this character\n")
            continue

        # Get character description
        desc = characters.get(character, {}).get('description', f'{character} character')

        if generate_character_reference_image(character, desc, first_scene, first_scene['scene_id']):
            success_count += 1

        print()

        # Rate limiting
        time.sleep(2)

    print(f"{'='*50}")
    print(f"✓ Character References Complete!")
    print(f"  ✅ Generated: {success_count}/{len(unique_speakers)} character references")
    print(f"  📁 Output: output/character_refs/*.png")

    if success_count == len(unique_speakers):
        print(f"\n✨ Ready for step 2b: python 2b_animate_videos.py")

if __name__ == "__main__":
    generate_all_character_refs()
