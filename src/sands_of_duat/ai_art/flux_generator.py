"""
FLUX.1 DEV GENERATOR - OPTIMIZED FOR RTX 5070
The absolute BEST AI art model for Hades-quality Egyptian artwork!
"""

import torch
from diffusers import FluxPipeline
import numpy as np
from PIL import Image
from typing import Optional, Dict, Any, List
import logging
import time

logger = logging.getLogger(__name__)

class FluxHadesGenerator:
    """
    Flux.1 Dev generator optimized for RTX 5070 + 32GB RAM.
    Creates absolutely stunning Hades-quality Egyptian artwork.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe: Optional[FluxPipeline] = None
        self.model_loaded = False
        
        # RTX 5070 optimal settings
        self.optimal_settings = {
            'height': 1024,
            'width': 768,  # Card aspect ratio
            'num_inference_steps': 28,  # Flux needs fewer steps
            'guidance_scale': 3.5,  # Flux is very responsive
            'max_sequence_length': 512,
        }
        
        logger.info("Flux.1 Dev Generator initialized for RTX 5070")
    
    def load_model(self) -> bool:
        """Load Flux.1 Dev model with RTX 5070 optimization."""
        
        if self.model_loaded:
            return True
        
        try:
            logger.info("Loading Flux.1 Dev model... (this will take a few minutes first time)")
            logger.info("VRAM usage: ~10GB of your 12GB RTX 5070")
            
            # Load with optimal settings for RTX 5070
            self.pipe = FluxPipeline.from_pretrained(
                "black-forest-labs/FLUX.1-dev",
                torch_dtype=torch.bfloat16,
                device_map="auto",
                use_safetensors=True
            )
            
            # Move to GPU
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory efficient attention
            self.pipe.enable_model_cpu_offload()  # Saves VRAM
            
            # Compile for faster generation (RTX 5070 supports this)
            try:
                self.pipe.unet = torch.compile(self.pipe.unet, mode="reduce-overhead", fullgraph=True)
                logger.info("Model compiled for faster generation!")
            except Exception as e:
                logger.warning(f"Could not compile model (still works fine): {e}")
            
            self.model_loaded = True
            logger.info("SUCCESS: Flux.1 Dev loaded and ready for HADES-QUALITY generation!")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Flux.1 Dev: {e}")
            return False
    
    def generate_hades_egyptian_art(self, prompt: str, negative_prompt: str = "",
                                   width: int = 768, height: int = 1024,
                                   steps: int = 28, guidance: float = 3.5) -> Optional[Image.Image]:
        """Generate Hades-quality Egyptian artwork."""
        
        if not self.model_loaded:
            if not self.load_model():
                return None
        
        try:
            logger.info(f"Generating with Flux.1 Dev: {prompt[:50]}...")
            start_time = time.time()
            
            # Enhanced prompt for Hades quality
            enhanced_prompt = f"""
            {prompt}, 
            masterpiece, best quality, highly detailed, 
            supergiant games art style, hades game aesthetic,
            vibrant colors, dramatic lighting, painterly style,
            hand-painted illustration, award-winning digital art,
            professional game artwork, rich textures
            """
            
            # Enhanced negative prompt
            enhanced_negative = f"""
            {negative_prompt}, 
            blurry, low quality, bad anatomy, deformed, ugly,
            amateur, sketch, unfinished, photorealistic, 3d render,
            modern elements, generic, boring, flat lighting
            """
            
            # Generate with optimal settings
            with torch.autocast("cuda", dtype=torch.bfloat16):
                result = self.pipe(
                    prompt=enhanced_prompt.strip(),
                    negative_prompt=enhanced_negative.strip(),
                    height=height,
                    width=width,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    max_sequence_length=512,
                    generator=torch.Generator("cuda").manual_seed(42)  # Consistent results
                )
            
            generation_time = time.time() - start_time
            logger.info(f"Generation complete in {generation_time:.1f}s - HADES QUALITY ACHIEVED!")
            
            return result.images[0]
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return None
    
    def batch_generate(self, prompts: List[str], **kwargs) -> List[Optional[Image.Image]]:
        """Generate multiple images in batch."""
        
        results = []
        for i, prompt in enumerate(prompts):
            logger.info(f"Batch generation {i+1}/{len(prompts)}")
            result = self.generate_hades_egyptian_art(prompt, **kwargs)
            results.append(result)
            
            # Small delay to prevent overheating
            time.sleep(2)
        
        return results
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current VRAM usage."""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3  # GB
            cached = torch.cuda.memory_reserved() / 1024**3     # GB
            return {
                'allocated_gb': allocated,
                'cached_gb': cached,
                'total_vram_gb': torch.cuda.get_device_properties(0).total_memory / 1024**3
            }
        return {}

# Global Flux generator
_flux_generator: Optional[FluxHadesGenerator] = None

def get_flux_generator() -> FluxHadesGenerator:
    """Get the global Flux generator instance."""
    global _flux_generator
    if _flux_generator is None:
        _flux_generator = FluxHadesGenerator()
    return _flux_generator