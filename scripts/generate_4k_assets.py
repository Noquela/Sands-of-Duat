"""
Generate 4K Egyptian Assets - SPRINT 2
Creates all professional game assets using local AI pipeline.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sands_of_duat.assets.art_pipeline import egyptian_art_pipeline

async def main():
    """Generate all 4K Egyptian art assets."""
    print("🏺 SPRINT 2 - 4K Egyptian Art Generation")
    print("=" * 50)
    
    # Check if AI is available
    try:
        import torch
        import diffusers
        print("✅ AI libraries detected")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU: {gpu_name}")
            print(f"✅ CUDA Memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3}GB")
        else:
            print("⚠️ No CUDA GPU - using CPU (will be slower)")
            
    except ImportError as e:
        print(f"❌ Missing AI libraries: {e}")
        print("\nInstall required packages:")
        print("pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121")
        print("pip install diffusers transformers accelerate")
        return False
    
    print(f"\n📁 Output directory: {egyptian_art_pipeline.assets_dir}")
    print("\nThis will generate:")
    print("• 4K Backgrounds (4096x2048): Menu, Combat, Deck Builder, Collection")
    print("• Card Frames (1024x1024): Common, Rare, Epic, Legendary")
    print("• Character Portraits (1024x1024): Ra, Anubis, Isis, Set, Thoth, Horus")
    print("• UI Elements (512x512): Health, Mana, Attack, Shield icons")
    
    # Confirm generation
    if not os.environ.get('AUTO_GENERATE'):
        response = input("\n🎨 Generate all Egyptian assets? (y/N): ").strip().lower()
        if response != 'y':
            print("Asset generation cancelled")
            return False
    
    try:
        print("\n🚀 Starting 4K asset generation...")
        results = await egyptian_art_pipeline.generate_all_assets()
        
        if not results:
            print("❌ Generation failed - pipeline not initialized")
            return False
        
        # Show results
        print("\n" + "=" * 50)
        print("🎭 GENERATION RESULTS")
        print("=" * 50)
        
        successful = 0
        failed = 0
        
        # Group by asset type
        by_type = {}
        for asset_name, success in results.items():
            # Determine type from specs
            asset_type = "unknown"
            if "background" in asset_name:
                asset_type = "backgrounds"
            elif "frame" in asset_name:
                asset_type = "card_frames"
            elif "portrait" in asset_name:
                asset_type = "character_portraits"
            elif "icon" in asset_name:
                asset_type = "ui_elements"
            
            if asset_type not in by_type:
                by_type[asset_type] = []
            by_type[asset_type].append((asset_name, success))
        
        # Display by type
        for asset_type, assets in by_type.items():
            print(f"\n📂 {asset_type.upper()}:")
            for name, success in assets:
                status = "✅" if success else "❌"
                print(f"  {status} {name}")
                if success:
                    successful += 1
                else:
                    failed += 1
        
        print(f"\n📊 Summary: {successful} successful, {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 4K Egyptian assets generated successfully!")
            print(f"📁 Location: {egyptian_art_pipeline.assets_dir}")
            print("\nThe game will now use these professional 4K assets!")
            
            # List generated files
            print(f"\n📋 Generated files:")
            for asset_dir in egyptian_art_pipeline.assets_dir.iterdir():
                if asset_dir.is_dir():
                    files = list(asset_dir.glob("*.png"))
                    if files:
                        print(f"  {asset_dir.name}/: {len(files)} files")
        else:
            print(f"\n😞 No assets were generated successfully")
            
        return successful > 0
        
    except KeyboardInterrupt:
        print("\n❌ Generation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        raise
    finally:
        # Always cleanup
        egyptian_art_pipeline.cleanup()

def check_disk_space():
    """Check if enough disk space is available."""
    import shutil
    free_bytes = shutil.disk_usage(".")[2]
    free_gb = free_bytes / (1024**3)
    
    if free_gb < 10:  # Need at least 10GB for generation + models
        print(f"⚠️ Warning: Only {free_gb:.1f}GB disk space available")
        print("Recommend at least 10GB for model downloads + generated assets")
        return False
    
    print(f"✅ Disk space: {free_gb:.1f}GB available")
    return True

if __name__ == "__main__":
    print("Checking system requirements...")
    if check_disk_space():
        success = asyncio.run(main())
        if success:
            print("\n🏺 SPRINT 2 art generation complete!")
        else:
            print("\n💔 Art generation failed")
            sys.exit(1)
    else:
        print("❌ Insufficient disk space")
        sys.exit(1)