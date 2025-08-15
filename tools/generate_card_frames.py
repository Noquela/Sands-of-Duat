#!/usr/bin/env python3
"""
Generate Egyptian-themed card frames for different rarities.
"""

import pygame
import math
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def create_egyptian_card_frame(rarity: str, width: int = 256, height: int = 384) -> pygame.Surface:
    """Create Egyptian-themed card frame for specific rarity."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Rarity colors
    rarity_colors = {
        'common': {
            'primary': (245, 245, 220),  # Beige
            'accent': (139, 125, 107),   # Dark beige
            'highlight': (255, 248, 220) # Light beige
        },
        'rare': {
            'primary': (65, 105, 225),   # Royal blue
            'accent': (25, 25, 112),     # Navy
            'highlight': (135, 206, 250) # Sky blue
        },
        'epic': {
            'primary': (138, 43, 226),   # Blue violet
            'accent': (75, 0, 130),      # Indigo
            'highlight': (186, 85, 211)  # Medium orchid
        },
        'legendary': {
            'primary': (255, 215, 0),    # Gold
            'accent': (184, 134, 11),    # Dark gold
            'highlight': (255, 255, 224) # Light yellow
        }
    }
    
    colors = rarity_colors.get(rarity, rarity_colors['common'])
    
    # Outer border (Egyptian style)
    border_width = 12
    pygame.draw.rect(surface, colors['accent'], (0, 0, width, height))
    pygame.draw.rect(surface, colors['primary'], 
                    (border_width//2, border_width//2, 
                     width - border_width, height - border_width))
    
    # Inner decorative border
    inner_border = 8
    inner_rect = pygame.Rect(border_width + inner_border, border_width + inner_border,
                           width - 2*(border_width + inner_border), 
                           height - 2*(border_width + inner_border))
    pygame.draw.rect(surface, colors['accent'], inner_rect, 3)
    
    # Egyptian corner decorations
    corner_size = 20
    corners = [
        (border_width, border_width),  # Top-left
        (width - border_width - corner_size, border_width),  # Top-right
        (border_width, height - border_width - corner_size),  # Bottom-left
        (width - border_width - corner_size, height - border_width - corner_size)  # Bottom-right
    ]
    
    for x, y in corners:
        # Egyptian corner symbol (simplified ankh or scarab)
        if rarity == 'legendary':
            # Ankh symbol for legendary
            pygame.draw.rect(surface, colors['highlight'], (x + 8, y + 5, 4, 15))  # Vertical
            pygame.draw.rect(surface, colors['highlight'], (x + 3, y + 12, 14, 4))  # Horizontal
            pygame.draw.ellipse(surface, colors['highlight'], (x + 6, y + 2, 8, 8), 2)  # Top loop
        else:
            # Simple geometric pattern
            pygame.draw.circle(surface, colors['highlight'], (x + corner_size//2, y + corner_size//2), corner_size//3, 2)
            pygame.draw.line(surface, colors['highlight'], 
                           (x + 4, y + corner_size//2), (x + corner_size - 4, y + corner_size//2), 2)
    
    # Side decorations (Egyptian hieroglyph-style)
    if rarity in ['epic', 'legendary']:
        # Add more elaborate decorations for higher rarities
        mid_y = height // 2
        
        # Left side decoration
        left_x = border_width + 2
        for i in range(3):
            y_pos = mid_y - 30 + i * 30
            pygame.draw.circle(surface, colors['highlight'], (left_x, y_pos), 3)
            pygame.draw.line(surface, colors['highlight'], (left_x + 5, y_pos), (left_x + 15, y_pos), 2)
        
        # Right side decoration
        right_x = width - border_width - 2
        for i in range(3):
            y_pos = mid_y - 30 + i * 30
            pygame.draw.circle(surface, colors['highlight'], (right_x, y_pos), 3)
            pygame.draw.line(surface, colors['highlight'], (right_x - 15, y_pos), (right_x - 5, y_pos), 2)
    
    # Bottom name plate area (where card name goes)
    name_plate_height = 40
    name_plate_y = height - border_width - name_plate_height - 5
    name_plate_rect = pygame.Rect(border_width + 5, name_plate_y, 
                                 width - 2*(border_width + 5), name_plate_height)
    
    # Name plate background
    pygame.draw.rect(surface, (*colors['accent'], 180), name_plate_rect)
    pygame.draw.rect(surface, colors['primary'], name_plate_rect, 2)
    
    # Subtle gradient effect for legendary cards
    if rarity == 'legendary':
        # Add golden glow effect
        for i in range(5):
            alpha = 30 - i * 5
            glow_rect = pygame.Rect(i, i, width - 2*i, height - 2*i)
            glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*colors['highlight'], alpha), glow_rect, 2)
            surface.blit(glow_surface, (0, 0))
    
    return surface

def main():
    """Generate card frames for all rarities."""
    pygame.init()
    
    # Create directory
    assets_dir = Path("assets/generated_4k")
    card_frame_dir = assets_dir / "card_frame"
    card_frame_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Egyptian card frames...")
    
    rarities = ['common', 'rare', 'epic', 'legendary']
    
    for rarity in rarities:
        print(f"   Creating {rarity} card frame...")
        frame_surface = create_egyptian_card_frame(rarity)
        
        # Save both naming conventions
        pygame.image.save(frame_surface, str(card_frame_dir / f"card_frame_{rarity}.png"))
        pygame.image.save(frame_surface, str(card_frame_dir / f"{rarity}_frame.png"))
    
    print("Card frame generation complete!")
    print(f"   Generated frames for {len(rarities)} rarities")
    print(f"   Assets saved to: {card_frame_dir}")

if __name__ == "__main__":
    main()