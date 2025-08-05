"""
Asset Manager for Sands of Duat

Comprehensive asset preloading and optimization system that manages
AI-generated assets efficiently for smooth gameplay performance.
"""

import pygame
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import logging
import json
from dataclasses import dataclass, asdict

from .card_art_loader import get_card_art_loader
from .background_loader import get_background_loader
from .sprite_animator import create_character_sprite


class AssetType(Enum):
    """Types of assets"""
    CARD_ART = "card_art"
    BACKGROUND = "background"
    CHARACTER_SPRITE = "character_sprite"
    SOUND = "sound"
    FONT = "font"


class LoadingPriority(Enum):
    """Asset loading priorities"""
    CRITICAL = 1    # Must be loaded before game starts
    HIGH = 2        # Load immediately after critical
    MEDIUM = 3      # Load during gameplay transitions
    LOW = 4         # Load when system is idle


@dataclass
class AssetRequest:
    """Request for asset loading"""
    asset_type: AssetType
    asset_id: str
    path: str
    size: Optional[Tuple[int, int]] = None
    priority: LoadingPriority = LoadingPriority.MEDIUM
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class LoadingProgress:
    """Progress tracking for asset loading"""
    total_assets: int = 0
    loaded_assets: int = 0
    failed_assets: int = 0
    current_asset: str = ""
    
    @property
    def progress_percent(self) -> float:
        if self.total_assets == 0:
            return 100.0
        return (self.loaded_assets / self.total_assets) * 100.0
    
    @property
    def is_complete(self) -> bool:
        return self.loaded_assets + self.failed_assets >= self.total_assets


class AssetManager:
    """Main asset management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Asset storage
        self.loaded_assets: Dict[str, Any] = {}
        self.loading_queue: List[AssetRequest] = []
        self.failed_assets: List[str] = []
        
        # Loading state
        self.is_loading = False
        self.loading_thread: Optional[threading.Thread] = None
        self.progress = LoadingProgress()
        
        # Callbacks
        self.progress_callbacks: List[Callable[[LoadingProgress], None]] = []
        self.completion_callbacks: List[Callable[[bool], None]] = []
        
        # Performance settings
        self.max_memory_mb = 512  # Maximum memory usage in MB
        self.enable_compression = True
        self.enable_lazy_loading = True
        
        # Preload definitions
        self.preload_sets = {
            "core_game": self._get_core_game_assets(),
            "combat": self._get_combat_assets(),
            "menu": self._get_menu_assets(),
            "deck_builder": self._get_deck_builder_assets()
        }
        
        self.logger.info("Asset Manager initialized")
    
    def add_progress_callback(self, callback: Callable[[LoadingProgress], None]) -> None:
        """Add callback for loading progress updates"""
        self.progress_callbacks.append(callback)
    
    def add_completion_callback(self, callback: Callable[[bool], None]) -> None:
        """Add callback for loading completion"""
        self.completion_callbacks.append(callback)
    
    def request_asset(self, request: AssetRequest) -> None:
        """Request an asset to be loaded"""
        # Check if already loaded
        if request.asset_id in self.loaded_assets:
            return
        
        # Check if already in queue
        for queued_request in self.loading_queue:
            if queued_request.asset_id == request.asset_id:
                # Upgrade priority if needed
                if request.priority.value < queued_request.priority.value:
                    queued_request.priority = request.priority
                return
        
        self.loading_queue.append(request)
        self._sort_loading_queue()
        
        self.logger.debug(f"Queued asset: {request.asset_id} (priority: {request.priority.name})")
    
    def preload_set(self, set_name: str, blocking: bool = False) -> None:
        """Preload a predefined set of assets"""
        if set_name not in self.preload_sets:
            self.logger.warning(f"Unknown preload set: {set_name}")
            return
        
        assets = self.preload_sets[set_name]
        for asset_request in assets:
            self.request_asset(asset_request)
        
        if blocking:
            self.start_loading(blocking=True)
        elif not self.is_loading:
            self.start_loading(blocking=False)
    
    def start_loading(self, blocking: bool = False) -> None:
        """Start loading queued assets"""
        if self.is_loading:
            self.logger.warning("Asset loading already in progress")
            return
        
        if not self.loading_queue:
            self.logger.info("No assets queued for loading")
            return
        
        self.is_loading = True
        self.progress = LoadingProgress(total_assets=len(self.loading_queue))
        
        if blocking:
            self._load_assets_sync()
        else:
            self.loading_thread = threading.Thread(target=self._load_assets_sync, daemon=True)
            self.loading_thread.start()
        
        self.logger.info(f"Started loading {len(self.loading_queue)} assets")
    
    def _load_assets_sync(self) -> None:
        """Load assets synchronously (runs in thread)"""
        success_count = 0
        
        while self.loading_queue and self.is_loading:
            request = self.loading_queue.pop(0)
            self.progress.current_asset = request.asset_id
            
            try:
                asset = self._load_single_asset(request)
                if asset is not None:
                    self.loaded_assets[request.asset_id] = asset
                    success_count += 1
                    self.progress.loaded_assets += 1
                    self.logger.debug(f"Loaded asset: {request.asset_id}")
                else:
                    self.failed_assets.append(request.asset_id)
                    self.progress.failed_assets += 1
                    self.logger.warning(f"Failed to load asset: {request.asset_id}")
                
            except Exception as e:
                self.failed_assets.append(request.asset_id)
                self.progress.failed_assets += 1
                self.logger.error(f"Error loading asset {request.asset_id}: {e}")
            
            # Update progress
            self._notify_progress()
            
            # Small delay to prevent blocking
            time.sleep(0.001)
        
        # Loading complete
        self.is_loading = False
        self.progress.current_asset = ""
        
        success = len(self.failed_assets) == 0
        self.logger.info(f"Asset loading complete: {success_count} loaded, {len(self.failed_assets)} failed")
        
        # Notify completion
        for callback in self.completion_callbacks:
            try:
                callback(success)
            except Exception as e:
                self.logger.error(f"Error in completion callback: {e}")
    
    def _load_single_asset(self, request: AssetRequest) -> Optional[Any]:
        """Load a single asset"""
        try:
            if request.asset_type == AssetType.CARD_ART:
                loader = get_card_art_loader()
                return loader.load_card_art(request.asset_id, request.size)
            
            elif request.asset_type == AssetType.BACKGROUND:
                loader = get_background_loader()
                return loader.load_background(request.asset_id, request.size, request.context)
            
            elif request.asset_type == AssetType.CHARACTER_SPRITE:
                return create_character_sprite(request.asset_id)
            
            elif request.asset_type == AssetType.SOUND:
                # Sound loading would go here
                return None
            
            elif request.asset_type == AssetType.FONT:
                # Font loading would go here
                return None
            
            else:
                self.logger.warning(f"Unknown asset type: {request.asset_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to load {request.asset_type.value} asset {request.asset_id}: {e}")
            return None
    
    def _sort_loading_queue(self) -> None:
        """Sort loading queue by priority"""
        self.loading_queue.sort(key=lambda x: x.priority.value)
    
    def _notify_progress(self) -> None:
        """Notify progress callbacks"""
        for callback in self.progress_callbacks:
            try:
                callback(self.progress)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {e}")
    
    def get_asset(self, asset_id: str) -> Optional[Any]:
        """Get a loaded asset"""
        return self.loaded_assets.get(asset_id)
    
    def is_asset_loaded(self, asset_id: str) -> bool:
        """Check if asset is loaded"""
        return asset_id in self.loaded_assets
    
    def unload_asset(self, asset_id: str) -> None:
        """Unload an asset to free memory"""
        if asset_id in self.loaded_assets:
            del self.loaded_assets[asset_id]
            self.logger.debug(f"Unloaded asset: {asset_id}")
    
    def get_memory_usage_mb(self) -> float:
        """Estimate memory usage in MB (simplified)"""
        # This is a rough estimate - actual implementation would be more precise
        return len(self.loaded_assets) * 0.5  # Assume 0.5MB per asset on average
    
    def optimize_memory(self) -> None:
        """Optimize memory usage by unloading low-priority assets"""
        current_usage = self.get_memory_usage_mb()
        if current_usage <= self.max_memory_mb:
            return
        
        # This is a simplified optimization - real implementation would be more sophisticated
        assets_to_unload = list(self.loaded_assets.keys())[-10:]  # Remove 10 most recent
        for asset_id in assets_to_unload:
            self.unload_asset(asset_id)
        
        self.logger.info(f"Memory optimization: unloaded {len(assets_to_unload)} assets")
    
    def get_loading_stats(self) -> Dict[str, Any]:
        """Get comprehensive loading statistics"""
        return {
            "loaded_count": len(self.loaded_assets),
            "failed_count": len(self.failed_assets),
            "queue_count": len(self.loading_queue),
            "is_loading": self.is_loading,
            "memory_usage_mb": self.get_memory_usage_mb(),
            "progress": asdict(self.progress)
        }
    
    def _get_core_game_assets(self) -> List[AssetRequest]:
        """Get core game assets that must be loaded first"""
        assets = []
        
        # Critical backgrounds
        assets.append(AssetRequest(
            AssetType.BACKGROUND, "menu", "menu_background.png",
            priority=LoadingPriority.CRITICAL
        ))
        
        # Essential card arts (starter deck)
        starter_cards = ["Desert Whisper", "Sand Grain", "Tomb Strike", "Ankh Blessing"]
        for card_name in starter_cards:
            assets.append(AssetRequest(
                AssetType.CARD_ART, card_name, f"{card_name.lower().replace(' ', '_')}.png",
                size=(300, 420), priority=LoadingPriority.CRITICAL
            ))
        
        # Essential character sprites
        assets.append(AssetRequest(
            AssetType.CHARACTER_SPRITE, "player_character", "player_character_idle.png",
            priority=LoadingPriority.CRITICAL
        ))
        
        return assets
    
    def _get_combat_assets(self) -> List[AssetRequest]:
        """Get combat-specific assets"""
        assets = []
        
        # Combat background
        assets.append(AssetRequest(
            AssetType.BACKGROUND, "combat", "combat_background.png",
            priority=LoadingPriority.HIGH
        ))
        
        # Enemy sprites
        enemies = ["anubis_guardian", "desert_scorpion", "pharaoh_lich"]
        for enemy in enemies:
            assets.append(AssetRequest(
                AssetType.CHARACTER_SPRITE, enemy, f"{enemy}_idle.png",
                priority=LoadingPriority.HIGH
            ))
        
        return assets
    
    def _get_menu_assets(self) -> List[AssetRequest]:
        """Get menu-specific assets"""
        assets = []
        
        # Menu backgrounds with context
        contexts = [
            {"game_state": "victory"},
            {"game_state": "defeat"}
        ]
        
        for context in contexts:
            assets.append(AssetRequest(
                AssetType.BACKGROUND, "menu", "menu_background.png",
                context=context, priority=LoadingPriority.MEDIUM
            ))
        
        return assets
    
    def _get_deck_builder_assets(self) -> List[AssetRequest]:
        """Get deck builder assets"""
        assets = []
        
        # All card arts at deck builder size
        card_names = [
            "Scarab Swarm", "Papyrus Scroll", "Mummy's Wrath", "Isis's Grace",
            "Pyramid Power", "Thoth's Wisdom", "Anubis Judgment", "Ra's Solar Flare",
            "Pharaoh's Resurrection"
        ]
        
        for card_name in card_names:
            assets.append(AssetRequest(
                AssetType.CARD_ART, card_name, f"{card_name.lower().replace(' ', '_')}.png",
                size=(220, 300), priority=LoadingPriority.MEDIUM
            ))
        
        return assets


# Global asset manager
_global_asset_manager = None

def get_asset_manager() -> AssetManager:
    """Get global asset manager"""
    global _global_asset_manager
    if _global_asset_manager is None:
        _global_asset_manager = AssetManager()
    return _global_asset_manager

def preload_for_screen(screen_name: str) -> None:
    """Preload assets for a specific screen"""
    manager = get_asset_manager()
    
    if screen_name in ["menu", "main_menu"]:
        manager.preload_set("menu")
    elif screen_name in ["combat", "dynamic_combat"]:
        manager.preload_set("combat")  
    elif screen_name == "deck_builder":
        manager.preload_set("deck_builder")

def initialize_asset_system() -> None:
    """Initialize the asset system with core assets"""
    manager = get_asset_manager()
    manager.preload_set("core_game", blocking=True)
    
def get_loading_progress() -> LoadingProgress:
    """Get current loading progress"""
    return get_asset_manager().progress