#!/usr/bin/env python3
"""
SANDS OF DUAT - COMBAT SCREEN
============================

Premium Egyptian-themed combat interface with authentic underworld visuals.
Features card battles in the Egyptian afterlife with proper theming.
"""

import pygame
import math
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
from ..components.card_display import EgyptianCard, CardData

# Asset paths
ASSETS_ROOT = Path(__file__).parent.parent.parent.parent.parent / "assets"
FINAL_DATASET_PATH = ASSETS_ROOT / "images" / "lora_training" / "final_dataset"

@dataclass
class CombatState:
    """Current state of the combat encounter."""
    player_health: int = 30
    player_max_health: int = 30
    enemy_health: int = 30
    enemy_max_health: int = 30
    player_mana: int = 3
    player_max_mana: int = 10
    turn: str = "player"  # "player" or "enemy"
    phase: str = "main"   # "main", "combat", "end"

class CombatScreen:
    """Egyptian underworld combat interface."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Egyptian color palette
        self.colors = {
            'GOLD': (255, 215, 0),
            'GOLD_DARK': (184, 134, 11),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'DARK_BLUE': (25, 25, 112),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'RED': (220, 20, 20),
            'GREEN': (20, 220, 20),
            'UNDERWORLD_FOG': (40, 20, 60, 100),
            'COMBAT_GLOW': (255, 215, 0, 150)
        }
        
        # Combat state
        self.combat_state = CombatState()
        
        # Load underworld background
        self.background = self._load_underworld_background()
        
        # Initialize fonts
        self._init_fonts()
        
        # Create demo cards for combat
        self._setup_combat_cards()
        
        # UI layout
        self._setup_combat_layout()
        
        # Animation state
        self.health_bar_animation = 1.0
        self.mana_crystal_glow = 0
        self.turn_indicator_pulse = 0
        self.combat_effects = []
        
        # Selected card for playing
        self.selected_card = None
        self.dragging_card = False
        self.drag_offset = (0, 0)
    
    def _load_underworld_background(self) -> pygame.Surface:
        """Load authentic Egyptian underworld background."""
        underworld_assets = [
            "underworld_scene_01_q68.png",
            "underworld_scene_03_q67.png", 
            "underworld_scene_06_q67.png",
            "underworld_scene_07_q65.png",
            "underworld_location_20_q66.png",
            "underworld_location_23_q65.png"
        ]
        
        for asset_name in underworld_assets:
            asset_path = FINAL_DATASET_PATH / asset_name
            if asset_path.exists():
                try:
                    bg_image = pygame.image.load(str(asset_path))
                    return self._scale_background(bg_image)
                except pygame.error as e:
                    print(f"Could not load {asset_name}: {e}")
                    continue
        
        # Fallback underworld background
        fallback = pygame.Surface((self.screen_width, self.screen_height))
        fallback.fill((20, 10, 40))  # Dark purple underworld
        return fallback
    
    def _scale_background(self, image: pygame.Surface) -> pygame.Surface:
        """Scale background to fit screen."""
        img_width, img_height = image.get_size()
        scale_x = self.screen_width / img_width
        scale_y = self.screen_height / img_height
        scale = max(scale_x, scale_y)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        
        final_surface = pygame.Surface((self.screen_width, self.screen_height))
        x_offset = (self.screen_width - new_width) // 2
        y_offset = (self.screen_height - new_height) // 2
        final_surface.blit(scaled_image, (x_offset, y_offset))
        
        return final_surface
    
    def _init_fonts(self):
        """Initialize fonts for combat UI."""
        self.title_font = pygame.font.Font(None, 36)
        self.header_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        self.large_font = pygame.font.Font(None, 48)
    
    def _setup_combat_cards(self):
        """Setup demo cards for combat."""
        # Player hand
        player_cards_data = [
            CardData("ANUBIS", "Guardian of Dead", 6, 8, 8, "legendary", 
                    "Judge the souls", "egyptian_god_anubis_02_q75.png", "major"),
            CardData("HORUS", "Sky God", 5, 7, 6, "rare", 
                    "Flying strike", "egyptian_god_horus_06_q77.png", "major"), 
            CardData("BASTET", "Protector", 3, 3, 4, "common",
                    "Summon cats", "egyptian_god_bastet_08_q73.png", "guardian"),
            CardData("THOTH", "God of Wisdom", 4, 2, 8, "rare",
                    "Draw cards", "egyptian_god_thoth_03_q74.png", "minor"),
        ]
        
        self.player_hand = []
        for card_data in player_cards_data:
            card = EgyptianCard(card_data)
            card.size = (160, 240)  # Combat card size
            self.player_hand.append(card)
        
        # Enemy cards (face down initially)
        enemy_card_data = CardData("SET", "God of Chaos", 7, 9, 7, "legendary",
                                  "Chaos incarnate", "egyptian_god_set_06_q73.png", "major")
        self.enemy_card = EgyptianCard(enemy_card_data)
        self.enemy_card.size = (160, 240)
        
        # Battlefield cards
        self.player_battlefield = []
        self.enemy_battlefield = []
    
    def _setup_combat_layout(self):
        """Setup combat UI layout areas."""
        # Player hand area
        self.hand_area = pygame.Rect(
            50,
            self.screen_height - 260,
            self.screen_width - 100,
            240
        )
        
        # Battlefield areas
        self.player_battlefield_area = pygame.Rect(
            200,
            self.screen_height - 520,
            self.screen_width - 400,
            200
        )
        
        self.enemy_battlefield_area = pygame.Rect(
            200,
            200,
            self.screen_width - 400,
            200
        )
        
        # Health/mana UI positions
        self.player_ui_pos = (50, self.screen_height - 100)
        self.enemy_ui_pos = (50, 50)
        
        # Update card positions
        self._update_hand_positions()
        self._update_battlefield_positions()
    
    def _update_hand_positions(self):
        """Update positions of cards in player hand."""
        if not self.player_hand:
            return
            
        card_spacing = min(200, (self.hand_area.width - 160) // max(1, len(self.player_hand) - 1))
        start_x = self.hand_area.centerx - ((len(self.player_hand) - 1) * card_spacing) // 2
        
        for i, card in enumerate(self.player_hand):
            if card != self.selected_card or not self.dragging_card:
                card.position = (start_x + i * card_spacing, self.hand_area.y)
    
    def _update_battlefield_positions(self):
        """Update positions of cards on battlefield."""
        # Player battlefield
        for i, card in enumerate(self.player_battlefield):
            x = self.player_battlefield_area.x + i * 180
            y = self.player_battlefield_area.y
            card.position = (x, y)
        
        # Enemy battlefield  
        for i, card in enumerate(self.enemy_battlefield):
            x = self.enemy_battlefield_area.x + i * 180
            y = self.enemy_battlefield_area.y
            card.position = (x, y)
        
        # Enemy card (if exists)
        if hasattr(self, 'enemy_card'):
            self.enemy_card.position = (self.screen_width - 210, 50)
    
    def _draw_health_bar(self, surface: pygame.Surface, pos: Tuple[int, int], 
                        current: int, maximum: int, width: int = 200):
        """Draw Egyptian-themed health bar."""
        bar_height = 20
        bar_rect = pygame.Rect(pos[0], pos[1], width, bar_height)
        
        # Background
        pygame.draw.rect(surface, self.colors['BLACK'], bar_rect)
        pygame.draw.rect(surface, self.colors['GOLD'], bar_rect, 2)
        
        # Health fill
        if current > 0:
            fill_width = int((current / maximum) * (width - 4))
            fill_rect = pygame.Rect(pos[0] + 2, pos[1] + 2, fill_width, bar_height - 4)
            
            # Health color based on percentage
            health_percent = current / maximum
            if health_percent > 0.6:
                color = self.colors['GREEN']
            elif health_percent > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = self.colors['RED']
            
            pygame.draw.rect(surface, color, fill_rect)
        
        # Health text
        health_text = f"{current}/{maximum}"
        text_surface = self.text_font.render(health_text, True, self.colors['WHITE'])
        text_x = pos[0] + width // 2 - text_surface.get_width() // 2
        text_y = pos[1] + bar_height // 2 - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_mana_crystals(self, surface: pygame.Surface, pos: Tuple[int, int], 
                           current: int, maximum: int):
        """Draw Egyptian-themed mana crystals."""
        crystal_size = 25
        crystal_spacing = 30
        
        for i in range(maximum):
            crystal_x = pos[0] + i * crystal_spacing
            crystal_y = pos[1]
            crystal_rect = pygame.Rect(crystal_x, crystal_y, crystal_size, crystal_size)
            
            if i < current:
                # Filled crystal with glow
                glow_alpha = int(100 + 50 * math.sin(self.mana_crystal_glow))
                glow_surface = pygame.Surface((crystal_size + 6, crystal_size + 6), pygame.SRCALPHA)
                glow_color = (*self.colors['LAPIS_LAZULI'], glow_alpha)
                pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect())
                surface.blit(glow_surface, (crystal_x - 3, crystal_y - 3))
                
                pygame.draw.ellipse(surface, self.colors['LAPIS_LAZULI'], crystal_rect)
            else:
                # Empty crystal
                pygame.draw.ellipse(surface, self.colors['BLACK'], crystal_rect)
            
            pygame.draw.ellipse(surface, self.colors['GOLD'], crystal_rect, 2)
    
    def _draw_turn_indicator(self, surface: pygame.Surface):
        """Draw current turn indicator with Egyptian styling."""
        if self.combat_state.turn == "player":
            text = "YOUR TURN"
            color = self.colors['GOLD']
            pos = (self.screen_width // 2, self.screen_height - 50)
        else:
            text = "ENEMY TURN"  
            color = self.colors['RED']
            pos = (self.screen_width // 2, 100)
        
        # Pulsing effect
        alpha = int(200 + 55 * math.sin(self.turn_indicator_pulse))
        
        text_surface = self.header_font.render(text, True, color)
        text_surface.set_alpha(alpha)
        
        text_x = pos[0] - text_surface.get_width() // 2
        text_y = pos[1] - text_surface.get_height() // 2
        
        # Glow effect
        for offset in range(1, 3):
            for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
                surface.blit(text_surface, (text_x + dx, text_y + dy))
        
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_play_area_indicators(self, surface: pygame.Surface):
        """Draw battlefield area indicators."""
        # Player battlefield indicator
        if self.player_battlefield_area.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, self.colors['COMBAT_GLOW'], 
                           self.player_battlefield_area, 3)
        else:
            pygame.draw.rect(surface, self.colors['GOLD'], 
                           self.player_battlefield_area, 1)
        
        # Enemy battlefield indicator
        pygame.draw.rect(surface, self.colors['RED'], 
                        self.enemy_battlefield_area, 1)
        
        # Labels
        player_label = self.small_font.render("PLAYER BATTLEFIELD", True, self.colors['GOLD'])
        surface.blit(player_label, (self.player_battlefield_area.x, 
                                   self.player_battlefield_area.bottom + 5))
        
        enemy_label = self.small_font.render("ENEMY BATTLEFIELD", True, self.colors['RED'])
        surface.blit(enemy_label, (self.enemy_battlefield_area.x,
                                  self.enemy_battlefield_area.y - 20))
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle combat events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
            elif event.key == pygame.K_SPACE and self.combat_state.turn == "player":
                # End turn
                self._end_player_turn()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Check if clicking on a card in hand
            if self.combat_state.turn == "player":
                for card in self.player_hand:
                    card_rect = pygame.Rect(*card.position, *card.size)
                    if card_rect.collidepoint(mouse_pos):
                        if self.combat_state.player_mana >= card.data.cost:
                            self.selected_card = card
                            self.dragging_card = True
                            self.drag_offset = (mouse_pos[0] - card.position[0],
                                              mouse_pos[1] - card.position[1])
                        break
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_card and self.selected_card:
                mouse_pos = event.pos
                
                # Check if dropped on battlefield
                if self.player_battlefield_area.collidepoint(mouse_pos):
                    self._play_card(self.selected_card)
                
                # Reset drag state
                self.selected_card = None
                self.dragging_card = False
                self._update_hand_positions()
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_card and self.selected_card:
                mouse_pos = event.pos
                self.selected_card.position = (mouse_pos[0] - self.drag_offset[0],
                                             mouse_pos[1] - self.drag_offset[1])
            
            # Update hover states
            for card in self.player_hand:
                if not self.dragging_card or card != self.selected_card:
                    card.handle_event(event)
            
            for card in self.player_battlefield:
                card.handle_event(event)
        
        return None
    
    def _play_card(self, card: EgyptianCard):
        """Play a card from hand to battlefield."""
        if card in self.player_hand and self.combat_state.player_mana >= card.data.cost:
            self.player_hand.remove(card)
            self.player_battlefield.append(card)
            self.combat_state.player_mana -= card.data.cost
            
            self._update_hand_positions()
            self._update_battlefield_positions()
            
            # TODO: Trigger card effects
    
    def _end_player_turn(self):
        """End the player's turn and start enemy turn."""
        self.combat_state.turn = "enemy"
        # TODO: Enemy AI logic
        # For now, just end enemy turn immediately
        self.combat_state.turn = "player"
        self.combat_state.player_mana = min(self.combat_state.player_mana + 1, 
                                          self.combat_state.player_max_mana)
    
    def update(self, dt: float):
        """Update combat animations and logic."""
        # Update animations
        self.health_bar_animation += dt
        self.mana_crystal_glow += dt * 3
        self.turn_indicator_pulse += dt * 4
        
        # Update cards
        for card in self.player_hand:
            if card != self.selected_card or not self.dragging_card:
                card.update(dt)
        
        for card in self.player_battlefield:
            card.update(dt)
            
        for card in self.enemy_battlefield:
            card.update(dt)
        
        if hasattr(self, 'enemy_card'):
            self.enemy_card.update(dt)
    
    def draw(self):
        """Draw the combat screen."""
        # Underworld background
        self.screen.blit(self.background, (0, 0))
        
        # Atmospheric overlay
        fog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        fog_surface.fill(self.colors['UNDERWORLD_FOG'])
        self.screen.blit(fog_surface, (0, 0))
        
        # Draw battlefield area indicators
        self._draw_play_area_indicators()
        
        # Player UI
        # Health bar
        self._draw_health_bar(self.screen, 
                             (self.player_ui_pos[0], self.player_ui_pos[1] - 30),
                             self.combat_state.player_health,
                             self.combat_state.player_max_health)
        
        # Mana crystals
        self._draw_mana_crystals(self.screen,
                                (self.player_ui_pos[0], self.player_ui_pos[1]),
                                self.combat_state.player_mana,
                                self.combat_state.player_max_mana)
        
        # Enemy UI
        # Health bar
        self._draw_health_bar(self.screen,
                             (self.enemy_ui_pos[0], self.enemy_ui_pos[1] + 50),
                             self.combat_state.enemy_health,
                             self.combat_state.enemy_max_health)
        
        # Enemy label
        enemy_label = self.text_font.render("ENEMY", True, self.colors['RED'])
        self.screen.blit(enemy_label, self.enemy_ui_pos)
        
        # Turn indicator
        self._draw_turn_indicator()
        
        # Draw cards
        # Player hand (draw non-selected cards first)
        for card in self.player_hand:
            if card != self.selected_card:
                card.draw(self.screen)
        
        # Battlefield cards
        for card in self.player_battlefield:
            card.draw(self.screen)
            
        for card in self.enemy_battlefield:
            card.draw(self.screen)
        
        # Enemy card
        if hasattr(self, 'enemy_card'):
            self.enemy_card.draw(self.screen)
        
        # Draw selected card last (on top)
        if self.selected_card:
            self.selected_card.draw(self.screen)
        
        # Instructions
        instructions = [
            "Drag cards to battlefield to play them",
            "SPACE: End turn    ESC: Back to menu",
            f"Mana: {self.combat_state.player_mana}/{self.combat_state.player_max_mana}"
        ]
        
        y_offset = 150
        for instruction in instructions:
            text_surface = self.small_font.render(instruction, True, self.colors['PAPYRUS'])
            self.screen.blit(text_surface, (self.screen_width - 300, y_offset))
            y_offset += 20


def create_combat_screen(screen: pygame.Surface) -> CombatScreen:
    """Factory function to create combat screen."""
    return CombatScreen(screen)