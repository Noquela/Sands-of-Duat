"""
Background Loader for AI Generated Backgrounds
Loads and manages professional background artwork for all game screens
"""

import pygame
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging


class BackgroundLoader:
    """Enhanced loader for AI-generated background artwork with contextual switching"""
    
    def __init__(self, asset_root: str = "game_assets"):
        self.asset_root = Path(asset_root)
        self.backgrounds_dir = self.asset_root / "environments"
        self.background_cache: Dict[str, pygame.Surface] = {}
        self.logger = logging.getLogger(__name__)
        
        # Current context for dynamic switching
        self.current_context = {}
        self.last_background_key = None
        
        # Background mapping with contextual variations
        self.background_mapping = {
            "menu": "menu_background",
            "combat": "combat_background", 
            "map": "map_background",
            "deck_builder": "menu_background",
            "victory": "combat_background",
            "defeat": "combat_background",
            "tutorial": "menu_background",
            "progression": "menu_background"
        }
        
        # Contextual background variations
        self.contextual_mappings = {
            "combat": {
                "desert": "desert_combat_background",
                "tomb": "tomb_combat_background", 
                "temple": "temple_combat_background",
                "underworld": "underworld_combat_background",
                "boss": "boss_combat_background"
            },
            "map": {
                "hour_1": "early_night_map",
                "hour_6": "deep_night_map", 
                "hour_12": "dawn_approach_map",
                "underworld": "underworld_map"
            },
            "menu": {
                "victory": "victory_menu_background",
                "defeat": "defeat_menu_background"
            }
        }
    
    def load_background(self, screen_name: str, size: Tuple[int, int] = None, 
                       context: Dict[str, str] = None) -> Optional[pygame.Surface]:
        """Enhanced background loading with contextual switching"""
        # Determine the best background based on context
        file_name = self._get_contextual_background(screen_name, context or {})
        
        # Create comprehensive cache key including context
        context_key = "_".join(f"{k}:{v}" for k, v in sorted((context or {}).items()))
        cache_key = f"{screen_name}_{context_key}_{size}" if size else f"{screen_name}_{context_key}"
        
        if cache_key in self.background_cache:
            return self.background_cache[cache_key]
        
        if not file_name:
            self.logger.warning(f"No background mapping found for screen: {screen_name}")
            return self._create_fallback_background(screen_name, size, context)
        
        # Try contextual background first, then fallback to base
        background_path = self.backgrounds_dir / f"{file_name}.png"
        if not background_path.exists():
            # Try base background as fallback
            base_file = self.background_mapping.get(screen_name)
            if base_file and base_file != file_name:
                background_path = self.backgrounds_dir / f"{base_file}.png"
                if not background_path.exists():
                    self.logger.warning(f"Neither contextual nor base background found for: {screen_name}")
                    return self._create_fallback_background(screen_name, size, context)
            else:
                self.logger.warning(f"Background not found: {background_path}")
                return self._create_fallback_background(screen_name, size, context)
        
        try:
            # Load high-quality AI background
            background_surface = pygame.image.load(str(background_path))
            
            # Convert for better performance (only if display is set)
            try:
                background_surface = background_surface.convert()
            except pygame.error:
                # If no display mode is set, use convert_alpha
                background_surface = background_surface.convert_alpha()
            
            # Resize if needed
            if size and size != background_surface.get_size():
                background_surface = pygame.transform.smoothscale(background_surface, size)
            
            # Cache for future use
            self.background_cache[cache_key] = background_surface
            
            self.logger.info(f"Loaded AI background: {screen_name} from {background_path}")
            return background_surface
            
        except Exception as e:
            self.logger.error(f"Failed to load background {background_path}: {e}")
            return self._create_fallback_background(screen_name, size, context)
    
    def _get_contextual_background(self, screen_name: str, context: Dict[str, str]) -> Optional[str]:
        """Get the most appropriate background file based on context"""
        # Check for contextual variations first
        if screen_name in self.contextual_mappings:
            contextual_options = self.contextual_mappings[screen_name]
            
            # Priority order for context matching
            context_priorities = {
                "combat": ["boss", "location", "enemy_type", "hour"],
                "map": ["hour", "location", "progress"],
                "menu": ["game_state", "last_result"]
            }
            
            priorities = context_priorities.get(screen_name, list(contextual_options.keys()))
            
            # Find best match based on priority
            for priority_key in priorities:
                if priority_key in context:
                    context_value = context[priority_key]
                    # Try exact match
                    if context_value in contextual_options:
                        return contextual_options[context_value]
                    # Try partial matches
                    for key, file_name in contextual_options.items():
                        if key in context_value or context_value in key:
                            return file_name
        
        # Fallback to base mapping
        return self.background_mapping.get(screen_name)
    
    def set_context(self, context: Dict[str, str]) -> None:
        """Set current context for background selection"""
        self.current_context.update(context)
        self.logger.debug(f"Updated background context: {self.current_context}")
    
    def clear_context(self) -> None:
        """Clear current context"""
        self.current_context.clear()
    
    def get_context(self) -> Dict[str, str]:
        """Get current context"""
        return self.current_context.copy()
    
    def _create_fallback_background(self, screen_name: str, size: Tuple[int, int] = None, 
                                   context: Dict[str, str] = None) -> pygame.Surface:
        """Create fallback background if AI art not available"""
        if not size:
            size = (3440, 1440)  # Default ultrawide size
        
        # Create Egyptian-themed gradient background
        surface = pygame.Surface(size)
        
        # Context-aware Egyptian color scheme
        if screen_name == "combat":
            # Determine combat context colors
            if context and context.get("boss"):
                # Boss combat - more dramatic colors
                top_color = (60, 20, 20)      # Deep red
                bottom_color = (100, 40, 40)  # Dark red
            elif context and context.get("location") == "desert":
                # Desert combat
                top_color = (80, 60, 20)      # Sandy brown
                bottom_color = (120, 90, 40)  # Light sand
            elif context and context.get("location") == "tomb":
                # Tomb combat - darker
                top_color = (15, 10, 5)       # Very dark
                bottom_color = (40, 30, 15)   # Dark brown
            else:
                # Default combat colors
                top_color = (25, 15, 10)      # Dark brown
                bottom_color = (60, 40, 20)   # Medium brown
        elif screen_name == "menu":
            if context and context.get("game_state") == "victory":
                # Victory menu - golden colors
                top_color = (120, 100, 40)    # Bright gold
                bottom_color = (160, 140, 80) # Light gold
            elif context and context.get("game_state") == "defeat":
                # Defeat menu - muted colors
                top_color = (40, 30, 20)      # Muted brown
                bottom_color = (60, 45, 30)   # Dark tan
            else:
                # Default menu - desert sunset colors
                top_color = (80, 60, 30)      # Dark gold
                bottom_color = (120, 80, 40)  # Light gold
        elif screen_name == "map":
            if context and context.get("hour"):
                hour = int(context.get("hour", "1"))
                if hour <= 3:
                    # Early night - purple hues
                    top_color = (30, 20, 50)      # Dark purple
                    bottom_color = (60, 40, 80)   # Medium purple
                elif hour >= 10:
                    # Late night approaching dawn - warmer
                    top_color = (50, 40, 30)      # Warm brown
                    bottom_color = (90, 70, 50)   # Light brown
                else:
                    # Deep night - blue-black
                    top_color = (15, 15, 30)      # Deep blue
                    bottom_color = (30, 30, 60)   # Dark blue
            else:
                # Default map colors
                top_color = (25, 35, 15)      # Dark green-brown
                bottom_color = (50, 70, 35)   # Medium green-brown
        else:
            # Temple colors
            top_color = (40, 35, 25)      # Dark stone
            bottom_color = (80, 70, 50)   # Light stone
        
        # Create vertical gradient
        for y in range(size[1]):
            blend = y / size[1]
            color = (
                int(top_color[0] * (1 - blend) + bottom_color[0] * blend),
                int(top_color[1] * (1 - blend) + bottom_color[1] * blend), 
                int(top_color[2] * (1 - blend) + bottom_color[2] * blend)
            )
            pygame.draw.line(surface, color, (0, y), (size[0], y))
        
        # Add some texture
        for i in range(0, size[0], 100):
            for j in range(0, size[1], 100):
                alpha = 20
                overlay = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.rect(overlay, (*bottom_color, alpha), overlay.get_rect())
                surface.blit(overlay, (i, j))
        
        context_str = f" with context {context}" if context else ""
        self.logger.info(f"Created contextual fallback background for {screen_name}{context_str}")
        return surface
    
    def preload_all_backgrounds(self, screen_size: Tuple[int, int] = None):
        """Preload all available backgrounds"""
        self.logger.info("Preloading AI backgrounds...")
        loaded_count = 0
        
        for screen_name in self.background_mapping.keys():
            if self.load_background(screen_name, screen_size):
                loaded_count += 1
        
        self.logger.info(f"Preloaded {loaded_count}/{len(self.background_mapping)} backgrounds")
        return loaded_count
    
    def get_available_backgrounds(self) -> list:
        """Get list of screens with AI backgrounds available"""
        available = []
        for screen_name, file_name in self.background_mapping.items():
            background_path = self.backgrounds_dir / f"{file_name}.png"
            if background_path.exists():
                available.append(screen_name)
        return available


# Global background loader instance
_background_loader = None

def get_background_loader() -> BackgroundLoader:
    """Get global background loader instance"""
    global _background_loader
    if _background_loader is None:
        _background_loader = BackgroundLoader()
    return _background_loader

def load_background(screen_name: str, size: Tuple[int, int] = None, 
                   context: Dict[str, str] = None) -> Optional[pygame.Surface]:
    """Convenience function to load background with context"""
    return get_background_loader().load_background(screen_name, size, context)

def set_background_context(context: Dict[str, str]) -> None:
    """Convenience function to set background context"""  
    get_background_loader().set_context(context)

def clear_background_context() -> None:
    """Convenience function to clear background context"""
    get_background_loader().clear_context()