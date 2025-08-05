"""
Combat Screen

Main battle interface featuring Hour-Glass Initiative visualization,
card hand management, and real-time combat mechanics.
"""

import pygame
import math
import random
import time
from typing import List, Optional, Dict, Any, Tuple
from .base import UIScreen, UIComponent
from .theme import get_theme
from .particle_system import ParticleSystem, ParticleEmitter, ParticleType
from ..core.hourglass import HourGlass
from ..core.cards import Card, CardType, EffectType
from ..core.combat_manager import CombatManager
from ..audio.sound_effects import play_card_interaction_sound, play_combat_feedback_sound, play_sand_feedback_sound
from ..graphics.sprite_animator import CharacterSprite, AnimationState, create_character_sprite
from ..graphics.card_art_loader import load_card_art

# Import parallax and atmospheric systems
try:
    from sands_duat.graphics.interactive_parallax_system import (
        get_interactive_parallax_system, InteractionType, trigger_ui_interaction, handle_mouse_parallax
    )
    from sands_duat.graphics.egyptian_atmospheric_effects import get_atmospheric_manager
    PARALLAX_AVAILABLE = True
except ImportError:
    PARALLAX_AVAILABLE = False


class AccessibilitySettings:
    """Accessibility settings for improved usability."""
    
    def __init__(self):
        self.colorblind_mode = "none"  # none, protanopia, deuteranopia, tritanopia
        self.font_scale = 1.0  # 0.8 to 1.5
        self.high_contrast = False
        self.reduced_motion = False
    
    def get_color(self, base_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert color for colorblind accessibility."""
        if self.colorblind_mode == "none":
            return base_color
        
        r, g, b = base_color
        
        if self.colorblind_mode == "protanopia":
            # Red-blind: enhance green/blue contrast
            new_r = int(r * 0.567 + g * 0.433)
            new_g = int(g * 0.558 + b * 0.442)
            new_b = int(b * 0.242 + g * 0.758)
            return (new_r, new_g, new_b)
        
        elif self.colorblind_mode == "deuteranopia":
            # Green-blind: enhance red/blue contrast
            new_r = int(r * 0.625 + g * 0.375)
            new_g = int(g * 0.7 + r * 0.3)
            new_b = int(b * 0.3 + g * 0.7)
            return (new_r, new_g, new_b)
        
        elif self.colorblind_mode == "tritanopia":
            # Blue-blind: enhance red/green contrast
            new_r = int(r * 0.95 + g * 0.05)
            new_g = int(g * 0.433 + r * 0.567)
            new_b = int(b * 0.475 + g * 0.525)
            return (new_r, new_g, new_b)
        
        return base_color
    
    def get_font_size(self, base_size: int) -> int:
        """Get scaled font size."""
        return int(base_size * self.font_scale)


# Global accessibility settings instance
accessibility_settings = AccessibilitySettings()


class SandGauge(UIComponent):
    """
    Visual representation of the Hour-Glass sand system.
    
    Shows current sand level with smooth animations and
    time-until-next-grain indicators.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, hourglass: HourGlass):
        super().__init__(x, y, width, height)
        self.hourglass = hourglass
        self.sand_particles: List[Dict[str, Any]] = []
        self.animation_time = 0.0
        self.last_sand_count = 0
        
        # Visual settings
        self.glass_color = (200, 200, 255, 100)  # Light blue glass
        self.sand_color = (255, 215, 0)          # Gold sand
        self.frame_color = (139, 117, 93)        # Bronze frame
    
    def update(self, delta_time: float) -> None:
        """Update sand gauge animations."""
        self.animation_time += delta_time
        
        # Update hourglass state
        self.hourglass.update_sand()
        
        # Check for sand changes to trigger animations
        current_sand = self.hourglass.current_sand
        if current_sand != self.last_sand_count:
            if current_sand > self.last_sand_count:
                # Sand was gained - animate new particles
                self._animate_sand_gain()
            self.last_sand_count = current_sand
        
        # Update particle animations
        self._update_particles(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the sand gauge."""
        if not self.visible:
            return
        
        # Draw hourglass frame
        self._draw_hourglass_frame(surface)
        
        # Draw sand level
        self._draw_sand_level(surface)
        
        # Draw sand particles
        self._draw_particles(surface)
        
        # Draw progress indicator for next sand
        self._draw_progress_indicator(surface)
        
        # Draw sand count text
        self._draw_sand_text(surface)
    
    def _draw_hourglass_frame(self, surface: pygame.Surface) -> None:
        """Draw the hourglass frame."""
        # Outer frame
        pygame.draw.rect(surface, self.frame_color, self.rect, self.border_width)
        
        # Glass effect (simplified)
        glass_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)
        glass_surface = pygame.Surface(glass_rect.size, pygame.SRCALPHA)
        glass_surface.fill(self.glass_color)
        surface.blit(glass_surface, glass_rect.topleft)
        
        # Hourglass shape outline
        center_x = self.rect.centerx
        center_y = self.rect.centery
        top_y = self.rect.top + 10
        bottom_y = self.rect.bottom - 10
        width = self.rect.width - 20
        
        # Draw hourglass outline
        points = [
            (center_x - width//2, top_y),
            (center_x + width//2, top_y),
            (center_x + 10, center_y),
            (center_x + width//2, bottom_y),
            (center_x - width//2, bottom_y),
            (center_x - 10, center_y)
        ]
        pygame.draw.polygon(surface, self.frame_color, points, 2)
    
    def _draw_sand_level(self, surface: pygame.Surface) -> None:
        """Draw the current sand level."""
        if self.hourglass.current_sand == 0:
            return
        
        # Calculate sand height based on current sand
        max_height = self.rect.height - 40  # Leave space for frame
        sand_height = (self.hourglass.current_sand / self.hourglass.max_sand) * max_height
        
        # Draw sand in bottom chamber
        sand_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.bottom - 20 - sand_height,
            self.rect.width - 20,
            sand_height
        )
        
        pygame.draw.rect(surface, self.sand_color, sand_rect)
        
        # Add shimmer effect
        shimmer_alpha = int(50 + 30 * math.sin(self.animation_time * 3))
        shimmer_surface = pygame.Surface(sand_rect.size, pygame.SRCALPHA)
        shimmer_surface.fill((*self.sand_color, shimmer_alpha))
        surface.blit(shimmer_surface, sand_rect.topleft)
    
    def _draw_particles(self, surface: pygame.Surface) -> None:
        """Draw animated sand particles."""
        for particle in self.sand_particles:
            if particle['alpha'] > 0:
                color = (*self.sand_color, int(particle['alpha']))
                particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                particle_surface.fill(color)
                surface.blit(particle_surface, (particle['x'], particle['y']))
    
    def _draw_progress_indicator(self, surface: pygame.Surface) -> None:
        """Draw progress until next sand grain."""
        if self.hourglass.current_sand >= self.hourglass.max_sand:
            return
        
        time_until_next = self.hourglass.get_time_until_next_sand()
        if time_until_next == float('inf'):
            return
        
        # Progress bar showing time until next sand
        progress = 1.0 - (time_until_next / (1.0 / self.hourglass.timer.regeneration_rate))
        progress = max(0.0, min(1.0, progress))
        
        bar_width = self.rect.width - 20
        bar_height = 4
        bar_x = self.rect.x + 10
        bar_y = self.rect.bottom + 5
        
        # Background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(surface, self.sand_color, (bar_x, bar_y, progress_width, bar_height))
    
    def _draw_sand_text(self, surface: pygame.Surface) -> None:
        """Draw sand count text."""
        font = pygame.font.Font(None, 24)
        text = f"{self.hourglass.current_sand}/{self.hourglass.max_sand}"
        text_surface = font.render(text, True, self.text_color)
        
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.y = self.rect.bottom + 15
        
        surface.blit(text_surface, text_rect)
    
    def _animate_sand_gain(self) -> None:
        """Create particles for sand gain animation."""
        for _ in range(5):  # Create 5 particles per sand grain
            particle = {
                'x': self.rect.centerx + (random.random() - 0.5) * 20,
                'y': self.rect.top,
                'vx': (random.random() - 0.5) * 2,
                'vy': 2 + random.random() * 2,
                'alpha': 255,
                'life': 1.0
            }
            self.sand_particles.append(particle)
    
    def _update_particles(self, delta_time: float) -> None:
        """Update particle animations."""
        for particle in self.sand_particles[:]:  # Copy list to avoid modification during iteration
            particle['x'] += particle['vx'] * delta_time * 60
            particle['y'] += particle['vy'] * delta_time * 60
            particle['life'] -= delta_time
            particle['alpha'] = max(0, particle['alpha'] - 200 * delta_time)
            
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.sand_particles.remove(particle)


class CardDisplay(UIComponent):
    """
    Displays a single card with enhanced hover effects and interaction.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, card: Optional[Card] = None):
        super().__init__(x, y, width, height)
        self.card = card
        self.scale = 1.0
        self.target_scale = 1.0
        self.playable = True
        self.hover_glow_alpha = 0
        self.target_glow_alpha = 0
        self.pulse_time = 0.0
        self.shimmer_offset = 0.0
        
        # Drag and drop state
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.drag_start_pos = (0, 0)
        self.original_pos = (x, y)
        self.in_play_zone = False
        self.play_zone_alpha = 0
        self.target_play_zone_alpha = 0
        
        # Visual settings
        self.card_bg_color = (40, 30, 20)
        self.card_border_color = (139, 117, 93)
        self.highlight_color = (255, 215, 0)
        self.glow_color = (255, 215, 0, 80)
        self.shimmer_color = (255, 255, 255, 60)
        
        # Enable Egyptian feedback effects for combat cards
        self.enable_egyptian_feedback('all')
        
        # Enhanced effects for special cards
        if card and hasattr(card, 'type'):
            if card.type in ['LEGENDARY', 'ARTIFACT']:
                self.egyptian_feedback['mystical_particles'] = True
    
    def update(self, delta_time: float) -> None:
        """Update card display animations with enhanced hover effects."""
        # Update pulse time for animation effects
        self.pulse_time += delta_time * 3.0
        self.shimmer_offset += delta_time * 200.0
        
        # Smooth scale animation
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * delta_time * 10
        
        # Smooth glow animation
        if abs(self.hover_glow_alpha - self.target_glow_alpha) > 1:
            self.hover_glow_alpha += (self.target_glow_alpha - self.hover_glow_alpha) * delta_time * 8
        
        # Smooth play zone alpha animation
        if abs(self.play_zone_alpha - self.target_play_zone_alpha) > 1:
            self.play_zone_alpha += (self.target_play_zone_alpha - self.play_zone_alpha) * delta_time * 10
        
        # Update target effects based on hover, drag, and playability
        if self.being_dragged:
            self.target_scale = 1.2
            self.target_glow_alpha = 255
            # Check if in play zone (dragged up significantly)
            if self.drag_offset_y < -80:
                self.in_play_zone = True
                self.target_play_zone_alpha = 150
            else:
                self.in_play_zone = False
                self.target_play_zone_alpha = 0
        elif self.hovered and self.playable:
            self.target_scale = 1.15
            self.target_glow_alpha = 255
            self.target_play_zone_alpha = 0
        elif self.hovered:
            self.target_scale = 1.05
            self.target_glow_alpha = 100
            self.target_play_zone_alpha = 0
        else:
            self.target_scale = 1.0
            self.target_glow_alpha = 0
            self.target_play_zone_alpha = 0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the card with enhanced visual effects."""
        if not self.visible or not self.card:
            return
        
        # Calculate scaled rect with drag offset
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        
        # Apply drag offset if being dragged
        if self.being_dragged:
            center_x = self.rect.centerx + self.drag_offset_x
            center_y = self.rect.centery + self.drag_offset_y
        else:
            center_x = self.rect.centerx
            center_y = self.rect.centery
        
        scaled_rect = pygame.Rect(
            center_x - scaled_width // 2,
            center_y - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Draw hover glow effect
        if self.hover_glow_alpha > 0:
            self._draw_glow_effect(surface, scaled_rect)
        
        # Draw card background with depth
        self._draw_card_background(surface, scaled_rect)
        
        # Draw border with enhanced effects
        self._draw_card_border(surface, scaled_rect)
        
        # Draw shimmer effect for playable cards
        if self.playable and self.hovered:
            self._draw_shimmer_effect(surface, scaled_rect)
        
        # Draw card content
        self._draw_card_content(surface, scaled_rect)
        
        # Draw unplayable overlay
        if not self.playable:
            self._draw_unplayable_overlay(surface, scaled_rect)
        
        # Draw pulse effect for very playable cards
        if self.playable and self.hovered:
            self._draw_pulse_effect(surface, scaled_rect)
        
        # Draw play zone indicator when dragging
        if self.being_dragged and self.play_zone_alpha > 0:
            self._draw_play_zone_indicator(surface, scaled_rect)
    
    def _draw_glow_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw a glow effect around the card."""
        glow_size = 8
        glow_rect = rect.inflate(glow_size * 2, glow_size * 2)
        
        # Create glow surface with alpha
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        # Draw multiple glow layers for softer effect
        for i in range(glow_size):
            alpha = int(self.hover_glow_alpha * (1.0 - i / glow_size) * 0.3)
            if alpha > 0:
                glow_color = (*self.glow_color[:3], alpha)
                inner_rect = pygame.Rect(i, i, glow_rect.width - i*2, glow_rect.height - i*2)
                pygame.draw.rect(glow_surface, glow_color, inner_rect, 1)
        
        surface.blit(glow_surface, glow_rect.topleft)
    
    def _draw_card_background(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw card background with depth effect."""
        # Main background
        pygame.draw.rect(surface, self.card_bg_color, rect)
        
        # Add subtle gradient effect
        if self.hovered:
            gradient_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            for y in range(rect.height):
                alpha = int(20 * (1.0 - y / rect.height))
                color = (*self.highlight_color[:3], alpha)
                pygame.draw.line(gradient_surface, color, (0, y), (rect.width, y))
            surface.blit(gradient_surface, rect.topleft)
    
    def _draw_card_border(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw enhanced card border."""
        if self.hovered and self.playable:
            # Animated border thickness
            thickness = 3 + int(2 * abs(math.sin(self.pulse_time)))
            border_color = self.highlight_color
        elif self.hovered:
            thickness = 2
            border_color = (150, 150, 150)
        else:
            thickness = 2
            border_color = self.card_border_color
        
        pygame.draw.rect(surface, border_color, rect, thickness)
    
    def _draw_shimmer_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw shimmer effect across the card."""
        shimmer_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        
        # Moving shimmer line
        shimmer_x = (self.shimmer_offset % (rect.width + 40)) - 20
        
        for i in range(-10, 11):
            x = int(shimmer_x + i)
            if 0 <= x < rect.width:
                alpha = int(self.shimmer_color[3] * (1.0 - abs(i) / 10.0))
                color = (*self.shimmer_color[:3], alpha)
                pygame.draw.line(shimmer_surface, color, (x, 0), (x, rect.height))
        
        surface.blit(shimmer_surface, rect.topleft)
    
    def _draw_pulse_effect(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw subtle pulse effect for playable cards."""
        pulse_alpha = int(30 + 20 * math.sin(self.pulse_time * 2))
        pulse_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pulse_color = (*self.highlight_color[:3], pulse_alpha)
        pygame.draw.rect(pulse_surface, pulse_color, (0, 0, rect.width, rect.height))
        surface.blit(pulse_surface, rect.topleft)
    
    def _draw_unplayable_overlay(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw overlay for unplayable cards."""
        overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, rect.topleft)
        
        # Add "X" pattern for very clear feedback
        pygame.draw.line(overlay, (255, 0, 0), (0, 0), (rect.width, rect.height), 3)
        pygame.draw.line(overlay, (255, 0, 0), (rect.width, 0), (0, rect.height), 3)
        surface.blit(overlay, rect.topleft)
    
    def _draw_card_artwork(self, surface: pygame.Surface, art_rect: pygame.Rect) -> None:
        """Draw AI-generated card artwork"""
        try:
            # Load AI artwork for this card
            from ..graphics.card_art_loader import load_card_art
            artwork = load_card_art(self.card.name, (art_rect.width, art_rect.height))
            
            if artwork:
                # Draw the AI artwork
                surface.blit(artwork, art_rect)
                
                # Add subtle border around artwork
                pygame.draw.rect(surface, (139, 117, 93), art_rect, 2)
                
                # Success indicator for debugging
                font = pygame.font.Font(None, 12)
                debug_text = font.render("AI Art", True, (0, 255, 0))
                surface.blit(debug_text, (art_rect.x + 2, art_rect.y + 2))
                
            else:
                # Fallback to simple colored background with card name
                color = self._get_card_type_color()
                pygame.draw.rect(surface, color, art_rect)
                pygame.draw.rect(surface, (100, 50, 25), art_rect, 2)
                
                # Show card name in fallback
                font = pygame.font.Font(None, 16)
                name_lines = self.card.name.split(' ')
                for i, line in enumerate(name_lines[:3]):  # Max 3 lines
                    text = font.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(art_rect.centerx, art_rect.centery + i * 20 - 20))
                    surface.blit(text, text_rect)
                
        except Exception as e:
            # Error fallback - draw simple rectangle
            pygame.draw.rect(surface, (80, 40, 20), art_rect)
            pygame.draw.rect(surface, (120, 60, 30), art_rect, 2)
            
            # Show error info for debugging
            font = pygame.font.Font(None, 14)
            error_text = font.render(f"Error: {str(e)[:20]}", True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(art_rect.centerx, art_rect.centery - 10))
            surface.blit(error_text, error_rect)
            
            card_text = font.render(self.card.name[:15], True, (255, 255, 255))
            card_rect = card_text.get_rect(center=(art_rect.centerx, art_rect.centery + 10))
            surface.blit(card_text, card_rect)
    
    def _get_card_type_color(self) -> tuple:
        """Get color based on card type"""
        type_colors = {
            CardType.ATTACK: (150, 50, 50),
            CardType.DEFENSE: (50, 100, 150),
            CardType.MAGIC: (100, 50, 150),
            CardType.SUPPORT: (50, 150, 100)
        }
        return type_colors.get(self.card.card_type, (100, 100, 100))
    
    def _draw_card_content(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw the card's content with enhanced visibility."""
        # Sand cost with background
        cost_font = pygame.font.Font(None, 28)
        cost_text = str(self.card.sand_cost)
        cost_surface = cost_font.render(cost_text, True, (255, 255, 255))
        
        # Cost background circle
        cost_bg_radius = 15
        cost_center = (rect.right - 20, rect.top + 20)
        pygame.draw.circle(surface, self.highlight_color, cost_center, cost_bg_radius)
        pygame.draw.circle(surface, (0, 0, 0), cost_center, cost_bg_radius, 2)
        
        cost_rect = cost_surface.get_rect(center=cost_center)
        surface.blit(cost_surface, cost_rect)
        
        # AI Card Artwork (prominent center area)
        art_rect = pygame.Rect(
            rect.left + 5, 
            rect.top + 30, 
            rect.width - 10, 
            rect.height - 60
        )
        self._draw_card_artwork(surface, art_rect)
        
        # Card name with shadow
        name_font = pygame.font.Font(None, 22)
        # Shadow
        name_shadow = name_font.render(self.card.name, True, (0, 0, 0))
        name_shadow_rect = name_shadow.get_rect(centerx=rect.centerx + 1, top=rect.top + 36)
        surface.blit(name_shadow, name_shadow_rect)
        # Main text
        name_text = name_font.render(self.card.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(centerx=rect.centerx, top=rect.top + 35)
        surface.blit(name_text, name_rect)
        
        # Card type with background
        type_font = pygame.font.Font(None, 16)
        type_text = self.card.card_type.value.title()
        type_surface = type_font.render(type_text, True, (255, 255, 255))
        type_rect = type_surface.get_rect(centerx=rect.centerx, top=name_rect.bottom + 8)
        
        # Type background
        type_bg_rect = type_rect.inflate(10, 4)
        pygame.draw.rect(surface, (60, 60, 60), type_bg_rect)
        pygame.draw.rect(surface, (120, 120, 120), type_bg_rect, 1)
        surface.blit(type_surface, type_rect)
    
    def set_card(self, card: Optional[Card]) -> None:
        """Set the card to display."""
        self.card = card
    
    def set_playable(self, playable: bool) -> None:
        """Set whether the card can be played."""
        self.playable = playable
    
    def _draw_play_zone_indicator(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw indicator when card is in play zone."""
        if self.in_play_zone:
            # Draw green glow when in play zone
            indicator_color = (0, 255, 100, int(self.play_zone_alpha))
            indicator_rect = rect.inflate(20, 20)
            
            # Create indicator surface
            indicator_surface = pygame.Surface(indicator_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(indicator_surface, indicator_color, indicator_surface.get_rect(), 5)
            surface.blit(indicator_surface, indicator_rect.topleft)
            
            # Draw "PLAY" text
            font = pygame.font.Font(None, 24)
            play_text = font.render("JOGAR", True, (255, 255, 255))
            play_rect = play_text.get_rect(center=(rect.centerx, rect.bottom + 30))
            surface.blit(play_text, play_rect)
        else:
            # Draw red indication when dragging but not in play zone
            if self.being_dragged:
                indicator_color = (255, 100, 100, int(self.play_zone_alpha))
                indicator_rect = rect.inflate(10, 10)
                
                indicator_surface = pygame.Surface(indicator_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(indicator_surface, indicator_color, indicator_surface.get_rect(), 3)
                surface.blit(indicator_surface, indicator_rect.topleft)
    
    def start_play_animation(self) -> None:
        """Start the card play animation."""
        # Quick scale animation when card is played
        self.target_scale = 1.3
        # Reset to normal after a short delay
        # (In a real implementation, this would be handled by the animation system)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle enhanced card interaction including drag and drop."""
        if not self.visible or not self.card:
            return False
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.playable:
                self.being_dragged = True
                self.drag_offset_x = 0
                self.drag_offset_y = 0
                self.drag_start_time = time.time()  # Track drag start time
                self._trigger_event("card_drag_start", {"card": self.card})
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.being_dragged:
                self.being_dragged = False
                drag_duration = time.time() - getattr(self, 'drag_start_time', 0)
                
                # If it was a quick click (< 0.2 seconds) and minimal drag, treat as direct play
                if drag_duration < 0.2 and abs(self.drag_offset_x) < 10 and abs(self.drag_offset_y) < 10:
                    if self.playable:  # Only trigger if card is actually playable
                        self.start_play_animation()
                        self._trigger_event("card_played", {"card": self.card})
                    else:
                        # Show feedback that card cannot be played
                        self._trigger_event("card_play_failed", {"card": self.card})
                # Check if card was dropped in a valid play area (drag-and-drop)
                elif self.in_play_zone and self.drag_offset_y < -80:  # Dragged up significantly into play zone
                    self.start_play_animation()
                    self._trigger_event("card_played", {"card": self.card})
                else:
                    # Card was released but not in play zone - return to hand
                    self._trigger_event("card_drag_end", {"card": self.card})
                
                self.drag_offset_x = 0
                self.drag_offset_y = 0
                return True
        
        elif event.type == pygame.MOUSEMOTION and self.being_dragged:
            # Update drag position
            mouse_x, mouse_y = event.pos
            card_center_x = self.rect.centerx
            card_center_y = self.rect.centery
            
            self.drag_offset_x = mouse_x - card_center_x
            self.drag_offset_y = mouse_y - card_center_y
            return True
        
        return super().handle_event(event)


class HandDisplay(UIComponent):
    """
    Enhanced hand display with smooth card animations and interactions.
    
    Features:
    - Dynamic card spacing based on hand size
    - Smooth card arrangement animations
    - Card hover effects with neighboring card adjustment
    - Visual feedback for playable/unplayable cards
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.cards: List[Card] = []
        self.card_displays: List[CardDisplay] = []
        self.selected_card: Optional[int] = None
        self.hovered_card: Optional[int] = None
        self.hourglass: Optional[HourGlass] = None
        
        # Layout settings (adaptive) - Much larger cards to showcase AI artwork
        self.base_card_width = 300
        self.base_card_height = 420
        self.min_card_spacing = 5
        self.max_card_spacing = 20
        self.hover_elevation = -30
        
        # Animation properties
        self.card_positions: List[Tuple[int, int]] = []
        self.target_positions: List[Tuple[int, int]] = []
        self.animation_speed = 8.0
    
    def update(self, delta_time: float) -> None:
        """Update enhanced hand display with animations."""
        # Update card playability based on sand cost
        if self.hourglass:
            for i, card_display in enumerate(self.card_displays):
                if card_display.card:
                    playable = self.hourglass.can_afford(card_display.card.sand_cost)
                    card_display.set_playable(playable)
        
        # Update hover detection with improved accuracy and audio feedback
        mouse_pos = pygame.mouse.get_pos()
        new_hovered_card = None
        for i, card_display in enumerate(self.card_displays):
            if card_display.rect.collidepoint(mouse_pos):
                new_hovered_card = i
                if not card_display.hovered:
                    # Play hover sound when card is first hovered
                    play_card_interaction_sound("hover")
                card_display.hovered = True
            else:
                card_display.hovered = False
        
        # Update hovered card and recalculate positions if needed
        if new_hovered_card != self.hovered_card:
            self.hovered_card = new_hovered_card
            self._calculate_card_positions()
        
        # Smooth position animation
        self._animate_card_positions(delta_time)
        
        # Update card displays
        for card_display in self.card_displays:
            card_display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the hand."""
        if not self.visible:
            return
        
        # Render each card
        for card_display in self.card_displays:
            card_display.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for card interaction."""
        # Let card displays handle their own events first
        for i, card_display in enumerate(self.card_displays):
            if card_display.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selected_card = i
                    self._trigger_event("card_selected", {"card_index": i, "card": card_display.card})
                return True
        
        return super().handle_event(event)
    
    def set_cards(self, cards: List[Card]) -> None:
        """Set the cards to display."""
        self.cards = cards
        self._update_card_displays()
    
    def set_hourglass(self, hourglass: HourGlass) -> None:
        """Set the hourglass for sand cost checking."""
        self.hourglass = hourglass
    
    def _update_card_displays(self) -> None:
        """Update the card display components with adaptive sizing."""
        self.card_displays.clear()
        
        if not self.cards:
            return
        
        # Calculate adaptive card size based on hand size
        hand_size = len(self.cards)
        available_width = self.rect.width - 40  # Margins
        
        # Adaptive card width and spacing
        if hand_size <= 5:
            card_width = self.base_card_width
            spacing = self.max_card_spacing
        else:
            # Reduce size for larger hands
            total_card_width = hand_size * self.base_card_width
            total_spacing = (hand_size - 1) * self.min_card_spacing
            
            if total_card_width + total_spacing > available_width:
                # Scale down cards to fit
                scale_factor = available_width / (total_card_width + total_spacing)
                card_width = int(self.base_card_width * scale_factor)
                spacing = self.min_card_spacing
            else:
                card_width = self.base_card_width
                spacing = min(self.max_card_spacing, 
                             (available_width - total_card_width) // (hand_size - 1))
        
        # Create card displays
        for i, card in enumerate(self.cards):
            card_display = CardDisplay(0, 0, card_width, self.base_card_height, card)
            # Add event handlers for new card interactions
            card_display.add_event_handler("card_played", self._on_card_played)
            card_display.add_event_handler("card_play_failed", self._on_card_play_failed)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            self.card_displays.append(card_display)
        
        # Calculate initial positions
        self._calculate_card_positions()
        
        # Set initial positions (no animation)
        for i, card_display in enumerate(self.card_displays):
            if i < len(self.target_positions):
                x, y = self.target_positions[i]
                card_display.rect.centerx = x
                card_display.rect.centery = y
    
    def _calculate_card_positions(self) -> None:
        """Calculate target positions for all cards with hover effects."""
        if not self.card_displays:
            return
        
        hand_size = len(self.card_displays)
        card_width = self.card_displays[0].rect.width
        spacing = self.min_card_spacing if hand_size > 5 else self.max_card_spacing
        
        # Calculate base layout
        total_width = hand_size * card_width + (hand_size - 1) * spacing
        start_x = self.rect.centerx - total_width // 2 + card_width // 2
        base_y = self.rect.centery
        
        self.target_positions.clear()
        
        for i in range(hand_size):
            x = start_x + i * (card_width + spacing)
            y = base_y
            
            # Adjust for hovered card
            if self.hovered_card is not None:
                if i == self.hovered_card:
                    y += self.hover_elevation  # Lift hovered card
                elif abs(i - self.hovered_card) == 1:
                    # Slightly adjust neighboring cards
                    offset = 5 if i < self.hovered_card else -5
                    x += offset
            
            self.target_positions.append((x, y))
    
    def _animate_card_positions(self, delta_time: float) -> None:
        """Smoothly animate cards to their target positions."""
        if len(self.card_positions) != len(self.target_positions):
            # Initialize positions if needed
            self.card_positions = [(display.rect.centerx, display.rect.centery) 
                                 for display in self.card_displays]
        
        for i, card_display in enumerate(self.card_displays):
            if i < len(self.target_positions):
                target_x, target_y = self.target_positions[i]
                current_x, current_y = self.card_positions[i]
                
                # Smooth interpolation
                new_x = current_x + (target_x - current_x) * delta_time * self.animation_speed
                new_y = current_y + (target_y - current_y) * delta_time * self.animation_speed
                
                self.card_positions[i] = (new_x, new_y)
                card_display.rect.centerx = int(new_x)
                card_display.rect.centery = int(new_y)
    
    def _on_card_played(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card being played with audio feedback."""
        card = event_data.get("card")
        if card:
            # Play card sound effect
            play_card_interaction_sound("play")
            
            # Remove card from hand with animation
            for i, display in enumerate(self.card_displays):
                if display.card and display.card.id == card.id:
                    self.cards.pop(i)
                    self.card_displays.pop(i)
                    self._calculate_card_positions()
                    break
            
            # Trigger parent event
            self._trigger_event("card_played", event_data)
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag start."""
        self._trigger_event("card_drag_start", event_data)
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag end."""
        self._trigger_event("card_drag_end", event_data)
    
    def _on_card_play_failed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card play failure (e.g., not enough sand)."""
        # Trigger parent event to let CombatScreen handle the failure
        self._trigger_event("card_play_failed", event_data)


class CombatScreen(UIScreen):
    """
    Main combat interface screen.
    
    Manages the battle UI including sand gauges, card hand,
    enemy display, and combat actions.
    """
    
    def __init__(self):
        super().__init__("combat")
        
        # UI components
        self.player_sand_gauge: Optional[SandGauge] = None
        self.enemy_sand_gauge: Optional[SandGauge] = None
        self.hand_display: Optional[HandDisplay] = None
        
        # Combat system
        self.combat_manager = CombatManager()
        
        # Professional sprite characters
        self.player_sprite: Optional[CharacterSprite] = None
        self.enemy_sprite: Optional[CharacterSprite] = None
        self._setup_character_sprites()
        
        # Initialize parallax and atmospheric systems
        self.parallax_system = None
        self.atmospheric_manager = None
        
        if PARALLAX_AVAILABLE:
            try:
                display_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (1920, 1080)
                self.parallax_system = get_interactive_parallax_system(display_size[0], display_size[1])
                self.parallax_system.set_current_screen("combat")
                
                self.atmospheric_manager = get_atmospheric_manager(display_size[0], display_size[1])
                self.atmospheric_manager.setup_screen_atmosphere("combat")
            except Exception as e:
                print(f"Combat parallax initialization failed: {e}")
                self.parallax_system = None
                self.atmospheric_manager = None
        
        # Visual settings
        self.font = pygame.font.Font(None, 24)
        self.text_color = (255, 248, 220)  # Cornsilk
        
        # Visual effects
        self.damage_numbers: List[Dict[str, Any]] = []
        self.effect_animations: List[Dict[str, Any]] = []
        self.particle_system = ParticleSystem(max_particles=50)
        
        # UI state
        self.selected_card_index: Optional[int] = None
        self.end_turn_button: Optional[UIComponent] = None
    
    def _setup_character_sprites(self) -> None:
        """Setup professional character sprites from asset pipeline"""
        try:
            # Player sprite (Egyptian warrior)
            self.player_sprite = create_character_sprite("player_character", "game_assets")
            if not self.player_sprite:
                self.player_sprite = create_character_sprite("anubis_guardian", "game_assets")  # Fallback
            
            if self.player_sprite:
                # Position dynamically based on screen size
                screen_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else 1920
                screen_height = pygame.display.get_surface().get_height() if pygame.display.get_surface() else 1080
                
                # Player on left side, prominent position
                player_x = min(300, screen_width // 6)
                player_y = screen_height // 2 - 50
                
                self.player_sprite.set_position(player_x, player_y)
                self.player_sprite.set_scale(3.0)  # Larger for better visibility
                self.player_sprite.set_state(AnimationState.IDLE)
            
            # Enemy sprite (Anubis Guardian for demo)
            self.enemy_sprite = create_character_sprite("anubis_guardian", "game_assets")
            if self.enemy_sprite:
                # Enemy on right side, prominent position
                screen_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else 1920
                screen_height = pygame.display.get_surface().get_height() if pygame.display.get_surface() else 1080
                
                enemy_x = max(screen_width - 300, screen_width * 5 // 6)
                enemy_y = screen_height // 2 - 50
                
                self.enemy_sprite.set_position(enemy_x, enemy_y)
                self.enemy_sprite.set_scale(3.0)  # Larger for better visibility
                self.enemy_sprite.set_flip(True)  # Face player
                self.enemy_sprite.set_state(AnimationState.IDLE)
            
            self.logger.info("Professional character sprites loaded successfully")
            
        except Exception as e:
            self.logger.warning(f"Failed to load professional sprites: {e}")
            self.player_sprite = None
            self.enemy_sprite = None
    
    def on_enter(self) -> None:
        """Initialize combat screen."""
        self.logger.info("Entering combat screen")
        self._setup_ui_components()
        self._setup_demo_combat_manager()
        self._setup_event_handlers()
    
    def on_exit(self) -> None:
        """Clean up combat screen."""
        self.logger.info("Exiting combat screen")
        self.clear_components()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle combat screen events including button clicks and accessibility shortcuts."""
        # Handle mouse movement for parallax effects
        if event.type == pygame.MOUSEMOTION and self.parallax_system:
            try:
                handle_mouse_parallax(event.pos[0], event.pos[1])
            except:
                pass  # Fallback if parallax not available
        
        # Handle accessibility keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            # Toggle colorblind mode (Ctrl+C)
            if event.key == pygame.K_c and pygame.key.get_pressed()[pygame.K_LCTRL]:
                modes = ["none", "protanopia", "deuteranopia", "tritanopia"]
                current_index = modes.index(accessibility_settings.colorblind_mode)
                accessibility_settings.colorblind_mode = modes[(current_index + 1) % len(modes)]
                self.logger.info(f"Colorblind mode changed to: {accessibility_settings.colorblind_mode}")
                return True
            
            # Font size adjustment (Ctrl++ / Ctrl+-)
            elif event.key == pygame.K_EQUALS and pygame.key.get_pressed()[pygame.K_LCTRL]:
                accessibility_settings.font_scale = min(1.5, accessibility_settings.font_scale + 0.1)
                self.logger.info(f"Font scale increased to: {accessibility_settings.font_scale:.1f}")
                return True
            elif event.key == pygame.K_MINUS and pygame.key.get_pressed()[pygame.K_LCTRL]:
                accessibility_settings.font_scale = max(0.8, accessibility_settings.font_scale - 0.1)
                self.logger.info(f"Font scale decreased to: {accessibility_settings.font_scale:.1f}")
                return True
            
            # High contrast toggle (Ctrl+H)
            elif event.key == pygame.K_h and pygame.key.get_pressed()[pygame.K_LCTRL]:
                accessibility_settings.high_contrast = not accessibility_settings.high_contrast
                self.logger.info(f"High contrast mode: {accessibility_settings.high_contrast}")
                return True
            
            # Reduced motion toggle (Ctrl+M)
            elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_LCTRL]:
                accessibility_settings.reduced_motion = not accessibility_settings.reduced_motion
                self.logger.info(f"Reduced motion mode: {accessibility_settings.reduced_motion}")
                return True
            
            # End turn shortcut (Space or Enter)
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                state = self.combat_manager.get_combat_state()
                if state['phase'] == 'player_turn':
                    self.combat_manager.end_player_turn()
                    self.logger.info("Player ended turn via keyboard shortcut")
                    return True
            
            # Show accessibility help (F1)
            elif event.key == pygame.K_F1:
                self._show_accessibility_help()
                return True
        
        # Handle end turn button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self, 'end_turn_button_rect') and self.end_turn_button_rect.collidepoint(event.pos):
                state = self.combat_manager.get_combat_state()
                if state['phase'] == 'player_turn':
                    self.combat_manager.end_player_turn()
                    self.logger.info("Player ended turn via button click")
                    return True
        
        # Let parent handle other events
        return super().handle_event(event)
    
    def _setup_ui_components(self) -> None:
        """Set up Egyptian temple chamber layout with organized information architecture."""
        # Get combat data for information organization
        player_hourglass = self.combat_manager.player.hourglass if self.combat_manager.player else HourGlass()
        enemy_hourglass = self.combat_manager.enemy.hourglass if self.combat_manager.enemy else HourGlass()
        
        # Get screen dimensions for temple chamber layout
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        # Egyptian Temple Chamber Layout Implementation
        # Based on information architecture reorganization analysis
        
        # Zone 1: Sacred Antechamber (Top Status Bar) - 15% of screen height
        antechamber_height = int(screen_height * 0.15)
        
        # Zone 2: Canopic Chambers (Left/Right) - 25% each of screen width
        chamber_width = int(screen_width * 0.25)
        chamber_height = int(screen_height * 0.65)  # Exclude top and bottom zones
        chamber_y = antechamber_height
        
        # Zone 3: Central Sanctuary (Battlefield) - 50% of screen width
        sanctuary_width = screen_width - (chamber_width * 2)
        sanctuary_x = chamber_width
        
        # Zone 4: Hall of Offerings (Bottom) - 20% of screen height
        hall_height = int(screen_height * 0.20)
        hall_y = screen_height - hall_height
        
        # Create Western Canopic Chamber (Player Information)
        from .components.canopic_chamber import CanoplicChamber
        self.player_chamber = CanoplicChamber(
            10, chamber_y + 10, chamber_width - 20, chamber_height - 20, "player"
        )
        
        # Populate player chamber with organized information
        if self.combat_manager.player:
            self.player_chamber.set_information_slot('vital_status', self.combat_manager.player.health)
            self.player_chamber.set_information_slot('resource_level', player_hourglass)
            self.player_chamber.set_information_slot('active_effects', getattr(self.combat_manager.player, 'effects', []))
        
        self.add_component(self.player_chamber)
        
        # Create Eastern Canopic Chamber (Enemy Information)
        enemy_chamber_x = screen_width - chamber_width + 10
        self.enemy_chamber = CanoplicChamber(
            enemy_chamber_x, chamber_y + 10, chamber_width - 20, chamber_height - 20, "enemy"
        )
        
        # Populate enemy chamber with organized information
        if self.combat_manager.enemy:
            self.enemy_chamber.set_information_slot('vital_status', self.combat_manager.enemy.health)
            self.enemy_chamber.set_information_slot('resource_level', enemy_hourglass)
            self.enemy_chamber.set_information_slot('intent_preview', getattr(self.combat_manager, 'enemy_intent', None))
            self.enemy_chamber.set_information_slot('active_effects', getattr(self.combat_manager.enemy, 'effects', []))
        
        self.add_component(self.enemy_chamber)
        
        # Hall of Offerings (Enhanced Hand Display)
        hand_margin = 20
        hand_x = hand_margin
        hand_y = hall_y + 10
        hand_width = screen_width - (hand_margin * 2)
        hand_height = hall_height - 20
        
        self.hand_display = HandDisplay(hand_x, hand_y, hand_width, hand_height)
        self.hand_display.set_hourglass(player_hourglass)
        
        # Enhanced card interactions with Egyptian feedback
        self.hand_display.add_event_handler("card_played", self._on_card_played)
        self.hand_display.add_event_handler("card_play_failed", self._on_card_play_failed)
        self.hand_display.add_event_handler("card_drag_start", self._on_card_drag_start)
        self.hand_display.add_event_handler("card_drag_end", self._on_card_drag_end)
        self.add_component(self.hand_display)
        
        # Navigation and Action Buttons - Positioned within Hall of Offerings
        from .menu_screen import MenuButton
        button_width = 150
        button_height = 40
        
        # Back button (left side of Hall of Offerings)
        back_button_x = 30
        back_button_y = hall_y + hall_height - button_height - 15
        
        self.back_button = MenuButton(
            back_button_x, back_button_y, button_width, button_height,
            "< Back to Progression", self._back_to_progression
        )
        self.back_button.enable_egyptian_feedback('all')  # Enable Egyptian feedback
        self.add_component(self.back_button)
        
        # End Turn Button (right side of Hall of Offerings)
        button_x = screen_width - button_width - 30
        button_y = hall_y + hall_height - button_height - 15
        
        self.end_turn_button = MenuButton(
            button_x, button_y, button_width, button_height,
            "End Turn", self._on_end_turn
        )
        self.end_turn_button.enable_egyptian_feedback('all')  # Enable Egyptian feedback
        self.add_component(self.end_turn_button)
        
        # Legacy sand gauges for backward compatibility
        # These will be phased out as information moves into canopic chambers
        self.player_sand_gauge = None
        self.enemy_sand_gauge = None
    
    def _setup_demo_combat_manager(self) -> None:
        """Setup a demo combat scenario using the combat manager."""
        from sands_duat.content.starter_cards import create_starter_cards, get_starter_deck
        
        try:
            # Create cards and get starter deck
            create_starter_cards()
            deck = get_starter_deck()
            hand_cards = deck.draw(7)  # Draw 7 cards for demo
            
            # Setup combat with demo values
            self.combat_manager.setup_combat(
                player_health=100,
                player_max_health=100,
                enemy_name="Desert Mummy",
                enemy_health=60,
                enemy_max_health=60,
                player_cards=hand_cards
            )
            
            # Update UI with combat state
            self._update_ui_from_combat_state()
            
            self.logger.info("Demo combat setup complete")
            
        except Exception as e:
            self.logger.error(f"Failed to setup demo combat: {e}")
            # Fallback to basic setup
            self._setup_fallback_combat()
    
    def _setup_fallback_combat(self) -> None:
        """Setup a basic combat without complex dependencies."""
        from core.cards import Card, CardEffect, CardType, CardRarity, EffectType, TargetType
        
        # Create simple demo cards
        demo_cards = [
            Card(
                name="Strike",
                description="Deal 6 damage.",
                sand_cost=1,
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(effect_type=EffectType.DAMAGE, value=6, target=TargetType.ENEMY)]
            ),
            Card(
                name="Heal",
                description="Restore 8 health.",
                sand_cost=2,
                card_type=CardType.SKILL,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(effect_type=EffectType.HEAL, value=8, target=TargetType.SELF)]
            )
        ]
        
        # Setup basic combat
        self.combat_manager.setup_combat(
            player_health=100,
            player_max_health=100,
            enemy_name="Test Enemy",
            enemy_health=40,
            enemy_max_health=40,
            player_cards=demo_cards
        )
        
        self._update_ui_from_combat_state()
    
    def _setup_event_handlers(self) -> None:
        """Setup event handlers for combat events."""
        self.combat_manager.add_event_handler("combat_started", self._on_combat_started)
        self.combat_manager.add_event_handler("player_turn_started", self._on_player_turn_started)
        self.combat_manager.add_event_handler("enemy_turn_started", self._on_enemy_turn_started)
        self.combat_manager.add_event_handler("combat_ended", self._on_combat_ended)
    
    def _update_ui_from_combat_state(self) -> None:
        """Update UI components based on current combat state."""
        state = self.combat_manager.get_combat_state()
        
        # Update hand display
        if self.hand_display:
            self.hand_display.set_cards(self.combat_manager.player_hand)
            if self.combat_manager.player:
                self.hand_display.set_hourglass(self.combat_manager.player.hourglass)
        
        # Update sand gauges
        if self.player_sand_gauge and self.combat_manager.player:
            self.player_sand_gauge.hourglass = self.combat_manager.player.hourglass
        
        if self.enemy_sand_gauge and self.combat_manager.enemy:
            self.enemy_sand_gauge.hourglass = self.combat_manager.enemy.hourglass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the combat screen with enhanced theming."""
        # Render parallax background first
        if self.parallax_system:
            try:
                camera_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
                self.parallax_system.render(surface, camera_rect)
            except Exception as e:
                print(f"Combat parallax render error: {e}")
                # Fallback: Draw themed background
                self._draw_themed_background(surface)
        else:
            # Fallback: Draw themed background instead of basic clear
            self._draw_themed_background(surface)
        
        # Render atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.render(surface)
            except Exception as e:
                print(f"Combat atmospheric render error: {e}")
        
        # Render particle effects (behind other UI elements)
        self.particle_system.render(surface)
        
        # Draw main UI components
        super().render(surface)
        
        # Draw Egyptian battlefield atmosphere
        self._draw_battlefield_elements(surface)
        
        # Draw themed health bars
        self._draw_themed_health_bars(surface)
        
        # Draw professional character sprites
        self._draw_character_sprites(surface)
        
        # Draw combat status with better styling
        self._draw_enhanced_combat_status(surface)
        
        # Draw visual effects
        self._draw_visual_effects(surface)
        
        # Draw AI magical effects
        self._draw_ai_effects(surface)
        
        # Draw enemy intent with better styling
        self._draw_enhanced_enemy_intent(surface)
        
        # NOTE: Cards and end turn button are now rendered by base components
        # Removed duplicate enhanced drawing to fix double rendering bug on ultrawide displays
        
        # Draw atmospheric UI elements
        self._draw_atmospheric_elements(surface)
        
        # Draw particle count debug info (if enabled)
        self._draw_debug_info(surface)
        
        # Draw failure message if active
        self._draw_failure_message(surface)
    
    def _draw_failure_message(self, surface: pygame.Surface) -> None:
        """Draw failure message when card cannot be played."""
        if hasattr(self, 'failure_message_timer') and self.failure_message_timer > 0 and hasattr(self, 'failure_message'):
            font = pygame.font.Font(None, 36)
            
            # Calculate alpha based on remaining time
            alpha = min(255, int(self.failure_message_timer * 85))  # Fade out
            
            # Create text surface
            text_surface = font.render(self.failure_message, True, (255, 100, 100))
            
            # Add background for better readability
            bg_rect = text_surface.get_rect()
            bg_rect.inflate_ip(20, 10)
            bg_rect.centerx = surface.get_width() // 2
            bg_rect.y = surface.get_height() // 2 - 100
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(alpha // 2)
            bg_surface.fill((50, 20, 20))
            surface.blit(bg_surface, bg_rect)
            
            # Draw text
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect()
            text_rect.center = bg_rect.center
            surface.blit(text_surface, text_rect)
    
    def _draw_battlefield_elements(self, surface: pygame.Surface) -> None:
        """Draw Egyptian battlefield atmospheric elements in the central sanctuary."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Define central sanctuary zone (50% width, positioned between canopic chambers)
        antechamber_height = int(screen_height * 0.15)
        hall_height = int(screen_height * 0.20)
        chamber_width = int(screen_width * 0.25)
        
        # Central sanctuary positioning
        battlefield_x = chamber_width
        battlefield_y = antechamber_height
        battlefield_width = screen_width - (chamber_width * 2)
        battlefield_height = screen_height - antechamber_height - hall_height
        
        # Draw background sand dunes
        self._draw_sand_dunes(surface, battlefield_x, battlefield_y, battlefield_width, battlefield_height)
        
        # Draw temple columns flanking the battlefield
        self._draw_temple_columns(surface, battlefield_x, battlefield_y, battlefield_width, battlefield_height)
        
        # Draw central obelisk
        self._draw_central_obelisk(surface, battlefield_x, battlefield_y, battlefield_width, battlefield_height)
        
        # Draw hieroglyphic panels
        self._draw_hieroglyphic_panels(surface, battlefield_x, battlefield_y, battlefield_width, battlefield_height)
        
        # Draw atmospheric torch flames
        self._draw_torch_flames(surface, battlefield_x, battlefield_y, battlefield_width, battlefield_height)
    
    def _draw_sand_dunes(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw subtle sand dune silhouettes in background."""
        # Create gentle dune shapes
        dune_points = [
            (x, y + height - 50),
            (x + width // 4, y + height - 70),
            (x + width // 2, y + height - 60),
            (x + 3 * width // 4, y + height - 75),
            (x + width, y + height - 55),
            (x + width, y + height),
            (x, y + height)
        ]
        
        # Draw with warm sandstone gradient
        for i in range(len(dune_points) - 1):
            start_point = dune_points[i]
            end_point = dune_points[i + 1]
            
            # Subtle dune color (slightly darker than background)
            dune_color = (190, 160, 130, 80)
            dune_surface = pygame.Surface((abs(end_point[0] - start_point[0]), 20), pygame.SRCALPHA)
            dune_surface.fill(dune_color)
            surface.blit(dune_surface, (min(start_point[0], end_point[0]), start_point[1]))
    
    def _draw_temple_columns(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw Egyptian temple columns flanking the battlefield."""
        column_width = 60
        column_height = 180
        
        # Left column
        left_x = x + 40
        left_y = y + 60
        self._draw_single_column(surface, left_x, left_y, column_width, column_height)
        
        # Right column  
        right_x = x + width - column_width - 40
        right_y = y + 60
        self._draw_single_column(surface, right_x, right_y, column_width, column_height)
    
    def _draw_single_column(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw a single Egyptian papyrus-style column."""
        # Column base
        base_height = 20
        base_rect = pygame.Rect(x - 5, y + height - base_height, width + 10, base_height)
        pygame.draw.rect(surface, (160, 140, 110), base_rect)
        pygame.draw.rect(surface, (139, 117, 93), base_rect, 2)
        
        # Column shaft with vertical lines (fluted effect)
        shaft_rect = pygame.Rect(x, y + 30, width, height - 50)
        pygame.draw.rect(surface, (180, 155, 130), shaft_rect)
        pygame.draw.rect(surface, (139, 117, 93), shaft_rect, 2)
        
        # Add fluted lines
        for i in range(5):
            line_x = x + (i + 1) * width // 6
            pygame.draw.line(surface, (160, 140, 110), 
                           (line_x, y + 30), (line_x, y + height - 20), 1)
        
        # Papyrus capital (top)
        capital_height = 30
        capital_rect = pygame.Rect(x - 8, y, width + 16, capital_height)
        pygame.draw.ellipse(surface, (200, 180, 150), capital_rect)
        pygame.draw.ellipse(surface, (139, 117, 93), capital_rect, 2)
        
        # Papyrus bundle details on capital
        for i in range(3):
            bundle_x = x + i * width // 3 + width // 6
            pygame.draw.circle(surface, (180, 160, 130), (bundle_x, y + 15), 8)
            pygame.draw.circle(surface, (139, 117, 93), (bundle_x, y + 15), 8, 1)
    
    def _draw_central_obelisk(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw Egyptian obelisk serving as turn indicator and battlefield centerpiece."""
        # Get combat state for turn information
        state = self.combat_manager.get_combat_state()
        
        obelisk_width = 35
        obelisk_height = 140
        obelisk_x = x + width // 2 - obelisk_width // 2
        obelisk_y = y + height // 2 - obelisk_height // 2
        
        # Phase-based coloring for mystical significance
        if state['phase'] == 'player_turn':
            base_color = (200, 180, 150)  # Warm sandstone
            accent_color = (255, 215, 0)  # Gold
            glow_color = (255, 215, 0, 60)  # Golden glow
        else:
            base_color = (180, 150, 130)  # Cooler stone
            accent_color = (200, 100, 100)  # Muted red
            glow_color = (200, 100, 100, 60)  # Red glow
        
        # Enhanced obelisk body with traditional proportions
        obelisk_points = [
            (obelisk_x + obelisk_width // 2, obelisk_y),  # Pyramidion apex
            (obelisk_x + obelisk_width - 4, obelisk_y + 25),  # Pyramidion base
            (obelisk_x + obelisk_width - 2, obelisk_y + 30),  # Shaft top
            (obelisk_x + obelisk_width, obelisk_y + obelisk_height),  # Base corner
            (obelisk_x, obelisk_y + obelisk_height),  # Base corner
            (obelisk_x + 2, obelisk_y + 30),  # Shaft top
            (obelisk_x + 4, obelisk_y + 25)  # Pyramidion base
        ]
        
        pygame.draw.polygon(surface, base_color, obelisk_points)
        pygame.draw.polygon(surface, (139, 117, 93), obelisk_points, 2)
        
        # Pyramidion (turn indicator section)
        pyramidion_points = [
            (obelisk_x + obelisk_width // 2, obelisk_y),
            (obelisk_x + obelisk_width - 4, obelisk_y + 25),
            (obelisk_x + 4, obelisk_y + 25)
        ]
        pygame.draw.polygon(surface, accent_color, pyramidion_points)
        pygame.draw.polygon(surface, (139, 117, 93), pyramidion_points, 2)
        
        # Turn number hieroglyph in pyramidion
        turn_font = pygame.font.Font(None, 16)
        turn_text = str(state['turn_number'])
        turn_surface = turn_font.render(turn_text, True, (47, 27, 20))
        turn_rect = turn_surface.get_rect(center=(obelisk_x + obelisk_width // 2, obelisk_y + 15))
        surface.blit(turn_surface, turn_rect)
        
        # Phase indicator hieroglyphic symbols in shaft
        symbol_y_start = obelisk_y + 35
        phase_symbols = {
            'player_turn': [(0, "PLAYER"), (1, "◉"), (2, "♦")],  # Sun, diamond, dot
            'enemy_turn': [(0, "ENEMY"), (1, "▲"), (2, "●")],  # Triangle, circle
            'preparation': [(0, "PREP"), (1, "○"), (2, "◇")]  # Open circle, diamond
        }
        
        current_symbols = phase_symbols.get(state['phase'], phase_symbols['preparation'])
        
        for i, (symbol_index, symbol) in enumerate(current_symbols):
            symbol_y = symbol_y_start + i * 28
            
            if i == 0:  # Phase name in top section
                phase_font = pygame.font.Font(None, 12)
                phase_surface = phase_font.render(symbol, True, (120, 100, 80))
                phase_rect = phase_surface.get_rect(center=(obelisk_x + obelisk_width // 2, symbol_y))
                surface.blit(phase_surface, phase_rect)
            else:  # Symbolic hieroglyphs
                symbol_font = pygame.font.Font(None, 18)
                symbol_surface = symbol_font.render(symbol, True, (120, 100, 80))
                symbol_rect = symbol_surface.get_rect(center=(obelisk_x + obelisk_width // 2, symbol_y))
                surface.blit(symbol_surface, symbol_rect)
        
        # Enhanced mystical glow effect with phase-appropriate color
        import time
        glow_intensity = 0.4 + 0.15 * math.sin(time.time() * 2)
        glow_surface = pygame.Surface((obelisk_width + 25, obelisk_height + 25), pygame.SRCALPHA)
        
        # Create layered glow effect
        for layer in range(3):
            layer_alpha = int((glow_color[3] * glow_intensity) / (layer + 1))
            layer_size = (obelisk_width + 25 - layer * 5, obelisk_height + 25 - layer * 5)
            layer_surface = pygame.Surface(layer_size, pygame.SRCALPHA)
            layer_surface.fill((*glow_color[:3], layer_alpha))
            layer_x = obelisk_x - 12 + layer * 2
            layer_y = obelisk_y - 12 + layer * 2
            surface.blit(layer_surface, (layer_x, layer_y))
        
        # Base foundation stones
        base_y = obelisk_y + obelisk_height
        for i in range(3):
            stone_width = obelisk_width + (2 - i) * 4
            stone_x = obelisk_x - (2 - i) * 2
            stone_rect = pygame.Rect(stone_x, base_y + i * 3, stone_width, 4)
            pygame.draw.rect(surface, (160, 140, 110), stone_rect)
            pygame.draw.rect(surface, (139, 117, 93), stone_rect, 1)
    
    def _draw_hieroglyphic_panels(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw hieroglyphic panels at top and bottom of battlefield."""
        panel_height = 40
        
        # Top panel
        top_panel = pygame.Rect(x, y, width, panel_height)
        panel_surface = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((180, 155, 130, 60))
        surface.blit(panel_surface, (x, y))
        
        # Bottom panel
        bottom_panel = pygame.Rect(x, y + height - panel_height, width, panel_height)
        panel_surface = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((180, 155, 130, 60))
        surface.blit(panel_surface, (x, y + height - panel_height))
        
        # Add simple hieroglyphic symbols
        symbol_color = (120, 100, 80, 120)
        for i in range(width // 60):
            symbol_x = x + 30 + i * 60
            
            # Top panel symbols
            self._draw_simple_hieroglyph(surface, symbol_x, y + 10, symbol_color, i % 4)
            
            # Bottom panel symbols  
            self._draw_simple_hieroglyph(surface, symbol_x, y + height - 30, symbol_color, (i + 2) % 4)
    
    def _draw_simple_hieroglyph(self, surface: pygame.Surface, x: int, y: int, color: tuple, symbol_type: int) -> None:
        """Draw simple hieroglyphic symbols."""
        size = 20
        
        if symbol_type == 0:  # Ankh
            pygame.draw.line(surface, color[:3], (x + size//2, y), (x + size//2, y + size), 2)
            pygame.draw.line(surface, color[:3], (x + size//4, y + size//3), (x + 3*size//4, y + size//3), 2)
            pygame.draw.circle(surface, color[:3], (x + size//2, y + size//4), size//4, 1)
        elif symbol_type == 1:  # Eye
            pygame.draw.ellipse(surface, color[:3], (x + 2, y + size//3, size - 4, size//3), 1)
            pygame.draw.circle(surface, color[:3], (x + size//2, y + size//2), 3)
        elif symbol_type == 2:  # Scarab
            pygame.draw.ellipse(surface, color[:3], (x + 4, y + 4, size - 8, size - 8), 1)
            pygame.draw.line(surface, color[:3], (x + size//2, y + 4), (x + size//2, y + size - 4), 1)
        else:  # Cartouche
            pygame.draw.ellipse(surface, color[:3], (x + 2, y + 2, size - 4, size - 4), 1)
            pygame.draw.line(surface, color[:3], (x + size//4, y + size//2), (x + 3*size//4, y + size//2), 1)
    
    def _draw_torch_flames(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """Draw animated torch flames flanking the battlefield."""
        import time
        current_time = time.time()
        
        # Torch positions
        torch_positions = [
            (x + 70, y + 80),
            (x + width - 90, y + 80)
        ]
        
        for i, (torch_x, torch_y) in enumerate(torch_positions):
            # Torch base
            base_width = 12
            base_height = 30
            pygame.draw.rect(surface, (101, 67, 33), 
                           (torch_x - base_width//2, torch_y, base_width, base_height))
            
            # Animated flame
            flame_offset = 5 * math.sin(current_time * 3 + i)
            flame_intensity = 0.8 + 0.2 * math.sin(current_time * 4 + i)
            
            # Flame colors (orange to yellow)
            flame_colors = [
                (255, int(140 * flame_intensity), 0),
                (255, int(200 * flame_intensity), 50),
                (255, 255, int(100 * flame_intensity))
            ]
            
            # Draw flame layers for depth
            for layer, color in enumerate(flame_colors):
                flame_height = 25 - layer * 5
                flame_width = 8 - layer * 2
                flame_y = torch_y - flame_height + flame_offset
                
                # Create flame shape (triangle with some variation)
                flame_points = [
                    (torch_x, flame_y),
                    (torch_x - flame_width//2, torch_y),
                    (torch_x + flame_width//2, torch_y)
                ]
                
                # Draw flame with transparency
                flame_surface = pygame.Surface((flame_width, flame_height), pygame.SRCALPHA)
                pygame.draw.polygon(flame_surface, (*color, 180), 
                                  [(p[0] - torch_x + flame_width//2, p[1] - flame_y) for p in flame_points])
                surface.blit(flame_surface, (torch_x - flame_width//2, flame_y))
    
    def _draw_health_bars(self, surface: pygame.Surface) -> None:
        """Draw large, visible health bars and game status."""
        state = self.combat_manager.get_combat_state()
        
        # Draw large, prominent health bars
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Player health bar (bottom left)
        player_bar_width = 300
        player_bar_height = 40
        player_x = 50
        player_y = screen_height - 200
        
        # Player health background
        player_bg_rect = pygame.Rect(player_x, player_y, player_bar_width, player_bar_height)
        pygame.draw.rect(surface, (100, 0, 0), player_bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), player_bg_rect, 3)
        
        # Player health fill
        health_percent = state['player']['health'] / max(1, state['player']['max_health'])
        health_width = int(player_bar_width * health_percent)
        health_rect = pygame.Rect(player_x, player_y, health_width, player_bar_height)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)
        
        # Player health text
        font = pygame.font.Font(None, 36)
        health_text = f"PLAYER: {state['player']['health']}/{state['player']['max_health']} HP"
        text_surface = font.render(health_text, True, (255, 255, 255))
        surface.blit(text_surface, (player_x, player_y - 35))
        
        # Player sand display
        sand_text = f"SAND: {state['player']['sand']}/{state['player']['max_sand']}"
        sand_surface = font.render(sand_text, True, (255, 215, 0))
        surface.blit(sand_surface, (player_x, player_y + player_bar_height + 10))
        
        # Enemy health bar (top right)
        enemy_bar_width = 300
        enemy_bar_height = 40
        enemy_x = screen_width - enemy_bar_width - 50
        enemy_y = 200
        
        # Enemy health background
        enemy_bg_rect = pygame.Rect(enemy_x, enemy_y, enemy_bar_width, enemy_bar_height)
        pygame.draw.rect(surface, (100, 0, 0), enemy_bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), enemy_bg_rect, 3)
        
        # Enemy health fill
        enemy_health_percent = state['enemy']['health'] / max(1, state['enemy']['max_health'])
        enemy_health_width = int(enemy_bar_width * enemy_health_percent)
        enemy_health_rect = pygame.Rect(enemy_x, enemy_y, enemy_health_width, enemy_bar_height)
        pygame.draw.rect(surface, (255, 0, 0), enemy_health_rect)
        
        # Enemy health text
        enemy_health_text = f"{state['enemy']['name']}: {state['enemy']['health']}/{state['enemy']['max_health']} HP"
        enemy_text_surface = font.render(enemy_health_text, True, (255, 255, 255))
        surface.blit(enemy_text_surface, (enemy_x, enemy_y - 35))
        
        # Combat status
        status_font = pygame.font.Font(None, 48)
        phase_text = f"PHASE: {state['phase'].upper()}"
        if state['phase'] == 'player_turn':
            phase_color = (0, 255, 0)
            phase_text += " - YOUR TURN!"
        else:
            phase_color = (255, 0, 0)
            phase_text += " - ENEMY TURN"
        
        phase_surface = status_font.render(phase_text, True, phase_color)
        phase_rect = phase_surface.get_rect(centerx=screen_width//2, y=300)
        surface.blit(phase_surface, phase_rect)
    
    def _draw_health_bar(self, surface: pygame.Surface, rect: pygame.Rect, 
                        current: int, maximum: int, color: Tuple[int, int, int], label: str) -> None:
        """Draw a health bar."""
        # Background
        pygame.draw.rect(surface, (50, 50, 50), rect)
        
        # Health bar
        if maximum > 0:
            health_width = int(rect.width * (current / maximum))
            health_rect = pygame.Rect(rect.x, rect.y, health_width, rect.height)
            pygame.draw.rect(surface, color, health_rect)
        
        # Border
        pygame.draw.rect(surface, (200, 200, 200), rect, 2)
        
        # Text
        text = f"{label}: {current}/{maximum}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.bottom = rect.top - 5
        surface.blit(text_surface, text_rect)
    
    def _draw_combat_status(self, surface: pygame.Surface) -> None:
        """Draw combat status information."""
        state = self.combat_manager.get_combat_state()
        
        # Combat phase indicator
        phase_text = f"Turn {state['turn_number']} - {state['phase'].replace('_', ' ').title()}"
        text_surface = self.font.render(phase_text, True, self.text_color)
        surface.blit(text_surface, (surface.get_width() // 2 - text_surface.get_width() // 2, 20))
        
        # Block indicators
        if state['player']['block'] > 0:
            block_text = f"Block: {state['player']['block']}"
            block_surface = self.font.render(block_text, True, (100, 150, 255))
            surface.blit(block_surface, (50, 500))
        
        if state['enemy']['block'] > 0:
            enemy_block_text = f"Block: {state['enemy']['block']}"
            enemy_block_surface = self.font.render(enemy_block_text, True, (100, 150, 255))
            surface.blit(enemy_block_surface, (750, 150))
    
    def _draw_visual_effects(self, surface: pygame.Surface) -> None:
        """Draw floating damage numbers and other effects."""
        font = pygame.font.Font(None, 32)
        
        for effect in self.damage_numbers:
            color = (*effect['color'], int(effect['alpha']))
            text_surface = font.render(effect['text'], True, effect['color'])
            
            # Create alpha surface for fading
            alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            alpha_surface.fill(color)
            alpha_surface.blit(text_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            surface.blit(alpha_surface, (effect['x'], effect['y']))
    
    def _draw_ai_effects(self, surface: pygame.Surface) -> None:
        """Draw AI magical effects"""
        try:
            from ..graphics.ai_effects_system import get_ai_effects
            effects_system = get_ai_effects()
            effects_system.update(1/60)  # Assume 60 FPS
            effects_system.render(surface)
        except Exception as e:
            # Fail silently - effects are optional
            pass
    
    def _draw_enemy_intent(self, surface: pygame.Surface) -> None:
        """Draw enemy intent indicator."""
        if not self.combat_manager.enemy_intent:
            return
        
        intent = self.combat_manager.enemy_intent
        font = pygame.font.Font(None, 20)
        
        # Draw intent above enemy
        text = f"Intent: {intent.name}"
        text_surface = font.render(text, True, (255, 255, 100))
        
        # Position above enemy area
        x = 600  # Enemy area
        y = 50
        
        surface.blit(text_surface, (x, y))
    
    def _on_card_played(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle enhanced card play with effects."""
        card = event_data.get("card")
        if card:
            # Use CombatManager to handle card playing (includes sand cost validation and spending)
            if self.combat_manager.play_card(card):
                self.logger.info(f"Successfully played card: {card.name} (cost: {card.sand_cost})")
                
                # Sync the display hourglass with combat manager
                if self.player_hourglass and self.combat_manager.player:
                    self.player_hourglass.set_sand(self.combat_manager.player.hourglass.current_sand)
                
                # Trigger visual effects
                self._trigger_card_play_effects(card)
                
                # Trigger AI magical effects
                self._trigger_ai_card_effects(card)
                
                # Trigger character animations
                self._trigger_character_animations(card)
                
            else:
                self.logger.info(f"Cannot play card: {card.name} (cost: {card.sand_cost})")
                # Show visual feedback for failed card play
                self._show_card_play_failure_feedback(card)
    
    def _on_card_play_failed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card play failure (e.g., not enough sand)."""
        card = event_data.get("card")
        if card:
            self.logger.info(f"Card play failed: {card.name} (cost: {card.sand_cost})")
            self._show_card_play_failure_feedback(card)
    
    def _show_card_play_failure_feedback(self, card: Card) -> None:
        """Show visual feedback when card cannot be played."""
        # Add a temporary message showing why the card couldn't be played
        if hasattr(self, 'failure_message_timer'):
            self.failure_message_timer = 3.0  # Show for 3 seconds
        else:
            self.failure_message_timer = 3.0
        
        current_sand = self.combat_manager.player.hourglass.current_sand if self.combat_manager.player else 0
        self.failure_message = f"Need {card.sand_cost} sand, have {current_sand}"
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag start."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Started dragging card: {card.name}")
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag end."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Stopped dragging card: {card.name}")
    
    def _trigger_card_play_effects(self, card: Card) -> None:
        """Trigger visual/audio effects for card play."""
        # Add visual effects based on card type
        if card.card_type == CardType.ATTACK:
            # Could trigger screen shake, damage numbers, etc.
            pass
        elif card.card_type == CardType.SKILL:
            # Could trigger particle effects, etc.
            pass
        
        # Log for now (in future could trigger particle systems)
    
    def _trigger_ai_card_effects(self, card: Card) -> None:
        """Trigger AI magical effects when card is played"""
        try:
            from ..graphics.ai_effects_system import get_ai_effects
            effects_system = get_ai_effects()
            
            # Get screen center for effect positioning
            screen_center_x = self.rect.width // 2
            screen_center_y = self.rect.height // 2
            
            # Create card-specific magical effect
            effects_system.create_card_cast_effect(screen_center_x, screen_center_y, card.name)
            
            self.logger.debug(f"Triggered AI effects for card: {card.name}")
            
        except Exception as e:
            self.logger.warning(f"Failed to trigger AI card effects: {e}")
        self.logger.debug(f"Triggered visual effects for {card.card_type.value} card")
    
    def _trigger_character_animations(self, card: Card) -> None:
        """Trigger character sprite animations based on card type."""
        if not self.player_sprite:
            return
        
        # Determine animation based on card type
        if card.card_type == CardType.ATTACK:
            # Player attacks
            self.player_sprite.set_state(AnimationState.ATTACK, force_restart=True)
            
            # Enemy takes damage (could add hurt animation later)
            if self.enemy_sprite:
                # For now, just make enemy flash or step back slightly
                pass
                
        elif card.card_type == CardType.DEFENSE:
            # Defensive stance
            self.player_sprite.set_state(AnimationState.IDLE, force_restart=True)
            
        elif card.card_type == CardType.MAGIC:
            # Casting animation (use attack for now, could add cast later)
            self.player_sprite.set_state(AnimationState.ATTACK, force_restart=True)
            
        elif card.card_type == CardType.SUPPORT:
            # Support gesture
            self.player_sprite.set_state(AnimationState.IDLE, force_restart=True)
        
        self.logger.debug(f"Triggered character animation for {card.card_type.value} card")
    
    def update(self, delta_time: float) -> None:
        """Update combat screen and all systems."""
        super().update(delta_time)
        
        # Update combat manager
        self.combat_manager.update(delta_time)
        
        # Update professional character sprites
        if self.player_sprite:
            self.player_sprite.update(delta_time)
        if self.enemy_sprite:
            self.enemy_sprite.update(delta_time)
        
        # Update particle system
        self.particle_system.update(delta_time)
        
        # Update visual effects
        self._update_visual_effects(delta_time)
        
        # Update parallax system
        if self.parallax_system:
            try:
                self.parallax_system.update(delta_time)
            except Exception as e:
                print(f"Combat parallax update error: {e}")
        
        # Update atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.update(delta_time)
            except Exception as e:
                print(f"Combat atmospheric update error: {e}")
        
        # Process pending combat effects
        self._process_combat_effects()
        
        # Update UI state based on combat phase
        self._update_ui_state()
        
        # Update sand particle effects based on hourglass states
        self._update_sand_particles(delta_time)
        
        # Update failure message timer
        if hasattr(self, 'failure_message_timer') and self.failure_message_timer > 0:
            self.failure_message_timer -= delta_time
    
    def _update_visual_effects(self, delta_time: float) -> None:
        """Update visual effects like damage numbers."""
        # Update damage numbers
        for effect in self.damage_numbers[:]:
            effect['life'] -= delta_time
            effect['y'] -= 50 * delta_time  # Float upward
            effect['alpha'] = max(0, effect['alpha'] - 200 * delta_time)
            
            if effect['life'] <= 0 or effect['alpha'] <= 0:
                self.damage_numbers.remove(effect)
        
        # Update other effect animations
        for effect in self.effect_animations[:]:
            effect['time'] += delta_time
            if effect['time'] >= effect['duration']:
                self.effect_animations.remove(effect)
    
    def _process_combat_effects(self) -> None:
        """Process pending combat effects from combat manager."""
        effects = self.combat_manager.get_pending_effects()
        
        for effect in effects:
            effect_type = effect['type']
            data = effect['data']
            
            if effect_type == 'damage':
                self._show_damage_number(data['amount'], data['target'])
                # Trigger damage particle effect
                target_pos = self._get_entity_position(data['target'])
                if target_pos:
                    self.trigger_damage_effect(target_pos[0], target_pos[1], data['amount'])
            elif effect_type == 'heal':
                self._show_heal_number(data['amount'], data['target'])
                # Trigger heal particle effect
                target_pos = self._get_entity_position(data['target'])
                if target_pos:
                    self.trigger_heal_effect(target_pos[0], target_pos[1], data['amount'])
            elif effect_type == 'block':
                self._show_block_effect(data['amount'], data['target'])
                # Trigger sand burst for block
                target_pos = self._get_entity_position(data['target'])
                if target_pos:
                    self.trigger_sand_burst(target_pos[0], target_pos[1], data['amount'] // 2)
    
    def _update_ui_state(self) -> None:
        """Update UI components based on combat state."""
        state = self.combat_manager.get_combat_state()
        
        # Update end turn button visibility
        if self.end_turn_button:
            is_player_turn = state['phase'] == 'player_turn' and state['turn_phase'] == 'main'
            self.end_turn_button.visible = is_player_turn
        
        # Update hand display
        if self.hand_display:
            self.hand_display.set_cards(self.combat_manager.player_hand)
    
    def _on_end_turn(self) -> None:
        """Handle end turn button click."""
        self.combat_manager.end_player_turn()
    
    def _back_to_progression(self) -> None:
        """Return to progression screen."""
        self.logger.info("Returning to progression screen from combat")
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("progression", "slide_right")
        else:
            self._trigger_event("switch_screen", {"screen": "progression"})
    
    def _show_damage_number(self, amount: int, target) -> None:
        """Show floating damage number."""
        # Determine position based on target
        if target == self.combat_manager.player:
            x, y = 300, 400  # Player area
        else:
            x, y = 500, 200  # Enemy area
        
        self.damage_numbers.append({
            'text': str(amount),
            'x': x,
            'y': y,
            'alpha': 255,
            'life': 2.0,
            'color': (255, 100, 100)  # Red for damage
        })
    
    def _show_heal_number(self, amount: int, target) -> None:
        """Show floating heal number."""
        if target == self.combat_manager.player:
            x, y = 300, 400
        else:
            x, y = 500, 200
        
        self.damage_numbers.append({
            'text': f"+{amount}",
            'x': x,
            'y': y,
            'alpha': 255,
            'life': 2.0,
            'color': (100, 255, 100)  # Green for healing
        })
    
    def _show_block_effect(self, amount: int, target) -> None:
        """Show block effect."""
        # Add visual effect for block gain
        pass
    
    # Combat event handlers
    def _on_combat_started(self, data: Dict[str, Any]) -> None:
        """Handle combat start event."""
        self.logger.info("Combat started!")
        self._update_ui_from_combat_state()
    
    def _on_player_turn_started(self, data: Dict[str, Any]) -> None:
        """Handle player turn start."""
        turn = data['turn']
        self.logger.info(f"Player turn {turn} started")
    
    def _on_enemy_turn_started(self, data: Dict[str, Any]) -> None:
        """Handle enemy turn start."""
        enemy = data['enemy']
        intent = data.get('intent')
        
        if intent:
            self.logger.info(f"{enemy.name} intends to use {intent.name}")
        else:
            self.logger.info(f"{enemy.name} is waiting...")
    
    def _on_combat_ended(self, data: Dict[str, Any]) -> None:
        """Handle combat end event."""
        victory = data['victory']
        turns = data['turns']
        
        # Get game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        
        if victory:
            self.logger.info(f"Victory! Combat lasted {turns} turns")
            
            # Create basic rewards
            rewards = {
                'gold': 20 + (turns * 2),  # Base gold + turn bonus
                'cards': [],  # No card rewards for now
                'health': 0   # No healing by default
            }
            
            # Prepare victory data
            victory_data = {
                'turns': turns,
                'gold_earned': rewards['gold'],
                'total_gold': 120 + rewards['gold'],  # Base + earned
                'run_completed': False  # Regular combat, not final boss
            }
            
            if game_flow:
                game_flow.handle_combat_victory(rewards)
                
                # Set victory data on victory screen
                victory_screen = self.ui_manager.screens.get("victory") if self.ui_manager else None
                if victory_screen:
                    victory_screen.set_victory_data(victory_data)
            else:
                # Fallback: show victory screen directly
                if self.ui_manager:
                    victory_screen = self.ui_manager.screens.get("victory")
                    if victory_screen:
                        victory_screen.set_victory_data(victory_data)
                    self.ui_manager.switch_to_screen_with_transition("victory", "fade")
        else:
            self.logger.info(f"Defeat! Combat lasted {turns} turns")
            
            # Prepare defeat data
            defeat_data = {
                'turns_survived': turns,
                'damage_dealt': 50,  # Could track this in combat manager
                'cards_played': 10,  # Could track this too
                'hours_reached': 1,
                'cause_of_death': 'Desert Mummy'
            }
            
            if game_flow:
                game_flow.handle_combat_defeat()
                
                # Set defeat data on defeat screen
                defeat_screen = self.ui_manager.screens.get("defeat") if self.ui_manager else None
                if defeat_screen:
                    defeat_screen.set_defeat_data(defeat_data)
            else:
                # Fallback: show defeat screen directly
                if self.ui_manager:
                    defeat_screen = self.ui_manager.screens.get("defeat")
                    if defeat_screen:
                        defeat_screen.set_defeat_data(defeat_data)
                    self.ui_manager.switch_to_screen_with_transition("defeat", "fade")
    
    def set_player_cards(self, cards: List[Card]) -> None:
        """Set the player's hand (legacy method - now handled by combat manager)."""
        if self.hand_display:
            self.hand_display.set_cards(cards)
    
    def _update_sand_particles(self, delta_time: float) -> None:
        """Update sand particle effects based on hourglass states."""
        theme = get_theme()
        
        # Get sand gauge positions for particle emission
        try:
            player_zone = theme.get_zone('player_sand')
            enemy_zone = theme.get_zone('enemy_sand')
        except:
            # Fallback positioning
            player_zone = type('Zone', (), {'x': 50, 'y': 400, 'width': 200, 'height': 200})()
            enemy_zone = type('Zone', (), {'x': 750, 'y': 100, 'width': 200, 'height': 200})()
        
        # Create atmospheric sand particles
        if random.random() < 0.1:  # 10% chance per frame (reduced for performance)
            # Random atmospheric sand using proper Particle class
            from .particle_system import Particle
            
            x = random.uniform(0, 3440)
            y = random.uniform(-50, 0)
            
            particle = Particle(
                x=x, y=y,
                vel_x=random.uniform(-20, 20),
                vel_y=random.uniform(10, 40),
                size=random.uniform(0.5, 1.5),
                life=random.uniform(3.0, 8.0),
                max_life=5.0,
                color=(255, 215, random.randint(0, 100)),
                alpha=random.randint(50, 150),
                gravity=random.uniform(5, 15),
                fade_rate=0.5,
                particle_type=ParticleType.ATMOSPHERIC
            )
            
            self.particle_system.particles.append(particle)
        
        # Add sand flow effects between hourglasses during regeneration
        if hasattr(self, 'player_hourglass') and self.player_hourglass:
            if self.player_hourglass.current_sand < self.player_hourglass.max_sand:
                # Sand flowing into player hourglass
                flow_x = player_zone.x + player_zone.width // 2
                flow_y = player_zone.y - 20
                self.particle_system.create_sand_flow_effect(
                    flow_x, flow_y - 50, flow_x, flow_y + 100, intensity=0.5
                )
    
    
    def _draw_debug_info(self, surface: pygame.Surface) -> None:
        """Draw debug information including particle count and accessibility status."""
        if hasattr(self, 'debug_mode') and self.debug_mode:
            font = pygame.font.Font(None, 24)
            particle_count = self.particle_system.get_particle_count()
            debug_text = f"Particles: {particle_count}"
            text_surface = font.render(debug_text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10))
        
        # Always show accessibility status if any features are active
        if (accessibility_settings.colorblind_mode != "none" or 
            accessibility_settings.font_scale != 1.0 or 
            accessibility_settings.high_contrast or 
            accessibility_settings.reduced_motion):
            
            font = pygame.font.Font(None, 20)
            y_offset = 40
            
            # Show active accessibility features
            if accessibility_settings.colorblind_mode != "none":
                mode_text = f"Colorblind: {accessibility_settings.colorblind_mode}"
                text_surface = font.render(mode_text, True, (200, 255, 200))
                surface.blit(text_surface, (10, y_offset))
                y_offset += 25
            
            if accessibility_settings.font_scale != 1.0:
                scale_text = f"Font Scale: {accessibility_settings.font_scale:.1f}x"
                text_surface = font.render(scale_text, True, (200, 255, 200))
                surface.blit(text_surface, (10, y_offset))
                y_offset += 25
            
            if accessibility_settings.high_contrast:
                contrast_text = "High Contrast: ON"
                text_surface = font.render(contrast_text, True, (200, 255, 200))
                surface.blit(text_surface, (10, y_offset))
                y_offset += 25
            
            if accessibility_settings.reduced_motion:
                motion_text = "Reduced Motion: ON"
                text_surface = font.render(motion_text, True, (200, 255, 200))
                surface.blit(text_surface, (10, y_offset))
    
    def _show_accessibility_help(self) -> None:
        """Log accessibility help information to console."""
        help_text = """
=== ACCESSIBILITY CONTROLS ===
Ctrl+C: Toggle colorblind mode (none/protanopia/deuteranopia/tritanopia)
Ctrl++: Increase font size
Ctrl+-: Decrease font size  
Ctrl+H: Toggle high contrast mode
Ctrl+M: Toggle reduced motion mode
Space/Enter: End turn
F1: Show this help

Current Settings:
- Colorblind Mode: {colorblind}
- Font Scale: {scale:.1f}x
- High Contrast: {contrast}
- Reduced Motion: {motion}
        """.format(
            colorblind=accessibility_settings.colorblind_mode,
            scale=accessibility_settings.font_scale,
            contrast="ON" if accessibility_settings.high_contrast else "OFF",
            motion="ON" if accessibility_settings.reduced_motion else "OFF"
        )
        
        self.logger.info(help_text)
        print(help_text)  # Also print to console for immediate visibility
    
    def trigger_damage_effect(self, x: float, y: float, damage: int) -> None:
        """Trigger visual damage effect at position."""
        self.particle_system.create_combat_hit_effect(x, y, damage)
        
        # Add floating damage number
        self.damage_numbers.append({
            'text': str(damage),
            'x': x,
            'y': y,
            'vel_y': -50,
            'life': 2.0,
            'alpha': 255,
            'color': (255, 100, 100)
        })
    
    def trigger_heal_effect(self, x: float, y: float, healing: int) -> None:
        """Trigger visual healing effect at position."""
        self.particle_system.create_heal_effect(x, y, healing)
        
        # Add floating heal number
        self.damage_numbers.append({
            'text': f"+{healing}",
            'x': x,
            'y': y,
            'vel_y': -30,
            'life': 2.0,
            'alpha': 255,
            'color': (100, 255, 100)
        })
    
    def trigger_sand_burst(self, x: float, y: float, sand_amount: int) -> None:
        """Trigger sand burst effect when sand is gained or spent."""
        # Create sand emitter for burst effect
        emitter = ParticleEmitter(x, y, ParticleType.SAND_GRAIN)
        emitter.emission_rate = 0  # Don't emit continuously
        emitter.color = (255, 215, 0)
        emitter.velocity_range = (30, 100)
        emitter.life_range = (1.0, 2.5)
        
        # Create burst particles
        burst_particles = emitter.burst(sand_amount * 3)
        self.particle_system.particles.extend(burst_particles)
    
    def _get_entity_position(self, entity) -> Optional[Tuple[float, float]]:
        """Get screen position for an entity for particle effects."""
        theme = get_theme()
        
        if entity and hasattr(entity, 'is_player'):
            if entity.is_player:
                # Player position
                try:
                    player_zone = theme.get_zone('player_area')
                    return (player_zone.x + player_zone.width // 2, 
                           player_zone.y + player_zone.height // 2)
                except:
                    return (400, 700)  # Fallback player position
            else:
                # Enemy position
                try:
                    enemy_zone = theme.get_zone('enemy_area')
                    return (enemy_zone.x + enemy_zone.width // 2, 
                           enemy_zone.y + enemy_zone.height // 2)
                except:
                    return (800, 300)  # Fallback enemy position
        
        return None
    
    def _draw_game_title(self, surface: pygame.Surface) -> None:
        """Draw game title and instructions."""
        theme = get_theme()
        
        # Draw main title
        title_font = theme.fonts.get_font('large')
        title_text = "SANDS OF DUAT"
        title_surface = title_font.render(title_text, True, theme.colors.GOLD)
        title_rect = title_surface.get_rect(centerx=surface.get_width() // 2, y=20)
        surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_font = theme.fonts.get_font('medium')
        subtitle_text = "Hour-Glass Initiative Combat"
        subtitle_surface = subtitle_font.render(subtitle_text, True, theme.colors.PAPYRUS)
        subtitle_rect = subtitle_surface.get_rect(centerx=surface.get_width() // 2, y=title_rect.bottom + 5)
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw instructions
        instruction_font = theme.fonts.get_font('small')
        instructions = [
            "Drag cards UP to play them",
            "Watch your sand regenerate over time", 
            "Defeat the enemy to win!",
            "ESC to exit (dev mode)"
        ]
        
        start_y = subtitle_rect.bottom + 20
        for i, instruction in enumerate(instructions):
            instruction_surface = instruction_font.render(instruction, True, theme.colors.PAPYRUS)
            instruction_rect = instruction_surface.get_rect(centerx=surface.get_width() // 2, y=start_y + i * 25)
            surface.blit(instruction_surface, instruction_rect)
    
    def _draw_cards_simple(self, surface: pygame.Surface) -> None:
        """Draw cards in hand with large, visible display."""
        if not self.combat_manager.player_hand:
            return
        
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Card dimensions
        card_width = 120
        card_height = 160
        card_spacing = 20
        
        # Calculate starting position to center cards
        total_width = len(self.combat_manager.player_hand) * (card_width + card_spacing) - card_spacing
        start_x = (screen_width - total_width) // 2
        card_y = screen_height - card_height - 50
        
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        for i, card in enumerate(self.combat_manager.player_hand):
            if i >= 6:  # Limit displayed cards
                break
                
            card_x = start_x + i * (card_width + card_spacing)
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            # Determine if card is playable
            can_play = self.combat_manager.player and self.combat_manager.player.hourglass.can_afford(card.sand_cost)
            
            # Card background
            if can_play:
                bg_color = (0, 100, 0)  # Green if playable
                border_color = (0, 255, 0)
            else:
                bg_color = (100, 0, 0)  # Red if not playable
                border_color = (255, 0, 0)
            
            pygame.draw.rect(surface, bg_color, card_rect)
            pygame.draw.rect(surface, border_color, card_rect, 3)
            
            # Card name
            name_surface = font.render(card.name[:10], True, (255, 255, 255))
            name_rect = name_surface.get_rect(centerx=card_rect.centerx, y=card_rect.y + 10)
            surface.blit(name_surface, name_rect)
            
            # Sand cost
            cost_text = f"Cost: {card.sand_cost}"
            cost_surface = small_font.render(cost_text, True, (255, 215, 0))
            cost_rect = cost_surface.get_rect(centerx=card_rect.centerx, y=card_rect.y + 35)
            surface.blit(cost_surface, cost_rect)
            
            # Card description (truncated)
            desc_lines = card.description.split(' ')
            desc_text = ' '.join(desc_lines[:4]) + "..."
            desc_surface = small_font.render(desc_text[:15], True, (200, 200, 200))
            desc_rect = desc_surface.get_rect(centerx=card_rect.centerx, y=card_rect.y + 55)
            surface.blit(desc_surface, desc_rect)
            
            # Play instruction
            if can_play:
                play_text = "DRAG UP"
                play_color = (255, 255, 0)
            else:
                play_text = "NO SAND"
                play_color = (255, 100, 100)
            
            play_surface = small_font.render(play_text, True, play_color)
            play_rect = play_surface.get_rect(centerx=card_rect.centerx, y=card_rect.bottom - 25)
            surface.blit(play_surface, play_rect)
    
    def _draw_end_turn_button(self, surface: pygame.Surface) -> None:
        """Draw a large, visible end turn button."""
        state = self.combat_manager.get_combat_state()
        
        # Only show during player turn
        if state['phase'] != 'player_turn':
            return
        
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Button dimensions and position
        button_width = 200
        button_height = 60
        button_x = screen_width - button_width - 50
        button_y = screen_height - button_height - 50
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Button background
        pygame.draw.rect(surface, (100, 100, 0), button_rect)
        pygame.draw.rect(surface, (255, 255, 0), button_rect, 4)
        
        # Button text
        font = pygame.font.Font(None, 36)
        button_text = "END TURN"
        text_surface = font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Store button rect for click detection
        self.end_turn_button_rect = button_rect
    
    def _draw_themed_background(self, surface: pygame.Surface) -> None:
        """Draw improved Egyptian-themed background with warm sandstone palette."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Create warm gradient from sandstone to deeper papyrus
        for y in range(screen_height):
            ratio = y / screen_height
            # Top: Warm sandstone, Bottom: Deeper papyrus
            r = int(212 - ratio * 12)  # 212 to 200 (sandstone to papyrus)
            g = int(184 - ratio * 5)   # 184 to 179
            b = int(150 - ratio * 6)   # 150 to 144
            pygame.draw.line(surface, (r, g, b), (0, y), (screen_width, y))
        
        # Add subtle sandstone texture lines
        for i in range(0, screen_height, 50):
            alpha = 40 if i % 100 == 0 else 20
            # Warmer texture color
            color = (180, 155, 120, alpha)
            texture_surface = pygame.Surface((screen_width, 2), pygame.SRCALPHA)
            texture_surface.fill(color)
            surface.blit(texture_surface, (0, i))
        
        # Add subtle papyrus fiber texture
        import random
        random.seed(42)  # Consistent pattern
        for _ in range(15):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            length = random.randint(20, 60)
            thickness = random.randint(1, 2)
            alpha = random.randint(15, 35)
            
            # Papyrus fiber color
            fiber_color = (190, 170, 130, alpha)
            fiber_surface = pygame.Surface((length, thickness), pygame.SRCALPHA)
            fiber_surface.fill(fiber_color)
            surface.blit(fiber_surface, (x, y))
        
        # Add some atmospheric sand particles in background
        import random
        random.seed(42)  # Consistent pattern
        for _ in range(20):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            size = random.randint(1, 3)
            alpha = random.randint(20, 60)
            particle_color = (139, 117, 93, alpha)
            particle_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, (size, size), size)
            surface.blit(particle_surface, (x, y))
    
    def _draw_themed_health_bars(self, surface: pygame.Surface) -> None:
        """Draw health bars with Egyptian theming and accessibility support."""
        state = self.combat_manager.get_combat_state()
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Player health area (left side with ornate frame)
        player_x = 30
        player_y = screen_height - 180
        player_width = 320
        player_height = 80
        
        # Draw ornate frame background with accessible colors
        frame_color = accessibility_settings.get_color((139, 117, 93))
        inner_color = accessibility_settings.get_color((60, 45, 30))
        
        # Outer frame
        player_frame = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(surface, frame_color, player_frame, border_radius=8)
        
        # Inner area
        inner_frame = player_frame.inflate(-8, -8)
        pygame.draw.rect(surface, inner_color, inner_frame, border_radius=5)
        
        # Health bar with accessible colors
        health_bar_rect = pygame.Rect(player_x + 15, player_y + 25, player_width - 30, 20)
        bg_color = accessibility_settings.get_color((40, 20, 20))
        pygame.draw.rect(surface, bg_color, health_bar_rect, border_radius=3)
        
        health_percent = state['player']['health'] / max(1, state['player']['max_health'])
        health_width = int((player_width - 30) * health_percent)
        if health_width > 0:
            health_fill = pygame.Rect(player_x + 15, player_y + 25, health_width, 20)
            # Accessible gradient health bar
            for i in range(health_width):
                ratio = i / max(1, health_width)
                base_r = int(80 + ratio * 100)  # Red gradient
                base_g = int(200 - ratio * 150)  # Green gradient 
                base_b = 20
                accessible_color = accessibility_settings.get_color((base_r, base_g, base_b))
                pygame.draw.line(surface, accessible_color, 
                               (health_fill.x + i, health_fill.y), 
                               (health_fill.x + i, health_fill.bottom))
        
        # Player health text with accessible font size
        font_size = accessibility_settings.get_font_size(28)
        font = pygame.font.Font(None, font_size)
        health_text = f"PLAYER: {state['player']['health']}/{state['player']['max_health']}"
        text_color = accessibility_settings.get_color((255, 215, 0))
        text_surface = font.render(health_text, True, text_color)
        surface.blit(text_surface, (player_x + 15, player_y + 5))
        
        # Sand display with accessible styling
        sand_text = f"SAND: {state['player']['sand']}/{state['player']['max_sand']}"
        sand_font_size = accessibility_settings.get_font_size(24)
        sand_color = accessibility_settings.get_color((255, 215, 0))
        sand_surface = pygame.font.Font(None, sand_font_size).render(sand_text, True, sand_color)
        surface.blit(sand_surface, (player_x + 15, player_y + 50))
        
        # Enemy health area (right side)
        enemy_x = screen_width - 350
        enemy_y = 100
        enemy_width = 320
        enemy_height = 80
        
        # Enemy frame (darker, more menacing) with accessible colors
        enemy_frame_color = accessibility_settings.get_color((80, 60, 40))
        enemy_inner_color = accessibility_settings.get_color((40, 25, 15))
        
        enemy_frame = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        pygame.draw.rect(surface, enemy_frame_color, enemy_frame, border_radius=8)
        
        enemy_inner = enemy_frame.inflate(-8, -8)
        pygame.draw.rect(surface, enemy_inner_color, enemy_inner, border_radius=5)
        
        # Enemy health bar with accessible colors
        enemy_health_rect = pygame.Rect(enemy_x + 15, enemy_y + 25, enemy_width - 30, 20)
        enemy_bg_color = accessibility_settings.get_color((40, 20, 20))
        pygame.draw.rect(surface, enemy_bg_color, enemy_health_rect, border_radius=3)
        
        enemy_health_percent = state['enemy']['health'] / max(1, state['enemy']['max_health'])
        enemy_health_width = int((enemy_width - 30) * enemy_health_percent)
        if enemy_health_width > 0:
            enemy_health_fill = pygame.Rect(enemy_x + 15, enemy_y + 25, enemy_health_width, 20)
            # Accessible red health bar for enemy
            for i in range(enemy_health_width):
                ratio = i / max(1, enemy_health_width)
                base_r = int(150 + ratio * 80)
                base_g = int(50 - ratio * 30)
                base_b = int(50 - ratio * 30)
                accessible_color = accessibility_settings.get_color((base_r, base_g, base_b))
                pygame.draw.line(surface, accessible_color,
                               (enemy_health_fill.x + i, enemy_health_fill.y),
                               (enemy_health_fill.x + i, enemy_health_fill.bottom))
        
        # Enemy health text with accessible styling
        enemy_health_text = f"{state['enemy']['name']}: {state['enemy']['health']}/{state['enemy']['max_health']}"
        enemy_text_color = accessibility_settings.get_color((255, 100, 100))
        enemy_text_surface = font.render(enemy_health_text, True, enemy_text_color)
        surface.blit(enemy_text_surface, (enemy_x + 15, enemy_y + 5))
        
        # Enemy type/description
        if hasattr(state['enemy'], 'description'):
            desc_font_size = accessibility_settings.get_font_size(16)
            desc_font = pygame.font.Font(None, desc_font_size)
            desc_color = accessibility_settings.get_color((180, 180, 180))
            desc_text = state['enemy']['description'][:40]  # Limit length
            desc_surface = desc_font.render(desc_text, True, desc_color)
            surface.blit(desc_surface, (enemy_x + 15, enemy_y + 50))
        
        # Draw enemy status effects (if any)
        if hasattr(state['enemy'], 'status_effects') and state['enemy']['status_effects']:
            status_y = enemy_y + enemy_height + 10
            self._draw_enemy_status_effects(surface, enemy_x, status_y, state['enemy']['status_effects'])
    
    def _draw_character_sprites(self, surface: pygame.Surface) -> None:
        """Draw professional character sprites from asset pipeline."""
        # Render player sprite
        if self.player_sprite:
            self.player_sprite.render(surface)
        
        # Render enemy sprite
        if self.enemy_sprite:
            self.enemy_sprite.render(surface)
        
        # Fallback to old method if sprites not available
        if not self.player_sprite or not self.enemy_sprite:
            self._draw_enemy_character_fallback(surface)
    
    def _draw_enemy_character_fallback(self, surface: pygame.Surface) -> None:
        """Fallback enemy drawing method."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Enemy position (center-right)
        enemy_center_x = screen_width - 200
        enemy_center_y = screen_height // 2 - 50
        
        # Draw Desert Mummy representation
        state = self.combat_manager.get_combat_state()
        enemy_name = state['enemy']['name']
        
        if "Mummy" in enemy_name:
            self._draw_mummy_character(surface, enemy_center_x, enemy_center_y)
        else:
            self._draw_generic_enemy(surface, enemy_center_x, enemy_center_y)
    
    def _draw_mummy_character(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw a stylized mummy character."""
        # Mummy body (wrapped figure)
        body_width = 60
        body_height = 120
        body_rect = pygame.Rect(x - body_width//2, y - body_height//2, body_width, body_height)
        
        # Base body
        pygame.draw.ellipse(surface, (139, 117, 93), body_rect)
        pygame.draw.ellipse(surface, (160, 140, 110), body_rect.inflate(-4, -4))
        
        # Wrapping lines
        for i in range(5):
            wrap_y = body_rect.top + 15 + i * 20
            pygame.draw.line(surface, (100, 80, 60), 
                           (body_rect.left, wrap_y), 
                           (body_rect.right, wrap_y), 3)
        
        # Head
        head_radius = 25
        head_center = (x, y - body_height//2 - 15)
        pygame.draw.circle(surface, (139, 117, 93), head_center, head_radius)
        pygame.draw.circle(surface, (160, 140, 110), head_center, head_radius - 2)
        
        # Eyes (glowing)
        eye_color = (255, 100, 100) if random.random() > 0.8 else (200, 80, 80)
        left_eye = (head_center[0] - 8, head_center[1] - 3)
        right_eye = (head_center[0] + 8, head_center[1] - 3)
        pygame.draw.circle(surface, eye_color, left_eye, 4)
        pygame.draw.circle(surface, eye_color, right_eye, 4)
        
        # Arms
        arm_length = 40
        left_arm_end = (x - body_width//2 - 20, y)
        right_arm_end = (x + body_width//2 + 20, y)
        
        pygame.draw.line(surface, (139, 117, 93), 
                        (x - body_width//2, y - 10), left_arm_end, 8)
        pygame.draw.line(surface, (139, 117, 93), 
                        (x + body_width//2, y - 10), right_arm_end, 8)
        
        # Add floating sand particles around the mummy
        for i in range(8):
            angle = i * (math.pi * 2 / 8) + time.time() * 2
            orbit_x = x + math.cos(angle) * 80
            orbit_y = y + math.sin(angle) * 40
            particle_size = 2 + int(math.sin(time.time() * 3 + i) * 1)
            pygame.draw.circle(surface, (255, 215, 0, 100), 
                             (int(orbit_x), int(orbit_y)), particle_size)
    
    def _draw_generic_enemy(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw a generic enemy placeholder."""
        # Simple shadowy figure
        pygame.draw.circle(surface, (80, 60, 40), (x, y), 50)
        pygame.draw.circle(surface, (60, 40, 20), (x, y), 45)
        
        # Glowing eyes
        pygame.draw.circle(surface, (255, 100, 100), (x - 15, y - 10), 5)
        pygame.draw.circle(surface, (255, 100, 100), (x + 15, y - 10), 5)
    
    def _draw_enhanced_combat_status(self, surface: pygame.Surface) -> None:
        """Combat status is now integrated into the central obelisk turn indicator."""
        # Turn indicator functionality moved to _draw_central_obelisk()
        # This method preserved for backward compatibility but no longer renders separate status
        pass
    
    def _draw_enhanced_enemy_intent(self, surface: pygame.Surface) -> None:
        """Draw enhanced enemy intent with detailed information and accessibility support."""
        if not self.combat_manager.enemy_intent:
            return
        
        intent = self.combat_manager.enemy_intent
        screen_width = surface.get_width()
        
        # Intent display area (larger for more information)
        intent_x = screen_width - 350
        intent_y = 200
        intent_width = 320
        intent_height = 120
        
        # Background with accessible colors
        bg_color = accessibility_settings.get_color((60, 20, 20))
        border_color = accessibility_settings.get_color((255, 100, 100))
        
        intent_rect = pygame.Rect(intent_x, intent_y, intent_width, intent_height)
        bg_surface = pygame.Surface((intent_width, intent_height), pygame.SRCALPHA)
        bg_surface.fill((*bg_color, 200))
        surface.blit(bg_surface, (intent_x, intent_y))
        pygame.draw.rect(surface, border_color, intent_rect, 2, border_radius=8)
        
        # Title
        title_font_size = accessibility_settings.get_font_size(20)
        title_font = pygame.font.Font(None, title_font_size)
        title_text = "ENEMY INTENT"
        title_color = accessibility_settings.get_color((255, 215, 0))
        title_surface = title_font.render(title_text, True, title_color)
        surface.blit(title_surface, (intent_x + 10, intent_y + 5))
        
        # Intent name with accessible styling
        name_font_size = accessibility_settings.get_font_size(24)
        name_font = pygame.font.Font(None, name_font_size)
        name_text = intent.name.upper()
        name_color = accessibility_settings.get_color((255, 255, 100))
        name_surface = name_font.render(name_text, True, name_color)
        surface.blit(name_surface, (intent_x + 10, intent_y + 30))
        
        # Intent details
        detail_font_size = accessibility_settings.get_font_size(18)
        detail_font = pygame.font.Font(None, detail_font_size)
        detail_color = accessibility_settings.get_color((200, 200, 200))
        
        # Show damage/effect amount if available
        if hasattr(intent, 'damage') and intent.damage:
            damage_text = f"Damage: {intent.damage}"
            damage_surface = detail_font.render(damage_text, True, accessibility_settings.get_color((255, 150, 150)))
            surface.blit(damage_surface, (intent_x + 10, intent_y + 55))
        
        if hasattr(intent, 'effect') and intent.effect:
            effect_text = f"Effect: {intent.effect}"
            effect_surface = detail_font.render(effect_text, True, accessibility_settings.get_color((150, 255, 150)))
            surface.blit(effect_surface, (intent_x + 10, intent_y + 75))
        
        # Intent icon/symbol (simple visual indicator)
        icon_size = 30
        icon_x = intent_x + intent_width - icon_size - 10
        icon_y = intent_y + 10
        icon_color = accessibility_settings.get_color((255, 100, 100))
        
        # Draw different symbols based on intent type
        if hasattr(intent, 'type'):
            if intent.type == 'attack':
                # Draw sword symbol (simple lines)
                pygame.draw.line(surface, icon_color, 
                               (icon_x + 5, icon_y + 25), (icon_x + 25, icon_y + 5), 3)
                pygame.draw.line(surface, icon_color,
                               (icon_x + 10, icon_y + 20), (icon_x + 20, icon_y + 10), 2)
            elif intent.type == 'defend':
                # Draw shield symbol
                shield_points = [(icon_x + 15, icon_y + 5), (icon_x + 25, icon_y + 15), 
                               (icon_x + 25, icon_y + 20), (icon_x + 15, icon_y + 25),
                               (icon_x + 5, icon_y + 20), (icon_x + 5, icon_y + 15)]
                pygame.draw.polygon(surface, icon_color, shield_points)
            else:
                # Default: warning triangle
                triangle_points = [(icon_x + 15, icon_y + 5), (icon_x + 25, icon_y + 25), (icon_x + 5, icon_y + 25)]
                pygame.draw.polygon(surface, icon_color, triangle_points)
    
    def _draw_enemy_status_effects(self, surface: pygame.Surface, x: int, y: int, status_effects: Dict[str, Any]) -> None:
        """Draw enemy status effects with icons and duration."""
        if not status_effects:
            return
        
        effect_width = 40
        effect_height = 30
        spacing = 5
        current_x = x + 15
        
        for effect_name, effect_data in status_effects.items():
            # Background for status effect
            effect_rect = pygame.Rect(current_x, y, effect_width, effect_height)
            
            # Choose color based on effect type
            if effect_name.lower() in ['poison', 'bleed', 'burn', 'weakness']:
                bg_color = accessibility_settings.get_color((120, 40, 40))  # Red for debuffs
                text_color = accessibility_settings.get_color((255, 150, 150))
            else:
                bg_color = accessibility_settings.get_color((40, 120, 40))  # Green for buffs
                text_color = accessibility_settings.get_color((150, 255, 150))
            
            pygame.draw.rect(surface, bg_color, effect_rect, border_radius=3)
            pygame.draw.rect(surface, text_color, effect_rect, 1, border_radius=3)
            
            # Effect duration or stacks
            duration = effect_data.get('duration', effect_data.get('stacks', 1))
            duration_font_size = accessibility_settings.get_font_size(16)
            duration_font = pygame.font.Font(None, duration_font_size)
            duration_text = str(duration)
            duration_surface = duration_font.render(duration_text, True, text_color)
            
            # Center text in effect box
            text_rect = duration_surface.get_rect(center=effect_rect.center)
            surface.blit(duration_surface, text_rect)
            
            current_x += effect_width + spacing
        
        # Status effects label
        if status_effects:
            label_font_size = accessibility_settings.get_font_size(14)
            label_font = pygame.font.Font(None, label_font_size)
            label_text = "Status Effects:"
            label_color = accessibility_settings.get_color((200, 200, 200))
            label_surface = label_font.render(label_text, True, label_color)
            surface.blit(label_surface, (x + 15, y - 20))
    
    def _draw_enhanced_cards(self, surface: pygame.Surface) -> None:
        """Draw enhanced card display with better theming."""
        if not self.combat_manager.player_hand:
            return
        
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Card area background
        card_area_height = 200
        card_area_y = screen_height - card_area_height
        
        # Draw improved papyrus-style background for card area
        card_bg_rect = pygame.Rect(0, card_area_y, screen_width, card_area_height)
        card_bg_surface = pygame.Surface((screen_width, card_area_height), pygame.SRCALPHA)
        # Use warmer papyrus color
        card_bg_surface.fill((200, 185, 156, 140))  # Papyrus with transparency
        surface.blit(card_bg_surface, (0, card_area_y))
        
        # Enhanced decorative border with Egyptian styling
        border_color = (139, 117, 93)
        pygame.draw.line(surface, border_color, 
                        (0, card_area_y), (screen_width, card_area_y), 4)
        
        # Add subtle texture to border
        for i in range(0, screen_width, 20):
            pygame.draw.line(surface, (160, 140, 110), 
                           (i, card_area_y - 1), (i + 10, card_area_y - 1), 1)
        
        # Draw cards with enhanced styling
        self._draw_cards_simple(surface)  # Use existing card drawing for now
    
    def _draw_styled_end_turn_button(self, surface: pygame.Surface) -> None:
        """Draw end turn button with Egyptian styling."""
        state = self.combat_manager.get_combat_state()
        
        if state['phase'] != 'player_turn':
            return
        
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Button position and size
        button_width = 160
        button_height = 50
        button_x = screen_width - button_width - 40
        button_y = screen_height - button_height - 40
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Ornate button background
        pygame.draw.rect(surface, (139, 117, 93), button_rect, border_radius=8)
        inner_rect = button_rect.inflate(-6, -6)
        pygame.draw.rect(surface, (100, 80, 60), inner_rect, border_radius=5)
        
        # Highlight border
        pygame.draw.rect(surface, (255, 215, 0), button_rect, 3, border_radius=8)
        
        # Button text with shadow
        font = pygame.font.Font(None, 32)
        button_text = "END TURN"
        
        # Text shadow
        shadow_surface = font.render(button_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = font.render(button_text, True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Store for click detection
        self.end_turn_button_rect = button_rect
    
    def _draw_atmospheric_elements(self, surface: pygame.Surface) -> None:
        """Draw atmospheric elements like floating particles and environmental effects."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Floating sand particles
        current_time = time.time()
        for i in range(15):
            # Create floating particles with sine wave motion
            base_x = (i * 200) % screen_width
            base_y = (i * 150) % screen_height
            
            offset_x = math.sin(current_time * 0.5 + i) * 30
            offset_y = math.cos(current_time * 0.3 + i) * 20
            
            particle_x = int(base_x + offset_x)
            particle_y = int(base_y + offset_y)
            
            # Varying particle sizes and colors
            size = 1 + int(math.sin(current_time * 2 + i) * 1)
            alpha = int(30 + math.sin(current_time + i) * 20)
            
            particle_color = (255, 215, 0, max(10, alpha))
            if size > 0:
                particle_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, (size, size), size)
                surface.blit(particle_surface, (particle_x, particle_y))
        
        # Corner decorative elements (Egyptian-style corners)
        corner_size = 60
        corner_color = (139, 117, 93, 100)
        
        # Top corners
        for x, y in [(20, 20), (screen_width - corner_size - 20, 20)]:
            corner_surface = pygame.Surface((corner_size, corner_size), pygame.SRCALPHA)
            # Draw simple hieroglyph-like patterns
            pygame.draw.lines(corner_surface, corner_color, False, 
                            [(10, 10), (30, 10), (30, 30), (50, 30)], 3)
            pygame.draw.lines(corner_surface, corner_color, False,
                            [(10, 50), (30, 50), (30, 30)], 3)
            surface.blit(corner_surface, (x, y))