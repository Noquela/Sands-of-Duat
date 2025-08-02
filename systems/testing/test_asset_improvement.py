#!/usr/bin/env python3
"""
Test Asset Improvement - Focus on generating better quality Egyptian assets
"""

import asyncio
import sys
from pathlib import Path

# Add agents to path
sys.path.append(str(Path(__file__).parent / "agents"))

async def test_asset_improvement():
    """Test improved asset generation focusing on quality"""
    print("TESTING ASSET QUALITY IMPROVEMENTS")
    print("=" * 50)
    print("Focus: Better Egyptian assets with Hades-quality techniques")
    
    # Test with current AssetGenAgent 
    sys.path.append("tools")
    
    try:
        # Run existing asset generation with improvements
        from asset_gen_agent import AssetGenAgent
        
        print("\nInitializing Enhanced Asset Generation Agent...")
        agent = AssetGenAgent()
        
        # Define improved Egyptian assets
        improved_assets = {
            "player_anubis_hades_quality": {
                "prompt": "masterpiece, Egyptian god Anubis warrior, golden armor, jackal head, divine aura, cel-shaded, outlined art style, dramatic lighting, Hades game style, detailed",
                "type": "player_sprite",
                "size": (1024, 256),
                "frames": 4
            },
            "altar_ra_divine": {
                "prompt": "masterpiece, Altar of Ra sun god, golden pyramid structure, solar disk, divine flames, hieroglyphic inscriptions, dramatic lighting, Hades environment style, detailed",
                "type": "environment",
                "size": (512, 512),
                "frames": 1
            },
            "enemy_scarab_warrior": {
                "prompt": "masterpiece, Egyptian scarab warrior, bronze chitinous armor, mandibles, ancient guardian, Hades enemy style, cel-shaded, detailed",
                "type": "enemy_sprite", 
                "size": (768, 192),
                "frames": 4
            }
        }
        
        print(f"\nGenerating {len(improved_assets)} improved Egyptian assets...")
        
        results = []
        for asset_name, config in improved_assets.items():
            print(f"\nGenerating: {asset_name}")
            print(f"  Prompt: {config['prompt'][:60]}...")
            
            try:
                # Generate with improved prompt using async method
                asset_def = {
                    "prompt": config["prompt"],
                    "type": config["type"],
                    "size": config["size"][0],
                    "cols": config.get("frames", 1),
                    "rows": 1
                }
                
                result = await agent.generate_asset(asset_name, asset_def)
                
                if result:
                    print(f"  SUCCESS: Generated {asset_name}")
                    results.append({"name": asset_name, "status": "success"})
                else:
                    print(f"  FAILED: {asset_name}")
                    results.append({"name": asset_name, "status": "failed"})
                    
            except Exception as e:
                print(f"  ERROR: {e}")
                results.append({"name": asset_name, "status": "error", "error": str(e)})
        
        # Summary
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] != "success"]
        
        print(f"\n" + "=" * 50)
        print("ASSET IMPROVEMENT RESULTS:")
        print(f"  Total: {len(results)}")
        print(f"  Successful: {len(successful)}")
        print(f"  Failed: {len(failed)}")
        
        if successful:
            print(f"\nSUCCESSFUL IMPROVEMENTS:")
            for result in successful:
                print(f"  - {result['name']}")
            print(f"\nAssets saved in: assets/generated/")
            
        if failed:
            print(f"\nFAILED ASSETS:")
            for result in failed:
                print(f"  - {result['name']}: {result.get('error', 'Generation failed')}")
        
        return len(successful) > 0
        
    except Exception as e:
        print(f"ERROR: Failed to import or run asset generation: {e}")
        return False

async def compare_asset_quality():
    """Compare current vs improved asset quality"""
    print("\nCOMPARING ASSET QUALITY")
    print("=" * 30)
    
    # Check existing assets
    assets_dir = Path("assets/generated")
    if assets_dir.exists():
        existing_assets = list(assets_dir.glob("*.png"))
        print(f"Existing assets: {len(existing_assets)}")
        
        for asset in existing_assets[:5]:  # Show first 5
            print(f"  - {asset.name}")
        
        if len(existing_assets) > 5:
            print(f"  ... and {len(existing_assets) - 5} more")
    
    # Run improvement test
    improvement_success = await test_asset_improvement()
    
    if improvement_success:
        print("\nQUALITY IMPROVEMENTS APPLIED:")
        print("  * Enhanced prompts with 'masterpiece' and quality terms")
        print("  * Hades game style keywords for consistent art direction")
        print("  * Dramatic lighting and cel-shading specifications")
        print("  * Detailed Egyptian mythology references")
        print("  * Optimized dimensions for each asset type")
        
        print("\nRECOMMENDATIONS FOR FURTHER IMPROVEMENT:")
        print("  1. Add LoRA fine-tuning for Hades art style")
        print("  2. Implement ControlNet for better pose control") 
        print("  3. Add Real-ESRGAN upscaling for higher resolution")
        print("  4. Apply post-processing for cel-shading effects")
        print("  5. Use advanced schedulers (DPMSolver++)")
    else:
        print("\nIMPROVEMENT TEST FAILED")
        print("Falling back to standard generation...")

if __name__ == "__main__":
    asyncio.run(compare_asset_quality())