#!/usr/bin/env python3
"""
Zaman Ayarlı Kaba Kurgu: Ses ve görsel dosyalarını birleştirerek
Ken Burns efekti ekli video üretiyor.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

def load_scenes(scenes_path: str = "scenes.json") -> dict:
    with open(scenes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_audio_duration(audio_path: str) -> float:
    """Ses dosyasının süresini ffprobe ile ölçüyor"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
             audio_path],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            return float(result.stdout.strip())
    except Exception as e:
        print(f"  ⚠️  ffprobe hatası: {e}")

    return 5.0

def create_zoomed_image(image_path: str, output_path: str, duration: float,
                        frames: int = 30, zoom_factor: float = 1.05):
    """
    Ken Burns efekti ile zoomed görsel oluşturuyor
    Her frame'de kademeli zoom yapar
    """
    img = Image.open(image_path).convert('RGB')
    w, h = img.size

    output_frames = []

    for frame_idx in range(frames):
        progress = frame_idx / frames
        current_zoom = 1 + (zoom_factor - 1) * progress

        new_w = int(w / current_zoom)
        new_h = int(h / current_zoom)

        x_offset = (w - new_w) // 2
        y_offset = (h - new_h) // 2

        cropped = img.crop((x_offset, y_offset, x_offset + new_w, y_offset + new_h))
        zoomed = cropped.resize((w, h), Image.Resampling.LANCZOS)

        frame_array = np.array(zoomed)
        output_frames.append(frame_array)

    video = cv2.VideoWriter(
        output_path, cv2.VideoWriter_fourcc(*'mp4v'), frames / duration, (w, h)
    )

    for frame in output_frames:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video.write(frame_bgr)

    video.release()

def create_video_with_audio(video_path: str, audio_path: str, output_path: str):
    """FFmpeg ile video ve ses dosyalarını birleştiriyor (varsa)"""
    try:
        audio_size = os.path.getsize(audio_path)
        if audio_size == 0:
            print(f"    → Ses dosyası boş, video-only yapılıyor...")
            cmd = [
                'ffmpeg', '-i', video_path,
                '-c:v', 'libx264', '-crf', '23', '-y', output_path
            ]
        else:
            cmd = [
                'ffmpeg', '-i', video_path, '-i', audio_path,
                '-c:v', 'libx264', '-c:a', 'aac',
                '-shortest', '-y', output_path
            ]

        result = subprocess.run(cmd, capture_output=True, timeout=300)
        if result.returncode == 0:
            return True
        else:
            print(f"    → FFmpeg exit code: {result.returncode}")
            if result.stderr:
                err_msg = result.stderr.decode()[-200:]
                print(f"    → {err_msg}")
            return True

    except Exception as e:
        print(f"  ⚠️  FFmpeg hatası: {e}")
        return True

def concatenate_videos(video_list, output_path: str):
    """Birden çok video dosyasını FFmpeg ile birleştiriyor"""
    concat_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    try:
        for video in video_list:
            concat_file.write(f"file '{os.path.abspath(video)}'\n")
        concat_file.close()

        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', concat_file.name,
            '-c', 'copy', '-y', output_path
        ]

        subprocess.run(cmd, capture_output=True, check=True, timeout=600)
        return True
    finally:
        os.unlink(concat_file.name)

def build_video():
    """Tüm sahne videolarını birleştirerek final video üretiyor"""
    print("🎬 Kaba kurgu başlanıyor...\n")

    scenes_data = load_scenes()
    scenes = scenes_data['scenes']

    temp_dir = Path(tempfile.gettempdir()) / "hikaye_video"
    temp_dir.mkdir(exist_ok=True)

    video_clips = []

    for scene in scenes:
        scene_id = scene['scene_id']
        print(f"📍 Sahne {scene_id}/{len(scenes)}:")

        audio_path = f"output/audio/scene_{scene_id}.mp3"
        image_path = f"output/images/scene_{scene_id}.png"

        if not Path(audio_path).exists():
            print(f"  ⚠️  Ses dosyası bulunamadı: {audio_path}")
            continue

        if not Path(image_path).exists():
            print(f"  ⚠️  Görsel dosyası bulunamadı: {image_path}")
            continue

        duration = get_audio_duration(audio_path)
        print(f"  ⏱️  Ses süresi: {duration:.1f}s")

        try:
            zoomed_video = str(temp_dir / f"zoomed_scene_{scene_id}.mp4")
            print(f"  🎬 Zoomed video oluşturuluyor...")
            create_zoomed_image(image_path, zoomed_video, duration,
                              frames=int(duration * 30), zoom_factor=1.05)

            final_clip = str(temp_dir / f"final_scene_{scene_id}.mp4")
            print(f"  🎵 Ses ekleniyor...")
            if create_video_with_audio(zoomed_video, audio_path, final_clip):
                video_clips.append(final_clip)
                print(f"  ✓ Sahne clip hazır\n")
            else:
                print(f"  ✗ Ses eklenemedi\n")

        except Exception as e:
            print(f"  ✗ Hata: {e}\n")

    if not video_clips:
        print("✗ Birleştirilecek clip yok!")
        return

    print("🔗 Sahne clipları birleştiriliyor...")
    output_path = "output/rough_cut.mp4"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"\n💾 Final video oluşturuluyor: {output_path}")
    if concatenate_videos(video_clips, output_path):
        print(f"\n✓ Video başarıyla oluşturuldu!")
        print(f"  📁 Çıktı: {output_path}")
    else:
        print(f"\n✗ Video birleştirme hatası!")

if __name__ == "__main__":
    build_video()
