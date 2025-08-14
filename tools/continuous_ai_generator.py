#!/usr/bin/env python3
"""
CONTINUOUS AI ASSET GENERATOR - RTX 5070 MAXIMUM POWER
"""

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from pathlib import Path
import time
import os
from PIL import Image
import gc

class ContinuousAIGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        
        # MAXIMUM QUALITY SETTINGS
        self.settings = {
            "steps": 50,
            "guidance_scale": 8.5,
            "use_karras": True,
        }
        
        # ASSETS TO GENERATE
        self.queue = {
            "ui_mana_icon": {
                "size": (1024, 1024),
                "category": "ui_elements",
                "prompt": "ancient egyptian scarab beetle, mana energy crystal, lapis lazuli blue, mystical power symbol, game UI, hades style, ultra detailed, 8k masterpiece, golden accents, divine energy, ornate hieroglyphs",
                "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple, people"
            },
            "ui_attack_icon": {
                "size": (1024, 1024), 
                "category": "ui_elements",
                "prompt": "ancient egyptian khopesh sword, bronze weapon, hieroglyphic engravings, warrior symbol, game UI, hades style, ultra detailed, 8k masterpiece, battle worn, divine metal, ornate details",
                "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple, people"
            },
            "ui_shield_icon": {
                "size": (1024, 1024),
                "category": "ui_elements", 
                "prompt": "ancient egyptian shield with eye of horus, golden protection symbol, divine guardian, ornate details, game UI, hades style, ultra detailed, 8k masterpiece, sacred geometry, mystical",
                "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple, people"
            },
            "bg_main_menu_ai": {
                "size": (3440, 1440),
                "category": "backgrounds",
                "prompt": "ancient egyptian temple interior, massive stone columns with hieroglyphs, golden light streaming through openings, hades video game style, cinematic lighting, ultra detailed, 8k masterpiece, atmospheric, mysterious, divine architecture",
                "negative": "modern, people, cartoon, low quality, blurry, text, watermark, bright, simple, crowded"
            },
            "bg_combat_ai": {
                "size": (3440, 1440),
                "category": "backgrounds", 
                "prompt": "ancient egyptian underworld battlefield, mystical energy, floating hieroglyphs, dark atmosphere, hades video game style, cinematic lighting, ultra detailed, 8k masterpiece, epic, divine power, magical aura",
                "negative": "modern, people, cartoon, low quality, blurry, text, watermark, bright, simple, crowded"
            }
        }
        
        # Directories
        self.output_dirs = {
            'ui_elements': Path("../assets/approved_hades_quality/ui_elements"),
            'backgrounds': Path("../assets/approved_hades_quality/backgrounds")
        }
        
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def initialize_pipeline(self):
        """Initialize SDXL with maximum quality."""
        print("INITIALIZING SDXL MAXIMUM QUALITY PIPELINE...")
        
        try:
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                variant="fp16", 
                use_safetensors=True
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # Use Karras scheduler for better quality
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config,
                use_karras_sigmas=self.settings["use_karras"]
            )
            
            print("SDXL Pipeline Ready for Maximum Quality Generation!")
            return True
            
        except Exception as e:
            print(f"Pipeline initialization failed: {e}")
            return False

    def generate_asset(self, name, spec):
        """Generate single asset with maximum quality."""
        output_path = self.output_dirs[spec["category"]] / f"{name}.png"
        
        # Skip if exists
        if output_path.exists():
            print(f"[SKIP] {name} already exists")
            return True
        
        print(f"[GENERATING] {name} ({spec['size'][0]}x{spec['size'][1]})...")
        
        try:
            # VRAM monitoring
            if self.device == "cuda":
                vram_used = torch.cuda.memory_allocated() / 1024**3
                vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"VRAM: {vram_used:.1f}/{vram_total:.1f}GB ({vram_used/vram_total*100:.1f}%)")
            
            # Generate with maximum quality
            image = self.pipe(
                prompt=spec["prompt"],
                negative_prompt=spec["negative"],
                width=spec["size"][0],
                height=spec["size"][1],
                num_inference_steps=self.settings["steps"],
                guidance_scale=self.settings["guidance_scale"],
                generator=torch.Generator(device=self.device).manual_seed(42)
            ).images[0]
            
            # Save with high quality
            image.save(output_path, "PNG", optimize=True, compress_level=1)
            
            # Verify generation
            file_size = output_path.stat().st_size / 1024**2
            print(f"[SUCCESS] {name} generated ({file_size:.1f}MB)")
            
            # Cleanup
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to generate {name}: {e}")
            if self.device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()
            return False

    def run_continuous_generation(self):
        """Run continuous asset generation."""
        print("RTX 5070 MAXIMUM QUALITY CONTINUOUS GENERATION")
        print("=" * 60)
        
        # GPU Info
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory // 1024**3
            print(f"GPU: {gpu_name} ({memory_gb}GB VRAM)")
        
        # Initialize
        if not self.initialize_pipeline():
            return False
        
        # Generate all assets
        success_count = 0
        total_count = len(self.queue)
        
        for name, spec in self.queue.items():
            if self.generate_asset(name, spec):
                success_count += 1
            time.sleep(1)  # Small delay between generations
        
        print(f"\nGENERATION COMPLETE: {success_count}/{total_count} successful")
        return success_count == total_count

def main():
    generator = ContinuousAIGenerator()
    generator.run_continuous_generation()

if __name__ == "__main__":
    main()