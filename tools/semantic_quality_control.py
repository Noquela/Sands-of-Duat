#!/usr/bin/env python3
"""
SEMANTIC QUALITY CONTROL SYSTEM
===============================

Manual review and validation of generated assets for prompt adherence
and semantic correctness beyond technical metrics.
"""

from pathlib import Path
import json

class SemanticQualityControl:
    def __init__(self):
        self.assets_dir = Path("../assets/generated_art_lora")
        self.rejected_dir = Path("../assets/rejected_semantic")
        self.approved_dir = Path("../assets/approved_semantic")
        self.rejected_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        
        # Define what each asset SHOULD contain
        self.asset_expectations = {
            # Characters - should be SINGLE characters
            "char_player_hero": "Single Egyptian warrior hero with pharaonic armor",
            "char_anubis_boss": "Single imposing Anubis deity",
            "char_mummy_guardian": "Single ancient mummy guardian", 
            "char_desert_scorpion": "Single giant magical scorpion",
            "char_sand_elemental": "Single swirling sand creature",
            
            # Common cards - simple objects/concepts
            "sand_grain": "Simple magical grain of sand (NOT a full character)",
            "papyrus_scroll": "Ancient papyrus manuscript",
            "desert_meditation": "Peaceful meditation scene",
            "sacred_scarab": "Single golden scarab beetle",
            "whisper_of_thoth": "Ethereal wisdom/knowledge visualization",
            
            # Backgrounds - environmental scenes
            "bg_menu_temple": "Egyptian temple entrance/interior",
            "bg_combat_underworld": "Underworld battlefield environment", 
            "bg_deck_builder_sanctum": "Sacred scrolls chamber",
            "bg_victory_sunrise": "Dawn over Egyptian desert",
            "bg_defeat_dusk": "Evening necropolis scene"
        }
    
    def get_problematic_assets(self):
        """Identify assets that don't match their intended purpose."""
        print("SEMANTIC QUALITY CONTROL - MANUAL REVIEW REQUIRED")
        print("=" * 60)
        
        problematic_assets = []
        
        # Based on manual inspection, flag known issues
        issues = [
            {
                "file": "char_player_hero.png",
                "issue": "Shows 3 identical characters instead of 1 single hero",
                "severity": "CRITICAL",
                "needs_regeneration": True
            },
            {
                "file": "sand_grain.png", 
                "issue": "Shows full pharaoh character instead of simple sand grain",
                "severity": "CRITICAL", 
                "needs_regeneration": True
            }
        ]
        
        for issue in issues:
            print(f"FAILED {issue['file']}: {issue['issue']}")
            problematic_assets.append(issue)
        
        return problematic_assets
    
    def create_regeneration_list(self):
        """Create list of assets that need to be regenerated."""
        problematic = self.get_problematic_assets()
        
        regeneration_specs = []
        
        for asset in problematic:
            if asset["needs_regeneration"]:
                # Improve prompts for problematic assets
                if "char_player_hero" in asset["file"]:
                    regeneration_specs.append({
                        "name": "char_player_hero",
                        "improved_prompt": "egyptian_hades_art, masterpiece, single Egyptian warrior hero portrait, determined expression, traditional pharaonic armor, golden headdress, heroic bearing, centered composition, one character only",
                        "category": "characters",
                        "resolution": {"width": 512, "height": 768}
                    })
                
                elif "sand_grain" in asset["file"]:
                    regeneration_specs.append({
                        "name": "sand_grain", 
                        "improved_prompt": "egyptian_hades_art, masterpiece, tiny magical grain of sand, glowing with power, desert magic essence, golden sparkle, simple object, minimal composition, close-up view",
                        "category": "common_cards", 
                        "resolution": {"width": 768, "height": 1024}
                    })
        
        return regeneration_specs
    
    def generate_improved_assets(self):
        """Generate improved versions of problematic assets."""
        specs = self.create_regeneration_list()
        
        if not specs:
            print("No assets need regeneration!")
            return
            
        print(f"\nRegenerating {len(specs)} problematic assets...")
        
        # Save regeneration specifications
        regen_file = Path("../assets/regeneration_specs.json")
        with open(regen_file, 'w') as f:
            json.dump(specs, f, indent=2)
        
        print(f"Regeneration specifications saved to: {regen_file}")
        print("\nTo regenerate these assets, run the selective asset regenerator.")

def main():
    sqc = SemanticQualityControl()
    problematic = sqc.get_problematic_assets()
    
    if problematic:
        print(f"\nFound {len(problematic)} assets with semantic issues")
        sqc.generate_improved_assets()
    else:
        print("\nAll assets pass semantic quality control!")

if __name__ == "__main__":
    main()