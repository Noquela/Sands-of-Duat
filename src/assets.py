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
        
        # Organized asset paths (relative to project root, not src/)
        self.assets_root = Path("../assets")
        self.generated_path = self.assets_root / "generated"  # Legacy support
        self.raw_path = self.assets_root / "raw"
        
        # New organized structure
        self.characters_path = self.assets_root / "characters"
        self.enemies_path = self.assets_root / "enemies"
        self.environments_path = self.assets_root / "environments"
        self.portals_path = self.assets_root / "portals"
        self.ui_path = self.assets_root / "ui"
        
        # Ensure directories exist
        for path in [self.generated_path, self.raw_path, self.characters_path, 
                     self.enemies_path, self.environments_path, self.portals_path, self.ui_path]:
            path.mkdir(parents=True, exist_ok=True)
    
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
    """Load all game assets using High-Quality SDXL-generated assets."""
    print("Loading High-Quality SDXL-generated game assets...")
    
    # Load player character sprites from generated/ folder (HQ SDXL assets)
    player_loaded = load_ai_sprite_legacy("player_anubis_idle_hq", "player_anubis", scale_factor=0.2)
    if not player_loaded:
        # Try lower quality versions
        player_loaded = load_ai_sprite_legacy("player_anubis_idle", "player_anubis", scale_factor=0.25)
    if not player_loaded:
        # Generate placeholder with correct dimensions for player (64x64 frames)
        player_sheet = asset_manager.create_sprite_sheet("player_anubis", 64, 64, 4, 1)
        asset_manager.sprites["player_anubis"] = player_sheet
        print("Generated placeholder player sprite: 64x64 frames")
    
    # Load enemy sprites from generated/ folder (HQ SDXL assets)
    scarab_loaded = load_ai_sprite_legacy("enemy_scarab_guardian_hq", "scarab_enemy", scale_factor=0.2)
    if not scarab_loaded:
        scarab_loaded = load_ai_sprite_legacy("enemy_scarab_idle", "scarab_enemy", scale_factor=0.25)
    if not scarab_loaded:
        # Generate placeholder with correct dimensions for enemies (48x48 frames)
        scarab_sheet = asset_manager.create_sprite_sheet("scarab_enemy", 48, 48, 4, 1)
        asset_manager.sprites["scarab_enemy"] = scarab_sheet
        print("Generated placeholder scarab sprite: 48x48 frames")
    
    # Load portal sprites from generated/ folder (HQ SDXL assets)
    portal_loaded = load_ai_sprite_legacy("portal_arena_hq", "portal_arena", scale_factor=0.2)
    if not portal_loaded:
        # Generate placeholder portal (96x96 single frame)
        portal_surface = asset_manager.create_placeholder_sprite(96, 96, "portal")
        asset_manager.sprites["portal_arena"] = portal_surface
        print("Generated placeholder portal sprite: 96x96")
    
    # Load environment assets (altars) from generated/ folder (SDXL assets)
    load_sdxl_environment_assets()
    
    # Generate placeholders for any missing sprites
    generate_hub_placeholders()
    
    print("SDXL assets loaded successfully!")


def load_sdxl_environment_assets():
    """Load environment assets from HQ SDXL generated folder."""
    # Load altar sprites from generated/ folder (HQ SDXL assets)
    altars = [
        ("altar_ra_hq", "altar_ra"),
        ("altar_thoth_hq", "altar_thoth"), 
        ("altar_isis_hq", "altar_isis"),
        ("altar_ptah_hq", "altar_ptah"),
        ("altar_ra", "altar_ra")  # Backup option
    ]
    
    for ai_sprite_name, sprite_key in altars:
        if sprite_key not in asset_manager.sprites:  # Only load if not already loaded
            loaded = load_ai_sprite_legacy(ai_sprite_name, sprite_key, scale_factor=0.25)
            if loaded:
                print(f"Loaded SDXL altar: {ai_sprite_name}")

def load_organized_environment_assets():
    """Load environment assets from organized structure."""
    # Load altar sprites from environments/ folder
    altars = ["altar_ra", "altar_thoth", "altar_isis", "altar_ptah"]
    
    for altar_name in altars:
        loaded = load_organized_sprite(altar_name, altar_name, "environments", scale_factor=0.5)
        if loaded:
            print(f"Loaded organized altar: {altar_name}")


def generate_hub_placeholders():
    """Generate placeholder sprites for hub elements, trying SDXL first."""
    # Load NPCs from SDXL generated assets first
    npc_mappings = [
        ("npc_mirror_anubis", "npc_mirror_anubis"),
        ("npc_merchant", "npc_merchant")
    ]
    
    for ai_sprite_name, sprite_key in npc_mappings:
        if sprite_key not in asset_manager.sprites:
            loaded = load_ai_sprite_legacy(ai_sprite_name, sprite_key, scale_factor=0.25)
            if loaded:
                print(f"Loaded SDXL NPC: {ai_sprite_name}")
    
    # Altar sprites (64x64 single frames for NPCs and altars) - fallback placeholders
    for altar in ["altar_ra", "altar_thoth", "altar_isis", "altar_ptah"]:
        if altar not in asset_manager.sprites:
            altar_surface = asset_manager.create_placeholder_sprite(64, 64, altar)
            asset_manager.sprites[altar] = altar_surface
    
    # NPC sprites (64x64 single frames) - fallback placeholders
    for npc in ["npc_mirror_anubis", "npc_merchant"]:
        if npc not in asset_manager.sprites:
            npc_surface = asset_manager.create_placeholder_sprite(64, 64, npc)
            asset_manager.sprites[npc] = npc_surface


def load_organized_sprite(sprite_name: str, sprite_key: str, category: str = "characters", scale_factor: float = 1.0) -> bool:
    """Load a sprite from organized structure and scale for gameplay."""
    
    # Get the appropriate category path
    category_paths = {
        "characters": asset_manager.characters_path,
        "enemies": asset_manager.enemies_path,
        "environments": asset_manager.environments_path,
        "portals": asset_manager.portals_path,
        "ui": asset_manager.ui_path
    }
    
    category_path = category_paths.get(category, asset_manager.characters_path)
    sprite_path = category_path / f"{sprite_name}.png"
    
    # Try organized structure first
    if sprite_path.exists():
        try:
            sprite = pygame.image.load(str(sprite_path)).convert_alpha()
            
            # Scale if needed
            if scale_factor != 1.0:
                original_size = sprite.get_size()
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.smoothscale(sprite, new_size)
                print(f"Scaled organized sprite {sprite_name}: {original_size} -> {new_size}")
            
            asset_manager.sprites[sprite_key] = sprite
            print(f"Loaded organized sprite: {sprite_name} from {category}")
            return True
            
        except pygame.error as e:
            print(f"Failed to load organized sprite {sprite_name}: {e}")
            return False
    
    # Fallback to legacy generated path
    return load_ai_sprite_legacy(sprite_name, sprite_key, scale_factor)


def load_ai_sprite_legacy(ai_sprite_name: str, sprite_key: str, scale_factor: float = 0.25) -> bool:
    """Load an AI-generated sprite from legacy generated folder (fallback)."""
    ai_path = asset_manager.generated_path / f"{ai_sprite_name}.png"
    
    if ai_path.exists():
        try:
            sprite = pygame.image.load(str(ai_path)).convert_alpha()
            
            # Scale down high-resolution AI sprites for gameplay
            if scale_factor != 1.0:
                original_size = sprite.get_size()
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.smoothscale(sprite, new_size)
                print(f"Scaled legacy AI sprite {ai_sprite_name}: {original_size} -> {new_size}")
            
            asset_manager.sprites[sprite_key] = sprite
            print(f"Loaded legacy AI-generated sprite: {ai_sprite_name}")
            return True
        except pygame.error as e:
            print(f"Failed to load legacy AI sprite {ai_sprite_name}: {e}")
            return False
    else:
        print(f"Legacy AI sprite not found: {ai_sprite_name}, using placeholder")
        return False


def get_sprite(name: str) -> Optional[pygame.Surface]:
    """Get a sprite by name."""
    return asset_manager.get_sprite(name)