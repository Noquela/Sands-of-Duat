#!/usr/bin/env python3
"""
COMBAT UI SYSTEM
================

Functional combat user interface for the Egyptian card battle system.
Allows players to interact with all combat mechanics including card play,
soul management, divine interventions, and underworld navigation.
"""

import pygame
import logging
import math
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Import our combat systems
from .initiative_system import HourGlassInitiative, TimePhase
from .thirteen_phase_system import ThirteenPhaseManager, CombatPhase
from .ba_ka_system import BaKaManager, SoulState, BaAbility, KaAbility
from .divine_judgment import DivineJudgmentSystem, JudgmentOutcome
from .underworld_passage import UnderworldPassageSystem, UnderworldHour
from .resurrection_system import EgyptianResurrectionSystem, ResurrectionType

logger = logging.getLogger(__name__)

class UIState(Enum):
    """States of the combat UI."""
    MAIN_COMBAT = "main_combat"
    CARD_SELECTION = "card_selection"
    TARGET_SELECTION = "target_selection"
    DIVINE_INTERVENTION = "divine_intervention"
    SOUL_MANAGEMENT = "soul_management"
    UNDERWORLD_NAVIGATION = "underworld_navigation"
    JUDGMENT_PREVIEW = "judgment_preview"
    RESURRECTION_MENU = "resurrection_menu"
    PHASE_TRANSITION = "phase_transition"

class UIAction(Enum):
    """Available UI actions."""
    PLAY_CARD = "play_card"
    END_TURN = "end_turn"
    SEPARATE_BA = "separate_ba"
    MANIFEST_KA = "manifest_ka"
    REQUEST_JUDGMENT = "request_judgment"
    DIVINE_INTERVENTION = "divine_intervention"
    NAVIGATE_UNDERWORLD = "navigate_underworld"
    ATTEMPT_RESURRECTION = "attempt_resurrection"
    VIEW_SOUL_STATUS = "view_soul_status"
    CHECK_INITIATIVE = "check_initiative"
    PREVIEW_PHASE = "preview_phase"

@dataclass
class UIElement:
    """Base UI element with positioning and interaction."""
    rect: pygame.Rect
    visible: bool = True
    enabled: bool = True
    hover_color: Tuple[int, int, int] = (200, 200, 100)
    click_action: Optional[Callable] = None
    tooltip: str = ""

@dataclass
class CardDisplay(UIElement):
    """UI element for displaying a card."""
    card_data: Dict[str, Any] = field(default_factory=dict)
    selected: bool = False
    playable: bool = True
    animation_offset: Tuple[int, int] = (0, 0)
    
class EgyptianCombatUI:
    """
    Complete combat UI system integrating all Egyptian combat mechanics.
    
    Provides visual interface for:
    - Card hand management and play
    - Ba-Ka soul manipulation
    - Divine interventions and prayers
    - Underworld navigation
    - Resurrection attempts
    - Initiative and phase tracking
    """
    
    def __init__(self, screen_width: int = 1400, screen_height: int = 900):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_state = UIState.MAIN_COMBAT
        self.selected_card = None
        self.selected_target = None
        
        # Combat systems integration
        self.initiative_system = HourGlassInitiative()
        self.phase_manager = ThirteenPhaseManager()
        self.ba_ka_manager = BaKaManager()
        self.judgment_system = DivineJudgmentSystem()
        self.underworld_system = UnderworldPassageSystem()
        self.resurrection_system = EgyptianResurrectionSystem()
        
        # UI Elements
        self.ui_elements: Dict[str, UIElement] = {}
        self.card_displays: List[CardDisplay] = []
        self.action_buttons: Dict[UIAction, UIElement] = {}
        
        # Egyptian color scheme
        self.colors = {
            'GOLD': (255, 215, 0),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'DARK_BLUE': (25, 25, 112),
            'HIEROGLYPH_BLUE': (30, 144, 255),
            'MUMMY_WRAP': (240, 230, 140),
            'BLOOD_RED': (139, 0, 0),
            'DIVINE_LIGHT': (255, 255, 224),
            'SHADOW_BLACK': (20, 20, 20),
            'COPPER': (184, 115, 51)
        }
        
        # Fonts (would be loaded from files in real implementation)
        pygame.font.init()
        self.fonts = {
            'title': pygame.font.Font(None, 36),
            'header': pygame.font.Font(None, 28),
            'body': pygame.font.Font(None, 20),
            'small': pygame.font.Font(None, 16),
            'card_name': pygame.font.Font(None, 18),
            'phase': pygame.font.Font(None, 24)
        }
        
        self._initialize_ui_layout()
    
    def _initialize_ui_layout(self):
        """Initialize the UI layout with Egyptian-themed positioning."""
        
        # Main combat area (center)
        combat_area_width = self.screen_width * 0.6
        combat_area_height = self.screen_height * 0.6
        combat_x = (self.screen_width - combat_area_width) // 2
        combat_y = 50
        
        self.ui_elements['combat_area'] = UIElement(
            rect=pygame.Rect(combat_x, combat_y, combat_area_width, combat_area_height)
        )
        
        # Player hand area (bottom)
        hand_width = self.screen_width * 0.8
        hand_height = 120
        hand_x = (self.screen_width - hand_width) // 2
        hand_y = self.screen_height - hand_height - 10
        
        self.ui_elements['hand_area'] = UIElement(
            rect=pygame.Rect(hand_x, hand_y, hand_width, hand_height)
        )
        
        # Initiative hourglass (left side)
        hourglass_size = 150
        self.ui_elements['hourglass'] = UIElement(
            rect=pygame.Rect(20, 100, hourglass_size, hourglass_size)
        )
        
        # Phase indicator (top center)
        phase_width = 400
        phase_height = 40
        self.ui_elements['phase_indicator'] = UIElement(
            rect=pygame.Rect((self.screen_width - phase_width) // 2, 10, phase_width, phase_height)
        )
        
        # Soul status panel (right side)
        soul_panel_width = 200
        soul_panel_height = 300
        self.ui_elements['soul_panel'] = UIElement(
            rect=pygame.Rect(self.screen_width - soul_panel_width - 20, 100, 
                           soul_panel_width, soul_panel_height)
        )
        
        # Action buttons (bottom right)
        button_width = 120
        button_height = 30
        button_spacing = 35
        button_start_x = self.screen_width - button_width - 20
        button_start_y = self.screen_height - 200
        
        actions = [
            UIAction.END_TURN,
            UIAction.SEPARATE_BA,
            UIAction.MANIFEST_KA,
            UIAction.DIVINE_INTERVENTION,
            UIAction.VIEW_SOUL_STATUS
        ]
        
        for i, action in enumerate(actions):
            self.action_buttons[action] = UIElement(
                rect=pygame.Rect(button_start_x, button_start_y + i * button_spacing,
                               button_width, button_height),
                click_action=lambda a=action: self._handle_action_button(a)
            )
        
        # Divine intervention panel (initially hidden)
        divine_panel_width = 350
        divine_panel_height = 400
        self.ui_elements['divine_panel'] = UIElement(
            rect=pygame.Rect((self.screen_width - divine_panel_width) // 2,
                           (self.screen_height - divine_panel_height) // 2,
                           divine_panel_width, divine_panel_height),
            visible=False
        )
        
        # Underworld navigation (initially hidden)
        underworld_width = 500
        underworld_height = 350
        self.ui_elements['underworld_panel'] = UIElement(
            rect=pygame.Rect((self.screen_width - underworld_width) // 2,
                           (self.screen_height - underworld_height) // 2,
                           underworld_width, underworld_height),
            visible=False
        )
        
        # Judgment preview (initially hidden)
        judgment_width = 400
        judgment_height = 300
        self.ui_elements['judgment_panel'] = UIElement(
            rect=pygame.Rect((self.screen_width - judgment_width) // 2,
                           (self.screen_height - judgment_height) // 2,
                           judgment_width, judgment_height),
            visible=False
        )
    
    def render(self, screen: pygame.Surface, game_state: Dict[str, Any]):
        """Main render method for the combat UI."""
        # Clear screen with Egyptian background
        screen.fill(self.colors['DARK_BLUE'])
        
        # Draw Egyptian-style border
        self._draw_egyptian_border(screen)
        
        # Render main UI elements based on current state
        if self.ui_state == UIState.MAIN_COMBAT:
            self._render_main_combat(screen, game_state)
        elif self.ui_state == UIState.DIVINE_INTERVENTION:
            self._render_divine_intervention_panel(screen, game_state)
        elif self.ui_state == UIState.SOUL_MANAGEMENT:
            self._render_soul_management_panel(screen, game_state)
        elif self.ui_state == UIState.UNDERWORLD_NAVIGATION:
            self._render_underworld_navigation(screen, game_state)
        elif self.ui_state == UIState.JUDGMENT_PREVIEW:
            self._render_judgment_preview(screen, game_state)
        elif self.ui_state == UIState.RESURRECTION_MENU:
            self._render_resurrection_menu(screen, game_state)
    
    def _render_main_combat(self, screen: pygame.Surface, game_state: Dict[str, Any]):
        """Render the main combat interface."""
        # Combat area background
        combat_rect = self.ui_elements['combat_area'].rect
        pygame.draw.rect(screen, self.colors['PAPYRUS'], combat_rect)
        pygame.draw.rect(screen, self.colors['GOLD'], combat_rect, 3)
        
        # Draw entities in combat
        self._draw_combat_entities(screen, game_state.get('entities', {}))
        
        # Initiative hourglass
        self._draw_hourglass(screen, game_state.get('initiative_data', {}))
        
        # Phase indicator  
        self._draw_phase_indicator(screen, game_state.get('current_phase', 'dawn_preparation'))
        
        # Player hand
        self._draw_hand(screen, game_state.get('player_hand', []))
        
        # Soul status panel
        self._draw_soul_panel(screen, game_state.get('soul_status', {}))
        
        # Action buttons
        self._draw_action_buttons(screen)
        
        # Status text
        self._draw_status_text(screen, game_state.get('status_message', ''))
    
    def _draw_egyptian_border(self, screen: pygame.Surface):
        """Draw Egyptian-style decorative border."""
        border_width = 15
        
        # Top and bottom borders with gold
        pygame.draw.rect(screen, self.colors['GOLD'], 
                        (0, 0, self.screen_width, border_width))
        pygame.draw.rect(screen, self.colors['GOLD'], 
                        (0, self.screen_height - border_width, self.screen_width, border_width))
        
        # Side borders
        pygame.draw.rect(screen, self.colors['GOLD'], 
                        (0, 0, border_width, self.screen_height))
        pygame.draw.rect(screen, self.colors['GOLD'], 
                        (self.screen_width - border_width, 0, border_width, self.screen_height))
        
        # Hieroglyph-style decorations (simplified)
        for i in range(0, self.screen_width, 100):
            pygame.draw.circle(screen, self.colors['LAPIS_LAZULI'], (i + 50, 7), 5)
            pygame.draw.circle(screen, self.colors['LAPIS_LAZULI'], 
                             (i + 50, self.screen_height - 7), 5)
    
    def _draw_combat_entities(self, screen: pygame.Surface, entities: Dict[str, Any]):
        """Draw entities participating in combat."""
        combat_rect = self.ui_elements['combat_area'].rect
        
        # Player entities (bottom of combat area)
        player_y = combat_rect.bottom - 80
        player_entities = [e for e in entities.values() if e.get('controller') == 'player']
        
        entity_width = 60
        entity_spacing = 80
        start_x = combat_rect.centerx - (len(player_entities) * entity_spacing) // 2
        
        for i, entity in enumerate(player_entities):
            entity_x = start_x + i * entity_spacing
            entity_rect = pygame.Rect(entity_x, player_y, entity_width, 60)
            
            # Entity background (varies by state)
            if entity.get('is_alive', True):
                bg_color = self.colors['DIVINE_LIGHT']
            else:
                bg_color = self.colors['SHADOW_BLACK']
            
            pygame.draw.rect(screen, bg_color, entity_rect)
            pygame.draw.rect(screen, self.colors['GOLD'], entity_rect, 2)
            
            # Entity info
            name_text = self.fonts['small'].render(entity.get('name', 'Entity'), True, 
                                                 self.colors['DARK_BLUE'])
            screen.blit(name_text, (entity_x, player_y - 20))
            
            # Health bar
            if entity.get('is_alive', True):
                health_ratio = entity.get('current_health', 100) / entity.get('max_health', 100)
                health_width = int(entity_width * health_ratio)
                health_rect = pygame.Rect(entity_x, player_y + 50, health_width, 8)
                pygame.draw.rect(screen, (255, 0, 0), 
                               pygame.Rect(entity_x, player_y + 50, entity_width, 8))
                pygame.draw.rect(screen, (0, 255, 0), health_rect)
        
        # Enemy entities (top of combat area)
        enemy_y = combat_rect.top + 20
        enemy_entities = [e for e in entities.values() if e.get('controller') == 'enemy']
        
        enemy_start_x = combat_rect.centerx - (len(enemy_entities) * entity_spacing) // 2
        
        for i, entity in enumerate(enemy_entities):
            entity_x = enemy_start_x + i * entity_spacing
            entity_rect = pygame.Rect(entity_x, enemy_y, entity_width, 60)
            
            # Enemy styling
            bg_color = self.colors['BLOOD_RED'] if entity.get('is_alive', True) else self.colors['SHADOW_BLACK']
            pygame.draw.rect(screen, bg_color, entity_rect)
            pygame.draw.rect(screen, self.colors['GOLD'], entity_rect, 2)
            
            # Enemy info
            name_text = self.fonts['small'].render(entity.get('name', 'Enemy'), True, 
                                                 self.colors['PAPYRUS'])
            screen.blit(name_text, (entity_x, enemy_y - 20))
    
    def _draw_hourglass(self, screen: pygame.Surface, initiative_data: Dict[str, Any]):
        """Draw the Egyptian hourglass initiative system."""
        hourglass_rect = self.ui_elements['hourglass'].rect
        
        # Hourglass frame (golden)
        pygame.draw.ellipse(screen, self.colors['GOLD'], 
                          (hourglass_rect.x, hourglass_rect.y, hourglass_rect.width, 40))
        pygame.draw.ellipse(screen, self.colors['GOLD'], 
                          (hourglass_rect.x, hourglass_rect.bottom - 40, hourglass_rect.width, 40))
        
        # Center constriction
        center_y = hourglass_rect.centery
        center_width = hourglass_rect.width // 4
        center_x = hourglass_rect.centerx - center_width // 2
        pygame.draw.rect(screen, self.colors['GOLD'], 
                        (center_x, center_y - 10, center_width, 20))
        
        # Sand flow visualization
        sand_position = initiative_data.get('sand_position', 0.0)  # -1.0 to 1.0
        
        # Upper chamber sand
        if sand_position < 0:
            upper_sand_height = int((1.0 + sand_position) * 60)  # More negative = more sand
            upper_sand_rect = pygame.Rect(hourglass_rect.x + 10, hourglass_rect.y + 10,
                                        hourglass_rect.width - 20, upper_sand_height)
            pygame.draw.rect(screen, self.colors['DESERT_SAND'], upper_sand_rect)
        
        # Lower chamber sand  
        if sand_position > 0:
            lower_sand_height = int(sand_position * 60)  # More positive = more sand
            lower_sand_rect = pygame.Rect(hourglass_rect.x + 10, 
                                        hourglass_rect.bottom - 10 - lower_sand_height,
                                        hourglass_rect.width - 20, lower_sand_height)
            pygame.draw.rect(screen, self.colors['DESERT_SAND'], lower_sand_rect)
        
        # Time phase indicator
        time_phase = initiative_data.get('time_phase', 'dawn')
        phase_colors = {
            'dawn': self.colors['DIVINE_LIGHT'],
            'midday': self.colors['GOLD'],
            'dusk': (255, 165, 0),  # Orange
            'midnight': self.colors['DARK_BLUE']
        }
        
        phase_color = phase_colors.get(time_phase, self.colors['PAPYRUS'])
        phase_text = self.fonts['small'].render(time_phase.title(), True, phase_color)
        screen.blit(phase_text, (hourglass_rect.x, hourglass_rect.bottom + 5))
    
    def _draw_phase_indicator(self, screen: pygame.Surface, current_phase: str):
        """Draw the 13-phase combat system indicator."""
        phase_rect = self.ui_elements['phase_indicator'].rect
        
        # Background
        pygame.draw.rect(screen, self.colors['LAPIS_LAZULI'], phase_rect)
        pygame.draw.rect(screen, self.colors['GOLD'], phase_rect, 2)
        
        # Phase text
        phase_display = current_phase.replace('_', ' ').title()
        phase_text = self.fonts['phase'].render(phase_display, True, self.colors['DIVINE_LIGHT'])
        
        text_rect = phase_text.get_rect(center=phase_rect.center)
        screen.blit(phase_text, text_rect)
        
        # Phase progress indicators (13 small circles)
        circle_radius = 8
        total_width = 13 * (circle_radius * 2 + 2)
        start_x = phase_rect.centerx - total_width // 2
        circle_y = phase_rect.bottom + 10
        
        phases = [
            'dawn_preparation', 'divine_invocation', 'ba_separation', 'targeting',
            'combat_action', 'damage_resolution', 'divine_judgment', 'spell_weaving',
            'status_effects', 'underworld_passage', 'ka_manifestation', 
            'afterlife_transition', 'cosmic_balance', 'dusk_cleanup'
        ]
        
        for i, phase in enumerate(phases):
            circle_x = start_x + i * (circle_radius * 2 + 2) + circle_radius
            
            if phase == current_phase:
                color = self.colors['GOLD']  # Current phase
            elif phases.index(current_phase) > i:
                color = self.colors['HIEROGLYPH_BLUE']  # Completed phase
            else:
                color = self.colors['SHADOW_BLACK']  # Future phase
            
            pygame.draw.circle(screen, color, (circle_x, circle_y), circle_radius)
            pygame.draw.circle(screen, self.colors['PAPYRUS'], (circle_x, circle_y), circle_radius, 1)
    
    def _draw_hand(self, screen: pygame.Surface, player_hand: List[Dict[str, Any]]):
        """Draw the player's hand of cards."""
        hand_rect = self.ui_elements['hand_area'].rect
        
        # Hand background
        pygame.draw.rect(screen, self.colors['MUMMY_WRAP'], hand_rect)
        pygame.draw.rect(screen, self.colors['COPPER'], hand_rect, 2)
        
        if not player_hand:
            # No cards message
            no_cards_text = self.fonts['body'].render("No cards in hand", True, self.colors['DARK_BLUE'])
            text_rect = no_cards_text.get_rect(center=hand_rect.center)
            screen.blit(no_cards_text, text_rect)
            return
        
        # Card dimensions
        card_width = 80
        card_height = 100
        card_spacing = 5
        
        # Calculate card positions
        total_width = len(player_hand) * card_width + (len(player_hand) - 1) * card_spacing
        start_x = hand_rect.centerx - total_width // 2
        card_y = hand_rect.y + 10
        
        # Draw cards
        for i, card_data in enumerate(player_hand):
            card_x = start_x + i * (card_width + card_spacing)
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            # Card background (varies by type/element)
            element = card_data.get('element', 'neutral')
            element_colors = {
                'sun': (255, 215, 0),
                'death': (139, 0, 0),
                'magic': (138, 43, 226),
                'water': (0, 191, 255),
                'earth': (139, 69, 19),
                'air': (176, 196, 222),
                'protection': (255, 218, 185),
                'chaos': (255, 20, 147),
                'neutral': self.colors['PAPYRUS']
            }
            
            card_color = element_colors.get(element, self.colors['PAPYRUS'])
            pygame.draw.rect(screen, card_color, card_rect)
            
            # Card border (gold for selected, copper for normal)
            border_color = self.colors['GOLD'] if i == self.selected_card else self.colors['COPPER']
            pygame.draw.rect(screen, border_color, card_rect, 2)
            
            # Card name
            name = card_data.get('name', 'Unknown Card')
            if len(name) > 12:
                name = name[:10] + "..."
            name_text = self.fonts['card_name'].render(name, True, self.colors['DARK_BLUE'])
            screen.blit(name_text, (card_x + 2, card_y + 2))
            
            # Mana cost
            mana_cost = card_data.get('mana_cost', 0)
            cost_text = self.fonts['small'].render(f"{mana_cost}", True, self.colors['LAPIS_LAZULI'])
            screen.blit(cost_text, (card_x + 2, card_y + card_height - 16))
            
            # Sand cost (if any)
            sand_cost = card_data.get('sand_cost', 0)
            if sand_cost > 0:
                sand_text = self.fonts['small'].render(f"S:{sand_cost}", True, self.colors['DESERT_SAND'])
                screen.blit(sand_text, (card_x + card_width - 30, card_y + card_height - 16))
            
            # Divine favor indicator
            divine_favor = card_data.get('divine_favor', 0)
            if divine_favor != 0:
                favor_color = self.colors['DIVINE_LIGHT'] if divine_favor > 0 else self.colors['BLOOD_RED']
                favor_text = self.fonts['small'].render(f"{divine_favor:+}", True, favor_color)
                screen.blit(favor_text, (card_x + card_width - 20, card_y + 2))
    
    def _draw_soul_panel(self, screen: pygame.Surface, soul_status: Dict[str, Any]):
        """Draw the Ba-Ka soul status panel."""
        panel_rect = self.ui_elements['soul_panel'].rect
        
        # Panel background
        pygame.draw.rect(screen, self.colors['SHADOW_BLACK'], panel_rect)
        pygame.draw.rect(screen, self.colors['GOLD'], panel_rect, 2)
        
        # Title
        title_text = self.fonts['header'].render("Soul Status", True, self.colors['DIVINE_LIGHT'])
        screen.blit(title_text, (panel_rect.x + 5, panel_rect.y + 5))
        
        y_offset = 35
        
        # Soul state
        soul_state = soul_status.get('state', 'unified')
        state_text = self.fonts['body'].render(f"State: {soul_state.title()}", True, self.colors['PAPYRUS'])
        screen.blit(state_text, (panel_rect.x + 5, panel_rect.y + y_offset))
        y_offset += 25
        
        # Ba status
        ba_strength = soul_status.get('ba_strength', 1.0)
        ba_color = self.colors['HIEROGLYPH_BLUE'] if ba_strength > 0.5 else self.colors['BLOOD_RED']
        ba_text = self.fonts['body'].render(f"Ba: {ba_strength:.1f}", True, ba_color)
        screen.blit(ba_text, (panel_rect.x + 5, panel_rect.y + y_offset))
        y_offset += 20
        
        # Ka status
        ka_strength = soul_status.get('ka_strength', 1.0)
        ka_color = self.colors['DIVINE_LIGHT'] if ka_strength > 0.5 else self.colors['BLOOD_RED']
        ka_text = self.fonts['body'].render(f"Ka: {ka_strength:.1f}", True, ka_color)
        screen.blit(ka_text, (panel_rect.x + 5, panel_rect.y + y_offset))
        y_offset += 25
        
        # Divine judgment score
        judgment_score = soul_status.get('divine_judgment', 0.0)
        judgment_color = self.colors['DIVINE_LIGHT'] if judgment_score > 0 else self.colors['BLOOD_RED']
        judgment_text = self.fonts['body'].render(f"Ma'at: {judgment_score:+.1f}", True, judgment_color)
        screen.blit(judgment_text, (panel_rect.x + 5, panel_rect.y + y_offset))
        y_offset += 25
        
        # Soul abilities
        abilities = soul_status.get('abilities', [])
        if abilities:
            abilities_text = self.fonts['small'].render("Abilities:", True, self.colors['PAPYRUS'])
            screen.blit(abilities_text, (panel_rect.x + 5, panel_rect.y + y_offset))
            y_offset += 20
            
            for ability in abilities[:4]:  # Show max 4 abilities
                ability_text = self.fonts['small'].render(f"• {ability}", True, self.colors['MUMMY_WRAP'])
                screen.blit(ability_text, (panel_rect.x + 10, panel_rect.y + y_offset))
                y_offset += 18
        
        # Underworld journey status (if applicable)
        journey_status = soul_status.get('underworld_journey')
        if journey_status:
            journey_text = self.fonts['small'].render("Underworld Journey:", True, self.colors['PAPYRUS'])
            screen.blit(journey_text, (panel_rect.x + 5, panel_rect.y + y_offset))
            y_offset += 20
            
            hour = journey_status.get('current_hour', 'not_started')
            hour_text = self.fonts['small'].render(f"Hour: {hour}", True, self.colors['DESERT_SAND'])
            screen.blit(hour_text, (panel_rect.x + 10, panel_rect.y + y_offset))
    
    def _draw_action_buttons(self, screen: pygame.Surface):
        """Draw action buttons with Egyptian styling."""
        for action, button_element in self.action_buttons.items():
            rect = button_element.rect
            
            # Button background
            if button_element.enabled:
                bg_color = self.colors['LAPIS_LAZULI']
                text_color = self.colors['DIVINE_LIGHT']
            else:
                bg_color = self.colors['SHADOW_BLACK']
                text_color = self.colors['PAPYRUS']
            
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, self.colors['GOLD'], rect, 2)
            
            # Button text
            action_names = {
                UIAction.END_TURN: "End Turn",
                UIAction.SEPARATE_BA: "Separate Ba",
                UIAction.MANIFEST_KA: "Manifest Ka", 
                UIAction.DIVINE_INTERVENTION: "Divine Aid",
                UIAction.VIEW_SOUL_STATUS: "Soul Status"
            }
            
            button_text = self.fonts['small'].render(action_names.get(action, action.value),
                                                   True, text_color)
            text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, text_rect)
    
    def _draw_status_text(self, screen: pygame.Surface, status_message: str):
        """Draw status text at the bottom of the screen."""
        if not status_message:
            return
            
        status_text = self.fonts['body'].render(status_message, True, self.colors['DIVINE_LIGHT'])
        text_x = 20
        text_y = self.screen_height - 30
        
        # Background for better readability
        text_rect = status_text.get_rect()
        text_rect.x = text_x - 5
        text_rect.y = text_y - 2
        text_rect.width += 10
        text_rect.height += 4
        
        pygame.draw.rect(screen, self.colors['SHADOW_BLACK'], text_rect)
        screen.blit(status_text, (text_x, text_y))
    
    def _render_divine_intervention_panel(self, screen: pygame.Surface, game_state: Dict[str, Any]):
        """Render the divine intervention selection panel."""
        # Semi-transparent background
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.colors['SHADOW_BLACK'])
        screen.blit(overlay, (0, 0))
        
        panel_rect = self.ui_elements['divine_panel'].rect
        
        # Panel background
        pygame.draw.rect(screen, self.colors['LAPIS_LAZULI'], panel_rect)
        pygame.draw.rect(screen, self.colors['GOLD'], panel_rect, 3)
        
        # Title
        title_text = self.fonts['header'].render("Call Upon the Gods", True, self.colors['DIVINE_LIGHT'])
        title_rect = title_text.get_rect(centerx=panel_rect.centerx, y=panel_rect.y + 10)
        screen.blit(title_text, title_rect)
        
        # Available gods and their interventions
        gods = game_state.get('available_gods', ['Ra', 'Isis', 'Anubis', 'Thoth'])
        
        y_offset = 50
        for i, god in enumerate(gods):
            god_y = panel_rect.y + y_offset + i * 60
            
            # God button
            god_rect = pygame.Rect(panel_rect.x + 20, god_y, 300, 50)
            pygame.draw.rect(screen, self.colors['DIVINE_LIGHT'], god_rect)
            pygame.draw.rect(screen, self.colors['GOLD'], god_rect, 2)
            
            # God name and power
            god_text = self.fonts['body'].render(god, True, self.colors['DARK_BLUE'])
            screen.blit(god_text, (god_rect.x + 5, god_rect.y + 5))
            
            # God's specialty
            specialties = {
                'Ra': 'Solar power and divine judgment',
                'Isis': 'Magic and healing',
                'Anubis': 'Death and soul guidance',
                'Thoth': 'Wisdom and spell mastery'
            }
            
            specialty_text = self.fonts['small'].render(specialties.get(god, 'Divine power'),
                                                      True, self.colors['DARK_BLUE'])
            screen.blit(specialty_text, (god_rect.x + 5, god_rect.y + 25))
        
        # Close button
        close_rect = pygame.Rect(panel_rect.right - 30, panel_rect.y + 5, 25, 25)
        pygame.draw.rect(screen, self.colors['BLOOD_RED'], close_rect)
        close_text = self.fonts['body'].render("X", True, self.colors['DIVINE_LIGHT'])
        close_text_rect = close_text.get_rect(center=close_rect.center)
        screen.blit(close_text, close_text_rect)
    
    def _render_underworld_navigation(self, screen: pygame.Surface, game_state: Dict[str, Any]):
        """Render the underworld navigation interface."""
        # Similar to divine intervention but for underworld travel
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.colors['SHADOW_BLACK'])
        screen.blit(overlay, (0, 0))
        
        panel_rect = self.ui_elements['underworld_panel'].rect
        
        # Panel background
        pygame.draw.rect(screen, self.colors['DARK_BLUE'], panel_rect)
        pygame.draw.rect(screen, self.colors['GOLD'], panel_rect, 3)
        
        # Title
        title_text = self.fonts['header'].render("Underworld Journey", True, self.colors['DIVINE_LIGHT'])
        title_rect = title_text.get_rect(centerx=panel_rect.centerx, y=panel_rect.y + 10)
        screen.blit(title_text, title_rect)
        
        # Current hour and progress
        current_hour = game_state.get('underworld_hour', 'first_hour')
        progress = game_state.get('underworld_progress', 0) / 12
        
        hour_text = self.fonts['body'].render(f"Current: {current_hour.replace('_', ' ').title()}", 
                                            True, self.colors['PAPYRUS'])
        screen.blit(hour_text, (panel_rect.x + 20, panel_rect.y + 50))
        
        # Progress bar
        progress_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 80, 
                                  panel_rect.width - 40, 20)
        pygame.draw.rect(screen, self.colors['SHADOW_BLACK'], progress_rect)
        progress_fill = pygame.Rect(progress_rect.x, progress_rect.y, 
                                  int(progress_rect.width * progress), progress_rect.height)
        pygame.draw.rect(screen, self.colors['DESERT_SAND'], progress_fill)
        pygame.draw.rect(screen, self.colors['GOLD'], progress_rect, 2)
    
    def handle_click(self, pos: Tuple[int, int], game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle mouse click events."""
        # Check UI state and route to appropriate handler
        if self.ui_state == UIState.MAIN_COMBAT:
            return self._handle_main_combat_click(pos, game_state)
        elif self.ui_state == UIState.DIVINE_INTERVENTION:
            return self._handle_divine_intervention_click(pos, game_state)
        # Add other UI state handlers as needed
        
        return None
    
    def _handle_main_combat_click(self, pos: Tuple[int, int], game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle clicks in main combat view."""
        # Check action buttons
        for action, button in self.action_buttons.items():
            if button.rect.collidepoint(pos) and button.enabled:
                return {'action': action.value, 'ui_change': True}
        
        # Check hand for card selection
        hand_rect = self.ui_elements['hand_area'].rect
        if hand_rect.collidepoint(pos):
            return self._handle_hand_click(pos, game_state)
        
        # Check combat area for targeting
        combat_rect = self.ui_elements['combat_area'].rect
        if combat_rect.collidepoint(pos):
            return self._handle_combat_area_click(pos, game_state)
        
        return None
    
    def _handle_hand_click(self, pos: Tuple[int, int], game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle clicking on cards in hand."""
        player_hand = game_state.get('player_hand', [])
        if not player_hand:
            return None
        
        hand_rect = self.ui_elements['hand_area'].rect
        card_width = 80
        card_spacing = 5
        
        total_width = len(player_hand) * card_width + (len(player_hand) - 1) * card_spacing
        start_x = hand_rect.centerx - total_width // 2
        
        # Determine which card was clicked
        relative_x = pos[0] - start_x
        if relative_x < 0:
            return None
        
        card_index = relative_x // (card_width + card_spacing)
        if card_index >= len(player_hand):
            return None
        
        # Select/deselect card
        if self.selected_card == card_index:
            self.selected_card = None
            return {'action': 'deselect_card', 'ui_change': True}
        else:
            self.selected_card = card_index
            return {'action': 'select_card', 'card_index': card_index, 'ui_change': True}
    
    def _handle_action_button(self, action: UIAction) -> Dict[str, Any]:
        """Handle action button clicks."""
        if action == UIAction.DIVINE_INTERVENTION:
            self.ui_state = UIState.DIVINE_INTERVENTION
            return {'action': 'show_divine_intervention', 'ui_change': True}
        elif action == UIAction.VIEW_SOUL_STATUS:
            self.ui_state = UIState.SOUL_MANAGEMENT
            return {'action': 'show_soul_management', 'ui_change': True}
        else:
            return {'action': action.value, 'ui_change': False}
    
    def update_ui_state(self, new_state: UIState):
        """Update the UI state."""
        self.ui_state = new_state
        
        # Show/hide relevant panels
        if new_state == UIState.MAIN_COMBAT:
            self.ui_elements['divine_panel'].visible = False
            self.ui_elements['underworld_panel'].visible = False
            self.ui_elements['judgment_panel'].visible = False
        elif new_state == UIState.DIVINE_INTERVENTION:
            self.ui_elements['divine_panel'].visible = True
        elif new_state == UIState.UNDERWORLD_NAVIGATION:
            self.ui_elements['underworld_panel'].visible = True
        elif new_state == UIState.JUDGMENT_PREVIEW:
            self.ui_elements['judgment_panel'].visible = True
    
    def get_selected_card(self) -> Optional[int]:
        """Get the index of the currently selected card."""
        return self.selected_card
    
    def clear_selection(self):
        """Clear current selection."""
        self.selected_card = None
        self.selected_target = None