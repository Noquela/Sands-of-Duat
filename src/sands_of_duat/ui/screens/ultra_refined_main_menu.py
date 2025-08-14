"""
Ultra Refined Main Menu - Professional AAA Layout
Advanced visual hierarchy with Egyptian theming and perfect ultrawide utilization.
"""

import pygame
import math
import time
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout, LayoutZone, ElementType
from ...assets.smart_asset_loader import smart_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton
from ..effects.professional_transitions import professional_transitions, TransitionType
from ..effects.advanced_visual_effects import advanced_visual_effects

class MenuAction(Enum):
    """Main menu actions."""
    START_GAME = auto()
    DECK_BUILDER = auto()
    COLLECTION = auto()
    SETTINGS = auto()
    ANIMATION_FORGE = auto()
    QUIT = auto()

class UltraRefinedMainMenu:
    """
    Ultra refined main menu with AAA visual hierarchy and perfect ultrawide layout.
    Professional presentation with Egyptian theming and smooth interactions.
    """
    
    def __init__(self, on_menu_action: Optional[Callable[[MenuAction], None]] = None):
        self.on_menu_action = on_menu_action
        self.layout = enhanced_ultrawide_layout
        
        # Visual state
        self.animation_time = 0.0
        self.particle_time = 0.0
        self.glow_pulse = 0.0
        self.screen_flash_alpha = 0.0
        self.screen_flash_time = 0.0
        
        # Load and prepare visual elements
        self._create_background_system()
        self._create_title_system()
        self._create_navigation_system()
        self._create_information_panels()
        self._create_decorative_elements()
        
        # Interactive elements
        self.hover_button = None
        self.selected_index = 0
        
    def _create_background_system(self):
        """Create sophisticated background with multiple layers."""
        # Load main background
        bg_surface = smart_asset_loader.load_asset('menu_background')
        if bg_surface:
            self.background = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.background = self._create_advanced_gradient()
        
        # Create overlay layers for depth
        self.overlay_alpha = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Subtle vignette effect
        self._create_vignette_overlay()
        
        # Animated particle background
        self.background_particles = []
        self._initialize_background_particles()
    
    def _create_advanced_gradient(self):
        """Create sophisticated Egyptian gradient background."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Multi-layer gradient for depth
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            
            # Layer 1: Night sky to golden horizon
            if progress < 0.6:
                # Deep night blue to lapis lazuli
                t = progress / 0.6
                r = int(Colors.DARK_BLUE[0] + (Colors.LAPIS_LAZULI[0] - Colors.DARK_BLUE[0]) * t)
                g = int(Colors.DARK_BLUE[1] + (Colors.LAPIS_LAZULI[1] - Colors.DARK_BLUE[1]) * t)
                b = int(Colors.DARK_BLUE[2] + (Colors.LAPIS_LAZULI[2] - Colors.DARK_BLUE[2]) * t)
            else:
                # Lapis to gold horizon
                t = (progress - 0.6) / 0.4
                r = int(Colors.LAPIS_LAZULI[0] + (Colors.GOLD_DARK[0] - Colors.LAPIS_LAZULI[0]) * t)
                g = int(Colors.LAPIS_LAZULI[1] + (Colors.GOLD_DARK[1] - Colors.LAPIS_LAZULI[1]) * t)
                b = int(Colors.LAPIS_LAZULI[2] + (Colors.GOLD_DARK[2] - Colors.LAPIS_LAZULI[2]) * t)
            
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        return surface
    
    def _create_vignette_overlay(self):
        """Create subtle vignette for focus."""
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        center_x, center_y = SCREEN_CENTER
        max_radius = max(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for radius in range(0, max_radius // 2, 20):
            alpha = min(60, radius // 15)  # Subtle vignette
            color = (0, 0, 0, alpha)
            
            # Draw circles from outside in
            for i in range(4):  # Multiple circles for smooth gradient
                pygame.draw.circle(vignette, color, (center_x, center_y), max_radius // 2 - radius + i * 5)
        
        self.vignette = vignette
    
    def _initialize_background_particles(self):
        """Initialize floating background particles for ambiance."""
        particle_count = 30 if self.layout.is_ultrawide else 20
        
        for i in range(particle_count):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 1.5),
                'size': random.uniform(2, 6),
                'alpha': random.uniform(30, 80),
                'color': random.choice([Colors.GOLD, Colors.PAPYRUS, Colors.LAPIS_LAZULI, Colors.DESERT_SAND]),
                'pulse_speed': random.uniform(0.5, 2.0),
                'angle': random.uniform(0, 360),
                'drift_x': random.uniform(-0.3, 0.3)
            }
            self.background_particles.append(particle)
    
    def _create_title_system(self):
        """Create professional title system with Egyptian hierarchy."""
        # Title fonts with perfect scaling
        title_size = self.layout.get_font_size('huge_title')
        subtitle_size = self.layout.get_font_size('title') 
        tagline_size = self.layout.get_font_size('subtitle')
        
        # Create title fonts (TODO: Replace with Egyptian fonts)
        self.title_font = pygame.font.Font(None, title_size)
        self.subtitle_font = pygame.font.Font(None, subtitle_size)  
        self.tagline_font = pygame.font.Font(None, tagline_size)
        
        # Title text with golden glow
        self.main_title = self.title_font.render("SANDS OF DUAT", True, Colors.GOLD)
        self.subtitle = self.subtitle_font.render("Egyptian Underworld Card Game", True, Colors.PAPYRUS)
        self.tagline = self.tagline_font.render("Journey Through the Realm of the Dead", True, Colors.DESERT_SAND)
        
        # Position in top zone with perfect spacing
        top_zone = self.layout.get_zone_rect(LayoutZone.TOP_BAR)
        spacing = self.layout.get_spacing('medium')
        
        # Center horizontally, stack vertically
        total_height = (self.main_title.get_height() + spacing +
                       self.subtitle.get_height() + spacing +
                       self.tagline.get_height())
        
        start_y = top_zone.y + (top_zone.height - total_height) // 2
        
        self.title_pos = (top_zone.centerx - self.main_title.get_width() // 2, start_y)
        self.subtitle_pos = (top_zone.centerx - self.subtitle.get_width() // 2, 
                           start_y + self.main_title.get_height() + spacing)
        self.tagline_pos = (top_zone.centerx - self.tagline.get_width() // 2,
                          start_y + self.main_title.get_height() + spacing +
                          self.subtitle.get_height() + spacing)
        
        # Title glow effect surfaces
        self._create_title_glow_effects()
    
    def _create_title_glow_effects(self):
        """Create glow effects for titles."""
        # Gold glow for main title
        glow_surface = pygame.Surface(
            (self.main_title.get_width() + 40, self.main_title.get_height() + 40),
            pygame.SRCALPHA
        )
        
        # Multiple glow layers
        for i in range(5):
            alpha = 30 - i * 5
            glow_color = (*Colors.GOLD, alpha)
            expanded_rect = pygame.Rect(
                20 - i * 2, 20 - i * 2,
                self.main_title.get_width() + i * 4,
                self.main_title.get_height() + i * 4
            )
            pygame.draw.rect(glow_surface, glow_color, expanded_rect, border_radius=5)
        
        self.title_glow = glow_surface
    
    def _create_navigation_system(self):
        """Create sophisticated navigation with perfect button layout."""
        # Professional button configurations
        button_configs = [
            ("Begin Journey", MenuAction.START_GAME, Colors.GOLD, "Start your descent into the Egyptian underworld"),
            ("Construct Deck", MenuAction.DECK_BUILDER, Colors.LAPIS_LAZULI, "Build powerful card combinations"),
            ("Hall of Gods", MenuAction.COLLECTION, Colors.PURPLE, "View your divine collection"),
            ("Animation Forge", MenuAction.ANIMATION_FORGE, Colors.GREEN, "Generate card animations with AI"),
            ("Sacred Settings", MenuAction.SETTINGS, Colors.GRAY, "Configure your journey"),
            ("Return to Mortality", MenuAction.QUIT, Colors.RED, "Exit the underworld")
        ]
        
        # Calculate perfect button layout for ultrawide
        center_zone = self.layout.get_zone_rect(LayoutZone.CENTER_MAIN)
        button_width, button_height = self.layout.get_element_size(ElementType.BUTTON)
        button_font_size = self.layout.get_font_size('button')
        spacing = self.layout.get_spacing('large')
        
        # Enhanced button positioning
        total_buttons = len(button_configs)
        if self.layout.is_ultrawide:
            # Two column layout for ultrawide
            cols = 2
            rows = (total_buttons + 1) // 2
            
            button_spacing_x = button_width + self.layout.get_spacing('huge')
            button_spacing_y = button_height + spacing
            
            total_width = cols * button_width + (cols - 1) * self.layout.get_spacing('huge')
            total_height = rows * button_height + (rows - 1) * spacing
            
            start_x = center_zone.x + (center_zone.width - total_width) // 2
            start_y = center_zone.y + (center_zone.height - total_height) // 2
            
            positions = []
            for i in range(total_buttons):
                row = i // cols
                col = i % cols
                x = start_x + col * button_spacing_x
                y = start_y + row * button_spacing_y
                positions.append((x, y))
        else:
            # Single column for standard displays
            positions = self.layout.create_button_layout(LayoutZone.CENTER_MAIN, total_buttons, 'vertical')
        
        # Create enhanced buttons
        self.buttons = []
        self.button_descriptions = []
        
        for i, (text, action, color, description) in enumerate(button_configs):
            if i < len(positions):
                pos = positions[i]
                button = AnimatedButton(
                    x=pos[0],
                    y=pos[1],
                    width=button_width,
                    height=button_height,
                    text=text,
                    font_size=button_font_size
                )
                button.action = action
                button.base_color = color
                button.description = description
                self.buttons.append(button)
                self.button_descriptions.append(description)
    
    def _create_information_panels(self):
        """Create informative side panels with Egyptian lore."""
        panel_font_size = self.layout.get_font_size('body')
        small_font_size = self.layout.get_font_size('small') 
        self.panel_font = pygame.font.Font(None, panel_font_size)
        self.small_font = pygame.font.Font(None, small_font_size)
        
        # Left panel: Egyptian mythology and lore
        left_zone = self.layout.get_zone_rect(LayoutZone.LEFT_PANEL)
        
        lore_sections = [
            ("THE UNDERWORLD AWAITS", Colors.GOLD),
            ("", None),
            ("In ancient Egypt, death was", Colors.PAPYRUS),
            ("not an end, but a journey", Colors.PAPYRUS), 
            ("through the Duat - the", Colors.PAPYRUS),
            ("realm of the dead.", Colors.PAPYRUS),
            ("", None),
            ("Guide your soul through", Colors.DESERT_SAND),
            ("trials of gods and monsters,", Colors.DESERT_SAND),
            ("using cards blessed by", Colors.DESERT_SAND),
            ("divine powers.", Colors.DESERT_SAND),
            ("", None),
            ("Victory means eternal", Colors.GOLD),
            ("rest in the Field of Reeds.", Colors.GOLD),
        ]
        
        self.left_panel_elements = self._create_panel_elements(left_zone, lore_sections)
        
        # Right panel: Game features and technical info
        right_zone = self.layout.get_zone_rect(LayoutZone.RIGHT_PANEL)
        
        feature_sections = [
            ("DIVINE FEATURES", Colors.GOLD),
            ("", None),
            ("• Hades-level polish", Colors.LAPIS_LAZULI),
            ("• Authentic Egyptian art", Colors.LAPIS_LAZULI),
            ("• Strategic card combat", Colors.LAPIS_LAZULI),
            ("• AI-generated animations", Colors.LAPIS_LAZULI),
            ("• 4K ultrawide support", Colors.LAPIS_LAZULI),
            ("", None),
            ("TECHNICAL EXCELLENCE", Colors.GOLD),
            ("", None),
            (f"• Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", Colors.PAPYRUS),
            (f"• Display: {'Ultrawide' if self.layout.is_ultrawide else 'Standard'}", Colors.PAPYRUS),
            (f"• Scaling: {int(self.layout.ui_scale * 100)}%", Colors.PAPYRUS),
            ("• Engine: Professional Python", Colors.PAPYRUS),
            ("", None),
            ("Version 1.0 - Egyptian Edition", Colors.DESERT_SAND),
        ]
        
        self.right_panel_elements = self._create_panel_elements(right_zone, feature_sections)
    
    def _create_panel_elements(self, zone_rect, sections):
        """Create rendered panel elements."""
        elements = []
        y_offset = zone_rect.y + self.layout.get_spacing('large')
        line_spacing = self.layout.get_spacing('small')
        
        for text, color in sections:
            if text == "":
                # Empty line for spacing
                y_offset += line_spacing
            elif text.startswith("•"):
                # Bullet point
                surface = self.panel_font.render(text, True, color)
                pos = (zone_rect.x + self.layout.get_spacing('medium'), y_offset)
                elements.append((surface, pos, 'bullet'))
                y_offset += surface.get_height() + line_spacing
            elif color == Colors.GOLD:
                # Section header
                surface = self.panel_font.render(text, True, color)
                pos = (zone_rect.x + self.layout.get_spacing('small'), y_offset)
                elements.append((surface, pos, 'header'))
                y_offset += surface.get_height() + self.layout.get_spacing('medium')
            else:
                # Regular text
                surface = self.panel_font.render(text, True, color)
                pos = (zone_rect.x + self.layout.get_spacing('medium'), y_offset)
                elements.append((surface, pos, 'text'))
                y_offset += surface.get_height() + line_spacing
        
        return elements
    
    def _create_decorative_elements(self):
        """Create decorative Egyptian elements."""
        # TODO: Add hieroglyphic decorations, ankh symbols, etc.
        pass
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: tuple):
        """Update menu with smooth animations."""
        self.animation_time += dt
        self.particle_time += dt
        self.glow_pulse = math.sin(self.animation_time * 1.5) * 0.3 + 0.7
        
        # Update screen flash
        if self.screen_flash_alpha > 0:
            self.screen_flash_time += dt
            self.screen_flash_alpha = max(0, 30 - self.screen_flash_time * 100)
        
        # Handle input events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.handle_click(mouse_pos):
                        # Add click effect
                        advanced_visual_effects.add_button_glow(
                            button.x, button.y, button.width, button.height,
                            button.base_color, intensity=1.0, duration=0.5
                        )
                        
                        if self.on_menu_action and hasattr(button, 'action'):
                            # Add screen flash for button feedback
                            self.screen_flash_alpha = 30
                            self.screen_flash_time = 0.0
                            self.on_menu_action(button.action)
                        break
        
        # Update button states and animations
        self.hover_button = None
        for i, button in enumerate(self.buttons):
            # Handle different mouse_pressed formats
            if isinstance(mouse_pressed, (list, tuple)) and len(mouse_pressed) > 0:
                mouse_button_pressed = mouse_pressed[0]
            else:
                mouse_button_pressed = bool(mouse_pressed) if mouse_pressed else False
            
            button.update(dt, mouse_pos, mouse_button_pressed)
            if button.is_hovered:
                self.hover_button = button
                self.selected_index = i
        
        # Update background particles
        self._update_background_particles(dt)
    
    def _update_background_particles(self, dt: float):
        """Update floating background particles."""
        for particle in self.background_particles:
            # Move particles up with drift
            particle['y'] -= particle['speed'] * dt * 60
            particle['x'] += particle['drift_x'] * dt * 60
            
            # Update pulse
            particle['angle'] += particle['pulse_speed'] * dt * 360
            
            # Keep particles on screen horizontally
            if particle['x'] < -10:
                particle['x'] = SCREEN_WIDTH + 10
            elif particle['x'] > SCREEN_WIDTH + 10:
                particle['x'] = -10
            
            # Reset particle when it goes off screen vertically
            if particle['y'] < -10:
                particle['y'] = SCREEN_HEIGHT + 10
                particle['x'] = random.randint(0, SCREEN_WIDTH)
                particle['speed'] = random.uniform(0.5, 1.5)
                particle['size'] = random.uniform(2, 6)
    
    def render(self, surface: pygame.Surface):
        """Render ultra refined menu with professional presentation."""
        # Background layers
        surface.blit(self.background, (0, 0))
        
        # Background particles
        self._render_background_particles(surface)
        
        # Vignette overlay
        surface.blit(self.vignette, (0, 0))
        
        # Title system with glow
        self._render_title_system(surface)
        
        # Side panels
        self._render_information_panels(surface)
        
        # Navigation buttons with enhancements
        self._render_navigation_system(surface)
        
        # Hover tooltip
        if self.hover_button:
            self._render_hover_tooltip(surface)
        
        # Screen flash effect for button feedback
        if self.screen_flash_alpha > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((*Colors.GOLD, int(self.screen_flash_alpha)))
            surface.blit(flash_surface, (0, 0))
    
    def _render_background_particles(self, surface: pygame.Surface):
        """Render enhanced background particles."""
        for particle in self.background_particles:
            # Calculate pulsing alpha
            pulse_factor = math.sin(math.radians(particle['angle'])) * 0.3 + 0.7
            alpha = int(particle['alpha'] * self.glow_pulse * pulse_factor)
            
            # Create glowing particle
            base_size = int(particle['size'])
            glow_size = int(base_size * 1.5)
            
            # Create particle surface with glow
            particle_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            # Draw glow layers
            for i in range(3):
                glow_alpha = alpha // (i + 2)
                glow_color = (*particle['color'][:3], glow_alpha)
                glow_radius = glow_size - i
                
                if glow_radius > 0:
                    pygame.draw.circle(particle_surface, glow_color,
                                     (glow_size, glow_size), glow_radius)
            
            # Draw core
            core_color = (*particle['color'][:3], min(255, alpha + 50))
            pygame.draw.circle(particle_surface, core_color,
                             (glow_size, glow_size), base_size)
            
            surface.blit(particle_surface, 
                        (particle['x'] - glow_size, particle['y'] - glow_size))
    
    def _render_title_system(self, surface: pygame.Surface):
        """Render title system with glow effects."""
        # Title glow effect
        glow_alpha = int(100 * self.glow_pulse)
        glow_copy = self.title_glow.copy()
        glow_copy.set_alpha(glow_alpha)
        
        glow_pos = (self.title_pos[0] - 20, self.title_pos[1] - 20)
        surface.blit(glow_copy, glow_pos)
        
        # Main title
        surface.blit(self.main_title, self.title_pos)
        surface.blit(self.subtitle, self.subtitle_pos)
        surface.blit(self.tagline, self.tagline_pos)
    
    def _render_information_panels(self, surface: pygame.Surface):
        """Render side information panels."""
        # Left panel
        for element_surface, pos, element_type in self.left_panel_elements:
            if element_type == 'header':
                # Add subtle glow to headers
                glow_rect = pygame.Rect(pos[0] - 5, pos[1] - 2, 
                                      element_surface.get_width() + 10, 
                                      element_surface.get_height() + 4)
                glow_color = (*Colors.GOLD, int(30 * self.glow_pulse))
                pygame.draw.rect(surface, glow_color, glow_rect, border_radius=3)
            
            surface.blit(element_surface, pos)
        
        # Right panel  
        for element_surface, pos, element_type in self.right_panel_elements:
            if element_type == 'header':
                # Add subtle glow to headers
                glow_rect = pygame.Rect(pos[0] - 5, pos[1] - 2,
                                      element_surface.get_width() + 10,
                                      element_surface.get_height() + 4)
                glow_color = (*Colors.GOLD, int(30 * self.glow_pulse))
                pygame.draw.rect(surface, glow_color, glow_rect, border_radius=3)
            
            surface.blit(element_surface, pos)
    
    def _render_navigation_system(self, surface: pygame.Surface):
        """Render navigation buttons with enhancements."""
        for i, button in enumerate(self.buttons):
            # Render button
            button.render(surface)
            
            # Add selection indicator for keyboard navigation
            if i == self.selected_index and not button.is_hovered:
                indicator_rect = pygame.Rect(
                    button.x - 5, button.y - 5,
                    button.width + 10, button.height + 10
                )
                indicator_color = (*Colors.PAPYRUS, int(50 * self.glow_pulse))
                pygame.draw.rect(surface, indicator_color, indicator_rect, width=2, border_radius=8)
    
    def _render_hover_tooltip(self, surface: pygame.Surface):
        """Render tooltip for hovered button."""
        if not hasattr(self.hover_button, 'description'):
            return
            
        description = self.hover_button.description
        tooltip_font = self.small_font
        tooltip_surface = tooltip_font.render(description, True, Colors.PAPYRUS)
        
        # Position tooltip near button
        tooltip_x = self.hover_button.x + self.hover_button.width + self.layout.get_spacing('medium')
        tooltip_y = self.hover_button.y + self.hover_button.height // 2 - tooltip_surface.get_height() // 2
        
        # Ensure tooltip stays on screen
        if tooltip_x + tooltip_surface.get_width() > SCREEN_WIDTH:
            tooltip_x = self.hover_button.x - tooltip_surface.get_width() - self.layout.get_spacing('medium')
        
        # Tooltip background
        padding = self.layout.get_spacing('small')
        tooltip_bg = pygame.Rect(
            tooltip_x - padding, tooltip_y - padding,
            tooltip_surface.get_width() + padding * 2,
            tooltip_surface.get_height() + padding * 2
        )
        
        bg_color = (*Colors.DARK_BLUE, 220)
        pygame.draw.rect(surface, bg_color, tooltip_bg, border_radius=5)
        pygame.draw.rect(surface, Colors.GOLD, tooltip_bg, width=2, border_radius=5)
        
        surface.blit(tooltip_surface, (tooltip_x, tooltip_y))
    
    def reset_animations(self):
        """Reset all animations."""
        self.animation_time = 0.0
        self.particle_time = 0.0
        for button in self.buttons:
            if hasattr(button, 'reset_animation'):
                button.reset_animation()

# Need to import random for particles
import random