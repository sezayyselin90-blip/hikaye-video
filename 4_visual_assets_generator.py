#!/usr/bin/env python3
"""
Görsel Asset Üretici: 59 sahneyi 5-saniyelik segmentlere bölüp
Flux Dev ile görselleri generate ediyor
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()

def parse_scenario_file(txt_path: str) -> list:
    """Türkçe metin dosyasından sahneleri parse et"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    scenes = []
    scene_pattern = r'\[SAHNE (\d+)\] \((\d+)s\)\nKonuşan: (.+?)\nMetni: (.+?)\nGörsel: (.+?)(?:\n---|\n\[SAHNE|\Z)'

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
    """Sahneleri 5-saniyelik segmentlere böl"""
    segments = []
    segment_id = 1
    current_time = 0

    for scene in scenes:
        duration = scene['duration']
        scene_id = scene['scene_id']
        visual_prompt = scene['visual_prompt']
        text = scene['text']

        # Sahneleri 5-saniyelik parçalara böl
        num_segments = (duration + 4) // 5  # Round up
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
    """Flux Dev için optimize edilmiş prompt oluştur"""
    prompt = f"""{visual_prompt}

    [Quality: 8K, cinematic, professional, high detail]
    [Style: photorealistic, dramatic lighting, 16:9 aspect ratio]
    [Technical: ultra sharp focus, color graded]"""

    return prompt

def prepare_flux_batch(segments: list, batch_size: int = 10) -> list:
    """Flux API'ye gönderilecek batch'ler hazırla"""
    batches = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        batch_prompts = []

        for seg in batch:
            prompt = generate_flux_prompt(seg['visual_prompt'])
            batch_prompts.append({
                'segment_id': seg['segment_id'],
                'prompt': prompt,
                'negative_prompt': 'blurry, low quality, distorted, watermark'
            })

        batches.append(batch_prompts)

    return batches

def main():
    scenario_path = "scripts/hikaye_genisletilmis.txt"

    if not Path(scenario_path).exists():
        print(f"Hata: {scenario_path} bulunamadı!")
        return

    print("📖 Senaryo parse ediliyor...")
    scenes = parse_scenario_file(scenario_path)
    print(f"✓ {len(scenes)} sahne bulundu\n")

    print("📏 Sahneler 5-saniyelik segmentlere bölünüyor...")
    segments = create_visual_segments(scenes)
    print(f"✓ {len(segments)} görsel segment oluşturuldu\n")

    total_duration = sum(seg['duration'] for seg in segments)
    minutes = int(total_duration) // 60
    seconds = int(total_duration) % 60

    print(f"⏱️  Toplam video süresi: {minutes}m {seconds}s\n")

    print("🎨 Flux Dev prompts hazırlanıyor...")
    batches = prepare_flux_batch(segments)
    print(f"✓ {len(batches)} batch hazırlandı\n")

    # Metadata kaydet
    metadata = {
        'total_scenes': len(scenes),
        'total_segments': len(segments),
        'total_duration': total_duration,
        'segments': segments,
        'batches': len(batches),
        'batch_size': 10
    }

    with open("metadata_visuals.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # Flux prompts kaydet
    flux_prompts = []
    for seg in segments:
        flux_prompts.append({
            'segment_id': seg['segment_id'],
            'prompt': generate_flux_prompt(seg['visual_prompt']),
            'negative_prompt': 'blurry, low quality, distorted, watermark',
            'scene_id': seg['scene_id'],
            'duration': seg['duration']
        })

    with open("flux_prompts.json", 'w', encoding='utf-8') as f:
        json.dump(flux_prompts, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("✅ GÖRSEL ASSET HAZIRLIĞI TAMAMLANDI!")
    print("=" * 80)
    print(f"\n📊 İstatistikler:")
    print(f"   • Orijinal sahneler: {len(scenes)}")
    print(f"   • Görsel segmentler: {len(segments)}")
    print(f"   • Toplam süresi: {minutes}m {seconds}s")
    print(f"   • Batch sayısı: {len(batches)}")
    print(f"\n📝 Metadata dosyaları:")
    print(f"   • metadata_visuals.json")
    print(f"   • flux_prompts.json")

    print("\n" + "=" * 80)
    print("⚠️  SONRAKI ADIM: Flux Dev ile görselleri generate et")
    print("=" * 80)
    print(f"\nFlux API'ye {len(segments)} görsel için istek gönderilecek.")
    print(f"Tahmini maliyet: ${len(segments) * 0.05:.2f} USD\n")

if __name__ == "__main__":
    main()
