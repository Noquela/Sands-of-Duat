"""
Core Engine Systems

This module contains the comprehensive Hour-Glass Initiative system for Sands of Duat:

- HourGlass System: Real-time sand regeneration with 50ms timing accuracy
- Enhanced Combat Engine: Sand-based action scheduling and queue management
- Enemy AI: Strategic sand management and adaptive decision making
- Visual Feedback: Real-time sand level indicators and regeneration progress
- Animation Coordination: Synchronized animations with sand regeneration pausing
- Pygame Integration: Seamless integration with game loop and input handling
- Debug & Monitoring: Comprehensive timing analysis and performance profiling

The complete system provides frame-rate independent timing, visual feedback,
and strategic depth through the innovative Hour-Glass Initiative mechanics.
"""

from .hourglass import HourGlass, SandTimer, TimingAccuracy
from .combat import CombatEngine, ActionQueue, ActionType, CombatPhase
from .combat_enhanced import EnhancedCombatEngine, EnhancedCombatAction, ActionPriority
from .sand_visuals import SandVisualizer, HourGlassWidget, VisualTheme, sand_visualizer
from .animation_coordinator import AnimationCoordinator, AnimationType, animation_coordinator
from .enemy_ai import EnemyAI, EnemyAIManager, AIDifficultyLevel, SandStrategy, enemy_ai_manager
from .pygame_integration import PygameHourGlassManager, RenderQuality
from .debug_logger import HourGlassLogger, debug_logger, DebugCategory
from .ecs import Entity, Component, System
from .cards import Card, CardEffect, Deck
from .engine import GameEngine, GameState

__all__ = [
    # Core Hour-Glass Initiative System
    'HourGlass', 'SandTimer', 'TimingAccuracy',
    
    # Combat Systems
    'CombatEngine', 'ActionQueue', 'ActionType', 'CombatPhase',
    'EnhancedCombatEngine', 'EnhancedCombatAction', 'ActionPriority',
    
    # Visual & Animation Systems
    'SandVisualizer', 'HourGlassWidget', 'VisualTheme', 'sand_visualizer',
    'AnimationCoordinator', 'AnimationType', 'animation_coordinator',
    
    # AI System
    'EnemyAI', 'EnemyAIManager', 'AIDifficultyLevel', 'SandStrategy', 'enemy_ai_manager',
    
    # Integration & Tools
    'PygameHourGlassManager', 'RenderQuality',
    'HourGlassLogger', 'debug_logger', 'DebugCategory',
    
    # Base Systems
    'Entity', 'Component', 'System',
    'Card', 'CardEffect', 'Deck',
    'GameEngine', 'GameState'
]