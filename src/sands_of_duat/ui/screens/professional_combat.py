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
from ...core.deck_manager import deck_manager
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton

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
    """Professional 3D-style combat card with animations."""
    
    def __init__(self, data: CombatCard, x: int = 0, y: int = 0):
        self.data = data
        self.x = x
        self.y = y
        # Use the enhanced card sizes from constants
        self.width = Layout.CARD_WIDTH
        self.height = Layout.CARD_HEIGHT
        
        # Animation state
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
        """Render the card with Egyptian styling."""
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Card background with gradient
        for i in range(self.height):
            ratio = i / self.height
            r = int(245 * (1 - ratio * 0.2))
            g = int(245 * (1 - ratio * 0.2))
            b = int(220 * (1 - ratio * 0.1))
            color = (r, g, b)
            pygame.draw.line(self.surface, color, (0, i), (self.width, i))
        
        # Rarity border
        rarity_colors = {
            'common': Colors.DESERT_SAND,
            'rare': (138, 43, 226),
            'legendary': (255, 140, 0)
        }
        border_color = rarity_colors.get(self.data.rarity, Colors.DESERT_SAND)
        pygame.draw.rect(self.surface, border_color, (0, 0, self.width, self.height), 3)
        
        # Cost gem
        cost_radius = 15
        cost_center = (20, 20)
        pygame.draw.circle(self.surface, Colors.LAPIS_LAZULI, cost_center, cost_radius)
        pygame.draw.circle(self.surface, Colors.GOLD, cost_center, cost_radius, 2)
        
        # Cost text
        font = pygame.font.Font(None, 20)
        cost_text = font.render(str(self.data.cost), True, Colors.WHITE)
        cost_rect = cost_text.get_rect(center=cost_center)
        self.surface.blit(cost_text, cost_rect)
        
        # Artwork area
        art_rect = pygame.Rect(10, 40, self.width - 20, 80)
        
        # Load ultra-high resolution card artwork using asset loader
        from ...core.asset_loader import get_asset_loader
        asset_loader = get_asset_loader()
        
        # Try to load animated artwork first (1024x1536 ultra-high resolution), then fallback to static
        card_artwork = asset_loader.load_card_art_by_name(self.data.name)
        if not card_artwork:
            # Try fallback by rarity (use new ultra-high resolution assets)
            card_artwork = asset_loader.get_random_card_art_by_rarity(self.data.rarity)
        
        if card_artwork:
            # Scale ultra-high resolution artwork to fit in card art area with proper quality
            # Use LANCZOS for better quality scaling from 1024x1536 source
            scaled_artwork = pygame.transform.smoothscale(card_artwork, (art_rect.width, art_rect.height))
            self.surface.blit(scaled_artwork, art_rect)
        else:
            # Enhanced fallback with Egyptian pattern
            pygame.draw.rect(self.surface, Colors.LAPIS_LAZULI, art_rect)
            # Add hieroglyphic-style pattern
            for i in range(3):
                pattern_rect = pygame.Rect(art_rect.x + 5 + i * 20, art_rect.y + 10, 15, 60)
                pygame.draw.rect(self.surface, Colors.GOLD, pattern_rect, 1)
        
        # Always draw the golden border
        pygame.draw.rect(self.surface, Colors.GOLD, art_rect, 2)
        
        # Card name
        name_font = pygame.font.Font(None, 18)
        name_text = name_font.render(self.data.name, True, Colors.BLACK)
        name_rect = name_text.get_rect(center=(self.width // 2, 135))
        self.surface.blit(name_text, name_rect)
        
        # Attack and Health
        if self.data.card_type == "creature":
            # Attack (bottom-left)
            attack_center = (20, self.height - 20)
            pygame.draw.circle(self.surface, Colors.DESERT_SAND, attack_center, 12)
            pygame.draw.circle(self.surface, Colors.GOLD, attack_center, 12, 2)
            
            attack_font = pygame.font.Font(None, 18)
            attack_text = attack_font.render(str(self.data.attack), True, Colors.BLACK)
            attack_rect = attack_text.get_rect(center=attack_center)
            self.surface.blit(attack_text, attack_rect)
            
            # Health (bottom-right)
            health_center = (self.width - 20, self.height - 20)
            pygame.draw.circle(self.surface, Colors.LAPIS_LAZULI, health_center, 12)
            pygame.draw.circle(self.surface, Colors.GOLD, health_center, 12, 2)
            
            health_text = attack_font.render(str(self.data.health), True, Colors.WHITE)
            health_rect = health_text.get_rect(center=health_center)
            self.surface.blit(health_text, health_rect)
        
        # Description
        desc_font = pygame.font.Font(None, 12)
        words = self.data.description.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if desc_font.size(test_line)[0] <= self.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        y_offset = 150
        for line in lines[:2]:  # Max 2 lines
            line_text = desc_font.render(line, True, Colors.BLACK)
            line_rect = line_text.get_rect(center=(self.width // 2, y_offset))
            self.surface.blit(line_text, line_rect)
            y_offset += 12
    
    def get_rect(self):
        """Get card rectangle."""
        return pygame.Rect(int(self.x + self.shake_offset), 
                          int(self.y + self.hover_offset), 
                          self.width, self.height)
    
    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        """Update card animations."""
        # Hover detection
        self.is_hovered = self.get_rect().collidepoint(mouse_pos)
        
        # Hover animation
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
        """Trigger card play animation."""
        self.play_animation = 1.0
        
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
        """Show damage number animation."""
        self.damage_numbers.append({
            'damage': damage,
            'x': self.x + self.width // 2,
            'y': self.y,
            'speed': 100,
            'life': 2.0,
            'max_life': 2.0,
            'alpha': 255
        })
    
    def render(self, surface: pygame.Surface):
        """Render the card with all effects."""
        draw_pos = (int(self.x + self.shake_offset), int(self.y + self.hover_offset))
        
        # Glow effect
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            glow_alpha = int(100 * self.glow_intensity)
            glow_color = (*Colors.GOLD, glow_alpha)
            
            for i in range(5):
                glow_rect = pygame.Rect(i, i, self.width + 20 - i*2, self.height + 20 - i*2)
                pygame.draw.rect(glow_surface, glow_color, glow_rect, 1)
            
            surface.blit(glow_surface, (draw_pos[0] - 10, draw_pos[1] - 10))
        
        # Main card
        surface.blit(self.surface, draw_pos)
        
        # Particle effects
        for particle in self.particle_effects:
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_surface.fill((*particle['color'], int(particle['alpha'])))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Damage numbers
        font = pygame.font.Font(None, 24)
        for damage in self.damage_numbers:
            damage_text = font.render(f"-{damage['damage']}", True, Colors.RED)
            damage_text.set_alpha(damage['alpha'])
            surface.blit(damage_text, (int(damage['x']), int(damage['y'])))

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
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.enemy_turn_timer = 0.0  # Timer for enemy turn delay
        
        # Background and effects
        self.background_surface = self._create_background()
        self.battlefield_particles = []
        self.combat_effects = []
        
        # Initialize combatants - BALANCED STATS
        self.player = Combatant("PHARAOH", 30, 30, 3, 10)
        self.enemy = Combatant("ANUBIS", 30, 30, 3, 8)  # Equal health, equal starting mana
        
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
        
        # Initialize positions
        self._update_card_positions()
        self._spawn_battlefield_particles()
        
        # Initialize asset loader for animations
        from ...core.asset_loader import get_asset_loader
        self.asset_loader = get_asset_loader()
        
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
        from ...core.asset_loader import get_asset_loader
        
        # Try to load the ultra-high resolution generated Egyptian temple background (4096x2048)
        asset_loader = get_asset_loader()
        temple_bg = asset_loader.load_background('combat')
        
        if temple_bg:
            # Scale the ultra-high resolution temple background to fit screen with quality scaling
            # Use smoothscale for better quality from 4096x2048 source
            background = pygame.transform.smoothscale(temple_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add atmospheric overlay for depth and Hades-style ambiance
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # Enhanced gradient overlay with Egyptian underworld atmosphere  
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT  
                # More sophisticated gradient with Egyptian color scheme
                alpha = int(35 + ratio * 25)  # Subtle darkening
                red_tint = int(10 + ratio * 5)   # Subtle red underworld tint
                blue_tint = int(15 + ratio * 10)  # Deeper blue shadows
                overlay.fill((red_tint, 5, blue_tint, alpha), (0, y, SCREEN_WIDTH, 1))
            
            background.blit(overlay, (0, 0))
            
            # Add subtle particles effect for ultra-high resolution backgrounds
            particle_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for _ in range(20):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 2)
                alpha = random.randint(20, 60)
                particle_color = (*Colors.GOLD, alpha)
                pygame.draw.circle(particle_overlay, particle_color, (x, y), size)
            
            background.blit(particle_overlay, (0, 0))
            return background
        else:
            # Enhanced fallback with Egyptian theme if ultra-high resolution asset loading fails
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                # Egyptian-themed gradient colors
                r = int(25 + ratio * 20)  # Warmer tones
                g = int(15 + ratio * 15)  # Muted greens
                b = int(45 + ratio * 25)  # Deep blues
                background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
            
            # Add Egyptian pattern overlay
            pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for x in range(0, SCREEN_WIDTH, 100):
                for y in range(0, SCREEN_HEIGHT, 100):
                    # Simple hieroglyphic-style pattern
                    pygame.draw.rect(pattern_surface, (*Colors.GOLD, 15), (x, y, 20, 5))
                    pygame.draw.rect(pattern_surface, (*Colors.GOLD, 15), (x, y + 10, 5, 20))
            
            background.blit(pattern_surface, (0, 0))
            return background
    
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
        
        button_width = 100
        button_height = 35
        spacing = 10
        start_x = SCREEN_WIDTH - (len(button_configs) * (button_width + spacing))
        
        for i, (text, action) in enumerate(button_configs):
            x = start_x + i * (button_width + spacing)
            button = AnimatedButton(
                x, 20, button_width, button_height, text, FontSizes.CARD_TEXT,
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
        # Enhanced spacing for ultrawide displays
        if Layout.IS_ULTRAWIDE:
            card_spacing = min(250, (self.hand_area.width - Layout.CARD_WIDTH) // max(1, len(self.player_hand) - 1))
            battlefield_spacing = 200  # More space between battlefield cards
        else:
            card_spacing = min(160, (self.hand_area.width - Layout.CARD_WIDTH) // max(1, len(self.player_hand) - 1))
            battlefield_spacing = 160
        
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
            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
    
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
        self.player.mana = min(self.player.mana + 1, self.player.max_mana)
    
    def _play_card(self, card: CombatCard3D):
        """Play a card from hand to battlefield."""
        if card in self.player_hand and self.player.mana >= card.data.cost:
            self.player_hand.remove(card)
            self.player_battlefield.append(card)
            self.player.mana -= card.data.cost
            
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
        """Resolve spell effects."""
        # Player spells targeting enemy
        for card in self.player_battlefield[:]:
            if card.data.card_type == "spell":
                self.enemy.health -= card.data.attack
                card.show_damage(card.data.attack)
                self.player_battlefield.remove(card)
                
                # Play damage sound effect
                audio_manager.play_sound(SoundEffect.DAMAGE_DEALT, 0.8)
                
                # Add spell effect
                self.combat_effects.append({
                    'type': 'spell_cast',
                    'time': 2.0,
                    'damage': card.data.attack,
                    'target': 'enemy'
                })
        
        # Enemy spells targeting player
        for card in self.enemy_battlefield[:]:
            if card.data.card_type == "spell":
                self.player.health -= card.data.attack
                card.show_damage(card.data.attack)
                self.enemy_battlefield.remove(card)
                
                # Play damage sound effect
                audio_manager.play_sound(SoundEffect.DAMAGE_DEALT, 0.8)
                
                # Add spell effect
                self.combat_effects.append({
                    'type': 'spell_cast',
                    'time': 2.0,
                    'damage': card.data.attack,
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
                
                # Show damage numbers
                if enemy_damage > 0:
                    player_card.show_damage(enemy_damage)
                if player_damage > 0:
                    enemy_card.show_damage(player_damage)
                
                # Remove dead creatures
                if player_card.data.health <= 0:
                    self.player_battlefield.remove(player_card)
                if enemy_card.data.health <= 0:
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
                self.enemy.health -= player_card.data.attack
                self.combat_effects.append({
                    'type': 'direct_attack',
                    'time': 2.0,
                    'attacker': player_card.data.name,
                    'damage': player_card.data.attack,
                    'target': 'enemy'
                })
        
        for enemy_card in enemy_creatures:
            if enemy_card in self.enemy_battlefield and not player_creatures:
                # Attack player directly
                self.player.health -= enemy_card.data.attack
                self.combat_effects.append({
                    'type': 'direct_attack',
                    'time': 2.0,
                    'attacker': enemy_card.data.name,
                    'damage': enemy_card.data.attack,
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
        """Render the combat screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Ultrawide bars
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Battlefield particles
        self._render_battlefield_particles(surface)
        
        # Combat UI
        self._render_combat_ui(surface)
        
        # Battle areas
        self._render_battle_areas(surface)
        
        # Cards
        self._render_cards(surface)
        
        # Turn indicator
        self._render_turn_indicator(surface)
        
        # Combat effects
        self._render_combat_effects(surface)
        
        # Buttons
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
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render enhanced ultrawide side panels with useful information."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        # Much smaller side bars since we're using more content width
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # More sophisticated pattern instead of solid black
        pattern_color = (20, 10, 30)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Add decorative elements to the side panels
        for bar_rect in [left_bar, right_bar]:
            if bar_rect.width > 50:  # Only add decorations if bars are wide enough
                center_x = bar_rect.centerx
                
                # Egyptian-style vertical decorations
                for y in range(100, SCREEN_HEIGHT - 100, 150):
                    # Simple hieroglyphic-style patterns
                    pygame.draw.circle(surface, (*Colors.GOLD, 60), (center_x, y), 8, 2)
                    pygame.draw.rect(surface, (*Colors.GOLD, 60), (center_x - 15, y + 20, 30, 3))
                    pygame.draw.rect(surface, (*Colors.GOLD, 60), (center_x - 3, y + 30, 6, 20))
    
    def _render_battlefield_particles(self, surface: pygame.Surface):
        """Render atmospheric particles."""
        for particle in self.battlefield_particles:
            alpha = int(120 + 80 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*particle['color'], alpha))
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_combat_ui(self, surface: pygame.Surface):
        """Render player and enemy UI."""
        # Player health and mana
        self._render_health_bar(surface, (50, SCREEN_HEIGHT - 80), 
                               self.player.health, self.player.max_health, Colors.GREEN)
        self._render_mana_crystals(surface, (50, SCREEN_HEIGHT - 50), 
                                  self.player.mana, self.player.max_mana)
        
        # Player label
        font = pygame.font.Font(None, FontSizes.BUTTON)
        player_label = font.render("PHARAOH", True, Colors.GOLD)
        surface.blit(player_label, (50, SCREEN_HEIGHT - 110))
        
        # Enemy health and mana
        self._render_health_bar(surface, (50, 80), 
                               self.enemy.health, self.enemy.max_health, Colors.RED)
        self._render_mana_crystals(surface, (50, 110), 
                                  self.enemy.mana, self.enemy.max_mana)
        
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
        
        # Enemy label
        enemy_label = font.render("ANUBIS - JUDGE OF THE DEAD", True, Colors.RED)
        surface.blit(enemy_label, (50, 50))
    
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
        
        # Health text
        font = pygame.font.Font(None, 18)
        health_text = font.render(f"{current}/{maximum}", True, Colors.WHITE)
        text_rect = health_text.get_rect(center=bg_rect.center)
        surface.blit(health_text, text_rect)
    
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
                glow_surface.fill((*Colors.LAPIS_LAZULI, glow_alpha))
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
        
        # Area labels
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        player_label = font.render("YOUR BATTLEFIELD", True, Colors.GOLD)
        surface.blit(player_label, (self.player_battle_area.x, self.player_battle_area.bottom + 5))
        
        enemy_label = font.render("ENEMY BATTLEFIELD", True, Colors.RED)
        surface.blit(enemy_label, (self.enemy_battle_area.x, self.enemy_battle_area.y - 20))
    
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
        title_font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        subtitle_font = pygame.font.Font(None, FontSizes.SUBTITLE)
        
        if self.phase == CombatPhase.PLAYER_TURN:
            main_text = "YOUR TURN"
            color = Colors.GOLD
            sub_text = f"Turn {self.turn_count} • Mana: {self.player.mana}/{self.player.max_mana}"
            # Check if can play cards
            if not self._can_player_play_cards():
                auto_end_text = "No playable cards - Turn will end automatically"
                auto_font = pygame.font.Font(None, FontSizes.CARD_TEXT)
                auto_surface = auto_font.render(auto_end_text, True, Colors.RED)
                auto_rect = auto_surface.get_rect(center=(turn_panel_x, turn_panel_y + 80))
                surface.blit(auto_surface, auto_rect)
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
        panel_surface.fill((*Colors.BLACK, 150))
        
        # Glowing border effect
        glow_alpha = int(100 + 80 * abs(math.sin(self.animation_time * 3)))
        border_color = (*color, glow_alpha)
        pygame.draw.rect(panel_surface, border_color, (0, 0, panel_width, panel_height), 3)
        
        surface.blit(panel_surface, panel_rect.topleft)
        
        # Main turn text with enhanced visibility
        main_surface = title_font.render(main_text, True, color)
        main_rect = main_surface.get_rect(center=(turn_panel_x, turn_panel_y + 10))
        
        # Add text shadow for better readability
        shadow_surface = title_font.render(main_text, True, Colors.BLACK)
        shadow_rect = shadow_surface.get_rect(center=(turn_panel_x + 2, turn_panel_y + 12))
        surface.blit(shadow_surface, shadow_rect)
        surface.blit(main_surface, main_rect)
        
        # Subtitle information
        sub_surface = subtitle_font.render(sub_text, True, Colors.PAPYRUS)
        sub_rect = sub_surface.get_rect(center=(turn_panel_x, turn_panel_y + 45))
        
        # Subtitle shadow
        sub_shadow = subtitle_font.render(sub_text, True, Colors.BLACK)
        sub_shadow_rect = sub_shadow.get_rect(center=(turn_panel_x + 1, turn_panel_y + 46))
        surface.blit(sub_shadow, sub_shadow_rect)
        surface.blit(sub_surface, sub_rect)
    
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
                    sparkle_surface.fill((*Colors.GOLD, int(effect['time'] * 127)))
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
        
        # Enhanced font size for ultrawide readability
        font = pygame.font.Font(None, FontSizes.TOOLTIP)  # Increased from CARD_TEXT
        
        # Better positioning for ultrawide displays - avoid overlapping with cards
        if Layout.IS_ULTRAWIDE:
            y_start = SCREEN_HEIGHT - 120  # Higher to avoid overlapping with larger cards
            line_spacing = 22  # Balanced spacing
        else:
            y_start = SCREEN_HEIGHT - 150
            line_spacing = 20
        
        y = y_start
        
        for instruction in instructions:
            text_surface = font.render(instruction, True, Colors.DESERT_SAND)
            text_rect = text_surface.get_rect(center=(SCREEN_CENTER[0], y))
            
            # Enhanced background for better contrast
            bg_rect = text_rect.inflate(16, 8)  # Larger padding
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((*Colors.BLACK, 140))  # Slightly more opaque
            
            # Add subtle border for enhanced definition
            pygame.draw.rect(bg_surface, (*Colors.GOLD, 60), (0, 0, bg_rect.width, bg_rect.height), 1)
            
            surface.blit(bg_surface, bg_rect.topleft)
            
            # Add text shadow for better readability
            shadow_surface = font.render(instruction, True, Colors.BLACK)
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_CENTER[0] + 1, y + 1))
            surface.blit(shadow_surface, shadow_rect)
            
            surface.blit(text_surface, text_rect)
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