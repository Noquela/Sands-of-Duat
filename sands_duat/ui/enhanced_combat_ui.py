"""
Enhanced Combat UI - Immersive Egyptian Underworld Interface

Provides enhanced combat screen elements with Egyptian theming,
improved visual feedback, and better information hierarchy.
"""

import pygame
import math
import time
from typing import List, Dict, Optional, Any, Tuple
from .base import UIComponent
from .hades_theme import HadesEgyptianTheme
from ..core.hourglass import HourGlass
from ..core.cards import Card
from ..core.combat_manager import CombatManager


class EnhancedSandGauge(UIComponent):
    """Enhanced hourglass sand gauge with Egyptian visual effects."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 hourglass: HourGlass, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hourglass = hourglass
        self.hades_theme = hades_theme
        self.animation_time = 0.0
        self.sand_particles = []
        self.last_sand_count = 0
        
        # Visual enhancement settings
        self.glass_shimmer = 0.0
        self.sand_flow_particles = []
        self.mystical_aura = 0.0
    
    def update(self, delta_time: float) -> None:
        """Update enhanced sand gauge with mystical effects."""
        super().update(delta_time)
        self.animation_time += delta_time
        
        # Update hourglass state
        self.hourglass.update_sand()
        
        # Mystical aura pulsing
        self.mystical_aura = 0.5 + 0.5 * math.sin(self.animation_time * 1.5)
        
        # Glass shimmer effect
        self.glass_shimmer = 0.3 + 0.7 * abs(math.sin(self.animation_time * 2.0))
        
        # Sand flow particle system
        self._update_sand_flow_particles(delta_time)
        
        # Check for sand changes
        current_sand = self.hourglass.current_sand
        if current_sand != self.last_sand_count:
            if current_sand > self.last_sand_count:
                self._trigger_sand_gain_effect()
            else:
                self._trigger_sand_flow_effect()
            self.last_sand_count = current_sand
    
    def _update_sand_flow_particles(self, delta_time: float):
        """Update flowing sand particle effects."""
        # Remove old particles
        self.sand_flow_particles = [p for p in self.sand_flow_particles if p['life'] > 0]
        
        # Update existing particles
        for particle in self.sand_flow_particles:
            particle['y'] += particle['vy'] * delta_time * 60
            particle['life'] -= delta_time
            particle['alpha'] = max(0, 255 * (particle['life'] / particle['max_life']))
        
        # Add new particles if sand is flowing
        if self.hourglass.time_until_next_grain < 0.5:  # About to gain sand
            self._spawn_flow_particle()
    
    def _spawn_flow_particle(self):
        """Spawn a new sand flow particle."""
        import random
        
        center_x = self.rect.centerx
        top_sand_y = self.rect.y + 30
        
        particle = {
            'x': center_x + random.randint(-5, 5),
            'y': top_sand_y,
            'vy': random.uniform(20, 40),
            'life': random.uniform(1.0, 2.0),
            'max_life': 2.0,
            'alpha': 255,
            'size': random.randint(1, 3)
        }
        self.sand_flow_particles.append(particle)
    
    def _trigger_sand_gain_effect(self):
        """Trigger visual effect for sand gain."""
        # Add burst of particles
        import random
        for _ in range(8):
            particle = {
                'x': self.rect.centerx + random.randint(-10, 10),
                'y': self.rect.centery + random.randint(-10, 10),
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-50, -20),
                'life': random.uniform(0.8, 1.5),
                'max_life': 1.5,
                'alpha': 255,
                'size': random.randint(2, 4)
            }
            self.sand_particles.append(particle)
    
    def _trigger_sand_flow_effect(self):
        """Trigger visual effect for sand flowing."""
        # Pulse the mystical aura
        self.mystical_aura = 1.0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render enhanced sand gauge with Egyptian mystical effects."""
        if not self.visible:
            return
        
        # Draw mystical aura background
        self._draw_mystical_aura(surface)
        
        # Draw hourglass structure with enhanced details
        self._draw_enhanced_hourglass(surface)
        
        # Draw sand with particle effects
        self._draw_enhanced_sand(surface)
        
        # Draw flowing sand particles
        self._draw_sand_particles(surface)
        
        # Draw hieroglyphic decorations
        self._draw_hieroglyphic_decorations(surface)
        
        # Draw sand count with Egyptian styling
        self._draw_sand_counter(surface)
    
    def _draw_mystical_aura(self, surface: pygame.Surface):
        """Draw mystical aura around the hourglass."""
        aura_surface = pygame.Surface((self.rect.width + 40, self.rect.height + 40), pygame.SRCALPHA)
        
        # Multiple aura rings
        for ring in range(3):
            radius = 20 + ring * 8
            alpha = int(self.mystical_aura * (80 - ring * 20))
            aura_color = (*self.hades_theme.get_color('sacred_turquoise'), alpha)
            
            pygame.draw.circle(aura_surface, aura_color, 
                             (aura_surface.get_width()//2, aura_surface.get_height()//2), 
                             radius, 2)
        
        surface.blit(aura_surface, (self.rect.x - 20, self.rect.y - 20))
    
    def _draw_enhanced_hourglass(self, surface: pygame.Surface):
        """Draw hourglass with enhanced Egyptian styling."""
        # Main frame with bronze material
        frame_color = self.hades_theme.get_color('pharaoh_bronze')
        
        # Hourglass outline with decorative elements
        center_x = self.rect.centerx
        center_y = self.rect.centery
        width = self.rect.width - 20
        height = self.rect.height - 20
        
        # Top and bottom bulbs
        top_rect = pygame.Rect(center_x - width//3, self.rect.y + 10, 2*width//3, height//3)
        bottom_rect = pygame.Rect(center_x - width//3, self.rect.bottom - 10 - height//3, 2*width//3, height//3)
        
        # Glass effect with shimmer
        glass_alpha = int(self.glass_shimmer * 150)
        glass_color = (*self.hades_theme.get_color('sacred_turquoise'), glass_alpha)
        
        pygame.draw.ellipse(surface, glass_color, top_rect)
        pygame.draw.ellipse(surface, glass_color, bottom_rect)
        pygame.draw.ellipse(surface, frame_color, top_rect, 3)
        pygame.draw.ellipse(surface, frame_color, bottom_rect, 3)
        
        # Connecting neck with decorative patterns
        neck_points = [
            (center_x - width//6, top_rect.bottom),
            (center_x + width//6, top_rect.bottom),
            (center_x + width//6, bottom_rect.top),
            (center_x - width//6, bottom_rect.top)
        ]
        pygame.draw.polygon(surface, glass_color, neck_points)
        pygame.draw.polygon(surface, frame_color, neck_points, 2)
        
        # Decorative Egyptian patterns on frame
        self._draw_frame_decorations(surface, top_rect, bottom_rect)
    
    def _draw_frame_decorations(self, surface: pygame.Surface, top_rect: pygame.Rect, bottom_rect: pygame.Rect):
        """Draw Egyptian decorative patterns on hourglass frame."""
        decoration_color = self.hades_theme.get_color('duat_gold')
        
        # Ankh symbols on sides
        ankh_size = 8
        left_ankh_pos = (top_rect.left - 15, top_rect.centery)
        right_ankh_pos = (top_rect.right + 15, top_rect.centery)
        
        self.hades_theme._draw_transition_ankh(surface, left_ankh_pos, ankh_size, (*decoration_color, 255))
        self.hades_theme._draw_transition_ankh(surface, right_ankh_pos, ankh_size, (*decoration_color, 255))
        
        # Scarab beetles on bottom
        scarab_y = bottom_rect.bottom + 10
        for i in range(3):
            scarab_x = bottom_rect.left + (i + 1) * (bottom_rect.width // 4)
            self._draw_scarab_decoration(surface, (scarab_x, scarab_y), 4, decoration_color)
    
    def _draw_scarab_decoration(self, surface: pygame.Surface, center: Tuple[int, int], 
                               size: int, color: Tuple[int, int, int]):
        """Draw small scarab beetle decoration."""
        x, y = center
        
        # Scarab body
        body_rect = pygame.Rect(x - size, y - size//2, size * 2, size)
        pygame.draw.ellipse(surface, color, body_rect)
        
        # Wings
        wing_size = size // 2
        pygame.draw.circle(surface, color, (x - size//2, y), wing_size)
        pygame.draw.circle(surface, color, (x + size//2, y), wing_size)
    
    def _draw_enhanced_sand(self, surface: pygame.Surface):
        """Draw sand with enhanced visual effects."""
        if self.hourglass.current_sand <= 0:
            return
        
        # Calculate sand levels
        sand_ratio = self.hourglass.current_sand / self.hourglass.max_sand
        
        # Top chamber sand (decreasing)
        top_sand_height = int((self.rect.height // 3 - 20) * (1 - sand_ratio))
        if top_sand_height > 0:
            top_sand_rect = pygame.Rect(
                self.rect.centerx - (self.rect.width//3 - 10),
                self.rect.y + 20 + (self.rect.height//3 - 20 - top_sand_height),
                2 * (self.rect.width//3 - 10),
                top_sand_height
            )
            self._draw_sand_pile(surface, top_sand_rect, "top")
        
        # Bottom chamber sand (increasing)
        bottom_sand_height = int((self.rect.height // 3 - 20) * sand_ratio)
        if bottom_sand_height > 0:
            bottom_sand_rect = pygame.Rect(
                self.rect.centerx - (self.rect.width//3 - 10),
                self.rect.bottom - 20 - (self.rect.height//3 - 10) + (self.rect.height//3 - 20 - bottom_sand_height),
                2 * (self.rect.width//3 - 10),
                bottom_sand_height
            )
            self._draw_sand_pile(surface, bottom_sand_rect, "bottom")
    
    def _draw_sand_pile(self, surface: pygame.Surface, rect: pygame.Rect, position: str):
        """Draw individual sand pile with texture and glow."""
        base_color = self.hades_theme.get_color('desert_amber')
        
        # Add glow effect
        glow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        glow_alpha = int(100 * self.mystical_aura)
        glow_color = (*base_color, glow_alpha)
        pygame.draw.ellipse(glow_surface, glow_color, (5, 5, rect.width, rect.height))
        surface.blit(glow_surface, (rect.x - 5, rect.y - 5))
        
        # Main sand pile
        if position == "top":
            # Conical shape for top chamber
            points = [
                (rect.centerx, rect.bottom),
                (rect.left, rect.top),
                (rect.right, rect.top)
            ]
            pygame.draw.polygon(surface, base_color, points)
        else:
            # Inverted cone for bottom chamber
            points = [
                (rect.centerx, rect.top),
                (rect.left, rect.bottom),
                (rect.right, rect.bottom)
            ]
            pygame.draw.polygon(surface, base_color, points)
        
        # Add sand texture
        self._add_sand_texture(surface, rect)
    
    def _add_sand_texture(self, surface: pygame.Surface, rect: pygame.Rect):
        """Add subtle sand grain texture."""
        import random
        
        # Use consistent seed for stable texture
        random.seed(rect.x + rect.y)
        
        for _ in range(rect.width * rect.height // 100):
            x = random.randint(rect.left, rect.right)
            y = random.randint(rect.top, rect.bottom)
            
            if rect.collidepoint(x, y):
                brightness = random.randint(-20, 20)
                base_color = self.hades_theme.get_color('desert_amber')
                grain_color = tuple(max(0, min(255, c + brightness)) for c in base_color)
                pygame.draw.circle(surface, grain_color, (x, y), 1)
    
    def _draw_sand_particles(self, surface: pygame.Surface):
        """Draw flowing sand particles."""
        for particle in self.sand_flow_particles:
            if particle['alpha'] > 0:
                particle_color = (*self.hades_theme.get_color('desert_amber'), int(particle['alpha']))
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, 
                                 (particle['size'], particle['size']), particle['size'])
                surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _draw_hieroglyphic_decorations(self, surface: pygame.Surface):
        """Draw animated hieroglyphic decorations around the gauge."""
        # Rotating hieroglyphs around the hourglass
        num_glyphs = 6
        radius = self.rect.width // 2 + 25
        
        for i in range(num_glyphs):
            angle = (self.animation_time * 0.5 + i * (2 * math.pi / num_glyphs))
            x = self.rect.centerx + radius * math.cos(angle)
            y = self.rect.centery + radius * math.sin(angle)
            
            # Fade based on distance and time
            fade = 0.5 + 0.5 * math.sin(self.animation_time * 2 + i)
            alpha = int(fade * 150)
            
            glyph_color = (*self.hades_theme.get_color('sacred_turquoise'), alpha)
            
            # Alternate between different hieroglyphs
            if i % 2 == 0:
                self.hades_theme._draw_transition_ankh(surface, (int(x), int(y)), 8, glyph_color)
            else:
                self.hades_theme._draw_transition_eye(surface, (int(x), int(y)), 6, glyph_color)
    
    def _draw_sand_counter(self, surface: pygame.Surface):
        """Draw sand count with Egyptian styling."""
        # Background papyrus scroll
        counter_rect = pygame.Rect(self.rect.centerx - 30, self.rect.bottom + 10, 60, 25)
        self.hades_theme.draw_ornate_button(surface, counter_rect, "", "normal")
        
        # Sand count text
        font_size = self.hades_theme.get_font_size('body')
        font = pygame.font.Font(None, font_size)
        
        sand_text = f"{self.hourglass.current_sand}/{self.hourglass.max_sand}"
        text_surface = font.render(sand_text, True, self.hades_theme.get_color('papyrus_cream'))
        text_rect = text_surface.get_rect(center=counter_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Next sand timer
        if self.hourglass.time_until_next_grain > 0:
            timer_text = f"Next: {self.hourglass.time_until_next_grain:.1f}s"
            timer_font = pygame.font.Font(None, 14)
            timer_surface = timer_font.render(timer_text, True, self.hades_theme.get_color('desert_amber'))
            timer_rect = timer_surface.get_rect(center=(counter_rect.centerx, counter_rect.bottom + 12))
            surface.blit(timer_surface, timer_rect)


class EnhancedCombatFeedback(UIComponent):
    """Enhanced visual feedback system for combat actions."""
    
    def __init__(self, x: int, y: int, width: int, height: int, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hades_theme = hades_theme
        self.active_effects = []
        self.screen_shake = 0.0
        self.flash_overlay = 0.0
    
    def add_damage_number(self, damage: int, position: Tuple[int, int], 
                         damage_type: str = "normal"):
        """Add floating damage number with Egyptian styling."""
        effect = {
            'type': 'damage_number',
            'value': damage,
            'position': list(position),
            'velocity': [0, -50],  # Float upward
            'life': 2.0,
            'max_life': 2.0,
            'damage_type': damage_type,
            'scale': 1.0
        }
        self.active_effects.append(effect)
    
    def add_healing_effect(self, amount: int, position: Tuple[int, int]):
        """Add healing visual effect."""
        effect = {
            'type': 'healing',
            'value': amount,
            'position': list(position),
            'velocity': [0, -30],
            'life': 2.5,
            'max_life': 2.5,
            'particles': self._create_healing_particles(position)
        }
        self.active_effects.append(effect)
    
    def add_card_play_effect(self, card: Card, position: Tuple[int, int]):
        """Add visual effect for card being played."""
        effect = {
            'type': 'card_play',
            'card': card,
            'position': list(position),
            'life': 1.5,
            'max_life': 1.5,
            'ring_radius': 0,
            'particles': self._create_card_particles(card, position)
        }
        self.active_effects.append(effect)
    
    def trigger_screen_shake(self, intensity: float = 1.0):
        """Trigger screen shake effect."""
        self.screen_shake = max(self.screen_shake, intensity)
    
    def trigger_flash_overlay(self, color: Tuple[int, int, int], intensity: float = 0.8):
        """Trigger flash overlay effect."""
        self.flash_overlay = intensity
        self.flash_color = color
    
    def _create_healing_particles(self, position: Tuple[int, int]) -> List[Dict]:
        """Create healing particle effect."""
        import random
        particles = []
        
        for _ in range(12):
            particle = {
                'x': position[0] + random.randint(-20, 20),
                'y': position[1] + random.randint(-20, 20),
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-50, -20),
                'life': random.uniform(1.0, 2.0),
                'max_life': 2.0,
                'size': random.randint(2, 5)
            }
            particles.append(particle)
        
        return particles
    
    def _create_card_particles(self, card: Card, position: Tuple[int, int]) -> List[Dict]:
        """Create card play particle effect based on card type."""
        import random
        particles = []
        
        # Different particles for different card types
        if card.card_type.value == "attack":
            color = self.hades_theme.get_color('underworld_crimson')
            num_particles = 15
        elif card.card_type.value == "defense":
            color = self.hades_theme.get_color('sacred_turquoise')
            num_particles = 12
        else:
            color = self.hades_theme.get_color('royal_purple')
            num_particles = 10
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60)
            
            particle = {
                'x': position[0],
                'y': position[1],
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle),
                'life': random.uniform(0.8, 1.5),
                'max_life': 1.5,
                'size': random.randint(2, 4),
                'color': color
            }
            particles.append(particle)
        
        return particles
    
    def update(self, delta_time: float) -> None:
        """Update all active effects."""
        super().update(delta_time)
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - delta_time * 3)
        
        # Update flash overlay
        if self.flash_overlay > 0:
            self.flash_overlay = max(0, self.flash_overlay - delta_time * 4)
        
        # Update active effects
        for effect in self.active_effects[:]:
            effect['life'] -= delta_time
            
            if effect['type'] == 'damage_number':
                self._update_damage_number(effect, delta_time)
            elif effect['type'] == 'healing':
                self._update_healing_effect(effect, delta_time)
            elif effect['type'] == 'card_play':
                self._update_card_play_effect(effect, delta_time)
            
            # Remove expired effects
            if effect['life'] <= 0:
                self.active_effects.remove(effect)
    
    def _update_damage_number(self, effect: Dict, delta_time: float):
        """Update damage number effect."""
        # Move upward and fade
        effect['position'][0] += effect['velocity'][0] * delta_time
        effect['position'][1] += effect['velocity'][1] * delta_time
        
        # Slow down velocity
        effect['velocity'][1] *= 0.95
        
        # Scale effect
        life_ratio = effect['life'] / effect['max_life']
        effect['scale'] = 1.0 + (1.0 - life_ratio) * 0.5
    
    def _update_healing_effect(self, effect: Dict, delta_time: float):
        """Update healing effect."""
        effect['position'][1] += effect['velocity'][1] * delta_time
        
        # Update healing particles
        for particle in effect['particles'][:]:
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            particle['life'] -= delta_time
            
            if particle['life'] <= 0:
                effect['particles'].remove(particle)
    
    def _update_card_play_effect(self, effect: Dict, delta_time: float):
        """Update card play effect."""
        # Expanding ring
        life_ratio = 1.0 - (effect['life'] / effect['max_life'])
        effect['ring_radius'] = life_ratio * 60
        
        # Update particles
        for particle in effect['particles'][:]:
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            particle['life'] -= delta_time
            
            # Add gravity to particles
            particle['vy'] += 50 * delta_time
            
            if particle['life'] <= 0:
                effect['particles'].remove(particle)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all combat feedback effects."""
        if not self.visible:
            return
        
        # Apply screen shake
        shake_offset = (0, 0)
        if self.screen_shake > 0:
            import random
            shake_intensity = self.screen_shake * 5
            shake_offset = (
                random.randint(-int(shake_intensity), int(shake_intensity)),
                random.randint(-int(shake_intensity), int(shake_intensity))
            )
        
        # Render all effects
        for effect in self.active_effects:
            if effect['type'] == 'damage_number':
                self._render_damage_number(surface, effect, shake_offset)
            elif effect['type'] == 'healing':
                self._render_healing_effect(surface, effect, shake_offset)
            elif effect['type'] == 'card_play':
                self._render_card_play_effect(surface, effect, shake_offset)
        
        # Render flash overlay
        if self.flash_overlay > 0:
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash_alpha = int(self.flash_overlay * 150)
            flash_surface.fill((*self.flash_color, flash_alpha))
            surface.blit(flash_surface, (0, 0))
    
    def _render_damage_number(self, surface: pygame.Surface, effect: Dict, shake_offset: Tuple[int, int]):
        """Render floating damage number."""
        # Color based on damage type
        if effect['damage_type'] == "critical":
            color = self.hades_theme.get_color('hover_gold')
        elif effect['damage_type'] == "magical":
            color = self.hades_theme.get_color('royal_purple')
        else:
            color = self.hades_theme.get_color('underworld_crimson')
        
        # Font size based on scale
        font_size = int(24 * effect['scale'])
        font = pygame.font.Font(None, font_size)
        
        # Fade based on life
        life_ratio = effect['life'] / effect['max_life']
        alpha = int(255 * life_ratio)
        
        # Render text with outline
        text = str(effect['value'])
        
        # Outline
        outline_surface = font.render(text, True, self.hades_theme.get_color('obsidian_black'))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                pos = (
                    int(effect['position'][0] + dx + shake_offset[0]),
                    int(effect['position'][1] + dy + shake_offset[1])
                )
                surface.blit(outline_surface, pos)
        
        # Main text
        text_surface = font.render(text, True, (*color, alpha))
        pos = (
            int(effect['position'][0] + shake_offset[0]),
            int(effect['position'][1] + shake_offset[1])
        )
        surface.blit(text_surface, pos)
    
    def _render_healing_effect(self, surface: pygame.Surface, effect: Dict, shake_offset: Tuple[int, int]):
        """Render healing effect with particles."""
        # Healing number
        font = pygame.font.Font(None, 20)
        life_ratio = effect['life'] / effect['max_life']
        alpha = int(255 * life_ratio)
        
        heal_text = f"+{effect['value']}"
        text_surface = font.render(heal_text, True, (*self.hades_theme.get_color('success_green'), alpha))
        pos = (
            int(effect['position'][0] + shake_offset[0]),
            int(effect['position'][1] + shake_offset[1])
        )
        surface.blit(text_surface, pos)
        
        # Healing particles
        for particle in effect['particles']:
            if particle['life'] > 0:
                particle_alpha = int(255 * (particle['life'] / particle['max_life']))
                particle_color = (*self.hades_theme.get_color('success_green'), particle_alpha)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, 
                                 (particle['size'], particle['size']), particle['size'])
                
                pos = (
                    int(particle['x'] + shake_offset[0]),
                    int(particle['y'] + shake_offset[1])
                )
                surface.blit(particle_surface, pos)
    
    def _render_card_play_effect(self, surface: pygame.Surface, effect: Dict, shake_offset: Tuple[int, int]):
        """Render card play effect."""
        # Expanding ring
        if effect['ring_radius'] > 0:
            ring_alpha = int(255 * (effect['life'] / effect['max_life']))
            ring_color = (*self.hades_theme.get_color('duat_gold'), ring_alpha)
            
            ring_pos = (
                int(effect['position'][0] + shake_offset[0]),
                int(effect['position'][1] + shake_offset[1])
            )
            
            pygame.draw.circle(surface, ring_color, ring_pos, int(effect['ring_radius']), 3)
        
        # Card particles
        for particle in effect['particles']:
            if particle['life'] > 0:
                particle_alpha = int(255 * (particle['life'] / particle['max_life']))
                particle_color = (*particle['color'], particle_alpha)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color,
                                 (particle['size'], particle['size']), particle['size'])
                
                pos = (
                    int(particle['x'] + shake_offset[0]),
                    int(particle['y'] + shake_offset[1])
                )
                surface.blit(particle_surface, pos)