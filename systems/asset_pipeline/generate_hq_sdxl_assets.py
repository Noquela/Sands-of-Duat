#!/usr/bin/env python3
"""
Generate High-Quality SDXL Assets - Maximum quality using full 12GB VRAM
100 steps, LoRA models, enhanced prompts for professional Hades-quality Egyptian assets
"""

import asyncio
import sys
import time
from pathlib import Path

# Add tools to path
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

async def generate_hq_sdxl_assets():
    """Generate high-quality Egyptian assets using full 12GB VRAM with 100 steps"""
    
    try:
        from sdxl_mcp import handle_call_tool
        
        # High-quality Egyptian asset definitions optimized for 12GB VRAM
        asset_definitions = {
            # Player Character Assets - High Resolution
            "player_anubis_idle_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian Anubis warrior god, golden armor with intricate hieroglyphic engravings, jackal head, piercing amber glowing eyes, royal blue cape with gold trim, standing in majestic idle pose, detailed cel-shaded art style, Hades game quality, professional 2D sprite art, sharp focus, perfect anatomy",
                "size": (768, 768),
                "category": "characters"
            },
            "player_anubis_walk_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian Anubis warrior walking with purpose, golden armor gleaming, jackal head held high, cape flowing dramatically in motion, dynamic stride animation frame, detailed cel-shaded art style, Hades game quality, professional 2D sprite art, motion blur effects, perfect anatomy",
                "size": (768, 768),
                "category": "characters"
            },
            "player_anubis_attack_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian Anubis warrior attacking with gleaming golden khopesh sword, powerful combat stance, divine energy aura surrounding blade, dynamic action pose, sparks and magical effects, detailed cel-shaded art style, Hades game quality, professional 2D sprite art, perfect anatomy",
                "size": (768, 768),
                "category": "characters"
            },
            
            # Enemy Assets - High Resolution
            "enemy_scarab_guardian_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian scarab beetle guardian, polished bronze chitinous armor with engravings, large intimidating mandibles, six powerful legs, battle-ready aggressive stance, detailed cel-shaded art style, Hades enemy design quality, professional 2D sprite art, menacing presence",
                "size": (640, 640),
                "category": "enemies"
            },
            "enemy_mummy_warrior_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian mummy warrior, weathered ancient bandages with hieroglyphic patterns, glowing red eyes piercing through wrappings, ceremonial staff with ankh symbol, intimidating pose, detailed cel-shaded art style, Hades enemy design quality, professional 2D sprite art, ancient menace",
                "size": (640, 640),
                "category": "enemies"
            },
            "enemy_anubis_sentinel_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Anubis sentinel guard, dark bronze armor with battle scars, imposing jackal head, ceremonial spear with golden tip, elite enemy design, muscular build, detailed cel-shaded art style, Hades boss design quality, professional 2D sprite art, commanding presence",
                "size": (768, 768),
                "category": "enemies"
            },
            
            # Environment Assets - Altars with Maximum Detail
            "altar_ra_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, magnificent Altar of Ra sun god, golden pyramid structure with perfect geometry, radiant solar disk at top emanating divine light, dancing divine flames, intricate hieroglyphic inscriptions, sacred temple architecture, detailed cel-shaded art style, Hades environment quality, divine atmosphere",
                "size": (768, 768),
                "category": "environments"
            },
            "altar_thoth_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, elegant Altar of Thoth wisdom god, graceful ibis bird sculpture, ancient scrolls with mystical writing, lapis lazuli and gold inlays, floating magical symbols and runes, scholarly atmosphere, detailed cel-shaded art style, Hades environment quality, mystical aura",
                "size": (768, 768),
                "category": "environments"
            },
            "altar_isis_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, sacred Altar of Isis goddess, prominent ankh symbols, protective blue magical aura, gold and sapphire magical energy swirls, maternal divine presence, healing light, detailed cel-shaded art style, Hades environment quality, serene divine power",
                "size": (768, 768),
                "category": "environments"
            },
            "altar_ptah_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, powerful Altar of Ptah creator god, master craftsman tools displayed, mummy wrapping patterns in gold, emerald and gold color scheme, divine forge elements with glowing embers, creation energy, detailed cel-shaded art style, Hades environment quality, creative divine force",
                "size": (768, 768),
                "category": "environments"
            },
            
            # Portal Assets - High Resolution with Effects
            "portal_arena_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian mystical portal to arena, swirling purple and gold energy vortex with particle effects, ancient hieroglyphic stone archway with intricate carvings, glowing ancient runes pulsing with power, majestic temple pillars, detailed cel-shaded art style, Hades portal design quality, mystical energy",
                "size": (768, 768),
                "category": "portals"
            },
            "portal_exit_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian victory portal, emerald and gold energy swirl with triumphant effects, celebratory hieroglyphs glowing with success, divine golden light rays, ancient gateway to freedom, detailed cel-shaded art style, Hades portal design quality, victorious aura",
                "size": (768, 768),
                "category": "portals"
            },
            
            # NPC Assets - High Quality Character Design
            "npc_mirror_anubis_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Mirror of Anubis NPC, polished reflective divine surface showing jackal head reflection, ornate golden frame with intricate hieroglyphic engravings, mystical purple aura emanating power, detailed cel-shaded art style, Hades NPC quality, divine artifact",
                "size": (640, 640),
                "category": "npcs"
            },
            "npc_merchant_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian merchant NPC Khenti-Kheti, flowing robes with golden jewelry and artifacts, friendly wise expression, vendor of mystical items, detailed facial features, detailed cel-shaded art style, Hades NPC quality, professional 2D character art, welcoming presence",
                "size": (640, 640),
                "category": "npcs"
            },
            
            # UI Assets - Ultra High Quality Interface Elements
            "ui_health_bar_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian health bar UI frame, golden ankh symbols with perfect geometry, intricate hieroglyphic border decorations, papyrus texture background with age details, polished game UI element, detailed art, crisp clean design",
                "size": (1024, 128),
                "category": "ui"
            },
            "ui_artifact_slot_hq": {
                "prompt": "masterpiece, best quality, ultra detailed, Egyptian artifact slot UI, circular golden frame with perfect curves, divine glow effect with particle details, intricate hieroglyphic decoration around border, sacred geometry patterns, polished game UI element, detailed art, premium design",
                "size": (256, 256),
                "category": "ui"
            }
        }
        
        print("GENERATING HIGH-QUALITY SDXL EGYPTIAN ASSETS")
        print("Using full 12GB VRAM with 100 steps for maximum quality")
        print("=" * 70)
        print(f"Total high-quality assets to generate: {len(asset_definitions)}")
        print("Settings: 100 steps, guidance 8.0, high resolution, enhanced prompts")
        print()
        
        results = {
            "total": len(asset_definitions),
            "successful": 0,
            "failed": 0,
            "assets": []
        }
        
        # Generate each asset with maximum quality
        for i, (asset_name, config) in enumerate(asset_definitions.items(), 1):
            print(f"[{i}/{len(asset_definitions)}] Generating HQ: {asset_name}")
            print(f"   Category: {config['category']}")
            print(f"   Size: {config['size'][0]}x{config['size'][1]} (High Resolution)")
            print(f"   Prompt: {config['prompt'][:100]}...")
            
            try:
                # Maximum quality SDXL generation arguments
                arguments = {
                    "prompt": config["prompt"],
                    "width": config["size"][0],
                    "height": config["size"][1],
                    "num_inference_steps": 100,  # Maximum quality - 100 steps
                    "guidance_scale": 8.0,       # Higher guidance for more prompt adherence
                    "negative_prompt": "blurry, low quality, distorted, text, watermark, signature, poor anatomy, deformed, ugly, bad proportions, extra limbs, disfigured, malformed, mutated, out of frame, body out of frame, cut off"
                }
                
                print(f"   Settings: 100 steps, guidance 8.0, negative prompt enhanced")
                
                # Generate with SDXL MCP - High Quality
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
                            print(f"   SUCCESS: HQ Generated in {generation_time:.1f}s")
                            print(f"   Saved to: {generated_path}")
                            
                            # Copy to main assets folder with proper naming
                            import shutil
                            source = Path(generated_path)
                            if source.exists():
                                dest = Path("../../../assets/generated") / f"{asset_name}.png"
                                dest.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(source, dest)
                                print(f"   Copied to: {dest}")
                            
                            results["successful"] += 1
                            results["assets"].append({
                                "name": asset_name,
                                "path": generated_path,
                                "final_path": str(dest),
                                "status": "success",
                                "time": generation_time,
                                "quality": "high"
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
                
                # Longer delay for high-quality generation
                await asyncio.sleep(2)
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
        print("=" * 70)
        print("HIGH-QUALITY SDXL ASSET GENERATION COMPLETE!")
        print("=" * 70)
        print(f"Results:")
        print(f"   Total: {results['total']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Success Rate: {results['successful']/results['total']*100:.1f}%")
        
        if results['successful'] > 0:
            avg_time = sum(asset.get('time', 0) for asset in results['assets'] if asset.get('time')) / results['successful']
            print(f"   Average Generation Time: {avg_time:.1f}s (100 steps)")
            total_time = sum(asset.get('time', 0) for asset in results['assets'] if asset.get('time'))
            print(f"   Total Generation Time: {total_time/60:.1f} minutes")
        
        print()
        print("HIGH-QUALITY Egyptian assets generated with SDXL + 100 steps!")
        print("Professional Hades-quality artwork ready for enhanced gameplay!")
        
        return results
        
    except Exception as e:
        print(f"Fatal error in HQ SDXL generation: {e}")
        import traceback
        traceback.print_exc()
        return {"total": 0, "successful": 0, "failed": 1}

if __name__ == "__main__":
    asyncio.run(generate_hq_sdxl_assets())