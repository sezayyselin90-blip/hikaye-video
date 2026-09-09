#!/usr/bin/env python3
"""
Senaryo TXT dosyasını JSON'a dönüştüren parser
"""

import re
import json
from pathlib import Path

def parse_txt_to_json(txt_path: str) -> dict:
    """TXT senaryo dosyasını JSON formatına çevirir"""
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Karakterleri bul
    characters = {}
    char_section = re.search(r"KARAKTERLER VE SESLERİ:(.*?)^=", content, re.MULTILINE | re.DOTALL)
    
    if char_section:
        char_text = char_section.group(1)
        char_blocks = re.findall(r"  • (.+?)\n    - Ses: (.+?)\n    - Açıklama: (.+?)(?=\n\n|  •)", char_text, re.DOTALL)
        
        for name, voice, desc in char_blocks:
            # Voice ID'leri belirle
            voice_map = {
                "James": "TxGEqnHWrfWFTfGW9XjX",
                "Bella": "EXAVITQu4vr4xnSDxMaL",
                "Grace": "21m00Tcm4TlvDq8ikWAM",
                "Rachel": "pNInz6obpgDQGcFmaJgB"
            }
            
            voice_id = voice_map.get(voice.strip(), "TxGEqnHWrfWFTfGW9XjX")
            characters[name.strip()] = {
                "voice_id": voice_id,
                "voice_name": voice.strip(),
                "description": desc.strip()
            }
    
    # Sahneleri bul
    scenes = []
    scene_blocks = re.findall(
        r"\[SAHNE (\d+)\] \((\d+)s\)\n"
        r"Konuşan: (.+?)\n"
        r"Metni: (.+?)\n"
        r"Görsel: (.+?)\n",
        content,
        re.MULTILINE
    )
    
    for scene_id, duration, speaker, text, image in scene_blocks:
        scenes.append({
            "scene_id": int(scene_id),
            "duration_seconds": int(duration),
            "voiceover_text": text.strip(),
            "speaker": speaker.strip(),
            "image_prompt": image.strip()
        })
    
    return {
        "characters": characters,
        "character_description": "Multiple characters with distinct voices",
        "scenes": scenes
    }

def update_scenes_json_from_txt(txt_path: str, json_path: str = "scenes.json"):
    """TXT'den JSON'u güncelle"""
    
    if not Path(txt_path).exists():
        print(f"Hata: {txt_path} dosyası bulunamadı!")
        return False
    
    try:
        parsed_data = parse_txt_to_json(txt_path)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {json_path} güncellendi ({len(parsed_data['scenes'])} sahne)")
        return True
    except Exception as e:
        print(f"✗ Parse hatası: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python utils_parser.py <txt_dosyası> [json_çıktısı]")
        sys.exit(1)
    
    txt_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else "scenes.json"
    
    success = update_scenes_json_from_txt(txt_file, json_file)
    sys.exit(0 if success else 1)
