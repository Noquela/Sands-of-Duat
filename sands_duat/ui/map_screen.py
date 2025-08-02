"""
Map Screen

Node progression interface for navigating through the 12 hours
of night in the Egyptian underworld.
"""

import pygame
import math
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from .base import UIScreen, UIComponent


class NodeType(Enum):
    """Types of map nodes."""
    COMBAT = "combat"
    EVENT = "event"
    SHOP = "shop"
    REST = "rest"
    BOSS = "boss"
    TREASURE = "treasure"


class MapNode(UIComponent):
    """
    Represents a single node on the map.
    """
    
    def __init__(self, x: int, y: int, node_id: str, node_type: NodeType):
        super().__init__(x - 25, y - 25, 50, 50)  # 50x50 node
        self.node_id = node_id
        self.node_type = node_type
        self.visited = False
        self.available = False
        self.connections: List[str] = []
        
        # Visual properties
        self.base_color = self._get_node_color()
        self.current_color = self.base_color
        self.pulse_time = 0.0
        
        # Icons (simplified - would use actual images in full implementation)
        self.icon_symbol = self._get_node_symbol()
    
    def update(self, delta_time: float) -> None:
        """Update node animations."""
        self.pulse_time += delta_time
        
        # Pulse animation for available nodes
        if self.available and not self.visited:
            pulse_factor = 0.8 + 0.2 * (1 + math.sin(self.pulse_time * 3)) / 2
            self.current_color = tuple(int(c * pulse_factor) for c in self.base_color)
        else:
            self.current_color = self.base_color
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the map node."""
        if not self.visible:
            return
        
        center = self.rect.center
        radius = 20
        
        # Node background
        if self.visited:
            # Darker for visited nodes
            color = tuple(c // 2 for c in self.current_color)
        elif self.available:
            color = self.current_color
        else:
            # Grayed out for unavailable nodes
            color = (100, 100, 100)
        
        pygame.draw.circle(surface, color, center, radius)
        
        # Node border
        border_color = (255, 255, 255) if self.available else (128, 128, 128)
        border_width = 3 if self.hovered else 2
        pygame.draw.circle(surface, border_color, center, radius, border_width)
        
        # Node icon/symbol
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.icon_symbol, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)
        
        # Visited indicator
        if self.visited:
            checkmark_points = [
                (center[0] - 8, center[1]),
                (center[0] - 3, center[1] + 5),
                (center[0] + 8, center[1] - 5)
            ]
            pygame.draw.lines(surface, (0, 255, 0), False, checkmark_points, 3)
    
    def _get_node_color(self) -> Tuple[int, int, int]:
        """Get the base color for this node type."""
        colors = {
            NodeType.COMBAT: (200, 50, 50),      # Red
            NodeType.EVENT: (50, 150, 200),      # Blue
            NodeType.SHOP: (200, 200, 50),       # Yellow
            NodeType.REST: (50, 200, 50),        # Green
            NodeType.BOSS: (150, 50, 150),       # Purple
            NodeType.TREASURE: (255, 165, 0)     # Orange
        }
        return colors.get(self.node_type, (128, 128, 128))
    
    def _get_node_symbol(self) -> str:
        """Get the symbol for this node type."""
        symbols = {
            NodeType.COMBAT: "⚔",
            NodeType.EVENT: "?",
            NodeType.SHOP: "$",
            NodeType.REST: "♥",
            NodeType.BOSS: "☠",
            NodeType.TREASURE: "★"
        }
        return symbols.get(self.node_type, "?")
    
    def set_available(self, available: bool) -> None:
        """Set whether this node is available for selection."""
        self.available = available
    
    def set_visited(self, visited: bool) -> None:
        """Set whether this node has been visited."""
        self.visited = visited


class MapPath(UIComponent):
    """
    Represents a connection between map nodes.
    """
    
    def __init__(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        # Calculate bounding rect for the path
        min_x = min(start_pos[0], end_pos[0]) - 5
        min_y = min(start_pos[1], end_pos[1]) - 5
        max_x = max(start_pos[0], end_pos[0]) + 5
        max_y = max(start_pos[1], end_pos[1]) + 5
        
        super().__init__(min_x, min_y, max_x - min_x, max_y - min_y)
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.active = False
        
        # Visual properties
        self.path_color = (139, 117, 93)  # Bronze
        self.active_color = (255, 215, 0)  # Gold
    
    def update(self, delta_time: float) -> None:
        """Update path animations."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the path connection."""
        if not self.visible:
            return
        
        color = self.active_color if self.active else self.path_color
        width = 4 if self.active else 2
        
        pygame.draw.line(surface, color, self.start_pos, self.end_pos, width)
    
    def set_active(self, active: bool) -> None:
        """Set whether this path is currently active."""
        self.active = active


class HourDisplay(UIComponent):
    """
    Displays the current hour of night and progress.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.current_hour = 1
        self.max_hours = 12
        self.hour_name = "First Hour of Night"
        
        # Visual settings
        self.bg_color = (20, 15, 10, 200)
        self.text_color = (255, 248, 220)
        self.accent_color = (255, 215, 0)
    
    def update(self, delta_time: float) -> None:
        """Update hour display."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the hour display."""
        if not self.visible:
            return
        
        # Background
        bg_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        surface.blit(bg_surface, self.rect.topleft)
        
        # Border
        pygame.draw.rect(surface, self.accent_color, self.rect, 2)
        
        # Hour title
        title_font = pygame.font.Font(None, 28)
        title_text = title_font.render(self.hour_name, True, self.accent_color)
        title_rect = title_text.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.top = self.rect.top + 10
        surface.blit(title_text, title_rect)
        
        # Hour progress
        progress_font = pygame.font.Font(None, 20)
        progress_text = progress_font.render(f"Hour {self.current_hour} of {self.max_hours}", True, self.text_color)
        progress_rect = progress_text.get_rect()
        progress_rect.centerx = self.rect.centerx
        progress_rect.top = title_rect.bottom + 5
        surface.blit(progress_text, progress_rect)
        
        # Progress bar
        bar_width = self.rect.width - 40
        bar_height = 8
        bar_x = self.rect.x + 20
        bar_y = progress_rect.bottom + 10
        
        # Background bar
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress bar
        progress = self.current_hour / self.max_hours
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(surface, self.accent_color, (bar_x, bar_y, progress_width, bar_height))
    
    def set_hour(self, hour: int, hour_name: str) -> None:
        """Set the current hour."""
        self.current_hour = hour
        self.hour_name = hour_name


class MapScreen(UIScreen):
    """
    Map navigation screen for the 12 hours of night.
    
    Displays available paths, nodes, and progression through
    the Egyptian underworld.
    """
    
    def __init__(self):
        super().__init__("map")
        
        # Map data
        self.nodes: Dict[str, MapNode] = {}
        self.paths: List[MapPath] = []
        self.current_node: Optional[str] = None
        self.available_nodes: List[str] = []
        
        # UI components
        self.hour_display: Optional[HourDisplay] = None
        
        # Map layout
        self.map_width = 600
        self.map_height = 400
        self.map_offset_x = 100
        self.map_offset_y = 100
        
        # Hour names for the 12 hours of night
        self.hour_names = [
            "First Hour: The Entrance",
            "Second Hour: The River of Fire", 
            "Third Hour: The Desert of Knives",
            "Fourth Hour: The Valley of Serpents",
            "Fifth Hour: The Lake of Fire",
            "Sixth Hour: The Abyss of Osiris",
            "Seventh Hour: The Chamber of Judgment",
            "Eighth Hour: The Hall of Two Truths",
            "Ninth Hour: The Cavern of Sokar",
            "Tenth Hour: The Waters of Ra",
            "Eleventh Hour: The Gates of Dawn",
            "Twelfth Hour: The Rebirth"
        ]
    
    def on_enter(self) -> None:
        """Initialize map screen."""
        self.logger.info("Entering map screen")
        self._setup_ui_components()
        self._generate_map()
    
    def on_exit(self) -> None:
        """Clean up map screen."""
        self.logger.info("Exiting map screen")
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up UI components."""
        # Hour display
        self.hour_display = HourDisplay(50, 50, 300, 100)
        self.hour_display.set_hour(1, self.hour_names[0])
        self.add_component(self.hour_display)
    
    def _generate_map(self) -> None:
        """Generate the map layout."""
        # Clear existing map
        self.nodes.clear()
        self.paths.clear()
        
        # Generate nodes for current hour
        # This is a simplified generation - a full implementation would
        # have more sophisticated map generation
        
        # Create starting node
        start_node = MapNode(
            self.map_offset_x + 50,
            self.map_offset_y + self.map_height // 2,
            "start",
            NodeType.REST
        )
        start_node.set_visited(True)
        start_node.set_available(False)
        self.nodes["start"] = start_node
        self.add_component(start_node)
        
        # Create middle layer nodes
        middle_nodes = []
        for i in range(3):
            node_types = [NodeType.COMBAT, NodeType.EVENT, NodeType.SHOP]
            node_type = node_types[i]
            
            node = MapNode(
                self.map_offset_x + 250,
                self.map_offset_y + 100 + i * 100,
                f"middle_{i}",
                node_type
            )
            node.set_available(True)
            node.add_event_handler("click", self._on_node_clicked)
            
            self.nodes[f"middle_{i}"] = node
            middle_nodes.append(node)
            self.add_component(node)
        
        # Create end node (boss)
        end_node = MapNode(
            self.map_offset_x + 450,
            self.map_offset_y + self.map_height // 2,
            "end",
            NodeType.BOSS
        )
        end_node.set_available(False)
        self.nodes["end"] = end_node
        self.add_component(end_node)
        
        # Create paths
        start_pos = (start_node.rect.centerx, start_node.rect.centery)
        
        # Paths from start to middle
        for middle_node in middle_nodes:
            middle_pos = (middle_node.rect.centerx, middle_node.rect.centery)
            path = MapPath(start_pos, middle_pos)
            path.set_active(True)
            self.paths.append(path)
            self.add_component(path)
        
        # Paths from middle to end
        end_pos = (end_node.rect.centerx, end_node.rect.centery)
        for middle_node in middle_nodes:
            middle_pos = (middle_node.rect.centerx, middle_node.rect.centery)
            path = MapPath(middle_pos, end_pos)
            self.paths.append(path)
            self.add_component(path)
        
        # Set current available nodes
        self.available_nodes = ["middle_0", "middle_1", "middle_2"]
        self.current_node = "start"
    
    def _on_node_clicked(self, component: UIComponent, event_data: Dict[str, Any]) -> None:
        """Handle node selection."""
        if isinstance(component, MapNode) and component.available and not component.visited:
            self.logger.info(f"Selected node: {component.node_id} ({component.node_type.value})")
            
            # Mark node as visited
            component.set_visited(True)
            component.set_available(False)
            
            # Update current node
            self.current_node = component.node_id
            
            # Trigger appropriate screen transition based on node type
            if component.node_type == NodeType.COMBAT:
                self._trigger_event("enter_combat", {"node_id": component.node_id})
            elif component.node_type == NodeType.EVENT:
                self._trigger_event("enter_event", {"node_id": component.node_id})
            elif component.node_type == NodeType.SHOP:
                self._trigger_event("enter_shop", {"node_id": component.node_id})
            elif component.node_type == NodeType.REST:
                self._trigger_event("enter_rest", {"node_id": component.node_id})
            elif component.node_type == NodeType.BOSS:
                self._trigger_event("enter_boss", {"node_id": component.node_id})
    
    def advance_to_next_hour(self) -> None:
        """Advance to the next hour of night."""
        if self.hour_display and self.hour_display.current_hour < 12:
            new_hour = self.hour_display.current_hour + 1
            self.hour_display.set_hour(new_hour, self.hour_names[new_hour - 1])
            self._generate_map()  # Generate new map for the next hour
    
    def unlock_next_nodes(self, node_ids: List[str]) -> None:
        """Unlock specific nodes for progression."""
        for node_id in node_ids:
            if node_id in self.nodes:
                self.nodes[node_id].set_available(True)
                if node_id not in self.available_nodes:
                    self.available_nodes.append(node_id)
    
    def get_available_nodes(self) -> List[str]:
        """Get list of currently available node IDs."""
        return self.available_nodes.copy()
    
    def get_current_hour(self) -> int:
        """Get the current hour number."""
        return self.hour_display.current_hour if self.hour_display else 1