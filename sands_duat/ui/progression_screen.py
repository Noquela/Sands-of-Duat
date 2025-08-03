#!/usr/bin/env python3
"""
Progression Screen - Egyptian Temple Map

Interactive temple map showing player progression through different chambers.
Each chamber represents a different game mode or challenge.
"""

import pygame
import math
import random
from typing import Dict, Any, Optional, List, Callable, Tuple
from .base import UIScreen, UIComponent
from .theme import get_theme
from .animation_system import EasingType
from audio.sound_effects import play_button_sound
from .menu_screen import MenuButton


class TempleChambersMap(UIComponent):
    """
    Interactive map showing temple chambers representing different game areas.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.chambers = self._create_chamber_layout()
        self.selected_chamber = None
        self.hover_chamber = None
        
        # Animation properties
        self.map_scroll_x = 0
        self.map_scroll_y = 0
        self.target_scroll_x = 0
        self.target_scroll_y = 0
        
        # Egyptian colors
        self.sand_color = (194, 178, 128)
        self.stone_color = (139, 117, 93)
        self.gold_color = (255, 215, 0)
        self.path_color = (160, 140, 100)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.chamber_font = pygame.font.Font(None, 24)
    
    def _create_chamber_layout(self) -> Dict[str, Dict[str, Any]]:
        """Create the temple chamber layout."""
        chambers = {
            "entrance": {
                "name": "Temple Entrance",
                "position": (100, 400),
                "unlocked": True,
                "completed": False,
                "chamber_type": "tutorial",
                "description": "Learn the ways of the ancient pharaohs",
                "next_chambers": ["antechamber"]
            },
            "antechamber": {
                "name": "Antechamber of Preparation",
                "position": (300, 350),
                "unlocked": False,
                "completed": False,
                "chamber_type": "deck_building",
                "description": "Assemble your sacred deck of power",
                "next_chambers": ["first_trial"]
            },
            "first_trial": {
                "name": "Trial of Anubis",
                "position": (500, 300),
                "unlocked": False,
                "completed": False,
                "chamber_type": "combat",
                "description": "Face the guardian of the dead",
                "next_chambers": ["chamber_of_isis", "chamber_of_horus"]
            },
            "chamber_of_isis": {
                "name": "Chamber of Isis",
                "position": (400, 200),
                "unlocked": False,
                "completed": False,
                "chamber_type": "combat",
                "description": "Seek the blessing of the mother goddess",
                "next_chambers": ["hall_of_truth"]
            },
            "chamber_of_horus": {
                "name": "Chamber of Horus",
                "position": (600, 200),
                "unlocked": False,
                "completed": False,
                "chamber_type": "combat",
                "description": "Test your sight against the sky god",
                "next_chambers": ["hall_of_truth"]
            },
            "hall_of_truth": {
                "name": "Hall of Two Truths",
                "position": (500, 100),
                "unlocked": False,
                "completed": False,
                "chamber_type": "boss_combat",
                "description": "Face the final judgment of Ma'at",
                "next_chambers": ["pharaoh_tomb"]
            },
            "pharaoh_tomb": {
                "name": "Pharaoh's Burial Chamber",
                "position": (700, 150),
                "unlocked": False,
                "completed": False,
                "chamber_type": "final_boss",
                "description": "Claim the throne of the god-king",
                "next_chambers": []
            }
        }
        return chambers
    
    def update(self, delta_time: float) -> None:
        """Update map animations."""
        # Smooth scrolling
        if abs(self.map_scroll_x - self.target_scroll_x) > 1:
            self.map_scroll_x += (self.target_scroll_x - self.map_scroll_x) * delta_time * 5
        
        if abs(self.map_scroll_y - self.target_scroll_y) > 1:
            self.map_scroll_y += (self.target_scroll_y - self.map_scroll_y) * delta_time * 5
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the temple map."""
        if not self.visible:
            return
        
        # Create map surface
        map_surface = pygame.Surface((self.rect.width, self.rect.height))
        map_surface.fill((45, 35, 25))  # Dark temple background
        
        # Draw temple background decoration
        self._draw_temple_background(map_surface)
        
        # Draw paths between chambers
        self._draw_chamber_paths(map_surface)
        
        # Draw chambers
        self._draw_chambers(map_surface)
        
        # Draw title
        title_text = self.title_font.render("Temple of the Eternal Pharaoh", True, self.gold_color)
        title_rect = title_text.get_rect()
        title_rect.centerx = map_surface.get_width() // 2
        title_rect.y = 20
        map_surface.blit(title_text, title_rect)
        
        # Blit to main surface with scroll offset
        surface.blit(map_surface, (self.rect.x + self.map_scroll_x, self.rect.y + self.map_scroll_y))
    
    def _draw_temple_background(self, surface: pygame.Surface) -> None:
        """Draw decorative temple background elements."""
        # Draw sand dunes in background
        for i in range(5):
            dune_x = i * 150 + 50
            dune_y = surface.get_height() - 80 + random.randint(-20, 20)
            dune_points = [
                (dune_x, surface.get_height()),
                (dune_x + 30, dune_y),
                (dune_x + 80, dune_y + 10),
                (dune_x + 120, surface.get_height())
            ]
            pygame.draw.polygon(surface, self.sand_color, dune_points)
        
        # Draw hieroglyphic-style decorative borders
        border_color = (100, 80, 60)
        pygame.draw.rect(surface, border_color, (10, 10, surface.get_width() - 20, 5))
        pygame.draw.rect(surface, border_color, (10, surface.get_height() - 15, surface.get_width() - 20, 5))
        pygame.draw.rect(surface, border_color, (10, 10, 5, surface.get_height() - 20))
        pygame.draw.rect(surface, border_color, (surface.get_width() - 15, 10, 5, surface.get_height() - 20))
    
    def _draw_chamber_paths(self, surface: pygame.Surface) -> None:
        """Draw connecting paths between unlocked chambers."""
        for chamber_id, chamber in self.chambers.items():
            if not chamber["unlocked"]:
                continue
                
            start_pos = chamber["position"]
            for next_chamber_id in chamber["next_chambers"]:
                next_chamber = self.chambers[next_chamber_id]
                if next_chamber["unlocked"]:
                    end_pos = next_chamber["position"]
                    
                    # Draw path
                    pygame.draw.line(surface, self.path_color, start_pos, end_pos, 4)
                    
                    # Draw decorative dots along path
                    distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
                    steps = int(distance // 20)
                    for step in range(1, steps):
                        t = step / steps
                        dot_x = int(start_pos[0] + t * (end_pos[0] - start_pos[0]))
                        dot_y = int(start_pos[1] + t * (end_pos[1] - start_pos[1]))
                        pygame.draw.circle(surface, self.gold_color, (dot_x, dot_y), 2)
    
    def _draw_chambers(self, surface: pygame.Surface) -> None:
        """Draw all temple chambers."""
        for chamber_id, chamber in self.chambers.items():
            self._draw_single_chamber(surface, chamber_id, chamber)
    
    def _draw_single_chamber(self, surface: pygame.Surface, chamber_id: str, chamber: Dict[str, Any]) -> None:
        """Draw a single temple chamber."""
        pos = chamber["position"]
        is_unlocked = chamber["unlocked"]
        is_completed = chamber["completed"]
        is_hovered = (self.hover_chamber == chamber_id)
        
        # Chamber size and colors
        base_size = 40
        chamber_size = base_size + (10 if is_hovered else 0)
        
        if not is_unlocked:
            chamber_color = (60, 50, 40)  # Locked chambers are dark
            border_color = (80, 70, 60)
        elif is_completed:
            chamber_color = self.gold_color  # Completed chambers are gold
            border_color = (255, 255, 200)
        else:
            chamber_color = self.stone_color  # Available chambers are stone
            border_color = self.gold_color
        
        # Create chamber rect
        chamber_rect = pygame.Rect(
            pos[0] - chamber_size // 2,
            pos[1] - chamber_size // 2,
            chamber_size,
            chamber_size
        )
        
        # Draw chamber
        pygame.draw.rect(surface, chamber_color, chamber_rect)
        pygame.draw.rect(surface, border_color, chamber_rect, 3)
        
        # Draw chamber type symbol
        symbol = self._get_chamber_symbol(chamber["chamber_type"])
        symbol_surface = self.chamber_font.render(symbol, True, (0, 0, 0) if is_completed else (255, 255, 255))
        symbol_rect = symbol_surface.get_rect(center=chamber_rect.center)
        surface.blit(symbol_surface, symbol_rect)
        
        # Draw chamber name
        if is_unlocked:
            name_surface = self.chamber_font.render(chamber["name"], True, self.gold_color)
            name_rect = name_surface.get_rect()
            name_rect.centerx = pos[0]
            name_rect.y = pos[1] + chamber_size // 2 + 10
            surface.blit(name_surface, name_rect)
    
    def _get_chamber_symbol(self, chamber_type: str) -> str:
        """Get the symbol for a chamber type."""
        symbols = {
            "tutorial": "?",
            "deck_building": "D",
            "combat": "⚔",
            "boss_combat": "B",
            "final_boss": "♚"
        }
        return symbols.get(chamber_type, "•")
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle chamber selection and hover."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            # Check if hovering over any chamber
            mouse_pos = event.pos
            map_mouse_x = mouse_pos[0] - self.rect.x - self.map_scroll_x
            map_mouse_y = mouse_pos[1] - self.rect.y - self.map_scroll_y
            
            self.hover_chamber = None
            for chamber_id, chamber in self.chambers.items():
                if chamber["unlocked"]:
                    pos = chamber["position"]
                    distance = math.sqrt((map_mouse_x - pos[0])**2 + (map_mouse_y - pos[1])**2)
                    if distance <= 30:  # Chamber radius
                        self.hover_chamber = chamber_id
                        break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover_chamber:
                self.selected_chamber = self.hover_chamber
                chamber = self.chambers[self.hover_chamber]
                
                # Play selection sound
                try:
                    play_button_sound("click")
                except:
                    pass
                
                # Trigger chamber selection event
                self._trigger_event("chamber_selected", {
                    "chamber_id": self.hover_chamber,
                    "chamber_type": chamber["chamber_type"],
                    "chamber_data": chamber
                })
                return True
        
        return False
    
    def unlock_chamber(self, chamber_id: str) -> None:
        """Unlock a specific chamber."""
        if chamber_id in self.chambers:
            self.chambers[chamber_id]["unlocked"] = True
    
    def complete_chamber(self, chamber_id: str) -> None:
        """Mark a chamber as completed and unlock next chambers."""
        if chamber_id in self.chambers:
            chamber = self.chambers[chamber_id]
            chamber["completed"] = True
            
            # Unlock next chambers
            for next_chamber_id in chamber["next_chambers"]:
                self.unlock_chamber(next_chamber_id)


class ProgressionScreen(UIScreen):
    """
    Main progression screen showing the temple map and player progress.
    """
    
    def __init__(self):
        super().__init__("progression")
        self.temple_map: Optional[TempleChambersMap] = None
        self.ui_manager = None
    
    def on_enter(self) -> None:
        """Initialize progression screen."""
        self.logger.info("Entering progression screen")
        self._setup_ui_components()
    
    def on_exit(self) -> None:
        """Clean up progression screen."""
        self.logger.info("Exiting progression screen")
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up the progression UI."""
        theme = get_theme()
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Back button (top-left corner) - Egyptian themed
        back_button = MenuButton(
            20, 20, 150, 40,
            "⬅ Back to Menu",
            self._back_to_menu
        )
        self.add_component(back_button)
        
        # Create temple map
        map_width = screen_width - 100
        map_height = screen_height - 100
        map_x = 50
        map_y = 50
        
        self.temple_map = TempleChambersMap(map_x, map_y, map_width, map_height)
        
        # Initialize progression state - unlock tutorial chamber initially
        self.temple_map.unlock_chamber("entrance")
        
        # If accessing progression after tutorial, unlock more chambers
        self._setup_post_tutorial_state()
        
        # Set up event handlers
        self.temple_map.add_event_handler("chamber_selected", self._handle_chamber_selection)
        
        self.add_component(self.temple_map)
    
    def _handle_chamber_selection(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle chamber selection."""
        chamber_type = event_data["chamber_type"]
        chamber_id = event_data["chamber_id"]
        
        self.logger.info(f"Chamber selected: {chamber_id} (type: {chamber_type})")
        
        # Route to appropriate screen based on chamber type
        if chamber_type == "tutorial":
            if self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("tutorial", "fade")
        elif chamber_type == "deck_building":
            if self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("deck_builder", "fade")
        elif chamber_type in ["combat", "boss_combat", "final_boss"]:
            if self.ui_manager:
                self.ui_manager.switch_to_screen_with_transition("combat", "slide_left")
    
    def _setup_post_tutorial_state(self) -> None:
        """Setup progression state for players who completed tutorial."""
        # For new players coming from tutorial, unlock the starting chambers
        # This provides a clear progression path after tutorial completion
        if self.temple_map:
            # Mark tutorial as completed and unlock next chambers
            self.temple_map.complete_chamber("entrance")
            self.logger.info("Post-tutorial state: unlocked antechamber and basic progression")
    
    def _back_to_menu(self) -> None:
        """Return to main menu."""
        self.logger.info("Returning to main menu from progression screen")
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("menu", "slide_down")
        else:
            self._trigger_event("switch_screen", {"screen": "menu"})
    
    def update(self, delta_time: float) -> None:
        """Update progression screen."""
        super().update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render progression screen."""
        # Fill background with temple atmosphere
        surface.fill((30, 20, 10))  # Very dark brown
        
        # Render components
        super().render(surface)