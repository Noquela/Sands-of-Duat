#!/usr/bin/env python3
"""
SDXL Refiner Tool for Sands of Duat Asset Generation
Refines raw generated images using Stable Diffusion XL for final quality.
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import torch
    from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusionXLPipeline
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install torch diffusers pillow numpy")
    sys.exit(1)


class SDXLRefiner:
    """SDXL-based image refinement system."""
    
    def __init__(self, model_path: str = "stabilityai/stable-diffusion-xl-base-1.0", 
                 device: str = "auto", medvram: bool = False):
        self.device = self._setup_device(device)
        self.medvram = medvram
        self.model_path = model_path
        self.pipeline = None
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Egyptian-themed refinement prompts
        self.style_prompts = {
            "character": "highly detailed character art, cel-shaded, Egyptian mythology, golden ratio composition, professional concept art",
            "card": "trading card game art, Egyptian hieroglyphic border, mystical symbols, golden accents, high detail illustration",
            "environment": "Egyptian temple architecture, atmospheric lighting, sandstone textures, ancient mystical ambiance",
            "ui": "Egyptian UI elements, hieroglyphic patterns, golden ornamental details, papyrus texture"
        }
        
        self.negative_prompt = "blurry, low quality, distorted, watermark, signature, text, bad anatomy, deformed"
        
    def _setup_device(self, device: str) -> str:
        """Setup compute device with RTX 5070 optimization."""
        if device == "auto":
            if torch.cuda.is_available():
                # RTX 5070 optimization
                device = "cuda"
                torch.backends.cudnn.benchmark = True
                # Enable memory efficient attention for RTX 5070
                torch.backends.cuda.enable_flash_sdp(True)
            else:
                device = "cpu"
                print("WARNING: CUDA not available, falling back to CPU (will be slow)")
        
        print(f"Using device: {device}")
        if device == "cuda":
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        return device
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for pipeline tracking."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "sdxl_refiner.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def load_pipeline(self):
        """Load SDXL pipeline with memory optimization."""
        self.logger.info(f"Loading SDXL pipeline: {self.model_path}")
        
        kwargs = {
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            "use_safetensors": True,
            "variant": "fp16" if self.device == "cuda" else None
        }
        
        if self.medvram:
            kwargs["low_cpu_mem_usage"] = True
        
        try:
            self.pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                self.model_path, **kwargs
            ).to(self.device)
            
            if self.medvram and self.device == "cuda":
                # Enable memory efficient mode for RTX 5070
                self.pipeline.enable_model_cpu_offload()
                self.pipeline.enable_vae_slicing()
                self.pipeline.enable_attention_slicing("max")
            
            self.logger.info("SDXL pipeline loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load SDXL pipeline: {e}")
            raise
    
    def refine_image(self, input_path: str, output_path: str, 
                    style: str = "character", steps: int = 28, 
                    cfg: float = 7.0, strength: float = 0.35) -> bool:
        """Refine an input image using SDXL."""
        try:
            self.logger.info(f"Refining {input_path} -> {output_path}")
            
            if not self.pipeline:
                self.load_pipeline()
            
            # Load input image
            input_image = Image.open(input_path).convert("RGB")
            original_size = input_image.size
            
            # Resize for SDXL if needed (optimal: 1024x1024)
            if max(original_size) != 1024:
                ratio = 1024 / max(original_size)
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                input_image = input_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Get style-specific prompt
            style_prompt = self.style_prompts.get(style, self.style_prompts["character"])
            
            # Generate with SDXL
            start_time = time.time()
            
            result = self.pipeline(
                prompt=style_prompt,
                negative_prompt=self.negative_prompt,
                image=input_image,
                strength=strength,
                num_inference_steps=steps,
                guidance_scale=cfg,
                generator=torch.Generator(device=self.device).manual_seed(42)
            )
            
            refined_image = result.images[0]
            
            # Resize back to original if needed
            if refined_image.size != original_size:
                refined_image = refined_image.resize(original_size, Image.Resampling.LANCZOS)
            
            # Save result
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            refined_image.save(output_path, quality=95)
            
            generation_time = time.time() - start_time
            self.logger.info(f"Refinement completed in {generation_time:.2f}s")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to refine image: {e}")
            return False
    
    def batch_refine(self, input_dir: str, output_dir: str, 
                    style: str = "character", **kwargs) -> int:
        """Refine all images in a directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        image_files = list(input_path.glob("*.png")) + list(input_path.glob("*.jpg"))
        successful = 0
        
        self.logger.info(f"Starting batch refinement: {len(image_files)} images")
        
        for img_file in image_files:
            output_file = output_path / f"{img_file.stem}_refined.png"
            
            if self.refine_image(str(img_file), str(output_file), style, **kwargs):
                successful += 1
        
        self.logger.info(f"Batch refinement completed: {successful}/{len(image_files)} successful")
        return successful


def main():
    parser = argparse.ArgumentParser(description="SDXL Image Refiner for Sands of Duat")
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--style", default="character", 
                       choices=["character", "card", "environment", "ui"],
                       help="Art style for refinement")
    parser.add_argument("--steps", type=int, default=28, help="Number of inference steps")
    parser.add_argument("--cfg", type=float, default=7.0, help="Guidance scale")
    parser.add_argument("--strength", type=float, default=0.35, help="Refinement strength")
    parser.add_argument("--medvram", action="store_true", help="Enable memory efficient mode")
    parser.add_argument("--batch", help="Batch process directory instead of single image")
    
    args = parser.parse_args()
    
    # Initialize refiner
    refiner = SDXLRefiner(medvram=args.medvram)
    
    if args.batch:
        # Batch processing
        success_count = refiner.batch_refine(
            args.batch, args.output, args.style,
            steps=args.steps, cfg=args.cfg, strength=args.strength
        )
        print(f"Refined {success_count} images successfully")
    else:
        # Single image processing
        success = refiner.refine_image(
            args.input, args.output, args.style,
            args.steps, args.cfg, args.strength
        )
        
        if success:
            print(f"Successfully refined: {args.output}")
        else:
            print("Refinement failed")
            sys.exit(1)


if __name__ == "__main__":
    main()