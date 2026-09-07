# Multi-Character Voice Configuration

The pipeline automatically assigns different ElevenLabs voices to different characters in your story, creating natural dialogue and narration.

## Available English Voices

| Voice ID | Name | Gender | Tone | Best For |
|----------|------|--------|------|----------|
| `TxGEqnHWrfWFTfGW9XjX` | James | Male | Deep, professional, authoritative | Narrator, older men, authority figures |
| `EXAVITQu4vr4xnSDxMaL` | Bella | Female | Warm, conversational, friendly | Main character, emotional scenes |
| `21m00Tcm4TlvDq8ikWAM` | Grace | Female | Clear, intelligent, assertive | Strong women, professionals |
| `pNInz6obpgDQGcFmaJgB` | Rachel | Female | Young, energetic, upbeat | Young characters, action scenes |

## How Character Voices Work

### 1. Automatic Character Detection
The Claude API analyzes your story and identifies:
- Each unique character who has dialogue
- Their role in the story
- Appropriate voice characteristics

### 2. Voice Assignment
The system outputs a `characters` mapping:
```json
{
  "characters": {
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
  }
}
```

### 3. Per-Scene Speaker Attribution
Each scene includes a `speaker` field:
```json
{
  "scene_id": 1,
  "voiceover_text": "Quote or dialogue",
  "speaker": "Marcus",
  "image_prompt": "..."
}
```

### 4. Voice Generation
When generating audio:
- Marcus scenes → Bella voice (warm, character voice)
- Ray scenes → Grace voice (assertive tone)
- Narrator scenes → James voice (professional)

## Manual Voice Override

To manually assign voices, edit `scenes.json` after generation:

```json
{
  "characters": {
    "Your Character Name": {
      "voice_id": "TxGEqnHWrfWFTfGW9XjX",
      "voice_name": "James",
      "description": "Your description"
    }
  },
  "scenes": [
    {
      "scene_id": 1,
      "voiceover_text": "...",
      "speaker": "Your Character Name"
    }
  ]
}
```

Then re-run:
```bash
python 2_assets_fetcher.py
```

## Voice Selection Tips

| Character Type | Recommended Voice | Reason |
|---|---|---|
| Narrator/Storyteller | James | Professional, engaging |
| Female protagonist | Bella or Rachel | Natural, relatable |
| Male protagonist | James | Strong, authoritative |
| Antagonist | Grace | Assertive, commanding |
| Young character | Rachel | Energetic, youthful |
| Elderly character | James | Mature, experienced |
| Multiple characters | Mix 2-3 voices | Variety and clarity |

## Limitations

- Maximum 3-4 distinct voices recommended (maintains clarity)
- Same character should use same voice throughout (consistency)
- Narrator voice is separate from character voices
- ElevenLabs multilingual v2 model used (supports English perfectly)

## Example: Justice Story

```json
{
  "characters": {
    "Narrator": { "voice_id": "TxGEqnHWrfWFTfGW9XjX", "voice_name": "James" },
    "Marcus": { "voice_id": "EXAVITQu4vr4xnSDxMaL", "voice_name": "Bella" },
    "Ray": { "voice_id": "21m00Tcm4TlvDq8ikWAM", "voice_name": "Grace" },
    "Officer Miller": { "voice_id": "pNInz6obpgDQGcFmaJgB", "voice_name": "Rachel" }
  }
}
```

This creates distinct voices for each character, making the video more engaging and easier to follow.
