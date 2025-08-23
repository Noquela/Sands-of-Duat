#!/usr/bin/env python3
"""
Asset Integration System
Automatically integrates newly generated Hades-style Egyptian assets into the game
"""

import os
import shutil
from pathlib import Path
import json

class AssetIntegrator:
    def __init__(self):
        self.project_root = Path(".").resolve()
        self.generated_assets = self.project_root / "assets" / "hades_egyptian_generated"
        self.game_assets = self.project_root / "assets"
        
        # Create necessary asset directories
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create all necessary asset directories"""
        directories = [
            "assets/backgrounds",
            "assets/characters", 
            "assets/portraits",
            "assets/ui",
            "assets/environments",
            "assets/cards",
            "assets/fonts"  # We'll need Egyptian-style fonts too
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def integrate_hades_assets(self):
        """Integrate generated Hades-style assets into game directories"""
        
        if not self.generated_assets.exists():
            print("❌ No generated assets found. Run GENERATE_HADES_ART.bat first!")
            return False
        
        print("🔄 Integrating Hades-style Egyptian assets into game...")
        print("=" * 50)
        
        # Asset mapping: generated -> game locations
        asset_mappings = {
            # Characters
            "characters/pharaoh_warrior.png": "characters/pharaoh_warrior.png",
            "characters/anubis_judge.png": "characters/anubis_judge.png", 
            "characters/isis_mother.png": "characters/isis_mother.png",
            "characters/ra_sun_god.png": "characters/ra_sun_god.png",
            "characters/set_chaos.png": "characters/set_chaos.png",
            "characters/thoth_wisdom.png": "characters/thoth_wisdom.png",
            
            # God portraits for boon system
            "god_portraits/pharaoh_warrior_portrait.png": "portraits/pharaoh_warrior_portrait.png",
            "god_portraits/anubis_judge_portrait.png": "portraits/anubis_judge_portrait.png",
            "god_portraits/isis_mother_portrait.png": "portraits/isis_mother_portrait.png", 
            "god_portraits/ra_sun_god_portrait.png": "portraits/ra_sun_god_portrait.png",
            "god_portraits/set_chaos_portrait.png": "portraits/set_chaos_portrait.png",
            "god_portraits/thoth_wisdom_portrait.png": "portraits/thoth_wisdom_portrait.png",
            
            # Environments
            "environments/desert_temple_4k.png": "backgrounds/bg_combat_4k.png",
            "environments/underworld_hall_4k.png": "backgrounds/bg_hall_of_gods_4k.png", 
            "environments/pyramid_chamber_4k.png": "backgrounds/bg_deck_builder_4k.png",
            
            # UI Elements
            "ui_elements/boon_frame_common.png": "ui/boon_card_common.png",
            "ui_elements/boon_frame_rare.png": "ui/boon_card_rare.png",
            "ui_elements/boon_frame_epic.png": "ui/boon_card_epic.png",
            "ui_elements/boon_frame_legendary.png": "ui/boon_card_legendary.png",
            
            # Main menu
            "bg_main_menu_hades_egyptian_4k.png": "backgrounds/bg_main_menu_4k.png"
        }
        
        integrated_count = 0
        
        for source_path, dest_path in asset_mappings.items():
            source_file = self.generated_assets / source_path
            dest_file = self.game_assets / dest_path
            
            if source_file.exists():
                # Create destination directory if needed
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the asset
                shutil.copy2(source_file, dest_file)
                print(f"✅ Integrated: {dest_path}")
                integrated_count += 1
            else:
                print(f"⚠️ Missing: {source_path}")
        
        print("=" * 50)
        print(f"🎉 Successfully integrated {integrated_count} Hades-style assets!")
        print("🎮 Your game now has beautiful Egyptian art in Hades visual style")
        
        return True
    
    def create_asset_manifest(self):
        """Create a manifest of all integrated assets"""
        
        manifest = {
            "asset_style": "Hades Egyptian",
            "generation_date": str(Path().resolve().stat().st_mtime),
            "assets": {
                "characters": [
                    "pharaoh_warrior.png",
                    "anubis_judge.png", 
                    "isis_mother.png",
                    "ra_sun_god.png",
                    "set_chaos.png",
                    "thoth_wisdom.png"
                ],
                "god_portraits": [
                    "pharaoh_warrior_portrait.png",
                    "anubis_judge_portrait.png",
                    "isis_mother_portrait.png",
                    "ra_sun_god_portrait.png", 
                    "set_chaos_portrait.png",
                    "thoth_wisdom_portrait.png"
                ],
                "environments": [
                    "bg_combat_4k.png",
                    "bg_hall_of_gods_4k.png",
                    "bg_deck_builder_4k.png",
                    "bg_main_menu_4k.png"
                ],
                "ui_elements": [
                    "boon_card_common.png",
                    "boon_card_rare.png", 
                    "boon_card_epic.png",
                    "boon_card_legendary.png"
                ]
            }
        }
        
        manifest_path = self.game_assets / "asset_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"📋 Created asset manifest: {manifest_path}")

def main():
    integrator = AssetIntegrator()
    
    print("🔄 ASSET INTEGRATION SYSTEM")
    print("=" * 40)
    
    if integrator.integrate_hades_assets():
        integrator.create_asset_manifest()
        print("\n✅ Asset integration complete!")
        print("🎮 Your game is now ready with beautiful Hades-style Egyptian art!")
    else:
        print("\n❌ Integration failed. Generate assets first.")

if __name__ == "__main__":
    main()