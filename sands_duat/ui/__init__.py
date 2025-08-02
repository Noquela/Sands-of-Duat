"""
User Interface System

Pygame-based UI system for Sands of Duat, featuring Hour-Glass Initiative
visualizations, card interactions, and Egyptian-themed interface design.

Key Features:
- Real-time sand gauge visualization
- Interactive card hand and battlefield
- Combat interface with timing mechanics
- Map navigation and progression
- Deck building and collection management

Components:
- combat_screen.py: Main battle interface
- map_screen.py: Node progression and path selection
- deck_builder.py: Card collection management
- menu_screen.py: Main menu and settings
- components/: Reusable UI components

The UI system is designed to clearly communicate the unique Hour-Glass
Initiative mechanics while maintaining visual appeal and usability.
"""

# Import only the base classes to avoid circular import issues
from .base import UIScreen, UIComponent, UIManager

# Screen classes will be imported on-demand to avoid relative import issues
__all__ = [
    'UIScreen',
    'UIComponent', 
    'UIManager'
]

# Delayed import functions to avoid relative import issues
def get_menu_screen():
    from .menu_screen import MenuScreen
    return MenuScreen

def get_combat_screen():
    from .combat_screen import CombatScreen
    return CombatScreen

def get_map_screen():
    from .map_screen import MapScreen
    return MapScreen

def get_deck_builder_screen():
    from .deck_builder import DeckBuilderScreen
    return DeckBuilderScreen