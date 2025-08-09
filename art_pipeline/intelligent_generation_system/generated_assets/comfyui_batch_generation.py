
# COMFYUI BATCH GENERATION - HADES EGYPTIAN ASSETS
# =================================================
# 
# INSTRUCOES:
# 1. Abra ComfyUI
# 2. Carregue o workflow SDXL base
# 3. Configure os parametros abaixo
# 4. Execute em batch
#
# CONFIGURACOES OTIMIZADAS:
# - Modelo: SDXL Base 1.0
# - Resolucao: 1024x1024
# - Steps: 30
# - CFG: 7.5
# - Sampler: DPM++ 2M Karras
# - Scheduler: Karras

TOTAL_IMAGES = 64
BATCH_SIZE = 4

# PROMPTS PARA GERACAO:
prompts_data = [
  {
    "filename": "deity_anubis_var_1",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_2",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_3",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_anubis_var_4",
    "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_1",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_2",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_3",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_ra_var_4",
    "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_1",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_2",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_3",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_isis_var_4",
    "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_1",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_2",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_3",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_set_var_4",
    "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_1",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_2",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_3",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "deity_thoth_var_4",
    "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "deity",
    "rarity": "legendary"
  },
  {
    "filename": "hero_warrior_var_1",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_2",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_3",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_warrior_var_4",
    "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_1",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_2",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_3",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_pharaoh_var_4",
    "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_1",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_2",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_3",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "hero_priestess_var_4",
    "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "hero",
    "rarity": "epic"
  },
  {
    "filename": "creature_sphinx_var_1",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_2",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_3",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_sphinx_var_4",
    "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_1",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_2",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_3",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scarab_var_4",
    "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_1",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_2",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_3",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_mummy_var_4",
    "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_1",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_2",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_3",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "creature_scorpion_var_4",
    "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "creature",
    "rarity": "rare"
  },
  {
    "filename": "env_temple_var_1",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_2",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_3",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_temple_var_4",
    "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_1",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_2",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_3",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_tomb_var_4",
    "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_1",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_2",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_3",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "env_pyramid_var_4",
    "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "environment",
    "rarity": "epic"
  },
  {
    "filename": "ui_frame_var_1",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_2",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_3",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "ui_element",
    "rarity": "common"
  },
  {
    "filename": "ui_frame_var_4",
    "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
    "category": "ui_element",
    "rarity": "common"
  }
]

# WORKFLOW BASICO (JSON para ComfyUI):
workflow_template = {
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
            "seed": 42,
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
            "text": "PROMPT_PLACEHOLDER"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode", 
        "inputs": {
            "clip": ["4", 1],
            "text": "NEGATIVE_PLACEHOLDER"
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
            "filename_prefix": "hades_egyptian_",
            "images": ["8", 0]
        }
    }
}

print("COMFYUI BATCH SCRIPT CARREGADO")
print(f"Total de imagens para gerar: {TOTAL_IMAGES}")
print("Configure o workflow e execute!")
