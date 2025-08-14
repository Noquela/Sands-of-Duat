"""
Generate Missing Card Frames - Hades Quality
Creates Egyptian-themed card frames for common and rare rarities.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

async def generate_card_frames():
    """Generate missing card frames with Hades-quality styling."""
    print("SPRINT 1 Priority 2 - Missing Card Frames Generation")
    print("=" * 60)
    
    # Check for AI availability
    try:
        import torch
        print("Torch available")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("CPU mode - will be slower")
    except ImportError:
        print("AI libraries not available - using fallback generation")
        await generate_fallback_frames()
        return
    
    # Use fallback generation since AI pipeline method is not available
    print("Using fallback generation for card frames")
    await generate_fallback_frames()
    return
    
    # Try to use existing art pipeline (disabled for now)
    try:
        from sands_of_duat.assets.art_pipeline import egyptian_art_pipeline
        
        # Define card frame prompts in Hades style
        card_frame_prompts = {
            'common_frame': {
                'prompt': 'Hades game style, ancient Egyptian card frame, simple bronze borders, hieroglyphic patterns, weathered stone texture, minimal ornamentation, game UI element, clean design',
                'negative': 'oversaturated, modern, plastic, too ornate, cluttered',
                'size': (512, 768)
            },
            'rare_frame': {
                'prompt': 'Hades game style, ancient Egyptian card frame, silver borders with lapis lazuli accents, flowing hieroglyphic patterns, polished stone texture, moderate ornamentation, game UI element', 
                'negative': 'oversaturated, modern, plastic, too simple, too ornate',
                'size': (512, 768)
            }
        }
        
        # Generate missing frames
        output_dir = Path("assets/approved_hades_quality/card_frame")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for frame_name, config in card_frame_prompts.items():
            output_path = output_dir / f"{frame_name}.png"
            
            if output_path.exists():
                print(f"[OK] {frame_name} already exists")
                continue
                
            print(f"Generating {frame_name}...")
            try:
                # Use the art pipeline to generate
                image = await egyptian_art_pipeline.generate_image(
                    prompt=config['prompt'],
                    negative_prompt=config['negative'],
                    width=config['size'][0],
                    height=config['size'][1],
                    steps=25,
                    guidance_scale=7.5
                )
                
                if image:
                    image.save(output_path)
                    print(f"Generated: {output_path}")
                else:
                    print(f"Failed to generate {frame_name}")
                    
            except Exception as e:
                print(f"Error generating {frame_name}: {e}")
        
        print("\nCard frame generation complete!")
        
    except ImportError:
        print("Art pipeline not available - using fallback")
        await generate_fallback_frames()

async def generate_fallback_frames():
    """Generate simple fallback card frames using pygame."""
    print("Generating fallback card frames...")
    
    try:
        import pygame
        import numpy as np
        
        pygame.init()
        
        # Card frame specs
        width, height = 512, 768
        border_width = 12
        
        frames = {
            'common_frame': {
                'border_color': (139, 115, 85),  # Bronze
                'inner_color': (101, 83, 65),
                'accent_color': (180, 150, 120)
            },
            'rare_frame': {
                'border_color': (64, 130, 178),  # Lapis lazuli blue 
                'inner_color': (45, 95, 130),
                'accent_color': (90, 160, 200)
            }
        }
        
        output_dir = Path("assets/approved_hades_quality/card_frame")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for frame_name, colors in frames.items():
            output_path = output_dir / f"{frame_name}.png"
            
            if output_path.exists():
                print(f"[OK] {frame_name} already exists")
                continue
                
            print(f"Creating fallback {frame_name}...")
            
            # Create surface
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))  # Transparent background
            
            # Outer border
            pygame.draw.rect(surface, colors['border_color'], 
                           (0, 0, width, height), border_width, border_radius=16)
            
            # Inner border with accent
            inner_rect = pygame.Rect(border_width//2, border_width//2, 
                                   width - border_width, height - border_width)
            pygame.draw.rect(surface, colors['inner_color'], inner_rect, 
                           border_width//2, border_radius=12)
            
            # Decorative corners
            corner_size = 32
            corner_rects = [
                (border_width, border_width, corner_size, corner_size),  # Top-left
                (width - border_width - corner_size, border_width, corner_size, corner_size),  # Top-right
                (border_width, height - border_width - corner_size, corner_size, corner_size),  # Bottom-left
                (width - border_width - corner_size, height - border_width - corner_size, corner_size, corner_size)  # Bottom-right
            ]
            
            for rect in corner_rects:
                pygame.draw.rect(surface, colors['accent_color'], rect, 2, border_radius=4)
            
            # Save the frame
            pygame.image.save(surface, str(output_path))
            print(f"Created fallback: {output_path}")
        
        pygame.quit()
        print("Fallback card frames generated!")
        
    except ImportError:
        print("Pygame not available - cannot generate fallback frames")
    except Exception as e:
        print(f"Error in fallback generation: {e}")

if __name__ == "__main__":
    asyncio.run(generate_card_frames())