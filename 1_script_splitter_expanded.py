#!/usr/bin/env python3
"""
Genişletilmiş Senaryo Üretici: Hikayenin tüm detaylarını koruyarak
Türkçe düz metin formatında detaylı sahneler oluşturuyor.
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

def generate_expanded_scenario(story: str) -> str:
    """Hikayenin tüm detaylarını koruyarak genişletilmiş senaryo oluştur"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_key_here":
        print("  ⚠️  DEMO MODE: API anahtarı bulunamadı\n")
        return None

    client = Anthropic(api_key=api_key)

    system_prompt = """Sen bir senaryo yazarısın. Görevin:
1. Verilen hikayeyi Türkçe olarak EKSIKSIZ şekilde anlatmak
2. Hiçbir detayı atlamadan, hiçbir kısmını kısaltmadan tam senaryo yazmak
3. Her sahneyi 4-6 saniye okuma süresi için optimize etmek
4. Karakterleri ve diyalogları orijinal hikayeye uygun tutmak
5. Görsel açıklamaları 16:9 format için (Flux dev uyumlu) hazırlamak

ÇIKTI YAPISI:
Her sahne şu formatta olacak:
[SAHNE N] (Xs)
Konuşan: [Karakter Adı veya Anlatıcı]
Metni: [Tam Türkçe metni - 4-6 saniyede okunacak uzunlukta]
Görsel: [16:9 Flux dev uyumlu görsel açıklaması]
---

Kurallar:
- "Anlatıcı (Narrator)" kullan diyalog olmayan sahneler için
- Her sahne 5-6 saniye okuma süresi olacak şekilde planla
- Hikayenin tüm karakterlerini ve detaylarını koru
- Diyalogları orijinal hikayeye sadık kal
- Görsel açıklamalar detaylı ve sinematik olsun"""

    user_message = f"""Bu hikayeyi EKSIKSIZ, detaylı, uzun senaryo olarak Türkçe yazın.
Hiçbir şey atlamayın, özetlemeyin, kısaltmayın. Tüm hikayenin tamamını kapsayan senaryo yazın:

{story}

Çıktı tamamen Türkçe olacak. Tüm karakterleri, diyalogları ve detayları koru.
Her sahne 4-6 saniye okuma süresi olacak şekilde tasarla."""

    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=12000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        response_text = None
        for block in response.content:
            if hasattr(block, 'text'):
                response_text = block.text
                break

        if not response_text:
            raise ValueError("API'den metin yanıtı alınamadı")

        return response_text

    except Exception as e:
        print(f"  ⚠️  Claude API hatası: {e}")
        return None

def save_scenario_as_turkish_text(scenario_text: str, output_path: str = "scripts/hikaye_genisletilmis.txt"):
    """Senaryoyu Türkçe düz metin formatında kaydet"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("HIKAYE: GENİŞLETİLMİŞ SENARYO (Türkçe)\n")
        f.write("=" * 80 + "\n\n")
        f.write(scenario_text)
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("NOTLAR:\n")
        f.write("=" * 80 + "\n")
        f.write("• Bu senaryo orijinal hikayenin tüm detaylarını içerir\n")
        f.write("• Metin TTS (Türkçe text-to-speech) ile seslendirilecektir\n")
        f.write("• Düzenlemeler yapmak istersen bu dosyayı edit et\n")
        f.write("• Hazır olunca 'devam et' komutunu kullan\n")

    return output_path

def main():
    story_path = "story.txt"

    if not Path(story_path).exists():
        print(f"Hata: {story_path} dosyası bulunamadı!")
        return

    print("📖 Hikaye okunuyor...")
    story = load_story(story_path)
    print(f"Hikaye yüklendi ({len(story)} karakter)\n")

    print("🎬 Claude API ile genişletilmiş senaryo oluşturuluyor...")
    print("   (Tüm hikaye detaylarını koruyarak...)\n")

    scenario_text = generate_expanded_scenario(story)

    if not scenario_text:
        print("Senaryo oluşturulamadı!")
        return

    print(f"✓ Senaryo oluşturuldu ({len(scenario_text)} karakter)\n")

    # Türkçe metin formatında senaryo kaydet
    print("💾 Senaryo Türkçe metin formatında kaydediliyor...")
    txt_path = save_scenario_as_turkish_text(scenario_text)
    print(f"✓ Kaydedildi: {txt_path}\n")

    print("=" * 80)
    print("✅ GENİŞLETİLMİŞ SENARYO HAZIR!")
    print("=" * 80)
    print(f"\n📄 Senaryo dosyası: {txt_path}")
    print("\n📋 İçerik özeti:")
    lines = scenario_text.split('\n')
    scene_count = len([l for l in lines if l.startswith('[SAHNE')])
    print(f"   • Toplam sahne: {scene_count}")
    print(f"   • Toplam metin: {len(scenario_text)} karakter\n")

    print("=" * 80)
    print("⏸️  MANUEL CHECKPOINT - SENARYOyu INCELE")
    print("=" * 80)
    print(f"\n📖 Dosyayı aç: {txt_path}")
    print("\n✏️  İstersen yapabilecekleriniz:")
    print("   • Sahne metinlerini düzenle")
    print("   • Detayları ekle veya çıkar")
    print("   • Görsel açıklamalarını iyileştir")
    print("   • Sahne sürelerini ayarla")
    print("\n✅ Gözden geçirip hazır olunca 'devam et' komutunu gönder")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
