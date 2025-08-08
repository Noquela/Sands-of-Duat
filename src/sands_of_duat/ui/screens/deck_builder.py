#!/usr/bin/env python3
"""
SANDS OF DUAT - DECK BUILDER SCREEN
==================================

Premium deck builder interface for managing Egyptian god card collections.
Features authentic card artwork and intuitive deck construction.
"""

import pygame
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from ..components.card_display import CardCollection, EgyptianCard, create_card_collection

# Asset paths
ASSETS_ROOT = Path(__file__).parent.parent.parent.parent.parent / "assets"
FINAL_DATASET_PATH = ASSETS_ROOT / "images" / "lora_training" / "final_dataset"

class DeckBuilderScreen:
    """Egyptian-themed deck builder interface."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Egyptian color palette
        self.colors = {
            'GOLD': (255, 215, 0),
            'GOLD_DARK': (184, 134, 11),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'DARK_BLUE': (25, 25, 112),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'HOVER_GLOW': (255, 255, 255, 100),
            'PANEL_BG': (45, 45, 80, 200)
        }
        
        # Load background
        self.background = self._load_background()
        
        # Initialize fonts
        self._init_fonts()
        
        # Card collection and deck
        self.card_collection = create_card_collection()
        self.current_deck = []
        self.max_deck_size = 30
        
        # UI layout
        self._setup_layout()
        
        # State management
        self.selected_card = None
        self.filter_rarity = "all"  # "all", "common", "rare", "legendary"
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Animation
        self.transition_alpha = 255
    
    def _load_background(self) -> pygame.Surface:
        """Load Egyptian background for deck builder."""
        background_assets = [
            "egyptian_myth_09_q84.png",
            "egyptian_god_scene_06_q82.png",
            "egyptian_myth_07_q79.png"
        ]
        
        for asset_name in background_assets:
            asset_path = FINAL_DATASET_PATH / asset_name
            if asset_path.exists():
                try:
                    bg_image = pygame.image.load(str(asset_path))
                    return self._scale_background(bg_image)
                except pygame.error as e:
                    print(f"Could not load {asset_name}: {e}")
                    continue
        
        # Fallback background
        fallback = pygame.Surface((self.screen_width, self.screen_height))
        fallback.fill(self.colors['DARK_BLUE'])
        return fallback
    
    def _scale_background(self, image: pygame.Surface) -> pygame.Surface:
        """Scale background to fit screen."""
        img_width, img_height = image.get_size()
        scale_x = self.screen_width / img_width
        scale_y = self.screen_height / img_height
        scale = max(scale_x, scale_y)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        
        final_surface = pygame.Surface((self.screen_width, self.screen_height))
        x_offset = (self.screen_width - new_width) // 2
        y_offset = (self.screen_height - new_height) // 2
        final_surface.blit(scaled_image, (x_offset, y_offset))
        
        return final_surface
    
    def _init_fonts(self):
        """Initialize fonts for deck builder."""
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 24)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
    
    def _setup_layout(self):
        """Setup UI layout areas."""
        margin = 20
        
        # Collection panel (left side)
        self.collection_panel = pygame.Rect(
            margin, 
            100, 
            self.screen_width * 0.65 - margin, 
            self.screen_height - 140
        )
        
        # Deck panel (right side)  
        self.deck_panel = pygame.Rect(
            self.screen_width * 0.65,
            100,
            self.screen_width * 0.35 - margin,
            self.screen_height - 140
        )
        
        # Filter buttons
        self.filter_buttons = self._create_filter_buttons()
        
        # Control buttons
        self.control_buttons = self._create_control_buttons()
        
        # Calculate card positions in collection
        self._update_card_positions()
    
    def _create_filter_buttons(self) -> List[Dict]:
        """Create rarity filter buttons."""
        filters = ["ALL", "COMMON", "RARE", "LEGENDARY"]
        button_width = 100
        button_height = 35
        start_x = self.collection_panel.x
        y = 70
        
        buttons = []
        for i, filter_name in enumerate(filters):
            button_rect = pygame.Rect(
                start_x + i * (button_width + 10),
                y,
                button_width,
                button_height
            )
            buttons.append({
                'text': filter_name,
                'filter': filter_name.lower(),
                'rect': button_rect
            })
        
        return buttons
    
    def _create_control_buttons(self) -> List[Dict]:
        """Create control buttons (back, save, clear)."""
        button_width = 120
        button_height = 40
        margin = 10
        start_x = self.screen_width - (button_width * 3 + margin * 3)
        y = 20
        
        buttons = [
            {
                'text': 'BACK TO MENU',
                'action': 'back',
                'rect': pygame.Rect(start_x, y, button_width, button_height)
            },
            {
                'text': 'SAVE DECK',
                'action': 'save',
                'rect': pygame.Rect(start_x + button_width + margin, y, button_width, button_height)
            },
            {
                'text': 'CLEAR DECK',
                'action': 'clear',
                'rect': pygame.Rect(start_x + (button_width + margin) * 2, y, button_width, button_height)
            }
        ]
        
        return buttons
    
    def _update_card_positions(self):
        """Update card positions in the collection panel."""
        # Get filtered cards
        if self.filter_rarity == "all":
            cards = self.card_collection.cards
        else:
            cards = self.card_collection.get_cards_by_rarity(self.filter_rarity)
        
        # Calculate grid layout
        cards_per_row = 4
        card_width = 200
        card_height = 300
        card_spacing = 20
        
        for i, card in enumerate(cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.collection_panel.x + col * (card_width + card_spacing) + card_spacing
            y = self.collection_panel.y + row * (card_height + card_spacing) + card_spacing - self.scroll_offset
            
            card.position = (x, y)
        
        # Calculate max scroll
        total_rows = (len(cards) + cards_per_row - 1) // cards_per_row
        total_height = total_rows * (card_height + card_spacing)
        self.max_scroll = max(0, total_height - self.collection_panel.height + card_spacing)
    
    def _get_visible_cards(self) -> List[EgyptianCard]:
        """Get cards that are currently visible in the collection panel."""
        if self.filter_rarity == "all":
            cards = self.card_collection.cards
        else:
            cards = self.card_collection.get_cards_by_rarity(self.filter_rarity)
        
        visible_cards = []
        for card in cards:
            card_bottom = card.position[1] + card.size[1]
            if (card.position[1] < self.collection_panel.bottom and 
                card_bottom > self.collection_panel.top):
                visible_cards.append(card)
        
        return visible_cards
    
    def _draw_panel(self, surface: pygame.Surface, rect: pygame.Rect, title: str):
        """Draw a UI panel with Egyptian styling."""
        # Panel background
        panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel_surface.fill(self.colors['PANEL_BG'])
        surface.blit(panel_surface, rect.topleft)
        
        # Panel border
        pygame.draw.rect(surface, self.colors['GOLD'], rect, 3)
        
        # Egyptian corner decorations
        self._draw_egyptian_corners(surface, rect, self.colors['GOLD'])
        
        # Panel title
        title_surface = self.header_font.render(title, True, self.colors['GOLD'])
        title_x = rect.centerx - title_surface.get_width() // 2
        title_y = rect.top - 35
        surface.blit(title_surface, (title_x, title_y))
    
    def _draw_egyptian_corners(self, surface: pygame.Surface, rect: pygame.Rect, 
                              color: Tuple[int, int, int]):
        """Draw Egyptian-style decorative corners."""
        corner_size = 20
        thickness = 4
        
        corners = [
            # Top-left
            [(rect.left + corner_size, rect.top), (rect.left, rect.top), (rect.left, rect.top + corner_size)],
            # Top-right  
            [(rect.right - corner_size, rect.top), (rect.right, rect.top), (rect.right, rect.top + corner_size)],
            # Bottom-left
            [(rect.left + corner_size, rect.bottom), (rect.left, rect.bottom), (rect.left, rect.bottom - corner_size)],
            # Bottom-right
            [(rect.right - corner_size, rect.bottom), (rect.right, rect.bottom), (rect.right, rect.bottom - corner_size)]
        ]
        
        for corner in corners:
            pygame.draw.lines(surface, color, False, corner, thickness)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle deck builder events."""
        # Control buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Check control buttons
            for button in self.control_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    if button['action'] == 'clear':
                        self.current_deck.clear()
                    return button['action']
            
            # Check filter buttons
            for button in self.filter_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    self.filter_rarity = button['filter']
                    self.scroll_offset = 0
                    self._update_card_positions()
                    break
            
            # Check cards in collection
            for card in self._get_visible_cards():
                if card.handle_event(event):
                    if len(self.current_deck) < self.max_deck_size:
                        # Add to deck (create copy)
                        deck_card = EgyptianCard(card.data)
                        self.current_deck.append(deck_card)
                        self._update_deck_positions()
                    break
            
            # Check cards in deck (to remove them)
            for i, card in enumerate(self.current_deck):
                if card.handle_event(event):
                    self.current_deck.pop(i)
                    self._update_deck_positions()
                    break
        
        # Scrolling
        elif event.type == pygame.MOUSEWHEEL:
            if self.collection_panel.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset -= event.y * 50
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                self._update_card_positions()
        
        # Keyboard shortcuts
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        
        # Update card hover states
        elif event.type == pygame.MOUSEMOTION:
            for card in self._get_visible_cards():
                card.handle_event(event)
            for card in self.current_deck:
                card.handle_event(event)
        
        return None
    
    def _update_deck_positions(self):
        """Update positions of cards in the current deck."""
        card_width = 120  # Smaller cards in deck view
        card_height = 180
        card_spacing = 10
        start_y = self.deck_panel.y + 20
        
        for i, card in enumerate(self.current_deck):
            # Resize card for deck display
            if card.size != (card_width, card_height):
                card.size = (card_width, card_height)
                card._render_card()
            
            x = self.deck_panel.x + 10
            y = start_y + i * (card_height // 3 + card_spacing)  # Stacked view
            card.position = (x, y)
    
    def update(self, dt: float):
        """Update deck builder animations."""
        # Update card animations
        for card in self._get_visible_cards():
            card.update(dt)
        
        for card in self.current_deck:
            card.update(dt)
        
        # Transition animation
        if self.transition_alpha > 0:
            self.transition_alpha -= dt * 500
            if self.transition_alpha < 0:
                self.transition_alpha = 0
    
    def draw(self):
        """Draw the deck builder screen."""
        # Background
        self.screen.blit(self.background, (0, 0))
        
        # Dark overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        overlay.fill(self.colors['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = "DECK BUILDER"
        title_surface = self.title_font.render(title_text, True, self.colors['GOLD'])
        title_x = 50
        title_y = 20
        self.screen.blit(title_surface, (title_x, title_y))
        
        # Collection panel
        self._draw_panel(self.screen, self.collection_panel, "CARD COLLECTION")
        
        # Deck panel  
        self._draw_panel(self.screen, self.deck_panel, f"YOUR DECK ({len(self.current_deck)}/{self.max_deck_size})")
        
        # Filter buttons
        for i, button in enumerate(self.filter_buttons):
            is_active = button['filter'] == self.filter_rarity
            color = self.colors['GOLD'] if is_active else self.colors['DESERT_SAND']
            
            pygame.draw.rect(self.screen, color, button['rect'], 0 if is_active else 2)
            
            text_color = self.colors['BLACK'] if is_active else color
            text_surface = self.button_font.render(button['text'], True, text_color)
            text_x = button['rect'].centerx - text_surface.get_width() // 2
            text_y = button['rect'].centery - text_surface.get_height() // 2
            self.screen.blit(text_surface, (text_x, text_y))
        
        # Control buttons
        for button in self.control_buttons:
            pygame.draw.rect(self.screen, self.colors['LAPIS_LAZULI'], button['rect'])
            pygame.draw.rect(self.screen, self.colors['GOLD'], button['rect'], 2)
            
            text_surface = self.button_font.render(button['text'], True, self.colors['PAPYRUS'])
            text_x = button['rect'].centerx - text_surface.get_width() // 2
            text_y = button['rect'].centery - text_surface.get_height() // 2
            self.screen.blit(text_surface, (text_x, text_y))
        
        # Create clipping region for collection panel
        original_clip = self.screen.get_clip()
        self.screen.set_clip(self.collection_panel)
        
        # Draw collection cards
        for card in self._get_visible_cards():
            card.draw(self.screen)
        
        # Restore clipping
        self.screen.set_clip(original_clip)
        
        # Create clipping region for deck panel
        self.screen.set_clip(self.deck_panel)
        
        # Draw deck cards
        for card in self.current_deck:
            card.draw(self.screen)
        
        # Restore clipping
        self.screen.set_clip(original_clip)
        
        # Instructions
        instructions = [
            "Click cards to add to deck",
            "Mouse wheel to scroll",
            "Click deck cards to remove"
        ]
        
        y_offset = self.screen_height - 80
        for instruction in instructions:
            text_surface = self.small_font.render(instruction, True, self.colors['DESERT_SAND'])
            self.screen.blit(text_surface, (50, y_offset))
            y_offset += 20
        
        # Transition effect
        if self.transition_alpha > 0:
            transition_surface = pygame.Surface((self.screen_width, self.screen_height))
            transition_surface.set_alpha(self.transition_alpha)
            transition_surface.fill(self.colors['BLACK'])
            self.screen.blit(transition_surface, (0, 0))


def create_deck_builder(screen: pygame.Surface) -> DeckBuilderScreen:
    """Factory function to create deck builder screen."""
    return DeckBuilderScreen(screen)