"""
Divine Event Screen - Egyptian Mythology Interactive Storytelling
Features beautifully illustrated dialogue system with divine encounters.
"""

import pygame
import math
import random
from typing import List, Optional, Callable, Tuple, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.hades_button import HadesButton
from ..components.smooth_transitions import smooth_transitions, TransitionType, EasingType
from ..components.responsive_typography import responsive_typography, TextStyle

class EventType(Enum):
    """Types of divine events."""
    DIVINE_TRIAL = auto()
    ANCIENT_WISDOM = auto()
    MYSTICAL_ENCOUNTER = auto()
    DESERT_ORACLE = auto()
    TOMB_MYSTERY = auto()
    DIVINE_BLESSING = auto()
    MORAL_CHOICE = auto()

class EventAction(Enum):
    """Event screen actions."""
    BACK_TO_MAP = auto()
    CHOOSE_OPTION = auto()
    CONTINUE_STORY = auto()
    COLLECT_REWARD = auto()

@dataclass
class EventChoice:
    """A choice option in an event."""
    text: str
    consequence: str
    reward: Optional[str] = None
    cost: Optional[str] = None
    icon: str = "𓂀"
    color: Tuple[int, int, int] = Colors.GOLD

@dataclass
class DivineEvent:
    """A complete divine event with story and choices."""
    title: str
    description: str
    story_text: List[str]  # Multiple paragraphs for dramatic storytelling
    illustration_key: str  # Key for loading illustration
    choices: List[EventChoice]
    god_speaker: Optional[str] = None  # Which god is speaking
    background_music: Optional[str] = None
    ambient_effects: List[str] = None

class DivineEventScreen:
    """
    Divine Event Screen with AAA-quality interactive storytelling.
    Features beautiful illustrated dialogues with Egyptian gods and mysteries.
    """
    
    def __init__(self, on_action: Optional[Callable[[EventAction, Any], None]] = None):
        """Initialize the divine event screen."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.text_reveal_progress = 0.0
        self.choice_fade_progress = 0.0
        
        # Story state
        self.current_event: Optional[DivineEvent] = None
        self.current_story_index = 0
        self.story_complete = False
        self.choices_revealed = False
        self.selected_choice = None
        self.hovered_choice = None
        
        # Visual elements
        self.background_surface = self._create_background()
        self.illustration_surface = None
        self.story_scroll_y = 0.0
        self.target_scroll_y = 0.0
        
        # UI elements
        self.choice_buttons: List[HadesButton] = []
        self.action_buttons: List[HadesButton] = []
        
        # Atmospheric effects
        self.particles = []
        self.divine_glow_intensity = 0.0
        self.god_presence_alpha = 0.0
        
        # Event library
        self.event_library = self._create_event_library()
        
        # Initialize with random event
        self._load_random_event()
        
        # Create UI buttons
        self._create_ui_buttons()
        
        # Start fade-in
        smooth_transitions.fade_in_element("divine_event", Timing.FADE_DURATION)
        
        print("Divine Event Screen initialized - The gods await your choices")
    
    def _create_background(self):
        """Create atmospheric event background."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create deep mystical gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            # Deep purple to midnight blue gradient
            r = int(15 + ratio * 25)
            g = int(10 + ratio * 20) 
            b = int(45 + ratio * 55)
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add mystical pattern overlay
        pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, 80):
            for y in range(0, SCREEN_HEIGHT, 80):
                alpha = int(15 + 10 * math.sin(x * 0.02 + y * 0.02))
                hieroglyph_size = random.randint(20, 40)
                pattern_surface.fill(Colors.GOLD, (x, y, 2, hieroglyph_size))
                pattern_surface.set_alpha(alpha)
        
        background.blit(pattern_surface, (0, 0))
        return background
    
    def _create_event_library(self) -> Dict[str, DivineEvent]:
        """Create library of divine events."""
        events = {}
        
        # Divine Trial with Anubis
        events["anubis_trial"] = DivineEvent(
            title="Trial of the Jackal God",
            description="Anubis, Judge of the Dead, appears before you with scales of justice.",
            story_text=[
                "The air grows heavy as golden sand swirls around you, forming the imposing figure of Anubis, the Jackal-headed god of the dead.",
                "His obsidian eyes pierce through your soul as he speaks in a voice like distant thunder: 'Mortal, your heart shall be weighed against the feather of Ma'at.'",
                "The scales of justice materialize before you, glowing with divine light. 'Choose wisely, for your fate in the afterlife hangs in the balance.'"
            ],
            illustration_key="anubis_trial",
            choices=[
                EventChoice("Offer your most precious memory", "Your heart becomes lighter, but you forget something dear", "Divine Blessing", "Precious Memory", "♦", Colors.GOLD),
                EventChoice("Challenge the judgment", "Anubis respects your courage but demands proof", "Test of Courage", None, "⚡", Colors.RED),
                EventChoice("Accept whatever fate awaits", "Your humility impresses the god", "Wisdom of Acceptance", None, "♠", Colors.LAPIS_LAZULI)
            ],
            god_speaker="Anubis",
            background_music="divine_trial",
            ambient_effects=["sand_swirl", "divine_glow"]
        )
        
        # Oracle of Thoth
        events["thoth_wisdom"] = DivineEvent(
            title="Oracle of Infinite Wisdom",
            description="Thoth, the Ibis-headed god of wisdom, offers you ancient knowledge.",
            story_text=[
                "In a chamber filled with scrolls that stretch to infinity, Thoth the Wise appears, his ibis head crowned with the moon disk.",
                "'Seeker of knowledge,' his voice resonates with the weight of millennia, 'I offer you wisdom that spans the ages.'",
                "Before you appear three sacred scrolls, each containing different aspects of divine knowledge. Choose carefully - some truths come with a price."
            ],
            illustration_key="thoth_oracle",
            choices=[
                EventChoice("Learn the secrets of the afterlife", "Gain powerful death magic but become marked by the underworld", "Necromancy Mastery", "Soul Mark", "☆", Colors.PURPLE),
                EventChoice("Understand the language of animals", "Speak with all creatures but lose some human connections", "Beast Speech", "Social Distance", "♪", Colors.GREEN),
                EventChoice("See through divine illusions", "Perceive truth but can never be deceived again", "True Sight", "Loss of Wonder", "◊", Colors.GOLD)
            ],
            god_speaker="Thoth",
            background_music="mystical_wisdom",
            ambient_effects=["floating_scrolls", "wisdom_glow"]
        )
        
        # Isis Blessing
        events["isis_healing"] = DivineEvent(
            title="Blessing of the Divine Mother",
            description="Isis, the Great Goddess, appears in a vision of healing light.",
            story_text=[
                "A warm, golden light suffuses the chamber as Isis manifests, her wings spread wide in protection and love.",
                "'Child of the mortal realm,' her voice carries the gentleness of a mother and the power of creation itself.",
                "Her healing magic flows around you like liquid starlight. 'I offer you gifts of renewal, but each comes with its own sacred responsibility.'"
            ],
            illustration_key="isis_blessing",
            choices=[
                EventChoice("Accept healing for your soul", "Restore all health but promise to heal others", "Complete Healing", "Healer's Oath", "♥", Colors.GREEN),
                EventChoice("Request protection magic", "Gain magical armor but must protect the innocent", "Divine Ward", "Guardian's Duty", "♦", Colors.LAPIS_LAZULI),
                EventChoice("Ask for wisdom in love", "Understand hearts but feel all emotional pain", "Empathic Sight", "Emotional Burden", "♠", Colors.RED)
            ],
            god_speaker="Isis",
            background_music="divine_blessing",
            ambient_effects=["healing_light", "angelic_presence"]
        )
        
        return events
    
    def _load_random_event(self):
        """Load a random event from the library."""
        event_key = random.choice(list(self.event_library.keys()))
        self.current_event = self.event_library[event_key]
        self.current_story_index = 0
        self.story_complete = False
        self.choices_revealed = False
        self.text_reveal_progress = 0.0
        self.choice_fade_progress = 0.0
        
        # Try to load illustration
        self._load_event_illustration()
        
        # Create choice buttons
        self._create_choice_buttons()
        
        # Start atmospheric effects
        self._spawn_event_particles()
    
    def _load_event_illustration(self):
        """Load illustration for current event."""
        if not self.current_event:
            return
            
        # Try to load from assets
        illustration = self.asset_loader.load_image(f"events/{self.current_event.illustration_key}")
        
        if illustration:
            # Scale to fit left side of screen
            target_width = SCREEN_WIDTH // 2 - 100
            target_height = SCREEN_HEIGHT - 200
            
            # Maintain aspect ratio
            original_aspect = illustration.get_width() / illustration.get_height()
            if target_width / target_height > original_aspect:
                # Constrain by height
                final_width = int(target_height * original_aspect)
                final_height = target_height
            else:
                # Constrain by width
                final_width = target_width
                final_height = int(target_width / original_aspect)
            
            self.illustration_surface = pygame.transform.smoothscale(illustration, (final_width, final_height))
        else:
            # Create placeholder illustration
            self.illustration_surface = pygame.Surface((400, 600))
            self.illustration_surface.fill(Colors.BACKGROUND_SECONDARY)
            
            # Add placeholder art
            center = (200, 300)
            pygame.draw.circle(self.illustration_surface, Colors.GOLD, center, 150, 3)
            
            # Add symbols 
            symbols = ["♦", "♠", "♥", "♣", "◊"]
            font = pygame.font.Font(None, 60)
            for i, symbol in enumerate(symbols):
                angle = i * (360 / len(symbols))
                x = center[0] + 100 * math.cos(math.radians(angle))
                y = center[1] + 100 * math.sin(math.radians(angle))
                text = font.render(symbol, True, Colors.GOLD)
                rect = text.get_rect(center=(x, y))
                self.illustration_surface.blit(text, rect)
    
    def _create_choice_buttons(self):
        """Create choice buttons for current event."""
        self.choice_buttons.clear()
        
        if not self.current_event or not self.current_event.choices:
            return
        
        # Position choices on right side
        start_x = SCREEN_WIDTH // 2 + 50
        start_y = SCREEN_HEIGHT // 2
        button_width = 400
        button_height = 80
        spacing = 20
        
        for i, choice in enumerate(self.current_event.choices):
            y = start_y + i * (button_height + spacing)
            
            button = HadesButton(
                start_x, y, button_width, button_height,
                text=choice.text,
                theme_color=choice.color,
                hieroglyph=choice.icon,
                on_click=lambda idx=i: self._choose_option(idx)
            )
            self.choice_buttons.append(button)
    
    def _create_ui_buttons(self):
        """Create UI control buttons."""
        # Continue button (when story is not finished)
        self.continue_button = HadesButton(
            SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100, 150, 50,
            text="CONTINUE",
            theme_color=Colors.GOLD,
            hieroglyph=">",
            on_click=self._continue_story
        )
        
        # Back button
        self.back_button = HadesButton(
            50, 50, 120, 40,
            text="BACK",
            theme_color=Colors.RED,
            hieroglyph="<",
            on_click=lambda: self._handle_action(EventAction.BACK_TO_MAP)
        )
        
        self.action_buttons = [self.back_button, self.continue_button]
    
    def _spawn_event_particles(self):
        """Spawn atmospheric particles for the event."""
        self.particles.clear()
        
        # Create mystical floating particles
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(2, 6),
                'speed': random.randint(10, 30),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.LAPIS_LAZULI, Colors.PAPYRUS]),
                'alpha': random.randint(100, 200)
            })
    
    def _continue_story(self):
        """Continue to next story segment."""
        if not self.current_event:
            return
            
        if self.current_story_index < len(self.current_event.story_text) - 1:
            self.current_story_index += 1
            self.text_reveal_progress = 0.0
        else:
            self.story_complete = True
            self.choices_revealed = True
            self.choice_fade_progress = 0.0
    
    def _choose_option(self, choice_index: int):
        """Handle choice selection."""
        if not self.current_event or choice_index >= len(self.current_event.choices):
            return
        
        self.selected_choice = choice_index
        choice = self.current_event.choices[choice_index]
        
        # Handle action with choice data
        if self.on_action:
            self.on_action(EventAction.CHOOSE_OPTION, {
                'choice': choice,
                'event': self.current_event
            })
    
    def _handle_action(self, action: EventAction, data: Any = None):
        """Handle event actions."""
        if self.on_action:
            self.on_action(action, data)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update event screen."""
        self.animation_time += dt
        
        # Update fade-in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
        
        # Update text reveal
        if self.text_reveal_progress < 1.0:
            self.text_reveal_progress = min(1.0, self.text_reveal_progress + dt * 1.5)
        
        # Update choice fade-in
        if self.choices_revealed and self.choice_fade_progress < 1.0:
            self.choice_fade_progress = min(1.0, self.choice_fade_progress + dt * 2.0)
        
        # Update divine effects
        self.divine_glow_intensity = 0.5 + 0.3 * math.sin(self.animation_time * 1.5)
        if self.current_event and self.current_event.god_speaker:
            self.god_presence_alpha = min(200, self.god_presence_alpha + dt * 100)
        
        # Update particles
        for particle in self.particles:
            particle['x'] += math.sin(self.animation_time + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.7 + particle['phase']) * particle['speed'] * dt * 0.3
            
            # Wrap around
            if particle['x'] < -50:
                particle['x'] = SCREEN_WIDTH + 50
            elif particle['x'] > SCREEN_WIDTH + 50:
                particle['x'] = -50
            if particle['y'] < -50:
                particle['y'] = SCREEN_HEIGHT + 50
            elif particle['y'] > SCREEN_HEIGHT + 50:
                particle['y'] = -50
        
        # Update UI buttons
        for button in self.action_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Update choice buttons (only if revealed)
        if self.choices_revealed:
            self.hovered_choice = None
            for i, button in enumerate(self.choice_buttons):
                button.update(dt, mouse_pos, mouse_pressed)
                if button.rect.collidepoint(mouse_pos):
                    self.hovered_choice = i
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(EventAction.BACK_TO_MAP)
                elif event.key == pygame.K_SPACE:
                    if not self.story_complete:
                        self._continue_story()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    if self.choices_revealed:
                        choice_idx = event.key - pygame.K_1
                        if choice_idx < len(self.choice_buttons):
                            self._choose_option(choice_idx)
    
    def render(self, surface: pygame.Surface):
        """Render the divine event screen."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Divine glow effect
        if self.current_event and self.current_event.god_speaker:
            glow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            glow_alpha = int(30 * self.divine_glow_intensity)
            glow_surface.fill(Colors.GOLD)
            glow_surface.set_alpha(glow_alpha)
            surface.blit(glow_surface, (0, 0))
        
        # Particles
        for particle in self.particles:
            alpha = int(particle['alpha'] * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill(particle['color'])
            particle_surface.set_alpha(alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Illustration
        if self.illustration_surface:
            ill_x = 100
            ill_y = (SCREEN_HEIGHT - self.illustration_surface.get_height()) // 2
            surface.blit(self.illustration_surface, (ill_x, ill_y))
            
            # Divine frame around illustration
            frame_rect = pygame.Rect(ill_x - 10, ill_y - 10, 
                                   self.illustration_surface.get_width() + 20,
                                   self.illustration_surface.get_height() + 20)
            pygame.draw.rect(surface, Colors.GOLD, frame_rect, 3)
        
        # Story content area
        story_x = SCREEN_WIDTH // 2 + 50
        story_y = 120
        story_width = SCREEN_WIDTH // 2 - 100
        
        # Event title
        if self.current_event:
            responsive_typography.render_text(
                self.current_event.title, TextStyle.TITLE_LARGE, surface,
                (story_x + story_width // 2, 80), center=True, custom_color=Colors.GOLD
            )
            
            # God speaker indicator
            if self.current_event.god_speaker:
                responsive_typography.render_text(
                    f"— {self.current_event.god_speaker} speaks —", TextStyle.SUBTITLE, surface,
                    (story_x + story_width // 2, story_y - 30), center=True, custom_color=Colors.LAPIS_LAZULI
                )
        
        # Story text with reveal effect
        self._render_story_text(surface, story_x, story_y, story_width)
        
        # Choice buttons (if revealed)
        if self.choices_revealed:
            choice_alpha = int(255 * self.choice_fade_progress)
            for i, button in enumerate(self.choice_buttons):
                # Create faded surface for each button
                button_surface = pygame.Surface((button.width, button.height), pygame.SRCALPHA)
                button.render(button_surface, pygame.font.Font(None, FontSizes.BUTTON))
                button_surface.set_alpha(choice_alpha)
                surface.blit(button_surface, (button.x, button.y))
                
                # Render choice consequences on hover
                if self.hovered_choice == i and self.current_event:
                    self._render_choice_preview(surface, i, mouse_pos=pygame.mouse.get_pos())
        
        # UI buttons
        for button in self.action_buttons:
            # Only show continue button if story isn't complete
            if button == self.continue_button and (self.story_complete or self.choices_revealed):
                continue
            button.render(surface, pygame.font.Font(None, FontSizes.BUTTON))
        
        # Instructions
        instruction_y = SCREEN_HEIGHT - 50
        if not self.story_complete:
            instruction = "SPACE: Continue Story • ESC: Back to Map"
        else:
            instruction = "Choose your path • 1/2/3: Quick select • ESC: Back to Map"
        
        responsive_typography.render_text(
            instruction, TextStyle.TOOLTIP, surface,
            (SCREEN_CENTER[0], instruction_y), center=True, custom_color=Colors.DESERT_SAND
        )
        
        # Fade-in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
    
    def _render_story_text(self, surface: pygame.Surface, x: int, y: int, width: int):
        """Render story text with typewriter effect."""
        if not self.current_event or self.current_story_index >= len(self.current_event.story_text):
            return
        
        story_segment = self.current_event.story_text[self.current_story_index]
        
        # Calculate revealed characters
        total_chars = len(story_segment)
        revealed_chars = int(total_chars * self.text_reveal_progress)
        revealed_text = story_segment[:revealed_chars]
        
        # Word wrap and render
        words = revealed_text.split(' ')
        lines = []
        current_line = ""
        
        font = pygame.font.Font(None, FontSizes.BODY)
        max_line_width = width - 40
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_line_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Render lines
        line_height = FontSizes.BODY + 8
        for i, line in enumerate(lines):
            text_y = y + i * line_height
            responsive_typography.render_text(
                line, TextStyle.BODY, surface,
                (x + 20, text_y), custom_color=Colors.PAPYRUS
            )
        
        # Progress indicator
        if self.text_reveal_progress < 1.0:
            cursor_x = x + 20 + font.size(lines[-1] if lines else "")[0]
            cursor_y = y + (len(lines) - 1) * line_height if lines else y
            
            alpha = int(128 + 127 * abs(math.sin(self.animation_time * 4)))
            cursor_surface = pygame.Surface((3, FontSizes.BODY), pygame.SRCALPHA)
            cursor_surface.fill(Colors.GOLD)
            cursor_surface.set_alpha(alpha)
            surface.blit(cursor_surface, (cursor_x, cursor_y))
    
    def _render_choice_preview(self, surface: pygame.Surface, choice_index: int, mouse_pos: Tuple[int, int]):
        """Render preview tooltip for choice consequences."""
        if not self.current_event or choice_index >= len(self.current_event.choices):
            return
        
        choice = self.current_event.choices[choice_index]
        
        # Tooltip content
        lines = [
            f"Consequence: {choice.consequence}"
        ]
        
        if choice.reward:
            lines.append(f"Reward: {choice.reward}")
        if choice.cost:
            lines.append(f"Cost: {choice.cost}")
        
        # Calculate tooltip size
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        max_width = 0
        total_height = 0
        
        for line in lines:
            text_size = font.size(line)
            max_width = max(max_width, text_size[0])
            total_height += text_size[1] + 5
        
        # Tooltip background
        tooltip_width = max_width + 20
        tooltip_height = total_height + 10
        tooltip_x = mouse_pos[0] + 20
        tooltip_y = mouse_pos[1] - tooltip_height // 2
        
        # Keep on screen
        if tooltip_x + tooltip_width > SCREEN_WIDTH - 20:
            tooltip_x = mouse_pos[0] - tooltip_width - 20
        if tooltip_y < 20:
            tooltip_y = 20
        elif tooltip_y + tooltip_height > SCREEN_HEIGHT - 20:
            tooltip_y = SCREEN_HEIGHT - tooltip_height - 20
        
        # Draw background
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        tooltip_surface.fill(Colors.BACKGROUND_SECONDARY)
        tooltip_surface.set_alpha(240)
        pygame.draw.rect(tooltip_surface, choice.color, (0, 0, tooltip_width, tooltip_height), 2)
        surface.blit(tooltip_surface, (tooltip_x, tooltip_y))
        
        # Draw text
        y_offset = 10
        for i, line in enumerate(lines):
            color = choice.color if i == 0 else Colors.PAPYRUS
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (tooltip_x + 10, tooltip_y + y_offset))
            y_offset += font.size(line)[1] + 5
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.animation_time = 0.0
        self.text_reveal_progress = 0.0
        self.choice_fade_progress = 0.0
        
        # Start ambient music
        audio_manager.play_music(AudioTrack.AMBIENT, fade_in=2.0)