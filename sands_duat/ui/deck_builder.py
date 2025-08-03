"""
Deck Builder Screen

Enhanced card collection management interface for building and customizing decks.
Integrates with player collection system and provides comprehensive deck building tools.
"""

import pygame
import logging
from typing import List, Dict, Optional, Any, Tuple
from .base import UIScreen, UIComponent
from ..core.cards import Card, Deck, CardRarity, CardType
from ..core.player_collection import PlayerCollection, CardRewardSystem
from .menu_screen import MenuButton
from .theme import get_theme


class CardDisplay(UIComponent):
    """Enhanced card display component for deck builder with drag-and-drop support."""
    
    def __init__(self, x: int, y: int, width: int, height: int, card: Card, 
                 owned_count: int = 0, is_favorite: bool = False, draggable: bool = True):
        super().__init__(x, y, width, height)
        self.card = card
        self.owned_count = owned_count
        self.is_favorite = is_favorite
        self.hovered = False
        self.selected = False
        self.draggable = draggable
        
        # Drag and drop state
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.original_pos = (x, y)
        
        # Enable Egyptian feedback effects for cards
        self.enable_egyptian_feedback('all')
        
        # Special effects for rare cards
        if hasattr(card, 'rarity'):
            if card.rarity in ['LEGENDARY', 'EPIC']:
                self.egyptian_feedback['mystical_particles'] = True
                self.egyptian_feedback['glow_color'] = (255, 215, 0) if card.rarity == 'LEGENDARY' else (147, 112, 219)  # Gold for legendary, purple for epic
    
    def update(self, delta_time: float) -> None:
        """Update card display."""
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle card interaction and drag events."""
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle drag and drop
        if self.draggable:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.being_dragged = True
                    self.drag_offset_x = event.pos[0] - self.rect.x
                    self.drag_offset_y = event.pos[1] - self.rect.y
                    self.original_pos = (self.rect.x, self.rect.y)
                    self._trigger_event("card_drag_start", {"card": self.card, "component": self})
                    return True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.being_dragged:
                    self.being_dragged = False
                    self._trigger_event("card_drag_end", {
                        "card": self.card, 
                        "component": self,
                        "drop_pos": mouse_pos,
                        "original_pos": self.original_pos
                    })
                    return True
            
            elif event.type == pygame.MOUSEMOTION:
                if self.being_dragged:
                    self.rect.x = mouse_pos[0] - self.drag_offset_x
                    self.rect.y = mouse_pos[1] - self.drag_offset_y
                    self._trigger_event("card_dragging", {"card": self.card, "component": self})
                    return True
        
        # Handle selection for non-draggable cards or when not dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.being_dragged:
            if self.rect.collidepoint(event.pos):
                if not self.draggable:  # Only toggle selection for non-draggable cards
                    self.selected = not self.selected
                    self._trigger_event("card_selected", {"card": self.card, "selected": self.selected})
                super().handle_event(event)
                return True
        
        # Let base class handle other events (hover, etc.)
        return super().handle_event(event)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enhanced card with collection information."""
        if not self.visible:
            return
        
        # Card background with rarity color
        rarity_colors = {
            CardRarity.COMMON: (60, 60, 60),
            CardRarity.UNCOMMON: (30, 70, 30),
            CardRarity.RARE: (30, 30, 90),
            CardRarity.LEGENDARY: (90, 60, 30)
        }
        
        bg_color = rarity_colors.get(self.card.rarity, (60, 45, 30))
        border_color = (139, 117, 93)
        
        # Highlight if hovered, selected, or being dragged
        if self.hovered:
            bg_color = tuple(min(255, c + 20) for c in bg_color)
        if self.selected:
            border_color = (255, 215, 0)
        if self.being_dragged:
            bg_color = tuple(min(255, c + 40) for c in bg_color)
            border_color = (255, 100, 100)  # Red tint while dragging
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3 if self.selected else 2)
        
        # Responsive font sizing based on card size
        name_font_size = max(12, min(20, self.rect.width // 6))
        cost_font_size = max(16, min(28, self.rect.width // 4))
        count_font_size = max(10, min(16, self.rect.width // 8))
        
        # Card name (truncated if needed)
        font = pygame.font.Font(None, name_font_size)
        max_chars = max(8, self.rect.width // 8)
        display_name = self.card.name[:max_chars]
        text = font.render(display_name, True, (255, 248, 220))
        surface.blit(text, (self.rect.x + 3, self.rect.y + 3))
        
        # Sand cost
        cost_font = pygame.font.Font(None, cost_font_size)
        cost_text = cost_font.render(str(self.card.sand_cost), True, (255, 215, 0))
        cost_y = self.rect.y + self.rect.height - cost_font_size - 3
        surface.blit(cost_text, (self.rect.x + 3, cost_y))
        
        # Owned count
        if self.owned_count > 0:
            count_font = pygame.font.Font(None, count_font_size)
            count_text = count_font.render(f"x{self.owned_count}", True, (150, 255, 150))
            count_width = count_text.get_width()
            surface.blit(count_text, (self.rect.x + self.rect.width - count_width - 3, self.rect.y + 3))
        
        # Favorite indicator
        if self.is_favorite:
            star_radius = max(3, self.rect.width // 15)
            star_center = (self.rect.x + self.rect.width - star_radius - 3, 
                          self.rect.y + self.rect.height - star_radius - 3)
            pygame.draw.circle(surface, (255, 215, 0), star_center, star_radius)
        
        # Type indicator
        type_colors = {
            CardType.ATTACK: (200, 100, 100),
            CardType.SKILL: (100, 200, 100),
            CardType.POWER: (100, 100, 200),
            CardType.CURSE: (150, 50, 150)
        }
        type_color = type_colors.get(self.card.card_type, (128, 128, 128))
        type_height = max(4, self.rect.height // 20)
        type_width = min(self.rect.width // 3, 25)
        type_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.rect.height - type_height - 2, 
                               type_width, type_height)
        pygame.draw.rect(surface, type_color, type_rect)


class CardCollection(UIComponent):
    """
    Enhanced card collection display with player collection integration.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, player_collection: PlayerCollection, 
                 cards_per_row: int = 6, card_width: int = 90, card_height: int = 120):
        super().__init__(x, y, width, height)
        self.player_collection = player_collection
        self.logger = logging.getLogger(__name__)
        
        self.all_cards: List[Card] = []
        self.filtered_cards: List[Card] = []
        self.card_displays: List[CardDisplay] = []
        self.selected_cards: List[str] = []  # Card IDs
        
        # Layout settings - now configurable for different display sizes
        self.cards_per_row = cards_per_row
        self.card_width = card_width
        self.card_height = card_height
        self.card_spacing = max(8, width // 200)  # Adaptive spacing based on width
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Filters
        self.rarity_filter: Optional[CardRarity] = None
        self.type_filter: Optional[CardType] = None
        self.cost_filter: Optional[int] = None
        self.cost_min: Optional[int] = None
        self.cost_max: Optional[int] = None
        self.owned_only = True
        self.favorites_only = False
        self.show_new = False
        self.search_text = ""
        
        # Initialize with player's collection
        self.refresh_collection()
    
    def refresh_collection(self) -> None:
        """Refresh collection display from player collection."""
        # Get filtered cards based on current criteria
        self.filtered_cards = self.player_collection.filter_cards(
            rarity=self.rarity_filter,
            card_type=self.type_filter,
            cost_min=self.cost_min,
            cost_max=self.cost_max,
            owned_only=self.owned_only,
            favorites_only=self.favorites_only
        )
        
        # Add recently discovered cards if show_new is enabled
        if self.show_new:
            recent_cards = self.player_collection.get_recently_discovered()
            for card_id in recent_cards:
                from core.cards import CardLibrary
                card_library = CardLibrary()
                card = card_library.get_card(card_id)
                if card and card not in self.filtered_cards:
                    self.filtered_cards.insert(0, card)
        
        self._create_card_displays()
        self.logger.debug(f"Refreshed collection with {len(self.filtered_cards)} cards")
    
    def _create_card_displays(self) -> None:
        """Create card display components for filtered cards."""
        self.card_displays.clear()
        
        for i, card in enumerate(self.filtered_cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.rect.x + col * (self.card_width + self.card_spacing) + self.card_spacing
            y = self.rect.y + row * (self.card_height + self.card_spacing) + self.card_spacing
            
            owned_count = self.player_collection.get_card_count(card.id)
            is_favorite = self.player_collection.is_favorite(card.id)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, 
                                     card, owned_count, is_favorite, draggable=True)
            card_display.add_event_handler("card_selected", self._on_card_selected)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            card_display.add_event_handler("card_dragging", self._on_card_dragging)
            self.card_displays.append(card_display)
        
        # Calculate scrolling bounds
        total_rows = (len(self.filtered_cards) + self.cards_per_row - 1) // self.cards_per_row
        total_height = total_rows * (self.card_height + self.card_spacing) + self.card_spacing
        self.max_scroll = max(0, total_height - self.rect.height)
    
    def _on_card_selected(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card selection."""
        card = event_data["card"]
        selected = event_data["selected"]
        
        if selected:
            if card.id not in self.selected_cards:
                self.selected_cards.append(card.id)
        else:
            if card.id in self.selected_cards:
                self.selected_cards.remove(card.id)
        
        # Trigger parent event
        self._trigger_event("card_selection_changed", {
            "card": card,
            "selected": selected,
            "selected_cards": self.selected_cards[:]
        })
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle start of card drag operation."""
        card = event_data["card"]
        self._trigger_event("card_drag_start", {"card": card, "component": component})
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle end of card drag operation."""
        card = event_data["card"]
        drop_pos = event_data["drop_pos"]
        original_pos = event_data["original_pos"]
        
        # Reset card position to original if not successfully dropped
        component.rect.x, component.rect.y = original_pos
        
        # Trigger parent event for deck builder to handle
        self._trigger_event("card_drag_end", {
            "card": card, 
            "component": component,
            "drop_pos": drop_pos,
            "original_pos": original_pos
        })
    
    def _on_card_dragging(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card being dragged."""
        card = event_data["card"]
        self._trigger_event("card_dragging", {"card": card, "component": component})
    
    def set_filters(self, **filters) -> None:
        """Set multiple filters at once."""
        if "rarity" in filters:
            self.rarity_filter = filters["rarity"]
        if "type" in filters:
            self.type_filter = filters["type"]
        if "cost_min" in filters:
            self.cost_min = filters["cost_min"]
        if "cost_max" in filters:
            self.cost_max = filters["cost_max"]
        if "owned_only" in filters:
            self.owned_only = filters["owned_only"]
        if "favorites_only" in filters:
            self.favorites_only = filters["favorites_only"]
        if "show_new" in filters:
            self.show_new = filters["show_new"]
        
        self.refresh_collection()
    
    def toggle_favorite(self, card_id: str) -> None:
        """Toggle favorite status of a card."""
        self.player_collection.toggle_favorite(card_id)
        self.refresh_collection()
    
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
        
        # Handle card interactions by directly calling card display event handlers
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Adjust click position for scroll offset
            adjusted_pos = (event.pos[0], event.pos[1] + self.scroll_offset)
            
            for card_display in self.card_displays:
                if card_display.rect.collidepoint(adjusted_pos):
                    # Directly toggle card selection and trigger events
                    card_display.selected = not card_display.selected
                    
                    # Trigger the card selection event that CardCollection is listening for
                    self._on_card_selected(card_display, {
                        "card": card_display.card,
                        "selected": card_display.selected
                    })
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
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, card, draggable=True)
            card_display.add_event_handler("card_selected", self._on_card_selected)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            card_display.add_event_handler("card_dragging", self._on_card_dragging)
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
    Displays the current deck being built with drop zone functionality.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.deck: Optional[Deck] = None
        self.card_displays: List[CardDisplay] = []
        
        # Layout settings - responsive based on available width
        self.cards_per_row = max(6, width // 120)  # More cards per row for horizontal layout
        self.card_width = min(100, (width - 40) // self.cards_per_row - 10)  # Responsive card width
        self.card_height = int(self.card_width * 1.3)  # Maintain aspect ratio
        self.card_spacing = max(8, width // 100)  # Adaptive spacing
        
        # Drop zone visual feedback
        self.is_drop_target = False
        self.drop_highlight = False
    
    def update(self, delta_time: float) -> None:
        """Update deck view."""
        for card_display in self.card_displays:
            card_display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the deck view."""
        if not self.visible:
            return
        
        # Draw background with drop zone highlighting
        bg_color = (25, 20, 15)
        border_color = self.border_color
        
        if self.drop_highlight:
            bg_color = (40, 35, 25)  # Lighter background when hovering with card
            border_color = (255, 215, 0)  # Gold border for drop zone
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3 if self.drop_highlight else 2)
        
        # Draw title with responsive font size
        title_font_size = max(16, min(28, self.rect.width // 20))
        font = pygame.font.Font(None, title_font_size)
        title = "Deck"
        if self.deck:
            title += f" ({len(self.deck.cards)}/30)"  # Assuming 30 card limit
        
        title_surface = font.render(title, True, self.text_color)
        title_rect = title_surface.get_rect()
        title_rect.left = self.rect.left + 10
        title_rect.top = self.rect.top + 5
        surface.blit(title_surface, title_rect)
        
        # Draw drop zone hint if deck is empty
        if not self.deck or len(self.deck.cards) == 0:
            hint_font_size = max(14, min(20, self.rect.width // 30))
            hint_font = pygame.font.Font(None, hint_font_size)
            hint_text = "Drag cards here to build your deck"
            hint_surface = hint_font.render(hint_text, True, (150, 150, 100))
            hint_rect = hint_surface.get_rect()
            hint_rect.center = self.rect.center
            surface.blit(hint_surface, hint_rect)
        
        # Render cards
        for card_display in self.card_displays:
            card_display.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for deck interaction and drop zone."""
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle card removal (right-click on deck cards)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            for i, card_display in enumerate(self.card_displays):
                if card_display.rect.collidepoint(event.pos):
                    self._remove_card(i)
                    return True
        
        # Handle drag events for drop zone highlighting
        if event.type == pygame.MOUSEMOTION:
            # Check if we're in the drop zone
            in_drop_zone = self.rect.collidepoint(mouse_pos)
            if in_drop_zone != self.drop_highlight:
                self.drop_highlight = in_drop_zone
        
        # Let card displays handle their own events
        for card_display in self.card_displays:
            if card_display.handle_event(event):
                return True
        
        return super().handle_event(event)
    
    def set_deck(self, deck: Deck) -> None:
        """Set the deck to display."""
        self.deck = deck
        self._update_layout()
    
    def add_card(self, card: Card) -> bool:
        """Add a card to the deck."""
        if self.deck and len(self.deck.cards) < 30:  # Deck size limit
            # Create a copy of the card for the deck to avoid issues
            deck_card = card.copy(deep=True) if hasattr(card, 'copy') else card
            self.deck.add_card(deck_card)
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
        
        start_y = self.rect.top + 35  # Leave space for title
        
        for i, card in enumerate(self.deck.cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.rect.x + 15 + col * (self.card_width + self.card_spacing)
            y = start_y + row * (self.card_height + self.card_spacing)
            
            # Deck cards are not draggable, only removable via right-click
            card_display = CardDisplay(x, y, self.card_width, self.card_height, card, draggable=False)
            card_display.add_event_handler("card_selected", self._on_deck_card_selected)
            self.card_displays.append(card_display)
    
    def _remove_card(self, index: int) -> None:
        """Remove a card from the deck."""
        removed_card = self.remove_card_at(index)
        if removed_card:
            self._trigger_event("card_removed", {"card": removed_card, "index": index})
    
    def _on_deck_card_selected(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle selection of cards in the deck (for info display)."""
        card = event_data.get("card")
        if card:
            self._trigger_event("deck_card_info", {"card": card})
    
    def accept_dropped_card(self, card: Card) -> bool:
        """Accept a card dropped into this deck view."""
        if self.add_card(card):
            self._trigger_event("card_added_to_deck", {"card": card})
            return True
        return False
    
    def is_valid_drop_zone(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is a valid drop zone for cards."""
        return self.rect.collidepoint(pos)


class FilterPanel(UIComponent):
    """
    Panel with filter controls for the card collection.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.selected_rarity: Optional[CardRarity] = None
        self.selected_cost: Optional[int] = None
        
        # Responsive font sizing based on panel width
        self.font_size = max(16, min(24, width // 12))
        self.line_height = self.font_size + 4
        
    def update(self, delta_time: float) -> None:
        """Update filter panel."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the filter panel with responsive sizing."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, (35, 30, 25), self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Use responsive font sizing
        font = pygame.font.Font(None, self.font_size)
        small_font = pygame.font.Font(None, max(14, self.font_size - 4))
        
        padding = max(5, self.rect.width // 30)
        y_offset = self.rect.top + padding
        
        # Title
        title_text = font.render("Filters", True, (255, 215, 0))
        surface.blit(title_text, (self.rect.x + padding, y_offset))
        y_offset += self.line_height + padding
        
        # Rarity filters
        rarity_text = small_font.render("Rarity:", True, self.text_color)
        surface.blit(rarity_text, (self.rect.x + padding, y_offset))
        y_offset += self.line_height
        
        for rarity in CardRarity:
            color = self.text_color if self.selected_rarity != rarity else (255, 215, 0)
            rarity_label = small_font.render(rarity.value.title(), True, color)
            surface.blit(rarity_label, (self.rect.x + padding * 2, y_offset))
            y_offset += self.line_height - 2
        
        y_offset += padding
        
        # Cost filters
        cost_text = small_font.render("Cost:", True, self.text_color)
        surface.blit(cost_text, (self.rect.x + padding, y_offset))
        y_offset += self.line_height
        
        for cost in range(7):  # 0-6 sand cost
            color = self.text_color if self.selected_cost != cost else (255, 215, 0)
            cost_label = small_font.render(str(cost), True, color)
            surface.blit(cost_label, (self.rect.x + padding * 2, y_offset))
            y_offset += self.line_height - 2
    
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
        """Set up all UI components using responsive theme zones."""
        try:
            theme = get_theme()
            
            # Get layout zones for current display mode
            back_zone = theme.get_zone('deck_back_button')
            filter_zone = theme.get_zone('deck_filter_panel')
            collection_zone = theme.get_zone('deck_collection')
            deck_zone = theme.get_zone('deck_view')
            
            # Back button using theme zone
            back_button = MenuButton(
                back_zone.x, back_zone.y, back_zone.width, back_zone.height,
                "<- Back to Progression",
                self._back_to_progression
            )
            self.add_component(back_button)
            
            # Filter panel using theme zone
            self.filter_panel = FilterPanel(
                filter_zone.x, filter_zone.y, filter_zone.width, filter_zone.height
            )
            self.add_component(self.filter_panel)
            
            # Create temporary player collection for testing
            # TODO: Replace with actual player collection system
            temp_player_collection = PlayerCollection()
            
            # Calculate optimal card layout based on collection zone size
            # For ultrawide: 2200px width allows for ~15 cards per row at 130px width + spacing
            optimal_card_width = min(130, collection_zone.width // 15)
            optimal_card_height = int(optimal_card_width * 1.4)  # Maintain aspect ratio
            cards_per_row = max(8, collection_zone.width // (optimal_card_width + 15))
            
            # Card collection using theme zone with responsive sizing
            self.card_collection = CardCollection(
                collection_zone.x, collection_zone.y, 
                collection_zone.width, collection_zone.height,
                temp_player_collection,
                cards_per_row=cards_per_row,
                card_width=optimal_card_width,
                card_height=optimal_card_height
            )
            self.card_collection.add_event_handler("card_selection_changed", self._on_card_selected)
            self.card_collection.add_event_handler("card_drag_start", self._on_card_drag_start)
            self.card_collection.add_event_handler("card_drag_end", self._on_card_drag_end)
            self.card_collection.add_event_handler("card_dragging", self._on_card_dragging)
            self.add_component(self.card_collection)
            
            # Deck view using theme zone
            self.deck_view = DeckView(
                deck_zone.x, deck_zone.y, deck_zone.width, deck_zone.height
            )
            self.deck_view.add_event_handler("card_removed", self._on_card_removed)
            self.deck_view.add_event_handler("card_added_to_deck", self._on_card_added_to_deck)
            self.deck_view.add_event_handler("deck_card_info", self._on_deck_card_info)
            self.add_component(self.deck_view)
            
            # Initialize with empty deck
            self.current_deck = Deck(name="Custom Deck")
            self.deck_view.set_deck(self.current_deck)
            
            self.logger.info(f"Deck builder UI setup for {theme.display.display_mode.value} mode")
            
        except Exception as e:
            self.logger.error(f"Failed to setup UI with theme zones, using fallback: {e}")
            # Fallback to original hardcoded layout if theme fails
            self._setup_fallback_ui()
    
    def _setup_fallback_ui(self) -> None:
        """Fallback UI setup if theme system fails."""
        # Back button (top-left corner) - Egyptian themed
        back_button = MenuButton(
            20, 20, 150, 40,
            "<- Back to Progression",
            self._back_to_progression
        )
        self.add_component(back_button)
        
        # Filter panel (left side)
        self.filter_panel = FilterPanel(20, 80, 150, 500)
        self.add_component(self.filter_panel)
        
        # Create temporary player collection for testing
        temp_player_collection = PlayerCollection()
        
        # Card collection (center)
        self.card_collection = CardCollection(180, 80, 400, 500, temp_player_collection)
        self.card_collection.add_event_handler("card_selection_changed", self._on_card_selected)
        self.card_collection.add_event_handler("card_drag_start", self._on_card_drag_start)
        self.card_collection.add_event_handler("card_drag_end", self._on_card_drag_end)
        self.card_collection.add_event_handler("card_dragging", self._on_card_dragging)
        self.add_component(self.card_collection)
        
        # Deck view (right side)
        self.deck_view = DeckView(590, 80, 200, 500)
        self.deck_view.add_event_handler("card_removed", self._on_card_removed)
        self.deck_view.add_event_handler("card_added_to_deck", self._on_card_added_to_deck)
        self.deck_view.add_event_handler("deck_card_info", self._on_deck_card_info)
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
        """Handle card selection from collection - now for info display only."""
        card = event_data.get("card")
        selected = event_data.get("selected", False)
        
        # Card selection is now primarily for information display
        # Adding to deck is handled via drag-and-drop
        self.logger.debug(f"Card {card.name if card else 'unknown'} {'selected' if selected else 'deselected'} for info display")
    
    def _on_card_removed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card removal from deck."""
        card = event_data.get("card")
        if card:
            self.logger.info(f"Removed card from deck: {card.name}")
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle start of card drag from collection."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Started dragging card: {card.name}")
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle end of card drag - check if dropped on deck."""
        card = event_data.get("card")
        drop_pos = event_data.get("drop_pos")
        card_component = event_data.get("component")
        
        if card and drop_pos and self.deck_view:
            # Check if card was dropped on the deck view
            if self.deck_view.is_valid_drop_zone(drop_pos):
                # Try to add card to deck
                if self.deck_view.accept_dropped_card(card):
                    self.logger.info(f"Successfully added {card.name} to deck via drag-and-drop")
                    # Keep the card in its original position since it's been added
                else:
                    self.logger.warning(f"Failed to add {card.name} to deck - deck may be full")
            else:
                self.logger.debug(f"Card {card.name} dropped outside deck area")
    
    def _on_card_dragging(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card being dragged - update drop zone highlights."""
        card = event_data.get("card")
        if card and self.deck_view:
            mouse_pos = pygame.mouse.get_pos()
            self.deck_view.drop_highlight = self.deck_view.rect.collidepoint(mouse_pos)
    
    def _on_card_added_to_deck(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card successfully added to deck."""
        card = event_data.get("card")
        if card:
            self.logger.info(f"Card {card.name} added to deck")
    
    def _on_deck_card_info(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle deck card selection for info display."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Viewing info for deck card: {card.name}")
    
    def _back_to_progression(self) -> None:
        """Return to progression screen."""
        self.logger.info("Returning to progression screen from deck builder")
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("progression", "slide_right")
        else:
            # Fallback - just log for now since UIScreen doesn't have _trigger_event
            self.logger.warning("No UI manager available for screen transition")
    
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