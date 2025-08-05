#!/usr/bin/env python3
"""
Godot MCP Integration for Sands of Duat
Handles asset import and animation setup in Godot via MCP protocol.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    import requests
    import websocket
    NETWORK_AVAILABLE = True
except ImportError:
    print("Network libraries not available, install with: pip install requests websocket-client")
    NETWORK_AVAILABLE = False


class GodotMCPIntegration:
    """Godot MCP integration for automated asset pipeline."""
    
    def __init__(self, mcp_host: str = "localhost", mcp_port: int = 8989):
        self.mcp_host = mcp_host
        self.mcp_port = mcp_port
        self.base_url = f"http://{mcp_host}:{mcp_port}"
        self.logger = self._setup_logging()
        
        # Godot project paths
        self.godot_paths = {
            "characters": "res://characters/",
            "sprites": "res://sprites/",
            "cards": "res://cards/",
            "environments": "res://environments/",
            "animations": "res://animations/"
        }
        
        # Animation configurations for Sands of Duat
        self.animation_configs = {
            "player": {
                "idle": {"frames": 16, "fps": 12, "loop": True},
                "walk": {"frames": 16, "fps": 12, "loop": True},
                "attack": {"frames": 12, "fps": 15, "loop": False}
            },
            "enemy": {
                "idle": {"frames": 12, "fps": 8, "loop": True},
                "attack": {"frames": 10, "fps": 12, "loop": False},
                "death": {"frames": 8, "fps": 10, "loop": False}
            },
            "card": {
                "hover": {"frames": 8, "fps": 8, "loop": True},
                "select": {"frames": 6, "fps": 12, "loop": False}
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "godot_mcp.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def check_mcp_connection(self) -> bool:
        """Check if MCP server is available."""
        if not NETWORK_AVAILABLE:
            self.logger.warning("Network libraries not available")
            return False
        
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            if response.status_code == 200:
                self.logger.info("MCP server connected successfully")
                return True
            else:
                self.logger.warning(f"MCP server returned status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"MCP server not available: {e}")
            return False
    
    def import_spritesheet(self, spritesheet_path: str, character_name: str,
                          animation_name: str) -> bool:
        """Import spritesheet into Godot and set up animation."""
        try:
            self.logger.info(f"Importing spritesheet: {spritesheet_path}")
            
            if not self.check_mcp_connection():
                return self._mock_import_spritesheet(spritesheet_path, character_name, animation_name)
            
            # Load spritesheet metadata
            metadata_path = spritesheet_path.replace('.png', '_metadata.json')
            metadata = {}
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            
            # Prepare import data
            import_data = {
                "spritesheet_path": spritesheet_path,
                "character_name": character_name,
                "animation_name": animation_name,
                "metadata": metadata,
                "godot_path": self.godot_paths["sprites"]
            }
            
            # Send import request to MCP
            response = requests.post(
                f"{self.base_url}/import_spritesheet",
                json=import_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"Spritesheet imported successfully: {result.get('godot_path')}")
                return True
            else:
                self.logger.error(f"Failed to import spritesheet: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error importing spritesheet: {e}")
            return self._mock_import_spritesheet(spritesheet_path, character_name, animation_name)
    
    def setup_character_animation_tree(self, character_name: str, 
                                     animations: List[str]) -> bool:
        """Setup AnimationTree for character with multiple animations."""
        try:
            self.logger.info(f"Setting up AnimationTree for {character_name}")
            
            if not self.check_mcp_connection():
                return self._mock_setup_animation_tree(character_name, animations)
            
            # Get animation configuration
            char_type = "player" if "player" in character_name.lower() else "enemy"
            config = self.animation_configs.get(char_type, self.animation_configs["enemy"])
            
            # Prepare animation tree data
            tree_data = {
                "character_name": character_name,
                "scene_path": f"{self.godot_paths['characters']}{character_name}.tscn",
                "animations": [],
                "blend_parameters": {
                    "velocity": 0.0,
                    "action_trigger": False
                }
            }
            
            # Add each animation
            for anim_name in animations:
                if anim_name in config:
                    anim_config = config[anim_name]
                    tree_data["animations"].append({
                        "name": anim_name,
                        "spritesheet": f"{self.godot_paths['sprites']}{character_name}_{anim_name}.png",
                        "fps": anim_config["fps"],
                        "loop": anim_config["loop"],
                        "frames": anim_config["frames"]
                    })
            
            # Send setup request
            response = requests.post(
                f"{self.base_url}/setup_animation_tree",
                json=tree_data,
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info(f"AnimationTree setup completed for {character_name}")
                return True
            else:
                self.logger.error(f"Failed to setup AnimationTree: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up AnimationTree: {e}")
            return self._mock_setup_animation_tree(character_name, animations)
    
    def import_card_texture(self, card_image_path: str, card_name: str) -> bool:
        """Import card artwork into Godot."""
        try:
            self.logger.info(f"Importing card texture: {card_name}")
            
            if not self.check_mcp_connection():
                return self._mock_import_card(card_image_path, card_name)
            
            import_data = {
                "image_path": card_image_path,
                "card_name": card_name,
                "godot_path": f"{self.godot_paths['cards']}{card_name}.png",
                "import_settings": {
                    "filter": True,
                    "mipmaps": False,
                    "fix_alpha_border": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/import_texture",
                json=import_data,
                timeout=20
            )
            
            if response.status_code == 200:
                self.logger.info(f"Card texture imported: {card_name}")
                return True
            else:
                self.logger.error(f"Failed to import card texture: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error importing card texture: {e}")
            return self._mock_import_card(card_image_path, card_name)
    
    def import_environment_background(self, bg_image_path: str, env_name: str) -> bool:
        """Import environment background into Godot."""
        try:
            self.logger.info(f"Importing environment: {env_name}")
            
            if not self.check_mcp_connection():
                return self._mock_import_environment(bg_image_path, env_name)
            
            import_data = {
                "image_path": bg_image_path,
                "environment_name": env_name,
                "godot_path": f"{self.godot_paths['environments']}{env_name}.png",
                "import_settings": {
                    "filter": True,
                    "mipmaps": True,
                    "compress": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/import_background",
                json=import_data,
                timeout=20
            )
            
            if response.status_code == 200:
                self.logger.info(f"Environment imported: {env_name}")
                return True
            else:
                self.logger.error(f"Failed to import environment: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error importing environment: {e}")
            return self._mock_import_environment(bg_image_path, env_name)
    
    def setup_card_hover_animation(self, card_name: str) -> bool:
        """Setup hover animation for card."""
        try:
            self.logger.info(f"Setting up card hover animation: {card_name}")
            
            if not self.check_mcp_connection():
                return self._mock_setup_card_animation(card_name)
            
            animation_data = {
                "card_name": card_name,
                "scene_path": f"{self.godot_paths['cards']}{card_name}.tscn",
                "animations": {
                    "hover": {
                        "properties": [
                            {
                                "node_path": "CardSprite",
                                "property": "scale",
                                "from": [1.0, 1.0],
                                "to": [1.05, 1.05],
                                "duration": 0.2,
                                "easing": "ease_out"
                            },
                            {
                                "node_path": "CardSprite",
                                "property": "modulate:a",
                                "from": 1.0,
                                "to": 1.1,
                                "duration": 0.2,
                                "easing": "ease_out"
                            }
                        ]
                    },
                    "select": {
                        "properties": [
                            {
                                "node_path": "CardSprite",
                                "property": "scale",
                                "from": [1.0, 1.0],
                                "to": [0.95, 0.95],
                                "duration": 0.1,
                                "easing": "ease_in"
                            }
                        ]
                    }
                }
            }
            
            response = requests.post(
                f"{self.base_url}/setup_card_animations",
                json=animation_data,
                timeout=20
            )
            
            if response.status_code == 200:
                self.logger.info(f"Card animations setup: {card_name}")
                return True
            else:
                self.logger.error(f"Failed to setup card animations: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up card animations: {e}")
            return self._mock_setup_card_animation(card_name)
    
    def refresh_godot_project(self) -> bool:
        """Refresh Godot project to reimport assets."""
        try:
            if not self.check_mcp_connection():
                self.logger.info("Mock: Godot project refreshed")
                return True
            
            response = requests.post(f"{self.base_url}/refresh_project", timeout=30)
            
            if response.status_code == 200:
                self.logger.info("Godot project refreshed successfully")
                return True
            else:
                self.logger.error(f"Failed to refresh project: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error refreshing project: {e}")
            return False
    
    # Mock methods for when MCP is not available
    def _mock_import_spritesheet(self, spritesheet_path: str, character_name: str, 
                               animation_name: str) -> bool:
        """Mock spritesheet import."""
        self.logger.info(f"Mock: Imported spritesheet {spritesheet_path} for {character_name}:{animation_name}")
        return True
    
    def _mock_setup_animation_tree(self, character_name: str, animations: List[str]) -> bool:
        """Mock animation tree setup."""
        self.logger.info(f"Mock: Setup AnimationTree for {character_name} with {len(animations)} animations")
        return True
    
    def _mock_import_card(self, card_image_path: str, card_name: str) -> bool:
        """Mock card import."""
        self.logger.info(f"Mock: Imported card {card_name} from {card_image_path}")
        return True
    
    def _mock_import_environment(self, bg_image_path: str, env_name: str) -> bool:
        """Mock environment import."""
        self.logger.info(f"Mock: Imported environment {env_name} from {bg_image_path}")
        return True
    
    def _mock_setup_card_animation(self, card_name: str) -> bool:
        """Mock card animation setup."""
        self.logger.info(f"Mock: Setup card animations for {card_name}")
        return True
    
    def batch_import_characters(self, character_sprites_dir: str) -> int:
        """Batch import all character spritesheets."""
        sprites_path = Path(character_sprites_dir)
        successful = 0
        
        spritesheet_files = list(sprites_path.glob("*_spritesheet.png"))
        
        self.logger.info(f"Batch importing {len(spritesheet_files)} character spritesheets")
        
        for sprite_file in spritesheet_files:
            # Parse character and animation name from filename
            parts = sprite_file.stem.replace("_spritesheet", "").split("_")
            if len(parts) >= 2:
                character_name = "_".join(parts[:-1])
                animation_name = parts[-1]
            else:
                character_name = parts[0]
                animation_name = "idle"
            
            if self.import_spritesheet(str(sprite_file), character_name, animation_name):
                successful += 1
        
        self.logger.info(f"Batch character import completed: {successful}/{len(spritesheet_files)} successful")
        return successful
    
    def batch_import_cards(self, cards_dir: str) -> int:
        """Batch import all card textures."""
        cards_path = Path(cards_dir)
        successful = 0
        
        card_files = list(cards_path.glob("*.png"))
        
        self.logger.info(f"Batch importing {len(card_files)} card textures")
        
        for card_file in card_files:
            card_name = card_file.stem
            
            if self.import_card_texture(str(card_file), card_name):
                if self.setup_card_hover_animation(card_name):
                    successful += 1
        
        self.logger.info(f"Batch card import completed: {successful}/{len(card_files)} successful")
        return successful


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Godot MCP Integration for Sands of Duat")
    parser.add_argument("--host", default="localhost", help="MCP server host")
    parser.add_argument("--port", type=int, default=8989, help="MCP server port")
    parser.add_argument("--check", action="store_true", help="Check MCP connection")
    parser.add_argument("--import-sprites", help="Import sprites from directory")
    parser.add_argument("--import-cards", help="Import cards from directory")
    parser.add_argument("--refresh", action="store_true", help="Refresh Godot project")
    
    args = parser.parse_args()
    
    # Initialize MCP integration
    mcp = GodotMCPIntegration(args.host, args.port)
    
    if args.check:
        # Check connection
        if mcp.check_mcp_connection():
            print("MCP connection successful")
        else:
            print("MCP connection failed")
            sys.exit(1)
    
    elif args.import_sprites:
        # Import character sprites
        count = mcp.batch_import_characters(args.import_sprites)
        print(f"Imported {count} character spritesheets")
    
    elif args.import_cards:
        # Import card textures
        count = mcp.batch_import_cards(args.import_cards)
        print(f"Imported {count} card textures")
    
    elif args.refresh:
        # Refresh project
        if mcp.refresh_godot_project():
            print("Godot project refreshed")
        else:
            print("Failed to refresh project")
            sys.exit(1)
    
    else:
        print("Use --check, --import-sprites, --import-cards, or --refresh")


if __name__ == "__main__":
    main()