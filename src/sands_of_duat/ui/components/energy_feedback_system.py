"""
Energy Feedback System - Hades-Level Animated Energy/Mana Display
Pulsating energy bars with mystical Egyptian effects.
"""

import pygame
import math
import random
from typing import Tuple, Optional
from enum import Enum, auto

from ...core.constants import Colors, Layout, FontSizes

class EnergyState(Enum):
    """Energy system states."""
    NORMAL = auto()
    GAINING = auto()
    SPENDING = auto()
    CRITICAL_LOW = auto()
    FULL = auto()

class EnergyFeedbackSystem:
    """
    Professional energy display with Hades-level visual feedback.
    Features pulsating effects, gain/loss animations, and mystical glow.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 max_energy: int = 10, initial_energy: int = 0):
        """
        Initialize energy feedback system.
        
        Args:
            x, y: Position
            width, height: Dimensions
            max_energy: Maximum energy capacity
            initial_energy: Starting energy amount
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.max_energy = max_energy
        self.current_energy = initial_energy
        self.display_energy = float(initial_energy)  # For smooth animations
        
        # Visual state
        self.state = EnergyState.NORMAL
        self.pulse_intensity = 0.0      # 0.0 to 1.0
        self.glow_intensity = 0.0       # 0.0 to 1.0
        self.animation_time = 0.0
        
        # Animation settings
        self.pulse_speed = 3.0          # Pulse frequency
        self.animation_speed = 8.0      # State transition speed
        self.energy_change_speed = 12.0 # Energy bar animation speed
        
        # Color scheme (Egyptian mystical)
        self.colors = {
            'background': Colors.BACKGROUND_SECONDARY,
            'border': Colors.LAPIS_DARK,
            'energy_low': (100, 50, 200),      # Deep purple
            'energy_mid': (150, 100, 255),     # Electric purple
            'energy_high': (200, 150, 255),    # Bright purple
            'energy_full': Colors.LAPIS_LAZULI, # Electric blue
            'glow': Colors.ACCENT_GLOW,         # Warm golden glow
            'text': Colors.PAPYRUS,
            'critical': Colors.RED
        }
        
        # Effect particles
        self.particles = []
        self.particle_timer = 0.0
        
    def set_energy(self, new_energy: int):
        """
        Set energy value with state detection.
        
        Args:
            new_energy: New energy amount
        """
        old_energy = self.current_energy
        self.current_energy = max(0, min(new_energy, self.max_energy))
        
        # Determine state based on change
        if new_energy > old_energy:
            self.state = EnergyState.GAINING
            self._create_gain_particles()
        elif new_energy < old_energy:
            self.state = EnergyState.SPENDING
            self._create_spend_particles()
        
        # Special states
        if self.current_energy == 0:
            self.state = EnergyState.CRITICAL_LOW
        elif self.current_energy == self.max_energy:
            self.state = EnergyState.FULL
            
    def spend_energy(self, amount: int) -> bool:
        """
        Attempt to spend energy.
        
        Returns:
            bool: True if energy was spent successfully
        """
        if self.current_energy >= amount:
            self.set_energy(self.current_energy - amount)
            return True
        return False
        
    def gain_energy(self, amount: int):
        """Gain energy with visual feedback."""
        self.set_energy(self.current_energy + amount)
        
    def update(self, dt: float):
        """Update animations and effects."""
        self.animation_time += dt
        
        # Smooth energy bar animation
        energy_diff = self.current_energy - self.display_energy
        self.display_energy += energy_diff * dt * self.energy_change_speed
        
        # Update state-based effects
        self._update_state_effects(dt)
        
        # Update particles
        self._update_particles(dt)
        
        # Auto-return to normal state after animations
        if self.state in [EnergyState.GAINING, EnergyState.SPENDING]:
            if abs(self.display_energy - self.current_energy) < 0.1:
                if self.current_energy == 0:
                    self.state = EnergyState.CRITICAL_LOW
                elif self.current_energy == self.max_energy:
                    self.state = EnergyState.FULL
                else:
                    self.state = EnergyState.NORMAL
                    
    def _update_state_effects(self, dt: float):
        """Update visual effects based on current state."""
        target_pulse = 0.0
        target_glow = 0.0
        
        if self.state == EnergyState.NORMAL:
            target_pulse = 0.3
            target_glow = 0.2
        elif self.state == EnergyState.GAINING:
            target_pulse = 1.0
            target_glow = 0.8
        elif self.state == EnergyState.SPENDING:
            target_pulse = 0.6
            target_glow = 0.4
        elif self.state == EnergyState.CRITICAL_LOW:
            target_pulse = 0.8 + 0.2 * math.sin(self.animation_time * 4.0)  # Fast pulse
            target_glow = 0.6
        elif self.state == EnergyState.FULL:
            target_pulse = 0.7 + 0.3 * math.sin(self.animation_time * 2.0)  # Slow pulse
            target_glow = 1.0
            
        # Smooth transitions
        self.pulse_intensity += (target_pulse - self.pulse_intensity) * dt * self.animation_speed
        self.glow_intensity += (target_glow - self.glow_intensity) * dt * self.animation_speed
        
    def _create_gain_particles(self):
        """Create particles for energy gain effect."""
        for _ in range(3):
            self.particles.append({
                'x': self.rect.centerx + random.randint(-20, 20),
                'y': self.rect.bottom + random.randint(-5, 5),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-3, -1),
                'life': 1.0,
                'color': self.colors['energy_high'],
                'type': 'gain'
            })
            
    def _create_spend_particles(self):
        """Create particles for energy spend effect."""
        for _ in range(2):
            self.particles.append({
                'x': self.rect.centerx + random.randint(-15, 15),
                'y': self.rect.centery + random.randint(-10, 10),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-1, 1),
                'life': 0.8,
                'color': self.colors['energy_mid'],
                'type': 'spend'
            })
            
    def _update_particles(self, dt: float):
        """Update particle effects."""
        
        # Update existing particles
        for particle in self.particles[:]:  # Copy list to avoid modification issues
            particle['x'] += particle['vx'] * dt * 60
            particle['y'] += particle['vy'] * dt * 60
            particle['life'] -= dt * 2.0
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
        # Generate new particles for continuous effects
        self.particle_timer += dt
        if self.particle_timer > 0.2 and self.state in [EnergyState.FULL, EnergyState.CRITICAL_LOW]:
            if random.random() < 0.3:  # 30% chance
                color = self.colors['energy_full'] if self.state == EnergyState.FULL else self.colors['critical']
                self.particles.append({
                    'x': self.rect.x + random.randint(0, self.rect.width),
                    'y': self.rect.y + random.randint(0, self.rect.height),
                    'vx': random.uniform(-0.5, 0.5),
                    'vy': random.uniform(-1, -0.2),
                    'life': random.uniform(0.5, 1.0),
                    'color': color,
                    'type': 'ambient'
                })
            self.particle_timer = 0.0
            
    def render(self, surface: pygame.Surface):
        """Render energy bar with Hades-level effects."""
        # Render glow effect first (behind bar)
        if self.glow_intensity > 0.1:
            self._render_glow(surface)
            
        # Main energy bar background
        pygame.draw.rect(surface, self.colors['background'], self.rect, border_radius=6)
        
        # Energy fill with gradient effect
        if self.display_energy > 0:
            fill_width = int((self.display_energy / self.max_energy) * (self.rect.width - 4))
            fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, fill_width, self.rect.height - 4)
            
            # Energy color based on amount
            energy_ratio = self.display_energy / self.max_energy
            if energy_ratio < 0.25:
                fill_color = self.colors['energy_low']
            elif energy_ratio < 0.5:
                fill_color = self.colors['energy_mid']
            elif energy_ratio < 1.0:
                fill_color = self.colors['energy_high']
            else:
                fill_color = self.colors['energy_full']
                
            # Apply pulse effect
            pulse_factor = 1.0 + 0.3 * self.pulse_intensity * math.sin(self.animation_time * self.pulse_speed)
            pulsed_color = tuple(min(255, int(c * pulse_factor)) for c in fill_color)
            
            pygame.draw.rect(surface, pulsed_color, fill_rect, border_radius=4)
            
            # Highlight gradient on top
            highlight_rect = pygame.Rect(fill_rect.x, fill_rect.y, fill_rect.width, fill_rect.height // 3)
            highlight_color = tuple(min(255, int(c * 1.2)) for c in pulsed_color)
            highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            highlight_surface.fill(highlight_color)
            highlight_surface.set_alpha(100)
            surface.blit(highlight_surface, highlight_rect)
            
        # Border
        border_color = self.colors['critical'] if self.state == EnergyState.CRITICAL_LOW else self.colors['border']
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)
        
        # Energy text
        font = pygame.font.Font(None, FontSizes.BODY)
        energy_text = f"{int(self.current_energy)}/{self.max_energy}"
        text_surface = font.render(energy_text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text shadow for better visibility
        shadow_surface = font.render(energy_text, True, (0, 0, 0))
        shadow_surface.set_alpha(150)
        surface.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)
        
        # Render particles
        self._render_particles(surface)
        
    def _render_glow(self, surface: pygame.Surface):
        """Render glow effect around energy bar."""
        glow_size = int(8 * self.glow_intensity)
        glow_rect = pygame.Rect(
            self.rect.x - glow_size, self.rect.y - glow_size,
            self.rect.width + glow_size * 2, self.rect.height + glow_size * 2
        )
        
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow_alpha = int(60 * self.glow_intensity)
        
        # Multiple glow layers
        for i in range(3):
            layer_alpha = glow_alpha // (i + 1)
            layer_size = i * 2
            layer_rect = pygame.Rect(
                layer_size, layer_size,
                glow_rect.width - layer_size * 2,
                glow_rect.height - layer_size * 2
            )
            
            layer_surface = pygame.Surface((layer_rect.width, layer_rect.height), pygame.SRCALPHA)
            layer_surface.fill(self.colors['glow'])
            layer_surface.set_alpha(layer_alpha)
            glow_surface.blit(layer_surface, (layer_rect.x, layer_rect.y))
            
        surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
    def _render_particles(self, surface: pygame.Surface):
        """Render particle effects."""
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            size = max(1, int(4 * particle['life']))
            
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            particle_surface.fill(particle['color'])
            particle_surface.set_alpha(alpha)
            
            pygame.draw.circle(particle_surface, particle['color'], (size, size), size)
            surface.blit(particle_surface, (int(particle['x'] - size), int(particle['y'] - size)))