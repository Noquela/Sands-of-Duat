"""
Smart Asset Loader - Intelligent loading of 4K generated assets with fallbacks.
Provides seamless integration of AI-generated Egyptian art into the game.
"""

import pygame
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from enum import Enum
from ..core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class AssetQuality(Enum):
    """Asset quality levels for different use cases."""
    ULTRA = "ultra"      # Full 4K resolution
    HIGH = "high"        # 2K resolution  
    MEDIUM = "medium"    # 1080p resolution
    LOW = "low"          # 720p resolution

class SmartAssetLoader:
    """
    Intelligent asset loader that automatically selects best quality
    assets based on screen resolution and available resources.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("smart_asset_loader")
        
        # Asset directories - Priority order for Hades-quality assets
        self.approved_hades_dir = Path("assets/approved_hades_quality")
        self.generated_4k_dir = Path("assets/generated_4k")
        self.game_ready_dir = Path("assets/game_ready")
        self.fallback_dir = Path("assets/fallback")  # Fallback placeholder assets
        
        # Cache for loaded assets
        self._surface_cache: Dict[str, pygame.Surface] = {}
        self._metadata_cache: Dict[str, dict] = {}
        
        # Determine optimal quality based on screen resolution
        self.target_quality = self._determine_target_quality()
        
        # Asset mappings - Updated for Hades-quality assets + AI backgrounds
        self.asset_mappings = {
            # Backgrounds (4K Hades-quality + AI generated)
            'menu_background': 'backgrounds/bg_main_menu_4k.png',
            'bg_main_menu_ai': 'backgrounds/bg_main_menu_4k.png',  # AI alternative
            'combat_background': 'backgrounds/bg_combat_4k.png', 
            'bg_combat_ai': 'backgrounds/bg_combat_4k.png',  # AI alternative
            'deck_builder_background': 'backgrounds/bg_deck_builder_4k.png',
            'collection_background': 'backgrounds/bg_hall_of_gods_4k.png',
            'settings_background': 'backgrounds/bg_settings_4k.png',
            
            # Card frames (priority: Hades-quality → generated_4k)
            'ui_card_frame_common': 'card_frame/common_frame.png',
            'ui_card_frame_rare': 'card_frame/rare_frame.png', 
            'ui_card_frame_epic': 'card_frame/epic_frame.png',
            'ui_card_frame_legendary': 'card_frame/legendary_frame.png',
            'card_frame_common': 'card_frame/common_frame.png',
            'card_frame_rare': 'card_frame/rare_frame.png',
            'card_frame_epic': 'card_frame/epic_frame.png',
            'card_frame_legendary': 'card_frame/legendary_frame.png',
            
            # Hades-quality cards (from approved_hades_quality/cards)
            'anubis_judge_of_the_dead': 'cards/anubis_judge_of_the_dead.png',
            'egyptian_warrior': 'cards/egyptian_warrior.png',
            'isis_divine_mother': 'cards/isis_divine_mother.png',
            'mummy_guardian': 'cards/mummy_guardian.png',
            'pharaohs_guard': 'cards/pharaoh\'s_guard.png',
            'ra_sun_god': 'cards/ra_sun_god.png',
            'set_chaos_god': 'cards/set_chaos_god.png',
            'sphinx_guardian': 'cards/sphinx_guardian.png',
            
            # Characters (from approved_hades_quality/characters)
            'player_hero': 'characters/char_player_hero_2k.png',
            'anubis_boss': 'characters/char_anubis_boss_2k.png',
            'card_frame_epic': 'card_frame/epic_frame.png',
            'card_frame_legendary': 'card_frame/legendary_frame.png',
            
            # Character portraits
            'portrait_ra': 'character_portrait/ra_portrait.png',
            'portrait_anubis': 'character_portrait/anubis_portrait.png',
            'portrait_isis': 'character_portrait/isis_portrait.png',
            'portrait_set': 'character_portrait/set_portrait.png',
            'portrait_thoth': 'character_portrait/thoth_portrait.png',
            'portrait_horus': 'character_portrait/horus_portrait.png',
            
            # UI elements (Egyptian-themed icons)
            'icon_health': 'ui_elements/ui_health_icon.png',
            'icon_mana': 'ui_elements/ui_mana_icon.png',
            'icon_attack': 'ui_elements/ui_attack_icon.png',
            'icon_shield': 'ui_elements/ui_shield_icon.png',
            'icon_energy': 'ui_elements/ui_energy_icon.png',
            'icon_action_points': 'ui_elements/ui_action_points_icon.png',
            
            # Alternative UI element names
            'ui_health_icon': 'ui_elements/ui_health_icon.png',
            'ui_mana_icon': 'ui_elements/ui_mana_icon.png',
            'ui_attack_icon': 'ui_elements/ui_attack_icon.png',
            'ui_shield_icon': 'ui_elements/ui_shield_icon.png',
            'ui_energy_icon': 'ui_elements/ui_energy_icon.png',
            'ui_action_points_icon': 'ui_elements/ui_action_points_icon.png'
        }
        
        self.logger.info(f"Smart asset loader initialized - Target quality: {self.target_quality.value}")
    
    def _determine_target_quality(self) -> AssetQuality:
        """Determine optimal asset quality based on display resolution and performance."""
        total_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
        
        if total_pixels >= 3840 * 2160:  # 4K+ displays
            return AssetQuality.ULTRA
        elif total_pixels >= 2560 * 1440:  # 1440p+ displays (ultrawide)
            return AssetQuality.HIGH
        elif total_pixels >= 1920 * 1080:  # 1080p+ displays
            return AssetQuality.MEDIUM
        else:
            return AssetQuality.LOW
    
    def load_asset(self, asset_name: str, target_size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        Load an asset with intelligent quality selection and caching.
        
        Args:
            asset_name: Name of the asset to load
            target_size: Optional target size for automatic scaling
        
        Returns:
            Pygame surface or None if asset not found
        """
        cache_key = f"{asset_name}_{target_size}" if target_size else asset_name
        
        # Check cache first
        if cache_key in self._surface_cache:
            return self._surface_cache[cache_key]
        
        # Try to load assets in priority order: Hades-quality -> Game-ready -> Generated 4K
        surface = self._load_hades_quality_asset(asset_name)
        if not surface:
            surface = self._load_game_ready_asset(asset_name)
        if not surface:
            surface = self._load_generated_asset(asset_name)
        
        # Fallback to placeholder if needed
        if not surface:
            surface = self._load_fallback_asset(asset_name)
        
        if surface and target_size:
            # Scale to target size with high quality
            surface = pygame.transform.smoothscale(surface, target_size)
        
        # Cache the result
        if surface:
            self._surface_cache[cache_key] = surface
            self.logger.debug(f"Loaded and cached: {asset_name}")
        
        return surface
    
    def _load_hades_quality_asset(self, asset_name: str) -> Optional[pygame.Surface]:
        """Load Hades-quality approved asset (highest priority)."""
        if asset_name not in self.asset_mappings:
            return None
        
        asset_path = self.approved_hades_dir / self.asset_mappings[asset_name]
        
        if asset_path.exists():
            try:
                surface = pygame.image.load(str(asset_path))
                self.logger.info(f"✨ Loaded Hades-quality asset: {asset_name}")
                return surface
            except Exception as e:
                self.logger.warning(f"Failed to load Hades-quality asset {asset_name}: {e}")
        
        return None
    
    def _load_game_ready_asset(self, asset_name: str) -> Optional[pygame.Surface]:
        """Load game-ready asset (second priority)."""
        if asset_name not in self.asset_mappings:
            return None
        
        asset_path = self.game_ready_dir / self.asset_mappings[asset_name]
        
        if asset_path.exists():
            try:
                surface = pygame.image.load(str(asset_path))
                self.logger.debug(f"Loaded game-ready asset: {asset_name}")
                return surface
            except Exception as e:
                self.logger.warning(f"Failed to load game-ready asset {asset_name}: {e}")
        
        return None
    
    def _load_generated_asset(self, asset_name: str) -> Optional[pygame.Surface]:
        """Load AI-generated 4K asset with fallback patterns."""
        if asset_name not in self.asset_mappings:
            # Try common patterns for generated assets
            fallback_patterns = {
                'bg_main_menu_ai': 'background/menu_background.png',
                'bg_combat_ai': 'background/combat_background.png',
                'menu_background': 'background/menu_background.png',
                'combat_background': 'background/combat_background.png',
                'deck_builder_background': 'background/deck_builder_background.png',
                'collection_background': 'background/collection_background.png',
                'settings_background': 'background/settings_background.png'
            }
            
            if asset_name in fallback_patterns:
                asset_path = self.generated_4k_dir / fallback_patterns[asset_name]
                if asset_path.exists():
                    try:
                        surface = pygame.image.load(str(asset_path))
                        self.logger.info(f"🎨 Loaded AI-generated asset: {asset_name}")
                        return surface
                    except Exception as e:
                        self.logger.warning(f"Failed to load AI asset {asset_name}: {e}")
            return None
        
        asset_path = self.generated_4k_dir / self.asset_mappings[asset_name]
        
        if asset_path.exists():
            try:
                surface = pygame.image.load(str(asset_path))
                self.logger.info(f"🎨 Loaded AI-generated asset: {asset_name}")
                return surface
            except Exception as e:
                self.logger.warning(f"Failed to load 4K asset {asset_name}: {e}")
        
        return None
    
    def _load_fallback_asset(self, asset_name: str) -> Optional[pygame.Surface]:
        """Load fallback placeholder asset."""
        # For now, create simple colored rectangles as placeholders
        # In a full implementation, these would be basic Egyptian-themed placeholders
        
        fallback_assets = {
            # Backgrounds - create simple gradients
            'menu_background': self._create_gradient_background((25, 25, 112), (255, 215, 0), SCREEN_WIDTH, SCREEN_HEIGHT),
            'combat_background': self._create_gradient_background((60, 20, 60), (138, 43, 226), SCREEN_WIDTH, SCREEN_HEIGHT),
            'deck_builder_background': self._create_gradient_background((20, 60, 60), (65, 105, 225), SCREEN_WIDTH, SCREEN_HEIGHT),
            'collection_background': self._create_gradient_background((60, 40, 20), (255, 140, 0), SCREEN_WIDTH, SCREEN_HEIGHT),
            
            # Card frames - simple colored borders
            'card_frame_common': self._create_card_frame((245, 245, 220), 256, 384),
            'card_frame_rare': self._create_card_frame((255, 215, 0), 256, 384),
            'card_frame_epic': self._create_card_frame((138, 43, 226), 256, 384),
            'card_frame_legendary': self._create_card_frame((255, 140, 0), 256, 384),
            
            # Character portraits - colored circles with text
            'portrait_ra': self._create_character_placeholder("RA", (255, 215, 0)),
            'portrait_anubis': self._create_character_placeholder("ANUBIS", (60, 20, 60)),
            'portrait_isis': self._create_character_placeholder("ISIS", (65, 105, 225)),
            'portrait_set': self._create_character_placeholder("SET", (220, 20, 20)),
            'portrait_thoth': self._create_character_placeholder("THOTH", (0, 150, 150)),
            'portrait_horus': self._create_character_placeholder("HORUS", (255, 140, 0)),
            
            # UI elements - simple icons
            'icon_health': self._create_icon_placeholder("♥", (220, 20, 20)),
            'icon_mana': self._create_icon_placeholder("♦", (65, 105, 225)),
            'icon_attack': self._create_icon_placeholder("⚔", (255, 140, 0)),
            'icon_shield': self._create_icon_placeholder("🛡", (128, 128, 128))
        }
        
        if asset_name in fallback_assets:
            self.logger.debug(f"Using fallback for: {asset_name}")
            return fallback_assets[asset_name]
        
        return None
    
    def _create_gradient_background(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                                  width: int, height: int) -> pygame.Surface:
        """Create a simple gradient background."""
        surface = pygame.Surface((width, height))
        
        for y in range(height):
            ratio = y / height
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            surface.fill((r, g, b), (0, y, width, 1))
        
        return surface
    
    def _create_card_frame(self, color: Tuple[int, int, int], width: int, height: int) -> pygame.Surface:
        """Create a simple card frame placeholder."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fill with transparent background - Use set_alpha to avoid invalid color argument
        surface.fill((0, 0, 0))
        surface.set_alpha(0)
        
        # Draw border
        border_width = 8
        pygame.draw.rect(surface, color, (0, 0, width, height), border_width, border_radius=12)
        
        # Inner decoration
        inner_rect = pygame.Rect(border_width * 2, border_width * 2, 
                               width - border_width * 4, height - border_width * 4)
        pygame.draw.rect(surface, (*color, 100), inner_rect, 2, border_radius=8)
        
        return surface
    
    def _create_character_placeholder(self, name: str, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create a character portrait placeholder."""
        size = 256
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Background circle
        pygame.draw.circle(surface, color, (size//2, size//2), size//2 - 10)
        pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), size//2 - 10, 3)
        
        # Character name
        font = pygame.font.Font(None, 36)
        text = font.render(name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(size//2, size//2))
        surface.blit(text, text_rect)
        
        return surface
    
    def _create_icon_placeholder(self, symbol: str, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create a UI icon placeholder."""
        size = 64
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Background
        pygame.draw.circle(surface, color, (size//2, size//2), size//2 - 2)
        pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), size//2 - 2, 2)
        
        # Symbol
        font = pygame.font.Font(None, 48)
        text = font.render(symbol, True, (255, 255, 255))
        text_rect = text.get_rect(center=(size//2, size//2))
        surface.blit(text, text_rect)
        
        return surface
    
    def preload_common_assets(self):
        """Preload commonly used assets for better performance."""
        common_assets = [
            'menu_background',
            'combat_background', 
            'card_frame_common',
            'card_frame_rare',
            'icon_health',
            'icon_mana'
        ]
        
        self.logger.info("Preloading common assets...")
        for asset_name in common_assets:
            self.load_asset(asset_name)
        
        self.logger.info(f"Preloaded {len(common_assets)} assets")
    
    def get_background(self, screen_name: str) -> Optional[pygame.Surface]:
        """Get background for a specific screen."""
        background_map = {
            'menu': 'menu_background',
            'main_menu': 'menu_background',
            'combat': 'combat_background',
            'deck_builder': 'deck_builder_background',
            'collection': 'collection_background'
        }
        
        asset_name = background_map.get(screen_name)
        if asset_name:
            return self.load_asset(asset_name, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        return None
    
    def get_card_frame(self, rarity: str) -> Optional[pygame.Surface]:
        """Get card frame for specific rarity."""
        frame_name = f'card_frame_{rarity.lower()}'
        return self.load_asset(frame_name)
    
    def get_character_portrait(self, character: str) -> Optional[pygame.Surface]:
        """Get character portrait."""
        portrait_name = f'portrait_{character.lower()}'
        return self.load_asset(portrait_name)
    
    def get_ui_icon(self, icon_type: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get UI icon with optional sizing."""
        icon_name = f'icon_{icon_type.lower()}'
        return self.load_asset(icon_name, size)
    
    def clear_cache(self):
        """Clear the asset cache to free memory."""
        self._surface_cache.clear()
        self._metadata_cache.clear()
        self.logger.info("Asset cache cleared")
    
    def get_cache_info(self) -> Dict[str, int]:
        """Get cache statistics."""
        total_memory = 0
        for surface in self._surface_cache.values():
            total_memory += surface.get_width() * surface.get_height() * 4  # RGBA
        
        return {
            'cached_assets': len(self._surface_cache),
            'memory_mb': total_memory // (1024 * 1024)
        }

# Global smart asset loader instance
smart_asset_loader = SmartAssetLoader()