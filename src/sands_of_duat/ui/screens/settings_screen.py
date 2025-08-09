"""
Settings Screen - Temple Settings
Professional placeholder for game settings and options.
"""

import pygame
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...audio.simple_audio_manager import audio_manager, SoundEffect
from ..components.animated_button import AnimatedButton

class SettingsAction(Enum):
    """Settings screen actions."""
    BACK_TO_MENU = auto()

class SettingsScreen:
    """Professional settings screen placeholder."""
    
    def __init__(self, on_action: Optional[Callable[[SettingsAction], None]] = None):
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Create background
        self.background_surface = self._create_background()
        
        # Volume settings
        self.volume_settings = audio_manager.get_volume_settings()
        
        # Create buttons
        self.buttons = self._create_buttons()
        self.volume_buttons = self._create_volume_buttons()
        
        print("Settings Screen initialized - Temple configurations ready")
    
    def _create_background(self):
        """Create settings background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Desert stone gradient for settings
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(40 + ratio * 20)
            g = int(35 + ratio * 15)
            b = int(20 + ratio * 10)
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create UI buttons."""
        buttons = []
        
        back_button = AnimatedButton(
            50, 50, 150, 40,
            "BACK TO MENU", FontSizes.BUTTON,
            action=lambda: self._handle_action(SettingsAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        return buttons
    
    def _create_volume_buttons(self) -> List[AnimatedButton]:
        """Create volume control buttons."""
        buttons = []
        
        # Master volume buttons
        master_down = AnimatedButton(
            300, 200, 40, 30, "-", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("master", -0.1)
        )
        master_up = AnimatedButton(
            500, 200, 40, 30, "+", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("master", 0.1)
        )
        buttons.extend([master_down, master_up])
        
        # Music volume buttons
        music_down = AnimatedButton(
            300, 260, 40, 30, "-", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("music", -0.1)
        )
        music_up = AnimatedButton(
            500, 260, 40, 30, "+", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("music", 0.1)
        )
        buttons.extend([music_down, music_up])
        
        # SFX volume buttons
        sfx_down = AnimatedButton(
            300, 320, 40, 30, "-", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("sfx", -0.1)
        )
        sfx_up = AnimatedButton(
            500, 320, 40, 30, "+", FontSizes.BUTTON,
            action=lambda: self._adjust_volume("sfx", 0.1)
        )
        buttons.extend([sfx_down, sfx_up])
        
        return buttons
    
    def _adjust_volume(self, volume_type: str, delta: float):
        """Adjust volume setting."""
        current = self.volume_settings[volume_type]
        new_volume = max(0.0, min(1.0, current + delta))
        self.volume_settings[volume_type] = new_volume
        
        # Apply to audio manager
        if volume_type == "master":
            audio_manager.set_master_volume(new_volume)
        elif volume_type == "music":
            audio_manager.set_music_volume(new_volume)
        elif volume_type == "sfx":
            audio_manager.set_sfx_volume(new_volume)
        
        # Play test sound for feedback
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.5)
    
    def _render_volume_controls(self, surface: pygame.Surface):
        """Render volume control interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        # Volume labels and bars
        volume_types = [
            ("Master Volume", "master", 200),
            ("Music Volume", "music", 260),
            ("SFX Volume", "sfx", 320)
        ]
        
        for label, vol_type, y in volume_types:
            # Label
            label_surface = font.render(label, True, Colors.DESERT_SAND)
            surface.blit(label_surface, (200, y))
            
            # Volume bar
            bar_x = 350
            bar_width = 120
            bar_height = 20
            
            # Background bar
            bar_rect = pygame.Rect(bar_x, y, bar_width, bar_height)
            pygame.draw.rect(surface, Colors.BLACK, bar_rect)
            pygame.draw.rect(surface, Colors.GOLD, bar_rect, 2)
            
            # Volume fill
            volume_level = self.volume_settings[vol_type]
            fill_width = int(bar_width * volume_level)
            fill_rect = pygame.Rect(bar_x, y, fill_width, bar_height)
            pygame.draw.rect(surface, Colors.LAPIS_LAZULI, fill_rect)
            
            # Volume percentage
            percent_text = f"{int(volume_level * 100)}%"
            percent_surface = font.render(percent_text, True, Colors.WHITE)
            surface.blit(percent_surface, (bar_x + bar_width + 10, y))
    
    def _handle_action(self, action: SettingsAction):
        """Handle button actions."""
        if self.on_action:
            self.on_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the settings screen."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update buttons
        all_buttons = self.buttons + self.volume_buttons
        for button in all_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(SettingsAction.BACK_TO_MENU)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_buttons = self.buttons + self.volume_buttons
                for button in all_buttons:
                    if button.handle_click(mouse_pos):
                        break
    
    def render(self, surface: pygame.Surface):
        """Render the settings screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Title
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "TEMPLE SETTINGS"
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 120))
        surface.blit(title_surface, title_rect)
        
        # Volume controls
        self._render_volume_controls(surface)
        
        # Buttons
        all_buttons = self.buttons + self.volume_buttons
        for button in all_buttons:
            button.render(surface)
        
        # Settings preview
        body_font = pygame.font.Font(None, FontSizes.BODY)
        settings_list = [
            "Master Volume: 100%",
            "Music Volume: 70%", 
            "SFX Volume: 80%",
            "Resolution: Ultrawide Detected",
            "VSync: Enabled",
            "Quality: Hades-Level"
        ]
        
        y_start = SCREEN_CENTER[1] - 60
        for i, setting in enumerate(settings_list):
            setting_surface = body_font.render(setting, True, Colors.PAPYRUS)
            setting_rect = setting_surface.get_rect(center=(SCREEN_CENTER[0], y_start + i * 30))
            surface.blit(setting_surface, setting_rect)
        
        # Implementation note
        note_font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        note_text = "Interactive settings will be implemented in SPRINT 7"
        note_surface = note_font.render(note_text, True, Colors.DESERT_SAND)
        note_rect = note_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 120))
        surface.blit(note_surface, note_rect)
        
        # Instructions
        instruction_text = "ESC: Back to Menu"
        instruction_surface = note_font.render(instruction_text, True, Colors.DESERT_SAND)
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
        
        pattern_color = (20, 18, 10)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        all_buttons = self.buttons + self.volume_buttons
        for button in all_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0