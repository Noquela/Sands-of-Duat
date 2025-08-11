"""
Egyptian Card Animation Creator
Creates animated GIF files for Egyptian cards with mystical effects.
"""

import pygame
import os
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np

class EgyptianAnimationCreator:
    """Creates mystical Egyptian card animations."""
    
    def __init__(self):
        pygame.init()
        self.animations_dir = Path("assets/animations/generated")
        self.animations_dir.mkdir(parents=True, exist_ok=True)
        
    def create_ra_solar_deity_animation(self):
        """Create animation for Ra, Solar Deity."""
        print("Creating Ra, Solar Deity animation...")
        
        frames = []
        width, height = 256, 384
        frame_count = 16
        
        for frame in range(frame_count):
            # Create frame surface
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Golden gradient background
            for y in range(height):
                ratio = y / height
                r = int(255 * (0.8 + 0.2 * math.sin(frame * 0.2)))
                g = int(200 * (0.9 + 0.1 * math.sin(frame * 0.15)))
                b = int(50 * (0.5 + 0.5 * math.sin(frame * 0.1)))
                surface.fill((r, g, b), (0, y, width, 1))
            
            # Solar disk with pulsing effect
            disk_radius = 40 + 10 * math.sin(frame * 0.3)
            solar_intensity = int(255 * (0.8 + 0.2 * math.sin(frame * 0.4)))
            pygame.draw.circle(surface, (255, solar_intensity, 0), (width//2, height//3), int(disk_radius))
            
            # Solar rays
            for i in range(8):
                angle = (i * 45) + (frame * 2)  # Rotating rays
                ray_length = 60 + 20 * math.sin(frame * 0.2 + i)
                start_x = width//2 + math.cos(math.radians(angle)) * disk_radius
                start_y = height//3 + math.sin(math.radians(angle)) * disk_radius
                end_x = width//2 + math.cos(math.radians(angle)) * ray_length
                end_y = height//3 + math.sin(math.radians(angle)) * ray_length
                pygame.draw.line(surface, (255, 220, 0), (start_x, start_y), (end_x, end_y), 3)
            
            # Floating hieroglyphs
            for i in range(6):
                glyph_x = 50 + (i * 30) + 10 * math.sin(frame * 0.1 + i)
                glyph_y = height - 80 + 5 * math.cos(frame * 0.15 + i)
                alpha = int(150 + 50 * math.sin(frame * 0.2 + i))
                pygame.draw.circle(surface, (255, 215, 0, alpha), (int(glyph_x), int(glyph_y)), 3)
            
            # Convert to PIL Image
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        # Save as GIF
        output_path = self.animations_dir / "ra_solar_deity.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def create_anubis_judge_animation(self):
        """Create animation for Anubis, Judge of the Dead."""
        print("Creating Anubis, Judge of the Dead animation...")
        
        frames = []
        width, height = 256, 384
        frame_count = 16
        
        for frame in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Dark underworld gradient
            for y in range(height):
                ratio = y / height
                r = int(50 * (0.6 + 0.4 * math.sin(frame * 0.1)))
                g = int(20 * (0.7 + 0.3 * math.sin(frame * 0.12)))
                b = int(80 * (0.8 + 0.2 * math.sin(frame * 0.08)))
                surface.fill((r, g, b), (0, y, width, 1))
            
            # Purple underworld energy
            energy_radius = 30 + 15 * math.sin(frame * 0.25)
            energy_alpha = int(180 + 50 * math.sin(frame * 0.3))
            pygame.draw.circle(surface, (128, 0, 128, energy_alpha), (width//2, height//2), int(energy_radius))
            
            # Swirling mummification wraps
            for i in range(4):
                wrap_angle = (frame * 3 + i * 90) % 360
                wrap_x = width//2 + 40 * math.cos(math.radians(wrap_angle))
                wrap_y = height//2 + 40 * math.sin(math.radians(wrap_angle))
                pygame.draw.circle(surface, (200, 180, 120), (int(wrap_x), int(wrap_y)), 8)
            
            # Floating scales of justice
            scale_y = height//3 + 5 * math.sin(frame * 0.2)
            pygame.draw.rect(surface, (255, 215, 0), (width//2 - 30, int(scale_y), 60, 4))
            
            # Convert to PIL
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        output_path = self.animations_dir / "anubis_judge_of_the_dead.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=120,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def create_isis_mother_goddess_animation(self):
        """Create animation for Isis, Mother Goddess."""
        print("Creating Isis, Mother Goddess animation...")
        
        frames = []
        width, height = 256, 384
        frame_count = 16
        
        for frame in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Gentle blue healing gradient
            for y in range(height):
                ratio = y / height
                r = int(30 * (0.8 + 0.2 * math.sin(frame * 0.1)))
                g = int(100 * (0.9 + 0.1 * math.sin(frame * 0.12)))
                b = int(200 * (0.9 + 0.1 * math.sin(frame * 0.08)))
                surface.fill((r, g, b), (0, y, width, 1))
            
            # Healing aura
            aura_radius = 50 + 20 * math.sin(frame * 0.2)
            aura_alpha = int(100 + 50 * math.sin(frame * 0.3))
            pygame.draw.circle(surface, (0, 150, 255, aura_alpha), (width//2, height//2), int(aura_radius))
            
            # Protective wings (simplified)
            wing_span = 80 + 10 * math.sin(frame * 0.15)
            wing_y = height//2 - 20
            pygame.draw.ellipse(surface, (200, 200, 255), 
                              (width//2 - wing_span//2, wing_y - 20, wing_span, 40))
            
            # Floating ankh symbols
            for i in range(3):
                ankh_x = 60 + (i * 60) + 8 * math.sin(frame * 0.1 + i)
                ankh_y = height - 60 + 4 * math.cos(frame * 0.12 + i)
                pygame.draw.circle(surface, (255, 255, 255), (int(ankh_x), int(ankh_y)), 4)
                pygame.draw.rect(surface, (255, 255, 255), (int(ankh_x-2), int(ankh_y), 4, 15))
            
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        output_path = self.animations_dir / "isis_mother_goddess.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=110,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def create_set_chaos_lord_animation(self):
        """Create animation for Set, Lord of Chaos."""
        print("Creating Set, Lord of Chaos animation...")
        
        frames = []
        width, height = 256, 384
        frame_count = 20
        
        for frame in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Chaotic storm gradient
            for y in range(height):
                ratio = y / height
                chaos_factor = 0.3 * random.random()
                r = int((120 + chaos_factor * 100) * (0.8 + 0.2 * math.sin(frame * 0.2)))
                g = int((40 + chaos_factor * 60) * (0.7 + 0.3 * math.sin(frame * 0.15)))
                b = int((60 + chaos_factor * 80) * (0.6 + 0.4 * math.sin(frame * 0.1)))
                surface.fill((r, g, b), (0, y, width, 1))
            
            # Lightning bolts
            if frame % 4 == 0:  # Occasional lightning
                for i in range(2):
                    start_x = random.randint(20, width-20)
                    start_y = random.randint(20, 50)
                    end_x = start_x + random.randint(-40, 40)
                    end_y = start_y + random.randint(80, 120)
                    pygame.draw.line(surface, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)
            
            # Swirling chaos energy
            chaos_radius = 35 + 25 * abs(math.sin(frame * 0.4))
            pygame.draw.circle(surface, (255, 50, 50, 150), (width//2, height//2), int(chaos_radius))
            
            # Desert sand particles
            for i in range(8):
                sand_x = random.randint(0, width)
                sand_y = random.randint(height//2, height)
                sand_size = random.randint(1, 3)
                pygame.draw.circle(surface, (220, 180, 120), (sand_x, sand_y), sand_size)
            
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        output_path = self.animations_dir / "set_lord_of_chaos.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=80,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def create_spell_animations(self):
        """Create spell effect animations."""
        print("Creating spell animations...")
        
        # Solar Flare
        frames = []
        width, height = 256, 384
        frame_count = 12
        
        for frame in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Energy buildup
            energy_intensity = frame / frame_count
            flare_radius = int(20 * energy_intensity + 10 * math.sin(frame * 0.5))
            
            # Central energy core
            pygame.draw.circle(surface, (255, 255, 0), (width//2, height//2), flare_radius)
            
            # Radiating energy waves
            for wave in range(3):
                wave_radius = flare_radius + (wave * 20) + (frame * 5)
                if wave_radius < width:
                    alpha = int(255 * (1 - energy_intensity) * 0.3)
                    pygame.draw.circle(surface, (255, 200, 0, alpha), (width//2, height//2), wave_radius, 2)
            
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        output_path = self.animations_dir / "solar_flare_spell.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=60,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def create_artifact_animations(self):
        """Create artifact animations."""
        print("Creating artifact animations...")
        
        # Ankh of Eternity
        frames = []
        width, height = 256, 384
        frame_count = 16
        
        for frame in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Eternal energy background
            for y in range(height):
                ratio = y / height
                r = int(40 * (0.8 + 0.2 * math.sin(frame * 0.1 + ratio)))
                g = int(100 * (0.9 + 0.1 * math.sin(frame * 0.12 + ratio)))
                b = int(160 * (0.9 + 0.1 * math.sin(frame * 0.08 + ratio)))
                surface.fill((r, g, b), (0, y, width, 1))
            
            # Ankh symbol (simplified)
            ankh_glow = int(200 + 55 * math.sin(frame * 0.3))
            
            # Ankh circle (top)
            pygame.draw.circle(surface, (255, 215, 0), (width//2, height//2 - 30), 25, 4)
            
            # Ankh cross (body)
            pygame.draw.line(surface, (255, 215, 0), 
                           (width//2, height//2 - 5), (width//2, height//2 + 50), 6)
            pygame.draw.line(surface, (255, 215, 0), 
                           (width//2 - 25, height//2 + 10), (width//2 + 25, height//2 + 10), 6)
            
            # Pulsing energy around ankh
            pulse_radius = 60 + 20 * math.sin(frame * 0.4)
            pygame.draw.circle(surface, (255, 255, 255, 50), (width//2, height//2), int(pulse_radius))
            
            pil_image = self._pygame_to_pil(surface)
            frames.append(pil_image)
        
        output_path = self.animations_dir / "ankh_of_eternity.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        print(f"Saved: {output_path}")
    
    def _pygame_to_pil(self, surface):
        """Convert pygame surface to PIL Image."""
        # Get the RGBA array from pygame surface
        rgba_array = pygame.surfarray.array3d(surface)
        rgba_array = np.transpose(rgba_array, (1, 0, 2))
        
        # Create PIL Image
        return Image.fromarray(rgba_array, 'RGB')
    
    def create_all_animations(self):
        """Create all Egyptian card animations."""
        print("Creating Egyptian Card Animations...")
        print("=" * 50)
        
        self.create_ra_solar_deity_animation()
        self.create_anubis_judge_animation()
        self.create_isis_mother_goddess_animation()
        self.create_set_chaos_lord_animation()
        self.create_spell_animations()
        self.create_artifact_animations()
        
        print("=" * 50)
        print("All Egyptian card animations created!")
        print(f"Location: {self.animations_dir}")

def main():
    """Main function to create animations."""
    creator = EgyptianAnimationCreator()
    creator.create_all_animations()

if __name__ == "__main__":
    main()