#!/usr/bin/env python3
"""
Video Animator: Converts still images to animated video clips using Fal.ai Wan 2.5
Runs after 2_assets_fetcher.py generates images.
Uses image-to-video to create motion video matching audio duration.
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

def animate_image_to_video(image_path: str, scene_id: int, duration: float) -> bool:
    """Convert still image to animated video using Fal.ai Wan 2.5 image-to-video"""

    if not FAL_KEY or FAL_KEY == "your_fal_key_here":
        print(f"  ⚠️  Fal.ai API key not configured (skipping animation for scene_{scene_id})")
        return False

    try:
        # Read image and convert to base64 for Fal.ai
        with open(image_path, 'rb') as f:
            image_data = f.read()

        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        image_base64_url = f"data:image/png;base64,{image_base64}"

        # Fal.ai Wan 2.5 image-to-video endpoint
        url = "https://fal.run/fal-ai/wan/image-to-video"
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }

        # Limit duration to reasonable bounds (Wan 2.5 supports up to ~10 seconds)
        video_duration = min(duration, 10.0)

        payload = {
            "image_url": image_base64_url,
            "duration": video_duration,
            "cfgs": 7.5,
            "motion_bucket_id": 127,
            "fps": 24,
            "seed": 42 + scene_id  # Deterministic but varied per scene
        }

        print(f"  📹 Requesting Wan 2.5 animation ({video_duration:.1f}s)...")
        response = requests.post(url, json=payload, headers=headers, timeout=120)

        if response.status_code != 200:
            print(f"  ⚠️  HTTP {response.status_code}: {response.text[:200]}")
            return False

        result = response.json()

        # Parse response for video URL
        video_url = None
        if "video" in result:
            if isinstance(result["video"], dict) and "url" in result["video"]:
                video_url = result["video"]["url"]
            elif isinstance(result["video"], str):
                video_url = result["video"]
        elif "video_url" in result:
            video_url = result["video_url"]

        if not video_url:
            print(f"  ⚠️  No video URL in response: {result}")
            return False

        # Download video
        print(f"  ⬇️  Downloading animated video...")
        video_response = requests.get(video_url, timeout=60)
        video_response.raise_for_status()

        output_path = f"output/videos/scene_{scene_id}.mp4"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(video_response.content)

        print(f"  ✓ Video animation complete")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"  ⚠️  HTTP Error {e.response.status_code}")
        print(f"     Response: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"  ⚠️  Animation error: {e}")
        return False

def animate_all_videos():
    """Generate animated videos for all scenes"""
    print("🎬 Animating images with Wan 2.5 video generation...\n")

    scenes_data = load_scenes()
    scenes = scenes_data['scenes']

    success_count = 0
    fail_count = 0

    for scene in scenes:
        scene_id = scene['scene_id']
        image_path = f"output/images/scene_{scene_id}.png"
        audio_path = f"output/audio/scene_{scene_id}.mp3"

        if not Path(image_path).exists():
            print(f"📍 Scene {scene_id}: ⚠️  Image not found, skipping")
            continue

        duration = get_audio_duration(audio_path)
        print(f"📍 Scene {scene_id}/{len(scenes)}:")

        if animate_image_to_video(image_path, scene_id, duration):
            success_count += 1
            print()
        else:
            fail_count += 1
            print()

        # Rate limiting: Fal.ai has queue, wait between requests
        if scene_id < len(scenes):
            time.sleep(2)

    print(f"✓ Animation complete!")
    print(f"  ✓ Successful: {success_count} scenes")
    print(f"  ✗ Failed: {fail_count} scenes")
    print(f"  📁 Videos: output/videos/scene_*.mp4")

if __name__ == "__main__":
    animate_all_videos()
