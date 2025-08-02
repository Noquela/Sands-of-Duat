"""
Asset management for Sands of Duat
Handles loading and managing game assets
"""

import pygame
import os
from typing import Dict, Optional
from pathlib import Path


class AssetManager:
    """Manages loading and caching of game assets."""
    
    def __init__(self):
        self.sprites: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        
        # Asset paths
        self.assets_root = Path("assets")
        self.generated_path = self.assets_root / "generated"
        self.raw_path = self.assets_root / "raw"
        
        # Ensure directories exist
        self.generated_path.mkdir(parents=True, exist_ok=True)
        self.raw_path.mkdir(parents=True, exist_ok=True)
    
    def load_sprite(self, name: str, path: str) -> pygame.Surface:
        """Load a sprite and cache it."""
        if name in self.sprites:
            return self.sprites[name]
        
        full_path = self.assets_root / path
        if not full_path.exists():
            # Create placeholder sprite if file doesn't exist
            sprite = self.create_placeholder_sprite(64, 64, name)
            self.sprites[name] = sprite
            return sprite
        
        try:
            sprite = pygame.image.load(str(full_path)).convert_alpha()
            self.sprites[name] = sprite
            return sprite
        except pygame.error as e:
            print(f"Failed to load sprite {path}: {e}")
            # Return placeholder
            sprite = self.create_placeholder_sprite(64, 64, name)
            self.sprites[name] = sprite
            return sprite
    
    def create_placeholder_sprite(self, width: int, height: int, label: str = "") -> pygame.Surface:
        """Create a placeholder sprite for testing."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Egyptian-themed colors
        if "player" in label.lower() or "anubis" in label.lower():
            color = (218, 165, 32)  # Golden
        elif "scarab" in label.lower():
            color = (139, 69, 19)   # Saddle brown
        elif "mummy" in label.lower():
            color = (245, 245, 220) # Beige
        else:
            color = (128, 128, 128)  # Gray
        
        # Draw simple placeholder
        pygame.draw.rect(sprite, color, (0, 0, width, height))
        pygame.draw.rect(sprite, (0, 0, 0), (0, 0, width, height), 2)
        
        # Add simple features for characters
        if "player" in label.lower() or "anubis" in label.lower():
            # Anubis-like ears
            pygame.draw.polygon(sprite, (184, 134, 11), [
                (width//4, height//4), 
                (width//2 - 5, 5), 
                (width//2, height//4)
            ])
            pygame.draw.polygon(sprite, (184, 134, 11), [
                (width//2, height//4), 
                (width//2 + 5, 5), 
                (3*width//4, height//4)
            ])
            # Eyes
            pygame.draw.circle(sprite, (255, 215, 0), (width//3, height//2), 3)
            pygame.draw.circle(sprite, (255, 215, 0), (2*width//3, height//2), 3)
        
        return sprite
    
    def create_sprite_sheet(self, name: str, frame_width: int, frame_height: int, 
                          cols: int, rows: int) -> pygame.Surface:
        """Create a sprite sheet with placeholder frames."""
        sheet_width = frame_width * cols
        sheet_height = frame_height * rows
        sprite_sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
        
        for row in range(rows):
            for col in range(cols):
                frame = self.create_placeholder_sprite(frame_width, frame_height, name)
                x = col * frame_width
                y = row * frame_height
                sprite_sheet.blit(frame, (x, y))
                
                # Add frame number for debugging
                font = pygame.font.Font(None, 24)
                frame_num = row * cols + col
                text = font.render(str(frame_num), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + frame_width//2, y + frame_height - 10))
                sprite_sheet.blit(text, text_rect)
        
        return sprite_sheet
    
    def get_sprite(self, name: str) -> Optional[pygame.Surface]:
        """Get a cached sprite."""
        return self.sprites.get(name)
    
    def generate_character_sprites(self):
        """Generate placeholder character sprites."""
        # Player/Anubis warrior sprite sheet
        player_sheet = self.create_sprite_sheet("player_anubis", 64, 64, 4, 4)
        self.sprites["player_anubis"] = player_sheet
        
        # Save placeholder sprite sheet
        player_path = self.generated_path / "player_anubis_placeholder.png"
        pygame.image.save(player_sheet, str(player_path))
        print(f"Generated placeholder player sprite: {player_path}")
        
        # Scarab enemy sprite sheet
        scarab_sheet = self.create_sprite_sheet("scarab_enemy", 48, 48, 4, 2)
        self.sprites["scarab_enemy"] = scarab_sheet
        
        scarab_path = self.generated_path / "scarab_enemy_placeholder.png"
        pygame.image.save(scarab_sheet, str(scarab_path))
        print(f"Generated placeholder scarab sprite: {scarab_path}")


# Global asset manager instance
asset_manager = AssetManager()


def load_assets():
    """Load all game assets."""
    print("Loading game assets...")
    
    # Try to load existing sprites or generate placeholders
    asset_manager.generate_character_sprites()
    
    # Load player sprite
    asset_manager.load_sprite("player_anubis", "generated/player_anubis_placeholder.png")
    
    # Load enemy sprites
    asset_manager.load_sprite("scarab_enemy", "generated/scarab_enemy_placeholder.png")
    
    print("Assets loaded successfully!")


def get_sprite(name: str) -> Optional[pygame.Surface]:
    """Get a sprite by name."""
    return asset_manager.get_sprite(name)