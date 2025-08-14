#!/usr/bin/env python3
"""
SANDS OF DUAT - ENHANCED ASSET LOADING SYSTEM
==============================================

SPRINT 2 UPGRADE: Now uses Smart Asset Loader with 4K AI-generated assets
- Professional Egyptian art pipeline with Stable Diffusion XL
- Intelligent quality selection based on screen resolution  
- Fallback system for missing assets
- Enhanced caching and memory management
"""

import pygame
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from enum import Enum
import time
from dataclasses import dataclass

# Import the new smart asset loader
from ..assets.smart_asset_loader import smart_asset_loader

logger = logging.getLogger(__name__)

@dataclass
class AnimationFrame:
    """Single frame of an animated sprite"""
    surface: pygame.Surface
    duration: float  # Duration in milliseconds
    
@dataclass 
class AnimationData:
    """Complete animation data for a sprite"""
    frames: List[AnimationFrame]
    loop: bool
    fps: int
    total_duration: float
    metadata: Dict

class AssetType(Enum):
    """Types of generated game assets"""
    CARD_LEGENDARY = "legendary"
    CARD_EPIC = "epic" 
    CARD_RARE = "rare"
    CARD_COMMON = "common"
    BACKGROUND = "bg_"
    CHARACTER = "char_"
    UI_FRAME = "ui_card_frame_"
    UI_ICON = "ui_"
    UI_BUTTON = "ui_"
    ANIMATED_CARD = "anim_card_"
    ANIMATED_BACKGROUND = "anim_bg_"
    ANIMATED_UI = "anim_ui_"

class GeneratedAssetLoader:
    """
    Manages loading and caching of AI-generated game assets.
    
    Features:
    - Lazy loading for performance
    - Asset categorization by game function
    - Memory management with LRU cache
    - Direct access to generated artwork
    - Card rarity mapping
    """
    
    def __init__(self, assets_path: Optional[Path] = None):
        self.assets_path = assets_path or self._get_assets_path()
        self.generated_art_path = self.assets_path / "generated_art"
        self.approved_art_path = self.assets_path / "approved_hades_quality"
        self.animated_cards_path = self.assets_path / "game_ready" / "cards"
        self.compressed_sprites_path = self.assets_path / "compressed_sprites"
        
        # Asset caches
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._animation_cache: Dict[str, AnimationData] = {}
        self._asset_registry: Dict[AssetType, List[str]] = {}
        self._active_animations: Dict[str, Tuple[int, float]] = {}  # frame_index, last_update
        
        # Game-specific asset mappings
        self.card_art_mapping = self._create_card_mapping()
        self.background_mapping = self._create_background_mapping()
        self.character_mapping = self._create_character_mapping()
        self.ui_mapping = self._create_ui_mapping()
        self.animated_card_mapping = self._create_animated_card_mapping()
        
        # Performance settings
        self.max_cache_size = 100  # Maximum cached images
        self.target_card_size = (300, 420)  # Standard card dimensions
        
        # Initialize the asset system
        self._initialize()
    
    def _get_assets_path(self) -> Path:
        """Get the assets directory path."""
        current_dir = Path(__file__).parent
        return current_dir.parent.parent.parent / "assets"
    
    def _initialize(self):
        """Initialize the asset loading system with SPRINT 2 enhancements."""
        logger.info("Initializing Enhanced Asset Loader (SPRINT 2)...")
        
        # Initialize smart asset loader integration
        smart_asset_loader.preload_common_assets()
        
        # Check if approved assets exist (priority), fallback to generated
        if self.approved_art_path.exists():
            logger.info(f"Using approved Hades-quality assets from: {self.approved_art_path}")
        elif not self.generated_art_path.exists():
            logger.warning(f"No legacy assets found - using SPRINT 2 smart asset system")
        
        # Scan and categorize assets
        self._scan_generated_assets()
        
        logger.info(f"Enhanced asset loader initialized with smart 4K asset pipeline")
    
    def _create_card_mapping(self) -> Dict[str, str]:
        """Create mapping of card names to RTX 5070 generated Egyptian cards."""
        return {
            # RTX 5070 Generated Egyptian Cards (Legendary)
            'ANUBIS - JUDGE OF THE DEAD': 'anubis_judge_of_the_dead.png',
            'RA - SUN GOD': 'ra_sun_god.png',
            'ISIS - DIVINE MOTHER': 'isis_divine_mother.png',
            'SET - CHAOS GOD': 'set_chaos_god.png',
            
            # RTX 5070 Generated Egyptian Cards (Epic)
            'EGYPTIAN WARRIOR': 'egyptian_warrior.png',
            'PHARAOH\'S GUARD': 'pharaoh\'s_guard.png',
            
            # RTX 5070 Generated Egyptian Cards (Rare)
            'MUMMY GUARDIAN': 'mummy_guardian.png',
            'SPHINX GUARDIAN': 'sphinx_guardian.png',
            
            # Alternative names for compatibility
            'Ra - Sun God': 'ra_sun_god.png',
            'Ra': 'ra_sun_god.png',
            'Anubis - Judgment': 'anubis_judge_of_the_dead.png',
            'Anubis': 'anubis_judge_of_the_dead.png',
            'Isis - Protection': 'isis_divine_mother.png',
            'Isis': 'isis_divine_mother.png',
            'Horus': 'ra_sun_god.png',  # Use Ra as fallback
            'Bastet': 'isis_divine_mother.png',  # Use Isis as fallback
            'Thoth': 'anubis_judge_of_the_dead.png',  # Use Anubis as fallback
            'Sobek': 'mummy_guardian.png',
            'Ptah': 'egyptian_warrior.png',
            'Set - Chaos Storm': 'set_chaos_god.png',
            'Egyptian Warrior': 'egyptian_warrior.png',
            'Mummy Guardian': 'mummy_guardian.png',
            'Sphinx Guardian': 'sphinx_guardian.png',
            'Pharaoh\'s Guard': 'pharaoh\'s_guard.png',
            
            # Additional deck cards mapping
            'TEMPLE GUARD': 'egyptian_warrior.png',
            'DIVINE LIGHTNING': 'ra_sun_god.png',
            'ANUBIS BLESSING': 'anubis_judge_of_the_dead.png',
            'SHADOW SERVANT': 'mummy_guardian.png',
            'UNDERWORLD CURSE': 'set_chaos_god.png',
            'DEATH\'S EMBRACE': 'anubis_judge_of_the_dead.png',
            
            # Combat system alternative names
            'JUDGMENT SCALE': 'anubis_judge_of_the_dead.png',
            'DEITY\'S EMBRACE': 'isis_divine_mother.png',
            'ANUBIS\'S WRATH': 'set_chaos_god.png',
            'BLESSED SCARAB': 'sphinx_guardian.png',
            'SACRED SCARAB': 'sphinx_guardian.png',
            'PHARAOH POWER': 'egyptian_warrior.png',
            'PYRAMID POWER': 'ra_sun_god.png',
            'WISDOM SERVANT': 'mummy_guardian.png'
        }
    
    def _create_animated_card_mapping(self) -> Dict[str, str]:
        """Create mapping of card names to RTX 5070 Hades-quality animated sprites."""
        return {
            # RTX 5070 Generated Animations (16 frames @ 12fps each)
            'ANUBIS - JUDGE OF THE DEAD': 'anubis_judge_of_the_dead_animated.png',
            'RA - SUN GOD': 'ra_sun_god_animated.png',
            'ISIS - DIVINE MOTHER': 'isis_divine_mother_animated.png',
            'SET - CHAOS GOD': 'set_chaos_god_animated.png',
            'EGYPTIAN WARRIOR': 'egyptian_warrior_animated.png',
            'PHARAOH\'S GUARD': 'pharaoh\'s_guard_animated.png',
            'MUMMY GUARDIAN': 'mummy_guardian_animated.png',
            'SPHINX GUARDIAN': 'sphinx_guardian_animated.png',
            
            # Alternative names for compatibility
            'Anubis - Judgment': 'anubis_judge_of_the_dead_animated.png',
            'Ra - Sun God': 'ra_sun_god_animated.png', 
            'Isis - Protection': 'isis_divine_mother_animated.png',
            'Set - Chaos Storm': 'set_chaos_god_animated.png',
            'Egyptian Warrior': 'egyptian_warrior_animated.png',
            'Mummy Guardian': 'mummy_guardian_animated.png',
            'Sphinx Guardian': 'sphinx_guardian_animated.png',
            'Pharaoh\'s Guard': 'pharaoh\'s_guard_animated.png'
        }
    
    def _create_background_mapping(self) -> Dict[str, str]:
        """Create mapping of game screens to ultra high resolution background files."""
        return {
            # Ultra High Resolution Backgrounds (4096x2048)
            'main_menu': 'bg_main_menu_4k.png',
            'menu': 'bg_main_menu_4k.png',
            'deck_builder': 'bg_deck_builder_4k.png',
            'combat': 'bg_combat_4k.png',
            'hall_of_gods': 'bg_hall_of_gods_4k.png',
            'collection': 'bg_hall_of_gods_4k.png',
            'settings': 'bg_settings_4k.png',
            'underworld': 'bg_combat_4k.png',
            'map': 'bg_map_4k.png',  # Egyptian progression map background
            
            # Fallback for any unmapped screens
            'default': 'bg_main_menu_4k.png'
        }
    
    def _create_character_mapping(self) -> Dict[str, str]:
        """Create mapping of characters to ultra high resolution portrait files."""
        return {
            # Ultra High Resolution Character Portraits (2048x2048)
            'player_hero': 'char_player_hero_2k.png',
            'anubis_boss': 'char_anubis_boss_2k.png',
            'mummy_guardian': 'char_mummy_guardian_2k.png',
            'sphinx_guardian': 'char_sphinx_guardian_2k.png',
            'ra_deity': 'char_ra_deity_2k.png',
            'isis_goddess': 'char_isis_goddess_2k.png',
            'set_god': 'char_set_god_2k.png',
            
            # Alternative names for compatibility
            'anubis': 'char_anubis_boss_2k.png',
            'player': 'char_player_hero_2k.png',
            'hero': 'char_player_hero_2k.png'
        }
    
    def _create_ui_mapping(self) -> Dict[str, str]:
        """Create mapping of UI elements to ultra high resolution files."""
        return {
            # Ultra High Resolution Card Frames (1024x1536)
            'frame_legendary': 'ui_card_frame_legendary.png',
            'frame_epic': 'ui_card_frame_epic.png',
            'frame_rare': 'ui_card_frame_epic.png',     # Use epic as fallback for rare
            'frame_common': 'ui_card_frame_epic.png',   # Use epic as fallback for common
            
            # Card frames with proper ui_ prefix (for compatibility)
            'ui_card_frame_legendary': 'ui_card_frame_legendary.png',
            'ui_card_frame_epic': 'ui_card_frame_epic.png', 
            'ui_card_frame_rare': 'ui_card_frame_legendary.png',     # Use legendary as fallback
            'ui_card_frame_common': 'ui_card_frame_epic.png',   # Use epic for common
            
            # High Resolution Icons (512x512)
            'health_icon': 'ui_ankh_health_icon.png',
            'energy_icon': 'ui_scarab_energy_icon.png',
            'time_icon': 'ui_hourglass_icon.png',
            'victory_icon': 'ui_pyramid_victory_icon.png',
            'mana_icon': 'ui_scarab_energy_icon.png',
            'attack_icon': 'ui_scarab_energy_icon.png',  # Fallback until khopesh icon available
            'defense_icon': 'ui_ankh_health_icon.png',   # Fallback until shield icon available
            
            # Enhanced Buttons
            'play_button': 'ui_play_button.png',
            'deck_button': 'ui_deck_button.png',
            'collection_button': 'ui_collection_button.png',
            'settings_button': 'ui_settings_button.png',
            'exit_button': 'ui_exit_button.png',
            'back_button': 'ui_back_button.png'
        }
    
    def _scan_generated_assets(self):
        """Scan and categorize all generated game assets."""
        for asset_type in AssetType:
            self._asset_registry[asset_type] = []
        
        # First scan approved assets if they exist
        png_files = []
        if self.approved_art_path.exists():
            # Scan all subdirectories in approved assets
            for subdir in ['characters', 'environments', 'ui', 'cards']:
                subdir_path = self.approved_art_path / subdir
                if subdir_path.exists():
                    png_files.extend(list(subdir_path.glob("*.png")))
        
        # Scan animated cards directory
        if self.animated_cards_path.exists():
            png_files.extend(list(self.animated_cards_path.glob("*.png")))
        
        # Scan compressed sprites directory
        if self.compressed_sprites_path.exists():
            for subdir in ['cards', 'backgrounds', 'ui']:
                subdir_path = self.compressed_sprites_path / subdir
                if subdir_path.exists():
                    png_files.extend(list(subdir_path.glob("*.png")))
        
        # Also scan generated_art directory
        if self.generated_art_path.exists():
            png_files.extend(list(self.generated_art_path.glob("*.png")))
        
        for png_file in png_files:
            filename = png_file.name
            
            # Categorize by filename patterns
            if filename.startswith('bg_'):
                self._asset_registry[AssetType.BACKGROUND].append(filename)
            elif filename.startswith('char_'):
                self._asset_registry[AssetType.CHARACTER].append(filename)
            elif filename.startswith('ui_card_frame_'):
                self._asset_registry[AssetType.UI_FRAME].append(filename)
            elif filename.startswith('ui_') and ('button' in filename or 'icon' in filename):
                if 'button' in filename:
                    self._asset_registry[AssetType.UI_BUTTON].append(filename)
                else:
                    self._asset_registry[AssetType.UI_ICON].append(filename)
            elif filename.endswith('_anim.png'):
                # Animated assets
                if 'card' in filename.lower() or any(card_name.lower().replace(' ', '_').replace('-', '_') in filename.lower() for card_name in self.animated_card_mapping.keys()):
                    self._asset_registry[AssetType.ANIMATED_CARD].append(filename)
                elif 'bg_' in filename or 'background' in filename:
                    self._asset_registry[AssetType.ANIMATED_BACKGROUND].append(filename) 
                elif 'ui_' in filename:
                    self._asset_registry[AssetType.ANIMATED_UI].append(filename)
            else:
                # Card artwork - categorize by card name mapping
                for card_name, card_file in self.card_art_mapping.items():
                    if filename == card_file:
                        if 'ra_sun_god' in filename or 'anubis_judgment' in filename or 'osiris_resurrection' in filename or 'horus_divine_sight' in filename or 'isis_protection' in filename:
                            self._asset_registry[AssetType.CARD_LEGENDARY].append(filename)
                        elif 'thoth_wisdom' in filename or 'bastet_feline_grace' in filename or 'set_chaos_storm' in filename or 'sekhmet_war_cry' in filename or 'pharaoh_divine_mandate' in filename or 'pyramid_power' in filename or 'ankh_blessing' in filename:
                            self._asset_registry[AssetType.CARD_EPIC].append(filename)
                        elif 'mummy_wrath' in filename or 'scarab_swarm' in filename or 'desert_whisper' in filename or 'temple_offering' in filename or 'canopic_jar_ritual' in filename:
                            self._asset_registry[AssetType.CARD_RARE].append(filename)
                        else:
                            self._asset_registry[AssetType.CARD_COMMON].append(filename)
                        break
        
        # Log categorization results
        for asset_type, files in self._asset_registry.items():
            if files:
                logger.info(f"{asset_type.name}: {len(files)} assets")
    
    def get_total_asset_count(self) -> int:
        """Get total number of available assets."""
        return sum(len(files) for files in self._asset_registry.values())
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[str]:
        """Get all asset filenames for a specific type."""
        return self._asset_registry.get(asset_type, []).copy()
    
    def load_image(self, filename: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        Load an image asset with optional resizing.
        
        Args:
            filename: Name of the image file
            size: Optional target size (width, height)
            
        Returns:
            Loaded pygame Surface or None if not found
        """
        cache_key = f"{filename}_{size}" if size else filename
        
        # Check cache first
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # Try approved assets first, then fallback to generated
        image_path = None
        
        # Check approved assets directory structure (ultra high resolution)
        if self.approved_art_path.exists():
            # Handle paths with subdirectories (e.g., "events/thoth_oracle")
            if "/" in filename or "\\" in filename:
                candidate_path = self.approved_art_path / filename
                if candidate_path.exists():
                    image_path = candidate_path
                elif not filename.endswith('.png'):
                    # Try with .png extension
                    candidate_path_png = self.approved_art_path / f"{filename}.png"
                    if candidate_path_png.exists():
                        image_path = candidate_path_png
            else:
                # Priority search order for ultra high resolution assets
                search_dirs = [
                    self.approved_art_path / "cards",
                    self.approved_art_path / "backgrounds", 
                    self.approved_art_path / "characters",
                    self.approved_art_path / "ui_elements",
                    self.approved_art_path / "animated_cards",
                    self.approved_art_path / "events"  # Divine event illustrations
                ]
                
                for search_dir in search_dirs:
                    if search_dir.exists():
                        candidate_path = search_dir / filename
                        if candidate_path.exists():
                            image_path = candidate_path
                            break
        
        # Fallback to generated art
        if not image_path:
            image_path = self.generated_art_path / filename
            
        if not image_path.exists():
            logger.warning(f"Asset not found: {filename}")
            return None
        
        try:
            # Load image
            surface = pygame.image.load(str(image_path))
            
            # Resize if requested
            if size:
                surface = pygame.transform.scale(surface, size)
            
            # Cache the image (with LRU management)
            self._cache_image(cache_key, surface)
            
            logger.debug(f"Loaded asset: {filename}")
            return surface
            
        except Exception as e:
            logger.error(f"Failed to load asset {filename}: {e}")
            return None
    
    def _cache_image(self, cache_key: str, surface: pygame.Surface):
        """Cache an image with LRU management."""
        # Simple LRU: remove oldest if cache is full
        if len(self._image_cache) >= self.max_cache_size:
            # Remove the first (oldest) item
            oldest_key = next(iter(self._image_cache))
            del self._image_cache[oldest_key]
        
        self._image_cache[cache_key] = surface
    
    def load_card_art_by_name(self, card_name: str) -> Optional[pygame.Surface]:
        """
        Load card art by card name (prioritizes animated version).
        
        Args:
            card_name: Name of the card to load art for
            
        Returns:
            Card-sized pygame Surface or None
        """
        # Check for animated version first
        animated_filename = self.animated_card_mapping.get(card_name)
        if animated_filename:
            animated_surface = self.load_animated_card(card_name)
            if animated_surface:
                return animated_surface
        
        # Fallback to static image
        filename = self.card_art_mapping.get(card_name)
        if not filename:
            logger.warning(f"No artwork mapped for card: {card_name}")
            return None
        
        return self.load_image(filename, self.target_card_size)
    
    def load_background(self, screen_name: str) -> Optional[pygame.Surface]:
        """
        Load background for a specific screen with SPRINT 2 smart loading.
        
        Args:
            screen_name: Name of the screen (combat, menu, deck_builder, etc.)
            
        Returns:
            Full-sized pygame Surface or None
        """
        # Try smart asset loader first (SPRINT 2)
        background = smart_asset_loader.get_background(screen_name)
        if background:
            logger.debug(f"Loaded 4K background for {screen_name}")
            return background
        
        # Fallback to legacy system
        filename = self.background_mapping.get(screen_name)
        if filename:
            legacy_bg = self.load_image(filename)
            if legacy_bg:
                logger.debug(f"Using legacy background for {screen_name}")
                return legacy_bg
        
        logger.warning(f"No background found for screen: {screen_name}")
        return None
    
    def load_character_portrait(self, character_name: str) -> Optional[pygame.Surface]:
        """
        Load character portrait by name.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Portrait-sized pygame Surface or None
        """
        filename = self.character_mapping.get(character_name)
        if not filename:
            logger.warning(f"No portrait mapped for character: {character_name}")
            return None
        
        return self.load_image(filename, (512, 768))  # Portrait aspect ratio
    
    def load_ui_element(self, element_name: str) -> Optional[pygame.Surface]:
        """
        Load UI element by name.
        
        Args:
            element_name: Name of the UI element
            
        Returns:
            UI-sized pygame Surface or None
        """
        filename = self.ui_mapping.get(element_name)
        if not filename:
            logger.warning(f"No UI element mapped for: {element_name}")
            return None
        
        return self.load_image(filename)
    
    def load_ui_icon(self, icon_name: str) -> Optional[pygame.Surface]:
        """Load a UI icon by name."""
        # Try UI mapping first
        filename = self.ui_mapping.get(icon_name)
        if filename:
            return self.load_image(filename)
            
        # Try direct filename
        if icon_name.endswith('.png'):
            return self.load_image(icon_name)
        
        # Try adding .png extension
        filename = f"{icon_name}.png"
        return self.load_image(filename)
    
    def get_random_card_art_by_rarity(self, rarity: str) -> Optional[pygame.Surface]:
        """Get random card art by rarity level."""
        import random
        
        rarity_mapping = {
            'legendary': AssetType.CARD_LEGENDARY,
            'epic': AssetType.CARD_EPIC, 
            'rare': AssetType.CARD_RARE,
            'common': AssetType.CARD_COMMON
        }
        
        asset_type = rarity_mapping.get(rarity.lower())
        if not asset_type:
            return None
            
        assets = self.get_assets_by_type(asset_type)
        if not assets:
            return None
        
        filename = random.choice(assets)
        return self.load_image(filename, self.target_card_size)
    
    def get_card_frame_by_rarity(self, rarity: str) -> Optional[pygame.Surface]:
        """Get card frame by rarity level."""
        frame_name = f"frame_{rarity.lower()}"
        return self.load_ui_element(frame_name)
    
    def preload_essential_assets(self):
        """Preload essential assets for smooth gameplay."""
        logger.info("Preloading essential Egyptian assets...")
        
        # Preload essential assets for immediate use
        # Preload one asset from each type
        for asset_type in AssetType:
            assets = self.get_assets_by_type(asset_type)
            if assets:
                # Load the first asset from each type
                self.load_image(assets[0])
        
        # Preload key backgrounds
        self.load_background('menu')
        self.load_background('combat')
        
        logger.info("Essential assets preloaded")
    
    def get_all_card_names(self) -> List[str]:
        """Get all available card names."""
        return list(self.card_art_mapping.keys())
    
    def get_all_backgrounds(self) -> List[str]:
        """Get all available background screen names."""
        return list(self.background_mapping.keys())
    
    def get_all_characters(self) -> List[str]:
        """Get all available character names."""
        return list(self.character_mapping.keys())
    
    def get_all_ui_elements(self) -> List[str]:
        """Get all available UI element names."""
        return list(self.ui_mapping.keys())
    
    def load_animation_spritesheet(self, filename: str) -> Optional[AnimationData]:
        """Load and parse an animated spritesheet."""
        
        # Check cache first
        if filename in self._animation_cache:
            return self._animation_cache[filename]
        
        # Load spritesheet image
        spritesheet_path = None
        metadata_path = None
        
        # Check different directories for the spritesheet
        search_paths = [
            self.animated_cards_path,
            self.compressed_sprites_path / "cards",
            self.compressed_sprites_path / "backgrounds", 
            self.compressed_sprites_path / "ui"
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                test_path = search_path / filename
                # Try both naming conventions for metadata
                test_metadata1 = search_path / filename.replace('.png', '.json')
                test_metadata2 = search_path / filename.replace('_animated.png', '_animation.json')
                
                metadata_path_found = None
                if test_metadata1.exists():
                    metadata_path_found = test_metadata1
                elif test_metadata2.exists():
                    metadata_path_found = test_metadata2
                    
                if test_path.exists() and metadata_path_found:
                    spritesheet_path = test_path
                    metadata_path = metadata_path_found
                    break
        
        if not spritesheet_path or not metadata_path:
            logger.warning(f"Animation spritesheet or metadata not found: {filename}")
            return None
        
        try:
            # Load metadata
            with open(metadata_path) as f:
                metadata = json.load(f)
            
            # Load spritesheet
            spritesheet = pygame.image.load(str(spritesheet_path))
            
            # Extract frames
            frames = self._extract_animation_frames(spritesheet, metadata)
            
            if not frames:
                return None
            
            # Create animation data
            fps = metadata.get('fps', 12)
            frame_duration = 1000.0 / fps  # milliseconds per frame
            
            animation_frames = [
                AnimationFrame(surface=frame, duration=frame_duration)
                for frame in frames
            ]
            
            animation_data = AnimationData(
                frames=animation_frames,
                loop=metadata.get('loop', True),
                fps=fps,
                total_duration=len(frames) * frame_duration,
                metadata=metadata
            )
            
            # Cache animation
            self._animation_cache[filename] = animation_data
            
            logger.debug(f"Loaded animation: {filename} ({len(frames)} frames, {fps} fps)")
            return animation_data
            
        except Exception as e:
            logger.error(f"Failed to load animation {filename}: {e}")
            return None
    
    def _extract_animation_frames(self, spritesheet: pygame.Surface, metadata: Dict) -> List[pygame.Surface]:
        """Extract individual frames from a spritesheet."""
        
        frames = []
        frame_width, frame_height = metadata['frame_size']
        # Handle both naming conventions
        cols = metadata.get('cols', metadata.get('sheet_cols', 4))
        frame_count = metadata['frame_count']
        
        for i in range(frame_count):
            row = i // cols
            col = i % cols
            
            x = col * frame_width
            y = row * frame_height
            
            # Create subsurface for this frame
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            
            # Extract frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(spritesheet, (0, 0), frame_rect)
            
            frames.append(frame)
        
        return frames
    
    def load_animated_card(self, card_name: str) -> Optional[pygame.Surface]:
        """Load current frame of an animated card."""
        
        animated_filename = self.animated_card_mapping.get(card_name)
        if not animated_filename:
            return None
        
        animation_data = self.load_animation_spritesheet(animated_filename)
        if not animation_data:
            return None
        
        # Get current frame based on time
        current_time = time.time() * 1000  # milliseconds
        
        if card_name not in self._active_animations:
            self._active_animations[card_name] = (0, current_time)
        
        frame_index, last_update = self._active_animations[card_name]
        
        # Update frame if enough time has passed
        frame_duration = animation_data.frames[0].duration
        if current_time - last_update >= frame_duration:
            frame_index = (frame_index + 1) % len(animation_data.frames)
            self._active_animations[card_name] = (frame_index, current_time)
        
        # Get current frame surface
        current_frame = animation_data.frames[frame_index].surface
        
        # Scale to card size if needed
        if current_frame.get_size() != self.target_card_size:
            current_frame = pygame.transform.scale(current_frame, self.target_card_size)
        
        return current_frame
    
    def update_animations(self, dt: float):
        """Update all active animations. Call this in your game loop."""
        current_time = time.time() * 1000
        
        # Update active animations
        for animation_name in list(self._active_animations.keys()):
            frame_index, last_update = self._active_animations[animation_name]
            
            # Find the animation data
            animation_data = None
            if animation_name in self.animated_card_mapping:
                filename = self.animated_card_mapping[animation_name]
                animation_data = self.load_animation_spritesheet(filename)
            
            if not animation_data:
                continue
            
            # Check if we need to advance frame
            frame_duration = animation_data.frames[frame_index].duration
            if current_time - last_update >= frame_duration:
                new_frame_index = (frame_index + 1) % len(animation_data.frames)
                self._active_animations[animation_name] = (new_frame_index, current_time)
    
    def get_animation_info(self, animation_name: str) -> Optional[Dict]:
        """Get information about an animation."""
        
        if animation_name in self.animated_card_mapping:
            filename = self.animated_card_mapping[animation_name]
            animation_data = self.load_animation_spritesheet(filename)
            
            if animation_data:
                return {
                    'filename': filename,
                    'frame_count': len(animation_data.frames),
                    'fps': animation_data.fps,
                    'duration_ms': animation_data.total_duration,
                    'loop': animation_data.loop,
                    'metadata': animation_data.metadata
                }
        
        return None
    
    def preload_animations(self, animation_names: List[str] = None):
        """Preload specific animations for smooth gameplay."""
        
        if not animation_names:
            # Preload all animated cards by default
            animation_names = list(self.animated_card_mapping.keys())
        
        logger.info(f"Preloading {len(animation_names)} animations...")
        
        for animation_name in animation_names:
            # This will load and cache the animation
            self.load_animated_card(animation_name)
            
        logger.info("Animation preloading complete")
    
    def get_all_animated_cards(self) -> List[str]:
        """Get all available animated card names."""
        return list(self.animated_card_mapping.keys())
    
    def clear_cache(self):
        """Clear all caches to free memory."""
        self._image_cache.clear()
        self._animation_cache.clear()
        self._active_animations.clear()
        logger.info("All asset caches cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cached_images': len(self._image_cache),
            'cached_animations': len(self._animation_cache),
            'active_animations': len(self._active_animations),
            'max_cache_size': self.max_cache_size,
            'total_types': len(AssetType),
            'total_assets': self.get_total_asset_count()
        }

# Global asset loader instance
_asset_loader: Optional[GeneratedAssetLoader] = None

def get_asset_loader() -> GeneratedAssetLoader:
    """Get the global asset loader instance."""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = GeneratedAssetLoader()
    return _asset_loader

def initialize_assets():
    """Initialize the global asset loader."""
    global _asset_loader
    _asset_loader = GeneratedAssetLoader()
    _asset_loader.preload_essential_assets()
    return _asset_loader