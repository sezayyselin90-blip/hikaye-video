#!/usr/bin/env python3
"""
English Visual Assets Generator: Creates 5-second visual segments and Flux prompts
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def parse_english_scenario(txt_path: str) -> list:
    """Parse English scenario file"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    scenes = []
    scene_pattern = r'\[SCENE (\d+)\] \((\d+)s\)\nSpeaker: (.+?)\nText: (.+?)\nVisual: (.+?)(?:\n\[SCENE|\n---|\Z)'

    matches = re.finditer(scene_pattern, content, re.DOTALL)
    for match in matches:
        scene_id = int(match.group(1))
        duration = int(match.group(2))
        speaker = match.group(3).strip()
        text = match.group(4).strip()
        visual_prompt = match.group(5).strip()

        scenes.append({
            'scene_id': scene_id,
            'duration': duration,
            'speaker': speaker,
            'text': text,
            'visual_prompt': visual_prompt
        })

    return scenes

def create_visual_segments(scenes: list) -> list:
    """Split scenes into 5-second visual segments"""
    segments = []
    segment_id = 1
    current_time = 0

    for scene in scenes:
        duration = scene['duration']
        scene_id = scene['scene_id']
        visual_prompt = scene['visual_prompt']
        text = scene['text']

        num_segments = (duration + 4) // 5
        segment_duration = duration / num_segments if num_segments > 0 else duration

        for seg_idx in range(num_segments):
            segments.append({
                'segment_id': segment_id,
                'scene_id': scene_id,
                'start_time': current_time,
                'duration': segment_duration,
                'visual_prompt': visual_prompt,
                'text_excerpt': text[:50] + "..." if len(text) > 50 else text
            })
            segment_id += 1
            current_time += segment_duration

    return segments

def generate_flux_prompt(visual_prompt: str) -> str:
    """Create Flux Dev optimized prompt"""
    prompt = f"""{visual_prompt}

    [Quality: 8K, cinematic, professional, high detail]
    [Style: photorealistic, dramatic lighting, 16:9 aspect ratio]
    [Technical: ultra sharp focus, color graded]"""

    return prompt

def main():
    scenario_path = "scripts/hikaye_english_full.txt"

    if not Path(scenario_path).exists():
        print(f"Error: {scenario_path} not found!")
        return

    print("📖 Parsing English scenario...")
    scenes = parse_english_scenario(scenario_path)
    print(f"✓ Found {len(scenes)} scenes\n")

    print("📏 Splitting scenes into 5-second visual segments...")
    segments = create_visual_segments(scenes)
    print(f"✓ Created {len(segments)} visual segments\n")

    total_duration = sum(seg['duration'] for seg in segments)
    minutes = int(total_duration) // 60
    seconds = int(total_duration) % 60

    print(f"⏱️  Total video duration: {minutes}m {seconds}s\n")

    print("🎨 Preparing Flux Dev prompts...")

    # Save metadata
    metadata = {
        'total_scenes': len(scenes),
        'total_segments': len(segments),
        'total_duration': total_duration,
        'segments': segments,
        'batches': (len(segments) + 9) // 10
    }

    with open("metadata_visuals_english.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    # Save Flux prompts
    flux_prompts = []
    for seg in segments:
        flux_prompts.append({
            'segment_id': seg['segment_id'],
            'prompt': generate_flux_prompt(seg['visual_prompt']),
            'negative_prompt': 'blurry, low quality, distorted, watermark',
            'scene_id': seg['scene_id'],
            'duration': seg['duration']
        })

    with open("flux_prompts_english.json", 'w', encoding='utf-8') as f:
        json.dump(flux_prompts, f, indent=2)

    print("✓ Prompts prepared\n")

    print("=" * 80)
    print("✅ ENGLISH VISUAL ASSET PREPARATION COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Statistics:")
    print(f"   • Original scenes: {len(scenes)}")
    print(f"   • Visual segments: {len(segments)}")
    print(f"   • Total duration: {minutes}m {seconds}s")
    print(f"   • Batch count: {metadata['batches']}")
    print(f"\n📝 Metadata files:")
    print(f"   • metadata_visuals_english.json")
    print(f"   • flux_prompts_english.json")
    print(f"\n💰 Estimated cost: ${len(segments) * 0.05:.2f} USD (Flux Dev)")

if __name__ == "__main__":
    main()
