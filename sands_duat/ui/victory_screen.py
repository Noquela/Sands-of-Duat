"""
Victory Screen

Victory celebration screen shown when the player completes a run
or wins a significant battle.
"""

import pygame
import math
from typing import Dict, Any, Optional
from .base import UIScreen, UIComponent
from .menu_screen import MenuButton
from .theme import get_theme


class VictoryScreen(UIScreen):
    """
    Victory screen with Egyptian themed celebration.
    
    Shows run statistics, rewards earned, and options to continue
    or return to menu.
    """
    
    def __init__(self):
        super().__init__("victory")
        
        # Victory data
        self.victory_data: Optional[Dict[str, Any]] = None
        self.animation_time = 0.0
        
        # UI components
        self.title_text = None
        self.stats_display = None
        self.buttons = []
    
    def on_enter(self) -> None:
        """Initialize victory screen."""
        self.logger.info("Entering victory screen")
        self.animation_time = 0.0
        
        # Check for victory data from game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        if game_flow:
            # Get the current context data if available
            # This would be set by the transition context
            pass
        
        self.logger.info(f"Victory screen entered with data: {self.victory_data}")
        self._setup_ui_components()
    
    def on_exit(self) -> None:
        """Clean up victory screen."""
        self.logger.info("Exiting victory screen")
        self.clear_components()
    
    def update(self, delta_time: float) -> None:
        """Update victory screen animations."""
        super().update(delta_time)
        self.animation_time += delta_time
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the victory screen."""
        # Draw background
        self._draw_background(surface)
        
        # Draw victory content
        self._draw_victory_content(surface)
        
        # Render UI components
        super().render(surface)
    
    def set_victory_data(self, data: Dict[str, Any]) -> None:
        """Set the victory data to display."""
        self.victory_data = data
        self.logger.info(f"Victory data set: {data}")
    
    def _setup_ui_components(self) -> None:
        """Set up victory screen UI components."""
        theme = get_theme()
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Continue button
        button_width = 300
        button_height = 60
        continue_x = screen_width // 2 - button_width // 2
        continue_y = screen_height - 200
        
        continue_button = MenuButton(
            continue_x, continue_y, button_width, button_height,
            "Continue Adventure", self._continue_adventure
        )
        self.add_component(continue_button)
        
        # Return to menu button
        menu_y = continue_y + button_height + 20
        menu_button = MenuButton(
            continue_x, menu_y, button_width, button_height,
            "Return to Menu", self._return_to_menu
        )
        self.add_component(menu_button)
    
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw Egyptian victory background."""
        # Golden gradient background
        for y in range(surface.get_height()):
            ratio = y / surface.get_height()
            r = int(40 + ratio * 60)   # 40 to 100
            g = int(30 + ratio * 50)   # 30 to 80
            b = int(10 + ratio * 20)   # 10 to 30
            
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
        
        # Animated golden particles
        self._draw_victory_particles(surface)
    
    def _draw_victory_particles(self, surface: pygame.Surface) -> None:
        """Draw animated victory particles."""
        import random
        random.seed(42)  # Consistent particles
        
        for i in range(50):
            # Create floating golden particles
            x = (random.random() * surface.get_width())
            base_y = random.random() * surface.get_height()
            
            # Animate particles floating upward
            offset = math.sin(self.animation_time * 0.5 + i * 0.1) * 10
            y = base_y + offset - (self.animation_time * 20) % surface.get_height()
            
            # Golden color with some variation
            golden_intensity = 200 + int(30 * math.sin(self.animation_time + i))
            color = (golden_intensity, golden_intensity - 50, 50)
            
            # Draw particle
            size = 2 + int(math.sin(self.animation_time * 2 + i) * 1)
            pygame.draw.circle(surface, color, (int(x), int(y)), size)
    
    def _draw_victory_content(self, surface: pygame.Surface) -> None:
        """Draw main victory content."""
        # Victory title
        font_large = pygame.font.Font(None, 72)
        title_text = font_large.render("VICTORY!", True, (255, 215, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = surface.get_width() // 2
        title_rect.y = 100
        
        # Add glow effect
        glow_offset = int(math.sin(self.animation_time * 3) * 2)
        glow_text = font_large.render("VICTORY!", True, (200, 150, 0))
        glow_rect = glow_text.get_rect()
        glow_rect.center = (title_rect.centerx + glow_offset, title_rect.centery + glow_offset)
        surface.blit(glow_text, glow_rect)
        surface.blit(title_text, title_rect)
        
        # Victory message
        font_medium = pygame.font.Font(None, 36)
        if self.victory_data:
            if self.victory_data.get('run_completed', False):
                message = "You have conquered the 12 Hours of Night!"
                submessage = "The pharaoh's curse is broken!"
            else:
                message = "Battle won! The desert spirits smile upon you."
                submessage = "Continue your journey through the Duat..."
        else:
            message = "Another step closer to freedom!"
            submessage = "The path ahead grows brighter..."
        
        # Main message
        msg_text = font_medium.render(message, True, (255, 255, 200))
        msg_rect = msg_text.get_rect()
        msg_rect.centerx = surface.get_width() // 2
        msg_rect.y = title_rect.bottom + 40
        surface.blit(msg_text, msg_rect)
        
        # Submessage
        font_small = pygame.font.Font(None, 24)
        sub_text = font_small.render(submessage, True, (200, 200, 150))
        sub_rect = sub_text.get_rect()
        sub_rect.centerx = surface.get_width() // 2
        sub_rect.y = msg_rect.bottom + 20
        surface.blit(sub_text, sub_rect)
        
        # Stats display
        if self.victory_data:
            self._draw_victory_stats(surface, sub_rect.bottom + 40)
    
    def _draw_victory_stats(self, surface: pygame.Surface, start_y: int) -> None:
        """Draw victory statistics."""
        if not self.victory_data:
            return
        
        font = pygame.font.Font(None, 28)
        center_x = surface.get_width() // 2
        current_y = start_y
        line_height = 35
        
        # Prepare stats to display
        stats = []
        
        if 'turns' in self.victory_data:
            stats.append(f"Combat Duration: {self.victory_data['turns']} turns")
        
        if 'gold_earned' in self.victory_data:
            stats.append(f"Gold Earned: {self.victory_data['gold_earned']}")
        
        if 'total_gold' in self.victory_data:
            stats.append(f"Total Gold: {self.victory_data['total_gold']}")
        
        if 'hours_completed' in self.victory_data:
            stats.append(f"Hours Completed: {self.victory_data['hours_completed']}/12")
        
        if 'final_score' in self.victory_data:
            stats.append(f"Final Score: {self.victory_data['final_score']}")
        
        # Draw stats
        for stat in stats:
            text = font.render(stat, True, (255, 255, 255))
            rect = text.get_rect()
            rect.centerx = center_x
            rect.y = current_y
            surface.blit(text, rect)
            current_y += line_height
        
        # Draw card rewards
        if 'cards' in self.victory_data and self.victory_data['cards']:
            current_y += 20  # Extra spacing
            reward_title = font.render("Cards Earned:", True, (255, 215, 0))
            title_rect = reward_title.get_rect()
            title_rect.centerx = center_x
            title_rect.y = current_y
            surface.blit(reward_title, title_rect)
            current_y += line_height
            
            for card in self.victory_data['cards']:
                card_text = font.render(f"• {card.name}", True, (100, 255, 100))
                card_rect = card_text.get_rect()
                card_rect.centerx = center_x
                card_rect.y = current_y
                surface.blit(card_text, card_rect)
                current_y += line_height
    
    def _continue_adventure(self) -> None:
        """Continue the adventure (return to map or start new run)."""
        self.logger.info("Continuing adventure")
        
        # Get game flow manager
        game_flow = getattr(self.ui_manager, 'game_flow', None) if self.ui_manager else None
        
        if game_flow:
            self.logger.info(f"Game flow manager found. Victory data: {self.victory_data}")
            # Check if run is completed
            if self.victory_data and self.victory_data.get('run_completed', False):
                self.logger.info("Run completed - starting new run")
                # Start new run
                game_flow.start_new_run("wanderer")
            else:
                self.logger.info("Returning to progression screen via game flow manager")
                # Return to progression screen (temple map)
                from ..core.game_flow_manager import GameScreen
                game_flow.transition_to_screen(GameScreen.PROGRESSION)
        else:
            self.logger.info("No game flow manager - using fallback")
            # Fallback
            if self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("progression", "fade")
    
    def _return_to_menu(self) -> None:
        """Return to main menu."""
        self.logger.info("Returning to main menu")
        
        if self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("menu", "fade")