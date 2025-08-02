"""
Services Layer

External integrations and utilities for Sands of Duat,
providing clean interfaces for persistence, logging, telemetry,
and configuration management.

Services:
- save_load.py: Game state persistence
- logging.py: Centralized logging system
- telemetry.py: Performance monitoring and metrics
- config.py: Configuration management
"""

from .config import ConfigManager, get_config
from .logging import setup_logging, get_logger
from .telemetry import PerformanceMonitor, get_performance_monitor
from .save_load import SaveLoadManager, get_save_manager

__all__ = [
    'ConfigManager',
    'get_config',
    'setup_logging',
    'get_logger',
    'PerformanceMonitor',
    'get_performance_monitor',
    'SaveLoadManager',
    'get_save_manager'
]