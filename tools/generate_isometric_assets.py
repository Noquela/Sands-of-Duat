#!/usr/bin/env python3
"""
SANDS OF DUAT - Generate True 3D Isometric Assets
Specialized script to generate proper isometric game sprites using RTX 5070
"""

import torch
import os
import time
from pathlib import Path

def generate_isometric_assets():
    """Generate true 3D isometric assets for the game."""
    
    try:
        from diffusers import DiffusionPipeline
        import torch
        from PIL import Image
        import numpy as np
        
        # Check RTX 5070 availability
        use_gpu = torch.cuda.is_available()
        device = "cuda" if use_gpu else "cpu" 
        dtype = torch.float16 if use_gpu else torch.float32
        
        if use_gpu:
            gpu_name = torch.cuda.get_device_name(0)
            print(f"[GPU] Using: {gpu_name}")
            print(f"[VRAM] Available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        print("[AI] Loading SDXL for isometric asset generation...")
        
        # Load SDXL pipeline
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=dtype,
            use_safetensors=True,
            variant="fp16" if use_gpu else None
        )
        pipe = pipe.to(device)
        
        print("[SUCCESS] SDXL Pipeline loaded!")
        
        # TRUE 3D ISOMETRIC CHARACTER PROMPTS
        isometric_characters = {
            "pharaoh_warrior_iso": "3D isometric view, 3/4 angle perspective, majestic Egyptian pharaoh warrior, golden armor and headdress, holding ceremonial khopesh sword, muscular build, regal stance, game character sprite, clean transparent background, high detail, cinematic lighting, Hades game art style, masterpiece",
            
            "anubis_judge_iso": "3D isometric view, 3/4 angle perspective, intimidating Anubis jackal-headed judge, black and gold Egyptian ceremonial robes, holding scales of justice, tall imposing figure, ancient deity, game character sprite, clean transparent background, dramatic lighting, Hades game art style, masterpiece",
            
            "mummy_guardian_iso": "3D isometric view, 3/4 angle perspective, menacing Egyptian mummy guardian, wrapped in ancient bandages, glowing red eyes, tattered burial wrappings, defensive combat stance, undead warrior, game character sprite, clean transparent background, eerie lighting, Hades game art style, masterpiece",
            
            "set_chaos_iso": "3D isometric view, 3/4 angle perspective, fierce Set Egyptian god of chaos, red-skinned muscular warrior, distinctive Set animal head, bronze armor with chaos symbols, wielding curved war blade, aggressive battle pose, game character sprite, clean transparent background, dramatic lighting, Hades game art style, masterpiece"
        }
        
        # Create output directories
        output_dirs = {
            "characters": Path("assets/characters_isometric"),
            "environments": Path("assets/environments_isometric"),
        }
        
        for dir_path in output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Generate isometric character sprites
        print("\n[GENERATION] Creating true 3D isometric character sprites...")
        
        for asset_name, prompt in isometric_characters.items():
            print(f"\n[GENERATING] {asset_name}")
            print(f"[PROMPT] {prompt[:80]}...")
            
            try:
                # Generate with SDXL optimized settings for isometric game sprites
                image = pipe(
                    prompt=prompt,
                    negative_prompt="blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts, front view, side view, back view, 2D flat, not isometric",
                    height=1152,  # SDXL optimal resolution
                    width=1152,   # Square format for game sprites
                    num_inference_steps=50,  # Higher steps for better quality
                    guidance_scale=7.5,      # SDXL optimal guidance
                    generator=torch.Generator(device=device).manual_seed(42)
                ).images[0]
                
                # Save the generated image
                output_path = output_dirs["characters"] / f"{asset_name}.png"
                image.save(output_path)
                print(f"[SUCCESS] Saved: {output_path}")
                
                # Create alpha version (remove background)
                alpha_path = output_dirs["characters"] / f"{asset_name}_alpha.png"
                
                # Simple background removal - convert white/near-white to transparent
                img_array = np.array(image.convert("RGBA"))
                
                # Create alpha mask - remove white/light backgrounds
                # Adjust threshold to remove light backgrounds while keeping character
                threshold = 240
                mask = (img_array[:,:,0] > threshold) & (img_array[:,:,1] > threshold) & (img_array[:,:,2] > threshold)
                img_array[mask, 3] = 0  # Set alpha to 0 for background pixels
                
                # Save alpha version
                alpha_image = Image.fromarray(img_array, 'RGBA')
                alpha_image.save(alpha_path)
                print(f"[ALPHA] Saved: {alpha_path}")
                
                # Brief pause to prevent overheating
                time.sleep(2)
                
            except Exception as e:
                print(f"[ERROR] Failed to generate {asset_name}: {e}")
                continue
        
        print("\n[COMPLETE] Isometric asset generation finished!")
        print("[INFO] Assets saved to:")
        for name, path in output_dirs.items():
            print(f"  - {name}: {path.absolute()}")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Missing required packages: {e}")
        print("[FIX] Run: pip install torch diffusers transformers pillow")
        return False
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        return False

if __name__ == "__main__":
    print("SANDS OF DUAT - RTX 5070 Isometric Asset Generator")
    print("=" * 50)
    
    success = generate_isometric_assets()
    
    if success:
        print("\n[SUCCESS] All isometric assets generated!")
    else:
        print("\n[FAILED] Asset generation failed.")