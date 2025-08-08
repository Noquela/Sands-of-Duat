#!/usr/bin/env python3
"""
SANDS OF DUAT - GAME MANAGER
===========================

Central game manager that coordinates all UI screens and game flow.
Handles transitions between menu, deck builder, and combat screens.
"""

import pygame
import sys
from typing import Optional, Dict, Any
from .screens.main_menu import create_main_menu
from .screens.deck_builder import create_deck_builder  
from .screens.combat import create_combat_screen

class GameManager:
    """Central game manager for Egyptian card game UI."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Game state
        self.current_screen = "main_menu"
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Screen instances
        self.screens = {}
        self._initialize_screens()
        
        # Transition effects
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_target = None
        
        # Game data
        self.player_deck = []
        self.game_settings = {
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'fullscreen': False
        }
    
    def _initialize_screens(self):
        """Initialize all game screens."""
        self.screens = {
            'main_menu': create_main_menu(self.screen),
            'deck_builder': create_deck_builder(self.screen),
            'combat': create_combat_screen(self.screen)
        }
    
    def _start_transition(self, target_screen: str):
        """Start transition to target screen."""
        if target_screen in self.screens:
            self.transitioning = True
            self.transition_target = target_screen
            self.transition_alpha = 0
    
    def _handle_menu_action(self, action: str):
        """Handle main menu actions."""
        if action == 'start_game':
            self._start_transition('combat')
        elif action == 'deck_builder':
            self._start_transition('deck_builder')
        elif action == 'collection':
            # TODO: Implement collection screen
            print("Collection screen coming soon!")
        elif action == 'settings':
            # TODO: Implement settings screen  
            print("Settings screen coming soon!")
        elif action == 'quit':
            self.running = False
    
    def _handle_deck_builder_action(self, action: str):
        """Handle deck builder actions."""
        if action == 'back':
            self._start_transition('main_menu')
        elif action == 'save':
            # Save current deck
            if hasattr(self.screens['deck_builder'], 'current_deck'):
                self.player_deck = self.screens['deck_builder'].current_deck.copy()
                print(f"Deck saved! {len(self.player_deck)} cards in deck.")
        elif action == 'clear':
            # Deck is cleared by the screen itself
            print("Deck cleared!")
    
    def _handle_combat_action(self, action: str):
        """Handle combat screen actions."""
        if action == 'back':
            self._start_transition('main_menu')
        elif action == 'victory':
            # TODO: Handle combat victory
            print("Victory! Returning to main menu.")
            self._start_transition('main_menu')
        elif action == 'defeat':
            # TODO: Handle combat defeat  
            print("Defeat! Returning to main menu.")
            self._start_transition('main_menu')
    
    def handle_event(self, event: pygame.event.Event):
        """Handle game events."""
        if event.type == pygame.QUIT:
            self.running = False
            return
        
        # Global hotkeys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                # Toggle fullscreen
                self.game_settings['fullscreen'] = not self.game_settings['fullscreen']
                if self.game_settings['fullscreen']:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode((1400, 900))
                
                # Recreate screens with new screen size
                self._initialize_screens()
                return
        
        # Don't handle events during transition
        if self.transitioning:
            return
        
        # Route events to current screen
        current_screen = self.screens[self.current_screen]
        action = current_screen.handle_event(event)
        
        # Handle screen-specific actions
        if action:
            if self.current_screen == 'main_menu':
                self._handle_menu_action(action)
            elif self.current_screen == 'deck_builder':
                self._handle_deck_builder_action(action)
            elif self.current_screen == 'combat':
                self._handle_combat_action(action)
    
    def update(self, dt: float):
        """Update game logic and screens."""
        # Handle transitions
        if self.transitioning:
            self.transition_alpha += dt * 4  # Transition speed
            
            if self.transition_alpha >= 1.0:
                # Complete transition
                self.current_screen = self.transition_target
                self.transition_alpha = 1.0
                
                # Start fade in
                self.transition_alpha = 1.0
            
            if self.transition_alpha >= 2.0:
                # Fade in complete
                self.transitioning = False
                self.transition_alpha = 0
                self.transition_target = None
        
        # Update current screen
        if not self.transitioning:
            current_screen = self.screens[self.current_screen]
            current_screen.update(dt)
    
    def draw(self):
        """Draw current screen and transitions."""
        # Draw current screen
        current_screen = self.screens[self.current_screen]
        current_screen.draw()
        
        # Draw transition overlay
        if self.transitioning:
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            
            if self.transition_alpha <= 1.0:
                # Fade out
                alpha = int(self.transition_alpha * 255)
            else:
                # Fade in  
                alpha = int((2.0 - self.transition_alpha) * 255)
            
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
    
    def run(self):
        """Main game loop."""
        print("🏺 Sands of Duat - Egyptian UI System Starting...")
        print("Available screens: Main Menu, Deck Builder, Combat")
        print("Controls: ESC to go back, F11 to toggle fullscreen")
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                self.handle_event(event)
            
            # Update game state
            self.update(dt)
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
        
        print("🏺 May the gods remember your journey. Farewell!")


def create_game_manager(screen: pygame.Surface) -> GameManager:
    """Factory function to create game manager."""
    return GameManager(screen)