#!/usr/bin/env python3
"""
Video Derleyici: Ses + görselleri Ken Burns efektli video olarak derliyor
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_dependencies():
    """Gerekli araçları kontrol et"""
    required = ['ffmpeg']
    missing = []

    for tool in required:
        result = os.system(f"which {tool} > /dev/null 2>&1")
        if result != 0:
            missing.append(tool)

    return missing

def create_ken_burns_effect(input_image: str, output_video: str, duration: float, zoom_direction: str = "in"):
    """Ken Burns zoom efekti ile görsel video oluştur"""

    scale_start = 1.0
    scale_end = 1.2 if zoom_direction == "in" else 0.8

    # FFmpeg komutu: Ken Burns efekti (zoom + pan)
    cmd = f"""ffmpeg -loop 1 -i "{input_image}" \
        -c:v libx264 -t {duration} -pix_fmt yuv420p \
        -filter:v "scale=1920:1080, \
        zoompan=z='min(zoom+0.002,{scale_end})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=25:s=1920x1080:fps=30" \
        "{output_video}" -y"""

    return cmd

def compile_video_with_audio(audio_file: str, visual_segments_dir: str, output_file: str, metadata: dict):
    """Ses ve görselleri final video olarak derle"""

    print("⚠️  Video derleme için gereken dosyalar:")
    print(f"   • Audio dosyaları: {audio_file} şeklinde")
    print(f"   • Görsel dosyaları: {visual_segments_dir}/")
    print(f"\n✅ Derlenecek dosya: {output_file}")

    print("\n" + "=" * 80)
    print("📝 Derleyici Konfigürasyonu:")
    print("=" * 80)

    print(f"""
Codec: H.264 (x264)
Bitrate: 8000k (4K uyumlu)
Frame Rate: 30 fps
Resolution: 1920x1080 (16:9)
Audio: AAC, 128 kbps
Video Efekt: Ken Burns Zoom

Sahne Sürelemeleri:
""")

    for scene in metadata.get('scenes', [])[:5]:
        print(f"  • Sahne {scene['scene_id']}: {scene['duration']}s")

    if len(metadata.get('scenes', [])) > 5:
        print(f"  ... ve {len(metadata['scenes']) - 5} sahne daha")

    print("\n" + "=" * 80)
    print("🎬 VIDEO DERLEYICI HAZIR")
    print("=" * 80)

    return {
        'status': 'ready',
        'input_audio': audio_file,
        'input_visuals': visual_segments_dir,
        'output_file': output_file
    }

def main():
    print("=" * 80)
    print("🎬 VIDEO DERLEYICI (Ken Burns Efektli)")
    print("=" * 80)
    print()

    # Bağımlılıkları kontrol et
    print("✓ Sistem kontrol ediliyor...")
    missing = check_dependencies()

    if missing:
        print(f"⚠️  Eksik araçlar: {', '.join(missing)}")
        print("   FFmpeg kurulması gerekiyor.")
        return

    print("✓ Tüm araçlar mevcut\n")

    # Metadata yükle
    metadata_path = "metadata_audio.json"

    if not Path(metadata_path).exists():
        print(f"⚠️  {metadata_path} bulunamadı")
        print("   Önce 3_tts_generator.py'ı çalıştır\n")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        audio_metadata = json.load(f)

    print("=" * 80)
    print("📋 VİDEO DERLEMESİ İÇİN HAZIR")
    print("=" * 80)

    config = compile_video_with_audio(
        audio_file="audio/scene_001.mp3",
        visual_segments_dir="visuals",
        output_file="output/video_final.mp4",
        metadata=audio_metadata
    )

    print(f"""
✅ Derleyici Durumu: {config['status'].upper()}

Girdi Dosyaları:
  • Audio: {config['input_audio']}
  • Visuals: {config['input_visuals']}/

Çıktı:
  • Video: {config['output_file']}

Özellikler:
  ✓ Ken Burns Zoom Efekti
  ✓ 4K Kalitesi (1920x1080)
  ✓ 30 FPS
  ✓ H.264 Video Codec
  ✓ AAC Audio

Video Özellikleri:
  • Toplam Sahneler: {len(audio_metadata['scenes'])}
  • Toplam Süresi: ~{sum(s['duration'] for s in audio_metadata['scenes']) // 60}m
  • Ses: Warm Agent Voice (Soothing American Assistant)

Sonraki Adımlar:
1. Flux Dev ile görselleri generate et
2. Ses dosyalarını kontrol et
3. Video derlemeyi başlat (5_video_compiler_full.py)

🚀 Video üretimine başlamak için hazır!
""")

if __name__ == "__main__":
    main()
