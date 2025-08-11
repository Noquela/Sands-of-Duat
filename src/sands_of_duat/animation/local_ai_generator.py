"""
Local AI Animation Generator
Uses local Stable Diffusion + AnimateDiff to generate Egyptian card animations
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import time

try:
    import torch
    from diffusers import StableDiffusionPipeline, AnimateDiffPipeline, MotionAdapter
    from diffusers.utils import export_to_gif
    AI_LIBS_AVAILABLE = True
except ImportError:
    AI_LIBS_AVAILABLE = False

class LocalAIGenerator:
    """Generates Egyptian card animations using local AI models."""
    
    def __init__(self):
        self.logger = logging.getLogger("local_ai_generator")
        self.models_dir = Path("models/ai")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = Path("assets/animations/ai_generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check GPU availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Using device: {self.device}")
        
        # Model configurations
        self.sd_model_id = "runwayml/stable-diffusion-v1-5"
        self.animatediff_adapter = "guoyww/animatediff-motion-adapter-v1-5-2"
        
        # Initialize pipelines
        self.sd_pipeline = None
        self.animatediff_pipeline = None
        self.initialized = False
        
    async def initialize(self) -> bool:
        """Initialize AI models for generation."""
        if not AI_LIBS_AVAILABLE:
            self.logger.error("AI libraries not available - install diffusers and torch")
            return False
            
        try:
            self.logger.info("Initializing AI models for local generation...")
            
            # Initialize Stable Diffusion pipeline
            self.logger.info("Loading Stable Diffusion model...")
            self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
                self.sd_model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            self.sd_pipeline = self.sd_pipeline.to(self.device)
            
            # Initialize AnimateDiff pipeline
            self.logger.info("Loading AnimateDiff model...")
            adapter = MotionAdapter.from_pretrained(self.animatediff_adapter, torch_dtype=torch.float16)
            self.animatediff_pipeline = AnimateDiffPipeline.from_pretrained(
                self.sd_model_id,
                motion_adapter=adapter,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            self.animatediff_pipeline = self.animatediff_pipeline.to(self.device)
            self.animatediff_pipeline.enable_vae_slicing()
            
            self.initialized = True
            self.logger.info("AI models initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            return False
    
    def get_egyptian_card_prompts(self) -> Dict[str, Dict]:
        """Get prompts for Egyptian card generation."""
        return {
            "ra_solar_deity": {
                "prompt": "ancient egyptian god Ra, falcon head with solar disk crown, golden divine radiance, hieroglyphs floating around, papyrus scroll background, cinematic lighting, highly detailed, 4k, trending on artstation",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark, signature",
                "animation_prompt": "gentle floating motion, divine energy pulsing, hieroglyphs slowly rotating, solar rays flickering"
            },
            "anubis_judge_of_the_dead": {
                "prompt": "ancient egyptian god Anubis, black jackal head, golden collar, scales of justice, underworld atmosphere, purple mystical energy, ancient temple background, dramatic lighting, highly detailed, 4k",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark",
                "animation_prompt": "mysterious mist swirling, purple energy flowing, scales gently swaying, shadows dancing"
            },
            "isis_mother_goddess": {
                "prompt": "ancient egyptian goddess Isis, beautiful woman with isis crown, protective wings spread, ankh symbol glowing, healing blue aura, temple of isis background, soft divine lighting, highly detailed, 4k",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark",
                "animation_prompt": "wings gently flapping, healing aura pulsing, ankh symbol glowing rhythmically"
            },
            "set_chaos_lord": {
                "prompt": "ancient egyptian god Set, red eyes, desert storm, chaos energy, lightning, sand particles, dark pyramid background, dramatic red lighting, highly detailed, 4k, ominous atmosphere",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark",
                "animation_prompt": "chaotic energy crackling, sand storm swirling, lightning flashing, dramatic shadows"
            },
            "thoth_wisdom_keeper": {
                "prompt": "ancient egyptian god Thoth, ibis head, scroll of wisdom, hieroglyphic magic, golden library of alexandria, mystical blue energy, ancient knowledge, highly detailed, 4k",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark", 
                "animation_prompt": "scrolls unrolling, hieroglyphs glowing and writing themselves, wisdom energy flowing"
            },
            "horus_sky_god": {
                "prompt": "ancient egyptian god Horus, falcon head, eye of horus glowing, golden armor, sky temple, divine authority, royal blue and gold colors, highly detailed, 4k, majestic",
                "negative_prompt": "blurry, low quality, modern objects, text, watermark",
                "animation_prompt": "eye of horus blinking with divine power, golden armor gleaming, clouds moving in background"
            }
        }
    
    async def generate_static_card(self, card_name: str, save_path: str) -> bool:
        """Generate static card image using Stable Diffusion."""
        if not self.initialized:
            self.logger.error("AI models not initialized")
            return False
            
        try:
            prompts = self.get_egyptian_card_prompts()
            if card_name not in prompts:
                self.logger.error(f"No prompt found for card: {card_name}")
                return False
                
            card_data = prompts[card_name]
            self.logger.info(f"Generating static image for {card_name}...")
            
            # Generate image
            image = self.sd_pipeline(
                prompt=card_data["prompt"],
                negative_prompt=card_data["negative_prompt"],
                height=768,
                width=512,  # Card aspect ratio
                num_inference_steps=20,
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(42)
            ).images[0]
            
            # Save image
            image.save(save_path)
            self.logger.info(f"Static card saved: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate static card {card_name}: {e}")
            return False
    
    async def generate_animated_card(self, card_name: str, save_path: str) -> bool:
        """Generate animated card using AnimateDiff."""
        if not self.initialized:
            self.logger.error("AI models not initialized")
            return False
            
        try:
            prompts = self.get_egyptian_card_prompts()
            if card_name not in prompts:
                self.logger.error(f"No prompt found for card: {card_name}")
                return False
                
            card_data = prompts[card_name]
            self.logger.info(f"Generating animation for {card_name}...")
            
            # Combine base prompt with animation prompt
            full_prompt = f"{card_data['prompt']}, {card_data['animation_prompt']}"
            
            # Generate animation
            output = self.animatediff_pipeline(
                prompt=full_prompt,
                negative_prompt=card_data["negative_prompt"],
                num_frames=16,  # 16 frame animation
                height=768,
                width=512,
                num_inference_steps=25,
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(42)
            )
            
            frames = output.frames[0]
            
            # Export to GIF
            export_to_gif(frames, save_path, fps=8)
            self.logger.info(f"Animated card saved: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate animated card {card_name}: {e}")
            return False
    
    async def generate_all_cards(self, animated: bool = True) -> Dict[str, bool]:
        """Generate all Egyptian card images/animations."""
        if not self.initialized:
            if not await self.initialize():
                return {}
        
        results = {}
        prompts = self.get_egyptian_card_prompts()
        
        self.logger.info(f"Generating {'animated' if animated else 'static'} cards for {len(prompts)} Egyptian deities...")
        
        for card_name in prompts.keys():
            try:
                if animated:
                    save_path = self.output_dir / f"{card_name}_animated.gif"
                    success = await self.generate_animated_card(card_name, str(save_path))
                else:
                    save_path = self.output_dir / f"{card_name}_static.png"
                    success = await self.generate_static_card(card_name, str(save_path))
                
                results[card_name] = success
                
                # Small delay between generations to prevent GPU overload
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Failed to generate {card_name}: {e}")
                results[card_name] = False
        
        successful = sum(results.values())
        total = len(results)
        self.logger.info(f"Generation complete: {successful}/{total} cards generated successfully")
        
        return results
    
    def cleanup_models(self):
        """Free GPU memory by unloading models."""
        if self.sd_pipeline:
            del self.sd_pipeline
        if self.animatediff_pipeline:
            del self.animatediff_pipeline
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.initialized = False
        self.logger.info("AI models cleaned up")

# Main generation function
async def main():
    """Generate all Egyptian card animations using local AI."""
    generator = LocalAIGenerator()
    
    if not AI_LIBS_AVAILABLE:
        print("ERROR: AI libraries not available!")
        print("Install with: pip install diffusers transformers torch torchvision accelerate")
        return
    
    print("Initializing local AI animation generator...")
    if await generator.initialize():
        print("Generating animated Egyptian cards...")
        results = await generator.generate_all_cards(animated=True)
        
        print("\n=== Generation Results ===")
        for card_name, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            print(f"{card_name}: {status}")
        
        # Also generate static versions
        print("\nGenerating static card images...")
        static_results = await generator.generate_all_cards(animated=False)
        
        generator.cleanup_models()
    else:
        print("Failed to initialize AI models")

if __name__ == "__main__":
    asyncio.run(main())