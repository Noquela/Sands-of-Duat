#!/usr/bin/env python3
"""
Simple Asset Generator - Create placeholder assets organized in folders
Creates colored placeholders with proper organization while advanced pipeline is being fixed
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Any
import json
import time

# Simple asset generation without complex dependencies
from PIL import Image, ImageDraw, ImageFont

class SimpleAssetGenerator:
    """Simple placeholder asset generator for game development"""
    
    def __init__(self):
        self.name = "Simple Asset Generator"
        self.base_path = Path(__file__).parent.parent.parent
        
        # Asset specifications
        self.asset_specs = {
            "characters": {
                "path": "assets/characters/",
                "color": (218, 165, 32),  # Gold
                "assets": [
                    {"name": "anubis_warrior_idle", "size": (128, 128)},
                    {"name": "anubis_warrior_walk", "size": (128, 128)},
                    {"name": "anubis_warrior_attack", "size": (128, 128)}
                ]
            },
            "enemies": {
                "path": "assets/enemies/",
                "color": (139, 69, 19),  # Brown
                "assets": [
                    {"name": "scarab_guardian_idle", "size": (96, 96)},
                    {"name": "mummy_warrior_idle", "size": (96, 96)},
                    {"name": "anubis_sentinel_idle", "size": (128, 128)}
                ]
            },
            "environments": {
                "path": "assets/environments/",
                "color": (65, 105, 225),  # Blue
                "assets": [
                    {"name": "altar_ra", "size": (128, 128)},
                    {"name": "altar_thoth", "size": (128, 128)},
                    {"name": "altar_isis", "size": (128, 128)},
                    {"name": "altar_ptah", "size": (128, 128)}
                ]
            },
            "portals": {
                "path": "assets/portals/",
                "color": (138, 43, 226),  # Purple
                "assets": [
                    {"name": "arena_portal", "size": (128, 128)},
                    {"name": "exit_portal", "size": (128, 128)}
                ]
            },
            "ui": {
                "path": "assets/ui/",
                "color": (255, 215, 0),  # Yellow
                "assets": [
                    {"name": "health_bar_frame", "size": (256, 32)},
                    {"name": "artifact_slot_frame", "size": (64, 64)}
                ]
            }
        }
        
        print(f"Simple Asset Generator initialized")
        print(f"Base path: {self.base_path}")
    
    def create_directories(self) -> bool:
        """Create organized directory structure"""
        try:
            print("Creating asset directories...")
            
            for category, spec in self.asset_specs.items():
                asset_dir = self.base_path / spec["path"]
                asset_dir.mkdir(parents=True, exist_ok=True)
                print(f"  Created: {asset_dir}")
            
            return True
            
        except Exception as e:
            print(f"Failed to create directories: {e}")
            return False
    
    async def generate_all_assets(self) -> Dict[str, Any]:
        """Generate all placeholder assets"""
        
        print("\nGenerating Organized Egyptian Assets...")
        print("=" * 45)
        
        if not self.create_directories():
            return {"status": "failed", "error": "Directory creation failed"}
        
        results = {
            "status": "success",
            "categories": {},
            "total_assets": 0,
            "successful_assets": 0
        }
        
        # Generate assets by category
        for category, spec in self.asset_specs.items():
            print(f"\nGenerating {category.title()}...")
            
            category_path = self.base_path / spec["path"]
            category_results = []
            
            for asset_config in spec["assets"]:
                try:
                    print(f"  Creating: {asset_config['name']}")
                    
                    # Create placeholder asset
                    success = self._create_placeholder_asset(
                        asset_config, category_path, spec["color"]
                    )
                    
                    if success:
                        category_results.append({
                            "name": asset_config["name"],
                            "status": "success",
                            "path": str(category_path / f"{asset_config['name']}.png")
                        })
                        results["successful_assets"] += 1
                        print(f"    SUCCESS: {asset_config['name']}")
                    else:
                        category_results.append({
                            "name": asset_config["name"],
                            "status": "failed"
                        })
                    
                    results["total_assets"] += 1
                    
                except Exception as e:
                    print(f"    ERROR: {asset_config['name']} - {e}")
                    category_results.append({
                        "name": asset_config["name"],
                        "status": "failed",
                        "error": str(e)
                    })
            
            results["categories"][category] = {
                "path": str(category_path),
                "assets": category_results,
                "count": len(category_results)
            }
        
        # Save summary
        self._save_asset_summary(results)
        
        print(f"\nAsset Generation Complete!")
        print(f"Total: {results['total_assets']}")
        print(f"Success: {results['successful_assets']}")
        print(f"Success Rate: {results['successful_assets']/results['total_assets']*100:.1f}%")
        
        return results
    
    def _create_placeholder_asset(self, asset_config: Dict, output_path: Path, color: tuple) -> bool:
        """Create a colored placeholder asset"""
        
        try:
            size = asset_config["size"]
            name = asset_config["name"]
            
            # Create image with transparency
            image = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw colored background with some transparency
            draw.rectangle([0, 0, size[0], size[1]], fill=color + (180,))
            
            # Draw border
            draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=color, width=2)
            
            # Add text if size allows
            if size[0] >= 64 and size[1] >= 32:
                try:
                    # Use default font
                    font = ImageFont.load_default()
                    
                    # Format name for display
                    display_name = name.replace("_", " ").title()
                    if len(display_name) > 15:
                        # Split long names
                        words = display_name.split()
                        if len(words) > 1:
                            display_name = words[0] + "\n" + " ".join(words[1:])
                    
                    # Calculate text position
                    bbox = draw.textbbox((0, 0), display_name, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    text_x = (size[0] - text_width) // 2
                    text_y = (size[1] - text_height) // 2
                    
                    # Draw text with shadow
                    draw.text((text_x + 1, text_y + 1), display_name, fill=(0, 0, 0), font=font)
                    draw.text((text_x, text_y), display_name, fill=(255, 255, 255), font=font)
                    
                except Exception:
                    # If text fails, just draw a simple shape
                    center_x, center_y = size[0] // 2, size[1] // 2
                    radius = min(size) // 4
                    draw.ellipse([center_x - radius, center_y - radius, 
                                center_x + radius, center_y + radius], 
                               fill=(255, 255, 255))
            
            # Save the image
            output_file = output_path / f"{name}.png"
            image.save(output_file, "PNG")
            
            return True
            
        except Exception as e:
            print(f"    Failed to create {name}: {e}")
            return False
    
    def _save_asset_summary(self, results: Dict) -> None:
        """Save asset summary"""
        
        summary_path = self.base_path / "assets" / "asset_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary = {
            "generation_time": time.time(),
            "generator": self.name,
            "total_assets": results["total_assets"],
            "successful_assets": results["successful_assets"],
            "success_rate": results["successful_assets"] / results["total_assets"] * 100 if results["total_assets"] > 0 else 0,
            "categories": {}
        }
        
        for category, info in results["categories"].items():
            summary["categories"][category] = {
                "path": info["path"],
                "asset_count": info["count"],
                "assets": [asset["name"] for asset in info["assets"] if asset["status"] == "success"]
            }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Asset summary saved: {summary_path}")

async def main():
    """Generate simple organized assets"""
    
    generator = SimpleAssetGenerator()
    
    print("SANDS OF DUAT - SIMPLE ASSET GENERATION")
    print("=" * 50)
    
    # Generate all assets
    results = await generator.generate_all_assets()
    
    if results["status"] == "success":
        print(f"\nSUCCESS: Assets created in organized structure!")
        print(f"Game assets ready for use")
    else:
        print(f"\nAsset generation failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())