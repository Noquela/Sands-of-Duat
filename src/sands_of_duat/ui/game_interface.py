#!/usr/bin/env python3
"""
SANDS OF DUAT - MAIN GAME INTERFACE
===================================

Complete game interface integrating:
- Menu system
- Deck building with Egyptian card art
- Combat system
- Asset management
- Performance monitoring
"""

import pygame
import sys
from enum import Enum
from typing import Dict, List, Optional, Tuple
import logging

from ..core.asset_loader import get_asset_loader, AssetCategory, initialize_assets
from ..cards.egyptian_cards import get_deck_builder, EgyptianCard, CardType

logger = logging.getLogger(__name__)

class GameState(Enum):
    """Game states"""
    MENU = "menu"
    DECK_BUILDER = "deck_builder"
    COMBAT = "combat"
    SETTINGS = "settings"
    CARD_GALLERY = "card_gallery"

class SandsOfDuatGame:
    """
    Main game class that manages all systems and provides complete gameplay.
    
    Features:
    - Complete menu system
    - Interactive deck building
    - Card gallery with all 71 Egyptian assets
    - Combat prototype
    - Performance monitoring
    """
    
    def __init__(self, screen_size: Tuple[int, int] = (1400, 900)):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Sands of Duat - Egyptian Underworld Card Game")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Game state
        self.state = GameState.MENU
        self.previous_state = GameState.MENU
        
        # Egyptian color scheme
        self.colors = {
            'GOLD': (255, 215, 0),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'DARK_BLUE': (25, 25, 112),
            'DARK_GOLD': (184, 134, 11),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255)
        }
        
        # Initialize game systems
        self._initialize_systems()
        
        # UI elements
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Menu system
        self.menu_buttons = []
        self._create_menu_buttons()
        
        # Deck builder
        self.player_deck: List[EgyptianCard] = []
        self.available_cards: List[EgyptianCard] = []
        self.selected_card: Optional[EgyptianCard] = None
        self.deck_scroll = 0
        self.gallery_scroll = 0
        
        # Card gallery
        self.gallery_cards: List[EgyptianCard] = []
        self.gallery_filter = None
        
        # Performance monitoring
        self.frame_times = []
        self.show_debug = False
        
        logger.info("Sands of Duat game initialized")
    
    def _initialize_systems(self):
        """Initialize all game systems."""
        logger.info("Initializing game systems...")
        
        # Initialize assets
        self.asset_loader = initialize_assets()
        
        # Initialize deck builder
        self.deck_builder = get_deck_builder()
        
        # Load initial data
        self.available_cards = self.deck_builder.get_all_cards()
        self.gallery_cards = self.available_cards.copy()
        self.player_deck = self.deck_builder.create_starter_deck()
        
        logger.info("All systems initialized successfully")
    
    def _create_menu_buttons(self):
        """Create main menu buttons."""
        center_x = self.screen_size[0] // 2
        start_y = 400
        button_height = 60
        button_spacing = 80
        
        buttons = [
            ("PLAY", GameState.COMBAT),
            ("DECK BUILDER", GameState.DECK_BUILDER),
            ("CARD GALLERY", GameState.CARD_GALLERY),
            ("SETTINGS", GameState.SETTINGS),
            ("EXIT", None)
        ]
        
        for i, (text, state) in enumerate(buttons):
            button_rect = pygame.Rect(center_x - 150, start_y + i * button_spacing, 300, button_height)
            self.menu_buttons.append((button_rect, text, state))
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos, event.button)
            
            elif event.type == pygame.MOUSEWHEEL:
                self._handle_mouse_wheel(event.y)
    
    def _handle_keydown(self, event):
        """Handle keyboard input."""
        if event.key == pygame.K_ESCAPE:
            if self.state == GameState.MENU:
                self.running = False
            else:
                self.state = GameState.MENU
        
        elif event.key == pygame.K_F1:
            self.show_debug = not self.show_debug
        
        elif event.key == pygame.K_F5:
            # Reload assets
            self.asset_loader.clear_cache()
            logger.info("Assets reloaded")
    
    def _handle_mouse_click(self, pos: Tuple[int, int], button: int):
        """Handle mouse clicks based on current state."""
        if self.state == GameState.MENU:
            self._handle_menu_click(pos)
        elif self.state == GameState.DECK_BUILDER:
            self._handle_deck_builder_click(pos)
        elif self.state == GameState.CARD_GALLERY:
            self._handle_gallery_click(pos)
        elif self.state == GameState.COMBAT:
            self._handle_combat_click(pos)
    
    def _handle_mouse_wheel(self, direction: int):
        """Handle mouse wheel scrolling."""
        if self.state == GameState.DECK_BUILDER:
            self.gallery_scroll = max(0, self.gallery_scroll - direction * 30)
        elif self.state == GameState.CARD_GALLERY:
            self.gallery_scroll = max(0, self.gallery_scroll - direction * 30)
    
    def _handle_menu_click(self, pos: Tuple[int, int]):
        """Handle main menu clicks."""
        for button_rect, text, state in self.menu_buttons:
            if button_rect.collidepoint(pos):
                if text == "EXIT":
                    self.running = False
                elif state:
                    self.previous_state = self.state
                    self.state = state
                    logger.info(f"Switched to {state.value}")
    
    def _handle_deck_builder_click(self, pos: Tuple[int, int]):
        """Handle deck builder clicks."""
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        if back_rect.collidepoint(pos):
            self.state = GameState.MENU
            return
        
        # Card selection area
        cards_per_row = 4
        card_width = 160
        card_height = 224
        margin = 20
        start_x = 50
        start_y = 100 - self.gallery_scroll
        
        for i, card in enumerate(self.available_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            card_x = start_x + col * (card_width + margin)
            card_y = start_y + row * (card_height + margin)
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            if card_rect.collidepoint(pos) and card_rect.bottom > 80:
                self.selected_card = card
                if len(self.player_deck) < 30:  # Max deck size
                    self.player_deck.append(card)
                    logger.info(f"Added {card.name} to deck")
    
    def _handle_gallery_click(self, pos: Tuple[int, int]):
        """Handle card gallery clicks."""
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        if back_rect.collidepoint(pos):
            self.state = GameState.MENU
    
    def _handle_combat_click(self, pos: Tuple[int, int]):
        """Handle combat clicks."""
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        if back_rect.collidepoint(pos):
            self.state = GameState.MENU
    
    def update(self):
        """Update game logic."""
        # Update frame time tracking
        frame_time = self.clock.get_time()
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
    
    def render(self):
        """Render the current game state."""
        if self.state == GameState.MENU:
            self._render_menu()
        elif self.state == GameState.DECK_BUILDER:
            self._render_deck_builder()
        elif self.state == GameState.CARD_GALLERY:
            self._render_card_gallery()
        elif self.state == GameState.COMBAT:
            self._render_combat()
        elif self.state == GameState.SETTINGS:
            self._render_settings()
        
        # Debug overlay
        if self.show_debug:
            self._render_debug_info()
        
        pygame.display.flip()
    
    def _render_menu(self):
        """Render the main menu."""
        # Background
        self.screen.fill(self.colors['DARK_BLUE'])
        
        # Title
        title_surface = self.font_large.render("SANDS OF DUAT", True, self.colors['GOLD'])
        title_rect = title_surface.get_rect(center=(self.screen_size[0]//2, 150))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.font_medium.render("Egyptian Underworld Card Game", True, self.colors['PAPYRUS'])
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_size[0]//2, 200))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Version and asset info
        info_lines = [
            f"Assets: {self.asset_loader.get_total_asset_count()} Egyptian artworks loaded",
            f"Cards: {len(self.available_cards)} cards available",
            "Press F1 for debug info • ESC to navigate back"
        ]
        
        for i, line in enumerate(info_lines):
            info_surface = self.font_small.render(line, True, self.colors['DESERT_SAND'])
            info_rect = info_surface.get_rect(center=(self.screen_size[0]//2, 250 + i * 25))
            self.screen.blit(info_surface, info_rect)
        
        # Menu buttons
        for button_rect, text, state in self.menu_buttons:
            # Button background
            pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], button_rect)
            pygame.draw.rect(self.screen, self.colors['GOLD'], button_rect, 3)
            
            # Button text
            button_text = self.font_medium.render(text, True, self.colors['PAPYRUS'])
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
    
    def _render_deck_builder(self):
        """Render the deck building interface."""
        self.screen.fill(self.colors['PAPYRUS'])
        
        # Title
        title_surface = self.font_large.render("DECK BUILDER", True, self.colors['DARK_BLUE'])
        self.screen.blit(title_surface, (50, 20))
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], back_rect)
        back_text = self.font_small.render("← BACK", True, self.colors['WHITE'])
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Current deck info
        deck_info = f"Current Deck: {len(self.player_deck)}/30 cards"
        deck_surface = self.font_medium.render(deck_info, True, self.colors['DARK_BLUE'])
        self.screen.blit(deck_surface, (self.screen_size[0] - 300, 30))
        
        # Available cards grid
        cards_per_row = 4
        card_width = 160
        card_height = 224
        margin = 20
        start_x = 50
        start_y = 100 - self.gallery_scroll
        
        for i, card in enumerate(self.available_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            card_x = start_x + col * (card_width + margin)
            card_y = start_y + row * (card_height + margin)
            
            # Skip cards that are scrolled out of view
            if card_y + card_height < 80 or card_y > self.screen_size[1]:
                continue
            
            # Render card
            card_surface = card.render_card((card_width, card_height))
            
            # Highlight selected card
            if card == self.selected_card:
                pygame.draw.rect(self.screen, self.colors['GOLD'], 
                               (card_x - 3, card_y - 3, card_width + 6, card_height + 6), 3)
            
            self.screen.blit(card_surface, (card_x, card_y))
        
        # Current deck display (right side)
        deck_x = self.screen_size[0] - 320
        deck_y = 80
        deck_title = self.font_medium.render("Your Deck:", True, self.colors['DARK_BLUE'])
        self.screen.blit(deck_title, (deck_x, deck_y))
        
        # Show deck cards as a list
        for i, card in enumerate(self.player_deck[:10]):  # Show first 10
            card_text = f"• {card.name} ({card.stats.cost})"
            text_surface = self.font_small.render(card_text, True, self.colors['DARK_BLUE'])
            self.screen.blit(text_surface, (deck_x, deck_y + 40 + i * 25))
        
        if len(self.player_deck) > 10:
            more_text = f"... and {len(self.player_deck) - 10} more"
            more_surface = self.font_small.render(more_text, True, self.colors['DARK_BLUE'])
            self.screen.blit(more_surface, (deck_x, deck_y + 40 + 10 * 25))
    
    def _render_card_gallery(self):
        """Render the card gallery showing all Egyptian assets."""
        self.screen.fill(self.colors['PAPYRUS'])
        
        # Title
        title_surface = self.font_large.render("CARD GALLERY", True, self.colors['DARK_BLUE'])
        self.screen.blit(title_surface, (50, 20))
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], back_rect)
        back_text = self.font_small.render("← BACK", True, self.colors['WHITE'])
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Gallery info
        gallery_info = f"Viewing {len(self.gallery_cards)} cards • Scroll to browse"
        info_surface = self.font_small.render(gallery_info, True, self.colors['DARK_BLUE'])
        self.screen.blit(info_surface, (50, 60))
        
        # Cards grid
        cards_per_row = 5
        card_width = 200
        card_height = 280
        margin = 15
        start_x = 50
        start_y = 100 - self.gallery_scroll
        
        for i, card in enumerate(self.gallery_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            card_x = start_x + col * (card_width + margin)
            card_y = start_y + row * (card_height + margin)
            
            # Skip cards that are scrolled out of view
            if card_y + card_height < 80 or card_y > self.screen_size[1]:
                continue
            
            # Render card
            card_surface = card.render_card((card_width, card_height))
            self.screen.blit(card_surface, (card_x, card_y))
    
    def _render_combat(self):
        """Render the combat interface."""
        self.screen.fill(self.colors['DESERT_SAND'])
        
        # Title
        title_surface = self.font_large.render("COMBAT MODE", True, self.colors['DARK_BLUE'])
        self.screen.blit(title_surface, (50, 20))
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], back_rect)
        back_text = self.font_small.render("← BACK", True, self.colors['WHITE'])
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Combat placeholder
        center_x, center_y = self.screen_size[0]//2, self.screen_size[1]//2
        
        combat_text = [
            "BATTLE ARENA",
            "",
            "Combat system ready for implementation",
            "Egyptian gods await your challenge",
            "",
            f"Your deck contains {len(self.player_deck)} cards"
        ]
        
        for i, line in enumerate(combat_text):
            if line:
                text_surface = self.font_medium.render(line, True, self.colors['DARK_BLUE'])
                text_rect = text_surface.get_rect(center=(center_x, center_y - 100 + i * 40))
                self.screen.blit(text_surface, text_rect)
        
        # Show a sample card from deck
        if self.player_deck:
            sample_card = self.player_deck[0]
            card_surface = sample_card.render_card((300, 420))
            card_rect = card_surface.get_rect(center=(center_x, center_y + 200))
            self.screen.blit(card_surface, card_rect)
    
    def _render_settings(self):
        """Render the settings screen."""
        self.screen.fill(self.colors['PAPYRUS'])
        
        # Title
        title_surface = self.font_large.render("SETTINGS", True, self.colors['DARK_BLUE'])
        self.screen.blit(title_surface, (50, 20))
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], back_rect)
        back_text = self.font_small.render("← BACK", True, self.colors['WHITE'])
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Settings info
        center_x, center_y = self.screen_size[0]//2, self.screen_size[1]//2
        
        settings_text = [
            "GAME SETTINGS",
            "",
            f"Resolution: {self.screen_size[0]}x{self.screen_size[1]}",
            f"FPS Target: {self.fps}",
            f"Asset Cache: {len(self.asset_loader._image_cache)} images loaded",
            "",
            "CONTROLS:",
            "F1 - Toggle debug info",
            "F5 - Reload assets",
            "ESC - Back to menu",
            "Mouse wheel - Scroll in deck builder/gallery"
        ]
        
        for i, line in enumerate(settings_text):
            if line:
                text_surface = self.font_medium.render(line, True, self.colors['DARK_BLUE'])
                text_rect = text_surface.get_rect(center=(center_x, center_y - 150 + i * 35))
                self.screen.blit(text_surface, text_rect)
    
    def _render_debug_info(self):
        """Render debug information overlay."""
        if not self.frame_times:
            return
        
        # Performance stats
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        current_fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0
        
        cache_stats = self.asset_loader.get_cache_stats()
        
        debug_lines = [
            f"FPS: {current_fps:.1f}",
            f"Frame Time: {avg_frame_time:.1f}ms",
            f"State: {self.state.value}",
            f"Cached Images: {cache_stats['cached_images']}/{cache_stats['max_cache_size']}",
            f"Total Assets: {cache_stats['total_assets']}",
            f"Cards Available: {len(self.available_cards)}",
            f"Player Deck: {len(self.player_deck)} cards"
        ]
        
        # Debug background
        debug_width = 250
        debug_height = len(debug_lines) * 25 + 20
        debug_surface = pygame.Surface((debug_width, debug_height))
        debug_surface.set_alpha(200)
        debug_surface.fill((0, 0, 0))
        
        # Debug text
        for i, line in enumerate(debug_lines):
            text_surface = self.font_small.render(line, True, self.colors['WHITE'])
            debug_surface.blit(text_surface, (10, 10 + i * 25))
        
        self.screen.blit(debug_surface, (self.screen_size[0] - debug_width - 10, 10))
    
    def run(self):
        """Main game loop."""
        logger.info("Starting Sands of Duat main game loop...")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        logger.info("Sands of Duat closed. May the gods remember your journey.")
        pygame.quit()
        sys.exit()

def main():
    """Main entry point for the complete game."""
    pygame.init()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    logger = logging.getLogger("sands_of_duat")
    logger.info("🏺 SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME 🏺")
    logger.info("Complete integration with all 71 Egyptian assets")
    
    # Create and run the game
    game = SandsOfDuatGame()
    game.run()

if __name__ == "__main__":
    main()