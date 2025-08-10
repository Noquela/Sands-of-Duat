"""
HALL OF GODS - Professional Egyptian Collection Screen
Ultra-high resolution card gallery with Hades-level polish and Egyptian pantheon theming.
"""

import pygame
import math
import time
import random
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton

class HallAction(Enum):
    """Hall of Gods actions."""
    BACK_TO_MENU = auto()
    FILTER_ALL = auto()
    FILTER_LEGENDARY = auto()
    FILTER_EPIC = auto()
    FILTER_RARE = auto()
    FILTER_COMMON = auto()

@dataclass
class CollectionCard:
    """Card in the collection with display properties."""
    name: str
    rarity: str
    artwork: Optional[pygame.Surface]
    is_unlocked: bool
    god_domain: str
    lore_text: str
    x: float = 0
    y: float = 0
    hover_offset: float = 0
    glow_intensity: float = 0
    is_hovered: bool = False

class ProfessionalHallOfGods:
    """
    Stunning Hall of Gods collection screen showcasing ultra-high resolution Egyptian cards.
    Features animated card galleries, filtering, and immersive Egyptian pantheon atmosphere.
    """
    
    def __init__(self, on_action: Optional[Callable[[HallAction], None]] = None):
        """Initialize the Hall of Gods."""
        self.on_action = on_action
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.title_glow_phase = 0.0
        
        # Collection state
        self.selected_filter = "all"
        self.selected_card = None
        self.card_hover_time = 0.0
        
        # Create ultra-high resolution background
        self.background_surface = self._create_divine_background()
        
        # Initialize card collection
        self.collection_cards = self._initialize_card_collection()
        
        # UI elements
        self.buttons = self._create_buttons()
        self.filter_buttons = self._create_filter_buttons()
        
        # Divine particles
        self.divine_particles = []
        self._spawn_divine_particles()
        
        # Update card positions
        self._update_card_positions()
        
        print("[HALL] Hall of Gods initialized - Behold the Egyptian pantheon in ultra-HD!")
    
    def _create_divine_background(self) -> pygame.Surface:
        """Create ultra-high resolution divine Egyptian pantheon background."""
        # Try to load the ultra-high resolution Hall of Gods background (4096x2048)
        asset_loader = get_asset_loader()
        hall_bg = asset_loader.load_background('hall_of_gods')
        
        if hall_bg:
            # Scale ultra-high resolution background with quality
            background = pygame.transform.smoothscale(hall_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add divine atmospheric overlay for Hall of Gods ambiance
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Divine gradient overlay with Egyptian pantheon atmosphere
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                alpha = int(30 + ratio * 20)  # Subtle darkening for divine readability
                # Golden divine light from top
                red_tint = int(15 + (1 - ratio) * 10)
                blue_tint = int(5 + ratio * 15)
                overlay.fill((red_tint, 8, blue_tint, alpha), (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            return background
        
        # Enhanced fallback: Divine Egyptian pantheon hall theme
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Divine gradient with Egyptian golden hour
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            # Divine golden hall colors
            r = int(40 + ratio * 20)  # Golden temple stones
            g = int(30 + ratio * 25)  # Warm divine light
            b = int(60 + ratio * 30)  # Deep sacred blues
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add divine temple pattern overlay
        pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, 150):
            for y in range(0, SCREEN_HEIGHT, 150):
                # Divine column patterns
                pygame.draw.rect(pattern_surface, (*Colors.GOLD, 15), (x, y, 12, 120))
                pygame.draw.rect(pattern_surface, (*Colors.GOLD, 15), (x, y + 130, 40, 8))
        
        background.blit(pattern_surface, (0, 0))
        return background
    
    def _initialize_card_collection(self) -> List[CollectionCard]:
        """Initialize the divine card collection with ultra-high resolution artwork."""
        asset_loader = get_asset_loader()
        
        # Egyptian pantheon card collection with lore
        divine_cards = [
            # Legendary Gods
            {
                'name': 'RA - SUN GOD', 'rarity': 'legendary', 
                'god_domain': 'Solar Divinity', 
                'lore': 'The supreme sun god, ruler of the heavens and creator of all life.'
            },
            {
                'name': 'ANUBIS - JUDGE OF THE DEAD', 'rarity': 'legendary',
                'god_domain': 'Death & Judgment', 
                'lore': 'Guardian of the underworld, weigher of hearts against the feather of truth.'
            },
            {
                'name': 'ISIS - DIVINE MOTHER', 'rarity': 'legendary',
                'god_domain': 'Magic & Motherhood', 
                'lore': 'Goddess of magic, motherhood, and healing. Resurrector of Osiris.'
            },
            {
                'name': 'SET - CHAOS GOD', 'rarity': 'legendary',
                'god_domain': 'Chaos & Storm', 
                'lore': 'God of chaos, storms, and the desert. Eternal rival of Osiris.'
            },
            
            # Epic Heroes
            {
                'name': 'EGYPTIAN WARRIOR', 'rarity': 'epic',
                'god_domain': 'Mortal Champion', 
                'lore': 'Elite warrior blessed by the gods, defender of the pharaoh.'
            },
            {
                'name': "PHARAOH'S GUARD", 'rarity': 'epic',
                'god_domain': 'Royal Protection', 
                'lore': 'Sacred guardian of the divine pharaoh, sworn to eternal service.'
            },
            
            # Rare Creatures
            {
                'name': 'MUMMY GUARDIAN', 'rarity': 'rare',
                'god_domain': 'Undead Sentinel', 
                'lore': 'Ancient guardian risen from eternal rest to protect sacred tombs.'
            },
            {
                'name': 'SPHINX GUARDIAN', 'rarity': 'rare',
                'god_domain': 'Riddle Keeper', 
                'lore': 'Wise sentinel of ancient knowledge, keeper of eternal riddles.'
            },
        ]
        
        collection = []
        for card_data in divine_cards:
            # Try to load ultra-high resolution artwork
            artwork = asset_loader.load_card_art_by_name(card_data['name'])
            
            card = CollectionCard(
                name=card_data['name'],
                rarity=card_data['rarity'],
                artwork=artwork,
                is_unlocked=True,  # All cards unlocked for showcase
                god_domain=card_data['god_domain'],
                lore_text=card_data['lore']
            )
            collection.append(card)
        
        return collection
    
    def _spawn_divine_particles(self):
        """Spawn divine floating particles for Hall of Gods atmosphere."""
        for _ in range(25):
            self.divine_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(2, 5),
                'speed': random.randint(15, 40),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.LAPIS_LAZULI, Colors.PAPYRUS]),
                'alpha_base': random.randint(40, 120)
            })
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create divine UI buttons."""
        buttons = []
        
        # Back button with Egyptian styling
        back_button = AnimatedButton(
            50, 50, 180, 50,
            "<- RETURN TO MORTAL REALM", FontSizes.BUTTON,
            action=lambda: self._handle_action(HallAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        return buttons
    
    def _create_filter_buttons(self) -> List[AnimatedButton]:
        """Create divine filter buttons for card rarities."""
        buttons = []
        
        filter_configs = [
            ("ALL DIVINE", HallAction.FILTER_ALL, "all"),
            ("LEGENDARY", HallAction.FILTER_LEGENDARY, "legendary"),
            ("EPIC", HallAction.FILTER_EPIC, "epic"),
            ("RARE", HallAction.FILTER_RARE, "rare"),
        ]
        
        button_width = 150
        button_height = 40
        spacing = 20
        start_x = SCREEN_CENTER[0] - ((len(filter_configs) * (button_width + spacing)) // 2)
        
        for i, (text, action, filter_type) in enumerate(filter_configs):
            x = start_x + i * (button_width + spacing)
            y = 120
            
            button = AnimatedButton(
                x, y, button_width, button_height,
                text, FontSizes.CARD_TEXT,
                action=lambda a=action, f=filter_type: self._handle_filter_action(a, f)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_action(self, action: HallAction):
        """Handle divine action."""
        if self.on_action:
            self.on_action(action)
    
    def _handle_filter_action(self, action: HallAction, filter_type: str):
        """Handle filter selection."""
        self.selected_filter = filter_type
        self._update_card_positions()
        audio_manager.play_sound(SoundEffect.BUTTON_HOVER, 0.4)
    
    def _get_filtered_cards(self) -> List[CollectionCard]:
        """Get cards matching current filter."""
        if self.selected_filter == "all":
            return self.collection_cards
        return [card for card in self.collection_cards if card.rarity == self.selected_filter]
    
    def _update_card_positions(self):
        """Update card positions in divine formation."""
        filtered_cards = self._get_filtered_cards()
        
        # Divine grid layout optimized for ultrawide
        cards_per_row = 6 if Layout.IS_ULTRAWIDE else 4
        card_spacing = 20
        card_display_size = 180
        
        # Center the grid in content area
        total_width = cards_per_row * card_display_size + (cards_per_row - 1) * card_spacing
        start_x = SCREEN_CENTER[0] - total_width // 2
        start_y = 200
        
        for i, card in enumerate(filtered_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            card.x = start_x + col * (card_display_size + card_spacing)
            card.y = start_y + row * (card_display_size * 1.3 + card_spacing)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the divine Hall of Gods."""
        self.animation_time += dt
        self.title_glow_phase += dt * 2
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 1.5)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update divine particles
        for particle in self.divine_particles:
            particle['x'] += math.sin(self.animation_time * 0.5 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.5
            
            # Wrap around screen
            if particle['x'] < 0: particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH: particle['x'] = 0
            if particle['y'] < 0: particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT: particle['y'] = 0
        
        # Update card animations
        self.selected_card = None
        for card in self._get_filtered_cards():
            card_rect = pygame.Rect(card.x, card.y, 180, 250)
            card.is_hovered = card_rect.collidepoint(mouse_pos)
            
            if card.is_hovered:
                self.selected_card = card
                self.card_hover_time += dt
                
            # Smooth hover animations
            target_offset = -15 if card.is_hovered else 0
            card.hover_offset += (target_offset - card.hover_offset) * dt * 8
            
            target_glow = 1.0 if card.is_hovered else 0.0
            card.glow_intensity += (target_glow - card.glow_intensity) * dt * 6
        
        # Update buttons
        for button in self.buttons + self.filter_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(HallAction.BACK_TO_MENU)
                elif event.key == pygame.K_1:
                    self._handle_filter_action(HallAction.FILTER_ALL, "all")
                elif event.key == pygame.K_2:
                    self._handle_filter_action(HallAction.FILTER_LEGENDARY, "legendary")
                elif event.key == pygame.K_3:
                    self._handle_filter_action(HallAction.FILTER_EPIC, "epic")
                elif event.key == pygame.K_4:
                    self._handle_filter_action(HallAction.FILTER_RARE, "rare")
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle button clicks
                for button in self.buttons + self.filter_buttons:
                    if button.handle_click(mouse_pos):
                        break
    
    def render(self, surface: pygame.Surface):
        """Render the divine Hall of Gods."""
        # Ultra-high resolution background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide divine bars
        if Layout.IS_ULTRAWIDE:
            self._render_divine_ultrawide_bars(surface)
        
        # Divine particles
        self._render_divine_particles(surface)
        
        # Divine title with pulsing glow
        self._render_divine_title(surface)
        
        # Filter buttons
        self._render_filter_buttons(surface)
        
        # Divine card collection
        self._render_divine_cards(surface)
        
        # Selected card details
        if self.selected_card:
            self._render_card_details(surface)
        
        # UI buttons
        for button in self.buttons:
            button.render(surface)
        
        # Divine instructions
        self._render_divine_instructions(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_divine_ultrawide_bars(self, surface: pygame.Surface):
        """Render divine ultrawide sidebar decorations."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # Divine hall pattern
        pattern_color = (15, 10, 25)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Divine column decorations
        for bar_rect in [left_bar, right_bar]:
            center_x = bar_rect.centerx
            
            # Divine pillars
            pillar_width = min(40, bar_rect.width - 20)
            pillar_rect = pygame.Rect(center_x - pillar_width//2, 100, pillar_width, SCREEN_HEIGHT - 200)
            
            # Pillar surface with divine texture
            pillar_surface = pygame.Surface((pillar_width, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
            pillar_surface.fill((*Colors.GOLD, 30))
            
            # Divine hieroglyphic patterns
            for y in range(50, SCREEN_HEIGHT - 250, 80):
                pattern_y = y - 100
                if 0 <= pattern_y <= SCREEN_HEIGHT - 300:
                    # Egyptian divine symbols
                    pygame.draw.circle(pillar_surface, (*Colors.GOLD, 60), (pillar_width//2, pattern_y), 8, 2)
                    pygame.draw.rect(pillar_surface, (*Colors.GOLD, 60), (pillar_width//2 - 12, pattern_y + 15, 24, 3))
            
            surface.blit(pillar_surface, pillar_rect.topleft)
    
    def _render_divine_particles(self, surface: pygame.Surface):
        """Render divine floating particles."""
        for particle in self.divine_particles:
            alpha = int(particle['alpha_base'] + 60 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*particle['color'], alpha))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_divine_title(self, surface: pygame.Surface):
        """Render divine title with Egyptian theming."""
        # Main title with divine glow
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_text = "[HALL OF GODS]"
        
        # Pulsing divine glow
        glow_intensity = int(150 + 100 * abs(math.sin(self.title_glow_phase)))
        
        # Draw glow effect
        glow_surface = font.render(title_text, True, Colors.GOLD)
        glow_surface.set_alpha(glow_intensity // 3)
        for offset in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2)]:
            glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0] + offset[0], 80 + offset[1]))
            surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 80))
        surface.blit(title_surface, title_rect)
    
    def _render_filter_buttons(self, surface: pygame.Surface):
        """Render divine filter buttons."""
        for i, button in enumerate(self.filter_buttons):
            # Highlight selected filter
            filter_types = ["all", "legendary", "epic", "rare"]
            if i < len(filter_types) and filter_types[i] == self.selected_filter:
                highlight_rect = button.rect.inflate(8, 8)
                pygame.draw.rect(surface, Colors.GOLD, highlight_rect, 3)
            
            button.render(surface)
    
    def _render_divine_cards(self, surface: pygame.Surface):
        """Render the divine card collection with ultra-high resolution artwork."""
        for card in self._get_filtered_cards():
            if not card.is_unlocked:
                continue
                
            card_rect = pygame.Rect(card.x, card.y + card.hover_offset, 180, 250)
            
            # Divine glow effect for hovered cards
            if card.glow_intensity > 0:
                glow_rect = card_rect.inflate(int(20 * card.glow_intensity), int(20 * card.glow_intensity))
                glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                glow_alpha = int(100 * card.glow_intensity)
                
                for i in range(5):
                    inner_rect = pygame.Rect(i, i, glow_rect.width - i*2, glow_rect.height - i*2)
                    pygame.draw.rect(glow_surface, (*Colors.GOLD, glow_alpha // (i+1)), inner_rect, 1)
                
                surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
            
            # Card background
            pygame.draw.rect(surface, Colors.PAPYRUS, card_rect)
            
            # Rarity border
            rarity_colors = {
                'legendary': Colors.GOLD,
                'epic': (138, 43, 226),
                'rare': (65, 105, 225),
                'common': Colors.DESERT_SAND
            }
            border_color = rarity_colors.get(card.rarity, Colors.DESERT_SAND)
            pygame.draw.rect(surface, border_color, card_rect, 4)
            
            # Ultra-high resolution artwork
            if card.artwork:
                art_rect = pygame.Rect(card.x + 10, card.y + card.hover_offset + 10, 160, 120)
                # Quality scaling from ultra-high resolution
                scaled_artwork = pygame.transform.smoothscale(card.artwork, (art_rect.width, art_rect.height))
                surface.blit(scaled_artwork, art_rect)
                pygame.draw.rect(surface, Colors.GOLD, art_rect, 2)
            
            # Card name
            name_font = pygame.font.Font(None, 18)
            name_text = name_font.render(card.name, True, Colors.BLACK)
            name_rect = name_text.get_rect(center=(card.x + 90, card.y + card.hover_offset + 150))
            surface.blit(name_text, name_rect)
            
            # God domain
            domain_font = pygame.font.Font(None, 14)
            domain_text = domain_font.render(card.god_domain, True, Colors.LAPIS_LAZULI)
            domain_rect = domain_text.get_rect(center=(card.x + 90, card.y + card.hover_offset + 170))
            surface.blit(domain_text, domain_rect)
            
            # Rarity indicator
            rarity_text = domain_font.render(card.rarity.upper(), True, border_color)
            rarity_rect = rarity_text.get_rect(center=(card.x + 90, card.y + card.hover_offset + 230))
            surface.blit(rarity_text, rarity_rect)
    
    def _render_card_details(self, surface: pygame.Surface):
        """Render detailed information for selected card."""
        if not self.selected_card:
            return
        
        # Detail panel background
        panel_width = 400
        panel_height = 200
        panel_x = SCREEN_WIDTH - panel_width - 50
        panel_y = SCREEN_HEIGHT - panel_height - 50
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Divine panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*Colors.BLACK, 180))
        pygame.draw.rect(panel_surface, Colors.GOLD, (0, 0, panel_width, panel_height), 3)
        surface.blit(panel_surface, (panel_x, panel_y))
        
        # Card details
        y_offset = panel_y + 20
        
        # Name
        name_font = pygame.font.Font(None, 24)
        name_text = name_font.render(self.selected_card.name, True, Colors.GOLD)
        surface.blit(name_text, (panel_x + 20, y_offset))
        y_offset += 30
        
        # Domain
        domain_font = pygame.font.Font(None, 18)
        domain_text = domain_font.render(f"Domain: {self.selected_card.god_domain}", True, Colors.LAPIS_LAZULI)
        surface.blit(domain_text, (panel_x + 20, y_offset))
        y_offset += 25
        
        # Lore (wrapped text)
        lore_font = pygame.font.Font(None, 16)
        words = self.selected_card.lore_text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if lore_font.size(test_line)[0] <= panel_width - 40:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines[:4]:  # Max 4 lines
            lore_text = lore_font.render(line, True, Colors.PAPYRUS)
            surface.blit(lore_text, (panel_x + 20, y_offset))
            y_offset += 18
    
    def _render_divine_instructions(self, surface: pygame.Surface):
        """Render divine control instructions."""
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        
        instructions = [
            "1-4: Filter by Rarity  •  ESC: Return to Menu",
            f"Collection: {len([c for c in self.collection_cards if c.is_unlocked])}/{len(self.collection_cards)} Divine Cards",
            "Hover over cards to view divine lore and domains"
        ]
        
        y = SCREEN_HEIGHT - 80
        for instruction in instructions:
            text_surface = font.render(instruction, True, Colors.DESERT_SAND)
            text_rect = text_surface.get_rect(center=(SCREEN_CENTER[0], y))
            
            # Subtle background
            bg_rect = text_rect.inflate(20, 6)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 120))
            surface.blit(bg_surface, bg_rect.topleft)
            
            surface.blit(text_surface, text_rect)
            y += 22
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        self.title_glow_phase = 0.0
        
        for button in self.buttons + self.filter_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0
        
        # Start divine ambiance music
        audio_manager.play_music(AudioTrack.MENU, fade_in=2.0)