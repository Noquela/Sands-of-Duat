"""
Enhanced Deck Builder - Egyptian Themed UI Improvements

Provides improved visual hierarchy, better card organization, and enhanced
user experience following Hades-style design principles with Egyptian theming.
"""

import pygame
import math
from typing import List, Dict, Optional, Any, Tuple, Callable
from .base import UIScreen, UIComponent
from .hades_theme import HadesEgyptianTheme
from .deck_builder import CardDisplay, CardCollection
from ..core.cards import Card, CardRarity, CardType, Deck
from ..core.player_collection import PlayerCollection


class EnhancedCardSorter(UIComponent):
    """Enhanced card sorting interface with Egyptian visual styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hades_theme = hades_theme
        self.current_sort = "rarity"  # rarity, cost, type, name, owned
        self.sort_ascending = True
        self.active_filters = {
            'rarity': None,
            'type': None,
            'cost_range': (None, None),
            'owned_only': True,
            'favorites_only': False
        }
        
        # Create filter buttons
        self._create_filter_buttons()
        
    def _create_filter_buttons(self):
        """Create Egyptian-themed filter buttons."""
        button_width = (self.rect.width - 30) // 5
        button_height = 35
        y_pos = self.rect.y + 10
        
        # Sort buttons
        sort_options = [
            ("Rarity", "rarity"),
            ("Cost", "cost"), 
            ("Type", "type"),
            ("Name", "name"),
            ("Owned", "owned")
        ]
        
        for i, (label, sort_key) in enumerate(sort_options):
            x_pos = self.rect.x + 10 + i * (button_width + 5)
            button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
            
            # Store button info for rendering and interaction
            button_info = {
                'rect': button_rect,
                'label': label,
                'sort_key': sort_key,
                'active': sort_key == self.current_sort
            }
            
            if not hasattr(self, 'sort_buttons'):
                self.sort_buttons = []
            self.sort_buttons.append(button_info)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enhanced sorting interface."""
        if not self.visible:
            return
        
        # Draw background panel with Egyptian styling
        panel_rect = self.rect.inflate(-5, -5)
        self.hades_theme.draw_ornate_button(surface, panel_rect, "", "normal")
        
        # Render sort buttons
        for button in self.sort_buttons:
            state = "active" if button['active'] else "normal"
            self.hades_theme.draw_ornate_button(surface, button['rect'], button['label'], state)
            
            # Add ascending/descending indicator for active sort
            if button['active']:
                arrow = "↑" if self.sort_ascending else "↓"
                font = pygame.font.Font(None, 20)
                arrow_surface = font.render(arrow, True, self.hades_theme.get_color('papyrus_cream'))
                arrow_x = button['rect'].right - 15
                arrow_y = button['rect'].centery - 10
                surface.blit(arrow_surface, (arrow_x, arrow_y))
        
        # Draw filter status indicators
        self._draw_filter_indicators(surface)
    
    def _draw_filter_indicators(self, surface: pygame.Surface):
        """Draw active filter indicators."""
        indicator_y = self.rect.bottom - 25
        x_offset = self.rect.x + 10
        
        font = pygame.font.Font(None, 16)
        
        # Show active filters
        if self.active_filters['rarity']:
            text = f"Rarity: {self.active_filters['rarity'].value}"
            indicator_surface = font.render(text, True, self.hades_theme.get_color('sacred_turquoise'))
            surface.blit(indicator_surface, (x_offset, indicator_y))
            x_offset += indicator_surface.get_width() + 15
        
        if self.active_filters['type']:
            text = f"Type: {self.active_filters['type'].value}"
            indicator_surface = font.render(text, True, self.hades_theme.get_color('royal_purple'))
            surface.blit(indicator_surface, (x_offset, indicator_y))
            x_offset += indicator_surface.get_width() + 15
        
        if self.active_filters['owned_only']:
            text = "Owned Only"
            indicator_surface = font.render(text, True, self.hades_theme.get_color('duat_gold'))
            surface.blit(indicator_surface, (x_offset, indicator_y))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle sorting and filtering interactions."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.sort_buttons:
                if button['rect'].collidepoint(event.pos):
                    if button['sort_key'] == self.current_sort:
                        # Toggle sort direction
                        self.sort_ascending = not self.sort_ascending
                    else:
                        # Change sort method
                        self.current_sort = button['sort_key']
                        self.sort_ascending = True
                    
                    # Update button states
                    for btn in self.sort_buttons:
                        btn['active'] = btn['sort_key'] == self.current_sort
                    
                    self._trigger_event("sort_changed", {
                        "sort_key": self.current_sort,
                        "ascending": self.sort_ascending
                    })
                    return True
        
        return False


class EnhancedDeckView(UIComponent):
    """Enhanced deck visualization with Egyptian theming and better organization."""
    
    def __init__(self, x: int, y: int, width: int, height: int, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hades_theme = hades_theme
        self.current_deck: Optional[Deck] = None
        self.deck_cards: List[CardDisplay] = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Visual settings
        self.card_width = 100
        self.card_height = 140
        self.cards_per_row = max(1, (width - 40) // (self.card_width + 10))
        self.card_spacing = 10
        
        # Deck statistics
        self.deck_stats = {
            'total_cards': 0,
            'total_cost': 0,
            'average_cost': 0.0,
            'type_distribution': {},
            'rarity_distribution': {}
        }
    
    def set_deck(self, deck: Deck):
        """Set the current deck to display."""
        self.current_deck = deck
        self._update_deck_display()
        self._calculate_deck_stats()
    
    def add_card_to_deck(self, card: Card) -> bool:
        """Add a card to the current deck."""
        if not self.current_deck:
            return False
        
        if self.current_deck.add_card(card):
            self._update_deck_display()
            self._calculate_deck_stats()
            self._trigger_event("deck_changed", {"deck": self.current_deck})
            return True
        return False
    
    def remove_card_from_deck(self, card: Card) -> bool:
        """Remove a card from the current deck."""
        if not self.current_deck:
            return False
        
        if self.current_deck.remove_card(card.id):
            self._update_deck_display()
            self._calculate_deck_stats()
            self._trigger_event("deck_changed", {"deck": self.current_deck})
            return True
        return False
    
    def _update_deck_display(self):
        """Update the visual representation of deck cards."""
        self.deck_cards.clear()
        
        if not self.current_deck:
            return
        
        # Group cards by ID for count display
        card_counts = {}
        for card in self.current_deck.cards:
            card_counts[card.id] = card_counts.get(card.id, 0) + 1
        
        # Create unique card displays
        unique_cards = {}
        for card in self.current_deck.cards:
            if card.id not in unique_cards:
                unique_cards[card.id] = card
        
        # Position cards in grid
        for i, (card_id, card) in enumerate(unique_cards.items()):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.rect.x + 20 + col * (self.card_width + self.card_spacing)
            y = self.rect.y + 80 + row * (self.card_height + self.card_spacing) - self.scroll_offset
            
            card_display = CardDisplay(
                x, y, self.card_width, self.card_height,
                card, owned_count=card_counts[card_id], draggable=True
            )
            
            # Bind removal event
            card_display.bind_event("card_double_click", self._on_card_double_click)
            
            self.deck_cards.append(card_display)
        
        # Calculate scroll bounds
        total_rows = (len(unique_cards) + self.cards_per_row - 1) // self.cards_per_row
        total_height = total_rows * (self.card_height + self.card_spacing) + 160
        self.max_scroll = max(0, total_height - self.rect.height)
    
    def _calculate_deck_stats(self):
        """Calculate and update deck statistics."""
        if not self.current_deck:
            self.deck_stats = {
                'total_cards': 0,
                'total_cost': 0,
                'average_cost': 0.0,
                'type_distribution': {},
                'rarity_distribution': {}
            }
            return
        
        cards = self.current_deck.cards
        self.deck_stats['total_cards'] = len(cards)
        self.deck_stats['total_cost'] = sum(card.sand_cost for card in cards)
        self.deck_stats['average_cost'] = self.deck_stats['total_cost'] / len(cards) if cards else 0.0
        
        # Type distribution
        type_counts = {}
        for card in cards:
            card_type = card.card_type.value
            type_counts[card_type] = type_counts.get(card_type, 0) + 1
        self.deck_stats['type_distribution'] = type_counts
        
        # Rarity distribution
        rarity_counts = {}
        for card in cards:
            rarity = card.rarity.value
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        self.deck_stats['rarity_distribution'] = rarity_counts
    
    def _on_card_double_click(self, event_data: Dict[str, Any]):
        """Handle card double-click for removal."""
        card = event_data['card']
        self.remove_card_from_deck(card)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enhanced deck view."""
        if not self.visible:
            return
        
        # Draw deck panel background
        panel_rect = self.rect.inflate(-5, -5)
        self.hades_theme.draw_ornate_button(surface, panel_rect, "", "normal")
        
        # Draw deck title and stats
        self._draw_deck_header(surface)
        
        # Draw deck cards
        for card_display in self.deck_cards:
            if self._is_card_visible(card_display):
                card_display.render(surface)
        
        # Draw deck statistics
        self._draw_deck_statistics(surface)
    
    def _draw_deck_header(self, surface: pygame.Surface):
        """Draw deck title and basic info."""
        header_y = self.rect.y + 15
        
        # Deck name
        deck_name = self.current_deck.name if self.current_deck else "No Deck Selected"
        self.hades_theme.draw_title_text(surface, deck_name, 
                                        (self.rect.centerx, header_y), 'header')
        
        # Card count
        if self.current_deck:
            count_text = f"{self.deck_stats['total_cards']}/30 cards"
            font = pygame.font.Font(None, 18)
            count_surface = font.render(count_text, True, self.hades_theme.get_color('papyrus_cream'))
            count_x = self.rect.centerx - count_surface.get_width() // 2
            surface.blit(count_surface, (count_x, header_y + 35))
    
    def _draw_deck_statistics(self, surface: pygame.Surface):
        """Draw detailed deck statistics."""
        stats_x = self.rect.x + 10
        stats_y = self.rect.bottom - 120
        
        font = pygame.font.Font(None, 16)
        
        # Average cost
        avg_cost_text = f"Avg Cost: {self.deck_stats['average_cost']:.1f}"
        avg_surface = font.render(avg_cost_text, True, self.hades_theme.get_color('desert_amber'))
        surface.blit(avg_surface, (stats_x, stats_y))
        
        # Type distribution
        y_offset = 20
        for card_type, count in self.deck_stats['type_distribution'].items():
            type_text = f"{card_type}: {count}"
            type_surface = font.render(type_text, True, self.hades_theme.get_color('sacred_turquoise'))
            surface.blit(type_surface, (stats_x, stats_y + y_offset))
            y_offset += 15
    
    def _is_card_visible(self, card_display: CardDisplay) -> bool:
        """Check if a card is within the visible area."""
        return (card_display.rect.bottom > self.rect.y + 60 and 
                card_display.rect.top < self.rect.bottom)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle deck view interactions including scrolling."""
        if not self.visible or not self.enabled:
            return False
        
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            scroll_amount = event.y * 30
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - scroll_amount))
            self._update_deck_display()  # Refresh positions
            return True
        
        # Forward events to visible cards
        for card_display in self.deck_cards:
            if self._is_card_visible(card_display):
                if card_display.handle_event(event):
                    return True
        
        return False


class VisualHierarchyEnhancements:
    """Visual hierarchy improvements for the deck builder."""
    
    @staticmethod
    def create_section_divider(surface: pygame.Surface, hades_theme: HadesEgyptianTheme,
                              start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                              style: str = "papyrus_scroll") -> None:
        """Create Egyptian-themed section dividers."""
        if style == "papyrus_scroll":
            # Draw papyrus-style scroll divider
            pygame.draw.line(surface, hades_theme.get_color('pharaoh_bronze'), 
                           start_pos, end_pos, 3)
            
            # Add decorative elements at ends
            for pos in [start_pos, end_pos]:
                pygame.draw.circle(surface, hades_theme.get_color('duat_gold'), pos, 8)
                pygame.draw.circle(surface, hades_theme.get_color('pharaoh_bronze'), pos, 8, 2)
        
        elif style == "hieroglyph_border":
            # Draw with hieroglyphic decorations
            pygame.draw.line(surface, hades_theme.get_color('sacred_turquoise'),
                           start_pos, end_pos, 2)
            
            # Add ankh symbols along the line
            line_length = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
            num_symbols = int(line_length // 50)
            
            for i in range(num_symbols):
                t = i / max(1, num_symbols - 1)
                x = int(start_pos[0] + t * (end_pos[0] - start_pos[0]))
                y = int(start_pos[1] + t * (end_pos[1] - start_pos[1]))
                
                # Small ankh symbol
                hades_theme._draw_transition_ankh(surface, (x, y), 6, 
                                                (*hades_theme.get_color('duat_gold'), 255))
    
    @staticmethod
    def create_card_category_header(surface: pygame.Surface, hades_theme: HadesEgyptianTheme,
                                  rect: pygame.Rect, category_name: str, 
                                  card_count: int = 0) -> None:
        """Create category headers for card sections."""
        # Background with Egyptian styling
        header_rect = pygame.Rect(rect.x, rect.y, rect.width, 40)
        hades_theme.draw_ornate_button(surface, header_rect, "", "normal")
        
        # Category title
        title_pos = (header_rect.centerx - 50, header_rect.centery)
        hades_theme.draw_title_text(surface, category_name, title_pos, 'body')
        
        # Card count badge
        if card_count > 0:
            badge_x = header_rect.right - 40
            badge_y = header_rect.centery
            badge_rect = pygame.Rect(badge_x - 15, badge_y - 10, 30, 20)
            
            pygame.draw.ellipse(surface, hades_theme.get_color('underworld_crimson'), badge_rect)
            pygame.draw.ellipse(surface, hades_theme.get_color('duat_gold'), badge_rect, 2)
            
            # Count text
            font = pygame.font.Font(None, 16)
            count_surface = font.render(str(card_count), True, 
                                      hades_theme.get_color('papyrus_cream'))
            count_rect = count_surface.get_rect(center=(badge_x, badge_y))
            surface.blit(count_surface, count_rect)
    
    @staticmethod
    def add_atmospheric_effects(surface: pygame.Surface, hades_theme: HadesEgyptianTheme,
                               screen_rect: pygame.Rect, time_factor: float) -> None:
        """Add subtle atmospheric effects to enhance immersion."""
        # Floating sand particles
        import random
        random.seed(int(time_factor * 100) % 1000)
        
        for _ in range(15):
            x = random.randint(0, screen_rect.width)
            y = random.randint(0, screen_rect.height)
            
            # Particle movement based on time
            offset_x = math.sin(time_factor * 0.5 + x * 0.01) * 20
            offset_y = math.cos(time_factor * 0.3 + y * 0.01) * 15
            
            particle_x = int(x + offset_x)
            particle_y = int(y + offset_y)
            
            if 0 <= particle_x < screen_rect.width and 0 <= particle_y < screen_rect.height:
                alpha = int(50 + 30 * abs(math.sin(time_factor * 2 + x)))
                particle_color = (*hades_theme.get_color('desert_amber'), alpha)
                
                particle_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, (1, 1), 1)
                surface.blit(particle_surface, (particle_x, particle_y))