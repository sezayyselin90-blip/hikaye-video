#!/usr/bin/env python3
"""
Full 13-Minute Scenario Generator: Creates 156 segments × 5 seconds each
Complete narrative preservation with deep, cinematic details
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def load_story(story_path: str) -> str:
    with open(story_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_full_scenario(story: str) -> str:
    """Generate complete 13-minute (156 segment) scenario"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_key_here":
        print("  ⚠️  DEMO MODE: API key not found\n")
        return None

    client = Anthropic(api_key=api_key)

    system_prompt = """You are a master screenwriter and narrator. Create a COMPLETE 156-segment screenplay.

CRITICAL REQUIREMENTS:
1. Exactly 156 scenes (13 minutes × 60 / 5 seconds per scene)
2. Each scene = EXACTLY 5 seconds of narration when read aloud
3. FULL narrative preservation - include ALL story details, emotions, context
4. Each segment needs 25-30 words (optimal 5-second reading at 150 wpm)
5. Deep, cinematic narration style - not screenplay, pure narrative
6. Detailed visual prompts for Flux Dev (16:9 format)
7. Smooth transitions between segments

EXPANSION AREAS:
- Character emotions and internal states
- Environmental details and atmosphere
- Dialogue expansion with more exchanges
- Reaction shots and emotional beats
- Contextual explanations
- Dramatic pauses and tension building
- Sensory details (sounds, textures, temperatures)

OUTPUT FORMAT FOR EACH SCENE:
[SCENE N] (5s)
Speaker: Narrator
Text: [Exactly 25-30 words of narration - 5-second reading time]
Visual: [Detailed 16:9 Flux Dev prompt]

TOTAL: Must be exactly 156 scenes"""

    user_message = f"""Create EXACTLY 156 scenes for a complete 13-minute video.

STORY:
{story}

REQUIREMENTS:
1. Expand to 156 segments (not compress)
2. Each segment = 5 seconds = 25-30 words
3. Preserve EVERY detail from the story
4. Add emotional depth and sensory details
5. Include character reactions and thoughts
6. Build dramatic tension throughout
7. Detailed visual descriptions for each segment

Output ONLY the 156 scenes in the specified format.
No introduction, no summary, just all 156 scenes.
Start with [SCENE 1] and end with [SCENE 156].
Total must equal exactly 13 minutes (156 × 5 seconds)."""

    try:
        print("🔄 Claude API generating 156-segment 13-minute scenario...")
        print("   (This will take 1-2 minutes)...\n")

        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=16000,
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

def save_scenario_as_text(scenario_text: str, output_path: str = "scripts/hikaye_13min_full.txt"):
    """Save complete 13-minute scenario"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("STORY: COMPLETE 13-MINUTE ENGLISH SCENARIO\n")
        f.write("=" * 80 + "\n\n")
        f.write("NARRATOR: Warm Agent Voice (Soothing American Assistant)\n")
        f.write("LANGUAGE: English\n")
        f.write("FORMAT: 156 Scenes × 5 seconds = 13 minutes (780 seconds total)\n")
        f.write("VISUAL SYNC: Perfect 5-second interval synchronization\n\n")
        f.write("=" * 80 + "\n\n")
        f.write(scenario_text)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("PRODUCTION NOTES:\n")
        f.write("=" * 80 + "\n")
        f.write("• 156 segments = exactly 13 minutes\n")
        f.write("• Each segment: 5 seconds narration + 5 seconds visual\n")
        f.write("• Visual changes every 5 seconds (perfect sync)\n")
        f.write("• 25-30 words per segment (optimal for 5-second reading)\n")
        f.write("• Full story preservation with emotional depth\n")
        f.write("• Ken Burns zoom effects across all segments\n")

    return output_path

def main():
    story_path = "story.txt"

    if not Path(story_path).exists():
        print(f"Error: {story_path} not found!")
        return

    print("📖 Loading original English story...")
    story = load_story(story_path)
    print(f"✓ Story loaded ({len(story)} characters)\n")

    scenario_text = generate_full_scenario(story)

    if not scenario_text:
        print("Scenario generation failed!")
        return

    print(f"✓ Scenario generated ({len(scenario_text)} characters)\n")

    print("💾 Saving 13-minute scenario...")
    txt_path = save_scenario_as_text(scenario_text)
    print(f"✓ Saved: {txt_path}\n")

    print("=" * 80)
    print("✅ 13-MINUTE COMPLETE SCENARIO READY!")
    print("=" * 80)
    print(f"\n📄 Scenario file: {txt_path}")
    print("\n📋 Production specifications:")
    print(f"   • Total duration: 13 minutes (780 seconds)")
    print(f"   • Total segments: 156 (5 seconds each)")
    print(f"   • Words per segment: 25-30 (5-second narration)")
    print(f"   • Visual sync: Perfect 5-second intervals")
    print(f"   • Narrator: Warm Agent Voice (AIJ0ViCZ83NSXLNIERjD)")
    print(f"   • Language: English")
    print(f"   • Style: Deep, cinematic, emotional\n")

    print("=" * 80)
    print("✅ READY FOR FULL PRODUCTION")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Process 156 visual segments for 5-second sync")
    print("2. Generate Flux Dev prompts (156 images)")
    print("3. Create ElevenLabs TTS for 156 segments")
    print("4. Compile final 13-minute video with Ken Burns\n")

if __name__ == "__main__":
    main()
