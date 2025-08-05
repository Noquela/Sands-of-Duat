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
from .animation_system import AnimationManager, EgyptianAnimationRenderer

# Import parallax and atmospheric systems
try:
    from sands_duat.graphics.interactive_parallax_system import (
        get_interactive_parallax_system, InteractionType, trigger_ui_interaction, handle_mouse_parallax
    )
    from sands_duat.graphics.egyptian_atmospheric_effects import get_atmospheric_manager
    PARALLAX_AVAILABLE = True
except ImportError:
    PARALLAX_AVAILABLE = False


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
        
        # Double click detection
        self.last_click_time = 0
        self.double_click_threshold = 0.3  # 300ms for double click
        
        # Egyptian animation system
        self.animation_manager = AnimationManager()
        self.egyptian_renderer = EgyptianAnimationRenderer()
        self.animation_state = {
            'ankh_glow': 0.0,
            'scarab_rotation': 0.0,
            'lotus_bloom': 1.0,
            'egyptian_pulse': 1.0
        }
        
        # Accessibility features
        self.accessibility = {
            'role': 'button',
            'label': f"{card.name}",
            'keyboard_accessible': True,
            'screen_reader_text': f"Card: {card.name}",
            'high_contrast_mode': False,
            'focus_indicator': False
        }
        self.keyboard_focused = False
        self.high_contrast_mode = False
        
        # Enable Egyptian feedback effects for cards
        self.enable_egyptian_feedback('all')
        
        # Special effects for rare cards
        if hasattr(card, 'rarity'):
            if card.rarity in [CardRarity.LEGENDARY, CardRarity.RARE]:
                # Start continuous scarab rotation for rare cards
                self.animation_manager.scarab_rare_rotation(f"card_{id(self)}", duration=3.0)
                self.egyptian_feedback['mystical_particles'] = True
                self.egyptian_feedback['glow_color'] = (255, 215, 0) if card.rarity == CardRarity.LEGENDARY else (147, 112, 219)
    
    def update(self, delta_time: float) -> None:
        """Update card display with Egyptian animations."""
        # Update animations
        animation_values = self.animation_manager.update(delta_time)
        card_id = f"card_{id(self)}"
        
        if card_id in animation_values:
            for anim_type, value in animation_values[card_id].items():
                if anim_type.value == 'ankh_glow':
                    self.animation_state['ankh_glow'] = value
                elif anim_type.value == 'scarab_spin':
                    self.animation_state['scarab_rotation'] = value
                elif anim_type.value == 'lotus_bloom':
                    self.animation_state['lotus_bloom'] = value
                elif anim_type.value == 'egyptian_pulse':
                    self.animation_state['egyptian_pulse'] = value
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle card interaction with double-click to add to deck."""
        if not self.visible or not self.enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                import time
                current_time = time.time()
                
                # Check for double click
                if current_time - self.last_click_time <= self.double_click_threshold:
                    # Double click detected - add card to deck
                    self._trigger_event("card_double_click", {"card": self.card, "component": self})
                    self.last_click_time = 0  # Reset to prevent triple clicks
                    return True
                else:
                    # Single click - start drag or selection
                    self.last_click_time = current_time
                    
                    if self.draggable:
                        self.being_dragged = True
                        self.drag_offset_x = event.pos[0] - self.rect.x
                        self.drag_offset_y = event.pos[1] - self.rect.y
                        self.original_pos = (self.rect.x, self.rect.y)
                        self._trigger_event("card_drag_start", {"card": self.card, "component": self})
                    else:
                        self.selected = not self.selected
                        self._trigger_event("card_selected", {"card": self.card, "selected": self.selected})
                    
                    super().handle_event(event)
                    return True
        
        # Handle drag and drop (only if already dragging)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.being_dragged:
                self.being_dragged = False
                self._trigger_event("card_drag_end", {
                    "card": self.card, 
                    "component": self,
                    "drop_pos": event.pos,
                    "original_pos": self.original_pos
                })
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.being_dragged:
                self.rect.x = event.pos[0] - self.drag_offset_x
                self.rect.y = event.pos[1] - self.drag_offset_y
                self._trigger_event("card_dragging", {"card": self.card, "component": self})
                return True
        
        # Handle hover events for lotus bloom animation
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            
            # Trigger lotus bloom on hover start
            if self.hovered and not was_hovered:
                self.animation_manager.lotus_hover_bloom(f"card_{id(self)}")
            # Reset bloom on hover end
            elif not self.hovered and was_hovered:
                self.animation_state['lotus_bloom'] = 1.0
        
        # Trigger ankh glow on selection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and not self.being_dragged:
                self.animation_manager.ankh_selection(f"card_{id(self)}")
        
        # Let base class handle other events (hover, etc.)
        return super().handle_event(event)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enhanced card with collection information."""
        if not self.visible:
            return
        
        # Get theme-based card styling
        theme = get_theme()
        card_style = theme.create_card_style(self.card.rarity, self.card.card_type)
        
        bg_color = card_style['background_color']
        border_color = card_style['border_color']
        
        # Highlight if hovered, selected, or being dragged with theme colors
        if self.hovered:
            bg_color = card_style['hover_color']
        if self.selected:
            border_color = card_style['selected_color']
            # Add selection glow background
            selection_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, 
                                       self.rect.width + 4, self.rect.height + 4)
            pygame.draw.rect(surface, theme.colors.GOLD, selection_rect)
        if self.being_dragged:
            bg_color = tuple(min(255, c + 30) for c in bg_color)
            border_color = theme.colors.COPPER  # Copper tint while dragging
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3 if self.selected else 2)
        
        # AI Card Artwork (main focus of the card)
        art_rect = pygame.Rect(
            self.rect.x + 3,
            self.rect.y + 20,  # Leave space for name
            self.rect.width - 6,
            self.rect.height - 50  # Leave space for name and cost
        )
        self._draw_card_artwork(surface, art_rect)
        
        # Responsive font sizing based on card size
        name_font_size = max(12, min(20, self.rect.width // 6))
        cost_font_size = max(16, min(28, self.rect.width // 4))
        count_font_size = max(10, min(16, self.rect.width // 8))
        
        # Card name with theme text color (on top)
        font = pygame.font.Font(None, name_font_size)
        max_chars = max(8, self.rect.width // 8)
        display_name = self.card.name[:max_chars]
        text = font.render(display_name, True, card_style['text_color'])
        # Add text background for better readability
        text_bg = pygame.Rect(self.rect.x, self.rect.y, text.get_width() + 6, text.get_height() + 6)
        pygame.draw.rect(surface, (0, 0, 0, 180), text_bg)
        surface.blit(text, (self.rect.x + 3, self.rect.y + 3))
        
        # Sand cost with theme cost color
        cost_font = pygame.font.Font(None, cost_font_size)
        cost_text = cost_font.render(str(self.card.sand_cost), True, card_style['cost_color'])
        cost_y = self.rect.y + self.rect.height - cost_font_size - 3
        surface.blit(cost_text, (self.rect.x + 3, cost_y))
        
        # Owned count with theme colors
        if self.owned_count > 0:
            count_font = pygame.font.Font(None, count_font_size)
            count_text = count_font.render(f"x{self.owned_count}", True, theme.colors.GOLD)
            count_width = count_text.get_width()
            surface.blit(count_text, (self.rect.x + self.rect.width - count_width - 3, self.rect.y + 3))
        
        # Favorite indicator with theme gold
        if self.is_favorite:
            star_radius = max(3, self.rect.width // 15)
            star_center = (self.rect.x + self.rect.width - star_radius - 3, 
                          self.rect.y + self.rect.height - star_radius - 3)
            pygame.draw.circle(surface, theme.colors.GOLD, star_center, star_radius)
        
        # Type indicator with theme type colors
        type_color = card_style['type_accent']
        type_height = max(4, self.rect.height // 20)
        type_width = min(self.rect.width // 3, 25)
        type_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.rect.height - type_height - 2, 
                               type_width, type_height)
        pygame.draw.rect(surface, type_color, type_rect)
        
        # Render Egyptian animations
        self._render_egyptian_effects(surface)
    
    def _draw_card_artwork(self, surface: pygame.Surface, art_rect: pygame.Rect) -> None:
        """Draw AI-generated card artwork."""
        try:
            from ..graphics.card_art_loader import load_card_art
            
            artwork = load_card_art(self.card.name, (art_rect.width, art_rect.height))
            if artwork:
                surface.blit(artwork, art_rect)
                
                # Add Egyptian-style border
                pygame.draw.rect(surface, (139, 117, 93), art_rect, 2)
                
                # Success indicator
                font = pygame.font.Font(None, 10)
                debug_text = font.render("AI", True, (0, 255, 0))
                surface.blit(debug_text, (art_rect.x + 2, art_rect.y + 2))
                
            else:
                # Enhanced fallback with card name
                pygame.draw.rect(surface, (80, 60, 40), art_rect)
                pygame.draw.rect(surface, (139, 117, 93), art_rect, 2)
                
                # Card name display
                font = pygame.font.Font(None, 12)
                name_lines = self.card.name.split(' ')
                for i, line in enumerate(name_lines[:2]):  # Max 2 lines for deck builder
                    text = font.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(art_rect.centerx, art_rect.centery + i * 12 - 6))
                    surface.blit(text, text_rect)
                
                # Type indicator
                type_font = pygame.font.Font(None, 10)
                type_text = type_font.render(self.card.card_type.value[:4], True, (200, 200, 200))
                type_rect = type_text.get_rect(center=(art_rect.centerx, art_rect.bottom - 8))
                surface.blit(type_text, type_rect)
                
        except Exception as e:
            # Error fallback with more info
            pygame.draw.rect(surface, (60, 30, 30), art_rect)
            pygame.draw.rect(surface, (120, 60, 60), art_rect, 2)
            
            font = pygame.font.Font(None, 12)
            error_text = font.render("Error", True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(art_rect.centerx, art_rect.centery - 8))
            surface.blit(error_text, error_rect)
            
            card_text = font.render(self.card.name[:10], True, (255, 255, 255))
            card_rect = card_text.get_rect(center=(art_rect.centerx, art_rect.centery + 8))
            surface.blit(card_text, card_rect)
    
    def _render_egyptian_effects(self, surface: pygame.Surface) -> None:
        """Render Egyptian-themed visual effects on the card."""
        # Ankh glow effect for selection
        if self.animation_state['ankh_glow'] > 0.1:
            self.egyptian_renderer.render_ankh_glow(
                surface, self.rect, self.animation_state['ankh_glow']
            )
        
        # Scarab rotation for rare cards
        if self.card.rarity in [CardRarity.RARE, CardRarity.LEGENDARY] and self.animation_state['scarab_rotation'] > 0:
            self.egyptian_renderer.render_scarab_rotation(
                surface, self.rect, self.animation_state['scarab_rotation']
            )
        
        # Lotus bloom for hover effects
        if self.hovered and self.animation_state['lotus_bloom'] != 1.0:
            self.egyptian_renderer.render_lotus_bloom(
                surface, self.rect, self.animation_state['lotus_bloom']
            )
        
        # Egyptian pulse for legendary cards
        if self.card.rarity == CardRarity.LEGENDARY and self.animation_state['egyptian_pulse'] != 1.0:
            self.egyptian_renderer.render_egyptian_pulse(
                surface, self.rect, self.animation_state['egyptian_pulse'] - 1.0
            )


class CardCollection(UIComponent):
    """
    Enhanced card collection display with player collection integration.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, player_collection: PlayerCollection, 
                 cards_per_row: int = 3, card_width: int = 220, card_height: int = 300):
        super().__init__(x, y, width, height)
        self.player_collection = player_collection
        self.logger = logging.getLogger(__name__)
        
        self.all_cards: List[Card] = []
        self.filtered_cards: List[Card] = []
        self.card_displays: List[CardDisplay] = []
        self.selected_cards: List[str] = []  # Card IDs
        
        # Improved layout settings - better responsive design
        self.cards_per_row = cards_per_row
        self.card_width = card_width
        self.card_height = card_height
        # Better spacing calculation with minimum and maximum bounds
        self.card_spacing = min(20, max(10, width // 120))  # More consistent spacing
        self.margin_x = max(15, width // 80)  # Side margins
        self.margin_y = max(10, height // 60)  # Top/bottom margins
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
        
        # Performance optimizations
        self.lazy_loading_enabled = True
        self.visible_card_cache: Dict[int, CardDisplay] = {}
        self.last_visible_range = (0, 0)
        
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
        
        # Apply search text filter
        if self.search_text:
            search_lower = self.search_text.lower()
            self.filtered_cards = [
                card for card in self.filtered_cards
                if search_lower in card.name.lower() or search_lower in card.description.lower()
            ]
        
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
    
    def remove_card_from_collection_display(self, card: Card) -> bool:
        """Remove a card from the collection display after it's been moved to deck."""
        # Remove from filtered cards
        if card in self.filtered_cards:
            self.filtered_cards.remove(card)
            
        # Remove the corresponding card display
        for i, card_display in enumerate(self.card_displays):
            if card_display.card.id == card.id:
                self.card_displays.pop(i)
                break
        
        # Update layout to fill the gap
        self._create_card_displays()
        self.logger.debug(f"Removed {card.name} from collection display")
        return True
    
    def _create_card_displays(self) -> None:
        """Create card display components for filtered cards with lazy loading optimization."""
        if self.lazy_loading_enabled:
            # Only create displays for cards that might be visible
            self._create_visible_card_displays()
        else:
            # Create all displays (fallback for compatibility)
            self._create_all_card_displays()
        
        # Calculate scrolling bounds with proper margins
        total_rows = (len(self.filtered_cards) + self.cards_per_row - 1) // self.cards_per_row
        total_height = total_rows * (self.card_height + self.card_spacing) + self.margin_y * 2
        self.max_scroll = max(0, total_height - self.rect.height)
    
    def _create_visible_card_displays(self) -> None:
        """Create card displays only for currently visible cards (lazy loading)."""
        self.card_displays.clear()
        
        if not self.filtered_cards:
            return
        
        # Calculate visible range based on scroll position
        visible_start_row = max(0, (self.scroll_offset - self.card_height) // (self.card_height + self.card_spacing))
        visible_end_row = min(
            (len(self.filtered_cards) + self.cards_per_row - 1) // self.cards_per_row,
            (self.scroll_offset + self.rect.height + self.card_height) // (self.card_height + self.card_spacing) + 1
        )
        
        visible_start_index = visible_start_row * self.cards_per_row
        visible_end_index = min(len(self.filtered_cards), (visible_end_row + 1) * self.cards_per_row)
        
        # Cache visible range for performance tracking
        self.last_visible_range = (visible_start_index, visible_end_index)
        
        for i in range(visible_start_index, visible_end_index):
            if i >= len(self.filtered_cards):
                break
                
            card = self.filtered_cards[i]
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            # Improved card positioning with proper margins
            x = self.rect.x + self.margin_x + col * (self.card_width + self.card_spacing)
            y = self.rect.y + self.margin_y + row * (self.card_height + self.card_spacing)
            
            owned_count = self.player_collection.get_card_count(card.id)
            is_favorite = self.player_collection.is_favorite(card.id)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, 
                                     card, owned_count, is_favorite, draggable=True)
            card_display.add_event_handler("card_selected", self._on_card_selected)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            card_display.add_event_handler("card_dragging", self._on_card_dragging)
            card_display.add_event_handler("card_double_click", self._on_card_double_click)
            
            # Add accessibility attributes
            rarity_text = card.rarity.value if hasattr(card.rarity, 'value') else str(card.rarity)
            type_text = card.card_type.value if hasattr(card.card_type, 'value') else str(card.card_type)
            favorite_text = " (favorite)" if is_favorite else ""
            
            card_display.accessibility = {
                'role': 'button',
                'label': f"{card.name}, {rarity_text} {type_text}, {card.sand_cost} sand cost, owned: {owned_count}{favorite_text}",
                'keyboard_accessible': True,
                'screen_reader_text': f"Collection card {i+1}: {card.name}, drag to deck or click for details",
                'drag_instructions': "Drag to deck area to add to your deck"
            }
            
            self.card_displays.append(card_display)
    
    def _create_all_card_displays(self) -> None:
        """Create card displays for all cards (fallback method)."""
        self.card_displays.clear()
        
        for i, card in enumerate(self.filtered_cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            # Improved card positioning with proper margins
            x = self.rect.x + self.margin_x + col * (self.card_width + self.card_spacing)
            y = self.rect.y + self.margin_y + row * (self.card_height + self.card_spacing)
            
            owned_count = self.player_collection.get_card_count(card.id)
            is_favorite = self.player_collection.is_favorite(card.id)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, 
                                     card, owned_count, is_favorite, draggable=True)
            card_display.add_event_handler("card_selected", self._on_card_selected)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            card_display.add_event_handler("card_dragging", self._on_card_dragging)
            card_display.add_event_handler("card_double_click", self._on_card_double_click)
            self.card_displays.append(card_display)
    
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
    
    def _on_card_double_click(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card double-click to add to deck automatically."""
        card = event_data["card"]
        self.logger.debug(f"Double-click detected on card: {card.name}")
        
        # Trigger event for deck builder to handle adding the card
        self._trigger_event("card_double_click", {
            "card": card, 
            "component": component
        })
    
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
        if "search_text" in filters:
            self.search_text = filters["search_text"]
        
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
        
        # Draw background with theme colors
        theme = get_theme()
        pygame.draw.rect(surface, theme.colors.COLLECTION_BG, self.rect)
        pygame.draw.rect(surface, theme.colors.BRONZE, self.rect, 2)
        
        # Create clipping surface for scrolling
        clip_surface = surface.subsurface(self.rect)
        
        # Render visible cards with proper scroll offset
        for card_display in self.card_displays:
            if self._is_card_visible(card_display):
                # Calculate position relative to the collection area
                render_x = card_display.rect.x - self.rect.x
                render_y = card_display.rect.y - self.rect.y - self.scroll_offset
                
                # Only render if the card is within the visible area
                if render_y + card_display.rect.height >= 0 and render_y <= self.rect.height:
                    # Create a temporary rect for rendering
                    render_rect = pygame.Rect(render_x, render_y, card_display.rect.width, card_display.rect.height)
                    
                    # Temporarily adjust the card display position for rendering
                    old_rect = card_display.rect
                    card_display.rect = render_rect
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
        
        # Forward events to card displays for proper drag handling
        mouse_in_area = self.rect.collidepoint(pygame.mouse.get_pos()) if hasattr(event, 'pos') else False
        any_dragging = any(card.being_dragged for card in self.card_displays)
        
        if mouse_in_area or any_dragging:
            # CRITICAL FIX: Create adjusted event with correct collision detection
            if hasattr(event, 'pos'):
                # Create event with original position for accurate collision detection
                # We'll handle scroll offset inside the card rendering/collision logic
                adjusted_event = event
                
                # Debug logging for coordinate tracking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.logger.debug(f"Click event: pos={event.pos}, scroll_offset={self.scroll_offset}")
            else:
                adjusted_event = event
            
            # Forward to card displays with scroll-aware collision detection
            for card_display in reversed(self.card_displays):
                if self._is_card_visible(card_display):
                    # Create scroll-adjusted rect for collision detection
                    if hasattr(event, 'pos'):
                        adjusted_card_rect = card_display.rect.copy()
                        adjusted_card_rect.y -= self.scroll_offset
                        
                        # Check collision with adjusted rect
                        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                            if adjusted_card_rect.collidepoint(event.pos):
                                # Create event with position adjusted to card's coordinate space
                                card_adjusted_pos = (event.pos[0], event.pos[1] + self.scroll_offset)
                                card_event = pygame.event.Event(
                                    event.type,
                                    dict(event.dict, pos=card_adjusted_pos)
                                )
                                if card_display.handle_event(card_event):
                                    return True
                        else:
                            if card_display.handle_event(adjusted_event):
                                return True
                    else:
                        if card_display.handle_event(adjusted_event):
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
        total_height = rows * (self.card_height + self.card_spacing) + self.margin_y * 2
        self.max_scroll = max(0, total_height - self.rect.height)
        
        for i, card in enumerate(self.filtered_cards):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            # Improved card positioning with proper margins
            x = self.rect.x + self.margin_x + col * (self.card_width + self.card_spacing)
            y = self.rect.y + self.margin_y + row * (self.card_height + self.card_spacing)
            
            card_display = CardDisplay(x, y, self.card_width, self.card_height, card, draggable=True)
            card_display.add_event_handler("card_selected", self._on_card_selected)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            card_display.add_event_handler("card_dragging", self._on_card_dragging)
            card_display.add_event_handler("card_double_click", self._on_card_double_click)
            self.card_displays.append(card_display)
    
    def _scroll(self, delta: int) -> None:
        """Scroll the card collection with lazy loading optimization."""
        old_scroll = self.scroll_offset
        self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset + delta))
        
        # Recreate card displays if scroll position changed significantly with lazy loading
        if self.lazy_loading_enabled and abs(self.scroll_offset - old_scroll) > self.card_height:
            self._create_card_displays()
    
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
        
        # Improved layout settings - better responsive design for deck area
        margin_total = 30  # Total margins
        min_spacing = 12  # Minimum spacing between cards
        base_card_width = 180  # Much larger cards to showcase AI artwork
        
        available_width = width - margin_total
        max_cards_per_row = available_width // (base_card_width + min_spacing)
        self.cards_per_row = min(max(4, max_cards_per_row), 15)  # Reasonable bounds for deck
        
        # Recalculate actual dimensions
        total_spacing = (self.cards_per_row - 1) * min_spacing
        self.card_width = (available_width - total_spacing) // self.cards_per_row
        self.card_height = int(self.card_width * 1.3)  # Maintain aspect ratio
        self.card_spacing = min_spacing
        
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
        
        # Draw background with theme colors and drop zone highlighting
        theme = get_theme()
        bg_color = theme.colors.DECK_VIEW_BG
        border_color = theme.colors.BRONZE
        
        if self.drop_highlight:
            bg_color = theme.colors.HOVER  # Lighter background when hovering with card
            border_color = theme.colors.GOLD  # Gold border for drop zone
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3 if self.drop_highlight else 2)
        
        # Draw title with theme colors
        title_font_size = max(16, min(28, self.rect.width // 20))
        font = pygame.font.Font(None, title_font_size)
        title = "Deck"
        if self.deck is not None:
            title += f" ({len(self.deck.cards)}/30)"  # Assuming 30 card limit
        
        title_surface = font.render(title, True, theme.colors.HIGH_CONTRAST_TEXT)
        title_rect = title_surface.get_rect()
        title_rect.left = self.rect.left + 10
        title_rect.top = self.rect.top + 5
        surface.blit(title_surface, title_rect)
        
        # Draw drop zone hint with theme colors
        if self.deck is None or len(self.deck.cards) == 0:
            hint_font_size = max(14, min(20, self.rect.width // 30))
            hint_font = pygame.font.Font(None, hint_font_size)
            hint_text = "Drag cards here to build your deck"
            hint_surface = hint_font.render(hint_text, True, theme.colors.MEDIUM_CONTRAST_TEXT)
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
            # Check if we're in the drop zone using the same logic as is_valid_drop_zone
            in_drop_zone = self.is_valid_drop_zone(mouse_pos)
            if in_drop_zone != self.drop_highlight:
                self.drop_highlight = in_drop_zone
                # Debug logging
                logging.getLogger(__name__).debug(f"Drop highlight changed: {self.drop_highlight} at {mouse_pos}")
        
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
        if self.deck is not None:
            # Create a copy of the card for the deck to avoid issues
            if hasattr(card, 'model_copy'):
                deck_card = card.model_copy(deep=True)
            elif hasattr(card, 'copy'):
                deck_card = card.copy(deep=True)
            else:
                deck_card = card
            # Use deck's own size validation (max_size)
            success = self.deck.add_card(deck_card)
            if success:
                self._update_layout()
            return success
        return False
    
    def remove_card_at(self, index: int) -> Optional[Card]:
        """Remove a card at the specified index."""
        if self.deck is not None and 0 <= index < len(self.deck.cards):
            card = self.deck.cards.pop(index)
            self._update_layout()
            return card
        return None
    
    def _update_layout(self) -> None:
        """Update the layout of cards in the deck view."""
        self.card_displays.clear()
        
        if self.deck is None:
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
            
            # Add accessibility attributes
            card_display.accessibility = {
                'role': 'button',
                'label': f"{card.name} in deck, {card.sand_cost} sand cost, right-click to remove",
                'keyboard_accessible': True,
                'screen_reader_text': f"Deck card {i+1} of {len(self.deck.cards)}: {card.name}"
            }
            
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
        logger = logging.getLogger(__name__)
        logger.debug(f"Attempting to add card {card.name} to deck")
        
        if self.deck is None:
            logger.error("No deck available to add card to")
            return False
        
        if self.add_card(card):
            logger.info(f"Successfully added {card.name} to deck (deck size: {len(self.deck.cards)})")
            self._trigger_event("card_added_to_deck", {"card": card})
            return True
        else:
            logger.warning(f"Failed to add {card.name} to deck")
            return False
    
    def is_valid_drop_zone(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is a valid drop zone for cards."""
        # CRITICAL FIX: More robust drop zone detection
        if not self.rect.collidepoint(pos):
            return False
        
        # Additional validation to ensure we're in the actual deck area
        # (not just the title or borders)
        title_height = 35  # Space reserved for title
        actual_deck_area = pygame.Rect(
            self.rect.x + 10,  # Small margin from border
            self.rect.y + title_height,
            self.rect.width - 20,  # Margins on both sides
            self.rect.height - title_height - 10  # Bottom margin
        )
        is_valid = actual_deck_area.collidepoint(pos)
        
        # Debug logging
        if hasattr(self, 'logger'):
            if not hasattr(self, '_last_drop_debug') or self._last_drop_debug != pos:
                self._last_drop_debug = pos
                logging.getLogger(__name__).debug(f"Drop zone check: pos={pos}, deck_rect={self.rect}, deck_area={actual_deck_area}, valid={is_valid}")
        
        return is_valid


class FilterPanel(UIComponent):
    """
    Enhanced collapsible panel with filter controls for the card collection.
    Includes Egyptian-themed visual elements and improved UX.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        
        # Filter state
        self.selected_rarity: Optional[CardRarity] = None
        self.selected_type: Optional[CardType] = None
        self.selected_cost: Optional[int] = None
        self.cost_min: Optional[int] = None
        self.cost_max: Optional[int] = None
        self.search_text: str = ""
        
        # Panel state
        self.is_collapsed = False
        self.collapse_height = 40  # Height when collapsed
        self.expanded_height = height
        self.collapse_animation_progress = 1.0  # 1.0 = expanded, 0.0 = collapsed
        
        # Improved responsive font sizing based on panel width
        self.font_size = max(18, min(26, width // 10))  # Better scaling
        self.line_height = self.font_size + 6  # More breathing room
        
        # Interactive areas for clicking filters
        self.filter_buttons: Dict[str, pygame.Rect] = {}
        self.search_input_active = False
        
        # Accessibility features
        self.high_contrast_mode = False
        
        # Egyptian icons for visual appeal (simple shapes for now)
        self.egyptian_colors = {
            'ankh': (255, 215, 0),     # Gold
            'scarab': (139, 117, 93),  # Bronze
            'lotus': (100, 180, 100)   # Green
        }
        
    def update(self, delta_time: float) -> None:
        """Update filter panel and collapse animation."""
        # Update collapse animation
        target_progress = 0.0 if self.is_collapsed else 1.0
        if abs(self.collapse_animation_progress - target_progress) > 0.01:
            animation_speed = 5.0  # Animation speed
            if self.collapse_animation_progress < target_progress:
                self.collapse_animation_progress = min(1.0, self.collapse_animation_progress + delta_time * animation_speed)
            else:
                self.collapse_animation_progress = max(0.0, self.collapse_animation_progress - delta_time * animation_speed)
        
        # Update actual height based on animation progress
        current_height = int(self.collapse_height + (self.expanded_height - self.collapse_height) * self.collapse_animation_progress)
        self.rect.height = current_height
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enhanced filter panel with sandstone colors and Egyptian styling."""
        if not self.visible:
            return
        
        # Use sandstone background color
        bg_color = (245, 222, 179) if not self.is_collapsed else (220, 200, 165)  # F5DEB3 sandstone
        border_color = (139, 117, 93)  # Bronze border
        
        # Draw background with Egyptian styling
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3)
        
        # Add decorative corner elements (simple Egyptian-style corners)
        corner_size = min(10, self.rect.width // 20)
        for corner in [(self.rect.left, self.rect.top), (self.rect.right - corner_size, self.rect.top)]:
            pygame.draw.rect(surface, (255, 215, 0), (corner[0], corner[1], corner_size, corner_size))
        
        # Use improved responsive font sizing
        font = pygame.font.Font(None, self.font_size)
        small_font = pygame.font.Font(None, max(16, self.font_size - 3))  # Larger small fonts
        tiny_font = pygame.font.Font(None, max(14, self.font_size - 4))  # Readable tiny fonts
        
        # Improved padding calculation for better space utilization
        padding = max(8, self.rect.width // 25)  # Better base padding
        item_spacing = max(4, self.rect.width // 50)  # Consistent item spacing
        y_offset = self.rect.top + padding
        
        # Title with collapse/expand button
        title_text = "Filters " + ("▼" if not self.is_collapsed else "▶")
        title_surface = font.render(title_text, True, (139, 117, 93))  # Deep brown text
        surface.blit(title_surface, (self.rect.x + padding, y_offset))
        
        # Store collapse button area for click detection
        self.filter_buttons['collapse'] = pygame.Rect(
            self.rect.x + padding, y_offset, 
            title_surface.get_width(), title_surface.get_height()
        )
        
        y_offset += self.line_height + item_spacing
        
        # Only show filters if not collapsed or still animating
        if self.collapse_animation_progress > 0.1:
            # Create a clipping surface for smooth collapse animation
            if self.collapse_animation_progress < 1.0:
                remaining_height = int((self.rect.bottom - y_offset) * self.collapse_animation_progress)
                if remaining_height <= 0:
                    return
                clip_surface = surface.subsurface(
                    pygame.Rect(self.rect.x, y_offset, self.rect.width, remaining_height)
                )
                render_surface = clip_surface
                base_y = 0
            else:
                render_surface = surface
                base_y = y_offset
            
            # Search box
            search_label = small_font.render("Search:", True, (47, 27, 20))
            render_surface.blit(search_label, (padding, base_y))
            search_y = base_y + self.line_height
            
            # Search input box with Egyptian styling - better width utilization
            search_box_width = max(120, self.rect.width - padding * 2)
            search_box_rect = pygame.Rect(padding, search_y, search_box_width, self.line_height + 4)
            search_bg = (255, 248, 220) if self.search_input_active else (235, 228, 200)
            pygame.draw.rect(render_surface, search_bg, search_box_rect)
            pygame.draw.rect(render_surface, border_color, search_box_rect, 2)
            
            search_display = self.search_text if self.search_text else "Enter card name..."
            search_color = (47, 27, 20) if self.search_text else (120, 100, 80)
            search_surface = tiny_font.render(search_display, True, search_color)
            render_surface.blit(search_surface, (search_box_rect.x + 4, search_box_rect.y + 2))
            
            self.filter_buttons['search'] = pygame.Rect(
                self.rect.x + search_box_rect.x, self.rect.y + search_y, 
                search_box_rect.width, search_box_rect.height
            )
            
            current_y = base_y + self.line_height * 3
            
            # Rarity filters with Egyptian icons
            rarity_text = small_font.render("✦ Rarity:", True, (47, 27, 20))
            render_surface.blit(rarity_text, (padding, current_y))
            current_y += self.line_height
            
            rarity_colors = {
                CardRarity.COMMON: (139, 117, 93),
                CardRarity.UNCOMMON: (100, 150, 100),
                CardRarity.RARE: (100, 100, 200),
                CardRarity.LEGENDARY: (255, 215, 0)
            }
            
            for rarity in CardRarity:
                is_selected = self.selected_rarity == rarity
                color = rarity_colors.get(rarity, (47, 27, 20))
                if is_selected:
                    # Highlight selected with sandstone background - better width usage
                    highlight_width = max(80, self.rect.width - padding * 3)
                    highlight_rect = pygame.Rect(padding * 2 - 2, current_y - 2, highlight_width, self.line_height)
                    pygame.draw.rect(render_surface, (200, 180, 140), highlight_rect)
                    pygame.draw.rect(render_surface, (255, 215, 0), highlight_rect, 1)
                
                rarity_label = tiny_font.render(f"● {rarity.value.title()}", True, color)
                render_surface.blit(rarity_label, (padding * 2, current_y))
                
                # Store button area
                button_rect = pygame.Rect(
                    self.rect.x + padding * 2, self.rect.y + current_y,
                    rarity_label.get_width(), rarity_label.get_height()
                )
                self.filter_buttons[f'rarity_{rarity.value}'] = button_rect
                
                current_y += self.line_height - item_spacing // 2  # Better spacing between filter items
            
            current_y += item_spacing * 2  # Section spacing
            
            # Card Type filters
            type_text = small_font.render("⚔ Type:", True, (47, 27, 20))
            render_surface.blit(type_text, (padding, current_y))
            current_y += self.line_height
            
            type_colors = {
                CardType.ATTACK: (200, 100, 100),
                CardType.SKILL: (100, 200, 100),
                CardType.POWER: (100, 100, 200),
                CardType.CURSE: (150, 50, 150)
            }
            
            for card_type in CardType:
                is_selected = self.selected_type == card_type
                color = type_colors.get(card_type, (47, 27, 20))
                if is_selected:
                    highlight_width = max(80, self.rect.width - padding * 3)
                    highlight_rect = pygame.Rect(padding * 2 - 2, current_y - 2, highlight_width, self.line_height)
                    pygame.draw.rect(render_surface, (200, 180, 140), highlight_rect)
                    pygame.draw.rect(render_surface, (255, 215, 0), highlight_rect, 1)
                
                type_label = tiny_font.render(f"◆ {card_type.value.title()}", True, color)
                render_surface.blit(type_label, (padding * 2, current_y))
                
                self.filter_buttons[f'type_{card_type.value}'] = pygame.Rect(
                    self.rect.x + padding * 2, self.rect.y + current_y,
                    type_label.get_width(), type_label.get_height()
                )
                
                current_y += self.line_height - item_spacing // 2  # Better spacing between filter items
            
            current_y += item_spacing * 2  # Section spacing
            
            # Cost filters with Egyptian styling
            cost_text = small_font.render("⏳ Sand Cost:", True, (47, 27, 20))
            render_surface.blit(cost_text, (padding, current_y))
            current_y += self.line_height
            
            # Cost range display
            cost_range_text = "All" if self.cost_min is None and self.cost_max is None else f"{self.cost_min or 0}-{self.cost_max or 6}"
            range_surface = tiny_font.render(f"Range: {cost_range_text}", True, (47, 27, 20))
            render_surface.blit(range_surface, (padding * 2, current_y))
            current_y += self.line_height
            
            # Individual cost buttons
            cost_x = padding * 2
            for cost in range(7):  # 0-6 sand cost
                is_selected = self.selected_cost == cost
                color = (255, 215, 0) if is_selected else (139, 117, 93)
                
                if is_selected:
                    cost_bg = pygame.Rect(cost_x - 2, current_y - 2, 20, self.line_height)
                    pygame.draw.rect(render_surface, (200, 180, 140), cost_bg)
                    pygame.draw.rect(render_surface, (255, 215, 0), cost_bg, 1)
                
                cost_label = tiny_font.render(str(cost), True, color)
                render_surface.blit(cost_label, (cost_x, current_y))
                
                self.filter_buttons[f'cost_{cost}'] = pygame.Rect(
                    self.rect.x + cost_x, self.rect.y + current_y,
                    15, cost_label.get_height()
                )
                
                cost_x += 25
            
            current_y += self.line_height + item_spacing
            
            # Clear filters button
            clear_button_rect = pygame.Rect(padding, current_y, self.rect.width - padding * 2, self.line_height + 4)
            pygame.draw.rect(render_surface, (220, 200, 160), clear_button_rect)
            pygame.draw.rect(render_surface, border_color, clear_button_rect, 2)
            clear_text = tiny_font.render("Clear All Filters", True, (47, 27, 20))
            text_x = clear_button_rect.x + (clear_button_rect.width - clear_text.get_width()) // 2
            render_surface.blit(clear_text, (text_x, clear_button_rect.y + 2))
            
            self.filter_buttons['clear'] = pygame.Rect(
                self.rect.x + clear_button_rect.x, self.rect.y + current_y,
                clear_button_rect.width, clear_button_rect.height
            )
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle enhanced filter interactions including collapse/expand."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check all filter button clicks
            for button_name, button_rect in self.filter_buttons.items():
                if button_rect.collidepoint(event.pos):
                    if button_name == 'collapse':
                        self.is_collapsed = not self.is_collapsed
                        return True
                    
                    elif button_name == 'search':
                        self.search_input_active = True
                        return True
                    
                    elif button_name.startswith('rarity_'):
                        rarity_name = button_name.split('_', 1)[1]
                        target_rarity = None
                        for rarity in CardRarity:
                            if rarity.value == rarity_name:
                                target_rarity = rarity
                                break
                        
                        # Toggle selection
                        if self.selected_rarity == target_rarity:
                            self.selected_rarity = None
                        else:
                            self.selected_rarity = target_rarity
                        
                        self._trigger_filter_change()
                        return True
                    
                    elif button_name.startswith('type_'):
                        type_name = button_name.split('_', 1)[1]
                        target_type = None
                        for card_type in CardType:
                            if card_type.value == type_name:
                                target_type = card_type
                                break
                        
                        # Toggle selection
                        if self.selected_type == target_type:
                            self.selected_type = None
                        else:
                            self.selected_type = target_type
                        
                        self._trigger_filter_change()
                        return True
                    
                    elif button_name.startswith('cost_'):
                        cost = int(button_name.split('_', 1)[1])
                        
                        # Toggle cost selection
                        if self.selected_cost == cost:
                            self.selected_cost = None
                            self.cost_min = None
                            self.cost_max = None
                        else:
                            self.selected_cost = cost
                            self.cost_min = cost
                            self.cost_max = cost
                        
                        self._trigger_filter_change()
                        return True
                    
                    elif button_name == 'clear':
                        self.clear_all_filters()
                        return True
            
            # Click outside search box deactivates it
            if self.search_input_active:
                search_rect = self.filter_buttons.get('search')
                if not search_rect or not search_rect.collidepoint(event.pos):
                    self.search_input_active = False
        
        elif event.type == pygame.KEYDOWN:
            # Handle keyboard navigation and search input
            if self.search_input_active:
                # Handle search text input
                if event.key == pygame.K_BACKSPACE:
                    self.search_text = self.search_text[:-1]
                    self._trigger_filter_change()
                    return True
                elif event.key == pygame.K_RETURN:
                    self.search_input_active = False
                    return True
                elif event.key == pygame.K_ESCAPE:
                    self.search_input_active = False
                    self.search_text = ""
                    self._trigger_filter_change()
                    return True
                elif event.unicode.isprintable() and len(self.search_text) < 20:
                    self.search_text += event.unicode
                    self._trigger_filter_change()
                    return True
            else:
                # Handle keyboard shortcuts for accessibility
                if event.key == pygame.K_F1:
                    # Toggle high contrast mode
                    self.toggle_high_contrast()
                    return True
                elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL:
                    # Clear all filters (Ctrl+C)
                    self.clear_all_filters()
                    return True
                elif event.key == pygame.K_SLASH:
                    # Focus search (/) 
                    self.search_input_active = True
                    return True
        
        return super().handle_event(event)
    
    def _trigger_filter_change(self) -> None:
        """Trigger filter change event."""
        filter_data = {
            'rarity': self.selected_rarity,
            'type': self.selected_type,
            'cost_min': self.cost_min,
            'cost_max': self.cost_max,
            'search_text': self.search_text
        }
        self._trigger_event('filters_changed', filter_data)
    
    def clear_all_filters(self) -> None:
        """Clear all active filters."""
        self.selected_rarity = None
        self.selected_type = None
        self.selected_cost = None
        self.cost_min = None
        self.cost_max = None
        self.search_text = ""
        self._trigger_filter_change()
    
    def get_active_filters(self) -> Dict[str, Any]:
        """Get currently active filters."""
        return {
            'rarity': self.selected_rarity,
            'type': self.selected_type,
            'cost_min': self.cost_min,
            'cost_max': self.cost_max,
            'search_text': self.search_text
        }
    
    def toggle_high_contrast(self) -> None:
        """Toggle high contrast mode for accessibility."""
        self.high_contrast_mode = not self.high_contrast_mode
        self._trigger_event('high_contrast_changed', {'enabled': self.high_contrast_mode})
    
    def get_accessibility_info(self) -> str:
        """Get current filter status for screen readers."""
        filters = []
        if self.selected_rarity:
            filters.append(f"Rarity: {self.selected_rarity.value}")
        if self.selected_type:
            filters.append(f"Type: {self.selected_type.value}")
        if self.cost_min is not None or self.cost_max is not None:
            cost_range = f"{self.cost_min or 0}-{self.cost_max or 6}"
            filters.append(f"Cost: {cost_range}")
        if self.search_text:
            filters.append(f"Search: {self.search_text}")
        
        if filters:
            return f"Active filters: {', '.join(filters)}"
        else:
            return "No active filters"


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
        
        # Initialize parallax and atmospheric systems
        self.parallax_system = None
        self.atmospheric_manager = None
        
        if PARALLAX_AVAILABLE:
            try:
                display_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (1920, 1080)
                self.parallax_system = get_interactive_parallax_system(display_size[0], display_size[1])
                self.parallax_system.set_current_screen("deck_builder")
                
                self.atmospheric_manager = get_atmospheric_manager(display_size[0], display_size[1])
                self.atmospheric_manager.setup_screen_atmosphere("deck_builder")
            except Exception as e:
                print(f"Deck builder parallax initialization failed: {e}")
                self.parallax_system = None
                self.atmospheric_manager = None
        
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
                "< Back to Progression",
                self._back_to_progression
            )
            self.add_component(back_button)
            
            # Add Start Combat button
            combat_button = MenuButton(
                back_zone.x + back_zone.width + 20, back_zone.y, back_zone.width, back_zone.height,
                "Start Combat",
                self._start_combat
            )
            self.add_component(combat_button)
            
            # Filter panel using theme zone
            self.filter_panel = FilterPanel(
                filter_zone.x, filter_zone.y, filter_zone.width, filter_zone.height
            )
            self.filter_panel.add_event_handler("filters_changed", self._on_filters_changed)
            self.filter_panel.add_event_handler("high_contrast_changed", self._on_high_contrast_changed)
            self.add_component(self.filter_panel)
            
            # Create temporary player collection for testing
            # TODO: Replace with actual player collection system
            temp_player_collection = PlayerCollection()
            
            # Calculate optimal card layout based on collection zone size
            # Better responsive calculation for card sizing
            base_card_width = 200  # Much larger target to showcase AI artwork
            min_spacing = 15  # Minimum spacing between cards
            margin_total = 30  # Total left/right margins
            
            # Calculate how many cards fit with proper spacing
            available_width = collection_zone.width - margin_total
            max_cards_per_row = available_width // (base_card_width + min_spacing)
            cards_per_row = min(max(6, max_cards_per_row), 20)  # Reasonable bounds
            
            # Recalculate card width based on actual cards per row
            total_spacing = (cards_per_row - 1) * min_spacing
            optimal_card_width = (available_width - total_spacing) // cards_per_row
            optimal_card_height = int(optimal_card_width * 1.4)  # Maintain aspect ratio
            
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
            self.card_collection.add_event_handler("card_double_click", self._on_card_double_click)
            self.add_component(self.card_collection)
            
            # Deck view using theme zone
            self.deck_view = DeckView(
                deck_zone.x, deck_zone.y, deck_zone.width, deck_zone.height
            )
            self.deck_view.add_event_handler("card_removed", self._on_card_removed)
            self.deck_view.add_event_handler("card_added_to_deck", self._on_card_added_to_deck)
            self.deck_view.add_event_handler("deck_card_info", self._on_deck_card_info)
            self.add_component(self.deck_view)
            
            # Initialize with empty deck with proper size limits
            self.current_deck = Deck(name="Custom Deck", max_size=30)
            self.deck_view.set_deck(self.current_deck)
            
            self.logger.info(f"Deck builder UI setup for {theme.display.display_mode.value} mode")
            
        except Exception as e:
            self.logger.error(f"Failed to setup UI with theme zones, using fallback: {e}")
            # Fallback to original hardcoded layout if theme fails
            self._setup_fallback_ui()
    
    def _setup_fallback_ui(self) -> None:
        """Improved fallback UI setup with responsive breakpoints."""
        # Get screen dimensions for responsive layout
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        
        # Define responsive breakpoints
        if screen_width >= 3200:  # Ultrawide+
            filter_width, collection_width, deck_width = 280, 1800, 400
            button_width = 180
        elif screen_width >= 2560:  # Ultrawide
            filter_width, collection_width, deck_width = 250, 1400, 350
            button_width = 160
        elif screen_width >= 1920:  # Full HD
            filter_width, collection_width, deck_width = 220, 1000, 300
            button_width = 150
        elif screen_width >= 1366:  # Standard laptop
            filter_width, collection_width, deck_width = 180, 700, 250
            button_width = 130
        else:  # Compact
            filter_width, collection_width, deck_width = 150, 500, 200
            button_width = 120
        
        margin = max(10, screen_width // 200)
        button_height = max(35, screen_height // 30)
        
        # Responsive button positioning
        back_button = MenuButton(
            margin, margin, button_width, button_height,
            "< Back to Progression",
            self._back_to_progression
        )
        self.add_component(back_button)
        
        combat_button = MenuButton(
            margin + button_width + 10, margin, button_width, button_height,
            "Start Combat",
            self._start_combat
        )
        self.add_component(combat_button)
        
        # Responsive filter panel
        filter_y = margin + button_height + 15
        filter_height = min(600, screen_height - filter_y - margin)
        self.filter_panel = FilterPanel(margin, filter_y, filter_width, filter_height)
        self.filter_panel.add_event_handler("filters_changed", self._on_filters_changed)
        self.filter_panel.add_event_handler("high_contrast_changed", self._on_high_contrast_changed)
        self.add_component(self.filter_panel)
        
        # Create temporary player collection for testing
        temp_player_collection = PlayerCollection()
        
        # Responsive card collection
        collection_x = margin + filter_width + 15
        collection_height = filter_height
        self.card_collection = CardCollection(
            collection_x, filter_y, collection_width, collection_height, 
            temp_player_collection
        )
        self.card_collection.add_event_handler("card_selection_changed", self._on_card_selected)
        self.card_collection.add_event_handler("card_drag_start", self._on_card_drag_start)
        self.card_collection.add_event_handler("card_drag_end", self._on_card_drag_end)
        self.card_collection.add_event_handler("card_dragging", self._on_card_dragging)
        self.card_collection.add_event_handler("card_double_click", self._on_card_double_click)
        self.add_component(self.card_collection)
        
        # Responsive deck view
        deck_x = collection_x + collection_width + 15
        self.deck_view = DeckView(deck_x, filter_y, deck_width, collection_height)
        self.deck_view.add_event_handler("card_removed", self._on_card_removed)
        self.deck_view.add_event_handler("card_added_to_deck", self._on_card_added_to_deck)
        self.deck_view.add_event_handler("deck_card_info", self._on_deck_card_info)
        self.add_component(self.deck_view)
        
        # Initialize with empty deck with proper size limits
        self.current_deck = Deck(name="Custom Deck", max_size=30)
        self.deck_view.set_deck(self.current_deck)
        
        self.logger.info(f"Fallback UI setup for {screen_width}x{screen_height} resolution")
    
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
        original_pos = event_data.get("original_pos")
        
        self.logger.debug(f"Card drag ended: card={card.name if card else 'None'}, drop_pos={drop_pos}, original_pos={original_pos}")
        
        if card and drop_pos and self.deck_view:
            # Check if card was dropped on the deck view
            is_valid_drop = self.deck_view.is_valid_drop_zone(drop_pos)
            self.logger.debug(f"Drop zone validation for {card.name}: valid={is_valid_drop}")
            
            if is_valid_drop:
                # Try to add card to deck
                add_success = self.deck_view.accept_dropped_card(card)
                self.logger.debug(f"Deck add attempt for {card.name}: success={add_success}")
                
                if add_success:
                    self.logger.info(f"Successfully added {card.name} to deck via drag-and-drop")
                    # CRITICAL FIX: Remove card from collection display instead of resetting position
                    if self.card_collection:
                        self.card_collection.remove_card_from_collection_display(card)
                    
                    # Clear drag state but don't reset position - card should disappear from collection
                    if card_component:
                        card_component.being_dragged = False
                        card_component.drag_offset_x = 0
                        card_component.drag_offset_y = 0
                        # Remove the card component from the collection's display list
                        # (this is handled by remove_card_from_collection_display)
                else:
                    self.logger.warning(f"Failed to add {card.name} to deck - deck may be full")
                    # Reset card position on failed drop
                    if card_component and original_pos:
                        card_component.rect.x, card_component.rect.y = original_pos
                        card_component.being_dragged = False
            else:
                self.logger.debug(f"Card {card.name} dropped outside deck area at {drop_pos}")
                # Reset card position when dropped outside valid zone
                if card_component and original_pos:
                    card_component.rect.x, card_component.rect.y = original_pos
                    card_component.being_dragged = False
        else:
            self.logger.warning(f"Incomplete drag end data: card={card}, drop_pos={drop_pos}, deck_view={self.deck_view}")
            # Reset card position as fallback
            if card_component and original_pos:
                card_component.rect.x, card_component.rect.y = original_pos
                card_component.being_dragged = False
    
    def _on_card_dragging(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card being dragged - update drop zone highlights."""
        card = event_data.get("card")
        if card and self.deck_view:
            mouse_pos = pygame.mouse.get_pos()
            self.deck_view.drop_highlight = self.deck_view.rect.collidepoint(mouse_pos)
    
    def _on_card_double_click(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card double-click to automatically add to deck."""
        card = event_data.get("card")
        card_component = event_data.get("component")
        
        if card and self.deck_view:
            self.logger.info(f"Double-click adding {card.name} to deck")
            
            # Try to add card to deck
            add_success = self.deck_view.accept_dropped_card(card)
            
            if add_success:
                self.logger.info(f"Successfully added {card.name} to deck via double-click")
                # Remove card from collection display
                if self.card_collection:
                    self.card_collection.remove_card_from_collection_display(card)
            else:
                self.logger.warning(f"Failed to add {card.name} to deck - deck may be full")
        else:
            self.logger.warning(f"Double-click failed: card={card}, deck_view={self.deck_view}")
    
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
    
    def _on_filters_changed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle filter changes from the filter panel."""
        if self.card_collection:
            # Apply filters to card collection
            self.card_collection.set_filters(
                rarity=event_data.get('rarity'),
                type=event_data.get('type'),
                cost_min=event_data.get('cost_min'),
                cost_max=event_data.get('cost_max'),
                search_text=event_data.get('search_text', '')
            )
            self.logger.debug(f"Applied filters: {event_data}")
            
            # Log accessibility info
            if hasattr(self.filter_panel, 'get_accessibility_info'):
                accessibility_status = self.filter_panel.get_accessibility_info()
                self.logger.info(f"Filter accessibility status: {accessibility_status}")
    
    def _on_high_contrast_changed(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle high contrast mode changes."""
        enabled = event_data.get('enabled', False)
        self.logger.info(f"High contrast mode {'enabled' if enabled else 'disabled'}")
        
        # Propagate to all UI components that support high contrast
        if self.card_collection:
            for card_display in self.card_collection.card_displays:
                if hasattr(card_display, 'accessibility'):
                    card_display.accessibility['high_contrast_mode'] = enabled
                    card_display.high_contrast_mode = enabled
    
    def toggle_accessibility_features(self) -> None:
        """Toggle various accessibility features."""
        if self.filter_panel and hasattr(self.filter_panel, 'toggle_high_contrast'):
            self.filter_panel.toggle_high_contrast()
    
    def _back_to_progression(self) -> None:
        """Return to progression screen."""
        self.logger.info("Returning to progression screen from deck builder")
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("progression", "slide_right")
        else:
            # Fallback - just log for now since UIScreen doesn't have _trigger_event
            self.logger.warning("No UI manager available for screen transition")
    
    def _start_combat(self) -> None:
        """Start combat with current deck."""
        self.logger.info("Starting combat from deck builder")
        
        # Get game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        
        if game_flow:
            # Use Game Flow Manager to handle combat
            node_data = {
                "enemy_id": "desert_mummy",
                "is_boss": False
            }
            game_flow.handle_node_selection("combat", node_data)
        else:
            # Fallback to direct transition
            if hasattr(self, 'ui_manager') and self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("dynamic_combat", "slide_left")
            else:
                self.logger.warning("No UI manager available for combat transition")
    
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
    
    def update(self, delta_time: float) -> None:
        """Update deck builder screen with parallax and atmospheric effects."""
        super().update(delta_time)
        
        # Update parallax system
        if self.parallax_system:
            try:
                self.parallax_system.update(delta_time)
            except Exception as e:
                print(f"Deck builder parallax update error: {e}")
        
        # Update atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.update(delta_time)
            except Exception as e:
                print(f"Deck builder atmospheric update error: {e}")
    
    def render(self, surface: pygame.Surface) -> None:
        """Render deck builder screen with parallax background."""
        # Render parallax background first
        if self.parallax_system:
            try:
                camera_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
                self.parallax_system.render(surface, camera_rect)
            except Exception as e:
                print(f"Deck builder parallax render error: {e}")
        
        # Render atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.render(surface)
            except Exception as e:
                print(f"Deck builder atmospheric render error: {e}")
        
        # Render UI components
        super().render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle deck builder events including mouse movement for parallax."""
        # Handle mouse movement for parallax effects
        if event.type == pygame.MOUSEMOTION and self.parallax_system:
            try:
                handle_mouse_parallax(event.pos[0], event.pos[1])
            except:
                pass  # Fallback if parallax not available
        
        # Handle card hover and interaction effects
        if event.type == pygame.MOUSEMOTION and self.card_collection:
            # Check if hovering over cards and trigger effects
            for card_display in self.card_collection.card_displays:
                if card_display.rect.collidepoint(event.pos) and not card_display.hovered:
                    try:
                        trigger_ui_interaction(InteractionType.CARD_HOVER, event.pos[0], event.pos[1])
                    except:
                        pass
        
        # Let base class handle other events
        return super().handle_event(event)