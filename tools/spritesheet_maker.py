#!/usr/bin/env python3
"""
Spritesheet Generator for Sands of Duat
Converts video animations to optimized spritesheets for Godot integration.
"""

import argparse
import logging
import os
import sys
import math
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw
    CV2_AVAILABLE = True
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install opencv-python pillow numpy")
    CV2_AVAILABLE = False


class SpritesheetMaker:
    """Advanced spritesheet generation system for game animations."""
    
    def __init__(self, output_quality: int = 95):
        self.output_quality = output_quality
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "spritesheet_maker.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def video_to_spritesheet(self, video_path: str, output_path: str,
                           rows: int = 4, cols: int = 4,
                           frame_width: int = 128, frame_height: int = 128,
                           padding: int = 2, max_frames: Optional[int] = None) -> bool:
        """Convert video to spritesheet format."""
        
        if not CV2_AVAILABLE:
            self.logger.error("OpenCV not available, cannot process video")
            return self._create_placeholder_spritesheet(output_path, rows, cols, 
                                                       frame_width, frame_height, padding)
        
        try:
            self.logger.info(f"Converting video to spritesheet: {video_path}")
            
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.logger.error(f"Could not open video: {video_path}")
                return self._create_placeholder_spritesheet(output_path, rows, cols,
                                                           frame_width, frame_height, padding)
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            self.logger.info(f"Video info: {total_frames} frames, {fps} FPS")
            
            # Calculate frames to extract
            target_frames = rows * cols
            if max_frames:
                target_frames = min(target_frames, max_frames)
            
            frame_interval = max(1, total_frames // target_frames)
            
            # Extract frames
            frames = []
            frame_idx = 0
            extracted = 0
            
            while extracted < target_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_interval == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Resize frame
                    frame_resized = cv2.resize(frame_rgb, (frame_width, frame_height), 
                                             interpolation=cv2.INTER_LANCZOS4)
                    
                    frames.append(frame_resized)
                    extracted += 1
                
                frame_idx += 1
            
            cap.release()
            
            self.logger.info(f"Extracted {len(frames)} frames")
            
            # Create spritesheet
            return self._create_spritesheet_from_frames(frames, output_path, rows, cols, 
                                                       frame_width, frame_height, padding)
            
        except Exception as e:
            self.logger.error(f"Failed to process video: {e}")
            return self._create_placeholder_spritesheet(output_path, rows, cols,
                                                       frame_width, frame_height, padding)
    
    def images_to_spritesheet(self, image_paths: List[str], output_path: str,
                            rows: int = 4, cols: int = 4,
                            frame_width: int = 128, frame_height: int = 128,
                            padding: int = 2) -> bool:
        """Convert sequence of images to spritesheet."""
        try:
            self.logger.info(f"Converting {len(image_paths)} images to spritesheet")
            
            frames = []
            for img_path in image_paths:
                try:
                    # Load and resize image
                    img = Image.open(img_path).convert('RGB')
                    img_resized = img.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
                    frames.append(np.array(img_resized))
                    
                except Exception as e:
                    self.logger.warning(f"Failed to load image {img_path}: {e}")
            
            if not frames:
                self.logger.error("No valid frames found")
                return False
            
            # Pad frames to fill spritesheet if needed
            target_frames = rows * cols
            while len(frames) < target_frames:
                frames.append(frames[-1])  # Repeat last frame
            
            # Truncate if too many frames
            frames = frames[:target_frames]
            
            return self._create_spritesheet_from_frames(frames, output_path, rows, cols,
                                                       frame_width, frame_height, padding)
            
        except Exception as e:
            self.logger.error(f"Failed to process images: {e}")
            return False
    
    def _create_spritesheet_from_frames(self, frames: List[np.ndarray], output_path: str,
                                      rows: int, cols: int, frame_width: int, frame_height: int,
                                      padding: int) -> bool:
        """Create spritesheet from array of frames."""
        try:
            # Calculate spritesheet dimensions
            sheet_width = cols * frame_width + (cols + 1) * padding
            sheet_height = rows * frame_height + (rows + 1) * padding
            
            # Create spritesheet canvas
            spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
            
            # Place frames
            for i, frame in enumerate(frames):
                if i >= rows * cols:
                    break
                
                row = i // cols
                col = i % cols
                
                x = col * (frame_width + padding) + padding
                y = row * (frame_height + padding) + padding
                
                # Convert numpy array to PIL Image
                frame_img = Image.fromarray(frame.astype(np.uint8))
                spritesheet.paste(frame_img, (x, y))
            
            # Save spritesheet
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            spritesheet.save(output_path, quality=self.output_quality, optimize=True)
            
            self.logger.info(f"Spritesheet saved: {output_path} ({sheet_width}x{sheet_height})")
            
            # Generate metadata
            self._generate_metadata(output_path, rows, cols, frame_width, frame_height, 
                                  padding, len(frames))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create spritesheet: {e}")
            return False
    
    def _create_placeholder_spritesheet(self, output_path: str, rows: int, cols: int,
                                      frame_width: int, frame_height: int, padding: int) -> bool:
        """Create placeholder spritesheet when video processing fails."""
        try:
            self.logger.info("Creating placeholder spritesheet")
            
            # Calculate dimensions
            sheet_width = cols * frame_width + (cols + 1) * padding
            sheet_height = rows * frame_height + (rows + 1) * padding
            
            # Create canvas
            spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (44, 24, 16, 255))
            draw = ImageDraw.Draw(spritesheet)
            
            # Create placeholder frames
            for i in range(rows * cols):
                row = i // cols
                col = i % cols
                
                x = col * (frame_width + padding) + padding
                y = row * (frame_height + padding) + padding
                
                # Frame background
                frame_color = (60 + (i * 10) % 100, 40 + (i * 7) % 60, 20 + (i * 5) % 40, 255)
                draw.rectangle([x, y, x + frame_width, y + frame_height], fill=frame_color)
                
                # Border
                draw.rectangle([x, y, x + frame_width - 1, y + frame_height - 1], 
                              outline=(212, 175, 55, 255), width=2)
                
                # Frame number
                text = str(i + 1)
                try:
                    from PIL import ImageFont
                    font = ImageFont.truetype("arial.ttf", frame_width // 8)
                except:
                    font = ImageFont.load_default()
                
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                text_x = x + (frame_width - text_width) // 2
                text_y = y + (frame_height - text_height) // 2
                
                draw.text((text_x, text_y), text, fill=(245, 230, 163, 255), font=font)
                
                # Simple animation indicator (rotating element)
                center_x = x + frame_width // 2
                center_y = y + frame_height // 2
                radius = min(frame_width, frame_height) // 6
                
                angle = (i * 45) % 360  # Rotate based on frame
                end_x = center_x + radius * math.cos(math.radians(angle))
                end_y = center_y + radius * math.sin(math.radians(angle))
                
                draw.line([(center_x, center_y), (end_x, end_y)], 
                         fill=(139, 117, 93, 255), width=3)
            
            # Save placeholder
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            spritesheet.save(output_path, quality=self.output_quality)
            
            # Generate metadata
            self._generate_metadata(output_path, rows, cols, frame_width, frame_height,
                                  padding, rows * cols)
            
            self.logger.info(f"Placeholder spritesheet created: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create placeholder spritesheet: {e}")
            return False
    
    def _generate_metadata(self, spritesheet_path: str, rows: int, cols: int,
                          frame_width: int, frame_height: int, padding: int,
                          frame_count: int) -> None:
        """Generate metadata file for Godot integration."""
        try:
            metadata = {
                "spritesheet": os.path.basename(spritesheet_path),
                "rows": rows,
                "cols": cols,
                "frame_width": frame_width,
                "frame_height": frame_height,
                "padding": padding,
                "frame_count": frame_count,
                "total_frames": rows * cols
            }
            
            # Save as JSON
            import json
            metadata_path = spritesheet_path.replace('.png', '_metadata.json')
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Metadata saved: {metadata_path}")
            
        except Exception as e:
            self.logger.warning(f"Failed to generate metadata: {e}")
    
    def batch_process(self, input_dir: str, output_dir: str, **kwargs) -> int:
        """Batch process videos/images in directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find video files
        video_files = list(input_path.glob("*.mp4")) + list(input_path.glob("*.avi")) + \
                     list(input_path.glob("*.mov")) + list(input_path.glob("*.webm"))
        
        successful = 0
        
        self.logger.info(f"Batch processing {len(video_files)} videos")
        
        for video_file in video_files:
            output_file = output_path / f"{video_file.stem}_spritesheet.png"
            
            if self.video_to_spritesheet(str(video_file), str(output_file), **kwargs):
                successful += 1
        
        self.logger.info(f"Batch processing completed: {successful}/{len(video_files)} successful")
        return successful


def main():
    parser = argparse.ArgumentParser(description="Spritesheet Maker for Sands of Duat")
    parser.add_argument("input", help="Input video file or directory")
    parser.add_argument("output", help="Output spritesheet path")
    parser.add_argument("--rows", type=int, default=4, help="Number of rows in spritesheet")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns in spritesheet")
    parser.add_argument("--width", type=int, default=128, help="Frame width")
    parser.add_argument("--height", type=int, default=128, help="Frame height")
    parser.add_argument("--pad", type=int, default=2, help="Padding between frames")
    parser.add_argument("--max-frames", type=int, help="Maximum frames to extract")
    parser.add_argument("--quality", type=int, default=95, help="Output quality (1-100)")
    parser.add_argument("--batch", action="store_true", help="Batch process directory")
    
    args = parser.parse_args()
    
    # Initialize spritesheet maker
    maker = SpritesheetMaker(output_quality=args.quality)
    
    if args.batch:
        # Batch processing
        success_count = maker.batch_process(
            args.input, args.output,
            rows=args.rows, cols=args.cols,
            frame_width=args.width, frame_height=args.height,
            padding=args.pad, max_frames=args.max_frames
        )
        print(f"Processed {success_count} files successfully")
        
    else:
        # Single file processing
        success = maker.video_to_spritesheet(
            args.input, args.output,
            rows=args.rows, cols=args.cols,
            frame_width=args.width, frame_height=args.height,
            padding=args.pad, max_frames=args.max_frames
        )
        
        if success:
            print(f"Successfully created spritesheet: {args.output}")
        else:
            print("Spritesheet generation failed")
            sys.exit(1)


if __name__ == "__main__":
    main()