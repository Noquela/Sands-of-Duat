"""
Dynamic Combat Screen

UI for the Initiative Queue based combat system where actions execute
based on Hour-Glass timing rather than discrete turns.

Features:
- Real-time sand visualization
- Action queue preview
- Reaction window indicators
- Continuous gameplay flow
"""

import pygame
import math
import time
import random
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from .base import UIScreen, UIComponent
from .theme import get_theme
from .combat_screen import SandGauge, CardDisplay, HandDisplay  # Reuse existing components
from .menu_screen import MenuButton
from ..core.dynamic_combat_manager import DynamicCombatManager, CombatState
from ..core.action_queue import QueuedAction
from ..core.cards import Card


class ActionQueueDisplay(UIComponent):
    """
    Visual display of the action queue showing what actions are pending
    and when they will execute.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.queued_actions: List[Dict[str, Any]] = []
        self.owner = "player"  # "player" or "enemy"
        
        # Visual settings
        self.action_height = 40
        self.action_spacing = 5
        self.max_visible_actions = 5
        
        # Colors
        self.bg_color = (40, 30, 20, 180)
        self.action_color = (200, 180, 140)
        self.ready_color = (100, 255, 100)
        self.waiting_color = (255, 200, 100)
        self.border_color = (139, 117, 93)
    
    def update_queue(self, actions: List[Dict[str, Any]]) -> None:
        """Update the displayed queue."""
        self.queued_actions = actions
    
    def update(self, delta_time: float) -> None:
        """Update component (required by UIComponent)."""
        # No animation needed for this component
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the action queue."""
        if not self.visible or not self.queued_actions:
            return
        
        # Background
        queue_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(queue_surface, self.bg_color, queue_surface.get_rect())
        pygame.draw.rect(queue_surface, self.border_color, queue_surface.get_rect(), 2)
        
        # Title
        font = pygame.font.Font(None, 20)
        title = f"{self.owner.title()} Queue"
        title_surface = font.render(title, True, (255, 255, 255))
        queue_surface.blit(title_surface, (10, 5))
        
        # Actions
        y_offset = 30
        visible_actions = self.queued_actions[:self.max_visible_actions]
        
        for i, action in enumerate(visible_actions):
            action_rect = pygame.Rect(
                5, y_offset + i * (self.action_height + self.action_spacing),
                self.rect.width - 10, self.action_height
            )
            
            # Action background color based on status
            action_status = action.get('status', 'UNKNOWN')
            if action_status == "READY":
                color = self.ready_color
                status = "READY"
            elif action_status == "CASTING":
                color = (255, 150, 0)  # Orange for casting
                status = f"CASTING ({action['time_remaining']:.1f}s)"
            elif action_status == "READY TO CAST":
                color = (0, 200, 200)  # Cyan for ready to cast
                status = f"READY ({action['cast_time']:.1f}s cast)"
            else:  # WAITING FOR SAND
                color = self.waiting_color
                status = f"WAIT ({action['time_remaining']:.1f}s)"
            
            # Draw action background
            pygame.draw.rect(queue_surface, color, action_rect)
            pygame.draw.rect(queue_surface, self.border_color, action_rect, 1)
            
            # Action text
            action_font = pygame.font.Font(None, 16)
            
            # Card name or action type
            if action['card_name']:
                action_text = action['card_name']
            else:
                action_text = action['action_type'].replace('_', ' ').title()
            
            text_surface = action_font.render(action_text, True, (0, 0, 0))
            queue_surface.blit(text_surface, (action_rect.x + 5, action_rect.y + 5))
            
            # Cost and status
            cost_text = f"Cost: {action['sand_cost']}"
            cost_surface = action_font.render(cost_text, True, (0, 0, 0))
            queue_surface.blit(cost_surface, (action_rect.x + 5, action_rect.y + 20))
            
            status_surface = action_font.render(status, True, (0, 0, 0))
            status_rect = status_surface.get_rect()
            status_rect.right = action_rect.right - 5
            status_rect.centery = action_rect.centery
            queue_surface.blit(status_surface, status_rect)
        
        surface.blit(queue_surface, self.rect.topleft)


class ReactionWindowIndicator(UIComponent):
    """
    Visual indicator for when a reaction window is open and players
    can respond with instant cards.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.is_active = False
        self.time_remaining = 0.0
        self.animation_time = 0.0
    
    def set_active(self, active: bool, time_remaining: float = 0.0) -> None:
        """Set reaction window state."""
        self.is_active = active
        self.time_remaining = time_remaining
    
    def update(self, delta_time: float) -> None:
        """Update animation."""
        self.animation_time += delta_time
        if self.is_active:
            self.time_remaining -= delta_time
    
    def render(self, surface: pygame.Surface) -> None:
        """Render reaction window indicator."""
        if not self.visible or not self.is_active:
            return
        
        # Pulsing background
        pulse = (math.sin(self.animation_time * 6) + 1) / 2  # 0 to 1
        alpha = int(100 + pulse * 100)  # 100 to 200
        
        indicator_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        color = (255, 255, 100, alpha)  # Yellow with pulsing alpha
        pygame.draw.rect(indicator_surface, color, indicator_surface.get_rect())
        
        # Border
        border_color = (255, 255, 0)
        pygame.draw.rect(indicator_surface, border_color, indicator_surface.get_rect(), 3)
        
        # Text
        font = pygame.font.Font(None, 36)
        text = "REACTION WINDOW"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2 - 10))
        indicator_surface.blit(text_surface, text_rect)
        
        # Time remaining
        time_font = pygame.font.Font(None, 24)
        time_text = f"{self.time_remaining:.1f}s remaining"
        time_surface = time_font.render(time_text, True, (0, 0, 0))
        time_rect = time_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2 + 15))
        indicator_surface.blit(time_surface, time_rect)
        
        surface.blit(indicator_surface, self.rect.topleft)


class DamageNumber:
    """Floating damage number effect."""
    def __init__(self, x: int, y: int, damage: int, is_heal: bool = False):
        self.x = float(x)
        self.y = float(y)
        self.start_y = float(y)
        self.damage = damage
        self.is_heal = is_heal
        self.life_time = 2.0  # 2 seconds
        self.max_life = 2.0
        self.velocity_y = -100  # Move upward
        self.velocity_x = random.uniform(-20, 20)  # Slight horizontal drift
        
    def update(self, delta_time: float) -> bool:
        """Update damage number. Returns False if expired."""
        self.life_time -= delta_time
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        self.velocity_y += 150 * delta_time  # Gravity effect
        return self.life_time > 0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the damage number."""
        alpha = max(0, int(255 * (self.life_time / self.max_life)))
        color = (100, 255, 100) if self.is_heal else (255, 100, 100)
        
        font = pygame.font.Font(None, 36)
        text = f"+{self.damage}" if self.is_heal else f"-{self.damage}"
        text_surface = font.render(text, True, color)
        
        # Apply alpha
        text_surface.set_alpha(alpha)
        
        # Scale effect
        scale = 1.0 + (1.0 - self.life_time / self.max_life) * 0.5
        if scale != 1.0:
            width = int(text_surface.get_width() * scale)
            height = int(text_surface.get_height() * scale)
            text_surface = pygame.transform.scale(text_surface, (width, height))
        
        rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text_surface, rect)


class CombatParticle:
    """Combat particle effect."""
    def __init__(self, x: int, y: int, effect_type: str = "impact"):
        self.x = float(x)
        self.y = float(y)
        self.effect_type = effect_type
        self.life_time = 1.0
        self.max_life = 1.0
        self.size = random.uniform(3, 8)
        self.velocity_x = random.uniform(-100, 100)
        self.velocity_y = random.uniform(-150, -50)
        self.color = self._get_particle_color()
        
    def _get_particle_color(self) -> Tuple[int, int, int]:
        """Get particle color based on effect type."""
        if self.effect_type == "impact":
            return (255, 200, 100)  # Orange
        elif self.effect_type == "heal":
            return (100, 255, 100)  # Green
        elif self.effect_type == "sand":
            return (194, 178, 128)  # Sand color
        else:
            return (255, 255, 255)  # White
    
    def update(self, delta_time: float) -> bool:
        """Update particle. Returns False if expired."""
        self.life_time -= delta_time
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        self.velocity_y += 200 * delta_time  # Gravity
        self.size *= 0.98  # Shrink over time
        return self.life_time > 0 and self.size > 0.5
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the particle."""
        alpha = max(0, int(255 * (self.life_time / self.max_life)))
        color = (*self.color, alpha)
        
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (int(self.size), int(self.size)), int(self.size))
        
        surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class DynamicCombatScreen(UIScreen):
    """
    Main dynamic combat interface using Initiative Queue System.
    
    Replaces turn-based combat with continuous action/reaction flow
    based on Hour-Glass sand timing.
    """
    
    def __init__(self):
        super().__init__("dynamic_combat")
        print("DYNAMIC COMBAT SCREEN INITIALIZED WITH IMPROVEMENTS!")
        
        # Combat manager
        self.combat_manager: Optional[DynamicCombatManager] = None
        
        # UI components
        self.player_sand_gauge: Optional[SandGauge] = None
        self.enemy_sand_gauge: Optional[SandGauge] = None
        self.hand_display: Optional[HandDisplay] = None
        self.player_queue_display: Optional[ActionQueueDisplay] = None
        self.enemy_queue_display: Optional[ActionQueueDisplay] = None
        self.reaction_indicator: Optional[ReactionWindowIndicator] = None
        
        # Game state
        self.selected_card: Optional[Card] = None
        self.combat_active = False
        
        # Double-click detection
        self.last_click_time = 0.0
        self.last_clicked_card: Optional[Card] = None
        self.double_click_threshold = 0.5  # seconds
        
        # Visual effects
        self.damage_numbers: List[DamageNumber] = []
        self.combat_particles: List[CombatParticle] = []
        self.screen_shake_intensity = 0.0
        self.screen_shake_duration = 0.0
        self.shake_offset_x = 0.0
        self.shake_offset_y = 0.0
        
        # UI layout
        self.theme = None
    
    def on_enter(self) -> None:
        """Initialize dynamic combat screen."""
        self.logger.info("Entering dynamic combat screen")
        self.theme = get_theme()
        self._setup_ui_components()
        
        # Initialize combat manager
        self.combat_manager = DynamicCombatManager()
        self._setup_combat_callbacks()
        
        # Start demo combat for testing
        
        # Skip combat asset preloading for faster startup
        # self._preload_combat_assets()
        self._start_demo_combat()
    
    def on_exit(self) -> None:
        """Clean up dynamic combat screen."""
        self.logger.info("Exiting dynamic combat screen")
        self.combat_active = False
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up the dynamic combat UI."""
        screen_width = self.theme.display.base_width
        screen_height = self.theme.display.base_height
        
        # Player sand gauge (left side) - will be created after combat setup
        self.player_sand_gauge = None
        
        # Enemy sand gauge (right side) - will be created after combat setup  
        self.enemy_sand_gauge = None
        
        # Player action queue (left side, repositioned for larger cards)
        self.player_queue_display = ActionQueueDisplay(
            20, 100, 200, 300
        )
        self.player_queue_display.owner = "player"
        self.add_component(self.player_queue_display)
        
        # Enemy action queue (right side, repositioned for larger cards)
        self.enemy_queue_display = ActionQueueDisplay(
            screen_width - 220, 100, 200, 300
        )
        self.enemy_queue_display.owner = "enemy"
        self.add_component(self.enemy_queue_display)
        
        # Hand display (bottom) - larger to accommodate 300x420 cards
        self.hand_display = HandDisplay(
            150, screen_height - 450, screen_width - 300, 420
        )
        self.add_component(self.hand_display)
        
        # Reaction window indicator (center top)
        self.reaction_indicator = ReactionWindowIndicator(
            screen_width // 2 - 200, 50, 400, 80
        )
        self.add_component(self.reaction_indicator)
        
        # End combat button (for testing)
        end_button = MenuButton(
            screen_width - 150, 20, 120, 40,
            "End Combat", self._end_combat
        )
        self.add_component(end_button)
    
    def _setup_combat_callbacks(self) -> None:
        """Set up combat manager callbacks."""
        if not self.combat_manager:
            return
        
        self.combat_manager.on_state_changed = self._handle_state_change
        self.combat_manager.on_action_executed = self._handle_action_executed
        self.combat_manager.on_reaction_window = self._handle_reaction_window
        self.combat_manager.on_health_changed = self._handle_health_changed
        self.combat_manager.on_combat_ended = self._handle_combat_ended
    
    def _start_demo_combat(self) -> None:
        """Start a demo combat for testing."""
        if not self.combat_manager:
            return
        
        # Create a demo deck
        demo_deck = self._create_demo_deck()
        
        # Start combat
        self.combat_manager.setup_combat(demo_deck, "desert_mummy")
        
        # Connect UI to combat entities
        if self.combat_manager.player and self.combat_manager.enemy:
            # Create sand gauges now that we have hourglasses
            screen_width = self.theme.display.base_width
            
            self.player_sand_gauge = SandGauge(
                20, 100, 150, 400,
                self.combat_manager.player.hourglass
            )
            self.add_component(self.player_sand_gauge)
            
            self.enemy_sand_gauge = SandGauge(
                screen_width - 170, 100, 150, 400,
                self.combat_manager.enemy.hourglass
            )
            self.add_component(self.enemy_sand_gauge)
            
            if self.hand_display:
                self.hand_display.hourglass = self.combat_manager.player.hourglass
                self.hand_display.set_cards(self.combat_manager.player.hand)
        
        self.combat_active = True
        self.logger.info("Demo dynamic combat started")
    
    def _create_demo_deck(self) -> List[Card]:
        """Create a demo deck using actual starter cards with AI artwork."""
        from ..core.cards import CardEffect, EffectType, TargetType, CardType, CardRarity
        
        deck = []
        
        # Use actual starter cards that have AI artwork
        # Desert Whisper (0 cost) - multiple copies
        for i in range(3):
            card = Card(
                id=f"desert_whisper_{i}",
                name="Desert Whisper",
                sand_cost=0,
                cast_time=0.2,
                card_type=CardType.SKILL,
                rarity=CardRarity.COMMON,
                description="A whisper from the desert sands",
                effects=[
                    CardEffect(
                        effect_type=EffectType.DAMAGE,
                        value=2,
                        target_type=TargetType.ENEMY
                    )
                ]
            )
            deck.append(card)
        
        # Sand Grain (1 cost) - multiple copies
        for i in range(4):
            card = Card(
                id=f"sand_grain_{i}",
                name="Sand Grain",
                sand_cost=1,
                cast_time=0.4,
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                description="Small but numerous",
                effects=[
                    CardEffect(
                        effect_type=EffectType.DAMAGE,
                        value=3,
                        target_type=TargetType.ENEMY
                    )
                ]
            )
            deck.append(card)
        
        # Tomb Strike (2 cost) - multiple copies
        for i in range(3):
            card = Card(
                id=f"tomb_strike_{i}",
                name="Tomb Strike",
                sand_cost=2,
                cast_time=0.6,
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                description="Strike from the ancient tombs",
                effects=[
                    CardEffect(
                        effect_type=EffectType.DAMAGE,
                        value=5,
                        target_type=TargetType.ENEMY
                    )
                ]
            )
            deck.append(card)
        
        # Mummy's Wrath (3 cost) - single copies
        for i in range(2):
            card = Card(
                id=f"mummys_wrath_{i}",
                name="Mummy's Wrath",
                sand_cost=3,
                cast_time=0.8,
                card_type=CardType.ATTACK,
                rarity=CardRarity.UNCOMMON,
                description="The fury of the undead",
                effects=[
                    CardEffect(
                        effect_type=EffectType.DAMAGE,
                        value=8,
                        target_type=TargetType.ENEMY
                    )
                ]
            )
            deck.append(card)
        
        return deck
    
    def _generate_card_rewards(self) -> List[Card]:
        """Generate card rewards for victory."""
        rewards = []
        
        # 50% chance to get a card reward
        if random.random() < 0.5:
            from ..core.cards import CardEffect, EffectType, TargetType, CardType, CardRarity
            
            # Simple reward cards that enhance player power
            reward_options = [
                Card(
                    id="sand_boost",
                    name="Sand Mastery",
                    sand_cost=0,
                    cast_time=0.1,
                    card_type=CardType.SKILL,
                    rarity=CardRarity.UNCOMMON,
                    description="Gain 2 sand instantly",
                    effects=[
                        CardEffect(
                            effect_type=EffectType.GAIN_SAND,
                            value=2,
                            target_type=TargetType.SELF
                        )
                    ]
                ),
                Card(
                    id="healing_light",
                    name="Ra's Blessing",
                    sand_cost=1,
                    cast_time=0.5,
                    card_type=CardType.SKILL,
                    rarity=CardRarity.UNCOMMON,
                    description="Restore health with divine light",
                    effects=[
                        CardEffect(
                            effect_type=EffectType.HEAL,
                            value=8,
                            target_type=TargetType.SELF
                        )
                    ]
                ),
                Card(
                    id="divine_strike",
                    name="Divine Strike",
                    sand_cost=2,
                    cast_time=0.6,
                    card_type=CardType.ATTACK,
                    rarity=CardRarity.UNCOMMON,
                    description="A blessed attack that never misses",
                    effects=[
                        CardEffect(
                            effect_type=EffectType.DAMAGE,
                            value=8,
                            target_type=TargetType.ENEMY
                        )
                    ]
                )
            ]
            
            # Pick a random reward
            reward_card = random.choice(reward_options)
            rewards.append(reward_card)
        
        return rewards
    
    def update(self, delta_time: float) -> None:
        """Update dynamic combat."""
        super().update(delta_time)
        
        if self.combat_active and self.combat_manager:
            self.combat_manager.update(delta_time)
            self._update_ui_displays()
        
        # Update visual effects
        self._update_visual_effects(delta_time)
    
    def _update_ui_displays(self) -> None:
        """Update UI displays with current combat state."""
        if not self.combat_manager:
            return
        
        # Update action queue displays
        if self.player_queue_display:
            player_queue = self.combat_manager.get_queue_preview("player")
            self.player_queue_display.update_queue(player_queue)
        
        if self.enemy_queue_display:
            enemy_queue = self.combat_manager.get_queue_preview("enemy")
            self.enemy_queue_display.update_queue(enemy_queue)
        
        # Update reaction window indicator
        if self.reaction_indicator:
            is_reaction_open = self.combat_manager.is_reaction_window_open()
            time_remaining = self.combat_manager.get_reaction_time_remaining()
            self.reaction_indicator.set_active(is_reaction_open, time_remaining)
        
        # Update hand display
        if self.hand_display and self.combat_manager.player:
            self.hand_display.set_cards(self.combat_manager.player.hand)
    
    def _update_visual_effects(self, delta_time: float) -> None:
        """Update all visual effects."""
        # Update damage numbers
        self.damage_numbers = [dn for dn in self.damage_numbers if dn.update(delta_time)]
        
        # Update particles
        self.combat_particles = [p for p in self.combat_particles if p.update(delta_time)]
        
        # Update screen shake
        if self.screen_shake_duration > 0:
            self.screen_shake_duration -= delta_time
            shake_magnitude = self.screen_shake_intensity * (self.screen_shake_duration / 0.3)  # 0.3s shake
            self.shake_offset_x = random.uniform(-shake_magnitude, shake_magnitude)
            self.shake_offset_y = random.uniform(-shake_magnitude, shake_magnitude)
        else:
            self.shake_offset_x = 0.0
            self.shake_offset_y = 0.0
    
    def add_damage_number(self, x: int, y: int, damage: int, is_heal: bool = False) -> None:
        """Add a floating damage number effect."""
        self.damage_numbers.append(DamageNumber(x, y, damage, is_heal))
    
    def add_combat_particles(self, x: int, y: int, effect_type: str = "impact", count: int = 8) -> None:
        """Add combat particle effects."""
        for _ in range(count):
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            self.combat_particles.append(CombatParticle(x + offset_x, y + offset_y, effect_type))
    
    def trigger_screen_shake(self, intensity: float = 10.0, duration: float = 0.3) -> None:
        """Trigger screen shake effect."""
        self.screen_shake_intensity = intensity
        self.screen_shake_duration = duration
    
    def render(self, surface: pygame.Surface) -> None:
        """Render dynamic combat screen."""
        # Apply screen shake offset
        if self.screen_shake_duration > 0:
            # Create temporary surface for shake effect
            temp_surface = pygame.Surface(surface.get_size())
            self._render_combat_content(temp_surface)
            surface.blit(temp_surface, (self.shake_offset_x, self.shake_offset_y))
        else:
            self._render_combat_content(surface)
    
    def _render_combat_content(self, surface: pygame.Surface) -> None:
        """Render the main combat content."""
        # AI Combat background (if available)
        if hasattr(self, 'background_surface') and self.background_surface:
            # Scale background to fit if needed
            if self.background_surface.get_size() != surface.get_size():
                scaled_bg = pygame.transform.smoothscale(self.background_surface, surface.get_size())
                surface.blit(scaled_bg, (0, 0))
            else:
                surface.blit(self.background_surface, (0, 0))
        else:
            # Load AI background directly if not loaded
            try:
                from ..graphics.background_loader import load_background
                bg = load_background('combat', surface.get_size())
                if bg:
                    surface.blit(bg, (0, 0))
                else:
                    # Egyptian-themed gradient fallback
                    for y in range(surface.get_height()):
                        blend = y / surface.get_height()
                        r = int(60 * (1 - blend) + 25 * blend)
                        g = int(40 * (1 - blend) + 15 * blend)  
                        b = int(20 * (1 - blend) + 5 * blend)
                        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
            except:
                # Simple fallback
                surface.fill((30, 20, 10))
        
        # Combat area - much larger and more prominent
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        combat_area = pygame.Rect(screen_width // 8, screen_height // 6, 
                                 screen_width * 3 // 4, screen_height * 2 // 3)
        
        # Minimal overlay so characters are prominent
        combat_overlay = pygame.Surface((combat_area.width, combat_area.height), pygame.SRCALPHA)
        pygame.draw.rect(combat_overlay, (30, 20, 10, 80), combat_overlay.get_rect())  # Very subtle
        pygame.draw.rect(combat_overlay, (139, 117, 93, 150), combat_overlay.get_rect(), 3)
        surface.blit(combat_overlay, combat_area.topleft)
        
        # Draw large, prominent character sprites
        self._draw_character_sprites(surface, combat_area)
        
        # Player and enemy health bars
        if self.combat_manager and self.combat_manager.player and self.combat_manager.enemy:
            self._draw_health_bars(surface)
        
        # Combat status text
        if self.combat_manager:
            self._draw_combat_status(surface)
        
        # Selected card info
        if self.selected_card:
            self._draw_selected_card_info(surface)
        
        # Render UI components
        super().render(surface)
        
        # Render visual effects on top
        self._render_visual_effects(surface)
        
        # Render AI magical effects
        self._render_ai_effects(surface)
        
        # Skip lighting effects for performance
        # self._render_lighting_effects(surface)
    
    def _draw_character_sprites(self, surface: pygame.Surface, combat_area: pygame.Rect) -> None:
        """Draw large, impressive AI character sprites in the combat area."""
        try:
            # Player sprite (right side) - much larger and more prominent
            player_x = combat_area.centerx + combat_area.width // 4
            player_y = combat_area.centery + 20  # Slightly below center for ground positioning
            
            try:
                player_sprite_path = Path('game_assets/characters/sprites/player_character_idle.png')
                if player_sprite_path.exists():
                    player_sprite = pygame.image.load(str(player_sprite_path)).convert_alpha()
                    
                    # Large, impressive scale - up to 65% of combat area height
                    max_sprite_height = int(combat_area.height * 0.65)
                    original_height = player_sprite.get_height()
                    scale_factor = max_sprite_height / original_height
                    
                    new_width = int(player_sprite.get_width() * scale_factor)
                    new_height = max_sprite_height
                    
                    player_sprite = pygame.transform.smoothscale(player_sprite, (new_width, new_height))
                    sprite_rect = player_sprite.get_rect(center=(player_x, player_y))
                    
                    # Add character shadow for depth
                    shadow_surface = pygame.Surface((sprite_rect.width - 10, 20), pygame.SRCALPHA)
                    pygame.draw.ellipse(shadow_surface, (0, 0, 0, 120), shadow_surface.get_rect())
                    shadow_rect = shadow_surface.get_rect(centerx=sprite_rect.centerx, top=sprite_rect.bottom - 15)
                    surface.blit(shadow_surface, shadow_rect)
                    
                    # Render player sprite
                    surface.blit(player_sprite, sprite_rect)
                    
                    # Add character nameplate with Egyptian styling
                    font = pygame.font.Font(None, 32)
                    name_text = font.render("Desert Wanderer", True, (255, 215, 0))
                    name_bg = pygame.Surface((name_text.get_width() + 20, name_text.get_height() + 8), pygame.SRCALPHA)
                    pygame.draw.rect(name_bg, (60, 40, 20, 200), name_bg.get_rect(), border_radius=5)
                    pygame.draw.rect(name_bg, (139, 117, 93, 255), name_bg.get_rect(), 2, border_radius=5)
                    name_bg.blit(name_text, (10, 4))
                    name_rect = name_bg.get_rect(centerx=player_x, top=sprite_rect.bottom + 10)
                    surface.blit(name_bg, name_rect)
                    
                else:
                    # Fallback player representation - larger
                    pygame.draw.circle(surface, (100, 150, 255), (player_x, player_y), 60)
                    font = pygame.font.Font(None, 24)
                    text = font.render("Player", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(player_x, player_y))
                    surface.blit(text, text_rect)
                    
            except Exception as e:
                self.logger.warning(f"Failed to load player sprite: {e}")
                
            # Enemy sprite (left side) - equally impressive
            enemy_x = combat_area.centerx - combat_area.width // 4
            enemy_y = combat_area.centery + 20
            
            try:
                enemy_sprite_path = Path('game_assets/characters/sprites/anubis_guardian_idle.png')
                if enemy_sprite_path.exists():
                    enemy_sprite = pygame.image.load(str(enemy_sprite_path)).convert_alpha()
                    
                    # Large, impressive scale - up to 70% of combat area height (slightly larger for intimidation)
                    max_sprite_height = int(combat_area.height * 0.70)
                    original_height = enemy_sprite.get_height()
                    scale_factor = max_sprite_height / original_height
                    
                    new_width = int(enemy_sprite.get_width() * scale_factor)
                    new_height = max_sprite_height
                    
                    enemy_sprite = pygame.transform.smoothscale(enemy_sprite, (new_width, new_height))
                    # Flip to face player
                    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
                    sprite_rect = enemy_sprite.get_rect(center=(enemy_x, enemy_y))
                    
                    # Add menacing red glow effect
                    glow_surface = pygame.Surface((sprite_rect.width + 20, sprite_rect.height + 20), pygame.SRCALPHA)
                    for i in range(3):
                        glow_alpha = 30 - (i * 10)
                        glow_rect = pygame.Rect(10 - i * 3, 10 - i * 3, 
                                              sprite_rect.width + i * 6, sprite_rect.height + i * 6)
                        pygame.draw.rect(glow_surface, (255, 0, 0, glow_alpha), glow_rect)
                    glow_pos = (sprite_rect.x - 10, sprite_rect.y - 10)
                    surface.blit(glow_surface, glow_pos)
                    
                    # Add character shadow for depth
                    shadow_surface = pygame.Surface((sprite_rect.width - 10, 25), pygame.SRCALPHA)
                    pygame.draw.ellipse(shadow_surface, (0, 0, 0, 140), shadow_surface.get_rect())
                    shadow_rect = shadow_surface.get_rect(centerx=sprite_rect.centerx, top=sprite_rect.bottom - 20)
                    surface.blit(shadow_surface, shadow_rect)
                    
                    # Render enemy sprite
                    surface.blit(enemy_sprite, sprite_rect)
                    
                    # Add character nameplate with menacing styling
                    font = pygame.font.Font(None, 32)
                    name_text = font.render("Anubis Guardian", True, (255, 50, 50))
                    name_bg = pygame.Surface((name_text.get_width() + 20, name_text.get_height() + 8), pygame.SRCALPHA)
                    pygame.draw.rect(name_bg, (40, 20, 20, 200), name_bg.get_rect(), border_radius=5)
                    pygame.draw.rect(name_bg, (150, 50, 50, 255), name_bg.get_rect(), 2, border_radius=5)
                    name_bg.blit(name_text, (10, 4))
                    name_rect = name_bg.get_rect(centerx=enemy_x, top=sprite_rect.bottom + 10)
                    surface.blit(name_bg, name_rect)
                    
                else:
                    # Fallback enemy representation - larger
                    pygame.draw.circle(surface, (255, 100, 100), (enemy_x, enemy_y), 60)
                    font = pygame.font.Font(None, 24)
                    text = font.render("Enemy", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(enemy_x, enemy_y))
                    surface.blit(text, text_rect)
                    
            except Exception as e:
                self.logger.warning(f"Failed to load enemy sprite: {e}")
                
        except Exception as e:
            self.logger.warning(f"Failed to draw character sprites: {e}")
    
    def _render_ai_effects(self, surface: pygame.Surface) -> None:
        """Render AI magical effects"""
        try:
            from ..graphics.ai_effects_system import get_ai_effects
            effects_system = get_ai_effects()
            effects_system.update(1/60)  # Assume 60 FPS
            effects_system.render(surface)
        except Exception as e:
            self.logger.warning(f"Failed to render AI effects: {e}")
    
    def trigger_card_effect(self, card_name: str, x: int, y: int) -> None:
        """Trigger magical effect when card is played"""
        try:
            from ..graphics.ai_effects_system import get_ai_effects
            effects_system = get_ai_effects()
            effects_system.create_card_cast_effect(x, y, card_name)
        except Exception as e:
            self.logger.warning(f"Failed to trigger card effect: {e}")
    
    def _render_lighting_effects(self, surface: pygame.Surface) -> None:
        """Render dynamic lighting system"""
        try:
            from ..graphics.lighting_system import get_lighting_system, create_lighting_for_screen
            
            # Initialize combat lighting if not already done
            if not hasattr(self, '_lighting_initialized'):
                player_pos = (surface.get_width() * 3//4, surface.get_height() // 2)
                enemy_pos = (surface.get_width() // 4, surface.get_height() // 2)
                
                create_lighting_for_screen("combat", {
                    "player_pos": player_pos,
                    "enemy_pos": enemy_pos
                })
                self._lighting_initialized = True
            
            # Render lighting effects
            lighting_system = get_lighting_system(surface.get_width(), surface.get_height())
            lighting_system.update(1/60)  # Assume 60 FPS
            lighting_system.render_lighting(surface)
            
        except Exception as e:
            self.logger.warning(f"Failed to render lighting effects: {e}")
    
    def _preload_combat_assets(self) -> None:
        """Preload combat assets for smooth performance"""
        try:
            from ..graphics.asset_manager import get_asset_manager, preload_for_screen
            
            # Preload combat-specific assets
            preload_for_screen("combat")
            
            # Preload deck builder assets for transitions
            asset_manager = get_asset_manager()
            asset_manager.preload_set("deck_builder", blocking=False)
            
            self.logger.info("Started combat asset preloading")
            
        except Exception as e:
            self.logger.warning(f"Failed to preload combat assets: {e}")

    def _render_visual_effects(self, surface: pygame.Surface) -> None:
        """Render all visual effects using AI-generated magic effects."""
        # Try to use AI effects system instead of ugly particles
        try:
            from ..graphics.ai_effects_system import get_ai_effects
            ai_effects = get_ai_effects()
            ai_effects.update(1/60)  # Assuming 60 FPS
            ai_effects.render(surface)
        except Exception as e:
            # Fallback to particle system if AI effects not available
            for particle in self.combat_particles:
                particle.render(surface)
        
        # Render damage numbers
        for damage_number in self.damage_numbers:
            damage_number.render(surface)
    
    def _draw_health_bars(self, surface: pygame.Surface) -> None:
        """Draw player and enemy health bars."""
        if not self.combat_manager or not self.combat_manager.player or not self.combat_manager.enemy:
            return
        
        # Player health (bottom left of combat area)
        player_health = self.combat_manager.player.health
        player_max_health = self.combat_manager.player.max_health
        player_ratio = player_health / player_max_health
        
        player_health_rect = pygame.Rect(270, 450, 200, 20)
        pygame.draw.rect(surface, (100, 0, 0), player_health_rect)
        
        player_fill_rect = pygame.Rect(270, 450, int(200 * player_ratio), 20)
        pygame.draw.rect(surface, (0, 200, 0), player_fill_rect)
        
        pygame.draw.rect(surface, (255, 255, 255), player_health_rect, 2)
        
        # Player health text
        font = pygame.font.Font(None, 24)
        player_text = f"Player: {player_health}/{player_max_health}"
        player_surface = font.render(player_text, True, (255, 255, 255))
        surface.blit(player_surface, (270, 475))
        
        # Enemy health (bottom right of combat area)
        enemy_health = self.combat_manager.enemy.health
        enemy_max_health = self.combat_manager.enemy.max_health
        enemy_ratio = enemy_health / enemy_max_health
        
        enemy_health_rect = pygame.Rect(surface.get_width() - 470, 450, 200, 20)
        pygame.draw.rect(surface, (100, 0, 0), enemy_health_rect)
        
        enemy_fill_rect = pygame.Rect(surface.get_width() - 470, 450, int(200 * enemy_ratio), 20)
        pygame.draw.rect(surface, (200, 0, 0), enemy_fill_rect)
        
        pygame.draw.rect(surface, (255, 255, 255), enemy_health_rect, 2)
        
        # Enemy health text
        enemy_text = f"Enemy: {enemy_health}/{enemy_max_health}"
        enemy_surface = font.render(enemy_text, True, (255, 255, 255))
        surface.blit(enemy_surface, (surface.get_width() - 470, 475))
    
    def _draw_combat_status(self, surface: pygame.Surface) -> None:
        """Draw combat status information."""
        stats = self.combat_manager.get_combat_statistics()
        
        font = pygame.font.Font(None, 20)
        status_lines = [
            f"Combat Duration: {stats['duration']:.1f}s",
            f"Actions Executed: {stats['actions_executed']}",
            f"Sand Spent: {stats['total_sand_spent']}",
            f"State: {stats['state']}"
        ]
        
        y = 300
        for line in status_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
            surface.blit(text_surface, text_rect)
            y += 25
    
    def _draw_selected_card_info(self, surface: pygame.Surface) -> None:
        """Draw information about the selected card."""
        if not self.selected_card:
            return
        
        # Draw info panel at bottom right
        panel_width = 300
        panel_height = 120
        panel_x = surface.get_width() - panel_width - 20
        panel_y = surface.get_height() - panel_height - 20
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(surface, (40, 30, 20, 200), panel_rect)
        pygame.draw.rect(surface, (139, 117, 93), panel_rect, 2)
        
        # Card info
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        y_offset = panel_y + 10
        
        # Card name
        name_text = font.render(self.selected_card.name, True, (255, 215, 0))
        surface.blit(name_text, (panel_x + 10, y_offset))
        y_offset += 25
        
        # Cost and cast time
        cost_text = small_font.render(f"Sand Cost: {self.selected_card.sand_cost}", True, (255, 255, 255))
        surface.blit(cost_text, (panel_x + 10, y_offset))
        
        cast_time = getattr(self.selected_card, 'cast_time', 0.0)
        if cast_time > 0:
            cast_text = small_font.render(f"Cast Time: {cast_time:.1f}s", True, (255, 255, 255))
            surface.blit(cast_text, (panel_x + 150, y_offset))
        y_offset += 20
        
        # Description
        desc_lines = []
        if len(self.selected_card.description) > 35:
            # Split long descriptions
            words = self.selected_card.description.split()
            current_line = ""
            for word in words:
                if len(current_line + word) < 35:
                    current_line += word + " "
                else:
                    desc_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                desc_lines.append(current_line.strip())
        else:
            desc_lines = [self.selected_card.description]
        
        for line in desc_lines[:2]:  # Max 2 lines
            desc_text = small_font.render(line, True, (200, 200, 200))
            surface.blit(desc_text, (panel_x + 10, y_offset))
            y_offset += 18
        
        # Double-click instruction
        instruction_text = small_font.render("Double-click to queue for casting!", True, (100, 255, 100))
        surface.blit(instruction_text, (panel_x + 10, panel_y + panel_height - 20))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle dynamic combat events."""
        # Debug: Log all events to see if ANY reach us
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.logger.info(f"DYNAMIC COMBAT: Mouse click detected at {event.pos}, button {event.button}")
        elif event.type == pygame.KEYDOWN:
            self.logger.info(f"DYNAMIC COMBAT: Key pressed: {event.key}")
        
        # Handle card selection and playing with double-click FIRST (before components consume the event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hand_display and self.combat_manager:
                current_time = time.time()
                
                # Debug: Check hand display state
                card_displays = getattr(self.hand_display, 'card_displays', [])
                self.logger.info(f"Click detected. Hand display has {len(card_displays)} card displays")
                
                # Check if clicking on a card in hand
                for i, card_display in enumerate(card_displays):
                    if hasattr(card_display, 'rect') and card_display.rect.collidepoint(event.pos):
                        self.logger.info(f"Clicked on card display {i} at {event.pos}")
                        if hasattr(card_display, 'card') and card_display.card:
                            clicked_card = card_display.card
                            
                            # Check for double-click
                            is_double_click = (
                                self.last_clicked_card == clicked_card and
                                current_time - self.last_click_time <= self.double_click_threshold
                            )
                            
                            if is_double_click:
                                # Double-click: Queue the card for play
                                success = self.combat_manager.queue_player_card(clicked_card)
                                if success:
                                    self.logger.info(f"Double-click queued card: {clicked_card.name}")
                                else:
                                    self.logger.info(f"Failed to queue card: {clicked_card.name}")
                                
                                # Reset double-click tracking
                                self.last_clicked_card = None
                                self.last_click_time = 0.0
                            else:
                                # Single click: Select card and show preview
                                self.selected_card = clicked_card
                                self.logger.info(f"Selected card: {clicked_card.name} (double-click to queue)")
                                
                                # Update double-click tracking
                                self.last_clicked_card = clicked_card
                                self.last_click_time = current_time
                            
                            return True
        
        # Let components handle other events
        if super().handle_event(event):
            return True
        
        return False
    
    def _handle_state_change(self, new_state: CombatState) -> None:
        """Handle combat state changes."""
        self.logger.info(f"Combat state changed to: {new_state.value}")
    
    def _handle_action_executed(self, action: QueuedAction, owner: str) -> None:
        """Handle action execution."""
        self.logger.info(f"{owner} executed: {action.action_type.value}")
    
    def _handle_reaction_window(self, triggering_action: QueuedAction) -> None:
        """Handle reaction window opening."""
        self.logger.info(f"Reaction window opened for: {triggering_action.action_type.value}")
    
    def _handle_health_changed(self, entity_id: str, old_health: int, new_health: int) -> None:
        """Handle health changes."""
        self.logger.info(f"{entity_id} health: {old_health} -> {new_health}")
        
        # Calculate damage/healing
        health_change = new_health - old_health
        is_heal = health_change > 0
        damage_amount = abs(health_change)
        
        # Determine position for effects
        if entity_id == "player":
            effect_x = 400  # Player area
            effect_y = 400
        else:
            effect_x = self.theme.display.base_width - 400  # Enemy area
            effect_y = 400
        
        # Add visual effects
        if damage_amount > 0:
            # Damage/healing number
            self.add_damage_number(effect_x, effect_y, damage_amount, is_heal)
            
            # Particles
            particle_type = "heal" if is_heal else "impact"
            self.add_combat_particles(effect_x, effect_y, particle_type, 10)
            
            # Screen shake for damage
            if not is_heal and damage_amount >= 5:
                intensity = min(15.0, damage_amount * 2.0)
                self.trigger_screen_shake(intensity, 0.2)
    
    def _handle_combat_ended(self, player_won: bool) -> None:
        """Handle combat end."""
        self.combat_active = False
        result = "Victory" if player_won else "Defeat"
        self.logger.info(f"Combat ended: {result}")
        
        # Get game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        
        if game_flow:
            if player_won:
                # Calculate rewards based on combat performance
                card_rewards = self._generate_card_rewards()
                rewards = {
                    'gold': 25 + random.randint(0, 15),  # 25-40 gold
                    'experience': 100,
                    'cards': card_rewards
                }
                game_flow.handle_combat_victory(rewards)
            else:
                game_flow.handle_combat_defeat()
        else:
            # Fallback to direct transition
            if hasattr(self, 'ui_manager') and self.ui_manager:
                if player_won:
                    self.ui_manager.switch_to_screen_with_transition("victory", "fade")
                else:
                    self.ui_manager.switch_to_screen_with_transition("defeat", "fade")
    
    def _end_combat(self) -> None:
        """End combat (for testing)."""
        self.combat_active = False
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("menu", "fade")