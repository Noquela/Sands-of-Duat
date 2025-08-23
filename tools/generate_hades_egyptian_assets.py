#!/usr/bin/env python
"""
Egyptian Hades-style Asset Generator with SDXL
Generates assets with transparent backgrounds for direct game integration
"""

import torch
from diffusers import DiffusionPipeline
from PIL import Image, ImageOps
import pathlib
import json
import time

class EgyptianHadesGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.pipe = None
        self.prompts_log = []
        
    def load_pipeline(self):
        print(f"[GPU] Loading SDXL pipeline on {self.device}...")
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=self.dtype,
            use_safetensors=True,
            variant="fp16" if torch.cuda.is_available() else None
        )
        
        if torch.cuda.is_available():
            self.pipe = self.pipe.to(self.device)
            # RTX 5070 optimizations
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_attention_slicing()
        
        print("[SUCCESS] SDXL pipeline loaded!")

    def generate_asset(self, prompt, negative_prompt, output_path, seed=42):
        """Generate single asset with transparent background ready for game"""
        if not self.pipe:
            self.load_pipeline()
            
        # Egyptian Hades style enhancement
        enhanced_prompt = f"{prompt}, Egyptian art style, Hades game style, dark fantasy, cinematic lighting, detailed, sharp focus, transparent background, no background, isolated on transparent, clean edges"
        
        enhanced_negative = f"{negative_prompt}, background, scenery, environment, blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts, solid background, gradient background"
        
        print(f"[GPU] Generating: {prompt[:50]}...")
        
        generator = torch.Generator(device=self.device).manual_seed(seed)
        image = self.pipe(
            prompt=enhanced_prompt,
            negative_prompt=enhanced_negative,
            height=1152,  # SDXL optimal
            width=1152,   # Square format for sprites
            num_inference_steps=40,
            guidance_scale=8.0,
            generator=generator
        ).images[0]
        
        # Post-process for game use
        image = self.post_process_for_game(image)
        
        # Save
        output_path = pathlib.Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "PNG")
        
        # Log prompt
        self.prompts_log.append({
            "prompt": enhanced_prompt,
            "negative": enhanced_negative,
            "seed": seed,
            "output": str(output_path),
            "timestamp": time.time()
        })
        
        print(f"[SUCCESS] Saved: {output_path}")
        return image
    
    def post_process_for_game(self, image):
        """Post-process image for game integration"""
        # Convert to RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Make white/very light pixels transparent (common SDXL background issue)
        data = image.getdata()
        new_data = []
        for item in data:
            # If pixel is very light (near white background), make transparent
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((item[0], item[1], item[2], 0))  # Transparent
            else:
                new_data.append(item)
        
        image.putdata(new_data)
        return image
    
    def generate_egyptian_character_set(self):
        """Generate complete Egyptian character set for Hades-style game"""
        characters = [
            {
                "name": "pharaoh_warrior",
                "prompt": "Egyptian pharaoh warrior, golden armor, khopesh sword, muscular build, ancient Egyptian crown, detailed armor plates",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "anubis_judge", 
                "prompt": "Anubis god of death, black jackal head, Egyptian robe, glowing eyes, holding scales of justice",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "isis_mother",
                "prompt": "Isis goddess, beautiful Egyptian woman, flowing robes, golden wings, maternal expression, ankh symbol",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "ra_sun_god",
                "prompt": "Ra sun god, falcon head, golden solar disk, radiant energy, Egyptian royal garments, powerful stance",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "set_chaos_god",
                "prompt": "Set god of chaos, dark Egyptian deity, red skin, curved horn, menacing expression, dark energy",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "mummy_guardian",
                "prompt": "Ancient Egyptian mummy, wrapped in bandages, glowing eyes, defensive pose, tomb guardian",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "sphinx_guardian",
                "prompt": "Egyptian sphinx, lion body with human head, stone texture, majestic pose, ancient wisdom",
                "folder": "art/sdxl/raw/characters"
            },
            {
                "name": "egyptian_warrior",
                "prompt": "Egyptian soldier, bronze armor, spear and shield, desert warrior, detailed military gear",
                "folder": "art/sdxl/raw/characters"
            }
        ]
        
        negative = "blurry, low quality, modern clothing, cartoon, anime, multiple characters, crowd"
        
        for char in characters:
            for variation in range(3):  # Generate 3 variations of each
                seed = 42 + hash(char["name"]) + variation * 100
                filename = f"{char['name']}_var{variation+1}.png"
                output_path = pathlib.Path(char["folder"]) / filename
                
                self.generate_asset(
                    char["prompt"],
                    negative,
                    output_path,
                    seed
                )
    
    def generate_environment_textures(self):
        """Generate tileable Egyptian environment textures"""
        textures = [
            {
                "name": "sand_desert",
                "prompt": "seamless desert sand texture, fine golden sand, tileable, top-down view, Egyptian desert",
                "folder": "art/sdxl/tiles_raw"
            },
            {
                "name": "stone_blocks", 
                "prompt": "seamless Egyptian stone blocks, carved limestone, hieroglyphs, tileable texture",
                "folder": "art/sdxl/tiles_raw"
            },
            {
                "name": "tomb_floor",
                "prompt": "seamless ancient Egyptian tomb floor, worn stone, carved patterns, tileable",
                "folder": "art/sdxl/tiles_raw"
            },
            {
                "name": "pyramid_interior",
                "prompt": "Egyptian pyramid interior wall, hieroglyphic carvings, aged stone texture, seamless",
                "folder": "art/sdxl/tiles_raw"
            }
        ]
        
        negative = "3d, perspective, characters, objects, non-tileable, seams, borders"
        
        for texture in textures:
            seed = 42 + hash(texture["name"])
            filename = f"{texture['name']}.png" 
            output_path = pathlib.Path(texture["folder"]) / filename
            
            self.generate_asset(
                texture["prompt"],
                negative,
                output_path,
                seed
            )
    
    def generate_ui_icons(self):
        """Generate Egyptian-themed UI icons"""
        icons = [
            {
                "name": "ankh_health",
                "prompt": "Egyptian ankh symbol, golden, detailed carving, icon style, simple background",
                "folder": "art/sdxl/ui_raw"
            },
            {
                "name": "scarab_energy", 
                "prompt": "Egyptian scarab beetle, golden, detailed wings, icon style, energy symbol",
                "folder": "art/sdxl/ui_raw"
            },
            {
                "name": "eye_of_horus",
                "prompt": "Eye of Horus, Egyptian symbol, golden, detailed, icon style, protection symbol",
                "folder": "art/sdxl/ui_raw"
            },
            {
                "name": "khopesh_sword",
                "prompt": "Egyptian khopesh sword, curved blade, golden handle, weapon icon, detailed craftsmanship",
                "folder": "art/sdxl/ui_raw"
            }
        ]
        
        negative = "characters, complex background, blurry, low quality, multiple objects"
        
        for icon in icons:
            seed = 42 + hash(icon["name"])
            filename = f"{icon['name']}.png"
            output_path = pathlib.Path(icon["folder"]) / filename
            
            self.generate_asset(
                icon["prompt"],
                negative, 
                output_path,
                seed
            )
    
    def save_prompts_log(self):
        """Save all prompts used for reproducibility"""
        log_file = pathlib.Path("art/prompts/generation_log.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(self.prompts_log, f, indent=2)
        
        print(f"[SUCCESS] Prompts log saved to {log_file}")

def main():
    """Generate complete Egyptian Hades-style asset set"""
    generator = EgyptianHadesGenerator()
    
    print("=== Egyptian Hades Asset Generator ===")
    print("Generating character sprites...")
    generator.generate_egyptian_character_set()
    
    print("\nGenerating environment textures...")
    generator.generate_environment_textures()
    
    print("\nGenerating UI icons...")
    generator.generate_ui_icons()
    
    print("\nSaving prompts log...")
    generator.save_prompts_log()
    
    print("\n=== GENERATION COMPLETE ===")
    print("Next steps:")
    print("1. Run: make cleanbg  (remove backgrounds)")
    print("2. Run: make atlas   (create sprite atlases)")
    print("3. Run: make pack    (copy to assets/)")
    print("4. Run: cargo run    (test in game)")

if __name__ == "__main__":
    main()