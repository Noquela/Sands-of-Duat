"""
Settings Manager - SPRINT 7: Complete Settings & Options System
Handles all game settings with persistence and Egyptian theming.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum, auto

class GraphicsQuality(Enum):
    """Graphics quality presets."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    ULTRA = auto()

class AnimationSpeed(Enum):
    """Animation speed options."""
    SLOW = auto()
    NORMAL = auto()
    FAST = auto()

@dataclass
class GraphicsSettings:
    """Graphics-related settings."""
    resolution_width: int = 1920
    resolution_height: int = 1080
    fullscreen: bool = False
    vsync: bool = True
    quality: GraphicsQuality = GraphicsQuality.HIGH
    show_fps: bool = False
    ultrawide_support: bool = True

@dataclass
class AudioSettings:
    """Audio-related settings."""
    master_volume: float = 0.7
    music_volume: float = 0.6
    sfx_volume: float = 0.8
    ambient_volume: float = 0.4
    mute_all: bool = False

@dataclass
class GameplaySettings:
    """Gameplay-related settings."""
    auto_end_turn: bool = False
    animation_speed: AnimationSpeed = AnimationSpeed.NORMAL
    show_tooltips: bool = True
    confirm_actions: bool = True
    skip_animations: bool = False
    auto_save: bool = True

@dataclass
class KeyBindings:
    """Keybinding settings."""
    end_turn: str = "Space"
    cancel_action: str = "Escape"
    deck_builder: str = "D"
    settings: str = "S"
    fullscreen: str = "F11"
    screenshot: str = "F12"

class SettingsManager:
    """
    Comprehensive settings manager for Sands of Duat.
    Handles persistence, validation, and Egyptian-themed organization.
    """
    
    def __init__(self):
        """Initialize settings manager."""
        # Settings file path
        self.settings_dir = Path.home() / ".sands_of_duat"
        self.settings_file = self.settings_dir / "settings.json"
        
        # Default settings
        self.graphics = GraphicsSettings()
        self.audio = AudioSettings()
        self.gameplay = GameplaySettings()
        self.keybindings = KeyBindings()
        
        # Create settings directory if needed
        self.settings_dir.mkdir(exist_ok=True)
        
        # Load existing settings
        self.load_settings()
        
        print("Settings Manager initialized - Temple configurations ready")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as a dictionary."""
        return {
            "graphics": asdict(self.graphics),
            "audio": asdict(self.audio),
            "gameplay": asdict(self.gameplay),
            "keybindings": asdict(self.keybindings)
        }
    
    def save_settings(self) -> bool:
        """Save all settings to file."""
        try:
            settings_data = self.get_all_settings()
            
            # Convert enums to strings for JSON serialization
            settings_data["graphics"]["quality"] = self.graphics.quality.name
            settings_data["gameplay"]["animation_speed"] = self.gameplay.animation_speed.name
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings_data, f, indent=2)
            
            print(f"Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    def load_settings(self) -> bool:
        """Load settings from file."""
        try:
            if not self.settings_file.exists():
                print("No settings file found, using defaults")
                return False
            
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
            
            # Load graphics settings
            if "graphics" in data:
                g = data["graphics"]
                self.graphics.resolution_width = g.get("resolution_width", 1920)
                self.graphics.resolution_height = g.get("resolution_height", 1080)
                self.graphics.fullscreen = g.get("fullscreen", False)
                self.graphics.vsync = g.get("vsync", True)
                self.graphics.show_fps = g.get("show_fps", False)
                self.graphics.ultrawide_support = g.get("ultrawide_support", True)
                
                # Handle enum conversion
                quality_name = g.get("quality", "HIGH")
                try:
                    self.graphics.quality = GraphicsQuality[quality_name]
                except KeyError:
                    self.graphics.quality = GraphicsQuality.HIGH
            
            # Load audio settings
            if "audio" in data:
                a = data["audio"]
                self.audio.master_volume = a.get("master_volume", 0.7)
                self.audio.music_volume = a.get("music_volume", 0.6)
                self.audio.sfx_volume = a.get("sfx_volume", 0.8)
                self.audio.ambient_volume = a.get("ambient_volume", 0.4)
                self.audio.mute_all = a.get("mute_all", False)
            
            # Load gameplay settings
            if "gameplay" in data:
                gp = data["gameplay"]
                self.gameplay.auto_end_turn = gp.get("auto_end_turn", False)
                self.gameplay.show_tooltips = gp.get("show_tooltips", True)
                self.gameplay.confirm_actions = gp.get("confirm_actions", True)
                self.gameplay.skip_animations = gp.get("skip_animations", False)
                self.gameplay.auto_save = gp.get("auto_save", True)
                
                # Handle enum conversion
                speed_name = gp.get("animation_speed", "NORMAL")
                try:
                    self.gameplay.animation_speed = AnimationSpeed[speed_name]
                except KeyError:
                    self.gameplay.animation_speed = AnimationSpeed.NORMAL
            
            # Load keybindings
            if "keybindings" in data:
                kb = data["keybindings"]
                self.keybindings.end_turn = kb.get("end_turn", "Space")
                self.keybindings.cancel_action = kb.get("cancel_action", "Escape")
                self.keybindings.deck_builder = kb.get("deck_builder", "D")
                self.keybindings.settings = kb.get("settings", "S")
                self.keybindings.fullscreen = kb.get("fullscreen", "F11")
                self.keybindings.screenshot = kb.get("screenshot", "F12")
            
            print("Settings loaded successfully")
            return True
            
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.graphics = GraphicsSettings()
        self.audio = AudioSettings()
        self.gameplay = GameplaySettings()
        self.keybindings = KeyBindings()
        print("Settings reset to defaults")
    
    def get_resolution_options(self) -> list:
        """Get available resolution options."""
        return [
            (1280, 720),   # HD
            (1920, 1080),  # Full HD
            (2560, 1440),  # QHD
            (3440, 1440),  # Ultrawide QHD
            (3840, 2160),  # 4K
        ]
    
    def get_quality_description(self, quality: GraphicsQuality) -> str:
        """Get description for graphics quality setting."""
        descriptions = {
            GraphicsQuality.LOW: "Basic graphics for older hardware",
            GraphicsQuality.MEDIUM: "Balanced performance and visuals",
            GraphicsQuality.HIGH: "Enhanced visuals with good performance",
            GraphicsQuality.ULTRA: "Maximum visual fidelity"
        }
        return descriptions.get(quality, "Unknown quality level")
    
    def validate_settings(self) -> bool:
        """Validate current settings for consistency."""
        # Validate volume ranges
        volumes = [
            self.audio.master_volume,
            self.audio.music_volume,
            self.audio.sfx_volume,
            self.audio.ambient_volume
        ]
        
        for vol in volumes:
            if not (0.0 <= vol <= 1.0):
                print(f"Invalid volume value: {vol}")
                return False
        
        # Validate resolution
        if self.graphics.resolution_width < 800 or self.graphics.resolution_height < 600:
            print(f"Invalid resolution: {self.graphics.resolution_width}x{self.graphics.resolution_height}")
            return False
        
        return True
    
    def apply_graphics_settings(self, game_engine):
        """Apply graphics settings to the game engine."""
        try:
            import pygame
            
            # Set resolution
            if self.graphics.fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                size = (self.graphics.resolution_width, self.graphics.resolution_height)
                screen = pygame.display.set_mode(size)
            
            # Update engine screen reference
            game_engine.screen = screen
            
            # Apply VSync (if supported)
            if hasattr(pygame, 'DOUBLEBUF') and self.graphics.vsync:
                pygame.display.set_mode(screen.get_size(), pygame.DOUBLEBUF)
            
            print(f"Graphics settings applied: {self.graphics.resolution_width}x{self.graphics.resolution_height}")
            return True
            
        except Exception as e:
            print(f"Failed to apply graphics settings: {e}")
            return False
    
    def apply_audio_settings(self, audio_manager):
        """Apply audio settings to the audio manager."""
        try:
            audio_manager.set_master_volume(self.audio.master_volume)
            audio_manager.set_music_volume(self.audio.music_volume)
            audio_manager.set_sfx_volume(self.audio.sfx_volume)
            audio_manager.set_ambient_volume(self.audio.ambient_volume)
            
            print("Audio settings applied successfully")
            return True
            
        except Exception as e:
            print(f"Failed to apply audio settings: {e}")
            return False
    
    def get_settings_categories(self) -> Dict[str, str]:
        """Get Egyptian-themed settings categories."""
        return {
            "graphics": "Temple Visuals",
            "audio": "Sacred Sounds", 
            "gameplay": "Divine Gameplay",
            "keybindings": "Sacred Bindings"
        }

# Global settings manager instance
settings_manager = SettingsManager()