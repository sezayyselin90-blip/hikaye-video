# YouTube Story Video Automation Pipeline

Automatically transform story texts into YouTube-ready videos with English voiceover and AI-generated visuals. A modular Python automation system for content creators.

## 🏗️ Architecture - Premium Mode (Full Motion + Character Consistency)

```
story.txt (input)
    ↓
1_script_splitter.py (Claude API)
    ↓ scenes.json (with character assignments)
2_assets_fetcher.py (ElevenLabs Multi-Voice + Fal.ai Flux Dev)
    ↓ (audio/*.mp3 with character voices + images/*.png)
2c_character_refs.py (Generate character reference portraits)
    ↓ (character_refs/*.png - focused character images for consistency)
2b_animate_videos.py (Kling 2.5 Turbo Pro - Full Motion)
    ↓ (videos/*.mp4 - professional cinematic video)
3_video_builder.py (FFmpeg - Final compositing)
    ↓
output/rough_cut.mp4 (output) - Professional quality!
```

**Premium Features:**
- ✨ **Kling 2.5 Turbo Pro** image-to-video (Hollywood quality motion)
- 🎤 **Multi-character voices** (each character has unique ElevenLabs voice)
- 👥 **Character consistency** (reference portraits maintain appearance)

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

## 🚀 Quick Start (Premium Mode)

```bash
# Step 1: Analyze story
python 1_script_splitter.py

# Step 2: Generate audio (multi-voice) + images (safe)
python 2_assets_fetcher.py

# Step 3: Character reference portraits
python 2c_character_refs.py

# Step 4: Animate all scenes (Kling 2.5)
python 2b_animate_videos.py

# Step 5: Build final video
python 3_video_builder.py

# Result: output/rough_cut.mp4 ✨
```

**Estimated Cost:** ~$2-3 per 20-second video (high quality, professional result)

---

## 📋 Detailed Usage

### 1️⃣ Prepare Story
Write your story in `story.txt` (English text)

### 2️⃣ Split into Scenes
```bash
python 1_script_splitter.py
```
**Output:** `scenes.json` (with character assignments and voice mappings)

### 3️⃣ Generate Audio & Images (Multi-Voice + Safety)
```bash
python 2_assets_fetcher.py
```
**Output:** 
- `output/audio/scene_*.mp3` (Multi-character English voiceovers)
  - Each character gets unique ElevenLabs voice (Narrator: James, Marcus: Bella, Ray: Grace)
- `output/images/scene_*.png` (Fal.ai Flux-dev with safety prompts)
  - Explicitly avoids real/famous people resemblance
  - Clearly fictional characters, illustration/animation style

### 3b️⃣ Generate Character References (Premium)
```bash
python 2c_character_refs.py
```
**Output:** 
- `output/character_refs/{character}.png` (Focused character portraits)
- Cost: ~$0.07/second per character (typically 3-5 characters = ~$1-2)
- Used for character consistency across scenes
- Ensures each character looks the same in every scene

### 3c️⃣ Animate All Scenes to Video (Kling 2.5 Turbo Pro)
```bash
python 2b_animate_videos.py
```
**Output:** 
- `output/videos/scene_*.mp4` (Professional motion videos)
- Model: Kling 2.5 Turbo Pro (Hollywood quality)
- Cost: ~$0.07/second (~$1.50 per 21-second video)
- Creates cinematic motion, character-aware animation
- Much higher quality than Ken Burns or Wan 2.5

### 4️⃣ Build Final Video
```bash
python 3_video_builder.py
```
**Output:** 
- `output/rough_cut.mp4` (Final professional video)
- Combines all animated scenes with multi-character audio
- Perfect for YouTube shorts/TikTok/professional use

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

### 2c_character_refs.py (Premium)
**Purpose:** Generate focused character reference images for consistency

- Generates portrait-style images of each unique character
- Creates `output/character_refs/{character}.png` for each actor
- Used by 2b_animate_videos.py to maintain character appearance
- One-time generation: ~$1-2 total for all characters
- Ensures characters look identical across all scenes

**Input:** `scenes.json` (character descriptions)
**Output:** `output/character_refs/*.png`

Essential for premium character consistency. Run AFTER 2_assets_fetcher.py.

### 2b_animate_videos.py (Premium)
**Purpose:** Convert all images to professional motion videos

- **Model:** Kling 2.5 Turbo Pro (Hollywood-quality image-to-video)
- Generates smooth cinematic motion from still images
- Matches video duration exactly to audio length (5-6 seconds per scene)
- Cost: ~$0.07/second (~$1.50 per 21-second full video)
- Uses character references for appearance consistency

**Input:** `output/images/` + `output/character_refs/` + `output/audio/` (for duration)
**Output:** `output/videos/scene_*.mp4`

This is the key premium feature - creates professional-quality motion videos instead of static images.

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
