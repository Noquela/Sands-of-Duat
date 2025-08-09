#!/usr/bin/env python3
"""
IMPROVED ASSET REGENERATION FOR SANDS OF DUAT
============================================

Fixed generation strategy addressing quality issues:
- No watermarks or text overlays
- Consistent Hades-level artistic style
- Single focused elements per asset
- Proper Egyptian authentic styling
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time

# Optimized generation settings
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
ASSETS_PATH = Path("../assets/generated_art")

def initialize_pipeline():
    """Initialize SDXL pipeline with optimal settings."""
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        variant="fp16" if DEVICE == "cuda" else None,
        use_safetensors=True
    )
    
    pipe = pipe.to(DEVICE)
    pipe.enable_model_cpu_offload()
    
    return pipe

def create_improved_prompts():
    """Create improved prompts with no watermarks and consistent style."""
    
    # Base style prompt for consistency
    base_style = """
    masterpiece, highest quality, professional game art,
    Supergiant Games Hades art style, hand painted illustration,
    rich saturated colors, dramatic lighting, painterly texture,
    no text, no watermarks, no logos, clean single subject
    """
    
    # Improved UI prompts (single elements, no watermarks)
    ui_prompts = {
        'ui_card_frame_legendary': f"""
        {base_style}, ornate golden Egyptian card frame, 
        ancient hieroglyphic decorations, precious gems, 
        royal blue and gold colors, luxury border design,
        single frame only, transparent background
        """,
        
        'ui_card_frame_epic': f"""
        {base_style}, elegant silver Egyptian card frame,
        turquoise and silver accents, mystical symbols,
        refined border decoration, single frame only,
        transparent background
        """,
        
        'ui_play_button': f"""
        {base_style}, Egyptian stone play button,
        ankh symbol carved in center, sandstone texture,
        golden highlights, single button element,
        game UI design, no text overlays
        """,
        
        'ui_settings_button': f"""
        {base_style}, Egyptian gear button design,
        golden mechanical scarab motif, intricate details,
        single button element, game UI style,
        no text or watermarks
        """
    }
    
    # Improved character prompts (consistent realistic style)
    character_prompts = {
        'char_player_hero': f"""
        {base_style}, Egyptian warrior hero character,
        realistic painted portrait, strong determined face,
        traditional Egyptian armor and headwear,
        dramatic lighting, heroic pose, desert background,
        Hades character art quality
        """,
        
        'char_anubis_boss': f"""
        {base_style}, Anubis god boss character,
        imposing jackal-headed deity, golden armor,
        divine radiance, commanding presence,
        Egyptian underworld setting, epic boss design
        """
    }
    
    return ui_prompts, character_prompts

def regenerate_problematic_assets(pipe):
    """Regenerate the most problematic assets with improved prompts."""
    
    ui_prompts, character_prompts = create_improved_prompts()
    
    # Regenerate UI elements (biggest problems)
    print("Regenerating UI elements...")
    for filename, prompt in ui_prompts.items():
        print(f"Generating {filename}...")
        
        image = pipe(
            prompt=prompt,
            negative_prompt="text, watermarks, logos, multiple frames, blur, low quality, distorted",
            num_inference_steps=30,
            guidance_scale=9.0,
            width=512,
            height=512,
            generator=torch.Generator(device=DEVICE).manual_seed(42)
        ).images[0]
        
        output_path = ASSETS_PATH / f"{filename}.png"
        image.save(output_path)
        print(f"Saved: {output_path}")
        time.sleep(2)  # Prevent overheating
    
    # Regenerate character portraits (style inconsistency)
    print("Regenerating character portraits...")
    for filename, prompt in character_prompts.items():
        print(f"Generating {filename}...")
        
        image = pipe(
            prompt=prompt,
            negative_prompt="cartoon, anime, watermarks, text, blur, low quality",
            num_inference_steps=30,
            guidance_scale=8.5,
            width=512,
            height=768,
            generator=torch.Generator(device=DEVICE).manual_seed(123)
        ).images[0]
        
        output_path = ASSETS_PATH / f"{filename}.png"
        image.save(output_path)
        print(f"Saved: {output_path}")
        time.sleep(2)

def main():
    """Main regeneration process."""
    print("STARTING IMPROVED ASSET REGENERATION")
    print("Addressing watermarks, style inconsistencies, and quality issues")
    
    # Initialize pipeline
    print("Initializing SDXL pipeline...")
    pipe = initialize_pipeline()
    
    # Regenerate problematic assets
    regenerate_problematic_assets(pipe)
    
    print("ASSET REGENERATION COMPLETE!")
    print("Fixed issues:")
    print("- Removed watermarks and text overlays")
    print("- Created single focused UI elements")
    print("- Consistent realistic art style for characters")
    print("- Proper Egyptian authentic styling")

if __name__ == "__main__":
    main()