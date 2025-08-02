#!/usr/bin/env python3
"""
Generate All SDXL Assets - Create all Egyptian game assets using SDXL pipeline
"""

import asyncio
import sys
import time
from pathlib import Path

# Add tools to path
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

async def generate_all_sdxl_assets():
    """Generate all Egyptian assets using SDXL MCP pipeline"""
    
    try:
        from sdxl_mcp import handle_call_tool
        
        # Egyptian asset definitions with optimized prompts for SDXL
        asset_definitions = {
            # Player Character Assets
            "player_anubis_idle": {
                "prompt": "masterpiece, Egyptian Anubis warrior god, golden armor with hieroglyphic engravings, jackal head, amber glowing eyes, royal blue cape, standing idle pose, detailed cel-shaded art style, Hades game quality, 2D sprite art",
                "size": (512, 512),
                "category": "characters"
            },
            "player_anubis_walk": {
                "prompt": "masterpiece, Egyptian Anubis warrior walking, golden armor, jackal head, cape flowing in motion, dynamic stride animation, detailed cel-shaded art style, Hades game quality, 2D sprite art",
                "size": (512, 512),
                "category": "characters"
            },
            "player_anubis_attack": {
                "prompt": "masterpiece, Egyptian Anubis warrior attacking with golden khopesh sword, combat stance, divine energy aura, dynamic action pose, detailed cel-shaded art style, Hades game quality, 2D sprite art",
                "size": (512, 512),
                "category": "characters"
            },
            
            # Enemy Assets
            "enemy_scarab_guardian": {
                "prompt": "masterpiece, Egyptian scarab beetle guardian, bronze chitinous armor, large mandibles, six legs, battle-ready stance, detailed cel-shaded art style, Hades enemy design, 2D sprite art",
                "size": (384, 384),
                "category": "enemies"
            },
            "enemy_mummy_warrior": {
                "prompt": "masterpiece, Egyptian mummy warrior, ancient bandages, glowing red eyes, ceremonial staff, weathered wrappings, detailed cel-shaded art style, Hades enemy design, 2D sprite art",
                "size": (384, 384),
                "category": "enemies"
            },
            "enemy_anubis_sentinel": {
                "prompt": "masterpiece, Anubis sentinel guard, dark bronze armor, jackal head, ceremonial spear, elite enemy design, detailed cel-shaded art style, Hades boss design, 2D sprite art",
                "size": (512, 512),
                "category": "enemies"
            },
            
            # Environment Assets - Altars
            "altar_ra": {
                "prompt": "masterpiece, Altar of Ra sun god, golden pyramid structure, solar disk at top, divine flames, hieroglyphic inscriptions, sacred temple architecture, detailed cel-shaded art style, Hades environment quality",
                "size": (512, 512),
                "category": "environments"
            },
            "altar_thoth": {
                "prompt": "masterpiece, Altar of Thoth wisdom god, ibis bird sculpture, ancient scrolls, lapis lazuli and gold details, magical symbols floating, detailed cel-shaded art style, Hades environment quality",
                "size": (512, 512),
                "category": "environments"
            },
            "altar_isis": {
                "prompt": "masterpiece, Altar of Isis goddess, ankh symbols, protective blue aura, gold and sapphire magical energy, maternal divine presence, detailed cel-shaded art style, Hades environment quality",
                "size": (512, 512),
                "category": "environments"
            },
            "altar_ptah": {
                "prompt": "masterpiece, Altar of Ptah creator god, craftsman tools, mummy wrapping patterns, emerald and gold colors, divine forge elements, detailed cel-shaded art style, Hades environment quality",
                "size": (512, 512),
                "category": "environments"
            },
            
            # Portal Assets
            "portal_arena": {
                "prompt": "masterpiece, Egyptian mystical portal to arena, purple and gold energy vortex, hieroglyphic stone archway, glowing ancient runes, temple pillars, detailed cel-shaded art style, Hades portal design",
                "size": (512, 512),
                "category": "portals"
            },
            "portal_exit": {
                "prompt": "masterpiece, Egyptian victory portal, emerald and gold energy swirl, celebratory hieroglyphs, divine golden light, ancient gateway, detailed cel-shaded art style, Hades portal design",
                "size": (512, 512),
                "category": "portals"
            },
            
            # NPC Assets
            "npc_mirror_anubis": {
                "prompt": "masterpiece, Mirror of Anubis NPC, reflective divine surface, jackal head reflection, golden frame with hieroglyphs, mystical aura, detailed cel-shaded art style, Hades NPC quality",
                "size": (384, 384),
                "category": "npcs"
            },
            "npc_merchant": {
                "prompt": "masterpiece, Egyptian merchant NPC Khenti-Kheti, robes and golden jewelry, artifact vendor, friendly expression, detailed cel-shaded art style, Hades NPC quality, 2D sprite art",
                "size": (384, 384),
                "category": "npcs"
            },
            
            # UI Assets
            "ui_health_bar": {
                "prompt": "masterpiece, Egyptian health bar UI frame, golden ankh symbols, hieroglyphic border decoration, papyrus texture background, game UI element, detailed art",
                "size": (512, 64),
                "category": "ui"
            },
            "ui_artifact_slot": {
                "prompt": "masterpiece, Egyptian artifact slot UI, circular golden frame, divine glow effect, hieroglyphic decoration, sacred geometry, game UI element, detailed art",
                "size": (128, 128),
                "category": "ui"
            }
        }
        
        print("GENERATING ALL SDXL EGYPTIAN ASSETS")
        print("=" * 60)
        print(f"Total assets to generate: {len(asset_definitions)}")
        print("Using RTX 5070 with SDXL pipeline...")
        print()
        
        results = {
            "total": len(asset_definitions),
            "successful": 0,
            "failed": 0,
            "assets": []
        }
        
        # Generate each asset
        for i, (asset_name, config) in enumerate(asset_definitions.items(), 1):
            print(f"[{i}/{len(asset_definitions)}] Generating: {asset_name}")
            print(f"   Category: {config['category']}")
            print(f"   Size: {config['size'][0]}x{config['size'][1]}")
            print(f"   Prompt: {config['prompt'][:80]}...")
            
            try:
                # Prepare SDXL generation arguments
                arguments = {
                    "prompt": config["prompt"],
                    "width": config["size"][0],
                    "height": config["size"][1],
                    "num_inference_steps": 30,  # Higher quality
                    "guidance_scale": 7.5,
                    "negative_prompt": "blurry, low quality, distorted, text, watermark, signature, poor anatomy, deformed"
                }
                
                # Generate with SDXL MCP
                start_time = time.time()
                result = await handle_call_tool("text2img", arguments)
                generation_time = time.time() - start_time
                
                if result and isinstance(result, list) and len(result) > 0:
                    response_text = result[0].text if hasattr(result[0], 'text') else str(result[0])
                    
                    if "SUCCESS" in response_text and "Saved to:" in response_text:
                        # Extract file path
                        import re
                        path_match = re.search(r'Saved to: ([^\n]+)', response_text)
                        if path_match:
                            generated_path = path_match.group(1).strip()
                            print(f"   SUCCESS: Generated in {generation_time:.1f}s")
                            print(f"   Saved to: {generated_path}")
                            
                            results["successful"] += 1
                            results["assets"].append({
                                "name": asset_name,
                                "path": generated_path,
                                "status": "success",
                                "time": generation_time
                            })
                        else:
                            print(f"   FAILED: Could not extract file path")
                            results["failed"] += 1
                    else:
                        print(f"   FAILED: {response_text}")
                        results["failed"] += 1
                else:
                    print(f"   FAILED: No valid result from SDXL")
                    results["failed"] += 1
                
                # Small delay between generations
                await asyncio.sleep(1)
                print()
                
            except Exception as e:
                print(f"   ERROR: {e}")
                results["failed"] += 1
                results["assets"].append({
                    "name": asset_name,
                    "status": "failed",
                    "error": str(e)
                })
                print()
        
        # Final summary
        print("=" * 60)
        print("SDXL ASSET GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Results:")
        print(f"   Total: {results['total']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Success Rate: {results['successful']/results['total']*100:.1f}%")
        
        if results['successful'] > 0:
            avg_time = sum(asset.get('time', 0) for asset in results['assets'] if asset.get('time')) / results['successful']
            print(f"   Average Generation Time: {avg_time:.1f}s")
        
        print()
        print("All Egyptian assets generated with SDXL!")
        print("Ready for enhanced Sands of Duat gameplay!")
        
        return results
        
    except Exception as e:
        print(f"Fatal error in SDXL generation: {e}")
        import traceback
        traceback.print_exc()
        return {"total": 0, "successful": 0, "failed": 1}

if __name__ == "__main__":
    asyncio.run(generate_all_sdxl_assets())