#!/usr/bin/env python3
"""
Complete Animation Pipeline for Sands of Duat
End-to-end automation: Image Generation → Animation → Spritesheet → Godot Integration
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import our pipeline components
from gen_art import ArtGenerator
from refine_sdxl import SDXLRefiner
from animation_pipeline import AnimationPipeline
from spritesheet_maker import SpritesheetMaker
from godot_mcp_integration import GodotMCPIntegration


class CompleteAnimationPipeline:
    """Complete end-to-end animation pipeline for Sands of Duat."""
    
    def __init__(self, medvram: bool = False, mcp_host: str = "localhost", mcp_port: int = 8989):
        self.medvram = medvram
        self.logger = self._setup_logging()
        
        # Initialize pipeline components
        self.art_generator = ArtGenerator(medvram=medvram)
        self.sdxl_refiner = SDXLRefiner(medvram=medvram)
        self.animation_pipeline = AnimationPipeline(medvram=medvram)
        self.spritesheet_maker = SpritesheetMaker()
        self.godot_integration = GodotMCPIntegration(mcp_host, mcp_port)
        
        # Pipeline directories
        self.dirs = {
            "art_raw": Path("art_raw"),
            "art_clean": Path("art_clean"),
            "anim_clips": Path("anim_clips"),
            "sprites": Path("sprites"),
            "logs": Path("logs")
        }
        
        # Create directories
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Character animation sets for Sands of Duat
        self.character_sets = {
            "player": {
                "animations": ["idle", "walk", "attack"],
                "prompt": "Egyptian warrior hero, detailed character design, golden armor, confident pose, desert background, concept art"
            },
            "desert_scorpion": {
                "animations": ["idle", "attack"],
                "prompt": "Giant desert scorpion, Egyptian mythology creature, detailed exoskeleton, menacing claws, desert environment"
            },
            "anubis_guardian": {
                "animations": ["idle", "attack"],
                "prompt": "Anubis guardian warrior, jackal head, Egyptian armor, ceremonial staff, temple setting"
            },
            "temple_guardian": {
                "animations": ["idle", "attack"],
                "prompt": "Egyptian temple guardian statue, stone construct, hieroglyphic details, ancient magic glow"
            },
            "pharaoh_lich": {
                "animations": ["idle", "attack", "death"],
                "prompt": "Undead pharaoh, mummified king, golden death mask, ancient Egyptian royal regalia, dark magic aura"
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "complete_pipeline.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def create_character_animation_set(self, character: str, style: str = "cel-shade desert",
                                     force_regenerate: bool = False) -> bool:
        """Create complete animation set for a character."""
        
        if character not in self.character_sets:
            self.logger.error(f"Unknown character: {character}")
            return False
        
        char_config = self.character_sets[character]
        animations = char_config["animations"]
        base_prompt = char_config["prompt"]
        
        self.logger.info(f"Creating animation set for {character} with {len(animations)} animations")
        
        try:
            # Step 1: Generate base character image (if not exists or force regenerate)
            base_image_path = self.dirs["art_raw"] / f"{character}_base.png"
            
            if not base_image_path.exists() or force_regenerate:
                self.logger.info(f"Step 1: Generating base image for {character}")
                
                # Generate with SDTurbo for speed
                success = self.art_generator.generate_image(
                    prompt=f"{base_prompt}, {style}",
                    output_path=str(base_image_path),
                    steps=8, cfg=3.5, width=512, height=512
                )
                
                if not success:
                    self.logger.error(f"Failed to generate base image for {character}")
                    return False
            
            # Step 2: Refine base image with SDXL
            refined_image_path = self.dirs["art_clean"] / f"{character}_refined.png"
            
            if not refined_image_path.exists() or force_regenerate:
                self.logger.info(f"Step 2: Refining image for {character}")
                
                success = self.sdxl_refiner.refine_image(
                    input_path=str(base_image_path),
                    output_path=str(refined_image_path),
                    style="character",
                    steps=28, cfg=7.0, strength=0.35
                )
                
                if not success:
                    self.logger.error(f"Failed to refine image for {character}")
                    return False
            
            # Step 3: Generate animations for each action
            successful_animations = 0
            
            for animation in animations:
                self.logger.info(f"Step 3.{successful_animations+1}: Creating {animation} animation for {character}")
                
                # Generate animation
                anim_video_path = self.dirs["anim_clips"] / f"{character}_{animation}.mp4"
                
                if not anim_video_path.exists() or force_regenerate:
                    preset = f"character_{animation}"
                    success = self.animation_pipeline.animate_diff_generate(
                        input_image=str(refined_image_path),
                        output_video=str(anim_video_path),
                        preset=preset
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to create {animation} animation for {character}")
                        continue
                
                # Step 4: Convert to spritesheet
                spritesheet_path = self.dirs["sprites"] / f"{character}_{animation}_spritesheet.png"
                
                if not spritesheet_path.exists() or force_regenerate:
                    success = self.spritesheet_maker.video_to_spritesheet(
                        video_path=str(anim_video_path),
                        output_path=str(spritesheet_path),
                        rows=4, cols=4, frame_width=128, frame_height=128, padding=2
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to create spritesheet for {character}:{animation}")
                        continue
                
                # Step 5: Import to Godot
                success = self.godot_integration.import_spritesheet(
                    spritesheet_path=str(spritesheet_path),
                    character_name=character,
                    animation_name=animation
                )
                
                if success:
                    successful_animations += 1
                    self.logger.info(f"Successfully created {animation} animation for {character}")
                else:
                    self.logger.warning(f"Failed to import {animation} animation for {character}")
            
            # Step 6: Setup AnimationTree
            if successful_animations > 0:
                self.logger.info(f"Step 6: Setting up AnimationTree for {character}")
                
                completed_animations = [anim for anim in animations 
                                      if (self.dirs["sprites"] / f"{character}_{anim}_spritesheet.png").exists()]
                
                success = self.godot_integration.setup_character_animation_tree(
                    character_name=character,
                    animations=completed_animations
                )
                
                if success:
                    self.logger.info(f"AnimationTree setup completed for {character}")
                else:
                    self.logger.warning(f"Failed to setup AnimationTree for {character}")
            
            # Report results
            total_time = time.time()
            self.logger.info(f"Character animation set completed for {character}: "
                           f"{successful_animations}/{len(animations)} animations successful")
            
            return successful_animations > 0
            
        except Exception as e:
            self.logger.error(f"Pipeline failed for {character}: {e}")
            return False
    
    def create_card_art_set(self, force_regenerate: bool = False) -> int:
        """Generate complete card art set for Sands of Duat."""
        
        # Card definitions from the game
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
        
        successful = 0
        total_cards = len(card_prompts)
        
        self.logger.info(f"Generating card art set: {total_cards} cards")
        
        for card_name, prompt in card_prompts.items():
            try:
                self.logger.info(f"Creating card art: {card_name}")
                
                # Step 1: Generate raw card art
                raw_path = self.dirs["art_raw"] / "cards" / f"{card_name}.png"
                raw_path.parent.mkdir(exist_ok=True)
                
                if not raw_path.exists() or force_regenerate:
                    success = self.art_generator.generate_image(
                        prompt=prompt,
                        output_path=str(raw_path),
                        width=400, height=600, steps=8, cfg=3.5
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to generate raw art for {card_name}")
                        continue
                
                # Step 2: Refine with SDXL
                refined_path = self.dirs["art_clean"] / "cards" / f"{card_name}.png"
                refined_path.parent.mkdir(exist_ok=True)
                
                if not refined_path.exists() or force_regenerate:
                    success = self.sdxl_refiner.refine_image(
                        input_path=str(raw_path),
                        output_path=str(refined_path),
                        style="card",
                        steps=28, cfg=7.0, strength=0.3
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to refine art for {card_name}")
                        continue
                
                # Step 3: Import to Godot
                success = self.godot_integration.import_card_texture(
                    card_image_path=str(refined_path),
                    card_name=card_name
                )
                
                if success:
                    successful += 1
                    self.logger.info(f"Successfully created card art: {card_name}")
                else:
                    self.logger.warning(f"Failed to import card art: {card_name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to create card art for {card_name}: {e}")
        
        self.logger.info(f"Card art generation completed: {successful}/{total_cards} successful")
        return successful
    
    def create_environment_set(self, force_regenerate: bool = False) -> int:
        """Generate environment backgrounds."""
        
        environment_prompts = {
            "desert_outskirts": "Egyptian desert landscape, sand dunes, ancient ruins in distance, atmospheric lighting, game background",
            "temple_entrance": "Ancient Egyptian temple entrance, massive stone columns, hieroglyphic carvings, mysterious atmosphere, game background",
            "inner_sanctum": "Sacred Egyptian temple interior, golden treasures, magical lighting, pharaoh's chamber, game background"
        }
        
        successful = 0
        total_envs = len(environment_prompts)
        
        self.logger.info(f"Generating environment set: {total_envs} backgrounds")
        
        for env_name, prompt in environment_prompts.items():
            try:
                self.logger.info(f"Creating environment: {env_name}")
                
                # Step 1: Generate raw environment
                raw_path = self.dirs["art_raw"] / "environments" / f"{env_name}.png"
                raw_path.parent.mkdir(exist_ok=True)
                
                if not raw_path.exists() or force_regenerate:
                    success = self.art_generator.generate_image(
                        prompt=prompt,
                        output_path=str(raw_path),
                        width=1024, height=768, steps=12, cfg=4.0
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to generate environment: {env_name}")
                        continue
                
                # Step 2: Refine with SDXL
                refined_path = self.dirs["art_clean"] / "environments" / f"{env_name}.png"
                refined_path.parent.mkdir(exist_ok=True)
                
                if not refined_path.exists() or force_regenerate:
                    success = self.sdxl_refiner.refine_image(
                        input_path=str(raw_path),
                        output_path=str(refined_path),
                        style="environment",
                        steps=28, cfg=6.0, strength=0.4
                    )
                    
                    if not success:
                        self.logger.warning(f"Failed to refine environment: {env_name}")
                        continue
                
                # Step 3: Import to Godot
                success = self.godot_integration.import_environment_background(
                    bg_image_path=str(refined_path),
                    env_name=env_name
                )
                
                if success:
                    successful += 1
                    self.logger.info(f"Successfully created environment: {env_name}")
                else:
                    self.logger.warning(f"Failed to import environment: {env_name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to create environment {env_name}: {e}")
        
        self.logger.info(f"Environment generation completed: {successful}/{total_envs} successful")
        return successful
    
    def create_complete_asset_set(self, force_regenerate: bool = False) -> Dict[str, int]:
        """Generate complete asset set for Sands of Duat."""
        
        self.logger.info("Starting complete asset generation for Sands of Duat")
        start_time = time.time()
        
        results = {
            "characters": 0,
            "cards": 0,
            "environments": 0
        }
        
        # Generate all characters
        self.logger.info("=== GENERATING CHARACTERS ===")
        for character in self.character_sets.keys():
            if self.create_character_animation_set(character, force_regenerate=force_regenerate):
                results["characters"] += 1
        
        # Generate all cards
        self.logger.info("=== GENERATING CARDS ===")
        results["cards"] = self.create_card_art_set(force_regenerate=force_regenerate)
        
        # Generate all environments
        self.logger.info("=== GENERATING ENVIRONMENTS ===")
        results["environments"] = self.create_environment_set(force_regenerate=force_regenerate)
        
        # Refresh Godot project
        self.logger.info("=== REFRESHING GODOT PROJECT ===")
        self.godot_integration.refresh_godot_project()
        
        # Final report
        total_time = time.time() - start_time
        self.logger.info(f"Complete asset generation finished in {total_time:.1f}s")
        self.logger.info(f"Results: {results['characters']} characters, "
                        f"{results['cards']} cards, {results['environments']} environments")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Complete Animation Pipeline for Sands of Duat")
    parser.add_argument("--character", help="Generate animation set for specific character")
    parser.add_argument("--style", default="cel-shade desert", help="Art style for characters")
    parser.add_argument("--cards", action="store_true", help="Generate card art set")
    parser.add_argument("--environments", action="store_true", help="Generate environment set")
    parser.add_argument("--all", action="store_true", help="Generate complete asset set")
    parser.add_argument("--force", action="store_true", help="Force regenerate existing assets")
    parser.add_argument("--medvram", action="store_true", help="Enable memory efficient mode")
    parser.add_argument("--mcp-host", default="localhost", help="MCP server host")
    parser.add_argument("--mcp-port", type=int, default=8989, help="MCP server port")
    
    args = parser.parse_args()
    
    # Initialize complete pipeline
    pipeline = CompleteAnimationPipeline(
        medvram=args.medvram,
        mcp_host=args.mcp_host,
        mcp_port=args.mcp_port
    )
    
    if args.all:
        # Generate complete asset set
        results = pipeline.create_complete_asset_set(force_regenerate=args.force)
        print(f"Complete asset generation completed:")
        print(f"  Characters: {results['characters']}")
        print(f"  Cards: {results['cards']}")
        print(f"  Environments: {results['environments']}")
        
    elif args.character:
        # Generate specific character
        success = pipeline.create_character_animation_set(
            args.character, args.style, args.force
        )
        if success:
            print(f"Successfully generated animation set for {args.character}")
        else:
            print(f"Failed to generate animation set for {args.character}")
            sys.exit(1)
    
    elif args.cards:
        # Generate card art
        count = pipeline.create_card_art_set(force_regenerate=args.force)
        print(f"Generated {count} card artworks")
    
    elif args.environments:
        # Generate environments
        count = pipeline.create_environment_set(force_regenerate=args.force)
        print(f"Generated {count} environment backgrounds")
    
    else:
        print("Use --character, --cards, --environments, or --all")
        print("Available characters:", list(pipeline.character_sets.keys()))


if __name__ == "__main__":
    main()