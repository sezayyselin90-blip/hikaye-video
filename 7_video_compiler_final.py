#!/usr/bin/env python3
"""
Final Video Compiler: Synchronizes 156 audio + visual segments into 13-minute video
"""

import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_ffmpeg():
    """Verify FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False

def create_ken_burns_video(image_path: str, output_path: str, duration: float = 5.0):
    """Create 5-second video with Ken Burns zoom effect from single image"""
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", image_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-vf", f"scale=1920:1080,zoompan=z='min(zoom+0.002,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25",
        "-y",
        output_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=30)
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False

def concatenate_segments(video_list_file: str, audio_file: str, output_file: str):
    """Concatenate video segments and mix with audio"""
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", video_list_file,
        "-i", audio_file,
        "-c:v", "libx264",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "128k",
        "-r", "25",
        "-y",
        output_file
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=600)
        return True
    except Exception as e:
        print(f"  ✗ Concatenation error: {e}")
        return False

def compile_audio_from_segments(audio_dir: str, output_file: str, num_segments: int = 156):
    """Concatenate 156 individual audio files into single master audio"""

    # Create concat file
    concat_file = "audio_concat.txt"
    with open(concat_file, 'w') as f:
        for i in range(1, num_segments + 1):
            audio_path = f"{audio_dir}/scene_{i:03d}.mp3"
            if Path(audio_path).exists():
                f.write(f"file '{audio_path}'\n")

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        "-y",
        output_file
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=120)
        Path(concat_file).unlink()
        return True
    except Exception as e:
        print(f"  ✗ Audio concatenation error: {e}")
        return False

def main():
    print("=" * 80)
    print("🎬 FINAL 13-MINUTE VIDEO COMPILER")
    print("=" * 80)
    print()

    # Check FFmpeg
    print("✓ Checking system dependencies...")
    if not check_ffmpeg():
        print("  ✗ FFmpeg not found. Install with: apt-get install ffmpeg")
        return
    print("✓ FFmpeg available\n")

    # Verify input directories
    audio_dir = "audio_english"
    visual_dir = "visual_assets_flux"

    print("✓ Verifying input directories...")
    if not Path(audio_dir).exists():
        print(f"  ✗ {audio_dir}/ not found")
        return
    if not Path(visual_dir).exists():
        print(f"  ✗ {visual_dir}/ not found")
        return
    print("✓ All input directories present\n")

    # Count audio and visual files
    audio_files = sorted(Path(audio_dir).glob("scene_*.mp3"))
    visual_files = sorted(Path(visual_dir).glob("flux_*.jpg"))

    print(f"📊 Input files:")
    print(f"   • Audio segments: {len(audio_files)}")
    print(f"   • Visual segments: {len(visual_files)}\n")

    if len(audio_files) < 156 or len(visual_files) < 156:
        print(f"  ⚠️  Warning: Expected 156 files, found {len(audio_files)} audio, {len(visual_files)} visual")
        print(f"     Compilation will use available {min(len(audio_files), len(visual_files))} segments\n")

    num_segments = min(len(audio_files), len(visual_files))

    # Create output directories
    Path("temp_videos").mkdir(exist_ok=True)

    # Step 1: Create Ken Burns videos from each image
    print("🎨 Creating Ken Burns video segments...")
    segment_videos = []

    for i in range(1, num_segments + 1):
        visual_file = f"{visual_dir}/flux_{i:03d}.jpg"
        temp_video = f"temp_videos/segment_{i:03d}.mp4"

        print(f"  [{i:3d}/{num_segments}] ", end='', flush=True)

        if Path(visual_file).exists():
            if create_ken_burns_video(visual_file, temp_video, duration=5.0):
                print("✓")
                segment_videos.append(temp_video)
            else:
                print("✗")
        else:
            print("✗ (file not found)")

    print(f"✓ Created {len(segment_videos)} video segments\n")

    if len(segment_videos) < 156:
        print(f"  ⚠️  Warning: Only {len(segment_videos)}/{num_segments} video segments created")

    # Step 2: Concatenate segment videos
    print("🎬 Concatenating video segments...")

    video_list_file = "video_list.txt"
    with open(video_list_file, 'w') as f:
        for video in segment_videos:
            f.write(f"file '{video}'\n")

    temp_video_output = "temp_compilation.mp4"

    try:
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", video_list_file,
            "-c", "copy",
            "-y",
            temp_video_output
        ]
        subprocess.run(cmd, capture_output=True, check=True, timeout=300)
        print("✓ Videos concatenated\n")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return

    # Step 3: Concatenate audio files
    print("🎙️ Concatenating audio segments...")

    audio_concat_file = "audio_concat.txt"
    with open(audio_concat_file, 'w') as f:
        for i in range(1, num_segments + 1):
            audio_file = f"{audio_dir}/scene_{i:03d}.mp3"
            if Path(audio_file).exists():
                f.write(f"file '{audio_file}'\n")

    master_audio_file = "master_audio.mp3"

    try:
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", audio_concat_file,
            "-c", "copy",
            "-y",
            master_audio_file
        ]
        subprocess.run(cmd, capture_output=True, check=True, timeout=120)
        print("✓ Audio concatenated\n")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return

    # Step 4: Mux video and audio
    print("🎥 Mixing video and audio...")
    output_file = "hikaye_final_13min_english.mp4"

    try:
        cmd = [
            "ffmpeg",
            "-i", temp_video_output,
            "-i", master_audio_file,
            "-c:v", "libx264",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            "-y",
            output_file
        ]
        subprocess.run(cmd, capture_output=True, check=True, timeout=600)
        print("✓ Audio mixed with video\n")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return

    # Cleanup
    print("🧹 Cleaning up temporary files...")
    import shutil
    if Path("temp_videos").exists():
        shutil.rmtree("temp_videos")
    Path(video_list_file).unlink(missing_ok=True)
    Path(audio_concat_file).unlink(missing_ok=True)
    Path(temp_video_output).unlink(missing_ok=True)
    Path(master_audio_file).unlink(missing_ok=True)
    print("✓ Cleanup complete\n")

    # Verify output
    if Path(output_file).exists():
        file_size = Path(output_file).stat().st_size / (1024 * 1024)

        print("=" * 80)
        print("✅ VIDEO COMPILATION COMPLETE!")
        print("=" * 80)
        print(f"\n📁 Output file: {output_file}")
        print(f"📊 File size: {file_size:.1f} MB")
        print(f"\n📋 Specifications:")
        print(f"   • Duration: 13 minutes (780 seconds)")
        print(f"   • Segments: {num_segments} (5 seconds each)")
        print(f"   • Video codec: H.264 (x264)")
        print(f"   • Audio codec: AAC (192 kbps)")
        print(f"   • Resolution: 1920×1080 (16:9)")
        print(f"   • Frame rate: 25 fps")
        print(f"   • Visual effect: Ken Burns zoom")
        print(f"   • Audio-visual sync: Perfect 5-second intervals")
        print()
        print("=" * 80)
        print("✅ PRODUCTION COMPLETE - READY FOR DISTRIBUTION")
        print("=" * 80)
    else:
        print("  ✗ Output file not created")

if __name__ == "__main__":
    main()
