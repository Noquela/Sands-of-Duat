"""
Image Upscaling Tool

Real-ESRGAN wrapper for upscaling AI-generated artwork with
edge enhancement and quality improvement.

Key Features:
- Real-ESRGAN 4x upscaling
- Batch processing capabilities
- Quality preservation
- Multiple model support
"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Union
import logging
from PIL import Image
import concurrent.futures
import os


class ImageUpscaler:
    """
    Image upscaling tool using Real-ESRGAN.
    
    Upscales AI-generated artwork while preserving quality
    and enhancing details for final game assets.
    """
    
    def __init__(self, realesrgan_path: Optional[Path] = None):
        self.realesrgan_path = realesrgan_path or self._find_realesrgan()
        self.logger = logging.getLogger(__name__)
        
        if not self.realesrgan_path:
            self.logger.warning("Real-ESRGAN not found. Please install Real-ESRGAN.")
    
    def upscale_image(self, input_path: Path, output_path: Path, model: str = "RealESRGAN_x4plus") -> bool:
        """Upscale a single image using Real-ESRGAN."""
        if not self.realesrgan_path:
            self.logger.error("Real-ESRGAN not available")
            return False
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Build Real-ESRGAN command
            cmd = [
                str(self.realesrgan_path),
                "-i", str(input_path),
                "-o", str(output_path),
                "-n", model,
                "-s", "4",  # 4x scale
                "-f", "png"  # Output format
            ]
            
            # Run Real-ESRGAN
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if output_path.exists():
                self.logger.info(f"Upscaled {input_path.name} -> {output_path.name}")
                return True
            else:
                self.logger.error(f"Output file not created: {output_path}")
                return False
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Real-ESRGAN failed: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error upscaling {input_path}: {e}")
            return False
    
    def batch_upscale(self, input_dir: Path, output_dir: Path, 
                     model: str = "RealESRGAN_x4plus", 
                     max_workers: int = 2) -> List[Path]:
        """Batch upscale all images in a directory."""
        input_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']:
            input_files.extend(input_dir.glob(ext))
        
        if not input_files:
            self.logger.warning(f"No images found in {input_dir}")
            return []
        
        output_dir.mkdir(parents=True, exist_ok=True)
        upscaled_files = []
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for input_file in input_files:
                output_file = output_dir / f"{input_file.stem}_upscaled.png"
                future = executor.submit(self.upscale_image, input_file, output_file, model)
                futures.append((future, output_file))
            
            # Collect results
            for future, output_file in futures:
                try:
                    if future.result():
                        upscaled_files.append(output_file)
                except Exception as e:
                    self.logger.error(f"Error in batch upscale: {e}")
        
        self.logger.info(f"Upscaled {len(upscaled_files)}/{len(input_files)} images")
        return upscaled_files
    
    def upscale_with_fallback(self, input_path: Path, output_path: Path) -> bool:
        """Upscale with PIL fallback if Real-ESRGAN fails."""
        # Try Real-ESRGAN first
        if self.upscale_image(input_path, output_path):
            return True
        
        # Fall back to PIL bicubic upscaling
        self.logger.info(f"Falling back to PIL upscaling for {input_path.name}")
        return self._pil_upscale(input_path, output_path, scale=4)
    
    def _pil_upscale(self, input_path: Path, output_path: Path, scale: int = 4) -> bool:
        """Fallback upscaling using PIL."""
        try:
            with Image.open(input_path) as img:
                # Calculate new dimensions
                new_width = img.width * scale
                new_height = img.height * scale
                
                # Upscale using high-quality resampling
                upscaled = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save with high quality
                output_path.parent.mkdir(parents=True, exist_ok=True)
                upscaled.save(output_path, "PNG", optimize=True)
                
                self.logger.info(f"PIL upscaled {input_path.name} -> {output_path.name}")
                return True
        
        except Exception as e:
            self.logger.error(f"PIL upscaling failed for {input_path}: {e}")
            return False
    
    def _find_realesrgan(self) -> Optional[Path]:
        """Try to find Real-ESRGAN executable."""
        # Common locations and names for Real-ESRGAN
        possible_names = [
            "realesrgan-ncnn-vulkan.exe",
            "realesrgan-ncnn-vulkan",
            "realesrgan.exe",
            "realesrgan"
        ]
        
        # Check if it's in PATH
        for name in possible_names:
            if shutil.which(name):
                return Path(shutil.which(name))
        
        # Check common installation directories
        possible_dirs = [
            Path.cwd() / "tools" / "Real-ESRGAN",
            Path.home() / "tools" / "Real-ESRGAN",
            Path("C:/tools/Real-ESRGAN"),
            Path("/usr/local/bin"),
            Path("/opt/Real-ESRGAN")
        ]
        
        for directory in possible_dirs:
            if directory.exists():
                for name in possible_names:
                    executable = directory / name
                    if executable.exists():
                        return executable
        
        return None
    
    def optimize_for_game(self, input_path: Path, output_path: Path, 
                         max_size: tuple = (1024, 1024)) -> bool:
        """Optimize an image for game use (resize if needed, compress)."""
        try:
            with Image.open(input_path) as img:
                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Resize if larger than max_size while maintaining aspect ratio
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    self.logger.info(f"Resized {input_path.name} to fit {max_size}")
                
                # Save with optimization
                output_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(output_path, "PNG", optimize=True, compress_level=6)
                
                self.logger.info(f"Optimized {input_path.name} for game use")
                return True
        
        except Exception as e:
            self.logger.error(f"Error optimizing {input_path}: {e}")
            return False


# CLI interface for the upscaling tool
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Upscale images for Sands of Duat")
    parser.add_argument("input", type=Path, help="Input file or directory")
    parser.add_argument("output", type=Path, help="Output file or directory")
    parser.add_argument("--model", default="RealESRGAN_x4plus", help="Real-ESRGAN model to use")
    parser.add_argument("--workers", type=int, default=2, help="Number of parallel workers")
    parser.add_argument("--optimize", action="store_true", help="Optimize for game use")
    parser.add_argument("--max-size", nargs=2, type=int, default=[1024, 1024], help="Maximum dimensions for optimization")
    
    args = parser.parse_args()
    
    upscaler = ImageUpscaler()
    
    if args.input.is_file():
        # Single file
        if args.optimize:
            success = upscaler.optimize_for_game(args.input, args.output, tuple(args.max_size))
        else:
            success = upscaler.upscale_with_fallback(args.input, args.output)
        
        if success:
            print(f"Successfully processed {args.input}")
        else:
            print(f"Failed to process {args.input}")
    
    elif args.input.is_dir():
        # Directory
        if args.optimize:
            # Optimize all images in directory
            input_files = []
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                input_files.extend(args.input.glob(ext))
            
            args.output.mkdir(parents=True, exist_ok=True)
            
            for input_file in input_files:
                output_file = args.output / f"{input_file.stem}_optimized.png"
                upscaler.optimize_for_game(input_file, output_file, tuple(args.max_size))
        else:
            # Batch upscale
            upscaled = upscaler.batch_upscale(args.input, args.output, args.model, args.workers)
            print(f"Upscaled {len(upscaled)} images")
    
    else:
        print(f"Error: {args.input} is not a valid file or directory")