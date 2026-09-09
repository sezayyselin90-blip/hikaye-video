#!/usr/bin/env python3
"""
Flux Dev Image Generator: Creates 156 photorealistic images for video
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def generate_flux_image(prompt: str, image_id: int, output_dir: str) -> bool:
    """Generate single image using Flux Dev via Fal.ai"""
    try:
        import fal_client
    except ImportError:
        print("  ⚠️  fal-client not installed. Install with: pip install fal-client")
        return False

    api_key = os.getenv("FAL_KEY")
    if not api_key:
        print("  ⚠️  FAL_KEY not found in .env")
        return False

    fal_client.api_key = api_key

    try:
        result = fal_client.run(
            "fal-ai/flux-pro",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
                "output_format": "jpeg"
            }
        )

        if result and "images" in result:
            image_url = result["images"][0]["url"]

            # Download image
            import urllib.request
            output_path = f"{output_dir}/flux_{image_id:03d}.jpg"
            urllib.request.urlretrieve(image_url, output_path)

            return True

    except Exception as e:
        print(f"  ✗ Flux error: {e}")
        return False

    return False

def main():
    prompts_path = "flux_prompts_english.json"
    output_dir = "visual_assets_flux"

    if not Path(prompts_path).exists():
        print(f"Error: {prompts_path} not found!")
        return

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Load prompts
    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    total = len(prompts)
    print(f"🎨 Generating {total} Flux Dev images...")
    print(f"   Output directory: {output_dir}/\n")

    success_count = 0
    for i, prompt_data in enumerate(prompts, 1):
        segment_id = prompt_data['segment_id']
        prompt = prompt_data['prompt']

        print(f"[{i:3d}/{total}] Segment {segment_id:3d}: ", end='', flush=True)

        if generate_flux_image(prompt, segment_id, output_dir):
            print("✓")
            success_count += 1
        else:
            print("✗")

        # Rate limiting
        if i < total:
            time.sleep(2)

    print(f"\n✓ Generated {success_count}/{total} images")

    print("\n" + "=" * 80)
    print("✅ FLUX IMAGE GENERATION COMPLETE!")
    print("=" * 80)
    print(f"\n📁 Visual assets: {output_dir}/")
    print(f"📊 Successfully generated: {success_count}/{total}")
    print(f"💰 Cost: ${total * 0.05:.2f} USD")

if __name__ == "__main__":
    main()
