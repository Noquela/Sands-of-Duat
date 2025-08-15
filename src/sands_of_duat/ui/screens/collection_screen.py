"""
Collection Screen - Hall of Gods
Professional responsive card collection viewing with Egyptian theming.
"""

import pygame
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.hades_button import HadesButton
from ..responsive.scaling_manager import scaling_manager
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout
from ..components.responsive_typography import responsive_typography, TextStyle

class CollectionAction(Enum):
    """Collection screen actions."""
    BACK_TO_MENU = auto()

class CollectionScreen:
    """Professional responsive collection screen with Egyptian theming."""
    
    def __init__(self, on_action: Optional[Callable[[CollectionAction], None]] = None):
        self.on_action = on_action
        
        # Initialize responsive systems
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Collection state
        self.selected_card = None
        self.card_grid_offset = 0
        
        # Create background
        self.background_surface = self._create_enhanced_background()
        
        # Create buttons
        self.buttons = self._create_enhanced_buttons()
        
        # Pre-render card collection to avoid loading assets every frame
        self.card_collection_surface = None
        self._pre_render_card_collection()
        
        # Initialize audio
        try:
            audio_manager.play_sound(SoundEffect.UI_HOVER)
        except Exception as e:
            print(f"Could not play collection screen sound: {e}")
        
        print("Enhanced Collection Screen initialized - Hall of Gods awaits your presence")
    
    def _pre_render_card_collection(self):
        """Pre-render the card collection once to avoid loading assets every frame."""
        try:
            # Create a surface for the card collection
            from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout
            center_zone = enhanced_ultrawide_layout.get_zone_rect(enhanced_ultrawide_layout.LayoutZone.CENTER_MAIN)
            
            self.card_collection_surface = pygame.Surface((center_zone.width, center_zone.height), pygame.SRCALPHA)
            self._render_card_collection(self.card_collection_surface, center_zone)
        except Exception as e:
            print(f"Failed to pre-render card collection: {e}")
            self.card_collection_surface = None
    
    def _render_card_collection(self, surface: pygame.Surface, center_zone: pygame.Rect):
        """Render card collection using asset pipeline for beautiful card display."""
        from ...assets.smart_asset_loader import smart_asset_loader
        
        # Sample Egyptian cards to display
        sample_cards = [
            {'name': 'Ra - Sun God', 'rarity': 'legendary'},
            {'name': 'Anubis - Judge of the Dead', 'rarity': 'legendary'},
            {'name': 'Isis - Divine Mother', 'rarity': 'legendary'},
            {'name': 'Set - Chaos God', 'rarity': 'legendary'},
            {'name': 'Egyptian Warrior', 'rarity': 'common'},
            {'name': 'Mummy Guardian', 'rarity': 'rare'}
        ]
        
        # Card display settings
        card_width, card_height = 120, 168  # Scaled down for collection view
        cards_per_row = 6
        spacing_x = 140
        spacing_y = 190
        
        # Calculate starting position for centered grid
        total_width = (cards_per_row - 1) * spacing_x + card_width
        start_x = center_zone.centerx - total_width // 2
        start_y = center_zone.centery - 20
        
        for i, card_data in enumerate(sample_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            
            card_x = start_x + col * spacing_x
            card_y = start_y + row * spacing_y
            
            # Load card artwork using asset pipeline
            card_art = smart_asset_loader.load_asset(f'card_{card_data["name"].lower().replace(" ", "_").replace("-", "_")}')
            if not card_art:
                # Try card mapping fallback
                card_art = self.asset_loader.load_card_art_by_name(card_data['name'])
            
            # Load card frame using asset pipeline
            card_frame = smart_asset_loader.get_card_frame(card_data['rarity'])
            if not card_frame:
                card_frame = smart_asset_loader.load_asset(f'ui_card_frame_{card_data["rarity"]}')
            
            # Create card surface
            card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
            
            if card_art:
                # Scale and blit card artwork
                scaled_art = pygame.transform.smoothscale(card_art, (card_width - 10, card_height - 10))
                card_surface.blit(scaled_art, (5, 5))
            else:
                # Fallback: Beautiful colored rectangle with rarity color
                rarity_colors = {
                    'legendary': Colors.GOLD,
                    'epic': Colors.PURPLE,
                    'rare': Colors.LAPIS_LAZULI,
                    'common': Colors.DESERT_SAND
                }
                card_color = rarity_colors.get(card_data['rarity'], Colors.GRAY)
                pygame.draw.rect(card_surface, card_color, (5, 5, card_width - 10, card_height - 10))
                pygame.draw.rect(card_surface, Colors.GOLD, (5, 5, card_width - 10, card_height - 10), 2)
            
            if card_frame:
                # Scale and overlay card frame
                scaled_frame = pygame.transform.smoothscale(card_frame, (card_width, card_height))
                card_surface.blit(scaled_frame, (0, 0))
            
            # Add subtle glow effect
            glow_surface = pygame.Surface((card_width + 6, card_height + 6), pygame.SRCALPHA)
            glow_color = (*Colors.GOLD, 100)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, card_width + 6, card_height + 6), 3, border_radius=8)
            surface.blit(glow_surface, (card_x - 3, card_y - 3))
            
            # Blit the final card
            surface.blit(card_surface, (card_x, card_y))
    
    def _create_enhanced_background(self):
        """Create enhanced collection background using asset pipeline."""
        from ...assets.smart_asset_loader import smart_asset_loader
        
        # SPRINT 2: Use smart asset loader for beautiful collection background
        bg_asset = smart_asset_loader.get_background('collection')
        if not bg_asset:
            bg_asset = smart_asset_loader.get_background('hall_of_gods')
        if not bg_asset:
            bg_asset = smart_asset_loader.load_asset('bg_hall_of_gods_4k')
        
        if bg_asset:
            # Scale the high-quality background to screen size
            background = pygame.transform.smoothscale(bg_asset, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add minimal Egyptian ambiance overlay to preserve art quality
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 5, 20, 40))  # Very light mystical overlay
            background.blit(overlay, (0, 0))
            return background
        
        # Fallback: Enhanced gradient
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Deep Egyptian temple gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            # Richer, more atmospheric colors
            r = int(25 + ratio * 35)  # Deeper browns
            g = int(15 + ratio * 25)  # Subtle golds
            b = int(45 + ratio * 55)  # Deep blues
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        return background
    
    def _create_enhanced_buttons(self) -> List[HadesButton]:
        """Create enhanced UI buttons with responsive design."""
        buttons = []
        
        # Get responsive button dimensions
        button_width, button_height = scaling_manager.get_component_size('button_default')
        
        # Back button with Egyptian theming
        back_button = HadesButton(
            50, 50, button_width, button_height, "RETURN TO TEMPLE",
            theme_color=Colors.RED,
            hieroglyph="◄",
            on_click=lambda: self._handle_action(CollectionAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        return buttons
    
    def _handle_action(self, action: CollectionAction):
        """Handle button actions."""
        if self.on_action:
            self.on_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update the collection screen."""
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(CollectionAction.BACK_TO_MENU)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # HadesButton handles clicks internally via on_click callback
                pass
    
    def render(self, surface: pygame.Surface):
        """Render the enhanced collection screen with responsive design."""
        try:
            # Background
            surface.blit(self.background_surface, (0, 0))
            
            # Enhanced title with responsive typography
            responsive_typography.render_text(
                "HALL OF GODS", TextStyle.TITLE_HUGE, surface,
                (SCREEN_CENTER[0], 150), center=True, custom_color=Colors.GOLD
            )
            
            # Subtitle with Egyptian theming
            center_zone = enhanced_ultrawide_layout.get_zone_rect(enhanced_ultrawide_layout.LayoutZone.CENTER_MAIN)
            responsive_typography.render_text(
                "Sacred Collection of Divine Cards", TextStyle.SUBTITLE, surface,
                (SCREEN_CENTER[0], 220), center=True, custom_color=Colors.LAPIS_LAZULI
            )
            
            # Enhanced description
            responsive_typography.render_text(
                "Behold the divine artifacts collected on your journey through the underworld.", 
                TextStyle.CARD_TEXT, surface,
                (SCREEN_CENTER[0], center_zone.centery - 50), center=True, custom_color=Colors.PAPYRUS
            )
            
            # SPRINT 2: Display pre-rendered card collection
            if self.card_collection_surface:
                surface.blit(self.card_collection_surface, (center_zone.x, center_zone.y))
            else:
                # Fallback: render directly if pre-rendering failed
                self._render_card_collection(surface, center_zone)
            
            # Responsive instructions
            responsive_typography.render_text(
                "ESC: Return to Main Temple", TextStyle.TOOLTIP, surface,
                (SCREEN_CENTER[0], SCREEN_HEIGHT - 80), center=True, custom_color=Colors.DESERT_SAND
            )
            
            # Buttons with proper font
            for button in self.buttons:
                button.render(surface, scaling_manager.get_font('button'))
            
            # Fade-in effect
            if not self.fade_in_complete:
                fade_alpha = int(255 * (1.0 - self.fade_in_progress))
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                fade_surface.fill((0, 0, 0, fade_alpha))
                surface.blit(fade_surface, (0, 0))
                
        except Exception as e:
            print(f"Error rendering collection screen: {e}")
            # Emergency fallback rendering
            surface.fill(Colors.BLACK)
            font = pygame.font.Font(None, 48)
            error_text = font.render("HALL OF GODS", True, Colors.GOLD)
            surface.blit(error_text, (SCREEN_CENTER[0] - 120, SCREEN_CENTER[1]))
            
            # Render buttons even in error case
            for button in self.buttons:
                try:
                    button.render(surface, pygame.font.Font(None, 24))
                except:
                    pass
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        # Reset button animations (HadesButton compatible)
        for button in self.buttons:
            try:
                button.reset_animation()
            except AttributeError:
                # Fallback for older button types
                if hasattr(button, 'hover_progress'):
                    button.hover_progress = 0.0
            button.press_progress = 0.0