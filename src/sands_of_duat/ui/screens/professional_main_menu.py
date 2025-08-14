"""
Professional Main Menu - Inspired by AAA games like The Witcher 3, Hades, Cyberpunk 2077
Elegant, minimal, sophisticated - no excessive effects, perfect typography and spacing.
"""

import pygame
import math
import time
import logging
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER, FontSizes
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout, LayoutZone, ElementType
from ..responsive.scaling_manager import scaling_manager
from ..responsive.responsive_components import ResponsiveButton
from ...assets.smart_asset_loader import smart_asset_loader
from ...audio.simple_audio_manager import audio_manager
from ..components.hades_button import HadesButton, ButtonState

class MenuAction(Enum):
    """Main menu actions."""
    START_GAME = auto()
    DECK_BUILDER = auto()
    COLLECTION = auto()
    SETTINGS = auto()
    ANIMATION_FORGE = auto()
    QUIT = auto()

class ProfessionalButton:
    """Simple, elegant button inspired by AAA games."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, action: MenuAction, color: tuple, hieroglyph: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hieroglyph = hieroglyph
        self.is_hovered = False
        self.is_pressed = False
        
        # Smooth animation values
        self.hover_progress = 0.0
        self.press_progress = 0.0
        
        # Egyptian-themed colors with background
        self.theme_color = color
        self.base_color = self._create_egyptian_base_color(color)  # Egyptian-themed background
        self.hover_color = self._brighten_color(self.base_color, 0.3)  # Brighter on hover
        self.press_color = self._brighten_color(color, 0.2)  # Bright press effect
        self.border_color = self._darken_color(color, 0.4)  # Darker border
        self.text_color = Colors.PAPYRUS
        self.accent_color = color  # Theme color for accent
        
    def update(self, dt: float, mouse_pos: tuple, mouse_pressed: bool):
        """Update button state with smooth animations."""
        # Check hover state
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_pressed = self.is_hovered and mouse_pressed
        
        # Smooth hover animation
        target_hover = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target_hover - self.hover_progress) * dt * 8.0
        
        # Smooth press animation  
        target_press = 1.0 if self.is_pressed else 0.0
        self.press_progress += (target_press - self.press_progress) * dt * 12.0
    
    def handle_click(self, mouse_pos: tuple) -> bool:
        """Handle click event."""
        return self.rect.collidepoint(mouse_pos)
    
    def render(self, surface: pygame.Surface, font: pygame.font.Font):
        """Render elegant Egyptian-themed button."""
        # Calculate current colors based on animation progress
        bg_progress = max(self.hover_progress, self.press_progress * 0.3)
        
        # Interpolate background color for smooth Egyptian transitions
        current_bg = self._lerp_color(self.base_color, self.hover_color, bg_progress)
        
        # Add press effect with theme color blend
        if self.press_progress > 0.1:
            press_blend = self._lerp_color(current_bg, self.press_color, self.press_progress * 0.4)
            current_bg = press_blend
        
        # Draw subtle glow effect for Egyptian mystique
        if self.hover_progress > 0.2 or self.press_progress > 0.1:
            glow_intensity = max(self.hover_progress, self.press_progress) * 0.3
            glow_color = (self.theme_color[0], self.theme_color[1], self.theme_color[2], int(50 * glow_intensity))
            glow_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, 
                                  self.rect.width + 4, self.rect.height + 4)
            
            # Create glow surface
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, 
                           pygame.Rect(0, 0, glow_rect.width, glow_rect.height), 
                           border_radius=8)
            surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
        # Draw main button background with Egyptian styling
        pygame.draw.rect(surface, current_bg, self.rect, border_radius=6)
        
        # Draw gradient effect for depth
        gradient_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height // 3)
        gradient_color = self._brighten_color(current_bg, 0.15)
        pygame.draw.rect(surface, gradient_color, gradient_rect, border_radius=6)
        
        # Draw borders with Egyptian styling
        # Outer border with theme color
        border_intensity = 0.6 + 0.4 * self.hover_progress
        border_color = self._lerp_color(self.border_color, self.theme_color, border_intensity)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)
        
        # Inner subtle highlight
        inner_rect = pygame.Rect(self.rect.x + 1, self.rect.y + 1, 
                               self.rect.width - 2, self.rect.height - 2)
        inner_color = self._brighten_color(current_bg, 0.2)
        pygame.draw.rect(surface, inner_color, inner_rect, width=1, border_radius=5)
        
        # Draw accent line on hover (Egyptian style)
        if self.hover_progress > 0.1:
            accent_width = int(self.rect.width * self.hover_progress * 0.8)
            accent_x = self.rect.x + (self.rect.width - accent_width) // 2
            accent_rect = pygame.Rect(accent_x, self.rect.bottom - 3, accent_width, 2)
            pygame.draw.rect(surface, self.accent_color, accent_rect, border_radius=1)
        
        # Render hieroglyph on the left side if available
        if self.hieroglyph:
            try:
                hieroglyph_font = pygame.font.Font(None, int(font.get_height() * 1.2))
                hieroglyph_surface = hieroglyph_font.render(self.hieroglyph, True, self.accent_color)
                hieroglyph_rect = hieroglyph_surface.get_rect()
                hieroglyph_rect.centery = self.rect.centery
                hieroglyph_rect.x = self.rect.x + 15
                
                # Add hieroglyph shadow
                hieroglyph_shadow = hieroglyph_font.render(self.hieroglyph, True, (0, 0, 0, 120))
                hieroglyph_shadow_rect = pygame.Rect(hieroglyph_rect.x + 1, hieroglyph_rect.y + 1,
                                                   hieroglyph_rect.width, hieroglyph_rect.height)
                surface.blit(hieroglyph_shadow, hieroglyph_shadow_rect)
                surface.blit(hieroglyph_surface, hieroglyph_rect)
            except:
                # Fallback if hieroglyph can't be rendered
                pass
        
        # Render text with Egyptian styling (adjusted for hieroglyph space)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.centery = self.rect.centery
        text_rect.x = self.rect.x + (40 if self.hieroglyph else 20)  # Offset for hieroglyph
        
        # Subtle text offset when pressed
        if self.press_progress > 0.1:
            text_rect.y += int(self.press_progress * 1.5)
        
        # Add text shadow for better visibility
        shadow_offset = 1
        shadow_surface = font.render(self.text, True, (0, 0, 0, 100))
        shadow_rect = pygame.Rect(text_rect.x + shadow_offset, text_rect.y + shadow_offset,
                                text_rect.width, text_rect.height)
        surface.blit(shadow_surface, shadow_rect)
        
        surface.blit(text_surface, text_rect)
    
    def _lerp_color(self, color1: tuple, color2: tuple, t: float) -> tuple:
        """Linear interpolation between two colors."""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
    
    def _darken_color(self, color: tuple, factor: float) -> tuple:
        """Darken a color by a factor (0.0 = black, 1.0 = original)."""
        return tuple(int(c * factor) for c in color)
    
    def _brighten_color(self, color: tuple, factor: float) -> tuple:
        """Brighten a color by a factor."""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color)
    
    def _create_egyptian_base_color(self, theme_color: tuple) -> tuple:
        """Create Egyptian-themed background color based on theme."""
        # Create a darker, more muted version with Egyptian warmth
        r, g, b = theme_color
        
        # Add warm Egyptian undertones with better contrast
        if theme_color == Colors.GOLD:
            return (80, 60, 25)  # Rich golden brown
        elif theme_color == Colors.LAPIS_LAZULI:
            return (20, 35, 70)  # Rich lapis blue
        elif theme_color == Colors.PURPLE:
            return (55, 30, 80)  # Rich amethyst
        elif theme_color == Colors.GREEN:
            return (25, 55, 35)  # Rich emerald
        elif theme_color == Colors.GRAY:
            return (50, 50, 55)  # Rich slate gray
        elif theme_color == Colors.RED:
            return (70, 25, 25)  # Rich carnelian
        else:
            # Fallback: create darker version with warm tint
            return tuple(max(10, int(c * 0.2 + 15)) for c in theme_color)

class ProfessionalMainMenu:
    """
    Professional main menu with AAA game quality presentation.
    Clean, elegant, sophisticated - inspired by the best games in the industry.
    """
    
    def __init__(self, on_menu_action: Optional[Callable[[MenuAction], None]] = None):
        self.on_menu_action = on_menu_action
        self.layout = enhanced_ultrawide_layout
        self.logger = logging.getLogger("professional_main_menu")
        
        # Animation state - minimal and elegant
        self.time = 0.0
        self.fade_in_progress = 0.0
        
        # Load background
        self._create_background()
        
        # Create elegant typography
        self._create_typography()
        
        # Create professional buttons
        self._create_buttons()
        
        # Create subtle decorative elements
        self._create_decoration()
        
        # State
        self.selected_index = 0
        
    def _create_background(self):
        """Create elegant background using Hades-quality assets."""
        # Load Hades-quality background using smart asset loader
        bg_surface = smart_asset_loader.load_asset('menu_background')
        if bg_surface:
            # Scale to exact screen resolution with high quality
            self.background = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.logger.info("✨ Menu background loaded from Hades-quality assets")
        else:
            # Fallback to elegant gradient
            self.background = self._create_elegant_gradient()
            self.logger.warning("Using fallback gradient for menu background")
        
        # Create subtle overlay for UI readability over the 4K background
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Use RGB color and set alpha separately to avoid invalid color argument
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(60)
    
    def _create_elegant_gradient(self):
        """Create sophisticated Hades-level background gradient."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Hades-style dramatic gradient - deep purple to dark purple
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            
            # Deep purple gradient with Egyptian mystique
            r = int(Colors.BACKGROUND_PRIMARY[0] + (Colors.BACKGROUND_SECONDARY[0] - Colors.BACKGROUND_PRIMARY[0]) * progress)
            g = int(Colors.BACKGROUND_PRIMARY[1] + (Colors.BACKGROUND_SECONDARY[1] - Colors.BACKGROUND_PRIMARY[1]) * progress)  
            b = int(Colors.BACKGROUND_PRIMARY[2] + (Colors.BACKGROUND_SECONDARY[2] - Colors.BACKGROUND_PRIMARY[2]) * progress)
            
            # Add subtle warmth and mystique
            r = min(255, int(r + 5 * math.sin(progress * 3.14159)))  # Subtle warmth variation
            g = min(255, int(g + 3 * math.sin(progress * 3.14159)))
            b = min(255, int(b + 8 * math.sin(progress * 3.14159)))  # More blue mystique
            
            color = (r, g, b)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        return surface
    
    def _create_typography(self):
        """SPRINT 1: Create enhanced typography system with scaling manager."""
        # SPRINT 1: Use scaling manager for enhanced font hierarchy
        self.title_font = scaling_manager.get_font('title_huge')
        self.subtitle_font = scaling_manager.get_font('title_medium')
        self.button_font = scaling_manager.get_font('button')
        
        # Create title text with enhanced hierarchy
        self.title_text = self.title_font.render("SANDS OF DUAT", True, Colors.GOLD)
        self.subtitle_text = self.subtitle_font.render("Egyptian Underworld", True, Colors.PAPYRUS)
        
        # SPRINT 1: Enhanced positioning for ultrawide displays
        title_y = int(SCREEN_HEIGHT * 0.18)  # Slightly higher for better composition
        spacing = scaling_manager.scale_value(25, 'spacing')  # Responsive spacing
        
        self.title_pos = (SCREEN_CENTER[0] - self.title_text.get_width() // 2, title_y)
        self.subtitle_pos = (SCREEN_CENTER[0] - self.subtitle_text.get_width() // 2, 
                           title_y + self.title_text.get_height() + spacing)
    
    def _create_buttons(self):
        """SPRINT 1: Create enhanced button layout with scaling system."""
        button_configs = [
            ("Begin Journey", MenuAction.START_GAME, Colors.GOLD, "𓇳"),          # Solar disk 
            ("Construct Deck", MenuAction.DECK_BUILDER, Colors.LAPIS_LAZULI, "𓊪"), # Building/scroll
            ("Hall of Gods", MenuAction.COLLECTION, Colors.PURPLE, "𓊽"),         # Temple/shrine
            ("Animation Forge", MenuAction.ANIMATION_FORGE, Colors.GREEN, "𓈖"),   # Creative power
            ("Sacred Settings", MenuAction.SETTINGS, Colors.GRAY, "𓊖"),          # Scales/balance
            ("Return to Mortality", MenuAction.QUIT, Colors.RED, "𓅓")            # Bird/departure
        ]
        
        # SPRINT 1: Use scaling manager for responsive button layout
        button_positions = scaling_manager.get_button_layout(
            button_count=len(button_configs),
            button_type='large',
            zone='center_content'
        )
        
        # SPRINT 1: Create enhanced buttons with responsive scaling
        self.buttons = []
        button_width, button_height = scaling_manager.get_component_size('button_large')
        
        for i, (text, action, color, hieroglyph) in enumerate(button_configs):
            x, y = button_positions[i]
            
            # Create callback function for this specific action
            def create_callback(menu_action):
                return lambda: self._handle_menu_action(menu_action)
            
            button = HadesButton(
                x, y, button_width, button_height,
                text=text,
                theme_color=color,
                hieroglyph=hieroglyph,
                on_click=create_callback(action)
            )
            self.buttons.append(button)
            
    def _handle_menu_action(self, action: MenuAction):
        """Handle menu action with enhanced feedback."""
        if self.on_menu_action:
            self.on_menu_action(action)
    
    def _create_decoration(self):
        """Create subtle decorative elements."""
        # Simple corner decorations (like Hades style)
        self.corner_size = 60
        self.corner_thickness = 2
        self.decoration_alpha = 0.6
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: tuple):
        """Update menu with smooth animations."""
        self.time += dt
        
        # Smooth fade in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
        
        # Handle mouse state for Hades buttons
        mouse_button_pressed = False
        if isinstance(mouse_pressed, (list, tuple)) and len(mouse_pressed) > 0:
            mouse_button_pressed = mouse_pressed[0]
        else:
            mouse_button_pressed = bool(mouse_pressed) if mouse_pressed else False
        
        # Update Hades buttons with smooth animations
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_button_pressed)
        
        # Handle events (keyboard navigation)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    # Trigger selected button
                    if 0 <= self.selected_index < len(self.buttons):
                        button = self.buttons[self.selected_index]
                        if button.on_click:
                            button.on_click()
    
    def render(self, surface: pygame.Surface):
        """Render professional menu."""
        # Background
        surface.blit(self.background, (0, 0))
        surface.blit(self.overlay, (0, 0))
        
        # Apply fade in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
        
        # Render corner decorations
        self._render_decorations(surface)
        
        # Title system
        surface.blit(self.title_text, self.title_pos)
        surface.blit(self.subtitle_text, self.subtitle_pos)
        
        # Buttons
        for button in self.buttons:
            button.render(surface, self.button_font)
        
        # Version info (bottom right)
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render("v1.0", True, (100, 100, 100))
        version_pos = (SCREEN_WIDTH - version_text.get_width() - 20, 
                      SCREEN_HEIGHT - version_text.get_height() - 20)
        surface.blit(version_text, version_pos)
    
    def _render_decorations(self, surface: pygame.Surface):
        """Render subtle corner decorations."""
        alpha = int(255 * self.decoration_alpha * self.fade_in_progress)
        # This line was unused - removed to fix color argument error
        
        # Top left corner
        pygame.draw.line(surface, Colors.GOLD, (20, 20), (20 + self.corner_size, 20), self.corner_thickness)
        pygame.draw.line(surface, Colors.GOLD, (20, 20), (20, 20 + self.corner_size), self.corner_thickness)
        
        # Top right corner
        pygame.draw.line(surface, Colors.GOLD, (SCREEN_WIDTH - 20 - self.corner_size, 20), 
                        (SCREEN_WIDTH - 20, 20), self.corner_thickness)
        pygame.draw.line(surface, Colors.GOLD, (SCREEN_WIDTH - 20, 20), 
                        (SCREEN_WIDTH - 20, 20 + self.corner_size), self.corner_thickness)
        
        # Bottom left corner
        pygame.draw.line(surface, Colors.GOLD, (20, SCREEN_HEIGHT - 20), 
                        (20 + self.corner_size, SCREEN_HEIGHT - 20), self.corner_thickness)
        pygame.draw.line(surface, Colors.GOLD, (20, SCREEN_HEIGHT - 20 - self.corner_size), 
                        (20, SCREEN_HEIGHT - 20), self.corner_thickness)
        
        # Bottom right corner
        pygame.draw.line(surface, Colors.GOLD, (SCREEN_WIDTH - 20 - self.corner_size, SCREEN_HEIGHT - 20), 
                        (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), self.corner_thickness)
        pygame.draw.line(surface, Colors.GOLD, (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20 - self.corner_size), 
                        (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), self.corner_thickness)
    
    def reset_animations(self):
        """Reset animations."""
        self.time = 0.0
        self.fade_in_progress = 0.0