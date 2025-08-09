#!/usr/bin/env python3
"""
GERADOR DE DATASET HADES-EGYPTIAN - VERSAO SIMPLES
==================================================
Usa sistema básico para gerar dataset LoRA sem dependências quebradas
"""

import json
import time
from pathlib import Path
from datetime import datetime

def create_hades_egyptian_dataset():
    """Cria dataset de prompts para LoRA training."""
    
    print("CRIANDO DATASET HADES-EGYPTIAN PARA LORA")
    print("=" * 40)
    
    # Dataset de prompts otimizados para LoRA
    hades_egyptian_prompts = [
        # Deidades - Legendary
        {
            "id": "deity_anubis",
            "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece",
            "category": "deity",
            "character": "Anubis",
            "rarity": "legendary"
        },
        {
            "id": "deity_ra", 
            "prompt": "Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece",
            "category": "deity",
            "character": "Ra", 
            "rarity": "legendary"
        },
        {
            "id": "deity_isis",
            "prompt": "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece",
            "category": "deity",
            "character": "Isis",
            "rarity": "legendary"
        },
        {
            "id": "deity_set",
            "prompt": "Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece",
            "category": "deity", 
            "character": "Set",
            "rarity": "legendary"
        },
        {
            "id": "deity_thoth",
            "prompt": "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece",
            "category": "deity",
            "character": "Thoth", 
            "rarity": "legendary"
        },
        
        # Heróis - Epic
        {
            "id": "hero_warrior",
            "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece",
            "category": "hero",
            "character": "Egyptian Warrior",
            "rarity": "epic"
        },
        {
            "id": "hero_pharaoh",
            "prompt": "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece",
            "category": "hero",
            "character": "Divine Pharaoh",
            "rarity": "epic"
        },
        {
            "id": "hero_priestess",
            "prompt": "Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece",
            "category": "hero",
            "character": "High Priestess",
            "rarity": "epic"
        },
        
        # Criaturas - Rare
        {
            "id": "creature_sphinx",
            "prompt": "Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece", 
            "category": "creature",
            "character": "Desert Sphinx",
            "rarity": "rare"
        },
        {
            "id": "creature_scarab",
            "prompt": "Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece",
            "category": "creature",
            "character": "Sacred Scarab",
            "rarity": "rare"
        },
        {
            "id": "creature_mummy",
            "prompt": "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece",
            "category": "creature", 
            "character": "Mummy Guardian",
            "rarity": "rare"
        },
        {
            "id": "creature_scorpion",
            "prompt": "Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece",
            "category": "creature",
            "character": "Desert Scorpion", 
            "rarity": "rare"
        },
        
        # Ambientes - Epic
        {
            "id": "env_temple",
            "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece",
            "category": "environment",
            "character": "Sacred Temple",
            "rarity": "epic"
        },
        {
            "id": "env_tomb",
            "prompt": "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece",
            "category": "environment",
            "character": "Pharaoh's Tomb",
            "rarity": "epic"
        },
        {
            "id": "env_pyramid", 
            "prompt": "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece",
            "category": "environment",
            "character": "Great Pyramid",
            "rarity": "epic"
        },
        
        # UI Elements - Common
        {
            "id": "ui_frame",
            "prompt": "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece",
            "category": "ui_element",
            "character": "Sacred Frame", 
            "rarity": "common"
        }
    ]
    
    # Cria dataset estruturado
    dataset = {
        "name": "Hades-Egyptian Fusion Dataset",
        "description": "Training dataset for LoRA model specialized in Hades-style Egyptian artwork",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "total_prompts": len(hades_egyptian_prompts),
        "target_images": len(hades_egyptian_prompts) * 4,  # 4 variações cada
        "categories": {
            "deity": len([p for p in hades_egyptian_prompts if p["category"] == "deity"]),
            "hero": len([p for p in hades_egyptian_prompts if p["category"] == "hero"]),
            "creature": len([p for p in hades_egyptian_prompts if p["category"] == "creature"]),
            "environment": len([p for p in hades_egyptian_prompts if p["category"] == "environment"]),
            "ui_element": len([p for p in hades_egyptian_prompts if p["category"] == "ui_element"])
        },
        "prompts": hades_egyptian_prompts
    }
    
    # Salva dataset
    output_dir = Path("art_pipeline/lora_training/dataset/hades_egyptian")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dataset_file = output_dir / "hades_egyptian_dataset.json"
    with open(dataset_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"Dataset criado: {dataset_file}")
    print(f"Total de prompts: {dataset['total_prompts']}")
    print(f"Target de imagens: {dataset['target_images']}")
    print("Categorias:")
    for cat, count in dataset["categories"].items():
        print(f"  {cat}: {count} prompts")
    
    # Cria instruções de uso
    instructions = f"""
DATASET HADES-EGYPTIAN CRIADO COM SUCESSO!
=========================================

ARQUIVO: {dataset_file}
TOTAL: {dataset['total_prompts']} prompts únicos
TARGET: {dataset['target_images']} imagens (4 variações cada)

PRÓXIMOS PASSOS:
1. Gerar imagens usando ComfyUI, Automatic1111 ou similar
2. Criar captions (.txt) para cada imagem
3. Treinar LoRA com dataset completo
4. Testar LoRA treinado

PROMPTS INCLUÍDOS:
- {dataset['categories']['deity']} Deidades (Ra, Anubis, Isis, Set, Thoth)
- {dataset['categories']['hero']} Heróis (Guerreiro, Faraó, Sacerdotisa)  
- {dataset['categories']['creature']} Criaturas (Esfinge, Escorpião, Múmia, Escaravelho)
- {dataset['categories']['environment']} Ambientes (Templo, Tumba, Pirâmide)
- {dataset['categories']['ui_element']} UI (Molduras ornamentadas)

QUALIDADE: Todos os prompts otimizados para estilo Hades + Egípcio
CONSISTÊNCIA: Palavras-chave padronizadas para LoRA training
"""
    
    instructions_file = output_dir / "DATASET_READY.txt"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"Instruções salvas: {instructions_file}")
    
    return dataset

def main():
    """Executa criação do dataset."""
    dataset = create_hades_egyptian_dataset()
    
    print("\n" + "=" * 50)
    print("DATASET HADES-EGYPTIAN PRONTO PARA LORA TRAINING!")
    print("=" * 50)
    print("Use ComfyUI, Automatic1111 ou similar para gerar as imagens")
    print("Dataset localizado em: art_pipeline/lora_training/dataset/")

if __name__ == "__main__":
    main()