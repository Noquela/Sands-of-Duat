
#!/usr/bin/env python3
"""
COMFYUI MASS PRODUCTION SYSTEM
==============================
Automated batch generation for all 64 Hades-Egyptian assets
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime

class ComfyUIMassProduction:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"
        self.assets = [
  {
    "id": "deity_anubis_var_1",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_anubis_var_2",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_anubis_var_3",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_anubis_var_4",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "character": "Anubis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_ra_var_1",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_ra_var_2",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_ra_var_3",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_ra_var_4",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "character": "Ra",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_isis_var_1",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_isis_var_2",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_isis_var_3",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_isis_var_4",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "character": "Isis",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_set_var_1",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_set_var_2",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_set_var_3",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_set_var_4",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "character": "Set",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_thoth_var_1",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_thoth_var_2",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_thoth_var_3",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "deity_thoth_var_4",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "character": "Thoth",
    "category": "deity",
    "rarity": "legendary",
    "quality_threshold": 0.9
  },
  {
    "id": "hero_warrior_var_1",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_warrior_var_2",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_warrior_var_3",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_warrior_var_4",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "character": "Egyptian Warrior",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_pharaoh_var_1",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_pharaoh_var_2",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_pharaoh_var_3",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_pharaoh_var_4",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "character": "Divine Pharaoh",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_priestess_var_1",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_priestess_var_2",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_priestess_var_3",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "hero_priestess_var_4",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "character": "High Priestess",
    "category": "hero",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "creature_sphinx_var_1",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_sphinx_var_2",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_sphinx_var_3",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_sphinx_var_4",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "character": "Desert Sphinx",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scarab_var_1",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scarab_var_2",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scarab_var_3",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scarab_var_4",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "character": "Sacred Scarab",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_mummy_var_1",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_mummy_var_2",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_mummy_var_3",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_mummy_var_4",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "character": "Mummy Guardian",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scorpion_var_1",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scorpion_var_2",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scorpion_var_3",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "creature_scorpion_var_4",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "character": "Desert Scorpion",
    "category": "creature",
    "rarity": "rare",
    "quality_threshold": 0.8
  },
  {
    "id": "env_temple_var_1",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_temple_var_2",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_temple_var_3",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_temple_var_4",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "character": "Sacred Temple",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_tomb_var_1",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_tomb_var_2",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_tomb_var_3",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_tomb_var_4",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "character": "Pharaoh's Tomb",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_pyramid_var_1",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_pyramid_var_2",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_pyramid_var_3",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "env_pyramid_var_4",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "character": "Great Pyramid",
    "category": "environment",
    "rarity": "epic",
    "quality_threshold": 0.85
  },
  {
    "id": "ui_frame_var_1",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "category": "ui_element",
    "rarity": "common",
    "quality_threshold": 0.75
  },
  {
    "id": "ui_frame_var_2",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "category": "ui_element",
    "rarity": "common",
    "quality_threshold": 0.75
  },
  {
    "id": "ui_frame_var_3",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "category": "ui_element",
    "rarity": "common",
    "quality_threshold": 0.75
  },
  {
    "id": "ui_frame_var_4",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "character": "Sacred Frame",
    "category": "ui_element",
    "rarity": "common",
    "quality_threshold": 0.75
  }
]
        self.output_dir = Path("assets")
        self.completed = 0
        self.failed = 0
        
    def check_comfyui_status(self):
        """Check if ComfyUI is running."""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats")
            return response.status_code == 200
        except:
            return False
    
    def generate_asset(self, asset_data):
        """Generate single asset via ComfyUI API."""
        
        workflow = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 7.5,
                    "denoise": 1,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0], 
                    "positive": ["6", 0],
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "seed": hash(asset_data["id"]) % 1000000,
                    "steps": 30
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": 1024,
                    "width": 1024
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": asset_data["prompt"]
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": f"mass_production_{asset_data['rarity']}_{asset_data['id']}",
                    "images": ["8", 0]
                }
            }
        }
        
        try:
            # Queue workflow
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow, "client_id": "mass_production"}
            )
            
            if response.status_code == 200:
                prompt_id = response.json()["prompt_id"]
                
                # Wait for completion
                while True:
                    status_response = requests.get(f"{self.comfyui_url}/history/{prompt_id}")
                    if status_response.status_code == 200:
                        history = status_response.json()
                        if prompt_id in history:
                            return True
                    time.sleep(2)
            
            return False
            
        except Exception as e:
            print(f"Error generating {asset_data['id']}: {e}")
            return False
    
    def run_mass_production(self):
        """Execute mass production for all assets."""
        print("COMFYUI MASS PRODUCTION INICIADA")
        print("=" * 32)
        
        if not self.check_comfyui_status():
            print("ERRO: ComfyUI nao esta rodando!")
            print("Inicie ComfyUI primeiro")
            return
        
        print(f"Iniciando producao de {len(self.assets)} assets...")
        
        start_time = time.time()
        
        for i, asset in enumerate(self.assets):
            print(f"\nGerando {i+1}/{len(self.assets)}: {asset['character']} ({asset['rarity']})")
            
            if self.generate_asset(asset):
                self.completed += 1
                print(f"  SUCESSO - {asset['id']}")
            else:
                self.failed += 1  
                print(f"  FALHA - {asset['id']}")
            
            # Progress update
            progress = (i + 1) / len(self.assets) * 100
            elapsed = time.time() - start_time
            eta = (elapsed / (i + 1)) * (len(self.assets) - i - 1) if i > 0 else 0
            
            print(f"  Progresso: {progress:.1f}% | ETA: {eta/60:.0f} min")
            
            # Small delay to prevent overwhelming
            time.sleep(1)
        
        total_time = time.time() - start_time
        
        print(f"\nPRODUCAO COMPLETA!")
        print(f"Sucessos: {self.completed}/{len(self.assets)}")
        print(f"Falhas: {self.failed}")
        print(f"Tempo total: {total_time/3600:.1f} horas")
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "method": "ComfyUI Mass Production",
            "total_assets": len(self.assets),
            "completed": self.completed,
            "failed": self.failed,
            "success_rate": self.completed / len(self.assets) * 100,
            "total_time_hours": total_time / 3600
        }
        
        report_file = Path("mass_production_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Relatorio salvo: {report_file}")

if __name__ == "__main__":
    producer = ComfyUIMassProduction()
    producer.run_mass_production()
