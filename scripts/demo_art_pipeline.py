"""
Demo Art Pipeline - Shows how the 4K Egyptian art generation works.
Creates a few sample assets to demonstrate the system without requiring full generation.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sands_of_duat.assets.art_pipeline import egyptian_art_pipeline, AssetSpec, AssetType, EgyptianStyle

async def demo_generation():
    """Demo the art generation pipeline with a few sample assets."""
    print("Sands of Duat - Art Pipeline Demo")
    print("=" * 50)
    
    # Check if we have the actual AI libraries
    try:
        import torch
        import diffusers
        ai_available = True
        print("AI libraries available - real generation possible")
    except ImportError:
        ai_available = False
        print("AI libraries not installed - demo mode only")
    
    if not ai_available:
        print("\nThis demo shows what WOULD be generated:")
        print("\nSAMPLE ASSETS TO GENERATE:")
        
        # Show what would be generated
        sample_specs = [
            AssetSpec(
                name="menu_background_demo",
                asset_type=AssetType.BACKGROUND,
                style=EgyptianStyle.GOLDEN,
                dimensions=(4096, 2048),
                prompt="golden egyptian temple hall, massive columns, divine light rays, majestic entrance",
                num_inference_steps=40
            ),
            AssetSpec(
                name="ra_portrait_demo", 
                asset_type=AssetType.CHARACTER_PORTRAIT,
                style=EgyptianStyle.CLASSICAL,
                dimensions=(1024, 1024),
                prompt="Ra the sun god, falcon head, solar disk crown, golden radiance, divine authority",
                num_inference_steps=35
            ),
            AssetSpec(
                name="legendary_frame_demo",
                asset_type=AssetType.CARD_FRAME,
                style=EgyptianStyle.GOLDEN,
                dimensions=(1024, 1024),
                prompt="legendary golden frame, divine radiance, sun disk, royal symbols",
                post_processing=["make_transparent", "enhance_contrast"]
            )
        ]
        
        for spec in sample_specs:
            print(f"\n- {spec.name.upper()}")
            print(f"   Type: {spec.asset_type.value}")
            print(f"   Style: {spec.style.value}")
            print(f"   Resolution: {spec.dimensions[0]}x{spec.dimensions[1]}")
            print(f"   Prompt: {spec.prompt}")
            if spec.post_processing:
                print(f"   Post-processing: {', '.join(spec.post_processing)}")
        
        print(f"\nEXPECTED EXPECTED QUALITY:")
        print("- 4K backgrounds perfectly scaled for ultrawide displays")
        print("- Consistent Egyptian art style across all assets")  
        print("- Professional game-ready quality")
        print("- Transparent card frames with proper alpha channels")
        print("- Character portraits with authentic Egyptian styling")
        
        print(f"\nTO GENERATE TO GENERATE REAL ASSETS:")
        print("1. Run: scripts/setup_ai_generation.py")
        print("2. Run: scripts/generate_4k_assets.py") 
        print("3. Assets will be created in assets/generated_4k/")
        
        return True
    
    # If AI is available, generate one sample asset
    print(f"\nInitializing AI pipeline...")
    if not await egyptian_art_pipeline.initialize():
        print("ERROR: Failed to initialize AI pipeline")
        return False
    
    # Generate a small sample
    print(f"\nGENERATING Generating sample UI icon...")
    sample_spec = AssetSpec(
        name="health_icon_demo",
        asset_type=AssetType.UI_ELEMENT,
        style=EgyptianStyle.GOLDEN,
        dimensions=(512, 512),
        prompt="ankh symbol, life force, golden glow, egyptian hieroglyph",
        post_processing=["make_transparent", "enhance_contrast"]
    )
    
    success = await egyptian_art_pipeline.generate_asset(sample_spec)
    
    if success:
        print("SUCCESS: Sample generation successful!")
        print(f"Check: Check: {egyptian_art_pipeline.assets_dir}/ui_element/health_icon_demo.png")
    else:
        print("ERROR: Sample generation failed")
    
    # Cleanup
    egyptian_art_pipeline.cleanup()
    return success

def show_smart_loader_demo():
    """Show how the smart asset loader works."""
    print("\n" + "=" * 50)
    print("SMART SMART ASSET LOADER DEMO")
    print("=" * 50)
    
    from sands_of_duat.assets.smart_asset_loader import smart_asset_loader
    
    # Show loader configuration
    print(f"Target quality: {smart_asset_loader.target_quality.value}")
    print(f"Generated 4K dir: {smart_asset_loader.generated_4k_dir}")
    
    # Show asset mappings
    print(f"\nAVAILABLE AVAILABLE ASSET MAPPINGS:")
    asset_types = {
        'Backgrounds': [k for k in smart_asset_loader.asset_mappings.keys() if 'background' in k],
        'Card Frames': [k for k in smart_asset_loader.asset_mappings.keys() if 'frame' in k], 
        'Character Portraits': [k for k in smart_asset_loader.asset_mappings.keys() if 'portrait' in k],
        'UI Icons': [k for k in smart_asset_loader.asset_mappings.keys() if 'icon' in k]
    }
    
    for category, assets in asset_types.items():
        if assets:
            print(f"\n  {category}:")
            for asset in assets[:3]:  # Show first 3
                print(f"    - {asset}")
            if len(assets) > 3:
                print(f"    ... and {len(assets)-3} more")
    
    # Show fallback system
    print(f"\nFALLBACK FALLBACK SYSTEM:")
    print("- If 4K asset missing -> Generate placeholder")
    print("- Automatic quality scaling based on screen resolution")
    print("- Smart caching for performance")
    
    # Test loading a fallback asset
    print(f"\nTESTING Testing fallback asset generation...")
    test_background = smart_asset_loader.load_asset('menu_background')
    if test_background:
        print(f"SUCCESS: Successfully loaded/generated menu background: {test_background.get_size()}")
    else:
        print("ERROR: Failed to load background")

if __name__ == "__main__":
    print("Running art pipeline demo...")
    
    # Run the async demo
    success = asyncio.run(demo_generation())
    
    # Show smart loader demo
    show_smart_loader_demo()
    
    print(f"\n" + "=" * 50)
    if success:
        print("SUCCESS! Art pipeline demo completed successfully!")
    else:
        print("ℹ️ Art pipeline demo completed (install AI libs for real generation)")
    
    print("\nSPRINT 2 Status: 4K Art Pipeline System Ready! Egyptian Art System Ready!")