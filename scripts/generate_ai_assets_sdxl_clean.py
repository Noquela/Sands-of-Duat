"""
Generate AI Assets using SDXL Pipeline
Uses the existing art pipeline to generate real Hades-quality assets.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sands_of_duat.assets.art_pipeline import egyptian_art_pipeline, AssetType, EgyptianStyle

# Configure logging to see progress
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def generate_ai_card_frames():
    """Generate card frames using SDXL AI pipeline."""
    print("SPRINT 1 - AI-Generated Card Frames with SDXL")
    print("=" * 55)
    
    # Initialize the art pipeline
    if not await egyptian_art_pipeline.initialize():
        print("Failed to initialize AI pipeline")
        return False
    
    print("[OK] SDXL Pipeline initialized successfully!")
    
    # Card frame specifications
    card_frames = {
        'common_frame': {
            'prompt': 'ancient egyptian card frame, simple bronze borders, weathered stone texture, hieroglyphic patterns, game UI element, hades video game style, clean design, symmetrical',
            'style': EgyptianStyle.HIEROGLYPHIC,
            'size': (512, 768)
        },
        'rare_frame': {
            'prompt': 'ancient egyptian card frame, silver borders with lapis lazuli accents, flowing hieroglyphic patterns, polished stone texture, game UI element, hades video game style',
            'style': EgyptianStyle.MYSTICAL,
            'size': (512, 768)
        },
        'epic_frame': {
            'prompt': 'ancient egyptian card frame, golden borders with amethyst gems, intricate hieroglyphic carvings, divine aura, game UI element, hades video game style, majestic',
            'style': EgyptianStyle.GOLDEN,
            'size': (1024, 1536)
        },
        'legendary_frame': {
            'prompt': 'ancient egyptian card frame, divine golden borders, cosmic energy, celestial hieroglyphs, radiant divine power, game UI element, hades video game style, legendary quality',
            'style': EgyptianStyle.GOLDEN,
            'size': (1024, 1536)
        }
    }
    
    output_dir = Path("assets/approved_hades_quality/card_frame")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for frame_name, config in card_frames.items():
        output_path = output_dir / f"{frame_name}.png"
        
        print(f"\nGenerating AI {frame_name}...")
        print(f"   Prompt: {config['prompt'][:50]}...")
        
        try:
            # Generate using the art pipeline
            image = await egyptian_art_pipeline.generate_asset(
                asset_type=AssetType.CARD_FRAME,
                name=frame_name,
                prompt=config['prompt'],
                style=config['style'],
                size=config['size'],
                steps=25,
                guidance_scale=7.5
            )
            
            if image:
                image.save(output_path)
                print(f"Generated AI asset: {output_path}")
            else:
                print(f"Failed to generate {frame_name}")
                
        except Exception as e:
            print(f"Error generating {frame_name}: {e}")
    
    print("\nAI Card frame generation complete!")
    return True

async def generate_ai_ui_elements():
    """Generate UI elements using SDXL AI pipeline."""
    print("\nAI-Generated UI Elements with SDXL")
    print("=" * 45)
    
    # UI element specifications  
    ui_elements = {
        'ui_health_icon': {
            'prompt': 'egyptian ankh symbol, health icon, golden bronze metal, divine life symbol, game UI element, hades video game style, clean icon design, 64x64 pixel perfect',
            'style': EgyptianStyle.GOLDEN
        },
        'ui_mana_icon': {
            'prompt': 'egyptian scarab beetle, mana energy icon, lapis lazuli blue gem, magical power symbol, game UI element, hades video game style, clean icon design',
            'style': EgyptianStyle.MYSTICAL
        },
        'ui_attack_icon': {
            'prompt': 'egyptian khopesh sword, attack icon, bronze weapon, warrior symbol, game UI element, hades video game style, clean icon design',
            'style': EgyptianStyle.CLASSICAL
        },
        'ui_shield_icon': {
            'prompt': 'egyptian shield with eye of horus, defense icon, golden protection symbol, divine guardian, game UI element, hades video game style, clean icon design',
            'style': EgyptianStyle.GOLDEN
        }
    }
    
    output_dir = Path("assets/approved_hades_quality/ui_elements")
    
    for element_name, config in ui_elements.items():
        output_path = output_dir / f"{element_name}.png"
        
        print(f"\nGenerating AI {element_name}...")
        
        try:
            # Generate using the art pipeline
            image = await egyptian_art_pipeline.generate_asset(
                asset_type=AssetType.UI_ELEMENT,
                name=element_name,
                prompt=config['prompt'],
                style=config['style'],
                size=(512, 512),  # UI elements are square
                steps=20,
                guidance_scale=8.0
            )
            
            if image:
                image.save(output_path)
                print(f"Generated AI UI element: {output_path}")
            else:
                print(f"Failed to generate {element_name}")
                
        except Exception as e:
            print(f"Error generating {element_name}: {e}")
    
    print("\nAI UI elements generation complete!")

async def main():
    """Main generation workflow."""
    print("SANDS OF DUAT - AI Asset Generation with SDXL")
    print("=" * 60)
    
    # Check GPU
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory // 1024**3
            print(f"GPU: {gpu_name} ({memory_gb}GB VRAM)")
        else:
            print("Warning: Using CPU - will be slower")
    except ImportError:
        print("Error: PyTorch not available")
        return
    
    # Generate assets
    success = await generate_ai_card_frames()
    if success:
        await generate_ai_ui_elements()
    
    print("\nAI Asset generation complete! Ready for Hades-quality game experience!")

if __name__ == "__main__":
    asyncio.run(main())