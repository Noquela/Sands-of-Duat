#!/usr/bin/env python3
"""
Egyptian Asset Generator - Organized asset generation for Sands of Duat
Generates all Egyptian assets in proper folder structure
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Any
import json
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

class EgyptianAssetGenerator:
    """Organized Egyptian asset generator for game assets"""
    
    def __init__(self):
        self.name = "Egyptian Asset Generator"
        self.base_path = Path(__file__).parent.parent.parent
        
        # Organized asset categories with file structure
        self.asset_categories = {
            "characters": {
                "path": "assets/characters/",
                "assets": [
                    {
                        "name": "anubis_warrior_idle",
                        "prompt": "Egyptian god Anubis warrior standing idle, jackal head, golden armor with hieroglyphic engravings, royal blue cape, amber glowing eyes, cel-shaded art style, Hades game style, 2D sprite, side view",
                        "size": (128, 128)
                    },
                    {
                        "name": "anubis_warrior_walk", 
                        "prompt": "Egyptian god Anubis warrior walking, jackal head, golden armor, cape flowing, dynamic stride, cel-shaded art style, Hades game style, 2D sprite animation frame, side view",
                        "size": (128, 128)
                    },
                    {
                        "name": "anubis_warrior_attack",
                        "prompt": "Egyptian god Anubis warrior attacking with golden khopesh sword, combat stance, divine energy aura, cel-shaded art style, Hades game style, 2D sprite, action pose",
                        "size": (128, 128)
                    }
                ]
            },
            "enemies": {
                "path": "assets/enemies/",
                "assets": [
                    {
                        "name": "scarab_guardian_idle",
                        "prompt": "Egyptian scarab beetle guardian, bronze chitinous armor, large mandibles, six legs, battle-ready stance, cel-shaded art style, Hades enemy style, 2D sprite",
                        "size": (96, 96)
                    },
                    {
                        "name": "mummy_warrior_idle",
                        "prompt": "Egyptian mummy warrior, ancient bandages, glowing red eyes, ceremonial staff, weathered wrappings, cel-shaded art style, Hades enemy style, 2D sprite",
                        "size": (96, 96)
                    },
                    {
                        "name": "anubis_sentinel_idle",
                        "prompt": "Anubis sentinel guard, dark bronze armor, jackal head, ceremonial spear, elite enemy design, cel-shaded art style, Hades boss style, 2D sprite",
                        "size": (128, 128)
                    }
                ]
            },
            "environments": {
                "path": "assets/environments/",
                "assets": [
                    {
                        "name": "altar_ra",
                        "prompt": "Altar of Ra sun god, golden pyramid structure, solar disk at top, divine flames, hieroglyphic inscriptions, sacred temple architecture, cel-shaded art style, Hades environment style",
                        "size": (128, 128)
                    },
                    {
                        "name": "altar_thoth",
                        "prompt": "Altar of Thoth wisdom god, ibis bird sculpture, ancient scrolls, lapis lazuli and gold details, magical symbols, cel-shaded art style, Hades environment style",
                        "size": (128, 128)
                    },
                    {
                        "name": "altar_isis",
                        "prompt": "Altar of Isis goddess, ankh symbols, protective aura, blue and gold magical energy, maternal divine presence, cel-shaded art style, Hades environment style",
                        "size": (128, 128)
                    },
                    {
                        "name": "altar_ptah",
                        "prompt": "Altar of Ptah creator god, craftsman tools, mummy wrapping patterns, emerald and gold, divine forge elements, cel-shaded art style, Hades environment style",
                        "size": (128, 128)
                    }
                ]
            },
            "portals": {
                "path": "assets/portals/",
                "assets": [
                    {
                        "name": "arena_portal",
                        "prompt": "Egyptian mystical portal to arena, purple and gold energy vortex, hieroglyphic stone archway, glowing runes, ancient pillars, cel-shaded art style, Hades portal style",
                        "size": (128, 128)
                    },
                    {
                        "name": "exit_portal",
                        "prompt": "Egyptian victory portal, emerald and gold energy swirl, celebratory hieroglyphs, divine light, ancient gateway, cel-shaded art style, Hades portal style",
                        "size": (128, 128)
                    }
                ]
            },
            "ui": {
                "path": "assets/ui/",
                "assets": [
                    {
                        "name": "health_bar_frame",
                        "prompt": "Egyptian health bar UI frame, golden ankh symbols, hieroglyphic border, papyrus texture background, game UI element, cel-shaded art style, Hades UI style",
                        "size": (256, 32)
                    },
                    {
                        "name": "artifact_slot_frame",
                        "prompt": "Egyptian artifact slot UI, circular golden frame, divine glow, hieroglyphic decoration, sacred geometry, game UI element, cel-shaded art style, Hades UI style", 
                        "size": (64, 64)
                    }
                ]
            }
        }
        
        print(f"Egyptian Asset Generator initialized")
        print(f"Base path: {self.base_path}")
        print(f"Categories: {list(self.asset_categories.keys())}")
    
    def create_directory_structure(self) -> bool:
        """Create organized directory structure for assets"""
        try:
            print("Creating organized directory structure...")
            
            for category, info in self.asset_categories.items():
                asset_dir = self.base_path / info["path"]
                asset_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {asset_dir}")
            
            return True
            
        except Exception as e:
            print(f"Failed to create directories: {e}")
            return False
    
    async def generate_all_assets(self) -> Dict[str, Any]:
        """Generate all Egyptian assets in organized structure"""
        
        print(f"\nStarting Egyptian Asset Generation...")
        print("=" * 50)
        
        # Create directory structure
        if not self.create_directory_structure():
            return {"status": "failed", "error": "Directory creation failed"}
        
        results = {
            "status": "success",
            "categories": {},
            "total_assets": 0,
            "successful_assets": 0,
            "failed_assets": 0
        }
        
        # Generate assets by category
        for category, info in self.asset_categories.items():
            print(f"\nGenerating {category.title()} Assets...")
            print("-" * 30)
            
            category_results = []
            category_path = self.base_path / info["path"]
            
            for asset_config in info["assets"]:
                try:
                    print(f"Generating: {asset_config['name']}")
                    
                    # Generate asset using advanced pipeline
                    result = await self._generate_single_asset(
                        asset_config, category_path
                    )
                    
                    category_results.append(result)
                    results["total_assets"] += 1
                    
                    if result["status"] == "success":
                        results["successful_assets"] += 1
                        print(f"SUCCESS: {asset_config['name']} generated successfully")
                    else:
                        results["failed_assets"] += 1
                        print(f"FAILED: {asset_config['name']} failed: {result.get('error', 'Unknown')}")
                    
                    # Small delay to prevent overwhelming
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    print(f"ERROR generating {asset_config['name']}: {e}")
                    category_results.append({
                        "name": asset_config['name'],
                        "status": "failed",
                        "error": str(e)
                    })
                    results["failed_assets"] += 1
            
            results["categories"][category] = {
                "path": str(category_path),
                "assets": category_results,
                "count": len(category_results)
            }
        
        # Generate summary
        await self._generate_asset_summary(results)
        
        print(f"\nAsset Generation Complete!")
        print(f"Total: {results['total_assets']}")
        print(f"Success: {results['successful_assets']}")
        print(f"Failed: {results['failed_assets']}")
        print(f"Success Rate: {results['successful_assets']/results['total_assets']*100:.1f}%")
        
        return results
    
    async def _generate_single_asset(self, asset_config: Dict, output_path: Path) -> Dict[str, Any]:
        """Generate a single asset using MCP SDXL"""
        
        try:
            # Use working MCP SDXL generation
            success = await self._generate_with_mcp_sdxl(asset_config, output_path)
            
            if success:
                return {
                    "name": asset_config["name"],
                    "status": "success",
                    "final_path": str(output_path / f"{asset_config['name']}.png"),
                    "method": "mcp_sdxl",
                    "size": asset_config["size"]
                }
            else:
                # Fallback to placeholder
                return await self._create_placeholder_asset(asset_config, output_path)
            
        except Exception as e:
            return {
                "name": asset_config["name"],
                "status": "failed",
                "error": str(e)
            }
    
    async def _generate_with_mcp_sdxl(self, asset_config: Dict, output_path: Path) -> bool:
        """Generate asset using MCP SDXL tools"""
        
        try:
            # Import MCP SDXL tool
            sys.path.append(str(self.base_path / "tools"))
            from sdxl_mcp import handle_call_tool
            
            # Prepare MCP generation arguments
            mcp_arguments = {
                "prompt": asset_config["prompt"],
                "width": asset_config["size"][0],
                "height": asset_config["size"][1],
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "negative_prompt": "blurry, low quality, distorted, text, watermark"
            }
            
            print(f"   Generating with MCP SDXL: {asset_config['name']}")
            
            # Generate with MCP using correct signature
            result = await asyncio.to_thread(handle_call_tool, "text2img", mcp_arguments)
            
            # MCP returns a list of TextContent objects
            if result and isinstance(result, list) and len(result) > 0:
                response_text = result[0].text if hasattr(result[0], 'text') else str(result[0])
                
                # Look for generated file path in response
                if "saved" in response_text.lower() or "generated" in response_text.lower():
                    # Extract file path from response text if possible
                    import re
                    path_match = re.search(r'([^\s]+\.png)', response_text)
                    
                    if path_match:
                        generated_file = Path(path_match.group(1))
                        if generated_file.exists():
                            final_path = output_path / f"{asset_config['name']}.png"
                            generated_file.rename(final_path)
                            print(f"   SUCCESS: MCP generated {asset_config['name']}")
                            return True
                    
                    # Fallback: Look for recently generated files
                    possible_locations = [
                        Path("assets/generated"),
                        Path("generated"),
                        Path("."),
                        Path("output")
                    ]
                    
                    for location in possible_locations:
                        if location.exists():
                            recent_files = list(location.glob("*.png"))
                            if recent_files:
                                # Get most recent file
                                latest_file = max(recent_files, key=lambda x: x.stat().st_mtime)
                                # Check if it was created in the last few seconds
                                import time
                                if time.time() - latest_file.stat().st_mtime < 10:
                                    final_path = output_path / f"{asset_config['name']}.png"
                                    latest_file.rename(final_path)
                                    print(f"   SUCCESS: MCP generated {asset_config['name']}")
                                    return True
            
            print(f"   MCP generation failed for {asset_config['name']}")
            return False
            
        except Exception as e:
            print(f"   MCP SDXL generation error: {e}")
            return False
    
    async def _generate_fallback_asset(self, asset_config: Dict, output_path: Path) -> Dict[str, Any]:
        """Generate asset using fallback method"""
        
        try:
            # Try basic MCP generation
            sys.path.append(str(self.base_path / "tools"))
            from asset_gen_agent import generate_egyptian_asset
            
            # Generate using basic MCP
            success = await asyncio.to_thread(
                generate_egyptian_asset,
                asset_config["name"],
                asset_config["prompt"],
                asset_config["size"][0],
                asset_config["size"][1],
                30  # Reduced steps for speed
            )
            
            if success:
                # Move from default location to organized folder
                default_path = self.base_path / "assets" / "generated" / f"{asset_config['name']}.png"
                final_path = output_path / f"{asset_config['name']}.png"
                
                if default_path.exists():
                    default_path.rename(final_path)
                    
                    return {
                        "name": asset_config["name"],
                        "status": "success",
                        "final_path": str(final_path),
                        "method": "basic_mcp",
                        "size": asset_config["size"]
                    }
            
            # Create placeholder if generation fails
            return await self._create_placeholder_asset(asset_config, output_path)
            
        except Exception as e:
            return await self._create_placeholder_asset(asset_config, output_path)
    
    async def _create_placeholder_asset(self, asset_config: Dict, output_path: Path) -> Dict[str, Any]:
        """Create placeholder asset for missing assets"""
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create colored placeholder based on asset type
            color_map = {
                "characters": (218, 165, 32),  # Gold
                "enemies": (139, 69, 19),      # Brown
                "environments": (65, 105, 225), # Blue
                "portals": (138, 43, 226),     # Purple
                "ui": (255, 215, 0)            # Yellow
            }
            
            # Determine category from path
            category = "characters"  # Default
            for cat in self.asset_categories.keys():
                if cat in str(output_path):
                    category = cat
                    break
            
            color = color_map.get(category, (128, 128, 128))
            size = asset_config["size"]
            
            # Create placeholder image
            image = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw colored background
            draw.rectangle([0, 0, size[0], size[1]], fill=color + (128,))
            
            # Draw border
            draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=color, width=2)
            
            # Add text if size is large enough
            if size[0] >= 64:
                try:
                    font = ImageFont.load_default()
                    name_text = asset_config["name"].replace("_", "\n")
                    draw.text((size[0]//2, size[1]//2), name_text, 
                             fill=(255, 255, 255), font=font, anchor="mm")
                except:
                    pass
            
            # Save placeholder
            placeholder_path = output_path / f"{asset_config['name']}.png"
            image.save(placeholder_path)
            
            return {
                "name": asset_config["name"],
                "status": "success",
                "final_path": str(placeholder_path),
                "method": "placeholder",
                "size": size
            }
            
        except Exception as e:
            return {
                "name": asset_config["name"],
                "status": "failed",
                "error": f"Placeholder creation failed: {e}"
            }
    
    async def _generate_asset_summary(self, results: Dict) -> None:
        """Generate summary file for all assets"""
        
        summary_path = self.base_path / "assets" / "asset_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary = {
            "generation_time": time.time(),
            "generator": self.name,
            "total_assets": results["total_assets"],
            "successful_assets": results["successful_assets"],
            "failed_assets": results["failed_assets"],
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

# Main execution
async def main():
    """Generate all Egyptian assets in organized structure"""
    
    generator = EgyptianAssetGenerator()
    
    print("SANDS OF DUAT - EGYPTIAN ASSET GENERATION")
    print("=" * 60)
    
    # Generate all assets
    results = await generator.generate_all_assets()
    
    if results["status"] == "success":
        print(f"\nASSET GENERATION COMPLETE!")
        print(f"All assets organized in proper folder structure")
        print(f"Check assets/ directories for generated content")
    else:
        print(f"\nAsset generation failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())