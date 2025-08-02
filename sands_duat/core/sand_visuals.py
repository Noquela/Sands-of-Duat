"""
Sand Visual Feedback System

Provides visual feedback for sand levels, regeneration timing, and
Hour-Glass Initiative state for both player and enemy hourglasses.

Key Features:
- Real-time sand level indicators
- Regeneration progress visualization
- Animation-aware visual states
- Enemy sand tracking display
- Color-coded sand availability

Classes:
- SandVisualizer: Main visual feedback coordinator
- SandDisplayElement: Individual sand grain visual representation
- RegenerationIndicator: Progress bar for sand regeneration
- HourGlassWidget: Complete hourglass UI component
"""

import time
import math
from typing import Optional, List, Tuple, Dict, Any, Callable
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass

from .hourglass import HourGlass, TimingAccuracy


class SandState(Enum):
    """Visual states for sand grains."""
    EMPTY = "empty"
    FILLING = "filling"
    FULL = "full"
    SPENDING = "spending"
    REGENERATING = "regenerating"


class VisualTheme(Enum):
    """Visual themes for sand display."""
    DESERT = "desert"
    MYSTICAL = "mystical"
    MINIMALIST = "minimalist"
    COMBAT = "combat"


@dataclass
class ColorScheme:
    """Color scheme for sand visualization."""
    empty: Tuple[int, int, int] = (60, 60, 60)        # Dark gray
    full: Tuple[int, int, int] = (255, 215, 0)        # Gold
    regenerating: Tuple[int, int, int] = (255, 255, 150)  # Light yellow
    spending: Tuple[int, int, int] = (255, 100, 100)  # Red
    background: Tuple[int, int, int] = (40, 40, 40)   # Very dark gray
    border: Tuple[int, int, int] = (100, 100, 100)    # Medium gray
    progress_bg: Tuple[int, int, int] = (80, 80, 80)  # Dark gray
    progress_fill: Tuple[int, int, int] = (0, 255, 0) # Green


class SandDisplayElement(BaseModel):
    """Individual sand grain visual representation."""
    
    index: int = Field(description="Grain index (0-5)")
    state: SandState = Field(default=SandState.EMPTY)
    animation_progress: float = Field(default=0.0, ge=0.0, le=1.0)
    last_state_change: float = Field(default_factory=time.time)
    animation_duration: float = Field(default=0.3, description="Animation duration in seconds")
    
    def update_state(self, new_state: SandState) -> None:
        """Update the visual state with animation."""
        if new_state != self.state:
            self.state = new_state
            self.animation_progress = 0.0
            self.last_state_change = time.time()
    
    def update_animation(self) -> None:
        """Update animation progress."""
        if self.animation_progress < 1.0:
            elapsed = time.time() - self.last_state_change
            self.animation_progress = min(1.0, elapsed / self.animation_duration)
    
    def get_visual_alpha(self) -> float:
        """Get alpha value for visual effects."""
        if self.state == SandState.FILLING:
            return self.animation_progress
        elif self.state == SandState.SPENDING:
            return 1.0 - self.animation_progress
        elif self.state == SandState.REGENERATING:
            # Pulse effect
            pulse = math.sin(time.time() * 4) * 0.3 + 0.7
            return pulse * self.animation_progress
        return 1.0
    
    def is_animation_complete(self) -> bool:
        """Check if current animation is complete."""
        return self.animation_progress >= 1.0


class RegenerationIndicator(BaseModel):
    """Progress indicator for sand regeneration timing."""
    
    progress: float = Field(default=0.0, ge=0.0, le=1.0)
    time_remaining: float = Field(default=0.0, ge=0.0)
    is_visible: bool = Field(default=True)
    pulse_phase: float = Field(default=0.0)
    
    def update(self, hourglass: HourGlass) -> None:
        """Update progress based on hourglass state."""
        if hourglass.current_sand >= hourglass.max_sand or hourglass.timer.is_paused:
            self.is_visible = False
            return
        
        self.is_visible = True
        self.progress = hourglass.get_sand_progress()
        self.time_remaining = hourglass.get_time_until_next_sand()
        
        # Update pulse animation
        self.pulse_phase = (time.time() * 2) % (2 * math.pi)
    
    def get_pulse_intensity(self) -> float:
        """Get pulsing intensity for visual feedback."""
        return math.sin(self.pulse_phase) * 0.2 + 0.8


class HourGlassWidget(BaseModel):
    """Complete hourglass UI component with visual feedback."""
    
    hourglass: HourGlass = Field(description="Associated hourglass instance")
    sand_elements: List[SandDisplayElement] = Field(default_factory=list)
    regen_indicator: RegenerationIndicator = Field(default_factory=RegenerationIndicator)
    theme: VisualTheme = Field(default=VisualTheme.DESERT)
    color_scheme: ColorScheme = Field(default_factory=ColorScheme)
    is_enemy: bool = Field(default=False, description="Whether this is an enemy hourglass")
    show_exact_timing: bool = Field(default=True, description="Show precise timing information")
    animation_speed_multiplier: float = Field(default=1.0, description="Animation speed modifier")
    
    def __init__(self, **data):
        super().__init__(**data)
        self._initialize_sand_elements()
    
    def _initialize_sand_elements(self) -> None:
        """Initialize sand grain visual elements."""
        self.sand_elements = [
            SandDisplayElement(index=i) for i in range(self.hourglass.max_sand)
        ]
    
    def update(self) -> None:
        """Update all visual elements."""
        # Update sand grain visuals
        for i, element in enumerate(self.sand_elements):
            if i < self.hourglass.current_sand:
                element.update_state(SandState.FULL)
            else:
                # Check if this grain is currently regenerating
                progress = self.hourglass.get_sand_progress()
                if i == self.hourglass.current_sand and progress > 0:
                    element.update_state(SandState.REGENERATING)
                else:
                    element.update_state(SandState.EMPTY)
            
            element.update_animation()
        
        # Update regeneration indicator
        self.regen_indicator.update(self.hourglass)
    
    def spend_sand_visual(self, amount: int) -> None:
        """Trigger spending animation for specified amount."""
        for i in range(amount):
            sand_index = self.hourglass.current_sand + i
            if sand_index < len(self.sand_elements):
                self.sand_elements[sand_index].update_state(SandState.SPENDING)
    
    def get_display_data(self) -> Dict[str, Any]:
        """Get all data needed for rendering the hourglass."""
        return {
            'sand_count': self.hourglass.current_sand,
            'max_sand': self.hourglass.max_sand,
            'sand_elements': [
                {
                    'index': elem.index,
                    'state': elem.state.value,
                    'alpha': elem.get_visual_alpha(),
                    'animation_complete': elem.is_animation_complete()
                }
                for elem in self.sand_elements
            ],
            'regeneration': {
                'progress': self.regen_indicator.progress,
                'time_remaining': self.regen_indicator.time_remaining,
                'is_visible': self.regen_indicator.is_visible,
                'pulse_intensity': self.regen_indicator.get_pulse_intensity()
            },
            'theme': self.theme.value,
            'is_enemy': self.is_enemy,
            'is_paused': self.hourglass.timer.is_paused,
            'color_scheme': {
                'empty': self.color_scheme.empty,
                'full': self.color_scheme.full,
                'regenerating': self.color_scheme.regenerating,
                'spending': self.color_scheme.spending,
                'background': self.color_scheme.background,
                'border': self.color_scheme.border,
                'progress_bg': self.color_scheme.progress_bg,
                'progress_fill': self.color_scheme.progress_fill
            }
        }
    
    def set_theme(self, theme: VisualTheme) -> None:
        """Change the visual theme."""
        self.theme = theme
        
        # Apply theme-specific color schemes
        if theme == VisualTheme.DESERT:
            self.color_scheme = ColorScheme(
                full=(255, 215, 0),      # Gold
                regenerating=(255, 255, 150),
                spending=(255, 140, 0)   # Dark orange
            )
        elif theme == VisualTheme.MYSTICAL:
            self.color_scheme = ColorScheme(
                full=(138, 43, 226),     # Blue violet
                regenerating=(200, 150, 255),
                spending=(255, 0, 255)   # Magenta
            )
        elif theme == VisualTheme.COMBAT:
            self.color_scheme = ColorScheme(
                full=(255, 0, 0),        # Red
                regenerating=(255, 100, 100),
                spending=(255, 255, 0)   # Yellow
            )
        elif theme == VisualTheme.MINIMALIST:
            self.color_scheme = ColorScheme(
                full=(255, 255, 255),    # White
                regenerating=(200, 200, 200),
                spending=(128, 128, 128) # Gray
            )
    
    def set_enemy_display(self, is_enemy: bool) -> None:
        """Configure display for enemy hourglass."""
        self.is_enemy = is_enemy
        if is_enemy:
            # Enemy hourglasses have different visual styling
            self.show_exact_timing = False  # Hide precise timing from player
            self.set_theme(VisualTheme.COMBAT)
    
    def get_cost_indicator(self, sand_cost: int) -> Dict[str, Any]:
        """Get visual feedback for a potential sand cost."""
        can_afford = self.hourglass.can_afford(sand_cost)
        
        affected_grains = []
        for i in range(sand_cost):
            grain_index = self.hourglass.current_sand - 1 - i
            if grain_index >= 0:
                affected_grains.append({
                    'index': grain_index,
                    'can_afford': True
                })
            else:
                affected_grains.append({
                    'index': abs(grain_index) - 1,
                    'can_afford': False
                })
        
        return {
            'cost': sand_cost,
            'can_afford': can_afford,
            'affected_grains': affected_grains,
            'color': self.color_scheme.full if can_afford else self.color_scheme.spending
        }


class SandVisualizer:
    """
    Main coordinator for sand visual feedback system.
    
    Manages multiple hourglass widgets and provides unified
    visual feedback for the Hour-Glass Initiative system.
    """
    
    def __init__(self):
        self.widgets: Dict[str, HourGlassWidget] = {}
        self.global_theme = VisualTheme.DESERT
        self.animation_enabled = True
        self.debug_overlay = False
        
    def register_hourglass(self, entity_id: str, hourglass: HourGlass, is_enemy: bool = False) -> HourGlassWidget:
        """Register a hourglass for visual tracking."""
        widget = HourGlassWidget(
            hourglass=hourglass,
            theme=self.global_theme,
            is_enemy=is_enemy
        )
        widget.set_enemy_display(is_enemy)
        self.widgets[entity_id] = widget
        return widget
    
    def unregister_hourglass(self, entity_id: str) -> None:
        """Remove hourglass from visual tracking."""
        if entity_id in self.widgets:
            del self.widgets[entity_id]
    
    def update_all(self) -> None:
        """Update all registered hourglass widgets."""
        for widget in self.widgets.values():
            widget.update()
    
    def get_widget(self, entity_id: str) -> Optional[HourGlassWidget]:
        """Get widget for specific entity."""
        return self.widgets.get(entity_id)
    
    def set_global_theme(self, theme: VisualTheme) -> None:
        """Set theme for all widgets."""
        self.global_theme = theme
        for widget in self.widgets.values():
            if not widget.is_enemy:  # Keep enemy themes separate
                widget.set_theme(theme)
    
    def trigger_sand_spending(self, entity_id: str, amount: int) -> None:
        """Trigger visual spending animation."""
        widget = self.widgets.get(entity_id)
        if widget:
            widget.spend_sand_visual(amount)
    
    def get_all_display_data(self) -> Dict[str, Dict[str, Any]]:
        """Get display data for all widgets."""
        return {
            entity_id: widget.get_display_data()
            for entity_id, widget in self.widgets.items()
        }
    
    def enable_debug_overlay(self) -> None:
        """Enable debug information overlay."""
        self.debug_overlay = True
    
    def disable_debug_overlay(self) -> None:
        """Disable debug information overlay."""
        self.debug_overlay = False
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information for all hourglasses."""
        if not self.debug_overlay:
            return {}
        
        debug_data = {}
        for entity_id, widget in self.widgets.items():
            debug_data[entity_id] = {
                'status': widget.hourglass.get_regeneration_status(),
                'visual_state': {
                    'theme': widget.theme.value,
                    'animation_elements': len([e for e in widget.sand_elements if not e.is_animation_complete()]),
                    'regen_visible': widget.regen_indicator.is_visible
                }
            }
        
        return debug_data


# Global sand visualizer instance
sand_visualizer = SandVisualizer()