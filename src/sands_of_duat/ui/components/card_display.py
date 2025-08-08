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

# Asset paths
ASSETS_ROOT = Path(__file__).parent.parent.parent.parent.parent / "assets"
FINAL_DATASET_PATH = ASSETS_ROOT / "images" / "lora_training" / "final_dataset"

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
        
        # Load artwork
        self.artwork = self._load_artwork()
        self.card_surface = None
        self._render_card()
        
        # Egyptian colors
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
            'legendary': self.colors['LEGENDARY_ORANGE']
        }
    
    def _load_artwork(self) -> Optional[pygame.Surface]:
        """Load the authentic Egyptian god artwork."""
        artwork_path = FINAL_DATASET_PATH / self.data.artwork_file
        if artwork_path.exists():
            try:
                artwork = pygame.image.load(str(artwork_path))
                # Scale to fit card artwork area
                return pygame.transform.scale(artwork, (160, 120))
            except pygame.error as e:
                print(f"Could not load artwork {self.data.artwork_file}: {e}")
        
        # Fallback artwork
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
        # Define Egyptian god cards with their authentic artwork
        god_cards = [
            CardData(
                name="RA", 
                title="Sun God of Creation",
                cost=8, attack=10, health=12, rarity="legendary",
                description="At dawn, deal 3 damage to all enemies. Divine radiance cannot be extinguished.",
                artwork_file="egyptian_god_ra_01_q81.png",
                god_type="major"
            ),
            CardData(
                name="ANUBIS", 
                title="Guardian of the Dead",
                cost=6, attack=8, health=8, rarity="legendary",
                description="When a creature dies, gain +2/+2. Judge the souls of the fallen.",
                artwork_file="egyptian_god_anubis_02_q75.png",
                god_type="major"
            ),
            CardData(
                name="HORUS", 
                title="Sky God of Vengeance",
                cost=5, attack=7, health=6, rarity="rare",
                description="Flying. When played, deal 4 damage to target enemy. The falcon strikes swift.",
                artwork_file="egyptian_god_horus_06_q77.png",
                god_type="major"
            ),
            CardData(
                name="ISIS", 
                title="Goddess of Magic",
                cost=4, attack=4, health=6, rarity="rare",
                description="Restore 5 health to all friendly creatures. Ancient magic flows eternal.",
                artwork_file="egyptian_god_isis_04_q76.png",
                god_type="major"
            ),
            CardData(
                name="OSIRIS", 
                title="Lord of the Underworld",
                cost=7, attack=6, health=10, rarity="legendary",
                description="Resurrect all dead friendly creatures with 1 health. Death is but a door.",
                artwork_file="egyptian_god_osiris_05_q76.png",
                god_type="major"
            ),
            CardData(
                name="BASTET", 
                title="Protector Goddess",
                cost=3, attack=3, health=4, rarity="common",
                description="Summon two 1/1 sacred cats. Feline grace protects the innocent.",
                artwork_file="egyptian_god_bastet_08_q73.png",
                god_type="guardian"
            ),
            CardData(
                name="THOTH", 
                title="God of Wisdom",
                cost=4, attack=2, health=8, rarity="rare",
                description="Draw 2 cards. Knowledge is the greatest weapon of all.",
                artwork_file="egyptian_god_thoth_03_q74.png",
                god_type="minor"
            ),
            CardData(
                name="SEKHMET", 
                title="Lioness of War",
                cost=6, attack=9, health=5, rarity="rare",
                description="Destroy target creature. The lioness knows no mercy in battle.",
                artwork_file="egyptian_god_sekhmet_09_q77.png",
                god_type="major"
            ),
            CardData(
                name="SOBEK", 
                title="Crocodile God",
                cost=5, attack=6, health=7, rarity="common",
                description="When attacked, deal 2 damage to attacker. The Nile's fury unleashed.",
                artwork_file="egyptian_god_sobek_10_q74.png",
                god_type="guardian"
            ),
            CardData(
                name="PTAH", 
                title="Creator of Crafts",
                cost=3, attack=2, health=5, rarity="common",
                description="Create a random artifact card. The craftsman's touch brings wonders.",
                artwork_file="egyptian_god_ptah_12_q74.png",
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