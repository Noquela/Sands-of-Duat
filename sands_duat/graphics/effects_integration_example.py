"""
Visual Effects Integration Example

Shows how to integrate the new sophisticated visual effects system
into existing UI screens for cinematic Egyptian underworld atmosphere.

This example demonstrates:
- Initializing effects for different screens
- Card interaction effects
- Combat and victory/defeat effects
- Performance monitoring
- Easy integration with existing UI code
"""

import pygame
from typing import Dict, Any, Tuple

# Import the master visual effects manager
from .master_visual_effects import get_visual_effects_manager, VisualEffectsManager


class ExampleGameScreen:
    """Example showing how to integrate visual effects into a game screen."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Get the global visual effects manager
        self.vfx = get_visual_effects_manager(screen_width, screen_height)
        
        # Initialize for combat screen with context
        self.vfx.initialize_screen_effects("combat", {
            "player_pos": (600, 400),
            "enemy_pos": (1200, 400),
            "hour": 6  # Deep night
        })
        
        # Example cards for demonstration
        self.cards = [
            {"id": "fire_strike", "type": "attack", "rarity": "common", "rect": pygame.Rect(100, 500, 120, 180)},
            {"id": "lightning_bolt", "type": "skill", "rarity": "rare", "rect": pygame.Rect(250, 500, 120, 180)},
            {"id": "divine_blessing", "type": "power", "rarity": "legendary", "rect": pygame.Rect(400, 500, 120, 180)}
        ]
        
        # Register cards with the effects system
        for card in self.cards:
            self.vfx.register_card(card["id"], card["type"], card["rarity"])
        
        # Example state
        self.hovered_card = None
        self.combat_active = True
    
    def handle_card_hover(self, card_id: str, hovering: bool) -> None:
        """Handle card hover events."""
        if hovering and card_id != self.hovered_card:
            # Stop previous hover effect
            if self.hovered_card:
                self.vfx.set_card_hover(self.hovered_card, False)
            
            # Start new hover effect
            self.vfx.set_card_hover(card_id, True)
            self.hovered_card = card_id
            
        elif not hovering and card_id == self.hovered_card:
            # Stop hover effect
            self.vfx.set_card_hover(card_id, False)
            self.hovered_card = None
    
    def play_card(self, card_id: str, target_pos: Tuple[int, int]) -> None:
        """Play a card with dramatic visual effects."""
        # Find the card
        card_data = None
        for card in self.cards:
            if card["id"] == card_id:
                card_data = card
                break
        
        if not card_data:
            return
        
        # Trigger card play effects
        self.vfx.play_card_effect(
            card_id, 
            card_data["rect"], 
            target_pos, 
            card_data["type"]
        )
        
        # Remove card from hand (in real game)
        # self.cards.remove(card_data)
    
    def trigger_victory(self) -> None:
        """Trigger victory effects."""
        self.combat_active = False
        self.vfx.create_victory_effects()
        
        # Optional: Transition to victory screen
        self.vfx.trigger_screen_transition("mystical_portal", 2.0)
    
    def trigger_defeat(self) -> None:
        """Trigger defeat effects."""
        self.combat_active = False
        self.vfx.create_defeat_effects()
        
        # Optional: Transition to defeat screen
        self.vfx.trigger_screen_transition("fade", 1.5)
    
    def update(self, delta_time: float) -> None:
        """Update the screen and all visual effects."""
        # Update visual effects
        self.vfx.update(delta_time)
        
        # Example: Trigger random mystical effects during combat
        if self.combat_active:
            import random
            if random.random() < 0.002:  # Small chance each frame
                self.vfx.particle_system.create_egyptian_mystical_effect(
                    random.randint(200, self.screen_width - 200),
                    random.randint(100, self.screen_height - 200),
                    random.choice(["spirit_wisp", "hieroglyph_magic"]),
                    0.8
                )
        
        # Example: Check performance and adjust if needed
        stats = self.vfx.get_performance_stats()
        if stats["particle_count"] > 1500:
            print(f"High particle count: {stats['particle_count']}")
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the screen with all visual effects."""
        # Clear screen
        surface.fill((0, 0, 0))
        
        # Render all visual effects (parallax, lighting, particles, etc.)
        self.vfx.render(surface)
        
        # Render game elements (cards, UI, etc.)
        self._render_game_elements(surface)
        
        # Render card-specific effects
        for card in self.cards:
            self.vfx.render_card_effects(surface, card["rect"], card["id"])
    
    def _render_game_elements(self, surface: pygame.Surface) -> None:
        """Render basic game elements."""
        # Draw example cards
        for card in self.cards:
            # Card background
            color = (100, 100, 100)
            if card["rarity"] == "rare":
                color = (100, 150, 255)
            elif card["rarity"] == "legendary":
                color = (255, 215, 0)
            
            pygame.draw.rect(surface, color, card["rect"])
            pygame.draw.rect(surface, (255, 255, 255), card["rect"], 2)
        
        # Draw example combat areas
        if self.combat_active:
            # Player area
            pygame.draw.circle(surface, (100, 255, 100), (600, 400), 50, 3)
            # Enemy area
            pygame.draw.circle(surface, (255, 100, 100), (1200, 400), 50, 3)


class ExampleMenuScreen:
    """Example menu screen with atmospheric effects."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Get the visual effects manager
        self.vfx = get_visual_effects_manager(screen_width, screen_height)
        
        # Initialize for menu screen
        self.vfx.initialize_screen_effects("menu", {
            "time_of_day": "night"
        })
    
    def update(self, delta_time: float) -> None:
        """Update menu and effects."""
        self.vfx.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render menu with atmospheric effects."""
        surface.fill((0, 0, 0))
        
        # Render all visual effects
        self.vfx.render(surface)
        
        # Render menu elements
        self._render_menu_elements(surface)
    
    def _render_menu_elements(self, surface: pygame.Surface) -> None:
        """Render basic menu elements."""
        # Draw menu title area
        title_rect = pygame.Rect(self.screen_width // 2 - 200, 100, 400, 100)
        pygame.draw.rect(surface, (40, 35, 30), title_rect)
        pygame.draw.rect(surface, (255, 215, 0), title_rect, 3)
        
        # Draw menu buttons
        button_y = 300
        for i, button_text in enumerate(["Start Game", "Deck Builder", "Settings", "Quit"]):
            button_rect = pygame.Rect(self.screen_width // 2 - 100, button_y + i * 80, 200, 60)
            pygame.draw.rect(surface, (60, 50, 40), button_rect)
            pygame.draw.rect(surface, (200, 180, 140), button_rect, 2)


def example_integration_in_existing_ui():
    """
    Example showing how to integrate visual effects into existing UI code.
    This shows the minimal changes needed to add cinematic effects.
    """
    
    # Initialize Pygame (example)
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    
    # Get the visual effects manager
    vfx = get_visual_effects_manager(1920, 1080)
    
    # Example: In your existing combat screen initialization
    def init_combat_screen():
        # Your existing combat initialization code here...
        
        # Add this line to initialize cinematic effects
        vfx.initialize_screen_effects("combat", {
            "player_pos": (600, 400),
            "enemy_pos": (1200, 400)
        })
    
    # Example: In your existing card hover handler
    def on_card_hover(card_id: str, card_type: str, rarity: str, hovering: bool):
        # Your existing hover code here...
        
        # Add these lines for visual effects
        if hovering:
            vfx.register_card(card_id, card_type, rarity)  # Register if not already done
            vfx.set_card_hover(card_id, True)
        else:
            vfx.set_card_hover(card_id, False)
    
    # Example: In your existing card play handler
    def on_card_played(card_id: str, card_rect: pygame.Rect, target_pos: tuple, card_type: str):
        # Your existing card play logic here...
        
        # Add this line for dramatic visual effects
        vfx.play_card_effect(card_id, card_rect, target_pos, card_type)
    
    # Example: In your existing game loop
    def game_loop():
        running = True
        while running:
            delta_time = clock.tick(60) / 1000.0
            
            # Your existing event handling...
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Your existing game logic updates...
            
            # Add this line to update visual effects
            vfx.update(delta_time)
            
            # Your existing rendering...
            screen.fill((0, 0, 0))
            
            # Add this line to render visual effects BEFORE your game elements
            vfx.render(screen)
            
            # Your existing game element rendering...
            
            # Add this for card effects (if on a screen with cards)
            # for card in your_cards:
            #     vfx.render_card_effects(screen, card.rect, card.id)
            
            pygame.display.flip()
    
    # Example: Performance monitoring
    def check_performance():
        stats = vfx.get_performance_stats()
        print(f"Performance Stats: {stats}")
        
        # Optionally adjust settings based on performance
        if stats["particle_count"] > 1500:
            vfx.set_performance_mode("medium")


# Performance optimization tips
def performance_tips():
    """
    Tips for optimizing visual effects performance:
    
    1. Use performance modes:
       vfx.set_performance_mode("low")    # For low-end devices
       vfx.set_performance_mode("medium") # Balanced
       vfx.set_performance_mode("high")   # High-end devices
    
    2. Enable auto-adjustment:
       vfx.auto_adjust_quality = True  # Automatically adjusts based on FPS
    
    3. Disable effects for specific screens:
       vfx.screen_effects_config["deck_builder"]["particles"] = False
    
    4. Monitor performance:
       stats = vfx.get_performance_stats()
       if stats["particle_count"] > threshold:
           # Reduce effects or switch modes
    
    5. Disable all effects if needed:
       vfx.set_effects_enabled(False)  # For very low-end devices
    
    6. Clear effects when changing screens:
       vfx.clear_all_effects()  # Clears all active effects
    """
    pass


if __name__ == "__main__":
    # Run example
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    
    # Create example screens
    combat_screen = ExampleGameScreen(1920, 1080)
    menu_screen = ExampleMenuScreen(1920, 1080)
    
    current_screen = combat_screen
    running = True
    
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_screen = combat_screen
                elif event.key == pygame.K_2:
                    current_screen = menu_screen
                elif event.key == pygame.K_v:
                    current_screen.trigger_victory()
                elif event.key == pygame.K_d:
                    current_screen.trigger_defeat()
                elif event.key == pygame.K_SPACE:
                    # Example card play
                    if hasattr(current_screen, 'play_card'):
                        current_screen.play_card("fire_strike", (1200, 400))
        
        current_screen.update(delta_time)
        current_screen.render(screen)
        
        pygame.display.flip()
    
    pygame.quit()