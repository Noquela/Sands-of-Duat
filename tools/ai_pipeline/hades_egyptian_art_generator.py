#!/usr/bin/env python3
"""
Hades-Quality Egyptian Art Generator
RTX 5070 optimized - uses local diffusers for high-quality art generation
Focused on creating Hades-style Egyptian game assets
"""

import os
import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline, AutoencoderKL
from diffusers import DDIMScheduler, EulerDiscreteScheduler
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
import json
from datetime import datetime

class HadesEgyptianArtGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models_dir = Path("tools/ai_pipeline/models")
        self.output_dir = Path("tools/ai_pipeline/outputs")
        
        # RTX 5070 optimizations
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        
        self.pipeline = None
        self.refiner = None
        
    def setup_models(self):
        """Setup SDXL models optimized for RTX 5070"""
        print("Setting up SDXL models for RTX 5070...")
        
        try:
            # Use Hugging Face models directly (no download needed)
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True,
                device_map="auto"
            ).to(self.device)
            
            # Enable memory efficient attention
            self.pipeline.enable_model_cpu_offload()
            self.pipeline.enable_vae_slicing()
            self.pipeline.enable_attention_slicing(1)
            
            print("SDXL Base model loaded successfully")
            
        except Exception as e:
            print(f"Error loading SDXL: {e}")
            print("Using alternative setup...")
            self.setup_alternative_pipeline()
    
    def setup_alternative_pipeline(self):
        """Alternative pipeline if SDXL fails"""
        try:
            from diffusers import StableDiffusionPipeline
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16,
                safety_checker=None,
                requires_safety_checker=False
            ).to(self.device)
            
            self.pipeline.enable_attention_slicing()
            print("Alternative SD 1.5 model loaded")
            
        except Exception as e:
            print(f"Failed to load models: {e}")
            raise
    
    def get_hades_egyptian_prompts(self):
        """Hades-style Egyptian character prompts"""
        return {
            "pharaoh_hero": {
                "positive": """masterpiece, best quality, highly detailed, professional game art, 
                Hades game art style, Egyptian pharaoh warrior hero, golden royal armor with intricate hieroglyphs, 
                ornate khopesh sword, cobra crown headdress, confident heroic pose, dramatic cinematic lighting, 
                rich saturated colors, hand-painted texture style, stylized proportions, 
                desert tomb background, dynamic action pose, 4K resolution, trending on artstation""",
                
                "negative": """low quality, blurry, pixelated, amateur, simple, flat lighting, 
                modern clothing, realistic photography, plain background, boring pose, 
                low resolution, bad anatomy, deformed, ugly, watermark"""
            },
            
            "anubis_boss": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, Anubis Egyptian jackal god boss, powerful intimidating build, 
                ornate black and gold armor, glowing amber eyes, ceremonial staff weapon, 
                dramatic boss pose, threatening stance, epic dramatic lighting, 
                rich dark colors with gold accents, hand-painted texture style, 
                stylized muscular proportions, ancient temple background, 4K resolution""",
                
                "negative": """low quality, blurry, pixelated, amateur, simple, flat lighting, 
                cute, friendly, modern, realistic photography, plain background, 
                weak pose, low resolution, bad anatomy, deformed"""
            },
            
            "mummy_enemy": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, ancient Egyptian mummy warrior enemy, wrapped linen bandages, 
                glowing green curse eyes, ornate tomb guardian armor, weathered ancient weapons, 
                menacing combat pose, eerie atmospheric lighting, muted earth tones with green glow, 
                hand-painted texture style, stylized undead proportions, 
                dark tomb corridor background, 4K resolution""",
                
                "negative": """low quality, blurry, pixelated, amateur, simple, flat lighting, 
                modern, clean, bright colors, realistic photography, 
                plain background, friendly pose, low resolution, bad anatomy"""
            },
            
            "isis_npc": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, Isis Egyptian goddess NPC, elegant graceful beauty, 
                flowing ornate robes, golden winged headdress, divine jewelry, 
                welcoming peaceful pose, soft ethereal lighting, rich blue and gold colors, 
                hand-painted texture style, stylized feminine proportions, 
                celestial temple background, magical aura, 4K resolution""",
                
                "negative": """low quality, blurry, pixelated, amateur, simple, flat lighting, 
                modern clothing, aggressive pose, dark colors, realistic photography, 
                plain background, low resolution, bad anatomy, deformed"""
            }
        }
    
    def generate_character_concept(self, character_name, variations=4):
        """Generate high-quality character concept art"""
        print(f"Generating Hades-quality concept art for {character_name}...")
        
        if not self.pipeline:
            self.setup_models()
        
        prompts = self.get_hades_egyptian_prompts()
        if character_name not in prompts:
            print(f"Character {character_name} not found in prompts")
            return None
        
        character_prompt = prompts[character_name]
        output_paths = []
        
        for i in range(variations):
            print(f"  Generating variation {i+1}/{variations}...")
            
            # Generate base image
            image = self.pipeline(
                prompt=character_prompt["positive"],
                negative_prompt=character_prompt["negative"],
                height=1024,
                width=1024,
                num_inference_steps=30,
                guidance_scale=8.5,
                generator=torch.Generator(device=self.device).manual_seed(42 + i)
            ).images[0]
            
            # Post-process for game art quality
            enhanced_image = self.enhance_for_game_art(image)
            
            # Save image
            output_path = self.output_dir / "characters" / f"{character_name}_concept_v{i+1}.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            enhanced_image.save(output_path)
            
            # Save metadata
            metadata = {
                "character": character_name,
                "variation": i + 1,
                "prompt": character_prompt["positive"],
                "negative_prompt": character_prompt["negative"],
                "generated_at": datetime.now().isoformat(),
                "model": "SDXL",
                "resolution": "1024x1024"
            }
            
            metadata_path = output_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            output_paths.append(output_path)
            print(f"    Saved: {output_path}")
        
        print(f"Generated {len(output_paths)} concept variations for {character_name}")
        return output_paths
    
    def enhance_for_game_art(self, image):
        """Post-process image for game art quality"""
        # Increase saturation for vibrant game art look
        enhancer = ImageEnhance.Color(image)
        enhanced = enhancer.enhance(1.3)
        
        # Increase contrast for dramatic effect
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.2)
        
        # Slight sharpening
        enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        return enhanced
    
    def generate_environment_concept(self, environment_type="egyptian_tomb"):
        """Generate environment concept art"""
        print(f"Generating environment concept: {environment_type}")
        
        environment_prompts = {
            "egyptian_tomb": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, ancient Egyptian tomb interior, ornate hieroglyph walls, 
                dramatic torch lighting, stone pillars and statues, gold treasure scattered, 
                atmospheric dust particles, rich earth tones with golden highlights, 
                cinematic composition, hand-painted texture style, 4K resolution""",
                
                "negative": """low quality, modern, bright daylight, clean, simple, 
                realistic photography, plain walls, empty space, low resolution"""
            },
            
            "pharaoh_throne_room": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, Egyptian pharaoh throne room, massive golden throne, 
                ornate columns with hieroglyphs, ceremonial braziers, rich tapestries, 
                dramatic royal lighting, opulent gold and blue colors, 
                majestic composition, hand-painted texture style, 4K resolution""",
                
                "negative": """low quality, simple, modern, plain, realistic photography, 
                empty space, bright lighting, low resolution"""
            }
        }
        
        if environment_type not in environment_prompts:
            environment_type = "egyptian_tomb"
        
        prompt_data = environment_prompts[environment_type]
        
        if not self.pipeline:
            self.setup_models()
        
        image = self.pipeline(
            prompt=prompt_data["positive"],
            negative_prompt=prompt_data["negative"],
            height=768,
            width=1024,
            num_inference_steps=35,
            guidance_scale=9.0,
            generator=torch.Generator(device=self.device).manual_seed(123)
        ).images[0]
        
        enhanced_image = self.enhance_for_game_art(image)
        
        output_path = self.output_dir / "environments" / f"{environment_type}_concept.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        enhanced_image.save(output_path)
        
        print(f"Environment concept saved: {output_path}")
        return output_path
    
    def batch_generate_all_characters(self):
        """Generate concept art for all main characters"""
        characters = ["pharaoh_hero", "anubis_boss", "mummy_enemy", "isis_npc"]
        all_paths = {}
        
        for character in characters:
            paths = self.generate_character_concept(character, variations=3)
            all_paths[character] = paths
        
        return all_paths

def main():
    generator = HadesEgyptianArtGenerator()
    
    print("Starting Hades-Quality Egyptian Art Generation...")
    print("Optimized for RTX 5070 - 12GB VRAM")
    
    # Generate all character concepts
    all_concepts = generator.batch_generate_all_characters()
    
    # Generate environment concepts
    generator.generate_environment_concept("egyptian_tomb")
    generator.generate_environment_concept("pharaoh_throne_room")
    
    print("\nHades-Quality Art Generation Complete!")
    print(f"Generated concepts for {len(all_concepts)} characters")
    print("Check 'tools/ai_pipeline/outputs/' for results")

if __name__ == "__main__":
    main()