"""
Combat Screen

Main battle interface featuring Hour-Glass Initiative visualization,
card hand management, and real-time combat mechanics.
"""

import pygame
import math
import random
from typing import List, Optional, Dict, Any, Tuple
from .base import UIScreen, UIComponent
from .theme import get_theme
from core.hourglass import HourGlass
from core.cards import Card, CardType, EffectType


class SandGauge(UIComponent):
    """
    Visual representation of the Hour-Glass sand system.
    
    Shows current sand level with smooth animations and
    time-until-next-grain indicators.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, hourglass: HourGlass):
        super().__init__(x, y, width, height)
        self.hourglass = hourglass
        self.sand_particles: List[Dict[str, Any]] = []
        self.animation_time = 0.0
        self.last_sand_count = 0
        
        # Visual settings
        self.glass_color = (200, 200, 255, 100)  # Light blue glass
        self.sand_color = (255, 215, 0)          # Gold sand
        self.frame_color = (139, 117, 93)        # Bronze frame
    
    def update(self, delta_time: float) -> None:
        """Update sand gauge animations."""
        self.animation_time += delta_time
        
        # Update hourglass state
        self.hourglass.update_sand()
        
        # Check for sand changes to trigger animations
        current_sand = self.hourglass.current_sand
        if current_sand != self.last_sand_count:
            if current_sand > self.last_sand_count:
                # Sand was gained - animate new particles
                self._animate_sand_gain()
            self.last_sand_count = current_sand
        
        # Update particle animations
        self._update_particles(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the sand gauge."""
        if not self.visible:
            return
        
        # Draw hourglass frame
        self._draw_hourglass_frame(surface)
        
        # Draw sand level
        self._draw_sand_level(surface)
        
        # Draw sand particles
        self._draw_particles(surface)
        
        # Draw progress indicator for next sand
        self._draw_progress_indicator(surface)
        
        # Draw sand count text
        self._draw_sand_text(surface)
    
    def _draw_hourglass_frame(self, surface: pygame.Surface) -> None:
        """Draw the hourglass frame."""
        # Outer frame
        pygame.draw.rect(surface, self.frame_color, self.rect, self.border_width)
        
        # Glass effect (simplified)
        glass_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)
        glass_surface = pygame.Surface(glass_rect.size, pygame.SRCALPHA)
        glass_surface.fill(self.glass_color)
        surface.blit(glass_surface, glass_rect.topleft)
        
        # Hourglass shape outline
        center_x = self.rect.centerx
        center_y = self.rect.centery
        top_y = self.rect.top + 10
        bottom_y = self.rect.bottom - 10
        width = self.rect.width - 20
        
        # Draw hourglass outline
        points = [
            (center_x - width//2, top_y),
            (center_x + width//2, top_y),
            (center_x + 10, center_y),
            (center_x + width//2, bottom_y),
            (center_x - width//2, bottom_y),
            (center_x - 10, center_y)
        ]
        pygame.draw.polygon(surface, self.frame_color, points, 2)
    
    def _draw_sand_level(self, surface: pygame.Surface) -> None:
        """Draw the current sand level."""
        if self.hourglass.current_sand == 0:
            return
        
        # Calculate sand height based on current sand
        max_height = self.rect.height - 40  # Leave space for frame
        sand_height = (self.hourglass.current_sand / self.hourglass.max_sand) * max_height
        
        # Draw sand in bottom chamber
        sand_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.bottom - 20 - sand_height,
            self.rect.width - 20,
            sand_height
        )
        
        pygame.draw.rect(surface, self.sand_color, sand_rect)
        
        # Add shimmer effect
        shimmer_alpha = int(50 + 30 * math.sin(self.animation_time * 3))
        shimmer_surface = pygame.Surface(sand_rect.size, pygame.SRCALPHA)
        shimmer_surface.fill((*self.sand_color, shimmer_alpha))
        surface.blit(shimmer_surface, sand_rect.topleft)
    
    def _draw_particles(self, surface: pygame.Surface) -> None:
        """Draw animated sand particles."""
        for particle in self.sand_particles:
            if particle['alpha'] > 0:
                color = (*self.sand_color, int(particle['alpha']))
                particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                particle_surface.fill(color)
                surface.blit(particle_surface, (particle['x'], particle['y']))
    
    def _draw_progress_indicator(self, surface: pygame.Surface) -> None:
        """Draw progress until next sand grain."""
        if self.hourglass.current_sand >= self.hourglass.max_sand:
            return
        
        time_until_next = self.hourglass.get_time_until_next_sand()
        if time_until_next == float('inf'):
            return
        
        # Progress bar showing time until next sand
        progress = 1.0 - (time_until_next / (1.0 / self.hourglass.timer.regeneration_rate))
        progress = max(0.0, min(1.0, progress))
        
        bar_width = self.rect.width - 20
        bar_height = 4
        bar_x = self.rect.x + 10
        bar_y = self.rect.bottom + 5
        
        # Background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(surface, self.sand_color, (bar_x, bar_y, progress_width, bar_height))
    
    def _draw_sand_text(self, surface: pygame.Surface) -> None:
        """Draw sand count text."""
        font = pygame.font.Font(None, 24)
        text = f"{self.hourglass.current_sand}/{self.hourglass.max_sand}"
        text_surface = font.render(text, True, self.text_color)
        
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.y = self.rect.bottom + 15
        
        surface.blit(text_surface, text_rect)
    
    def _animate_sand_gain(self) -> None:
        """Create particles for sand gain animation."""
        for _ in range(5):  # Create 5 particles per sand grain
            particle = {
                'x': self.rect.centerx + (random.random() - 0.5) * 20,
                'y': self.rect.top,
                'vx': (random.random() - 0.5) * 2,
                'vy': 2 + random.random() * 2,
                'alpha': 255,
                'life': 1.0
            }
            self.sand_particles.append(particle)
    
    def _update_particles(self, delta_time: float) -> None:
        """Update particle animations."""
        for particle in self.sand_particles[:]:  # Copy list to avoid modification during iteration
            particle['x'] += particle['vx'] * delta_time * 60
            particle['y'] += particle['vy'] * delta_time * 60
            particle['life'] -= delta_time
            particle['alpha'] = max(0, particle['alpha'] - 200 * delta_time)
            
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.sand_particles.remove(particle)


class CardDisplay(UIComponent):
    """
    Displays a single card with hover effects and interaction.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, card: Optional[Card] = None):
        super().__init__(x, y, width, height)
        self.card = card
        self.scale = 1.0
        self.target_scale = 1.0
        self.playable = True
        
        # Visual settings
        self.card_bg_color = (40, 30, 20)
        self.card_border_color = (139, 117, 93)
        self.highlight_color = (255, 215, 0)
    
    def update(self, delta_time: float) -> None:
        """Update card display animations."""
        # Smooth scale animation
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * delta_time * 10
        
        # Update target scale based on hover
        if self.hovered and self.playable:
            self.target_scale = 1.1
        else:
            self.target_scale = 1.0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the card."""
        if not self.visible or not self.card:
            return
        
        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Draw card background
        pygame.draw.rect(surface, self.card_bg_color, scaled_rect)
        
        # Draw border (highlight if hovered)
        border_color = self.highlight_color if self.hovered else self.card_border_color
        pygame.draw.rect(surface, border_color, scaled_rect, 2)
        
        # Draw card content
        self._draw_card_content(surface, scaled_rect)
        
        # Draw unplayable overlay
        if not self.playable:
            overlay = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            surface.blit(overlay, scaled_rect.topleft)
    
    def _draw_card_content(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Draw the card's content (name, cost, description)."""
        # Sand cost
        cost_font = pygame.font.Font(None, 24)
        cost_text = cost_font.render(str(self.card.sand_cost), True, self.highlight_color)
        cost_rect = cost_text.get_rect()
        cost_rect.topright = (rect.right - 5, rect.top + 5)
        surface.blit(cost_text, cost_rect)
        
        # Card name
        name_font = pygame.font.Font(None, 20)
        name_text = name_font.render(self.card.name, True, self.text_color)
        name_rect = name_text.get_rect()
        name_rect.centerx = rect.centerx
        name_rect.top = rect.top + 30
        surface.blit(name_text, name_rect)
        
        # Card type
        type_font = pygame.font.Font(None, 16)
        type_text = type_font.render(self.card.card_type.value.title(), True, (180, 180, 180))
        type_rect = type_text.get_rect()
        type_rect.centerx = rect.centerx
        type_rect.top = name_rect.bottom + 5
        surface.blit(type_text, type_rect)
    
    def set_card(self, card: Optional[Card]) -> None:
        """Set the card to display."""
        self.card = card
    
    def set_playable(self, playable: bool) -> None:
        """Set whether the card can be played."""
        self.playable = playable
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle enhanced card interaction including drag and drop."""
        if not self.visible or not self.card:
            return False
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.playable:
                self.being_dragged = True
                self.drag_offset_x = 0
                self.drag_offset_y = 0
                self._trigger_event("card_drag_start", {"card": self.card})
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.being_dragged:
                self.being_dragged = False
                self.drag_offset_x = 0
                self.drag_offset_y = 0
                
                # Check if card was dropped in a valid play area
                if abs(self.drag_offset_y) > 50:  # Dragged up significantly
                    self.start_play_animation()
                    self._trigger_event("card_played", {"card": self.card})
                else:
                    self._trigger_event("card_drag_end", {"card": self.card})
                return True
        
        elif event.type == pygame.MOUSEMOTION and self.being_dragged:
            # Update drag position
            mouse_x, mouse_y = event.pos
            card_center_x = self.rect.centerx
            card_center_y = self.rect.centery
            
            self.drag_offset_x = mouse_x - card_center_x
            self.drag_offset_y = mouse_y - card_center_y
            return True
        
        return super().handle_event(event)


class HandDisplay(UIComponent):
    """
    Enhanced hand display with smooth card animations and interactions.
    
    Features:
    - Dynamic card spacing based on hand size
    - Smooth card arrangement animations
    - Card hover effects with neighboring card adjustment
    - Visual feedback for playable/unplayable cards
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.cards: List[Card] = []
        self.card_displays: List[CardDisplay] = []
        self.selected_card: Optional[int] = None
        self.hovered_card: Optional[int] = None
        self.hourglass: Optional[HourGlass] = None
        
        # Layout settings (adaptive)
        self.base_card_width = 120
        self.base_card_height = 160
        self.min_card_spacing = 5
        self.max_card_spacing = 20
        self.hover_elevation = -30
        
        # Animation properties
        self.card_positions: List[Tuple[int, int]] = []
        self.target_positions: List[Tuple[int, int]] = []
        self.animation_speed = 8.0
    
    def update(self, delta_time: float) -> None:
        """Update enhanced hand display with animations."""
        # Update card playability based on sand cost
        if self.hourglass:
            for i, card_display in enumerate(self.card_displays):
                if card_display.card:
                    playable = self.hourglass.can_afford(card_display.card.sand_cost)
                    card_display.set_playable(playable)
        
        # Update hover detection
        mouse_pos = pygame.mouse.get_pos()
        new_hovered_card = None
        for i, card_display in enumerate(self.card_displays):
            if card_display.rect.collidepoint(mouse_pos):
                new_hovered_card = i
                break
        
        # Update hovered card and recalculate positions if needed
        if new_hovered_card != self.hovered_card:
            self.hovered_card = new_hovered_card
            self._calculate_card_positions()
        
        # Smooth position animation
        self._animate_card_positions(delta_time)
        
        # Update card displays
        for card_display in self.card_displays:
            card_display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the hand."""
        if not self.visible:
            return
        
        # Render each card
        for card_display in self.card_displays:
            card_display.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for card interaction."""
        # Let card displays handle their own events first
        for i, card_display in enumerate(self.card_displays):
            if card_display.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selected_card = i
                    self._trigger_event("card_selected", {"card_index": i, "card": card_display.card})
                return True
        
        return super().handle_event(event)
    
    def set_cards(self, cards: List[Card]) -> None:
        """Set the cards to display."""
        self.cards = cards
        self._update_card_displays()
    
    def set_hourglass(self, hourglass: HourGlass) -> None:
        """Set the hourglass for sand cost checking."""
        self.hourglass = hourglass
    
    def _update_card_displays(self) -> None:
        """Update the card display components with adaptive sizing."""
        self.card_displays.clear()
        
        if not self.cards:
            return
        
        # Calculate adaptive card size based on hand size
        hand_size = len(self.cards)
        available_width = self.rect.width - 40  # Margins
        
        # Adaptive card width and spacing
        if hand_size <= 5:
            card_width = self.base_card_width
            spacing = self.max_card_spacing
        else:
            # Reduce size for larger hands
            total_card_width = hand_size * self.base_card_width
            total_spacing = (hand_size - 1) * self.min_card_spacing
            
            if total_card_width + total_spacing > available_width:
                # Scale down cards to fit
                scale_factor = available_width / (total_card_width + total_spacing)
                card_width = int(self.base_card_width * scale_factor)
                spacing = self.min_card_spacing
            else:
                card_width = self.base_card_width
                spacing = min(self.max_card_spacing, 
                             (available_width - total_card_width) // (hand_size - 1))
        
        # Create card displays
        for i, card in enumerate(self.cards):
            card_display = CardDisplay(0, 0, card_width, self.base_card_height, card)
            # Add event handlers for new card interactions
            card_display.add_event_handler("card_played", self._on_card_played)
            card_display.add_event_handler("card_drag_start", self._on_card_drag_start)
            card_display.add_event_handler("card_drag_end", self._on_card_drag_end)
            self.card_displays.append(card_display)
        
        # Calculate initial positions
        self._calculate_card_positions()
        
        # Set initial positions (no animation)
        for i, card_display in enumerate(self.card_displays):
            if i < len(self.target_positions):
                x, y = self.target_positions[i]
                card_display.rect.centerx = x
                card_display.rect.centery = y
    
    def _calculate_card_positions(self) -> None:
        """Calculate target positions for all cards with hover effects."""
        if not self.card_displays:
            return
        
        hand_size = len(self.card_displays)
        card_width = self.card_displays[0].rect.width
        spacing = self.min_card_spacing if hand_size > 5 else self.max_card_spacing
        
        # Calculate base layout
        total_width = hand_size * card_width + (hand_size - 1) * spacing
        start_x = self.rect.centerx - total_width // 2 + card_width // 2
        base_y = self.rect.centery
        
        self.target_positions.clear()
        
        for i in range(hand_size):
            x = start_x + i * (card_width + spacing)
            y = base_y
            
            # Adjust for hovered card
            if self.hovered_card is not None:
                if i == self.hovered_card:
                    y += self.hover_elevation  # Lift hovered card
                elif abs(i - self.hovered_card) == 1:
                    # Slightly adjust neighboring cards
                    offset = 5 if i < self.hovered_card else -5
                    x += offset
            
            self.target_positions.append((x, y))
    
    def _animate_card_positions(self, delta_time: float) -> None:
        """Smoothly animate cards to their target positions."""
        if len(self.card_positions) != len(self.target_positions):
            # Initialize positions if needed
            self.card_positions = [(display.rect.centerx, display.rect.centery) 
                                 for display in self.card_displays]
        
        for i, card_display in enumerate(self.card_displays):
            if i < len(self.target_positions):
                target_x, target_y = self.target_positions[i]
                current_x, current_y = self.card_positions[i]
                
                # Smooth interpolation
                new_x = current_x + (target_x - current_x) * delta_time * self.animation_speed
                new_y = current_y + (target_y - current_y) * delta_time * self.animation_speed
                
                self.card_positions[i] = (new_x, new_y)
                card_display.rect.centerx = int(new_x)
                card_display.rect.centery = int(new_y)
    
    def _on_card_played(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card being played."""
        card = event_data.get("card")
        if card:
            # Remove card from hand with animation
            for i, display in enumerate(self.card_displays):
                if display.card and display.card.id == card.id:
                    self.cards.pop(i)
                    self.card_displays.pop(i)
                    self._calculate_card_positions()
                    break
            
            # Trigger parent event
            self._trigger_event("card_played", event_data)
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag start."""
        self._trigger_event("card_drag_start", event_data)
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag end."""
        self._trigger_event("card_drag_end", event_data)


class CombatScreen(UIScreen):
    """
    Main combat interface screen.
    
    Manages the battle UI including sand gauges, card hand,
    enemy display, and combat actions.
    """
    
    def __init__(self):
        super().__init__("combat")
        
        # UI components
        self.player_sand_gauge: Optional[SandGauge] = None
        self.enemy_sand_gauge: Optional[SandGauge] = None
        self.hand_display: Optional[HandDisplay] = None
        
        # Game state references
        self.player_hourglass: Optional[HourGlass] = None
        self.enemy_hourglass: Optional[HourGlass] = None
        
        # Combat state
        self.player_health = 100
        self.player_max_health = 100
        self.enemy_health = 50
        self.enemy_max_health = 50
        
        # Visual settings
        self.font = pygame.font.Font(None, 24)
        self.text_color = (255, 248, 220)  # Cornsilk
    
    def on_enter(self) -> None:
        """Initialize combat screen."""
        self.logger.info("Entering combat screen")
        self._setup_ui_components()
        # Temporarily disable demo setup due to content system conflicts
        # self._setup_demo_combat()
    
    def on_exit(self) -> None:
        """Clean up combat screen."""
        self.logger.info("Exiting combat screen")
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up all UI components for combat using ultrawide-optimized layout."""
        # Create hourglasses if not provided
        if not self.player_hourglass:
            self.player_hourglass = HourGlass()
        if not self.enemy_hourglass:
            self.enemy_hourglass = HourGlass()
        
        # Get theme and layout zones for current resolution
        theme = get_theme()
        player_sand_zone = theme.get_zone('player_sand')
        enemy_sand_zone = theme.get_zone('enemy_sand')
        hand_zone = theme.get_zone('hand_display')
        
        # Player sand gauge (left side for ultrawide)
        gauge_width = min(player_sand_zone.width - 20, 120)
        gauge_height = min(player_sand_zone.height - 20, 200)
        gauge_x = player_sand_zone.x + (player_sand_zone.width - gauge_width) // 2
        gauge_y = player_sand_zone.y + (player_sand_zone.height - gauge_height) // 2
        
        self.player_sand_gauge = SandGauge(gauge_x, gauge_y, gauge_width, gauge_height, self.player_hourglass)
        self.add_component(self.player_sand_gauge)
        
        # Enemy sand gauge (right side for ultrawide)
        enemy_gauge_x = enemy_sand_zone.x + (enemy_sand_zone.width - gauge_width) // 2
        enemy_gauge_y = enemy_sand_zone.y + (enemy_sand_zone.height - gauge_height) // 2
        
        self.enemy_sand_gauge = SandGauge(enemy_gauge_x, enemy_gauge_y, gauge_width, gauge_height, self.enemy_hourglass)
        self.add_component(self.enemy_sand_gauge)
        
        # Hand display (bottom full width for ultrawide)
        hand_margin = 20
        hand_x = hand_zone.x + hand_margin
        hand_y = hand_zone.y + hand_margin
        hand_width = hand_zone.width - (hand_margin * 2)
        hand_height = hand_zone.height - (hand_margin * 2)
        
        self.hand_display = HandDisplay(hand_x, hand_y, hand_width, hand_height)
        self.hand_display.set_hourglass(self.player_hourglass)
        # Add event handlers for enhanced card interactions
        self.hand_display.add_event_handler("card_played", self._on_card_played)
        self.hand_display.add_event_handler("card_drag_start", self._on_card_drag_start)
        self.hand_display.add_event_handler("card_drag_end", self._on_card_drag_end)
        self.add_component(self.hand_display)
    
    def _setup_demo_combat(self) -> None:
        """Setup a demo combat scenario with starter cards."""
        from content.starter_cards import get_starter_deck
        
        try:
            # Get starter deck and draw a hand
            deck = get_starter_deck()
            hand_cards = deck.draw(7)  # Draw 7 cards for demo
            
            # Set up the hand display
            if self.hand_display:
                self.hand_display.set_cards(hand_cards)
            
            self.logger.info(f"Demo combat setup with {len(hand_cards)} cards")
            
        except Exception as e:
            self.logger.error(f"Failed to setup demo combat: {e}")
            # Fallback to empty hand
            if self.hand_display:
                self.hand_display.set_cards([])
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the combat screen."""
        super().render(surface)
        
        # Draw health bars
        self._draw_health_bars(surface)
        
        # Draw combat log or status
        self._draw_combat_status(surface)
    
    def _draw_health_bars(self, surface: pygame.Surface) -> None:
        """Draw player and enemy health bars using theme layout."""
        theme = get_theme()
        player_area_zone = theme.get_zone('player_area')
        enemy_area_zone = theme.get_zone('enemy_area')
        
        # Player health bar (bottom area)
        bar_width = min(player_area_zone.width - 40, 300)
        bar_height = 24
        player_health_rect = pygame.Rect(
            player_area_zone.x + (player_area_zone.width - bar_width) // 2,
            player_area_zone.y + player_area_zone.height - bar_height - 10,
            bar_width,
            bar_height
        )
        self._draw_health_bar(surface, player_health_rect, self.player_health, self.player_max_health, 
                             (0, 255, 0), "Player")
        
        # Enemy health bar (top area)
        enemy_health_rect = pygame.Rect(
            enemy_area_zone.x + (enemy_area_zone.width - bar_width) // 2,
            enemy_area_zone.y + 10,
            bar_width,
            bar_height
        )
        self._draw_health_bar(surface, enemy_health_rect, self.enemy_health, self.enemy_max_health,
                             (255, 0, 0), "Enemy")
    
    def _draw_health_bar(self, surface: pygame.Surface, rect: pygame.Rect, 
                        current: int, maximum: int, color: Tuple[int, int, int], label: str) -> None:
        """Draw a health bar."""
        # Background
        pygame.draw.rect(surface, (50, 50, 50), rect)
        
        # Health bar
        if maximum > 0:
            health_width = int(rect.width * (current / maximum))
            health_rect = pygame.Rect(rect.x, rect.y, health_width, rect.height)
            pygame.draw.rect(surface, color, health_rect)
        
        # Border
        pygame.draw.rect(surface, (200, 200, 200), rect, 2)
        
        # Text
        text = f"{label}: {current}/{maximum}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.bottom = rect.top - 5
        surface.blit(text_surface, text_rect)
    
    def _draw_combat_status(self, surface: pygame.Surface) -> None:
        """Draw combat status information using theme layout."""
        theme = get_theme()
        combat_zone = theme.get_zone('battlefield')
        
        status_text = "Select a card to play"
        text_surface = self.font.render(status_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (combat_zone.x + combat_zone.width // 2, 
                           combat_zone.y + combat_zone.height // 2)
        surface.blit(text_surface, text_rect)
    
    def _on_card_played(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle enhanced card play with effects."""
        card = event_data.get("card")
        if card and self.player_hourglass:
            if self.player_hourglass.can_afford(card.sand_cost):
                # Play the card with sand cost
                self.player_hourglass.spend_sand(card.sand_cost)
                self.logger.info(f"Played card: {card.name} (cost: {card.sand_cost})")
                
                # Apply card effects
                self._apply_card_effects(card)
                
                # Trigger visual effects
                self._trigger_card_play_effects(card)
                
            else:
                self.logger.info(f"Cannot afford card: {card.name} (cost: {card.sand_cost})")
    
    def _on_card_drag_start(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag start."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Started dragging card: {card.name}")
    
    def _on_card_drag_end(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle card drag end."""
        card = event_data.get("card")
        if card:
            self.logger.debug(f"Stopped dragging card: {card.name}")
    
    def _apply_card_effects(self, card: Card) -> None:
        """Apply the effects of a played card."""
        for effect in card.effects:
            if effect.effect_type == EffectType.DAMAGE:
                # Deal damage to enemy
                damage = effect.value
                self.enemy_health = max(0, self.enemy_health - damage)
                self.logger.info(f"Dealt {damage} damage to enemy (Health: {self.enemy_health})")
                
            elif effect.effect_type == EffectType.HEAL:
                # Heal player
                heal = effect.value
                self.player_health = min(self.player_max_health, self.player_health + heal)
                self.logger.info(f"Healed {heal} health (Health: {self.player_health})")
                
            elif effect.effect_type == EffectType.GAIN_SAND:
                # Add sand to hourglass
                sand_gain = effect.value
                current_sand = self.player_hourglass.current_sand
                max_sand = self.player_hourglass.max_sand
                new_sand = min(max_sand, current_sand + sand_gain)
                self.player_hourglass.set_sand(new_sand)
                self.logger.info(f"Gained {sand_gain} sand (Sand: {new_sand})")
                
            elif effect.effect_type == EffectType.DRAW_CARDS:
                # Draw cards (placeholder - would need deck integration)
                cards_to_draw = effect.value
                self.logger.info(f"Draw {cards_to_draw} cards effect applied")
    
    def _trigger_card_play_effects(self, card: Card) -> None:
        """Trigger visual/audio effects for card play."""
        # Add visual effects based on card type
        if card.card_type == CardType.ATTACK:
            # Could trigger screen shake, damage numbers, etc.
            pass
        elif card.card_type == CardType.SKILL:
            # Could trigger particle effects, etc.
            pass
        
        # Log for now (in future could trigger particle systems)
        self.logger.debug(f"Triggered visual effects for {card.card_type.value} card")
    
    def set_player_cards(self, cards: List[Card]) -> None:
        """Set the player's hand."""
        if self.hand_display:
            self.hand_display.set_cards(cards)
    
    def set_player_health(self, current: int, maximum: int) -> None:
        """Set player health."""
        self.player_health = current
        self.player_max_health = maximum
    
    def set_enemy_health(self, current: int, maximum: int) -> None:
        """Set enemy health."""
        self.enemy_health = current
        self.enemy_max_health = maximum