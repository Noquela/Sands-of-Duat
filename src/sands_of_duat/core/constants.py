"""
Core constants for the Egyptian card game.
Defines colors, dimensions, timing, and Egyptian-themed values.
"""

import pygame
from typing import Tuple, Dict, Any

# SCREEN DIMENSIONS (Multiple Resolution Support)
# Default resolution (16:10 golden ratio for Egyptian aesthetic)
DEFAULT_WIDTH = 1400
DEFAULT_HEIGHT = 900

# Ultrawide support (21:9 aspect ratio)
ULTRAWIDE_WIDTH = 3440
ULTRAWIDE_HEIGHT = 1440

# Auto-detect best resolution
import pygame
pygame.init()
info = pygame.display.Info()
NATIVE_WIDTH = info.current_w
NATIVE_HEIGHT = info.current_h
NATIVE_ASPECT = NATIVE_WIDTH / NATIVE_HEIGHT

# Choose appropriate resolution based on screen
if NATIVE_ASPECT >= 2.3:  # Ultrawide 21:9 or wider
    SCREEN_WIDTH = min(ULTRAWIDE_WIDTH, NATIVE_WIDTH)
    SCREEN_HEIGHT = min(ULTRAWIDE_HEIGHT, NATIVE_HEIGHT)
elif NATIVE_WIDTH >= 2560:  # High resolution displays
    SCREEN_WIDTH = min(2560, NATIVE_WIDTH)
    SCREEN_HEIGHT = min(1440, NATIVE_HEIGHT)
else:  # Standard displays
    SCREEN_WIDTH = min(DEFAULT_WIDTH, NATIVE_WIDTH)
    SCREEN_HEIGHT = min(DEFAULT_HEIGHT, NATIVE_HEIGHT)

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# EGYPTIAN COLOR PALETTE
class Colors:
    """Egyptian-themed color constants with Hades-level polish."""
    
    # Primary Egyptian Colors
    GOLD = (255, 215, 0)
    GOLD_DARK = (184, 134, 11)
    LAPIS_LAZULI = (26, 81, 171)
    PAPYRUS = (245, 245, 220)
    DESERT_SAND = (238, 203, 173)
    DARK_BLUE = (25, 25, 112)
    
    # UI Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (220, 20, 20)
    GREEN = (20, 220, 20)
    TRANSPARENT = (0, 0, 0, 0)
    
    # Interactive Colors
    HOVER_GLOW = (255, 255, 255, 100)
    BUTTON_SELECTED = (255, 215, 0, 200)
    BUTTON_DISABLED = (128, 128, 128, 100)
    
    # Game State Colors
    HEALTH_FULL = (220, 20, 60)
    HEALTH_LOW = (139, 0, 0)
    MANA_FULL = (65, 105, 225)
    MANA_EMPTY = (25, 25, 112)
    
    # Card Colors
    CARD_COMMON = (245, 245, 220)
    CARD_RARE = (255, 215, 0)
    CARD_EPIC = (138, 43, 226)
    CARD_LEGENDARY = (255, 140, 0)

# TIMING CONSTANTS (60 FPS Targeting)
class Timing:
    """Animation and timing constants for smooth 60fps experience."""
    
    TARGET_FPS = 60
    FRAME_TIME = 1.0 / TARGET_FPS
    
    # Animation Durations (in seconds)
    FADE_DURATION = 0.3
    SLIDE_DURATION = 0.4
    BUTTON_HOVER_DURATION = 0.2
    CARD_FLIP_DURATION = 0.5
    DAMAGE_NUMBER_DURATION = 1.0
    
    # UI Timing
    TOOLTIP_DELAY = 0.8
    DOUBLE_CLICK_TIME = 0.5
    MENU_TRANSITION_TIME = 0.6

# LAYOUT CONSTANTS
class Layout:
    """UI layout and spacing constants with ultrawide support."""
    
    # Ultrawide-specific layouts - DEFINE FIRST
    IS_ULTRAWIDE = SCREEN_WIDTH >= 2560
    
    # Dynamic margins based on screen width
    SCREEN_MARGIN = max(20, SCREEN_WIDTH // 70)  # Scales with screen size
    COMPONENT_PADDING = 10
    BUTTON_PADDING = 15
    CARD_SPACING = 8
    
    # Component Sizes - Enhanced for ultrawide visibility
    BUTTON_HEIGHT = int(70 * (1.4 if IS_ULTRAWIDE else 1.0))  # 40% larger on ultrawide
    BUTTON_WIDTH_STANDARD = int(250 * (1.4 if IS_ULTRAWIDE else 1.0))
    BUTTON_WIDTH_WIDE = int(350 * (1.4 if IS_ULTRAWIDE else 1.0))
    
    # Health/Mana Bar
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    BAR_BORDER = 2
    
    # Card Dimensions (scaled for ultra high resolution assets)
    # Enhanced card sizing for ultrawide displays
    BASE_CARD_SCALE = min(1.5, SCREEN_HEIGHT / 900)  # Increased base scale for better visibility
    
    # Ultrawide gets even larger cards to fill the space better
    if IS_ULTRAWIDE:
        CARD_WIDTH = int(200 * BASE_CARD_SCALE)   # Much larger for ultrawide
        CARD_HEIGHT = int(300 * BASE_CARD_SCALE)  # Proportional increase
    else:
        CARD_WIDTH = int(150 * BASE_CARD_SCALE)
        CARD_HEIGHT = int(225 * BASE_CARD_SCALE)
    
    CARD_SCALE_HOVER = 1.15  # More noticeable hover effect
    CARD_SCALE_SELECTED = 1.08
    CARD_SCALE_TRANSITION_SPEED = 0.15  # Smooth scaling animation
    
    # High resolution card rendering
    CARD_SOURCE_WIDTH = 1024   # Ultra high res source resolution
    CARD_SOURCE_HEIGHT = 1536  # Matches generated asset resolution
    
    # Content area - using much more of the ultrawide space
    if IS_ULTRAWIDE:
        CONTENT_WIDTH = min(3200, SCREEN_WIDTH - (SCREEN_MARGIN * 2))  # Use 90% of ultrawide width
        CONTENT_X_OFFSET = (SCREEN_WIDTH - CONTENT_WIDTH) // 2
    else:
        CONTENT_WIDTH = SCREEN_WIDTH - (SCREEN_MARGIN * 2)
        CONTENT_X_OFFSET = SCREEN_MARGIN
    
    # Safe areas for UI elements
    UI_SAFE_LEFT = CONTENT_X_OFFSET
    UI_SAFE_RIGHT = CONTENT_X_OFFSET + CONTENT_WIDTH
    UI_SAFE_WIDTH = CONTENT_WIDTH
    UI_SAFE_HEIGHT = SCREEN_HEIGHT - (SCREEN_MARGIN * 2)
    UI_SAFE_TOP = SCREEN_MARGIN
    UI_SAFE_BOTTOM = SCREEN_HEIGHT - SCREEN_MARGIN
    
    # Ultra High Resolution Asset Constants
    BACKGROUND_SOURCE_WIDTH = 4096   # Ultra panoramic backgrounds
    BACKGROUND_SOURCE_HEIGHT = 2048  # 2:1 aspect ratio for ultrawide scaling
    CHARACTER_PORTRAIT_SIZE = 2048   # Square ultra high res portraits
    UI_ICON_SIZE = 512              # High resolution UI icons
    
    # Enhanced responsive font scaling for ultrawide displays
    BASE_FONT_SCALE = SCREEN_HEIGHT / 1080  # Base scaling from height
    ULTRAWIDE_BONUS = 0.2 if IS_ULTRAWIDE else 0.0  # Extra scaling for ultrawide readability
    FONT_SCALE = min(1.5, BASE_FONT_SCALE + ULTRAWIDE_BONUS)  # Enhanced scaling with ultrawide bonus
    
    # Enhanced visual effects for high resolution
    GLOW_RADIUS = max(4, int(8 * FONT_SCALE))
    SHADOW_OFFSET = max(2, int(3 * FONT_SCALE))
    BORDER_WIDTH = max(2, int(3 * FONT_SCALE))

# EGYPTIAN MYTHOLOGY CONSTANTS
class Egyptian:
    """Egyptian mythology-related constants."""
    
    # Gods and their colors
    GODS = {
        'RA': {'color': (255, 215, 0), 'domain': 'sun'},
        'ANUBIS': {'color': (64, 64, 64), 'domain': 'death'},
        'THOTH': {'color': (138, 43, 226), 'domain': 'wisdom'},
        'ISIS': {'color': (0, 191, 255), 'domain': 'magic'},
        'SET': {'color': (220, 20, 60), 'domain': 'chaos'},
        'OSIRIS': {'color': (34, 139, 34), 'domain': 'resurrection'},
    }
    
    # Card Types
    CARD_TYPES = [
        'SPELL',
        'ARTIFACT',
        'BLESSING',
        'CURSE',
        'RITUAL'
    ]
    
    # Underworld Locations
    UNDERWORLD_HOURS = [
        'Hour of Decision',
        'Hour of Shadows',
        'Hour of Judgment',
        'Hour of Weighing Hearts',
        'Hour of Divine Fire',
        'Hour of Resurrection',
        'Hour of Solar Rebirth'
    ]

# FONT SIZES - Enhanced for Ultrawide Readability
class FontSizes:
    """Font size constants for different UI elements with ultrawide scaling."""
    
    # Apply enhanced scaling for better readability and visual hierarchy
    TITLE_HUGE = int(88 * Layout.FONT_SCALE)    # Increased from 72 for stronger hierarchy
    TITLE_LARGE = int(64 * Layout.FONT_SCALE)   # Increased from 48 for better visibility
    TITLE_MEDIUM = int(48 * Layout.FONT_SCALE)  # Increased from 36 for clarity
    SUBTITLE = int(32 * Layout.FONT_SCALE)      # Increased from 28 for ultrawide
    BUTTON = int(26 * Layout.FONT_SCALE)        # Increased from 24 for button clarity
    BODY = int(24 * Layout.FONT_SCALE)          # Increased from 20 for readability
    CARD_NAME = int(20 * Layout.FONT_SCALE)     # Increased from 18 for card visibility
    TOOLTIP = int(18 * Layout.FONT_SCALE)       # Kept for comfortable reading
    CARD_TEXT = int(16 * Layout.FONT_SCALE)     # Good for card descriptions
    DEBUG = int(14 * Layout.FONT_SCALE)         # Kept smaller for debug info

# AUDIO CONSTANTS
class Audio:
    """Audio-related constants."""
    
    # Volume Levels (0.0 to 1.0)
    MASTER_VOLUME = 1.0
    MUSIC_VOLUME = 0.7
    SFX_VOLUME = 0.8
    UI_VOLUME = 0.6
    
    # Audio Settings
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 512
    CHANNELS = 2

# GAME BALANCE CONSTANTS
class Balance:
    """Game balance and mechanics constants."""
    
    # Player Stats
    STARTING_HEALTH = 100
    STARTING_MANA = 50
    MAX_HAND_SIZE = 7
    CARDS_PER_TURN = 1
    
    # Combat
    DAMAGE_MULTIPLIER_MIN = 0.8
    DAMAGE_MULTIPLIER_MAX = 1.2
    CRITICAL_CHANCE = 0.1
    CRITICAL_MULTIPLIER = 2.0
    
    # Egyptian Mechanics
    BA_KA_SEPARATION_COST = 25  # Mana cost to separate soul
    DIVINE_JUDGMENT_THRESHOLD = 50  # Moral alignment threshold
    RESURRECTION_COOLDOWN = 3  # Turns

# INPUT CONSTANTS
class Input:
    """Input handling constants."""
    
    # Mouse
    LEFT_CLICK = 1
    RIGHT_CLICK = 3
    MOUSE_WHEEL_UP = 4
    MOUSE_WHEEL_DOWN = 5
    
    # Keyboard shortcuts
    QUIT_KEYS = [pygame.K_ESCAPE]
    CONFIRM_KEYS = [pygame.K_RETURN, pygame.K_SPACE]
    MENU_KEYS = [pygame.K_TAB]
    
    # Gamepad (if implemented later)
    DEADZONE = 0.2

# FILE PATHS
class Paths:
    """File path constants."""
    
    import os
    from pathlib import Path
    
    # Project root
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
    
    # Asset directories
    ASSETS_DIR = PROJECT_ROOT / "assets"
    IMAGES_DIR = ASSETS_DIR / "images"
    AUDIO_DIR = ASSETS_DIR / "audio"
    FONTS_DIR = ASSETS_DIR / "fonts"
    
    # LORA training data
    LORA_DATASET = IMAGES_DIR / "lora_training" / "final_dataset"
    
    # Save data
    SAVE_DIR = PROJECT_ROOT / "save_games"
    CONFIG_DIR = PROJECT_ROOT / "config"
    
    # Logs
    LOG_DIR = PROJECT_ROOT / "logs"

# DEVELOPMENT CONSTANTS
class Dev:
    """Development and debug constants."""
    
    DEBUG_MODE = True
    SHOW_FPS = True
    SHOW_MEMORY_USAGE = False
    ENABLE_CHEATS = True
    
    # Debug Colors
    DEBUG_RED = (255, 0, 0, 128)
    DEBUG_GREEN = (0, 255, 0, 128)
    DEBUG_BLUE = (0, 0, 255, 128)
    
    # Performance Monitoring
    FRAME_TIME_SAMPLES = 60
    MEMORY_CHECK_INTERVAL = 5.0  # seconds