"""
Enhanced Hall of Gods - Professional Collection Screen with Modern Grid Layout
Features improved filtering, search, grid view, and enhanced Egyptian theming.
"""

import pygame
import math
import random
from typing import List, Optional, Tuple, Callable, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.hades_button import HadesButton
from ..components.smooth_transitions import smooth_transitions, TransitionType, EasingType
from ..components.responsive_typography import responsive_typography, TextStyle

class HallAction(Enum):
    """Enhanced Hall of Gods actions."""
    BACK_TO_MENU = auto()
    FILTER_BY_GOD = auto()
    FILTER_BY_RARITY = auto()
    FILTER_BY_TYPE = auto()
    SEARCH_CARDS = auto()
    VIEW_CARD_DETAILS = auto()
    CHANGE_VIEW_MODE = auto()
    SORT_COLLECTION = auto()

class ViewMode(Enum):
    """Collection view modes."""
    GRID = auto()
    LIST = auto()
    DETAILS = auto()

class SortMode(Enum):
    """Collection sorting modes."""
    NAME = auto()
    RARITY = auto()
    COST = auto()
    GOD = auto()
    TYPE = auto()

@dataclass
class CardInfo:
    """Enhanced card information for collection."""
    name: str
    rarity: str
    god: str
    card_type: str
    cost: int
    attack: int
    health: int
    description: str
    lore: str
    unlocked: bool = True
    discovered: bool = True
    favorite: bool = False
    new: bool = False
    copies_owned: int = 1
    
    def __hash__(self):
        """Make CardInfo hashable based on name (unique identifier)."""
        return hash(self.name)

class EnhancedHallOfGods:
    """
    Enhanced Hall of Gods collection screen with modern grid layout.
    Features professional filtering, search, sorting, and beautiful Egyptian theming.
    """
    
    def __init__(self, on_action: Optional[Callable[[HallAction, Any], None]] = None):
        """Initialize enhanced Hall of Gods screen."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.grid_animation_progress = 0.0
        self.card_hover_scale = {}
        
        # View state
        self.view_mode = ViewMode.GRID
        self.sort_mode = SortMode.NAME
        self.sort_ascending = True
        
        # Filter state
        self.current_god_filter = "all"
        self.current_rarity_filter = "all"
        self.current_type_filter = "all"
        self.search_query = ""
        
        # Grid layout
        self.grid_columns = 6 if Layout.IS_ULTRAWIDE else 4
        self.grid_rows = 4
        self.card_size = (180, 270)
        self.card_spacing = 20
        self.grid_start_x = Layout.UI_SAFE_LEFT + 50
        self.grid_start_y = 250
        
        # Scroll state
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_velocity = 0
        
        # Card collection
        self.all_cards = self._create_enhanced_card_collection()
        self.filtered_cards = self.all_cards.copy()
        self.visible_cards = []
        
        # Selected/hovered state
        self.selected_card = None
        self.hovered_card = None
        self.card_details_visible = False
        
        # Background and effects
        self.background_surface = self._create_background()
        self.particles = []
        self._spawn_divine_particles()
        
        # UI components
        self.control_buttons = self._create_control_buttons()
        self.filter_buttons = self._create_filter_buttons()
        self.search_box = self._create_search_box()
        
        # Update initial view
        self._apply_filters()
        self._update_grid_layout()
        
        # Start fade-in
        smooth_transitions.fade_in_element("hall_of_gods", Timing.FADE_DURATION)
        
        print("Enhanced Hall of Gods initialized - Divine Collection with Grid Layout Ready")
    
    def _create_background(self):
        """Create atmospheric Hall of Gods background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create rich gradient background
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(15 + ratio * 20)
            g = int(8 + ratio * 12)
            b = int(35 + ratio * 30)
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add mystical pattern overlay
        pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, 120):
            for y in range(0, SCREEN_HEIGHT, 120):
                alpha = int(10 + 8 * math.sin(x * 0.02 + y * 0.02))
                pygame.draw.circle(pattern_surface, Colors.GOLD, (x, y), 2)
                pattern_surface.set_alpha(alpha)
        
        background.blit(pattern_surface, (0, 0))
        return background
    
    def _create_enhanced_card_collection(self) -> List[CardInfo]:
        """Create enhanced divine card collection with more details."""
        cards = [
            # Legendary Gods
            CardInfo("RA - SUN GOD", "legendary", "ra", "deity", 8, 10, 12,
                    "Deal 3 damage at dawn to all enemies", 
                    "Ra, the falcon-headed sun god, travels across the sky in his solar barque.", copies_owned=1),
            
            CardInfo("ANUBIS - JUDGE OF THE DEAD", "legendary", "anubis", "deity", 6, 8, 8,
                    "When a creature dies, gain +2/+2",
                    "Anubis weighs hearts against the feather of Ma'at.", copies_owned=1),
            
            CardInfo("ISIS - DIVINE MOTHER", "legendary", "isis", "deity", 7, 5, 10,
                    "Restore 5 health to all friendly creatures",
                    "Isis, mistress of magic and healing, protects the faithful.", copies_owned=1),
            
            CardInfo("SET - CHAOS GOD", "legendary", "set", "deity", 7, 9, 6,
                    "Deal 2 damage to all creatures when played",
                    "Set brings destruction and discord wherever he treads.", copies_owned=1),
            
            # Epic Spells and Artifacts
            CardInfo("PYRAMID POWER", "epic", "ra", "spell", 5, 0, 0,
                    "All creatures gain +2/+2 until end of turn",
                    "The great pyramids channel Ra's divine energy.", copies_owned=2),
            
            CardInfo("BOOK OF THE DEAD", "epic", "anubis", "artifact", 4, 0, 0,
                    "Draw a card when a creature dies",
                    "Sacred text containing spells for the afterlife.", copies_owned=1),
            
            CardInfo("ANKH OF LIFE", "epic", "isis", "artifact", 3, 0, 0,
                    "Prevent the next damage to any creature",
                    "Symbol of eternal life and divine protection.", copies_owned=3),
            
            # Rare Creatures
            CardInfo("SPHINX GUARDIAN", "rare", "general", "creature", 5, 6, 5,
                    "Cannot be targeted by spells",
                    "Wise and ancient, poses riddles to travelers.", copies_owned=2),
            
            CardInfo("MUMMY GUARDIAN", "rare", "anubis", "creature", 4, 3, 7,
                    "Returns to hand when destroyed",
                    "Ancient guardians bound by sacred wrappings.", copies_owned=4),
            
            CardInfo("PHARAOH'S GUARD", "rare", "general", "creature", 6, 7, 6,
                    "Other friendly creatures gain +1/+1",
                    "Elite guards blessed by the gods.", copies_owned=2),
            
            # Common Cards
            CardInfo("EGYPTIAN WARRIOR", "common", "general", "creature", 3, 4, 4,
                    "Steadfast defender of the pharaoh",
                    "Elite soldiers who guard the temples.", copies_owned=8),
            
            CardInfo("SAND BOLT", "common", "set", "spell", 2, 0, 0,
                    "Deal 3 damage to target",
                    "Harness the fury of the desert winds.", copies_owned=6),
            
            CardInfo("DIVINE HEALING", "common", "isis", "spell", 1, 0, 0,
                    "Restore 5 health to target",
                    "Channel the goddess's healing power.", copies_owned=5),
            
            CardInfo("SCARAB SWARM", "common", "general", "creature", 2, 2, 1,
                    "Summon two 1/1 Scarab tokens",
                    "Sacred beetles that devour corruption.", copies_owned=7),
        ]
        
        return cards
    
    def _spawn_divine_particles(self):
        """Spawn atmospheric divine particles."""
        for _ in range(40):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 4),
                'speed': random.randint(5, 15),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.LAPIS_LAZULI, Colors.PAPYRUS]),
                'alpha': random.randint(60, 150)
            })
    
    def _create_control_buttons(self) -> List[HadesButton]:
        """Create control buttons for the collection."""
        buttons = []
        
        # Back button
        back_btn = HadesButton(
            50, 50, 120, 40, "BACK",
            theme_color=Colors.RED,
            hieroglyph="<",
            on_click=lambda: self._handle_action(HallAction.BACK_TO_MENU)
        )
        buttons.append(back_btn)
        
        # View mode toggle
        view_btn = HadesButton(
            SCREEN_WIDTH - 200, 50, 140, 40, "GRID VIEW",
            theme_color=Colors.LAPIS_LAZULI,
            hieroglyph="◊",
            on_click=self._toggle_view_mode
        )
        buttons.append(view_btn)
        
        # Sort button
        sort_btn = HadesButton(
            SCREEN_WIDTH - 350, 50, 120, 40, "SORT",
            theme_color=Colors.GOLD,
            hieroglyph="↕",
            on_click=self._cycle_sort_mode
        )
        buttons.append(sort_btn)
        
        return buttons
    
    def _create_filter_buttons(self) -> Dict[str, List[HadesButton]]:
        """Create filter buttons organized by category."""
        filters = {
            'god': [],
            'rarity': [],
            'type': []
        }
        
        # God filters
        gods = ["all", "ra", "anubis", "isis", "set", "general"]
        god_colors = {
            "all": Colors.PAPYRUS,
            "ra": Colors.GOLD,
            "anubis": Colors.DARK_BLUE,
            "isis": Colors.LAPIS_LAZULI,
            "set": Colors.RED,
            "general": Colors.DESERT_SAND
        }
        
        start_x = self.grid_start_x
        for i, god in enumerate(gods):
            btn = HadesButton(
                start_x + i * 110, 150, 100, 30,
                text=god.upper(),
                theme_color=god_colors[god],
                on_click=lambda g=god: self._filter_by_god(g)
            )
            filters['god'].append(btn)
        
        # Rarity filters
        rarities = ["all", "common", "rare", "epic", "legendary"]
        rarity_colors = {
            "all": Colors.PAPYRUS,
            "common": Colors.GRAY,
            "rare": Colors.LAPIS_LAZULI,
            "epic": Colors.PURPLE,
            "legendary": Colors.GOLD
        }
        
        for i, rarity in enumerate(rarities):
            btn = HadesButton(
                start_x + i * 110, 185, 100, 30,
                text=rarity.upper(),
                theme_color=rarity_colors[rarity],
                on_click=lambda r=rarity: self._filter_by_rarity(r)
            )
            filters['rarity'].append(btn)
        
        # Type filters  
        types = ["all", "deity", "creature", "spell", "artifact"]
        for i, card_type in enumerate(types):
            btn = HadesButton(
                start_x + i * 110, 220, 100, 30,
                text=card_type.upper(),
                theme_color=Colors.DESERT_SAND,
                on_click=lambda t=card_type: self._filter_by_type(t)
            )
            filters['type'].append(btn)
        
        return filters
    
    def _create_search_box(self):
        """Create search input area."""
        return {
            'rect': pygame.Rect(SCREEN_WIDTH - 250, 120, 200, 30),
            'active': False,
            'text': '',
            'cursor_pos': 0
        }
    
    def _toggle_view_mode(self):
        """Toggle between view modes."""
        if self.view_mode == ViewMode.GRID:
            self.view_mode = ViewMode.LIST
            self.control_buttons[1].text = "LIST VIEW"
        else:
            self.view_mode = ViewMode.GRID
            self.control_buttons[1].text = "GRID VIEW"
        
        self._update_grid_layout()
    
    def _cycle_sort_mode(self):
        """Cycle through sort modes."""
        modes = list(SortMode)
        current_index = modes.index(self.sort_mode)
        next_index = (current_index + 1) % len(modes)
        self.sort_mode = modes[next_index]
        
        # Update button text
        self.control_buttons[2].text = f"SORT: {self.sort_mode.name}"
        
        self._apply_filters()
    
    def _filter_by_god(self, god: str):
        """Filter collection by god."""
        self.current_god_filter = god
        self._apply_filters()
    
    def _filter_by_rarity(self, rarity: str):
        """Filter collection by rarity."""
        self.current_rarity_filter = rarity
        self._apply_filters()
    
    def _filter_by_type(self, card_type: str):
        """Filter collection by type."""
        self.current_type_filter = card_type
        self._apply_filters()
    
    def _apply_filters(self):
        """Apply all active filters and sorting."""
        filtered = self.all_cards.copy()
        
        # Apply god filter
        if self.current_god_filter != "all":
            filtered = [c for c in filtered if c.god == self.current_god_filter]
        
        # Apply rarity filter
        if self.current_rarity_filter != "all":
            filtered = [c for c in filtered if c.rarity == self.current_rarity_filter]
        
        # Apply type filter
        if self.current_type_filter != "all":
            filtered = [c for c in filtered if c.card_type == self.current_type_filter]
        
        # Apply search filter
        if self.search_query:
            query = self.search_query.lower()
            filtered = [c for c in filtered if query in c.name.lower() or query in c.description.lower()]
        
        # Apply sorting
        if self.sort_mode == SortMode.NAME:
            filtered.sort(key=lambda c: c.name, reverse=not self.sort_ascending)
        elif self.sort_mode == SortMode.RARITY:
            rarity_order = {"common": 1, "rare": 2, "epic": 3, "legendary": 4}
            filtered.sort(key=lambda c: rarity_order.get(c.rarity, 0), reverse=not self.sort_ascending)
        elif self.sort_mode == SortMode.COST:
            filtered.sort(key=lambda c: c.cost, reverse=not self.sort_ascending)
        elif self.sort_mode == SortMode.GOD:
            filtered.sort(key=lambda c: c.god, reverse=not self.sort_ascending)
        elif self.sort_mode == SortMode.TYPE:
            filtered.sort(key=lambda c: c.card_type, reverse=not self.sort_ascending)
        
        self.filtered_cards = filtered
        self.scroll_offset = 0  # Reset scroll when filters change
        self._update_grid_layout()
    
    def _update_grid_layout(self):
        """Update the grid layout based on current view mode."""
        if self.view_mode == ViewMode.GRID:
            # Calculate grid dimensions
            cards_per_row = self.grid_columns
            total_rows = math.ceil(len(self.filtered_cards) / cards_per_row)
            
            # Calculate scroll limits
            visible_rows = self.grid_rows
            self.max_scroll = max(0, (total_rows - visible_rows) * (self.card_size[1] + self.card_spacing))
            
            # Update visible cards
            start_row = int(self.scroll_offset // (self.card_size[1] + self.card_spacing))
            end_row = start_row + visible_rows + 2  # Extra for smooth scrolling
            
            start_index = start_row * cards_per_row
            end_index = min(len(self.filtered_cards), end_row * cards_per_row)
            
            self.visible_cards = self.filtered_cards[start_index:end_index]
        else:
            # List view - show more cards vertically
            self.visible_cards = self.filtered_cards
    
    def _get_card_rect(self, card_index: int) -> pygame.Rect:
        """Get the screen rectangle for a card in the grid."""
        if self.view_mode == ViewMode.GRID:
            row = card_index // self.grid_columns
            col = card_index % self.grid_columns
            
            x = self.grid_start_x + col * (self.card_size[0] + self.card_spacing)
            y = self.grid_start_y + row * (self.card_size[1] + self.card_spacing) - self.scroll_offset
            
            return pygame.Rect(x, y, self.card_size[0], self.card_size[1])
        else:
            # List view layout
            x = self.grid_start_x
            y = self.grid_start_y + card_index * 80 - self.scroll_offset
            return pygame.Rect(x, y, 600, 70)
    
    def _handle_action(self, action: HallAction, data: Any = None):
        """Handle hall actions."""
        if self.on_action:
            self.on_action(action, data)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update the enhanced hall of gods."""
        self.animation_time += dt
        
        # Update fade-in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
        
        # Update grid animation
        if self.grid_animation_progress < 1.0:
            self.grid_animation_progress = min(1.0, self.grid_animation_progress + dt * 3.0)
        
        # Update scroll velocity (smooth scrolling)
        if abs(self.scroll_velocity) > 1:
            self.scroll_offset += self.scroll_velocity * dt
            self.scroll_velocity *= 0.95  # Deceleration
            
            # Clamp scroll
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Update particles
        for particle in self.particles:
            particle['x'] += math.sin(self.animation_time + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.8 + particle['phase']) * particle['speed'] * dt * 0.5
            
            # Wrap around
            if particle['x'] < -20:
                particle['x'] = SCREEN_WIDTH + 20
            elif particle['x'] > SCREEN_WIDTH + 20:
                particle['x'] = -20
            if particle['y'] < -20:
                particle['y'] = SCREEN_HEIGHT + 20
            elif particle['y'] > SCREEN_HEIGHT + 20:
                particle['y'] = -20
        
        # Update card hover animations
        self.hovered_card = None
        for i, card in enumerate(self.visible_cards):
            card_rect = self._get_card_rect(i)
            if card_rect.collidepoint(mouse_pos):
                self.hovered_card = card
                
                # Animate hover scale
                if card not in self.card_hover_scale:
                    self.card_hover_scale[card] = 1.0
                self.card_hover_scale[card] = min(1.1, self.card_hover_scale[card] + dt * 4.0)
            else:
                # Animate out
                if card in self.card_hover_scale:
                    self.card_hover_scale[card] = max(1.0, self.card_hover_scale[card] - dt * 4.0)
                    if self.card_hover_scale[card] <= 1.0:
                        del self.card_hover_scale[card]
        
        # Update UI buttons
        for button in self.control_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        for button_list in self.filter_buttons.values():
            for button in button_list:
                button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(HallAction.BACK_TO_MENU)
                elif event.key == pygame.K_TAB:
                    self._toggle_view_mode()
                elif event.key == pygame.K_f:
                    # Toggle favorites (example)
                    if self.selected_card:
                        self.selected_card.favorite = not self.selected_card.favorite
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check card selection
                    for i, card in enumerate(self.visible_cards):
                        card_rect = self._get_card_rect(i)
                        if card_rect.collidepoint(mouse_pos):
                            self.selected_card = card
                            self._handle_action(HallAction.VIEW_CARD_DETAILS, card)
                            break
            
            elif event.type == pygame.MOUSEWHEEL:
                # Smooth scrolling
                scroll_amount = event.y * 60
                self.scroll_velocity -= scroll_amount
    
    def render(self, surface: pygame.Surface):
        """Render the enhanced Hall of Gods."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Divine particles
        for particle in self.particles:
            alpha = int(particle['alpha'] * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill(particle['color'])
            particle_surface.set_alpha(alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Title
        responsive_typography.render_text(
            "HALL OF THE GODS", TextStyle.TITLE_LARGE, surface,
            (SCREEN_CENTER[0], 80), center=True, custom_color=Colors.GOLD
        )
        
        # Collection stats
        total_cards = len(self.all_cards)
        filtered_count = len(self.filtered_cards)
        responsive_typography.render_text(
            f"Collection: {filtered_count}/{total_cards} Cards",
            TextStyle.SUBTITLE, surface,
            (SCREEN_CENTER[0], 110), center=True, custom_color=Colors.PAPYRUS
        )
        
        # Filter buttons
        self._render_filter_buttons(surface)
        
        # Search box
        self._render_search_box(surface)
        
        # Card grid/list
        if self.view_mode == ViewMode.GRID:
            self._render_card_grid(surface)
        else:
            self._render_card_list(surface)
        
        # Selected card details
        if self.selected_card:
            self._render_card_details(surface)
        
        # Control buttons
        for button in self.control_buttons:
            button.render(surface, pygame.font.Font(None, FontSizes.BUTTON))
        
        # Instructions
        instruction_text = "Mouse Wheel: Scroll • Click: Select Card • TAB: Change View • F: Favorite • ESC: Back"
        responsive_typography.render_text(
            instruction_text, TextStyle.TOOLTIP, surface,
            (SCREEN_CENTER[0], SCREEN_HEIGHT - 30), center=True, custom_color=Colors.DESERT_SAND
        )
        
        # Fade-in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
    
    def _render_filter_buttons(self, surface: pygame.Surface):
        """Render filter button sections."""
        # God filters
        responsive_typography.render_text(
            "GODS:", TextStyle.CARD_TEXT, surface,
            (self.grid_start_x - 40, 155), custom_color=Colors.GOLD
        )
        
        for button in self.filter_buttons['god']:
            # Highlight active filter
            if button.text.lower() == self.current_god_filter:
                button.glow_intensity = 1.0
            else:
                button.glow_intensity = 0.0
            button.render(surface, pygame.font.Font(None, FontSizes.CARD_TEXT))
        
        # Rarity filters
        responsive_typography.render_text(
            "RARITY:", TextStyle.CARD_TEXT, surface,
            (self.grid_start_x - 40, 190), custom_color=Colors.LAPIS_LAZULI
        )
        
        for button in self.filter_buttons['rarity']:
            if button.text.lower() == self.current_rarity_filter:
                button.glow_intensity = 1.0
            else:
                button.glow_intensity = 0.0
            button.render(surface, pygame.font.Font(None, FontSizes.CARD_TEXT))
        
        # Type filters
        responsive_typography.render_text(
            "TYPE:", TextStyle.CARD_TEXT, surface,
            (self.grid_start_x - 40, 225), custom_color=Colors.PURPLE
        )
        
        for button in self.filter_buttons['type']:
            if button.text.lower() == self.current_type_filter:
                button.glow_intensity = 1.0
            else:
                button.glow_intensity = 0.0
            button.render(surface, pygame.font.Font(None, FontSizes.CARD_TEXT))
    
    def _render_search_box(self, surface: pygame.Surface):
        """Render search input box."""
        search_rect = self.search_box['rect']
        
        # Background
        pygame.draw.rect(surface, Colors.BACKGROUND_SECONDARY, search_rect)
        pygame.draw.rect(surface, Colors.GOLD, search_rect, 2)
        
        # Search text
        search_text = self.search_box['text'] or "Search cards..."
        text_color = Colors.PAPYRUS if self.search_box['text'] else Colors.GRAY
        
        responsive_typography.render_text(
            search_text, TextStyle.CARD_TEXT, surface,
            (search_rect.x + 10, search_rect.centery), custom_color=text_color
        )
        
        # Label
        responsive_typography.render_text(
            "SEARCH:", TextStyle.CARD_TEXT, surface,
            (search_rect.x - 60, search_rect.centery), custom_color=Colors.DESERT_SAND
        )
    
    def _render_card_grid(self, surface: pygame.Surface):
        """Render cards in grid layout."""
        for i, card in enumerate(self.visible_cards):
            card_rect = self._get_card_rect(i)
            
            # Skip cards outside viewport
            if card_rect.bottom < self.grid_start_y - 50 or card_rect.top > SCREEN_HEIGHT + 50:
                continue
            
            # Apply hover animation
            scale = self.card_hover_scale.get(card, 1.0)
            if scale > 1.0:
                # Scale around center
                scaled_size = (int(card_rect.width * scale), int(card_rect.height * scale))
                scaled_rect = pygame.Rect(0, 0, *scaled_size)
                scaled_rect.center = card_rect.center
                card_rect = scaled_rect
            
            self._render_card_compact(surface, card, card_rect)
    
    def _render_card_list(self, surface: pygame.Surface):
        """Render cards in list layout."""
        for i, card in enumerate(self.visible_cards):
            card_rect = self._get_card_rect(i)
            
            if card_rect.bottom < self.grid_start_y - 50 or card_rect.top > SCREEN_HEIGHT + 50:
                continue
            
            self._render_card_list_item(surface, card, card_rect)
    
    def _render_card_compact(self, surface: pygame.Surface, card: CardInfo, rect: pygame.Rect):
        """Render a card in compact grid format."""
        # Card background
        rarity_colors = {
            "common": Colors.GRAY,
            "rare": Colors.LAPIS_LAZULI,
            "epic": Colors.PURPLE,
            "legendary": Colors.GOLD
        }
        
        card_color = rarity_colors.get(card.rarity, Colors.GRAY)
        
        # Card border and background
        pygame.draw.rect(surface, Colors.BACKGROUND_SECONDARY, rect)
        pygame.draw.rect(surface, card_color, rect, 3)
        
        # Selection highlight
        if card == self.selected_card:
            glow_rect = rect.inflate(10, 10)
            pygame.draw.rect(surface, Colors.GOLD, glow_rect, 5)
        
        # Card name
        name_y = rect.y + 10
        responsive_typography.render_text(
            card.name, TextStyle.CARD_NAME, surface,
            (rect.centerx, name_y), center=True, custom_color=card_color
        )
        
        # Mana cost (top right)
        if card.cost > 0:
            cost_circle = pygame.Rect(rect.right - 30, rect.y + 5, 25, 25)
            pygame.draw.circle(surface, Colors.LAPIS_LAZULI, cost_circle.center, 12)
            responsive_typography.render_text(
                str(card.cost), TextStyle.CARD_TEXT, surface,
                cost_circle.center, center=True, custom_color=Colors.WHITE
            )
        
        # Attack/Health (bottom)
        if card.attack > 0 or card.health > 0:
            stats_y = rect.bottom - 25
            stats_text = f"{card.attack}/{card.health}"
            responsive_typography.render_text(
                stats_text, TextStyle.CARD_TEXT, surface,
                (rect.centerx, stats_y), center=True, custom_color=Colors.PAPYRUS
            )
        
        # Card type icon (bottom left)
        type_icons = {
            "deity": "♦",
            "creature": "♠", 
            "spell": "♥",
            "artifact": "♣"
        }
        
        if card.card_type in type_icons:
            responsive_typography.render_text(
                type_icons[card.card_type], TextStyle.CARD_NAME, surface,
                (rect.x + 15, rect.bottom - 20), custom_color=card_color
            )
        
        # Copies owned (top left)
        if card.copies_owned > 1:
            responsive_typography.render_text(
                f"x{card.copies_owned}", TextStyle.TOOLTIP, surface,
                (rect.x + 5, rect.y + 5), custom_color=Colors.GOLD
            )
        
        # Favorite indicator
        if card.favorite:
            responsive_typography.render_text(
                "★", TextStyle.CARD_TEXT, surface,
                (rect.right - 15, rect.y + 35), custom_color=Colors.GOLD
            )
    
    def _render_card_list_item(self, surface: pygame.Surface, card: CardInfo, rect: pygame.Rect):
        """Render a card as a list item."""
        # Background
        bg_color = Colors.BACKGROUND_SECONDARY if card != self.selected_card else Colors.GOLD
        alpha = 100 if card != self.selected_card else 50
        
        list_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        list_surface.fill(bg_color)
        list_surface.set_alpha(alpha)
        surface.blit(list_surface, rect)
        
        # Border
        border_color = Colors.GOLD if card == self.selected_card else Colors.GRAY
        pygame.draw.rect(surface, border_color, rect, 2)
        
        # Card info layout
        name_x = rect.x + 10
        responsive_typography.render_text(
            card.name, TextStyle.CARD_NAME, surface,
            (name_x, rect.y + 10), custom_color=Colors.GOLD
        )
        
        # Stats and details
        details = f"{card.rarity.title()} {card.card_type.title()} | Cost: {card.cost}"
        if card.attack > 0 or card.health > 0:
            details += f" | {card.attack}/{card.health}"
        
        responsive_typography.render_text(
            details, TextStyle.CARD_TEXT, surface,
            (name_x, rect.y + 30), custom_color=Colors.PAPYRUS
        )
        
        # Description
        responsive_typography.render_text(
            card.description, TextStyle.TOOLTIP, surface,
            (name_x, rect.y + 50), custom_color=Colors.DESERT_SAND
        )
    
    def _render_card_details(self, surface: pygame.Surface):
        """Render detailed view of selected card."""
        if not self.selected_card:
            return
        
        # Details panel on the right
        panel_rect = pygame.Rect(SCREEN_WIDTH - 400, 250, 350, 500)
        
        # Panel background
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(Colors.BACKGROUND_SECONDARY)
        panel_surface.set_alpha(220)
        surface.blit(panel_surface, panel_rect)
        
        # Panel border
        pygame.draw.rect(surface, Colors.GOLD, panel_rect, 3)
        
        card = self.selected_card
        y_offset = panel_rect.y + 20
        
        # Card name
        responsive_typography.render_text(
            card.name, TextStyle.SUBTITLE, surface,
            (panel_rect.centerx, y_offset), center=True, custom_color=Colors.GOLD
        )
        y_offset += 40
        
        # Card details
        details = [
            f"Rarity: {card.rarity.title()}",
            f"Type: {card.card_type.title()}",
            f"God: {card.god.title()}",
            f"Cost: {card.cost}",
            f"Copies: {card.copies_owned}"
        ]
        
        if card.attack > 0 or card.health > 0:
            details.append(f"Attack/Health: {card.attack}/{card.health}")
        
        for detail in details:
            responsive_typography.render_text(
                detail, TextStyle.CARD_TEXT, surface,
                (panel_rect.x + 20, y_offset), custom_color=Colors.PAPYRUS
            )
            y_offset += 25
        
        y_offset += 20
        
        # Description
        responsive_typography.render_text(
            "Description:", TextStyle.CARD_NAME, surface,
            (panel_rect.x + 20, y_offset), custom_color=Colors.LAPIS_LAZULI
        )
        y_offset += 30
        
        # Word wrap description
        words = card.description.split()
        lines = []
        current_line = ""
        max_width = panel_rect.width - 40
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            responsive_typography.render_text(
                line, TextStyle.CARD_TEXT, surface,
                (panel_rect.x + 20, y_offset), custom_color=Colors.PAPYRUS
            )
            y_offset += 20
        
        y_offset += 20
        
        # Lore
        responsive_typography.render_text(
            "Lore:", TextStyle.CARD_NAME, surface,
            (panel_rect.x + 20, y_offset), custom_color=Colors.PURPLE
        )
        y_offset += 30
        
        # Word wrap lore
        words = card.lore.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            responsive_typography.render_text(
                line, TextStyle.TOOLTIP, surface,
                (panel_rect.x + 20, y_offset), custom_color=Colors.DESERT_SAND
            )
            y_offset += 18
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.animation_time = 0.0
        self.grid_animation_progress = 0.0
        self.card_hover_scale.clear()
        
        # Start ambient music
        audio_manager.play_music(AudioTrack.AMBIENT, fade_in=2.0)