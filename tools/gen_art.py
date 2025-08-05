#!/usr/bin/env python3
"""
Advanced Art Generation Tool for Sands of Duat
Generates high-quality art assets using SDTurbo and Stable Diffusion models.
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
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install torch diffusers pillow numpy")
    # Fallback to placeholder generation
    from PIL import Image, ImageDraw, ImageFont
    DIFFUSERS_AVAILABLE = False
else:
    DIFFUSERS_AVAILABLE = True


class ArtGenerator:
    """Advanced art generation system for Sands of Duat."""
    
    def __init__(self, model: str = "sdturbo", device: str = "auto", medvram: bool = False):
        self.model = model
        self.medvram = medvram
        self.pipeline = None
        
        # Setup logging first
        self.logger = self._setup_logging()
        
        # Then setup device
        self.device = self._setup_device(device)
        
        # Egyptian-themed prompts for different asset types
        self.prompts = {
            "character": {
                "player": "Egyptian warrior hero, cel-shaded art style, detailed character design, golden armor, confident pose, desert background, concept art, high quality",
                "desert_scorpion": "Giant desert scorpion, Egyptian mythology creature, detailed exoskeleton, menacing claws, desert environment, concept art style",
                "anubis_guardian": "Anubis guardian warrior, jackal head, Egyptian armor, ceremonial staff, temple setting, detailed character art",
                "temple_guardian": "Egyptian temple guardian statue, stone construct, hieroglyphic details, ancient magic glow, imposing presence",
                "pharaoh_lich": "Undead pharaoh, mummified king, golden death mask, ancient Egyptian royal regalia, dark magic aura, final boss design"
            },
            "cards": {
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
            },
            "environments": {
                "desert_outskirts": "Egyptian desert landscape, sand dunes, ancient ruins in distance, atmospheric lighting",
                "temple_entrance": "Ancient Egyptian temple entrance, massive stone columns, hieroglyphic carvings, mysterious atmosphere",
                "inner_sanctum": "Sacred Egyptian temple interior, golden treasures, magical lighting, pharaoh's chamber"
            }
        }
        
        self.negative_prompt = "blurry, low quality, distorted, watermark, signature, text, bad anatomy, deformed, ugly, cartoon, anime"
        
    def _setup_device(self, device: str) -> str:
        """Setup compute device with RTX 5070 optimization."""
        if not DIFFUSERS_AVAILABLE:
            return "cpu"
            
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                # RTX 5070 optimizations
                torch.backends.cudnn.benchmark = True
                torch.backends.cuda.enable_flash_sdp(True)
            else:
                device = "cpu"
                self.logger.warning("CUDA not available, falling back to CPU")
        
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
                logging.FileHandler(log_dir / "gen_art.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def load_pipeline(self):
        """Load the specified diffusion pipeline."""
        if not DIFFUSERS_AVAILABLE:
            self.logger.warning("Diffusers not available, using placeholder generation")
            return
            
        self.logger.info(f"Loading {self.model} pipeline...")
        
        model_configs = {
            "sdturbo": {
                "model_id": "stabilityai/sd-turbo",
                "pipeline": StableDiffusionPipeline
            },
            "sdxl": {
                "model_id": "stabilityai/stable-diffusion-xl-base-1.0", 
                "pipeline": DiffusionPipeline
            }
        }
        
        if self.model not in model_configs:
            raise ValueError(f"Unknown model: {self.model}")
        
        config = model_configs[self.model]
        
        kwargs = {
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            "use_safetensors": True,
            "variant": "fp16" if self.device == "cuda" else None
        }
        
        if self.medvram:
            kwargs["low_cpu_mem_usage"] = True
        
        try:
            self.pipeline = config["pipeline"].from_pretrained(
                config["model_id"], **kwargs
            ).to(self.device)
            
            if self.medvram and self.device == "cuda":
                self.pipeline.enable_model_cpu_offload()
                self.pipeline.enable_vae_slicing()
                self.pipeline.enable_attention_slicing("max")
            
            self.logger.info(f"{self.model} pipeline loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load pipeline: {e}")
            self.logger.info("Falling back to placeholder generation")
            self.pipeline = None
    
    def generate_image(self, prompt: str, output_path: str, 
                      steps: int = 8, cfg: float = 3.5, 
                      width: int = 512, height: int = 512,
                      seed: Optional[int] = None) -> bool:
        """Generate a single image."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.pipeline:
                # Fallback to placeholder
                return self._generate_placeholder(prompt, output_path, width, height)
            
            self.logger.info(f"Generating: {prompt[:50]}...")
            
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            start_time = time.time()
            
            # Generate image
            if self.model == "sdturbo":
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=self.negative_prompt,
                    num_inference_steps=steps,
                    guidance_scale=cfg,
                    width=width,
                    height=height,
                    generator=generator
                )
            else:  # SDXL
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=self.negative_prompt,
                    num_inference_steps=steps,
                    guidance_scale=cfg,
                    width=width,
                    height=height,
                    generator=generator
                )
            
            # Save image
            image = result.images[0]
            image.save(output_path, quality=95)
            
            generation_time = time.time() - start_time
            self.logger.info(f"Generated in {generation_time:.2f}s: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate image: {e}")
            return self._generate_placeholder(prompt, output_path, width, height)
    
    def generate_batch(self, prompts: List[str], output_dir: str, 
                      batch_size: int = 6, **kwargs) -> int:
        """Generate multiple images in batch."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        successful = 0
        
        self.logger.info(f"Starting batch generation: {len(prompts)} images")
        
        for i, prompt in enumerate(prompts):
            output_path = str(Path(output_dir) / f"image_{i:03d}.png")
            
            # Add some randomness to seeds
            seed = kwargs.get('seed', 42) + i if 'seed' in kwargs else None
            kwargs_with_seed = {**kwargs, 'seed': seed}
            
            if self.generate_image(prompt, output_path, **kwargs_with_seed):
                successful += 1
        
        self.logger.info(f"Batch generation completed: {successful}/{len(prompts)} successful")
        return successful
    
    def _generate_placeholder(self, prompt: str, output_path: str, 
                            width: int = 512, height: int = 512) -> bool:
        """Generate placeholder image when AI generation fails."""
        try:
            self.logger.info(f"Generating placeholder for: {prompt[:30]}...")
            
            # Create base image
            img = Image.new('RGB', (width, height), color='#2C1810')
            draw = ImageDraw.Draw(img)
            
            # Draw gradient background
            for y in range(height):
                ratio = y / height
                r = int(44 + ratio * 50)
                g = int(24 + ratio * 30) 
                b = int(16 + ratio * 20)
                color = (r, g, b)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Draw Egyptian-style border
            border_color = '#D4AF37'
            border_width = max(2, width // 100)
            draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                          outline=border_color, width=border_width)
            
            # Add decorative elements
            center_x, center_y = width // 2, height // 2
            
            # Draw simplified ankh or Egyptian symbol
            symbol_color = '#8B7355'
            symbol_size = min(width, height) // 6
            
            # Ankh symbol
            draw.ellipse([center_x - symbol_size//2, center_y - symbol_size, 
                         center_x + symbol_size//2, center_y - symbol_size//3], 
                        outline=symbol_color, width=3)
            draw.rectangle([center_x - symbol_size//6, center_y - symbol_size//3,
                           center_x + symbol_size//6, center_y + symbol_size//2], 
                          fill=symbol_color)
            draw.rectangle([center_x - symbol_size//3, center_y - symbol_size//6,
                           center_x + symbol_size//3, center_y + symbol_size//6], 
                          fill=symbol_color)
            
            # Add prompt text (truncated)
            try:
                font_size = max(12, width // 30)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text_color = '#F5E6A3'
            prompt_text = prompt[:40] + "..." if len(prompt) > 40 else prompt
            
            # Get text size and center it
            text_bbox = draw.textbbox((0, 0), prompt_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = center_y + symbol_size + 20
            
            draw.text((text_x, text_y), prompt_text, fill=text_color, font=font)
            
            # Save placeholder
            img.save(output_path, quality=95)
            self.logger.info(f"Generated placeholder: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate placeholder: {e}")
            return False
    
    def generate_character_set(self, output_dir: str) -> int:
        """Generate complete character set for Sands of Duat."""
        characters = list(self.prompts["character"].keys())
        character_prompts = [self.prompts["character"][char] for char in characters]
        
        char_dir = Path(output_dir) / "characters"
        return self.generate_batch(character_prompts, str(char_dir))
    
    def generate_card_set(self, output_dir: str) -> int:
        """Generate complete card art set."""
        cards = list(self.prompts["cards"].keys())
        card_prompts = [self.prompts["cards"][card] for card in cards]
        
        card_dir = Path(output_dir) / "cards"
        return self.generate_batch(card_prompts, str(card_dir), width=400, height=600)
    
    def generate_environment_set(self, output_dir: str) -> int:
        """Generate environment backgrounds."""
        environments = list(self.prompts["environments"].keys())
        env_prompts = [self.prompts["environments"][env] for env in environments]
        
        env_dir = Path(output_dir) / "environments"
        return self.generate_batch(env_prompts, str(env_dir), width=1024, height=768)


def main():
    parser = argparse.ArgumentParser(description="Art Generator for Sands of Duat")
    parser.add_argument("--model", default="sdturbo", choices=["sdturbo", "sdxl"],
                       help="Model to use for generation")
    parser.add_argument("--prompt", help="Single prompt to generate")
    parser.add_argument("--out", help="Output path/directory")
    parser.add_argument("--steps", type=int, default=8, help="Number of inference steps")
    parser.add_argument("--cfg", type=float, default=3.5, help="Guidance scale")
    parser.add_argument("--batch", type=int, default=6, help="Batch size for generation")
    parser.add_argument("--width", type=int, default=512, help="Image width")
    parser.add_argument("--height", type=int, default=512, help="Image height")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--medvram", action="store_true", help="Enable memory efficient mode")
    parser.add_argument("--generate-all", action="store_true", help="Generate all game assets")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = ArtGenerator(model=args.model, medvram=args.medvram)
    generator.load_pipeline()
    
    if args.generate_all:
        # Generate complete asset set
        output_base = args.out or "art_raw"
        print("Generating complete Sands of Duat asset set...")
        
        char_count = generator.generate_character_set(output_base)
        card_count = generator.generate_card_set(output_base) 
        env_count = generator.generate_environment_set(output_base)
        
        print(f"Generation complete:")
        print(f"  Characters: {char_count}")
        print(f"  Cards: {card_count}")
        print(f"  Environments: {env_count}")
        
    elif args.prompt and args.out:
        # Single image generation
        success = generator.generate_image(
            args.prompt, args.out,
            steps=args.steps, cfg=args.cfg,
            width=args.width, height=args.height,
            seed=args.seed
        )
        
        if success:
            print(f"Successfully generated: {args.out}")
        else:
            print("Generation failed")
            sys.exit(1)
    else:
        print("Use --prompt and --out for single image, or --generate-all for complete set")
        sys.exit(1)


if __name__ == "__main__":
    main()