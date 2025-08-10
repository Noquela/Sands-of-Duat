"""
Ultrawide Display Decorations System
Professional hieroglyphic patterns and textures for 3440x1440 displays.
"""

import pygame
import math
import random
import time
from typing import Tuple, List, Optional

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT,
    FontSizes
)
from ...core.asset_loader import get_asset_loader


class UltrawideDecorations:
    """
    Professional ultrawide decoration system with Egyptian theming.
    Creates immersive side panels with hieroglyphic patterns and ambient effects.
    """
    
    def __init__(self):
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.particle_systems = []
        
        # Create decorative elements
        self._create_hieroglyphic_patterns()
        self._create_stone_textures()
        self._spawn_ambient_particles()
        
        print("[DECORATIONS] Ultrawide decoration system initialized")
    
    def _create_hieroglyphic_patterns(self):
        """Create hieroglyphic pattern surfaces for side panels."""
        if not Layout.IS_ULTRAWIDE:
            return
            
        panel_width = Layout.CONTENT_X_OFFSET
        panel_height = SCREEN_HEIGHT
        
        # Left panel hieroglyphs
        self.left_hieroglyphs = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        self._draw_hieroglyphic_column(self.left_hieroglyphs, panel_width)
        
        # Right panel hieroglyphs  
        self.right_hieroglyphs = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        self._draw_hieroglyphic_column(self.right_hieroglyphs, panel_width)
    
    def _draw_hieroglyphic_column(self, surface: pygame.Surface, width: int):
        """Draw a column of hieroglyphic patterns."""
        center_x = width // 2
        
        # Vertical line of hieroglyphs
        for y in range(100, SCREEN_HEIGHT - 100, 120):
            self._draw_egyptian_symbol(surface, center_x, y, 40)
            
        # Decorative borders
        border_color = (*Colors.GOLD, 80)
        
        # Vertical golden lines
        pygame.draw.line(surface, border_color, (width//4, 50), (width//4, SCREEN_HEIGHT-50), 2)
        pygame.draw.line(surface, border_color, (3*width//4, 50), (3*width//4, SCREEN_HEIGHT-50), 2)
        
        # Horizontal connectors
        for y in range(150, SCREEN_HEIGHT-150, 200):
            pygame.draw.line(surface, border_color, (width//4, y), (3*width//4, y), 1)
    
    def _draw_egyptian_symbol(self, surface: pygame.Surface, x: int, y: int, size: int):
        """Draw various Egyptian hieroglyphic symbols."""
        symbol_type = random.choice(['ankh', 'eye_of_horus', 'scarab', 'pyramid', 'sun_disk'])
        color = (*Colors.GOLD, random.randint(60, 120))
        
        if symbol_type == 'ankh':
            # Ankh symbol
            pygame.draw.circle(surface, color, (x, y-size//3), size//4, 2)
            pygame.draw.line(surface, color, (x, y-size//6), (x, y+size//2), 3)
            pygame.draw.line(surface, color, (x-size//4, y), (x+size//4, y), 3)
            
        elif symbol_type == 'eye_of_horus':
            # Eye of Horus
            pygame.draw.ellipse(surface, color, (x-size//3, y-size//6, 2*size//3, size//3), 2)
            pygame.draw.circle(surface, color, (x-size//6, y), size//8, 2)
            pygame.draw.line(surface, color, (x+size//6, y), (x+size//3, y+size//4), 2)
            
        elif symbol_type == 'scarab':
            # Scarab beetle
            pygame.draw.ellipse(surface, color, (x-size//4, y-size//6, size//2, size//3), 2)
            pygame.draw.line(surface, color, (x-size//3, y), (x-size//6, y-size//8), 1)
            pygame.draw.line(surface, color, (x+size//6, y-size//8), (x+size//3, y), 1)
            
        elif symbol_type == 'pyramid':
            # Pyramid
            points = [(x, y-size//3), (x-size//3, y+size//3), (x+size//3, y+size//3)]
            pygame.draw.polygon(surface, color, points, 2)
            pygame.draw.line(surface, color, (x, y-size//3), (x+size//6, y), 1)
            
        elif symbol_type == 'sun_disk':
            # Solar disk
            pygame.draw.circle(surface, color, (x, y), size//4, 2)
            # Sun rays
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                start_x = x + math.cos(rad) * (size//4 + 5)
                start_y = y + math.sin(rad) * (size//4 + 5)
                end_x = x + math.cos(rad) * (size//4 + 15)
                end_y = y + math.sin(rad) * (size//4 + 15)
                pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 1)
    
    def _create_stone_textures(self):
        """Create stone texture backgrounds for panels."""
        if not Layout.IS_ULTRAWIDE:
            return
            
        panel_width = Layout.CONTENT_X_OFFSET
        panel_height = SCREEN_HEIGHT
        
        # Base stone texture color
        base_color = (25, 20, 35)  # Dark stone
        
        self.left_texture = pygame.Surface((panel_width, panel_height))
        self.right_texture = pygame.Surface((panel_width, panel_height))
        
        # Create subtle stone texture with noise
        for surface in [self.left_texture, self.right_texture]:
            surface.fill(base_color)
            
            # Add texture noise
            for _ in range(panel_width * panel_height // 50):
                x = random.randint(0, panel_width-1)
                y = random.randint(0, panel_height-1)
                brightness_offset = random.randint(-15, 15)
                
                texture_color = tuple(max(0, min(255, c + brightness_offset)) for c in base_color)
                surface.set_at((x, y), texture_color)
    
    def _spawn_ambient_particles(self):
        """Spawn ambient particle effects for the side panels."""
        if not Layout.IS_ULTRAWIDE:
            return
            
        # Sand particles for left panel
        for _ in range(15):
            self.particle_systems.append({
                'type': 'sand',
                'x': random.randint(0, Layout.CONTENT_X_OFFSET),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed_y': random.uniform(10, 30),
                'speed_x': random.uniform(-5, 5),
                'size': random.randint(1, 3),
                'alpha': random.randint(40, 100),
                'life': random.uniform(5, 10),
                'max_life': random.uniform(5, 10)
            })
        
        # Golden sparkles for right panel  
        for _ in range(10):
            self.particle_systems.append({
                'type': 'sparkle',
                'x': random.randint(Layout.UI_SAFE_RIGHT, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed_y': random.uniform(15, 40),
                'speed_x': random.uniform(-3, 3),
                'size': random.randint(2, 4),
                'alpha': random.randint(80, 150),
                'life': random.uniform(3, 8),
                'max_life': random.uniform(3, 8),
                'twinkle_phase': random.uniform(0, math.pi * 2)
            })
    
    def update(self, dt: float):
        """Update all decoration animations."""
        self.animation_time += dt
        
        # Update particles
        for particle in self.particle_systems[:]:
            particle['life'] -= dt
            particle['y'] += particle['speed_y'] * dt
            particle['x'] += particle['speed_x'] * dt
            
            # Fade out over time
            particle['alpha'] = int(particle['alpha'] * (particle['life'] / particle['max_life']))
            
            # Remove dead particles
            if particle['life'] <= 0 or particle['y'] > SCREEN_HEIGHT:
                self.particle_systems.remove(particle)
        
        # Respawn particles to maintain count
        while len([p for p in self.particle_systems if p['type'] == 'sand']) < 15:
            self.particle_systems.append({
                'type': 'sand',
                'x': random.randint(0, Layout.CONTENT_X_OFFSET),
                'y': -10,
                'speed_y': random.uniform(10, 30),
                'speed_x': random.uniform(-5, 5),
                'size': random.randint(1, 3),
                'alpha': random.randint(40, 100),
                'life': random.uniform(5, 10),
                'max_life': random.uniform(5, 10)
            })
        
        while len([p for p in self.particle_systems if p['type'] == 'sparkle']) < 10:
            self.particle_systems.append({
                'type': 'sparkle',
                'x': random.randint(Layout.UI_SAFE_RIGHT, SCREEN_WIDTH),
                'y': -10,
                'speed_y': random.uniform(15, 40),
                'speed_x': random.uniform(-3, 3),
                'size': random.randint(2, 4),
                'alpha': random.randint(80, 150),
                'life': random.uniform(3, 8),
                'max_life': random.uniform(3, 8),
                'twinkle_phase': random.uniform(0, math.pi * 2)
            })
    
    def render(self, surface: pygame.Surface):
        """Render all ultrawide decorations."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        # Render base textures
        surface.blit(self.left_texture, (0, 0))
        surface.blit(self.right_texture, (Layout.UI_SAFE_RIGHT, 0))
        
        # Render hieroglyphic patterns with breathing effect
        alpha_modifier = int(50 + 30 * abs(math.sin(self.animation_time * 0.5)))
        
        left_copy = self.left_hieroglyphs.copy()
        left_copy.set_alpha(alpha_modifier)
        surface.blit(left_copy, (0, 0))
        
        right_copy = self.right_hieroglyphs.copy()  
        right_copy.set_alpha(alpha_modifier)
        surface.blit(right_copy, (Layout.UI_SAFE_RIGHT, 0))
        
        # Render particles
        self._render_particles(surface)
        
        # Add subtle gradients at edges
        self._render_edge_gradients(surface)
    
    def _render_particles(self, surface: pygame.Surface):
        """Render ambient particles."""
        for particle in self.particle_systems:
            if particle['type'] == 'sand':
                color = (*Colors.DESERT_SAND, max(0, min(255, int(particle['alpha']))))
                particle_surface = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
                surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
                
            elif particle['type'] == 'sparkle':
                # Twinkling effect
                twinkle = abs(math.sin(self.animation_time * 2 + particle['twinkle_phase']))
                alpha = int(particle['alpha'] * twinkle)
                color = (*Colors.GOLD, max(0, min(255, alpha)))
                
                sparkle_surface = pygame.Surface((particle['size']*3, particle['size']*3), pygame.SRCALPHA)
                pygame.draw.circle(sparkle_surface, color, (particle['size']*3//2, particle['size']*3//2), particle['size'])
                
                # Add cross sparkle effect
                cross_color = (*Colors.GOLD, max(0, min(255, alpha//2)))
                pygame.draw.line(sparkle_surface, cross_color, 
                               (0, particle['size']*3//2), (particle['size']*3, particle['size']*3//2), 1)
                pygame.draw.line(sparkle_surface, cross_color,
                               (particle['size']*3//2, 0), (particle['size']*3//2, particle['size']*3), 1)
                
                surface.blit(sparkle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_edge_gradients(self, surface: pygame.Surface):
        """Render subtle gradients at the edges of content area."""
        gradient_width = 30
        
        # Left gradient (fade from decoration to content)
        left_gradient = pygame.Surface((gradient_width, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(gradient_width):
            alpha = int(50 * (1 - x / gradient_width))
            gradient_color = (*Colors.BLACK, alpha)
            pygame.draw.line(left_gradient, gradient_color, (x, 0), (x, SCREEN_HEIGHT))
        
        surface.blit(left_gradient, (Layout.CONTENT_X_OFFSET - gradient_width, 0))
        
        # Right gradient
        right_gradient = pygame.Surface((gradient_width, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(gradient_width):
            alpha = int(50 * (x / gradient_width))  # Reverse direction
            gradient_color = (*Colors.BLACK, alpha)
            pygame.draw.line(right_gradient, gradient_color, (x, 0), (x, SCREEN_HEIGHT))
            
        surface.blit(right_gradient, (Layout.UI_SAFE_RIGHT, 0))


# Global instance for easy access
ultrawide_decorations = UltrawideDecorations()