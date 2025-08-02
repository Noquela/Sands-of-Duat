#!/usr/bin/env python3
"""
AssetGenAgent - Automated Egyptian sprite generation for Sands of Duat
Uses SDXL-MCP to generate all game assets with Egyptian theming
"""

import asyncio
import sys
import os
from pathlib import Path

# Add tools to path
sys.path.insert(0, os.path.dirname(__file__))

from sdxl_mcp import handle_call_tool


class AssetGenAgent:
    """Automated asset generation agent for Sands of Duat."""
    
    def __init__(self):
        self.assets_dir = Path("assets/generated")
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # PREMIUM EGYPTIAN ARTWORK - Hades quality prompts  
        self.asset_definitions = {
            # Player Character - Anubis Warrior
            "player_anubis_idle": {
                "prompt": "Egyptian Anubis warrior god, golden armor, jackal head, amber eyes, royal pose, ceremonial cape, hieroglyphic engravings, Hades game style",
                "type": "sprite_sheet", 
                "animation": "idle",
                "size": 256,
                "cols": 4,
                "rows": 1
            },
            "player_anubis_walk": {
                "prompt": "Anubis warrior walking, golden armor, jackal head, cape flowing, dynamic movement, Egyptian god, Hades style",
                "type": "sprite_sheet",
                "animation": "walk",
                "size": 256,
                "cols": 4,
                "rows": 1
            },
            "player_anubis_attack": {
                "prompt": "Anubis warrior attacking, golden khopesh sword, combat pose, divine energy, hieroglyphic blade, Hades combat style",
                "type": "sprite_sheet", 
                "animation": "attack",
                "size": 256,
                "cols": 4,
                "rows": 1
            },
            
            # Enemies - Scarab Warriors
            "enemy_scarab_idle": {
                "prompt": "Egyptian scarab beetle warrior, bronze armor, insect mandibles, six legs, chitinous shell, battle scars, Hades enemy style",
                "type": "sprite_sheet",
                "animation": "idle", 
                "size": 192,
                "cols": 4,
                "rows": 1
            },
            "enemy_scarab_walk": {
                "prompt": "Scarab warrior walking, bronze chitin armor, six legs moving, menacing patrol, dust clouds, Hades enemy animation",
                "type": "sprite_sheet",
                "animation": "walk",
                "size": 192,
                "cols": 4, 
                "rows": 1
            },
            
            # Hub Elements - Altars and NPCs
            "altar_ra": {
                "prompt": "Ra sun god altar, golden pyramid, solar disk, hieroglyphs glowing, sacred flames, divine light, Hades shrine style",
                "type": "single",
                "size": 384
            },
            "altar_thoth": {
                "prompt": "Thoth wisdom altar, ibis bird sculpture, ancient scrolls, magical symbols, lapis lazuli, gold, Hades shrine style",
                "type": "single", 
                "size": 384
            },
            "altar_isis": {
                "prompt": "Isis magic altar, ankh symbols, blue gold aura, magical energy, divine feminine, protective presence, Hades shrine style",
                "type": "single",
                "size": 384
            },
            "altar_ptah": {
                "prompt": "Ptah creator altar, craftsman tools, mummy wrapping patterns, emerald gold, divine forge, Hades crafting style",
                "type": "single",
                "size": 384
            },
            
            # NPCs for Hub
            "npc_mirror_anubis": {
                "prompt": "Divine Anubis mirror, obsidian surface, jackal god reflection, golden frame, hieroglyphs, magical energy, Hades object style",
                "type": "single",
                "size": 512
            },
            "npc_merchant": {
                "prompt": "Egyptian merchant, traditional robes, golden threading, scrolls, artifacts, welcoming gesture, Hades NPC style",
                "type": "single",
                "size": 384
            },
            
            # Portals and UI
            "portal_arena": {
                "prompt": "Egyptian mystical portal, purple gold energy vortex, hieroglyphic archway, glowing runes, stone pillars, Hades portal style",
                "type": "single",
                "size": 512
            },
            "portal_exit": {
                "prompt": "Egyptian victory portal, emerald gold vortex, celebratory hieroglyphs, ancient gates, divine light, Hades portal style",
                "type": "single", 
                "size": 512
            }
        }
    
    async def generate_asset(self, asset_name: str, asset_def: dict) -> bool:
        """Generate a single asset."""
        print(f"\nGenerating {asset_name}...")
        
        try:
            if asset_def["type"] == "sprite_sheet":
                # Generate sprite sheet
                result = await handle_call_tool("sprite_sheet", {
                    "prompt": asset_def["prompt"],
                    "animation_type": asset_def["animation"],
                    "cols": asset_def["cols"],
                    "rows": asset_def["rows"], 
                    "size": asset_def["size"],
                    "seed": 42,  # Consistent results
                    "steps": 75,  # High quality generation
                    "output_path": f"assets/generated/{asset_name}.png"
                })
            else:
                # Generate single image
                result = await handle_call_tool("text2img", {
                    "prompt": asset_def["prompt"],
                    "width": asset_def["size"],
                    "height": asset_def["size"],
                    "steps": 75,  # High quality generation
                    "seed": 42,  # Consistent results
                    "output_path": f"assets/generated/{asset_name}.png"
                })
            
            if result and len(result) > 0:
                if "Error" in result[0].text:
                    print(f"FAILED to generate {asset_name}: {result[0].text}")
                    return False
                else:
                    print(f"SUCCESS: Generated {asset_name}")
                    print(f"   {result[0].text}")
                    return True
            else:
                print(f"ERROR: No result for {asset_name}")
                return False
                
        except Exception as e:
            print(f"ERROR generating {asset_name}: {e}")
            return False
    
    async def generate_all_assets(self) -> None:
        """Generate all game assets."""
        print("SANDS OF DUAT - ASSET GENERATION AGENT")
        print("=" * 60)
        print("Generating Egyptian-themed game assets using SDXL...")
        print(f"Output directory: {self.assets_dir.absolute()}")
        print()
        
        # Generate assets in priority order
        priority_order = [
            # Critical player assets first
            "player_anubis_idle",
            "player_anubis_walk", 
            "player_anubis_attack",
            
            # Enemy assets
            "enemy_scarab_idle",
            "enemy_scarab_walk",
            
            # Hub elements
            "altar_ra",
            "altar_thoth", 
            "altar_isis",
            "altar_ptah",
            
            # NPCs
            "npc_mirror_anubis",
            "npc_merchant",
            
            # Portals
            "portal_arena",
            "portal_exit"
        ]
        
        successful = 0
        total = len(priority_order)
        
        for asset_name in priority_order:
            if asset_name in self.asset_definitions:
                asset_def = self.asset_definitions[asset_name]
                success = await self.generate_asset(asset_name, asset_def)
                if success:
                    successful += 1
            else:
                print(f"WARNING: Asset definition not found: {asset_name}")
        
        print("\n" + "=" * 60)
        print(f"GENERATION COMPLETE: {successful}/{total} assets generated")
        
        if successful == total:
            print("SUCCESS: All Egyptian assets generated successfully!")
            print("READY: Update game with AI-generated sprites!")
        else:
            print(f"WARNING: {total - successful} assets failed to generate")
            print("TIP: Check CUDA memory and model availability")
        
        print(f"\nAssets saved to: {self.assets_dir.absolute()}")
    
    async def generate_priority_assets(self) -> None:
        """Generate only the most critical assets for immediate testing."""
        print("GENERATING PRIORITY ASSETS FOR TESTING...")
        print("=" * 50)
        
        priority_assets = [
            "player_anubis_idle",
            "enemy_scarab_idle", 
            "portal_arena"
        ]
        
        successful = 0
        for asset_name in priority_assets:
            if asset_name in self.asset_definitions:
                asset_def = self.asset_definitions[asset_name]
                success = await self.generate_asset(asset_name, asset_def)
                if success:
                    successful += 1
        
        print(f"\nPriority assets: {successful}/{len(priority_assets)} generated")
        return successful == len(priority_assets)


async def main():
    """Main entry point for asset generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Egyptian game assets for Sands of Duat")
    parser.add_argument("--priority", action="store_true", help="Generate only priority assets for testing")
    args = parser.parse_args()
    
    agent = AssetGenAgent()
    
    try:
        if args.priority:
            success = await agent.generate_priority_assets()
            return 0 if success else 1
        else:
            await agent.generate_all_assets()
            return 0
            
    except KeyboardInterrupt:
        print("\nAsset generation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nAsset generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))