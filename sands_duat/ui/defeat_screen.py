"""
Defeat Screen

Game over screen shown when the player loses a run or dies in combat.
"""

import pygame
import math
from typing import Dict, Any, Optional
from .base import UIScreen, UIComponent
from .menu_screen import MenuButton
from .theme import get_theme


class DefeatScreen(UIScreen):
    """
    Defeat screen with Egyptian themed game over presentation.
    
    Shows death statistics and options to retry or return to menu.
    """
    
    def __init__(self):
        super().__init__("defeat")
        
        # Defeat data
        self.defeat_data: Optional[Dict[str, Any]] = None
        self.animation_time = 0.0
        
        # UI components
        self.buttons = []
    
    def on_enter(self) -> None:
        """Initialize defeat screen."""
        self.logger.info("Entering defeat screen")
        self.animation_time = 0.0
        self._setup_ui_components()
    
    def on_exit(self) -> None:
        """Clean up defeat screen."""
        self.logger.info("Exiting defeat screen")
        self.clear_components()
    
    def update(self, delta_time: float) -> None:
        """Update defeat screen animations."""
        super().update(delta_time)
        self.animation_time += delta_time
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the defeat screen."""
        # Draw background
        self._draw_background(surface)
        
        # Draw defeat content
        self._draw_defeat_content(surface)
        
        # Render UI components
        super().render(surface)
    
    def set_defeat_data(self, data: Dict[str, Any]) -> None:
        """Set the defeat data to display."""
        self.defeat_data = data
        self.logger.info(f"Defeat data set: {data}")
    
    def _setup_ui_components(self) -> None:
        """Set up defeat screen UI components."""
        theme = get_theme()
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Try again button
        button_width = 300
        button_height = 60
        retry_x = screen_width // 2 - button_width // 2
        retry_y = screen_height - 200
        
        retry_button = MenuButton(
            retry_x, retry_y, button_width, button_height,
            "Try Again", self._try_again
        )
        self.add_component(retry_button)
        
        # Return to menu button
        menu_y = retry_y + button_height + 20
        menu_button = MenuButton(
            retry_x, menu_y, button_width, button_height,
            "Return to Menu", self._return_to_menu
        )
        self.add_component(menu_button)
    
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw Egyptian defeat background."""
        # Dark, ominous gradient
        for y in range(surface.get_height()):
            ratio = y / surface.get_height()
            r = int(20 - ratio * 10)   # 20 to 10
            g = int(10 - ratio * 5)    # 10 to 5
            b = int(15 - ratio * 5)    # 15 to 10
            
            # Ensure no negative values
            r = max(0, r)
            g = max(0, g)
            b = max(0, b)
            
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
        
        # Animated dark particles (sand storm effect)
        self._draw_defeat_particles(surface)
    
    def _draw_defeat_particles(self, surface: pygame.Surface) -> None:
        """Draw animated defeat particles (sandstorm)."""
        import random
        random.seed(24)  # Consistent particles
        
        for i in range(30):
            # Create swirling sand particles
            angle = self.animation_time * 0.3 + i * 0.2
            radius = 50 + i * 20
            
            center_x = surface.get_width() // 2
            center_y = surface.get_height() // 2
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.5
            
            # Dark sand color
            intensity = 60 + int(20 * math.sin(self.animation_time + i))
            color = (intensity, intensity - 20, intensity - 30)
            
            # Draw particle
            size = 1 + int(math.sin(self.animation_time * 1.5 + i) * 1)
            if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                pygame.draw.circle(surface, color, (int(x), int(y)), max(1, size))
    
    def _draw_defeat_content(self, surface: pygame.Surface) -> None:
        """Draw main defeat content."""
        # Defeat title
        font_large = pygame.font.Font(None, 72)
        title_text = font_large.render("DEFEAT", True, (150, 50, 50))
        title_rect = title_text.get_rect()
        title_rect.centerx = surface.get_width() // 2
        title_rect.y = 120
        
        # Add shadow effect
        shadow_offset = 3
        shadow_text = font_large.render("DEFEAT", True, (80, 20, 20))
        shadow_rect = shadow_text.get_rect()
        shadow_rect.center = (title_rect.centerx + shadow_offset, title_rect.centery + shadow_offset)
        surface.blit(shadow_text, shadow_rect)
        surface.blit(title_text, title_rect)
        
        # Defeat message
        font_medium = pygame.font.Font(None, 36)
        message = "The desert has claimed another soul..."
        submessage = "But the sands remember your struggle."
        
        # Main message
        msg_text = font_medium.render(message, True, (200, 150, 150))
        msg_rect = msg_text.get_rect()
        msg_rect.centerx = surface.get_width() // 2
        msg_rect.y = title_rect.bottom + 40
        surface.blit(msg_text, msg_rect)
        
        # Submessage
        font_small = pygame.font.Font(None, 24)
        sub_text = font_small.render(submessage, True, (150, 120, 120))
        sub_rect = sub_text.get_rect()
        sub_rect.centerx = surface.get_width() // 2
        sub_rect.y = msg_rect.bottom + 20
        surface.blit(sub_text, sub_rect)
        
        # Stats display
        if self.defeat_data:
            self._draw_defeat_stats(surface, sub_rect.bottom + 40)
        
        # Egyptian quote
        self._draw_egyptian_quote(surface)
    
    def _draw_defeat_stats(self, surface: pygame.Surface, start_y: int) -> None:
        """Draw defeat statistics."""
        if not self.defeat_data:
            return
        
        font = pygame.font.Font(None, 28)
        center_x = surface.get_width() // 2
        current_y = start_y
        line_height = 35
        
        # Prepare stats to display
        stats = []
        
        if 'turns_survived' in self.defeat_data:
            stats.append(f"Turns Survived: {self.defeat_data['turns_survived']}")
        
        if 'damage_dealt' in self.defeat_data:
            stats.append(f"Damage Dealt: {self.defeat_data['damage_dealt']}")
        
        if 'cards_played' in self.defeat_data:
            stats.append(f"Cards Played: {self.defeat_data['cards_played']}")
        
        if 'hours_reached' in self.defeat_data:
            stats.append(f"Hours Reached: {self.defeat_data['hours_reached']}/12")
        
        if 'cause_of_death' in self.defeat_data:
            stats.append(f"Defeated by: {self.defeat_data['cause_of_death']}")
        
        # Draw stats
        for stat in stats:
            text = font.render(stat, True, (200, 200, 200))
            rect = text.get_rect()
            rect.centerx = center_x
            rect.y = current_y
            surface.blit(text, rect)
            current_y += line_height
    
    def _draw_egyptian_quote(self, surface: pygame.Surface) -> None:
        """Draw an Egyptian-themed quote about death and rebirth."""
        quotes = [
            '"Death is not the opposite of life, but a part of it." - Ancient Proverb',
            '"In the afterlife, the heart is weighed against a feather." - Book of the Dead',
            '"The dead do not rest until they are avenged." - Pharaoh\'s Curse',
            '"What is buried in the sand may rise again." - Desert Wisdom'
        ]
        
        # Select quote based on animation time for variety
        quote_index = int(self.animation_time / 10) % len(quotes)
        quote = quotes[quote_index]
        
        font = pygame.font.Font(None, 22)
        text = font.render(quote, True, (120, 100, 80))
        rect = text.get_rect()
        rect.centerx = surface.get_width() // 2
        rect.y = surface.get_height() - 120
        
        surface.blit(text, rect)
    
    def _try_again(self) -> None:
        """Start a new run."""
        self.logger.info("Starting new run after defeat")
        
        # Get game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        
        if game_flow:
            # Start new run
            game_flow.start_new_run("wanderer")
        else:
            # Fallback: go to menu
            if self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("menu", "fade")
    
    def _return_to_menu(self) -> None:
        """Return to main menu."""
        self.logger.info("Returning to main menu after defeat")
        
        if self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("menu", "fade")