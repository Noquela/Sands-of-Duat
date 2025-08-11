"""
Narrative Screen - Egyptian Lore Display
Beautiful presentation of Egyptian mythology and story events.
"""

import pygame
import math
import textwrap
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ...narrative.egyptian_lore_system import NarrativeEvent, EgyptianGod
from ..components.animated_button import AnimatedButton

class NarrativeAction(Enum):
    """Narrative screen actions."""
    CONTINUE = auto()
    MAKE_CHOICE = auto()
    SKIP = auto()

class NarrativeScreen:
    """
    Professional narrative screen for Egyptian lore presentation.
    Features typewriter effects, god portraits, and atmospheric presentation.
    """
    
    def __init__(self, on_action: Optional[Callable[[NarrativeAction, str], None]] = None):
        """Initialize narrative screen."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Current narrative state
        self.current_event: Optional[NarrativeEvent] = None
        self.text_progress = 0.0
        self.text_speed = 30.0  # Characters per second
        self.current_character = 0
        self.text_complete = False
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Visual effects
        self.particle_effects = []
        self.glow_intensity = 0.0
        
        # UI components
        self.continue_button = None
        self.choice_buttons = []
        self.skip_button = None
        
        # Background
        self.background_surface = self._create_background()
        
        # Create UI
        self._create_ui_elements()
        
        print("Narrative Screen initialized - Ready for Egyptian storytelling")
    
    def _create_background(self) -> pygame.Surface:
        """Create atmospheric narrative background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Deep blue-purple gradient for mystical atmosphere
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(15 + ratio * 10)   # Deep blues
            g = int(10 + ratio * 15)   # Mystical purples
            b = int(35 + ratio * 25)   # Rich night sky
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add subtle stars
        import random
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)  # Upper half only
            pygame.draw.circle(background, (*Colors.GOLD, 100), (x, y), 1)
        
        return background
    
    def _create_ui_elements(self):
        """Create UI buttons."""
        # Continue button
        self.continue_button = AnimatedButton(
            SCREEN_CENTER[0] - 100, SCREEN_HEIGHT - 100, 200, 50,
            "CONTINUE", FontSizes.BUTTON,
            action=lambda: self._handle_action(NarrativeAction.CONTINUE, "")
        )
        
        # Skip button
        self.skip_button = AnimatedButton(
            SCREEN_WIDTH - 120, 20, 100, 30,
            "SKIP", FontSizes.CARD_TEXT,
            action=lambda: self._handle_action(NarrativeAction.SKIP, "")
        )
    
    def show_narrative(self, event: NarrativeEvent):
        """Show a narrative event."""
        self.current_event = event
        self.text_progress = 0.0
        self.current_character = 0
        self.text_complete = False
        
        # Reset animations
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        # Create choice buttons if needed
        self.choice_buttons.clear()
        if event.choices:
            button_width = 300
            button_height = 40
            spacing = 10
            total_height = len(event.choices) * (button_height + spacing)
            start_y = SCREEN_CENTER[1] + 100
            
            for i, choice in enumerate(event.choices):
                y = start_y + i * (button_height + spacing)
                x = SCREEN_CENTER[0] - button_width // 2
                
                button = AnimatedButton(
                    x, y, button_width, button_height, choice, FontSizes.BODY,
                    action=lambda c=choice: self._handle_action(NarrativeAction.MAKE_CHOICE, c)
                )
                self.choice_buttons.append(button)
        
        print(f"Showing narrative: {event.title}")
    
    def _handle_action(self, action: NarrativeAction, data: str = ""):
        """Handle narrative actions."""
        if action == NarrativeAction.CONTINUE and not self.text_complete:
            # Skip to end of text if still typing
            self.text_complete = True
            self.current_character = len(self.current_event.text)
        elif self.on_action:
            self.on_action(action, data)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """Update narrative screen."""
        if not self.current_event:
            return
        
        self.animation_time += dt
        
        # Fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Text typewriter effect
        if not self.text_complete:
            self.text_progress += dt * self.text_speed
            self.current_character = min(int(self.text_progress), len(self.current_event.text))
            
            if self.current_character >= len(self.current_event.text):
                self.text_complete = True
        
        # Update visual effects
        self.glow_intensity = 0.5 + 0.3 * math.sin(self.animation_time * 2)
        
        # Update particles (simple floating effect)
        self._update_particles(dt)
        
        # Update UI elements
        if self.text_complete:
            self.continue_button.update(dt, mouse_pos, mouse_pressed)
            
        for button in self.choice_buttons:
            if self.text_complete:
                button.update(dt, mouse_pos, mouse_pressed)
        
        self.skip_button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not self.text_complete:
                        self.text_complete = True
                        self.current_character = len(self.current_event.text)
                    else:
                        self._handle_action(NarrativeAction.CONTINUE)
                elif event.key == pygame.K_ESCAPE:
                    self._handle_action(NarrativeAction.SKIP)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks
                if self.text_complete and self.continue_button.handle_click(mouse_pos):
                    audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
                elif self.skip_button.handle_click(mouse_pos):
                    audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.4)
                else:
                    # Check choice buttons
                    for button in self.choice_buttons:
                        if self.text_complete and button.handle_click(mouse_pos):
                            audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
                            break
                    else:
                        # Click anywhere to advance text
                        if not self.text_complete:
                            self.text_complete = True
                            self.current_character = len(self.current_event.text)
    
    def _update_particles(self, dt: float):
        """Update floating particle effects."""
        # Simple particle system for atmosphere
        if len(self.particle_effects) < 20:
            import random
            self.particle_effects.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT + 10,
                'size': random.randint(1, 3),
                'speed': random.randint(20, 50),
                'alpha': random.randint(50, 100),
                'color': random.choice([Colors.GOLD, Colors.LAPIS_LAZULI, Colors.PAPYRUS])
            })
        
        # Update existing particles
        for particle in self.particle_effects[:]:
            particle['y'] -= particle['speed'] * dt
            particle['alpha'] = max(0, particle['alpha'] - 30 * dt)
            
            if particle['y'] < -10 or particle['alpha'] <= 0:
                self.particle_effects.remove(particle)
    
    def render(self, surface: pygame.Surface):
        """Render the narrative screen."""
        if not self.current_event:
            return
        
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Particles
        self._render_particles(surface)
        
        # God portrait if available
        self._render_god_portrait(surface)
        
        # Title
        self._render_title(surface)
        
        # Main narrative text
        self._render_narrative_text(surface)
        
        # Choice buttons
        if self.text_complete and self.choice_buttons:
            for button in self.choice_buttons:
                button.render(surface)
        
        # Continue button
        if self.text_complete and not self.choice_buttons:
            self.continue_button.render(surface)
        
        # Skip button
        self.skip_button.render(surface)
        
        # Subtle UI instructions
        self._render_instructions(surface)
        
        # Fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_particles(self, surface: pygame.Surface):
        """Render floating particles."""
        for particle in self.particle_effects:
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle['color'], int(particle['alpha']))
            particle_surface.fill(color_with_alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def _render_god_portrait(self, surface: pygame.Surface):
        """Render god portrait if available."""
        if not self.current_event.god_associated:
            return
        
        # Try to load god portrait
        god_name = self.current_event.god_associated.name.lower()
        portrait = self.asset_loader.load_character_portrait(f"{god_name}_deity")
        
        if portrait:
            # Scale and position portrait
            portrait_size = (200, 300)
            scaled_portrait = pygame.transform.smoothscale(portrait, portrait_size)
            
            # Position on left side
            portrait_rect = pygame.Rect(50, 100, *portrait_size)
            
            # Add glow effect
            glow_alpha = int(100 * self.glow_intensity)
            glow_surface = pygame.Surface((portrait_size[0] + 20, portrait_size[1] + 20), pygame.SRCALPHA)
            glow_surface.fill((*Colors.GOLD, glow_alpha))
            surface.blit(glow_surface, (portrait_rect.x - 10, portrait_rect.y - 10))
            
            surface.blit(scaled_portrait, portrait_rect)
            
            # Golden border
            pygame.draw.rect(surface, Colors.GOLD, portrait_rect, 3)
    
    def _render_title(self, surface: pygame.Surface):
        """Render narrative title."""
        font = pygame.font.Font(None, FontSizes.TITLE_MEDIUM)
        title_text = self.current_event.title
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.LAPIS_LAZULI)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 80))
        glow_surface.set_alpha(150)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 78))
        surface.blit(title_surface, title_rect)
        
        # Speaker name
        if self.current_event.speaker:
            speaker_font = pygame.font.Font(None, FontSizes.BODY)
            speaker_surface = speaker_font.render(f"~ {self.current_event.speaker} ~", True, Colors.PAPYRUS)
            speaker_rect = speaker_surface.get_rect(center=(SCREEN_CENTER[0], 110))
            surface.blit(speaker_surface, speaker_rect)
    
    def _render_narrative_text(self, surface: pygame.Surface):
        """Render main narrative text with typewriter effect."""
        if not self.current_event.text:
            return
        
        # Get displayed text (up to current character)
        displayed_text = self.current_event.text[:self.current_character]
        
        # Word wrap the text
        font = pygame.font.Font(None, FontSizes.BODY)
        max_width = SCREEN_WIDTH - 300  # Leave room for portrait
        
        # Simple word wrapping
        words = displayed_text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, Colors.WHITE)
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Render text lines
        text_start_y = 180
        line_height = 35
        text_x = 300  # Offset for portrait
        
        # Text background panel
        panel_height = len(lines) * line_height + 40
        panel_rect = pygame.Rect(text_x - 20, text_start_y - 20, max_width + 40, panel_height)
        panel_surface = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel_surface.fill((*Colors.BLACK, 150))
        surface.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(surface, Colors.GOLD, panel_rect, 2)
        
        # Render each line
        for i, line in enumerate(lines):
            y = text_start_y + i * line_height
            
            # Text shadow
            shadow_surface = font.render(line, True, Colors.BLACK)
            surface.blit(shadow_surface, (text_x + 2, y + 2))
            
            # Main text
            text_surface = font.render(line, True, Colors.PAPYRUS)
            surface.blit(text_surface, (text_x, y))
    
    def _render_instructions(self, surface: pygame.Surface):
        """Render subtle instruction text."""
        if not self.text_complete:
            instruction = "Click or press SPACE to continue reading"
        elif self.choice_buttons:
            instruction = "Choose your response"
        else:
            instruction = "Click CONTINUE or press SPACE to proceed"
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        instruction_surface = font.render(instruction, True, (*Colors.DESERT_SAND, 150))
        instruction_surface.set_alpha(150)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 50))
        surface.blit(instruction_surface, instruction_rect)
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        self.particle_effects.clear()
        
        # Start ambient narrative music
        # audio_manager.play_music(AudioTrack.AMBIENT, fade_in=3.0)