#!/usr/bin/env python3
"""
Cinematic Egyptian Environment Generator
Creates Hades-quality Egyptian environments for the roguelike
Following the Egyptian Art Bible standards
"""

import os
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
import json
from datetime import datetime

class CinematicEnvironmentGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = Path("tools/ai_pipeline/outputs/environments")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # RTX 5070 optimizations
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        
        self.pipeline = None
        
    def setup_pipeline(self):
        """Setup SDXL pipeline for environment generation"""
        print("Setting up environment generation pipeline...")
        
        try:
            # Use alternative pipeline for compatibility
            from diffusers import StableDiffusionPipeline
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16,
                safety_checker=None,
                requires_safety_checker=False
            ).to(self.device)
            
            self.pipeline.enable_attention_slicing()
            print("Environment generation pipeline ready")
            
        except Exception as e:
            print(f"Failed to load pipeline: {e}")
            raise
    
    def get_environment_prompts(self):
        """Hades-style Egyptian environment prompts"""
        return {
            "pharaoh_tomb_chamber": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, ancient Egyptian pharaoh tomb chamber, massive stone sarcophagus,
                golden treasures scattered, ornate hieroglyphic wall murals, dramatic torch lighting,
                atmospheric dust particles, rich earth tones with golden highlights, mysterious shadows,
                carved stone pillars, ceremonial canopic jars, cinematic composition,
                hand-painted texture style, epic scale architecture, 4K resolution""",
                
                "negative": """low quality, modern, bright daylight, clean, simple, plain walls,
                empty space, realistic photography, amateur, blurry, pixelated"""
            },
            
            "temple_of_gods": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, massive Egyptian temple interior, towering stone columns,
                ornate golden altar, hieroglyphic inscriptions, divine blue lighting,
                ceremonial braziers with flickering flames, majestic throne room,
                rich blue and gold color scheme, dramatic perspective, atmospheric haze,
                hand-painted texture style, cinematic lighting, 4K resolution""",
                
                "negative": """low quality, small scale, modern, bright lighting, simple, plain,
                realistic photography, empty space, amateur, blurry"""
            },
            
            "underworld_passage": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, ancient Egyptian underworld corridor, flowing sand waterfalls,
                ghostly green mist, ornate stone archways, mysterious hieroglyphic symbols,
                eerie supernatural lighting, floating particles, ancient mechanisms,
                dark obsidian colors with emerald glow, foreboding atmosphere,
                hand-painted texture style, cinematic depth, 4K resolution""",
                
                "negative": """low quality, bright, cheerful, modern, simple, plain walls,
                realistic photography, amateur, blurry, low resolution"""
            },
            
            "hall_of_judgment": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, Egyptian hall of judgment, massive scales of justice,
                towering Anubis statues, ornate pillars with hieroglyphs, divine lighting,
                ceremonial pedestals, golden Egyptian artifacts, dramatic shadows,
                rich dark blues and golds, mystical atmosphere, floating divine particles,
                hand-painted texture style, epic architectural scale, 4K resolution""",
                
                "negative": """low quality, small scale, modern, bright, simple, plain,
                realistic photography, empty, amateur, blurry"""
            },
            
            "desert_oasis_sanctuary": {
                "positive": """masterpiece, best quality, highly detailed, professional game art,
                Hades game art style, magical Egyptian desert oasis, crystal clear water,
                ornate pavilion with silk curtains, date palm trees, golden sand dunes,
                warm sunset lighting, magical shimmer effects, rich warm colors,
                peaceful sanctuary atmosphere, ornate rugs and cushions,
                hand-painted texture style, cinematic beauty, 4K resolution""",
                
                "negative": """low quality, dark, gloomy, modern, simple, realistic photography,
                plain, amateur, blurry, low resolution"""
            }
        }
    
    def generate_environment_concept(self, environment_name, variations=2):
        """Generate high-quality environment concept art"""
        print(f"Generating cinematic environment: {environment_name}...")
        
        if not self.pipeline:
            self.setup_pipeline()
        
        prompts = self.get_environment_prompts()
        if environment_name not in prompts:
            print(f"Environment {environment_name} not found in prompts")
            return None
        
        environment_prompt = prompts[environment_name]
        output_paths = []
        
        for i in range(variations):
            print(f"  Generating variation {i+1}/{variations}...")
            
            # Generate base image with cinematic aspect ratio
            image = self.pipeline(
                prompt=environment_prompt["positive"],
                negative_prompt=environment_prompt["negative"],
                height=768,  # Cinematic height
                width=1024,  # Wider for environment shots
                num_inference_steps=35,
                guidance_scale=9.0,
                generator=torch.Generator(device=self.device).manual_seed(100 + i)
            ).images[0]
            
            # Post-process for cinematic quality
            enhanced_image = self.enhance_for_cinematic_quality(image)
            
            # Save image
            output_path = self.output_dir / f"{environment_name}_v{i+1}.png"
            enhanced_image.save(output_path)
            
            # Save metadata
            metadata = {
                "environment": environment_name,
                "variation": i + 1,
                "prompt": environment_prompt["positive"],
                "negative_prompt": environment_prompt["negative"],
                "generated_at": datetime.now().isoformat(),
                "aspect_ratio": "cinematic_16_9",
                "resolution": "1024x768",
                "art_style": "Hades_Egyptian_Cinematic"
            }
            
            metadata_path = output_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            output_paths.append(output_path)
            print(f"    Saved: {output_path}")
        
        print(f"Generated {len(output_paths)} environment variations for {environment_name}")
        return output_paths
    
    def enhance_for_cinematic_quality(self, image):
        """Post-process image for cinematic environment quality"""
        # Increase contrast for dramatic effect
        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(1.4)
        
        # Increase saturation for rich colors
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.2)
        
        # Slight vignetting effect for cinematic look
        # Create vignette mask
        width, height = enhanced.size
        vignette = Image.new('RGB', (width, height), (255, 255, 255))
        
        # Create gradient from center
        for y in range(height):
            for x in range(width):
                # Distance from center
                dist_x = abs(x - width/2) / (width/2)
                dist_y = abs(y - height/2) / (height/2)
                distance = (dist_x**2 + dist_y**2)**0.5
                
                # Vignette strength
                vignette_strength = max(0, 1 - distance * 0.8)
                brightness = int(255 * vignette_strength)
                
                if distance > 1.0:
                    brightness = int(255 * 0.2)  # Dark edges
        
        # Apply subtle sharpening
        enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
        
        return enhanced
    
    def batch_generate_all_environments(self):
        """Generate all Egyptian environments for the game"""
        environments = [
            "pharaoh_tomb_chamber",
            "temple_of_gods", 
            "underworld_passage",
            "hall_of_judgment",
            "desert_oasis_sanctuary"
        ]
        
        all_paths = {}
        
        for environment in environments:
            paths = self.generate_environment_concept(environment, variations=2)
            all_paths[environment] = paths
        
        return all_paths
    
    def create_environment_report(self, generated_environments):
        """Create a report of generated environments"""
        report = {
            "generation_summary": {
                "total_environments": len(generated_environments),
                "total_variations": sum(len(paths) for paths in generated_environments.values() if paths),
                "art_style": "Hades_Egyptian_Cinematic",
                "resolution": "1024x768_cinematic",
                "generated_at": datetime.now().isoformat()
            },
            "environments": {}
        }
        
        for env_name, paths in generated_environments.items():
            if paths:
                report["environments"][env_name] = {
                    "variations_count": len(paths),
                    "paths": [str(path) for path in paths],
                    "status": "success",
                    "quality": "Cinematic_Hades_Style"
                }
            else:
                report["environments"][env_name] = {
                    "status": "failed"
                }
        
        report_path = self.output_dir / "environment_generation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Environment report saved: {report_path}")

def main():
    generator = CinematicEnvironmentGenerator()
    
    print("CINEMATIC EGYPTIAN ENVIRONMENT GENERATION")
    print("Creating Hades-quality environments for the roguelike")
    print("Following Egyptian Art Bible standards")
    
    # Generate all environments
    all_environments = generator.batch_generate_all_environments()
    
    # Create generation report
    generator.create_environment_report(all_environments)
    
    print(f"\nCinematic Environment Generation Complete!")
    total_generated = sum(len(paths) for paths in all_environments.values() if paths)
    print(f"Generated {total_generated} environment variations across {len(all_environments)} locations")
    print(f"Environments saved to: {generator.output_dir}")

if __name__ == "__main__":
    main()