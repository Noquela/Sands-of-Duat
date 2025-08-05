#!/usr/bin/env python3
"""
Hades-Style Art Generator for Sands of Duat
Creates professional-quality Egyptian underworld art in the style of Hades game.
"""

import argparse
import logging
import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import torch
    from diffusers import StableDiffusionPipeline, DiffusionPipeline
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    import numpy as np
    DIFFUSERS_AVAILABLE = True
except ImportError as e:
    print(f"Missing AI dependencies: {e}")
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    DIFFUSERS_AVAILABLE = False


class HadesStyleArtGenerator:
    """Professional Hades-style art generator for Egyptian underworld theme."""
    
    def __init__(self, model: str = "sdxl", device: str = "auto", high_quality: bool = True):
        self.model = model
        self.high_quality = high_quality
        self.pipeline = None
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Setup device
        if DIFFUSERS_AVAILABLE:
            self.device = self._setup_device(device)
        else:
            self.device = "cpu"
        
        # HADES-STYLE Egyptian Underworld Prompts
        self.art_style_base = (
            "Hades game art style, cel-shaded illustration, highly detailed, "
            "dramatic lighting, rich colors, professional game art, "
            "Egyptian mythology, underworld aesthetic, "
            "intricate lineart, painted illustration style"
        )
        
        self.duat_atmosphere = (
            "Sands of Duat, Egyptian underworld, mystical atmosphere, "
            "golden hieroglyphs, ancient magic, shadowy depths, "
            "ornate Egyptian decorations, burial chamber aesthetic"
        )
        
        # Ultra-detailed prompts for each asset type
        self.prompts = {
            "cards": {
                # Attack Cards
                "sand_strike": f"{self.art_style_base}, {self.duat_atmosphere}, "
                             "swirling sand tornado attack, magical sand particles with golden glow, "
                             "desert warrior casting spell, intricate sand magic symbols, "
                             "dramatic action pose, Egyptian armor details, card frame border",
                
                "tomb_strike": f"{self.art_style_base}, {self.duat_atmosphere}, "
                             "undead mummy warrior emerging from sarcophagus, ancient bandages flowing, "
                             "golden death mask, ceremonial khopesh sword, tomb interior background, "
                             "dramatic shadows, Egyptian burial treasures, intimidating pose",
                
                "ra_solar_flare": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "Ra the sun god casting solar magic, falcon-headed deity, "
                                "intense golden solar flare energy, sun disk crown, "
                                "hieroglyphic spell circles, blazing solar powers, divine presence",
                
                "scarab_swarm": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "massive swarm of golden scarab beetles, jeweled carapaces, "
                              "mystical insect magic, ancient Egyptian burial scarabs, "
                              "swirling cloud formation, desert tomb environment, ominous atmosphere",
                
                # Defense Cards  
                "ankh_blessing": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "ornate golden ankh symbol radiating healing light, "
                               "divine protection aura, intricate Egyptian engravings, "
                               "peaceful healing energy, sacred temple background, blessed atmosphere",
                
                "isis_grace": f"{self.art_style_base}, {self.duat_atmosphere}, "
                            "Isis goddess with outstretched winged arms, protective divine aura, "
                            "elegant Egyptian dress and jewelry, golden headdress, "
                            "healing magic emanating from hands, temple of Isis background",
                
                "pyramid_power": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "ancient pyramid channeling mystical energy, golden capstone glowing, "
                               "geometric sacred patterns, powerful ley lines, "
                               "desert night sky with stars, monumental architecture",
                
                # Utility Cards
                "papyrus_scroll": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "ancient papyrus with glowing hieroglyphs, magical writing appearing, "
                                "Thoth's wisdom magic, ibis feather quill, "
                                "scholarly spells, library of Alexandria atmosphere, knowledge power",
                
                "desert_whisper": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "mysterious figure in desert robes, sand magic swirling around, "
                                "hidden face with glowing eyes, ancient secrets, "
                                "whispered incantations, mystical desert winds, ethereal presence",
                
                "thoths_wisdom": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "Thoth the ibis-headed god of knowledge, sacred scrolls floating, "
                               "hieroglyphic magic circles, divine wisdom emanating, "
                               "hall of two truths background, scales of justice, scholarly magic",
                
                "anubis_judgment": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "Anubis jackal-headed god weighing heart against feather, "
                                 "sacred scales of justice, weighing of the heart ceremony, "
                                 "judgment hall of the dead, solemn divine presence, afterlife trial",
                
                "pharaohs_resurrection": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                       "pharaoh rising from golden sarcophagus, royal burial mask, "
                                       "resurrection magic swirling, undead royal power, "
                                       "treasure-filled tomb chamber, regal undead presence",
                
                "mummys_wrath": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "enraged mummy warrior, ancient bandages unwrapping, "
                              "cursed burial magic, tomb guardian fury, "
                              "egyptian weapons and armor, vengeful undead spirit"
            },
            
            "characters": {
                "player_character": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                  "heroic Egyptian adventurer, detailed character design, "
                                  "bronze and gold armor with hieroglyphic details, confident stance, "
                                  "ancient Egyptian weapons, determined expression, "
                                  "protagonist energy, ready for adventure pose",
                
                "anubis_guardian": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "imposing Anubis temple guardian, jackal-headed warrior, "
                                 "ceremonial Egyptian armor, staff of judgment, "
                                 "divine authority presence, guardian of the dead, intimidating pose",
                
                "desert_scorpion": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "giant desert scorpion creature, chitinous exoskeleton with golden markings, "
                                 "venomous stinger raised, menacing claws, "
                                 "sand creature design, predatory stance, desert predator",
                
                "pharaoh_lich": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "undead pharaoh final boss, ornate golden death mask, "
                              "royal Egyptian regalia, dark necromantic aura, "
                              "floating above throne, commanding presence, ancient evil power",
                
                "temple_guardian": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "stone temple guardian construct, hieroglyphic carved body, "
                                 "ancient magic animating statue, imposing size, "
                                 "temple defender, carved Egyptian details, mystical glow in eyes"
            },
            
            "environments": {
                "menu_background": f"{self.art_style_base}, cinematic Egyptian underworld landscape, "
                                 "vast desert with ancient pyramids silhouetted against twilight sky, "
                                 "golden sand dunes, mysterious atmosphere, "
                                 "entrance to the underworld, epic scale, dramatic lighting",
                
                "combat_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                   "ancient Egyptian tomb chamber interior, stone pillars with hieroglyphs, "
                                   "flickering torch lighting, mysterious shadows, "
                                   "burial treasures scattered, sacred Egyptian architecture",
                
                "deck_builder_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                         "scholarly chamber in Egyptian temple, papyrus scrolls everywhere, "
                                         "magical writing implements, Thoth's wisdom shrine, "
                                         "peaceful study atmosphere, ancient library aesthetic",
                
                "progression_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                        "map of the Egyptian underworld, Duat realm passages, "
                                        "glowing pathways through afterlife, divine judgment chambers, "
                                        "mystical journey map, celestial Egyptian art style"
            },
            
            "ui_elements": {
                "ornate_button": f"{self.art_style_base}, ornate Egyptian button design, "
                               "golden hieroglyphic border, carved stone texture, "
                               "ancient Egyptian decorative elements, clickable UI element",
                
                "card_frame": f"{self.art_style_base}, elegant Egyptian card frame border, "
                            "intricate golden decorations, hieroglyphic patterns, "
                            "papyrus texture background, professional card game design",
                
                "health_orb": f"{self.art_style_base}, Egyptian scarab health orb, "
                            "golden beetle with gem center, life force energy, "
                            "glowing magical essence, UI health indicator design",
                
                "mana_crystal": f"{self.art_style_base}, Egyptian ankh mana crystal, "
                              "mystical blue energy core, golden ankh structure, "
                              "magical power reservoir, UI mana indicator design"
            }
        }
        
        # Negative prompts for quality control
        self.negative_prompt = (
            "blurry, low quality, distorted, watermark, signature, text, "
            "bad anatomy, deformed, ugly, amateur art, simple drawing, "
            "cartoon style, anime style, low detail, boring composition, "
            "modern elements, contemporary clothing, photography, realistic photo"
        )
        
        # Egyptian color palette
        self.egyptian_colors = {
            'gold': '#FFD700',
            'bronze': '#CD7F32', 
            'deep_gold': '#B8860B',
            'royal_blue': '#4169E1',
            'desert_sand': '#DEB887',
            'papyrus': '#F5E6A3',
            'obsidian': '#0C0C0C',
            'carnelian': '#B22222',
            'turquoise': '#40E0D0',
            'ivory': '#FFFFF0'
        }
    
    def _setup_device(self, device: str) -> str:
        """Setup compute device with optimizations."""
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                torch.backends.cudnn.benchmark = True
                torch.backends.cuda.enable_flash_sdp(True)
            else:
                device = "cpu"
                self.logger.warning("CUDA not available, using CPU")
        
        if device == "cuda" and torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            self.logger.info(f"Using GPU: {gpu_name} ({memory_gb:.1f} GB)")
        
        return device
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "hades_art.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def load_pipeline(self):
        """Load the AI art generation pipeline."""
        if not DIFFUSERS_AVAILABLE:
            self.logger.warning("AI generation not available, using professional placeholders")
            return
        
        self.logger.info(f"Loading {self.model} pipeline for Hades-style art...")
        
        model_configs = {
            "sdxl": {
                "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
                "pipeline": DiffusionPipeline
            },
            "sdturbo": {
                "model_id": "stabilityai/sd-turbo", 
                "pipeline": StableDiffusionPipeline
            }
        }
        
        if self.model not in model_configs:
            raise ValueError(f"Unknown model: {self.model}")
        
        config = model_configs[self.model]
        
        try:
            kwargs = {
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
                "use_safetensors": True,
                "variant": "fp16" if self.device == "cuda" else None
            }
            
            self.pipeline = config["pipeline"].from_pretrained(
                config["model_id"], **kwargs
            ).to(self.device)
            
            if self.device == "cuda":
                self.pipeline.enable_model_cpu_offload()
                self.pipeline.enable_vae_slicing() 
                self.pipeline.enable_attention_slicing("max")
            
            self.logger.info(f"Pipeline loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load AI pipeline: {e}")
            self.pipeline = None
    
    def generate_professional_image(self, prompt: str, output_path: str,
                                  width: int = 1024, height: int = 1024,
                                  steps: int = 50, cfg: float = 7.5,
                                  seed: Optional[int] = None) -> bool:
        """Generate a professional-quality Hades-style image."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.pipeline:
                return self._generate_professional_placeholder(prompt, output_path, width, height)
            
            self.logger.info(f"Generating Hades-style art: {prompt[:60]}...")
            
            # Enhanced prompt for Hades style
            enhanced_prompt = f"{prompt}, masterpiece, best quality, highly detailed, professional illustration"
            
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            start_time = time.time()
            
            # Generate with high quality settings
            result = self.pipeline(
                prompt=enhanced_prompt,
                negative_prompt=self.negative_prompt,
                num_inference_steps=steps,
                guidance_scale=cfg,
                width=width,
                height=height,
                generator=generator
            )
            
            # Post-process for Hades style
            image = result.images[0]
            image = self._enhance_hades_style(image)
            
            # Save with high quality
            image.save(output_path, quality=95, optimize=True)
            
            generation_time = time.time() - start_time
            self.logger.info(f"Generated in {generation_time:.2f}s: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate image: {e}")
            return self._generate_professional_placeholder(prompt, output_path, width, height)
    
    def _enhance_hades_style(self, image: Image.Image) -> Image.Image:
        """Apply Hades-style post-processing effects."""
        # Enhance colors and contrast like Hades
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # Boost saturation
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)  # Boost contrast
        
        enhancer = ImageEnhance.Sharpness(image) 
        image = enhancer.enhance(1.1)  # Sharpen details
        
        return image
    
    def _generate_professional_placeholder(self, prompt: str, output_path: str,
                                         width: int = 1024, height: int = 1024) -> bool:
        """Generate professional Egyptian-style placeholder."""
        try:
            self.logger.info(f"Creating professional placeholder: {prompt[:40]}...")
            
            # Create base with Egyptian gradient
            img = Image.new('RGB', (width, height), color='#1a1611')
            draw = ImageDraw.Draw(img)
            
            # Egyptian gradient background
            for y in range(height):
                ratio = y / height
                # Deep brown to golden sand gradient
                r = int(26 + ratio * 60)  # 26 -> 86
                g = int(22 + ratio * 40)  # 22 -> 62  
                b = int(17 + ratio * 20)  # 17 -> 37
                color = (r, g, b)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Ornate Egyptian border
            border_width = max(4, width // 80)
            gold_color = '#DAA520'
            
            # Outer border
            draw.rectangle([0, 0, width-1, height-1], outline=gold_color, width=border_width)
            
            # Inner decorative border  
            inner_margin = border_width * 3
            draw.rectangle([inner_margin, inner_margin, width-inner_margin-1, height-inner_margin-1], 
                          outline='#B8860B', width=2)
            
            # Egyptian decorative elements
            center_x, center_y = width // 2, height // 2
            
            # Draw ornate ankh symbol
            symbol_size = min(width, height) // 4
            ankh_color = '#FFD700'
            
            # Ankh oval (top)
            oval_top = center_y - symbol_size // 2
            oval_bottom = center_y - symbol_size // 6
            draw.ellipse([center_x - symbol_size//3, oval_top,
                         center_x + symbol_size//3, oval_bottom], 
                        outline=ankh_color, width=6)
            
            # Ankh vertical line
            draw.rectangle([center_x - symbol_size//12, oval_bottom,
                           center_x + symbol_size//12, center_y + symbol_size//2], 
                          fill=ankh_color)
            
            # Ankh horizontal line
            draw.rectangle([center_x - symbol_size//2, center_y - symbol_size//24,
                           center_x + symbol_size//2, center_y + symbol_size//24], 
                          fill=ankh_color)
            
            # Decorative hieroglyphs around the ankh
            self._draw_hieroglyph_decorations(draw, center_x, center_y, symbol_size, '#CD7F32')
            
            # Title text
            title_size = max(16, width // 40)
            try:
                title_font = ImageFont.truetype("arial.ttf", title_size)
            except:
                title_font = ImageFont.load_default()
            
            title_text = "SANDS OF DUAT"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            title_y = center_y - symbol_size - 40
            
            draw.text((title_x, title_y), title_text, fill='#F5E6A3', font=title_font)
            
            # Subtitle (prompt description)
            subtitle_size = max(12, width // 60)
            try:
                subtitle_font = ImageFont.truetype("arial.ttf", subtitle_size)
            except:
                subtitle_font = ImageFont.load_default()
            
            # Process prompt for display
            display_text = self._format_prompt_for_display(prompt)
            subtitle_bbox = draw.textbbox((0, 0), display_text, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = center_y + symbol_size + 30
            
            draw.text((subtitle_x, subtitle_y), display_text, fill='#DEB887', font=subtitle_font)
            
            # Save high-quality placeholder
            img.save(output_path, quality=95, optimize=True)
            self.logger.info(f"Professional placeholder created: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create placeholder: {e}")
            return False
    
    def _draw_hieroglyph_decorations(self, draw, center_x, center_y, size, color):
        """Draw decorative hieroglyph-style elements."""
        # Simple geometric patterns inspired by hieroglyphs
        offset = size // 2 + 20
        
        # Left side decorations
        draw.rectangle([center_x - offset - 10, center_y - 15, 
                       center_x - offset, center_y + 15], fill=color)
        draw.ellipse([center_x - offset - 20, center_y - 8,
                     center_x - offset - 5, center_y + 8], outline=color, width=2)
        
        # Right side decorations  
        draw.rectangle([center_x + offset, center_y - 15,
                       center_x + offset + 10, center_y + 15], fill=color)
        draw.ellipse([center_x + offset + 5, center_y - 8,
                     center_x + offset + 20, center_y + 8], outline=color, width=2)
    
    def _format_prompt_for_display(self, prompt: str) -> str:
        """Format prompt text for elegant display."""
        # Extract key terms from prompt
        key_terms = []
        if "card" in prompt.lower():
            key_terms.append("Card Art")
        if "character" in prompt.lower():
            key_terms.append("Character")
        if "environment" in prompt.lower():
            key_terms.append("Environment")
        if "ui" in prompt.lower():
            key_terms.append("UI Element")
        
        # Find Egyptian theme elements
        egyptian_terms = []
        terms_to_check = ["ankh", "anubis", "isis", "ra", "thoth", "pharaoh", "pyramid", "desert", "sand", "mummy"]
        for term in terms_to_check:
            if term in prompt.lower():
                egyptian_terms.append(term.title())
        
        # Combine for display
        if key_terms and egyptian_terms:
            return f"{' '.join(key_terms)} - {', '.join(egyptian_terms[:2])}"
        elif key_terms:
            return ' '.join(key_terms)
        else:
            # Fallback to truncated prompt
            return prompt[:30] + "..." if len(prompt) > 30 else prompt
    
    def generate_complete_card_set(self, output_dir: str) -> int:
        """Generate all cards with Hades-level artistic quality."""
        card_dir = Path(output_dir) / "cards"
        card_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_cards = len(self.prompts["cards"])
        
        self.logger.info(f"Generating {total_cards} Hades-style cards...")
        
        for i, (card_name, prompt) in enumerate(self.prompts["cards"].items()):
            output_path = str(card_dir / f"{card_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=512, height=768,  # Card aspect ratio
                steps=50 if self.high_quality else 20,
                cfg=7.5,
                seed=42 + i
            ):
                successful += 1
                self.logger.info(f"Card {i+1}/{total_cards} completed: {card_name}")
            
            # Small delay to prevent overheating
            time.sleep(0.5)
        
        self.logger.info(f"Card generation completed: {successful}/{total_cards}")
        return successful
    
    def generate_complete_character_set(self, output_dir: str) -> int:
        """Generate all characters with Hades-level detail."""
        char_dir = Path(output_dir) / "characters"
        char_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_chars = len(self.prompts["characters"])
        
        self.logger.info(f"Generating {total_chars} Hades-style characters...")
        
        for i, (char_name, prompt) in enumerate(self.prompts["characters"].items()):
            output_path = str(char_dir / f"{char_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=512, height=768,  # Character portrait
                steps=60 if self.high_quality else 25,
                cfg=8.0,
                seed=100 + i
            ):
                successful += 1
                self.logger.info(f"Character {i+1}/{total_chars} completed: {char_name}")
            
            time.sleep(0.5)
        
        self.logger.info(f"Character generation completed: {successful}/{total_chars}")
        return successful
    
    def generate_complete_environment_set(self, output_dir: str) -> int:
        """Generate all environments with cinematic quality."""
        env_dir = Path(output_dir) / "environments"
        env_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_envs = len(self.prompts["environments"])
        
        self.logger.info(f"Generating {total_envs} cinematic environments...")
        
        for i, (env_name, prompt) in enumerate(self.prompts["environments"].items()):
            output_path = str(env_dir / f"{env_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=1920, height=1080,  # HD background
                steps=70 if self.high_quality else 30,
                cfg=7.0,
                seed=200 + i
            ):
                successful += 1
                self.logger.info(f"Environment {i+1}/{total_envs} completed: {env_name}")
            
            time.sleep(0.5)
        
        self.logger.info(f"Environment generation completed: {successful}/{total_envs}")
        return successful


def main():
    parser = argparse.ArgumentParser(description="Hades-Style Art Generator for Sands of Duat")
    parser.add_argument("--model", default="sdxl", choices=["sdxl", "sdturbo"],
                       help="AI model for generation (sdxl for highest quality)")
    parser.add_argument("--prompt", help="Custom prompt to generate")
    parser.add_argument("--out", help="Output path")
    parser.add_argument("--generate-all", action="store_true", 
                       help="Generate complete professional asset set")
    parser.add_argument("--cards-only", action="store_true", help="Generate cards only")
    parser.add_argument("--characters-only", action="store_true", help="Generate characters only")
    parser.add_argument("--environments-only", action="store_true", help="Generate environments only") 
    parser.add_argument("--high-quality", action="store_true", default=True,
                       help="Use highest quality settings (default)")
    parser.add_argument("--fast", action="store_true", help="Use fast generation mode")
    
    args = parser.parse_args()
    
    # Initialize Hades-style generator
    generator = HadesStyleArtGenerator(
        model=args.model,
        high_quality=not args.fast
    )
    generator.load_pipeline()
    
    output_base = args.out or "game_assets"
    
    print("SANDS OF DUAT - Hades Style Art Generator")
    print("=" * 50)
    
    if args.generate_all:
        print("Generating complete professional asset set...")
        
        card_count = generator.generate_complete_card_set(output_base)
        char_count = generator.generate_complete_character_set(output_base)
        env_count = generator.generate_complete_environment_set(output_base)
        
        print(f"\nGeneration Complete:")
        print(f"  Cards: {card_count}/13")
        print(f"  Characters: {char_count}/5")
        print(f"  Environments: {env_count}/4")
        
    elif args.cards_only:
        card_count = generator.generate_complete_card_set(output_base)
        print(f"Generated {card_count} cards")
        
    elif args.characters_only:
        char_count = generator.generate_complete_character_set(output_base)
        print(f"Generated {char_count} characters")
        
    elif args.environments_only:
        env_count = generator.generate_complete_environment_set(output_base)
        print(f"Generated {env_count} environments")
        
    elif args.prompt and args.out:
        success = generator.generate_professional_image(args.prompt, args.out)
        if success:
            print(f"Successfully generated: {args.out}")
        else:
            print("Generation failed")
            sys.exit(1)
    else:
        print("Use --generate-all for complete set, or --prompt/--out for single image")
        sys.exit(1)


if __name__ == "__main__":
    main()