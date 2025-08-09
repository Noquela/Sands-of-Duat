#!/usr/bin/env python3
'''
Egyptian-Hades LoRA Asset Generator
Generates consistent game assets using trained LoRA
'''

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from pathlib import Path

class EgyptianHadesAssetGenerator:
    def __init__(self, lora_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load SDXL pipeline
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to(self.device)
        
        # Load our custom LoRA
        self.pipe.load_lora_weights(lora_path)
        
        # Optimize for quality
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        self.pipe.enable_model_cpu_offload()
        
    def generate_card_art(self, card_name, card_desc):
        prompt = f"egyptian_hades_art, {card_desc}, trading card art, masterpiece, highly detailed, professional game art"
        
        negative = "low quality, blurry, text, watermark, signature"
        
        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative,
            width=768,
            height=1024,
            num_inference_steps=30,
            guidance_scale=7.5,
            num_images_per_prompt=1
        ).images[0]
        
        return image

# Usage example:
if __name__ == "__main__":
    generator = EgyptianHadesAssetGenerator("path/to/egyptian-hades-gameart-v1.safetensors")
    
    ra_card = generator.generate_card_art(
        "Ra Sun God", 
        "Ra the Egyptian sun god with falcon head and solar disk crown"
    )
    
    ra_card.save("ra_sun_god_lora.png")
