"""
Professional Asset Manager for Sands of Duat
Manages quality-based asset loading with Hades-style preference system.
"""

import pygame
import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass, asdict
import logging


class AssetQuality(Enum):
    """Asset quality levels in order of preference"""
    HADES = "hades_quality"      # Professional Hades-style art
    STANDARD = "standard_quality" # Original/placeholder art
    CONCEPT = "concept"          # Concept art fallback


class AssetCategory(Enum):
    """Asset categories"""
    CARDS = "cards"
    CHARACTERS = "characters"
    ENVIRONMENTS = "environments"
    UI_ELEMENTS = "ui_elements"
    EFFECTS = "effects"


@dataclass
class AssetDescriptor:
    """Describes an asset and its quality variants"""
    asset_id: str
    category: AssetCategory
    base_name: str
    available_qualities: List[AssetQuality]
    preferred_quality: AssetQuality = AssetQuality.HADES
    fallback_quality: AssetQuality = AssetQuality.STANDARD
    
    def get_quality_path(self, quality: AssetQuality, base_path: Path) -> Path:
        """Get the file path for a specific quality level"""
        if quality == AssetQuality.HADES:
            if self.category == AssetCategory.CARDS:
                return base_path / "cards" / "hades_quality" / f"{self.base_name}_hades.png"
            else:
                return base_path / self.category.value / "hades_quality" / f"{self.base_name}.png"
        elif quality == AssetQuality.STANDARD:
            if self.category == AssetCategory.CARDS:
                return base_path / "cards" / "standard_quality" / f"{self.base_name}.png"
            else:
                return base_path / self.category.value / "standard_quality" / f"{self.base_name}.png"
        else:  # CONCEPT
            return base_path / self.category.value / "concepts" / f"{self.base_name}.png"


class ProfessionalAssetManager:
    """
    Professional asset management system with quality-based loading.
    Automatically prefers Hades-style assets with intelligent fallbacks.
    """
    
    def __init__(self, assets_root: Union[str, Path] = None):
        if assets_root is None:
            # Default to game_assets folder in project root
            project_root = Path(__file__).parent.parent.parent
            self.assets_root = project_root / "game_assets"
        else:
            self.assets_root = Path(assets_root)
        
        self.logger = logging.getLogger(__name__)
        
        # Asset storage by category and quality
        self.loaded_assets: Dict[str, pygame.Surface] = {}
        self.asset_descriptors: Dict[str, AssetDescriptor] = {}
        self.loading_queue: List[AssetDescriptor] = []
        
        # Performance settings
        self.enable_quality_fallback = True
        self.prefer_hades_quality = True
        self.cache_enabled = True
        
        # Threading for background loading
        self.loading_thread: Optional[threading.Thread] = None
        self.is_loading = False
        self.loading_complete_callbacks: List[Callable] = []
        
        # Initialize asset registry
        self._initialize_asset_registry()
        self._load_asset_manifest()
        
        # Initialize pygame if needed
        if not pygame.get_init():
            pygame.init()
            
        self.logger.info(f"Professional Asset Manager initialized with {len(self.asset_descriptors)} registered assets")
    
    def _initialize_asset_registry(self):
        """Initialize the registry of all known assets"""
        
        # Card assets
        card_names = [
            "sand_strike", "anubis_judgment", "ra_solar_flare", "isis_grace",
            "tomb_strike", "scarab_swarm", "ankh_blessing", "pyramid_power",
            "papyrus_scroll", "desert_whisper", "thoths_wisdom", 
            "pharaohs_resurrection", "mummys_wrath", "sand_grain"
        ]
        
        for card_name in card_names:
            # Determine available qualities based on file existence
            qualities = []
            hades_path = self.assets_root / "cards" / "hades_quality" / f"{card_name}_hades.png"
            standard_path = self.assets_root / "cards" / "standard_quality" / f"{card_name}.png"
            
            if hades_path.exists():
                qualities.append(AssetQuality.HADES)
            if standard_path.exists():
                qualities.append(AssetQuality.STANDARD)
            
            if qualities:
                descriptor = AssetDescriptor(
                    asset_id=f"card_{card_name}",
                    category=AssetCategory.CARDS,
                    base_name=card_name,
                    available_qualities=qualities
                )
                self.asset_descriptors[descriptor.asset_id] = descriptor
        
        # Environment assets
        env_names = ["menu_background", "combat_background", "deck_builder_background", "progression_background"]
        for env_name in env_names:
            qualities = []
            hades_path = self.assets_root / "environments" / "hades_quality" / f"{env_name}.png"
            standard_path = self.assets_root / "environments" / "standard_quality" / f"{env_name}.png"
            
            if hades_path.exists():
                qualities.append(AssetQuality.HADES)
            if standard_path.exists():
                qualities.append(AssetQuality.STANDARD)
                
            if qualities:
                descriptor = AssetDescriptor(
                    asset_id=f"env_{env_name}",
                    category=AssetCategory.ENVIRONMENTS,
                    base_name=env_name,
                    available_qualities=qualities
                )
                self.asset_descriptors[descriptor.asset_id] = descriptor
        
        # Character assets
        char_names = ["player_character", "anubis_guardian", "desert_scorpion", "pharaoh_lich", "temple_guardian"]
        for char_name in char_names:
            # Check for concept art
            concept_path = self.assets_root / "characters" / "concepts" / f"{char_name}.png"
            sprite_path = self.assets_root / "characters" / "standard_quality" / "sprites" / f"{char_name}_idle.png"
            
            qualities = []
            if concept_path.exists():
                qualities.append(AssetQuality.CONCEPT)
            if sprite_path.exists():
                qualities.append(AssetQuality.STANDARD)
                
            if qualities:
                descriptor = AssetDescriptor(
                    asset_id=f"char_{char_name}",
                    category=AssetCategory.CHARACTERS,
                    base_name=char_name,
                    available_qualities=qualities,
                    preferred_quality=AssetQuality.CONCEPT  # Prefer concept art for characters
                )
                self.asset_descriptors[descriptor.asset_id] = descriptor
        
        # UI Elements
        ui_names = ["ornate_button", "card_frame", "health_orb", "mana_crystal"]
        for ui_name in ui_names:
            hades_path = self.assets_root / "ui_elements" / "hades_quality" / f"{ui_name}.png"
            
            qualities = []
            if hades_path.exists():
                qualities.append(AssetQuality.HADES)
                
            if qualities:
                descriptor = AssetDescriptor(
                    asset_id=f"ui_{ui_name}",
                    category=AssetCategory.UI_ELEMENTS,
                    base_name=ui_name,
                    available_qualities=qualities
                )
                self.asset_descriptors[descriptor.asset_id] = descriptor
    
    def _load_asset_manifest(self):
        """Load asset manifest if available"""
        manifest_path = self.assets_root / "ASSET_MANIFEST.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                self.logger.info(f"Loaded asset manifest v{manifest.get('version', 'unknown')}")
            except Exception as e:
                self.logger.warning(f"Failed to load asset manifest: {e}")
    
    def get_asset(self, asset_id: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        Get an asset with intelligent quality selection.
        Returns the highest quality available asset.
        """
        # Check if already loaded
        cache_key = f"{asset_id}_{size}" if size else asset_id
        if cache_key in self.loaded_assets and self.cache_enabled:
            return self.loaded_assets[cache_key]
        
        # Get asset descriptor
        descriptor = self.asset_descriptors.get(asset_id)
        if not descriptor:
            self.logger.warning(f"Unknown asset: {asset_id}")
            return self._create_placeholder(asset_id, size)
        
        # Try to load in quality preference order
        quality_order = [AssetQuality.HADES, AssetQuality.STANDARD, AssetQuality.CONCEPT]
        if not self.prefer_hades_quality:
            quality_order = [AssetQuality.STANDARD, AssetQuality.HADES, AssetQuality.CONCEPT]
        
        for quality in quality_order:
            if quality in descriptor.available_qualities:
                asset_path = descriptor.get_quality_path(quality, self.assets_root)
                surface = self._load_surface(asset_path, size)
                if surface:
                    # Cache the loaded asset
                    if self.cache_enabled:
                        self.loaded_assets[cache_key] = surface
                    
                    self.logger.debug(f"Loaded {asset_id} at {quality.value} quality")
                    return surface
        
        # No asset found, create placeholder
        self.logger.warning(f"No valid asset found for {asset_id}, using placeholder")
        return self._create_placeholder(asset_id, size)
    
    def _load_surface(self, path: Path, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Load a pygame surface from file path"""
        if not path.exists():
            return None
        
        try:
            surface = pygame.image.load(str(path)).convert_alpha()
            if size:
                surface = pygame.transform.scale(surface, size)
            return surface
        except Exception as e:
            self.logger.error(f"Failed to load surface from {path}: {e}")
            return None
    
    def _create_placeholder(self, asset_id: str, size: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """Create a placeholder surface for missing assets"""
        if size is None:
            size = (256, 256)  # Default placeholder size
        
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Egyptian-themed placeholder colors
        if "card_" in asset_id:
            surface.fill((139, 115, 85, 200))  # Papyrus brown
        elif "env_" in asset_id:
            surface.fill((26, 22, 17, 255))    # Dark brown background
        elif "char_" in asset_id:
            surface.fill((205, 127, 50, 200))  # Bronze
        elif "ui_" in asset_id:
            surface.fill((255, 215, 0, 180))   # Gold
        else:
            surface.fill((128, 128, 128, 200)) # Generic gray
        
        # Add simple border
        pygame.draw.rect(surface, (255, 215, 0), surface.get_rect(), 2)
        
        return surface
    
    def preload_card_set(self, card_names: List[str], card_size: Tuple[int, int] = (300, 420)) -> None:
        """Preload a set of cards for performance"""
        for card_name in card_names:
            asset_id = f"card_{card_name}"
            self.get_asset(asset_id, card_size)
    
    def preload_environment_set(self, env_names: List[str]) -> None:
        """Preload environment backgrounds"""
        for env_name in env_names:
            asset_id = f"env_{env_name}"
            self.get_asset(asset_id)
    
    def preload_for_screen(self, screen_name: str) -> None:
        """Preload assets for a specific game screen"""
        if screen_name in ["menu", "main_menu"]:
            self.get_asset("env_menu_background")
            self.get_asset("ui_ornate_button")
            
        elif screen_name in ["combat", "dynamic_combat"]:
            self.get_asset("env_combat_background")
            # Preload basic cards
            starter_cards = ["sand_grain", "desert_whisper", "tomb_strike", "ankh_blessing"]
            self.preload_card_set(starter_cards)
            
        elif screen_name == "deck_builder":
            self.get_asset("env_deck_builder_background")
            # Preload all available cards
            all_cards = [desc.base_name for desc in self.asset_descriptors.values() 
                        if desc.category == AssetCategory.CARDS]
            self.preload_card_set(all_cards, (220, 300))  # Smaller deck builder size
            
        elif screen_name == "progression":
            self.get_asset("env_progression_background")
    
    def get_asset_quality_info(self, asset_id: str) -> Dict[str, Any]:
        """Get information about asset quality levels"""
        descriptor = self.asset_descriptors.get(asset_id)
        if not descriptor:
            return {"error": f"Unknown asset: {asset_id}"}
        
        info = {
            "asset_id": asset_id,
            "category": descriptor.category.value,
            "base_name": descriptor.base_name,
            "available_qualities": [q.value for q in descriptor.available_qualities],
            "has_hades_quality": AssetQuality.HADES in descriptor.available_qualities,
            "has_standard_quality": AssetQuality.STANDARD in descriptor.available_qualities,
            "has_concept_art": AssetQuality.CONCEPT in descriptor.available_qualities
        }
        
        return info
    
    def get_all_assets_info(self) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive information about all assets"""
        return {asset_id: self.get_asset_quality_info(asset_id) 
                for asset_id in self.asset_descriptors.keys()}
    
    def get_quality_statistics(self) -> Dict[str, Any]:
        """Get statistics about asset quality coverage"""
        total_assets = len(self.asset_descriptors)
        hades_count = sum(1 for desc in self.asset_descriptors.values() 
                         if AssetQuality.HADES in desc.available_qualities)
        standard_count = sum(1 for desc in self.asset_descriptors.values() 
                           if AssetQuality.STANDARD in desc.available_qualities)
        
        return {
            "total_assets": total_assets,
            "hades_quality_count": hades_count,
            "standard_quality_count": standard_count,
            "hades_quality_percentage": (hades_count / total_assets * 100) if total_assets > 0 else 0,
            "professional_coverage": f"{hades_count}/{total_assets} assets at Hades quality"
        }
    
    def clear_cache(self) -> None:
        """Clear the asset cache"""
        self.loaded_assets.clear()
        self.logger.info("Asset cache cleared")
    
    def set_quality_preference(self, prefer_hades: bool = True) -> None:
        """Set whether to prefer Hades quality assets"""
        self.prefer_hades_quality = prefer_hades
        self.logger.info(f"Asset quality preference: {'Hades' if prefer_hades else 'Standard'}")
    
    def get_memory_usage_estimate(self) -> Dict[str, int]:
        """Get estimated memory usage of loaded assets"""
        total_memory = 0
        asset_count = len(self.loaded_assets)
        
        for surface in self.loaded_assets.values():
            # Rough estimate: width * height * 4 bytes per pixel (RGBA)
            memory = surface.get_width() * surface.get_height() * 4
            total_memory += memory
        
        return {
            "total_bytes": total_memory,
            "total_mb": total_memory / (1024 * 1024),
            "loaded_asset_count": asset_count
        }


# Global professional asset manager
_global_professional_manager = None

def get_professional_asset_manager() -> ProfessionalAssetManager:
    """Get the global professional asset manager"""
    global _global_professional_manager
    if _global_professional_manager is None:
        _global_professional_manager = ProfessionalAssetManager()
    return _global_professional_manager

def initialize_professional_assets() -> None:
    """Initialize the professional asset system"""
    manager = get_professional_asset_manager()
    # Preload critical assets
    manager.preload_for_screen("menu")
    manager.logger.info("Professional asset system initialized")

def get_card_art_professional(card_name: str, size: Tuple[int, int] = (300, 420)) -> Optional[pygame.Surface]:
    """Get professional card art with quality fallback"""
    manager = get_professional_asset_manager()
    return manager.get_asset(f"card_{card_name}", size)

def get_environment_professional(env_name: str) -> Optional[pygame.Surface]:
    """Get professional environment background"""
    manager = get_professional_asset_manager()
    return manager.get_asset(f"env_{env_name}")

def get_ui_element_professional(ui_name: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
    """Get professional UI element"""
    manager = get_professional_asset_manager()
    return manager.get_asset(f"ui_{ui_name}", size)

def print_asset_quality_report():
    """Print a comprehensive asset quality report"""
    manager = get_professional_asset_manager()
    stats = manager.get_quality_statistics()
    
    print("\n" + "="*60)
    print("SANDS OF DUAT - ASSET QUALITY REPORT")
    print("="*60)
    print(f"Total Registered Assets: {stats['total_assets']}")
    print(f"Hades Quality Assets: {stats['hades_quality_count']}")
    print(f"Standard Quality Assets: {stats['standard_quality_count']}")
    print(f"Professional Coverage: {stats['hades_quality_percentage']:.1f}%")
    print(f"Quality Status: {stats['professional_coverage']}")
    
    memory_info = manager.get_memory_usage_estimate()
    print(f"Memory Usage: {memory_info['total_mb']:.2f} MB ({memory_info['loaded_asset_count']} assets loaded)")
    print("="*60)