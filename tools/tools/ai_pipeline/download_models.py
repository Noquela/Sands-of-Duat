#!/usr/bin/env python3
"""
Download essential models for Hades-quality game art generation
Optimized for RTX 5070 (12GB VRAM)
"""

import requests
import os
from pathlib import Path
from tqdm import tqdm

def download_file(url, filename):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename.name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            progress_bar.update(size)

def main():
    models_dir = Path("tools/ai_pipeline/models")
    
    # Essential models for game art generation
    models = {
        # SDXL Base Model (High quality)
        "checkpoints/sd_xl_base_1.0.safetensors": 
            "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
        
        # SDXL Refiner (For ultra-high quality)
        "checkpoints/sd_xl_refiner_1.0.safetensors":
            "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
        
        # VAE for SDXL
        "vae/sdxl_vae.safetensors":
            "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors",
        
        # ControlNet for precise poses
        "controlnet/controlnet-openpose-sdxl-1.0.safetensors":
            "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_canny_full.safetensors",
        
        # Upscaling model
        "upscale_models/RealESRGAN_x4plus.pth":
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    }
    
    print("Downloading professional AI models for RTX 5070...")
    
    for relative_path, url in models.items():
        full_path = models_dir / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not full_path.exists():
            print(f"\nDownloading {relative_path}...")
            try:
                download_file(url, full_path)
                print(f"  Downloaded: {relative_path}")
            except Exception as e:
                print(f"  Failed to download {relative_path}: {e}")
        else:
            print(f"  Already exists: {relative_path}")
    
    print("\nModel download complete!")

if __name__ == "__main__":
    main()
