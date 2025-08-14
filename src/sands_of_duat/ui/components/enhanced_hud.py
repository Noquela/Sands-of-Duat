"""
Enhanced HUD Components - SPRINT 1 Implementation
Horizontal bars, clear visual hierarchy, minimalista design for ultrawide.
"""

import pygame
import math
from typing import Tuple, Dict, Optional
from ...core.constants import Colors, Timing
from ..responsive.scaling_manager import scaling_manager

class EnhancedHealthBar:
    """SPRINT 1: Horizontal health bar with gradient and smooth animations."""
    
    def __init__(self, max_health: int = 100):
        self.max_health = max_health
        self.current_health = max_health
        self.display_health = float(max_health)
        self.target_health = float(max_health)
        
        # Get enhanced dimensions from scaling manager
        self.width, self.height = scaling_manager.get_component_size('health_bar')
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Animation state
        self.pulse_timer = 0.0
        self.damage_flash = 0.0
        self.heal_flash = 0.0
        
        # Enhanced colors for better visibility
        self.colors = {
            'bg': (40, 15, 15),           # Dark red background
            'fill_high': (220, 60, 60),   # Bright red for high health
            'fill_med': (255, 140, 0),    # Orange for medium health
            'fill_low': (255, 80, 80),    # Bright red for low health
            'border': Colors.PAPYRUS,
            'text': Colors.PAPYRUS,
            'gradient_start': (255, 100, 100),
            'gradient_end': (180, 40, 40)
        }
    
    def set_position(self, x: int, y: int):
        """Set health bar position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_health(self, health: int):
        """Set current health with animation."""
        old_health = self.current_health
        self.current_health = max(0, min(health, self.max_health))
        self.target_health = float(self.current_health)
        
        # Trigger visual effects
        if self.current_health < old_health:
            self.damage_flash = 1.0  # Damage flash
        elif self.current_health > old_health:
            self.heal_flash = 1.0    # Heal flash
    
    def update(self, dt: float):
        """Update animations and effects."""
        # Smooth health animation
        health_speed = 150.0  # Health units per second
        health_diff = self.target_health - self.display_health
        
        if abs(health_diff) > 0.5:
            move_amount = health_speed * dt
            if health_diff > 0:
                self.display_health = min(self.display_health + move_amount, self.target_health)
            else:
                self.display_health = max(self.display_health - move_amount, self.target_health)
        
        # Update visual effects
        self.pulse_timer += dt * 3.0  # Pulse speed
        
        if self.damage_flash > 0:
            self.damage_flash = max(0, self.damage_flash - dt * 4.0)
        
        if self.heal_flash > 0:
            self.heal_flash = max(0, self.heal_flash - dt * 3.0)
    
    def render(self, surface: pygame.Surface):
        """Render enhanced health bar with gradient and effects."""
        # Background with subtle border
        pygame.draw.rect(surface, self.colors['bg'], self.rect, border_radius=6)
        
        # Health fill with gradient effect
        if self.max_health > 0:
            fill_ratio = self.display_health / self.max_health
            fill_width = int(self.rect.width * fill_ratio)
            
            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
                
                # Choose color based on health percentage
                health_percent = fill_ratio
                if health_percent > 0.6:
                    fill_color = self.colors['fill_high']
                elif health_percent > 0.3:
                    fill_color = self.colors['fill_med']
                else:
                    fill_color = self.colors['fill_low']
                    # Add pulsing effect for low health
                    pulse_intensity = abs(math.sin(self.pulse_timer))
                    fill_color = (
                        min(255, int(fill_color[0] + pulse_intensity * 60)),
                        min(255, int(fill_color[1] + pulse_intensity * 20)),
                        min(255, int(fill_color[2] + pulse_intensity * 20))
                    )
                
                # Apply damage/heal flash
                if self.damage_flash > 0:
                    flash_amount = int(100 * self.damage_flash)
                    fill_color = (
                        min(255, fill_color[0] + flash_amount),
                        max(0, fill_color[1] - flash_amount // 2),
                        max(0, fill_color[2] - flash_amount // 2)
                    )
                elif self.heal_flash > 0:
                    flash_amount = int(80 * self.heal_flash)
                    fill_color = (
                        max(0, fill_color[0] - flash_amount // 3),
                        min(255, fill_color[1] + flash_amount),
                        max(0, fill_color[2] - flash_amount // 3)
                    )
                
                pygame.draw.rect(surface, fill_color, fill_rect, border_radius=6)
        
        # Enhanced border
        border_color = self.colors['border']
        pygame.draw.rect(surface, border_color, self.rect, width=3, border_radius=6)
        
        # Health text with shadow
        text = f"{int(self.display_health)}/{self.max_health}"
        font = scaling_manager.get_font('body')
        
        # Text shadow
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class EnhancedManaBar:
    """SPRINT 1: Horizontal mana bar with flowing effect."""
    
    def __init__(self, max_mana: int = 50):
        self.max_mana = max_mana
        self.current_mana = max_mana
        self.display_mana = float(max_mana)
        self.target_mana = float(max_mana)
        
        # Get enhanced dimensions
        self.width, self.height = scaling_manager.get_component_size('mana_bar')
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Animation state
        self.flow_timer = 0.0
        self.spend_flash = 0.0
        self.regen_flash = 0.0
        
        # Enhanced colors
        self.colors = {
            'bg': (15, 15, 40),
            'fill': (100, 150, 255),
            'fill_flow': (150, 200, 255),
            'border': Colors.PAPYRUS,
            'text': Colors.PAPYRUS
        }
    
    def set_position(self, x: int, y: int):
        """Set mana bar position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_mana(self, mana: int):
        """Set current mana with animation."""
        old_mana = self.current_mana
        self.current_mana = max(0, min(mana, self.max_mana))
        self.target_mana = float(self.current_mana)
        
        # Trigger visual effects
        if self.current_mana < old_mana:
            self.spend_flash = 1.0
        elif self.current_mana > old_mana:
            self.regen_flash = 1.0
    
    def update(self, dt: float):
        """Update mana bar animations."""
        # Smooth mana animation
        mana_speed = 80.0
        mana_diff = self.target_mana - self.display_mana
        
        if abs(mana_diff) > 0.1:
            move_amount = mana_speed * dt
            if mana_diff > 0:
                self.display_mana = min(self.display_mana + move_amount, self.target_mana)
            else:
                self.display_mana = max(self.display_mana - move_amount, self.target_mana)
        
        # Flow animation
        self.flow_timer += dt * 2.0
        
        # Flash effects
        if self.spend_flash > 0:
            self.spend_flash = max(0, self.spend_flash - dt * 3.0)
        
        if self.regen_flash > 0:
            self.regen_flash = max(0, self.regen_flash - dt * 2.5)
    
    def render(self, surface: pygame.Surface):
        """Render enhanced mana bar with flowing effect."""
        # Background
        pygame.draw.rect(surface, self.colors['bg'], self.rect, border_radius=5)
        
        # Mana fill with flowing effect
        if self.max_mana > 0:
            fill_ratio = self.display_mana / self.max_mana
            fill_width = int(self.rect.width * fill_ratio)
            
            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
                
                # Base mana color
                fill_color = self.colors['fill']
                
                # Add flowing effect
                flow_intensity = (math.sin(self.flow_timer) + 1) * 0.3
                flowing_color = (
                    int(fill_color[0] + flow_intensity * 40),
                    int(fill_color[1] + flow_intensity * 30),
                    min(255, int(fill_color[2] + flow_intensity * 20))
                )
                
                # Apply flash effects
                if self.spend_flash > 0:
                    flash_amount = int(60 * self.spend_flash)
                    flowing_color = (
                        max(0, flowing_color[0] - flash_amount),
                        max(0, flowing_color[1] - flash_amount // 2),
                        flowing_color[2]
                    )
                elif self.regen_flash > 0:
                    flash_amount = int(80 * self.regen_flash)
                    flowing_color = (
                        flowing_color[0],
                        min(255, flowing_color[1] + flash_amount // 2),
                        min(255, flowing_color[2] + flash_amount)
                    )
                
                pygame.draw.rect(surface, flowing_color, fill_rect, border_radius=5)
        
        # Border
        pygame.draw.rect(surface, self.colors['border'], self.rect, width=2, border_radius=5)
        
        # Mana text
        text = f"{int(self.display_mana)}/{self.max_mana}"
        font = scaling_manager.get_font('body')
        
        # Text shadow
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        surface.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class EnhancedTurnIndicator:
    """SPRINT 1: Large, prominent turn indicator with animations."""
    
    def __init__(self):
        self.width, self.height = scaling_manager.get_component_size('turn_indicator')
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        self.is_player_turn = True
        self.turn_change_flash = 0.0
        self.pulse_timer = 0.0
        self.scale_animation = 1.0
        
        # Enhanced colors
        self.colors = {
            'player_bg': Colors.GOLD,
            'enemy_bg': Colors.RED,
            'text': Colors.DARK_BLUE,
            'border': Colors.PAPYRUS,
            'flash': (255, 255, 255)
        }
    
    def set_position(self, x: int, y: int):
        """Set turn indicator position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_turn(self, is_player_turn: bool):
        """Set whose turn it is with dramatic animation."""
        if self.is_player_turn != is_player_turn:
            self.is_player_turn = is_player_turn
            self.turn_change_flash = 1.5  # Longer flash for visibility
            self.scale_animation = 1.2    # Scale up when turn changes
    
    def update(self, dt: float):
        """Update turn indicator animations."""
        # Flash animation
        if self.turn_change_flash > 0:
            self.turn_change_flash = max(0, self.turn_change_flash - dt * 2.0)
        
        # Pulse animation
        self.pulse_timer += dt * 2.5
        
        # Scale animation back to normal
        if self.scale_animation > 1.0:
            self.scale_animation = max(1.0, self.scale_animation - dt * 3.0)
    
    def render(self, surface: pygame.Surface):
        """Render prominent turn indicator."""
        # Calculate animated scale
        current_scale = self.scale_animation
        if self.is_player_turn:
            # Add subtle pulse for player turn
            pulse_amount = abs(math.sin(self.pulse_timer)) * 0.05
            current_scale += pulse_amount
        
        # Scaled dimensions
        scaled_width = int(self.width * current_scale)
        scaled_height = int(self.height * current_scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width, scaled_height
        )
        
        # Background color
        bg_color = self.colors['player_bg'] if self.is_player_turn else self.colors['enemy_bg']
        
        # Apply flash effect
        if self.turn_change_flash > 0:
            flash_intensity = self.turn_change_flash * 0.7
            bg_color = (
                min(255, int(bg_color[0] + flash_intensity * 100)),
                min(255, int(bg_color[1] + flash_intensity * 100)),
                min(255, int(bg_color[2] + flash_intensity * 100))
            )
        
        # Background with rounded corners
        pygame.draw.rect(surface, bg_color, scaled_rect, border_radius=12)
        
        # Enhanced border
        border_width = 4 if self.is_player_turn else 3
        pygame.draw.rect(surface, self.colors['border'], scaled_rect, 
                        width=border_width, border_radius=12)
        
        # Turn text
        text = "YOUR TURN" if self.is_player_turn else "ENEMY TURN"
        font = scaling_manager.get_font('title_medium')
        
        # Text shadow for better readability
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)

class EnhancedHUD:
    """SPRINT 1: Complete enhanced HUD system with all components."""
    
    def __init__(self, max_health: int = 100, max_mana: int = 50):
        self.health_bar = EnhancedHealthBar(max_health)
        self.mana_bar = EnhancedManaBar(max_mana)
        self.turn_indicator = EnhancedTurnIndicator()
        
        # Get layout from scaling manager
        self.layout = scaling_manager.get_hud_layout()
        self._position_components()
    
    def _position_components(self):
        """Position all HUD components using enhanced layout."""
        self.health_bar.set_position(
            self.layout['health_bar'].x, 
            self.layout['health_bar'].y
        )
        
        self.mana_bar.set_position(
            self.layout['mana_bar'].x,
            self.layout['mana_bar'].y
        )
        
        self.turn_indicator.set_position(
            self.layout['turn_indicator'].x,
            self.layout['turn_indicator'].y
        )
    
    def set_health(self, health: int):
        """Update health value."""
        self.health_bar.set_health(health)
    
    def set_mana(self, mana: int):
        """Update mana value."""
        self.mana_bar.set_mana(mana)
    
    def set_turn(self, is_player_turn: bool):
        """Update turn state."""
        self.turn_indicator.set_turn(is_player_turn)
    
    def update(self, dt: float):
        """Update all HUD components."""
        self.health_bar.update(dt)
        self.mana_bar.update(dt)
        self.turn_indicator.update(dt)
    
    def render(self, surface: pygame.Surface):
        """Render all HUD components."""
        self.health_bar.render(surface)
        self.mana_bar.render(surface)
        self.turn_indicator.render(surface)
    
    def get_layout_info(self) -> Dict[str, pygame.Rect]:
        """Get layout information for other UI elements."""
        return self.layout