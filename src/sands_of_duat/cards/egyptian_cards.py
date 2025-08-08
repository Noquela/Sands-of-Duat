#!/usr/bin/env python3
"""
SANDS OF DUAT - EGYPTIAN CARD SYSTEM
===================================

Defines Egyptian-themed cards using the high-quality assets from final_dataset.
Creates a complete deck of Egyptian mythology cards with proper gameplay mechanics.
"""

import pygame
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

from ..core.asset_loader import get_asset_loader, AssetCategory

logger = logging.getLogger(__name__)

class CardType(Enum):
    """Types of Egyptian cards"""
    GOD = "god"
    ARTIFACT = "artifact"
    SPELL = "spell"
    LOCATION = "location"
    CREATURE = "creature"

class CardRarity(Enum):
    """Card rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon" 
    RARE = "rare"
    LEGENDARY = "legendary"

@dataclass
class CardStats:
    """Basic card statistics"""
    attack: int = 0
    health: int = 0
    cost: int = 0
    
class EgyptianCard:
    """
    Base class for all Egyptian-themed cards.
    
    Features:
    - High-quality artwork from final_dataset
    - Egyptian mythology theming
    - Balanced gameplay statistics
    - Rich flavor text
    """
    
    def __init__(self, name: str, card_type: CardType, rarity: CardRarity,
                 stats: CardStats, description: str, asset_category: AssetCategory,
                 asset_index: int = 0):
        self.name = name
        self.card_type = card_type
        self.rarity = rarity
        self.stats = stats
        self.description = description
        self.asset_category = asset_category
        self.asset_index = asset_index
        
        # Visual elements
        self._artwork: Optional[pygame.Surface] = None
        self._card_surface: Optional[pygame.Surface] = None
        
        # Gameplay elements
        self.keywords: List[str] = []
        self.flavor_text: str = ""
        
    def get_artwork(self) -> Optional[pygame.Surface]:
        """Get the card's artwork."""
        if self._artwork is None:
            asset_loader = get_asset_loader()
            self._artwork = asset_loader.load_card_art(self.asset_category, self.asset_index)
        return self._artwork
    
    def render_card(self, size: Tuple[int, int] = (300, 420)) -> pygame.Surface:
        """Render the complete card with artwork, stats, and text."""
        if self._card_surface is None or self._card_surface.get_size() != size:
            self._card_surface = self._create_card_surface(size)
        return self._card_surface
    
    def _create_card_surface(self, size: Tuple[int, int]) -> pygame.Surface:
        """Create the visual representation of the card."""
        width, height = size
        card_surface = pygame.Surface(size)
        
        # Egyptian color scheme
        colors = {
            'GOLD': (255, 215, 0),
            'PAPYRUS': (245, 245, 220),
            'DARK_BLUE': (25, 25, 112),
            'LAPIS_LAZULI': (26, 81, 171),
            'BORDER': (139, 69, 19)  # Brown border
        }
        
        # Card background based on rarity
        bg_color = colors['PAPYRUS']
        if self.rarity == CardRarity.RARE:
            bg_color = (245, 245, 245)  # Slightly brighter
        elif self.rarity == CardRarity.LEGENDARY:
            bg_color = (255, 250, 205)  # Golden tint
        
        card_surface.fill(bg_color)
        
        # Border
        border_width = 3
        pygame.draw.rect(card_surface, colors['BORDER'], 
                        (0, 0, width, height), border_width)
        
        # Get and draw artwork
        artwork = self.get_artwork()
        if artwork:
            # Scale artwork to fit in upper portion of card
            art_rect = pygame.Rect(border_width + 5, border_width + 25, 
                                 width - 2 * (border_width + 5), 
                                 int(height * 0.55))
            scaled_art = pygame.transform.scale(artwork, art_rect.size)
            card_surface.blit(scaled_art, art_rect)
        
        # Title area
        title_font = pygame.font.Font(None, 24)
        title_surface = title_font.render(self.name, True, colors['DARK_BLUE'])
        title_rect = title_surface.get_rect(centerx=width//2, y=5)
        card_surface.blit(title_surface, title_rect)
        
        # Stats area (bottom portion)
        stats_y = int(height * 0.75)
        
        # Cost (top-left corner)
        cost_font = pygame.font.Font(None, 36)
        cost_surface = cost_font.render(str(self.stats.cost), True, colors['GOLD'])
        cost_rect = pygame.Rect(5, 5, 30, 30)
        pygame.draw.ellipse(card_surface, colors['DARK_BLUE'], cost_rect)
        card_surface.blit(cost_surface, 
                         (cost_rect.centerx - cost_surface.get_width()//2,
                          cost_rect.centery - cost_surface.get_height()//2))
        
        # Attack and Health (for creatures/gods)
        if self.card_type in [CardType.GOD, CardType.CREATURE]:
            stats_font = pygame.font.Font(None, 32)
            
            # Attack (bottom-left)
            attack_surface = stats_font.render(str(self.stats.attack), True, colors['GOLD'])
            attack_rect = pygame.Rect(10, height - 40, 25, 25)
            pygame.draw.ellipse(card_surface, (178, 34, 34), attack_rect)  # Red
            card_surface.blit(attack_surface,
                             (attack_rect.centerx - attack_surface.get_width()//2,
                              attack_rect.centery - attack_surface.get_height()//2))
            
            # Health (bottom-right)
            health_surface = stats_font.render(str(self.stats.health), True, colors['GOLD'])
            health_rect = pygame.Rect(width - 35, height - 40, 25, 25)
            pygame.draw.ellipse(card_surface, (34, 139, 34), health_rect)  # Green
            card_surface.blit(health_surface,
                             (health_rect.centerx - health_surface.get_width()//2,
                              health_rect.centery - health_surface.get_height()//2))
        
        # Description text
        desc_font = pygame.font.Font(None, 16)
        desc_lines = self._wrap_text(self.description, desc_font, width - 20)
        desc_y = stats_y + 10
        
        for i, line in enumerate(desc_lines[:3]):  # Max 3 lines
            line_surface = desc_font.render(line, True, colors['DARK_BLUE'])
            card_surface.blit(line_surface, (10, desc_y + i * 18))
        
        return card_surface
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within the specified width."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

class EgyptianDeckBuilder:
    """
    Creates complete decks of Egyptian-themed cards using the available assets.
    """
    
    def __init__(self):
        self.asset_loader = get_asset_loader()
        self.all_cards: List[EgyptianCard] = []
        self._create_card_database()
    
    def _create_card_database(self):
        """Create the complete database of Egyptian cards."""
        logger.info("Creating Egyptian card database...")
        
        # God cards - Most powerful creatures
        god_cards = [
            EgyptianCard("Ra - Sun God", CardType.GOD, CardRarity.LEGENDARY,
                        CardStats(attack=8, health=8, cost=7),
                        "Lord of the heavens, bringer of light and life to all Egypt.",
                        AssetCategory.GODS, 0),
                        
            EgyptianCard("Anubis - Guide of the Dead", CardType.GOD, CardRarity.LEGENDARY,
                        CardStats(attack=6, health=7, cost=6),
                        "Guardian of the afterlife who weighs the hearts of the dead.",
                        AssetCategory.GODS, 1),
                        
            EgyptianCard("Horus - Sky God", CardType.GOD, CardRarity.RARE,
                        CardStats(attack=7, health=6, cost=6),
                        "Falcon-headed god of the sky and divine kingship.",
                        AssetCategory.GODS, 2),
                        
            EgyptianCard("Isis - Magic Goddess", CardType.GOD, CardRarity.RARE,
                        CardStats(attack=5, health=8, cost=6),
                        "Goddess of magic, motherhood, and healing.",
                        AssetCategory.GODS, 3),
                        
            EgyptianCard("Osiris - Lord of the Underworld", CardType.GOD, CardRarity.LEGENDARY,
                        CardStats(attack=7, health=9, cost=8),
                        "Ruler of the dead and judge of the afterlife.",
                        AssetCategory.GODS, 4),
                        
            EgyptianCard("Thoth - God of Wisdom", CardType.GOD, CardRarity.RARE,
                        CardStats(attack=4, health=6, cost=5),
                        "Keeper of divine knowledge and scribe of the gods.",
                        AssetCategory.GODS, 5),
        ]
        
        # Artifact cards - Powerful tools and treasures
        artifact_cards = [
            EgyptianCard("Ankh of Eternal Life", CardType.ARTIFACT, CardRarity.RARE,
                        CardStats(cost=3),
                        "Sacred symbol that grants its bearer protection from death.",
                        AssetCategory.ARTIFACTS, 0),
                        
            EgyptianCard("Canopic Jar", CardType.ARTIFACT, CardRarity.UNCOMMON,
                        CardStats(cost=2),
                        "Preserves the essence of fallen creatures for later use.",
                        AssetCategory.ARTIFACTS, 1),
                        
            EgyptianCard("Pharaoh's Scepter", CardType.ARTIFACT, CardRarity.RARE,
                        CardStats(cost=4),
                        "Grants the wielder command over lesser beings.",
                        AssetCategory.ARTIFACTS, 2),
                        
            EgyptianCard("Sacred Scarab", CardType.ARTIFACT, CardRarity.COMMON,
                        CardStats(cost=1),
                        "A protective amulet blessed by the gods.",
                        AssetCategory.ARTIFACTS, 3),
        ]
        
        # Location cards - Mystical places of power
        location_cards = [
            EgyptianCard("Valley of the Kings", CardType.LOCATION, CardRarity.RARE,
                        CardStats(cost=4),
                        "Sacred burial ground where pharaohs rest eternal.",
                        AssetCategory.UNDERWORLD_LOCATIONS, 0),
                        
            EgyptianCard("Temple of Karnak", CardType.LOCATION, CardRarity.UNCOMMON,
                        CardStats(cost=3),
                        "Vast temple complex dedicated to the god Amun.",
                        AssetCategory.UNDERWORLD_LOCATIONS, 1),
                        
            EgyptianCard("River of Souls", CardType.LOCATION, CardRarity.RARE,
                        CardStats(cost=5),
                        "The path through the underworld where souls are judged.",
                        AssetCategory.UNDERWORLD_LOCATIONS, 2),
                        
            EgyptianCard("Pyramid of Power", CardType.LOCATION, CardRarity.LEGENDARY,
                        CardStats(cost=6),
                        "Ancient monument that channels cosmic energy.",
                        AssetCategory.UNDERWORLD_LOCATIONS, 3),
        ]
        
        # Spell cards - Egyptian magic and myths
        spell_cards = [
            EgyptianCard("Curse of the Mummy", CardType.SPELL, CardRarity.COMMON,
                        CardStats(cost=2),
                        "Ancient curse that weakens enemies.",
                        AssetCategory.MYTHS, 0),
                        
            EgyptianCard("Blessing of Ra", CardType.SPELL, CardRarity.UNCOMMON,
                        CardStats(cost=3),
                        "Divine light that heals and strengthens allies.",
                        AssetCategory.MYTHS, 1),
                        
            EgyptianCard("Judgment of Osiris", CardType.SPELL, CardRarity.RARE,
                        CardStats(cost=4),
                        "Weighs the heart of target creature.",
                        AssetCategory.MYTHS, 2),
                        
            EgyptianCard("Sandstorm of Set", CardType.SPELL, CardRarity.UNCOMMON,
                        CardStats(cost=3),
                        "Chaotic storm that damages all enemies.",
                        AssetCategory.MYTHS, 3),
        ]
        
        # Creature cards - Egyptian mythological beings
        creature_cards = [
            EgyptianCard("Sacred Sphinx", CardType.CREATURE, CardRarity.RARE,
                        CardStats(attack=5, health=7, cost=5),
                        "Guardian of ancient secrets and riddles.",
                        AssetCategory.OBJECTS, 0),
                        
            EgyptianCard("Mummy Warrior", CardType.CREATURE, CardRarity.COMMON,
                        CardStats(attack=3, health=4, cost=3),
                        "Undead guardian wrapped in blessed linens.",
                        AssetCategory.OBJECTS, 1),
                        
            EgyptianCard("Desert Scorpion", CardType.CREATURE, CardRarity.COMMON,
                        CardStats(attack=2, health=1, cost=1),
                        "Venomous creature of the Egyptian sands.",
                        AssetCategory.OBJECTS, 2),
                        
            EgyptianCard("Crocodile of Sobek", CardType.CREATURE, CardRarity.UNCOMMON,
                        CardStats(attack=4, health=5, cost=4),
                        "Sacred crocodile blessed by the god Sobek.",
                        AssetCategory.OBJECTS, 3),
        ]
        
        # Combine all cards
        self.all_cards = god_cards + artifact_cards + location_cards + spell_cards + creature_cards
        
        logger.info(f"Created {len(self.all_cards)} Egyptian cards across {len(CardType)} types")
    
    def get_all_cards(self) -> List[EgyptianCard]:
        """Get all available cards."""
        return self.all_cards.copy()
    
    def get_cards_by_type(self, card_type: CardType) -> List[EgyptianCard]:
        """Get all cards of a specific type."""
        return [card for card in self.all_cards if card.card_type == card_type]
    
    def get_cards_by_rarity(self, rarity: CardRarity) -> List[EgyptianCard]:
        """Get all cards of a specific rarity."""
        return [card for card in self.all_cards if card.rarity == rarity]
    
    def create_starter_deck(self) -> List[EgyptianCard]:
        """Create a balanced starter deck for new players."""
        starter_deck = []
        
        # Add some of each card type for variety
        god_cards = self.get_cards_by_type(CardType.GOD)[:2]
        artifact_cards = self.get_cards_by_type(CardType.ARTIFACT)[:3]
        spell_cards = self.get_cards_by_type(CardType.SPELL)[:4]
        creature_cards = self.get_cards_by_type(CardType.CREATURE)[:4]
        location_cards = self.get_cards_by_type(CardType.LOCATION)[:2]
        
        starter_deck.extend(god_cards)
        starter_deck.extend(artifact_cards)
        starter_deck.extend(spell_cards)
        starter_deck.extend(creature_cards)
        starter_deck.extend(location_cards)
        
        logger.info(f"Created starter deck with {len(starter_deck)} cards")
        return starter_deck
    
    def create_random_deck(self, deck_size: int = 20) -> List[EgyptianCard]:
        """Create a random deck of specified size."""
        import random
        return random.sample(self.all_cards, min(deck_size, len(self.all_cards)))

# Global deck builder instance
_deck_builder: Optional[EgyptianDeckBuilder] = None

def get_deck_builder() -> EgyptianDeckBuilder:
    """Get the global deck builder instance."""
    global _deck_builder
    if _deck_builder is None:
        _deck_builder = EgyptianDeckBuilder()
    return _deck_builder