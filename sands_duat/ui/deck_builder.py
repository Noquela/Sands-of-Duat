"""
Deck Builder Screen

Card collection management interface for building and customizing decks.
"""

import pygame
from typing import List, Dict, Optional, Any, Tuple
from .base import UIScreen, UIComponent
from core.cards import Card, Deck, CardRarity


class CardDisplay(UIComponent):
    """Simple card display component for deck builder."""
    
    def __init__(self, x: int, y: int, width: int, height: int, card: Card):
        super().__init__(x, y, width, height)
        self.card = card
    
    def update(self, delta_time: float) -> None:
        """Update card display."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the card."""
        if not self.visible:
            return
        
        # Simple card rendering
        pygame.draw.rect(surface, (60, 45, 30), self.rect)
        pygame.draw.rect(surface, (139, 117, 93), self.rect, 2)
        
        # Card name
        font = pygame.font.Font(None, 20)
        text = font.render(self.card.name[:10], True, (255, 248, 220))
        surface.blit(text, (self.rect.x + 5, self.rect.y + 5))


class CardCollection(UIComponent):
    """
    Displays the player's card collection with filtering and search.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.all_cards: List[Card] = []
        self.filtered_cards: List[Card] = []
        self.card_displays: List[CardDisplay] = []
        self.selected_cards: List[int] = []
        
        # Layout settings
        self.cards_per_row = 6
        self.card_width = 90
        self.card_height = 120
        self.card_spacing = 10
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Filters
        self.rarity_filter: Optional[CardRarity] = None
        self.cost_filter: Optional[int] = None
        self.search_text = ""
    
    def update(self, delta_time: float) -> None:
        """Update card collection display."""
        # Update card displays
        for card_display in self.card_displays:
            card_display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the card collection."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, (30, 25, 20), self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Create clipping surface for scrolling
        clip_surface = surface.subsurface(self.rect)
        
        # Render visible cards
        for card_display in self.card_displays:
            if self._is_card_visible(card_display):
                adjusted_rect = card_display.rect.copy()
                adjusted_rect.y -= self.scroll_offset
                
                # Temporarily adjust the card display position
                old_rect = card_display.rect
                card_display.rect = adjusted_rect
                card_display.render(clip_surface)
                card_display.rect = old_rect
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for card selection and scrolling."""
        if not self.visible or not self.enabled:
            return False
        
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self._scroll(-event.y * 30)  # Scroll speed
            return True
        
        # Handle card clicks
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Adjust click position for scroll offset
            adjusted_pos = (event.pos[0], event.pos[1] + self.scroll_offset)
            
            for i, card_display in enumerate(self.card_displays):
                if card_display.rect.collidepoint(adjusted_pos):
                    self._select_card(i, event.button == 1)  # Left click to select
                    return True
        
        return super().handle_event(event)
    
    def set_cards(self, cards: List[Card]) -> None:
        """Set the collection of cards."""
        self.all_cards = cards
        self._apply_filters()
        self._update_layout()
    
    def set_rarity_filter(self, rarity: Optional[CardRarity]) -> None:
        """Filter cards by rarity."""
        self.rarity_filter = rarity
        self._apply_filters()
        self._update_layout()
    
    def set_cost_filter(self, cost: Optional[int]) -> None:
        """Filter cards by sand cost."""
        self.cost_filter = cost
        self._apply_filters()
        self._update_layout()
    
    def set_search_text(self, text: str) -> None:
        """Filter cards by search text."""
        self.search_text = text.lower()
        self._apply_filters()
        self._update_layout()
    
    def get_selected_cards(self) -> List[Card]:
        """Get the currently selected cards."""
        return [self.filtered_cards[i] for i in self.selected_cards if i < len(self.filtered_cards)]
    
    def clear_selection(self) -> None:
        """Clear all selected cards."""
        self.selected_cards.clear()
        for card_display in self.card_displays:
            card_display.background_color = (40, 30, 20)  # Reset to default
    
    def _apply_filters(self) -> None:
        """Apply current filters to the card collection."""
        self.filtered_cards = self.all_cards.copy()
        
        # Apply rarity filter
        if self.rarity_filter:
            self.filtered_cards = [c for c in self.filtered_cards if c.rarity == self.rarity_filter]
        
        # Apply cost filter
        if self.cost_filter is not None:
            self.filtered_cards = [c for c in self.filtered_cards if c.sand_cost == self.cost_filter]
        
        # Apply search filter
        if self.search_text:
            self.filtered_cards = [c for c in self.filtered_cards 
                                 if self.search_text in c.name.lower() or 
                                    self.search_text in c.description.lower()]
    
    def _update_layout(self) -> None:
        """Update the layout of card displays."""
        self.card_displays.clear()
        self.selected_cards.clear()
        
        rows = (len(self.filtered_cards) + self.cards_per_row - 1) // self.cards_per_row
        total_height = rows * (self.card_height + self.card_spacing)
        self.max_scroll = max(0, total_height - self.rect.height)
        
        for i, card in enumerate(self.filtered_cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.rect.x + col * (self.card_width + self.card_spacing)
            y = self.rect.y + row * (self.card_height + self.card_spacing)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, card)
            self.card_displays.append(card_display)
    
    def _scroll(self, delta: int) -> None:
        """Scroll the card collection."""
        self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset + delta))
    
    def _is_card_visible(self, card_display: CardDisplay) -> bool:
        """Check if a card display is currently visible."""
        adjusted_y = card_display.rect.y - self.scroll_offset
        return (adjusted_y + card_display.rect.height >= self.rect.y and 
                adjusted_y <= self.rect.bottom)
    
    def _select_card(self, index: int, select: bool) -> None:
        """Select or deselect a card."""
        if select:
            if index not in self.selected_cards:
                self.selected_cards.append(index)
                self.card_displays[index].background_color = (60, 60, 100)  # Blue tint
        else:
            if index in self.selected_cards:
                self.selected_cards.remove(index)
                self.card_displays[index].background_color = (40, 30, 20)  # Default


class DeckView(UIComponent):
    """
    Displays the current deck being built.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.deck: Optional[Deck] = None
        self.card_displays: List[CardDisplay] = []
        
        # Layout settings
        self.cards_per_row = 4
        self.card_width = 70
        self.card_height = 95
        self.card_spacing = 8
    
    def update(self, delta_time: float) -> None:
        """Update deck view."""
        for card_display in self.card_displays:
            card_display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the deck view."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, (25, 20, 15), self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw title
        font = pygame.font.Font(None, 24)
        title = "Current Deck"
        if self.deck:
            title += f" ({len(self.deck.cards)}/30)"  # Assuming 30 card limit
        
        title_surface = font.render(title, True, self.text_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.top = self.rect.top + 10
        surface.blit(title_surface, title_rect)
        
        # Render cards
        for card_display in self.card_displays:
            card_display.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for deck interaction."""
        if not self.visible or not self.enabled:
            return False
        
        # Handle card removal (right-click)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            for i, card_display in enumerate(self.card_displays):
                if card_display.rect.collidepoint(event.pos):
                    self._remove_card(i)
                    return True
        
        return super().handle_event(event)
    
    def set_deck(self, deck: Deck) -> None:
        """Set the deck to display."""
        self.deck = deck
        self._update_layout()
    
    def add_card(self, card: Card) -> bool:
        """Add a card to the deck."""
        if self.deck and len(self.deck.cards) < 30:  # Deck size limit
            self.deck.add_card(card)
            self._update_layout()
            return True
        return False
    
    def remove_card_at(self, index: int) -> Optional[Card]:
        """Remove a card at the specified index."""
        if self.deck and 0 <= index < len(self.deck.cards):
            card = self.deck.cards.pop(index)
            self._update_layout()
            return card
        return None
    
    def _update_layout(self) -> None:
        """Update the layout of cards in the deck view."""
        self.card_displays.clear()
        
        if not self.deck:
            return
        
        start_y = self.rect.top + 40  # Leave space for title
        
        for i, card in enumerate(self.deck.cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.rect.x + 10 + col * (self.card_width + self.card_spacing)
            y = start_y + row * (self.card_height + self.card_spacing)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, card)
            self.card_displays.append(card_display)
    
    def _remove_card(self, index: int) -> None:
        """Remove a card from the deck."""
        removed_card = self.remove_card_at(index)
        if removed_card:
            self._trigger_event("card_removed", {"card": removed_card, "index": index})


class FilterPanel(UIComponent):
    """
    Panel with filter controls for the card collection.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.selected_rarity: Optional[CardRarity] = None
        self.selected_cost: Optional[int] = None
        
    def update(self, delta_time: float) -> None:
        """Update filter panel."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the filter panel."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, (35, 30, 25), self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw filter buttons (simplified)
        font = pygame.font.Font(None, 20)
        y_offset = self.rect.top + 10
        
        # Rarity filters
        rarity_text = font.render("Rarity:", True, self.text_color)
        surface.blit(rarity_text, (self.rect.x + 10, y_offset))
        y_offset += 25
        
        for rarity in CardRarity:
            color = self.text_color if self.selected_rarity != rarity else (255, 215, 0)
            rarity_label = font.render(rarity.value.title(), True, color)
            surface.blit(rarity_label, (self.rect.x + 10, y_offset))
            y_offset += 20
        
        y_offset += 10
        
        # Cost filters
        cost_text = font.render("Cost:", True, self.text_color)
        surface.blit(cost_text, (self.rect.x + 10, y_offset))
        y_offset += 25
        
        for cost in range(7):  # 0-6 sand cost
            color = self.text_color if self.selected_cost != cost else (255, 215, 0)
            cost_label = font.render(str(cost), True, color)
            surface.blit(cost_label, (self.rect.x + 10, y_offset))
            y_offset += 20
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle filter interactions."""
        # Simplified click handling - in a full implementation,
        # this would use proper button components
        return super().handle_event(event)


class DeckBuilderScreen(UIScreen):
    """
    Deck building and card collection management screen.
    
    Allows players to browse their card collection, build custom decks,
    and manage their card inventory.
    """
    
    def __init__(self):
        super().__init__("deck_builder")
        
        # UI components
        self.card_collection: Optional[CardCollection] = None
        self.deck_view: Optional[DeckView] = None
        self.filter_panel: Optional[FilterPanel] = None
        
        # State
        self.current_deck: Optional[Deck] = None
        self.available_cards: List[Card] = []
    
    def on_enter(self) -> None:
        """Initialize deck builder screen."""
        self.logger.info("Entering deck builder screen")
        self._setup_ui_components()
        self._setup_sample_data()
    
    def on_exit(self) -> None:
        """Clean up deck builder screen."""
        self.logger.info("Exiting deck builder screen")
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up all UI components."""
        # Filter panel (left side)
        self.filter_panel = FilterPanel(20, 20, 150, 500)
        self.add_component(self.filter_panel)
        
        # Card collection (center)
        self.card_collection = CardCollection(180, 20, 400, 500)
        self.card_collection.add_event_handler("card_selected", self._on_card_selected)
        self.add_component(self.card_collection)
        
        # Deck view (right side)
        self.deck_view = DeckView(590, 20, 200, 500)
        self.deck_view.add_event_handler("card_removed", self._on_card_removed)
        self.add_component(self.deck_view)
        
        # Initialize with empty deck
        self.current_deck = Deck(name="Custom Deck")
        self.deck_view.set_deck(self.current_deck)
    
    def _setup_sample_data(self) -> None:
        """Set up sample cards for demonstration."""
        # This would normally load from the card library
        sample_cards = []
        
        # Create some sample cards
        from ..core.cards import Card, CardType, CardRarity, CardEffect, EffectType, TargetType
        
        # Sample attack cards
        for i in range(10):
            card = Card(
                name=f"Attack Card {i+1}",
                description=f"Deal {5+i} damage to an enemy.",
                sand_cost=1 + (i // 3),
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(
                    effect_type=EffectType.DAMAGE,
                    value=5+i,
                    target=TargetType.ENEMY
                )]
            )
            sample_cards.append(card)
        
        # Sample skill cards
        for i in range(8):
            card = Card(
                name=f"Skill Card {i+1}",
                description=f"Gain {3+i} block.",
                sand_cost=1 + (i // 4),
                card_type=CardType.SKILL,
                rarity=CardRarity.COMMON if i < 5 else CardRarity.UNCOMMON,
                effects=[CardEffect(
                    effect_type=EffectType.BLOCK,
                    value=3+i,
                    target=TargetType.SELF
                )]
            )
            sample_cards.append(card)
        
        self.available_cards = sample_cards
        self.card_collection.set_cards(sample_cards)
    
    def _on_card_selected(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card selection from collection."""
        selected_cards = self.card_collection.get_selected_cards()
        if selected_cards and self.deck_view:
            # Add first selected card to deck
            card = selected_cards[0]
            if self.deck_view.add_card(card):
                self.logger.info(f"Added card to deck: {card.name}")
                # Clear selection after adding
                self.card_collection.clear_selection()
            else:
                self.logger.warning("Cannot add card: deck is full")
    
    def _on_card_removed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card removal from deck."""
        card = event_data.get("card")
        if card:
            self.logger.info(f"Removed card from deck: {card.name}")
    
    def set_available_cards(self, cards: List[Card]) -> None:
        """Set the available card collection."""
        self.available_cards = cards
        if self.card_collection:
            self.card_collection.set_cards(cards)
    
    def get_current_deck(self) -> Optional[Deck]:
        """Get the currently built deck."""
        return self.current_deck
    
    def save_deck(self, name: str) -> bool:
        """Save the current deck with a given name."""
        if self.current_deck:
            self.current_deck.name = name
            # In a full implementation, this would save to file or database
            self.logger.info(f"Saved deck: {name}")
            return True
        return False
    
    def load_deck(self, deck: Deck) -> None:
        """Load a deck for editing."""
        self.current_deck = deck
        if self.deck_view:
            self.deck_view.set_deck(deck)
        self.logger.info(f"Loaded deck: {deck.name}")