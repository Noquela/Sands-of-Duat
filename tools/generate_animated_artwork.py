#!/usr/bin/env python3
"""
Animated Egyptian Art Generation Pipeline for RTX 5070
Generates high-quality 2D animated sprites with Hades-Egyptian style
"""

import os
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import requests
import threading
from concurrent.futures import ThreadPoolExecutor

class EgyptianAnimationPrompts:
    """Library of prompts for animated Egyptian artwork"""
    
    BASE_STYLE = "sands_of_duat_style, egyptian_underworld_art, hades_game_art_quality, hand_painted_texture, vibrant_rich_colors, dramatic_contrasts"
    NEGATIVE = "blurry, low quality, pixelated, modern, realistic photo, 3d render, static, stiff, unanimated"
    
    CARD_ANIMATIONS = {
        'legendary_gods': {
            'Anubis': [
                "Anubis raising divine scales, golden light emanating, fluid motion",
                "Anubis wielding crook and flail, dynamic pose, divine authority",
                "Anubis transforming into jackal form, mystical energy swirls",
                "Anubis opening underworld portal, reality warping effects"
            ],
            'Isis': [
                "Isis spreading healing wings, feathers flowing gracefully",
                "Isis channeling life magic, green energy spirals around hands",
                "Isis protecting with divine shield, radiant aura expanding",
                "Isis commanding wind currents, fabric and hair flowing"
            ],
            'Ra': [
                "Ra rising as solar disk, brilliant rays of light spreading",
                "Ra commanding solar barque, flames dancing around figure",
                "Ra transforming daylight to dusk, color transitions flowing",
                "Ra unleashing solar fury, energy waves rippling outward"
            ]
        },
        'epic_warriors': {
            'Egyptian Warrior': [
                "Egyptian warrior drawing khopesh sword, metal gleaming",
                "Warrior charging with spear thrust, dynamic action pose",
                "Warrior defending with bronze shield, armor plates shifting",
                "Warrior summoning battle fury, aura intensifying"
            ],
            'Pharaoh Guard': [
                "Guard marching in formation, synchronized movement",
                "Guard striking with ceremonial weapon, precise technique",
                "Guard activating protective ward, magical barriers forming",
                "Guard saluting pharaoh, respectful bow animation"
            ]
        },
        'rare_guardians': {
            'Mummy Guardian': [
                "Mummy unwrapping bandages, ancient power awakening",
                "Guardian shuffling forward, ominous presence approaching",
                "Mummy casting curse spell, dark energy tendrils writhing",
                "Guardian protecting sacred tomb, defensive stance"
            ],
            'Sphinx Guardian': [
                "Sphinx solving riddle, eyes glowing with wisdom",
                "Guardian spreading wings, preparing for flight",
                "Sphinx casting judgment, divine authority radiating",
                "Guardian prowling territory, predatory grace"
            ]
        }
    }
    
    BACKGROUND_ANIMATIONS = {
        'temple_interior': [
            "flickering torch flames casting dancing shadows",
            "hieroglyphs glowing with ancient magic",
            "sand particles drifting through sunbeams",
            "mysterious mist swirling around pillars"
        ],
        'underworld_realm': [
            "souls floating through ethereal mist",
            "underworld rivers flowing with otherworldly current",
            "ghostly apparitions materializing and fading",
            "divine judgment scales slowly swaying"
        ],
        'pyramid_chamber': [
            "treasure chests emanating golden light pulses",
            "ancient mechanisms slowly rotating",
            "dust motes dancing in light shafts",
            "mystical portals opening and closing"
        ]
    }

class LocalSDXLGenerator:
    """Interface for local ComfyUI/A1111 WebUI generation"""
    
    def __init__(self, endpoint: str = "http://127.0.0.1:8188", rtx5070_config: str = None):
        self.endpoint = endpoint
        self.config = self._load_rtx5070_config(rtx5070_config)
        self.session = requests.Session()
        
    def _load_rtx5070_config(self, config_path: str) -> Dict:
        """Load RTX 5070 optimized configuration"""
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                return json.load(f)
        
        # Default RTX 5070 config
        return {
            "batch_size": 4,
            "resolution": [1024, 1024],
            "steps": 30,
            "cfg_scale": 8.0,
            "scheduler": "karras",
            "gpu_memory_fraction": 0.95
        }
    
    def generate_animation_frames(self, 
                                prompt: str, 
                                negative_prompt: str,
                                num_frames: int = 8,
                                animation_type: str = "card") -> List[Image.Image]:
        """Generate animation frame sequence"""
        
        frames = []
        resolution = self.config["resolution"]
        if animation_type == "background":
            resolution = [1920, 1080]
        elif animation_type == "sprite":
            resolution = [512, 512]
        
        for frame in range(num_frames):
            # Add frame-specific motion to prompt
            frame_progress = frame / (num_frames - 1)  # 0.0 to 1.0
            motion_prompt = self._generate_motion_prompt(prompt, frame_progress)
            
            # Generate single frame
            payload = {
                "prompt": motion_prompt,
                "negative_prompt": negative_prompt,
                "width": resolution[0],
                "height": resolution[1],
                "steps": self.config["steps"],
                "cfg_scale": self.config["cfg_scale"],
                "scheduler": self.config["scheduler"],
                "seed": random.randint(0, 2147483647),
                "batch_size": 1  # Generate one frame at a time for consistency
            }
            
            try:
                response = self.session.post(f"{self.endpoint}/sdapi/v1/txt2img", 
                                           json=payload, timeout=120)
                response.raise_for_status()
                
                result = response.json()
                if result.get("images"):
                    import base64
                    from io import BytesIO
                    
                    image_data = base64.b64decode(result["images"][0])
                    image = Image.open(BytesIO(image_data))
                    frames.append(image)
                    
                    print(f"Generated frame {frame + 1}/{num_frames}")
                
            except Exception as e:
                print(f"Error generating frame {frame}: {e}")
                # Use previous frame or create placeholder
                if frames:
                    frames.append(frames[-1].copy())
                else:
                    # Create placeholder frame
                    placeholder = Image.new('RGB', resolution, (64, 32, 128))
                    frames.append(placeholder)
        
        return frames
    
    def _generate_motion_prompt(self, base_prompt: str, progress: float) -> str:
        """Add motion-specific details based on animation progress"""
        motion_descriptors = [
            f"animation frame {int(progress * 10)}, smooth motion",
            f"dynamic pose transition, fluid movement",
            f"sequential animation, frame {int(progress * 8) + 1} of 8"
        ]
        
        # Add motion blur for middle frames
        if 0.2 < progress < 0.8:
            motion_descriptors.append("subtle motion blur, kinetic energy")
        
        return f"{base_prompt}, {', '.join(motion_descriptors)}"

class AnimationProcessor:
    """Post-processes generated frames into optimized animations"""
    
    def __init__(self, rtx5070_optimized: bool = True):
        self.rtx5070_optimized = rtx5070_optimized
    
    def create_spritesheet(self, frames: List[Image.Image], 
                          output_path: Path,
                          sheet_size: Tuple[int, int] = (2048, 2048)) -> bool:
        """Create optimized spritesheet from animation frames"""
        
        if not frames:
            return False
        
        frame_width, frame_height = frames[0].size
        cols = sheet_size[0] // frame_width
        rows = sheet_size[1] // frame_height
        
        if len(frames) > cols * rows:
            print(f"Warning: Too many frames ({len(frames)}) for spritesheet size")
            frames = frames[:cols * rows]
        
        # Create spritesheet
        spritesheet = Image.new('RGBA', sheet_size, (0, 0, 0, 0))
        
        for i, frame in enumerate(frames):
            row = i // cols
            col = i % cols
            x = col * frame_width
            y = row * frame_height
            
            # Paste frame with alpha blending
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            spritesheet.paste(frame, (x, y), frame)
        
        # Save with optimization
        spritesheet.save(output_path, 'PNG', optimize=True)
        
        # Generate metadata
        metadata = {
            "frame_count": len(frames),
            "frame_size": [frame_width, frame_height],
            "sheet_size": sheet_size,
            "cols": cols,
            "rows": rows,
            "fps": 12,  # Recommended for card animations
            "loop": True
        }
        
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def optimize_frames(self, frames: List[Image.Image]) -> List[Image.Image]:
        """Apply RTX 5070 optimized post-processing"""
        
        optimized_frames = []
        
        for frame in frames:
            # Convert to RGBA for better blending
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            # Enhance colors for Egyptian vibrancy
            enhancer = ImageEnhance.Color(frame)
            frame = enhancer.enhance(1.15)  # 15% color boost
            
            # Slight contrast enhancement for depth
            enhancer = ImageEnhance.Contrast(frame)
            frame = enhancer.enhance(1.05)
            
            # Subtle sharpening for crisp details
            frame = frame.filter(ImageFilter.UnsharpMask(radius=1, percent=15))
            
            optimized_frames.append(frame)
        
        return optimized_frames

class AnimatedArtworkPipeline:
    """Main pipeline for generating animated Egyptian artwork"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.output_dir = self.base_dir / "assets" / "generated_animations"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.prompts = EgyptianAnimationPrompts()
        self.generator = LocalSDXLGenerator()
        self.processor = AnimationProcessor()
        
        # Quality validation metrics
        self.quality_threshold = 0.75
        
    def generate_card_animations(self, card_types: List[str] = None) -> Dict[str, bool]:
        """Generate animated card artwork"""
        
        if not card_types:
            card_types = ['legendary_gods', 'epic_warriors', 'rare_guardians']
        
        results = {}
        
        for card_type in card_types:
            if card_type not in self.prompts.CARD_ANIMATIONS:
                continue
                
            cards = self.prompts.CARD_ANIMATIONS[card_type]
            
            for card_name, animation_prompts in cards.items():
                print(f"\n🎨 Generating {card_name} animation...")
                
                success = self._generate_single_card_animation(
                    card_name, animation_prompts, card_type
                )
                
                results[f"{card_type}_{card_name}"] = success
                
                if success:
                    print(f"✅ {card_name} animation complete!")
                else:
                    print(f"❌ {card_name} animation failed")
        
        return results
    
    def _generate_single_card_animation(self, 
                                      card_name: str,
                                      animation_prompts: List[str],
                                      card_type: str) -> bool:
        """Generate animation for a single card"""
        
        try:
            # Create output directory
            card_output_dir = self.output_dir / "cards" / card_type
            card_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate frames for each animation variant
            all_frames = []
            
            for i, motion_prompt in enumerate(animation_prompts):
                full_prompt = f"{self.prompts.BASE_STYLE}, {motion_prompt}"
                
                frames = self.generator.generate_animation_frames(
                    prompt=full_prompt,
                    negative_prompt=self.prompts.NEGATIVE,
                    num_frames=8,
                    animation_type="card"
                )
                
                if frames:
                    # Optimize frames
                    frames = self.processor.optimize_frames(frames)
                    all_frames.extend(frames)
            
            if not all_frames:
                return False
            
            # Create spritesheet
            timestamp = int(time.time())
            output_path = card_output_dir / f"{card_name.lower().replace(' ', '_')}_anim_{timestamp}.png"
            
            success = self.processor.create_spritesheet(all_frames, output_path)
            
            if success:
                # Validate quality
                quality_score = self._validate_animation_quality(output_path)
                if quality_score >= self.quality_threshold:
                    # Move to approved folder
                    approved_dir = self.base_dir / "assets" / "approved_hades_quality" / "animated_cards"
                    approved_dir.mkdir(parents=True, exist_ok=True)
                    
                    final_path = approved_dir / f"{card_name.lower().replace(' ', '_')}_anim.png"
                    output_path.rename(final_path)
                    
                    # Also move metadata
                    metadata_src = output_path.with_suffix('.json')
                    metadata_dst = final_path.with_suffix('.json')
                    if metadata_src.exists():
                        metadata_src.rename(metadata_dst)
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error generating {card_name} animation: {e}")
            return False
    
    def _validate_animation_quality(self, spritesheet_path: Path) -> float:
        """Validate animation quality using RTX 5070 optimized metrics"""
        
        try:
            image = Image.open(spritesheet_path)
            
            # Convert to numpy for analysis
            img_array = np.array(image.convert('RGB'))
            
            # Metrics for Egyptian art quality
            scores = []
            
            # Color vibrancy (Egyptian art should be colorful)
            color_std = np.std(img_array)
            color_score = min(color_std / 80.0, 1.0)  # Normalize to 0-1
            scores.append(color_score)
            
            # Contrast (dramatic lighting)
            gray = np.mean(img_array, axis=2)
            contrast = np.std(gray)
            contrast_score = min(contrast / 60.0, 1.0)
            scores.append(contrast_score)
            
            # Complexity (detailed artwork)
            edges = np.gradient(gray)
            edge_density = np.mean(np.abs(edges[0]) + np.abs(edges[1]))
            complexity_score = min(edge_density / 20.0, 1.0)
            scores.append(complexity_score)
            
            # Overall quality
            final_score = np.mean(scores)
            
            print(f"Quality metrics - Color: {color_score:.2f}, Contrast: {contrast_score:.2f}, "
                  f"Complexity: {complexity_score:.2f}, Overall: {final_score:.2f}")
            
            return final_score
            
        except Exception as e:
            print(f"Quality validation error: {e}")
            return 0.0
    
    def run_full_pipeline(self):
        """Run complete animated artwork generation pipeline"""
        
        print("🏺 HADES-EGYPTIAN ANIMATED ART PIPELINE 🏺")
        print("RTX 5070 12GB VRAM - Optimized Generation")
        print("=" * 60)
        
        start_time = time.time()
        
        # Generate card animations
        print("\n📇 Generating Animated Cards...")
        card_results = self.generate_card_animations()
        
        # Generate background animations  
        print("\n🏛️ Generating Animated Backgrounds...")
        # TODO: Implement background animations
        
        # Statistics
        successful_cards = sum(1 for success in card_results.values() if success)
        total_cards = len(card_results)
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("🎉 ANIMATION GENERATION COMPLETE!")
        print(f"✅ Cards: {successful_cards}/{total_cards}")
        print(f"⏱️  Time: {elapsed_time/60:.1f} minutes")
        print(f"📁 Output: {self.output_dir}")
        print(f"✨ Approved: assets/approved_hades_quality/animated_cards/")
        
        return {
            'card_results': card_results,
            'success_rate': successful_cards / total_cards if total_cards > 0 else 0,
            'elapsed_time': elapsed_time
        }

if __name__ == "__main__":
    pipeline = AnimatedArtworkPipeline()
    results = pipeline.run_full_pipeline()
    
    print(f"\nFinal Success Rate: {results['success_rate']*100:.1f}%")