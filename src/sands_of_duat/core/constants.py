"""
Core constants for the Egyptian card game.
Defines colors, dimensions, timing, and Egyptian-themed values.
"""

import pygame
from typing import Tuple, Dict, Any

# SCREEN DIMENSIONS (Golden Ratio for Egyptian Aesthetic)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

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
    """UI layout and spacing constants."""
    
    # Margins and Padding
    SCREEN_MARGIN = 20
    COMPONENT_PADDING = 10
    BUTTON_PADDING = 15
    CARD_SPACING = 8
    
    # Component Sizes
    BUTTON_HEIGHT = 60
    BUTTON_WIDTH_STANDARD = 200
    BUTTON_WIDTH_WIDE = 300
    
    # Card Dimensions
    CARD_WIDTH = 120
    CARD_HEIGHT = 180
    CARD_SCALE_HOVER = 1.1
    CARD_SCALE_SELECTED = 1.05
    
    # Health/Mana Bar
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    BAR_BORDER = 2

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

# FONT SIZES
class FontSizes:
    """Font size constants for different UI elements."""
    
    TITLE_HUGE = 72
    TITLE_LARGE = 48
    TITLE_MEDIUM = 36
    SUBTITLE = 28
    BUTTON = 24
    BODY = 20
    CARD_NAME = 18
    CARD_TEXT = 14
    TOOLTIP = 16
    DEBUG = 12

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