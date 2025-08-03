"""
Canopic Chamber Component

Egyptian-themed information grouping component that organizes related player/enemy
information using authentic canopic jar design metaphors. Implements the 
information architecture reorganization for the Sands of Duat game.
"""

import pygame
import math
from typing import Dict, List, Optional, Any
from ..base import UIComponent
from ..theme import get_theme


class CanoplicChamber(UIComponent):
    """
    Container for grouped player/enemy information using Egyptian canopic chamber design.
    
    Canopic chambers were used to store vital organs during mummification,
    making them perfect metaphors for vital game information storage.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, chamber_type: str = "player"):
        super().__init__(x, y, width, height)
        self.chamber_type = chamber_type  # "player" or "enemy"
        self.information_slots: Dict[str, Any] = {}
        self.animation_time = 0.0
        
        # Enable Egyptian feedback for enhanced interactions
        self.enable_egyptian_feedback('all')
        
        # Chamber-specific styling
        if chamber_type == "player":
            self.primary_color = (255, 215, 0)  # Gold for player
            self.secondary_color = (212, 184, 150)  # Sandstone
            self.accent_color = (139, 117, 93)  # Bronze
            self.guardian_deity = "Horus"  # Player protection
        else:
            self.primary_color = (200, 100, 100)  # Muted red for enemy
            self.secondary_color = (180, 150, 130)  # Cooler stone
            self.accent_color = (120, 80, 60)  # Darker bronze
            self.guardian_deity = "Anubis"  # Death/enemy
        
        # Information organization slots
        self.slots = {
            'vital_status': {'type': 'health', 'priority': 1, 'content': None},
            'resource_level': {'type': 'sand', 'priority': 2, 'content': None},
            'active_effects': {'type': 'effects', 'priority': 3, 'content': None},
            'intent_preview': {'type': 'intent', 'priority': 2, 'content': None}
        }
    
    def set_information_slot(self, slot_name: str, content: Any) -> None:
        """Set content for a specific information slot."""
        if slot_name in self.slots:
            self.slots[slot_name]['content'] = content
    
    def update(self, delta_time: float) -> None:
        """Update chamber animations and information display."""
        self.animation_time += delta_time
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the canopic chamber with organized information."""
        if not self.visible:
            return
        
        # Draw chamber background with papyrus styling
        self._draw_chamber_background(surface)
        
        # Draw guardian deity symbol
        self._draw_guardian_symbol(surface)
        
        # Draw information slots in hierarchical order
        self._draw_information_slots(surface)
        
        # Draw chamber borders and decorative elements
        self._draw_chamber_borders(surface)
    
    def _draw_chamber_background(self, surface: pygame.Surface) -> None:
        """Draw Egyptian-themed chamber background."""
        # Main chamber body
        chamber_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 
                                 self.rect.width - 10, self.rect.height - 10)
        
        # Create papyrus-style background with subtle texture
        bg_surface = pygame.Surface((chamber_rect.width, chamber_rect.height), pygame.SRCALPHA)
        bg_surface.fill(self.secondary_color)
        
        # Add subtle texture lines to simulate papyrus
        for i in range(0, chamber_rect.height, 8):
            alpha = int(30 + 10 * math.sin(self.animation_time + i * 0.1))
            line_color = (*self.accent_color, alpha)
            line_surface = pygame.Surface((chamber_rect.width, 1), pygame.SRCALPHA)
            line_surface.fill(line_color)
            bg_surface.blit(line_surface, (0, i))
        
        surface.blit(bg_surface, chamber_rect.topleft)
    
    def _draw_guardian_symbol(self, surface: pygame.Surface) -> None:
        """Draw the guardian deity symbol at the top of the chamber."""
        symbol_size = 30
        symbol_x = self.rect.centerx - symbol_size // 2
        symbol_y = self.rect.y + 15
        
        # Animated glow for the symbol
        glow_intensity = 0.7 + 0.3 * math.sin(self.animation_time * 2)
        glow_color = (*self.primary_color, int(100 * glow_intensity))
        
        # Create glow effect
        glow_surface = pygame.Surface((symbol_size + 10, symbol_size + 10), pygame.SRCALPHA)
        glow_surface.fill(glow_color)
        surface.blit(glow_surface, (symbol_x - 5, symbol_y - 5))
        
        if self.guardian_deity == "Horus":
            # Draw Eye of Horus for player chamber
            self._draw_eye_of_horus(surface, symbol_x, symbol_y, symbol_size)
        else:
            # Draw Anubis symbol for enemy chamber
            self._draw_anubis_symbol(surface, symbol_x, symbol_y, symbol_size)
    
    def _draw_eye_of_horus(self, surface: pygame.Surface, x: int, y: int, size: int) -> None:
        """Draw the Eye of Horus symbol."""
        # Main eye shape
        eye_rect = pygame.Rect(x, y + size // 3, size, size // 3)
        pygame.draw.ellipse(surface, self.primary_color, eye_rect)
        pygame.draw.ellipse(surface, self.accent_color, eye_rect, 2)
        
        # Eye pupil
        pupil_x = x + size // 3
        pupil_y = y + size // 2
        pygame.draw.circle(surface, (47, 27, 20), (pupil_x, pupil_y), size // 8)
        
        # Eye markings (simplified)
        marking_points = [
            (x + size - 5, y + size // 2),
            (x + size, y + size - 5),
            (x + size - 10, y + size - 3)
        ]
        pygame.draw.lines(surface, self.accent_color, False, marking_points, 3)
    
    def _draw_anubis_symbol(self, surface: pygame.Surface, x: int, y: int, size: int) -> None:
        """Draw simplified Anubis symbol."""
        # Jackal head silhouette
        head_points = [
            (x + size // 2, y),  # Top of head
            (x + size - 3, y + size // 3),  # Right ear
            (x + size, y + size // 2),  # Right snout
            (x + size - 5, y + size),  # Right bottom
            (x + 5, y + size),  # Left bottom
            (x, y + size // 2),  # Left snout
            (x + 3, y + size // 3)  # Left ear
        ]
        
        pygame.draw.polygon(surface, self.primary_color, head_points)
        pygame.draw.polygon(surface, self.accent_color, head_points, 2)
        
        # Eyes
        pygame.draw.circle(surface, (200, 50, 50), (x + size // 3, y + size // 2), 3)
        pygame.draw.circle(surface, (200, 50, 50), (x + 2 * size // 3, y + size // 2), 3)
    
    def _draw_information_slots(self, surface: pygame.Surface) -> None:
        """Draw organized information in hierarchical slots."""
        slot_height = (self.rect.height - 80) // len(self.slots)  # Account for symbol space
        current_y = self.rect.y + 60  # Start below guardian symbol
        
        # Sort slots by priority
        sorted_slots = sorted(self.slots.items(), key=lambda x: x[1]['priority'])
        
        for slot_name, slot_data in sorted_slots:
            if slot_data['content'] is not None:
                self._draw_information_slot(surface, slot_name, slot_data, 
                                          self.rect.x + 15, current_y, 
                                          self.rect.width - 30, slot_height - 5)
            current_y += slot_height
    
    def _draw_information_slot(self, surface: pygame.Surface, slot_name: str, 
                             slot_data: Dict, x: int, y: int, width: int, height: int) -> None:
        """Draw individual information slot with Egyptian styling."""
        # Slot background
        slot_rect = pygame.Rect(x, y, width, height)
        slot_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Priority-based background intensity
        alpha = min(255, 50 + slot_data['priority'] * 30)
        slot_surface.fill((*self.accent_color, alpha))
        surface.blit(slot_surface, (x, y))
        
        # Slot border
        border_color = self.primary_color if slot_data['priority'] <= 2 else self.accent_color
        pygame.draw.rect(surface, border_color, slot_rect, 2)
        
        # Content rendering based on slot type
        content = slot_data['content']
        if slot_data['type'] == 'health':
            self._draw_health_content(surface, content, slot_rect)
        elif slot_data['type'] == 'sand':
            self._draw_sand_content(surface, content, slot_rect)
        elif slot_data['type'] == 'effects':
            self._draw_effects_content(surface, content, slot_rect)
        elif slot_data['type'] == 'intent':
            self._draw_intent_content(surface, content, slot_rect)
    
    def _draw_health_content(self, surface: pygame.Surface, health_data: Any, rect: pygame.Rect) -> None:
        """Draw health information with ankh symbols."""
        if not health_data:
            return
        
        # Ankh symbol for health
        ankh_size = min(rect.height - 10, 25)
        ankh_x = rect.x + 10
        ankh_y = rect.centery - ankh_size // 2
        
        # Draw simplified ankh
        # Vertical line
        pygame.draw.line(surface, self.primary_color, 
                        (ankh_x + ankh_size // 2, ankh_y), 
                        (ankh_x + ankh_size // 2, ankh_y + ankh_size), 3)
        # Horizontal line
        pygame.draw.line(surface, self.primary_color,
                        (ankh_x, ankh_y + ankh_size // 3),
                        (ankh_x + ankh_size, ankh_y + ankh_size // 3), 3)
        # Loop
        loop_rect = pygame.Rect(ankh_x + ankh_size // 4, ankh_y, ankh_size // 2, ankh_size // 3)
        pygame.draw.ellipse(surface, self.primary_color, loop_rect, 3)
        
        # Health text
        font = pygame.font.Font(None, 24)
        if hasattr(health_data, 'current') and hasattr(health_data, 'maximum'):
            health_text = f"{health_data.current}/{health_data.maximum}"
        else:
            health_text = str(health_data)
        
        text_surface = font.render(health_text, True, (255, 248, 220))
        text_x = ankh_x + ankh_size + 10
        text_y = rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_sand_content(self, surface: pygame.Surface, sand_data: Any, rect: pygame.Rect) -> None:
        """Draw sand/resource information with hourglass visualization."""
        if not sand_data:
            return
        
        # Hourglass symbol
        hourglass_size = min(rect.height - 10, 25)
        hourglass_x = rect.x + 10
        hourglass_y = rect.centery - hourglass_size // 2
        
        # Draw simplified hourglass
        points = [
            (hourglass_x, hourglass_y),
            (hourglass_x + hourglass_size, hourglass_y),
            (hourglass_x + hourglass_size // 2, hourglass_y + hourglass_size // 2),
            (hourglass_x + hourglass_size, hourglass_y + hourglass_size),
            (hourglass_x, hourglass_y + hourglass_size),
            (hourglass_x + hourglass_size // 2, hourglass_y + hourglass_size // 2)
        ]
        pygame.draw.polygon(surface, self.primary_color, points, 2)
        
        # Sand level indicator
        if hasattr(sand_data, 'current') and hasattr(sand_data, 'maximum'):
            sand_text = f"{sand_data.current}/{sand_data.maximum}"
        else:
            sand_text = str(sand_data)
        
        font = pygame.font.Font(None, 24)
        text_surface = font.render(sand_text, True, (255, 248, 220))
        text_x = hourglass_x + hourglass_size + 10
        text_y = rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_effects_content(self, surface: pygame.Surface, effects_data: Any, rect: pygame.Rect) -> None:
        """Draw active effects with hieroglyphic-style icons."""
        if not effects_data:
            return
        
        # Scarab symbol for effects
        scarab_size = min(rect.height - 10, 20)
        scarab_x = rect.x + 10
        scarab_y = rect.centery - scarab_size // 2
        
        # Draw simplified scarab
        pygame.draw.ellipse(surface, self.primary_color, 
                          (scarab_x, scarab_y, scarab_size, scarab_size // 2))
        pygame.draw.ellipse(surface, self.accent_color,
                          (scarab_x, scarab_y, scarab_size, scarab_size // 2), 2)
        
        # Effects count or description
        font = pygame.font.Font(None, 20)
        if isinstance(effects_data, list):
            effects_text = f"{len(effects_data)} effects"
        else:
            effects_text = str(effects_data)
        
        text_surface = font.render(effects_text, True, (255, 248, 220))
        text_x = scarab_x + scarab_size + 10
        text_y = rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_intent_content(self, surface: pygame.Surface, intent_data: Any, rect: pygame.Rect) -> None:
        """Draw enemy intent with Eye of Horus symbol."""
        if not intent_data or self.chamber_type != "enemy":
            return
        
        # Eye symbol for intent
        eye_size = min(rect.height - 10, 20)
        eye_x = rect.x + 10
        eye_y = rect.centery - eye_size // 2
        
        # Draw Eye of Horus (simplified)
        eye_rect = pygame.Rect(eye_x, eye_y, eye_size, eye_size // 2)
        pygame.draw.ellipse(surface, self.primary_color, eye_rect)
        pygame.draw.ellipse(surface, self.accent_color, eye_rect, 2)
        
        # Intent text
        font = pygame.font.Font(None, 20)
        intent_text = str(intent_data)
        text_surface = font.render(intent_text, True, (255, 248, 220))
        text_x = eye_x + eye_size + 10
        text_y = rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    
    def _draw_chamber_borders(self, surface: pygame.Surface) -> None:
        """Draw decorative Egyptian borders around the chamber."""
        # Main border
        pygame.draw.rect(surface, self.accent_color, self.rect, 3)
        
        # Corner decorations (simplified Egyptian motifs)
        corner_size = 15
        corners = [
            (self.rect.x, self.rect.y),  # Top-left
            (self.rect.x + self.rect.width - corner_size, self.rect.y),  # Top-right
            (self.rect.x, self.rect.y + self.rect.height - corner_size),  # Bottom-left
            (self.rect.x + self.rect.width - corner_size, self.rect.y + self.rect.height - corner_size)  # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            # Draw simplified lotus motif
            pygame.draw.circle(surface, self.primary_color, 
                             (corner_x + corner_size // 2, corner_y + corner_size // 2), 
                             corner_size // 3, 2)