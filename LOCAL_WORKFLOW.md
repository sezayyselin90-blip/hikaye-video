# Local Workflow Guide: Audio & Image Generation

## Problem
The remote environment's network policy blocks direct access to:
- ElevenLabs API (`api.elevenlabs.io`)
- Flux Dev API (`fal.run`)

## Solution
Generate audio and images locally on your Windows machine, then upload to the project.

---

## Step 1: Generate Audio (Windows Machine)

### Prerequisites
- Python 3.8+
- ElevenLabs API key: `sk_7e1a148f387710f5baf8ee5a1134ebd2bfc3b33c3cb386f6`

### Setup
```bash
pip install requests python-dotenv
```

### Generate Audio Files
```bash
# Copy .env file to your Windows machine
# Run this on Windows:
python 3_tts_generator_english.py
```

**Output:** `audio_english/` directory with 156 MP3 files
- `scene_001.mp3` through `scene_156.mp3`
- Each ~5 seconds, warm agent voice
- Estimated cost: $0.80 USD

---

## Step 2: Generate Images (Windows Machine - Option A: Fal.ai)

### Prerequisites
- Fal.ai API key: `9c1e6971-723a-49ed-999f-171040dfb02a:0f4d6e1230f2a5e4f8b5e692aa0bd187`

### Setup
```bash
pip install fal-client
```

### Generate Images
```bash
# Copy .env file to your Windows machine
# Run this on Windows:
python 6_flux_image_generator.py
```

**Output:** `visual_assets_flux/` directory with 156 JPEG files
- `flux_001.jpg` through `flux_156.jpg`
- Each 16:9 aspect ratio, photorealistic
- Estimated cost: $7.80 USD

---

## Step 2B: Alternative - Generate Images Using Web Interface

1. Visit: https://www.fal.ai/
2. Use API key: `9c1e6971-723a-49ed-999f-171040dfb02a:0f4d6e1230f2a5e4f8b5e692aa0bd187`
3. Copy prompts from `flux_prompts_english.json`
4. Generate and download images manually
5. Save to `visual_assets_flux/` directory with naming: `flux_001.jpg` to `flux_156.jpg`

---

## Step 3: Upload Files to Project

Once both audio and images are generated locally:

### Option A: Git Commit & Push
```bash
# On Windows machine with git configured
git clone https://github.com/sezayyselin90-blip/hikaye-video.git
cd hikaye-video

# Copy local audio and image directories
cp -r audio_english .
cp -r visual_assets_flux .

# Commit and push
git add audio_english/ visual_assets_flux/
git commit -m "Add 156-segment audio and visual assets"
git push origin claude/zealous-pasteur-bix1qe
```

### Option B: Manual Upload
1. Download the generated directories locally
2. Use GitHub web interface to upload files to `claude/zealous-pasteur-bix1qe` branch
3. Create commit via GitHub

---

## Step 4: Video Compilation (Remote Environment)

Once audio and images are uploaded to the repository:

```bash
# Run on remote environment:
python 5_video_compiler.py
```

**Output:** Final video file
- 13 minutes (780 seconds)
- H.264 codec
- AAC audio (5.1 surround)
- Ken Burns zoom effects
- Perfect text-visual synchronization

---

## File Structure After Generation

```
hikaye-video/
├── audio_english/
│   ├── scene_001.mp3
│   ├── scene_002.mp3
│   └── ... (156 files total)
├── visual_assets_flux/
│   ├── flux_001.jpg
│   ├── flux_002.jpg
│   └── ... (156 files total)
├── scripts/
│   └── hikaye_13min_full.txt
├── metadata_visuals_english.json
├── flux_prompts_english.json
└── metadata_audio_english.json
```

---

## Cost Summary

| Component | Count | Unit Cost | Total |
|-----------|-------|-----------|-------|
| ElevenLabs TTS | 156 segments | $0.005 | $0.80 |
| Flux Dev Images | 156 images | $0.05 | $7.80 |
| **Total** | | | **$8.60 USD** |

---

## Troubleshooting

### Audio Generation Fails
- Verify ElevenLabs API key is valid
- Check internet connection
- Ensure Python dependencies installed: `pip install requests python-dotenv`

### Image Generation Fails
- Verify Fal.ai API key is valid
- Check internet connection
- Verify FAL_KEY in .env file
- Check disk space for 156 JPEG files (~500MB-1GB)

### Upload to Repository Fails
- Verify git is configured correctly
- Ensure write access to repository
- Check branch name: `claude/zealous-pasteur-bix1qe`

---

## Timeline Estimate

| Task | Duration | Notes |
|------|----------|-------|
| Audio Generation | 10-15 minutes | 156 segments, 2-second API delays |
| Image Generation | 30-45 minutes | 156 images, 2-second API delays |
| File Upload | 5-10 minutes | Git push or manual upload |
| Video Compilation | 5-10 minutes | FFmpeg on remote environment |
| **Total** | ~50-80 minutes | Parallel: can start compilation while uploading |

---

## Next Steps

1. ✓ Scenario generated (scripts/hikaye_13min_full.txt)
2. ✓ Visual prompts created (flux_prompts_english.json)
3. → **Audio generation (local: Windows)**
4. → **Image generation (local: Windows)**
5. → **Upload to project (Git)**
6. → **Video compilation (remote)**

---

**Status:** Pipeline complete and ready for local generation phase.
