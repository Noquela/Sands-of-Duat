"""
Animation Generator Screen - ComfyUI Integration Interface
Professional interface for managing Egyptian card animation generation.
"""

import pygame
import math
import asyncio
from typing import List, Optional, Callable, Dict, Any
from enum import Enum, auto
from pathlib import Path

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...audio.simple_audio_manager import audio_manager, SoundEffect
from ..components.animated_button import AnimatedButton
from ..effects.advanced_visual_effects import advanced_visual_effects
from ...animation.card_animation_generator import card_animation_generator, AnimationPriority

class AnimationAction(Enum):
    """Animation generator actions."""
    BACK_TO_MENU = auto()
    GENERATE_SINGLE = auto()
    GENERATE_GOD_COLLECTION = auto()
    GENERATE_ALL_CARDS = auto()
    VIEW_GENERATED = auto()
    TOGGLE_COMFYUI = auto()

class GenerationTab(Enum):
    """Generation interface tabs."""
    SINGLE_CARD = auto()
    BATCH_GENERATION = auto()
    MONITORING = auto()
    SETTINGS = auto()

class AnimationGeneratorScreen:
    """
    Professional animation generation interface with Egyptian theming.
    Provides full control over ComfyUI integration and batch generation.
    """
    
    def __init__(self, on_action: Optional[Callable[[AnimationAction], None]] = None):
        """Initialize animation generator screen."""
        self.on_action = on_action
        
        # UI state
        self.current_tab = GenerationTab.SINGLE_CARD
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Generation state
        self.is_initializing = False
        self.is_generating = False
        self.comfyui_connected = False
        self.selected_card_id = None
        self.selected_god = "ra"
        self.generation_progress = 0.0
        
        # Card database
        self.card_list = []
        self.filtered_cards = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Background and particles
        self.background_surface = self._create_background()
        self.mystical_particles = self._create_particles()
        
        # UI components
        self.tab_buttons = self._create_tab_buttons()
        self.generation_buttons = self._create_generation_buttons()
        self.card_buttons = []
        self.status_display = {}
        
        # Initialize async
        self._initialize_async()
        
        print("Animation Generator Screen initialized - ComfyUI Interface ready")
    
    def _create_background(self) -> pygame.Surface:
        """Create mystical ComfyUI integration background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Deep tech-mystical gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(25 + ratio * 15)    # Deep blue-purple
            g = int(15 + ratio * 25)    # Mystical tech colors
            b = int(45 + ratio * 30)    # Rich digital atmosphere
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add circuit-like mystical patterns
        import random
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(2, 8)
            alpha = random.randint(30, 80)
            
            # Golden tech particles
            particle_color = (*Colors.GOLD, alpha)
            pygame.draw.circle(background, Colors.GOLD, (x, y), size)
        
        return background
    
    def _create_particles(self) -> List[Dict]:
        """Create mystical tech particles."""
        particles = []
        for i in range(15):
            particles.append({
                'x': SCREEN_WIDTH * (0.1 + 0.8 * (i / 15)),
                'y': SCREEN_HEIGHT * (0.1 + 0.8 * (i / 15)),
                'size': 2 + (i % 4),
                'speed': 10 + (i % 8),
                'phase': i * 0.5,
                'alpha': 60 + (i % 50),
                'color': Colors.LAPIS_LAZULI if i % 2 else Colors.GOLD
            })
        return particles
    
    def _create_tab_buttons(self) -> List[AnimatedButton]:
        """Create tab navigation buttons."""
        tabs = [
            ("SINGLE CARD", GenerationTab.SINGLE_CARD),
            ("BATCH GEN", GenerationTab.BATCH_GENERATION),
            ("MONITORING", GenerationTab.MONITORING),
            ("SETTINGS", GenerationTab.SETTINGS)
        ]
        
        tab_buttons = []
        tab_width = 180
        tab_height = 45
        start_x = SCREEN_CENTER[0] - (len(tabs) * tab_width) // 2
        
        for i, (name, tab) in enumerate(tabs):
            x = start_x + i * tab_width
            button = AnimatedButton(
                x, 80, tab_width - 10, tab_height, name, FontSizes.BODY,
                action=lambda t=tab: self._switch_tab(t)
            )
            tab_buttons.append(button)
        
        return tab_buttons
    
    def _create_generation_buttons(self) -> List[AnimatedButton]:
        """Create main generation control buttons."""
        buttons = []
        
        # Initialize ComfyUI button
        init_btn = AnimatedButton(
            50, 150, 200, 50, "CONNECT COMFYUI", FontSizes.BUTTON,
            action=lambda: self._initialize_comfyui()
        )
        buttons.append(init_btn)
        
        # Single card generation
        single_btn = AnimatedButton(
            300, 200, 180, 45, "GENERATE CARD", FontSizes.BUTTON,
            action=lambda: self._generate_single_card()
        )
        buttons.append(single_btn)
        
        # God collection generation
        god_btn = AnimatedButton(
            500, 200, 200, 45, "GENERATE GOD SET", FontSizes.BUTTON,
            action=lambda: self._generate_god_collection()
        )
        buttons.append(god_btn)
        
        # Full collection generation
        all_btn = AnimatedButton(
            720, 200, 180, 45, "GENERATE ALL", FontSizes.BUTTON,
            action=lambda: self._generate_all_cards()
        )
        buttons.append(all_btn)
        
        # Back button
        back_btn = AnimatedButton(
            50, 50, 120, 40, "BACK", FontSizes.BUTTON,
            action=lambda: self._handle_action(AnimationAction.BACK_TO_MENU)
        )
        buttons.append(back_btn)
        
        return buttons
    
    def _initialize_async(self):
        """Initialize async components."""
        # This would be called from the main game loop
        pass
    
    async def initialize_animation_system(self):
        """Initialize the animation generation system."""
        self.is_initializing = True
        
        try:
            # Initialize card animation generator
            success = await card_animation_generator.initialize()
            
            if success:
                self.comfyui_connected = True
                self.card_list = card_animation_generator.get_card_list()
                self.filtered_cards = self.card_list.copy()
                
                # Add progress callback
                card_animation_generator.add_progress_callback(self._on_generation_progress)
                card_animation_generator.add_completion_callback(self._on_animation_completed)
                
                print("Animation system initialized successfully")
            else:
                print("Failed to initialize animation system - ComfyUI not connected")
                
        except Exception as e:
            print(f"Animation system initialization error: {e}")
            
        finally:
            self.is_initializing = False
    
    def _initialize_comfyui(self):
        """Initialize ComfyUI connection."""
        if not self.is_initializing and not self.comfyui_connected:
            # Add visual effect
            advanced_visual_effects.add_energy_pulse(
                SCREEN_CENTER[0], 200, max_radius=100, color=Colors.LAPIS_LAZULI
            )
            advanced_visual_effects.add_hieroglyph_float(SCREEN_CENTER[0], 200)
            
            # This would trigger async initialization
            print("Initializing ComfyUI connection...")
            audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
    
    def _generate_single_card(self):
        """Generate animation for selected card."""
        if not self.comfyui_connected:
            print("ComfyUI not connected")
            return
        
        if not self.selected_card_id:
            print("No card selected")
            return
        
        # Add visual effects
        advanced_visual_effects.add_divine_aura(SCREEN_CENTER[0], 300, radius=150)
        advanced_visual_effects.add_ankh_blessing(SCREEN_CENTER[0], 300)
        
        self.is_generating = True
        print(f"Generating animation for card: {self.selected_card_id}")
        audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.5)
        
        # This would trigger async generation
        # await card_animation_generator.generate_card_animation(self.selected_card_id, AnimationPriority.HIGH)
    
    def _generate_god_collection(self):
        """Generate animations for all cards of selected god."""
        if not self.comfyui_connected:
            print("ComfyUI not connected")
            return
        
        # Add dramatic visual effects
        advanced_visual_effects.add_sand_swirl(SCREEN_CENTER[0], 350, radius=100)
        advanced_visual_effects.add_lightning_arc(200, 300, 600, 300)
        
        self.is_generating = True
        print(f"Generating {self.selected_god} collection...")
        audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.7)
    
    def _generate_all_cards(self):
        """Generate animations for all cards."""
        if not self.comfyui_connected:
            print("ComfyUI not connected") 
            return
        
        # Epic visual effects for full generation
        advanced_visual_effects.add_fire_ember(SCREEN_CENTER[0], 400, count=25)
        advanced_visual_effects.add_energy_pulse(SCREEN_CENTER[0], 400, max_radius=200)
        
        self.is_generating = True
        print("Generating ALL card animations...")
        audio_manager.play_sound(SoundEffect.VICTORY_FANFARE, 0.4)
    
    def _switch_tab(self, tab: GenerationTab):
        """Switch to different tab."""
        self.current_tab = tab
        audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.5)
        
        # Add tab switch visual effect
        tab_index = list(GenerationTab).index(tab)
        tab_x = SCREEN_CENTER[0] - 360 + (tab_index * 180)
        advanced_visual_effects.add_crystal_shine(tab_x, 80, 170, 45)
    
    def _on_generation_progress(self, completed: int, failed: int):
        """Handle generation progress updates."""
        total = completed + failed
        if total > 0:
            self.generation_progress = completed / total
        print(f"Generation progress: {completed} completed, {failed} failed")
    
    def _on_animation_completed(self, card_id: str, animation_path: str):
        """Handle single animation completion."""
        print(f"Animation completed for {card_id}: {animation_path}")
        
        # Add completion visual effect
        advanced_visual_effects.add_ankh_blessing(SCREEN_CENTER[0], 300)
    
    def _handle_action(self, action: AnimationAction):
        """Handle screen actions."""
        if self.on_action:
            self.on_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update animation generator screen."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update mystical particles
        for particle in self.mystical_particles:
            particle['x'] += math.sin(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.5
            particle['y'] += math.cos(self.animation_time * 0.2 + particle['phase']) * particle['speed'] * dt * 0.3
            
            # Wrap around screen
            if particle['x'] < -50:
                particle['x'] = SCREEN_WIDTH + 50
            elif particle['x'] > SCREEN_WIDTH + 50:
                particle['x'] = -50
        
        # Update UI components
        all_buttons = self.tab_buttons + self.generation_buttons + self.card_buttons
        for button in all_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(AnimationAction.BACK_TO_MENU)
                elif event.key == pygame.K_F1:
                    self._initialize_comfyui()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in all_buttons:
                    if button.handle_click(mouse_pos):
                        break
    
    def render(self, surface: pygame.Surface):
        """Render animation generator screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Mystical particles
        self._render_particles(surface)
        
        # Title
        self._render_title(surface)
        
        # Tab buttons
        self._render_tab_buttons(surface)
        
        # Current tab content
        self._render_current_tab(surface)
        
        # Generation buttons
        for button in self.generation_buttons:
            button.render(surface)
        
        # Status overlay
        self._render_status_overlay(surface)
        
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
        
        pattern_color = (20, 15, 35)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
    
    def _render_particles(self, surface: pygame.Surface):
        """Render mystical tech particles."""
        for particle in self.mystical_particles:
            alpha = int(particle['alpha'] + 30 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*particle['color'], min(255, alpha)))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_title(self, surface: pygame.Surface):
        """Render main title."""
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "ANIMATION GENERATOR"
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.LAPIS_LAZULI)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 40))
        glow_surface.set_alpha(150)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 38))
        surface.blit(title_surface, title_rect)
    
    def _render_tab_buttons(self, surface: pygame.Surface):
        """Render tab buttons with active highlighting."""
        for i, button in enumerate(self.tab_buttons):
            tab = list(GenerationTab)[i]
            
            # Highlight active tab
            if tab == self.current_tab:
                highlight_rect = button.rect.inflate(4, 4)
                highlight_surface = pygame.Surface(highlight_rect.size, pygame.SRCALPHA)
                highlight_surface.fill((*Colors.GOLD, 100))
                surface.blit(highlight_surface, highlight_rect.topleft)
            
            button.render(surface)
    
    def _render_current_tab(self, surface: pygame.Surface):
        """Render content for current tab."""
        if self.current_tab == GenerationTab.SINGLE_CARD:
            self._render_single_card_tab(surface)
        elif self.current_tab == GenerationTab.BATCH_GENERATION:
            self._render_batch_generation_tab(surface)
        elif self.current_tab == GenerationTab.MONITORING:
            self._render_monitoring_tab(surface)
        elif self.current_tab == GenerationTab.SETTINGS:
            self._render_settings_tab(surface)
    
    def _render_single_card_tab(self, surface: pygame.Surface):
        """Render single card generation interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        # Card selection area
        text = font.render("Select a card to generate animation:", True, Colors.PAPYRUS)
        surface.blit(text, (200, 280))
        
        # Simple card list (placeholder)
        if self.card_list:
            y_start = 320
            for i, card in enumerate(self.filtered_cards[:8]):  # Show first 8
                y = y_start + i * 30
                color = Colors.GOLD if card.get('card_id') == self.selected_card_id else Colors.DESERT_SAND
                card_text = font.render(f"• {card['name']} ({card['rarity']})", True, color)
                surface.blit(card_text, (220, y))
    
    def _render_batch_generation_tab(self, surface: pygame.Surface):
        """Render batch generation interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        text = font.render("Batch Generation Options:", True, Colors.PAPYRUS)
        surface.blit(text, (200, 280))
        
        options = [
            f"• Generate by God: {self.selected_god.title()}",
            "• Generate by Rarity",
            "• Generate All Cards",
            f"• Estimated time: {len(self.card_list) * 2} minutes"
        ]
        
        for i, option in enumerate(options):
            y = 320 + i * 30
            option_text = font.render(option, True, Colors.DESERT_SAND)
            surface.blit(option_text, (220, y))
    
    def _render_monitoring_tab(self, surface: pygame.Surface):
        """Render generation monitoring interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        text = font.render("Generation Status:", True, Colors.PAPYRUS)
        surface.blit(text, (200, 280))
        
        status_info = [
            f"• ComfyUI Connected: {'Yes' if self.comfyui_connected else 'No'}",
            f"• Generation Active: {'Yes' if self.is_generating else 'No'}",
            f"• Progress: {self.generation_progress:.1%}",
            f"• Total Cards: {len(self.card_list)}"
        ]
        
        for i, info in enumerate(status_info):
            y = 320 + i * 30
            color = Colors.LAPIS_LAZULI if self.comfyui_connected and i == 0 else Colors.DESERT_SAND
            info_text = font.render(info, True, color)
            surface.blit(info_text, (220, y))
    
    def _render_settings_tab(self, surface: pygame.Surface):
        """Render ComfyUI settings interface."""
        font = pygame.font.Font(None, FontSizes.BODY)
        
        text = font.render("ComfyUI Settings:", True, Colors.PAPYRUS)
        surface.blit(text, (200, 280))
        
        settings_info = [
            "• Server URL: http://127.0.0.1:8188",
            "• RTX 5070 Optimization: Enabled",
            "• Concurrent Requests: 2",
            "• Output Format: GIF"
        ]
        
        for i, setting in enumerate(settings_info):
            y = 320 + i * 30
            setting_text = font.render(setting, True, Colors.DESERT_SAND)
            surface.blit(setting_text, (220, y))
    
    def _render_status_overlay(self, surface: pygame.Surface):
        """Render status overlay."""
        if self.is_initializing:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))
            
            font = pygame.font.Font(None, FontSizes.TITLE_MEDIUM)
            text = font.render("Initializing ComfyUI...", True, Colors.GOLD)
            rect = text.get_rect(center=SCREEN_CENTER)
            surface.blit(text, rect)
        
        elif self.is_generating:
            # Progress bar
            bar_width = 400
            bar_height = 20
            bar_x = SCREEN_CENTER[0] - bar_width // 2
            bar_y = SCREEN_HEIGHT - 100
            
            # Background bar
            pygame.draw.rect(surface, Colors.BLACK, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, Colors.GOLD, (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Progress fill
            fill_width = int(bar_width * self.generation_progress)
            pygame.draw.rect(surface, Colors.LAPIS_LAZULI, (bar_x, bar_y, fill_width, bar_height))
            
            # Progress text
            font = pygame.font.Font(None, FontSizes.BODY)
            progress_text = font.render(f"Generating... {self.generation_progress:.1%}", True, Colors.PAPYRUS)
            progress_rect = progress_text.get_rect(center=(SCREEN_CENTER[0], bar_y - 30))
            surface.blit(progress_text, progress_rect)
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        all_buttons = self.tab_buttons + self.generation_buttons + self.card_buttons
        for button in all_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0