"""
Enhanced Progression Map Screen - Redesigned for better UX and visual clarity
Slay the Spire style Egyptian journey with professional design and responsive layout.
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
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout
from ..components.responsive_typography import responsive_typography, TextStyle
from ..responsive.scaling_manager import scaling_manager

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
    size: int = 80  # Larger default size

    def __post_init__(self):
        if self.connections is None:
            self.connections = []

class ProgressionMapAction(Enum):
    """Map screen actions."""
    BACK_TO_MENU = auto()
    ENTER_NODE = auto()
    VIEW_PROGRESS = auto()

class EnhancedProgressionMap:
    """
    Professional progression map with enhanced UX, visual design, and responsive layout.
    Features proper node sizing, clear visual hierarchy, and ultrawide optimization.
    """
    
    def __init__(self, on_action: Optional[Callable[[ProgressionMapAction, Any], None]] = None):
        """Initialize the enhanced progression map."""
        self.on_action = on_action
        self.asset_loader = get_asset_loader()
        
        # Animation and visual state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.target_camera_x = 0.0
        self.target_camera_y = 0.0
        self.zoom_level = 1.0
        
        # Map configuration using new specs
        self.current_level = 0
        self.max_levels = 15
        self.nodes_per_level = 3
        
        # Responsive spacing based on enhanced layout
        self.node_size = 120  # Even larger, highly clickable nodes  
        self.node_spacing_x = 200  # Better horizontal spacing
        self.node_spacing_y = 150  # Better vertical spacing
        self.hover_node = None  # Track hovered node for better feedback
        
        # Enhanced color scheme
        self.node_colors = {
            NodeType.START: Colors.GOLD,
            NodeType.COMBAT: (139, 69, 19),     # Brown
            NodeType.ELITE: (255, 69, 0),       # Red-Orange  
            NodeType.BOSS: (139, 0, 0),         # Dark Red
            NodeType.TREASURE: (255, 215, 0),   # Gold
            NodeType.EVENT: (147, 112, 219),    # Purple
            NodeType.REST: (0, 206, 209),       # Turquoise
            NodeType.SHOP: (50, 205, 50)        # Green
        }
        
        # Side panel system (define early)
        self.left_panel_width = 300
        self.right_panel_width = 300
        
        # Map state
        self.nodes = []
        self.current_node = None
        self.selected_node = None
        self.hovered_node = None
        
        # Generate enhanced map
        self._generate_enhanced_map()
        
        # Visual elements
        self.background_surface = self._create_enhanced_background()
        self.particles = []
        self._spawn_enhanced_particles()
        
        # UI elements with proper scaling
        self.buttons = self._create_enhanced_buttons()
        
        # Start transition
        smooth_transitions.fade_in_element("enhanced_progression_map", Timing.FADE_DURATION)
        
        print("Enhanced Progression Map initialized - Professional Egyptian journey begins!")
    
    def _generate_enhanced_map(self):
        """Generate the map with improved layout and responsive positioning."""
        # Calculate available map area (excluding side panels)
        map_area_width = SCREEN_WIDTH - (self.left_panel_width + self.right_panel_width)
        map_area_height = SCREEN_HEIGHT - 200  # Leave space for top/bottom UI
        
        # Calculate map dimensions
        total_width = self.max_levels * self.node_spacing_x
        total_height = (self.nodes_per_level - 1) * self.node_spacing_y
        
        # Center the map in available area
        map_start_x = self.left_panel_width + (map_area_width - total_width) // 2
        map_start_y = 100 + (map_area_height - total_height) // 2
        
        # Generate nodes with enhanced logic
        previous_level_nodes = []
        
        for level in range(self.max_levels + 1):
            current_level_nodes = []
            
            # Determine nodes for this level
            if level == 0:
                node_types = [NodeType.START]
                nodes_count = 1
            elif level == self.max_levels:
                node_types = [NodeType.BOSS]  # Final boss
                nodes_count = 1
            elif level % 5 == 0 and level > 0:
                node_types = [NodeType.BOSS]  # Boss every 5 levels
                nodes_count = 1
            elif level % 3 == 0 and level > 0:
                # Elite/special levels
                node_types = [NodeType.ELITE, NodeType.TREASURE, NodeType.REST]
                nodes_count = min(3, self.nodes_per_level)
            else:
                # Regular levels with variety
                node_types = [NodeType.COMBAT, NodeType.EVENT, NodeType.TREASURE, 
                             NodeType.REST, NodeType.SHOP]
                nodes_count = self.nodes_per_level
            
            # Create nodes for this level
            for i in range(nodes_count):
                x = map_start_x + level * self.node_spacing_x
                
                if nodes_count == 1:
                    # Single node (boss or start) - center vertically
                    y = map_start_y + total_height // 2
                    node_type = node_types[0]
                else:
                    # Multiple nodes - distribute vertically
                    y_offset = i * self.node_spacing_y
                    y = map_start_y + y_offset
                    node_type = random.choice(node_types)
                
                # Determine state
                if level <= self.current_level:
                    if level == self.current_level:
                        state = NodeState.CURRENT
                    else:
                        state = NodeState.COMPLETED
                elif level == self.current_level + 1:
                    state = NodeState.AVAILABLE
                else:
                    state = NodeState.LOCKED
                
                # Create enhanced node
                node = MapNode(
                    x=x, y=y,
                    node_type=node_type,
                    state=state,
                    name=self._get_enhanced_node_name(node_type, level),
                    description=self._get_enhanced_node_description(node_type),
                    level=level,
                    size=self.node_size
                )
                
                current_level_nodes.append(node)
                self.nodes.append(node)
                
                if state == NodeState.CURRENT:
                    self.current_node = node
            
            # Connect to previous level with better logic
            if previous_level_nodes:
                for prev_node in previous_level_nodes:
                    # Smart connection logic
                    if len(current_level_nodes) == 1:
                        # Connect all to single node (boss)
                        prev_node.connections.append(current_level_nodes[0])
                    else:
                        # Connect to 1-2 nearby nodes
                        connection_count = random.randint(1, min(2, len(current_level_nodes)))
                        connections = random.sample(current_level_nodes, connection_count)
                        prev_node.connections.extend(connections)
            
            previous_level_nodes = current_level_nodes
        
        # Set camera to current node with smooth positioning
        if self.current_node:
            self.target_camera_x = -self.current_node.x + SCREEN_CENTER[0]
            self.target_camera_y = -self.current_node.y + SCREEN_CENTER[1]
            self.camera_x = self.target_camera_x
            self.camera_y = self.target_camera_y
    
    def _get_enhanced_node_name(self, node_type: NodeType, level: int) -> str:
        """Get enhanced name for a node with Egyptian theming."""
        if node_type == NodeType.START:
            return "Gateway to the Duat"
        elif node_type == NodeType.COMBAT:
            enemies = [
                "Shadowy Ushabti", "Canopic Guardians", "Desert Wraiths", 
                "Cursed Scribes", "Mummified Warriors", "Sand Demons"
            ]
            return f"Battle: {random.choice(enemies)}"
        elif node_type == NodeType.ELITE:
            elites = [
                "Guardian Sphinx", "Anubis Champion", "Pharaoh's Wrath",
                "Divine Sentinel", "Temple Keeper", "Sacred Protector"
            ]
            return f"Elite Trial: {random.choice(elites)}"
        elif node_type == NodeType.BOSS:
            if level == self.max_levels:
                return "Final Judgment: Great Devourer"
            bosses = [
                "Tomb Lord Khenti-Amentiu", "Divine Avatar of Set", 
                "Guardian of the Scales", "Master of the Underworld"
            ]
            return f"Divine Challenge: {random.choice(bosses)}"
        elif node_type == NodeType.TREASURE:
            return "Sacred Vault"
        elif node_type == NodeType.EVENT:
            events = [
                "Trial of Ma'at", "Whispers of Thoth", "Vision of Isis",
                "Test of Horus", "Blessing of Ptah", "Oracle of Hathor"
            ]
            return random.choice(events)
        elif node_type == NodeType.REST:
            return "Temple of Restoration"
        elif node_type == NodeType.SHOP:
            return "Merchant of the Afterlife"
        
        return "Unknown Realm"
    
    def _get_enhanced_node_description(self, node_type: NodeType) -> str:
        """Get enhanced description with more detail."""
        descriptions = {
            NodeType.START: "Begin your perilous journey through the Egyptian underworld",
            NodeType.COMBAT: "Face the restless spirits and guardians of the dead",
            NodeType.ELITE: "Confront powerful divine champions in intense trials",
            NodeType.BOSS: "Epic confrontation with ancient Egyptian deities",
            NodeType.TREASURE: "Discover powerful artifacts and divine relics",
            NodeType.EVENT: "Experience mystical encounters that shape your destiny",
            NodeType.REST: "Find sanctuary and restore your strength for trials ahead",
            NodeType.SHOP: "Trade with otherworldly merchants for rare items"
        }
        return descriptions.get(node_type, "A mysterious encounter awaits")
    
    def _create_enhanced_background(self):
        """Create professional Egyptian-themed background using asset pipeline."""
        # SPRINT 2: Use smart asset loader for beautiful high-quality assets
        from ...assets.smart_asset_loader import smart_asset_loader
        
        # Load the professional map background using asset pipeline
        map_bg = smart_asset_loader.get_background('map')
        if not map_bg:
            # Try alternative asset names for map backgrounds
            map_bg = smart_asset_loader.load_asset('bg_map_4k')
        if not map_bg:
            map_bg = smart_asset_loader.load_asset('map_background')
        
        if map_bg:
            # Scale the high-quality background to screen size with smooth scaling
            background = pygame.transform.smoothscale(map_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add minimal overlay to preserve the beautiful artwork
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 15))  # Very light darkening to preserve art quality
            background.blit(overlay, (0, 0))
            
            return background
        
        # Enhanced fallback: Create professional Egyptian desert map
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Rich Egyptian desert gradient - from papyrus to deep desert night
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            # Papyrus to deep desert gradient with Egyptian warmth
            r = int(139 - ratio * 80)  # Warm papyrus to deep brown
            g = int(116 - ratio * 70)  # Golden to darker
            b = int(78 - ratio * 50)   # Warm brown to deep
            background.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
        
        # Add Egyptian papyrus texture pattern
        pattern_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Create realistic papyrus fiber pattern
        for i in range(0, SCREEN_WIDTH, 20):
            for j in range(0, SCREEN_HEIGHT, 20):
                # Vertical fibers
                if random.random() < 0.3:
                    fiber_height = random.randint(30, 80)
                    pygame.draw.line(pattern_surface, (160, 140, 100, 40), 
                                   (i, j), (i, j + fiber_height), 2)
                
                # Horizontal fibers  
                if random.random() < 0.2:
                    fiber_width = random.randint(40, 100)
                    pygame.draw.line(pattern_surface, (180, 160, 120, 30), 
                                   (i, j), (i + fiber_width, j), 1)
        
        # Add ancient wear marks and stains
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(20, 80)
            alpha = random.randint(10, 25)
            stain_color = (101, 67, 33, alpha)  # Brown stains
            pygame.draw.circle(pattern_surface, stain_color, (x, y), size)
        
        background.blit(pattern_surface, (0, 0))
        
        # Add subtle Egyptian hieroglyph watermarks
        hieroglyph_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        hieroglyphs = ["𓀀", "𓀁", "𓀂", "𓀃", "𓀄", "𓀅", "𓁹", "𓂀", "𓃭", "𓃰"]
        
        for _ in range(15):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            hieroglyph = random.choice(hieroglyphs)
            
            try:
                font = pygame.font.Font(None, random.randint(60, 120))
                text = font.render(hieroglyph, True, (139, 116, 78, 40))
                hieroglyph_surface.blit(text, (x, y))
            except:
                # Fallback to simple geometric patterns if hieroglyphs fail
                pygame.draw.circle(hieroglyph_surface, (139, 116, 78, 30), (x, y), 20, 3)
        
        background.blit(hieroglyph_surface, (0, 0))
        return background
    
    def _spawn_enhanced_particles(self):
        """Spawn atmospheric particles with Egyptian theming."""
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH * 2),
                'y': random.randint(0, SCREEN_HEIGHT * 2),
                'size': random.randint(2, 6),
                'speed': random.randint(8, 25),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([Colors.GOLD, Colors.DESERT_SAND, (255, 215, 0)]),
                'alpha': random.randint(60, 120)
            })
    
    def _create_enhanced_buttons(self) -> List[HadesButton]:
        """Create enhanced UI buttons with proper scaling."""
        buttons = []
        
        # Get proper button size from scaling manager
        button_width, button_height = scaling_manager.get_component_size('button_default')
        
        # Back button (top-left)
        back_button = HadesButton(
            50, 50, button_width, button_height, "BACK TO MENU",
            theme_color=Colors.RED,
            hieroglyph="◄",
            on_click=lambda: self._handle_action(ProgressionMapAction.BACK_TO_MENU)
        )
        buttons.append(back_button)
        
        # Progress button (top-right)
        progress_button = HadesButton(
            SCREEN_WIDTH - button_width - 50, 50, button_width, button_height, "VIEW PROGRESS",
            theme_color=Colors.GOLD,
            hieroglyph="⚡",
            on_click=lambda: self._handle_action(ProgressionMapAction.VIEW_PROGRESS)
        )
        buttons.append(progress_button)
        
        return buttons
    
    def _handle_action(self, action: ProgressionMapAction, data: Any = None):
        """Handle map actions with proper callback."""
        if self.on_action:
            self.on_action(action, data)
    
    def _get_node_color(self, node: MapNode) -> Tuple[int, int, int]:
        """Get enhanced color for a node based on type and state."""
        base_color = self.node_colors.get(node.node_type, Colors.GRAY)
        
        # State-based modifications
        if node.state == NodeState.LOCKED:
            return tuple(c // 4 for c in base_color)  # Very dark
        elif node.state == NodeState.COMPLETED:
            return tuple(c // 2 for c in base_color)  # Half brightness
        elif node.state == NodeState.CURRENT:
            return base_color  # Full brightness with pulse
        else:  # AVAILABLE
            return tuple(min(255, int(c * 0.9)) for c in base_color)  # Slightly dimmed
    
    def _get_node_icon(self, node_type: NodeType) -> str:
        """Get icon for node type."""
        icons = {
            NodeType.START: "◉",      # Start point
            NodeType.COMBAT: "⚔",     # Combat
            NodeType.ELITE: "★",      # Elite
            NodeType.BOSS: "♛",       # Boss
            NodeType.TREASURE: "♦",   # Treasure
            NodeType.EVENT: "?",      # Event
            NodeType.REST: "♥",       # Rest
            NodeType.SHOP: "$"        # Shop
        }
        return icons.get(node_type, "?")
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Update enhanced map with smooth animations and responsive input."""
        self.animation_time += dt
        
        # Smooth fade-in
        if self.fade_in_progress < 1.0:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.5)
        
        # Smooth camera movement
        camera_speed = 4.0 * dt
        self.camera_x += (self.target_camera_x - self.camera_x) * camera_speed
        self.camera_y += (self.target_camera_y - self.camera_y) * camera_speed
        
        # Enhanced particle system
        for particle in self.particles:
            particle['x'] += math.sin(self.animation_time * 0.3 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.2 + particle['phase']) * particle['speed'] * dt * 0.3
            
            # Wrap particles around screen
            if particle['x'] < -50:
                particle['x'] = SCREEN_WIDTH + 50
            elif particle['x'] > SCREEN_WIDTH + 50:
                particle['x'] = -50
            if particle['y'] < -50:
                particle['y'] = SCREEN_HEIGHT + 50
            elif particle['y'] > SCREEN_HEIGHT + 50:
                particle['y'] = -50
        
        # Update buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        # Enhanced node hovering with larger hit areas
        self.hovered_node = None
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            # Much larger hit area for excellent usability
            hit_radius = node.size // 2 + 25  # Generous click area
            distance = math.sqrt((mouse_pos[0] - node_screen_pos[0])**2 + 
                               (mouse_pos[1] - node_screen_pos[1])**2)
            
            if distance <= hit_radius:
                self.hovered_node = node
                break
        
        # Handle input events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_action(ProgressionMapAction.BACK_TO_MENU)
                elif event.key == pygame.K_SPACE:
                    if self.selected_node and self.selected_node.state == NodeState.AVAILABLE:
                        self._handle_action(ProgressionMapAction.ENTER_NODE, self.selected_node)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check button clicks first
                button_clicked = False
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button_clicked = True
                        break
                
                # Handle node clicks
                if not button_clicked and self.hovered_node:
                    self.selected_node = self.hovered_node
                    
                    # Smooth camera transition to selected node
                    self.target_camera_x = -self.hovered_node.x + SCREEN_CENTER[0]
                    self.target_camera_y = -self.hovered_node.y + SCREEN_CENTER[1]
                    
                    # Enter available nodes immediately
                    if self.hovered_node.state == NodeState.AVAILABLE:
                        self._handle_action(ProgressionMapAction.ENTER_NODE, self.hovered_node)
    
    def render(self, surface: pygame.Surface):
        """Render the enhanced progression map with professional visuals."""
        # Background
        surface.blit(self.background_surface, (0, 0))
        
        # Enhanced particles
        for particle in self.particles:
            alpha = int(particle['alpha'] + 60 * abs(math.sin(self.animation_time + particle['phase'])))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            # Fix: Use RGB color for fill, then set alpha separately
            particle_surface.fill(particle['color'])
            particle_surface.set_alpha(alpha)
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Render side panels
        self._render_side_panels(surface)
        
        # Map elements with camera transform
        self._render_enhanced_connections(surface)
        self._render_enhanced_nodes(surface)
        
        # UI overlays
        self._render_enhanced_progress(surface)
        
        # Buttons
        for button in self.buttons:
            button.render(surface, scaling_manager.get_font('button'))
        
        # Enhanced tooltip
        if self.hovered_node:
            self._render_enhanced_tooltip(surface, self.hovered_node)
        
        # Instructions
        self._render_enhanced_instructions(surface)
        
        # Fade-in effect
        if self.fade_in_progress < 1.0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_alpha = int(255 * (1.0 - self.fade_in_progress))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            surface.blit(fade_surface, (0, 0))
    
    def _render_side_panels(self, surface: pygame.Surface):
        """Render professional Egyptian-themed side panels using asset pipeline."""
        from ...assets.smart_asset_loader import smart_asset_loader
        
        # SPRINT 2: Load actual panel assets instead of manual rendering
        left_panel = smart_asset_loader.load_asset('ui_panel_left', (self.left_panel_width, SCREEN_HEIGHT))
        if not left_panel:
            left_panel = smart_asset_loader.load_asset('panel_papyrus', (self.left_panel_width, SCREEN_HEIGHT))
        if not left_panel:
            left_panel = smart_asset_loader.load_asset('ui_side_panel', (self.left_panel_width, SCREEN_HEIGHT))
        
        if left_panel:
            surface.blit(left_panel, (0, 0))
        else:
            # Fallback to simple semi-transparent panel
            left_panel_surf = pygame.Surface((self.left_panel_width, SCREEN_HEIGHT), pygame.SRCALPHA)
            left_panel_surf.fill((40, 30, 20, 180))  # Dark Egyptian brown with transparency
            surface.blit(left_panel_surf, (0, 0))
        
        # Right panel using asset pipeline
        right_panel = smart_asset_loader.load_asset('ui_panel_right', (self.right_panel_width, SCREEN_HEIGHT))
        if not right_panel:
            right_panel = smart_asset_loader.load_asset('panel_papyrus', (self.right_panel_width, SCREEN_HEIGHT))
        if not right_panel:
            right_panel = smart_asset_loader.load_asset('ui_side_panel', (self.right_panel_width, SCREEN_HEIGHT))
        
        if right_panel:
            surface.blit(right_panel, (SCREEN_WIDTH - self.right_panel_width, 0))
        else:
            # Fallback to simple semi-transparent panel
            right_panel_surf = pygame.Surface((self.right_panel_width, SCREEN_HEIGHT), pygame.SRCALPHA)
            right_panel_surf.fill((40, 30, 20, 180))  # Dark Egyptian brown with transparency
            surface.blit(right_panel_surf, (SCREEN_WIDTH - self.right_panel_width, 0))
    
    def _render_egyptian_panel(self, surface: pygame.Surface, x: int, y: int, 
                              width: int, height: int, side: str):
        """Render a professional Egyptian papyrus-style panel."""
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Create papyrus-like background gradient
        for i in range(height):
            ratio = i / height
            # Warm papyrus gradient
            r = int(210 - ratio * 40)  # Light papyrus to darker
            g = int(180 - ratio * 35)  # Warm golden
            b = int(140 - ratio * 30)  # Aged brown
            alpha = 220
            panel_surface.fill((r, g, b, alpha), (0, i, width, 1))
        
        # Add papyrus texture
        for i in range(0, width, 15):
            for j in range(0, height, 15):
                if random.random() < 0.3:
                    # Papyrus fibers
                    fiber_len = random.randint(20, 40)
                    if random.random() < 0.5:
                        # Vertical fiber
                        pygame.draw.line(panel_surface, (190, 170, 130, 80), 
                                       (i, j), (i, j + fiber_len), 1)
                    else:
                        # Horizontal fiber
                        pygame.draw.line(panel_surface, (190, 170, 130, 80), 
                                       (i, j), (i + fiber_len, j), 1)
        
        # Add Egyptian border decoration
        border_color = Colors.GOLD
        
        # Ornate border with Egyptian motifs
        if side == "left":
            # Left border (inner edge)
            border_x = width - 5
            pygame.draw.line(panel_surface, border_color, (border_x, 20), (border_x, height - 20), 3)
            
            # Egyptian decorative elements
            for i in range(50, height - 50, 80):
                # Ankh symbols along the border
                self._draw_mini_ankh(panel_surface, border_x - 15, i, 10)
                
        else:  # right panel
            # Right border (inner edge)
            border_x = 5
            pygame.draw.line(panel_surface, border_color, (border_x, 20), (border_x, height - 20), 3)
            
            # Egyptian decorative elements
            for i in range(50, height - 50, 80):
                # Eye of Horus symbols along the border
                self._draw_mini_eye_of_horus(panel_surface, border_x + 15, i, 8)
        
        # Top and bottom borders with geometric patterns
        pygame.draw.line(panel_surface, border_color, (10, 10), (width - 10, 10), 2)
        pygame.draw.line(panel_surface, border_color, (10, height - 10), (width - 10, height - 10), 2)
        
        # Corner decorations
        for corner_x, corner_y in [(15, 15), (width - 15, 15), (15, height - 15), (width - 15, height - 15)]:
            pygame.draw.circle(panel_surface, border_color, (corner_x, corner_y), 8, 2)
            pygame.draw.circle(panel_surface, (160, 140, 100), (corner_x, corner_y), 4)
        
        surface.blit(panel_surface, (x, y))
    
    def _draw_mini_ankh(self, surface: pygame.Surface, x: int, y: int, size: int):
        """Draw a small ankh symbol for decoration."""
        # Cross part
        pygame.draw.rect(surface, Colors.GOLD, (x - 1, y - size//2, 2, size))
        pygame.draw.rect(surface, Colors.GOLD, (x - size//3, y + size//4, size//3 * 2, 2))
        # Loop part
        pygame.draw.circle(surface, Colors.GOLD, (x, y - size//3), size//4, 2)
    
    def _draw_mini_eye_of_horus(self, surface: pygame.Surface, x: int, y: int, size: int):
        """Draw a small Eye of Horus for decoration."""
        # Eye outline (simplified)
        eye_points = [(x - size, y), (x - size//2, y - size//2), (x + size//2, y - size//3), 
                      (x + size, y), (x + size//2, y + size//2), (x - size//2, y + size//3)]
        if len(eye_points) >= 3:
            pygame.draw.polygon(surface, Colors.GOLD, eye_points, 1)
        # Pupil
        pygame.draw.circle(surface, Colors.GOLD, (x, y), size//4)
        
        # Left panel content - Journey Stats
        y = 100
        scaling_manager.draw_scaled_text(
            surface, "JOURNEY PROGRESS", (25, y), 'subtitle', Colors.GOLD, center=False
        )
        
        y += 50
        stats = [
            f"Current Level: {self.current_level + 1}/{self.max_levels + 1}",
            f"Nodes Completed: {len([n for n in self.nodes if n.state == NodeState.COMPLETED])}",
            f"Available Paths: {len([n for n in self.nodes if n.state == NodeState.AVAILABLE])}",
            f"Remaining Journey: {len([n for n in self.nodes if n.state == NodeState.LOCKED])}"
        ]
        
        for stat in stats:
            scaling_manager.draw_scaled_text(
                surface, stat, (25, y), 'body', Colors.PAPYRUS, center=False
            )
            y += 30
        
        # Right panel content - Map Legend
        y = 100
        scaling_manager.draw_scaled_text(
            surface, "MAP LEGEND", (SCREEN_WIDTH - self.right_panel_width + 25, y), 
            'subtitle', Colors.GOLD, center=False
        )
        
        y += 50
        legend_items = [
            ("⚔ Combat", "Battle against underworld enemies"),
            ("★ Elite", "Challenging elite encounters"),
            ("♛ Boss", "Epic divine confrontations"),
            ("♦ Treasure", "Discover ancient artifacts"),
            ("? Event", "Mystical encounters and trials"),
            ("♥ Rest", "Restore health and prepare"),
            ("$ Shop", "Trade with otherworldly merchants")
        ]
        
        for icon_text, description in legend_items:
            scaling_manager.draw_scaled_text(
                surface, icon_text, (SCREEN_WIDTH - self.right_panel_width + 25, y),
                'card_text', Colors.GOLD, center=False
            )
            y += 25
            scaling_manager.draw_scaled_text(
                surface, description, (SCREEN_WIDTH - self.right_panel_width + 45, y),
                'small', Colors.PAPYRUS, center=False
            )
            y += 35
    
    def _render_enhanced_connections(self, surface: pygame.Surface):
        """Render enhanced path connections between nodes."""
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            
            for connected_node in node.connections:
                connected_screen_pos = (connected_node.x + self.camera_x, 
                                      connected_node.y + self.camera_y)
                
                # Only render visible connections
                if (-100 < node_screen_pos[0] < SCREEN_WIDTH + 100 and 
                    -100 < connected_screen_pos[0] < SCREEN_WIDTH + 100):
                    
                    # Enhanced line styling based on state
                    if connected_node.state == NodeState.COMPLETED:
                        line_color = Colors.GOLD
                        line_width = 4
                    elif connected_node.state == NodeState.AVAILABLE:
                        line_color = Colors.DESERT_SAND
                        line_width = 3
                    elif connected_node.state == NodeState.CURRENT:
                        line_color = Colors.GOLD
                        line_width = 5
                    else:
                        line_color = (80, 80, 80)
                        line_width = 2
                    
                    # Draw path line
                    pygame.draw.line(surface, line_color, node_screen_pos, 
                                   connected_screen_pos, line_width)
    
    def _render_enhanced_nodes(self, surface: pygame.Surface):
        """Render enhanced map nodes with better visibility and feedback."""
        font = scaling_manager.get_font('card_text')
        
        for node in self.nodes:
            node_screen_pos = (node.x + self.camera_x, node.y + self.camera_y)
            
            # Only render visible nodes
            if (-100 < node_screen_pos[0] < SCREEN_WIDTH + 100 and 
                -100 < node_screen_pos[1] < SCREEN_HEIGHT + 100):
                
                node_color = self._get_node_color(node)
                node_radius = node.size // 2
                
                # Enhanced hover effect
                if node == self.hovered_node:
                    node_radius = int(node_radius * 1.2)
                    # Glow effect
                    glow_surface = pygame.Surface((node_radius * 4, node_radius * 4), pygame.SRCALPHA)
                    # Fix: Use RGB color for fill, then set alpha separately
                    glow_surface.fill(node_color)
                    glow_surface.set_alpha(80)
                    surface.blit(glow_surface, (node_screen_pos[0] - node_radius * 2, 
                                              node_screen_pos[1] - node_radius * 2))
                
                # Selection highlight
                if node == self.selected_node:
                    pygame.draw.circle(surface, Colors.GOLD, node_screen_pos, node_radius + 8, 4)
                
                # Available node pulse - much more prominent
                if node.state == NodeState.AVAILABLE:
                    pulse_radius = node_radius + int(20 * abs(math.sin(self.animation_time * 2)))
                    pulse_surface = pygame.Surface((pulse_radius * 2, pulse_radius * 2), pygame.SRCALPHA)
                    pulse_surface.fill((*Colors.GREEN, 80))  # Green pulse for clear availability
                    surface.blit(pulse_surface, (node_screen_pos[0] - pulse_radius, 
                                               node_screen_pos[1] - pulse_radius))
                    
                    # Add rotating border for extra visibility
                    border_thickness = 4
                    pygame.draw.circle(surface, Colors.GREEN, node_screen_pos, 
                                     node_radius + 5, border_thickness)
                
                # Current node special effect
                if node.state == NodeState.CURRENT:
                    pulse_alpha = int(120 + 100 * abs(math.sin(self.animation_time * 4)))
                    pulse_surface = pygame.Surface((node_radius * 3, node_radius * 3), pygame.SRCALPHA)
                    pulse_surface.fill((*Colors.GOLD, pulse_alpha))
                    surface.blit(pulse_surface, (node_screen_pos[0] - node_radius * 1.5, 
                                               node_screen_pos[1] - node_radius * 1.5))
                
                # PROFESSIONAL EGYPTIAN NODE RENDERING
                self._render_professional_node(surface, node, node_screen_pos, node_radius, node_color)
    
    def _render_professional_node(self, surface: pygame.Surface, node: MapNode, 
                                pos: Tuple[int, int], radius: int, base_color: Tuple[int, int, int]):
        """Render a professional Egyptian-themed map node using asset pipeline."""
        from ...assets.smart_asset_loader import smart_asset_loader
        
        # SPRINT 2: Load actual Egyptian node icons from asset pipeline
        node_icon_map = {
            NodeType.START: 'node_ankh',
            NodeType.BOSS: 'node_pyramid', 
            NodeType.ELITE: 'node_scarab',
            NodeType.TREASURE: 'node_treasure',
            NodeType.EVENT: 'node_eye_horus',
            NodeType.REST: 'node_lotus',
            NodeType.SHOP: 'node_scales',
            NodeType.COMBAT: 'node_combat'
        }
        
        icon_name = node_icon_map.get(node.node_type, 'node_combat')
        node_size = radius * 2
        
        # Try loading specific node icon
        node_icon = smart_asset_loader.load_asset(icon_name, (node_size, node_size))
        if not node_icon:
            # Try generic map node assets
            node_icon = smart_asset_loader.load_asset('map_node', (node_size, node_size))
        if not node_icon:
            # Try UI icon fallback
            node_icon = smart_asset_loader.load_asset(f'icon_{node.node_type.name.lower()}', (node_size, node_size))
        
        if node_icon:
            # Apply color tinting based on node state
            if node.state == NodeState.LOCKED:
                # Darken locked nodes
                tinted_icon = node_icon.copy()
                dark_overlay = pygame.Surface((node_size, node_size), pygame.SRCALPHA)
                dark_overlay.fill((0, 0, 0, 180))
                tinted_icon.blit(dark_overlay, (0, 0))
                node_icon = tinted_icon
            elif node.state == NodeState.CURRENT:
                # Add glow effect for current node
                glow_icon = node_icon.copy()
                glow_overlay = pygame.Surface((node_size, node_size), pygame.SRCALPHA)
                glow_overlay.fill((*Colors.GOLD, 80))
                glow_icon.blit(glow_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
                node_icon = glow_icon
            
            surface.blit(node_icon, (pos[0] - node_size//2, pos[1] - node_size//2))
        else:
            # Fallback to simple colored circle with modern text icon
            pygame.draw.circle(surface, base_color, pos, radius)
            pygame.draw.circle(surface, Colors.GOLD, pos, radius, 3)
            
            # Simple text icon fallback
            font = pygame.font.Font(None, radius)
            icon_text = self._get_node_icon(node.node_type)
            text_surface = font.render(icon_text, True, Colors.WHITE)
            text_rect = text_surface.get_rect(center=pos)
            surface.blit(text_surface, text_rect)
    
    def _draw_ankh_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw an ankh symbol for start nodes."""
        # Outer golden ring
        pygame.draw.circle(surface, Colors.GOLD, center, radius, 3)
        pygame.draw.circle(surface, (0, 0, 0, 120), center, radius - 5)
        
        # Ankh symbol
        x, y = center
        # Cross part
        pygame.draw.rect(surface, Colors.GOLD, (x - 3, y - 10, 6, 25))
        pygame.draw.rect(surface, Colors.GOLD, (x - 15, y + 5, 30, 6))
        # Loop part
        pygame.draw.circle(surface, Colors.GOLD, (x, y - 8), 12, 4)
        pygame.draw.circle(surface, (40, 30, 60), (x, y - 8), 8)
    
    def _draw_pyramid_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw a pyramid for boss nodes."""
        x, y = center
        
        # Shadow base
        shadow_points = [(x - radius + 5, y + radius - 5), (x + radius + 5, y + radius - 5), (x + 5, y - radius + 15)]
        pygame.draw.polygon(surface, (20, 15, 10), shadow_points)
        
        # Main pyramid
        points = [(x - radius, y + radius - 10), (x + radius, y + radius - 10), (x, y - radius + 10)]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, Colors.GOLD, points, 3)
        
        # Capstone
        cap_points = [(x - 15, y - radius + 25), (x + 15, y - radius + 25), (x, y - radius + 10)]
        pygame.draw.polygon(surface, Colors.GOLD, cap_points)
    
    def _draw_scarab_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw a scarab beetle for elite nodes."""
        x, y = center
        
        # Base circle
        pygame.draw.circle(surface, color, center, radius - 5)
        pygame.draw.circle(surface, Colors.GOLD, center, radius - 5, 3)
        
        # Scarab body (oval)
        body_rect = pygame.Rect(x - 12, y - 20, 24, 40)
        pygame.draw.ellipse(surface, Colors.GOLD, body_rect)
        pygame.draw.ellipse(surface, (40, 30, 10), body_rect)
        
        # Wing patterns
        pygame.draw.ellipse(surface, Colors.GOLD, (x - 10, y - 15, 8, 30), 2)
        pygame.draw.ellipse(surface, Colors.GOLD, (x + 2, y - 15, 8, 30), 2)
        
        # Antennae
        pygame.draw.line(surface, Colors.GOLD, (x - 5, y - 18), (x - 8, y - 25), 2)
        pygame.draw.line(surface, Colors.GOLD, (x + 5, y - 18), (x + 8, y - 25), 2)
    
    def _draw_treasure_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw a treasure chest for treasure nodes."""
        x, y = center
        
        # Chest base
        chest_rect = pygame.Rect(x - radius + 10, y - 5, (radius - 10) * 2, radius)
        pygame.draw.rect(surface, (139, 69, 19), chest_rect)  # Brown
        pygame.draw.rect(surface, Colors.GOLD, chest_rect, 3)
        
        # Chest lid
        lid_rect = pygame.Rect(x - radius + 10, y - radius + 5, (radius - 10) * 2, radius - 10)
        pygame.draw.rect(surface, (160, 82, 45), lid_rect)  # Lighter brown
        pygame.draw.rect(surface, Colors.GOLD, lid_rect, 3)
        
        # Lock and gems
        pygame.draw.circle(surface, Colors.GOLD, (x, y), 8)
        pygame.draw.circle(surface, Colors.LAPIS_LAZULI, (x - 10, y - 10), 4)
        pygame.draw.circle(surface, (255, 0, 255), (x + 10, y - 10), 4)  # Purple gem
    
    def _draw_event_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw Eye of Horus for event nodes."""
        x, y = center
        
        # Base circle with mystical glow
        pygame.draw.circle(surface, (75, 0, 130), center, radius - 3)  # Indigo
        pygame.draw.circle(surface, Colors.GOLD, center, radius - 3, 3)
        
        # Eye of Horus
        # Eye outline
        eye_points = [(x - 20, y), (x - 10, y - 8), (x + 10, y - 5), (x + 20, y), 
                      (x + 10, y + 8), (x - 10, y + 5)]
        pygame.draw.polygon(surface, Colors.GOLD, eye_points, 3)
        
        # Pupil
        pygame.draw.circle(surface, Colors.GOLD, center, 6)
        pygame.draw.circle(surface, (40, 30, 60), center, 4)
        
        # Horus markings
        pygame.draw.line(surface, Colors.GOLD, (x + 15, y + 3), (x + 18, y + 12), 3)
        pygame.draw.line(surface, Colors.GOLD, (x + 8, y + 8), (x + 12, y + 15), 2)
    
    def _draw_rest_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw a lotus flower for rest nodes."""
        x, y = center
        
        # Base water circle
        pygame.draw.circle(surface, Colors.LAPIS_LAZULI, center, radius - 5)
        pygame.draw.circle(surface, Colors.GOLD, center, radius - 5, 2)
        
        # Lotus petals
        for i in range(8):
            angle = i * 45
            petal_x = x + int(12 * math.cos(math.radians(angle)))
            petal_y = y + int(12 * math.sin(math.radians(angle)))
            pygame.draw.circle(surface, (255, 182, 193), (petal_x, petal_y), 8)  # Light pink
            pygame.draw.circle(surface, Colors.GOLD, (petal_x, petal_y), 8, 2)
        
        # Center
        pygame.draw.circle(surface, Colors.GOLD, center, 6)
    
    def _draw_shop_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw scales for merchant nodes."""
        x, y = center
        
        # Base circle
        pygame.draw.circle(surface, (34, 139, 34), center, radius - 5)  # Forest green
        pygame.draw.circle(surface, Colors.GOLD, center, radius - 5, 3)
        
        # Scale base
        pygame.draw.line(surface, Colors.GOLD, (x, y - 15), (x, y + 15), 4)
        
        # Scale pans
        pygame.draw.circle(surface, Colors.GOLD, (x - 15, y - 5), 8, 2)
        pygame.draw.circle(surface, Colors.GOLD, (x + 15, y - 5), 8, 2)
        
        # Scale arms
        pygame.draw.line(surface, Colors.GOLD, (x - 15, y - 5), (x, y - 8), 2)
        pygame.draw.line(surface, Colors.GOLD, (x + 15, y - 5), (x, y - 8), 2)
        
        # Coins
        pygame.draw.circle(surface, Colors.GOLD, (x - 15, y - 5), 4)
        pygame.draw.circle(surface, Colors.GOLD, (x + 15, y - 5), 4)
    
    def _draw_combat_node(self, surface: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw sword and shield for combat nodes."""
        x, y = center
        
        # Base circle
        pygame.draw.circle(surface, color, center, radius - 5)
        pygame.draw.circle(surface, Colors.GOLD, center, radius - 5, 3)
        
        # Shield
        shield_points = [(x - 8, y - 15), (x - 15, y - 5), (x - 15, y + 10), (x - 8, y + 18), (x - 8, y + 5)]
        pygame.draw.polygon(surface, (105, 105, 105), shield_points)  # Silver
        pygame.draw.polygon(surface, Colors.GOLD, shield_points, 2)
        
        # Sword
        # Blade
        pygame.draw.rect(surface, (192, 192, 192), (x + 5, y - 15, 4, 25))  # Silver blade
        # Hilt
        pygame.draw.rect(surface, Colors.GOLD, (x + 3, y + 8, 8, 4))
        # Pommel
        pygame.draw.circle(surface, Colors.GOLD, (x + 7, y + 12), 3)

    def _render_enhanced_progress(self, surface: pygame.Surface):
        """Render enhanced progress visualization."""
        # Progress bar at bottom
        progress_rect = pygame.Rect(self.left_panel_width + 50, SCREEN_HEIGHT - 80, 
                                   SCREEN_WIDTH - self.left_panel_width - self.right_panel_width - 100, 25)
        
        # Background
        pygame.draw.rect(surface, Colors.BLACK, progress_rect)
        pygame.draw.rect(surface, Colors.GOLD, progress_rect, 3)
        
        # Progress fill with gradient
        progress_ratio = self.current_level / self.max_levels
        fill_width = int(progress_ratio * (progress_rect.width - 6))
        if fill_width > 0:
            fill_rect = pygame.Rect(progress_rect.x + 3, progress_rect.y + 3, 
                                   fill_width, progress_rect.height - 6)
            pygame.draw.rect(surface, Colors.GOLD, fill_rect)
        
        # Progress text
        progress_text = f"Journey Progress: {self.current_level}/{self.max_levels} Levels Complete"
        scaling_manager.draw_scaled_text(
            surface, progress_text, (progress_rect.centerx, progress_rect.y - 35),
            'body', Colors.PAPYRUS, center=True
        )
    
    def _render_enhanced_tooltip(self, surface: pygame.Surface, node: MapNode):
        """Render enhanced tooltip with better styling and information."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Tooltip content
        lines = [
            node.name,
            f"Type: {node.node_type.name.title()}",
            node.description
        ]
        
        if node.reward:
            lines.append(f"Reward: {node.reward}")
        
        # State information
        if node.state == NodeState.LOCKED:
            lines.append("LOCKED - Complete previous nodes")
        elif node.state == NodeState.AVAILABLE:
            lines.append("AVAILABLE - Click to enter")
        elif node.state == NodeState.COMPLETED:
            lines.append("COMPLETED")
        elif node.state == NodeState.CURRENT:
            lines.append("CURRENT LOCATION")
        
        # Calculate tooltip size
        font = scaling_manager.get_font('tooltip')
        max_width = 0
        total_height = 0
        
        for line in lines:
            text_size = font.size(line)
            max_width = max(max_width, text_size[0])
            total_height += text_size[1] + 8
        
        # Enhanced tooltip styling
        tooltip_width = max_width + 30
        tooltip_height = total_height + 20
        tooltip_x = mouse_pos[0] + 25
        tooltip_y = mouse_pos[1] - tooltip_height // 2
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > SCREEN_WIDTH - 20:
            tooltip_x = mouse_pos[0] - tooltip_width - 25
        if tooltip_y < 20:
            tooltip_y = 20
        elif tooltip_y + tooltip_height > SCREEN_HEIGHT - 20:
            tooltip_y = SCREEN_HEIGHT - tooltip_height - 20
        
        # Enhanced background
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        tooltip_surface.fill((40, 30, 60))
        tooltip_surface.set_alpha(240)
        pygame.draw.rect(tooltip_surface, self._get_node_color(node), 
                        (0, 0, tooltip_width, tooltip_height), 3)
        surface.blit(tooltip_surface, (tooltip_x, tooltip_y))
        
        # Render text
        y_offset = 15
        for i, line in enumerate(lines):
            if i == 0:  # Title
                color = self._get_node_color(node)
                text_font = scaling_manager.get_font('card_name')
            else:
                color = Colors.PAPYRUS
                text_font = font
            
            text_surface = text_font.render(line, True, color)
            surface.blit(text_surface, (tooltip_x + 15, tooltip_y + y_offset))
            y_offset += text_font.size(line)[1] + 8
    
    def _render_enhanced_instructions(self, surface: pygame.Surface):
        """Render enhanced control instructions."""
        instructions = [
            "Click nodes to select and navigate • SPACE: Enter selected node",
            "Mouse: Pan camera • ESC: Return to main menu",
            "Follow the branching paths through the Egyptian underworld!"
        ]
        
        y = SCREEN_HEIGHT - 45
        for instruction in instructions:
            scaling_manager.draw_scaled_text(
                surface, instruction, (SCREEN_CENTER[0], y), 'tooltip',
                Colors.DESERT_SAND, center=True
            )
            y += 20
    
    def reset_animations(self):
        """Reset animations for clean entry."""
        self.fade_in_progress = 0.0
        self.animation_time = 0.0
        
        # Start ambient music
        audio_manager.play_music(AudioTrack.AMBIENT, fade_in=2.0)
    
    def complete_node(self, completed_node):
        """Complete a node and advance progression."""
        if not completed_node:
            return
            
        # Mark node as completed
        completed_node.state = NodeState.COMPLETED
        
        # Advance to next level if all current level nodes are completed
        current_level_nodes = [n for n in self.nodes if n.level == self.current_level]
        current_level_available = [n for n in current_level_nodes if n.state == NodeState.AVAILABLE]
        
        # If no more available nodes at current level, advance
        if not current_level_available:
            self.current_level += 1
            
            # Unlock next level nodes
            next_level_nodes = [n for n in self.nodes if n.level == self.current_level + 1]
            for node in next_level_nodes:
                if node.state == NodeState.LOCKED:
                    node.state = NodeState.AVAILABLE
            
            # Update current node tracking
            available_nodes = [n for n in self.nodes if n.state == NodeState.AVAILABLE]
            if available_nodes:
                self.current_node = available_nodes[0]
                # Update camera to new current node
                self.target_camera_x = -self.current_node.x + SCREEN_CENTER[0]
                self.target_camera_y = -self.current_node.y + SCREEN_CENTER[1]
        
        print(f"Node completed: {completed_node.name} - Current level: {self.current_level}")