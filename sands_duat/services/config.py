"""
Configuration Management Service

Centralized configuration system with support for INI files,
environment variables, and runtime configuration updates.

Features:
- Type-safe configuration access
- Environment variable overrides
- Hot-reload capability
- Validation and defaults
"""

import configparser
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union, TypeVar, Type
from dataclasses import dataclass
import logging

T = TypeVar('T')


@dataclass
class DisplayConfig:
    """Display configuration settings."""
    default_width: int = 3440
    default_height: int = 1440
    target_fps: int = 60
    vsync: bool = True
    fullscreen: bool = False
    ultrawide_scale: float = 1.0
    widescreen_scale: float = 0.8
    standard_scale: float = 0.6
    compact_scale: float = 0.4


@dataclass
class TimingConfig:
    """Hour-Glass timing configuration."""
    sand_regeneration_rate: float = 1.0
    max_delta_clamp: float = 0.05
    timing_precision: float = 0.001
    debug_time_scale: float = 1.0


@dataclass
class PerformanceConfig:
    """Performance monitoring configuration."""
    min_fps_warning: int = 45
    max_memory_growth: float = 1.2
    sand_timing_error_threshold: int = 50


@dataclass
class DevelopmentConfig:
    """Development and debugging settings."""
    debug_mode: bool = False
    hot_reload: bool = True
    log_level: str = "INFO"
    auto_reload_content: bool = True
    performance_monitoring: bool = True


@dataclass
class ArtGenerationConfig:
    """Art generation pipeline settings."""
    batch_size: int = 2
    max_vram_usage: float = 0.8
    offload_to_cpu: bool = True
    default_resolution: str = "512x768"
    card_frame_size: str = "400x650"
    papyrus_overlay_opacity: float = 0.6


class ConfigManager:
    """
    Centralized configuration management with type safety and hot-reload.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("config/config.ini")
        self.config = configparser.ConfigParser()
        self._watchers = []
        
        # Configuration sections
        self.display = DisplayConfig()
        self.timing = TimingConfig()
        self.performance = PerformanceConfig()
        self.development = DevelopmentConfig()
        self.art_generation = ArtGenerationConfig()
        
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.reload()
    
    def reload(self) -> None:
        """Reload configuration from file and environment variables."""
        # Load from INI file
        if self.config_path.exists():
            self.config.read(self.config_path)
            self._apply_config()
        else:
            self.logger.warning(f"Config file not found: {self.config_path}")
            self._create_default_config()
        
        # Apply environment variable overrides
        self._apply_env_overrides()
        
        self.logger.info("Configuration reloaded")
    
    def _apply_config(self) -> None:
        """Apply loaded configuration to dataclass instances."""
        # Display configuration
        if 'display' in self.config:
            display_section = self.config['display']
            self.display.default_width = display_section.getint('default_width', 3440)
            self.display.default_height = display_section.getint('default_height', 1440)
            self.display.target_fps = display_section.getint('target_fps', 60)
            self.display.vsync = display_section.getboolean('vsync', True)
            self.display.fullscreen = display_section.getboolean('fullscreen', False)
            self.display.ultrawide_scale = display_section.getfloat('ultrawide_scale', 1.0)
            self.display.widescreen_scale = display_section.getfloat('widescreen_scale', 0.8)
            self.display.standard_scale = display_section.getfloat('standard_scale', 0.6)
            self.display.compact_scale = display_section.getfloat('compact_scale', 0.4)
        
        # Timing configuration
        if 'timing' in self.config:
            timing_section = self.config['timing']
            self.timing.sand_regeneration_rate = timing_section.getfloat('sand_regeneration_rate', 1.0)
            self.timing.max_delta_clamp = timing_section.getfloat('max_delta_clamp', 0.05)
            self.timing.timing_precision = timing_section.getfloat('timing_precision', 0.001)
            self.timing.debug_time_scale = timing_section.getfloat('debug_time_scale', 1.0)
        
        # Performance configuration
        if 'performance' in self.config:
            perf_section = self.config['performance']
            self.performance.min_fps_warning = perf_section.getint('min_fps_warning', 45)
            self.performance.max_memory_growth = perf_section.getfloat('max_memory_growth', 1.2)
            self.performance.sand_timing_error_threshold = perf_section.getint('sand_timing_error_threshold', 50)
        
        # Development configuration
        if 'development' in self.config:
            dev_section = self.config['development']
            self.development.debug_mode = dev_section.getboolean('debug_mode', False)
            self.development.hot_reload = dev_section.getboolean('hot_reload', True)
            self.development.log_level = dev_section.get('log_level', 'INFO')
            self.development.auto_reload_content = dev_section.getboolean('auto_reload_content', True)
            self.development.performance_monitoring = dev_section.getboolean('performance_monitoring', True)
        
        # Art generation configuration
        if 'art_generation' in self.config:
            art_section = self.config['art_generation']
            self.art_generation.batch_size = art_section.getint('batch_size', 2)
            self.art_generation.max_vram_usage = art_section.getfloat('max_vram_usage', 0.8)
            self.art_generation.offload_to_cpu = art_section.getboolean('offload_to_cpu', True)
            self.art_generation.default_resolution = art_section.get('default_resolution', '512x768')
            self.art_generation.card_frame_size = art_section.get('card_frame_size', '400x650')
            self.art_generation.papyrus_overlay_opacity = art_section.getfloat('papyrus_overlay_opacity', 0.6)
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Environment variables with SANDS_DUAT_ prefix
        env_mappings = {
            'SANDS_DUAT_DEBUG': ('development', 'debug_mode', bool),
            'SANDS_DUAT_LOG_LEVEL': ('development', 'log_level', str),
            'SANDS_DUAT_WIDTH': ('display', 'default_width', int),
            'SANDS_DUAT_HEIGHT': ('display', 'default_height', int),
            'SANDS_DUAT_FPS': ('display', 'target_fps', int),
            'SANDS_DUAT_SAND_RATE': ('timing', 'sand_regeneration_rate', float),
            'SANDS_DUAT_TIME_SCALE': ('timing', 'debug_time_scale', float),
        }
        
        for env_var, (section, key, type_func) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    if type_func == bool:
                        parsed_value = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        parsed_value = type_func(value)
                    
                    # Apply to appropriate configuration section
                    config_section = getattr(self, section)
                    setattr(config_section, key, parsed_value)
                    
                    self.logger.info(f"Applied environment override: {env_var}={parsed_value}")
                    
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Invalid environment variable {env_var}={value}: {e}")
    
    def _create_default_config(self) -> None:
        """Create a default configuration file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        default_config = """[paths]
models_dir = models/
content_dir = sands_duat/content/
assets_dir = sands_duat/assets/
temp_dir = temp/
logs_dir = logs/

[display]
default_width = 3440
default_height = 1440
target_fps = 60
vsync = true
fullscreen = false
ultrawide_scale = 1.0
widescreen_scale = 0.8
standard_scale = 0.6
compact_scale = 0.4

[timing]
sand_regeneration_rate = 1.0
max_delta_clamp = 0.05
timing_precision = 0.001
debug_time_scale = 1.0

[performance]
min_fps_warning = 45
max_memory_growth = 1.2
sand_timing_error_threshold = 50

[development]
debug_mode = false
hot_reload = true
log_level = INFO
auto_reload_content = true
performance_monitoring = true

[art_generation]
batch_size = 2
max_vram_usage = 0.8
offload_to_cpu = true
default_resolution = 512x768
card_frame_size = 400x650
papyrus_overlay_opacity = 0.6
"""
        
        self.config_path.write_text(default_config)
        self.logger.info(f"Created default config: {self.config_path}")
        
        # Reload to apply the new configuration
        self.config.read(self.config_path)
        self._apply_config()
    
    def get(self, section: str, key: str, default: T = None, type_func: Type[T] = str) -> T:
        """Get a configuration value with type conversion."""
        try:
            if section in self.config and key in self.config[section]:
                value = self.config[section][key]
                if type_func == bool:
                    return self.config[section].getboolean(key)
                elif type_func == int:
                    return self.config[section].getint(key)
                elif type_func == float:
                    return self.config[section].getfloat(key)
                else:
                    return type_func(value)
            return default
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Error parsing config {section}.{key}: {e}")
            return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set a configuration value."""
        if section not in self.config:
            self.config.add_section(section)
        
        self.config[section][key] = str(value)
        self.logger.debug(f"Config updated: {section}.{key} = {value}")
    
    def save(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            'display': self.display.__dict__,
            'timing': self.timing.__dict__,
            'performance': self.performance.__dict__,
            'development': self.development.__dict__,
            'art_generation': self.art_generation.__dict__
        }


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get the global configuration manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def init_config(config_path: Optional[Path] = None) -> ConfigManager:
    """Initialize the global configuration manager."""
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager