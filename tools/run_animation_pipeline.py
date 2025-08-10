#!/usr/bin/env python3
"""
MASTER SCRIPT - Hades-Egyptian Animated Art Pipeline
RTX 5070 Optimized Complete Workflow

This script coordinates the entire pipeline:
1. Setup ComfyUI/WebUI environment
2. Generate animated artwork 
3. Validate quality automatically
4. Compress sprites for optimal performance
5. Integrate into game systems
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root / "src"))
sys.path.append(str(project_root / "tools"))

def run_pipeline_step(step_name: str, step_function, *args, **kwargs):
    """Run a pipeline step with error handling and timing."""
    print(f"\n{'='*60}")
    print(f"🎯 STEP: {step_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = step_function(*args, **kwargs)
        elapsed = time.time() - start_time
        
        print(f"✅ {step_name} completed successfully in {elapsed:.1f}s")
        return result, True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ {step_name} failed after {elapsed:.1f}s")
        print(f"Error: {e}")
        return None, False

def setup_environment():
    """Setup ComfyUI environment for RTX 5070."""
    try:
        from setup_comfyui import ComfyUISetup
        setup = ComfyUISetup()
        return setup.setup()
    except ImportError:
        print("ComfyUI setup script not found. Please ensure tools/setup_comfyui.py exists.")
        return False

def generate_animated_artwork():
    """Generate all animated artwork."""
    try:
        from generate_animated_artwork import AnimatedArtworkPipeline
        pipeline = AnimatedArtworkPipeline()
        results = pipeline.run_full_pipeline()
        return results['success_rate'] > 0.5  # At least 50% success rate
    except ImportError:
        print("Animation generation script not found.")
        return False

def validate_artwork_quality():
    """Validate generated artwork quality."""
    try:
        from quality_validator import RTX5070QualityValidator
        
        validator = RTX5070QualityValidator()
        
        # Validate generated animations
        generated_dir = Path("assets/generated_animations/cards")
        if generated_dir.exists():
            results = validator.batch_validate_directory(generated_dir, "animated")
            validator.save_validation_report(results, Path("animation_quality_report.json"))
            
            # Check if enough assets meet quality threshold
            good_quality_count = sum(1 for metrics in results.values() 
                                   if metrics.overall_score >= 0.75)
            
            return good_quality_count > 0
        else:
            print("No generated animations directory found.")
            return False
            
    except ImportError:
        print("Quality validation script not found.")
        return False

def compress_sprites():
    """Compress sprites for optimal performance."""
    try:
        import sys
        sys.path.append(str(project_root / "assets" / "post_processing"))
        
        from compress_sprites import BatchSpriteCompressor
        
        compressor = BatchSpriteCompressor()
        
        # Compress generated animations
        input_dir = Path("assets/generated_animations/cards")
        output_dir = Path("assets/compressed_sprites/cards")
        
        if input_dir.exists():
            results = compressor.compress_directory(
                input_dir, 
                output_dir, 
                preset='cards_balanced',
                max_workers=4
            )
            
            # Check compression success rate
            successful = sum(1 for r in results.values() if r.get('success', False))
            return successful > 0
        else:
            print("No animations to compress.")
            return False
            
    except ImportError:
        print("Compression script not found.")
        return False

def test_game_integration():
    """Test that animations integrate properly with the game."""
    try:
        # Test asset loader animation functions
        sys.path.append(str(project_root / "src" / "sands_of_duat" / "core"))
        from asset_loader import get_asset_loader
        
        asset_loader = get_asset_loader()
        
        # Test loading animated cards
        test_cards = ['ANUBIS - JUDGE OF THE DEAD', 'Egyptian Warrior']
        
        for card_name in test_cards:
            animation_info = asset_loader.get_animation_info(card_name)
            if animation_info:
                print(f"✓ {card_name}: {animation_info['frame_count']} frames @ {animation_info['fps']} fps")
            else:
                # Try loading static version
                static_card = asset_loader.load_card_art_by_name(card_name)
                if static_card:
                    print(f"✓ {card_name}: Static artwork loaded")
                else:
                    print(f"✗ {card_name}: No artwork found")
                    return False
        
        print("✓ Game integration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Game integration test failed: {e}")
        return False

def generate_final_report(results: Dict[str, bool]):
    """Generate final pipeline report."""
    
    report = {
        "pipeline_timestamp": time.time(),
        "rtx_5070_optimized": True,
        "pipeline_steps": results,
        "overall_success": all(results.values()),
        "success_rate": sum(results.values()) / len(results) * 100
    }
    
    print(f"\n{'='*60}")
    print("🏺 HADES-EGYPTIAN ANIMATION PIPELINE REPORT 🏺")
    print(f"{'='*60}")
    
    for step_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{step_name:.<40} {status}")
    
    print(f"\nOverall Success Rate: {report['success_rate']:.1f}%")
    
    if report['overall_success']:
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY! 🎉")
        print("Your RTX 5070 has generated gorgeous Hades-quality Egyptian art!")
        print("\nNext steps:")
        print("- Run the game to see animated cards in combat")
        print("- Generate more cards with different themes")
        print("- Experiment with animation settings")
    else:
        print("\n⚠️  PIPELINE COMPLETED WITH ISSUES")
        print("Some steps failed. Check individual step outputs above.")
        print("\nTroubleshooting:")
        print("- Ensure ComfyUI/WebUI is properly installed")
        print("- Check that RTX 5070 drivers are up to date")
        print("- Verify sufficient disk space for generated assets")
    
    # Save report
    report_path = project_root / "pipeline_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_path}")

def main():
    """Run the complete animated art pipeline."""
    
    print("🏺" * 20)
    print("   SANDS OF DUAT - RTX 5070 ANIMATION PIPELINE")
    print("   Generating Hades-Quality Egyptian Art")
    print("🏺" * 20)
    print(f"Starting pipeline at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    pipeline_start_time = time.time()
    results = {}
    
    # Step 1: Environment Setup
    result, success = run_pipeline_step(
        "Environment Setup", 
        setup_environment
    )
    results["Environment Setup"] = success
    
    # Step 2: Generate Animations (only if setup succeeded)
    if success:
        result, success = run_pipeline_step(
            "Generate Animated Artwork", 
            generate_animated_artwork
        )
        results["Generate Animated Artwork"] = success
    else:
        results["Generate Animated Artwork"] = False
        print("⏩ Skipping animation generation due to setup failure")
    
    # Step 3: Quality Validation
    if results["Generate Animated Artwork"]:
        result, success = run_pipeline_step(
            "Quality Validation", 
            validate_artwork_quality
        )
        results["Quality Validation"] = success
    else:
        results["Quality Validation"] = False
        print("⏩ Skipping quality validation - no animations generated")
    
    # Step 4: Sprite Compression
    if results["Quality Validation"]:
        result, success = run_pipeline_step(
            "Sprite Compression", 
            compress_sprites
        )
        results["Sprite Compression"] = success
    else:
        results["Sprite Compression"] = False
        print("⏩ Skipping sprite compression - no quality assets")
    
    # Step 5: Game Integration Test
    result, success = run_pipeline_step(
        "Game Integration Test", 
        test_game_integration
    )
    results["Game Integration Test"] = success
    
    # Generate final report
    pipeline_elapsed = time.time() - pipeline_start_time
    print(f"\n⏱️  Total Pipeline Time: {pipeline_elapsed/60:.1f} minutes")
    
    generate_final_report(results)

if __name__ == "__main__":
    # Check if we're in the right directory
    if not (Path.cwd() / "src" / "sands_of_duat").exists():
        print("❌ Please run this script from the Sands of Duat project root directory")
        sys.exit(1)
    
    main()