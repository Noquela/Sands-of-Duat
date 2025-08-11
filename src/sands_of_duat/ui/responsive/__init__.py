"""
Responsive UI System - Ultrawide and 4K display support.
"""

from .ultrawide_layout import ultrawide_layout, UltraWideLayout
from .scaling_manager import scaling_manager, ScalingManager

__all__ = [
    'ultrawide_layout',
    'UltraWideLayout', 
    'scaling_manager',
    'ScalingManager'
]