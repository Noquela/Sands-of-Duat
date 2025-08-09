
#!/usr/bin/env python3
"""
LEONARDO AI MASS PRODUCTION
===========================
Automated batch generation using Leonardo AI API
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime

class LeonardoAIProduction:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Leonardo AI optimal settings for game art
        self.settings = {
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Diffusion XL
            "width": 1024,
            "height": 1024,
            "num_images": 1,
            "guidance_scale": 7,
            "num_inference_steps": 30,
            "scheduler": "EULER_DISCRETE",
            "presetStyle": "LEONARDO"
        }
        
    def generate_image(self, prompt, negative_prompt=""):
        """Generate single image via Leonardo AI API."""
        
        payload = {
            **self.settings,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "public": False,
            "nsfw": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generations",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                generation_id = response.json()["sdGenerationJob"]["generationId"]
                
                # Poll for completion
                for _ in range(60):  # Max 5 minutes wait
                    status_response = requests.get(
                        f"{self.base_url}/generations/{generation_id}",
                        headers=self.headers
                    )
                    
                    if status_response.status_code == 200:
                        data = status_response.json()
                        if data["generations_by_pk"]["status"] == "COMPLETE":
                            image_url = data["generations_by_pk"]["generated_images"][0]["url"]
                            return image_url
                        elif data["generations_by_pk"]["status"] == "FAILED":
                            return None
                    
                    time.sleep(5)
            
            return None
            
        except Exception as e:
            print(f"Leonardo AI error: {e}")
            return None
    
    def download_image(self, url, filename):
        """Download image from URL."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return True
        except:
            pass
        return False
    
    def run_production(self):
        """Run mass production with Leonardo AI."""
        
        assets = [
  {
    "id": "deity_anubis_var_1",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "rarity": "legendary"
  },
  {
    "id": "deity_anubis_var_2",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "rarity": "legendary"
  },
  {
    "id": "deity_anubis_var_3",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "rarity": "legendary"
  },
  {
    "id": "deity_anubis_var_4",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "rarity": "legendary"
  },
  {
    "id": "deity_ra_var_1",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "rarity": "legendary"
  },
  {
    "id": "deity_ra_var_2",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "rarity": "legendary"
  },
  {
    "id": "deity_ra_var_3",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "rarity": "legendary"
  },
  {
    "id": "deity_ra_var_4",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "rarity": "legendary"
  },
  {
    "id": "deity_isis_var_1",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "rarity": "legendary"
  },
  {
    "id": "deity_isis_var_2",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "rarity": "legendary"
  },
  {
    "id": "deity_isis_var_3",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "rarity": "legendary"
  },
  {
    "id": "deity_isis_var_4",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "rarity": "legendary"
  },
  {
    "id": "deity_set_var_1",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "rarity": "legendary"
  },
  {
    "id": "deity_set_var_2",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "rarity": "legendary"
  },
  {
    "id": "deity_set_var_3",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "rarity": "legendary"
  },
  {
    "id": "deity_set_var_4",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "rarity": "legendary"
  },
  {
    "id": "deity_thoth_var_1",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "rarity": "legendary"
  },
  {
    "id": "deity_thoth_var_2",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "rarity": "legendary"
  },
  {
    "id": "deity_thoth_var_3",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "rarity": "legendary"
  },
  {
    "id": "deity_thoth_var_4",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "rarity": "legendary"
  },
  {
    "id": "hero_warrior_var_1",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "rarity": "epic"
  },
  {
    "id": "hero_warrior_var_2",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "rarity": "epic"
  },
  {
    "id": "hero_warrior_var_3",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "rarity": "epic"
  },
  {
    "id": "hero_warrior_var_4",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "rarity": "epic"
  },
  {
    "id": "hero_pharaoh_var_1",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "rarity": "epic"
  },
  {
    "id": "hero_pharaoh_var_2",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "rarity": "epic"
  },
  {
    "id": "hero_pharaoh_var_3",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "rarity": "epic"
  },
  {
    "id": "hero_pharaoh_var_4",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "rarity": "epic"
  },
  {
    "id": "hero_priestess_var_1",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "rarity": "epic"
  },
  {
    "id": "hero_priestess_var_2",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "rarity": "epic"
  },
  {
    "id": "hero_priestess_var_3",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "rarity": "epic"
  },
  {
    "id": "hero_priestess_var_4",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "rarity": "epic"
  },
  {
    "id": "creature_sphinx_var_1",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "rarity": "rare"
  },
  {
    "id": "creature_sphinx_var_2",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "rarity": "rare"
  },
  {
    "id": "creature_sphinx_var_3",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "rarity": "rare"
  },
  {
    "id": "creature_sphinx_var_4",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "rarity": "rare"
  },
  {
    "id": "creature_scarab_var_1",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "rarity": "rare"
  },
  {
    "id": "creature_scarab_var_2",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "rarity": "rare"
  },
  {
    "id": "creature_scarab_var_3",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "rarity": "rare"
  },
  {
    "id": "creature_scarab_var_4",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "rarity": "rare"
  },
  {
    "id": "creature_mummy_var_1",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "rarity": "rare"
  },
  {
    "id": "creature_mummy_var_2",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "rarity": "rare"
  },
  {
    "id": "creature_mummy_var_3",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "rarity": "rare"
  },
  {
    "id": "creature_mummy_var_4",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "rarity": "rare"
  },
  {
    "id": "creature_scorpion_var_1",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "rarity": "rare"
  },
  {
    "id": "creature_scorpion_var_2",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "rarity": "rare"
  },
  {
    "id": "creature_scorpion_var_3",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "rarity": "rare"
  },
  {
    "id": "creature_scorpion_var_4",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "rarity": "rare"
  },
  {
    "id": "env_temple_var_1",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "rarity": "epic"
  },
  {
    "id": "env_temple_var_2",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "rarity": "epic"
  },
  {
    "id": "env_temple_var_3",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "rarity": "epic"
  },
  {
    "id": "env_temple_var_4",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "rarity": "epic"
  },
  {
    "id": "env_tomb_var_1",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "rarity": "epic"
  },
  {
    "id": "env_tomb_var_2",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "rarity": "epic"
  },
  {
    "id": "env_tomb_var_3",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "rarity": "epic"
  },
  {
    "id": "env_tomb_var_4",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "rarity": "epic"
  },
  {
    "id": "env_pyramid_var_1",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "rarity": "epic"
  },
  {
    "id": "env_pyramid_var_2",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "rarity": "epic"
  },
  {
    "id": "env_pyramid_var_3",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "rarity": "epic"
  },
  {
    "id": "env_pyramid_var_4",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "rarity": "epic"
  },
  {
    "id": "ui_frame_var_1",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "rarity": "common"
  },
  {
    "id": "ui_frame_var_2",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "rarity": "common"
  },
  {
    "id": "ui_frame_var_3",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "rarity": "common"
  },
  {
    "id": "ui_frame_var_4",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "rarity": "common"
  }
]
        
        print("LEONARDO AI MASS PRODUCTION")
        print("=" * 27)
        print(f"Assets para gerar: {len(assets)}")
        print("Custo estimado: $5-10")
        
        output_dir = Path("leonardo_assets")
        output_dir.mkdir(exist_ok=True)
        
        successful = 0
        failed = 0
        
        for i, asset in enumerate(assets):
            print(f"\nGerando {i+1}/{len(assets)}: {asset['character']}")
            
            image_url = self.generate_image(asset["prompt"])
            
            if image_url:
                filename = output_dir / f"{asset['id']}.png"
                if self.download_image(image_url, filename):
                    successful += 1
                    print(f"  SUCESSO: {filename}")
                else:
                    failed += 1
                    print(f"  FALHA download: {asset['id']}")
            else:
                failed += 1
                print(f"  FALHA geracao: {asset['id']}")
            
            # Rate limiting
            time.sleep(2)
        
        print(f"\nCOMPLETO: {successful} sucessos, {failed} falhas")

# INSTRUCOES DE USO:
# 1. Obtenha API key em: https://app.leonardo.ai/settings
# 2. Execute: producer = LeonardoAIProduction("sua-api-key")
# 3. Execute: producer.run_production()

if __name__ == "__main__":
    api_key = input("Digite sua Leonardo AI API key: ")
    if api_key:
        producer = LeonardoAIProduction(api_key)
        producer.run_production()
    else:
        print("API key necessaria!")
