#!/usr/bin/env python3
"""
EVENT ASSET GENERATOR - STABLE DIFFUSION XL
Generate missing event illustrations using RTX 5070 SDXL pipeline
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
import os
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SDXLEventGenerator:
    """Generate divine event illustrations with Hades-level quality using SDXL."""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        
        # Project paths
        PROJECT_ROOT = Path(__file__).parent.parent
        self.output_dir = PROJECT_ROOT / "assets" / "approved_hades_quality" / "events"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Event specifications for generation
        self.event_specs = {
            "anubis_trial": {
                "prompt": """Anubis ancient Egyptian god with jackal head, golden ceremonial collar, 
                divine judgment scene, scales of justice with glowing feather of Ma'at, 
                mystical underworld throne room, dramatic lighting, hades video game art style, 
                dark mysterious atmosphere, epic divine presence, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, bright colors, cheerful",
                "size": (1024, 768)
            },
            "isis_blessing": {
                "prompt": """Isis ancient Egyptian goddess with wings of light, golden crown with solar disk, 
                divine blessing pose with outstretched arms, flowing magical energy, 
                sacred temple with hieroglyphic pillars, warm divine glow, hades video game art style, 
                protective motherly presence, mystical healing aura, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, dark, evil, scary",
                "size": (1024, 768)
            }
        }
    
    def load_model(self):
        """Load SDXL model optimized for RTX 5070."""
        logger.info("Loading Stable Diffusion XL model...")
        
        try:
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16"
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # RTX 5070 optimizations
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_slicing()
            
            logger.info("✅ SDXL model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load SDXL model: {e}")
            return False
    
    def generate_event_image(self, event_name: str, spec: dict):
        """Generate a single event image."""
        logger.info(f"🎨 Generating: {event_name}")
        
        output_path = self.output_dir / f"{event_name}.png"
        
        # Skip if already exists
        if output_path.exists():
            logger.info(f"✅ {event_name} already exists, skipping...")
            return True
        
        try:
            start_time = time.time()
            
            # Generate with RTX 5070 optimized settings
            image = self.pipe(
                prompt=spec["prompt"],
                negative_prompt=spec["negative"],
                width=spec["size"][0],
                height=spec["size"][1],
                num_inference_steps=25,  # Good quality/speed balance
                guidance_scale=7.5,     # Standard guidance
                num_images_per_prompt=1
            ).images[0]
            
            # Save the image
            image.save(output_path, "PNG", quality=95)
            
            generation_time = time.time() - start_time
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            
            logger.info(f"✅ Generated {event_name}:")
            logger.info(f"   📄 File: {output_path.name}")
            logger.info(f"   📐 Size: {spec['size'][0]}x{spec['size'][1]}")
            logger.info(f"   💾 File size: {file_size:.1f} MB")
            logger.info(f"   ⏱️  Time: {generation_time:.1f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error generating {event_name}: {e}")
            return False
    
    def generate_all_events(self):
        """Generate all missing event assets."""
        logger.info("🎨 Starting Egyptian Divine Event Asset Generation")
        logger.info(f"📁 Output directory: {self.output_dir}")
        
        # Load the SDXL model
        if not self.load_model():
            return False
        
        success_count = 0
        total_count = len(self.event_specs)
        
        for event_name, spec in self.event_specs.items():
            if self.generate_event_image(event_name, spec):
                success_count += 1
        
        # Summary
        logger.info(f"\n🎯 Generation Complete!")
        logger.info(f"✅ Success: {success_count}/{total_count} events")
        logger.info(f"📁 Assets saved to: {self.output_dir}")
        
        return success_count == total_count

def main():
    """Main generation function."""
    generator = SDXLEventGenerator()
    
    logger.info("🏺 SANDS OF DUAT - EVENT ASSET GENERATOR")
    logger.info("⚡ RTX 5070 Stable Diffusion XL Pipeline")
    logger.info("🎨 Hades-Quality Egyptian Divine Events")
    
    success = generator.generate_all_events()
    
    if success:
        logger.info("\n🎉 All event assets generated successfully!")
        logger.info("🎮 Ready for divine Egyptian storytelling!")
    else:
        logger.warning("\n⚠️ Some assets failed to generate")
        logger.info("🔧 Check logs and try again")

if __name__ == "__main__":
    main()