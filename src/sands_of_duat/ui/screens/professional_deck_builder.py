"""
Professional Deck Builder - SPRINT 4: Complete rewrite with Hades-level polish
Self-contained, modern architecture with Egyptian theming.
"""

import pygame
import math
import time
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum, auto
from pathlib import Path

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.deck_manager import deck_manager
from ...core.deck_collection_manager import deck_collection_manager
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton

class DeckBuilderAction(Enum):
    """Deck builder actions."""
    BACK_TO_MENU = auto()
    SAVE_DECK = auto()
    CLEAR_DECK = auto()
    EXPORT_DECK = auto()
    SAVE_DECK_AS = auto()
    LOAD_DECK = auto()
    DELETE_DECK = auto()

class CardData:
    """Simple card data structure."""
    def __init__(self, name: str, cost: int, attack: int, health: int, 
                 rarity: str, description: str):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.health = health
        self.rarity = rarity
        self.description = description

class Card:
    """Professional card with Egyptian styling."""
    
    def __init__(self, data: CardData, x: int = 0, y: int = 0):
        self.data = data
        self.x = x
        self.y = y
        self.width = 180
        self.height = 250
        self.is_hovered = False
        self.hover_offset = 0
        self.click_animation = 0
        
        # Render the card
        self._render()
    
    def _render(self):
        """Render the card surface."""
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Try to load high-resolution card frame first
        from ...core.asset_loader import get_asset_loader
        asset_loader = get_asset_loader()
        
        # Get the appropriate frame for this card's rarity
        frame_surface = asset_loader.get_card_frame_by_rarity(self.data.rarity)
        
        if frame_surface:
            # Scale frame to card size
            scaled_frame = pygame.transform.smoothscale(frame_surface, (self.width, self.height))
            self.surface.blit(scaled_frame, (0, 0))
        else:
            # Fallback: Card background with rarity border
            pygame.draw.rect(self.surface, Colors.PAPYRUS, (0, 0, self.width, self.height))
            
            # Enhanced rarity border
            rarity_colors = {
                'common': Colors.DESERT_SAND,
                'rare': (138, 43, 226),  # Purple
                'epic': (255, 140, 0),   # Orange
                'legendary': (255, 215, 0)  # Gold
            }
            border_color = rarity_colors.get(self.data.rarity, Colors.DESERT_SAND)
            pygame.draw.rect(self.surface, border_color, (0, 0, self.width, self.height), 4)
        
        # Cost crystal
        cost_rect = pygame.Rect(10, 10, 30, 30)
        pygame.draw.ellipse(self.surface, Colors.LAPIS_LAZULI, cost_rect)
        pygame.draw.ellipse(self.surface, Colors.GOLD, cost_rect, 2)
        
        font = pygame.font.Font(None, 24)
        cost_text = font.render(str(self.data.cost), True, Colors.WHITE)
        cost_pos = (25 - cost_text.get_width() // 2, 25 - cost_text.get_height() // 2)
        self.surface.blit(cost_text, cost_pos)
        
        # Ultra-high resolution artwork area with asset loader integration
        art_rect = pygame.Rect(15, 50, 150, 100)
        
        # Try to load animated artwork first, then fallback to static
        card_artwork = asset_loader.load_card_art_by_name(self.data.name)
        if not card_artwork:
            # Try fallback by rarity (use new ultra-high resolution assets)
            card_artwork = asset_loader.get_random_card_art_by_rarity(self.data.rarity)
        
        if card_artwork:
            # Scale ultra-high resolution artwork with quality scaling
            scaled_artwork = pygame.transform.smoothscale(card_artwork, (art_rect.width, art_rect.height))
            self.surface.blit(scaled_artwork, art_rect)
        else:
            # Enhanced fallback with Egyptian pattern
            pygame.draw.rect(self.surface, Colors.LAPIS_LAZULI, art_rect)
            # Add hieroglyphic-style pattern for ultra-high quality fallback
            for i in range(3):
                pattern_rect = pygame.Rect(art_rect.x + 10 + i * 25, art_rect.y + 15, 20, 70)
                pygame.draw.rect(self.surface, Colors.GOLD, pattern_rect, 1)
        
        # Always draw the golden border
        pygame.draw.rect(self.surface, Colors.GOLD, art_rect, 2)
        
        # Card name
        name_font = pygame.font.Font(None, 20)
        name_text = name_font.render(self.data.name, True, Colors.BLACK)
        name_pos = (self.width // 2 - name_text.get_width() // 2, 160)
        self.surface.blit(name_text, name_pos)
        
        # Stats
        stats_font = pygame.font.Font(None, 24)
        
        # Attack
        attack_rect = pygame.Rect(10, self.height - 35, 25, 25)
        pygame.draw.ellipse(self.surface, Colors.DESERT_SAND, attack_rect)
        pygame.draw.ellipse(self.surface, Colors.GOLD, attack_rect, 2)
        attack_text = stats_font.render(str(self.data.attack), True, Colors.BLACK)
        attack_pos = (22 - attack_text.get_width() // 2, self.height - 22 - attack_text.get_height() // 2)
        self.surface.blit(attack_text, attack_pos)
        
        # Health
        health_rect = pygame.Rect(self.width - 35, self.height - 35, 25, 25)
        pygame.draw.ellipse(self.surface, Colors.LAPIS_LAZULI, health_rect)
        pygame.draw.ellipse(self.surface, Colors.GOLD, health_rect, 2)
        health_text = stats_font.render(str(self.data.health), True, Colors.WHITE)
        health_pos = (self.width - 22 - health_text.get_width() // 2, self.height - 22 - health_text.get_height() // 2)
        self.surface.blit(health_text, health_pos)
        
        # Description (truncated)
        desc_font = pygame.font.Font(None, 14)
        desc_text = self.data.description[:40] + "..." if len(self.data.description) > 40 else self.data.description
        desc_surface = desc_font.render(desc_text, True, Colors.BLACK)
        desc_pos = (self.width // 2 - desc_surface.get_width() // 2, 185)
        self.surface.blit(desc_surface, desc_pos)
    
    def get_rect(self):
        """Get the card's rect."""
        return pygame.Rect(self.x, int(self.y + self.hover_offset), self.width, self.height)
    
    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        """Update card animations."""
        # Check hover state
        self.is_hovered = self.get_rect().collidepoint(mouse_pos)
        
        # Hover animation
        target_offset = -10 if self.is_hovered else 0
        self.hover_offset += (target_offset - self.hover_offset) * dt * 6
        
        # Click animation
        if self.click_animation > 0:
            self.click_animation -= dt * 3
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle click events."""
        if self.get_rect().collidepoint(mouse_pos):
            self.click_animation = 1.0
            return True
        return False
    
    def render(self, surface: pygame.Surface):
        """Render the card."""
        draw_pos = (self.x, int(self.y + self.hover_offset))
        
        # Click animation
        if self.click_animation > 0:
            scale = 1.0 + self.click_animation * 0.05
            scaled_size = (int(self.width * scale), int(self.height * scale))
            scaled_surface = pygame.transform.scale(self.surface, scaled_size)
            offset_x = (scaled_size[0] - self.width) // 2
            offset_y = (scaled_size[1] - self.height) // 2
            surface.blit(scaled_surface, (draw_pos[0] - offset_x, draw_pos[1] - offset_y))
        else:
            surface.blit(self.surface, draw_pos)
        
        # Hover glow
        if self.is_hovered:
            glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            glow_surface.fill((255, 255, 255, 20))
            surface.blit(glow_surface, draw_pos)

class ProfessionalDeckBuilder:
    """
    Professional deck builder with complete Hades-level polish.
    Self-contained with no legacy dependencies.
    """
    
    def __init__(self, on_action: Optional[Callable[[DeckBuilderAction], None]] = None):
        """Initialize the professional deck builder."""
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Background
        self.background_surface = self._create_background()
        
        # Sand particles
        self.sand_particles = []
        self._spawn_particles()
        
        # Cards
        self.collection_cards = self._create_card_collection()
        self.deck_cards = []
        self.max_deck_size = 30
        
        # UI state
        self.selected_filter = "all"
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Deck management
        self.current_deck_name = "Working Deck"
        self.show_deck_menu = False
        self.deck_menu_alpha = 0.0
        
        # Layout
        self.collection_area = pygame.Rect(50, 180, SCREEN_WIDTH * 0.7 - 100, SCREEN_HEIGHT - 280)
        self.deck_area = pygame.Rect(SCREEN_WIDTH * 0.7, 180, SCREEN_WIDTH * 0.3 - 50, SCREEN_HEIGHT - 280)
        
        # UI Elements
        self.buttons = self._create_buttons()
        self.filter_buttons = self._create_filter_buttons()
        
        # Update card positions
        self._update_card_positions()
        
        print("Professional Deck Builder initialized with Egyptian excellence")
    
    def _create_background(self):
        """Create ultra-high resolution enhanced background with Egyptian library theme."""
        # Try to load the ultra-high resolution generated deck builder background (4096x2048)
        from ...core.asset_loader import get_asset_loader
        asset_loader = get_asset_loader()
        deck_bg = asset_loader.load_background('deck_builder')
        
        if deck_bg:
            # Scale ultra-high resolution background to screen size with quality scaling
            # Use smoothscale for better quality from 4096x2048 source
            background = pygame.transform.smoothscale(deck_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add atmospheric overlay for enhanced Hades-style depth and readability
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Enhanced gradient overlay for Egyptian library atmosphere
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                alpha = int(25 + ratio * 20)  # Subtle darkening for UI readability
                overlay.fill((10, 5, 0, alpha), (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            return background
        
        # Enhanced fallback: Egyptian library/scroll theme if ultra-high resolution asset loading fails
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Enhanced papyrus-like gradient with Egyptian library ambiance
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(45 + ratio * 35)  # Warmer papyrus tones
            g = int(40 + ratio * 30)  # Aged paper greens
            b = int(25 + ratio * 20)  # Subtle browns
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _spawn_particles(self):
        """Spawn sand particles."""
        for _ in range(8):
            self.sand_particles.append({
                'x': SCREEN_WIDTH * (0.1 + 0.8 * (len(self.sand_particles) / 8)),
                'y': SCREEN_HEIGHT * (0.2 + 0.6 * (len(self.sand_particles) / 8)),
                'size': 2,
                'speed': 10,
                'phase': len(self.sand_particles) * 0.8
            })
    
    def _create_card_collection(self) -> List[Card]:
        """Create the card collection."""
        card_data = [
            CardData("Ra", 8, 10, 12, "legendary", "Sun God of Creation - Deal 3 damage at dawn"),
            CardData("Anubis", 6, 8, 8, "legendary", "Guardian of Dead - Gain +2/+2 when creature dies"),
            CardData("Horus", 5, 7, 6, "rare", "Sky God - Flying, deal 4 damage when played"),
            CardData("Isis", 4, 4, 6, "rare", "Goddess of Magic - Restore 5 health to all"),
            CardData("Bastet", 3, 3, 4, "common", "Protector - Summon two 1/1 sacred cats"),
            CardData("Thoth", 4, 2, 8, "rare", "God of Wisdom - Draw 2 cards"),
            CardData("Sobek", 5, 6, 7, "common", "Crocodile God - Deal 2 damage when attacked"),
            CardData("Ptah", 3, 2, 5, "common", "Creator - Create random artifact card"),
        ]
        
        cards = []
        for data in card_data:
            cards.append(Card(data))
        
        return cards
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create control buttons."""
        buttons = []
        
        button_configs = [
            ("BACK TO MENU", DeckBuilderAction.BACK_TO_MENU),
            ("SAVE", DeckBuilderAction.SAVE_DECK),
            ("SAVE AS...", DeckBuilderAction.SAVE_DECK_AS),
            ("LOAD", DeckBuilderAction.LOAD_DECK),
            ("CLEAR ALL", DeckBuilderAction.CLEAR_DECK)
        ]
        
        button_width = 130
        button_height = 40
        spacing = 15
        start_x = SCREEN_WIDTH - (len(button_configs) * (button_width + spacing))
        
        for i, (text, action) in enumerate(button_configs):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, 20, button_width, button_height, text, FontSizes.BUTTON,
                action=lambda a=action: self._handle_action(a)
            )
            buttons.append(button)
        
        return buttons
    
    def _create_filter_buttons(self) -> List[AnimatedButton]:
        """Create filter buttons."""
        buttons = []
        
        filters = [("ALL", "all"), ("COMMON", "common"), ("RARE", "rare"), ("LEGENDARY", "legendary")]
        button_width = 100
        button_height = 30
        spacing = 10
        start_x = 50
        
        for i, (text, filter_type) in enumerate(filters):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, 130, button_width, button_height, text, FontSizes.CARD_TEXT,
                action=lambda f=filter_type: self._handle_filter(f)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_action(self, action: DeckBuilderAction):
        """Handle button actions."""
        if action == DeckBuilderAction.CLEAR_DECK:
            self.deck_cards.clear()
            self._update_deck_positions()
            deck_manager.clear_deck()
        elif action == DeckBuilderAction.SAVE_DECK:
            # Save current deck with current name
            deck_cards_data = [card.data for card in self.deck_cards]
            
            # Convert to DeckCard format for collection manager
            from ...core.deck_collection_manager import DeckCard
            collection_cards = []
            for card_data in deck_cards_data:
                collection_cards.append(DeckCard(
                    name=card_data.name,
                    cost=card_data.cost,
                    attack=card_data.attack,
                    health=card_data.health,
                    rarity=card_data.rarity,
                    description=card_data.description
                ))
            
            success = deck_collection_manager.save_deck(self.current_deck_name, collection_cards)
            if success:
                # Also save to legacy system for combat compatibility
                deck_manager.save_deck(self.deck_cards)
                print(f"Deck '{self.current_deck_name}' saved successfully! {len(self.deck_cards)} cards ready for combat.")
            else:
                print("Failed to save deck.")
        elif action == DeckBuilderAction.SAVE_DECK_AS:
            self._show_save_as_dialog()
        elif action == DeckBuilderAction.LOAD_DECK:
            self._show_load_deck_menu()
        elif action == DeckBuilderAction.DELETE_DECK:
            self._show_delete_deck_menu()
        
        if self.on_action:
            self.on_action(action)
    
    def _show_save_as_dialog(self):
        """Show save as dialog (simplified for now)."""
        print("Save As functionality - would show text input dialog")
        # For now, create a timestamped deck name
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        new_name = f"Deck_{timestamp}"
        
        # Convert current cards
        from ...core.deck_collection_manager import DeckCard
        collection_cards = []
        for card in self.deck_cards:
            collection_cards.append(DeckCard(
                name=card.data.name,
                cost=card.data.cost,
                attack=card.data.attack,
                health=card.data.health,
                rarity=card.data.rarity,
                description=card.data.description
            ))
        
        success = deck_collection_manager.save_deck(new_name, collection_cards, 
                                                  f"Deck saved at {timestamp}")
        if success:
            self.current_deck_name = new_name
            print(f"Deck saved as '{new_name}'")
    
    def _show_load_deck_menu(self):
        """Show load deck menu (simplified for now)."""
        saved_decks = deck_collection_manager.get_all_deck_names()
        if not saved_decks:
            print("No saved decks found")
            return
        
        print("Available decks:")
        for i, deck_name in enumerate(saved_decks):
            deck_info = deck_collection_manager.get_deck_info(deck_name)
            print(f"{i+1}. {deck_name} ({deck_info.total_cards} cards)")
        
        # For now, load the first deck (in full game, would show selection UI)
        if saved_decks:
            deck_to_load = saved_decks[0]
            loaded_cards = deck_collection_manager.load_deck(deck_to_load)
            if loaded_cards:
                # Convert to Card objects for display
                self.deck_cards.clear()
                for deck_card in loaded_cards:
                    card_data = CardData(
                        deck_card.name, deck_card.cost, deck_card.attack,
                        deck_card.health, deck_card.rarity, deck_card.description
                    )
                    display_card = Card(card_data)
                    self.deck_cards.append(display_card)
                
                self.current_deck_name = deck_to_load
                self._update_deck_positions()
                print(f"Loaded deck: {deck_to_load}")
    
    def _show_delete_deck_menu(self):
        """Show delete deck menu (simplified for now)."""
        print("Delete deck functionality - would show confirmation dialog")
    
    def _handle_filter(self, filter_type: str):
        """Handle filter changes."""
        self.selected_filter = filter_type
        self.scroll_offset = 0
        self._update_card_positions()
    
    def _get_filtered_cards(self) -> List[Card]:
        """Get cards matching current filter."""
        if self.selected_filter == "all":
            return self.collection_cards
        return [card for card in self.collection_cards if card.data.rarity == self.selected_filter]
    
    def _update_card_positions(self):
        """Update card positions in collection."""
        cards = self._get_filtered_cards()
        cards_per_row = 5 if Layout.IS_ULTRAWIDE else 4
        card_spacing = 15
        
        for i, card in enumerate(cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.collection_area.x + col * (card.width + card_spacing)
            y = self.collection_area.y + row * (card.height + card_spacing) - self.scroll_offset
            
            card.x = x
            card.y = y
        
        # Calculate max scroll
        total_rows = (len(cards) + cards_per_row - 1) // cards_per_row
        total_height = total_rows * (card.height + card_spacing)
        self.max_scroll = max(0, total_height - self.collection_area.height)
    
    def _update_deck_positions(self):
        """Update positions of cards in deck."""
        for i, card in enumerate(self.deck_cards):
            card.x = self.deck_area.x + 10
            card.y = self.deck_area.y + i * 30  # Stacked view
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the deck builder."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update particles
        for particle in self.sand_particles:
            particle['x'] += math.sin(self.animation_time * 0.5 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.4
        
        # Update buttons
        for button in self.buttons + self.filter_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Update cards
        for card in self._get_filtered_cards():
            if self.collection_area.colliderect(card.get_rect()):
                card.update(dt, mouse_pos)
        
        for card in self.deck_cards:
            if self.deck_area.colliderect(card.get_rect()):
                card.update(dt, mouse_pos)
        
        # Handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks
                for button in self.buttons + self.filter_buttons:
                    if button.handle_click(mouse_pos):
                        break
                else:
                    # Check card clicks
                    self._handle_card_clicks(mouse_pos)
            
            elif event.type == pygame.MOUSEWHEEL:
                if self.collection_area.collidepoint(mouse_pos):
                    self.scroll_offset -= event.y * 30
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                    self._update_card_positions()
    
    def _handle_card_clicks(self, mouse_pos: Tuple[int, int]):
        """Handle card click events."""
        # Collection cards
        for card in self._get_filtered_cards():
            if self.collection_area.colliderect(card.get_rect()) and card.handle_click(mouse_pos):
                if len(self.deck_cards) < self.max_deck_size:
                    # Create a copy for the deck
                    deck_card = Card(card.data)
                    self.deck_cards.append(deck_card)
                    self._update_deck_positions()
                    # Play card add sound
                    audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.4)
                break
        
        # Deck cards (to remove)
        for i, card in enumerate(self.deck_cards):
            if self.deck_area.colliderect(card.get_rect()) and card.handle_click(mouse_pos):
                self.deck_cards.pop(i)
                self._update_deck_positions()
                # Play card remove sound (different pitch)
                audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.3)
                break
    
    def render(self, surface: pygame.Surface):
        """Render the deck builder."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Sand particles
        self._render_particles(surface)
        
        # Title
        self._render_title(surface)
        
        # Collection panel
        self._render_panel(surface, self.collection_area, "CARD COLLECTION")
        
        # Deck panel
        deck_title = f"YOUR DECK ({len(self.deck_cards)}/{self.max_deck_size})"
        self._render_panel(surface, self.deck_area, deck_title)
        
        # Filter buttons (highlight active)
        for button in self.filter_buttons:
            # Highlight active filter
            if button.action and hasattr(button.action, '__defaults__') and button.action.__defaults__:
                if button.action.__defaults__[0] == self.selected_filter:
                    glow_rect = button.rect.inflate(6, 6)
                    glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                    glow_surface.fill((*Colors.GOLD, 100))
                    surface.blit(glow_surface, glow_rect.topleft)
            
            button.render(surface)
        
        # Control buttons
        for button in self.buttons:
            button.render(surface)
        
        # Cards with clipping
        self._render_cards(surface)
        
        # Instructions
        self._render_instructions(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render sophisticated ultrawide side bars with Egyptian library decorations."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # Enhanced Egyptian library theme for ultrawide bars
        pattern_color = (20, 15, 10)  # Darker papyrus tone
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Add Egyptian scroll decorations for ultra-high resolution aesthetic
        scroll_color = (*Colors.GOLD, 60)
        
        # Vertical scroll patterns
        for bar_rect in [left_bar, right_bar]:
            center_x = bar_rect.centerx
            
            # Main scroll decoration
            scroll_width = min(60, bar_rect.width - 20)
            scroll_rect = pygame.Rect(center_x - scroll_width//2, 50, scroll_width, SCREEN_HEIGHT - 100)
            
            # Create papyrus scroll surface
            scroll_surface = pygame.Surface((scroll_width, SCREEN_HEIGHT - 100), pygame.SRCALPHA)
            scroll_surface.fill((*Colors.PAPYRUS, 40))
            
            # Add scroll top and bottom caps
            cap_height = 20
            pygame.draw.ellipse(scroll_surface, (*Colors.GOLD, 80), (5, 0, scroll_width-10, cap_height))
            pygame.draw.ellipse(scroll_surface, (*Colors.GOLD, 80), (5, SCREEN_HEIGHT-120, scroll_width-10, cap_height))
            
            # Add hieroglyphic-style text lines
            for y in range(cap_height + 20, SCREEN_HEIGHT - 140, 30):
                line_y = y - 50  # Adjust for scroll position
                if 0 <= line_y <= SCREEN_HEIGHT - 150:
                    # Hieroglyphic line patterns
                    pygame.draw.rect(scroll_surface, (*Colors.GOLD, 60), (10, line_y, scroll_width-20, 2))
                    pygame.draw.rect(scroll_surface, (*Colors.GOLD, 60), (15, line_y + 5, scroll_width-30, 2))
                    pygame.draw.rect(scroll_surface, (*Colors.GOLD, 60), (12, line_y + 10, scroll_width-24, 2))
            
            surface.blit(scroll_surface, scroll_rect.topleft)
        
        # Enhanced border lines with pulsing effect
        border_alpha = int(120 + 60 * abs(math.sin(self.animation_time * 2)))
        border_surface = pygame.Surface((4, SCREEN_HEIGHT))
        border_surface.set_alpha(border_alpha)
        border_surface.fill(Colors.GOLD)
        
        # Draw enhanced border lines
        surface.blit(border_surface, (Layout.CONTENT_X_OFFSET - 4, 0))
        surface.blit(border_surface, (Layout.UI_SAFE_RIGHT, 0))
    
    def _render_particles(self, surface: pygame.Surface):
        """Render sand particles."""
        for particle in self.sand_particles:
            alpha = int(100 + 60 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*Colors.DESERT_SAND, alpha))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_title(self, surface: pygame.Surface):
        """Render the main title."""
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "SACRED DECK BUILDER"
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.DESERT_SAND)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 50))
        glow_surface.set_alpha(150)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 48))
        surface.blit(title_surface, title_rect)
        
        # Current deck name
        deck_font = pygame.font.Font(None, FontSizes.BODY)
        deck_text = f"Editing: {self.current_deck_name}"
        deck_surface = deck_font.render(deck_text, True, Colors.LAPIS_LAZULI)
        deck_rect = deck_surface.get_rect(center=(SCREEN_CENTER[0], 75))
        surface.blit(deck_surface, deck_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        subtitle_surface = subtitle_font.render("Forge your divine arsenal", True, Colors.PAPYRUS)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_CENTER[0], 95))
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _render_panel(self, surface: pygame.Surface, rect: pygame.Rect, title: str):
        """Render a UI panel."""
        # Panel background
        panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 100))
        surface.blit(panel_surface, rect.topleft)
        
        # Border
        pygame.draw.rect(surface, Colors.GOLD, rect, 3)
        
        # Title
        font = pygame.font.Font(None, FontSizes.BUTTON)
        title_surface = font.render(title, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(rect.centerx, rect.top - 20))
        surface.blit(title_surface, title_rect)
    
    def _render_cards(self, surface: pygame.Surface):
        """Render cards with clipping."""
        # Collection cards
        original_clip = surface.get_clip()
        surface.set_clip(self.collection_area)
        
        for card in self._get_filtered_cards():
            if self.collection_area.colliderect(card.get_rect()):
                card.render(surface)
        
        surface.set_clip(original_clip)
        
        # Deck cards
        surface.set_clip(self.deck_area)
        for card in self.deck_cards:
            if self.deck_area.colliderect(card.get_rect()):
                card.render(surface)
        
        surface.set_clip(original_clip)
    
    def _render_instructions(self, surface: pygame.Surface):
        """Render helpful instructions."""
        instructions = [
            "Click cards to add to your deck",
            "Mouse wheel to scroll collection",
            "Click deck cards to remove them"
        ]
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        y = SCREEN_HEIGHT - 100
        
        for instruction in instructions:
            text_surface = font.render(instruction, True, Colors.DESERT_SAND)
            text_rect = text_surface.get_rect(center=(SCREEN_CENTER[0], y))
            surface.blit(text_surface, text_rect)
            y += 25
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        for button in self.buttons + self.filter_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0
        
        # Start deck builder music
        audio_manager.play_music(AudioTrack.DECK_BUILDER, fade_in=2.0)