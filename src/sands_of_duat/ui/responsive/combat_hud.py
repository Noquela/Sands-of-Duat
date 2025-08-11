"""
Responsive Combat HUD - Minimal, clean interface for ultrawide displays.
Provides clear visual hierarchy and prevents information overload.
"""

import pygame
from typing import Tuple, Optional
from ...core.constants import Colors
from .scaling_manager import scaling_manager
from .ultrawide_layout import ultrawide_layout
from .responsive_components import ResponsiveHealthBar, ResponsiveTurnIndicator, ResponsiveButton

class CombatHUD:
    """Minimal, responsive HUD for combat screen optimized for ultrawide displays."""
    
    def __init__(self):
        # Get HUD layout positions
        self.hud_layout = scaling_manager.get_hud_layout()
        
        # Player stats
        self.player_health = ResponsiveHealthBar(100, 'health')
        self.player_mana = ResponsiveHealthBar(50, 'mana') 
        
        # Enemy stats
        self.enemy_health = ResponsiveHealthBar(100, 'health')
        
        # Turn indicator
        self.turn_indicator = ResponsiveTurnIndicator()
        
        # Action buttons
        self.end_turn_button = ResponsiveButton(
            "END TURN", 
            button_type='default',
            zone='bottom_hud'
        )
        
        self.surrender_button = ResponsiveButton(
            "SURRENDER",
            button_type='default', 
            zone='bottom_hud'
        )
        
        # Position elements
        self._position_elements()
        
        # Animation state
        self.health_warning_flash = 0.0
        self.mana_empty_flash = 0.0
    
    def _position_elements(self):
        """Position all HUD elements using the responsive layout system."""
        # Player health (bottom left)
        player_health_pos = ultrawide_layout.position_in_zone('bottom_hud', 0.05, 0.3)
        self.player_health.set_position(*player_health_pos)
        
        # Player mana (bottom left, below health)
        player_mana_pos = (
            player_health_pos[0],
            player_health_pos[1] + self.player_health.height + scaling_manager.scale_value(10)
        )
        self.player_mana.set_position(*player_mana_pos)
        
        # Enemy health (top right)
        enemy_health_pos = ultrawide_layout.position_in_zone('top_hud', 0.75, 0.5)
        self.enemy_health.set_position(*enemy_health_pos)
        
        # Turn indicator (top center)
        turn_pos = ultrawide_layout.center_in_zone('top_hud', 
                                                  self.turn_indicator.width, 
                                                  self.turn_indicator.height)
        self.turn_indicator.set_position(*turn_pos)
        
        # Action buttons (bottom right)
        button_positions = scaling_manager.get_button_layout(2, 'default', 'bottom_hud')
        
        # Position buttons with proper spacing
        end_turn_pos = ultrawide_layout.position_in_zone('bottom_hud', 0.85, 0.2)
        surrender_pos = (end_turn_pos[0], end_turn_pos[1] + scaling_manager.scale_value(80))
        
        self.end_turn_button.set_position(*end_turn_pos)
        self.surrender_button.set_position(*surrender_pos)
    
    def set_player_health(self, current: int, max_health: int = None):
        """Update player health with warning flash for low health."""
        if max_health:
            self.player_health.max_value = max_health
        
        old_value = self.player_health.current_value
        self.player_health.set_value(current)
        
        # Flash warning if health drops below 25%
        if current < self.player_health.max_value * 0.25 and current < old_value:
            self.health_warning_flash = 1.0
    
    def set_player_mana(self, current: int, max_mana: int = None):
        """Update player mana with flash when empty."""
        if max_mana:
            self.player_mana.max_value = max_mana
        
        old_value = self.player_mana.current_value
        self.player_mana.set_value(current)
        
        # Flash when mana becomes empty
        if current == 0 and old_value > 0:
            self.mana_empty_flash = 0.8
    
    def set_enemy_health(self, current: int, max_health: int = None):
        """Update enemy health."""
        if max_health:
            self.enemy_health.max_value = max_health
        self.enemy_health.set_value(current)
    
    def set_turn(self, is_player_turn: bool):
        """Update whose turn it is."""
        self.turn_indicator.set_turn(is_player_turn)
    
    def set_action_callbacks(self, end_turn_callback, surrender_callback):
        """Set callbacks for action buttons."""
        self.end_turn_button.action = end_turn_callback
        self.surrender_button.action = surrender_callback
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool, events):
        """Update all HUD elements."""
        # Update bars
        self.player_health.update(dt)
        self.player_mana.update(dt) 
        self.enemy_health.update(dt)
        
        # Update turn indicator
        self.turn_indicator.update(dt)
        
        # Update buttons
        self.end_turn_button.update(dt, mouse_pos, mouse_pressed, events)
        self.surrender_button.update(dt, mouse_pos, mouse_pressed, events)
        
        # Update flash timers
        if self.health_warning_flash > 0:
            self.health_warning_flash -= dt * 2.0  # Flash duration
        
        if self.mana_empty_flash > 0:
            self.mana_empty_flash -= dt * 2.5  # Faster flash for mana
    
    def render(self, surface: pygame.Surface):
        """Render the minimal combat HUD."""
        # Render health bars with warning effects
        if self.health_warning_flash > 0:
            # Red warning flash overlay
            flash_alpha = int(100 * self.health_warning_flash)
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash_surface.fill((*Colors.RED, flash_alpha))
            surface.blit(flash_surface, (0, 0))
        
        # Render player elements
        self.player_health.render(surface)
        self.player_mana.render(surface)
        
        # Mana empty flash effect
        if self.mana_empty_flash > 0:
            flash_rect = self.player_mana.rect.inflate(10, 10)
            flash_alpha = int(150 * self.mana_empty_flash)
            pygame.draw.rect(surface, (*Colors.LAPIS_LAZULI, flash_alpha), flash_rect, 3)
        
        # Render enemy elements
        self.enemy_health.render(surface)
        
        # Render turn indicator
        self.turn_indicator.render(surface)
        
        # Render action buttons
        self.end_turn_button.render(surface)
        self.surrender_button.render(surface)
        
        # Add subtle labels for clarity
        self._render_labels(surface)
    
    def _render_labels(self, surface: pygame.Surface):
        """Render minimal labels for better UX."""
        label_font = scaling_manager.get_font('small')
        label_color = Colors.PAPYRUS
        
        # Player health label
        health_label = label_font.render("HEALTH", True, label_color)
        health_label_pos = (
            self.player_health.rect.x,
            self.player_health.rect.y - scaling_manager.scale_value(20)
        )
        surface.blit(health_label, health_label_pos)
        
        # Player mana label
        mana_label = label_font.render("MANA", True, label_color)
        mana_label_pos = (
            self.player_mana.rect.x,
            self.player_mana.rect.y - scaling_manager.scale_value(20)
        )
        surface.blit(mana_label, mana_label_pos)
        
        # Enemy health label  
        enemy_label = label_font.render("ENEMY", True, label_color)
        enemy_label_pos = (
            self.enemy_health.rect.x,
            self.enemy_health.rect.y - scaling_manager.scale_value(20)
        )
        surface.blit(enemy_label, enemy_label_pos)
    
    def get_layout_info(self):
        """Get HUD layout information for debugging."""
        return {
            'player_health': (self.player_health.rect.x, self.player_health.rect.y),
            'player_mana': (self.player_mana.rect.x, self.player_mana.rect.y),
            'enemy_health': (self.enemy_health.rect.x, self.enemy_health.rect.y),
            'turn_indicator': (self.turn_indicator.rect.x, self.turn_indicator.rect.y),
            'action_buttons': [(self.end_turn_button.rect.x, self.end_turn_button.rect.y),
                              (self.surrender_button.rect.x, self.surrender_button.rect.y)]
        }