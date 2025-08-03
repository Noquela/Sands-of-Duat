# Technical Implementation Guide: UI Improvements
*Generated: August 2, 2025*

## Overview

This guide provides specific code changes and implementation steps to address the "weird" feeling in the Sands of Duat interface. All changes are designed to work with the existing architecture while providing immediate visual and UX improvements.

## Phase 1: Immediate Layout & Color Improvements

### 1. Update Theme Colors (theme.py)

**File: `sands_duat/ui/theme.py`**

Replace the current `EgyptianColors` class:

```python
class EgyptianColors:
    """Improved Egyptian-themed color palette."""
    
    # Background colors
    SANDSTONE_BG = (230, 215, 197)         # Warm sandstone background
    PAPYRUS_LIGHT = (245, 241, 232)        # Light papyrus for cards
    PAPYRUS_DARK = (212, 197, 169)         # Darker papyrus for sections
    TOMB_SHADOW = (101, 67, 33)            # Deep shadow areas
    
    # Primary theme colors
    EGYPTIAN_GOLD = (255, 215, 0)          # Primary accent
    BRONZE_FRAME = (205, 127, 50)          # Borders and frames
    COPPER_ACCENT = (184, 115, 51)         # Interactive elements
    
    # Status colors
    HEALTH_RED = (204, 85, 0)              # Health indicators
    SAND_BLUE = (70, 130, 180)             # Sand/mana effects
    SAGE_GREEN = (135, 169, 107)           # Positive effects
    
    # Text colors
    HIEROGLYPH_BLACK = (47, 27, 20)        # Primary text
    BRONZE_TEXT = (139, 69, 19)            # Secondary text
    GOLD_TEXT = (184, 134, 11)             # Emphasis text
    
    # UI states
    HOVER = (255, 235, 205)                # Hover backgrounds
    PRESSED = (194, 154, 108)              # Pressed state
    DISABLED = (169, 169, 169)             # Disabled elements
    
    # Legacy compatibility
    background = SANDSTONE_BG
    PAPYRUS = HIEROGLYPH_BLACK
    GOLD = EGYPTIAN_GOLD
    BRONZE = BRONZE_FRAME
    DEEP_BROWN = PAPYRUS_DARK
    VERY_DARK = SANDSTONE_BG  # No more dark backgrounds
```

### 2. Improve Layout Zones (theme.py)

**Update the layout zone functions:**

```python
def _get_standard_layout(self) -> Dict[str, LayoutZone]:
    """Improved layout for 1920x1080 displays."""
    return {
        # Top status bar
        'status_bar': LayoutZone(0, 0, 1920, 60),
        
        # Main game areas (better proportioned)
        'player_zone': LayoutZone(20, 80, 360, 520),           # Left player area
        'combat_zone': LayoutZone(400, 120, 1120, 400),        # Center battlefield
        'enemy_zone': LayoutZone(1540, 80, 360, 520),          # Right enemy area
        
        # Bottom action area
        'hand_zone': LayoutZone(60, 620, 1800, 180),           # Hand cards
        'action_zone': LayoutZone(1620, 820, 280, 80),         # End turn button
        
        # Sub-zones for detailed positioning
        'player_health': LayoutZone(40, 100, 320, 60),
        'player_sand': LayoutZone(40, 180, 320, 120),
        'player_effects': LayoutZone(40, 320, 320, 180),
        
        'enemy_health': LayoutZone(1560, 100, 320, 60),
        'enemy_intent': LayoutZone(1560, 180, 320, 80),
        'enemy_effects': LayoutZone(1560, 280, 320, 140),
        
        'battlefield_center': LayoutZone(760, 240, 400, 240),
        'turn_indicator': LayoutZone(760, 140, 400, 60),
    }
```

### 3. Create Enhanced Card Component

**File: `sands_duat/ui/card_component.py` (new file)**

```python
"""Enhanced Card UI Component with Egyptian styling."""

import pygame
import math
from typing import Tuple, Optional
from .base import UIComponent
from .theme import get_theme
from core.cards import Card

class CardComponent(UIComponent):
    """Enhanced card component with Egyptian papyrus styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, card: Card):
        super().__init__(x, y, width, height)
        self.card = card
        self.theme = get_theme()
        
        # Visual state
        self.hover_elevation = 0.0
        self.target_elevation = 0.0
        self.glow_intensity = 0.0
        
        # Papyrus shape calculations
        self.corner_radius = min(width, height) // 8
        self.papyrus_points = self._calculate_papyrus_shape()
        
        # Pre-render text surfaces
        self._render_text_surfaces()
    
    def _calculate_papyrus_shape(self) -> List[Tuple[int, int]]:
        """Calculate points for papyrus scroll shape."""
        w, h = self.rect.width, self.rect.height
        x, y = self.rect.x, self.rect.y
        
        # Create papyrus scroll outline
        points = [
            (x + w//8, y),                    # Top left curve start
            (x + w - w//8, y),                # Top right curve start
            (x + w, y + h//6),                # Top right curve end
            (x + w, y + h - h//6),            # Bottom right curve start
            (x + w - w//8, y + h),            # Bottom right curve end
            (x + w//8, y + h),                # Bottom left curve end
            (x, y + h - h//6),                # Bottom left curve start
            (x, y + h//6),                    # Top left curve end
        ]
        return points
    
    def _render_text_surfaces(self):
        """Pre-render text for better performance."""
        theme = self.theme
        
        # Card title
        self.title_surface = theme.fonts.render_text(
            self.card.name, 'medium', theme.colors.HIEROGLYPH_BLACK
        )
        
        # Card cost
        self.cost_surface = theme.fonts.render_text(
            str(self.card.cost), 'large', theme.colors.EGYPTIAN_GOLD
        )
        
        # Card description (wrapped)
        self.desc_lines = self._wrap_text(
            self.card.description, theme.fonts.get_font('small'), 
            self.rect.width - 40
        )
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[pygame.Surface]:
        """Wrap text to fit within specified width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    line_surface = font.render(' '.join(current_line), True, self.theme.colors.BRONZE_TEXT)
                    lines.append(line_surface)
                current_line = [word]
        
        if current_line:
            line_surface = font.render(' '.join(current_line), True, self.theme.colors.BRONZE_TEXT)
            lines.append(line_surface)
        
        return lines
    
    def update(self, delta_time: float):
        """Update card animations."""
        # Smooth hover elevation
        elevation_speed = 8.0
        diff = self.target_elevation - self.hover_elevation
        self.hover_elevation += diff * elevation_speed * delta_time
        
        # Update glow for hover state
        if self.hovered:
            self.glow_intensity = min(1.0, self.glow_intensity + 4.0 * delta_time)
            self.target_elevation = 8.0
        else:
            self.glow_intensity = max(0.0, self.glow_intensity - 4.0 * delta_time)
            self.target_elevation = 0.0
    
    def render(self, surface: pygame.Surface):
        """Render the papyrus-styled card."""
        if not self.visible:
            return
        
        # Calculate render position with elevation
        render_rect = self.rect.copy()
        render_rect.y -= int(self.hover_elevation)
        
        # Draw shadow first
        if self.hover_elevation > 0:
            shadow_rect = render_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.polygon(shadow_surface, (0, 0, 0, 60), 
                               [(p[0] - render_rect.x + 4, p[1] - render_rect.y + 4) for p in self.papyrus_points])
            surface.blit(shadow_surface, shadow_rect)
        
        # Draw papyrus background
        papyrus_color = self.theme.colors.PAPYRUS_LIGHT
        if self.hovered:
            # Brighten on hover
            papyrus_color = tuple(min(255, c + 20) for c in papyrus_color)
        
        pygame.draw.polygon(surface, papyrus_color, 
                           [(p[0], p[1] - int(self.hover_elevation)) for p in self.papyrus_points])
        
        # Draw border
        border_color = self.theme.colors.BRONZE_FRAME
        if self.glow_intensity > 0:
            # Add golden glow
            glow_color = tuple(int(c + (255 - c) * self.glow_intensity * 0.3) for c in border_color)
            pygame.draw.polygon(surface, glow_color, 
                               [(p[0], p[1] - int(self.hover_elevation)) for p in self.papyrus_points], 3)
        else:
            pygame.draw.polygon(surface, border_color, 
                               [(p[0], p[1] - int(self.hover_elevation)) for p in self.papyrus_points], 2)
        
        # Render text content
        self._render_card_content(surface, render_rect)
    
    def _render_card_content(self, surface: pygame.Surface, rect: pygame.Rect):
        """Render card text content."""
        # Cost in top-left corner
        cost_pos = (rect.x + 15, rect.y + 10)
        surface.blit(self.cost_surface, cost_pos)
        
        # Title below cost
        title_pos = (rect.x + 15, rect.y + 45)
        surface.blit(self.title_surface, title_pos)
        
        # Description text
        desc_y = rect.y + 80
        for line_surface in self.desc_lines[:3]:  # Max 3 lines
            surface.blit(line_surface, (rect.x + 15, desc_y))
            desc_y += line_surface.get_height() + 2
```

### 4. Update Combat Screen Layout

**File: `sands_duat/ui/combat_screen.py`**

Add this method to reorganize the layout:

```python
def _setup_improved_layout(self):
    """Set up improved combat screen layout."""
    theme = get_theme()
    
    # Get layout zones
    player_zone = theme.get_zone('player_zone')
    enemy_zone = theme.get_zone('enemy_zone')
    combat_zone = theme.get_zone('combat_zone')
    hand_zone = theme.get_zone('hand_zone')
    
    # Player status area
    self.player_health_rect = theme.get_zone('player_health')
    self.player_sand_rect = theme.get_zone('player_sand')
    
    # Enemy status area  
    self.enemy_health_rect = theme.get_zone('enemy_health')
    self.enemy_intent_rect = theme.get_zone('enemy_intent')
    
    # Combat center
    self.battlefield_rect = theme.get_zone('battlefield_center')
    self.turn_indicator_rect = theme.get_zone('turn_indicator')
    
    # Hand positioning (improved spacing)
    card_width = 140
    card_height = 200
    cards_total_width = len(self.player_hand) * card_width + (len(self.player_hand) - 1) * 10
    start_x = hand_zone.x + (hand_zone.width - cards_total_width) // 2
    
    self.card_rects = []
    for i in range(len(self.player_hand)):
        card_x = start_x + i * (card_width + 10)
        card_y = hand_zone.y + 20
        self.card_rects.append(pygame.Rect(card_x, card_y, card_width, card_height))
```

## Phase 2: Interactive Feedback & Targeting

### 1. Add Hover System

**File: `sands_duat/ui/hover_manager.py` (new file)**

```python
"""Hover effect management system."""

import pygame
from typing import Dict, Optional, Callable, Any
from .base import UIComponent

class HoverManager:
    """Manages hover effects across UI components."""
    
    def __init__(self):
        self.hovered_component: Optional[UIComponent] = None
        self.hover_callbacks: Dict[UIComponent, Callable] = {}
        self.cursor_states = {
            'default': pygame.SYSTEM_CURSOR_ARROW,
            'hover': pygame.SYSTEM_CURSOR_HAND,
            'target': pygame.SYSTEM_CURSOR_CROSSHAIR,
            'disabled': pygame.SYSTEM_CURSOR_NO,
        }
        self.current_cursor = 'default'
    
    def register_component(self, component: UIComponent, hover_callback: Optional[Callable] = None):
        """Register a component for hover tracking."""
        if hover_callback:
            self.hover_callbacks[component] = hover_callback
    
    def update_hover(self, mouse_pos: tuple, components: list):
        """Update hover state based on mouse position."""
        new_hovered = None
        
        # Find topmost hovered component
        for component in reversed(components):  # Check top-most first
            if component.visible and component.enabled and component.contains_point(mouse_pos):
                new_hovered = component
                break
        
        # Handle hover state changes
        if new_hovered != self.hovered_component:
            # Clear previous hover
            if self.hovered_component:
                self.hovered_component.hovered = False
                if self.hovered_component in self.hover_callbacks:
                    self.hover_callbacks[self.hovered_component](False)
            
            # Set new hover
            self.hovered_component = new_hovered
            if self.hovered_component:
                self.hovered_component.hovered = True
                if self.hovered_component in self.hover_callbacks:
                    self.hover_callbacks[self.hovered_component](True)
        
        # Update cursor
        self._update_cursor()
    
    def _update_cursor(self):
        """Update mouse cursor based on hover state."""
        if self.hovered_component:
            if hasattr(self.hovered_component, 'cursor_type'):
                new_cursor = self.hovered_component.cursor_type
            else:
                new_cursor = 'hover'
        else:
            new_cursor = 'default'
        
        if new_cursor != self.current_cursor:
            pygame.mouse.set_cursor(self.cursor_states[new_cursor])
            self.current_cursor = new_cursor
```

### 2. Targeting System

**File: `sands_duat/ui/targeting_system.py` (new file)**

```python
"""Card targeting and validation system."""

import pygame
from typing import Optional, List, Tuple, Callable
from .base import UIComponent
from core.cards import Card

class TargetIndicator:
    """Visual indicator for valid/invalid targets."""
    
    def __init__(self, target_rect: pygame.Rect, is_valid: bool):
        self.rect = target_rect
        self.is_valid = is_valid
        self.pulse_time = 0.0
        self.alpha = 0.0
    
    def update(self, delta_time: float):
        """Animate the targeting indicator."""
        self.pulse_time += delta_time * 4.0
        self.alpha = 0.3 + 0.2 * abs(math.sin(self.pulse_time))
    
    def render(self, surface: pygame.Surface):
        """Render the targeting indicator."""
        color = (0, 255, 0) if self.is_valid else (255, 0, 0)
        alpha = int(self.alpha * 255)
        
        # Create transparent surface
        indicator_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(indicator_surface, (*color, alpha), 
                        pygame.Rect(5, 5, self.rect.width, self.rect.height), 3)
        
        surface.blit(indicator_surface, (self.rect.x - 5, self.rect.y - 5))

class TargetingSystem:
    """Manages card targeting interactions."""
    
    def __init__(self):
        self.active_card: Optional[Card] = None
        self.dragging = False
        self.drag_start_pos: Optional[Tuple[int, int]] = None
        self.current_mouse_pos: Optional[Tuple[int, int]] = None
        self.target_indicators: List[TargetIndicator] = []
        self.validation_callback: Optional[Callable] = None
    
    def start_targeting(self, card: Card, validation_callback: Callable):
        """Start targeting mode for a card."""
        self.active_card = card
        self.validation_callback = validation_callback
        self._update_target_indicators()
    
    def _update_target_indicators(self):
        """Update visual indicators for valid targets."""
        self.target_indicators.clear()
        
        if not self.active_card or not self.validation_callback:
            return
        
        # Get potential targets from validation callback
        potential_targets = self.validation_callback(self.active_card)
        
        for target_rect, is_valid in potential_targets:
            indicator = TargetIndicator(target_rect, is_valid)
            self.target_indicators.append(indicator)
    
    def update(self, delta_time: float):
        """Update targeting system."""
        for indicator in self.target_indicators:
            indicator.update(delta_time)
    
    def render(self, surface: pygame.Surface):
        """Render targeting indicators."""
        # Draw targeting line from card to mouse
        if self.dragging and self.drag_start_pos and self.current_mouse_pos:
            pygame.draw.line(surface, (255, 215, 0), self.drag_start_pos, self.current_mouse_pos, 3)
        
        # Draw target indicators
        for indicator in self.target_indicators:
            indicator.render(surface)
    
    def handle_mouse_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for targeting."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.active_card:
                self.dragging = True
                self.drag_start_pos = event.pos
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                self._process_target_selection(event.pos)
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            self.current_mouse_pos = event.pos
        
        return False
    
    def _process_target_selection(self, target_pos: Tuple[int, int]):
        """Process the final target selection."""
        for indicator in self.target_indicators:
            if indicator.rect.collidepoint(target_pos) and indicator.is_valid:
                # Valid target selected
                self._execute_card_action(indicator.rect)
                break
        
        # Clear targeting state
        self.cancel_targeting()
    
    def cancel_targeting(self):
        """Cancel current targeting operation."""
        self.active_card = None
        self.dragging = False
        self.drag_start_pos = None
        self.current_mouse_pos = None
        self.target_indicators.clear()
        self.validation_callback = None
```

## Phase 3: Performance & Accessibility

### 1. Accessibility Support

**File: `sands_duat/ui/accessibility.py` (new file)**

```python
"""Accessibility features for improved usability."""

import pygame
from typing import Dict, Tuple, Optional
from enum import Enum

class ColorBlindType(Enum):
    NONE = "none"
    PROTANOPIA = "protanopia"      # Red-blind
    DEUTERANOPIA = "deuteranopia"  # Green-blind  
    TRITANOPIA = "tritanopia"      # Blue-blind

class AccessibilityManager:
    """Manages accessibility features."""
    
    def __init__(self):
        self.colorblind_type = ColorBlindType.NONE
        self.font_scale = 1.0
        self.high_contrast = False
        self.reduced_motion = False
        self.show_tooltips = True
        
        # Color transformation matrices for colorblind support
        self.color_matrices = {
            ColorBlindType.PROTANOPIA: [
                [0.567, 0.433, 0.000],
                [0.558, 0.442, 0.000],
                [0.000, 0.242, 0.758]
            ],
            ColorBlindType.DEUTERANOPIA: [
                [0.625, 0.375, 0.000],
                [0.700, 0.300, 0.000],
                [0.000, 0.300, 0.700]
            ],
            ColorBlindType.TRITANOPIA: [
                [0.950, 0.050, 0.000],
                [0.000, 0.433, 0.567],
                [0.000, 0.475, 0.525]
            ]
        }
    
    def transform_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Transform color for colorblind accessibility."""
        if self.colorblind_type == ColorBlindType.NONE:
            return color
        
        r, g, b = [c / 255.0 for c in color]
        matrix = self.color_matrices[self.colorblind_type]
        
        new_r = r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2]
        new_g = r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2]
        new_b = r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2]
        
        return (
            int(max(0, min(255, new_r * 255))),
            int(max(0, min(255, new_g * 255))),
            int(max(0, min(255, new_b * 255)))
        )
    
    def scale_font_size(self, base_size: int) -> int:
        """Scale font size based on accessibility settings."""
        return int(base_size * self.font_scale)
    
    def get_high_contrast_color(self, color: Tuple[int, int, int], is_background: bool = False) -> Tuple[int, int, int]:
        """Get high contrast version of color."""
        if not self.high_contrast:
            return self.transform_color(color)
        
        # Convert to luminance
        r, g, b = color
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        
        if is_background:
            return (255, 255, 255) if luminance < 128 else (0, 0, 0)
        else:
            return (0, 0, 0) if luminance > 128 else (255, 255, 255)
```

## Integration Points

### 1. Update Main Game Loop

**File: `main.py`**

Add accessibility initialization:

```python
from ui.accessibility import AccessibilityManager

# In main() function, after UI manager creation:
accessibility = AccessibilityManager()
ui_manager.set_accessibility_manager(accessibility)
```

### 2. Update UIManager

**File: `sands_duat/ui/ui_manager.py`**

Add these methods:

```python
def set_accessibility_manager(self, accessibility_manager):
    """Set the accessibility manager for all screens."""
    self.accessibility_manager = accessibility_manager
    for screen in self.screens.values():
        if hasattr(screen, 'set_accessibility_manager'):
            screen.set_accessibility_manager(accessibility_manager)

def switch_to_screen_with_transition(self, screen_name: str, transition_type: str = "slide_left"):
    """Switch screen with specific transition type."""
    return self.switch_to_screen(screen_name, transition_type, 0.8)
```

## Testing & Validation

### 1. Visual Testing Checklist
- [ ] New color palette displays correctly
- [ ] Cards show hover effects
- [ ] Targeting system works smoothly
- [ ] Layout zones are properly positioned
- [ ] Text is readable with new colors

### 2. Accessibility Testing
- [ ] High contrast mode functions
- [ ] Font scaling works at 125%, 150%, 200%
- [ ] Colorblind simulation shows proper color transformation
- [ ] Keyboard navigation possible for all interactive elements

### 3. Performance Testing
- [ ] No frame rate drops with new animations
- [ ] Memory usage remains stable
- [ ] All transitions complete smoothly

---

*This implementation guide provides the foundation for transforming the "weird" UI into an intuitive, Egyptian-themed interface that enhances rather than hinders the gameplay experience.*