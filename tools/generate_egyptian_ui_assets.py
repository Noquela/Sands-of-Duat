#!/usr/bin/env python3
"""
Generate Egyptian-themed UI assets for the progression map.
Creates the missing node icons and panel assets that the game expects.
"""

import pygame
import math
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def create_egyptian_node_icon(icon_type: str, size: int = 120) -> pygame.Surface:
    """Create Egyptian-themed node icons for the progression map."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Base colors for different node types
    colors = {
        'node_ankh': (255, 215, 0),      # Gold for start/ankh
        'node_pyramid': (138, 43, 226),   # Purple for boss
        'node_scarab': (255, 140, 0),     # Orange for elite
        'node_treasure': (255, 215, 0),   # Gold for treasure
        'node_eye_horus': (65, 105, 225), # Blue for events
        'node_lotus': (34, 139, 34),      # Green for rest
        'node_scales': (160, 82, 45),     # Brown for shop
        'node_combat': (220, 20, 60)      # Red for combat
    }
    
    base_color = colors.get(icon_type, (128, 128, 128))
    
    # Create circular background
    pygame.draw.circle(surface, (0, 0, 0, 180), (center, center), center - 5)
    pygame.draw.circle(surface, base_color, (center, center), center - 10, 8)
    
    if icon_type == 'node_ankh':
        # Draw simplified ankh symbol
        # Vertical line
        pygame.draw.rect(surface, base_color, (center - 4, center - 20, 8, 40))
        # Horizontal line
        pygame.draw.rect(surface, base_color, (center - 15, center + 5, 30, 8))
        # Top loop (oval)
        pygame.draw.ellipse(surface, (0, 0, 0, 200), (center - 12, center - 30, 24, 20))
        pygame.draw.ellipse(surface, base_color, (center - 10, center - 28, 20, 16), 6)
        
    elif icon_type == 'node_pyramid':
        # Draw pyramid
        points = [
            (center, center - 25),        # Top
            (center - 20, center + 20),   # Bottom left
            (center + 20, center + 20)    # Bottom right
        ]
        pygame.draw.polygon(surface, base_color, points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 3)
        # Add inner lines
        pygame.draw.line(surface, (0, 0, 0), (center, center - 25), (center, center + 20), 2)
        
    elif icon_type == 'node_scarab':
        # Draw scarab beetle (simplified)
        # Body (oval)
        pygame.draw.ellipse(surface, base_color, (center - 15, center - 10, 30, 20))
        pygame.draw.ellipse(surface, (0, 0, 0), (center - 15, center - 10, 30, 20), 2)
        # Wing patterns
        pygame.draw.arc(surface, (0, 0, 0), (center - 12, center - 8, 10, 16), 0, math.pi, 2)
        pygame.draw.arc(surface, (0, 0, 0), (center + 2, center - 8, 10, 16), 0, math.pi, 2)
        
    elif icon_type == 'node_treasure':
        # Draw treasure chest
        # Base
        pygame.draw.rect(surface, base_color, (center - 18, center - 5, 36, 20))
        # Lid
        pygame.draw.rect(surface, base_color, (center - 20, center - 15, 40, 12))
        pygame.draw.rect(surface, (0, 0, 0), (center - 20, center - 15, 40, 12), 2)
        # Lock
        pygame.draw.rect(surface, (139, 69, 19), (center - 5, center - 10, 10, 8))
        
    elif icon_type == 'node_eye_horus':
        # Draw Eye of Horus (simplified)
        # Outer eye shape
        pygame.draw.ellipse(surface, base_color, (center - 20, center - 8, 40, 16))
        pygame.draw.ellipse(surface, (0, 0, 0), (center - 20, center - 8, 40, 16), 2)
        # Inner eye
        pygame.draw.circle(surface, (0, 0, 0), (center, center), 6)
        pygame.draw.circle(surface, (255, 255, 255), (center, center), 4)
        # Eye markings
        pygame.draw.line(surface, (0, 0, 0), (center + 20, center), (center + 25, center + 10), 3)
        pygame.draw.line(surface, (0, 0, 0), (center - 20, center), (center - 15, center + 8), 2)
        
    elif icon_type == 'node_lotus':
        # Draw lotus flower
        # Petals
        for i in range(8):
            angle = i * math.pi / 4
            x1 = center + int(15 * math.cos(angle))
            y1 = center + int(15 * math.sin(angle))
            x2 = center + int(8 * math.cos(angle))
            y2 = center + int(8 * math.sin(angle))
            pygame.draw.line(surface, base_color, (center, center), (x1, y1), 6)
        # Center
        pygame.draw.circle(surface, base_color, (center, center), 8)
        pygame.draw.circle(surface, (0, 0, 0), (center, center), 8, 2)
        
    elif icon_type == 'node_scales':
        # Draw scales of justice
        # Base
        pygame.draw.rect(surface, base_color, (center - 2, center + 10, 4, 15))
        # Beam
        pygame.draw.rect(surface, base_color, (center - 20, center - 2, 40, 4))
        # Left pan
        pygame.draw.ellipse(surface, base_color, (center - 25, center + 5, 12, 6))
        # Right pan
        pygame.draw.ellipse(surface, base_color, (center + 13, center + 5, 12, 6))
        # Chains
        pygame.draw.line(surface, (0, 0, 0), (center - 15, center), (center - 19, center + 5), 2)
        pygame.draw.line(surface, (0, 0, 0), (center + 15, center), (center + 19, center + 5), 2)
        
    elif icon_type == 'node_combat':
        # Draw crossed swords
        # Sword 1 (diagonal)
        pygame.draw.line(surface, base_color, (center - 15, center - 15), (center + 15, center + 15), 6)
        # Sword 2 (diagonal)
        pygame.draw.line(surface, base_color, (center + 15, center - 15), (center - 15, center + 15), 6)
        # Cross guards
        pygame.draw.line(surface, (0, 0, 0), (center - 8, center - 8), (center + 8, center + 8), 2)
        pygame.draw.line(surface, (0, 0, 0), (center + 8, center - 8), (center - 8, center + 8), 2)
    
    return surface

def create_ui_panel(panel_type: str, width: int, height: int) -> pygame.Surface:
    """Create Egyptian-themed UI panels."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Papyrus-like background
    base_color = (245, 238, 203)  # Papyrus color
    dark_color = (139, 125, 107)  # Dark papyrus
    
    # Fill with base papyrus color
    surface.fill(base_color)
    
    # Add papyrus texture pattern
    for y in range(0, height, 20):
        for x in range(0, width, 30):
            if (x + y) % 60 == 0:
                pygame.draw.rect(surface, dark_color, (x, y, 25, 3))
                pygame.draw.rect(surface, dark_color, (x + 10, y + 10, 3, 15))
    
    # Egyptian border pattern
    border_width = 12
    border_color = (139, 69, 19)  # Egyptian brown
    gold_color = (255, 215, 0)
    
    # Main border
    pygame.draw.rect(surface, border_color, (0, 0, width, border_width))
    pygame.draw.rect(surface, border_color, (0, height - border_width, width, border_width))
    pygame.draw.rect(surface, border_color, (0, 0, border_width, height))
    pygame.draw.rect(surface, border_color, (width - border_width, 0, border_width, height))
    
    # Gold accent lines
    pygame.draw.rect(surface, gold_color, (border_width//2, border_width//2, width - border_width, 2))
    pygame.draw.rect(surface, gold_color, (border_width//2, height - border_width//2 - 2, width - border_width, 2))
    pygame.draw.rect(surface, gold_color, (border_width//2, border_width//2, 2, height - border_width))
    pygame.draw.rect(surface, gold_color, (width - border_width//2 - 2, border_width//2, 2, height - border_width))
    
    # Corner decorations (simplified hieroglyphs)
    corner_size = 24
    for corner_x, corner_y in [(border_width, border_width), 
                               (width - border_width - corner_size, border_width),
                               (border_width, height - border_width - corner_size),
                               (width - border_width - corner_size, height - border_width - corner_size)]:
        # Small Egyptian symbol in each corner
        pygame.draw.circle(surface, gold_color, (corner_x + corner_size//2, corner_y + corner_size//2), corner_size//3, 2)
        pygame.draw.line(surface, gold_color, (corner_x + 4, corner_y + corner_size//2), 
                        (corner_x + corner_size - 4, corner_y + corner_size//2), 2)
    
    return surface

def main():
    """Generate all missing Egyptian UI assets."""
    pygame.init()
    
    # Create directories
    assets_dir = Path("assets/generated_4k")
    ui_dir = assets_dir / "ui_element"
    panel_dir = assets_dir / "ui_panel"
    
    ui_dir.mkdir(parents=True, exist_ok=True)
    panel_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Egyptian-themed UI assets...")
    
    # Generate node icons
    node_icons = [
        'node_ankh', 'node_pyramid', 'node_scarab', 'node_treasure',
        'node_eye_horus', 'node_lotus', 'node_scales', 'node_combat'
    ]
    
    for icon_name in node_icons:
        print(f"   Creating {icon_name}...")
        icon_surface = create_egyptian_node_icon(icon_name, 120)
        pygame.image.save(icon_surface, str(ui_dir / f"{icon_name}.png"))
    
    # Generate UI panels
    print("   Creating UI panels...")
    
    # Left panel (300x1440)
    left_panel = create_ui_panel("left", 300, 1440)
    pygame.image.save(left_panel, str(panel_dir / "ui_panel_left.png"))
    
    # Right panel (300x1440)
    right_panel = create_ui_panel("right", 300, 1440)
    pygame.image.save(right_panel, str(panel_dir / "ui_panel_right.png"))
    
    # Generic side panel
    side_panel = create_ui_panel("side", 300, 1440)
    pygame.image.save(side_panel, str(panel_dir / "ui_side_panel.png"))
    
    # Papyrus panel (alternative)
    papyrus_panel = create_ui_panel("papyrus", 300, 1440)
    pygame.image.save(papyrus_panel, str(panel_dir / "panel_papyrus.png"))
    
    print("Egyptian UI asset generation complete!")
    print(f"   Generated {len(node_icons)} node icons")
    print(f"   Generated 4 UI panels")
    print(f"   Assets saved to: {assets_dir}")

if __name__ == "__main__":
    main()