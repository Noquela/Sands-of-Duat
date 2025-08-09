#!/usr/bin/env python3
"""
SANDS OF DUAT - CARD DISPLAY SYSTEM
==================================

Premium card display system showcasing authentic Egyptian god artwork.
Uses high-quality god assets from final_dataset for card visuals.
"""

import pygame
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# Import our updated asset loader
from ...core.asset_loader import get_asset_loader

@dataclass
class CardData:
    """Data structure for Egyptian god cards."""
    name: str
    title: str
    cost: int
    attack: int
    health: int
    rarity: str  # 'common', 'rare', 'legendary'
    description: str
    artwork_file: str
    god_type: str  # 'major', 'minor', 'guardian'

class EgyptianCard:
    """Individual card with authentic Egyptian god artwork."""
    
    def __init__(self, card_data: CardData, position: Tuple[int, int] = (0, 0)):
        self.data = card_data
        self.position = position
        self.size = (200, 300)  # Standard card size
        self.hover_offset = 0
        self.is_hovered = False
        self.is_selected = False
        self.click_animation = 0
        
        # Egyptian colors (must be defined before loading artwork)
        self.colors = {
            'GOLD': (255, 215, 0),
            'GOLD_DARK': (184, 134, 11),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'RARE_PURPLE': (138, 43, 226),
            'LEGENDARY_ORANGE': (255, 140, 0)
        }
        
        # Rarity colors
        self.rarity_colors = {
            'common': self.colors['DESERT_SAND'],
            'rare': self.colors['RARE_PURPLE'],
            'epic': self.colors['LAPIS_LAZULI'],
            'legendary': self.colors['LEGENDARY_ORANGE']
        }
        
        # Load artwork (after colors are defined)
        self.artwork = self._load_artwork()
        self.card_surface = None
        self._render_card()
    
    def _load_artwork(self) -> Optional[pygame.Surface]:
        """Load the generated card artwork."""
        asset_loader = get_asset_loader()
        
        # Try loading by card name first
        artwork = asset_loader.load_card_art_by_name(self.data.name)
        if artwork:
            # Scale to fit card artwork area
            return pygame.transform.scale(artwork, (160, 120))
        
        # Fallback: try by rarity
        artwork = asset_loader.get_random_card_art_by_rarity(self.data.rarity)
        if artwork:
            return pygame.transform.scale(artwork, (160, 120))
        
        # Final fallback artwork
        fallback = pygame.Surface((160, 120))
        fallback.fill(self.colors['LAPIS_LAZULI'])
        return fallback
    
    def _render_card(self):
        """Render the complete card with Egyptian styling."""
        self.card_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        # Card background with Egyptian border
        card_rect = pygame.Rect(0, 0, *self.size)
        
        # Main background
        pygame.draw.rect(self.card_surface, self.colors['PAPYRUS'], card_rect)
        
        # Rarity border
        border_color = self.rarity_colors.get(self.data.rarity, self.colors['DESERT_SAND'])
        pygame.draw.rect(self.card_surface, border_color, card_rect, 4)
        
        # Egyptian decorative corners
        self._draw_egyptian_corners(self.card_surface, card_rect, border_color)
        
        # Cost crystal (top left)
        cost_pos = (15, 15)
        self._draw_cost_crystal(self.card_surface, cost_pos, self.data.cost)
        
        # Artwork area
        if self.artwork:
            artwork_pos = (20, 50)
            self.card_surface.blit(self.artwork, artwork_pos)
        
        # Artwork border
        artwork_rect = pygame.Rect(20, 50, 160, 120)
        pygame.draw.rect(self.card_surface, self.colors['GOLD'], artwork_rect, 2)
        
        # Card name
        font_name = pygame.font.Font(None, 24)
        name_surface = font_name.render(self.data.name.upper(), True, self.colors['BLACK'])
        name_pos = (self.size[0] // 2 - name_surface.get_width() // 2, 180)
        self.card_surface.blit(name_surface, name_pos)
        
        # Card title
        font_title = pygame.font.Font(None, 16)
        title_surface = font_title.render(self.data.title, True, self.colors['GOLD_DARK'])
        title_pos = (self.size[0] // 2 - title_surface.get_width() // 2, 200)
        self.card_surface.blit(title_surface, title_pos)
        
        # Stats (Attack/Health)
        self._draw_stats(self.card_surface)
        
        # Description
        self._draw_description(self.card_surface)
    
    def _draw_egyptian_corners(self, surface: pygame.Surface, rect: pygame.Rect, 
                              color: Tuple[int, int, int]):
        """Draw Egyptian-style decorative corners."""
        corner_size = 15
        thickness = 3
        
        # Top-left corner
        pygame.draw.lines(surface, color, False, [
            (rect.left + corner_size, rect.top + thickness),
            (rect.left + thickness, rect.top + thickness),
            (rect.left + thickness, rect.top + corner_size)
        ], thickness)
        
        # Top-right corner  
        pygame.draw.lines(surface, color, False, [
            (rect.right - corner_size, rect.top + thickness),
            (rect.right - thickness, rect.top + thickness),
            (rect.right - thickness, rect.top + corner_size)
        ], thickness)
        
        # Bottom-left corner
        pygame.draw.lines(surface, color, False, [
            (rect.left + corner_size, rect.bottom - thickness),
            (rect.left + thickness, rect.bottom - thickness),
            (rect.left + thickness, rect.bottom - corner_size)
        ], thickness)
        
        # Bottom-right corner
        pygame.draw.lines(surface, color, False, [
            (rect.right - corner_size, rect.bottom - thickness),
            (rect.right - thickness, rect.bottom - thickness),
            (rect.right - thickness, rect.bottom - corner_size)
        ], thickness)
    
    def _draw_cost_crystal(self, surface: pygame.Surface, pos: Tuple[int, int], cost: int):
        """Draw Egyptian-style mana cost crystal."""
        crystal_rect = pygame.Rect(pos[0], pos[1], 30, 30)
        
        # Crystal background
        pygame.draw.ellipse(surface, self.colors['LAPIS_LAZULI'], crystal_rect)
        pygame.draw.ellipse(surface, self.colors['GOLD'], crystal_rect, 2)
        
        # Cost number
        font = pygame.font.Font(None, 24)
        cost_surface = font.render(str(cost), True, self.colors['WHITE'])
        cost_pos = (pos[0] + 15 - cost_surface.get_width() // 2,
                   pos[1] + 15 - cost_surface.get_height() // 2)
        surface.blit(cost_surface, cost_pos)
    
    def _draw_stats(self, surface: pygame.Surface):
        """Draw attack and health stats."""
        font = pygame.font.Font(None, 28)
        
        # Attack (bottom-left)
        attack_surface = font.render(str(self.data.attack), True, self.colors['BLACK'])
        attack_bg = pygame.Rect(10, self.size[1] - 40, 30, 30)
        pygame.draw.ellipse(surface, self.colors['DESERT_SAND'], attack_bg)
        pygame.draw.ellipse(surface, self.colors['GOLD'], attack_bg, 2)
        attack_pos = (25 - attack_surface.get_width() // 2, 
                     self.size[1] - 25 - attack_surface.get_height() // 2)
        surface.blit(attack_surface, attack_pos)
        
        # Health (bottom-right)
        health_surface = font.render(str(self.data.health), True, self.colors['BLACK'])
        health_bg = pygame.Rect(self.size[0] - 40, self.size[1] - 40, 30, 30)
        pygame.draw.ellipse(surface, self.colors['LAPIS_LAZULI'], health_bg)
        pygame.draw.ellipse(surface, self.colors['GOLD'], health_bg, 2)
        health_pos = (self.size[0] - 25 - health_surface.get_width() // 2,
                     self.size[1] - 25 - health_surface.get_height() // 2)
        surface.blit(health_surface, health_pos)
    
    def _draw_description(self, surface: pygame.Surface):
        """Draw card description text."""
        font = pygame.font.Font(None, 14)
        words = self.data.description.split()
        lines = []
        current_line = []
        line_width = 0
        max_width = self.size[0] - 20
        
        for word in words:
            word_surface = font.render(word + " ", True, self.colors['BLACK'])
            word_width = word_surface.get_width()
            
            if line_width + word_width <= max_width:
                current_line.append(word)
                line_width += word_width
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                line_width = word_width
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Draw lines
        y_offset = 225
        for line in lines[:3]:  # Max 3 lines
            line_surface = font.render(line, True, self.colors['BLACK'])
            x_pos = self.size[0] // 2 - line_surface.get_width() // 2
            surface.blit(line_surface, (x_pos, y_offset))
            y_offset += 15
    
    def update(self, dt: float):
        """Update card animations."""
        # Hover animation
        target_offset = -20 if self.is_hovered else 0
        self.hover_offset += (target_offset - self.hover_offset) * dt * 8
        
        # Click animation
        if self.click_animation > 0:
            self.click_animation -= dt * 3
            if self.click_animation < 0:
                self.click_animation = 0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the card. Returns True if event was handled."""
        card_rect = pygame.Rect(*self.position, *self.size)
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = card_rect.collidepoint(event.pos)
            return self.is_hovered
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if card_rect.collidepoint(event.pos):
                self.click_animation = 1.0
                return True
                
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw the card with current animations."""
        if not self.card_surface:
            return
            
        draw_pos = (self.position[0], self.position[1] + int(self.hover_offset))
        
        # Click animation scale
        if self.click_animation > 0:
            scale = 1.0 + self.click_animation * 0.1
            scaled_size = (int(self.size[0] * scale), int(self.size[1] * scale))
            scaled_surface = pygame.transform.scale(self.card_surface, scaled_size)
            offset_x = (scaled_size[0] - self.size[0]) // 2
            offset_y = (scaled_size[1] - self.size[1]) // 2
            surface.blit(scaled_surface, (draw_pos[0] - offset_x, draw_pos[1] - offset_y))
        else:
            surface.blit(self.card_surface, draw_pos)
        
        # Hover glow effect
        if self.is_hovered:
            glow_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            glow_surface.fill((255, 255, 255, 30))
            surface.blit(glow_surface, draw_pos)


class CardCollection:
    """Manages a collection of Egyptian god cards."""
    
    def __init__(self):
        self.cards = []
        self._load_egyptian_gods()
    
    def _load_egyptian_gods(self):
        """Load all available Egyptian god cards from assets."""
        # Define Egyptian god cards using our generated artwork
        god_cards = [
            # Legendary Cards
            CardData(
                name="Ra - Sun God", 
                title="Creator of Light",
                cost=8, attack=10, health=12, rarity="legendary",
                description="At dawn, deal 3 damage to all enemies. Divine radiance cannot be extinguished.",
                artwork_file="ra_sun_god.png",
                god_type="major"
            ),
            CardData(
                name="Anubis - Judgment", 
                title="Guardian of the Dead",
                cost=6, attack=8, health=8, rarity="legendary",
                description="When a creature dies, gain +2/+2. Judge the souls of the fallen.",
                artwork_file="anubis_judgment.png",
                god_type="major"
            ),
            CardData(
                name="Osiris - Resurrection", 
                title="Lord of the Underworld",
                cost=7, attack=6, health=10, rarity="legendary",
                description="Resurrect all dead friendly creatures with 1 health. Death is but a door.",
                artwork_file="osiris_resurrection.png",
                god_type="major"
            ),
            CardData(
                name="Horus - Divine Sight", 
                title="Sky God of Vengeance",
                cost=5, attack=7, health=6, rarity="legendary",
                description="Flying. When played, deal 4 damage to target enemy. The falcon strikes swift.",
                artwork_file="horus_divine_sight.png",
                god_type="major"
            ),
            CardData(
                name="Isis - Protection", 
                title="Goddess of Magic",
                cost=4, attack=4, health=6, rarity="legendary",
                description="Restore 5 health to all friendly creatures. Ancient magic flows eternal.",
                artwork_file="isis_protection.png",
                god_type="major"
            ),
            
            # Epic Cards
            CardData(
                name="Thoth - Wisdom", 
                title="God of Knowledge",
                cost=4, attack=2, health=8, rarity="epic",
                description="Draw 2 cards. Knowledge is the greatest weapon of all.",
                artwork_file="thoth_wisdom.png",
                god_type="minor"
            ),
            CardData(
                name="Bastet - Feline Grace", 
                title="Protector Goddess",
                cost=3, attack=3, health=4, rarity="epic",
                description="Summon two 1/1 sacred cats. Feline grace protects the innocent.",
                artwork_file="bastet_feline_grace.png",
                god_type="guardian"
            ),
            CardData(
                name="Sekhmet - War Cry", 
                title="Lioness of War",
                cost=6, attack=9, health=5, rarity="epic",
                description="Destroy target creature. The lioness knows no mercy in battle.",
                artwork_file="sekhmet_war_cry.png",
                god_type="major"
            ),
            CardData(
                name="Set - Chaos Storm", 
                title="God of Chaos",
                cost=5, attack=8, health=4, rarity="epic",
                description="Deal 2 damage to all creatures. Chaos consumes order.",
                artwork_file="set_chaos_storm.png",
                god_type="major"
            ),
            CardData(
                name="Pharaoh - Divine Mandate", 
                title="Ruler of Egypt",
                cost=7, attack=6, health=8, rarity="epic",
                description="All friendly creatures gain +1/+1. The pharaoh's will commands.",
                artwork_file="pharaoh_divine_mandate.png",
                god_type="major"
            ),
            
            # Rare Cards
            CardData(
                name="Mummy Wrath", 
                title="Undead Guardian",
                cost=4, attack=5, health=3, rarity="rare",
                description="When destroyed, return to hand. The dead do not rest.",
                artwork_file="mummy_wrath.png",
                god_type="guardian"
            ),
            CardData(
                name="Scarab Swarm", 
                title="Desert Plague",
                cost=3, attack=2, health=2, rarity="rare",
                description="Summon three 1/1 scarab tokens. The swarm devours all.",
                artwork_file="scarab_swarm.png",
                god_type="minor"
            ),
            
            # Common Cards
            CardData(
                name="Sacred Scarab", 
                title="Holy Beetle",
                cost=1, attack=1, health=1, rarity="common",
                description="Draw a card when played. Sacred wisdom flows through all things.",
                artwork_file="sacred_scarab.png",
                god_type="minor"
            ),
            CardData(
                name="Desert Meditation", 
                title="Spiritual Focus",
                cost=2, attack=0, health=3, rarity="common",
                description="Restore 3 health. Inner peace brings strength.",
                artwork_file="desert_meditation.png",
                god_type="minor"
            ),
            CardData(
                name="Papyrus Scroll", 
                title="Ancient Wisdom",
                cost=1, attack=0, health=1, rarity="common",
                description="Draw a card. The wisdom of ages flows through papyrus.",
                artwork_file="papyrus_scroll.png",
                god_type="minor"
            )
        ]
        
        # Create card objects
        for card_data in god_cards:
            self.cards.append(EgyptianCard(card_data))
    
    def get_cards_by_rarity(self, rarity: str) -> List[EgyptianCard]:
        """Get all cards of specified rarity."""
        return [card for card in self.cards if card.data.rarity == rarity]
    
    def get_card_by_name(self, name: str) -> Optional[EgyptianCard]:
        """Get specific card by name."""
        for card in self.cards:
            if card.data.name == name:
                return card
        return None


def create_card_collection() -> CardCollection:
    """Factory function to create Egyptian god card collection."""
    return CardCollection()