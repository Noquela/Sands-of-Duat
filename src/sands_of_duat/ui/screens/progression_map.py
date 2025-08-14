"""
Progression Map Screen - Slay the Spire Style Egyptian Journey
Navigate through the underworld with branching paths and divine encounters.
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
# from ..components.enhanced_card_hover import EnhancedCardHover  # Not needed for map
from ..components.smooth_transitions import smooth_transitions, TransitionType, EasingType
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout
from ..components.responsive_typography import responsive_typography, TextStyle

class NodeType(Enum):
    """Types of nodes on the map."""
    COMBAT = auto()
    ELITE = auto()
    BOSS = auto()
    TREASURE = auto()
    EVENT = auto()
    REST = auto()
    SHOP = auto()
    START = auto()

class NodeState(Enum):
    """Node completion states."""
    LOCKED = auto()
    AVAILABLE = auto()
    COMPLETED = auto()
    CURRENT = auto()

@dataclass
class MapNode:
    """A node on the progression map."""
    x: int
    y: int
    node_type: NodeType
    state: NodeState
    name: str
    description: str
    connections: List['MapNode'] = None
    reward: str = ""
    level: int = 0

    def __post_init__(self):
        if self.connections is None:
            self.connections = []

class ProgressionMapAction(Enum):
    """Map screen actions."""
    BACK_TO_MENU = auto()
    ENTER_NODE = auto()
    VIEW_PROGRESS = auto()

class ProgressionMap:
    """
    Slay the Spire style progression map with Egyptian theming.
    Features branching paths through the underworld with various encounters.
    """
    
    def __init__(self, on_action: Optional[Callable[[ProgressionMapAction, Any], None]] = None):
        """Initialize the progression map."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.target_camera_x = 0.0
        self.target_camera_y = 0.0
        
        # Map state
        self.current_level = 0
        self.max_levels = 15
        self.nodes_per_level = 3
        self.level_spacing = 200
        self.node_spacing = 150
        
        # Generate map
        self.nodes = []
        self.current_node = None
        self.selected_node = None
        self.hovered_node = None
        
        self._generate_map()
        
        # Background and effects
        self.background_surface = self._create_background()
        self.particles = []
        self._spawn_particles()
        
        # UI elements
        self.buttons = self._create_buttons()
        
        # Node hover tooltips
        self.node_tooltips = {}
        self._create_node_tooltips()
        
        # Start fade-in
        smooth_transitions.fade_in_element("progression_map", Timing.FADE_DURATION)
        
        print("Progression Map initialized - The journey through the underworld begins!")
    
    def _generate_map(self):
        """Generate the progression map with branching paths."""
        # Calculate map dimensions for centering
        map_width = self.max_levels * self.level_spacing
        map_height = (self.nodes_per_level - 1) * self.node_spacing
        
        start_x = SCREEN_CENTER[0] - map_width // 2
        start_y = SCREEN_CENTER[1] - map_height // 2
        
        # Generate nodes level by level
        previous_level_nodes = []
        
        for level in range(self.max_levels + 1):
            current_level_nodes = []
            
            # Determine node types for this level
            if level == 0:
                # Starting node
                node_types = [NodeType.START]
                nodes_count = 1
            elif level == self.max_levels:
                # Final boss
                node_types = [NodeType.BOSS]
                nodes_count = 1
            elif level % 5 == 0 and level > 0:
                # Boss levels every 5 levels
                node_types = [NodeType.BOSS]
                nodes_count = 1
            elif level % 3 == 0 and level > 0:
                # Elite encounters
                node_types = [NodeType.ELITE, NodeType.TREASURE, NodeType.REST]
                nodes_count = min(3, self.nodes_per_level)
            else:
                # Regular levels
                node_types = [NodeType.COMBAT, NodeType.EVENT, NodeType.TREASURE, NodeType.REST, NodeType.SHOP]
                nodes_count = self.nodes_per_level
            
            # Create nodes for this level
            if nodes_count == 1:
                # Single node (boss or start)
                y = start_y + map_height // 2
                node_type = node_types[0]
            else:
                # Multiple nodes
                level_start_y = start_y + (map_height - (nodes_count - 1) * self.node_spacing) // 2
            
            for i in range(nodes_count):
                x = start_x + level * self.level_spacing
                
                if nodes_count == 1:
                    y = start_y + map_height // 2
                    node_type = node_types[0]
                else:
                    y = level_start_y + i * self.node_spacing
                    node_type = random.choice(node_types)
                
                # Determine node state
                if level == 0:
                    state = NodeState.COMPLETED if level < self.current_level else NodeState.CURRENT
                elif level <= self.current_level:
                    state = NodeState.COMPLETED
                elif level == self.current_level + 1:
                    state = NodeState.AVAILABLE
                else:
                    state = NodeState.LOCKED
                
                # Create node
                node = MapNode(
                    x=x, y=y,
                    node_type=node_type,
                    state=state,
                    name=self._get_node_name(node_type, level),
                    description=self._get_node_description(node_type),
                    level=level
                )
                
                current_level_nodes.append(node)
                self.nodes.append(node)
                
                # Set current node
                if state == NodeState.CURRENT:
                    self.current_node = node
            
            # Connect to previous level
            if previous_level_nodes:
                for prev_node in previous_level_nodes:
                    # Connect to 1-2 random nodes in the next level
                    connection_count = min(len(current_level_nodes), random.randint(1, 2))
                    connections = random.sample(current_level_nodes, connection_count)
                    
                    for conn_node in connections:
                        prev_node.connections.append(conn_node)
            
            previous_level_nodes = current_level_nodes
        
        # Set camera to current node
        if self.current_node:
            self.target_camera_x = -self.current_node.x + SCREEN_CENTER[0]
            self.target_camera_y = -self.current_node.y + SCREEN_CENTER[1]
            self.camera_x = self.target_camera_x
            self.camera_y = self.target_camera_y
    
    def _get_node_name(self, node_type: NodeType, level: int) -> str:
        """Get name for a node based on type and level."""
        if node_type == NodeType.START:
            return "Entrance to the Underworld"
        elif node_type == NodeType.COMBAT:
            enemies = ["Shadow Servants", "Undead Warriors", "Desert Spirits", "Cursed Mummies"]
            return f"Battle: {random.choice(enemies)}"
        elif node_type == NodeType.ELITE:
            elites = ["Guardian Sphinx", "Anubis Lieutenant", "Cursed Pharaoh", "Divine Executioner"]
            return f"Elite: {random.choice(elites)}"
        elif node_type == NodeType.BOSS:
            if level == self.max_levels:
                return "Final Judgment: Anubis"
            bosses = ["Tomb Guardian", "Underworld Lord", "Divine Avatar"]
            return f"Boss: {random.choice(bosses)}"
        elif node_type == NodeType.TREASURE:
            return "Sacred Treasure"
        elif node_type == NodeType.EVENT:
            events = ["Divine Trial", "Ancient Wisdom", "Mystical Encounter", "Desert Oracle"]
            return random.choice(events)
        elif node_type == NodeType.REST:
            return "Temple of Rest"
        elif node_type == NodeType.SHOP:
            return "Merchant of Souls"
        
        return "Unknown"
    
    def _get_node_description(self, node_type: NodeType) -> str:
        """Get description for a node type."""
        descriptions = {
            NodeType.START: "Begin your journey through the Egyptian underworld",
            NodeType.COMBAT: "Face the denizens of the underworld in battle",
            NodeType.ELITE: "Challenging encounter with powerful enemies",
            NodeType.BOSS: "Epic battle against a divine guardian",
            NodeType.TREASURE: "Discover ancient Egyptian artifacts",
            NodeType.EVENT: "Experience mystical encounters and divine trials",
            NodeType.REST: "Restore health and prepare for battles ahead",
            NodeType.SHOP: "Trade with mysterious merchants"
        }
        return descriptions.get(node_type, "Unknown encounter")
    
    def _create_background(self):
        """Create atmospheric map background."""
        # Load map background
        map_bg = self.asset_loader.load_background('map')
        
        if map_bg:
            background = pygame.transform.smoothscale(map_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add subtle overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                alpha = int(20 + ratio * 30)
                overlay.fill((10, 5, 20), (0, y, SCREEN_WIDTH, 1))
            
            overlay.set_alpha(100)
            background.blit(overlay, (0, 0))
            return background
        else:
            # Fallback gradient
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(15 + ratio * 25)
                g = int(10 + ratio * 15)
                b = int(35 + ratio * 40)
                background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
            
            return background
    
    def _spawn_particles(self):
        """Spawn atmospheric particles."""
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH * 2),
                'y': random.randint(0, SCREEN_HEIGHT * 2),
                'size': random.randint(1, 3),
                'speed': random.randint(5, 20),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.DESERT_SAND, Colors.LAPIS_LAZULI])
            })
    
    def _create_buttons(self) -> List[HadesButton]:
        """Create UI buttons."""
        buttons = []
        
        # Back button
        back_button = HadesButton(
            50, 50, 120, 40, "BACK",
            theme_color=Colors.RED,
            hieroglyph="𓅓",
            on_click=lambda: self._handle_action(ProgressionMapAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        # Progress button
        progress_button = HadesButton(
            SCREEN_WIDTH - 170, 50, 120, 40, "PROGRESS",
            theme_color=Colors.GOLD,
            hieroglyph="𓇳",
            on_click=lambda: self._handle_action(ProgressionMapAction.VIEW_PROGRESS)
        )
        buttons.append(progress_button)
        
        return buttons
    
    def _create_node_tooltips(self):
        """Create tooltips for map nodes."""
        # This will be populated on hover
        pass
    
    def _handle_action(self, action: ProgressionMapAction, data: Any = None):
        """Handle map actions."""
        if self.on_action:
            self.on_action(action, data)
    
    def _get_node_color(self, node: MapNode) -> Tuple[int, int, int]:
        """Get color for a node based on type and state."""
        # Base colors by type
        type_colors = {
            NodeType.START: Colors.GOLD,
            NodeType.COMBAT: Colors.RED,
            NodeType.ELITE: Colors.PURPLE,
            NodeType.BOSS: Colors.DARK_RED,
            NodeType.TREASURE: Colors.GOLD,
            NodeType.EVENT: Colors.LAPIS_LAZULI,
            NodeType.REST: Colors.GREEN,
            NodeType.SHOP: Colors.DESERT_SAND
        }
        
        base_color = type_colors.get(node.node_type, Colors.GRAY)
        
        # Modify based on state
        if node.state == NodeState.LOCKED:
            return tuple(c // 3 for c in base_color)  # Very dark
        elif node.state == NodeState.COMPLETED:
            return tuple(c // 2 for c in base_color)  # Half brightness
        elif node.state == NodeState.CURRENT:
            return base_color  # Full brightness
        else:  # AVAILABLE
            return tuple(min(255, int(c * 0.8)) for c in base_color)  # Slightly dimmed
    
    def _get_node_icon(self, node_type: NodeType) -> str:
        """Get hieroglyph icon for node type."""
        icons = {
            NodeType.START: "𓇳",     # Solar disk
            NodeType.COMBAT: "⚔️",    # Swords
            NodeType.ELITE: "𓊽",     # Temple
            NodeType.BOSS: "𓁿",      # Crown
            NodeType.TREASURE: "𓋴",  # Chest
            NodeType.EVENT: "𓂀",     # Eye
            NodeType.REST: "𓊖",      # Scales
            NodeType.SHOP: "𓊪"       # Scroll
        }
        return icons.get(node_type, "?")
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update map state."""
        self.animation_time += dt
        
        # Update fade-in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
        
        # Update camera smoothly
        self.camera_x += (self.target_camera_x - self.camera_x) * dt * 3.0
        self.camera_y += (self.target_camera_y - self.camera_y) * dt * 3.0
        
        # Update particles
        for particle in self.particles:
            particle['x'] += math.sin(self.animation_time * 0.5 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt * 0.5
            
            # Wrap around
            if particle['x'] < -100:
                particle['x'] = SCREEN_WIDTH + 100
            elif particle['x'] > SCREEN_WIDTH + 100:
                particle['x'] = -100
            if particle['y'] < -100:
                particle['y'] = SCREEN_HEIGHT + 100
            elif particle['y'] > SCREEN_HEIGHT + 100:
                particle['y'] = -100
        
        # Update buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Handle node hovering
        self.hovered_node = None
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            node_rect = pygame.Rect(node_screen_pos[0] - 25, node_screen_pos[1] - 25, 50, 50)
            
            if node_rect.collidepoint(mouse_pos):
                self.hovered_node = node
                break
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(ProgressionMapAction.BACK_TO_MENU)
                elif event.key == pygame.K_SPACE:
                    if self.selected_node and self.selected_node.state == NodeState.AVAILABLE:
                        self._handle_action(ProgressionMapAction.ENTER_NODE, self.selected_node)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks
                clicked_button = False
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        clicked_button = True
                        break
                
                # Check node clicks
                if not clicked_button:
                    for node in self.nodes:
                        node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
                        node_rect = pygame.Rect(node_screen_pos[0] - 25, node_screen_pos[1] - 25, 50, 50)
                        
                        if node_rect.collidepoint(mouse_pos):
                            self.selected_node = node
                            
                            # Move camera to selected node
                            self.target_camera_x = -node.x + SCREEN_CENTER[0]
                            self.target_camera_y = -node.y + SCREEN_CENTER[1]
                            
                            # Enter node if available
                            if node.state == NodeState.AVAILABLE:
                                self._handle_action(ProgressionMapAction.ENTER_NODE, node)
                            break
            
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom (for future implementation)
                pass
    
    def render(self, surface: pygame.Surface):
        """Render the progression map."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Particles
        for particle in self.particles:
            alpha = int(80 + 40 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill(particle['color'])
            particle_surface.set_alpha(alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Map elements (with camera offset)
        self._render_connections(surface)
        self._render_nodes(surface)
        
        # UI elements
        self._render_progress_bar(surface)
        self._render_level_indicators(surface)
        
        # Buttons
        for button in self.buttons:
            button.render(surface, pygame.font.Font(None, FontSizes.BUTTON))
        
        # Node tooltip
        if self.hovered_node:
            self._render_node_tooltip(surface, self.hovered_node)
        
        # Instructions
        self._render_instructions(surface)
        
        # Fade-in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
    
    def _render_connections(self, surface: pygame.Surface):
        """Render connections between nodes."""
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            
            for connected_node in node.connections:
                connected_screen_pos = (connected_node.x + self.camera_x, connected_node.y + self.camera_y)
                
                # Only render visible connections
                if (-100 < node_screen_pos[0] < SCREEN_WIDTH + 100 and 
                    -100 < connected_screen_pos[0] < SCREEN_WIDTH + 100):
                    
                    # Connection color based on state
                    if connected_node.state in [NodeState.COMPLETED, NodeState.CURRENT]:
                        line_color = Colors.GOLD
                        line_width = 3
                    elif connected_node.state == NodeState.AVAILABLE:
                        line_color = Colors.DESERT_SAND
                        line_width = 2
                    else:
                        line_color = Colors.GRAY
                        line_width = 1
                    
                    pygame.draw.line(surface, line_color, node_screen_pos, connected_screen_pos, line_width)
    
    def _render_nodes(self, surface: pygame.Surface):
        """Render map nodes."""
        font = pygame.font.Font(None, 32)
        
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            
            # Only render visible nodes
            if (-100 < node_screen_pos[0] < SCREEN_WIDTH + 100 and 
                -100 < node_screen_pos[1] < SCREEN_HEIGHT + 100):
                
                node_color = self._get_node_color(node)
                node_size = 25
                
                # Hover effect
                if node == self.hovered_node:
                    node_size = 30
                    # Glow effect
                    glow_surface = pygame.Surface((node_size * 3, node_size * 3), pygame.SRCALPHA)
                    glow_surface.fill(node_color)
                    glow_surface.set_alpha(60)
                    surface.blit(glow_surface, (node_screen_pos[0] - node_size * 1.5, node_screen_pos[1] - node_size * 1.5))
                
                # Selection highlight
                if node == self.selected_node:
                    pygame.draw.circle(surface, Colors.GOLD, node_screen_pos, node_size + 5, 3)
                
                # Node circle
                pygame.draw.circle(surface, node_color, node_screen_pos, node_size)
                pygame.draw.circle(surface, Colors.BLACK, node_screen_pos, node_size, 2)
                
                # Node icon
                icon = self._get_node_icon(node.node_type)
                icon_surface = font.render(icon, True, Colors.WHITE)
                icon_rect = icon_surface.get_rect(center=node_screen_pos)
                surface.blit(icon_surface, icon_rect)
                
                # Current node pulse
                if node.state == NodeState.CURRENT:
                    pulse_alpha = int(100 + 80 * abs(math.sin(self.animation_time * 3)))
                    pulse_surface = pygame.Surface((node_size * 2, node_size * 2), pygame.SRCALPHA)
                    pulse_surface.fill(Colors.GOLD)
                    pulse_surface.set_alpha(pulse_alpha)
                    surface.blit(pulse_surface, (node_screen_pos[0] - node_size, node_screen_pos[1] - node_size))
    
    def _render_progress_bar(self, surface: pygame.Surface):
        """Render progress through the underworld."""
        progress_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 20)
        
        # Background
        pygame.draw.rect(surface, Colors.BLACK, progress_rect)
        pygame.draw.rect(surface, Colors.GOLD, progress_rect, 2)
        
        # Progress fill
        progress_ratio = self.current_level / self.max_levels
        fill_width = int(progress_ratio * (progress_rect.width - 4))
        fill_rect = pygame.Rect(progress_rect.x + 2, progress_rect.y + 2, fill_width, progress_rect.height - 4)
        pygame.draw.rect(surface, Colors.GOLD, fill_rect)
        
        # Progress text
        responsive_typography.render_text(
            f"Underworld Progress: {self.current_level}/{self.max_levels}",
            TextStyle.CARD_TEXT, surface,
            (progress_rect.centerx, progress_rect.y - 25),
            center=True, custom_color=Colors.PAPYRUS
        )
    
    def _render_level_indicators(self, surface: pygame.Surface):
        """Render level indicators on the sides."""
        # Left side - current stats
        stats_text = [
            "CURRENT JOURNEY",
            f"Level: {self.current_level + 1}",
            f"Nodes Completed: {len([n for n in self.nodes if n.state == NodeState.COMPLETED])}",
            f"Remaining: {len([n for n in self.nodes if n.state in [NodeState.AVAILABLE, NodeState.LOCKED]])}"
        ]
        
        y = 200
        for text in stats_text:
            color = Colors.GOLD if "CURRENT" in text else Colors.PAPYRUS
            responsive_typography.render_text(
                text, TextStyle.CARD_TEXT, surface, (50, y), custom_color=color
            )
            y += 30
    
    def _render_node_tooltip(self, surface: pygame.Surface, node: MapNode):
        """Render tooltip for hovered node."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Tooltip content
        lines = [
            node.name,
            f"Type: {node.node_type.name.title()}",
            node.description
        ]
        
        if node.state == NodeState.LOCKED:
            lines.append("🔒 Complete previous nodes to unlock")
        elif node.state == NodeState.AVAILABLE:
            lines.append("⚡ Click to enter")
        elif node.state == NodeState.COMPLETED:
            lines.append("✅ Completed")
        
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
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > SCREEN_WIDTH - 20:
            tooltip_x = mouse_pos[0] - tooltip_width - 20
        if tooltip_y < 20:
            tooltip_y = 20
        elif tooltip_y + tooltip_height > SCREEN_HEIGHT - 20:
            tooltip_y = SCREEN_HEIGHT - tooltip_height - 20
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        
        # Draw background
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        tooltip_surface.fill(Colors.BACKGROUND_SECONDARY)
        tooltip_surface.set_alpha(240)
        pygame.draw.rect(tooltip_surface, self._get_node_color(node), (0, 0, tooltip_width, tooltip_height), 2)
        surface.blit(tooltip_surface, tooltip_rect)
        
        # Draw text
        y_offset = 10
        for i, line in enumerate(lines):
            color = self._get_node_color(node) if i == 0 else Colors.PAPYRUS
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (tooltip_x + 10, tooltip_y + y_offset))
            y_offset += font.size(line)[1] + 5
    
    def _render_instructions(self, surface: pygame.Surface):
        """Render control instructions."""
        instructions = [
            "Click nodes to select • SPACE: Enter selected node",
            "Mouse: Navigate map • ESC: Back to menu",
            "Follow the path through the Egyptian underworld!"
        ]
        
        y = SCREEN_HEIGHT - 70
        for instruction in instructions:
            responsive_typography.render_text(
                instruction, TextStyle.TOOLTIP, surface,
                (SCREEN_CENTER[0], y), center=True, custom_color=Colors.DESERT_SAND
            )
            y += 20
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.animation_time = 0.0
        
        # Start map music
        audio_manager.play_music(AudioTrack.AMBIENT, fade_in=2.0)