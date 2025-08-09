
import requests
import json
import time
from pathlib import Path

# Automatic1111 API endpoint
API_URL = "http://127.0.0.1:7860"

# All prompts for generation
prompts_data = [
  {
    "filename": "deity_anubis_var_1",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_2",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_3",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_4",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_1",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_2",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_3",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_4",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_1",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_2",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_3",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_4",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_1",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_2",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_3",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_4",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_1",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_2",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_3",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_4",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "hero_warrior_var_1",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_2",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_3",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_4",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_1",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_2",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_3",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_4",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_1",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_2",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_3",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_4",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "creature_sphinx_var_1",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_2",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_3",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_4",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_1",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_2",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_3",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_4",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_1",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_2",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_3",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_4",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_1",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_2",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_3",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_4",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "env_temple_var_1",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_2",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_3",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_4",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_1",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_2",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_3",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_4",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_1",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_2",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_3",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_4",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "ui_frame_var_1",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_2",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_3",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_4",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "category": "ui_element",
    "rarity": "common"
  }
]

def generate_image(prompt_data):
    """Generate single image via A1111 API."""
    
    payload = {
        "prompt": prompt_data["prompt"],
        "negative_prompt": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "cfg_scale": 7.5,
        "sampler_name": "DPM++ 2M Karras",
        "seed": -1,
        "save_images": True,
        "filename": prompt_data["filename"]
    }
    
    try:
        response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"Erro API: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro conexao: {e}")
        return False

def main():
    print("AUTOMATIC1111 BATCH GENERATOR")
    print("=" * 30)
    
    # Test API connection
    try:
        response = requests.get(f"{API_URL}/sdapi/v1/progress")
        if response.status_code != 200:
            print("ERRO: Nao conseguiu conectar com A1111 API")
            return
    except:
        print("ERRO: Automatic1111 nao esta rodando")
        print("Inicie com: python launch.py --api")
        return
    
    print("API conectada! Iniciando batch generation...")
    
    successful = 0
    failed = 0
    
    for i, prompt_data in enumerate(prompts_data):
        print(f"Gerando {i+1}/{len(prompts_data)}: {prompt_data['filename']}")
        
        if generate_image(prompt_data):
            successful += 1
            print(f"  ✓ Sucesso")
        else:
            failed += 1
            print(f"  ✗ Falhou")
        
        # Pausa entre geracoes
        time.sleep(2)
    
    print(f"\nCOMPLETO: {successful} sucessos, {failed} falhas")

if __name__ == "__main__":
    main()
