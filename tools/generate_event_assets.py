#!/usr/bin/env python3
"""
EVENT ASSET GENERATOR - FLUX.1 DEV
Generate missing event illustrations using RTX 5070 Flux pipeline
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.ai_art.flux_generator import FluxHadesGenerator
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventAssetGenerator:
    """Generate divine event illustrations with Hades-level quality."""
    
    def __init__(self):
        self.generator = FluxHadesGenerator()
        self.output_dir = PROJECT_ROOT / "assets" / "approved_hades_quality" / "events"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Event specifications for generation
        self.event_specs = {
            "anubis_trial": {
                "prompt": """Anubis, ancient Egyptian god with jackal head, golden ceremonial collar, 
                divine judgment scene, scales of justice with glowing feather of Ma'at, 
                mystical underworld throne room, dramatic lighting, hades video game art style, 
                dark mysterious atmosphere, epic divine presence, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, bright colors, cheerful",
                "size": (1024, 768)
            },
            "isis_blessing": {
                "prompt": """Isis, ancient Egyptian goddess with wings of light, golden crown with solar disk, 
                divine blessing pose with outstretched arms, flowing magical energy, 
                sacred temple with hieroglyphic pillars, warm divine glow, hades video game art style, 
                protective motherly presence, mystical healing aura, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, dark, evil, scary",
                "size": (1024, 768)
            },
            "ra_divine_encounter": {
                "prompt": """Ra, sun god with falcon head, solar disk crown radiating golden light, 
                divine solar barque sailing through cosmic waters, celestial hieroglyphs floating in air, 
                majestic throne of pure sunlight, hades video game art style, 
                overwhelming divine power, golden hour lighting, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, dark, night",
                "size": (1024, 768)
            },
            "set_chaos_storm": {
                "prompt": """Set, god of chaos with mysterious animal head, red eyes glowing with power, 
                desert storm swirling around divine form, lightning crackling through sand, 
                ancient ruins being consumed by chaos, hades video game art style, 
                menacing presence, destructive energy, dramatic red lighting, masterpiece, 8k quality""",
                "negative": "modern, cartoon, blurry, low quality, text, watermark, peaceful, calm",
                "size": (1024, 768)
            }
        }
    
    def generate_all_events(self):
        """Generate all missing event assets."""
        logger.info("🎨 Starting Egyptian Divine Event Asset Generation")
        logger.info(f"📁 Output directory: {self.output_dir}")
        
        # Load the Flux model
        if not self.generator.load_model():
            logger.error("❌ Failed to load Flux model!")
            return False
        
        success_count = 0
        total_count = len(self.event_specs)
        
        for event_name, spec in self.event_specs.items():
            logger.info(f"\n🏺 Generating: {event_name}")
            
            output_path = self.output_dir / f"{event_name}.png"
            
            # Skip if already exists
            if output_path.exists():
                logger.info(f"✅ {event_name} already exists, skipping...")
                success_count += 1
                continue
            
            # Generate the image
            start_time = time.time()
            
            try:
                image = self.generator.generate_image(
                    prompt=spec["prompt"],
                    negative_prompt=spec["negative"],
                    width=spec["size"][0],
                    height=spec["size"][1],
                    num_inference_steps=25,  # High quality
                    guidance_scale=3.5
                )
                
                if image:
                    # Save the image
                    image.save(output_path, "PNG", quality=95)
                    
                    generation_time = time.time() - start_time
                    file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                    
                    logger.info(f"✅ Generated {event_name}:")
                    logger.info(f"   📄 File: {output_path.name}")
                    logger.info(f"   📐 Size: {spec['size'][0]}x{spec['size'][1]}")
                    logger.info(f"   💾 File size: {file_size:.1f} MB")
                    logger.info(f"   ⏱️  Time: {generation_time:.1f}s")
                    
                    success_count += 1
                else:
                    logger.error(f"❌ Failed to generate {event_name}")
                    
            except Exception as e:
                logger.error(f"❌ Error generating {event_name}: {e}")
        
        # Summary
        logger.info(f"\n🎯 Generation Complete!")
        logger.info(f"✅ Success: {success_count}/{total_count} events")
        logger.info(f"📁 Assets saved to: {self.output_dir}")
        
        return success_count == total_count

def main():
    """Main generation function."""
    generator = EventAssetGenerator()
    
    logger.info("🏺 SANDS OF DUAT - EVENT ASSET GENERATOR")
    logger.info("⚡ RTX 5070 Flux.1 Dev Pipeline")
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