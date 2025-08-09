"""
Collection Screen - Hall of Gods
Professional placeholder for card collection viewing.
"""

import pygame
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ..components.animated_button import AnimatedButton

class CollectionAction(Enum):
    """Collection screen actions."""
    BACK_TO_MENU = auto()

class CollectionScreen:
    """Professional collection screen placeholder."""
    
    def __init__(self, on_action: Optional[Callable[[CollectionAction], None]] = None):
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Create background
        self.background_surface = self._create_background()
        
        # Create buttons
        self.buttons = self._create_buttons()
        
        print("Collection Screen initialized - Hall of Gods awaits")
    
    def _create_background(self):
        """Create collection background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Deep blue gradient for collection
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(15 + ratio * 25)
            g = int(25 + ratio * 35)
            b = int(60 + ratio * 40)
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create UI buttons."""
        buttons = []
        
        back_button = AnimatedButton(
            50, 50, 150, 40,
            "BACK TO MENU", FontSizes.BUTTON,
            action=lambda: self._handle_action(CollectionAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        return buttons
    
    def _handle_action(self, action: CollectionAction):
        """Handle button actions."""
        if self.on_action:
            self.on_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the collection screen."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(CollectionAction.BACK_TO_MENU)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.handle_click(mouse_pos):
                        break
    
    def render(self, surface: pygame.Surface):
        """Render the collection screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Title
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "HALL OF GODS"
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 200))
        surface.blit(title_surface, title_rect)
        
        # Coming soon message
        subtitle_font = pygame.font.Font(None, FontSizes.SUBTITLE)
        subtitle_text = "View your divine card collection"
        subtitle_surface = subtitle_font.render(subtitle_text, True, Colors.LAPIS_LAZULI)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_CENTER[0], 260))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Implementation note
        body_font = pygame.font.Font(None, FontSizes.BODY)
        note_text = "Collection system will be implemented in SPRINT 7"
        note_surface = body_font.render(note_text, True, Colors.PAPYRUS)
        note_rect = note_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_CENTER[1]))
        surface.blit(note_surface, note_rect)
        
        # Instructions
        instruction_text = "ESC: Back to Menu"
        instruction_surface = body_font.render(instruction_text, True, Colors.DESERT_SAND)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 100))
        surface.blit(instruction_surface, instruction_rect)
        
        # Buttons
        for button in self.buttons:
            button.render(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render ultrawide side bars."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        pattern_color = (10, 15, 30)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        for button in self.buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0