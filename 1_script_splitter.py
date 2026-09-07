#!/usr/bin/env python3
"""
Senaryo Parçalayıcı: Hikayeyi sahnelere bölüyor ve Claude API kullanarak
karakteri tanımlanıyor ve her sahne için ses ve görsel promptları oluşturuyor.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def load_story(story_path: str) -> str:
    with open(story_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_scenes(story: str) -> dict:
    """Claude API'yi kullanarak hikayeyi sahnelere bölüyor"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_key_here":
        print("  ⚠️  DEMO MODE: Gerçek API key yok, demo scenes oluşturuluyor...\n")
        return create_demo_scenes()

    client = Anthropic(api_key=api_key)

    system_prompt = """Sen deneyimli bir Film Senaristisisin. Görevin:
1. Verilen hikayeyi 4-6 saniye uzunluğunda sahne açıklamalarına bölmek
2. Her sahne için voiceover metni hazırlamak
3. Her sahne için görsel prompt yazması (Flux-dev için uygun)
4. Ana karakterin tutarlı tanımını korumak

ANA KARİKTER:
- Adı: Aylin
- Yaş: 25 yaşında, genç ve meraklı
- Görünüş: Uzun kahverengi saçlar, yeşil gözler, hafif bir tebessümü var
- Kıyafet: Maceraperest ruhuna uygun, yolculuk kıyafetleri giyiyor
- Kişilik: Cesur, meraklı, sevgi dolu, kahraman

Çıktı KESINLIKLE bu JSON formatında olmalı:
{
  "character_description": "Aylin'in tutarlı tanımı",
  "scenes": [
    {
      "scene_id": 1,
      "duration_seconds": 5,
      "voiceover_text": "Türkçe voiceover metni (4-6 saniye okuma süresi)",
      "image_prompt": "16:9 görsel prompt (Flux-dev/Flux-schnell için uygun)"
    }
  ]
}

Not: Voiceover metni okuması 4-6 saniye sürecek şekilde olmalı."""

    user_message = f"""Aşağıdaki hikayeyi sahnelere böl:

{story}

Döndür: Geçerli JSON formatında scenes.json çıktısı."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        response_text = response.content[0].text

        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            print("JSON parsing hatası! API yanıtını kontrol ederken...")

        print("API yanıtı:")
        print(response_text)
        raise ValueError("Claude API'den geçerli JSON alınamadı")

    except Exception as e:
        print(f"  ⚠️  Claude API hatası: {e}")
        print("  → Demo moduna geçiliyor...\n")
        return create_demo_scenes()

def create_demo_scenes() -> dict:
    """Demo sahneleri oluşturuyor (API olmadan test için)"""
    return {
        "character_description": "Aylin: 25 yaşında, uzun kahverengi saçlar, yeşil gözler, maceraperest ve cesur bir karakterdir.",
        "scenes": [
            {
                "scene_id": 1,
                "duration_seconds": 5,
                "voiceover_text": "Bir gün, genç ve meraklı maceraperest Aylin, eski bir haritanın izini takip ederek gizli bir ormana gitti.",
                "image_prompt": "Ancient mystical forest with glowing light in the distance, detailed environment"
            },
            {
                "scene_id": 2,
                "duration_seconds": 5,
                "voiceover_text": "Ormanın derinliklerinde, parlayan kristal bir kulenin tepesinden çıkan ışık ona yol gösteriyordu.",
                "image_prompt": "Crystal tower glowing in dark forest at night, magical atmosphere"
            },
            {
                "scene_id": 3,
                "duration_seconds": 5,
                "voiceover_text": "Kulenin kapısına varınca, bir ejderhayı andıran varlık onu selamladı ve yardımcı olmak istedi.",
                "image_prompt": "Dragon-like guardian creature at tower entrance, mystical lighting"
            },
            {
                "scene_id": 4,
                "duration_seconds": 6,
                "voiceover_text": "Aylin dört odadan oluşan bir labirentten geçti, her biri farklı bir engelle karşılaştı.",
                "image_prompt": "Magical labyrinth with four distinct chambers, glowing pathways"
            }
        ]
    }

def save_scenes(scenes_data: dict, output_path: str = "scenes.json"):
    """Sahneleri JSON dosyasına kaydediyor"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scenes_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Sahneler kaydedildi: {output_path}")

def main():
    story_path = "story.txt"

    if not Path(story_path).exists():
        print(f"Hata: {story_path} dosyası bulunamadı!")
        return

    print("📖 Hikaye okunuyor...")
    story = load_story(story_path)
    print(f"Hikaye yüklendi ({len(story)} karakter)")

    print("\n🎬 Claude API ile sahnelere bölünüyor...")
    scenes_data = split_into_scenes(story)

    print(f"✓ {len(scenes_data['scenes'])} sahne oluşturuldu")
    print(f"✓ Ana karakter tanımı: {scenes_data['character_description'][:50]}...")

    print("\n💾 Sahneler kaydediliyor...")
    save_scenes(scenes_data)

    print("\n📋 Sahne Özeti:")
    for scene in scenes_data['scenes']:
        print(f"  Sahne {scene['scene_id']}: {scene['duration_seconds']}s - {scene['voiceover_text'][:40]}...")

if __name__ == "__main__":
    main()
