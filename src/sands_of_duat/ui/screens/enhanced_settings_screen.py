"""
Enhanced Settings Screen - SPRINT 7: Professional Settings & Options
Complete Egyptian-themed settings interface with all game options.
"""

import pygame
import math
from typing import List, Optional, Callable, Dict, Any
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.settings_manager import settings_manager, GraphicsQuality, AnimationSpeed
from ...audio.simple_audio_manager import audio_manager, SoundEffect
from ..components.animated_button import AnimatedButton

class SettingsAction(Enum):
    """Settings screen actions."""
    BACK_TO_MENU = auto()
    APPLY_SETTINGS = auto()
    RESET_DEFAULTS = auto()

class SettingsCategory(Enum):
    """Settings categories."""
    TEMPLE_VISUALS = auto()
    SACRED_SOUNDS = auto()
    DIVINE_GAMEPLAY = auto()
    SACRED_BINDINGS = auto()

class EnhancedSettingsScreen:
    """
    Professional Egyptian-themed settings screen with complete functionality.
    Features tabbed interface, real-time preview, and comprehensive options.
    """
    
    def __init__(self, on_action: Optional[Callable[[SettingsAction], None]] = None):
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.sand_particles = []
        
        # Settings state
        self.current_category = SettingsCategory.TEMPLE_VISUALS
        self.settings_changed = False
        
        # Create background and particles
        self.background_surface = self._create_background()
        self._spawn_particles()
        
        # Create UI elements
        self.category_tabs = self._create_category_tabs()
        self.settings_buttons = self._create_settings_buttons()
        self.control_buttons = self._create_control_buttons()
        
        print("Enhanced Settings Screen initialized - Temple of Configuration ready")
    
    def _create_background(self):
        """Create enhanced Egyptian temple background using 4K assets."""
        # Try to load the ultra-high resolution settings background
        from ...core.asset_loader import get_asset_loader
        asset_loader = get_asset_loader()
        settings_bg = asset_loader.load_background('settings')
        
        if settings_bg:
            # Scale ultra-high resolution background to screen with quality scaling
            background = pygame.transform.smoothscale(settings_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add mystical overlay for better UI readability
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Enhanced temple atmosphere
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                alpha = int(40 + ratio * 20)  # Subtle darkening for UI
                overlay.fill((10, 5, 0, alpha), (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            return background
        
        # Enhanced fallback: Egyptian temple stone gradient
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Professional temple stone gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(35 + ratio * 25)    # Warm stone tones
            g = int(30 + ratio * 20)    # Sandstone colors
            b = int(15 + ratio * 10)    # Rich earth browns
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _spawn_particles(self):
        """Spawn mystical sand particles."""
        for i in range(12):
            self.sand_particles.append({
                'x': SCREEN_WIDTH * (0.1 + 0.8 * (i / 12)),
                'y': SCREEN_HEIGHT * (0.2 + 0.6 * (i / 12)),
                'size': 1 + (i % 3),
                'speed': 8 + (i % 5),
                'phase': i * 0.7,
                'alpha': 80 + (i % 40)
            })
    
    def _create_category_tabs(self) -> List[AnimatedButton]:
        """Create Egyptian-themed category tabs."""
        tabs = []
        
        categories = [
            ("TEMPLE VISUALS", SettingsCategory.TEMPLE_VISUALS),
            ("SACRED SOUNDS", SettingsCategory.SACRED_SOUNDS), 
            ("DIVINE GAMEPLAY", SettingsCategory.DIVINE_GAMEPLAY),
            ("SACRED BINDINGS", SettingsCategory.SACRED_BINDINGS)
        ]
        
        tab_width = 200
        tab_height = 50
        start_x = SCREEN_CENTER[0] - (len(categories) * tab_width) // 2
        
        for i, (name, category) in enumerate(categories):
            x = start_x + i * tab_width
            tab = AnimatedButton(
                x, 100, tab_width - 10, tab_height, name, FontSizes.CARD_NAME,
                action=lambda c=category: self._switch_category(c)
            )
            tabs.append(tab)
        
        return tabs
    
    def _create_settings_buttons(self) -> Dict[SettingsCategory, List[AnimatedButton]]:
        """Create setting controls for each category."""
        buttons = {}
        
        # Temple Visuals (Graphics) Settings
        buttons[SettingsCategory.TEMPLE_VISUALS] = self._create_graphics_buttons()
        
        # Sacred Sounds (Audio) Settings  
        buttons[SettingsCategory.SACRED_SOUNDS] = self._create_audio_buttons()
        
        # Divine Gameplay Settings
        buttons[SettingsCategory.DIVINE_GAMEPLAY] = self._create_gameplay_buttons()
        
        # Sacred Bindings (Keybindings) Settings
        buttons[SettingsCategory.SACRED_BINDINGS] = self._create_keybinding_buttons()
        
        return buttons
    
    def _create_graphics_buttons(self) -> List[AnimatedButton]:
        """Create graphics settings buttons."""
        buttons = []
        
        # Resolution buttons
        res_left = AnimatedButton(
            300, 220, 40, 30, "<", FontSizes.BUTTON,
            action=lambda: self._change_resolution(-1)
        )
        res_right = AnimatedButton(
            500, 220, 40, 30, ">", FontSizes.BUTTON,
            action=lambda: self._change_resolution(1)
        )
        buttons.extend([res_left, res_right])
        
        # Quality buttons
        qual_left = AnimatedButton(
            300, 280, 40, 30, "<", FontSizes.BUTTON,
            action=lambda: self._change_quality(-1)
        )
        qual_right = AnimatedButton(
            500, 280, 40, 30, ">", FontSizes.BUTTON,
            action=lambda: self._change_quality(1)
        )
        buttons.extend([qual_left, qual_right])
        
        # Toggle buttons
        fullscreen_btn = AnimatedButton(
            300, 340, 120, 30, "Toggle", FontSizes.BUTTON,
            action=lambda: self._toggle_fullscreen()
        )
        vsync_btn = AnimatedButton(
            500, 340, 120, 30, "Toggle", FontSizes.BUTTON,
            action=lambda: self._toggle_vsync()
        )
        buttons.extend([fullscreen_btn, vsync_btn])
        
        return buttons
    
    def _create_audio_buttons(self) -> List[AnimatedButton]:
        """Create audio settings buttons."""
        buttons = []
        
        # Volume sliders - using the existing system
        volume_types = [
            ("master", 220),
            ("music", 280), 
            ("sfx", 340),
            ("ambient", 400)
        ]
        
        for vol_type, y in volume_types:
            # Decrease button
            dec_btn = AnimatedButton(
                300, y, 40, 30, "-", FontSizes.BUTTON,
                action=lambda vt=vol_type: self._adjust_volume(vt, -0.1)
            )
            # Increase button  
            inc_btn = AnimatedButton(
                500, y, 40, 30, "+", FontSizes.BUTTON,
                action=lambda vt=vol_type: self._adjust_volume(vt, 0.1)
            )
            buttons.extend([dec_btn, inc_btn])
        
        return buttons
    
    def _create_gameplay_buttons(self) -> List[AnimatedButton]:
        """Create gameplay settings buttons."""
        buttons = []
        
        # Toggle buttons for various gameplay options
        toggles = [
            ("auto_end_turn", 220),
            ("show_tooltips", 280),
            ("confirm_actions", 340),
            ("skip_animations", 400)
        ]
        
        for setting, y in toggles:
            toggle_btn = AnimatedButton(
                400, y, 120, 30, "Toggle", FontSizes.BUTTON,
                action=lambda s=setting: self._toggle_gameplay_setting(s)
            )
            buttons.append(toggle_btn)
        
        # Animation speed buttons
        speed_left = AnimatedButton(
            300, 460, 40, 30, "<", FontSizes.BUTTON,
            action=lambda: self._change_animation_speed(-1)
        )
        speed_right = AnimatedButton(
            500, 460, 40, 30, ">", FontSizes.BUTTON,
            action=lambda: self._change_animation_speed(1)
        )
        buttons.extend([speed_left, speed_right])
        
        return buttons
    
    def _create_keybinding_buttons(self) -> List[AnimatedButton]:
        """Create keybinding settings buttons."""
        buttons = []
        
        # Keybinding change buttons
        keybinds = [
            ("end_turn", 220),
            ("cancel_action", 280),
            ("deck_builder", 340),
            ("settings", 400),
            ("fullscreen", 460),
            ("screenshot", 520)
        ]
        
        for binding, y in keybinds:
            change_btn = AnimatedButton(
                400, y, 120, 30, "Change", FontSizes.BUTTON,
                action=lambda b=binding: self._change_keybinding(b)
            )
            buttons.append(change_btn)
        
        return buttons
    
    def _create_control_buttons(self) -> List[AnimatedButton]:
        """Create main control buttons."""
        buttons = []
        
        # Main control buttons
        back_btn = AnimatedButton(
            50, 50, 120, 40, "BACK", FontSizes.BUTTON,
            action=lambda: self._handle_action(SettingsAction.BACK_TO_MENU)
        )
        
        apply_btn = AnimatedButton(
            SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100, 120, 40,
            "APPLY", FontSizes.BUTTON,
            action=lambda: self._handle_action(SettingsAction.APPLY_SETTINGS)
        )
        
        reset_btn = AnimatedButton(
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 120, 40,
            "RESET", FontSizes.BUTTON,
            action=lambda: self._handle_action(SettingsAction.RESET_DEFAULTS)
        )
        
        buttons.extend([back_btn, apply_btn, reset_btn])
        return buttons
    
    def _switch_category(self, category: SettingsCategory):
        """Switch to a different settings category."""
        self.current_category = category
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _change_resolution(self, direction: int):
        """Change screen resolution."""
        resolutions = settings_manager.get_resolution_options()
        current_res = (settings_manager.graphics.resolution_width, 
                      settings_manager.graphics.resolution_height)
        
        try:
            current_idx = resolutions.index(current_res)
        except ValueError:
            current_idx = 1  # Default to 1920x1080
        
        new_idx = (current_idx + direction) % len(resolutions)
        new_res = resolutions[new_idx]
        
        settings_manager.graphics.resolution_width = new_res[0]
        settings_manager.graphics.resolution_height = new_res[1]
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _change_quality(self, direction: int):
        """Change graphics quality."""
        qualities = list(GraphicsQuality)
        current_idx = qualities.index(settings_manager.graphics.quality)
        new_idx = (current_idx + direction) % len(qualities)
        
        settings_manager.graphics.quality = qualities[new_idx]
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        settings_manager.graphics.fullscreen = not settings_manager.graphics.fullscreen
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _toggle_vsync(self):
        """Toggle VSync."""
        settings_manager.graphics.vsync = not settings_manager.graphics.vsync
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _adjust_volume(self, volume_type: str, delta: float):
        """Adjust volume setting."""
        current = getattr(settings_manager.audio, f"{volume_type}_volume")
        new_volume = max(0.0, min(1.0, current + delta))
        setattr(settings_manager.audio, f"{volume_type}_volume", new_volume)
        
        # Apply to audio manager immediately
        if volume_type == "master":
            audio_manager.set_master_volume(new_volume)
        elif volume_type == "music":
            audio_manager.set_music_volume(new_volume)
        elif volume_type == "sfx":
            audio_manager.set_sfx_volume(new_volume)
        elif volume_type == "ambient":
            audio_manager.set_ambient_volume(new_volume)
        
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.5)
    
    def _toggle_gameplay_setting(self, setting: str):
        """Toggle a gameplay setting."""
        current = getattr(settings_manager.gameplay, setting)
        setattr(settings_manager.gameplay, setting, not current)
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _change_animation_speed(self, direction: int):
        """Change animation speed setting."""
        speeds = list(AnimationSpeed)
        current_idx = speeds.index(settings_manager.gameplay.animation_speed)
        new_idx = (current_idx + direction) % len(speeds)
        
        settings_manager.gameplay.animation_speed = speeds[new_idx]
        self.settings_changed = True
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _change_keybinding(self, binding: str):
        """Change a keybinding (placeholder for now)."""
        # This would open a key capture dialog in a full implementation
        audio_manager.play_sound(SoundEffect.BUTTON_HOVER, 0.4)
        print(f"Would change keybinding for: {binding}")
    
    def _handle_action(self, action: SettingsAction):
        """Handle main settings actions."""
        if action == SettingsAction.APPLY_SETTINGS:
            settings_manager.save_settings()
            settings_manager.apply_audio_settings(audio_manager)
            self.settings_changed = False
            audio_manager.play_sound(SoundEffect.VICTORY_FANFARE, 0.3)
            print("Settings applied and saved")
            
        elif action == SettingsAction.RESET_DEFAULTS:
            settings_manager.reset_to_defaults()
            settings_manager.apply_audio_settings(audio_manager)
            self.settings_changed = True
            audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
            print("Settings reset to defaults")
        
        if self.on_action:
            self.on_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the enhanced settings screen."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update particles
        for particle in self.sand_particles:
            particle['x'] += math.sin(self.animation_time * 0.4 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.2 + particle['phase']) * particle['speed'] * dt * 0.3
        
        # Update all buttons
        all_buttons = (self.category_tabs + 
                      self.settings_buttons.get(self.current_category, []) +
                      self.control_buttons)
        
        for button in all_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(SettingsAction.BACK_TO_MENU)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in all_buttons:
                    if button.handle_click(mouse_pos):
                        break
    
    def render(self, surface: pygame.Surface):
        """Render the enhanced settings screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Particles
        self._render_particles(surface)
        
        # Title
        self._render_title(surface)
        
        # Category tabs
        self._render_category_tabs(surface)
        
        # Current category content
        self._render_current_category(surface)
        
        # Control buttons
        for button in self.control_buttons:
            button.render(surface)
        
        # Settings changed indicator
        if self.settings_changed:
            self._render_changes_indicator(surface)
        
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
        
        pattern_color = (15, 12, 8)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
    
    def _render_particles(self, surface: pygame.Surface):
        """Render mystical sand particles."""
        for particle in self.sand_particles:
            alpha = int(particle['alpha'] + 40 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*Colors.GOLD, min(255, alpha)))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_title(self, surface: pygame.Surface):
        """Render the main title."""
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "TEMPLE OF CONFIGURATION"
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.DESERT_SAND)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 50))
        glow_surface.set_alpha(120)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 48))
        surface.blit(title_surface, title_rect)
    
    def _render_category_tabs(self, surface: pygame.Surface):
        """Render category tabs with active highlighting."""
        for i, tab in enumerate(self.category_tabs):
            # Highlight active tab
            category = list(SettingsCategory)[i]
            if category == self.current_category:
                highlight_rect = tab.rect.inflate(4, 4)
                highlight_surface = pygame.Surface(highlight_rect.size, pygame.SRCALPHA)
                highlight_surface.fill((*Colors.GOLD, 80))
                surface.blit(highlight_surface, highlight_rect.topleft)
            
            tab.render(surface)
    
    def _render_current_category(self, surface: pygame.Surface):
        """Render the current category's settings."""
        if self.current_category == SettingsCategory.TEMPLE_VISUALS:
            self._render_graphics_settings(surface)
        elif self.current_category == SettingsCategory.SACRED_SOUNDS:
            self._render_audio_settings(surface)
        elif self.current_category == SettingsCategory.DIVINE_GAMEPLAY:
            self._render_gameplay_settings(surface)
        elif self.current_category == SettingsCategory.SACRED_BINDINGS:
            self._render_keybinding_settings(surface)
    
    def _render_graphics_settings(self, surface: pygame.Surface):
        """Render graphics settings interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        # Resolution
        res_text = f"Resolution: {settings_manager.graphics.resolution_width}x{settings_manager.graphics.resolution_height}"
        res_surface = font.render(res_text, True, Colors.DESERT_SAND)
        surface.blit(res_surface, (200, 225))
        
        # Quality
        quality_text = f"Quality: {settings_manager.graphics.quality.name}"
        quality_surface = font.render(quality_text, True, Colors.DESERT_SAND)
        surface.blit(quality_surface, (200, 285))
        
        # Toggles
        fullscreen_text = f"Fullscreen: {'ON' if settings_manager.graphics.fullscreen else 'OFF'}"
        fullscreen_surface = font.render(fullscreen_text, True, Colors.DESERT_SAND)
        surface.blit(fullscreen_surface, (200, 345))
        
        vsync_text = f"VSync: {'ON' if settings_manager.graphics.vsync else 'OFF'}"
        vsync_surface = font.render(vsync_text, True, Colors.DESERT_SAND)
        surface.blit(vsync_surface, (450, 345))
        
        # Render buttons
        for button in self.settings_buttons[self.current_category]:
            button.render(surface)
    
    def _render_audio_settings(self, surface: pygame.Surface):
        """Render audio settings interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        volume_types = [
            ("Master Volume", "master", 220),
            ("Music Volume", "music", 280),
            ("SFX Volume", "sfx", 340),
            ("Ambient Volume", "ambient", 400)
        ]
        
        for label, vol_type, y in volume_types:
            # Label
            label_surface = font.render(label, True, Colors.DESERT_SAND)
            surface.blit(label_surface, (200, y + 5))
            
            # Volume bar
            volume = getattr(settings_manager.audio, f"{vol_type}_volume")
            bar_x = 350
            bar_width = 120
            bar_height = 20
            
            # Background bar
            bar_rect = pygame.Rect(bar_x, y, bar_width, bar_height)
            pygame.draw.rect(surface, Colors.BLACK, bar_rect)
            pygame.draw.rect(surface, Colors.GOLD, bar_rect, 2)
            
            # Volume fill
            fill_width = int(bar_width * volume)
            fill_rect = pygame.Rect(bar_x, y, fill_width, bar_height)
            pygame.draw.rect(surface, Colors.LAPIS_LAZULI, fill_rect)
            
            # Percentage
            percent_text = f"{int(volume * 100)}%"
            percent_surface = font.render(percent_text, True, Colors.WHITE)
            surface.blit(percent_surface, (bar_x + bar_width + 10, y + 2))
        
        # Render buttons
        for button in self.settings_buttons[self.current_category]:
            button.render(surface)
    
    def _render_gameplay_settings(self, surface: pygame.Surface):
        """Render gameplay settings interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        settings_list = [
            ("Auto End Turn", settings_manager.gameplay.auto_end_turn, 220),
            ("Show Tooltips", settings_manager.gameplay.show_tooltips, 280),
            ("Confirm Actions", settings_manager.gameplay.confirm_actions, 340),
            ("Skip Animations", settings_manager.gameplay.skip_animations, 400),
        ]
        
        for label, value, y in settings_list:
            text = f"{label}: {'ON' if value else 'OFF'}"
            text_surface = font.render(text, True, Colors.DESERT_SAND)
            surface.blit(text_surface, (200, y + 5))
        
        # Animation speed
        speed_text = f"Animation Speed: {settings_manager.gameplay.animation_speed.name}"
        speed_surface = font.render(speed_text, True, Colors.DESERT_SAND)
        surface.blit(speed_surface, (200, 465))
        
        # Render buttons
        for button in self.settings_buttons[self.current_category]:
            button.render(surface)
    
    def _render_keybinding_settings(self, surface: pygame.Surface):
        """Render keybinding settings interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        keybindings = [
            ("End Turn", settings_manager.keybindings.end_turn, 220),
            ("Cancel Action", settings_manager.keybindings.cancel_action, 280),
            ("Deck Builder", settings_manager.keybindings.deck_builder, 340),
            ("Settings", settings_manager.keybindings.settings, 400),
            ("Fullscreen", settings_manager.keybindings.fullscreen, 460),
            ("Screenshot", settings_manager.keybindings.screenshot, 520),
        ]
        
        for label, key, y in keybindings:
            text = f"{label}: {key}"
            text_surface = font.render(text, True, Colors.DESERT_SAND)
            surface.blit(text_surface, (200, y + 5))
        
        # Render buttons
        for button in self.settings_buttons[self.current_category]:
            button.render(surface)
    
    def _render_changes_indicator(self, surface: pygame.Surface):
        """Render indicator that settings have changed."""
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        text = "* Settings changed - click APPLY to save"
        text_surface = font.render(text, True, Colors.GOLD)
        surface.blit(text_surface, (SCREEN_CENTER[0] - text_surface.get_width() // 2, SCREEN_HEIGHT - 150))
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        all_buttons = (self.category_tabs + 
                      self.control_buttons +
                      [btn for btn_list in self.settings_buttons.values() for btn in btn_list])
        
        for button in all_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0