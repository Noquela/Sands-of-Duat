"""
Professional Settings Screen - AAA Quality Configuration Interface
Features categorized settings with beautiful sliders and controls.
"""

import pygame
import math
from typing import List, Optional, Callable, Tuple, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.settings_manager import settings_manager
from ...audio.simple_audio_manager import audio_manager, AudioTrack
from ..components.hades_button import HadesButton
from ..components.smooth_transitions import smooth_transitions, TransitionType, EasingType
from ..components.responsive_typography import responsive_typography, TextStyle

class SettingsCategory(Enum):
    """Settings categories."""
    AUDIO = auto()
    GRAPHICS = auto()
    GAMEPLAY = auto()
    CONTROLS = auto()
    ADVANCED = auto()

class SettingsAction(Enum):
    """Settings screen actions."""
    BACK_TO_MENU = auto()
    SAVE_SETTINGS = auto()
    RESET_DEFAULTS = auto()
    APPLY_CHANGES = auto()

@dataclass
class SettingSlider:
    """A professional slider control."""
    x: int
    y: int
    width: int
    height: int
    min_value: float
    max_value: float
    current_value: float
    setting_key: str
    label: str
    format_func: Callable[[float], str] = lambda x: f"{x:.1f}"
    
    def __post_init__(self):
        self.dragging = False
        self.hover = False
        self.animation_value = self.current_value

@dataclass  
class SettingToggle:
    """A professional toggle control."""
    x: int
    y: int
    width: int
    height: int
    setting_key: str
    label: str
    current_value: bool = False
    
    def __post_init__(self):
        self.hover = False
        self.animation_progress = 1.0 if self.current_value else 0.0

class ProfessionalSettings:
    """
    Professional settings screen with AAA game quality.
    Features beautiful categorized settings with smooth controls.
    """
    
    def __init__(self, on_action: Optional[Callable[[SettingsAction], None]] = None):
        """Initialize the settings screen."""
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.category_transition_progress = 0.0
        
        # Current category
        self.current_category = SettingsCategory.AUDIO
        self.target_category = SettingsCategory.AUDIO
        
        # Controls
        self.sliders: Dict[SettingsCategory, List[SettingSlider]] = {}
        self.toggles: Dict[SettingsCategory, List[SettingToggle]] = {}
        self.category_buttons: List[HadesButton] = []
        self.action_buttons: List[HadesButton] = []
        
        # Settings state
        self.pending_changes = {}
        self.has_changes = False
        
        # Create background
        self.background_surface = self._create_background()
        
        # Initialize all controls
        self._create_category_buttons()
        self._create_settings_controls()
        self._create_action_buttons()
        
        # Load current settings
        self._load_current_settings()
        
        # Start fade-in
        smooth_transitions.fade_in_element("settings_screen", Timing.FADE_DURATION)
        
        print("Professional Settings Screen initialized - Temple of Configuration ready")
    
    def _create_background(self):
        """Create atmospheric settings background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(25 + ratio * 15)
            g = int(15 + ratio * 10)
            b = int(45 + ratio * 25)
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add subtle pattern
        pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, 100):
            for y in range(0, SCREEN_HEIGHT, 100):
                alpha = int(20 + 15 * math.sin(x * 0.01 + y * 0.01))
                pattern_surface.fill(Colors.GOLD, (x, y, 2, 20))
                pattern_surface.set_alpha(alpha)
        
        background.blit(pattern_surface, (0, 0))
        return background
    
    def _create_category_buttons(self):
        """Create category navigation buttons."""
        categories = [
            (SettingsCategory.AUDIO, "Audio", "𓂀", Colors.LAPIS_LAZULI),
            (SettingsCategory.GRAPHICS, "Graphics", "𓇳", Colors.GOLD), 
            (SettingsCategory.GAMEPLAY, "Gameplay", "⚔️", Colors.RED),
            (SettingsCategory.CONTROLS, "Controls", "𓊪", Colors.GREEN),
            (SettingsCategory.ADVANCED, "Advanced", "𓊽", Colors.PURPLE)
        ]
        
        button_width = 140
        button_height = 50
        spacing = 20
        start_x = 50
        start_y = 150
        
        for i, (category, text, icon, color) in enumerate(categories):
            y = start_y + i * (button_height + spacing)
            
            button = HadesButton(
                start_x, y, button_width, button_height,
                text=text,
                theme_color=color,
                hieroglyph=icon,
                on_click=lambda c=category: self._change_category(c)
            )
            self.category_buttons.append(button)
    
    def _create_settings_controls(self):
        """Create all settings controls organized by category."""
        # Audio settings
        self.sliders[SettingsCategory.AUDIO] = [
            SettingSlider(400, 200, 300, 30, 0.0, 1.0, 0.7, "master_volume", "Master Volume", 
                         lambda x: f"{int(x * 100)}%"),
            SettingSlider(400, 260, 300, 30, 0.0, 1.0, 0.7, "music_volume", "Music Volume",
                         lambda x: f"{int(x * 100)}%"),
            SettingSlider(400, 320, 300, 30, 0.0, 1.0, 0.8, "sfx_volume", "Sound Effects",
                         lambda x: f"{int(x * 100)}%"),
            SettingSlider(400, 380, 300, 30, 0.0, 1.0, 0.6, "ui_volume", "UI Sounds",
                         lambda x: f"{int(x * 100)}%")
        ]
        
        self.toggles[SettingsCategory.AUDIO] = [
            SettingToggle(400, 450, 60, 30, "mute_audio", "Mute All Audio"),
            SettingToggle(400, 500, 60, 30, "spatial_audio", "3D Spatial Audio")
        ]
        
        # Graphics settings
        self.sliders[SettingsCategory.GRAPHICS] = [
            SettingSlider(400, 200, 300, 30, 30, 144, 60, "target_fps", "Target FPS",
                         lambda x: f"{int(x)} FPS"),
            SettingSlider(400, 260, 300, 30, 0.5, 2.0, 1.0, "ui_scale", "UI Scale",
                         lambda x: f"{x:.1f}x"),
            SettingSlider(400, 320, 300, 30, 0.0, 1.0, 0.8, "particle_density", "Particle Effects",
                         lambda x: f"{int(x * 100)}%"),
            SettingSlider(400, 380, 300, 30, 0.0, 1.0, 1.0, "animation_quality", "Animation Quality",
                         lambda x: ["Low", "Medium", "High", "Ultra"][int(x * 3)])
        ]
        
        self.toggles[SettingsCategory.GRAPHICS] = [
            SettingToggle(400, 450, 60, 30, "fullscreen", "Fullscreen Mode"),
            SettingToggle(400, 500, 60, 30, "vsync", "Vertical Sync"),
            SettingToggle(400, 550, 60, 30, "show_fps", "Show FPS Counter")
        ]
        
        # Gameplay settings
        self.sliders[SettingsCategory.GAMEPLAY] = [
            SettingSlider(400, 200, 300, 30, 0.5, 3.0, 1.0, "game_speed", "Game Speed",
                         lambda x: f"{x:.1f}x"),
            SettingSlider(400, 260, 300, 30, 1, 7, 4, "difficulty", "Difficulty",
                         lambda x: ["Easy", "Normal", "Hard", "Expert", "Master", "Divine", "Legendary"][int(x) - 1]),
            SettingSlider(400, 320, 300, 30, 0.0, 2.0, 0.5, "tooltip_delay", "Tooltip Delay",
                         lambda x: f"{x:.1f}s")
        ]
        
        self.toggles[SettingsCategory.GAMEPLAY] = [
            SettingToggle(400, 380, 60, 30, "auto_save", "Auto Save"),
            SettingToggle(400, 430, 60, 30, "pause_on_focus_loss", "Pause When Unfocused"),
            SettingToggle(400, 480, 60, 30, "confirm_actions", "Confirm Important Actions"),
            SettingToggle(400, 530, 60, 30, "advanced_tooltips", "Advanced Tooltips")
        ]
        
        # Controls settings  
        self.sliders[SettingsCategory.CONTROLS] = [
            SettingSlider(400, 200, 300, 30, 0.1, 2.0, 1.0, "mouse_sensitivity", "Mouse Sensitivity",
                         lambda x: f"{x:.1f}x"),
            SettingSlider(400, 260, 300, 30, 0.0, 1.0, 0.2, "scroll_speed", "Scroll Speed",
                         lambda x: f"{x:.1f}x")
        ]
        
        self.toggles[SettingsCategory.CONTROLS] = [
            SettingToggle(400, 320, 60, 30, "invert_mouse", "Invert Mouse Y"),
            SettingToggle(400, 370, 60, 30, "edge_scrolling", "Edge Scrolling"),
            SettingToggle(400, 420, 60, 30, "right_click_context", "Right-Click Context Menus")
        ]
        
        # Advanced settings
        self.sliders[SettingsCategory.ADVANCED] = [
            SettingSlider(400, 200, 300, 30, 512, 4096, 1024, "texture_memory", "Texture Memory (MB)",
                         lambda x: f"{int(x)} MB"),
            SettingSlider(400, 260, 300, 30, 1, 8, 4, "worker_threads", "Background Threads",
                         lambda x: f"{int(x)} threads")
        ]
        
        self.toggles[SettingsCategory.ADVANCED] = [
            SettingToggle(400, 320, 60, 30, "debug_mode", "Debug Mode"),
            SettingToggle(400, 370, 60, 30, "performance_monitoring", "Performance Monitoring"),
            SettingToggle(400, 420, 60, 30, "log_detailed_events", "Detailed Event Logging"),
            SettingToggle(400, 470, 60, 30, "experimental_features", "Experimental Features")
        ]
    
    def _create_action_buttons(self):
        """Create action buttons at the bottom."""
        button_configs = [
            ("SAVE", SettingsAction.SAVE_SETTINGS, Colors.GREEN, "💾"),
            ("RESET", SettingsAction.RESET_DEFAULTS, Colors.RED, "🔄"),
            ("APPLY", SettingsAction.APPLY_CHANGES, Colors.GOLD, "✓"),
            ("BACK", SettingsAction.BACK_TO_MENU, Colors.GRAY, "⬅️")
        ]
        
        button_width = 100
        button_height = 40
        spacing = 20
        total_width = len(button_configs) * button_width + (len(button_configs) - 1) * spacing
        start_x = SCREEN_CENTER[0] - total_width // 2
        y = SCREEN_HEIGHT - 100
        
        for i, (text, action, color, icon) in enumerate(button_configs):
            x = start_x + i * (button_width + spacing)
            
            button = HadesButton(
                x, y, button_width, button_height,
                text=text,
                theme_color=color,
                hieroglyph=icon,
                on_click=lambda a=action: self._handle_action(a)
            )
            self.action_buttons.append(button)
    
    def _load_current_settings(self):
        """Load current settings from settings manager."""
        # This would load from the actual settings manager
        # For now, using default values set in the controls
        pass
    
    def _change_category(self, category: SettingsCategory):
        """Change the current settings category."""
        if category != self.current_category:
            self.target_category = category
            self.category_transition_progress = 0.0
    
    def _handle_action(self, action: SettingsAction):
        """Handle action button clicks."""
        if action == SettingsAction.SAVE_SETTINGS:
            self._save_settings()
        elif action == SettingsAction.RESET_DEFAULTS:
            self._reset_to_defaults()
        elif action == SettingsAction.APPLY_CHANGES:
            self._apply_changes()
        elif action == SettingsAction.BACK_TO_MENU:
            if self.on_action:
                self.on_action(action)
    
    def _save_settings(self):
        """Save all current settings."""
        # Apply all pending changes
        self._apply_changes()
        
        # Save to settings manager
        settings_manager.save_settings()
        
        self.has_changes = False
        print("Settings saved successfully!")
    
    def _reset_to_defaults(self):
        """Reset all settings to default values."""
        # Reset all sliders and toggles to defaults
        for category_sliders in self.sliders.values():
            for slider in category_sliders:
                # Set to reasonable defaults
                if "volume" in slider.setting_key:
                    slider.current_value = 0.7
                elif "fps" in slider.setting_key:
                    slider.current_value = 60
                elif "scale" in slider.setting_key:
                    slider.current_value = 1.0
                else:
                    slider.current_value = (slider.min_value + slider.max_value) / 2
        
        for category_toggles in self.toggles.values():
            for toggle in category_toggles:
                # Set reasonable defaults
                toggle.current_value = toggle.setting_key in ["auto_save", "vsync", "advanced_tooltips"]
                toggle.animation_progress = 1.0 if toggle.current_value else 0.0
        
        self.has_changes = True
        print("Settings reset to defaults")
    
    def _apply_changes(self):
        """Apply current settings to the game."""
        # Audio settings
        if SettingsCategory.AUDIO in self.sliders:
            for slider in self.sliders[SettingsCategory.AUDIO]:
                if slider.setting_key == "master_volume":
                    audio_manager.set_master_volume(slider.current_value)
                elif slider.setting_key == "music_volume":
                    audio_manager.set_music_volume(slider.current_value)
                elif slider.setting_key == "sfx_volume":
                    audio_manager.set_sfx_volume(slider.current_value)
        
        print("Settings applied!")
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update settings screen."""
        self.animation_time += dt
        
        # Update fade-in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
        
        # Update category transition
        if self.target_category != self.current_category:
            self.category_transition_progress += dt * 5.0
            if self.category_transition_progress >= 1.0:
                self.current_category = self.target_category
                self.category_transition_progress = 0.0
        
        # Update category buttons
        for i, button in enumerate(self.category_buttons):
            # Highlight current category
            if list(SettingsCategory)[i] == self.current_category:
                button.glow_intensity = 1.0
            else:
                button.glow_intensity = 0.0
            
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Update action buttons
        for button in self.action_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Update current category controls
        self._update_category_controls(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.on_action:
                        self.on_action(SettingsAction.BACK_TO_MENU)
                elif event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self._save_settings()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_release(mouse_pos)
            
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(mouse_pos)
    
    def _update_category_controls(self, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update controls for the current category."""
        # Update sliders
        if self.current_category in self.sliders:
            for slider in self.sliders[self.current_category]:
                self._update_slider(slider, dt, mouse_pos, mouse_pressed)
        
        # Update toggles
        if self.current_category in self.toggles:
            for toggle in self.toggles[self.current_category]:
                self._update_toggle(toggle, dt, mouse_pos)
    
    def _update_slider(self, slider: SettingSlider, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update individual slider."""
        slider_rect = pygame.Rect(slider.x, slider.y, slider.width, slider.height)
        slider.hover = slider_rect.collidepoint(mouse_pos)
        
        # Smooth animation
        slider.animation_value += (slider.current_value - slider.animation_value) * dt * 8.0
        
        # Handle dragging
        if slider.dragging and mouse_pressed:
            # Calculate new value based on mouse position
            relative_x = mouse_pos[0] - slider.x
            progress = max(0.0, min(1.0, relative_x / slider.width))
            new_value = slider.min_value + progress * (slider.max_value - slider.min_value)
            
            if abs(new_value - slider.current_value) > 0.001:
                slider.current_value = new_value
                self.has_changes = True
    
    def _update_toggle(self, toggle: SettingToggle, dt: float, mouse_pos: Tuple[int, int]):
        """Update individual toggle."""
        toggle_rect = pygame.Rect(toggle.x, toggle.y, toggle.width, toggle.height)
        toggle.hover = toggle_rect.collidepoint(mouse_pos)
        
        # Smooth animation
        target = 1.0 if toggle.current_value else 0.0
        toggle.animation_progress += (target - toggle.animation_progress) * dt * 8.0
    
    def _handle_mouse_click(self, mouse_pos: Tuple[int, int]):
        """Handle mouse click events."""
        # Check sliders
        if self.current_category in self.sliders:
            for slider in self.sliders[self.current_category]:
                slider_rect = pygame.Rect(slider.x, slider.y, slider.width, slider.height)
                if slider_rect.collidepoint(mouse_pos):
                    slider.dragging = True
                    return
        
        # Check toggles
        if self.current_category in self.toggles:
            for toggle in self.toggles[self.current_category]:
                toggle_rect = pygame.Rect(toggle.x, toggle.y, toggle.width, toggle.height)
                if toggle_rect.collidepoint(mouse_pos):
                    toggle.current_value = not toggle.current_value
                    self.has_changes = True
                    return
    
    def _handle_mouse_release(self, mouse_pos: Tuple[int, int]):
        """Handle mouse release events."""
        # Stop all slider dragging
        for category_sliders in self.sliders.values():
            for slider in category_sliders:
                slider.dragging = False
    
    def _handle_mouse_motion(self, mouse_pos: Tuple[int, int]):
        """Handle mouse motion events."""
        pass
    
    def render(self, surface: pygame.Surface):
        """Render the settings screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Title
        responsive_typography.render_text(
            "TEMPLE OF CONFIGURATION", TextStyle.TITLE_LARGE, surface,
            (SCREEN_CENTER[0], 80), center=True, custom_color=Colors.GOLD
        )
        
        # Category buttons
        for button in self.category_buttons:
            button.render(surface, pygame.font.Font(None, FontSizes.BUTTON))
        
        # Current category title
        category_name = self.current_category.name.title()
        responsive_typography.render_text(
            f"{category_name} Settings", TextStyle.SUBTITLE, surface,
            (500, 150), custom_color=Colors.PAPYRUS
        )
        
        # Current category controls
        self._render_category_controls(surface)
        
        # Action buttons
        for button in self.action_buttons:
            button.render(surface, pygame.font.Font(None, FontSizes.BUTTON))
        
        # Changes indicator
        if self.has_changes:
            responsive_typography.render_text(
                "⚠️ You have unsaved changes", TextStyle.CARD_TEXT, surface,
                (SCREEN_CENTER[0], SCREEN_HEIGHT - 150), center=True, custom_color=Colors.ORANGE
            )
        
        # Fade-in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
    
    def _render_category_controls(self, surface: pygame.Surface):
        """Render controls for the current category."""
        # Render sliders
        if self.current_category in self.sliders:
            for slider in self.sliders[self.current_category]:
                self._render_slider(surface, slider)
        
        # Render toggles
        if self.current_category in self.toggles:
            for toggle in self.toggles[self.current_category]:
                self._render_toggle(surface, toggle)
    
    def _render_slider(self, surface: pygame.Surface, slider: SettingSlider):
        """Render an individual slider."""
        # Label
        responsive_typography.render_text(
            slider.label, TextStyle.CARD_TEXT, surface,
            (slider.x, slider.y - 25), custom_color=Colors.PAPYRUS
        )
        
        # Slider track
        track_rect = pygame.Rect(slider.x, slider.y + 10, slider.width, 6)
        pygame.draw.rect(surface, Colors.BACKGROUND_SECONDARY, track_rect, border_radius=3)
        pygame.draw.rect(surface, Colors.GOLD, track_rect, width=1, border_radius=3)
        
        # Slider fill
        progress = (slider.animation_value - slider.min_value) / (slider.max_value - slider.min_value)
        fill_width = int(progress * slider.width)
        fill_rect = pygame.Rect(slider.x, slider.y + 10, fill_width, 6)
        pygame.draw.rect(surface, Colors.LAPIS_LAZULI, fill_rect, border_radius=3)
        
        # Slider handle
        handle_x = slider.x + fill_width
        handle_y = slider.y + 13
        handle_size = 8 if not slider.hover else 10
        
        # Handle glow
        if slider.hover or slider.dragging:
            glow_surface = pygame.Surface((handle_size * 3, handle_size * 3), pygame.SRCALPHA)
            glow_surface.fill(Colors.GOLD)
            glow_surface.set_alpha(60)
            surface.blit(glow_surface, (handle_x - handle_size * 1.5, handle_y - handle_size * 1.5))
        
        pygame.draw.circle(surface, Colors.GOLD, (handle_x, handle_y), handle_size)
        pygame.draw.circle(surface, Colors.WHITE, (handle_x, handle_y), handle_size - 2)
        
        # Value display
        value_text = slider.format_func(slider.current_value)
        responsive_typography.render_text(
            value_text, TextStyle.CARD_TEXT, surface,
            (slider.x + slider.width + 20, slider.y), custom_color=Colors.GOLD
        )
    
    def _render_toggle(self, surface: pygame.Surface, toggle: SettingToggle):
        """Render an individual toggle."""
        # Label
        responsive_typography.render_text(
            toggle.label, TextStyle.CARD_TEXT, surface,
            (toggle.x + 80, toggle.y + 5), custom_color=Colors.PAPYRUS
        )
        
        # Toggle background
        bg_rect = pygame.Rect(toggle.x, toggle.y, toggle.width, toggle.height)
        bg_color = Colors.GREEN if toggle.current_value else Colors.BACKGROUND_SECONDARY
        pygame.draw.rect(surface, bg_color, bg_rect, border_radius=15)
        
        # Toggle border
        border_color = Colors.GOLD if toggle.hover else Colors.GRAY
        pygame.draw.rect(surface, border_color, bg_rect, width=2, border_radius=15)
        
        # Toggle handle
        handle_radius = toggle.height // 2 - 4
        handle_travel = toggle.width - toggle.height
        handle_x = toggle.x + handle_radius + 4 + int(handle_travel * toggle.animation_progress)
        handle_y = toggle.y + toggle.height // 2
        
        # Handle shadow
        shadow_surface = pygame.Surface((handle_radius * 3, handle_radius * 3), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0))
        shadow_surface.set_alpha(50)
        surface.blit(shadow_surface, (handle_x - handle_radius * 1.5, handle_y - handle_radius * 1.5 + 2))
        
        pygame.draw.circle(surface, Colors.WHITE, (handle_x, handle_y), handle_radius)
        
        # Status text
        status_text = "ON" if toggle.current_value else "OFF"
        status_color = Colors.GREEN if toggle.current_value else Colors.RED
        responsive_typography.render_text(
            status_text, TextStyle.TOOLTIP, surface,
            (toggle.x + toggle.width + 20, toggle.y + 8), custom_color=status_color
        )
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.animation_time = 0.0
        
        # Start ambient music
        audio_manager.play_music(AudioTrack.AMBIENT, fade_in=2.0)