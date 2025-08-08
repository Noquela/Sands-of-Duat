"""
Main Game Engine - The heart of Sands of Duat.
Provides smooth 60fps gameplay with Hades-level polish.
"""

import pygame
import sys
import logging
import time
from typing import Dict, Optional, Any

from .state_manager import StateManager, GameState
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE, SCREEN_CENTER,
    Colors, Timing, FontSizes, Dev, Layout
)

class GameEngine:
    """
    Main game engine managing core systems and game loop.
    Designed for smooth 60fps performance with professional polish.
    """
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        
        # Core systems
        self.state_manager = StateManager()
        
        # Performance tracking
        self.frame_times = []
        self.last_fps_update = 0.0
        self.current_fps = 0.0
        self.target_dt = Timing.FRAME_TIME
        
        # Input handling
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = [False, False, False]
        
        # Fonts (loaded once for performance)
        self.fonts = self._load_fonts()
        
        # Logger
        self.logger = logging.getLogger("game_engine")
        
        # Log display information
        self.logger.info(f"Display: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        if Layout.IS_ULTRAWIDE:
            self.logger.info("🖥️ Ultrawide display detected - using centered layout")
        
        # Initialize systems
        self._initialize_systems()
        
        self.logger.info("🏺 Game Engine initialized successfully")
    
    def _load_fonts(self) -> Dict[str, Dict[int, pygame.font.Font]]:
        """Load all fonts at different sizes for optimal performance."""
        fonts = {}
        
        # Default font for now (can be replaced with Egyptian fonts later)
        font_name = None  # Uses pygame default font
        
        sizes = [
            FontSizes.DEBUG, FontSizes.CARD_TEXT, FontSizes.TOOLTIP,
            FontSizes.CARD_NAME, FontSizes.BODY, FontSizes.BUTTON,
            FontSizes.SUBTITLE, FontSizes.TITLE_MEDIUM, FontSizes.TITLE_LARGE,
            FontSizes.TITLE_HUGE
        ]
        
        fonts['default'] = {}
        for size in sizes:
            fonts['default'][size] = pygame.font.Font(font_name, size)
        
        return fonts
    
    def _initialize_systems(self):
        """Initialize all game systems."""
        # Register state callbacks
        self._register_state_callbacks()
        
        # Start with splash screen
        self.state_manager.change_state(GameState.MAIN_MENU)  # Skip splash for now
    
    def _register_state_callbacks(self):
        """Register callbacks for all game states."""
        # For now, register placeholder callbacks
        # These will be replaced with actual screen implementations
        
        for state in GameState:
            self.state_manager.register_state_callbacks(
                state,
                enter_callback=lambda s=state: self._on_state_enter(s),
                exit_callback=lambda s=state: self._on_state_exit(s),
                update_callback=lambda dt, s=state: self._on_state_update(s, dt),
                render_callback=lambda surf, s=state: self._on_state_render(s, surf)
            )
    
    def _on_state_enter(self, state: GameState):
        """Called when entering a state."""
        self.logger.info(f"Entering state: {state.name}")
    
    def _on_state_exit(self, state: GameState):
        """Called when exiting a state."""
        self.logger.info(f"Exiting state: {state.name}")
    
    def _on_state_update(self, state: GameState, dt: float):
        """Called to update a state."""
        # Placeholder implementation
        pass
    
    def _on_state_render(self, state: GameState, surface: pygame.Surface):
        """Called to render a state."""
        # Placeholder implementation - render based on state
        if state == GameState.MAIN_MENU:
            self._render_main_menu_placeholder(surface)
        elif state == GameState.DECK_BUILDER:
            self._render_deck_builder_placeholder(surface)
        elif state == GameState.COMBAT:
            self._render_combat_placeholder(surface)
        else:
            self._render_default_placeholder(surface, state)
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events with input state tracking.
        
        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
            self.keys_just_pressed.add(event.key)
            
            # Global hotkeys
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif event.key == pygame.K_F1 and Dev.DEBUG_MODE:
                Dev.SHOW_FPS = not Dev.SHOW_FPS
        
        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)
            self.keys_just_released.add(event.key)
        
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button <= 3:
                self.mouse_buttons[event.button - 1] = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button <= 3:
                self.mouse_buttons[event.button - 1] = False
        
        # Pass event to current state (will be implemented per state)
        # For now, just handle basic navigation
        if event.type == pygame.KEYDOWN:
            current_state = self.state_manager.get_current_state()
            
            if event.key == pygame.K_ESCAPE:
                if current_state == GameState.MAIN_MENU:
                    self.running = False
                elif current_state != GameState.MAIN_MENU:
                    self.state_manager.change_state(GameState.MAIN_MENU)
            
            elif event.key == pygame.K_1 and current_state == GameState.MAIN_MENU:
                self.state_manager.change_state(GameState.DECK_BUILDER, "slide_left")
            elif event.key == pygame.K_2 and current_state == GameState.MAIN_MENU:
                self.state_manager.change_state(GameState.COMBAT, "slide_left")
            elif event.key == pygame.K_3 and current_state == GameState.MAIN_MENU:
                self.state_manager.change_state(GameState.SETTINGS, "slide_left")
    
    def update(self, dt: float):
        """
        Update all game systems.
        
        Args:
            dt: Delta time in seconds
        """
        # Update performance tracking
        self._update_performance_tracking(dt)
        
        # Update state manager
        self.state_manager.update(dt)
        
        # Clear per-frame input state
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
    
    def render(self):
        """Render the current game state with debug overlays."""
        # Clear screen
        self.screen.fill(Colors.DARK_BLUE)
        
        # Render current state
        self.state_manager.render(self.screen)
        
        # Render debug information
        if Dev.DEBUG_MODE:
            self._render_debug_info()
        
        # Present frame
        pygame.display.flip()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SCREEN_SIZE)
        
        self.logger.info(f"Fullscreen: {self.fullscreen}")
    
    def handle_escape(self) -> bool:
        """
        Handle escape key press based on current state.
        
        Returns:
            True if escape was handled, False if game should quit
        """
        current_state = self.state_manager.get_current_state()
        
        if current_state == GameState.MAIN_MENU:
            return False  # Quit game
        else:
            # Return to main menu
            self.state_manager.change_state(GameState.MAIN_MENU)
            return True
    
    def shutdown(self):
        """Clean shutdown of game engine."""
        self.logger.info("🏺 Game Engine shutting down...")
        self.running = False
    
    def _update_performance_tracking(self, dt: float):
        """Update FPS and performance tracking."""
        self.frame_times.append(dt)
        
        # Keep only recent samples
        if len(self.frame_times) > Dev.FRAME_TIME_SAMPLES:
            self.frame_times.pop(0)
        
        # Update FPS every half second
        current_time = time.time()
        if current_time - self.last_fps_update > 0.5:
            if self.frame_times:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                self.current_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            self.last_fps_update = current_time
    
    def _render_debug_info(self):
        """Render debug information overlay."""
        if not Dev.SHOW_FPS:
            return
        
        debug_font = self.fonts['default'][FontSizes.DEBUG]
        
        # FPS Counter
        fps_text = debug_font.render(f"FPS: {self.current_fps:.1f}", True, Colors.WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        # Current State
        state_text = debug_font.render(f"State: {self.state_manager.get_current_state().name}", True, Colors.WHITE)
        self.screen.blit(state_text, (10, 30))
        
        # Transition Info
        if self.state_manager.is_transitioning():
            progress = self.state_manager.get_transition_progress()
            trans_text = debug_font.render(f"Transition: {progress:.2f}", True, Colors.WHITE)
            self.screen.blit(trans_text, (10, 50))
    
    # Placeholder rendering methods (will be replaced with actual screens)
    def _render_main_menu_placeholder(self, surface: pygame.Surface):
        """Placeholder main menu rendering with ultrawide support."""
        surface.fill(Colors.DARK_BLUE)
        
        # Draw ultrawide background bars if needed
        if Layout.IS_ULTRAWIDE:
            # Draw darker bars on the sides for cinematic effect
            left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            pygame.draw.rect(surface, (15, 15, 50), left_bar)
            pygame.draw.rect(surface, (15, 15, 50), right_bar)
        
        title_font = self.fonts['default'][FontSizes.TITLE_HUGE]
        subtitle_font = self.fonts['default'][FontSizes.SUBTITLE]
        body_font = self.fonts['default'][FontSizes.BODY]
        
        # Center content in safe area
        center_x = SCREEN_CENTER[0]
        
        # Title
        title = title_font.render("SANDS OF DUAT", True, Colors.GOLD)
        title_rect = title.get_rect(center=(center_x, 150))
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = subtitle_font.render("Egyptian Underworld Card Game", True, Colors.PAPYRUS)
        subtitle_rect = subtitle.get_rect(center=(center_x, 220))
        surface.blit(subtitle, subtitle_rect)
        
        # Display info for ultrawide
        if Layout.IS_ULTRAWIDE:
            res_info = f"Ultrawide {SCREEN_WIDTH}x{SCREEN_HEIGHT} Display Optimized"
            res_font = self.fonts['default'][FontSizes.CARD_TEXT]
            res_text = res_font.render(res_info, True, Colors.GOLD)
            res_rect = res_text.get_rect(center=(center_x, 270))
            surface.blit(res_text, res_rect)
        
        # Instructions
        instructions = [
            "Press 1 for Deck Builder",
            "Press 2 for Combat",
            "Press 3 for Settings", 
            "Press ESC to Quit"
        ]
        
        y = 350 if not Layout.IS_ULTRAWIDE else 380
        for instruction in instructions:
            text = body_font.render(instruction, True, Colors.DESERT_SAND)
            text_rect = text.get_rect(center=(center_x, y))
            surface.blit(text, text_rect)
            y += 40
        
        # Version info
        version_font = self.fonts['default'][FontSizes.DEBUG]
        version = version_font.render("SPRINT 1: Foundation & Core Architecture", True, Colors.DESERT_SAND)
        version_rect = version.get_rect(center=(center_x, SCREEN_HEIGHT - 30))
        surface.blit(version, version_rect)
    
    def _render_deck_builder_placeholder(self, surface: pygame.Surface):
        """Placeholder deck builder rendering with ultrawide support."""
        surface.fill(Colors.LAPIS_LAZULI)
        
        # Ultrawide side bars
        if Layout.IS_ULTRAWIDE:
            left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            pygame.draw.rect(surface, (15, 35, 75), left_bar)
            pygame.draw.rect(surface, (15, 35, 75), right_bar)
        
        title_font = self.fonts['default'][FontSizes.TITLE_LARGE]
        body_font = self.fonts['default'][FontSizes.BODY]
        center_x = SCREEN_CENTER[0]
        
        title = title_font.render("DECK BUILDER", True, Colors.GOLD)
        title_rect = title.get_rect(center=(center_x, 100))
        surface.blit(title, title_rect)
        
        info = body_font.render("Deck Builder will be implemented in SPRINT 4", True, Colors.PAPYRUS)
        info_rect = info.get_rect(center=(center_x, 300))
        surface.blit(info, info_rect)
        
        back = body_font.render("Press ESC to return to Main Menu", True, Colors.DESERT_SAND)
        back_rect = back.get_rect(center=(center_x, 400))
        surface.blit(back, back_rect)
    
    def _render_combat_placeholder(self, surface: pygame.Surface):
        """Placeholder combat rendering with ultrawide support."""
        surface.fill((64, 32, 32))  # Dark red
        
        # Ultrawide side bars  
        if Layout.IS_ULTRAWIDE:
            left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            pygame.draw.rect(surface, (30, 15, 15), left_bar)
            pygame.draw.rect(surface, (30, 15, 15), right_bar)
        
        title_font = self.fonts['default'][FontSizes.TITLE_LARGE]
        body_font = self.fonts['default'][FontSizes.BODY]
        center_x = SCREEN_CENTER[0]
        
        title = title_font.render("COMBAT", True, Colors.GOLD)
        title_rect = title.get_rect(center=(center_x, 100))
        surface.blit(title, title_rect)
        
        info = body_font.render("Combat System will be implemented in SPRINT 5", True, Colors.PAPYRUS)
        info_rect = info.get_rect(center=(center_x, 300))
        surface.blit(info, info_rect)
        
        back = body_font.render("Press ESC to return to Main Menu", True, Colors.DESERT_SAND)
        back_rect = back.get_rect(center=(center_x, 400))
        surface.blit(back, back_rect)
    
    def _render_default_placeholder(self, surface: pygame.Surface, state: GameState):
        """Default placeholder for unimplemented states with ultrawide support."""
        surface.fill(Colors.BLACK)
        
        # Ultrawide side bars
        if Layout.IS_ULTRAWIDE:
            left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            pygame.draw.rect(surface, (20, 20, 20), left_bar)
            pygame.draw.rect(surface, (20, 20, 20), right_bar)
        
        title_font = self.fonts['default'][FontSizes.TITLE_LARGE]
        body_font = self.fonts['default'][FontSizes.BODY]
        center_x = SCREEN_CENTER[0]
        
        title = title_font.render(state.name.replace('_', ' '), True, Colors.GOLD)
        title_rect = title.get_rect(center=(center_x, 200))
        surface.blit(title, title_rect)
        
        info = body_font.render("This screen will be implemented in a future sprint", True, Colors.PAPYRUS)
        info_rect = info.get_rect(center=(center_x, 300))
        surface.blit(info, info_rect)
        
        back = body_font.render("Press ESC to return to Main Menu", True, Colors.DESERT_SAND)
        back_rect = back.get_rect(center=(center_x, 400))
        surface.blit(back, back_rect)