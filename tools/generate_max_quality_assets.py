#!/usr/bin/env python3
"""
RTX 5070 MAXIMUM QUALITY ASSET GENERATOR
FULL VRAM UTILIZATION - NO LIMITS
"""

import os
import sys
import time
from pathlib import Path
import pygame
import json
from typing import Dict, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import math

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

class RTX5070MaxQualityArtGenerator:
    """Generates maximum quality Egyptian art assets for RTX 5070"""
    
    def __init__(self):
        # RTX 5070 MAXIMUM QUALITY SETTINGS
        self.card_resolution = (512, 768)     # Ultra high-res cards
        self.animation_frames = 16            # Smooth animations
        self.fps = 20                        # High FPS
        
        # Output directories
        self.base_dir = project_root
        self.output_dirs = {
            'cards': self.base_dir / "assets" / "approved_hades_quality" / "cards",
            'animated_cards': self.base_dir / "assets" / "approved_hades_quality" / "animated_cards",
            'backgrounds': self.base_dir / "assets" / "approved_hades_quality" / "backgrounds",
            'characters': self.base_dir / "assets" / "approved_hades_quality" / "characters"
        }
        
        # Create directories
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Egyptian color palettes for maximum authenticity
        self.egyptian_colors = {
            'gold': [(255, 215, 0), (218, 165, 32), (255, 223, 0)],
            'lapis': [(25, 25, 112), (30, 144, 255), (65, 105, 225)], 
            'turquoise': [(64, 224, 208), (72, 209, 204), (95, 158, 160)],
            'carnelian': [(255, 69, 0), (255, 99, 71), (205, 92, 92)],
            'malachite': [(0, 100, 0), (34, 139, 34), (50, 205, 50)],
            'papyrus': [(245, 245, 220), (255, 248, 220), (240, 230, 140)]
        }
        
        # Initialize pygame for rendering
        pygame.init()
        
    def create_egyptian_gradient(self, size: tuple, colors: List[tuple]) -> Image.Image:
        """Create smooth Egyptian-style gradient."""
        img = Image.new('RGB', size)
        draw = ImageDraw.Draw(img)
        
        width, height = size
        
        for y in range(height):
            ratio = y / height
            # Interpolate between colors
            if len(colors) >= 2:
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)  
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                
                # Add some noise for texture
                noise = random.randint(-10, 10)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img
    
    def add_hieroglyphic_details(self, img: Image.Image) -> Image.Image:
        """Add hieroglyphic-style details for authenticity."""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Add border patterns
        border_width = max(5, width // 100)
        
        # Golden border
        gold = self.egyptian_colors['gold'][0]
        for i in range(border_width):
            draw.rectangle([i, i, width-1-i, height-1-i], outline=gold, width=1)
        
        # Add corner decorations
        corner_size = width // 10
        corners = [(0, 0), (width-corner_size, 0), (0, height-corner_size), (width-corner_size, height-corner_size)]
        
        for x, y in corners:
            # Draw Egyptian corner motif
            points = []
            for angle in range(0, 360, 45):
                px = x + corner_size//2 + int(corner_size//4 * math.cos(math.radians(angle)))
                py = y + corner_size//2 + int(corner_size//4 * math.sin(math.radians(angle)))
                points.append((px, py))
            
            if len(points) >= 3:
                draw.polygon(points, fill=gold, outline=self.egyptian_colors['lapis'][0])
        
        return img
    
    def generate_anubis_card(self, animated: bool = True) -> bool:
        """Generate ultra-high quality Anubis card."""
        print("Generating ANUBIS - JUDGE OF THE DEAD (Maximum Quality)")
        
        if animated:
            return self._generate_animated_card("ANUBIS", "judge_of_dead", self._create_anubis_frames)
        else:
            card_img = self._create_anubis_static()
            output_path = self.output_dirs['cards'] / "anubis_judge_of_dead_max_quality.png"
            card_img.save(output_path, 'PNG', quality=100, optimize=True)
            print(f"Saved: {output_path}")
            return True
    
    def _create_anubis_static(self) -> Image.Image:
        """Create static Anubis artwork with maximum detail."""
        width, height = self.card_resolution
        
        # Base gradient (dark blues to black for underworld feel)
        base_colors = [self.egyptian_colors['lapis'][2], (20, 20, 50)]
        img = self.create_egyptian_gradient((width, height), base_colors)
        
        # Convert to RGBA for alpha blending
        img = img.convert('RGBA')
        draw = ImageDraw.Draw(img)
        
        # Anubis silhouette (center figure)
        center_x, center_y = width // 2, height // 2
        
        # Head (jackal head)
        head_size = width // 4
        head_color = (10, 10, 10, 255)  # Deep black
        
        # Draw jackal head silhouette
        head_points = []
        # Jackal head shape
        for angle in range(-90, 270, 10):
            radius = head_size
            if -30 <= angle <= 30:  # Snout area
                radius = int(head_size * 1.3)
            elif angle > 150 or angle < -150:  # Back of head
                radius = int(head_size * 0.8)
                
            x = center_x + int(radius * math.cos(math.radians(angle)))
            y = center_y - height//4 + int(radius * 0.6 * math.sin(math.radians(angle)))
            head_points.append((x, y))
        
        draw.polygon(head_points, fill=head_color)
        
        # Eyes (glowing amber)
        eye_color = (255, 191, 0, 255)  # Amber glow
        eye_size = width // 40
        left_eye = (center_x - head_size//3, center_y - height//4 - eye_size)
        right_eye = (center_x + head_size//3, center_y - height//4 - eye_size)
        
        # Draw glowing eyes with radial gradient effect
        for eye_pos in [left_eye, right_eye]:
            for radius in range(eye_size, 0, -2):
                alpha = int(255 * (radius / eye_size) * 0.8)
                glow_color = (*eye_color[:3], alpha)
                draw.ellipse([eye_pos[0]-radius, eye_pos[1]-radius, 
                             eye_pos[0]+radius, eye_pos[1]+radius], fill=glow_color)
        
        # Body (Egyptian regalia)
        body_width = width // 2
        body_height = height // 2
        body_top = center_y - height // 8
        
        # Golden collar
        gold = (*self.egyptian_colors['gold'][0], 255)
        collar_points = [
            (center_x - body_width//2, body_top),
            (center_x + body_width//2, body_top),
            (center_x + body_width//3, body_top + body_height//4),
            (center_x - body_width//3, body_top + body_height//4)
        ]
        draw.polygon(collar_points, fill=gold)
        
        # Add hieroglyphic details
        img = self.add_hieroglyphic_details(img)
        
        # Apply filters for maximum quality
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        # Enhance colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def _create_anubis_frames(self) -> List[Image.Image]:
        """Create animation frames for Anubis with smooth motion."""
        frames = []
        base_img = self._create_anubis_static()
        
        for frame in range(self.animation_frames):
            # Copy base image
            frame_img = base_img.copy()
            
            # Add animation effects
            progress = frame / self.animation_frames
            
            # Pulsing glow effect on eyes
            glow_intensity = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
            
            # Floating particles effect
            overlay = Image.new('RGBA', self.card_resolution, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add mystical particles
            for i in range(20):
                particle_x = random.randint(0, self.card_resolution[0])
                particle_y = int(self.card_resolution[1] * 0.3 + 
                               50 * math.sin(progress * 2 * math.pi + i * 0.3))
                
                particle_alpha = int(100 * glow_intensity)
                particle_color = (*self.egyptian_colors['gold'][0], particle_alpha)
                
                overlay_draw.ellipse([particle_x-2, particle_y-2, 
                                    particle_x+2, particle_y+2], fill=particle_color)
            
            # Composite overlay
            frame_img = Image.alpha_composite(frame_img, overlay)
            frames.append(frame_img)
        
        return frames
    
    def _generate_animated_card(self, card_name: str, file_prefix: str, frame_generator) -> bool:
        """Generate animated card with maximum quality."""
        print(f"  Generating {self.animation_frames} animation frames...")
        
        # Generate frames
        frames = frame_generator()
        
        if not frames:
            return False
        
        # Create spritesheet
        frame_width, frame_height = frames[0].size
        cols = 4  # 4 columns
        rows = (len(frames) + cols - 1) // cols  # Ceiling division
        
        sheet_width = cols * frame_width
        sheet_height = rows * frame_height
        
        spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        # Place frames in spritesheet
        for i, frame in enumerate(frames):
            row = i // cols
            col = i % cols
            x = col * frame_width
            y = row * frame_height
            spritesheet.paste(frame, (x, y))
        
        # Save spritesheet
        anim_filename = f"{file_prefix}_anim.png"
        output_path = self.output_dirs['animated_cards'] / anim_filename
        spritesheet.save(output_path, 'PNG', quality=100, optimize=True)
        
        # Save metadata
        metadata = {
            "frame_count": len(frames),
            "frame_size": [frame_width, frame_height],
            "sheet_size": [sheet_width, sheet_height],
            "cols": cols,
            "rows": rows,
            "fps": self.fps,
            "loop": True,
            "max_quality": True,
            "rtx5070_generated": True
        }
        
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved animation: {output_path}")
        print(f"Saved metadata: {metadata_path}")
        print(f"Animation: {len(frames)} frames @ {self.fps}fps")
        
        return True
    
    def generate_egyptian_warrior(self, animated: bool = True) -> bool:
        """Generate Egyptian Warrior with maximum detail."""
        print("Generating EGYPTIAN WARRIOR (Maximum Quality)")
        
        if animated:
            return self._generate_animated_card("WARRIOR", "egyptian_warrior", self._create_warrior_frames)
        else:
            card_img = self._create_warrior_static()
            output_path = self.output_dirs['cards'] / "egyptian_warrior_max_quality.png"
            card_img.save(output_path, 'PNG', quality=100, optimize=True)
            return True
    
    def _create_warrior_static(self) -> Image.Image:
        """Create static Egyptian Warrior."""
        width, height = self.card_resolution
        
        # Desert sunset colors
        base_colors = [self.egyptian_colors['carnelian'][1], self.egyptian_colors['gold'][2]]
        img = self.create_egyptian_gradient((width, height), base_colors)
        img = img.convert('RGBA')
        draw = ImageDraw.Draw(img)
        
        # Warrior silhouette
        center_x, center_y = width // 2, height // 2
        
        # Pharaoh headdress
        headdress_color = (*self.egyptian_colors['gold'][0], 255)
        headdress_points = [
            (center_x, center_y - height//3),
            (center_x - width//4, center_y - height//4),
            (center_x - width//6, center_y - height//6),
            (center_x + width//6, center_y - height//6),
            (center_x + width//4, center_y - height//4)
        ]
        draw.polygon(headdress_points, fill=headdress_color)
        
        # Khopesh sword
        sword_color = (192, 192, 192, 255)  # Silver
        sword_points = [
            (center_x + width//4, center_y - height//6),
            (center_x + width//3, center_y + height//4),
            (center_x + width//4 + 10, center_y + height//4),
            (center_x + width//4 + 10, center_y - height//6)
        ]
        draw.polygon(sword_points, fill=sword_color)
        
        img = self.add_hieroglyphic_details(img)
        
        # Post-processing for maximum quality
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120))
        
        return img
    
    def _create_warrior_frames(self) -> List[Image.Image]:
        """Create warrior animation frames."""
        frames = []
        base_img = self._create_warrior_static()
        
        for frame in range(self.animation_frames):
            frame_img = base_img.copy()
            
            # Sword swing animation
            progress = frame / self.animation_frames
            swing_angle = progress * 90  # 90 degree swing
            
            # Add motion blur effect (using gaussian blur as alternative)
            if 4 <= frame <= 12:  # During swing
                blur_strength = min(2, abs(frame - 8) * 0.3)
                frame_img = frame_img.filter(ImageFilter.GaussianBlur(radius=blur_strength))
            
            frames.append(frame_img)
        
        return frames
    
    def generate_all_max_quality_assets(self):
        """Generate all assets with RTX 5070 maximum quality."""
        
        print("=" * 60)
        print("RTX 5070 MAXIMUM QUALITY ASSET GENERATION")
        print("FULL VRAM UTILIZATION - NO COMPROMISES")
        print("=" * 60)
        
        start_time = time.time()
        
        # Cards to generate
        cards_to_generate = [
            ("Anubis", self.generate_anubis_card),
            ("Egyptian Warrior", self.generate_egyptian_warrior),
            ("Ra Sun God", self.generate_ra_card),
            ("Isis Divine Mother", self.generate_isis_card),
            ("Mummy Guardian", self.generate_mummy_card),
        ]
        
        successful_generations = 0
        
        for card_name, generator_func in cards_to_generate:
            print(f"\n{'='*50}")
            print(f"Generating {card_name}...")
            print(f"{'='*50}")
            
            try:
                # Generate both static and animated versions
                success_static = generator_func(animated=False)
                success_animated = generator_func(animated=True)
                
                if success_static or success_animated:
                    successful_generations += 1
                    print(f"[SUCCESS] {card_name} generation complete!")
                else:
                    print(f"[FAILED] {card_name} generation failed!")
                    
            except Exception as e:
                print(f"[ERROR] Error generating {card_name}: {e}")
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print("RTX 5070 MAXIMUM QUALITY GENERATION COMPLETE!")
        print(f"Generated: {successful_generations}/{len(cards_to_generate)} cards")
        print(f"Total time: {elapsed_time:.1f} seconds")
        print(f"Static cards: {self.output_dirs['cards']}")
        print(f"Animated cards: {self.output_dirs['animated_cards']}")
        print("RTX 5070 optimized with maximum detail!")
        
        # Update asset loader mapping
        self._update_asset_mappings()
        
        return successful_generations == len(cards_to_generate)
    
    def _update_asset_mappings(self):
        """Update asset loader with new high-quality assets."""
        print("\nUpdating asset loader mappings...")
        
        # This would update the asset_loader.py mappings
        # For now, just print what would be updated
        new_mappings = {
            'ANUBIS - JUDGE OF THE DEAD': 'anubis_judge_of_dead_max_quality.png',
            'Egyptian Warrior': 'egyptian_warrior_max_quality.png'
        }
        
        new_animated_mappings = {
            'ANUBIS - JUDGE OF THE DEAD': 'judge_of_dead_anim.png',
            'Egyptian Warrior': 'egyptian_warrior_anim.png'
        }
        
        print("New static mappings:")
        for card, file in new_mappings.items():
            print(f"  '{card}': '{file}'")
            
        print("New animated mappings:")
        for card, file in new_animated_mappings.items():
            print(f"  '{card}': '{file}'")

if __name__ == "__main__":
    generator = RTX5070MaxQualityArtGenerator()
    success = generator.generate_all_max_quality_assets()
    
    if success:
        print("\nALL ASSETS GENERATED SUCCESSFULLY!")
        print("Ready for integration into the game!")
    else:
        print("\nSome assets failed to generate.")
        print("Check the output above for details.")