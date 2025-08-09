#!/usr/bin/env python3
"""
SELECTIVE ASSET REGENERATOR
==========================

Regenerate specific problematic assets with improved prompts.
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import json
import time

class SelectiveRegenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = Path("../assets/generated_art_lora")
        
        # Load regeneration specifications
        self.specs_file = Path("../assets/regeneration_specs.json")
        
    def setup_pipeline(self):
        """Setup SDXL pipeline."""
        print("Setting up SDXL pipeline for selective regeneration...")
        
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            variant="fp16" if self.device == "cuda" else None,
            use_safetensors=True
        ).to(self.device)
        
        self.pipe.enable_model_cpu_offload()
        print("Pipeline ready!")
    
    def load_regeneration_specs(self):
        """Load assets that need regeneration."""
        if not self.specs_file.exists():
            print(f"No regeneration specs found at {self.specs_file}")
            return []
            
        with open(self.specs_file, 'r') as f:
            specs = json.load(f)
            
        print(f"Found {len(specs)} assets to regenerate")
        return specs
    
    def regenerate_asset(self, spec):
        """Regenerate a single asset with improved prompt."""
        print(f"Regenerating {spec['name']}...")
        
        # Create backup of original
        original_path = self.output_dir / spec['category'] / f"{spec['name']}.png"
        backup_path = original_path.with_suffix('.png.backup')
        
        if original_path.exists():
            original_path.rename(backup_path)
            print(f"  Original backed up to {backup_path}")
        
        try:
            # Generate with improved prompt
            image = self.pipe(
                prompt=spec['improved_prompt'],
                negative_prompt="low quality, blurry, text, watermark, amateur, multiple characters, crowd, group",
                width=spec['resolution']['width'],
                height=spec['resolution']['height'],
                num_inference_steps=30,
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(12345)  # Fixed seed for consistency
            ).images[0]
            
            # Save regenerated asset
            image.save(original_path, "PNG", optimize=True)
            print(f"  Successfully regenerated: {original_path}")
            
            time.sleep(2)  # Prevent overheating
            
        except Exception as e:
            print(f"  Error regenerating {spec['name']}: {e}")
            # Restore backup
            if backup_path.exists():
                backup_path.rename(original_path)
                print(f"  Restored original from backup")
    
    def run_regeneration(self):
        """Execute selective regeneration."""
        print("=" * 60)
        print("SELECTIVE ASSET REGENERATION")
        print("Fixing problematic assets with improved prompts")
        print("=" * 60)
        
        # Setup pipeline
        self.setup_pipeline()
        
        # Load specifications
        specs = self.load_regeneration_specs()
        if not specs:
            return
        
        # Regenerate each problematic asset
        for spec in specs:
            self.regenerate_asset(spec)
        
        print("=" * 60)
        print("SELECTIVE REGENERATION COMPLETE!")
        print("Fixed problematic assets with improved prompts")
        print("Ready for quality validation")
        print("=" * 60)

def main():
    regenerator = SelectiveRegenerator()
    regenerator.run_regeneration()

if __name__ == "__main__":
    main()