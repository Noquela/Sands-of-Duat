#!/usr/bin/env python3
"""
SANDS OF DUAT - Generate 3D Environment Elements 
Generate walls, pillars, decorations for atmospheric 3D scenes
"""

import torch
import os
import time
from pathlib import Path

def generate_environment_elements():
    """Generate 3D environment elements for atmospheric scenes."""
    
    try:
        from diffusers import DiffusionPipeline
        import torch
        from PIL import Image
        import numpy as np
        
        # Check RTX 5070
        use_gpu = torch.cuda.is_available()
        device = "cuda" if use_gpu else "cpu" 
        dtype = torch.float16 if use_gpu else torch.float32
        
        if use_gpu:
            gpu_name = torch.cuda.get_device_name(0)
            print(f"[GPU] Using: {gpu_name}")
        
        print("[AI] Loading SDXL for 3D environment generation...")
        
        # Load SDXL pipeline
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=dtype,
            use_safetensors=True,
            variant="fp16" if use_gpu else None
        )
        pipe = pipe.to(device)
        
        print("[SUCCESS] SDXL Pipeline loaded!")
        
        # 3D ENVIRONMENT ELEMENTS - ISOMETRIC PERSPECTIVE
        environment_elements = {
            # Walls and Architecture
            "egyptian_wall_section": "3D isometric view, 3/4 angle perspective, Egyptian temple wall section, ancient sandstone blocks, carved hieroglyphic relief, weathered texture, architectural detail, game environment asset, clean background, atmospheric lighting, Hades art style, masterpiece",
            
            "stone_pillar_ornate": "3D isometric view, 3/4 angle perspective, massive Egyptian temple pillar, lotus capital, hieroglyphic carvings, weathered sandstone, ancient architecture column, game environment prop, clean background, dramatic lighting, Hades art style, masterpiece",
            
            "torch_brazier": "3D isometric view, 3/4 angle perspective, Egyptian bronze torch brazier, ornate fire bowl on decorative stand, flickering flames, warm orange glow, temple lighting fixture, game environment prop, transparent background, atmospheric lighting, masterpiece",
            
            # Decorative Elements  
            "anubis_guardian_statue": "3D isometric view, 3/4 angle perspective, imposing Anubis guardian statue, black stone carved jackal deity, sitting pose, golden accent details, temple sculpture, game decoration asset, clean background, mysterious lighting, Hades art style, masterpiece",
            
            "golden_sarcophagus": "3D isometric view, 3/4 angle perspective, ornate golden Egyptian sarcophagus, pharaoh burial casket, detailed hieroglyphic decorations, precious metals, royal tomb artifact, game environment prop, transparent background, luxurious lighting, masterpiece",
            
            "obelisk_monument": "3D isometric view, 3/4 angle perspective, tall Egyptian obelisk monument, weathered sandstone with hieroglyphic inscriptions, ancient temple marker, imposing monumental structure, game environment asset, clean background, epic lighting, Hades art style, masterpiece",
            
            # Floor Textures
            "hieroglyph_floor_seamless": "seamless tileable Egyptian hieroglyph floor texture, 3D isometric perspective, ancient stone tiles with carved hieroglyphs, gold inlay details, weathered sandstone pattern, temple flooring, high resolution game texture, neutral lighting",
            
            "ornate_tomb_floor": "seamless tileable ornate Egyptian tomb floor pattern, 3D isometric view, intricate geometric designs, blue and gold mosaic tiles, pharaoh burial chamber style, luxurious temple flooring, game texture, rich detailing"
        }
        
        # Create output directories
        output_dirs = {
            "environment_3d": Path("assets/environment_3d"),
            "floor_textures": Path("assets/floor_textures"),
        }
        
        for dir_path in output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Generate environment elements
        print("\n[GENERATION] Creating 3D environment elements...")
        
        for asset_name, prompt in environment_elements.items():
            print(f"\n[GENERATING] {asset_name}")
            print(f"[PROMPT] {prompt[:80]}...")
            
            try:
                # Generate with SDXL
                image = pipe(
                    prompt=prompt,
                    negative_prompt="blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts, front view, side view, back view, 2D flat, not isometric, modern items, plastic",
                    height=1152,
                    width=1152,
                    num_inference_steps=50,
                    guidance_scale=7.5,
                    generator=torch.Generator(device=device).manual_seed(42)
                ).images[0]
                
                # Determine output directory
                if "floor" in asset_name:
                    output_path = output_dirs["floor_textures"] / f"{asset_name}.png"
                else:
                    output_path = output_dirs["environment_3d"] / f"{asset_name}.png"
                
                # Save the generated image
                image.save(output_path)
                print(f"[SUCCESS] Saved: {output_path}")
                
                # Create alpha version for non-floor elements
                if "floor" not in asset_name:
                    alpha_path = output_path.with_name(f"{asset_name}_alpha.png")
                    
                    # Background removal
                    img_array = np.array(image.convert("RGBA"))
                    
                    # Remove light backgrounds
                    threshold = 230
                    mask = (img_array[:,:,0] > threshold) & (img_array[:,:,1] > threshold) & (img_array[:,:,2] > threshold)
                    img_array[mask, 3] = 0
                    
                    # Save alpha version
                    alpha_image = Image.fromarray(img_array, 'RGBA')
                    alpha_image.save(alpha_path)
                    print(f"[ALPHA] Saved: {alpha_path}")
                
                # Pause between generations
                time.sleep(2)
                
            except Exception as e:
                print(f"[ERROR] Failed to generate {asset_name}: {e}")
                continue
        
        print("\n[COMPLETE] Environment element generation finished!")
        print("[INFO] Assets saved to:")
        for name, path in output_dirs.items():
            print(f"  - {name}: {path.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        return False

if __name__ == "__main__":
    print("SANDS OF DUAT - RTX 5070 Environment Element Generator")
    print("=" * 55)
    
    success = generate_environment_elements()
    
    if success:
        print("\n[SUCCESS] All environment elements generated!")
    else:
        print("\n[FAILED] Environment generation failed.")