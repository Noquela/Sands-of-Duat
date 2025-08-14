#!/usr/bin/env python3
"""
MAXIMUM GPU UTILIZATION - RTX 5070 BEAST MODE
NO LIMITS - FULL VRAM + BATCH PROCESSING
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
import os
from PIL import Image
import gc

class MaxGPUAssetGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        
        # RTX 5070 BEAST MODE SETTINGS
        self.max_settings = {
            "batch_size": 2,  # Generate 2 at once
            "steps": 40,      # High quality
            "guidance_scale": 9.0,  # Strong guidance
            "resolution": 1024,  # Higher resolution
            "use_karras": True,
            "enable_attention_slicing": False,  # Use more VRAM for speed
            "enable_cpu_offload": False,  # Keep everything on GPU
        }
        
        # HIGH RESOLUTION ASSETS  
        self.assets_to_generate = {
            "ui_elements": {
                "ui_mana_icon": {
                    "size": (1024, 1024),  # High res
                    "prompt": "ancient egyptian scarab beetle, mana energy crystal, lapis lazuli blue, mystical power symbol, game UI, hades style, ultra detailed, 8k masterpiece, golden accents, divine energy",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple"
                },
                "ui_attack_icon": {
                    "size": (1024, 1024),
                    "prompt": "ancient egyptian khopesh sword, bronze weapon, hieroglyphic engravings, warrior symbol, game UI, hades style, ultra detailed, 8k masterpiece, battle worn, divine metal",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple"
                },
                "ui_shield_icon": {
                    "size": (1024, 1024),
                    "prompt": "ancient egyptian shield with eye of horus, golden protection symbol, divine guardian, ornate details, game UI, hades style, ultra detailed, 8k masterpiece, sacred geometry",
                    "negative": "background, modern, plastic, cartoon, blurry, low quality, text, watermark, simple"
                }
            },
            "backgrounds": {
                "bg_main_menu_4k_ai": {
                    "size": (3440, 1440),  # Ultrawide 4K
                    "prompt": "ancient egyptian temple interior, massive stone columns with hieroglyphs, golden light streaming through openings, hades video game style, cinematic lighting, ultra detailed, 8k masterpiece, atmospheric, mysterious",
                    "negative": "modern, people, cartoon, low quality, blurry, text, watermark, bright, simple"
                },
                "bg_combat_4k_ai": {
                    "size": (3440, 1440),
                    "prompt": "ancient egyptian underworld battlefield, mystical energy, floating hieroglyphs, dark atmosphere, hades video game style, cinematic lighting, ultra detailed, 8k masterpiece, epic, divine power",
                    "negative": "modern, people, cartoon, low quality, blurry, text, watermark, bright, simple"
                }
            }
        }
        
        # Output directories
        self.output_dirs = {
            'ui_elements': Path("../assets/approved_hades_quality/ui_elements"),
            'backgrounds': Path("../assets/approved_hades_quality/backgrounds")
        }
        
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def initialize_beast_mode_pipeline(self):
        """Initialize SDXL with MAXIMUM GPU utilization."""
        print("🔥 INITIALIZING RTX 5070 BEAST MODE...")
        
        try:
            # Load with maximum settings
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # BEAST MODE - NO CPU OFFLOADING
            if not self.max_settings["enable_cpu_offload"]:
                print("🚀 BEAST MODE: Keeping everything on GPU for maximum speed")
            else:
                self.pipe.enable_model_cpu_offload()
            
            # Attention settings for max performance
            if not self.max_settings["enable_attention_slicing"]:
                print("🚀 BEAST MODE: Using full attention for maximum quality")
            else:
                self.pipe.enable_attention_slicing()
            
            # Enable scheduler optimizations
            from diffusers import DPMSolverMultistepScheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config,
                use_karras_sigmas=self.max_settings["use_karras"]
            )
            
            print("⚡ RTX 5070 BEAST MODE ACTIVATED!")
            return True
            
        except Exception as e:
            print(f"❌ Beast mode failed: {e}")
            return False

    def generate_high_res_asset(self, name, prompt, negative_prompt, size, category):
        """Generate single high-resolution asset with beast mode."""
        output_path = self.output_dirs[category] / f"{name}.png"
        
        print(f"🎨 GENERATING BEAST MODE: {name} ({size[0]}x{size[1]})...")
        
        try:
            # Check VRAM before generation
            if self.device == "cuda":
                vram_used = torch.cuda.memory_allocated() / 1024**3
                vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"⚡ VRAM: {vram_used:.1f}/{vram_total:.1f}GB ({vram_used/vram_total*100:.1f}%)")
            
            # BEAST MODE GENERATION
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=size[0],
                height=size[1],
                num_inference_steps=self.max_settings["steps"],
                guidance_scale=self.max_settings["guidance_scale"],
                generator=torch.Generator(device=self.device).manual_seed(42)
            ).images[0]
            
            # Save with maximum quality
            image.save(output_path, "PNG", optimize=True, compress_level=1)
            
            # Check file size
            file_size = output_path.stat().st_size / 1024**2
            print(f"✨ BEAST MODE SUCCESS: {output_path} ({file_size:.1f}MB)")
            
            return True
            
        except Exception as e:
            print(f"❌ BEAST MODE ERROR {name}: {e}")
            # Force cleanup on error
            if self.device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()
            return False

    def run_beast_mode_generation(self):
        """Run continuous beast mode generation."""
        print("🔥🔥🔥 RTX 5070 BEAST MODE CONTINUOUS GENERATION 🔥🔥🔥")
        print("=" * 60)
        
        # GPU Info
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory // 1024**3
            print(f"🚀 GPU: {gpu_name} ({memory_gb}GB VRAM)")
        
        # Initialize beast mode
        if not self.initialize_beast_mode_pipeline():
            print("❌ BEAST MODE INITIALIZATION FAILED")
            return False
        
        total_generated = 0
        
        # Generate UI elements with beast mode
        print("\n🎨 BEAST MODE UI ELEMENTS...")
        for name, spec in self.assets_to_generate["ui_elements"].items():
            if self.generate_high_res_asset(name, spec["prompt"], spec["negative"], spec["size"], "ui_elements"):
                total_generated += 1
        
        # Generate backgrounds with beast mode  
        print("\n🎨 BEAST MODE BACKGROUNDS...")
        for name, spec in self.assets_to_generate["backgrounds"].items():
            if self.generate_high_res_asset(name, spec["prompt"], spec["negative"], spec["size"], "backgrounds"):
                total_generated += 1
        
        print(f"\n🔥 BEAST MODE COMPLETE: {total_generated} assets generated!")
        return True

def main():
    generator = MaxGPUAssetGenerator()
    generator.run_beast_mode_generation()

if __name__ == "__main__":
    main()