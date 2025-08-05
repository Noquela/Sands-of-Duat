#!/usr/bin/env python3
"""
Animation Pipeline for Sands of Duat
Handles AnimateDiff and video-to-animation conversion for game assets.
"""

import argparse
import logging
import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union

try:
    import torch
    from PIL import Image
    import cv2
    import numpy as np
    TORCH_AVAILABLE = True
except ImportError as e:
    print(f"Missing dependencies for AI animation: {e}")
    print("Install with: pip install torch pillow opencv-python numpy")
    TORCH_AVAILABLE = False


class AnimationPipeline:
    """Complete animation pipeline for Sands of Duat assets."""
    
    def __init__(self, device: str = "auto", medvram: bool = False):
        self.device = self._setup_device(device)
        self.medvram = medvram
        self.logger = self._setup_logging()
        
        # Animation presets for different character types
        self.animation_presets = {
            "character_idle": {
                "frames": 16,
                "fps": 12,
                "loop": True,
                "motion_strength": 0.3,
                "description": "Gentle breathing/idle animation"
            },
            "character_walk": {
                "frames": 16,
                "fps": 12,
                "loop": True,
                "motion_strength": 0.6,
                "description": "Walking cycle animation"
            },
            "character_attack": {
                "frames": 12,
                "fps": 15,
                "loop": False,
                "motion_strength": 0.8,
                "description": "Attack action animation"
            },
            "card_hover": {
                "frames": 8,
                "fps": 8,
                "loop": True,
                "motion_strength": 0.2,
                "description": "Subtle card hover effect"
            },
            "spell_cast": {
                "frames": 20,
                "fps": 15,
                "loop": False,
                "motion_strength": 0.9,
                "description": "Spell casting animation"
            },
            "environment_ambient": {
                "frames": 24,
                "fps": 8,
                "loop": True,
                "motion_strength": 0.4,
                "description": "Ambient environment animation"
            }
        }
        
    def _setup_device(self, device: str) -> str:
        """Setup compute device."""
        if not TORCH_AVAILABLE:
            return "cpu"
            
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        return device
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "animation_pipeline.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def animate_diff_generate(self, input_image: str, output_video: str,
                            preset: str = "character_idle",
                            custom_frames: Optional[int] = None,
                            custom_fps: Optional[int] = None) -> bool:
        """Generate animation using AnimateDiff-style approach."""
        
        if not TORCH_AVAILABLE:
            self.logger.warning("AI animation not available, creating placeholder")
            return self._create_placeholder_animation(input_image, output_video, preset)
        
        try:
            self.logger.info(f"Generating animation for {input_image} with preset '{preset}'")
            
            # Get preset configuration
            config = self.animation_presets.get(preset, self.animation_presets["character_idle"])
            frames = custom_frames or config["frames"]
            fps = custom_fps or config["fps"]
            
            # Load input image
            input_img = Image.open(input_image).convert('RGB')
            img_width, img_height = input_img.size
            
            # For now, create a simple motion animation since AnimateDiff is complex to implement
            # This would be replaced with actual AnimateDiff implementation
            return self._create_motion_animation(input_img, output_video, frames, fps, config)
            
        except Exception as e:
            self.logger.error(f"AnimateDiff generation failed: {e}")
            return self._create_placeholder_animation(input_image, output_video, preset)
    
    def viggle_generate(self, source_image: str, reference_video: str, 
                       output_video: str) -> bool:
        """Generate animation using Viggle-style motion transfer."""
        
        if not TORCH_AVAILABLE:
            self.logger.warning("AI animation not available, creating placeholder")
            return self._create_placeholder_animation(source_image, output_video, "character_walk")
        
        try:
            self.logger.info(f"Viggle motion transfer: {source_image} + {reference_video}")
            
            # Load source image
            source_img = Image.open(source_image).convert('RGB')
            
            # Load reference video
            cap = cv2.VideoCapture(reference_video)
            if not cap.isOpened():
                self.logger.error(f"Could not open reference video: {reference_video}")
                return False
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # For now, create a simplified motion transfer
            # This would be replaced with actual Viggle implementation
            return self._create_motion_transfer(source_img, output_video, frame_count, fps)
            
        except Exception as e:
            self.logger.error(f"Viggle generation failed: {e}")
            return self._create_placeholder_animation(source_image, output_video, "character_walk")
    
    def _create_motion_animation(self, source_img: Image.Image, output_path: str,
                               frames: int, fps: int, config: Dict) -> bool:
        """Create simple motion animation from static image."""
        try:
            self.logger.info(f"Creating motion animation: {frames} frames at {fps} FPS")
            
            img_array = np.array(source_img)
            height, width = img_array.shape[:2]
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            motion_strength = config.get("motion_strength", 0.5)
            
            for frame_idx in range(frames):
                # Create frame with subtle motion
                frame = img_array.copy()
                
                # Apply different motion types based on preset
                if "idle" in config.get("description", "").lower():
                    # Gentle breathing motion
                    scale_factor = 1.0 + 0.005 * motion_strength * np.sin(frame_idx * 0.3)
                    frame = self._apply_scale_motion(frame, scale_factor)
                    
                elif "walk" in config.get("description", "").lower():
                    # Walking motion (horizontal sway)
                    offset_x = int(2 * motion_strength * np.sin(frame_idx * 0.5))
                    frame = self._apply_translation_motion(frame, offset_x, 0)
                    
                elif "attack" in config.get("description", "").lower():
                    # Attack motion (forward thrust)
                    if frame_idx < frames // 2:
                        scale = 1.0 + 0.1 * motion_strength * (frame_idx / (frames // 2))
                    else:
                        scale = 1.1 * motion_strength - 0.1 * motion_strength * ((frame_idx - frames // 2) / (frames // 2))
                    frame = self._apply_scale_motion(frame, scale)
                    
                elif "hover" in config.get("description", "").lower():
                    # Floating motion
                    offset_y = int(1 * motion_strength * np.sin(frame_idx * 0.4))
                    frame = self._apply_translation_motion(frame, 0, offset_y)
                    
                else:
                    # Default gentle motion
                    offset_x = int(1 * motion_strength * np.sin(frame_idx * 0.3))
                    offset_y = int(1 * motion_strength * np.cos(frame_idx * 0.2))
                    frame = self._apply_translation_motion(frame, offset_x, offset_y)
                
                # Convert RGB to BGR for OpenCV
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            
            self.logger.info(f"Motion animation created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create motion animation: {e}")
            return False
    
    def _apply_scale_motion(self, img: np.ndarray, scale: float) -> np.ndarray:
        """Apply scaling motion to image."""
        height, width = img.shape[:2]
        
        # Create transformation matrix
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, 0, scale)
        
        # Apply transformation
        result = cv2.warpAffine(img, M, (width, height), borderMode=cv2.BORDER_REFLECT)
        return result
    
    def _apply_translation_motion(self, img: np.ndarray, offset_x: int, offset_y: int) -> np.ndarray:
        """Apply translation motion to image."""
        height, width = img.shape[:2]
        
        # Create translation matrix
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        
        # Apply transformation
        result = cv2.warpAffine(img, M, (width, height), borderMode=cv2.BORDER_REFLECT)
        return result
    
    def _create_motion_transfer(self, source_img: Image.Image, output_path: str,
                              frame_count: int, fps: int) -> bool:
        """Create motion transfer animation (simplified Viggle)."""
        try:
            self.logger.info(f"Creating motion transfer: {frame_count} frames")
            
            img_array = np.array(source_img)
            height, width = img_array.shape[:2]
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Create simple motion sequence
            for frame_idx in range(frame_count):
                frame = img_array.copy()
                
                # Apply motion based on frame position
                progress = frame_idx / frame_count
                
                # Walking motion simulation
                offset_x = int(5 * np.sin(progress * 4 * np.pi))  # Left-right sway
                offset_y = int(2 * np.abs(np.sin(progress * 8 * np.pi)))  # Up-down bounce
                
                frame = self._apply_translation_motion(frame, offset_x, offset_y)
                
                # Convert and write
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            
            self.logger.info(f"Motion transfer created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create motion transfer: {e}")
            return False
    
    def _create_placeholder_animation(self, input_image: str, output_path: str, 
                                    preset: str) -> bool:
        """Create placeholder animation when AI generation fails."""
        try:
            self.logger.info(f"Creating placeholder animation for {preset}")
            
            config = self.animation_presets.get(preset, self.animation_presets["character_idle"])
            frames = config["frames"]
            fps = config["fps"]
            
            # Load input image
            source_img = Image.open(input_image).convert('RGB')
            img_array = np.array(source_img)
            height, width = img_array.shape[:2]
            
            # Create video writer
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            for frame_idx in range(frames):
                frame = img_array.copy()
                
                # Add simple animation effect
                alpha = 0.8 + 0.2 * np.sin(frame_idx * 0.5)
                frame = (frame * alpha).astype(np.uint8)
                
                # Convert and write
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            
            self.logger.info(f"Placeholder animation created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create placeholder animation: {e}")
            return False
    
    def batch_animate(self, input_dir: str, output_dir: str, 
                     preset: str = "character_idle") -> int:
        """Batch animate all images in directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        image_files = list(input_path.glob("*.png")) + list(input_path.glob("*.jpg"))
        successful = 0
        
        self.logger.info(f"Batch animating {len(image_files)} images with preset '{preset}'")
        
        for img_file in image_files:
            output_file = output_path / f"{img_file.stem}_{preset}.mp4"
            
            if self.animate_diff_generate(str(img_file), str(output_file), preset):
                successful += 1
        
        self.logger.info(f"Batch animation completed: {successful}/{len(image_files)} successful")
        return successful


def main():
    parser = argparse.ArgumentParser(description="Animation Pipeline for Sands of Duat")
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--preset", default="character_idle",
                       choices=["character_idle", "character_walk", "character_attack", 
                               "card_hover", "spell_cast", "environment_ambient"],
                       help="Animation preset")
    parser.add_argument("--frames", type=int, help="Number of frames (overrides preset)")
    parser.add_argument("--fps", type=int, help="Frames per second (overrides preset)")
    parser.add_argument("--reference", help="Reference video for Viggle-style motion transfer")
    parser.add_argument("--medvram", action="store_true", help="Enable memory efficient mode")
    parser.add_argument("--batch", help="Batch process directory")
    
    args = parser.parse_args()
    
    # Initialize animation pipeline
    pipeline = AnimationPipeline(medvram=args.medvram)
    
    if args.batch:
        # Batch processing
        success_count = pipeline.batch_animate(args.batch, args.output, args.preset)
        print(f"Animated {success_count} images successfully")
        
    elif args.reference:
        # Viggle-style motion transfer
        success = pipeline.viggle_generate(args.input, args.reference, args.output)
        if success:
            print(f"Successfully created animation: {args.output}")
        else:
            print("Animation generation failed")
            sys.exit(1)
            
    else:
        # AnimateDiff-style generation
        success = pipeline.animate_diff_generate(
            args.input, args.output, args.preset, 
            args.frames, args.fps
        )
        
        if success:
            print(f"Successfully created animation: {args.output}")
        else:
            print("Animation generation failed")
            sys.exit(1)


if __name__ == "__main__":
    main()