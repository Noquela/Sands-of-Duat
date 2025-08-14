"""
Professional Combat System - SPRINT 5: Combat System Polish
Features epic Egyptian god battles with Hades-level visual effects and smooth gameplay.
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
from ..responsive.scaling_manager import scaling_manager
from ..responsive import ultrawide_layout
from ..responsive.combat_hud import CombatHUD
from ..responsive.responsive_components import ResponsiveCard
from ...core.asset_loader import get_asset_loader
from ...core.deck_manager import deck_manager
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton
from ..components.ultrawide_decorations import ultrawide_decorations
from ..components.enhanced_ui_components import (
    EgyptianPanel, EnhancedStatusBar, IconType, CardPreviewPanel, ResponsiveButton
)
from ..components.enhanced_card_hover import EnhancedCardHover, HoverState
from ..components.energy_feedback_system import EnergyFeedbackSystem, EnergyState
from ..components.responsive_typography import responsive_typography, TextStyle
from ..components.smooth_transitions import smooth_transitions, TransitionType, EasingType
from ..animations.card_animator import card_animator, AnimationType
from ..animations.combat_effects import combat_effects, EffectType, ParticleType

class CombatAction(Enum):
    """Combat actions."""
    BACK_TO_MENU = auto()
    END_TURN = auto()
    SURRENDER = auto()

class CombatPhase(Enum):
    """Combat phases."""
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    VICTORY = auto()
    DEFEAT = auto()

@dataclass
class CombatCard:
    """Combat card data."""
    name: str
    cost: int
    attack: int
    health: int
    description: str
    rarity: str = "common"
    card_type: str = "creature"

@dataclass
class Combatant:
    """Combat participant data."""
    name: str
    health: int
    max_health: int
    mana: int
    max_mana: int
    portrait: Optional[pygame.Surface] = None

class CombatCard3D:
    """Professional 3D-style combat card with Hades-level hover effects."""
    
    def __init__(self, data: CombatCard, x: int = 0, y: int = 0):
        self.data = data
        self.x = x
        self.y = y
        # Use the enhanced card sizes from constants
        self.width = Layout.CARD_WIDTH
        self.height = Layout.CARD_HEIGHT
        
        # Base rectangle for positioning
        self.base_rect = pygame.Rect(x, y, self.width, self.height)
        
        # Enhanced hover system
        card_data = {
            'name': data.name,
            'cost': data.cost,
            'attack': data.attack,
            'health': data.health,
            'description': data.description,
            'rarity': data.rarity
        }
        self.hover_system = EnhancedCardHover(self.base_rect, card_data)
        
        # Legacy animation state (for backward compatibility)
        self.hover_offset = 0
        self.is_hovered = False
        self.is_dragging = False
        self.glow_intensity = 0
        self.play_animation = 0
        self.shake_offset = 0
        
        # Visual effects
        self.particle_effects = []
        self.damage_numbers = []
        
        # Render the card
        self._render_card()
    
    def _render_card(self):
        """Render the card using enhanced card renderer with themed frames."""
        from ..components.enhanced_card_renderer import enhanced_card_renderer
        
        # Create surface for the card
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Prepare card data for enhanced renderer
        card_data = {
            'name': self.data.name,
            'cost': self.data.cost,
            'attack': self.data.attack,
            'health': self.data.health,
            'card_type': self.data.card_type,
            'rarity': self.data.rarity,
            'description': self.data.description
        }
        
        # Use enhanced card renderer with hover and glow effects
        enhanced_card_renderer.render_card(
            self.surface, 0, 0, self.width, self.height,
            self.data.name, card_data,
            hover_intensity=self.glow_intensity,
            glow_intensity=self.glow_intensity
        )
    
    def get_rect(self):
        """Get card rectangle."""
        return pygame.Rect(int(self.x + self.shake_offset), 
                          int(self.y + self.hover_offset), 
                          self.width, self.height)
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], is_selected: bool = False):
        """Update card animations with Hades-level hover effects."""
        # Update enhanced hover system
        self.is_hovered = self.hover_system.update(dt, mouse_pos, is_selected)
        
        # Update position from hover system
        current_rect = self.hover_system.get_render_rect()
        self.x = current_rect.x
        self.y = current_rect.y
        
        # Legacy animation compatibility
        target_offset = -15 if self.is_hovered else 0
        self.hover_offset += (target_offset - self.hover_offset) * dt * 8
        
        # Glow animation
        if self.is_hovered:
            self.glow_intensity = min(1.0, self.glow_intensity + dt * 4)
        else:
            self.glow_intensity = max(0.0, self.glow_intensity - dt * 6)
        
        # Play animation
        if self.play_animation > 0:
            self.play_animation -= dt * 3
            self.shake_offset = math.sin(self.play_animation * 20) * 5
        else:
            self.shake_offset = 0
        
        # Update particle effects
        for particle in self.particle_effects[:]:
            particle['life'] -= dt
            particle['y'] -= particle['speed'] * dt
            particle['alpha'] = max(0, particle['alpha'] - dt * 300)
            
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.particle_effects.remove(particle)
        
        # Update damage numbers
        for damage in self.damage_numbers[:]:
            damage['life'] -= dt
            damage['y'] -= damage['speed'] * dt
            damage['alpha'] = max(0, int(255 * (damage['life'] / damage['max_life'])))
            
            if damage['life'] <= 0:
                self.damage_numbers.remove(damage)
    
    def trigger_play_animation(self):
        """Trigger card play animation with smooth transitions."""
        self.play_animation = 1.0
        
        # Create smooth card play transition
        card_id = f"card_{id(self)}"
        smooth_transitions.scale_element(
            card_id, 1.0, 1.15, Timing.CARD_FLIP_DURATION / 2,
            EasingType.EASE_OUT_ELASTIC
        )
        
        # Scale back after peak
        def scale_back():
            smooth_transitions.scale_element(
                card_id, 1.15, 1.0, Timing.CARD_FLIP_DURATION / 2,
                EasingType.EASE_IN_QUAD
            )
        
        # Schedule scale back (simplified timing)
        smooth_transitions.start_transition(
            f"{card_id}_delay", TransitionType.FADE, 0, 1, 
            Timing.CARD_FLIP_DURATION / 2, EasingType.LINEAR, scale_back
        )
        
        # Add sparkle particles
        for _ in range(8):
            self.particle_effects.append({
                'x': self.x + self.width // 2 + random.randint(-30, 30),
                'y': self.y + self.height // 2,
                'speed': random.randint(30, 80),
                'life': 1.5,
                'alpha': 255,
                'color': Colors.GOLD
            })
    
    def show_damage(self, damage: int):
        """Show damage number animation with smooth transitions."""
        damage_id = f"damage_{pygame.time.get_ticks()}_{id(self)}"
        start_pos = (self.x + self.width // 2, self.y)
        
        # Create smooth floating transition for damage number
        smooth_transitions.create_damage_number_transition(damage, start_pos)
        
        self.damage_numbers.append({
            'damage': damage,
            'x': self.x + self.width // 2,
            'y': self.y,
            'speed': 100,
            'life': 2.0,
            'max_life': 2.0,
            'alpha': 255,
            'transition_id': damage_id
        })
    
    def render(self, surface: pygame.Surface):
        """Render the card with Hades-level effects and transitions."""
        # Render enhanced glow effect first (behind card)
        self.hover_system.render_glow(surface)
        
        # Get current render position from hover system
        current_rect = self.hover_system.get_render_rect()
        base_pos = (int(current_rect.x + self.shake_offset), int(current_rect.y))
        
        # Apply smooth transitions to card rendering
        card_id = f"card_{id(self)}"
        card_rect = smooth_transitions.render_element_with_transitions(
            surface, self.surface, base_pos, card_id
        )
        
        # Particle effects
        for particle in self.particle_effects:
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_surface.fill(particle['color'][:3])
            particle_surface.set_alpha(int(particle['alpha']))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Damage numbers with enhanced typography
        for damage in self.damage_numbers:
            # Create temporary surface for damage text with alpha
            damage_surface = pygame.Surface((100, 30), pygame.SRCALPHA)
            responsive_typography.render_text(
                f"-{damage['damage']}", TextStyle.CARD_NAME, damage_surface, 
                (0, 0), custom_color=Colors.RED
            )
            damage_surface.set_alpha(damage['alpha'])
            surface.blit(damage_surface, (int(damage['x']) - 50, int(damage['y'])))
            
    def render_tooltip(self, surface: pygame.Surface):
        """Render tooltip if hovering (should be called after all cards)."""
        self.hover_system.render_tooltip(surface)

class ProfessionalCombat:
    """
    Professional combat system with Hades-level polish and Egyptian theming.
    Features dynamic turn-based combat with visual effects and smooth animations.
    """
    
    def __init__(self, on_action: Optional[Callable[[CombatAction], None]] = None):
        """Initialize the combat system."""
        self.on_action = on_action
        
        # Combat state
        self.phase = CombatPhase.PLAYER_TURN
        self.turn_count = 1
        
        # Initialize asset loader first
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Start smooth screen transition
        smooth_transitions.fade_in_element("combat_screen", Timing.FADE_DURATION)
        self.enemy_turn_timer = 0.0  # Timer for enemy turn delay
        
        # Initialize combatants first - BALANCED STATS
        self.player = Combatant("PHARAOH", 30, 30, 3, 10)
        self.enemy = Combatant("ANUBIS", 30, 30, 3, 8)  # Equal health, equal starting mana
        
        # Background and effects
        self.background_surface = self._create_background()
        self.battlefield_particles = []
        self.combat_effects = []
        
        # Initialize responsive combat HUD
        self.combat_hud = CombatHUD()
        self.combat_hud.set_player_health(self.player.health, self.player.max_health)
        self.combat_hud.set_player_mana(self.player.mana, self.player.max_mana)
        self.combat_hud.set_enemy_health(self.enemy.health, self.enemy.max_health)
        self.combat_hud.set_turn(True)  # Player starts
        self.combat_hud.set_action_callbacks(
            self._handle_end_turn,
            self._handle_surrender
        )
        
        # Enhanced energy feedback system
        energy_x = 50
        energy_y = SCREEN_HEIGHT - 100
        energy_width = 200
        energy_height = 30
        self.energy_system = EnergyFeedbackSystem(
            energy_x, energy_y, energy_width, energy_height,
            max_energy=self.player.max_mana, 
            initial_energy=self.player.mana
        )
        
        # Card system - use saved deck if available
        if deck_manager.has_saved_deck():
            self.player_hand = self._create_hand_from_saved_deck()
            print(f"Using custom deck: {len(self.player_hand)} cards loaded from deck builder!")
        else:
            self.player_hand = self._create_starting_hand()
            print("Using default starter deck - build a custom deck to use it in combat!")
        
        self.enemy_hand = self._create_enemy_hand()  # Enemy now has cards
        self.player_battlefield = []
        self.enemy_battlefield = []
        self.selected_card = None
        self.dragging_card = False
        self.drag_offset = (0, 0)
        
        # UI elements
        self.buttons = self._create_buttons()
        
        # Enhanced layout areas for ultrawide
        if Layout.IS_ULTRAWIDE:
            # Use the full content width for better card spacing
            margin = Layout.CONTENT_X_OFFSET + 100
            content_width = Layout.CONTENT_WIDTH - 200
            
            self.hand_area = pygame.Rect(margin, SCREEN_HEIGHT - 320, content_width, 300)
            self.player_battle_area = pygame.Rect(margin, SCREEN_HEIGHT - 500, content_width, 180)  
            self.enemy_battle_area = pygame.Rect(margin, 250, content_width, 180)
        else:
            # Standard layout for non-ultrawide
            self.hand_area = pygame.Rect(50, SCREEN_HEIGHT - 220, SCREEN_WIDTH - 100, 200)
            self.player_battle_area = pygame.Rect(200, SCREEN_HEIGHT - 400, SCREEN_WIDTH - 400, 150)
            self.enemy_battle_area = pygame.Rect(200, 250, SCREEN_WIDTH - 400, 150)
        
        # Initialize card preview panel (fix bug)
        self.card_preview_panel = None
        
        # Initialize positions
        self._update_card_positions()
        self._spawn_battlefield_particles()
        
        
        # Preload combat animations
        self.asset_loader.preload_animations([
            'ANUBIS - JUDGE OF THE DEAD',
            'Egyptian Warrior', 
            'Mummy Guardian',
            'Sphinx Guardian'
        ])
        
        print("Professional Combat System initialized - Ready for Egyptian warfare!")
    
    def _create_background(self):
        """Create atmospheric combat background with ultra-high resolution Egyptian temple art."""
        # Load the specific combat background (bg_combat_4k.png - 4096x2048)
        combat_bg = self.asset_loader.load_background('combat')
        
        if combat_bg:
            # Scale the ultra-high resolution temple background with quality preservation
            background = pygame.transform.smoothscale(combat_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Lighter overlay to show more of the beautiful 4K artwork
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Reduced opacity to showcase the high-quality background art
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT  
                red_tint = int(5 + ratio * 3)   # Subtle warmth
                blue_tint = int(8 + ratio * 7)  # Subtle depth
                # Create color for this line
                line_color = (red_tint, 3, blue_tint)
                overlay.fill(line_color, (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            return background
        else:
            # Enhanced fallback maintains Egyptian theme
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(30 + ratio * 25)  # Warmer tones
                g = int(20 + ratio * 20)  # Golden undertones
                b = int(50 + ratio * 30)  # Deep mystical blues
                background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
            
            # Add Egyptian temple pattern
            pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for x in range(0, SCREEN_WIDTH, 120):
                for y in range(0, SCREEN_HEIGHT, 120):
                    # Temple column patterns
                    pygame.draw.rect(pattern_surface, (Colors.GOLD[0], Colors.GOLD[1], Colors.GOLD[2], 25), (x, y, 25, 8))
                    pygame.draw.rect(pattern_surface, (Colors.GOLD[0], Colors.GOLD[1], Colors.GOLD[2], 25), (x, y + 15, 8, 30))
                    pygame.draw.circle(pattern_surface, (Colors.GOLD[0], Colors.GOLD[1], Colors.GOLD[2], 20), (x + 12, y + 50), 6, 1)
            
            background.blit(pattern_surface, (0, 0))
            return background
    
    def _initialize_enhanced_ui(self):
        """Initialize enhanced UI components."""
        # Enhanced status bars with Egyptian icons
        if Layout.IS_ULTRAWIDE:
            # Position status bars in the side panels for ultrawide
            status_x = Layout.CONTENT_X_OFFSET + 20
            status_width = 200
        else:
            status_x = 50
            status_width = 180
        
        # Player status bars
        self.player_health_bar = EnhancedStatusBar(
            status_x, SCREEN_HEIGHT - 80, status_width, 25, 
            IconType.HEALTH, self.player.max_health
        )
        self.player_mana_bar = EnhancedStatusBar(
            status_x, SCREEN_HEIGHT - 50, status_width, 25,
            IconType.MANA, self.player.max_mana
        )
        
        # Enemy status bars  
        self.enemy_health_bar = EnhancedStatusBar(
            status_x, 80, status_width, 25,
            IconType.HEALTH, self.enemy.max_health
        )
        self.enemy_mana_bar = EnhancedStatusBar(
            status_x, 110, status_width, 25,
            IconType.MANA, self.enemy.max_mana
        )
        
        # Card preview panel for ultrawide
        if Layout.IS_ULTRAWIDE:
            preview_x = Layout.UI_SAFE_RIGHT - 320
            preview_y = 200
            self.card_preview_panel = CardPreviewPanel(preview_x, preview_y, 300, 500)
        else:
            self.card_preview_panel = None
    
    def _spawn_battlefield_particles(self):
        """Spawn atmospheric particles."""
        for _ in range(15):
            self.battlefield_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'speed': random.randint(10, 30),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.DESERT_SAND, Colors.LAPIS_LAZULI])
            })
    
    def _create_starting_hand(self) -> List[CombatCard3D]:
        """Create starting hand of cards."""
        card_data = [
            CombatCard("SACRED SCARAB", 2, 2, 2, "Swift desert guardian"),  # BUFFED: 2/2 instead of 2/1
            CombatCard("TEMPLE GUARD", 3, 2, 4, "Protects the sacred halls"),
            CombatCard("DIVINE LIGHTNING", 3, 5, 0, "Strike enemies with Ra's power", card_type="spell"),  # BUFFED: 3 cost instead of 4
            CombatCard("ANUBIS BLESSING", 3, 3, 3, "Judge the worthy souls", "rare"),
            CombatCard("PYRAMID POWER", 6, 6, 8, "Ancient monument of power", "legendary"),  # BALANCED: 6/8 instead of 7/7
        ]
        
        cards = []
        for data in card_data:
            card = CombatCard3D(data)
            cards.append(card)
        
        return cards
    
    def _create_hand_from_saved_deck(self) -> List[CombatCard3D]:
        """Create hand from saved deck - take first 5 cards as starting hand."""
        saved_deck = deck_manager.get_player_deck()
        
        if not saved_deck:
            return self._create_starting_hand()
        
        # Take first 5 cards as starting hand (or all if less than 5)
        hand_size = min(5, len(saved_deck))
        starting_cards = saved_deck[:hand_size]
        
        cards = []
        for deck_card in starting_cards:
            combat_card_data = CombatCard(
                name=deck_card.name,
                cost=deck_card.cost,
                attack=deck_card.attack,
                health=deck_card.health,
                description=deck_card.description,
                rarity=deck_card.rarity,
                card_type=deck_card.card_type
            )
            card = CombatCard3D(combat_card_data)
            cards.append(card)
        
        return cards
    
    def _create_enemy_hand(self) -> List[CombatCard3D]:
        """Create enemy's starting hand of cards."""
        enemy_card_data = [
            CombatCard("SHADOW SERVANT", 2, 2, 2, "Anubis's minion from the underworld"),
            CombatCard("JUDGMENT SCALE", 3, 1, 4, "Weighs the hearts of mortals", "rare"),
            CombatCard("UNDERWORLD CURSE", 3, 4, 0, "Deals 4 damage to enemy", card_type="spell"),  # BUFFED: 3 cost instead of 4
            CombatCard("DEATH'S EMBRACE", 5, 3, 6, "Gains +1/+1 when enemy dies", "rare"),
            CombatCard("ANUBIS'S WRATH", 7, 7, 8, "Legendary guardian of the dead", "legendary"),  # BALANCED: 7/8 instead of 8/8
        ]
        
        cards = []
        for data in enemy_card_data:
            card = CombatCard3D(data)
            cards.append(card)
        
        return cards
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create combat UI buttons."""
        buttons = []
        
        button_configs = [
            ("END TURN", CombatAction.END_TURN),
            ("SURRENDER", CombatAction.SURRENDER),
            ("BACK", CombatAction.BACK_TO_MENU)
        ]
        
        # SPRINT 1: Use scaling manager for responsive button sizing
        button_width, button_height = scaling_manager.get_component_size('button_default')
        spacing = scaling_manager.scale_value(15, 'spacing')
        start_x = SCREEN_WIDTH - (len(button_configs) * (button_width + spacing))
        
        for i, (text, action) in enumerate(button_configs):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, 20, button_width, button_height, text, scaling_manager.get_font('button').get_height(),
                action=lambda a=action: self._handle_action(a)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_action(self, action: CombatAction):
        """Handle button actions."""
        if action == CombatAction.END_TURN:
            self._end_turn()
        elif action == CombatAction.SURRENDER:
            self.phase = CombatPhase.DEFEAT
        
        if self.on_action:
            self.on_action(action)
    
    def _update_card_positions(self):
        """Update positions of all cards with enhanced ultrawide spacing."""
        # Use responsive card spacing system
        card_spacing = scaling_manager.layout.get_card_spacing()
        
        # Calculate proper spacing based on available width
        if self.player_hand:
            card_width = scaling_manager.get_component_size('card_medium')[0]
            available_width = self.hand_area.width - card_width
            cards_count = len(self.player_hand)
            if cards_count > 1:
                max_spacing = available_width // (cards_count - 1)
                card_spacing = min(card_spacing, max_spacing)
        
        battlefield_spacing = int(card_spacing * 1.2)  # Slightly wider spacing for battlefield
        
        # Player hand
        if self.player_hand:
            start_x = self.hand_area.centerx - ((len(self.player_hand) - 1) * card_spacing) // 2
            
            for i, card in enumerate(self.player_hand):
                if not card.is_dragging:
                    card.x = start_x + i * card_spacing
                    card.y = self.hand_area.y
        
        # Battlefield cards with enhanced spacing
        for i, card in enumerate(self.player_battlefield):
            card.x = self.player_battle_area.x + i * battlefield_spacing
            card.y = self.player_battle_area.y
        
        for i, card in enumerate(self.enemy_battlefield):
            card.x = self.enemy_battle_area.x + i * battlefield_spacing
            card.y = self.enemy_battle_area.y
        
        # Enemy hand (visible at top of screen) with enhanced layout
        if self.enemy_hand:
            if Layout.IS_ULTRAWIDE:
                enemy_hand_area = pygame.Rect(Layout.CONTENT_X_OFFSET + 100, 50, Layout.CONTENT_WIDTH - 200, 200)
            else:
                enemy_hand_area = pygame.Rect(200, 50, SCREEN_WIDTH - 400, 200)
                
            enemy_card_spacing = min(card_spacing, (enemy_hand_area.width - Layout.CARD_WIDTH) // max(1, len(self.enemy_hand) - 1))
            start_x = enemy_hand_area.centerx - ((len(self.enemy_hand) - 1) * enemy_card_spacing) // 2
            
            for i, card in enumerate(self.enemy_hand):
                card.x = start_x + i * enemy_card_spacing
                card.y = enemy_hand_area.y
    
    def _can_player_play_cards(self) -> bool:
        """Check if player can play any cards in hand."""
        for card in self.player_hand:
            if card.data.cost <= self.player.mana:
                return True
        return False
    
    def _auto_end_turn_if_needed(self):
        """Automatically end turn if player cannot play any cards."""
        if self.phase == CombatPhase.PLAYER_TURN and not self._can_player_play_cards():
            print(f"[AUTO-END] No playable cards (Mana: {self.player.mana}), ending turn automatically")
            self._end_turn()
    
    def _handle_end_turn(self):
        """Handle end turn button click."""
        if self.phase == CombatPhase.PLAYER_TURN:
            self._end_turn()
    
    def _handle_surrender(self):
        """Handle surrender button click."""
        if self.on_action:
            self.on_action(CombatAction.SURRENDER)
    
    def _end_turn(self):
        """End current player turn."""
        if self.phase == CombatPhase.PLAYER_TURN:
            # Resolve combat at end of player turn
            self._resolve_combat()
            
            # Check if game ended from combat
            if self.phase not in [CombatPhase.VICTORY, CombatPhase.DEFEAT]:
                self.phase = CombatPhase.ENEMY_TURN
                self.enemy_turn_timer = 2.0  # 2 second delay for enemy turn
        elif self.phase == CombatPhase.ENEMY_TURN:
            self.phase = CombatPhase.PLAYER_TURN
            self.turn_count += 1
            # Restore mana
            old_mana = self.player.mana
            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
            
            # Update energy system if mana increased
            if self.player.mana > old_mana:
                self.energy_system.gain_energy(self.player.mana - old_mana)
    
    def _enemy_turn(self):
        """Handle enemy turn logic with simple AI."""
        # Increase enemy mana
        self.enemy.mana = min(self.enemy.mana + 1, self.enemy.max_mana)
        
        # Simple AI: Play the most expensive card enemy can afford
        affordable_cards = [card for card in self.enemy_hand if card.data.cost <= self.enemy.mana]
        
        if affordable_cards:
            # Sort by cost (most expensive first) then by attack power
            affordable_cards.sort(key=lambda c: (c.data.cost, c.data.attack), reverse=True)
            chosen_card = affordable_cards[0]
            
            # Play the chosen card
            self._play_enemy_card(chosen_card)
        
        # Resolve combat between creatures
        self._resolve_combat()
        
        # End enemy turn and start player turn
        self.phase = CombatPhase.PLAYER_TURN
        self.turn_count += 1
        old_mana = self.player.mana
        self.player.mana = min(self.player.mana + 1, self.player.max_mana)
        
        # Update energy system if mana increased
        if self.player.mana > old_mana:
            self.energy_system.gain_energy(self.player.mana - old_mana)
    
    def _play_card(self, card: CombatCard3D):
        """Play a card from hand to battlefield with enhanced animations."""
        if card in self.player_hand and self.player.mana >= card.data.cost:
            self.player_hand.remove(card)
            self.player_battlefield.append(card)
            self.player.mana -= card.data.cost
            
            # Update energy system
            self.energy_system.spend_energy(card.data.cost)
            
            # Start play animation
            card_id = f"player_{id(card)}"
            card_animator.start_animation(card_id, AnimationType.PLAY)
            
            # Add play effects based on card type
            card_pos = (card.x, card.y)
            if card.data.card_type == "spell":
                combat_effects.trigger_effect(EffectType.ENERGY_WAVE, card_pos[0], card_pos[1])
                combat_effects.trigger_effect(EffectType.PARTICLE_BURST, card_pos[0], card_pos[1],
                                            particle_type=ParticleType.ENERGY, count=20)
            else:
                combat_effects.trigger_effect(EffectType.PARTICLE_BURST, card_pos[0], card_pos[1],
                                            particle_type=ParticleType.DIVINE, count=15)
            
            card.trigger_play_animation()
            self._update_card_positions()
            
            # Play card sound effect
            audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.7)
            
            # Add combat effect
            self.combat_effects.append({
                'type': 'card_played',
                'time': 2.0,
                'card': card
            })
            
            # Check if turn should auto-end after playing card
            self._auto_end_turn_if_needed()
    
    def _play_enemy_card(self, card: CombatCard3D):
        """Play an enemy card from hand to battlefield."""
        if card in self.enemy_hand and self.enemy.mana >= card.data.cost:
            self.enemy_hand.remove(card)
            self.enemy_battlefield.append(card)
            self.enemy.mana -= card.data.cost
            
            card.trigger_play_animation()
            self._update_card_positions()
            
            # Play enemy card sound (slightly different pitch)
            audio_manager.play_sound(SoundEffect.CARD_PLAY, 0.5)
            
            # Add combat effect for enemy card
            self.combat_effects.append({
                'type': 'enemy_card_played',
                'time': 2.0,
                'card': card
            })
    
    def _resolve_combat(self):
        """Resolve combat between creatures on the battlefield."""
        # Handle spells first (direct damage)
        self._resolve_spells()
        
        # Then resolve creature vs creature combat
        self._resolve_creature_combat()
        
        # Check for win/loss conditions
        self._check_win_conditions()
    
    def _resolve_spells(self):
        """Resolve spell effects with Hades-level visual effects."""
        # Player spells targeting enemy
        for card in self.player_battlefield[:]:
            if card.data.card_type == "spell":
                damage = card.data.attack
                is_critical = damage >= 5
                
                # Apply damage
                self.enemy.health -= damage
                card.show_damage(damage)
                self.player_battlefield.remove(card)
                
                # Get enemy center position for effects
                enemy_x = SCREEN_WIDTH - 200
                enemy_y = SCREEN_HEIGHT // 2
                
                # Trigger combat effects based on spell type
                if "LIGHTNING" in card.data.name.upper():
                    combat_effects.trigger_effect(EffectType.LIGHTNING_STRIKE, 
                                                enemy_x - 300, enemy_y - 100, 
                                                end_x=enemy_x, end_y=enemy_y)
                elif "FIRE" in card.data.name.upper():
                    combat_effects.trigger_effect(EffectType.FIRE_EXPLOSION, enemy_x, enemy_y)
                elif "DIVINE" in card.data.name.upper():
                    combat_effects.trigger_effect(EffectType.DIVINE_LIGHT, enemy_x, enemy_y)
                else:
                    combat_effects.trigger_effect(EffectType.ENERGY_WAVE, enemy_x, enemy_y)
                
                # Add damage number
                combat_effects.add_damage_number(enemy_x, enemy_y - 50, damage, is_critical)
                
                # Play damage sound effect
                audio_manager.play_sound(SoundEffect.DAMAGE_DEALT, 0.8)
                
                # Add spell effect for legacy system
                self.combat_effects.append({
                    'type': 'spell_cast',
                    'time': 2.0,
                    'damage': damage,
                    'target': 'enemy'
                })
        
        # Enemy spells targeting player
        for card in self.enemy_battlefield[:]:
            if card.data.card_type == "spell":
                damage = card.data.attack
                is_critical = damage >= 5
                
                # Apply damage
                self.player.health -= damage
                card.show_damage(damage)
                self.enemy_battlefield.remove(card)
                
                # Get player center position for effects
                player_x = 200
                player_y = SCREEN_HEIGHT // 2
                
                # Trigger combat effects
                if "CURSE" in card.data.name.upper():
                    combat_effects.trigger_effect(EffectType.PARTICLE_BURST, player_x, player_y,
                                                particle_type=ParticleType.POISON, count=20)
                else:
                    combat_effects.trigger_effect(EffectType.ENERGY_WAVE, player_x, player_y)
                
                # Add damage number
                combat_effects.add_damage_number(player_x, player_y - 50, damage, is_critical)
                
                # Play damage sound effect
                audio_manager.play_sound(SoundEffect.DAMAGE_DEALT, 0.8)
                
                # Add spell effect for legacy system
                self.combat_effects.append({
                    'type': 'spell_cast',
                    'time': 2.0,
                    'damage': damage,
                    'target': 'player'
                })
    
    def _resolve_creature_combat(self):
        """Resolve creature vs creature combat."""
        player_creatures = [c for c in self.player_battlefield if c.data.card_type == "creature"]
        enemy_creatures = [c for c in self.enemy_battlefield if c.data.card_type == "creature"]
        
        # Simple combat: Each creature fights the first available enemy creature
        for player_card in player_creatures[:]:
            if enemy_creatures:
                enemy_card = enemy_creatures[0]
                
                # Deal damage to each other
                player_damage = player_card.data.attack
                enemy_damage = enemy_card.data.attack
                
                # Apply damage
                player_card.data.health -= enemy_damage
                enemy_card.data.health -= player_damage
                
                # Get positions for effects
                player_card_pos = (400, SCREEN_HEIGHT - 200)  # Approximate card position
                enemy_card_pos = (SCREEN_WIDTH - 400, 200)
                
                # Show damage numbers and effects
                if enemy_damage > 0:
                    player_card.show_damage(enemy_damage)
                    # Add blood particles for damage
                    combat_effects.trigger_effect(EffectType.PARTICLE_BURST, 
                                                player_card_pos[0], player_card_pos[1],
                                                particle_type=ParticleType.BLOOD, count=8)
                    combat_effects.add_damage_number(player_card_pos[0], player_card_pos[1] - 30, 
                                                   enemy_damage, enemy_damage >= 4)
                
                if player_damage > 0:
                    enemy_card.show_damage(player_damage)
                    # Add blood particles for damage
                    combat_effects.trigger_effect(EffectType.PARTICLE_BURST,
                                                enemy_card_pos[0], enemy_card_pos[1], 
                                                particle_type=ParticleType.BLOOD, count=8)
                    combat_effects.add_damage_number(enemy_card_pos[0], enemy_card_pos[1] - 30,
                                                   player_damage, player_damage >= 4)
                
                # Screen shake for combat impact
                combat_effects.add_screen_shake(3.0, 0.2)
                
                # Remove dead creatures with death effects
                if player_card.data.health <= 0:
                    # Death animation
                    card_animator.start_animation(f"player_{id(player_card)}", AnimationType.DESTROY)
                    combat_effects.trigger_effect(EffectType.PARTICLE_BURST,
                                                player_card_pos[0], player_card_pos[1],
                                                particle_type=ParticleType.DUST, count=15)
                    self.player_battlefield.remove(player_card)
                
                if enemy_card.data.health <= 0:
                    # Death animation
                    card_animator.start_animation(f"enemy_{id(enemy_card)}", AnimationType.DESTROY)
                    combat_effects.trigger_effect(EffectType.PARTICLE_BURST,
                                                enemy_card_pos[0], enemy_card_pos[1],
                                                particle_type=ParticleType.DUST, count=15)
                    self.enemy_battlefield.remove(enemy_card)
                    enemy_creatures.remove(enemy_card)
                
                # Add combat effect
                self.combat_effects.append({
                    'type': 'creature_combat',
                    'time': 2.0,
                    'player_card': player_card.data.name,
                    'enemy_card': enemy_card.data.name
                })
        
        # Remaining creatures attack players directly
        for player_card in player_creatures:
            if player_card in self.player_battlefield and not enemy_creatures:
                # Attack enemy directly
                damage = player_card.data.attack
                is_critical = damage >= 5
                self.enemy.health -= damage
                
                # Enemy position for effects
                enemy_x = SCREEN_WIDTH - 200
                enemy_y = SCREEN_HEIGHT // 2
                
                # Add direct attack effects
                combat_effects.trigger_effect(EffectType.PARTICLE_BURST, enemy_x, enemy_y,
                                            particle_type=ParticleType.SPARK, count=12)
                combat_effects.add_damage_number(enemy_x, enemy_y - 50, damage, is_critical)
                combat_effects.add_screen_shake(4.0 if is_critical else 2.5, 0.2)
                
                self.combat_effects.append({
                    'type': 'direct_attack',
                    'time': 2.0,
                    'attacker': player_card.data.name,
                    'damage': damage,
                    'target': 'enemy'
                })
        
        for enemy_card in enemy_creatures:
            if enemy_card in self.enemy_battlefield and not player_creatures:
                # Attack player directly
                damage = enemy_card.data.attack
                is_critical = damage >= 5
                self.player.health -= damage
                
                # Player position for effects
                player_x = 200
                player_y = SCREEN_HEIGHT // 2
                
                # Add direct attack effects
                combat_effects.trigger_effect(EffectType.PARTICLE_BURST, player_x, player_y,
                                            particle_type=ParticleType.SPARK, count=12)
                combat_effects.add_damage_number(player_x, player_y - 50, damage, is_critical)
                combat_effects.add_screen_shake(4.0 if is_critical else 2.5, 0.2)
                
                self.combat_effects.append({
                    'type': 'direct_attack',
                    'time': 2.0,
                    'attacker': enemy_card.data.name,
                    'damage': damage,
                    'target': 'player'
                })
    
    def _check_win_conditions(self):
        """Check for victory or defeat conditions."""
        if self.player.health <= 0:
            if self.phase != CombatPhase.DEFEAT:  # Only play sound once
                audio_manager.play_sound(SoundEffect.DEFEAT_SOUND, 1.0)
                audio_manager.play_music(AudioTrack.DEFEAT, fade_in=1.0)
            self.phase = CombatPhase.DEFEAT
        elif self.enemy.health <= 0:
            if self.phase != CombatPhase.VICTORY:  # Only play sound once
                audio_manager.play_sound(SoundEffect.VICTORY_FANFARE, 1.0)
                audio_manager.play_music(AudioTrack.VICTORY, fade_in=1.0)
            self.phase = CombatPhase.VICTORY
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update combat system."""
        self.animation_time += dt
        
        # Update responsive combat HUD
        self.combat_hud.update(dt, mouse_pos, mouse_pressed, events)
        
        # Update enhanced energy feedback system
        self.energy_system.update(dt)
        
        # Keep HUD values synchronized with game state
        self.combat_hud.set_player_health(self.player.health)
        self.combat_hud.set_player_mana(self.player.mana)
        
        # Keep energy system synchronized
        if self.energy_system.current_energy != self.player.mana:
            self.energy_system.set_energy(self.player.mana)
        self.combat_hud.set_enemy_health(self.enemy.health)
        self.combat_hud.set_turn(self.phase == CombatPhase.PLAYER_TURN)
        
        # Update smooth transitions
        smooth_transitions.update_transitions(dt)
        
        
        # Update card preview panel
        if self.card_preview_panel:
            self.card_preview_panel.update(dt)
            
            # Show card details on hover
            hovered_card = None
            for card in self.player_hand + self.enemy_hand:
                if card.get_rect().collidepoint(mouse_pos):
                    hovered_card = card
                    break
            
            if hovered_card:
                card_details = {
                    'cost': hovered_card.data.cost,
                    'attack': hovered_card.data.attack,
                    'health': hovered_card.data.health,
                    'rarity': hovered_card.data.rarity,
                    'description': hovered_card.data.description
                }
                self.card_preview_panel.show_card(hovered_card.data.name, card_details)
            else:
                self.card_preview_panel.hide()
        
        # Update card animations 
        self.asset_loader.update_animations(dt)
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update particles
        for particle in self.battlefield_particles:
            particle['x'] += math.sin(self.animation_time * 0.5 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.5
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
        
        # Update combat effects
        for effect in self.combat_effects[:]:
            effect['time'] -= dt
            if effect['time'] <= 0:
                self.combat_effects.remove(effect)
        
        # Handle enemy turn timer
        if self.phase == CombatPhase.ENEMY_TURN and self.enemy_turn_timer > 0:
            self.enemy_turn_timer -= dt
            if self.enemy_turn_timer <= 0:
                self._enemy_turn()
        
        # Update buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Update cards
        for card in self.player_hand + self.player_battlefield + self.enemy_hand + self.enemy_battlefield:
            card.update(dt, mouse_pos)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.phase == CombatPhase.PLAYER_TURN:
                        self._end_turn()
                    elif self.phase in [CombatPhase.VICTORY, CombatPhase.DEFEAT]:
                        # Return to menu after game ends
                        if self.on_action:
                            self.on_action(CombatAction.BACK_TO_MENU)
                elif event.key == pygame.K_ESCAPE:
                    if self.on_action:
                        self.on_action(CombatAction.BACK_TO_MENU)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks
                for button in self.buttons:
                    if button.handle_click(mouse_pos):
                        break
                else:
                    # Check card clicks
                    self._handle_card_click(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging_card and self.selected_card:
                    # Check if dropped on battlefield
                    if self.player_battle_area.collidepoint(mouse_pos):
                        self._play_card(self.selected_card)
                    
                    # Reset drag state
                    self.selected_card.is_dragging = False
                    self.selected_card = None
                    self.dragging_card = False
                    self._update_card_positions()
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_card and self.selected_card:
                    self.selected_card.x = mouse_pos[0] - self.drag_offset[0]
                    self.selected_card.y = mouse_pos[1] - self.drag_offset[1]
    
    def _handle_card_click(self, mouse_pos: Tuple[int, int]):
        """Handle card click events."""
        if self.phase != CombatPhase.PLAYER_TURN:
            return
        
        for card in self.player_hand:
            if card.get_rect().collidepoint(mouse_pos):
                if self.player.mana >= card.data.cost:
                    self.selected_card = card
                    self.dragging_card = True
                    card.is_dragging = True
                    self.drag_offset = (mouse_pos[0] - card.x, mouse_pos[1] - card.y)
                break
    
    def render(self, surface: pygame.Surface):
        """Render the enhanced combat screen."""
        # Ultra-high resolution background
        surface.blit(self.background_surface, (0, 0))
        
        # Enhanced ultrawide decorations
        if Layout.IS_ULTRAWIDE:
            ultrawide_decorations.render(surface)
        
        # Battlefield particles
        self._render_battlefield_particles(surface)
        
        # Render responsive combat HUD (replaces old status bars)
        self.combat_hud.render(surface)
        
        # Render enhanced energy feedback system
        self.energy_system.render(surface)
        
        # Combat UI
        self._render_combat_ui(surface)
        
        # Battle areas
        self._render_battle_areas(surface)
        
        # Cards
        self._render_cards(surface)
        
        # Turn indicator
        self._render_turn_indicator(surface)
        
        # Combat effects (legacy)
        self._render_combat_effects(surface)
        
        # NEW: Professional combat effects system
        combat_effects.render(surface)
        
        # Buttons
        for button in self.buttons:
            button.render(surface)
        
        # Instructions
        self._render_instructions(surface)
        
        # Card preview panel for ultrawide
        if self.card_preview_panel:
            self.card_preview_panel.render(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    
    def _render_battlefield_particles(self, surface: pygame.Surface):
        """Render atmospheric particles."""
        for particle in self.battlefield_particles:
            alpha = int(120 + 80 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill(particle['color'][:3])
            particle_surface.set_alpha(alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_combat_ui(self, surface: pygame.Surface):
        """Render enhanced combat UI with labels and portraits."""
        # Player label
        if Layout.IS_ULTRAWIDE:
            label_x = Layout.CONTENT_X_OFFSET + 20
        else:
            label_x = 50
            
        # Enhanced typography for character labels
        responsive_typography.render_text(
            "PHARAOH", TextStyle.SUBTITLE, surface, (label_x, SCREEN_HEIGHT - 110)
        )
        
        responsive_typography.render_text(
            "ANUBIS - JUDGE OF THE DEAD", TextStyle.SUBTITLE, surface, 
            (label_x, 50), custom_color=Colors.RED
        )
        
        # Enemy portrait - Load ultra-high resolution Anubis artwork (2048x2048)!
        from ...core.asset_loader import get_asset_loader
        asset_loader = get_asset_loader()
        anubis_portrait = asset_loader.load_character_portrait('anubis_boss')
        
        if anubis_portrait:
            # Scale ultra-high resolution portrait to fit in UI area with quality scaling
            portrait_size = (150, 200)
            # Use smoothscale for better quality from 2048x2048 source
            scaled_portrait = pygame.transform.smoothscale(anubis_portrait, portrait_size)
            portrait_pos = (SCREEN_WIDTH - 200, 30)  # Top-right corner
            
            # Draw ornate Egyptian frame around ultra-high resolution portrait
            frame_rect = pygame.Rect(portrait_pos[0] - 8, portrait_pos[1] - 8, 
                                   portrait_size[0] + 16, portrait_size[1] + 16)
            # Multi-layered frame for ultra quality appearance
            pygame.draw.rect(surface, Colors.BLACK, frame_rect, 6)
            pygame.draw.rect(surface, Colors.GOLD, frame_rect, 4) 
            pygame.draw.rect(surface, Colors.LAPIS_LAZULI, frame_rect, 2)
            
            # Add corner decorations for ultra-high resolution aesthetic
            corner_size = 12
            # Top-left corner
            pygame.draw.polygon(surface, Colors.GOLD, [
                (frame_rect.left, frame_rect.top + corner_size),
                (frame_rect.left, frame_rect.top),
                (frame_rect.left + corner_size, frame_rect.top)
            ])
            # Top-right corner  
            pygame.draw.polygon(surface, Colors.GOLD, [
                (frame_rect.right - corner_size, frame_rect.top),
                (frame_rect.right, frame_rect.top),
                (frame_rect.right, frame_rect.top + corner_size)
            ])
            # Bottom corners
            pygame.draw.polygon(surface, Colors.GOLD, [
                (frame_rect.left, frame_rect.bottom - corner_size),
                (frame_rect.left, frame_rect.bottom),
                (frame_rect.left + corner_size, frame_rect.bottom)
            ])
            pygame.draw.polygon(surface, Colors.GOLD, [
                (frame_rect.right - corner_size, frame_rect.bottom),
                (frame_rect.right, frame_rect.bottom),
                (frame_rect.right, frame_rect.bottom - corner_size)
            ])
            
            # Draw the ultra-high resolution portrait
            surface.blit(scaled_portrait, portrait_pos)
        
    
    def _render_health_bar(self, surface: pygame.Surface, pos: Tuple[int, int], 
                          current: int, maximum: int, color: Tuple[int, int, int]):
        """Render health bar with Egyptian styling."""
        bar_width = 200
        bar_height = 20
        
        # Background
        bg_rect = pygame.Rect(pos[0], pos[1], bar_width, bar_height)
        pygame.draw.rect(surface, Colors.BLACK, bg_rect)
        pygame.draw.rect(surface, Colors.GOLD, bg_rect, 2)
        
        # Health fill
        if current > 0:
            fill_width = int((current / maximum) * (bar_width - 4))
            fill_rect = pygame.Rect(pos[0] + 2, pos[1] + 2, fill_width, bar_height - 4)
            pygame.draw.rect(surface, color, fill_rect)
        
        # Health text with enhanced typography
        responsive_typography.render_text(
            f"{current}/{maximum}", TextStyle.CARD_TEXT, surface, 
            bg_rect.center, center=True, custom_color=Colors.WHITE
        )
    
    def _render_mana_crystals(self, surface: pygame.Surface, pos: Tuple[int, int], 
                             current: int, maximum: int):
        """Render mana crystals."""
        crystal_size = 20
        spacing = 25
        
        for i in range(maximum):
            crystal_x = pos[0] + i * spacing
            crystal_rect = pygame.Rect(crystal_x, pos[1], crystal_size, crystal_size)
            
            if i < current:
                # Filled crystal with glow
                glow_alpha = int(150 + 100 * abs(math.sin(self.animation_time * 3)))
                glow_surface = pygame.Surface((crystal_size + 8, crystal_size + 8), pygame.SRCALPHA)
                glow_surface.fill(Colors.LAPIS_LAZULI)
                glow_surface.set_alpha(glow_alpha)
                surface.blit(glow_surface, (crystal_x - 4, pos[1] - 4))
                
                pygame.draw.ellipse(surface, Colors.LAPIS_LAZULI, crystal_rect)
            else:
                pygame.draw.ellipse(surface, Colors.BLACK, crystal_rect)
            
            pygame.draw.ellipse(surface, Colors.GOLD, crystal_rect, 2)
    
    def _render_battle_areas(self, surface: pygame.Surface):
        """Render battlefield areas."""
        # Player battlefield
        if self.player_battle_area.collidepoint(pygame.mouse.get_pos()) and self.dragging_card:
            pygame.draw.rect(surface, Colors.GOLD, self.player_battle_area, 3)
        else:
            pygame.draw.rect(surface, Colors.DESERT_SAND, self.player_battle_area, 1)
        
        # Enemy battlefield
        pygame.draw.rect(surface, Colors.RED, self.enemy_battle_area, 1)
        
        # Area labels with enhanced typography
        responsive_typography.render_text(
            "YOUR BATTLEFIELD", TextStyle.CARD_TEXT, surface, 
            (self.player_battle_area.x, self.player_battle_area.bottom + 5),
            custom_color=Colors.GOLD
        )
        
        responsive_typography.render_text(
            "ENEMY BATTLEFIELD", TextStyle.CARD_TEXT, surface, 
            (self.enemy_battle_area.x, self.enemy_battle_area.y - 20),
            custom_color=Colors.RED
        )
    
    def _render_cards(self, surface: pygame.Surface):
        """Render all cards."""
        # Hand cards (non-selected first)
        for card in self.player_hand:
            if card != self.selected_card:
                card.render(surface)
        
        # Enemy hand (render first, behind other cards)
        for card in self.enemy_hand:
            card.render(surface)
        
        # Battlefield cards
        for card in self.player_battlefield + self.enemy_battlefield:
            card.render(surface)
        
        # Selected card last (on top)
        if self.selected_card:
            self.selected_card.render(surface)
    
    def _render_turn_indicator(self, surface: pygame.Surface):
        """Render enhanced turn indicator with better ultrawide visibility."""
        
        # Enhanced positioning for ultrawide displays - avoid overlaps
        if Layout.IS_ULTRAWIDE:
            # Place in top-center of content area, not overlapping cards
            turn_panel_x = Layout.CONTENT_X_OFFSET + Layout.CONTENT_WIDTH // 2
            turn_panel_y = 180  # Higher to avoid enemy cards
        else:
            turn_panel_x = SCREEN_CENTER[0]
            turn_panel_y = 150
        
        # Larger, more visible turn indicator
        if self.phase == CombatPhase.PLAYER_TURN:
            main_text = "YOUR TURN"
            color = Colors.GOLD
            sub_text = f"Turn {self.turn_count} • Mana: {self.player.mana}/{self.player.max_mana}"
            # Check if can play cards
            if not self._can_player_play_cards():
                auto_end_text = "No playable cards - Turn will end automatically"
                responsive_typography.render_text(
                    auto_end_text, TextStyle.CARD_TEXT, surface,
                    (turn_panel_x, turn_panel_y + 80), center=True, custom_color=Colors.RED
                )
        elif self.phase == CombatPhase.ENEMY_TURN:
            main_text = "ENEMY TURN"
            color = Colors.RED  
            sub_text = f"Turn {self.turn_count} • Enemy Mana: {self.enemy.mana}/{self.enemy.max_mana}"
        elif self.phase == CombatPhase.VICTORY:
            main_text = "DIVINE VICTORY!"
            color = Colors.GOLD
            sub_text = "The gods smile upon you!"
        elif self.phase == CombatPhase.DEFEAT:
            main_text = "DEFEAT IN THE UNDERWORLD"
            color = Colors.RED
            sub_text = "The underworld claims another soul..."
        else:
            return
        
        # Enhanced background panel for better visibility
        panel_width = 400
        panel_height = 120
        panel_rect = pygame.Rect(turn_panel_x - panel_width//2, turn_panel_y - 20, 
                                panel_width, panel_height)
        
        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(Colors.BLACK)
        panel_surface.set_alpha(150)
        
        # Glowing border effect
        glow_alpha = int(100 + 80 * abs(math.sin(self.animation_time * 3)))
        # Create border with proper alpha handling
        border_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        border_surface.fill(color)
        border_surface.set_alpha(glow_alpha)
        pygame.draw.rect(panel_surface, color, (0, 0, panel_width, panel_height), 3)
        
        surface.blit(panel_surface, panel_rect.topleft)
        
        # Main turn text with enhanced typography
        responsive_typography.render_text(
            main_text, TextStyle.TITLE_LARGE, surface,
            (turn_panel_x, turn_panel_y + 10), center=True, custom_color=color
        )
        
        # Subtitle information with enhanced typography
        responsive_typography.render_text(
            sub_text, TextStyle.SUBTITLE, surface,
            (turn_panel_x, turn_panel_y + 45), center=True, custom_color=Colors.PAPYRUS
        )
    
    def _render_combat_effects(self, surface: pygame.Surface):
        """Render special combat effects."""
        for effect in self.combat_effects:
            if effect['type'] == 'card_played':
                # Sparkle effect around played card
                card = effect['card']
                for _ in range(int(effect['time'] * 10)):
                    sparkle_x = card.x + random.randint(0, card.width)
                    sparkle_y = card.y + random.randint(0, card.height)
                    sparkle_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                    sparkle_surface.fill(Colors.GOLD)
                    sparkle_surface.set_alpha(int(effect['time'] * 127))
                    surface.blit(sparkle_surface, (sparkle_x, sparkle_y))
    
    def _render_instructions(self, surface: pygame.Surface):
        """Render enhanced combat instructions with ultrawide readability."""
        if self.phase in [CombatPhase.VICTORY, CombatPhase.DEFEAT]:
            instructions = [
                "SPACE: Return to Menu • ESC: Return to Menu",
                "Combat complete! Well fought, warrior!"
            ]
        else:
            # Check if using custom deck
            deck_status = "Custom Deck" if deck_manager.has_saved_deck() else "Starter Deck"
            
            instructions = [
                "Drag cards to battlefield to play them",
                "SPACE: End Turn • ESC: Back to Menu",
                f"Your Mana: {self.player.mana}/{self.player.max_mana} • Enemy Mana: {self.enemy.mana}/{self.enemy.max_mana}",
                f"Turn: {self.turn_count} • {deck_status} • Phase: {self.phase.name.replace('_', ' ')}"
            ]
        
        # Better positioning for ultrawide displays - avoid overlapping with cards
        if Layout.IS_ULTRAWIDE:
            y_start = SCREEN_HEIGHT - 120  # Higher to avoid overlapping with larger cards
            line_spacing = 22  # Balanced spacing
        else:
            y_start = SCREEN_HEIGHT - 150
            line_spacing = 20
        
        y = y_start
        
        for instruction in instructions:
            # Enhanced background for better contrast
            text_size = responsive_typography.measure_text(instruction, TextStyle.TOOLTIP)
            bg_rect = pygame.Rect(SCREEN_CENTER[0] - text_size[0]//2 - 8, y - text_size[1]//2 - 4, 
                                 text_size[0] + 16, text_size[1] + 8)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill(Colors.BLACK)
            bg_surface.set_alpha(140)  # Slightly more opaque
            
            # Add subtle border for enhanced definition
            # Create a temporary surface for the border
            border_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            border_surface.fill(Colors.GOLD)
            border_surface.set_alpha(60)
            pygame.draw.rect(bg_surface, Colors.GOLD, (0, 0, bg_rect.width, bg_rect.height), 1)
            
            surface.blit(bg_surface, bg_rect.topleft)
            
            # Render text with enhanced typography
            responsive_typography.render_text(
                instruction, TextStyle.TOOLTIP, surface,
                (SCREEN_CENTER[0], y), center=True, custom_color=Colors.DESERT_SAND
            )
            
            y += line_spacing
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        for button in self.buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0
        
        # Start combat music
        audio_manager.play_music(AudioTrack.COMBAT, fade_in=2.0)