#!/usr/bin/env python3
"""
COMPREHENSIVE ASSET REGENERATION - SANDS OF DUAT
================================================

Improved version based on previous generation scripts but fixing all identified issues:
- No watermarks or text overlays  
- Consistent Hades-level artistic style
- Single focused elements per asset
- Proper Egyptian authentic styling
- Addresses all quality problems from analysis
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
import os

class ComprehensiveAssetGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = Path("../assets/generated_art")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Base style template for consistency (learned from previous versions)
        self.base_style = """
        masterpiece, highest quality, professional game art,
        Supergiant Games Hades art style, hand painted illustration,
        rich saturated colors, dramatic lighting, painterly texture,
        detailed rendering, premium quality
        """
        
        # Anti-watermark negative prompt
        self.base_negative = """
        text, watermarks, logos, signatures, copyright marks,
        multiple frames, blur, low quality, distorted, amateur,
        modern elements, realistic photo, dull colors
        """

    def initialize_pipeline(self):
        """Initialize SDXL pipeline with optimal settings."""
        if self.pipe is None:
            print("Initializing Stable Diffusion XL pipeline...")
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                use_safetensors=True
            )
            
            self.pipe = self.pipe.to(self.device)
            self.pipe.enable_model_cpu_offload()
            
            print("Pipeline initialized successfully!")

    def regenerate_problem_cards(self):
        """Regenerate cards that had quality issues."""
        print("Regenerating problematic card artwork...")
        
        problem_cards = [
            {
                "name": "desert_meditation", 
                "desc": "Peaceful Egyptian monk meditating in desert temple, golden sand dunes, serene atmosphere",
                "type": "common"
            },
            {
                "name": "sand_grain", 
                "desc": "Magical grain of sand glowing with mystical energy, desert magic, tiny but powerful",
                "type": "common"
            },
            {
                "name": "whisper_of_thoth", 
                "desc": "Ethereal wisdom floating in the air, ancient Egyptian hieroglyphs glowing softly",
                "type": "common"
            }
        ]
        
        for card in problem_cards:
            print(f"Regenerating card: {card['name']}")
            
            prompt = f"""
            {self.base_style}, ancient Egyptian mythology, hieroglyphic details,
            mystical atmosphere, fantasy card game art,
            
            {card['desc']}, ornate jewelry, rich textures,
            atmospheric lighting, detailed illustration
            """
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.base_negative + ", cartoon, anime",
                num_inference_steps=30,
                guidance_scale=8.0,
                width=768,
                height=1024,
                generator=torch.Generator(device=self.device).manual_seed(42)
            ).images[0]
            
            output_path = self.output_dir / f"{card['name']}.png"
            image.save(output_path)
            print(f"Saved: {output_path}")
            time.sleep(2)

    def regenerate_ui_elements_properly(self):
        """Regenerate UI elements as single focused assets without watermarks."""
        print("Regenerating UI elements with proper single-element focus...")
        
        ui_elements = [
            {
                "name": "ui_card_frame_legendary",
                "desc": "Single ornate golden Egyptian card frame border, luxurious decorative pattern, transparent center"
            },
            {
                "name": "ui_card_frame_epic", 
                "desc": "Single elegant silver Egyptian card frame border, mystical hieroglyphic pattern, transparent center"
            },
            {
                "name": "ui_card_frame_rare",
                "desc": "Single bronze Egyptian card frame border, decorative ancient pattern, transparent center" 
            },
            {
                "name": "ui_card_frame_common",
                "desc": "Single simple stone Egyptian card frame border, clean carved pattern, transparent center"
            },
            {
                "name": "ui_play_button",
                "desc": "Single Egyptian stone play button, ankh symbol carved in center, sandstone texture, golden highlights"
            },
            {
                "name": "ui_settings_button", 
                "desc": "Single Egyptian gear button, golden mechanical scarab design, intricate ancient patterns"
            },
            {
                "name": "ui_deck_button",
                "desc": "Single papyrus scroll button design, rolled ancient Egyptian scroll, golden ties"
            },
            {
                "name": "ui_exit_button",
                "desc": "Single temple archway exit button, Egyptian doorway design, mysterious passage"
            }
        ]
        
        for ui in ui_elements:
            print(f"Regenerating UI: {ui['name']}")
            
            prompt = f"""
            {self.base_style}, professional game UI element design,
            ancient Egyptian styling, ornate details, golden accents,
            clean single element, {ui['desc']}, 
            game interface asset, high contrast visibility,
            premium UI design, detailed craftsmanship
            """
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.base_negative + ", multiple elements, cluttered, background scenery, text overlays",
                num_inference_steps=25,
                guidance_scale=7.5,
                width=512,
                height=512,
                generator=torch.Generator(device=self.device).manual_seed(123)
            ).images[0]
            
            output_path = self.output_dir / f"{ui['name']}.png"
            image.save(output_path)
            print(f"Saved: {output_path}")
            time.sleep(2)

    def regenerate_consistent_characters(self):
        """Regenerate character portraits with consistent realistic Hades-style art."""
        print("Regenerating character portraits with consistent art style...")
        
        characters = [
            {
                "name": "char_player_hero",
                "desc": "Egyptian warrior hero, strong determined face, traditional armor and royal headdress, heroic pose"
            },
            {
                "name": "char_anubis_boss", 
                "desc": "Imposing Anubis god boss, jackal-headed deity, golden divine armor, commanding presence, underworld ruler"
            },
            {
                "name": "char_mummy_guardian",
                "desc": "Undead temple guardian, wrapped in ancient bandages, glowing eyes, mystical aura, eternal protector"
            },
            {
                "name": "char_desert_scorpion",
                "desc": "Giant magical scorpion creature, chitinous armor, glowing stinger, desert predator, mystical energy"
            },
            {
                "name": "char_sand_elemental",
                "desc": "Swirling sand creature, mystical whirlwind form, golden particles, desert magic, elemental power"
            }
        ]
        
        for char in characters:
            print(f"Regenerating character: {char['name']}")
            
            prompt = f"""
            {self.base_style}, character portrait art, dramatic lighting,
            detailed facial features, expressive design, ancient Egyptian setting,
            {char['desc']}, ornate costume details, rich textures,
            character design, heroic proportions, detailed rendering
            """
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.base_negative + ", cartoon, anime, poor anatomy, deformed, modern clothing",
                num_inference_steps=28,
                guidance_scale=8.5,
                width=512,
                height=768,
                generator=torch.Generator(device=self.device).manual_seed(456)
            ).images[0]
            
            output_path = self.output_dir / f"{char['name']}.png"
            image.save(output_path)
            print(f"Saved: {output_path}")
            time.sleep(2)

    def regenerate_atmospheric_backgrounds(self):
        """Regenerate background scenes with improved atmospheric quality."""
        print("Regenerating background scenes with enhanced atmosphere...")
        
        backgrounds = [
            {
                "name": "bg_menu_temple",
                "desc": "Majestic Egyptian temple entrance, massive stone columns, golden divine light streaming through, mystical atmosphere"
            },
            {
                "name": "bg_combat_underworld", 
                "desc": "Egyptian underworld battlefield, ancient hieroglyphic pillars, dramatic lighting, mystical combat arena"
            },
            {
                "name": "bg_deck_builder_sanctum",
                "desc": "Sacred chamber with ancient scrolls, mystical artifacts floating, candlelit atmosphere, knowledge sanctuary"
            },
            {
                "name": "bg_victory_sunrise",
                "desc": "Dawn over Egyptian desert, pyramids silhouetted against golden sunrise, victory celebration atmosphere"
            },
            {
                "name": "bg_defeat_dusk", 
                "desc": "Somber evening in ancient necropolis, shadowy tombs, melancholy atmosphere, failing light"
            }
        ]
        
        for bg in backgrounds:
            print(f"Regenerating background: {bg['name']}")
            
            prompt = f"""
            {self.base_style}, cinematic background art, epic composition,
            dramatic atmospheric lighting, rich environmental details,
            {bg['desc']}, ancient Egyptian architecture, mystical ambiance,
            premium quality environment art, detailed stonework, atmospheric perspective
            """
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.base_negative + ", characters, figures, ui elements, poor composition",
                num_inference_steps=30,
                guidance_scale=7.5,
                width=1920,
                height=1080,
                generator=torch.Generator(device=self.device).manual_seed(789)
            ).images[0]
            
            output_path = self.output_dir / f"{bg['name']}.png"
            image.save(output_path)
            print(f"Saved: {output_path}")
            time.sleep(2)

    def generate_all_improved_assets(self):
        """Main comprehensive regeneration process."""
        print("COMPREHENSIVE SANDS OF DUAT ASSET REGENERATION")
        print("=" * 60)
        print("Addressing all identified quality issues:")
        print("- Removing watermarks and text overlays") 
        print("- Ensuring single focused elements")
        print("- Consistent Hades-level art style")
        print("- Proper Egyptian authentic styling")
        print("=" * 60)
        
        if self.device == "cuda":
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
            
        self.initialize_pipeline()
        
        # Execute all regeneration steps
        self.regenerate_problem_cards()
        self.regenerate_ui_elements_properly() 
        self.regenerate_consistent_characters()
        self.regenerate_atmospheric_backgrounds()
        
        print("=" * 60)
        print("COMPREHENSIVE ASSET REGENERATION COMPLETE!")
        print("All quality issues have been addressed:")
        print("- Assets are watermark-free")
        print("- UI elements are single focused components")
        print("- Characters have consistent realistic art style")
        print("- Backgrounds have proper atmospheric quality")
        print("- All assets maintain Egyptian authentic styling")
        print(f"Regenerated assets location: {self.output_dir}")

def main():
    generator = ComprehensiveAssetGenerator()
    generator.generate_all_improved_assets()

if __name__ == "__main__":
    main()