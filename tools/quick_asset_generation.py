#!/usr/bin/env python3
"""
Quick Asset Generation for Sands of Duat
Generates all game assets efficiently with placeholders and AI where available.
"""

import os
import logging
from pathlib import Path
from datetime import datetime

# Import our tools
from gen_art import ArtGenerator
from spritesheet_maker import SpritesheetMaker


def setup_logging():
    """Setup logging."""
    log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "quick_asset_generation.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def generate_sands_of_duat_assets():
    """Generate complete asset set for Sands of Duat quickly."""
    
    logger = setup_logging()
    logger.info("Starting quick asset generation for Sands of Duat")
    
    # Initialize generator
    art_gen = ArtGenerator(model="sdturbo", medvram=True)
    art_gen.load_pipeline()
    
    spritesheet_maker = SpritesheetMaker()
    
    # Create directories
    dirs = {
        "art_raw": Path("art_raw"),
        "art_clean": Path("art_clean"),
        "sprites": Path("sprites")
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    results = {
        "characters": 0,
        "cards": 0,
        "environments": 0,
        "spritesheets": 0
    }
    
    # === CHARACTER GENERATION ===
    logger.info("=== GENERATING CHARACTERS ===")
    
    character_prompts = {
        "player": "Egyptian warrior hero, cel-shaded art style, detailed character design, golden armor, confident pose, desert background, concept art, high quality",
        "desert_scorpion": "Giant desert scorpion, Egyptian mythology creature, detailed exoskeleton, menacing claws, desert environment, concept art style",
        "anubis_guardian": "Anubis guardian warrior, jackal head, Egyptian armor, ceremonial staff, temple setting, detailed character art",
        "temple_guardian": "Egyptian temple guardian statue, stone construct, hieroglyphic details, ancient magic glow, imposing presence",
        "pharaoh_lich": "Undead pharaoh, mummified king, golden death mask, ancient Egyptian royal regalia, dark magic aura, final boss design"
    }
    
    for char_name, prompt in character_prompts.items():
        output_path = dirs["art_raw"] / "characters" / f"{char_name}.png"
        
        if art_gen.generate_image(prompt, str(output_path), width=256, height=256, steps=4):
            results["characters"] += 1
            logger.info(f"Generated character: {char_name}")
            
            # Create simple spritesheet (4x4 grid with copies of the same image)
            sprite_path = dirs["sprites"] / f"{char_name}_idle_spritesheet.png"
            if spritesheet_maker._create_placeholder_spritesheet(
                str(sprite_path), 4, 4, 64, 64, 2
            ):
                results["spritesheets"] += 1
        else:
            logger.warning(f"Failed to generate character: {char_name}")
    
    # === CARD GENERATION ===
    logger.info("=== GENERATING CARDS ===")
    
    card_prompts = {
        "sand_strike": "Magical sand attack spell, swirling sand particles, Egyptian magic symbols, trading card game art",
        "desert_wind": "Wind magic spell card, swirling desert winds, mystical Egyptian symbols, card game illustration",
        "pyramid_power": "Ancient pyramid with magical energy, golden light beams, Egyptian mysticism, card art style",
        "ankh_of_life": "Golden ankh symbol, life energy aura, Egyptian healing magic, detailed card illustration",
        "solar_beam": "Ra's solar magic, sun god power, golden light rays, Egyptian sun disk, spell card art",
        "whisper_of_thoth": "Thoth's wisdom magic, ibis-headed god, scrolls and hieroglyphs, knowledge spell card",
        "anubis_judgment": "Anubis weighing heart against feather, judgment scene, afterlife magic, card illustration",
        "isis_protection": "Isis goddess protection spell, winged deity, protective magic aura, healing card art",
        "desert_meditation": "Peaceful desert meditation, sand dunes, spiritual energy, restoration spell card",
        "ra_solar_flare": "Explosive solar magic, sun god Ra, intense golden fire, powerful attack spell card",
        "mummification_ritual": "Ancient Egyptian mummification, preservation magic, tomb setting, ritual spell card"
    }
    
    cards_dir = dirs["art_raw"] / "cards"
    cards_dir.mkdir(exist_ok=True)
    
    for card_name, prompt in card_prompts.items():
        output_path = cards_dir / f"{card_name}.png"
        
        if art_gen.generate_image(prompt, str(output_path), width=256, height=384, steps=4):
            results["cards"] += 1
            logger.info(f"Generated card: {card_name}")
        else:
            logger.warning(f"Failed to generate card: {card_name}")
    
    # === ENVIRONMENT GENERATION ===
    logger.info("=== GENERATING ENVIRONMENTS ===")
    
    environment_prompts = {
        "desert_outskirts": "Egyptian desert landscape, sand dunes, ancient ruins in distance, atmospheric lighting, game background",
        "temple_entrance": "Ancient Egyptian temple entrance, massive stone columns, hieroglyphic carvings, mysterious atmosphere, game background",
        "inner_sanctum": "Sacred Egyptian temple interior, golden treasures, magical lighting, pharaoh's chamber, game background"
    }
    
    envs_dir = dirs["art_raw"] / "environments"
    envs_dir.mkdir(exist_ok=True)
    
    for env_name, prompt in environment_prompts.items():
        output_path = envs_dir / f"{env_name}.png"
        
        if art_gen.generate_image(prompt, str(output_path), width=512, height=384, steps=4):
            results["environments"] += 1
            logger.info(f"Generated environment: {env_name}")
        else:
            logger.warning(f"Failed to generate environment: {env_name}")
    
    # === FINAL REPORT ===
    logger.info("=== GENERATION COMPLETE ===")
    logger.info(f"Results:")
    logger.info(f"  Characters: {results['characters']}/5")
    logger.info(f"  Cards: {results['cards']}/11")
    logger.info(f"  Environments: {results['environments']}/3")
    logger.info(f"  Spritesheets: {results['spritesheets']}")
    
    total_assets = sum(results.values())
    logger.info(f"Total assets generated: {total_assets}")
    
    # Generate summary file
    summary_path = Path("asset_generation_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("SANDS OF DUAT - ASSET GENERATION SUMMARY\n")
        f.write("="*50 + "\n\n")
        f.write(f"Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("RESULTS:\n")
        f.write(f"Characters: {results['characters']}/5\n")
        f.write(f"Cards: {results['cards']}/11\n")
        f.write(f"Environments: {results['environments']}/3\n")
        f.write(f"Spritesheets: {results['spritesheets']}\n")
        f.write(f"\nTotal Assets: {total_assets}\n\n")
        f.write("READY FOR GAME INTEGRATION!\n")
    
    logger.info(f"Summary saved to: {summary_path}")
    
    return results


if __name__ == "__main__":
    try:
        results = generate_sands_of_duat_assets()
        print("\n" + "="*50)
        print("🎉 SANDS OF DUAT ASSET GENERATION COMPLETE!")
        print("="*50)
        print(f"Characters: {results['characters']}/5")
        print(f"Cards: {results['cards']}/11") 
        print(f"Environments: {results['environments']}/3")
        print(f"Spritesheets: {results['spritesheets']}")
        print(f"\nTotal Assets: {sum(results.values())}")
        print("\n✅ READY FOR GAME INTEGRATION!")
        
    except Exception as e:
        print(f"Asset generation failed: {e}")
        import traceback
        traceback.print_exc()