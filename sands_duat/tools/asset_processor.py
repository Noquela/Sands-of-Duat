"""
Asset Processing Tool

Processes and optimizes game assets including adding papyrus overlays,
batch resizing, format conversion, and optimization for game use.

Key Features:
- Papyrus texture overlay application
- Batch image processing
- Format conversion and optimization
- Asset organization and naming
"""

from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from typing import List, Optional, Tuple, Union
import logging
import concurrent.futures
import json


class AssetProcessor:
    """
    Asset processing and optimization tool.
    
    Handles post-processing of AI-generated artwork and
    other game assets for optimal game performance.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_papyrus_overlay(self, input_path: Path, output_path: Path, 
                           overlay_path: Optional[Path] = None, 
                           opacity: float = 0.6) -> bool:
        """Add papyrus texture overlay to an image."""
        try:
            # Load the main image
            with Image.open(input_path) as main_image:
                main_image = main_image.convert('RGBA')
                
                # Create or load papyrus overlay
                if overlay_path and overlay_path.exists():
                    with Image.open(overlay_path) as overlay:
                        overlay = overlay.convert('RGBA')
                else:
                    # Generate a simple papyrus-like texture
                    overlay = self._generate_papyrus_texture(main_image.size)
                
                # Resize overlay to match main image
                if overlay.size != main_image.size:
                    overlay = overlay.resize(main_image.size, Image.Resampling.LANCZOS)
                
                # Apply opacity to overlay
                overlay_with_alpha = Image.new('RGBA', overlay.size)
                for x in range(overlay.width):
                    for y in range(overlay.height):
                        r, g, b, a = overlay.getpixel((x, y))
                        new_alpha = int(a * opacity)
                        overlay_with_alpha.putpixel((x, y), (r, g, b, new_alpha))
                
                # Composite the images
                result = Image.alpha_composite(main_image, overlay_with_alpha)
                
                # Save the result
                output_path.parent.mkdir(parents=True, exist_ok=True)
                result.save(output_path, 'PNG', optimize=True)
                
                self.logger.info(f"Added papyrus overlay to {input_path.name}")
                return True
        
        except Exception as e:
            self.logger.error(f"Error adding papyrus overlay to {input_path}: {e}")
            return False
    
    def _generate_papyrus_texture(self, size: Tuple[int, int]) -> Image.Image:
        """Generate a simple papyrus-like texture."""
        # Create a base beige/tan color
        texture = Image.new('RGBA', size, (240, 230, 200, 180))
        
        # Add some noise and variation
        # This is a simplified version - a real implementation would
        # use more sophisticated texture generation
        return texture
    
    def batch_process_papyrus(self, input_dir: Path, output_dir: Path,
                             overlay_path: Optional[Path] = None,
                             opacity: float = 0.6,
                             max_workers: int = 4) -> List[Path]:
        """Batch apply papyrus overlay to all images in a directory."""
        input_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            input_files.extend(input_dir.glob(ext))
        
        if not input_files:
            self.logger.warning(f"No images found in {input_dir}")
            return []
        
        output_dir.mkdir(parents=True, exist_ok=True)
        processed_files = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for input_file in input_files:
                output_file = output_dir / f"{input_file.stem}_papyrus.png"
                future = executor.submit(
                    self.add_papyrus_overlay, 
                    input_file, output_file, overlay_path, opacity
                )
                futures.append((future, output_file))
            
            for future, output_file in futures:
                try:
                    if future.result():
                        processed_files.append(output_file)
                except Exception as e:
                    self.logger.error(f"Error in batch papyrus processing: {e}")
        
        self.logger.info(f"Applied papyrus overlay to {len(processed_files)} images")
        return processed_files
    
    def resize_for_game(self, input_path: Path, output_path: Path,
                       target_size: Tuple[int, int] = (512, 512),
                       maintain_aspect: bool = True) -> bool:
        """Resize an image for game use."""
        try:
            with Image.open(input_path) as img:
                if maintain_aspect:
                    # Calculate size maintaining aspect ratio
                    img.thumbnail(target_size, Image.Resampling.LANCZOS)
                    
                    # Create a new image with target size and center the resized image
                    result = Image.new('RGBA', target_size, (0, 0, 0, 0))
                    offset = ((target_size[0] - img.width) // 2,
                             (target_size[1] - img.height) // 2)
                    result.paste(img, offset)
                else:
                    # Resize to exact dimensions
                    result = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Save with optimization
                output_path.parent.mkdir(parents=True, exist_ok=True)
                result.save(output_path, 'PNG', optimize=True)
                
                self.logger.info(f"Resized {input_path.name} to {target_size}")
                return True
        
        except Exception as e:
            self.logger.error(f"Error resizing {input_path}: {e}")
            return False
    
    def create_card_frames(self, input_dir: Path, output_dir: Path,
                          card_size: Tuple[int, int] = (300, 420)) -> List[Path]:
        """Create properly framed card images."""
        input_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            input_files.extend(input_dir.glob(ext))
        
        output_dir.mkdir(parents=True, exist_ok=True)
        framed_files = []
        
        for input_file in input_files:
            output_file = output_dir / f"{input_file.stem}_card.png"
            
            try:
                with Image.open(input_file) as img:
                    # Create card background
                    card = Image.new('RGBA', card_size, (20, 15, 10, 255))  # Dark brown background
                    
                    # Resize artwork to fit in card (leaving space for text)
                    art_size = (card_size[0] - 20, int(card_size[1] * 0.6))  # 60% for art
                    img_resized = img.convert('RGBA')
                    img_resized.thumbnail(art_size, Image.Resampling.LANCZOS)
                    
                    # Center the artwork in the upper portion of the card
                    art_offset = ((card_size[0] - img_resized.width) // 2, 10)
                    card.paste(img_resized, art_offset, img_resized)
                    
                    # Add a simple border
                    border_color = (139, 117, 93, 255)  # Bronze-like color
                    border_width = 3
                    
                    # Draw border (simplified)
                    for i in range(border_width):
                        # This would normally use ImageDraw for proper borders
                        pass
                    
                    card.save(output_file, 'PNG', optimize=True)
                    framed_files.append(output_file)
                    self.logger.info(f"Created card frame for {input_file.name}")
            
            except Exception as e:
                self.logger.error(f"Error creating card frame for {input_file}: {e}")
        
        return framed_files
    
    def optimize_assets(self, input_dir: Path, output_dir: Path,
                       quality: int = 85, max_size: Optional[Tuple[int, int]] = None) -> List[Path]:
        """Optimize assets for game use with compression and size limits."""
        input_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            input_files.extend(input_dir.glob(ext))
        
        output_dir.mkdir(parents=True, exist_ok=True)
        optimized_files = []
        
        for input_file in input_files:
            output_file = output_dir / f"{input_file.stem}_opt.png"
            
            try:
                with Image.open(input_file) as img:
                    # Convert to RGBA for consistency
                    img = img.convert('RGBA')
                    
                    # Resize if max_size is specified
                    if max_size and (img.width > max_size[0] or img.height > max_size[1]):
                        img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Save with optimization
                    img.save(output_file, 'PNG', optimize=True, compress_level=6)
                    
                    optimized_files.append(output_file)
                    
                    # Log size reduction
                    original_size = input_file.stat().st_size
                    new_size = output_file.stat().st_size
                    reduction = ((original_size - new_size) / original_size) * 100
                    
                    self.logger.info(f"Optimized {input_file.name}: {reduction:.1f}% size reduction")
            
            except Exception as e:
                self.logger.error(f"Error optimizing {input_file}: {e}")
        
        return optimized_files
    
    def create_asset_manifest(self, asset_dir: Path, output_path: Path) -> bool:
        """Create a manifest file listing all assets with metadata."""
        try:
            manifest = {
                "version": "1.0",
                "generated_at": str(Path(__file__).stat().st_mtime),
                "assets": {}
            }
            
            # Scan for asset files
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.wav', '*.ogg', '*.ttf']:
                for asset_file in asset_dir.rglob(ext):
                    relative_path = asset_file.relative_to(asset_dir)
                    
                    # Get file metadata
                    stat = asset_file.stat()
                    
                    manifest["assets"][str(relative_path)] = {
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "type": asset_file.suffix.lower()
                    }
                    
                    # Add image-specific metadata
                    if asset_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        try:
                            with Image.open(asset_file) as img:
                                manifest["assets"][str(relative_path)].update({
                                    "width": img.width,
                                    "height": img.height,
                                    "mode": img.mode
                                })
                        except:
                            pass
            
            # Save manifest
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"Created asset manifest: {len(manifest['assets'])} assets")
            return True
        
        except Exception as e:
            self.logger.error(f"Error creating asset manifest: {e}")
            return False


# CLI interface for asset processing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process assets for Sands of Duat")
    parser.add_argument("command", choices=["papyrus", "resize", "cards", "optimize", "manifest"])
    parser.add_argument("input", type=Path, help="Input directory")
    parser.add_argument("output", type=Path, help="Output directory or file")
    parser.add_argument("--opacity", type=float, default=0.6, help="Papyrus overlay opacity")
    parser.add_argument("--size", nargs=2, type=int, default=[512, 512], help="Target size for resize")
    parser.add_argument("--quality", type=int, default=85, help="Quality for optimization")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    
    args = parser.parse_args()
    
    processor = AssetProcessor()
    
    if args.command == "papyrus":
        processor.batch_process_papyrus(args.input, args.output, opacity=args.opacity, max_workers=args.workers)
    
    elif args.command == "resize":
        if args.input.is_file():
            processor.resize_for_game(args.input, args.output, tuple(args.size))
        else:
            for img_file in args.input.glob("*.png"):
                output_file = args.output / f"{img_file.stem}_resized.png"
                processor.resize_for_game(img_file, output_file, tuple(args.size))
    
    elif args.command == "cards":
        processor.create_card_frames(args.input, args.output, tuple(args.size))
    
    elif args.command == "optimize":
        processor.optimize_assets(args.input, args.output, args.quality, tuple(args.size) if args.size != [512, 512] else None)
    
    elif args.command == "manifest":
        processor.create_asset_manifest(args.input, args.output)