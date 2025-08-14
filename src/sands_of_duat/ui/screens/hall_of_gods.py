"""
Hall of Gods - Professional Collection Screen with Egyptian theming.
Display all unlocked cards with detailed information and Egyptian lore.
"""

import pygame
import math
from typing import List, Optional, Tuple, Callable, Dict
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton
from ..components.enhanced_ui_components import EgyptianPanel, CardPreviewPanel
from ..effects.advanced_visual_effects import advanced_visual_effects

class HallAction(Enum):
    """Hall of Gods actions."""
    BACK_TO_MENU = auto()
    FILTER_BY_GOD = auto()
    FILTER_BY_RARITY = auto()
    VIEW_LORE = auto()

@dataclass
class CardInfo:
    """Extended card information for collection."""
    name: str
    rarity: str
    god: str
    cost: int
    attack: int
    health: int
    description: str
    lore: str
    unlocked: bool = True
    discovered: bool = True
    
    def __hash__(self):
        """Make CardInfo hashable based on name (unique identifier)."""
        return hash(self.name)

class HallOfGodsScreen:
    """
    Professional Hall of Gods collection screen.
    Features Egyptian theming, detailed card views, and mythological lore.
    """
    
    def __init__(self, on_action: Optional[Callable[[HallAction], None]] = None):
        """Initialize Hall of Gods screen."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Background
        self.background_surface = self._create_background()
        
        # UI State
        self.current_filter = "all"  # all, ra, anubis, isis, set, etc.
        self.current_rarity_filter = "all"  # all, common, rare, epic, legendary
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Card collection
        self.all_cards = self._create_card_collection()
        self.filtered_cards = self.all_cards.copy()
        
        # Layout
        self.setup_layout()
        
        # UI Components
        self.buttons = self._create_control_buttons()
        self.god_filter_buttons = self._create_god_filters()
        self.rarity_filter_buttons = self._create_rarity_filters()
        self.card_preview = CardPreviewPanel(
            SCREEN_WIDTH - 350, 150, 330, 500
        )
        
        # Selected card
        self.selected_card = None
        self.hovered_card = None
        
        print("Hall of Gods initialized - Divine Collection Ready")
    
    def setup_layout(self):
        """Setup layout areas for different screen components."""
        # Main collection area (left side)
        margin = 50 if not Layout.IS_ULTRAWIDE else Layout.CONTENT_X_OFFSET + 50
        collection_width = (SCREEN_WIDTH - 400) if not Layout.IS_ULTRAWIDE else (Layout.UI_SAFE_WIDTH - 400)
        
        self.collection_area = pygame.Rect(
            margin, 180, collection_width, SCREEN_HEIGHT - 280
        )
        
        # Preview area (right side)
        preview_x = self.collection_area.right + 20
        self.preview_area = pygame.Rect(
            preview_x, 150, 350, SCREEN_HEIGHT - 200
        )
        
        # Filter areas
        self.god_filter_area = pygame.Rect(margin, 120, collection_width, 30)
        self.rarity_filter_area = pygame.Rect(margin, 150, collection_width, 25)
    
    def _create_background(self) -> pygame.Surface:
        """Create the Hall of Gods background."""
        # Load Hall of Gods 4K background
        hall_bg = self.asset_loader.load_background('hall_of_gods')
        
        if hall_bg:
            # Scale to screen with quality
            background = pygame.transform.smoothscale(hall_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add mystical overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Gradient for mystical atmosphere
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                alpha = int(30 + ratio * 15)  # Subtle darkening
                overlay.fill((5, 0, 15, alpha), (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            return background
        
        # Fallback: Create mystical Egyptian hall
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Deep purple/blue gradient for divine atmosphere
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 + ratio * 10)   # Deep purples
            g = int(10 + ratio * 15)   # Mystical blues
            b = int(40 + ratio * 20)   # Rich blues
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _create_card_collection(self) -> List[CardInfo]:
        """Create the divine card collection."""
        cards = [
            # Ra - Sun God Cards
            CardInfo("RA - SUN GOD", "legendary", "ra", 8, 10, 12,
                    "Deal 3 damage at dawn to all enemies",
                    "Ra, the falcon-headed sun god, travels across the sky in his solar barque, bringing light to the world and driving away the forces of chaos."),
            
            CardInfo("PYRAMID POWER", "epic", "ra", 5, 6, 4,
                    "Gain +2/+2 for each pyramid on field",
                    "The great pyramids channel Ra's divine energy, amplifying the power of those who serve the sun god."),
            
            # Anubis - Death God Cards  
            CardInfo("ANUBIS - JUDGE OF THE DEAD", "legendary", "anubis", 6, 8, 8,
                    "When a creature dies, gain +2/+2",
                    "Anubis weighs the hearts of the dead against the feather of Ma'at, determining their fate in the afterlife."),
            
            CardInfo("JUDGMENT SCALE", "rare", "anubis", 4, 3, 6,
                    "Destroy target creature with cost 4 or less",
                    "The scales of justice never lie. Those found wanting are consumed by Ammit the devourer."),
            
            # Isis - Magic Goddess Cards
            CardInfo("ISIS - DIVINE MOTHER", "legendary", "isis", 7, 5, 10,
                    "Restore 5 health to all friendly creatures",
                    "Isis, mistress of magic and healing, protects the faithful with her divine wings and sacred spells."),
            
            CardInfo("HEALING BLESSING", "common", "isis", 2, 0, 0,
                    "Restore 8 health to target",
                    "The gentle touch of Isis can mend even the most grievous wounds, bringing life from near death."),
            
            # Set - Chaos God Cards
            CardInfo("SET - CHAOS GOD", "legendary", "set", 7, 9, 6,
                    "Deal 2 damage to all creatures when played",
                    "Set, god of chaos and storms, brings destruction and discord wherever he treads."),
            
            CardInfo("DESERT STORM", "epic", "set", 5, 4, 3,
                    "Deal 4 damage to all enemy creatures",
                    "Set commands the fury of the desert, sending sandstorms to bury his enemies."),
            
            # Common Creatures
            CardInfo("EGYPTIAN WARRIOR", "common", "general", 3, 4, 4,
                    "Steadfast defender of the pharaoh",
                    "Elite soldiers who guard the temples and serve the gods with unwavering loyalty."),
            
            CardInfo("MUMMY GUARDIAN", "rare", "anubis", 4, 3, 7,
                    "Returns to hand when destroyed",
                    "Ancient guardians bound by sacred wrappings, they rise again and again to protect the tombs."),
            
            CardInfo("SPHINX GUARDIAN", "rare", "general", 5, 6, 5,
                    "Cannot be targeted by spells",
                    "Wise and ancient, the sphinx poses riddles to those who would pass. Answer incorrectly and face their wrath."),
            
            CardInfo("PHARAOH'S GUARD", "epic", "general", 6, 7, 6,
                    "Other friendly creatures gain +1/+1",
                    "The pharaoh's personal guards, blessed by the gods and trained in the deadliest combat arts."),
        ]
        
        # Determine unlock status (for demo, all are unlocked)
        for card in cards:
            card.unlocked = True
            card.discovered = True
            
        return cards
    
    def _create_control_buttons(self) -> List[AnimatedButton]:
        """Create main control buttons."""
        buttons = []
        
        button_configs = [
            ("RETURN TO REALM", HallAction.BACK_TO_MENU),
        ]
        
        button_width = 180
        button_height = 50
        start_x = SCREEN_WIDTH - button_width - 50
        
        for i, (text, action) in enumerate(button_configs):
            y = 50 + i * (button_height + 15)
            button = AnimatedButton(
                start_x, y, button_width, button_height, text, FontSizes.BUTTON,
                action=lambda a=action: self._handle_action(a)
            )
            buttons.append(button)
        
        return buttons
    
    def _create_god_filters(self) -> List[AnimatedButton]:
        """Create god filter buttons."""
        buttons = []
        gods = [("ALL", "all"), ("RA", "ra"), ("ANUBIS", "anubis"), ("ISIS", "isis"), ("SET", "set")]
        
        button_width = 80
        button_height = 25
        spacing = 10
        start_x = self.god_filter_area.x
        
        for i, (text, god) in enumerate(gods):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, self.god_filter_area.y, button_width, button_height, 
                text, FontSizes.CARD_TEXT,
                action=lambda g=god: self._filter_by_god(g)
            )
            buttons.append(button)
        
        return buttons
    
    def _create_rarity_filters(self) -> List[AnimatedButton]:
        """Create rarity filter buttons.""" 
        buttons = []
        rarities = [("ALL", "all"), ("COMMON", "common"), ("RARE", "rare"), 
                   ("EPIC", "epic"), ("LEGENDARY", "legendary")]
        
        button_width = 80
        button_height = 20
        spacing = 8
        start_x = self.rarity_filter_area.x
        
        for i, (text, rarity) in enumerate(rarities):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, self.rarity_filter_area.y, button_width, button_height,
                text, int(FontSizes.CARD_TEXT * 0.8),
                action=lambda r=rarity: self._filter_by_rarity(r)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_action(self, action: HallAction):
        """Handle button actions."""
        if self.on_action:
            self.on_action(action)
    
    def _filter_by_god(self, god: str):
        """Filter cards by god."""
        self.current_filter = god
        self.scroll_offset = 0
        self._update_filtered_cards()
    
    def _filter_by_rarity(self, rarity: str):
        """Filter cards by rarity."""
        self.current_rarity_filter = rarity
        self.scroll_offset = 0
        self._update_filtered_cards()
    
    def _update_filtered_cards(self):
        """Update the list of filtered cards."""
        self.filtered_cards = []
        
        for card in self.all_cards:
            # God filter
            if self.current_filter != "all" and card.god != self.current_filter:
                continue
                
            # Rarity filter
            if self.current_rarity_filter != "all" and card.rarity != self.current_rarity_filter:
                continue
                
            # Only show discovered cards
            if card.discovered:
                self.filtered_cards.append(card)
        
        # Update scroll limits
        cards_per_row = 5 if Layout.IS_ULTRAWIDE else 4
        rows = (len(self.filtered_cards) + cards_per_row - 1) // cards_per_row
        card_height = 150
        card_spacing = 20
        total_height = rows * (card_height + card_spacing)
        self.max_scroll = max(0, total_height - self.collection_area.height)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the Hall of Gods."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update buttons
        for button_list in [self.buttons, self.god_filter_buttons, self.rarity_filter_buttons]:
            for button in button_list:
                button.update(dt, mouse_pos, mouse_pressed)
        
        # Update card preview
        self.card_preview.update(dt)
        
        # Handle card hovering
        self._update_card_hover(mouse_pos)
        
        # Handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks
                clicked = False
                for button_list in [self.buttons, self.god_filter_buttons, self.rarity_filter_buttons]:
                    for button in button_list:
                        if button.handle_click(mouse_pos):
                            audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.5)
                            clicked = True
                            break
                    if clicked:
                        break
                
                # Check card clicks
                if not clicked:
                    self._handle_card_click(mouse_pos)
            
            elif event.type == pygame.MOUSEWHEEL:
                if self.collection_area.collidepoint(mouse_pos):
                    self.scroll_offset -= event.y * 40
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Initial filter setup
        if not hasattr(self, '_initial_filter_done'):
            self._update_filtered_cards()
            self._initial_filter_done = True
    
    def _update_card_hover(self, mouse_pos: Tuple[int, int]):
        """Update card hover states."""
        self.hovered_card = None
        
        if not self.collection_area.collidepoint(mouse_pos):
            return
        
        # Calculate card positions and check hover
        cards_per_row = 5 if Layout.IS_ULTRAWIDE else 4
        card_width = 120
        card_height = 150
        card_spacing = 20
        
        for i, card in enumerate(self.filtered_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.collection_area.x + col * (card_width + card_spacing)
            y = self.collection_area.y + row * (card_height + card_spacing) - self.scroll_offset
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            
            if card_rect.collidepoint(mouse_pos) and self.collection_area.colliderect(card_rect):
                self.hovered_card = card
                if card != self.selected_card:
                    self.card_preview.show_card(card.name, {
                        'cost': card.cost,
                        'attack': card.attack,
                        'health': card.health,
                        'rarity': card.rarity,
                        'description': card.description,
                        'lore': card.lore
                    })
                break
    
    def _handle_card_click(self, mouse_pos: Tuple[int, int]):
        """Handle card clicks."""
        if self.hovered_card:
            self.selected_card = self.hovered_card
            audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.4)
            
            # Add divine selection visual effects
            card_x = self.card_grid_area.x + (self.hovered_card.x * self.card_spacing_x)
            card_y = self.card_grid_area.y + (self.hovered_card.y * self.card_spacing_y)
            
            # Divine aura for legendary cards
            if self.selected_card.rarity.lower() == 'legendary':
                advanced_visual_effects.add_divine_aura(
                    card_x + self.card_width // 2, 
                    card_y + self.card_height // 2,
                    radius=120, color=Colors.GOLD
                )
                advanced_visual_effects.add_ankh_blessing(
                    card_x + self.card_width // 2, 
                    card_y + self.card_height // 2
                )
            else:
                # Energy pulse for other cards
                advanced_visual_effects.add_energy_pulse(
                    card_x + self.card_width // 2, 
                    card_y + self.card_height // 2,
                    max_radius=80, color=Colors.LAPIS_LAZULI
                )
            
            # Crystal shine effect
            advanced_visual_effects.add_crystal_shine(
                card_x, card_y, self.card_width, self.card_height
            )
            
            # Show detailed card info
            self.card_preview.show_card(self.selected_card.name, {
                'cost': self.selected_card.cost,
                'attack': self.selected_card.attack,
                'health': self.selected_card.health,
                'rarity': self.selected_card.rarity,
                'description': self.selected_card.description,
                'lore': self.selected_card.lore
            })
    
    def render(self, surface: pygame.Surface):
        """Render the Hall of Gods."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide decorations
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_decorations(surface)
        
        # Title
        self._render_title(surface)
        
        # Stats panel
        self._render_stats_panel(surface)
        
        # Filter buttons with highlights
        self._render_filter_buttons(surface)
        
        # Collection area
        self._render_collection_area(surface)
        
        # Cards
        self._render_cards(surface)
        
        # Preview panel
        self.card_preview.render(surface)
        
        # Control buttons
        for button in self.buttons:
            button.render(surface)
        
        # Instructions
        self._render_instructions(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_ultrawide_decorations(self, surface: pygame.Surface):
        """Render ultrawide decorations."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        # Side panels with divine decorations
        left_panel = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_panel = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        panel_color = (10, 5, 20)
        pygame.draw.rect(surface, panel_color, left_panel)
        pygame.draw.rect(surface, panel_color, right_panel)
        
        # Divine symbols
        glow_alpha = int(80 + 40 * abs(math.sin(self.animation_time * 2)))
        
        for panel_rect in [left_panel, right_panel]:
            center_x = panel_rect.centerx
            
            # Ankh symbols
            for y in [200, 400, 600, 800]:
                if y < SCREEN_HEIGHT:
                    pygame.draw.circle(surface, (*Colors.GOLD, glow_alpha), 
                                     (center_x, y), 8, 2)
                    pygame.draw.line(surface, (*Colors.GOLD, glow_alpha),
                                   (center_x, y - 15), (center_x, y + 15), 3)
                    pygame.draw.line(surface, (*Colors.GOLD, glow_alpha),
                                   (center_x - 10, y + 5), (center_x + 10, y + 5), 3)
    
    def _render_title(self, surface: pygame.Surface):
        """Render the main title."""
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "HALL OF GODS"
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.LAPIS_LAZULI)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 50))
        glow_surface.set_alpha(150)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 48))
        surface.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, FontSizes.BODY)
        subtitle_surface = subtitle_font.render("Divine Collection of Sacred Cards", True, Colors.PAPYRUS)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_CENTER[0], 80))
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _render_stats_panel(self, surface: pygame.Surface):
        """Render collection statistics."""
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        
        # Calculate stats
        total_cards = len(self.all_cards)
        unlocked_cards = len([c for c in self.all_cards if c.unlocked])
        legendary_cards = len([c for c in self.all_cards if c.rarity == "legendary" and c.unlocked])
        
        stats_text = f"Collection: {unlocked_cards}/{total_cards} • Legendary: {legendary_cards} • Filtered: {len(self.filtered_cards)}"
        stats_surface = font.render(stats_text, True, Colors.DESERT_SAND)
        stats_rect = stats_surface.get_rect(center=(SCREEN_CENTER[0], 100))
        surface.blit(stats_surface, stats_rect)
    
    def _render_filter_buttons(self, surface: pygame.Surface):
        """Render filter buttons with active highlights."""
        # God filters
        for i, button in enumerate(self.god_filter_buttons):
            # Highlight active filter
            if hasattr(button, 'action') and button.action:
                try:
                    # Check if this is the active god filter
                    if hasattr(button.action, '__closure__') and button.action.__closure__:
                        god_value = button.action.__closure__[0].cell_contents
                        if god_value == self.current_filter:
                            highlight_rect = button.rect.inflate(4, 4)
                            pygame.draw.rect(surface, Colors.GOLD, highlight_rect, 2)
                except:
                    pass
            button.render(surface)
        
        # Rarity filters
        for button in self.rarity_filter_buttons:
            # Highlight active filter
            if hasattr(button, 'action') and button.action:
                try:
                    if hasattr(button.action, '__closure__') and button.action.__closure__:
                        rarity_value = button.action.__closure__[0].cell_contents
                        if rarity_value == self.current_rarity_filter:
                            highlight_rect = button.rect.inflate(4, 4)
                            pygame.draw.rect(surface, Colors.LAPIS_LAZULI, highlight_rect, 2)
                except:
                    pass
            button.render(surface)
    
    def _render_collection_area(self, surface: pygame.Surface):
        """Render the collection area background."""
        # Semi-transparent panel
        panel_surface = pygame.Surface(self.collection_area.size, pygame.SRCALPHA)
        panel_surface.fill((*Colors.BLACK, 100))
        surface.blit(panel_surface, self.collection_area.topleft)
        
        # Ornate border
        pygame.draw.rect(surface, Colors.GOLD, self.collection_area, 3)
        
        # Inner decoration
        inner_rect = self.collection_area.inflate(-10, -10)
        pygame.draw.rect(surface, (*Colors.GOLD, 50), inner_rect, 1)
    
    def _render_cards(self, surface: pygame.Surface):
        """Render cards in the collection."""
        if not self.filtered_cards:
            # No cards message
            font = pygame.font.Font(None, FontSizes.SUBTITLE)
            no_cards_text = "No cards match current filters"
            no_cards_surface = font.render(no_cards_text, True, Colors.DESERT_SAND)
            no_cards_rect = no_cards_surface.get_rect(center=self.collection_area.center)
            surface.blit(no_cards_surface, no_cards_rect)
            return
        
        # Set clipping for scrolling
        original_clip = surface.get_clip()
        surface.set_clip(self.collection_area)
        
        cards_per_row = 5 if Layout.IS_ULTRAWIDE else 4
        card_width = 120
        card_height = 150
        card_spacing = 20
        
        for i, card in enumerate(self.filtered_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.collection_area.x + col * (card_width + card_spacing)
            y = self.collection_area.y + row * (card_height + card_spacing) - self.scroll_offset
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            
            # Skip if not visible
            if not self.collection_area.colliderect(card_rect):
                continue
            
            self._render_single_card(surface, card, card_rect)
        
        surface.set_clip(original_clip)
    
    def _render_single_card(self, surface: pygame.Surface, card: CardInfo, rect: pygame.Rect):
        """Render a single card in the collection."""
        # Card background
        if card.unlocked:
            bg_color = Colors.PAPYRUS
        else:
            bg_color = (50, 50, 50)  # Locked card
        
        pygame.draw.rect(surface, bg_color, rect)
        
        # Rarity border
        rarity_colors = {
            'common': Colors.DESERT_SAND,
            'rare': (138, 43, 226),
            'epic': (255, 140, 0),
            'legendary': Colors.GOLD
        }
        border_color = rarity_colors.get(card.rarity, Colors.DESERT_SAND)
        
        # Glow effect for hovered/selected cards
        if card == self.hovered_card or card == self.selected_card:
            glow_rect = rect.inflate(6, 6)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((*border_color, 100))
            surface.blit(glow_surface, glow_rect.topleft)
        
        pygame.draw.rect(surface, border_color, rect, 3)
        
        if card.unlocked:
            # Try to load card artwork
            artwork = self.asset_loader.load_card_art_by_name(card.name)
            if artwork:
                art_rect = pygame.Rect(rect.x + 10, rect.y + 20, rect.width - 20, 80)
                scaled_artwork = pygame.transform.smoothscale(artwork, (art_rect.width, art_rect.height))
                surface.blit(scaled_artwork, art_rect)
                pygame.draw.rect(surface, border_color, art_rect, 2)
            else:
                # Placeholder
                placeholder_rect = pygame.Rect(rect.x + 10, rect.y + 20, rect.width - 20, 80)
                pygame.draw.rect(surface, Colors.LAPIS_LAZULI, placeholder_rect)
                pygame.draw.rect(surface, border_color, placeholder_rect, 2)
            
            # Card name
            font = pygame.font.Font(None, 16)
            name_text = card.name[:15] + "..." if len(card.name) > 15 else card.name
            name_surface = font.render(name_text, True, Colors.BLACK)
            name_rect = name_surface.get_rect(centerx=rect.centerx, y=rect.y + 105)
            surface.blit(name_surface, name_rect)
            
            # Stats
            stats_font = pygame.font.Font(None, 14)
            stats_text = f"{card.cost}⚡ {card.attack}⚔️ {card.health}❤️"
            stats_surface = stats_font.render(stats_text, True, Colors.BLACK)
            stats_rect = stats_surface.get_rect(centerx=rect.centerx, y=rect.y + 125)
            surface.blit(stats_surface, stats_rect)
            
        else:
            # Locked card
            lock_font = pygame.font.Font(None, 48)
            lock_surface = lock_font.render("🔒", True, Colors.GOLD)
            lock_rect = lock_surface.get_rect(center=rect.center)
            surface.blit(lock_surface, lock_rect)
    
    def _render_instructions(self, surface: pygame.Surface):
        """Render helpful instructions."""
        instructions = [
            "Click cards to view detailed information and lore",
            "Use filters to organize your divine collection",
            "Mouse wheel to scroll through your cards"
        ]
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        y = SCREEN_HEIGHT - 90
        
        for instruction in instructions:
            text_surface = font.render(instruction, True, (*Colors.DESERT_SAND, 150))
            text_surface.set_alpha(150)
            text_rect = text_surface.get_rect(center=(SCREEN_CENTER[0], y))
            surface.blit(text_surface, text_rect)
            y += 20
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        # Reset button states
        for button_list in [self.buttons, self.god_filter_buttons, self.rarity_filter_buttons]:
            for button in button_list:
                button.hover_progress = 0.0
                button.press_progress = 0.0
        
        # Start mystical music
        audio_manager.play_music(AudioTrack.MENU, fade_in=2.0)