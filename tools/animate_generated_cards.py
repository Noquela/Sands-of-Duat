#!/usr/bin/env python3
"""
RTX 5070 EGYPTIAN CARD ANIMATION SYSTEM
Professional Hades-quality animation pipeline for RTX 5070 generated cards
"""

import os
import sys
import time
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

class RTX5070CardAnimator:
    """Hades-quality animation system for RTX 5070 generated Egyptian cards"""
    
    def __init__(self):
        self.base_dir = project_root
        self.input_dir = self.base_dir / "assets" / "approved_hades_quality" / "cards"
        self.output_dir = self.base_dir / "assets" / "approved_hades_quality" / "animated_cards"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Animation settings optimized for Hades-quality
        self.animation_config = {
            "frame_count": 16,         # Smooth 16-frame animations
            "fps": 12,                 # Hades-style frame rate
            "hover_amplitude": 8,      # Subtle hover effect
            "glow_intensity": 0.4,     # Egyptian mystical glow
            "particle_count": 12,      # Magical particles
            "quality_level": "maximum" # RTX 5070 maximum quality
        }
        
        print(f"[ANIMATOR] RTX 5070 Egyptian Card Animator initialized")
        print(f"[INPUT] {self.input_dir}")
        print(f"[OUTPUT] {self.output_dir}")
    
    def animate_all_cards(self) -> Dict[str, bool]:
        """Animate all RTX 5070 generated Egyptian cards"""
        
        print("\n" + "="*60)
        print("RTX 5070 EGYPTIAN CARD ANIMATION PIPELINE")
        print("HADES-QUALITY PROFESSIONAL ANIMATIONS")
        print("="*60)
        
        # Find all generated cards
        card_files = list(self.input_dir.glob("*.png"))
        
        if not card_files:
            print("[ERROR] No cards found for animation")
            return {}
        
        print(f"[FOUND] {len(card_files)} RTX 5070 cards to animate")
        
        results = {}
        successful = 0
        start_time = time.time()
        
        for i, card_file in enumerate(card_files, 1):
            card_name = card_file.stem
            print(f"\n[{i}/{len(card_files)}] [ANIMATING] {card_name}")
            print("-" * 50)
            
            success = self._animate_single_card(card_file, card_name)
            results[card_name] = success
            
            if success:
                successful += 1
                print(f"    [SUCCESS] {card_name} animation complete")
            else:
                print(f"    [FAILED] {card_name} animation failed")
        
        elapsed_time = time.time() - start_time
        
        print(f"\n" + "="*60)
        print("RTX 5070 ANIMATION PIPELINE COMPLETE")
        print("="*60)
        print(f"[TIME] Total animation time: {elapsed_time:.1f} seconds")
        print(f"[SUCCESS] Animated: {successful}/{len(card_files)} cards")
        print(f"[QUALITY] Hades-level professional animations")
        print(f"[OUTPUT] {self.output_dir}")
        
        return results
    
    def _animate_single_card(self, card_path: Path, card_name: str) -> bool:
        """Create Hades-quality animation for a single card"""
        
        try:
            # Load RTX 5070 generated card
            base_image = Image.open(card_path)
            print(f"    [LOADED] {base_image.size[0]}x{base_image.size[1]} RTX 5070 card")
            
            # Generate animation frames
            frames = self._create_hades_animation_frames(base_image, card_name)
            
            if not frames:
                print(f"    [ERROR] Failed to generate animation frames")
                return False
            
            # Create spritesheet
            spritesheet_path = self._create_spritesheet(frames, card_name)
            
            if not spritesheet_path:
                print(f"    [ERROR] Failed to create spritesheet")
                return False
            
            # Generate metadata
            metadata_path = self._create_animation_metadata(card_name, len(frames))
            
            print(f"    [SPRITESHEET] {spritesheet_path}")
            print(f"    [METADATA] {metadata_path}")
            print(f"    [FRAMES] {len(frames)} frames @ {self.animation_config['fps']}fps")
            
            return True
            
        except Exception as e:
            print(f"    [ERROR] Animation failed: {e}")
            return False
    
    def _create_hades_animation_frames(self, base_image: Image.Image, card_name: str) -> List[Image.Image]:
        """Create Hades-quality animation frames with Egyptian mystical effects"""
        
        frames = []
        frame_count = self.animation_config["frame_count"]
        
        print(f"    [GENERATING] {frame_count} Hades-quality frames...")
        
        for frame_idx in range(frame_count):
            # Animation progress (0.0 to 1.0)
            progress = frame_idx / frame_count
            
            # Create frame with base image
            frame = base_image.copy().convert('RGBA')
            width, height = frame.size
            
            # Apply Hades-style effects based on card type
            frame = self._apply_card_specific_effects(frame, card_name, progress)
            
            # Universal Hades effects
            frame = self._apply_universal_hades_effects(frame, progress)
            
            frames.append(frame)
        
        return frames
    
    def _apply_card_specific_effects(self, frame: Image.Image, card_name: str, progress: float) -> Image.Image:
        """Apply card-specific Egyptian mystical effects"""
        
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Card-specific animations
        if "anubis" in card_name.lower():
            # Death god golden aura
            frame = self._add_golden_aura(frame, progress, intensity=0.6)
            frame = self._add_shadow_particles(frame, progress)
            
        elif "ra" in card_name.lower():
            # Sun god solar flare effects
            frame = self._add_solar_flare(frame, progress)
            frame = self._add_light_rays(frame, progress)
            
        elif "isis" in card_name.lower():
            # Divine healing green magic
            frame = self._add_healing_magic(frame, progress)
            frame = self._add_floating_ankhs(frame, progress)
            
        elif "set" in card_name.lower():
            # Chaos god storm effects
            frame = self._add_chaos_lightning(frame, progress)
            frame = self._add_red_storm_particles(frame, progress)
            
        elif "warrior" in card_name.lower() or "guard" in card_name.lower():
            # Battle-ready warrior effects
            frame = self._add_bronze_gleam(frame, progress)
            frame = self._add_weapon_trail(frame, progress)
            
        elif "mummy" in card_name.lower():
            # Undead cursed effects
            frame = self._add_curse_aura(frame, progress)
            frame = self._add_bandage_wisps(frame, progress)
            
        elif "sphinx" in card_name.lower():
            # Ancient wisdom mystical effects
            frame = self._add_wisdom_glow(frame, progress)
            frame = self._add_hieroglyph_particles(frame, progress)
        
        return frame
    
    def _apply_universal_hades_effects(self, frame: Image.Image, progress: float) -> Image.Image:
        """Apply universal Hades-style effects to all cards"""
        
        # Subtle hover animation
        hover_offset = int(self.animation_config["hover_amplitude"] * 
                          math.sin(progress * 2 * math.pi))
        
        # Create new frame with hover offset
        if hover_offset != 0:
            new_frame = Image.new('RGBA', frame.size, (0, 0, 0, 0))
            new_frame.paste(frame, (0, hover_offset))
            frame = new_frame
        
        # Mystical glow pulse
        glow_strength = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
        frame = self._add_mystical_glow(frame, glow_strength)
        
        return frame
    
    def _add_golden_aura(self, frame: Image.Image, progress: float, intensity: float = 0.5) -> Image.Image:
        """Add Egyptian golden aura effect"""
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Pulsing golden glow
        pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(progress * 2 * math.pi))
        alpha = int(100 * intensity * pulse)
        
        # Draw golden aura around edges
        for i in range(20, 0, -2):
            glow_alpha = int(alpha * (i / 20))
            x1, y1 = max(0, i), max(0, i)
            x2, y2 = min(width, width-i), min(height, height-i)
            if x2 > x1 and y2 > y1:
                draw.ellipse([x1, y1, x2, y2], 
                            outline=(255, 215, 0, glow_alpha), width=2)
        
        return Image.alpha_composite(frame, overlay)
    
    def _add_solar_flare(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add Ra sun god solar flare effects"""
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Rotating solar rays
        center_x, center_y = width // 2, height // 3
        ray_length = width // 3
        ray_count = 8
        
        for i in range(ray_count):
            angle = (progress * 360 + i * (360 / ray_count)) * math.pi / 180
            end_x = max(0, min(width-1, center_x + int(ray_length * math.cos(angle))))
            end_y = max(0, min(height-1, center_y + int(ray_length * math.sin(angle))))
            
            alpha = int(120 * (0.5 + 0.5 * math.sin(progress * 4 * math.pi + i)))
            draw.line([center_x, center_y, end_x, end_y], 
                     fill=(255, 255, 0, alpha), width=3)
        
        return Image.alpha_composite(frame, overlay)
    
    def _add_healing_magic(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add Isis healing green magic effects"""
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Spiraling green healing energy
        center_x, center_y = width // 2, height // 2
        spiral_points = []
        
        for t in range(0, 360, 10):
            radius = 30 + 20 * math.sin((t + progress * 180) * math.pi / 180)
            angle = (t + progress * 180) * math.pi / 180
            x = max(0, min(width-1, center_x + int(radius * math.cos(angle))))
            y = max(0, min(height-1, center_y + int(radius * math.sin(angle))))
            spiral_points.append((x, y))
        
        # Draw healing spiral
        for i in range(len(spiral_points) - 1):
            alpha = int(150 * (1 - i / len(spiral_points)))
            if alpha > 0:
                draw.line([spiral_points[i], spiral_points[i+1]], 
                         fill=(0, 255, 100, alpha), width=2)
        
        return Image.alpha_composite(frame, overlay)
    
    def _add_chaos_lightning(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add Set chaos god lightning effects"""
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Chaotic red lightning bolts
        if int(progress * 16) % 4 == 0:  # Lightning flashes randomly
            # Create jagged lightning path
            start_x = int(width * (0.2 + 0.6 * progress))
            start_y = height // 4
            
            points = [(start_x, start_y)]
            for i in range(5):
                prev_x, prev_y = points[-1]
                next_x = max(0, min(width-1, prev_x + int(30 * (0.5 - progress + 0.5 * math.sin(i)))))
                next_y = max(0, min(height-1, prev_y + height // 8))
                points.append((next_x, next_y))
            
            # Draw lightning
            for i in range(len(points) - 1):
                alpha = int(200 * (1 - i / len(points)))
                draw.line([points[i], points[i+1]], 
                         fill=(255, 50, 50, alpha), width=4)
        
        return Image.alpha_composite(frame, overlay)
    
    def _add_shadow_particles(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add Anubis shadow particles for death god theme"""
        return self._add_generic_particles(frame, progress, (50, 0, 100, 100))  # Dark purple
    
    def _add_light_rays(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add Ra light ray effects"""
        return self._add_generic_particles(frame, progress, (255, 255, 150, 80))  # Bright yellow
    
    def _add_floating_ankhs(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add floating ankh symbols for Isis"""
        return self._add_generic_particles(frame, progress, (0, 255, 200, 120))  # Cyan
    
    def _add_red_storm_particles(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add red storm particles for Set"""
        return self._add_generic_particles(frame, progress, (255, 100, 0, 140))  # Red-orange
    
    def _add_bronze_gleam(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add bronze weapon gleam for warriors"""
        return self._add_generic_particles(frame, progress, (205, 127, 50, 100))  # Bronze color
    
    def _add_weapon_trail(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add weapon motion trail for warriors"""
        return self._add_generic_particles(frame, progress, (255, 255, 255, 60))  # White trail
    
    def _add_curse_aura(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add cursed aura for mummy"""
        return self._add_generic_particles(frame, progress, (150, 0, 150, 110))  # Purple curse
    
    def _add_bandage_wisps(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add floating bandage wisps for mummy"""
        return self._add_generic_particles(frame, progress, (200, 180, 140, 90))  # Aged bandage color
    
    def _add_wisdom_glow(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add wisdom glow for sphinx"""
        return self._add_generic_particles(frame, progress, (255, 215, 0, 100))  # Golden wisdom
    
    def _add_hieroglyph_particles(self, frame: Image.Image, progress: float) -> Image.Image:
        """Add floating hieroglyph particles for sphinx"""
        return self._add_generic_particles(frame, progress, (100, 100, 255, 80))  # Mystical blue
    
    def _add_generic_particles(self, frame: Image.Image, progress: float, color: Tuple[int, int, int, int]) -> Image.Image:
        """Add generic floating particles with specified color"""
        width, height = frame.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Generate particles
        particle_count = self.animation_config["particle_count"]
        
        for i in range(particle_count):
            # Particle position with floating motion
            base_x = (i * width) // particle_count
            base_y = height // 2 + int(50 * math.sin(i + progress * 3))
            
            # Add random variation
            offset_x = int(30 * math.sin(progress * 2 * math.pi + i))
            offset_y = int(20 * math.cos(progress * 3 * math.pi + i * 0.7))
            
            particle_x = max(0, min(width-1, base_x + offset_x))
            particle_y = max(0, min(height-1, base_y + offset_y))
            
            # Particle size varies with animation
            size = max(1, 2 + int(3 * math.sin(progress * 4 * math.pi + i)))
            
            # Draw particle with safe coordinates
            x1 = max(0, particle_x - size)
            y1 = max(0, particle_y - size)
            x2 = min(width-1, particle_x + size)
            y2 = min(height-1, particle_y + size)
            
            if x2 > x1 and y2 > y1:
                draw.ellipse([x1, y1, x2, y2], fill=color)
        
        return Image.alpha_composite(frame, overlay)
    
    def _add_mystical_glow(self, frame: Image.Image, intensity: float) -> Image.Image:
        """Add subtle mystical glow to entire card"""
        # Create glow effect by blurring and compositing
        glow = frame.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Adjust opacity based on intensity
        alpha = int(100 * intensity * self.animation_config["glow_intensity"])
        
        # Create alpha mask
        alpha_mask = Image.new('RGBA', frame.size, (0, 0, 0, alpha))
        glow = Image.alpha_composite(glow, alpha_mask)
        
        return Image.alpha_composite(frame, glow)
    
    def _create_spritesheet(self, frames: List[Image.Image], card_name: str) -> Optional[Path]:
        """Create optimized spritesheet from animation frames"""
        
        if not frames:
            return None
        
        frame_width, frame_height = frames[0].size
        cols = 4  # 4x4 grid for 16 frames
        rows = (len(frames) + cols - 1) // cols
        
        sheet_width = cols * frame_width
        sheet_height = rows * frame_height
        
        spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        # Place frames in grid
        for i, frame in enumerate(frames):
            col = i % cols
            row = i // cols
            x = col * frame_width
            y = row * frame_height
            spritesheet.paste(frame, (x, y))
        
        # Save spritesheet
        spritesheet_path = self.output_dir / f"{card_name}_animated.png"
        spritesheet.save(spritesheet_path, 'PNG', quality=100, optimize=True)
        
        return spritesheet_path
    
    def _create_animation_metadata(self, card_name: str, frame_count: int) -> Path:
        """Create animation metadata for game integration"""
        
        metadata = {
            "card_name": card_name,
            "animation_type": "hades_egyptian_mystical",
            "frame_count": frame_count,
            "fps": self.animation_config["fps"],
            "frame_size": [768, 1024],  # RTX 5070 generated size
            "sheet_cols": 4,
            "sheet_rows": (frame_count + 3) // 4,
            "loop": True,
            "quality": "hades_professional",
            "rtx5070_optimized": True,
            "effects": [
                "hover_animation",
                "mystical_glow",
                "card_specific_magic",
                "egyptian_particles"
            ],
            "generated_time": time.time(),
            "generator": "RTX5070CardAnimator"
        }
        
        metadata_path = self.output_dir / f"{card_name}_animation.json"
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata_path

def main():
    """Main animation pipeline execution"""
    
    animator = RTX5070CardAnimator()
    
    print("[START] RTX 5070 Egyptian Card Animation Pipeline")
    results = animator.animate_all_cards()
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\n[COMPLETE] Animation Results: {successful}/{total}")
    
    if successful == total:
        print("[SUCCESS] All Egyptian cards animated with Hades quality!")
        print("[READY] Animation system ready for game integration!")
        return True
    else:
        print(f"[PARTIAL] {successful} cards animated successfully")
        print("[ACTION] Check failed animations and retry if needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)