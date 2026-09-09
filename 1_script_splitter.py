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
    """Split story into scenes with character voice assignments"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_key_here":
        print("  ⚠️  DEMO MODE: No real API key, generating demo scenes...\n")
        return create_demo_scenes()

    client = Anthropic(api_key=api_key)

    system_prompt = """You are an experienced screenplay writer. Your tasks:
1. Break the story into 4-6 second scene descriptions
2. Generate voiceover text for each scene
3. Create visual prompts for each scene (Flux-dev compatible)
4. Identify all characters with dialogue
5. Maintain consistent character descriptions

CHARACTER VOICE ASSIGNMENT:
- Detect each unique character who speaks
- Assign a distinct voice from available options
- Characters without dialogue = narrator (James)

Available ElevenLabs English Voices:
- James (TxGEqnHWrfWFTfGW9XjX): Deep, professional, storyteller
- Bella (EXAVITQu4vr4xnSDxMaL): Warm female voice, conversational
- Grace (21m00Tcm4TlvDq8ikWAM): Clear female voice, authoritative
- Rachel (21m00Tcm4TlvDq8ikWAM): Young female voice, energetic

OUTPUT MUST BE EXACTLY THIS JSON FORMAT:
{
  "character_description": "Main character and all key characters",
  "characters": {
    "Character Name": {
      "voice_id": "TxGEqnHWrfWFTfGW9XjX",
      "voice_name": "James",
      "description": "Physical description and role"
    }
  },
  "scenes": [
    {
      "scene_id": 1,
      "duration_seconds": 5,
      "voiceover_text": "English voiceover text (4-6 second reading time)",
      "speaker": "Character Name or Narrator",
      "image_prompt": "16:9 visual prompt for Flux-dev"
    }
  ]
}

Notes:
- Voiceover text should take 4-6 seconds to read aloud
- "speaker" indicates who is speaking in that scene
- Same character = same voice throughout (consistency)
- Narrator = James voice for non-dialogue text"""

    user_message = f"""Break this story into scenes with character voices:

{story}

Instructions:
1. Identify all characters who speak
2. Assign each a unique English voice (consistency across scenes)
3. Include speaker name in each scene
4. Narrator (non-dialogue) = James voice
5. Return valid JSON with character voice mapping"""

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
    """Generate demo scenes for testing (without API)"""
    return {
        "character_description": "Marcus: Sharp-dressed lawyer. Joseph 'Silent Joe': Elderly homeless veteran. Ray: Angry shopkeeper.",
        "characters": {
            "Narrator": {
                "voice_id": "TxGEqnHWrfWFTfGW9XjX",
                "voice_name": "James",
                "description": "Professional narrator voice"
            },
            "Marcus": {
                "voice_id": "EXAVITQu4vr4xnSDxMaL",
                "voice_name": "Bella",
                "description": "Lawyer with calm, determined tone"
            },
            "Ray": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "voice_name": "Grace",
                "description": "Angry shopkeeper, aggressive tone"
            }
        },
        "scenes": [
            {
                "scene_id": 1,
                "duration_seconds": 5,
                "voiceover_text": "Under a concrete Chicago train bridge, Ray grabbed Marcus violently by his Italian suit collar. Buttons scattered across muddy asphalt.",
                "speaker": "Narrator",
                "image_prompt": "Tense confrontation under concrete train bridge, angry shopkeeper grabbing lawyer, crowd forming"
            },
            {
                "scene_id": 2,
                "duration_seconds": 5,
                "voiceover_text": "Ray shouted: You think you can rob this helpless mute man every morning? Wearing a thousand-dollar suit while you steal from the homeless!",
                "speaker": "Ray",
                "image_prompt": "Angry crowd gathering, phone cameras, rage and tension, urban scene"
            },
            {
                "scene_id": 3,
                "duration_seconds": 5,
                "voiceover_text": "Marcus remained eerily calm. He said: Before you judge me, open my car trunk. Inside is a black briefcase with code one-nine-nine-four.",
                "speaker": "Marcus",
                "image_prompt": "Police arriving, black Cadillac, briefcase revelation moment"
            },
            {
                "scene_id": 4,
                "duration_seconds": 6,
                "voiceover_text": "Inside were thousands of court documents. Officer Miller's expression changed. Marcus revealed the shocking truth.",
                "speaker": "Narrator",
                "image_prompt": "Official court documents, legal victory, justice imagery"
            }
        ]
    }

def save_scenes(scenes_data: dict, output_path: str = "scenes.json"):
    """Sahneleri JSON dosyasına kaydediyor"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scenes_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Sahneler kaydedildi: {output_path}")

def save_script_as_txt(scenes_data: dict, output_path: str = "scripts/hikaye_01.txt"):
    """Senaryoyu düz metin formatında kaydediyor (manuel düzenleme için)"""
    from pathlib import Path

    # Klasörü oluştur
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("HIKAYE: TAM SENARYO VE SES KONFIGÜRASYONU\n")
        f.write("=" * 80 + "\n\n")

        # Karakterler
        f.write("KARAKTERLER VE SESLERİ:\n")
        f.write("-" * 80 + "\n")
        for char, config in scenes_data.get('characters', {}).items():
            f.write(f"  • {char}\n")
            f.write(f"    - Ses: {config['voice_name']}\n")
            f.write(f"    - Açıklama: {config['description']}\n\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("SAHNELER\n")
        f.write("=" * 80 + "\n\n")

        # Sahneler
        for scene in scenes_data.get('scenes', []):
            f.write(f"[SAHNE {scene['scene_id']}] ({scene['duration_seconds']}s)\n")
            f.write(f"Konuşan: {scene['speaker']}\n")
            f.write(f"Metni: {scene['voiceover_text']}\n")
            f.write(f"Görsel: {scene['image_prompt']}\n")
            f.write("\n" + "-" * 80 + "\n\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("NOTLAR:\n")
        f.write("=" * 80 + "\n")
        f.write("• Her sahnenin metni TTS (text-to-speech) ile seslendirilecektir\n")
        f.write("• Konuşan kişi (Speaker) karakterin sesini belirler\n")
        f.write("• Metin içinde düzenlemeler yapmak istersen bu dosyayı düzenle\n")
        f.write("• Bitirince 'devam et' komutunu kullan\n")

    return output_path

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

    # TXT formatında senaryo kaydet
    print("\n📝 Senaryo metin formatında kaydediliyor...")
    txt_path = save_script_as_txt(scenes_data)

    print("\n" + "=" * 80)
    print("✅ SENARYO HAZIR!")
    print("=" * 80)
    print(f"\n📄 Senaryo dosyası: {txt_path}")
    print("\n📋 Sahne Özeti:")
    for scene in scenes_data['scenes']:
        print(f"  Sahne {scene['scene_id']}: {scene['duration_seconds']}s - {scene['voiceover_text'][:40]}...")

    print("\n" + "=" * 80)
    print("⏸️  MANUEL CHECKPOINT - DÜZENLEMESİ TAMAMLA")
    print("=" * 80)
    print(f"\n📖 Dosyayı aç: {txt_path}")
    print("\n✏️  Yapabilecekleriniz:")
    print("   • Sahne metinlerini düzenle")
    print("   • Karakterleri değiştir")
    print("   • Ses tariflerini güncelle")
    print("   • Görsel açıklamalarını iyileştir")
    print("\n✅ Hazır olunca bana 'devam et' komutunu gönder")
    print("   Pipeline '{0}' dosyasını okuyup video üretmeye başlayacak")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
