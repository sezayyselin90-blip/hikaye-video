# YouTube Hikaye Video Otomasyon Hattı

Türkçe hikaye metinlerini otomatik olarak YouTube reel'ine uygun video hale dönüştüren modüler Python otomasyon sistemi.

## 🏗️ Mimari

```
story.txt (girdi)
    ↓
1_script_splitter.py (Claude API)
    ↓ scenes.json
2_assets_fetcher.py (ElevenLabs + Fal.ai)
    ↓ (audio/ + images/)
3_video_builder.py (FFmpeg + OpenCV)
    ↓
output/rough_cut.mp4 (çıktı)
```

## 📦 Kurulum

### Gereksinimler
- Python 3.9+
- ffmpeg (sistem paketleri)

### Adım 1: Bağımlılıkları Kurma
```bash
pip install -r requirements.txt
```

### Adım 2: Ortam Değişkenlerini Ayarlama
```bash
cp .env.example .env
```

Sonra `.env` dosyasında API anahtarlarını ekleyin:
```
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
FAL_KEY=...
```

### Adım 3: ffmpeg Kurma (Linux)
```bash
apt-get install ffmpeg
```

## 🚀 Kullanım

### 1️⃣ Hikaye Hazırlama
`story.txt` dosyasına Türkçe hikayenizi yazın.

### 2️⃣ Sahnelere Bölme
```bash
python 1_script_splitter.py
```
**Çıktı:** `scenes.json` (4-6 saniyelik sahneler)

### 3️⃣ Ses ve Görsel Üretimi
```bash
python 2_assets_fetcher.py
```
**Çıktı:** 
- `output/audio/scene_*.mp3` (ElevenLabs TTS)
- `output/images/scene_*.png` (Fal.ai Flux-dev)

### 4️⃣ Video Kurgusu
```bash
python 3_video_builder.py
```
**Çıktı:** `output/rough_cut.mp4` (Ken Burns efekti, final video)

## 📋 Dosya Açıklamaları

### 1_script_splitter.py
**Görev:** Hikayeyi doğru uzunluktaki sahnelere bölme

- Claude API ile metin analizi
- Karakteri tutarlı tanımlama
- Türkçe voiceover metinleri
- Flux-dev uyumlu görsel promptları

**Girdi:** `story.txt`
**Çıktı:** `scenes.json`

### 2_assets_fetcher.py
**Görev:** Ses ve görsel dosyaları üretme

- **ElevenLabs TTS:** Doğal Türkçe seslendirme
- **Fal.ai Flux-dev:** 16:9 görsel üretimi
- **Demo Mode:** API key olmadan da çalışır

**Girdi:** `scenes.json`
**Çıktı:** `output/audio/` + `output/images/`

### 3_video_builder.py
**Görev:** Görselleri ses sürelerine kuru, Ken Burns efekti ekleyerek birleştirme

- Ses süresi + görsel süresi senkronizasyonu
- Kademeli zoom animasyonu (Ken Burns)
- FFmpeg ile codec optimizasyonu
- Sahne birleştirme

**Girdi:** `scenes.json` + `output/audio/` + `output/images/`
**Çıktı:** `output/rough_cut.mp4`

## 🎬 Çıktı Özellikleri

| Özellik | Değer |
|---------|-------|
| Çözünürlük | 1920x1080 (Full HD) |
| En Boy Oranı | 16:9 |
| FPS | 30 |
| Ses | AAC |
| Video Codec | H.264 |
| Efekt | Ken Burns (yavaş zoom) |

## ⚙️ Yapılandırma

### Ken Burns Zoom Oranı
`3_video_builder.py`'de değiştirin:
```python
create_zoomed_image(..., zoom_factor=1.05)  # 1.05 = %5 zoom
```

### Ses Hızı
`2_assets_fetcher.py`'de ElevenLabs parametrelerini düzenleyin:
```python
"voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
}
```

### Video Bitrate
`3_video_builder.py`'de FFmpeg parametrelerini değiştirin:
```bash
-c:v libx264 -crf 23  # 23 = yüksek kalite, 51 = düşük kalite
```

## 🧪 Demo Mode

API key'leri olmadan testler yapmak için:
```bash
# Script 1: Demo scenes.json üretir
python 1_script_splitter.py

# Script 2: Mock ses ve görsel dosyaları oluşturur
python 2_assets_fetcher.py

# Script 3: Video-only video üretir (ses olmadan)
python 3_video_builder.py
```

## 🐛 Sorun Giderme

### "ffmpeg: command not found"
```bash
apt-get install ffmpeg  # Linux
brew install ffmpeg     # macOS
```

### "ANTHROPIC_API_KEY invalid"
- `.env` dosyasında geçerli key kontrol edin
- Demo mode çalışacaktır (sabit scena)

### "ElevenLabs API error"
- API key ve kredi limitini kontrol edin
- Demo mode ses dosyaları boş oluşturur

### "Fal.ai API error"
- FAL_KEY kontrol edin
- Demo mode placeholder görseller oluşturur

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

## 🔧 API Anahtarları

### Anthropic (Claude API)
- **Kayıt:** https://console.anthropic.com/
- **Model:** claude-3-5-sonnet-20241022
- **Kullanım:** Hikaye analizi ve skenaryolaştırma

### ElevenLabs (TTS)
- **Kayıt:** https://elevenlabs.io/
- **Model:** eleven_monolingual_v1
- **Dil:** Türkçe destekli
- **Voice ID:** 21m00Tcm4TlvDq8ikWAM (Aylin)

### Fal.ai (Image Generation)
- **Kayıt:** https://fal.ai/
- **Model:** Flux-dev / Flux-schnell
- **Format:** 16:9 (1920x1080)

## 📝 Örnek Hikaye

`story.txt` örneği:
```
Bir gün, genç ve meraklı bir maceraperest olan Aylin, eski bir haritanın 
izini takip ederek gizli bir ormana gitti. Ormanın derinliklerinde, 
parlayan kristal bir kulenin tepesinden çıkan ışık ona yol gösteriyordu...
```

## 🎯 Geliştirme

### Planlanan Özellikler
- [ ] Background müzik ekleme
- [ ] Altyazı (SRT) üretimi
- [ ] Fade-in/fade-out efektleri
- [ ] Multi-character voiceover
- [ ] Thumbnail otomatik üretimi
- [ ] YouTube upload entegrasyonu

### Katkıda Bulunma
PR'lar ve issue'lar hoş geldiniz!

## 📄 Lisans

MIT License

---

**Made with ❤️ by Claude Code**
