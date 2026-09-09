#!/usr/bin/env python3
"""
İngilizce Senaryo Üretici: Orijinal İngilizce hikayeyi detaylı 59 sahneye bölüyor
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def load_story(story_path: str) -> str:
    with open(story_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_english_scenario(story: str) -> str:
    """İngilizce hikayeyi detaylı 59 sahneye bölüyor"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_key_here":
        print("  ⚠️  DEMO MODE: API key not found\n")
        return None

    client = Anthropic(api_key=api_key)

    system_prompt = """You are a professional screenplay writer and narrator. Your task:
1. Break the complete story into 55-60 scenes
2. Each scene should be 4-7 seconds of narration when read aloud
3. Preserve ALL narrative details - no condensing or summarizing
4. Create voiceover text for narrator (James voice)
5. Include character dialogue where appropriate
6. Create detailed visual prompts (16:9 Flux-compatible)
7. Maintain story continuity and emotional beats

OUTPUT FORMAT:
For each scene:
[SCENE N] (Xs)
Speaker: Narrator or Character Name
Text: [Full narration text - 4-7 seconds reading time]
Visual: [Detailed 16:9 visual description for Flux Dev]

IMPORTANT:
- Narrator voice for all non-dialogue narrative
- Preserve exact dialogue from original story
- Total must be 55-60 scenes covering entire story
- No summarization - include ALL key details and moments"""

    user_message = f"""Create a COMPLETE 55-60 scene breakdown of this story in English.
Each scene must be 4-7 seconds of narration. Cover the ENTIRE story with all details:

{story}

Create the full screenplay with detailed narration and visual prompts for each scene.
Output ONLY the scenes in the specified format, no additional text."""

    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=12000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        response_text = None
        for block in response.content:
            if hasattr(block, 'text'):
                response_text = block.text
                break

        if not response_text:
            raise ValueError("No text response from API")

        return response_text

    except Exception as e:
        print(f"  ⚠️  Claude API error: {e}")
        return None

def save_scenario_as_text(scenario_text: str, output_path: str = "scripts/hikaye_english_full.txt"):
    """Save scenario in English plain text format"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("STORY: COMPLETE ENGLISH SCENARIO\n")
        f.write("=" * 80 + "\n\n")
        f.write("NARRATOR: Warm Agent Voice (Soothing American Assistant)\n")
        f.write("LANGUAGE: English\n")
        f.write("FORMAT: 55-60 Scenes, Narrator-Only Voiceover\n\n")
        f.write("=" * 80 + "\n\n")
        f.write(scenario_text)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("NOTES:\n")
        f.write("=" * 80 + "\n")
        f.write("• Full story coverage with complete narrative detail\n")
        f.write("• Narrator voice: Warm, soothing American assistant\n")
        f.write("• Each scene optimized for 4-7 second reading time\n")
        f.write("• No condensing - all story elements preserved\n")
        f.write("• Visual prompts ready for Flux Dev generation\n")

    return output_path

def main():
    story_path = "story.txt"

    if not Path(story_path).exists():
        print(f"Error: {story_path} not found!")
        return

    print("📖 Loading original story...")
    story = load_story(story_path)
    print(f"✓ Story loaded ({len(story)} characters)\n")

    print("🎬 Claude API generating complete English scenario...")
    print("   (Preserving all narrative detail...)\n")

    scenario_text = generate_english_scenario(story)

    if not scenario_text:
        print("Scenario generation failed!")
        return

    print(f"✓ Scenario generated ({len(scenario_text)} characters)\n")

    print("💾 Saving English scenario...")
    txt_path = save_scenario_as_text(scenario_text)
    print(f"✓ Saved: {txt_path}\n")

    print("=" * 80)
    print("✅ ENGLISH SCENARIO READY!")
    print("=" * 80)
    print(f"\n📄 Scenario file: {txt_path}")
    print("\n📋 Content summary:")
    lines = scenario_text.split('\n')
    scene_count = len([l for l in lines if l.startswith('[SCENE')])
    print(f"   • Total scenes: {scene_count}")
    print(f"   • Total text: {len(scenario_text)} characters")
    print(f"   • Language: English")
    print(f"   • Narrator: Warm Agent Voice (AIJ0ViCZ83NSXLNIERjD)\n")

    print("=" * 80)
    print("✅ READY FOR ENGLISH VIDEO PRODUCTION")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Generate TTS audio with English voice")
    print("2. Create visual segments (89 images, 5-second intervals)")
    print("3. Generate Flux Dev images")
    print("4. Compile final video with Ken Burns effects\n")

if __name__ == "__main__":
    main()
