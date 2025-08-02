#!/usr/bin/env python3
"""
Simple test for advanced asset generation
"""

import asyncio
import sys
from pathlib import Path

# Add agents to path
sys.path.append(str(Path(__file__).parent / "agents"))

async def test_simple():
    """Simple test of advanced generation"""
    print("TESTING ADVANCED EGYPTIAN ASSET GENERATION")
    print("=" * 50)
    
    try:
        from advanced_asset_generation_agent import AdvancedAssetGenerationAgent
        
        # Initialize agent
        agent = AdvancedAssetGenerationAgent()
        
        print("Setting up advanced pipeline...")
        
        # Test simple generation without full setup
        result = await agent.generate_advanced_egyptian_asset(
            asset_name="test_simple_anubis",
            prompt="Egyptian god Anubis warrior, golden armor, divine aura",
            width=512,
            height=512,
            style="hades_egyptian",
            use_controlnet=False,  # Disable for simple test
            use_lora=False,        # Disable for simple test  
            upscale=False          # Disable for simple test
        )
        
        print(f"Result: {result}")
        
        if result["status"] == "success":
            print("SUCCESS: Advanced generation working!")
            print(f"Output: {result['output_path']}")
        else:
            print(f"FAILED: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        print("Falling back to standard generation test...")
        
        # Test standard generation
        sys.path.append("tools")
        from asset_gen_agent import generate_egyptian_asset
        
        result = await asyncio.to_thread(
            generate_egyptian_asset,
            "test_standard_anubis", 
            "Egyptian god Anubis warrior, golden armor", 
            512, 512, 30
        )
        
        if result:
            print("SUCCESS: Standard generation working!")
        else:
            print("FAILED: Standard generation failed")

if __name__ == "__main__":
    asyncio.run(test_simple())