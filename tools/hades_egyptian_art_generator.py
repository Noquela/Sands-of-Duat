#!/usr/bin/env python3
"""
Hades-Style Egyptian Art Generator
Creates high-quality Egyptian-themed game assets in the distinctive Hades visual style
"""

import os
import sys
import json
import time
from pathlib import Path
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Hades Art Style Characteristics:
# - Rich, saturated colors with deep shadows
# - Hand-painted digital art aesthetic  
# - Bold outlines and defined silhouettes
# - Dramatic lighting with rim lighting effects
# - Stylized proportions (slightly exaggerated features)
# - Classical mythology art influences
# - Clean, readable designs even at small sizes
# - Consistent color palette across assets

HADES_STYLE_BASE = """
masterpiece, best quality, highly detailed digital painting, 
Hades video game art style, hand-painted look, 
rich saturated colors, dramatic lighting, rim lighting,
bold outlines, stylized proportions, 
classical mythology art, clean readable design,
supergiant games art style, Jen Zee art style,
"""

EGYPTIAN_THEMES = {
    "characters": {
        "pharaoh_warrior": {
            "prompt": "Egyptian pharaoh warrior, golden armor with hieroglyphic engravings, ornate headdress with cobra, khopesh sword, regal pose",
            "colors": ["gold", "deep blue", "white", "red"]
        },
        "anubis_judge": {
            "prompt": "Anubis god of death, jackal head, black and gold Egyptian armor, holding scales of justice, mysterious aura",
            "colors": ["black", "gold", "deep purple", "silver"]
        },
        "isis_mother": {
            "prompt": "Isis goddess, elegant Egyptian dress, winged headdress, motherly pose, healing magic aura, serene expression",
            "colors": ["white", "gold", "sky blue", "green"]
        },
        "ra_sun_god": {
            "prompt": "Ra sun god, falcon head with solar disc crown, golden armor with sun motifs, radiating divine light",
            "colors": ["bright gold", "orange", "red", "yellow"]
        },
        "set_chaos": {
            "prompt": "Set god of chaos, animal-like head, dark armor with storm motifs, lightning crackling around, menacing pose",
            "colors": ["dark red", "black", "purple", "electric blue"]
        },
        "thoth_wisdom": {
            "prompt": "Thoth god of wisdom, ibis head, scholarly robes, holding ancient scrolls, mystical hieroglyphs floating",
            "colors": ["deep blue", "silver", "white", "gold"]
        }
    },
    
    "environments": {
        "desert_temple": {
            "prompt": "Ancient Egyptian temple interior, massive stone pillars with hieroglyphics, torch lighting, sand dunes visible through openings",
            "atmosphere": "warm golden lighting, mysterious shadows"
        },
        "underworld_hall": {
            "prompt": "Egyptian underworld throne room, obsidian pillars, glowing ankh symbols, flowing sand waterfalls, ethereal blue light",
            "atmosphere": "cool blue-purple lighting, otherworldly"
        },
        "pyramid_chamber": {
            "prompt": "Inside pyramid burial chamber, golden sarcophagi, jeweled walls, ray of sunlight through opening, treasure scattered",
            "atmosphere": "dramatic chiaroscuro lighting, treasure gleam"
        }
    },
    
    "ui_elements": {
        "boon_frames": {
            "common": "Simple papyrus scroll with basic hieroglyphic border",
            "rare": "Ornate golden ankh frame with blue gemstone accents",  
            "epic": "Elaborate pharaoh crown frame with precious metals",
            "legendary": "Divine sun disc frame with radiating golden rays"
        },
        
        "god_portraits": {
            "style": "Classical Egyptian art style, profile view, rich colors, golden accents, divine aura"
        }
    }
}

class HadesEgyptianArtGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = Path("assets/hades_egyptian_generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "characters").mkdir(exist_ok=True)
        (self.output_dir / "environments").mkdir(exist_ok=True)
        (self.output_dir / "ui_elements").mkdir(exist_ok=True)
        (self.output_dir / "god_portraits").mkdir(exist_ok=True)
        (self.output_dir / "boon_cards").mkdir(exist_ok=True)
        
        print(f"🎨 Initializing Hades-Style Egyptian Art Generator on {self.device.upper()}")
        
        # Load SDXL model optimized for artistic generation
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16"
        ).to(self.device)
        
        # Optimize for quality over speed
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            self.pipe.enable_model_cpu_offload()
    
    def enhance_hades_style(self, image):
        """Apply Hades-specific post-processing to match the game's art style"""
        
        # Increase saturation for that rich Hades color palette
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)
        
        # Boost contrast for dramatic lighting
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Slight sharpening for clean, defined edges
        image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        return image
    
    def generate_character_sprite(self, character_name, character_data):
        """Generate a character sprite in Hades Egyptian style"""
        
        full_prompt = f"""
        {HADES_STYLE_BASE}
        {character_data['prompt']},
        full body character art, heroic pose, 
        Egyptian mythology, ancient Egypt aesthetic,
        centered composition, transparent background ready,
        character concept art, game sprite,
        perfect anatomy, detailed clothing and armor
        """
        
        negative_prompt = """
        blurry, low quality, deformed, multiple heads, 
        modern clothing, contemporary elements,
        watermark, signature, text, cropped,
        bad anatomy, extra limbs
        """
        
        print(f"🏺 Generating {character_name} character sprite...")
        
        image = self.pipe(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=50,
            guidance_scale=8.0,
            width=1024,
            height=1024
        ).images[0]
        
        # Apply Hades style enhancement
        image = self.enhance_hades_style(image)
        
        # Save character sprite
        output_path = self.output_dir / "characters" / f"{character_name}.png"
        image.save(output_path, "PNG")
        print(f"✅ Saved character: {output_path}")
        
        return image
    
    def generate_god_portrait(self, god_name, character_data):
        """Generate Egyptian god portrait for boon selection"""
        
        full_prompt = f"""
        {HADES_STYLE_BASE}
        {character_data['prompt']},
        portrait art, head and shoulders,
        Egyptian god, divine presence, 
        classical Egyptian profile art style,
        ornate golden frame border,
        rich royal colors, mystical aura,
        detailed hieroglyphic background pattern,
        perfect symmetry, regal expression
        """
        
        negative_prompt = """
        full body, blurry, low quality, 
        modern elements, casual clothing,
        multiple faces, deformed features
        """
        
        print(f"👑 Generating {god_name} god portrait...")
        
        image = self.pipe(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=50,
            guidance_scale=8.5,
            width=512,
            height=512
        ).images[0]
        
        image = self.enhance_hades_style(image)
        
        output_path = self.output_dir / "god_portraits" / f"{god_name}_portrait.png"
        image.save(output_path, "PNG")
        print(f"✅ Saved god portrait: {output_path}")
        
        return image
    
    def generate_environment(self, env_name, env_data):
        """Generate Egyptian environment background"""
        
        full_prompt = f"""
        {HADES_STYLE_BASE}
        {env_data['prompt']},
        {env_data['atmosphere']},
        environment art, background painting,
        ancient Egyptian architecture,
        atmospheric perspective, detailed stonework,
        hieroglyphic decorations, torchlight,
        cinematic composition, wide aspect ratio,
        environmental storytelling
        """
        
        negative_prompt = """
        people, characters, modern elements,
        blurry, low detail, bad architecture,
        cartoon style, anime style
        """
        
        print(f"🏛️ Generating {env_name} environment...")
        
        image = self.pipe(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=45,
            guidance_scale=7.5,
            width=1344,  # Ultrawide aspect ratio for backgrounds
            height=768
        ).images[0]
        
        image = self.enhance_hades_style(image)
        
        output_path = self.output_dir / "environments" / f"{env_name}_4k.png"
        image.save(output_path, "PNG")
        print(f"✅ Saved environment: {output_path}")
        
        return image
    
    def generate_ui_frame(self, rarity_name, frame_description):
        """Generate ornate UI frames for boons and cards"""
        
        full_prompt = f"""
        {HADES_STYLE_BASE}
        {frame_description},
        ornate decorative frame, Egyptian motifs,
        UI element, game interface asset,
        symmetrical design, centered empty space,
        golden metalwork, jeweled accents,
        hieroglyphic patterns, ancient craftsmanship,
        clean readable design, high contrast,
        transparent center for content overlay
        """
        
        negative_prompt = """
        filled center, text, characters, 
        modern design, plain frame,
        blurry, low quality
        """
        
        print(f"🖼️ Generating {rarity_name} UI frame...")
        
        image = self.pipe(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=40,
            guidance_scale=8.0,
            width=512,
            height=700  # Card-like proportions
        ).images[0]
        
        image = self.enhance_hades_style(image)
        
        output_path = self.output_dir / "ui_elements" / f"boon_frame_{rarity_name}.png"
        image.save(output_path, "PNG")
        print(f"✅ Saved UI frame: {output_path}")
        
        return image
    
    def generate_main_menu_background(self):
        """Generate epic main menu background"""
        
        full_prompt = f"""
        {HADES_STYLE_BASE}
        Epic Egyptian throne room of the gods,
        massive pharaoh statue, golden throne,
        ray of divine light from above,
        hieroglyphic murals on walls,
        ornate columns with lotus capitals,
        mystical atmosphere, sand particles in air,
        cinematic composition, title screen worthy,
        majestic and awe-inspiring,
        warm golden and cool blue lighting
        """
        
        print("🌅 Generating epic main menu background...")
        
        image = self.pipe(
            prompt=full_prompt,
            negative_prompt="people, characters, text, UI elements",
            num_inference_steps=60,
            guidance_scale=8.0,
            width=1920,  # Full HD for main menu
            height=1080
        ).images[0]
        
        image = self.enhance_hades_style(image)
        
        output_path = self.output_dir / "bg_main_menu_hades_egyptian_4k.png"
        image.save(output_path, "PNG")
        print(f"✅ Saved main menu background: {output_path}")
        
        return image
    
    def generate_complete_asset_set(self):
        """Generate the complete set of Hades-style Egyptian assets"""
        
        print("🎨 Starting complete Hades-Egyptian asset generation...")
        print("=" * 60)
        
        # 1. Generate all character sprites
        print("\n📦 GENERATING CHARACTERS")
        print("-" * 30)
        for char_name, char_data in EGYPTIAN_THEMES["characters"].items():
            self.generate_character_sprite(char_name, char_data)
            time.sleep(2)  # Prevent overload
        
        # 2. Generate god portraits for boon system  
        print("\n👑 GENERATING GOD PORTRAITS")
        print("-" * 30)
        for god_name, char_data in EGYPTIAN_THEMES["characters"].items():
            self.generate_god_portrait(god_name, char_data)
            time.sleep(2)
        
        # 3. Generate environments
        print("\n🏛️ GENERATING ENVIRONMENTS")
        print("-" * 30)
        for env_name, env_data in EGYPTIAN_THEMES["environments"].items():
            self.generate_environment(env_name, env_data)
            time.sleep(3)  # Larger images need more time
        
        # 4. Generate UI frames
        print("\n🖼️ GENERATING UI ELEMENTS")
        print("-" * 30)
        for rarity, description in EGYPTIAN_THEMES["ui_elements"]["boon_frames"].items():
            self.generate_ui_frame(rarity, description)
            time.sleep(2)
        
        # 5. Generate main menu background
        print("\n🌅 GENERATING MAIN MENU")
        print("-" * 30)
        self.generate_main_menu_background()
        
        print("\n" + "=" * 60)
        print("✅ HADES-STYLE EGYPTIAN ASSET GENERATION COMPLETE!")
        print(f"📁 Assets saved to: {self.output_dir}")
        print(f"🎮 Ready for integration into Sands of Duat")

def main():
    """Main generation function"""
    
    print("🏺 SANDS OF DUAT - HADES EGYPTIAN ART GENERATOR 🏺")
    print("=" * 60)
    print("Generating high-quality Egyptian assets in Hades visual style...")
    print()
    
    # Check for GPU availability
    if not torch.cuda.is_available():
        print("⚠️ WARNING: CUDA not available. Generation will be much slower on CPU.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Initialize generator
    generator = HadesEgyptianArtGenerator()
    
    # Generate complete asset set
    generator.generate_complete_asset_set()
    
    print("\n🎉 Art generation complete! Your game now has beautiful Hades-style Egyptian assets.")

if __name__ == "__main__":
    main()