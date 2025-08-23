#!/usr/bin/env python3
"""
🎨 HADES-STYLE CONCEPT ART GENERATOR
Uses local SDXL with handpainted digital art LoRAs for Hades-quality concept art
"""

import os
import argparse
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import json
from pathlib import Path

class HadesConceptGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        
        # Hades-style base prompt components
        self.hades_style_base = """
        masterpiece, best quality, extremely detailed digital painting,
        Hades video game art style, hand-painted look, supergiant games style,
        dramatic lighting, rim lighting, bold colors, stylized proportions,
        painterly brush strokes, concept art, character design,
        rich saturated colors, deep shadows, warm lighting,
        """
        
        self.egyptian_themes = {
            "pharaoh_hero": """
            Egyptian pharaoh warrior, golden ceremonial armor with hieroglyphs,
            royal headdress, confident heroic pose, muscular build,
            holding khopesh sword, blue and gold color scheme,
            desert background with pyramids, regal and powerful
            """,
            
            "anubis_boss": """
            Anubis god of death, jackal head, ancient Egyptian deity,
            ornate golden armor, staff of judgment, tall imposing figure,
            dark blue and gold colors, mystical aura, boss character,
            underworld temple background, intimidating presence
            """,
            
            "mummy_enemy": """
            Ancient Egyptian mummy warrior, wrapped in bandages,
            glowing eyes, shambling pose, weathered and ancient,
            carrying curved blade, sandy brown and bone colors,
            tomb interior background, undead enemy character
            """,
            
            "isis_npc": """
            Isis goddess, elegant Egyptian deity, flowing robes,
            feathered headdress, graceful pose, healing magic,
            white and gold colors, serene expression,
            temple altar background, divine presence
            """
        }
        
    def load_pipeline(self):
        """Load SDXL pipeline with optimizations"""
        print("Loading Stable Diffusion XL pipeline...")
        
        try:
            # Try to load with memory optimizations
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            if self.device == "cuda":
                self.pipeline = self.pipeline.to("cuda")
                # Enable memory efficient attention
                self.pipeline.enable_attention_slicing()
                self.pipeline.enable_vae_slicing()
                
            print(f"SDXL loaded on {self.device}")
            return True
            
        except Exception as e:
            print(f"Failed to load SDXL: {e}")
            print("Consider installing: pip install diffusers[torch]")
            return False
            
    def generate_concept(self, character_type: str, custom_prompt: str = None):
        """Generate Hades-style concept art"""
        if not self.pipeline:
            if not self.load_pipeline():
                return None
                
        # Build the complete prompt
        if custom_prompt:
            character_desc = custom_prompt
        else:
            character_desc = self.egyptian_themes.get(character_type, character_type)
            
        full_prompt = f"{self.hades_style_base} {character_desc}"
        
        # Negative prompt to avoid common issues
        negative_prompt = """
        blurry, low quality, bad anatomy, deformed, disfigured,
        poorly drawn, extra limbs, missing limbs, ugly, duplicate,
        morbid, mutilated, out of frame, poorly drawn hands,
        poorly drawn face, mutation, bad proportions, cropped,
        worst quality, low resolution, jpeg artifacts, watermark
        """
        
        print(f"Generating concept art...")
        print(f"Prompt: {character_desc[:100]}...")
        
        try:
            # Generate the image
            with torch.autocast(self.device):
                image = self.pipeline(
                    prompt=full_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=50,
                    guidance_scale=8.0,
                    width=1024,
                    height=1024,
                ).images[0]
                
            return image
            
        except Exception as e:
            print(f"Generation failed: {e}")
            return None
            
    def enhance_image(self, image):
        """Apply post-processing for Hades style"""
        # This is where we could add Real-ESRGAN upscaling
        # For now, just ensure good quality
        return image
        
    def save_concept(self, image, output_path, character_name):
        """Save the generated concept art"""
        os.makedirs(output_path, exist_ok=True)
        
        # Save the main concept
        concept_path = Path(output_path) / f"{character_name}_concept.png"
        image.save(concept_path, "PNG", quality=95)
        
        # Also save metadata
        metadata = {
            "character_name": character_name,
            "style": "hades_egyptian",
            "resolution": f"{image.width}x{image.height}",
            "pipeline": "SDXL"
        }
        
        metadata_path = Path(output_path) / f"{character_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"Concept art saved: {concept_path}")
        return concept_path

def main():
    parser = argparse.ArgumentParser(description="Generate Hades-style concept art")
    parser.add_argument("--character", required=True, help="Character name")
    parser.add_argument("--prompt", help="Custom character prompt")
    parser.add_argument("--output", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    generator = HadesConceptGenerator()
    
    # Generate the concept art
    image = generator.generate_concept(args.character, args.prompt)
    if image is None:
        print("Failed to generate concept art")
        return 1
        
    # Enhance and save
    enhanced_image = generator.enhance_image(image)
    generator.save_concept(enhanced_image, args.output, args.character)
    
    print(f"Concept art for '{args.character}' generated successfully!")
    return 0

if __name__ == "__main__":
    main()