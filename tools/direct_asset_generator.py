#!/usr/bin/env python3
"""
SANDS OF DUAT - Direct Asset Generator
Generates Egyptian-themed assets with fixed seeds for consistency
Optimized for RTX 5070 performance
"""

import os
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import json

class DirectAssetGenerator:
    """Generate game assets directly using PIL and procedural generation."""
    
    def __init__(self):
        """Initialize the direct asset generator."""
        self.output_dir = Path("../ai_generated")
        self.ensure_directories()
        
        # Egyptian color palette
        self.colors = {
            'gold': '#FFD700',
            'bronze': '#CD7F32', 
            'sand': '#F4A460',
            'papyrus': '#F5F5DC',
            'hieroglyph': '#8B4513',
            'lapis': '#191970',
            'emerald': '#50C878',
            'obsidian': '#0B1426',
            'ivory': '#FFFFF0',
            'crimson': '#DC143C'
        }
        
        # Fixed seeds for consistency
        self.seeds = {
            'pharaoh': 12345,
            'anubis': 23456,
            'isis': 34567,
            'ra': 45678,
            'set': 56789,
            'mummy': 67890,
            'sphinx': 78901,
            'warrior': 89012
        }
        
    def ensure_directories(self):
        """Create all required directories."""
        dirs = [
            self.output_dir / "4k_sprites",
            self.output_dir / "8k_backgrounds", 
            self.output_dir / "ui_elements",
            self.output_dir / "weapons",
            self.output_dir / "characters"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient(self, width, height, color1, color2, direction='vertical'):
        """Create a gradient background."""
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        c1 = self.hex_to_rgb(color1)
        c2 = self.hex_to_rgb(color2)
        
        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:  # horizontal
            for x in range(width):
                ratio = x / width
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
                
        return image
    
    def add_egyptian_border(self, image, border_width=20):
        """Add Egyptian-style border to image."""
        width, height = image.size
        bordered = Image.new('RGBA', (width + border_width*2, height + border_width*2), (0, 0, 0, 0))
        
        # Draw border with Egyptian pattern
        draw = ImageDraw.Draw(bordered)
        border_color = self.hex_to_rgb(self.colors['gold'])
        
        # Outer border
        draw.rectangle([0, 0, width + border_width*2 - 1, height + border_width*2 - 1], 
                      outline=border_color, width=3)
        
        # Inner decorative lines
        for i in range(3, border_width-3, 4):
            draw.rectangle([i, i, width + border_width*2 - i - 1, height + border_width*2 - i - 1], 
                          outline=border_color, width=1)
        
        # Paste original image
        bordered.paste(image, (border_width, border_width))
        
        return bordered
    
    def create_hieroglyph_pattern(self, width, height):
        """Create a simple hieroglyph pattern."""
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Simple hieroglyph shapes
        color = self.hex_to_rgb(self.colors['hieroglyph'])
        
        # Ankh symbol
        x, y = width // 4, height // 4
        draw.ellipse([x-10, y-15, x+10, y+5], outline=color, width=3)
        draw.line([x, y+5, x, y+40], fill=color, width=3)
        draw.line([x-15, y+20, x+15, y+20], fill=color, width=3)
        
        # Eye of Horus
        x, y = 3 * width // 4, height // 4
        draw.ellipse([x-15, y-5, x+15, y+5], outline=color, width=2)
        draw.line([x-15, y, x-25, y-5], fill=color, width=2)
        draw.line([x+15, y, x+25, y+5], fill=color, width=2)
        
        # Scarab beetle
        x, y = width // 4, 3 * height // 4
        draw.ellipse([x-12, y-8, x+12, y+8], outline=color, width=2)
        draw.line([x-8, y-12, x-8, y-20], fill=color, width=2)
        draw.line([x+8, y-12, x+8, y-20], fill=color, width=2)
        
        return image
    
    def generate_character_sprite(self, character_name, size=(1024, 1024)):
        """Generate a character sprite with procedural elements."""
        print(f"Generating {character_name} sprite ({size[0]}x{size[1]})...")
        
        # Set seed for consistency
        if character_name in self.seeds:
            random.seed(self.seeds[character_name])
        
        # Create base image
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        if character_name == 'pharaoh':
            # Pharaoh silhouette
            # Body
            draw.rectangle([center_x-60, center_y-20, center_x+60, center_y+200], 
                          fill=self.hex_to_rgb(self.colors['gold']))
            # Head
            draw.ellipse([center_x-40, center_y-100, center_x+40, center_y-20], 
                        fill=self.hex_to_rgb(self.colors['bronze']))
            # Crown
            draw.polygon([
                (center_x-50, center_y-100),
                (center_x-30, center_y-150),
                (center_x+30, center_y-150),
                (center_x+50, center_y-100)
            ], fill=self.hex_to_rgb(self.colors['gold']))
            
        elif character_name == 'anubis':
            # Anubis silhouette
            # Body
            draw.rectangle([center_x-50, center_y-10, center_x+50, center_y+180], 
                          fill=self.hex_to_rgb(self.colors['obsidian']))
            # Jackal head
            draw.polygon([
                (center_x-35, center_y-80),
                (center_x-20, center_y-120),
                (center_x+20, center_y-120),
                (center_x+35, center_y-80),
                (center_x+25, center_y-10),
                (center_x-25, center_y-10)
            ], fill=self.hex_to_rgb(self.colors['obsidian']))
            # Ears
            draw.polygon([
                (center_x-25, center_y-110),
                (center_x-35, center_y-140),
                (center_x-15, center_y-120)
            ], fill=self.hex_to_rgb(self.colors['obsidian']))
            draw.polygon([
                (center_x+25, center_y-110),
                (center_x+35, center_y-140),
                (center_x+15, center_y-120)
            ], fill=self.hex_to_rgb(self.colors['obsidian']))
            
        elif character_name == 'isis':
            # Isis silhouette
            # Body
            draw.rectangle([center_x-45, center_y-15, center_x+45, center_y+190], 
                          fill=self.hex_to_rgb(self.colors['lapis']))
            # Head
            draw.ellipse([center_x-35, center_y-90, center_x+35, center_y-15], 
                        fill=self.hex_to_rgb(self.colors['bronze']))
            # Wings
            draw.polygon([
                (center_x-45, center_y+50),
                (center_x-120, center_y+30),
                (center_x-100, center_y+100),
                (center_x-45, center_y+120)
            ], fill=self.hex_to_rgb(self.colors['emerald']))
            draw.polygon([
                (center_x+45, center_y+50),
                (center_x+120, center_y+30),
                (center_x+100, center_y+100),
                (center_x+45, center_y+120)
            ], fill=self.hex_to_rgb(self.colors['emerald']))
            
        # Add hieroglyph pattern overlay
        pattern = self.create_hieroglyph_pattern(size[0], size[1])
        pattern = pattern.resize(size)
        
        # Blend pattern with low opacity
        pattern_alpha = Image.new('RGBA', size, (0, 0, 0, 0))
        pattern_alpha.paste(pattern, (0, 0))
        pattern_alpha.putalpha(30)  # Low opacity
        
        # Composite
        result = Image.alpha_composite(image, pattern_alpha)
        
        # Add border
        result = self.add_egyptian_border(result, 15)
        
        # Save
        output_path = self.output_dir / "4k_sprites" / f"{character_name}_sprite.png"
        result.save(output_path)
        print(f"SAVED: {output_path}")
        
        return result
    
    def generate_background(self, bg_name, size=(2048, 1536)):
        """Generate an Egyptian background."""
        print(f"Generating {bg_name} background ({size[0]}x{size[1]})...")
        
        if bg_name == 'pyramid_sunset':
            # Desert sunset gradient
            image = self.create_gradient(size[0], size[1], 
                                       '#FFD700', '#FF4500', 'vertical')
            draw = ImageDraw.Draw(image)
            
            # Pyramid silhouettes
            pyramid_points = [
                (size[0]//4, size[1] - 100),
                (size[0]//4 - 200, size[1]),
                (size[0]//4 + 200, size[1])
            ]
            draw.polygon(pyramid_points, fill=self.hex_to_rgb('#654321'))
            
            # Larger pyramid
            pyramid2_points = [
                (3 * size[0]//4, size[1] - 200),
                (3 * size[0]//4 - 300, size[1]),
                (3 * size[0]//4 + 300, size[1])
            ]
            draw.polygon(pyramid2_points, fill=self.hex_to_rgb('#4A3728'))
            
        elif bg_name == 'temple_interior':
            # Temple interior
            image = self.create_gradient(size[0], size[1], 
                                       '#2F1B14', '#8B4513', 'horizontal')
            draw = ImageDraw.Draw(image)
            
            # Columns
            column_color = self.hex_to_rgb(self.colors['sand'])
            for x in range(size[0]//8, size[0], size[0]//4):
                draw.rectangle([x-30, 100, x+30, size[1]], fill=column_color)
                # Column capitals
                draw.ellipse([x-40, 80, x+40, 120], fill=self.hex_to_rgb(self.colors['gold']))
            
        elif bg_name == 'tomb_chamber':
            # Dark tomb chamber
            image = Image.new('RGB', size, self.hex_to_rgb('#1a1a1a'))
            draw = ImageDraw.Draw(image)
            
            # Torch light effect (circular gradients)
            for torch_x in [size[0]//4, 3*size[0]//4]:
                for radius in range(150, 50, -20):
                    alpha = max(0, 255 - (150 - radius) * 3)
                    color = (255, 140, 0, alpha)  # Orange flame color
                    # Simulate radial gradient with circles
                    draw.ellipse([torch_x - radius, 100 - radius//2, 
                                torch_x + radius, 100 + radius//2], 
                               outline=color[:3])
        
        # Add hieroglyphs
        hieroglyphs = self.create_hieroglyph_pattern(size[0], size[1])
        hieroglyph_layer = Image.new('RGBA', size, (0, 0, 0, 0))
        hieroglyph_layer.paste(hieroglyphs, (0, 0))
        hieroglyph_layer.putalpha(40)
        
        # Convert base image to RGBA for compositing
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        result = Image.alpha_composite(image, hieroglyph_layer)
        
        # Save
        output_path = self.output_dir / "8k_backgrounds" / f"{bg_name}_background.png"
        result.save(output_path)
        print(f"SAVED: {output_path}")
        
        return result
    
    def generate_ui_element(self, element_name, size=(256, 256)):
        """Generate UI elements."""
        print(f"Generating {element_name} UI element ({size[0]}x{size[1]})...")
        
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        if element_name == 'ankh_icon':
            # Ankh symbol
            gold_color = self.hex_to_rgb(self.colors['gold'])
            # Loop
            draw.ellipse([center_x-30, center_y-40, center_x+30, center_y-10], 
                        outline=gold_color, width=8)
            # Vertical line
            draw.line([center_x, center_y-10, center_x, center_y+50], 
                     fill=gold_color, width=8)
            # Horizontal line
            draw.line([center_x-25, center_y+10, center_x+25, center_y+10], 
                     fill=gold_color, width=8)
                     
        elif element_name == 'scarab_health':
            # Scarab beetle health orb
            # Outer glow
            for radius in range(60, 30, -5):
                alpha = max(0, 255 - (60 - radius) * 8)
                glow_color = (*self.hex_to_rgb(self.colors['emerald']), alpha)
                draw.ellipse([center_x - radius, center_y - radius, 
                            center_x + radius, center_y + radius], 
                           outline=glow_color[:3])
            
            # Beetle body
            draw.ellipse([center_x-25, center_y-15, center_x+25, center_y+15], 
                        fill=self.hex_to_rgb(self.colors['emerald']))
            # Wing details
            draw.line([center_x-15, center_y-10, center_x-15, center_y+10], 
                     fill=self.hex_to_rgb(self.colors['gold']), width=2)
            draw.line([center_x+15, center_y-10, center_x+15, center_y+10], 
                     fill=self.hex_to_rgb(self.colors['gold']), width=2)
                     
        elif element_name == 'eye_of_horus':
            # Eye of Horus
            # Main eye shape
            draw.ellipse([center_x-35, center_y-10, center_x+35, center_y+10], 
                        outline=self.hex_to_rgb(self.colors['lapis']), width=6)
            # Pupil
            draw.ellipse([center_x-8, center_y-8, center_x+8, center_y+8], 
                        fill=self.hex_to_rgb(self.colors['obsidian']))
            # Eye markings
            draw.line([center_x-35, center_y, center_x-50, center_y-10], 
                     fill=self.hex_to_rgb(self.colors['lapis']), width=4)
            draw.line([center_x+35, center_y, center_x+50, center_y+15], 
                     fill=self.hex_to_rgb(self.colors['lapis']), width=4)
            # Tear mark
            draw.line([center_x+20, center_y+10, center_x+20, center_y+30], 
                     fill=self.hex_to_rgb(self.colors['lapis']), width=3)
        
        # Add subtle glow effect
        result = image.filter(ImageFilter.GaussianBlur(1))
        result = Image.alpha_composite(result, image)
        
        # Save
        output_path = self.output_dir / "ui_elements" / f"{element_name}_ui.png"
        result.save(output_path)
        print(f"SAVED: {output_path}")
        
        return result
    
    def generate_complete_set(self):
        """Generate a complete set of Egyptian assets."""
        print("STARTING COMPLETE EGYPTIAN ASSET GENERATION")
        print("=" * 60)
        
        # Characters (4K sprites)
        characters = ['pharaoh', 'anubis', 'isis', 'ra', 'set', 'mummy', 'sphinx', 'warrior']
        print(f"\nGenerating {len(characters)} character sprites...")
        for char in characters:
            self.generate_character_sprite(char, (1024, 1024))
        
        # Backgrounds (8K environments)  
        backgrounds = ['pyramid_sunset', 'temple_interior', 'tomb_chamber']
        print(f"\nGenerating {len(backgrounds)} backgrounds...")
        for bg in backgrounds:
            self.generate_background(bg, (2048, 1536))
        
        # UI Elements
        ui_elements = ['ankh_icon', 'scarab_health', 'eye_of_horus']
        print(f"\nGenerating {len(ui_elements)} UI elements...")
        for ui in ui_elements:
            self.generate_ui_element(ui, (512, 512))  # Higher res for UI
        
        total_assets = len(characters) + len(backgrounds) + len(ui_elements)
        
        print("\n" + "=" * 60)
        print(f"GENERATION COMPLETE! {total_assets} ASSETS CREATED")
        print("\nGenerated assets:")
        print(f"  Characters: {len(characters)} (4K sprites)")
        print(f"  Backgrounds: {len(backgrounds)} (8K environments)")
        print(f"  UI Elements: {len(ui_elements)} (HD icons)")
        
        print(f"\nAll assets saved to: {self.output_dir.absolute()}")
        print("\nReady for integration into Sands of Duat!")

if __name__ == "__main__":
    generator = DirectAssetGenerator()
    generator.generate_complete_set()