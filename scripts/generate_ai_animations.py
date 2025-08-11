"""
Generate AI Egyptian Card Animations
Simple script to generate all Egyptian card animations using local AI.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sands_of_duat.animation.animation_manager import animation_manager

async def main():
    """Generate all Egyptian card animations."""
    print("🏺 Sands of Duat - AI Animation Generation")
    print("=" * 50)
    
    # Check system status
    status = animation_manager.get_generation_status()
    print(f"Generation mode: {status['mode']}")
    print(f"Local AI available: {status['local_ai_available']}")
    print(f"ComfyUI available: {status['comfyui_available']}")
    print(f"Existing animations: {status['available_animations']}")
    
    if status['mode'] == 'placeholder':
        print("\n⚠️ WARNING: No AI generation available!")
        print("Run setup_ai_generation.py first to install AI libraries.")
        return
    
    print(f"\nOutput directory: {status['ai_output_dir']}")
    print("\nGenerating Egyptian card animations...")
    
    # Egyptian card names to generate
    egyptian_cards = [
        "ra_solar_deity",
        "anubis_judge_of_the_dead",
        "isis_mother_goddess", 
        "set_chaos_lord",
        "thoth_wisdom_keeper",
        "horus_sky_god"
    ]
    
    try:
        # Generate all animations
        results = await animation_manager.generate_all_cards(egyptian_cards)
        
        print("\n" + "=" * 50)
        print("🎬 GENERATION RESULTS")
        print("=" * 50)
        
        successful = 0
        failed = 0
        
        for card_name, path in results.items():
            if path:
                print(f"✅ {card_name}: {path}")
                successful += 1
            else:
                print(f"❌ {card_name}: FAILED")
                failed += 1
        
        print(f"\n📊 Summary: {successful} successful, {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 AI animations generated successfully!")
            print("The game will now use these AI-generated animations for Egyptian cards.")
        else:
            print(f"\n😞 No animations were generated successfully.")
            
    except KeyboardInterrupt:
        print("\n❌ Generation cancelled by user")
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        raise
    finally:
        # Cleanup
        animation_manager.cleanup()

def check_requirements():
    """Check if required libraries are installed."""
    try:
        import torch
        import diffusers
        print("✅ AI libraries detected")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU detected: {gpu_name}")
        else:
            print("⚠️ No GPU detected - generation will be slow")
        
        return True
    except ImportError as e:
        print(f"❌ Missing AI libraries: {e}")
        print("Run setup_ai_generation.py first to install dependencies")
        return False

if __name__ == "__main__":
    print("Checking requirements...")
    if check_requirements():
        asyncio.run(main())
    else:
        print("\nInstall AI libraries first:")
        print("python scripts/setup_ai_generation.py")