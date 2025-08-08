"""
Professional Loading Screen - Egyptian themed with animated progress indicators.
Features smooth animations and Hades-level polish.
"""

import pygame
import math
from typing import Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)

class LoadingType(Enum):
    """Types of loading operations."""
    ENTERING_COMBAT = auto()
    BUILDING_DECK = auto()
    GENERATING_ASSETS = auto()
    SAVING_GAME = auto()
    LOADING_GAME = auto()
    GENERAL = auto()

class LoadingScreen:
    """
    Professional loading screen with Egyptian theming and smooth animations.
    Features animated hieroglyphics, sand particles, and progress indicators.
    """
    
    def __init__(self, loading_type: LoadingType = LoadingType.GENERAL, 
                 completion_callback: Optional[Callable] = None):
        """
        Initialize loading screen.
        
        Args:
            loading_type: Type of loading operation
            completion_callback: Called when loading is complete
        """
        self.loading_type = loading_type
        self.completion_callback = completion_callback
        
        # Animation state
        self.animation_time = 0.0
        self.progress = 0.0  # 0.0 to 1.0
        self.is_complete = False
        
        # Visual elements
        self.sand_particles = []
        self.hieroglyph_rotation = 0.0
        
        # Loading messages
        self.loading_messages = {
            LoadingType.ENTERING_COMBAT: [
                "Preparing the battlefield...",
                "Awakening ancient powers...", 
                "Drawing cards from the void...",
                "The gods are watching..."
            ],
            LoadingType.BUILDING_DECK: [
                "Organizing sacred scrolls...",
                "Consulting the Book of Dead...",
                "Arranging mystical cards...",
                "Blessing your deck..."
            ],
            LoadingType.GENERATING_ASSETS: [
                "Summoning Egyptian spirits...",
                "Crafting divine imagery...",
                "Channeling artistic power...",
                "Materializing visions..."
            ],
            LoadingType.SAVING_GAME: [
                "Inscribing on sacred papyrus...",
                "Sealing in the temple vault...",
                "Recording your journey...",
                "Preserving your legacy..."
            ],
            LoadingType.LOADING_GAME: [
                "Reading ancient scrolls...",
                "Awakening from slumber...",
                "Restoring your journey...",
                "The pharaoh returns..."
            ],
            LoadingType.GENERAL: [
                "Working ancient magic...",
                "Consulting the gods...",
                "Preparing the ritual...",
                "Almost ready..."
            ]
        }
        
        self.current_message_index = 0
        self.message_change_timer = 0.0
        
        # Create background
        self.background_surface = self._create_background()
        
        # Initialize sand particles
        self._spawn_initial_particles()
    
    def _create_background(self) -> pygame.Surface:
        """Create animated background with Egyptian theming."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create gradient effect similar to main menu but darker
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            
            # Dark Egyptian night gradient
            r = int(Colors.DARK_BLUE[0] * (0.4 - ratio * 0.1))
            g = int(Colors.DARK_BLUE[1] * (0.4 - ratio * 0.1)) 
            b = int(Colors.DARK_BLUE[2] * (0.6 + ratio * 0.2))
            
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        return background
    
    def _spawn_initial_particles(self):
        """Spawn initial sand particles for atmosphere."""
        for _ in range(15):
            x = Layout.UI_SAFE_LEFT + (Layout.UI_SAFE_WIDTH * (0.2 + 0.6 * (len(self.sand_particles) / 15)))
            y = SCREEN_HEIGHT * (0.3 + 0.4 * (len(self.sand_particles) / 15))
            
            self.sand_particles.append({
                'x': x,
                'y': y,
                'size': 2 + (len(self.sand_particles) % 3),
                'speed': 20 + (len(self.sand_particles) % 20),
                'phase': len(self.sand_particles) * 0.5
            })
    
    def set_progress(self, progress: float):
        """
        Set loading progress.
        
        Args:
            progress: Progress from 0.0 to 1.0
        """
        self.progress = max(0.0, min(1.0, progress))
        
        if self.progress >= 1.0 and not self.is_complete:
            self.is_complete = True
            if self.completion_callback:
                self.completion_callback()
    
    def update(self, dt: float):
        """
        Update loading screen animations.
        
        Args:
            dt: Delta time in seconds
        """
        self.animation_time += dt
        
        # Update hieroglyph rotation
        self.hieroglyph_rotation += dt * 45  # 45 degrees per second
        
        # Update sand particles
        for particle in self.sand_particles:
            # Circular floating motion
            particle['x'] += math.sin(self.animation_time * 0.5 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.5
            
            # Keep particles in safe area
            if particle['x'] < Layout.UI_SAFE_LEFT:
                particle['x'] = Layout.UI_SAFE_RIGHT
            elif particle['x'] > Layout.UI_SAFE_RIGHT:
                particle['x'] = Layout.UI_SAFE_LEFT
                
            if particle['y'] < SCREEN_HEIGHT * 0.2:
                particle['y'] = SCREEN_HEIGHT * 0.8
            elif particle['y'] > SCREEN_HEIGHT * 0.8:
                particle['y'] = SCREEN_HEIGHT * 0.2
        
        # Update loading messages
        self.message_change_timer += dt
        if self.message_change_timer >= 2.0:  # Change message every 2 seconds
            messages = self.loading_messages[self.loading_type]
            self.current_message_index = (self.current_message_index + 1) % len(messages)
            self.message_change_timer = 0.0
    
    def render(self, surface: pygame.Surface):
        """
        Render the loading screen with all animations.
        
        Args:
            surface: Surface to render to
        """
        # Clear surface
        surface.blit(self.background_surface, (0, 0))
        
        # Draw ultrawide side bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Render sand particles
        self._render_sand_particles(surface)
        
        # Render main loading elements
        self._render_loading_title(surface)
        self._render_progress_bar(surface)
        self._render_loading_message(surface)
        self._render_hieroglyph_spinner(surface)
        
        # Render tips/flavor text
        self._render_loading_tips(surface)
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render Egyptian-themed side bars for ultrawide displays."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # Fill with darker pattern
        pattern_color = (5, 5, 25)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Add animated border pattern
        border_alpha = int(80 + 40 * abs(math.sin(self.animation_time * 2)))
        pattern_surface = pygame.Surface((6, SCREEN_HEIGHT))
        pattern_surface.set_alpha(border_alpha)
        pattern_surface.fill(Colors.GOLD)
        
        surface.blit(pattern_surface, (Layout.CONTENT_X_OFFSET - 6, 0))
        surface.blit(pattern_surface, (Layout.UI_SAFE_RIGHT, 0))
    
    def _render_sand_particles(self, surface: pygame.Surface):
        """Render floating sand particles for atmosphere."""
        for particle in self.sand_particles:
            # Pulsing alpha effect
            alpha = int(150 + 80 * abs(math.sin(self.animation_time + particle['phase'])))
            
            color = (*Colors.GOLD, alpha)
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(Colors.GOLD)
            
            pygame.draw.circle(particle_surface, Colors.GOLD, 
                             (particle['size'], particle['size']), particle['size'])
            
            surface.blit(particle_surface, 
                        (int(particle['x'] - particle['size']), 
                         int(particle['y'] - particle['size'])))
    
    def _render_loading_title(self, surface: pygame.Surface):
        """Render the main loading title."""
        font = pygame.font.Font(None, FontSizes.TITLE_MEDIUM)
        
        title_text = "LOADING"
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_CENTER[1] - 80))
        
        # Add glow effect
        glow_surface = font.render(title_text, True, Colors.PAPYRUS)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0] + 2, SCREEN_CENTER[1] - 78))
        glow_surface.set_alpha(120)
        
        surface.blit(glow_surface, glow_rect)
        surface.blit(title_surface, title_rect)
    
    def _render_progress_bar(self, surface: pygame.Surface):
        """Render animated progress bar with Egyptian styling."""
        # Progress bar dimensions
        bar_width = 400
        bar_height = 12
        bar_x = SCREEN_CENTER[0] - bar_width // 2
        bar_y = SCREEN_CENTER[1] - 20
        
        # Background bar
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, Colors.DARK_BLUE, bg_rect)
        pygame.draw.rect(surface, Colors.PAPYRUS, bg_rect, 2)
        
        # Progress fill
        if self.progress > 0:
            fill_width = int(bar_width * self.progress)
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            
            # Gradient effect for progress bar
            for i in range(fill_width):
                ratio = i / max(1, fill_width)
                r = int(Colors.GOLD[0] * (0.7 + 0.3 * ratio))
                g = int(Colors.GOLD[1] * (0.7 + 0.3 * ratio))
                b = int(Colors.GOLD[2] * (0.7 + 0.3 * ratio))
                
                color = (min(255, r), min(255, g), min(255, b))
                pygame.draw.line(surface, color, 
                               (bar_x + i, bar_y), (bar_x + i, bar_y + bar_height))
        
        # Progress percentage
        percentage = int(self.progress * 100)
        font = pygame.font.Font(None, FontSizes.BODY)
        percent_text = f"{percentage}%"
        percent_surface = font.render(percent_text, True, Colors.DESERT_SAND)
        percent_rect = percent_surface.get_rect(center=(SCREEN_CENTER[0], bar_y + bar_height + 20))
        
        surface.blit(percent_surface, percent_rect)
    
    def _render_loading_message(self, surface: pygame.Surface):
        """Render current loading message."""
        messages = self.loading_messages[self.loading_type]
        current_message = messages[self.current_message_index]
        
        font = pygame.font.Font(None, FontSizes.BUTTON)
        message_surface = font.render(current_message, True, Colors.PAPYRUS)
        message_rect = message_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_CENTER[1] + 40))
        
        surface.blit(message_surface, message_rect)
    
    def _render_hieroglyph_spinner(self, surface: pygame.Surface):
        """Render rotating hieroglyph symbol as spinner."""
        center_x = SCREEN_CENTER[0]
        center_y = SCREEN_CENTER[1] + 100
        radius = 25
        
        # Create rotating ankh-like symbol
        points = []
        num_points = 8
        
        for i in range(num_points):
            angle = (i * 360 / num_points + self.hieroglyph_rotation) * math.pi / 180
            
            # Alternate between inner and outer points for star effect
            r = radius if i % 2 == 0 else radius * 0.6
            
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, Colors.GOLD, points)
            pygame.draw.polygon(surface, Colors.PAPYRUS, points, 2)
    
    def _render_loading_tips(self, surface: pygame.Surface):
        """Render helpful tips or flavor text."""
        tips = [
            "Egyptian gods favor those who plan their moves carefully.",
            "Each card channels the power of ancient deities.",
            "The hourglass measures time until the final judgment.",
            "Anubis weighs your heart against Ma'at's feather.",
            "Ra's solar energy powers your most devastating attacks."
        ]
        
        # Choose tip based on animation time to cycle through them slowly
        tip_index = int(self.animation_time / 8) % len(tips)
        current_tip = tips[tip_index]
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        tip_surface = font.render(current_tip, True, Colors.DESERT_SAND)
        tip_rect = tip_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 60))
        
        # Add subtle alpha pulsing
        alpha = int(180 + 50 * math.sin(self.animation_time * 2))
        tip_surface.set_alpha(alpha)
        
        surface.blit(tip_surface, tip_rect)