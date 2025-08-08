"""
Animated Title Component - Hades-level title animations.
Features pulsing glow effects, particle systems, and smooth animations.
"""

import pygame
import math
import random
from typing import List, Tuple

from ...core.constants import Colors, FontSizes, SCREEN_CENTER

class Particle:
    """Individual sand/gold particle for atmospheric effect."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-20, 20)
        self.vy = random.uniform(-30, -10)
        self.life = random.uniform(2.0, 4.0)
        self.max_life = self.life
        self.size = random.uniform(1, 3)
        self.color = random.choice([Colors.GOLD, Colors.DESERT_SAND, Colors.PAPYRUS])
        self.alpha = 255
    
    def update(self, dt: float):
        """Update particle position and life."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 20 * dt  # Gravity
        self.life -= dt
        
        # Fade out as particle dies
        life_ratio = self.life / self.max_life
        self.alpha = int(255 * life_ratio)
        self.size = self.size * life_ratio
    
    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return self.life > 0
    
    def render(self, surface: pygame.Surface):
        """Render the particle."""
        if self.alpha > 0 and self.size > 0:
            # Create particle surface with alpha
            particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)))
            particle_surface.set_alpha(self.alpha)
            
            # Draw particle as small circle
            center = (int(self.size), int(self.size))
            pygame.draw.circle(particle_surface, self.color, center, int(self.size))
            
            surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class TitleAnimation:
    """
    Animated title component with Egyptian theming and particle effects.
    Features pulsing glow, floating particles, and smooth animations.
    """
    
    def __init__(self, title_text: str = "SANDS OF DUAT", 
                 subtitle_text: str = "Egyptian Underworld Card Game"):
        """
        Initialize animated title.
        
        Args:
            title_text: Main title text
            subtitle_text: Subtitle text
        """
        self.title_text = title_text
        self.subtitle_text = subtitle_text
        
        # Fonts
        self.title_font = pygame.font.Font(None, FontSizes.TITLE_HUGE)
        self.subtitle_font = pygame.font.Font(None, FontSizes.SUBTITLE)
        
        # Animation state
        self.glow_time = 0.0
        self.pulse_time = 0.0
        self.particle_spawn_time = 0.0
        
        # Particle system
        self.particles: List[Particle] = []
        self.particle_spawn_rate = 0.1  # seconds between spawns
        
        # Title positioning
        self.title_y = 120
        self.subtitle_y = 200
        
        # Animation intensities
        self.glow_intensity = 0.0
        self.pulse_intensity = 0.0
    
    def update(self, dt: float):
        """
        Update title animations and particle system.
        
        Args:
            dt: Delta time in seconds
        """
        # Update animation timers
        self.glow_time += dt
        self.pulse_time += dt * 1.5
        self.particle_spawn_time += dt
        
        # Calculate animation intensities
        self.glow_intensity = 0.5 + 0.3 * math.sin(self.glow_time * 2.0)
        self.pulse_intensity = 0.8 + 0.2 * math.sin(self.pulse_time)
        
        # Spawn particles
        if self.particle_spawn_time >= self.particle_spawn_rate:
            self._spawn_particle()
            self.particle_spawn_time = 0.0
        
        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)
    
    def _spawn_particle(self):
        """Spawn a new atmospheric particle."""
        # Spawn near title area
        center_x = SCREEN_CENTER[0]
        spawn_x = center_x + random.uniform(-200, 200)
        spawn_y = self.title_y + random.uniform(50, 100)
        
        self.particles.append(Particle(spawn_x, spawn_y))
        
        # Limit particle count for performance
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]
    
    def render(self, surface: pygame.Surface):
        """
        Render the animated title with all effects.
        
        Args:
            surface: Surface to render to
        """
        # Render particles behind title
        for particle in self.particles:
            particle.render(surface)
        
        # Render title with glow effect
        self._render_title_with_glow(surface)
        
        # Render subtitle
        self._render_subtitle(surface)
    
    def _render_title_with_glow(self, surface: pygame.Surface):
        """Render title text with animated glow effect."""
        center_x = SCREEN_CENTER[0]
        
        # Create title surface
        title_surface = self.title_font.render(self.title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(center_x, self.title_y))
        
        # Calculate glow properties
        glow_size = int(8 + self.glow_intensity * 6)
        glow_alpha = int(150 * self.glow_intensity)
        
        # Render glow layers
        for i in range(glow_size, 0, -1):
            glow_alpha_layer = int(glow_alpha * (1.0 - i / glow_size))
            if glow_alpha_layer > 0:
                # Create glow surface
                glow_surface = self.title_font.render(self.title_text, True, Colors.GOLD)
                glow_surface.set_alpha(glow_alpha_layer)
                
                # Render glow in all directions
                offsets = [(-i, -i), (i, -i), (-i, i), (i, i), 
                          (-i, 0), (i, 0), (0, -i), (0, i)]
                
                for dx, dy in offsets:
                    glow_rect = title_rect.copy()
                    glow_rect.x += dx
                    glow_rect.y += dy
                    surface.blit(glow_surface, glow_rect)
        
        # Render main title
        surface.blit(title_surface, title_rect)
        
        # Add extra bright center glow
        if self.glow_intensity > 0.7:
            bright_surface = self.title_font.render(self.title_text, True, Colors.WHITE)
            bright_surface.set_alpha(int(100 * (self.glow_intensity - 0.7) / 0.3))
            surface.blit(bright_surface, title_rect)
    
    def _render_subtitle(self, surface: pygame.Surface):
        """Render subtitle with subtle effects."""
        center_x = SCREEN_CENTER[0]
        
        # Create subtitle surface
        subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, Colors.PAPYRUS)
        subtitle_rect = subtitle_surface.get_rect(center=(center_x, self.subtitle_y))
        
        # Add subtle shadow
        shadow_surface = self.subtitle_font.render(self.subtitle_text, True, Colors.BLACK)
        shadow_rect = subtitle_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        surface.blit(shadow_surface, shadow_rect)
        
        # Render main subtitle
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Add subtle pulse effect
        if self.pulse_intensity > 0.9:
            pulse_surface = self.subtitle_font.render(self.subtitle_text, True, Colors.GOLD)
            pulse_alpha = int(50 * (self.pulse_intensity - 0.9) / 0.1)
            pulse_surface.set_alpha(pulse_alpha)
            surface.blit(pulse_surface, subtitle_rect)
    
    def get_title_bounds(self) -> pygame.Rect:
        """Get bounding rectangle of the title area."""
        center_x = SCREEN_CENTER[0]
        title_surface = self.title_font.render(self.title_text, True, Colors.GOLD)
        subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, Colors.PAPYRUS)
        
        title_rect = title_surface.get_rect(center=(center_x, self.title_y))
        subtitle_rect = subtitle_surface.get_rect(center=(center_x, self.subtitle_y))
        
        return title_rect.union(subtitle_rect)
    
    def set_position(self, title_y: int, subtitle_y: int):
        """Update title positioning."""
        self.title_y = title_y
        self.subtitle_y = subtitle_y