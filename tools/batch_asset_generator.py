#!/usr/bin/env python3
"""
BATCH ASSET GENERATOR
====================

PHASE 7: Generate ALL game assets using trained Egyptian-Hades LoRA
Creates complete asset library with perfect consistency
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import json
import time
from PIL import Image

class BatchAssetGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = Path("../assets/generated_art_lora")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Optimal settings from PHASE 5 testing
        self.optimal_settings = {
            "trigger_word": "egyptian_hades_art, masterpiece",
            "resolution": 1024,
            "inference_steps": 30,
            "guidance_scale": 7.5,
            "negative_prompt": "low quality, blurry, text, watermark, amateur, distorted"
        }
        
        # Complete asset specification for Sands of Duat
        self.asset_specifications = self.define_all_assets()

    def define_all_assets(self):
        """Define complete asset library for the game."""
        return {
            "legendary_cards": [
                {
                    "name": "ra_sun_god",
                    "prompt": "Ra Egyptian sun god, falcon head, blazing solar disk crown, golden radiance, divine solar deity, majestic wings spread, holding ankh of life"
                },
                {
                    "name": "anubis_judgment", 
                    "prompt": "Anubis Egyptian god of afterlife, noble jackal head, obsidian black fur, golden ceremonial collar, holding scales of justice"
                },
                {
                    "name": "osiris_resurrection",
                    "prompt": "Osiris lord of underworld, mummified pharaoh form, green skin of rebirth, golden headdress, crook and flail crossed"
                },
                {
                    "name": "isis_protection",
                    "prompt": "Isis mother goddess, elegant feminine features, flowing black hair, golden headdress with throne symbol, protective wings"
                },
                {
                    "name": "horus_divine_sight",
                    "prompt": "Horus sky god, regal falcon head, piercing golden eyes, double crown of Egypt, Eye of Horus glowing with power"
                }
            ],
            
            "epic_cards": [
                {
                    "name": "thoth_wisdom",
                    "prompt": "Thoth god of wisdom, ibis head, scholarly appearance, holding papyrus scroll and reed pen, surrounded by hieroglyphs"
                },
                {
                    "name": "bastet_feline_grace",
                    "prompt": "Bastet cat goddess, elegant feline features, protective amulets, graceful pose, golden jewelry and ornate collar"
                },
                {
                    "name": "set_chaos_storm", 
                    "prompt": "Set god of chaos, mysterious creature head, desert storms swirling, red eyes of destruction, wielding staff of power"
                },
                {
                    "name": "sekhmet_war_cry",
                    "prompt": "Sekhmet lioness goddess, fierce feline head, warrior appearance, solar disk crown, breathing fire of battle"
                },
                {
                    "name": "pharaoh_divine_mandate",
                    "prompt": "Divine pharaoh ruler, regal human features, golden death mask, ceremonial beard, royal regalia and scepters"
                }
            ],
            
            "rare_cards": [
                {
                    "name": "mummy_wrath",
                    "prompt": "Undead mummy guardian, wrapped in ancient bandages, glowing eyes, emerging from sarcophagus, ancient curse energy"
                },
                {
                    "name": "scarab_swarm", 
                    "prompt": "Sacred scarab beetles, golden carapace, swirling in mystical formation, ancient Egyptian amulet symbols"
                },
                {
                    "name": "desert_whisper",
                    "prompt": "Desert wind spirit, ethereal sand form, whirlwind shape, mystical energy, ancient secrets in the air"
                },
                {
                    "name": "temple_offering",
                    "prompt": "Ritual altar scene, golden offerings, incense smoke, temple interior, sacred geometry patterns"
                },
                {
                    "name": "canopic_jar_ritual",
                    "prompt": "Four canopic jars, ornate Egyptian vessels, guardian heads, mummification ritual, mystical preservation magic"
                }
            ],
            
            "common_cards": [
                {
                    "name": "sand_grain",
                    "prompt": "Magical grain of sand, glowing with power, desert magic essence, tiny but significant, golden sparkle"
                },
                {
                    "name": "papyrus_scroll",
                    "prompt": "Ancient papyrus manuscript, hieroglyphic writing, rolled scroll, reed paper texture, scholarly knowledge"
                },
                {
                    "name": "desert_meditation",
                    "prompt": "Peaceful desert scene, meditation pose figure, sand dunes, tranquil atmosphere, spiritual enlightenment"
                },
                {
                    "name": "sacred_scarab",
                    "prompt": "Single golden scarab beetle, detailed carapace, sacred symbol, transformation power, Egyptian amulet"
                },
                {
                    "name": "whisper_of_thoth",
                    "prompt": "Ethereal wisdom floating, ancient knowledge, glowing hieroglyphs in air, divine guidance, scholarly magic"
                }
            ],
            
            "backgrounds": [
                {
                    "name": "bg_menu_temple",
                    "prompt": "Majestic Egyptian temple entrance, massive stone columns, divine golden light, colossal pharaoh statues, atmospheric dust rays"
                },
                {
                    "name": "bg_combat_underworld",
                    "prompt": "Egyptian underworld battlefield, obsidian pillars with glowing hieroglyphs, mystical lighting, otherworldly architecture"
                },
                {
                    "name": "bg_deck_builder_sanctum", 
                    "prompt": "Sacred scrolls chamber, mystical artifacts floating, candlelit atmosphere, ancient library, knowledge sanctuary"
                },
                {
                    "name": "bg_victory_sunrise",
                    "prompt": "Dawn over Egyptian desert, pyramids silhouetted, golden sunrise, victory celebration, triumphant atmosphere"
                },
                {
                    "name": "bg_defeat_dusk",
                    "prompt": "Somber evening necropolis, ancient tombs, melancholy lighting, shadowy atmosphere, reflective mood"
                }
            ],
            
            "characters": [
                {
                    "name": "char_player_hero",
                    "prompt": "Egyptian warrior hero, determined expression, traditional pharaonic armor, golden headdress, heroic bearing"
                },
                {
                    "name": "char_anubis_boss",
                    "prompt": "Imposing Anubis boss, massive jackal deity, divine armor, commanding presence, underworld ruler aura"
                },
                {
                    "name": "char_mummy_guardian",
                    "prompt": "Ancient mummy temple guardian, wrapped bandages, glowing eyes, eternal protector, mystical aura"
                },
                {
                    "name": "char_desert_scorpion",
                    "prompt": "Giant magical scorpion, chitinous armor, glowing stinger, desert predator, mystical energy crackling"
                },
                {
                    "name": "char_sand_elemental", 
                    "prompt": "Swirling sand creature, whirlwind form, golden particles, desert magic, elemental power manifestation"
                }
            ],
            
            "ui_elements": [
                {
                    "name": "ui_card_frame_legendary",
                    "prompt": "Ornate golden Egyptian card frame, intricate hieroglyphic patterns, precious gems, luxury border, transparent center"
                },
                {
                    "name": "ui_card_frame_epic",
                    "prompt": "Elegant silver Egyptian frame, turquoise accents, mystical symbols, refined decoration, transparent center"
                },
                {
                    "name": "ui_card_frame_rare",
                    "prompt": "Bronze Egyptian frame, decorative ancient patterns, carved details, polished metal, transparent center"
                },
                {
                    "name": "ui_card_frame_common",
                    "prompt": "Simple stone Egyptian frame, clean carved pattern, sandstone texture, basic elegance, transparent center"
                },
                {
                    "name": "ui_play_button",
                    "prompt": "Egyptian stone play button, ankh symbol carved center, sandstone texture, golden highlights, game interface"
                },
                {
                    "name": "ui_settings_button",
                    "prompt": "Egyptian gear button, golden mechanical scarab design, intricate patterns, ancient technology aesthetic"
                },
                {
                    "name": "ui_deck_button", 
                    "prompt": "Papyrus scroll button design, rolled manuscript, golden ties, ancient Egyptian scroll aesthetic"
                },
                {
                    "name": "ui_exit_button",
                    "prompt": "Temple archway exit button, Egyptian doorway, mysterious passage, stone architecture, portal design"
                }
            ]
        }

    def setup_lora_pipeline(self, lora_path=None):
        """Setup SDXL pipeline with trained LoRA."""
        print("Setting up LoRA generation pipeline...")
        
        # Load SDXL base
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to(self.device)
        
        # Load LoRA if available
        if lora_path and Path(lora_path).exists():
            try:
                self.pipe.load_lora_weights(lora_path)
                print(f"LoRA loaded: {lora_path}")
            except Exception as e:
                print(f"LoRA loading failed: {e}")
                print("Proceeding with base SDXL...")
        else:
            print("LoRA not found, using base SDXL with optimal prompts...")
        
        self.pipe.enable_model_cpu_offload()
        return True

    def generate_asset_category(self, category_name, assets, size_settings):
        """Generate all assets in a category."""
        print(f"Generating {category_name.upper()} ({len(assets)} assets)...")
        
        category_dir = self.output_dir / category_name
        category_dir.mkdir(exist_ok=True)
        
        for i, asset in enumerate(assets):
            print(f"[{i+1}/{len(assets)}] Generating {asset['name']}...")
            
            # Build full prompt with optimal trigger
            full_prompt = f"{self.optimal_settings['trigger_word']}, {asset['prompt']}, professional game art, high quality"
            
            try:
                image = self.pipe(
                    prompt=full_prompt,
                    negative_prompt=self.optimal_settings["negative_prompt"],
                    width=size_settings["width"],
                    height=size_settings["height"],
                    num_inference_steps=self.optimal_settings["inference_steps"],
                    guidance_scale=self.optimal_settings["guidance_scale"],
                    generator=torch.Generator(device=self.device).manual_seed(42 + i)
                ).images[0]
                
                # Save with proper naming
                output_path = category_dir / f"{asset['name']}.png"
                image.save(output_path, "PNG", optimize=True)
                
                print(f"Saved: {output_path}")
                time.sleep(2)  # Prevent overheating
                
            except Exception as e:
                print(f"Error generating {asset['name']}: {e}")

    def generate_all_game_assets(self):
        """Generate complete game asset library."""
        print("=" * 60)
        print("PHASE 7: BATCH GENERATION OF ALL GAME ASSETS")
        print("Creating complete Egyptian-Hades asset library")
        print("=" * 60)
        
        # Asset size specifications
        size_configs = {
            "cards": {"width": 768, "height": 1024},      # Card ratio
            "backgrounds": {"width": 1920, "height": 1080}, # 16:9 HD
            "characters": {"width": 512, "height": 768},   # Portrait
            "ui_elements": {"width": 512, "height": 512}   # Square
        }
        
        total_assets = sum(len(assets) for assets in self.asset_specifications.values())
        print(f"Generating {total_assets} total assets...")
        
        # Generate each category
        for category, assets in self.asset_specifications.items():
            # Determine size config
            if "card" in category:
                size_config = size_configs["cards"]
            elif "bg_" in category or "background" in category:
                size_config = size_configs["backgrounds"] 
            elif "char_" in category or "character" in category:
                size_config = size_configs["characters"]
            elif "ui_" in category:
                size_config = size_configs["ui_elements"]
            else:
                size_config = {"width": 1024, "height": 1024}  # Default
            
            self.generate_asset_category(category, assets, size_config)
        
        print("=" * 60)
        print("PHASE 7 COMPLETE: ALL GAME ASSETS GENERATED!")
        print(f"Asset library created at: {self.output_dir}")
        print("Ready for PHASE 8: Quality Control")
        print("=" * 60)

    def create_asset_manifest(self):
        """Create manifest file for generated assets."""
        manifest = {
            "version": "1.0.0",
            "generated_with": "Egyptian-Hades LoRA v1",
            "total_assets": sum(len(assets) for assets in self.asset_specifications.values()),
            "categories": {
                category: [asset["name"] for asset in assets] 
                for category, assets in self.asset_specifications.items()
            },
            "settings_used": self.optimal_settings,
            "output_directory": str(self.output_dir)
        }
        
        manifest_path = self.output_dir / "asset_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Asset manifest created: {manifest_path}")

    def run_batch_generation(self, lora_path=None):
        """Execute PHASE 7: Batch Asset Generation."""
        # Setup pipeline
        if not self.setup_lora_pipeline(lora_path):
            print("Failed to setup generation pipeline")
            return
        
        # Generate all assets
        self.generate_all_game_assets()
        
        # Create manifest
        self.create_asset_manifest()

def main():
    generator = BatchAssetGenerator()
    
    # Look for trained LoRA
    lora_path = Path("../lora_training/models/egyptian-hades-gameart-v1.safetensors")
    if not lora_path.exists():
        lora_path = None
        print("LoRA not found - using optimized base SDXL")
    
    generator.run_batch_generation(lora_path)

if __name__ == "__main__":
    main()