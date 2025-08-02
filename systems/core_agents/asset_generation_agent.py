#!/usr/bin/env python3
"""
Asset Generation Agent - Specialized sub-agent for AI-powered Egyptian asset creation
Handles automated sprite generation, environment assets, and Egyptian-themed content
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import sys

class AssetGenerationAgent:
    """Specialized agent for Egyptian asset generation using SDXL"""
    
    def __init__(self):
        self.name = "AssetGenerationAgent"
        self.capabilities = [
            "sprite_sheet_generation",
            "environment_asset_creation", 
            "egyptian_themed_content",
            "character_animations",
            "ui_elements"
        ]
        self.active_generations = {}
        
        print(f"{self.name} initialized")
        print(f"   Capabilities: {', '.join(self.capabilities)}")
    
    async def generate_sprite_sheet(self, sprite_type: str, **parameters) -> Dict[str, Any]:
        """Generate animated sprite sheets for characters"""
        print(f"Generating {sprite_type} sprite sheet...")
        
        start_time = time.time()
        results = {}
        
        try:
            if sprite_type == "player":
                results = await self._generate_player_sprites(**parameters)
            elif sprite_type == "enemy":
                results = await self._generate_enemy_sprites(**parameters)
            else:
                raise ValueError(f"Unknown sprite type: {sprite_type}")
            
            duration = time.time() - start_time
            results["generation_time"] = duration
            results["status"] = "success"
            
            print(f"SUCCESS: {sprite_type} sprites generated in {duration:.2f}s")
            return results
            
        except Exception as e:
            print(f"FAILED to generate {sprite_type} sprites: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _generate_player_sprites(self, character: str, animations: List[str], 
                                     size: tuple, frames: int, **kwargs) -> Dict[str, Any]:
        """Generate player character sprite sheets"""
        generated_assets = []
        
        for animation in animations:
            asset_name = f"player_{character}_{animation}"
            
            # Define Egyptian player prompts
            prompts = {
                "anubis_warrior": {
                    "idle": "Egyptian god Anubis warrior, golden armor, jackal head, amber eyes, royal pose, ceremonial cape, hieroglyphic engravings, Hades game style, standing pose, idle animation, breathing, subtle movement",
                    "walk": "Anubis warrior walking, golden armor, jackal head, cape flowing, dynamic movement, Egyptian god, Hades style, walking cycle, side view, legs moving, step sequence",
                    "attack": "Anubis warrior attacking, golden khopesh sword, combat pose, divine energy, hieroglyphic blade, Hades combat style, attacking pose, weapon swing, combat stance, action sequence",
                    "dash": "Anubis warrior dashing, speed blur effect, divine energy trail, golden aura, quick movement, Egyptian god power, Hades dash style, motion blur, energy streak"
                }
            }
            
            character_prompts = prompts.get(character, prompts["anubis_warrior"])
            prompt = character_prompts.get(animation, character_prompts["idle"])
            
            # Add sprite sheet parameters
            prompt += f", sprite sheet, {frames}x1 grid, game asset, detailed"
            
            # Generate using SDXL MCP
            result = await self._call_sdxl_generation(
                prompt=prompt,
                asset_name=asset_name,
                width=size[0],
                height=size[1],
                steps=75
            )
            
            if result["success"]:
                generated_assets.append({
                    "name": asset_name,
                    "animation": animation,
                    "frames": frames,
                    "path": result["path"]
                })
        
        return {
            "character": character,
            "generated_assets": generated_assets,
            "total_animations": len(animations)
        }
    
    async def _generate_enemy_sprites(self, enemies: List[str], animations: List[str],
                                    size: tuple, frames: int, **kwargs) -> Dict[str, Any]:
        """Generate enemy sprite sheets"""
        generated_assets = []
        
        for enemy in enemies:
            for animation in animations:
                asset_name = f"enemy_{enemy}_{animation}"
                
                # Define Egyptian enemy prompts
                prompts = {
                    "scarab_warrior": {
                        "idle": "Egyptian scarab beetle warrior, bronze armor, insect mandibles, six legs, chitinous shell, battle scars, Hades enemy style, standing pose, idle animation, breathing, subtle movement",
                        "walk": "Scarab warrior walking, bronze chitin armor, six legs moving, menacing patrol, dust clouds, Hades enemy animation, walking cycle, side view, legs moving, step sequence",
                        "attack": "Scarab warrior attacking, mandible strike, bronze claws, aggressive stance, chitin gleaming, Hades combat style, attacking pose, insect fury, combat sequence"
                    },
                    "mummy_guard": {
                        "idle": "Egyptian mummy guard, ancient bandages, glowing eyes, ceremonial staff, weathered wrappings, Hades undead style, standing pose, idle animation, subtle sway",
                        "walk": "Mummy guard walking, dragging steps, bandages flowing, staff in hand, ancient stride, Hades enemy animation, walking cycle, shambling movement",
                        "attack": "Mummy guard attacking, staff strike, bandages unwrapping, ancient fury, magical energy, Hades combat style, attacking pose, undead wrath"
                    },
                    "anubis_sentinel": {
                        "idle": "Anubis sentinel guard, dark armor, jackal head, glowing eyes, ceremonial spear, divine authority, Hades elite enemy style, standing pose, idle animation, regal bearing",
                        "walk": "Anubis sentinel walking, armor clanking, spear ready, divine patrol, authoritative stride, Hades enemy animation, walking cycle, measured steps",
                        "attack": "Anubis sentinel attacking, spear thrust, divine energy, dark armor gleaming, elite combat, Hades boss style, attacking pose, divine wrath"
                    }
                }
                
                enemy_prompts = prompts.get(enemy, prompts["scarab_warrior"])
                prompt = enemy_prompts.get(animation, enemy_prompts["idle"])
                
                # Add sprite sheet parameters  
                prompt += f", sprite sheet, {frames}x1 grid, game asset, detailed"
                
                # Generate using SDXL MCP
                result = await self._call_sdxl_generation(
                    prompt=prompt,
                    asset_name=asset_name,
                    width=size[0],
                    height=size[1],
                    steps=75
                )
                
                if result["success"]:
                    generated_assets.append({
                        "name": asset_name,
                        "enemy": enemy,
                        "animation": animation,
                        "frames": frames,
                        "path": result["path"]
                    })
        
        return {
            "enemies": enemies,
            "generated_assets": generated_assets,
            "total_sprites": len(enemies) * len(animations)
        }
    
    async def generate_environment(self, environment_type: str, **parameters) -> Dict[str, Any]:
        """Generate environment assets like altars, portals, UI elements"""
        print(f"🏛️ Generating {environment_type} environment assets...")
        
        start_time = time.time()
        
        try:
            if environment_type == "altars":
                results = await self._generate_altar_assets(**parameters)
            elif environment_type == "portals":
                results = await self._generate_portal_assets(**parameters)
            elif environment_type == "ui_elements":
                results = await self._generate_ui_assets(**parameters)
            else:
                raise ValueError(f"Unknown environment type: {environment_type}")
            
            duration = time.time() - start_time
            results["generation_time"] = duration
            results["status"] = "success"
            
            print(f"✅ {environment_type} assets generated in {duration:.2f}s")
            return results
            
        except Exception as e:
            print(f"❌ Failed to generate {environment_type}: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _generate_altar_assets(self, gods: List[str], size: tuple, 
                                   style: str, **kwargs) -> Dict[str, Any]:
        """Generate Egyptian god altar assets"""
        generated_altars = []
        
        # Egyptian god altar prompts
        altar_prompts = {
            "Ra": "Ra sun god altar, golden pyramid, solar disk, hieroglyphs glowing, sacred flames, divine light, Hades shrine style",
            "Thoth": "Thoth wisdom altar, ibis bird sculpture, ancient scrolls, magical symbols, lapis lazuli, gold, Hades shrine style", 
            "Isis": "Isis magic altar, ankh symbols, blue gold aura, magical energy, divine feminine, protective presence, Hades shrine style",
            "Ptah": "Ptah creator altar, craftsman tools, mummy wrapping patterns, emerald gold, divine forge, Hades crafting style"
        }
        
        for god in gods:
            asset_name = f"altar_{god.lower()}"
            prompt = altar_prompts.get(god, altar_prompts["Ra"])
            
            result = await self._call_sdxl_generation(
                prompt=prompt,
                asset_name=asset_name,
                width=size[0],
                height=size[1],
                steps=75
            )
            
            if result["success"]:
                generated_altars.append({
                    "name": asset_name,
                    "god": god,
                    "path": result["path"]
                })
        
        return {
            "altar_style": style,
            "generated_altars": generated_altars,
            "gods": gods
        }
    
    async def _generate_portal_assets(self, portal_types: List[str], size: tuple, **kwargs) -> Dict[str, Any]:
        """Generate portal assets for scene transitions"""
        generated_portals = []
        
        portal_prompts = {
            "arena": "Egyptian mystical portal, purple gold energy vortex, hieroglyphic archway, glowing runes, stone pillars, Hades portal style",
            "exit": "Egyptian victory portal, emerald gold vortex, celebratory hieroglyphs, ancient gates, divine light, Hades portal style",
            "secret": "Egyptian hidden portal, dark energy swirl, mysterious symbols, shadowy archway, ancient secrets, Hades hidden style"
        }
        
        for portal_type in portal_types:
            asset_name = f"portal_{portal_type}"
            prompt = portal_prompts.get(portal_type, portal_prompts["arena"])
            
            result = await self._call_sdxl_generation(
                prompt=prompt,
                asset_name=asset_name,
                width=size[0],
                height=size[1],
                steps=75
            )
            
            if result["success"]:
                generated_portals.append({
                    "name": asset_name,
                    "type": portal_type,
                    "path": result["path"]
                })
        
        return {
            "generated_portals": generated_portals,
            "portal_types": portal_types
        }
    
    async def _generate_ui_assets(self, ui_elements: List[str], size: tuple, **kwargs) -> Dict[str, Any]:
        """Generate UI elements with Egyptian theming"""
        generated_ui = []
        
        ui_prompts = {
            "health_bar": "Egyptian health bar, golden ankh symbols, hieroglyphic frame, papyrus texture, Hades UI style",
            "mana_bar": "Egyptian mana bar, blue energy, sacred scarab, magical glow, ancient design, Hades UI style",
            "inventory_frame": "Egyptian inventory frame, golden borders, hieroglyphic patterns, papyrus background, Hades UI style",
            "button_normal": "Egyptian button, golden frame, hieroglyphic decoration, hover glow, Hades UI style",
            "artifact_slot": "Egyptian artifact slot, circular frame, golden border, divine glow, Hades boon style"
        }
        
        for ui_element in ui_elements:
            asset_name = f"ui_{ui_element}"
            prompt = ui_prompts.get(ui_element, ui_prompts["button_normal"])
            
            result = await self._call_sdxl_generation(
                prompt=prompt,
                asset_name=asset_name,
                width=size[0],
                height=size[1],
                steps=50  # UI elements need fewer steps
            )
            
            if result["success"]:
                generated_ui.append({
                    "name": asset_name,
                    "element": ui_element,
                    "path": result["path"]
                })
        
        return {
            "generated_ui": generated_ui,
            "ui_elements": ui_elements
        }
    
    async def _call_sdxl_generation(self, prompt: str, asset_name: str, 
                                   width: int, height: int, steps: int) -> Dict[str, Any]:
        """Call advanced SDXL generation with Hades-quality techniques"""
        try:
            # Try advanced generation first
            try:
                from ..advanced_generation.advanced_asset_generation_agent import AdvancedAssetGenerationAgent
                
                # Use advanced agent for high-quality generation
                advanced_agent = AdvancedAssetGenerationAgent()
                
                # Setup if not already done
                if not hasattr(advanced_agent, '_pipeline_ready'):
                    await advanced_agent.setup_advanced_pipeline()
                    advanced_agent._pipeline_ready = True
                
                # Generate with advanced techniques
                result = await advanced_agent.generate_advanced_egyptian_asset(
                    asset_name=asset_name,
                    prompt=prompt,
                    width=width,
                    height=height,
                    style="hades_egyptian",
                    use_controlnet=True,
                    use_lora=True,
                    upscale=True
                )
                
                if result["status"] == "success":
                    return {
                        "success": True,
                        "path": result["output_path"],
                        "prompt": prompt,
                        "dimensions": result["dimensions"],
                        "generation_time": result["generation_time"],
                        "advanced_techniques": True
                    }
                else:
                    print(f"⚠️ Advanced generation failed, falling back to standard: {result.get('error', '')}")
                    
            except Exception as advanced_error:
                print(f"⚠️ Advanced agent failed: {advanced_error}")
                print("🔄 Falling back to standard SDXL generation...")
            
            # Fallback to standard generation
            sys.path.append(str(Path(__file__).parent.parent / "tools"))
            from asset_gen_agent import generate_egyptian_asset
            
            # Generate the asset with standard method
            result = await asyncio.to_thread(
                generate_egyptian_asset,
                asset_name, prompt, width, height, steps
            )
            
            if result:
                asset_path = Path("assets/generated") / f"{asset_name}.png"
                return {
                    "success": True,
                    "path": str(asset_path),
                    "prompt": prompt,
                    "dimensions": (width, height),
                    "advanced_techniques": False
                }
            else:
                return {"success": False, "error": "Standard generation failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_generation_status(self) -> Dict[str, Any]:
        """Get current generation status"""
        return {
            "agent_name": self.name,
            "active_generations": len(self.active_generations),
            "capabilities": self.capabilities
        }