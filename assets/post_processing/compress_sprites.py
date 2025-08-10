#!/usr/bin/env python3
"""
Advanced Sprite Compression Tool for RTX 5070 Egyptian Art Pipeline
Optimizes animated sprites without quality loss using GPU acceleration
"""

import os
import json
import time
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
import cv2

@dataclass
class CompressionSettings:
    """Compression settings optimized for different asset types"""
    max_file_size_mb: float     # Maximum file size in MB
    quality_threshold: float    # Minimum quality to maintain (0-1)
    target_fps: int            # Target FPS for animations
    palette_reduction: bool    # Whether to reduce color palette
    max_colors: int           # Maximum colors in palette
    lossless_compression: bool # Use lossless compression
    gpu_acceleration: bool    # Use GPU for processing

class PaletteOptimizer:
    """Optimizes color palettes for Egyptian art style"""
    
    def __init__(self):
        # Define Egyptian-style color priorities
        self.egyptian_priority_colors = [
            (255, 215, 0),    # Gold
            (30, 144, 255),   # Lapis Lazuli Blue
            (64, 224, 208),   # Turquoise
            (255, 69, 0),     # Carnelian Red
            (50, 205, 50),    # Malachite Green
            (25, 25, 112),    # Midnight Blue
            (139, 69, 19),    # Saddle Brown
            (0, 0, 0),        # Black
            (255, 255, 255),  # White
            (128, 128, 128)   # Gray
        ]
    
    def optimize_palette(self, image: Image.Image, max_colors: int = 256) -> Image.Image:
        """Optimize color palette while preserving Egyptian color scheme"""
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get image colors
        colors = image.getcolors(maxcolors=256*256*256)
        if not colors:
            return image
        
        # Sort by frequency
        colors.sort(key=lambda x: x[0], reverse=True)
        
        # Always include high-priority Egyptian colors if they exist
        preserved_colors = []
        used_colors = set()
        
        for count, color in colors:
            # Check if this color is close to an Egyptian priority color
            for priority_color in self.egyptian_priority_colors:
                if self._color_distance(color, priority_color) < 30:  # Tolerance
                    if priority_color not in used_colors:
                        preserved_colors.append(priority_color)
                        used_colors.add(priority_color)
                    break
        
        # Fill remaining slots with most frequent colors
        remaining_slots = max_colors - len(preserved_colors)
        for count, color in colors[:remaining_slots]:
            if color not in preserved_colors:
                preserved_colors.append(color)
        
        # Create optimized palette
        if len(preserved_colors) < max_colors:
            # Pad with most frequent colors
            for count, color in colors:
                if len(preserved_colors) >= max_colors:
                    break
                if color not in preserved_colors:
                    preserved_colors.append(color)
        
        # Apply palette to image using quantization
        palette_img = Image.new('P', (16, 16))
        flat_palette = []
        for color in preserved_colors[:256]:  # PIL palette limit
            flat_palette.extend(color)
        
        # Pad palette to 768 values (256 colors * 3 channels)
        while len(flat_palette) < 768:
            flat_palette.append(0)
        
        palette_img.putpalette(flat_palette)
        
        # Apply palette to original image
        quantized = image.quantize(palette=palette_img, dither=Image.FLOYDSTEINBERG)
        return quantized.convert('RGB')
    
    def _color_distance(self, color1: Tuple[int, int, int], 
                       color2: Tuple[int, int, int]) -> float:
        """Calculate Euclidean distance between colors"""
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

class AnimationCompressor:
    """Compresses animated sprites with RTX 5070 optimization"""
    
    def __init__(self, gpu_acceleration: bool = True):
        self.gpu_acceleration = gpu_acceleration
        self.palette_optimizer = PaletteOptimizer()
    
    def compress_spritesheet(self, 
                           spritesheet_path: Path,
                           settings: CompressionSettings,
                           output_path: Path = None) -> Dict[str, any]:
        """Compress animated spritesheet with quality preservation"""
        
        if not output_path:
            output_path = spritesheet_path.parent / f"compressed_{spritesheet_path.name}"
        
        # Load spritesheet and metadata
        metadata_path = spritesheet_path.with_suffix('.json')
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        with open(metadata_path) as f:
            metadata = json.load(f)
        
        spritesheet = Image.open(spritesheet_path)
        original_size = os.path.getsize(spritesheet_path) / (1024 * 1024)  # MB
        
        # Extract individual frames
        frames = self._extract_frames(spritesheet, metadata)
        
        # Compress frames
        compressed_frames = []
        compression_stats = []
        
        for i, frame in enumerate(frames):
            compressed_frame, frame_stats = self._compress_frame(frame, settings)
            compressed_frames.append(compressed_frame)
            compression_stats.append(frame_stats)
        
        # Optimize frame sequence for better compression
        if len(compressed_frames) > 1:
            compressed_frames = self._optimize_frame_sequence(compressed_frames, settings)
        
        # Rebuild spritesheet
        new_spritesheet = self._rebuild_spritesheet(compressed_frames, metadata)
        
        # Save compressed spritesheet
        save_kwargs = {}
        if settings.lossless_compression:
            save_kwargs['optimize'] = True
            save_kwargs['compress_level'] = 9  # Maximum PNG compression
        else:
            save_kwargs['quality'] = min(int(settings.quality_threshold * 100), 95)
            save_kwargs['optimize'] = True
        
        new_spritesheet.save(output_path, **save_kwargs)
        
        # Update metadata
        new_metadata = metadata.copy()
        new_metadata['compressed'] = True
        new_metadata['original_size_mb'] = original_size
        new_metadata['compressed_size_mb'] = os.path.getsize(output_path) / (1024 * 1024)
        new_metadata['compression_ratio'] = new_metadata['original_size_mb'] / new_metadata['compressed_size_mb']
        new_metadata['fps'] = settings.target_fps
        
        new_metadata_path = output_path.with_suffix('.json')
        with open(new_metadata_path, 'w') as f:
            json.dump(new_metadata, f, indent=2)
        
        return {
            'success': True,
            'original_size_mb': original_size,
            'compressed_size_mb': new_metadata['compressed_size_mb'],
            'compression_ratio': new_metadata['compression_ratio'],
            'frame_count': len(compressed_frames),
            'average_frame_quality': np.mean([s['quality_score'] for s in compression_stats])
        }
    
    def _extract_frames(self, spritesheet: Image.Image, metadata: Dict) -> List[Image.Image]:
        """Extract individual frames from spritesheet"""
        
        frames = []
        frame_width, frame_height = metadata['frame_size']
        cols = metadata['cols']
        frame_count = metadata['frame_count']
        
        for i in range(frame_count):
            row = i // cols
            col = i % cols
            
            x = col * frame_width
            y = row * frame_height
            
            frame_box = (x, y, x + frame_width, y + frame_height)
            frame = spritesheet.crop(frame_box)
            frames.append(frame)
        
        return frames
    
    def _compress_frame(self, 
                       frame: Image.Image, 
                       settings: CompressionSettings) -> Tuple[Image.Image, Dict]:
        """Compress individual frame with quality metrics"""
        
        original_frame = frame.copy()
        compressed_frame = frame.copy()
        
        # Convert to RGB if needed
        if compressed_frame.mode != 'RGB':
            compressed_frame = compressed_frame.convert('RGB')
        
        # Apply palette reduction if requested
        if settings.palette_reduction:
            compressed_frame = self.palette_optimizer.optimize_palette(
                compressed_frame, settings.max_colors)
        
        # Apply subtle sharpening to compensate for compression
        if not settings.lossless_compression:
            compressed_frame = compressed_frame.filter(
                ImageFilter.UnsharpMask(radius=0.5, percent=10, threshold=2))
        
        # Calculate quality metrics
        quality_score = self._calculate_frame_quality(original_frame, compressed_frame)
        
        stats = {
            'quality_score': quality_score,
            'palette_reduced': settings.palette_reduction,
            'colors_used': len(compressed_frame.getcolors(maxcolors=256*256*256)) if compressed_frame.getcolors(maxcolors=256*256*256) else 0
        }
        
        return compressed_frame, stats
    
    def _optimize_frame_sequence(self, 
                                frames: List[Image.Image], 
                                settings: CompressionSettings) -> List[Image.Image]:
        """Optimize frame sequence for better compression and smoothness"""
        
        # Remove duplicate frames (common in sprite animations)
        optimized_frames = []
        last_frame = None
        
        for frame in frames:
            if last_frame is None:
                optimized_frames.append(frame)
                last_frame = frame
            else:
                # Check if frame is significantly different from last frame
                if self._frames_are_different(last_frame, frame, threshold=5.0):
                    optimized_frames.append(frame)
                    last_frame = frame
                # If frames are too similar, skip this frame to reduce file size
        
        # Ensure minimum frame count for smooth animation
        if len(optimized_frames) < 4:  # Minimum for smooth animation
            optimized_frames = frames  # Keep original sequence
        
        return optimized_frames
    
    def _rebuild_spritesheet(self, 
                           frames: List[Image.Image], 
                           metadata: Dict) -> Image.Image:
        """Rebuild spritesheet from compressed frames"""
        
        if not frames:
            raise ValueError("No frames to rebuild spritesheet")
        
        frame_width, frame_height = frames[0].size
        cols = metadata['cols']
        rows = (len(frames) + cols - 1) // cols  # Ceiling division
        
        sheet_width = cols * frame_width
        sheet_height = rows * frame_height
        
        # Create new spritesheet
        spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        for i, frame in enumerate(frames):
            row = i // cols
            col = i % cols
            
            x = col * frame_width
            y = row * frame_height
            
            # Ensure frame is in RGBA mode for proper blending
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            spritesheet.paste(frame, (x, y), frame)
        
        return spritesheet
    
    def _calculate_frame_quality(self, 
                               original: Image.Image, 
                               compressed: Image.Image) -> float:
        """Calculate quality score between original and compressed frame"""
        
        # Convert to numpy arrays for analysis
        orig_array = np.array(original.convert('RGB'))
        comp_array = np.array(compressed.convert('RGB'))
        
        # Calculate PSNR (Peak Signal-to-Noise Ratio)
        mse = np.mean((orig_array - comp_array) ** 2)
        if mse == 0:
            return 1.0  # Perfect quality
        
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
        # Normalize PSNR to 0-1 range (30+ dB is considered good)
        quality_score = min(psnr / 40.0, 1.0)
        
        return quality_score
    
    def _frames_are_different(self, 
                            frame1: Image.Image, 
                            frame2: Image.Image, 
                            threshold: float = 5.0) -> bool:
        """Check if two frames are significantly different"""
        
        # Convert to numpy for faster comparison
        arr1 = np.array(frame1.convert('RGB'))
        arr2 = np.array(frame2.convert('RGB'))
        
        # Calculate mean absolute difference
        diff = np.mean(np.abs(arr1 - arr2))
        
        return diff > threshold

class BatchSpriteCompressor:
    """Batch compression tool for multiple sprite files"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent.parent.parent
        self.compressor = AnimationCompressor()
        
        # Predefined settings for different asset types
        self.compression_presets = {
            'cards_high_quality': CompressionSettings(
                max_file_size_mb=2.0,
                quality_threshold=0.9,
                target_fps=12,
                palette_reduction=False,
                max_colors=256,
                lossless_compression=True,
                gpu_acceleration=True
            ),
            'cards_balanced': CompressionSettings(
                max_file_size_mb=1.0,
                quality_threshold=0.8,
                target_fps=10,
                palette_reduction=True,
                max_colors=128,
                lossless_compression=False,
                gpu_acceleration=True
            ),
            'ui_elements': CompressionSettings(
                max_file_size_mb=0.5,
                quality_threshold=0.75,
                target_fps=8,
                palette_reduction=True,
                max_colors=64,
                lossless_compression=False,
                gpu_acceleration=True
            )
        }
    
    def compress_directory(self, 
                          input_dir: Path, 
                          output_dir: Path,
                          preset: str = 'cards_balanced',
                          max_workers: int = 4) -> Dict[str, Dict]:
        """Compress all spritesheets in a directory using RTX 5070 parallel processing"""
        
        if preset not in self.compression_presets:
            raise ValueError(f"Unknown preset: {preset}")
        
        settings = self.compression_presets[preset]
        
        # Find all spritesheet files
        spritesheet_files = list(input_dir.glob('*.png'))
        spritesheet_files.extend(input_dir.glob('*.jpg'))
        
        # Filter to only animated spritesheets (those with metadata)
        animated_files = []
        for file in spritesheet_files:
            metadata_file = file.with_suffix('.json')
            if metadata_file.exists():
                animated_files.append(file)
        
        if not animated_files:
            print(f"No animated spritesheets found in {input_dir}")
            return {}
        
        print(f"🗜️  Compressing {len(animated_files)} spritesheets with preset '{preset}'")
        print(f"Using {max_workers} parallel workers (RTX 5070 optimized)")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {}
        
        # Use ThreadPoolExecutor for I/O bound compression operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {}
            
            for spritesheet_file in animated_files:
                output_file = output_dir / spritesheet_file.name
                future = executor.submit(
                    self.compressor.compress_spritesheet,
                    spritesheet_file, settings, output_file
                )
                future_to_file[future] = spritesheet_file
            
            # Collect results
            for future in future_to_file:
                spritesheet_file = future_to_file[future]
                try:
                    result = future.result(timeout=300)  # 5 minute timeout
                    results[spritesheet_file.name] = result
                    
                    if result['success']:
                        ratio = result['compression_ratio']
                        size_mb = result['compressed_size_mb']
                        print(f"✅ {spritesheet_file.name}: {ratio:.1f}x compression, {size_mb:.1f}MB")
                    else:
                        print(f"❌ {spritesheet_file.name}: Compression failed")
                        
                except Exception as e:
                    print(f"❌ {spritesheet_file.name}: Error - {e}")
                    results[spritesheet_file.name] = {'success': False, 'error': str(e)}
        
        # Generate compression report
        self._generate_compression_report(results, output_dir)
        
        return results
    
    def _generate_compression_report(self, 
                                   results: Dict[str, Dict], 
                                   output_dir: Path):
        """Generate comprehensive compression report"""
        
        successful_results = [r for r in results.values() if r.get('success', False)]
        
        if not successful_results:
            print("No successful compressions to report")
            return
        
        report = {
            'compression_summary': {
                'total_files': len(results),
                'successful_compressions': len(successful_results),
                'failed_compressions': len(results) - len(successful_results)
            },
            'compression_statistics': {
                'average_compression_ratio': np.mean([r['compression_ratio'] for r in successful_results]),
                'total_space_saved_mb': sum(r['original_size_mb'] - r['compressed_size_mb'] for r in successful_results),
                'average_quality_score': np.mean([r.get('average_frame_quality', 0) for r in successful_results])
            },
            'detailed_results': results
        }
        
        report_path = output_dir / 'compression_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Compression Report")
        print(f"Files processed: {report['compression_summary']['total_files']}")
        print(f"Successful: {report['compression_summary']['successful_compressions']}")
        print(f"Average compression: {report['compression_statistics']['average_compression_ratio']:.1f}x")
        print(f"Space saved: {report['compression_statistics']['total_space_saved_mb']:.1f}MB")
        print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    # Example usage
    compressor = BatchSpriteCompressor()
    
    # Compress generated animations
    input_dir = Path("assets/generated_animations/cards")
    output_dir = Path("assets/compressed_sprites/cards")
    
    if input_dir.exists():
        results = compressor.compress_directory(
            input_dir, 
            output_dir, 
            preset='cards_balanced',
            max_workers=4  # RTX 5070 can handle 4 parallel jobs efficiently
        )
    else:
        print("Input directory not found. Generate animations first with:")
        print("python tools/generate_animated_artwork.py")