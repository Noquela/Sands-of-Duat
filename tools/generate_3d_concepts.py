#!/usr/bin/env python3
"""
SANDS OF DUAT - 3D Concept + Texture Generator
Generate concept art and textures for 3D modeling, NOT 3D models themselves
"""

import torch
import os
import json
import time
from pathlib import Path

def generate_concepts_and_textures():
    """Generate concept art and textures for 3D modeling pipeline."""
    
    try:
        from diffusers import DiffusionPipeline
        from PIL import Image
        import numpy as np
        
        # Force RTX 5070 GPU usage
        if not torch.cuda.is_available():
            print("[ERROR] CUDA not available! Install PyTorch with CUDA 12.8")
            return False
        
        device = "cuda"
        dtype = torch.float16
        gpu_name = torch.cuda.get_device_name(0)
        print(f"[RTX-5070] Forcing GPU usage: {gpu_name}")
        
        # Clear GPU cache
        torch.cuda.empty_cache()
        
        print("[AI] Loading SDXL for concept art + texture generation...")
        
        # Load SDXL pipeline with GPU optimizations
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=dtype,
            use_safetensors=True,
            variant="fp16"
        )
        
        # Force GPU usage
        pipe = pipe.to(device)
        
        # Enable GPU memory optimizations (without xformers for RTX 5070)
        pipe.enable_attention_slicing()  # Reduce VRAM usage
        # Disable xformers for RTX 5070 compatibility
        print("[OPTIMIZATION] Using attention slicing for RTX 5070")
        
        print("[SUCCESS] SDXL Pipeline loaded!")
        
        # CONCEPT ART FOR 3D MODELING - Multiple views and details
        concepts = {
            # Character concepts - for 3D modeling reference
            "hero_pharaoh_concept": {
                "prompt": "Egyptian pharaoh warrior character concept art, multiple views (front, side, back, 3/4), detailed armor design, khopesh sword, golden ornaments, royal headpiece, athletic build, dark skin, concept sheet style, clean white background",
                "seed": 12345,
                "size": (1152, 1152)
            },
            
            "anubis_boss_concept": {
                "prompt": "Anubis boss character concept art, multiple views, tall imposing jackal-headed god, black fur, golden Egyptian armor, ceremonial staff, muscular humanoid body, intimidating pose, concept sheet style, white background",
                "seed": 12346,
                "size": (1152, 1152)
            },
            
            "mummy_enemy_concept": {
                "prompt": "Egyptian mummy enemy concept art, multiple views, wrapped in ancient bandages, glowing eyes, deteriorated pharaoh armor, shambling pose, undead warrior, concept sheet style, white background",
                "seed": 12347,
                "size": (1152, 1152)
            },
            
            # Weapon concepts - for 3D modeling
            "khopesh_sword_concept": {
                "prompt": "Ancient Egyptian khopesh sword concept art, multiple angles, curved bronze blade, ornate golden handle, hieroglyphic engravings, weathered metal texture, weapon design sheet, white background",
                "seed": 12348,
                "size": (1152, 1152)
            },
            
            "ceremonial_staff_concept": {
                "prompt": "Egyptian ceremonial staff concept art, detailed views, tall golden rod, ankh symbol at top, precious stones, ritual weapon, ornate decorations, weapon design sheet, white background",
                "seed": 12349,
                "size": (1152, 1152)
            },
        }
        
        # SEAMLESS TEXTURES - for 3D material application
        textures = {
            # Character textures
            "pharaoh_armor_albedo": {
                "prompt": "Egyptian pharaoh golden armor texture, seamless tileable, ornate patterns, hieroglyphic details, metallic gold surface, weathered royal armor, high resolution, material texture",
                "seed": 22345,
                "size": (1024, 1024),
                "seamless": True
            },
            
            "mummy_bandage_albedo": {
                "prompt": "Ancient mummy bandages texture, seamless tileable, aged linen wraps, stained and torn fabric, archaeological texture, beige and brown tones, high resolution material",
                "seed": 22346,
                "size": (1024, 1024),
                "seamless": True
            },
            
            "anubis_fur_albedo": {
                "prompt": "Black jackal fur texture, seamless tileable, dense canine fur pattern, dark black with subtle highlights, natural animal texture, high resolution material",
                "seed": 22347,
                "size": (1024, 1024),
                "seamless": True
            },
            
            # Environment textures
            "sandstone_wall_albedo": {
                "prompt": "Egyptian temple sandstone wall texture, seamless tileable, carved hieroglyphic blocks, weathered stone surface, desert beige color, architectural texture",
                "seed": 22348,
                "size": (1024, 1024),
                "seamless": True
            },
            
            "hieroglyph_floor_albedo": {
                "prompt": "Egyptian temple floor texture with hieroglyphs, seamless tileable, carved stone tiles, gold inlay details, ancient symbols, temple flooring material",
                "seed": 22349,
                "size": (1024, 1024),
                "seamless": True
            },
            
            # Emissive textures for glowing effects
            "rune_emissive": {
                "prompt": "Egyptian magical runes emissive texture, glowing hieroglyphs, bright golden yellow light, mystical symbols, alpha mask for glowing effects, black background",
                "seed": 32345,
                "size": (1024, 1024),
                "seamless": False
            },
            
            "eye_of_horus_emissive": {
                "prompt": "Eye of Horus glowing emissive texture, bright golden light, mystical Egyptian symbol, magical glow effect, alpha mask, black background",
                "seed": 32346,
                "size": (512, 512),
                "seamless": False
            }
        }
        
        # Create output directories
        output_dirs = {
            "concepts": Path("art/sdxl/concepts"),
            "textures": Path("art/sdxl/textures"),
            "emissive": Path("art/sdxl/emissive"),
            "prompts": Path("art/prompts")
        }
        
        for dir_path in output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("\\n[GENERATION] Creating concept art for 3D modeling...")
        
        # Generate concept art
        for concept_name, config in concepts.items():
            print(f"\\n[GENERATING] {concept_name}")
            print(f"[PROMPT] {config['prompt'][:80]}...")
            
            try:
                # Generate with SDXL
                image = pipe(
                    prompt=config["prompt"],
                    negative_prompt="blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts, cartoon, anime, 3d render, not concept art",
                    height=config["size"][1],
                    width=config["size"][0],
                    num_inference_steps=50,
                    guidance_scale=7.5,
                    generator=torch.Generator(device=device).manual_seed(config["seed"])
                ).images[0]
                
                # Save concept
                output_path = output_dirs["concepts"] / f"{concept_name}.png"
                image.save(output_path)
                print(f"[SUCCESS] Concept saved: {output_path}")
                
                # Save prompt config
                prompt_config = {
                    "name": concept_name,
                    "prompt": config["prompt"],
                    "negative": "blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts, cartoon, anime, 3d render, not concept art",
                    "seed": config["seed"],
                    "size": config["size"],
                    "steps": 50,
                    "guidance": 7.5,
                    "type": "concept"
                }
                
                prompt_path = output_dirs["prompts"] / f"{concept_name}.json"
                with open(prompt_path, 'w') as f:
                    json.dump(prompt_config, f, indent=2)
                
                time.sleep(2)
                
            except Exception as e:
                print(f"[ERROR] Failed to generate {concept_name}: {e}")
                continue
        
        print("\\n[GENERATION] Creating textures for 3D materials...")
        
        # Generate textures
        for texture_name, config in textures.items():
            print(f"\\n[GENERATING] {texture_name}")
            print(f"[PROMPT] {config['prompt'][:80]}...")
            
            try:
                # Generate with SDXL (with tiling for seamless textures)
                if config.get("seamless", False):
                    # For seamless textures, add tiling instructions
                    enhanced_prompt = config["prompt"] + ", perfect tileable pattern, no seams, repeatable texture"
                else:
                    enhanced_prompt = config["prompt"]
                
                image = pipe(
                    prompt=enhanced_prompt,
                    negative_prompt="seams, visible edges, not tileable, blurry, low quality, distorted, watermark, text, signature, photorealistic if texture",
                    height=config["size"][1],
                    width=config["size"][0],
                    num_inference_steps=40,
                    guidance_scale=6.5,
                    generator=torch.Generator(device=device).manual_seed(config["seed"])
                ).images[0]
                
                # Determine output directory
                if "emissive" in texture_name:
                    output_path = output_dirs["emissive"] / f"{texture_name}.png"
                else:
                    output_path = output_dirs["textures"] / f"{texture_name}.png"
                
                # Save texture
                image.save(output_path)
                print(f"[SUCCESS] Texture saved: {output_path}")
                
                # Save prompt config
                prompt_config = {
                    "name": texture_name,
                    "prompt": config["prompt"],
                    "negative": "seams, visible edges, not tileable, blurry, low quality, distorted, watermark, text, signature",
                    "seed": config["seed"],
                    "size": config["size"],
                    "steps": 40,
                    "guidance": 6.5,
                    "seamless": config.get("seamless", False),
                    "type": "texture"
                }
                
                prompt_path = output_dirs["prompts"] / f"{texture_name}.json"
                with open(prompt_path, 'w') as f:
                    json.dump(prompt_config, f, indent=2)
                
                time.sleep(1)
                
            except Exception as e:
                print(f"[ERROR] Failed to generate {texture_name}: {e}")
                continue
        
        print("\\n[COMPLETE] Concept art and texture generation finished!")
        print("[INFO] Assets saved to:")
        for name, path in output_dirs.items():
            print(f"  - {name}: {path.absolute()}")
        
        print("\\n[NEXT STEPS]")
        print("1. Clean backgrounds: python tools/clean_bg.py art/sdxl/concepts art/sdxl/clean")
        print("2. Use concepts as reference for 3D modeling in Blender")
        print("3. Apply textures to 3D models as materials")
        print("4. Export as glTF with rigging and animations")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        return False

if __name__ == "__main__":
    print("SANDS OF DUAT - RTX 5070 3D Concept + Texture Generator")
    print("=" * 60)
    
    success = generate_concepts_and_textures()
    
    if success:
        print("\\n[SUCCESS] All concepts and textures generated!")
    else:
        print("\\n[FAILED] Generation failed.")