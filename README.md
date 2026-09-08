# YouTube Story Video Automation Pipeline

Automatically transform story texts into YouTube-ready videos with English voiceover and AI-generated visuals. A modular Python automation system for content creators.

## 🏗️ Architecture

```
story.txt (input)
    ↓
1_script_splitter.py (Claude API)
    ↓ scenes.json
2_assets_fetcher.py (ElevenLabs + Fal.ai Flux Dev)
    ↓ (audio/ + images/)
2b_animate_videos.py (Fal.ai Wan 2.5 - OPTIONAL - Motion video)
    ↓ (videos/)
3_video_builder.py (FFmpeg + OpenCV)
    ↓ (prefers animated videos, falls back to Ken Burns)
output/rough_cut.mp4 (output)
```

**New: Motion Video Mode** - Animate still images into smooth video clips using Fal.ai Wan 2.5 image-to-video model (~$0.05/second). Optional but recommended for professional output.

## 📦 Installation

### Requirements
- Python 3.9+
- ffmpeg (system package)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

Then add your API keys to `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=sk_...
FAL_KEY=...
ELEVENLABS_VOICE_ID=TxGEqnHWrfWFTfGW9XjX  (or your preferred voice)
ELEVENLABS_LANGUAGE=en
```

### Step 3: Install ffmpeg
**Linux:**
```bash
apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## 🚀 Usage

### 1️⃣ Prepare Story
Write your story in `story.txt` (English text)

### 2️⃣ Split into Scenes
```bash
python 1_script_splitter.py
```
**Output:** `scenes.json` (4-6 second scenes)

### 3️⃣ Generate Audio & Images
```bash
python 2_assets_fetcher.py
```
**Output:** 
- `output/audio/scene_*.mp3` (English voiceover via ElevenLabs)
- `output/images/scene_*.png` (AI images via Fal.ai Flux-dev)

### 3️⃣b Animate Images to Video (OPTIONAL - Motion Mode)
```bash
python 2b_animate_videos.py
```
**Output:** 
- `output/videos/scene_*.mp4` (Animated clips via Fal.ai Wan 2.5)
- Cost: ~$0.05/second per video (~$10-20 per full video)
- Creates smooth motion from still images, much better than Ken Burns effect

**Skip this step** if you want to use Ken Burns zoom on static images instead (free, but less cinematic).

### 4️⃣ Build Video
```bash
python 3_video_builder.py
```
**Output:** 
- `output/rough_cut.mp4` 
- Uses animated videos if available (from step 3b)
- Falls back to Ken Burns zoom on static images if no animated videos

## 📋 Module Descriptions

### 1_script_splitter.py
**Purpose:** Break story into properly-timed scenes

- Claude API for text analysis
- Consistent character descriptions
- English voiceover text generation
- Flux-dev compatible image prompts

**Input:** `story.txt`
**Output:** `scenes.json`

### 2_assets_fetcher.py
**Purpose:** Generate audio and visual assets

- **ElevenLabs TTS:** Natural English voiceover with **multi-character voices**
  - Automatic character detection and voice assignment
  - Default narrator: James (TxGEqnHWrfWFTfGW9XjX)
  - Alternative character voices: Bella, Grace, Rachel, and many others
  - Each character maintains consistent voice throughout
  - Language: English (configurable)
- **Fal.ai Flux-dev:** 16:9 image generation
  - **Safety:** Explicit instructions to avoid real/famous people
  - Generates clearly fictional, generic-looking characters
  - Art style: illustration/animation/stylized art
- **Demo Mode:** Works without API keys

**Input:** `scenes.json` (with character voice mappings)
**Output:** `output/audio/` + `output/images/` (character-specific voicesovers)

### 2b_animate_videos.py (NEW - Optional)
**Purpose:** Convert still images to animated video clips

- **Fal.ai Wan 2.5 Image-to-Video:** Generates smooth motion from still images
- Creates cinematic video clips matching audio duration
- Replaces Ken Burns zoom with real motion
- Cost: ~$0.05/second (~$10-20 per full video)
- Motion control: CFG scale 7.5, motion bucket 127, 24 FPS

**Input:** `output/images/` + `output/audio/` (for duration)
**Output:** `output/videos/scene_*.mp4`

Run this AFTER 2_assets_fetcher.py if you want motion videos.
Skip this if you prefer the free Ken Burns effect.

### 3_video_builder.py
**Purpose:** Combine images/videos and audio into final output

- Prefers animated videos (from 2b_animate_videos.py)
- Falls back to Ken Burns zoom if no animated videos
- Syncs visual duration to audio length exactly
- FFmpeg codec optimization
- Scene concatenation

**Input:** `scenes.json` + `output/audio/` + `output/images/` + `output/videos/`
**Output:** `output/rough_cut.mp4`

## 🎙️ Multi-Character Voice System

The pipeline automatically generates **distinct voices for different characters** in your story:

### How It Works

1. **Character Detection** - Claude API identifies all characters with dialogue
2. **Voice Assignment** - Each character gets a unique ElevenLabs voice
3. **Consistency** - Same character = same voice throughout the video
4. **Speaker Attribution** - Each scene indicates who is speaking

### Available Voices

| Voice | Type | Best For |
|-------|------|----------|
| **James** | Deep male | Narrator, authority figures |
| **Bella** | Warm female | Main character, emotional scenes |
| **Grace** | Assertive female | Strong characters, professionals |
| **Rachel** | Young female | Young characters, action scenes |

### Example: Multi-Character Story

When you run the pipeline on a story with dialogue:

```bash
python 1_script_splitter.py  # Detects: Marcus (lawyer), Ray (shopkeeper), Narrator
python 2_assets_fetcher.py   # Assigns: Bella voice, Grace voice, James voice
```

Output shows:
```
🎙️ Multi-Character Voices:
  • Narrator: James
  • Marcus: Bella
  • Ray: Grace
```

Then generates audio with the correct voice for each character's lines.

### Manual Voice Configuration

You can customize character voices by editing `scenes.json`:

```json
{
  "characters": {
    "Marcus": {
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "voice_name": "Bella"
    }
  }
}
```

See [VOICE_CONFIG.md](VOICE_CONFIG.md) for complete voice options and customization guide.

## 🎬 Çıktı Özellikleri

| Özellik | Değer |
|---------|-------|
| Çözünürlük | 1920x1080 (Full HD) |
| En Boy Oranı | 16:9 |
| FPS | 30 |
| Ses | AAC |
| Video Codec | H.264 |
| Efekt | Ken Burns (yavaş zoom) |

## ⚙️ Configuration

### Voice Selection
Change `ELEVENLABS_VOICE_ID` in `.env`:
```
ELEVENLABS_VOICE_ID=TxGEqnHWrfWFTfGW9XjX  # James
ELEVENLABS_LANGUAGE=en                    # English
```

### Voice Settings
Adjust in `2_assets_fetcher.py`:
```python
"voice_settings": {
    "stability": 0.5,        # 0-1: lower = more variation
    "similarity_boost": 0.75 # 0-1: higher = closer to original
}
```

### Ken Burns Zoom Factor
Adjust in `3_video_builder.py`:
```python
create_zoomed_image(..., zoom_factor=1.05)  # 1.05 = 5% zoom
```

### Video Quality
Modify FFmpeg settings in `3_video_builder.py`:
```bash
-c:v libx264 -crf 23  # 23=high quality, 51=low quality
```

## 🧪 Demo Mode

Test without API keys:
```bash
# Script 1: Generate demo scenes.json
python 1_script_splitter.py

# Script 2: Create placeholder audio & image files
python 2_assets_fetcher.py

# Script 3: Build video-only (no audio) output
python 3_video_builder.py
```

All three scripts work in demo mode, creating a complete end-to-end test of the pipeline.

## 🐛 Troubleshooting

### "ffmpeg: command not found"
```bash
apt-get install ffmpeg  # Linux
brew install ffmpeg     # macOS
choco install ffmpeg    # Windows (with Chocolatey)
```

### "ANTHROPIC_API_KEY invalid"
- Verify valid key in `.env`
- Demo mode will still work with preset scenes

### "ElevenLabs API error"
- Check API key and account credits
- Demo mode creates empty audio files (playback requires real audio)
- Verify language is set to `en` in `.env`

### "Fal.ai API error"
- Verify FAL_KEY in `.env`
- Demo mode generates placeholder images
- Check Fal.ai account quota

## 📊 Örnek Çıktı

```
🎬 Kaba kurgu başlanıyor...

📍 Sahne 1/4:
  ⏱️  Ses süresi: 5.0s
  🎬 Zoomed video oluşturuluyor...
  🎵 Ses ekleniyor...
  ✓ Sahne clip hazır

...

✓ Video başarıyla oluşturuldu!
  📊 Toplam uzunluk: 20.0s
  📁 Çıktı: output/rough_cut.mp4
```

## 🔧 API Keys

### Anthropic (Claude API)
- **Sign up:** https://console.anthropic.com/
- **Model:** claude-3-5-sonnet-20241022
- **Usage:** Story analysis and scene generation

### ElevenLabs (Text-to-Speech)
- **Sign up:** https://elevenlabs.io/
- **Model:** eleven_multilingual_v2
- **Language:** English
- **Available Voices:**
  - `TxGEqnHWrfWFTfGW9XjX` - James (default)
  - `EXAVITQu4vr4xnSDxMaL` - Bella
  - `21m00Tcm4TlvDq8ikWAM` - Grace
  - See https://elevenlabs.io/voice-lab for all voices

### Fal.ai (Image Generation)
- **Sign up:** https://fal.ai/
- **Model:** Flux-dev (high quality) or Flux-schnell (fast)
- **Format:** 16:9 (1920x1080)

## 📝 Example Story

The `story.txt` file should contain narrative text in English. Example:
```
Under a concrete train bridge on Chicago's South Side, a sharp-dressed 
lawyer named Marcus pulled up in a black Cadillac every morning. Nobody 
understood why he took the pocket change from a homeless veteran called 
Silent Joe. Until the shocking truth emerged...
```

## 🎯 Development

### Planned Features
- [ ] Background music integration
- [ ] Subtitle (SRT) generation
- [ ] Fade-in/fade-out effects
- [ ] Multi-character English voiceover
- [ ] Automatic thumbnail generation
- [ ] Direct YouTube upload integration
- [ ] Chapter markers for long-form content
- [ ] Emotion-based voice pitch adjustment

### Contributing
Pull requests and issues welcome!

## 📄 Lisans

MIT License

---

**Made with ❤️ by Claude Code**
