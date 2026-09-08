#!/usr/bin/env python3
"""
Video Animator: Converts still images to animated video clips using Fal.ai Kling 2.5 Turbo Pro
Runs after 2_assets_fetcher.py generates images.
Uses image-to-video to create motion video matching audio duration.
Premium mode: Supports character consistency with reference images.
"""

import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

FAL_KEY = os.getenv("FAL_KEY")

def load_scenes(scenes_path: str = "scenes.json") -> dict:
    with open(scenes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_audio_duration(audio_path: str) -> float:
    """Get audio file duration"""
    import subprocess
    try:
        if os.path.getsize(audio_path) == 0:
            return 5.0
    except:
        pass

    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
             audio_path],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            return float(result.stdout.strip())
    except:
        pass

    return 5.0

def animate_image_to_video(image_path: str, scene_id: int, duration: float,
                          character_ref_image: str = None) -> bool:
    """Convert still image to animated video using Fal.ai Kling 2.5 Turbo Pro"""

    if not FAL_KEY or FAL_KEY == "your_fal_key_here":
        print(f"  ⚠️  Fal.ai API key not configured (skipping animation)")
        return False

    try:
        # Read image and convert to base64
        with open(image_path, 'rb') as f:
            image_data = f.read()

        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        image_base64_url = f"data:image/png;base64,{image_base64}"

        # Kling 2.5 Turbo Pro endpoint
        url = "https://fal.run/fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }

        # Kling max 10 seconds
        video_duration = min(duration, 10.0)

        payload = {
            "image_url": image_base64_url,
            "duration": video_duration,
            "mode": "default",
            "negative_prompt": "static camera, frozen, no motion",
            "seed": 42 + scene_id
        }

        print(f"  📹 Kling 2.5 Turbo Pro ({video_duration:.1f}s, ~${video_duration * 0.07:.2f})...")
        response = requests.post(url, json=payload, headers=headers, timeout=180)

        if response.status_code != 200:
            print(f"  ⚠️  HTTP {response.status_code}")
            try:
                error_msg = response.json().get('error', response.text[:100])
                print(f"     {error_msg}")
            except:
                print(f"     {response.text[:100]}")
            return False

        result = response.json()

        # Extract video URL
        video_url = None
        if "video" in result:
            if isinstance(result["video"], dict) and "url" in result["video"]:
                video_url = result["video"]["url"]
            elif isinstance(result["video"], str):
                video_url = result["video"]
        elif "video_url" in result:
            video_url = result["video_url"]

        if not video_url:
            print(f"  ⚠️  No video URL in response")
            return False

        # Download video
        print(f"  ⬇️  Downloading...")
        video_response = requests.get(video_url, timeout=60)
        video_response.raise_for_status()

        output_path = f"output/videos/scene_{scene_id}.mp4"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(video_response.content)

        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ Done ({file_size_mb:.1f}MB)")
        return True

    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        return False

def animate_all_videos():
    """Generate Kling 2.5 Turbo Pro animated videos for all scenes"""
    print("🎬 Kling 2.5 Turbo Pro: Full motion video generation\n")

    scenes_data = load_scenes()
    scenes = scenes_data['scenes']

    success_count = 0
    total_cost = 0

    for scene in scenes:
        scene_id = scene['scene_id']
        image_path = f"output/images/scene_{scene_id}.png"
        audio_path = f"output/audio/scene_{scene_id}.mp3"

        if not Path(image_path).exists():
            print(f"📍 Scene {scene_id}: ⚠️  Image not found")
            continue

        duration = get_audio_duration(audio_path)
        cost = duration * 0.07  # Kling pricing: $0.07/second
        total_cost += cost

        print(f"📍 Scene {scene_id}/{len(scenes)}:")
        print(f"     Duration: {duration:.1f}s | Cost: ${cost:.2f}")

        if animate_image_to_video(image_path, scene_id, duration):
            success_count += 1
            print()
        else:
            print()

        # Rate limiting
        if scene_id < len(scenes):
            time.sleep(3)

    print(f"{'='*50}")
    print(f"✓ Animation Complete!")
    print(f"  ✅ Successful: {success_count}/{len(scenes)} scenes")
    print(f"  💰 Total cost: ${total_cost:.2f}")
    print(f"  📁 Output: output/videos/scene_*.mp4")

    if success_count == len(scenes):
        print(f"\n✨ Ready for step 3: python 3_video_builder.py")

if __name__ == "__main__":
    animate_all_videos()
