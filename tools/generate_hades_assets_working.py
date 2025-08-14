#!/usr/bin/env python3
"""
WORKING HADES-QUALITY ASSET GENERATOR
Fixed dimensions and optimized for RTX 5070
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
import os
from PIL import Image

class WorkingHadesAssetGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        
        # CORRECTED DIMENSIONS (divisible by 8)
        self.asset_specs = {
            "card_frames": {
                "common_frame": {
                    "size": (512, 768),  # Divisible by 8
                    "prompt": "ancient egyptian card frame, bronze borders, hieroglyphic patterns, weathered stone texture, game UI element, hades video game style, symmetrical, clean design, masterpiece, 8k",
                    "negative": "modern, plastic, cartoon, blurry, low quality, text, watermark"
                },
                "rare_frame": {
                    "size": (512, 768),
                    "prompt": "ancient egyptian card frame, silver borders with lapis lazuli accents, flowing hieroglyphic patterns, polished stone, game UI element, hades video game style, masterpiece, 8k",
                    "negative": "modern, plastic, cartoon, blurry, low quality, text, watermark"
                },
                "epic_frame": {
                    "size": (512, 768),  # Reduced from 1024x1536 to avoid memory issues
                    "prompt": "ancient egyptian card frame, golden borders with amethyst gems, intricate hieroglyphic carvings, divine aura, game UI element, hades video game style, epic quality, masterpiece, 8k",
                    "negative": "modern, plastic, cartoon, blurry, low quality, text, watermark"
                },
                "legendary_frame": {
                    "size": (512, 768),  # Reduced from 1024x1536
                    "prompt": "ancient egyptian card frame, divine golden borders, cosmic energy, celestial hieroglyphs, radiant divine power, game UI element, hades video game style, legendary quality, masterpiece, 8k",
                    "negative": "modern, plastic, cartoon, blurry, low quality, text, watermark"
                }
            },
            "ui_elements": {
                "ui_health_icon": {
                    "size": (512, 512),
                    "prompt": "egyptian ankh symbol, health icon, golden bronze metal, divine life symbol, game UI element, hades video game style, clean icon design, masterpiece, 8k",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text"
                },
                "ui_mana_icon": {
                    "size": (512, 512),
                    "prompt": "egyptian scarab beetle, mana energy icon, lapis lazuli blue gem, magical power symbol, game UI element, hades video game style, clean icon design, masterpiece, 8k",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text"
                },
                "ui_attack_icon": {
                    "size": (512, 512),
                    "prompt": "egyptian khopesh sword, attack icon, bronze weapon, warrior symbol, game UI element, hades video game style, clean icon design, masterpiece, 8k",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text"
                },
                "ui_shield_icon": {
                    "size": (512, 512),
                    "prompt": "egyptian shield with eye of horus, defense icon, golden protection symbol, divine guardian, game UI element, hades video game style, clean icon design, masterpiece, 8k",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text"
                }
            }
        }
        
        # Output directories
        self.output_dirs = {
            'card_frames': Path("../assets/approved_hades_quality/card_frame"),
            'ui_elements': Path("../assets/approved_hades_quality/ui_elements")
        }
        
        # Create directories
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def initialize_pipeline(self):
        """Initialize SDXL pipeline with RTX 5070 optimizations."""
        print("Initializing SDXL Pipeline for RTX 5070...")
        
        try:
            # Load SDXL with optimizations
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                use_safetensors=True
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # RTX 5070 optimizations
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
                self.pipe.enable_attention_slicing()
                try:
                    self.pipe.enable_xformers_memory_efficient_attention()
                except:
                    print("xformers not available, using default attention")
            
            print("SDXL Pipeline Ready!")
            return True
            
        except Exception as e:
            print(f"Pipeline initialization failed: {e}")
            return False

    def generate_asset(self, name, prompt, negative_prompt, size, category):
        """Generate single asset with SDXL."""
        output_path = self.output_dirs[category] / f"{name}.png"
        
        # Skip if already exists
        if output_path.exists():
            print(f"[SKIP] {name} already exists")
            return True
        
        print(f"[GENERATING] {name} ({size[0]}x{size[1]})...")
        
        try:
            # Generate with SDXL
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=size[0],
                height=size[1],
                num_inference_steps=25,  # Balanced quality/speed
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(42)
            ).images[0]
            
            # Save with high quality
            image.save(output_path, "PNG", optimize=True)
            print(f"[SUCCESS] Generated: {output_path}")
            
            # Clear VRAM
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to generate {name}: {e}")
            return False

    def generate_all_assets(self):
        """Generate all Hades-quality assets."""
        print("STARTING HADES-QUALITY ASSET GENERATION")
        print("=" * 50)
        
        # Check GPU
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory // 1024**3
            print(f"GPU: {gpu_name} ({memory_gb}GB VRAM)")
        
        # Initialize pipeline
        if not self.initialize_pipeline():
            print("FAILED: Could not initialize pipeline")
            return False
        
        success_count = 0
        total_count = 0
        
        # Generate card frames
        print("\nGENERATING CARD FRAMES...")
        for name, spec in self.asset_specs["card_frames"].items():
            total_count += 1
            if self.generate_asset(name, spec["prompt"], spec["negative"], spec["size"], "card_frames"):
                success_count += 1
            time.sleep(1)  # Small delay between generations
        
        # Generate UI elements
        print("\nGENERATING UI ELEMENTS...")
        for name, spec in self.asset_specs["ui_elements"].items():
            total_count += 1
            if self.generate_asset(name, spec["prompt"], spec["negative"], spec["size"], "ui_elements"):
                success_count += 1
            time.sleep(1)
        
        # Results
        print("\n" + "=" * 50)
        print(f"GENERATION COMPLETE: {success_count}/{total_count} successful")
        print("=" * 50)
        
        return success_count == total_count

def main():
    """Main generation process."""
    generator = WorkingHadesAssetGenerator()
    
    print("HADES-QUALITY ASSET GENERATION - RTX 5070 OPTIMIZED")
    print("=" * 60)
    
    success = generator.generate_all_assets()
    
    if success:
        print("\nSUCCESS: All assets generated successfully!")
        print("Ready for Hades-quality game experience!")
    else:
        print("\nWARNING: Some assets failed to generate")
    
    return success

if __name__ == "__main__":
    main()