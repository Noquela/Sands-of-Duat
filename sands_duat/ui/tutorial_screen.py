"""
Tutorial Screen

Egyptian-themed tutorial system for Sands of Duat.
Implements multi-agent designed educational experience with authentic cultural representation.
"""

import pygame
import math
from typing import Dict, Any, Optional, List, Callable
from .base import UIScreen, UIComponent
from .theme import get_theme
from .animation_system import EasingType
from audio.sound_effects import play_button_sound


class HieroglyphicButton(UIComponent):
    """
    Interactive hieroglyphic button with authentic Egyptian styling.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, hieroglyph: str, tooltip: str, callback: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.hieroglyph = hieroglyph
        self.tooltip = tooltip
        self.callback = callback
        self.font = pygame.font.Font(None, 48)
        self.tooltip_font = pygame.font.Font(None, 24)
        
        # Visual states
        self.scale = 1.0
        self.target_scale = 1.0
        self.glow_alpha = 0
        self.target_glow = 0
        self.show_tooltip = False
        
        # Egyptian colors
        self.base_color = (139, 117, 93)  # Sandstone
        self.hover_color = (180, 150, 120)  # Light sandstone
        self.glyph_color = (255, 215, 0)  # Gold
        self.tooltip_bg = (60, 45, 30, 200)  # Dark brown with alpha
    
    def update(self, delta_time: float) -> None:
        """Update button animations."""
        # Scale animation
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * delta_time * 8
        
        # Glow animation
        if abs(self.glow_alpha - self.target_glow) > 1:
            self.glow_alpha += (self.target_glow - self.glow_alpha) * delta_time * 10
        
        # Update targets based on hover state
        if self.hovered:
            self.target_scale = 1.1
            self.target_glow = 80
            self.show_tooltip = True
        else:
            self.target_scale = 1.0
            self.target_glow = 0
            self.show_tooltip = False
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the hieroglyphic button."""
        if not self.visible:
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
        
        # Draw glow effect
        if self.glow_alpha > 0:
            glow_rect = scaled_rect.inflate(6, 6)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            glow_color = (*self.glyph_color, int(self.glow_alpha))
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect())
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Draw button background (circular)
        button_color = self.hover_color if self.hovered else self.base_color
        pygame.draw.ellipse(surface, button_color, scaled_rect)
        pygame.draw.ellipse(surface, self.glyph_color, scaled_rect, 3)
        
        # Draw hieroglyphic symbol
        glyph_surface = self.font.render(self.hieroglyph, True, self.glyph_color)
        glyph_rect = glyph_surface.get_rect(center=scaled_rect.center)
        surface.blit(glyph_surface, glyph_rect)
        
        # Draw tooltip
        if self.show_tooltip and self.tooltip:
            tooltip_surface = self.tooltip_font.render(self.tooltip, True, (255, 255, 255))
            tooltip_width = tooltip_surface.get_width() + 20
            tooltip_height = tooltip_surface.get_height() + 10
            
            tooltip_rect = pygame.Rect(
                self.rect.centerx - tooltip_width // 2,
                self.rect.bottom + 10,
                tooltip_width,
                tooltip_height
            )
            
            # Tooltip background
            tooltip_bg_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            tooltip_bg_surface.fill(self.tooltip_bg)
            surface.blit(tooltip_bg_surface, tooltip_rect.topleft)
            
            # Tooltip text
            text_rect = tooltip_surface.get_rect(center=tooltip_rect.center)
            surface.blit(tooltip_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button interaction."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                play_button_sound("click")
                if self.callback:
                    self.callback()
                self._trigger_event("hieroglyph_clicked", {"hieroglyph": self.hieroglyph})
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_over = self.rect.collidepoint(event.pos)
            if mouse_over and not self.hovered:
                self.hovered = True
                play_button_sound("hover")
            elif not mouse_over and self.hovered:
                self.hovered = False
        
        return False


class CanopicTutorialChamber(UIComponent):
    """
    Tutorial chamber organized around canopic jar themes.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, chamber_type: str, content: Dict[str, Any]):
        super().__init__(x, y, width, height)
        self.chamber_type = chamber_type  # "cards", "combat", "mythology", "strategy"
        self.content = content
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        
        # Chamber visual properties
        self.scroll_offset = 0
        self.target_scroll = 0
        self.chamber_alpha = 255
        
        # Egyptian colors based on canopic jar gods
        self.chamber_colors = {
            "cards": (180, 150, 120),      # Imsety (human-headed) - warm brown
            "combat": (160, 120, 90),      # Hapy (baboon-headed) - darker brown  
            "mythology": (200, 170, 140),  # Duamutef (jackal-headed) - light brown
            "strategy": (140, 110, 80)     # Qebehsenuef (falcon-headed) - deep brown
        }
        
        # Chamber symbols (simplified representations)
        self.chamber_symbols = {
            "cards": "☰",      # Deck representation
            "combat": "⚔",     # Combat representation
            "mythology": "◉",   # Eye of Ra
            "strategy": "△"     # Pyramid
        }
    
    def update(self, delta_time: float) -> None:
        """Update chamber animations."""
        # Smooth scrolling
        if abs(self.scroll_offset - self.target_scroll) > 1:
            self.scroll_offset += (self.target_scroll - self.scroll_offset) * delta_time * 6
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the tutorial chamber."""
        if not self.visible:
            return
        
        # Chamber background with Egyptian styling
        chamber_color = self.chamber_colors.get(self.chamber_type, (150, 120, 90))
        
        # Main chamber rectangle
        pygame.draw.rect(surface, chamber_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 215, 0), self.rect, 3, border_radius=10)
        
        # Chamber symbol and title
        symbol = self.chamber_symbols.get(self.chamber_type, "◉")
        symbol_surface = self.title_font.render(symbol, True, (255, 215, 0))
        symbol_rect = symbol_surface.get_rect()
        symbol_rect.centerx = self.rect.centerx
        symbol_rect.top = self.rect.top + 20
        surface.blit(symbol_surface, symbol_rect)
        
        # Chamber title
        title = self.content.get("title", self.chamber_type.title())
        title_surface = self.font.render(title, True, (255, 248, 220))
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.top = symbol_rect.bottom + 10
        surface.blit(title_surface, title_rect)
        
        # Chamber content area
        content_rect = pygame.Rect(
            self.rect.left + 20,
            title_rect.bottom + 20,
            self.rect.width - 40,
            self.rect.height - (title_rect.bottom + 40 - self.rect.top)
        )
        
        # Render content with scrolling
        self._render_chamber_content(surface, content_rect)
    
    def _render_chamber_content(self, surface: pygame.Surface, content_rect: pygame.Rect) -> None:
        """Render scrollable chamber content."""
        # Create content surface for scrolling
        content_surface = pygame.Surface((content_rect.width, content_rect.height + 200), pygame.SRCALPHA)
        
        y_offset = 0
        content_data = self.content.get("sections", [])
        
        for section in content_data:
            section_title = section.get("title", "")
            section_text = section.get("text", "")
            
            if section_title:
                title_surf = self.font.render(section_title, True, (255, 215, 0))
                content_surface.blit(title_surf, (10, y_offset))
                y_offset += title_surf.get_height() + 10
            
            if section_text:
                # Wrap text for chamber width
                wrapped_lines = self._wrap_text(section_text, content_rect.width - 20)
                for line in wrapped_lines:
                    line_surf = self.font.render(line, True, (255, 248, 220))
                    content_surface.blit(line_surf, (10, y_offset))
                    y_offset += line_surf.get_height() + 5
                
                y_offset += 15  # Section spacing
        
        # Blit scrolled content
        source_rect = pygame.Rect(0, int(self.scroll_offset), content_rect.width, content_rect.height)
        surface.blit(content_surface, content_rect.topleft, source_rect)
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within chamber width."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines


class NileRiverProgress(UIComponent):
    """
    Visual progress indicator themed as sailing down the Nile River.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, total_steps: int):
        super().__init__(x, y, width, height)
        self.total_steps = total_steps
        self.current_step = 0
        self.boat_position = 0.0
        self.target_position = 0.0
        
        # Animation properties
        self.wave_time = 0.0
        self.papyrus_sway = 0.0
    
    def update(self, delta_time: float) -> None:
        """Update river animation."""
        self.wave_time += delta_time
        self.papyrus_sway += delta_time * 0.5
        
        # Smooth boat movement
        if abs(self.boat_position - self.target_position) > 0.01:
            self.boat_position += (self.target_position - self.boat_position) * delta_time * 3
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Nile River progress indicator."""
        if not self.visible:
            return
        
        # River background
        river_color = (64, 128, 192)  # Nile blue
        bank_color = (139, 117, 93)   # Sandstone
        
        # Draw river banks
        pygame.draw.rect(surface, bank_color, (self.rect.left, self.rect.top, self.rect.width, 10))
        pygame.draw.rect(surface, bank_color, (self.rect.left, self.rect.bottom - 10, self.rect.width, 10))
        
        # Draw river with waves
        river_rect = pygame.Rect(self.rect.left, self.rect.top + 10, self.rect.width, self.rect.height - 20)
        pygame.draw.rect(surface, river_color, river_rect)
        
        # Draw wave pattern
        for x in range(0, self.rect.width, 20):
            wave_y = river_rect.centery + math.sin(self.wave_time * 2 + x * 0.1) * 3
            pygame.draw.circle(surface, (80, 150, 220), (self.rect.left + x, int(wave_y)), 3)
        
        # Draw progress markers (temples along the river)
        marker_spacing = self.rect.width // (self.total_steps + 1)
        for i in range(self.total_steps):
            marker_x = self.rect.left + (i + 1) * marker_spacing
            marker_color = (255, 215, 0) if i < self.current_step else (100, 100, 100)
            
            # Temple marker
            temple_rect = pygame.Rect(marker_x - 8, self.rect.top - 5, 16, 20)
            pygame.draw.rect(surface, marker_color, temple_rect)
            
            # Temple peak
            peak_points = [
                (marker_x, self.rect.top - 5),
                (marker_x - 8, self.rect.top + 5),
                (marker_x + 8, self.rect.top + 5)
            ]
            pygame.draw.polygon(surface, marker_color, peak_points)
        
        # Draw boat at current position
        boat_x = self.rect.left + self.boat_position * self.rect.width
        boat_y = river_rect.centery + math.sin(self.wave_time * 3) * 2
        
        # Simple boat shape
        boat_points = [
            (boat_x - 15, boat_y),
            (boat_x + 15, boat_y),
            (boat_x + 10, boat_y + 8),
            (boat_x - 10, boat_y + 8)
        ]
        pygame.draw.polygon(surface, (101, 67, 33), boat_points)  # Brown boat
        
        # Sail
        sail_sway = math.sin(self.papyrus_sway) * 2
        sail_points = [
            (boat_x - 5 + sail_sway, boat_y - 15),
            (boat_x + 5 + sail_sway, boat_y - 15),
            (boat_x + 3 + sail_sway, boat_y),
            (boat_x - 3 + sail_sway, boat_y)
        ]
        pygame.draw.polygon(surface, (255, 248, 220), sail_points)  # Papyrus colored sail
    
    def set_progress(self, step: int) -> None:
        """Update progress to specific step."""
        self.current_step = min(step, self.total_steps)
        self.target_position = self.current_step / self.total_steps


class TutorialScreen(UIScreen):
    """
    Egyptian-themed tutorial screen implementing multi-agent design recommendations.
    """
    
    def __init__(self):
        super().__init__("tutorial")
        
        # Tutorial state
        self.current_chamber = 0
        self.tutorial_chambers = []
        self.progress_indicator: Optional[NileRiverProgress] = None
        self.navigation_buttons: List[HieroglyphicButton] = []
        
        # Game flow context tracking
        self.is_new_game_flow = False  # Track if tutorial is part of new game journey
        self.return_screen = "progression"  # Default return destination
        
        # Tutorial content structure
        self.chamber_content = {
            "cards": {
                "title": "Sacred Scrolls & Artifacts",
                "sections": [
                    {
                        "title": "The Power of Egyptian Cards",
                        "text": "In ancient Egypt, priests wielded mystical artifacts and sacred scrolls. Your deck represents these powerful items, each card containing the essence of Egyptian magic and wisdom."
                    },
                    {
                        "title": "Building Your Collection",
                        "text": "Begin with basic canopic jars and papyrus scrolls. As you progress, unlock powerful artifacts blessed by the gods themselves. Each god favors different types of magic."
                    },
                    {
                        "title": "Card Synergies",
                        "text": "Combine artifacts of the same deity for powerful bonuses. Ra's solar cards gain strength during day cycles, while Khnum's creation cards work best with earth elements."
                    }
                ]
            },
            "combat": {
                "title": "HourGlass Initiative Combat",
                "sections": [
                    {
                        "title": "The Sacred Hourglass",
                        "text": "Time flows like sand through the cosmic hourglass. Each turn represents a grain of sand falling, determining when you and your enemies may act in the eternal dance of combat."
                    },
                    {
                        "title": "Initiative and Timing",
                        "text": "Watch the golden sands flow in the obelisk turn indicator. Faster cards act sooner, while powerful spells require patience as the sands accumulate their mystical energy."
                    },
                    {
                        "title": "Strategic Positioning",
                        "text": "Position your artifacts wisely on the battle grid. Distance affects spell power, and some ancient enchantments require specific geometric alignments to achieve their full potential."
                    }
                ]
            },
            "mythology": {
                "title": "Egyptian Pantheon & Lore",
                "sections": [
                    {
                        "title": "The Great Ennead",
                        "text": "Nine great gods rule over different aspects of magic and creation. Ra commands the sun and light magic, Anubis governs death and transformation, Thoth controls wisdom and time manipulation."
                    },
                    {
                        "title": "Divine Favor",
                        "text": "Each god grants different bonuses to their favored artifact types. Earning divine favor through proper worship and strategic play unlocks powerful blessing effects."
                    },
                    {
                        "title": "Mythological Encounters",
                        "text": "Face legendary creatures from Egyptian mythology. Battle Apep the serpent of chaos, negotiate with Sphinx riddlers, and earn the respect of Anubis's jackal guardians."
                    }
                ]
            },
            "strategy": {
                "title": "Mastering Egyptian Magic",
                "sections": [
                    {
                        "title": "Resource Management",
                        "text": "Manage your ka (spiritual energy) wisely. Powerful spells drain more ka, but meditation cards and temple visits can restore your spiritual reserves for the battles ahead."
                    },
                    {
                        "title": "Deck Archetypes",
                        "text": "Focus your deck around specific strategies: Solar Supremacy with Ra's blessing, Death Magic with Anubis artifacts, or Balanced Harmony drawing from multiple pantheons."
                    },
                    {
                        "title": "Advanced Tactics",
                        "text": "Master combo chains by understanding artifact interactions. Learn to read enemy patterns and adapt your strategy. Some battles require specific approaches to achieve victory."
                    }
                ]
            }
        }
        
        # Background animation
        self.background_time = 0.0
        self.hieroglyph_particles = []
    
    def on_enter(self) -> None:
        """Initialize tutorial screen."""
        self.logger.info("Entering Egyptian tutorial system")
        self._setup_tutorial_components()
        self._generate_background_elements()
    
    def set_game_flow_context(self, is_new_game: bool = False, return_screen: str = "progression") -> None:
        """Set context for how tutorial was entered and where it should return."""
        self.is_new_game_flow = is_new_game
        self.return_screen = return_screen
        self.logger.info(f"Tutorial context set: new_game={is_new_game}, return_to={return_screen}")
    
    def on_exit(self) -> None:
        """Clean up tutorial screen."""
        self.logger.info("Exiting tutorial system")
        self.clear_components()
    
    def update(self, delta_time: float) -> None:
        """Update tutorial animations and components."""
        super().update(delta_time)
        self.background_time += delta_time
        self._update_background_animation(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the tutorial screen."""
        self._draw_tutorial_background(surface)
        
        # Draw contextual header message
        if self.is_new_game_flow:
            self._draw_context_message(surface, "Welcome, New Pharaoh! Learn the ancient ways before your journey begins.")
        
        super().render(surface)
    
    def _setup_tutorial_components(self) -> None:
        """Set up tutorial UI components using multi-agent design recommendations."""
        theme = get_theme()
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Nile River progress indicator (top of screen)
        progress_width = min(screen_width - 200, 1000)
        progress_height = 60
        progress_x = (screen_width - progress_width) // 2
        progress_y = 50
        
        self.progress_indicator = NileRiverProgress(
            progress_x, progress_y, progress_width, progress_height, 
            len(self.chamber_content)
        )
        self.add_component(self.progress_indicator)
        
        # Tutorial chambers (main content area)
        chamber_width = min(screen_width - 300, 800)
        chamber_height = screen_height - 300
        chamber_x = (screen_width - chamber_width) // 2
        chamber_y = progress_y + progress_height + 50
        
        for i, (chamber_type, content) in enumerate(self.chamber_content.items()):
            chamber = CanopicTutorialChamber(
                chamber_x, chamber_y, chamber_width, chamber_height,
                chamber_type, content
            )
            chamber.visible = (i == self.current_chamber)
            self.tutorial_chambers.append(chamber)
            self.add_component(chamber)
        
        # Navigation hieroglyphic buttons (bottom of screen)
        button_size = 60
        button_spacing = 80
        total_width = len(self.chamber_content) * button_spacing
        start_x = (screen_width - total_width) // 2
        button_y = screen_height - 120
        
        hieroglyphs = ["☰", "⚔", "◉", "△"]  # Cards, Combat, Mythology, Strategy
        tooltips = ["Sacred Scrolls", "Combat System", "Egyptian Lore", "Strategy Guide"]
        
        for i, (hieroglyph, tooltip) in enumerate(zip(hieroglyphs, tooltips)):
            button = HieroglyphicButton(
                start_x + i * button_spacing, button_y,
                button_size, button_size,
                hieroglyph, tooltip,
                lambda idx=i: self._switch_to_chamber(idx)
            )
            self.navigation_buttons.append(button)
            self.add_component(button)
        
        # Exit button (top right corner) with context-aware tooltip
        exit_tooltip = "Continue to Game" if self.is_new_game_flow else "Return to Menu"
        exit_button = HieroglyphicButton(
            screen_width - 100, 50, 50, 50,
            "✕", exit_tooltip,
            self._exit_tutorial
        )
        self.add_component(exit_button)
    
    def _switch_to_chamber(self, chamber_index: int) -> None:
        """Switch to specific tutorial chamber."""
        if 0 <= chamber_index < len(self.tutorial_chambers):
            # Hide current chamber
            if 0 <= self.current_chamber < len(self.tutorial_chambers):
                self.tutorial_chambers[self.current_chamber].visible = False
            
            # Show new chamber
            self.current_chamber = chamber_index
            self.tutorial_chambers[self.current_chamber].visible = True
            
            # Update progress
            if self.progress_indicator:
                self.progress_indicator.set_progress(chamber_index + 1)
            
            play_button_sound("click")
            self.logger.info(f"Switched to tutorial chamber: {chamber_index}")
    
    def _exit_tutorial(self) -> None:
        """Exit tutorial and continue to appropriate screen based on context."""
        if self.is_new_game_flow:
            self.logger.info("Exiting tutorial system - continuing new game to progression")
            transition = "slide_left"
        else:
            self.logger.info(f"Exiting tutorial system - returning to {self.return_screen}")
            transition = "slide_right" if self.return_screen == "menu" else "slide_left"
        
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition(self.return_screen, transition)
        else:
            self._trigger_event("switch_screen", {"screen": self.return_screen})
    
    def _generate_background_elements(self) -> None:
        """Generate animated hieroglyphic particles."""
        import random
        
        hieroglyphs = ["𓀀", "𓂀", "𓃀", "𓄀", "𓅀", "𓆀", "𓇀", "𓈀"]
        
        for _ in range(15):
            particle = {
                'hieroglyph': random.choice(hieroglyphs),
                'x': random.randint(0, 3440),
                'y': random.randint(0, 1440),
                'speed': random.uniform(10, 30),
                'alpha': random.randint(30, 80),
                'size': random.randint(20, 40)
            }
            self.hieroglyph_particles.append(particle)
    
    def _update_background_animation(self, delta_time: float) -> None:
        """Update background hieroglyphic particles."""
        for particle in self.hieroglyph_particles:
            particle['x'] -= particle['speed'] * delta_time
            if particle['x'] < -50:
                particle['x'] = 3500
                particle['y'] = __import__('random').randint(0, 1440)
    
    def _draw_tutorial_background(self, surface: pygame.Surface) -> None:
        """Draw animated Egyptian background."""
        # Gradient background (temple interior)
        for y in range(surface.get_height()):
            ratio = y / surface.get_height()
            r = int(25 + ratio * 35)  # 25 to 60
            g = int(20 + ratio * 25)  # 20 to 45
            b = int(10 + ratio * 20)  # 10 to 30
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
        
        # Floating hieroglyphic particles
        for particle in self.hieroglyph_particles:
            alpha_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            color = (139, 117, 93, particle['alpha'])  # Sandstone with alpha
            
            # Simplified hieroglyph representation (using basic shapes)
            pygame.draw.rect(alpha_surface, color, (5, 5, particle['size']-10, particle['size']-10))
            surface.blit(alpha_surface, (particle['x'], particle['y']))
        
        # Temple column shadows (left and right edges)
        column_width = 50
        column_color = (30, 25, 20, 100)
        
        left_column = pygame.Surface((column_width, surface.get_height()), pygame.SRCALPHA)
        left_column.fill(column_color)
        surface.blit(left_column, (0, 0))
        
        right_column = pygame.Surface((column_width, surface.get_height()), pygame.SRCALPHA)
        right_column.fill(column_color)
        surface.blit(right_column, (surface.get_width() - column_width, 0))
    
    def _draw_context_message(self, surface: pygame.Surface, message: str) -> None:
        """Draw contextual message for new game flow."""
        font = pygame.font.Font(None, 28)
        text_surface = font.render(message, True, (255, 215, 0))  # Gold text
        
        # Semi-transparent background
        bg_width = text_surface.get_width() + 40
        bg_height = text_surface.get_height() + 20
        bg_x = (surface.get_width() - bg_width) // 2
        bg_y = 15
        
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((60, 45, 30, 180))  # Dark brown with alpha
        surface.blit(bg_surface, (bg_x, bg_y))
        
        # Draw border
        pygame.draw.rect(surface, (255, 215, 0), (bg_x, bg_y, bg_width, bg_height), 2)
        
        # Draw text
        text_rect = text_surface.get_rect()
        text_rect.centerx = surface.get_width() // 2
        text_rect.centery = bg_y + bg_height // 2
        surface.blit(text_surface, text_rect)