#!/usr/bin/env python3
"""
Advanced Quality Validation System for Egyptian Art Assets
RTX 5070 Optimized Analysis with Computer Vision Metrics
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageStat, ImageFilter, ImageEnhance
import cv2
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

@dataclass
class QualityMetrics:
    """Quality assessment metrics for Egyptian artwork"""
    color_vibrancy: float        # 0-1, richness of colors
    contrast_ratio: float        # 0-1, dramatic lighting
    detail_complexity: float     # 0-1, intricate details
    egyptian_authenticity: float # 0-1, style consistency
    animation_smoothness: float  # 0-1, for animated assets
    overall_score: float         # 0-1, weighted average
    
    def to_dict(self) -> Dict:
        return {
            'color_vibrancy': self.color_vibrancy,
            'contrast_ratio': self.contrast_ratio,
            'detail_complexity': self.detail_complexity,
            'egyptian_authenticity': self.egyptian_authenticity,
            'animation_smoothness': self.animation_smoothness,
            'overall_score': self.overall_score
        }

class EgyptianStyleAnalyzer:
    """Analyzes artwork for Egyptian style authenticity"""
    
    def __init__(self):
        # Egyptian color palette (HSV ranges)
        self.egyptian_colors = {
            'gold': [(15, 50, 180), (25, 255, 255)],      # Golden yellows
            'lapis': [(100, 100, 80), (130, 255, 255)],   # Deep blues
            'turquoise': [(80, 80, 150), (100, 255, 255)], # Turquoise/cyan
            'carnelian': [(0, 100, 150), (10, 255, 255)],  # Red-orange
            'malachite': [(60, 80, 50), (80, 255, 200)],   # Green
            'obsidian': [(0, 0, 0), (180, 50, 50)]         # Dark/black
        }
        
        # Hieroglyphic-like patterns (edge density thresholds)
        self.hieroglyph_patterns = {
            'geometric_shapes': 0.15,   # Regular geometric patterns
            'curved_lines': 0.25,       # Flowing organic shapes
            'fine_details': 0.35        # Intricate small elements
        }
    
    def analyze_color_authenticity(self, image: Image.Image) -> float:
        """Analyze color palette authenticity to Egyptian art"""
        
        # Convert to HSV for better color analysis
        hsv_img = image.convert('HSV')
        hsv_array = np.array(hsv_img)
        
        # Count pixels matching Egyptian color ranges
        total_pixels = hsv_array.shape[0] * hsv_array.shape[1]
        egyptian_pixel_count = 0
        
        for color_name, (lower, upper) in self.egyptian_colors.items():
            lower_bound = np.array(lower)
            upper_bound = np.array(upper)
            
            # Create mask for this color range
            mask = cv2.inRange(hsv_array, lower_bound, upper_bound)
            egyptian_pixel_count += np.sum(mask > 0)
        
        # Calculate authenticity score
        authenticity_ratio = egyptian_pixel_count / total_pixels
        return min(authenticity_ratio * 2.0, 1.0)  # Scale to 0-1 range
    
    def analyze_pattern_complexity(self, image: Image.Image) -> float:
        """Analyze hierarchical pattern complexity"""
        
        # Convert to grayscale for edge detection
        gray_img = image.convert('L')
        gray_array = np.array(gray_img)
        
        # Multi-scale edge detection (simulating hieroglyphic patterns)
        complexity_scores = []
        
        for scale in [1, 2, 4]:  # Different detail levels
            if scale > 1:
                # Resize for different scale analysis
                resized = cv2.resize(gray_array, 
                                   (gray_array.shape[1]//scale, 
                                    gray_array.shape[0]//scale))
            else:
                resized = gray_array
            
            # Sobel edge detection
            sobelx = cv2.Sobel(resized, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(resized, cv2.CV_64F, 0, 1, ksize=3)
            edge_magnitude = np.sqrt(sobelx**2 + sobely**2)
            
            # Calculate edge density
            edge_density = np.mean(edge_magnitude) / 255.0
            complexity_scores.append(edge_density)
        
        # Weight different scales (fine details matter more)
        weights = [0.2, 0.3, 0.5]  # Favor finer details
        weighted_complexity = sum(score * weight 
                                for score, weight in zip(complexity_scores, weights))
        
        return min(weighted_complexity * 3.0, 1.0)  # Scale to 0-1

class AnimationAnalyzer:
    """Analyzes animated sprite quality"""
    
    def __init__(self):
        self.motion_blur_threshold = 0.1
        self.frame_consistency_weight = 0.7
    
    def analyze_spritesheet(self, spritesheet_path: Path) -> Tuple[float, List[Image.Image]]:
        """Analyze spritesheet animation quality"""
        
        # Load spritesheet and metadata
        metadata_path = spritesheet_path.with_suffix('.json')
        if not metadata_path.exists():
            return 0.0, []
        
        with open(metadata_path) as f:
            metadata = json.load(f)
        
        # Extract individual frames
        spritesheet = Image.open(spritesheet_path)
        frames = self._extract_frames(spritesheet, metadata)
        
        if len(frames) < 2:
            return 0.0, frames
        
        # Analyze frame-to-frame consistency
        consistency_scores = []
        motion_scores = []
        
        for i in range(1, len(frames)):
            prev_frame = np.array(frames[i-1].convert('RGB'))
            curr_frame = np.array(frames[i].convert('RGB'))
            
            # Frame consistency (should be similar but not identical)
            frame_diff = np.mean(np.abs(prev_frame - curr_frame))
            consistency_score = 1.0 - min(frame_diff / 128.0, 1.0)
            consistency_scores.append(consistency_score)
            
            # Motion analysis (gradual changes indicate smooth animation)
            motion_magnitude = np.std(curr_frame - prev_frame)
            motion_score = min(motion_magnitude / 50.0, 1.0)
            motion_scores.append(motion_score)
        
        # Calculate overall animation smoothness
        avg_consistency = np.mean(consistency_scores)
        avg_motion = np.mean(motion_scores)
        
        smoothness = (avg_consistency * self.frame_consistency_weight + 
                     avg_motion * (1 - self.frame_consistency_weight))
        
        return smoothness, frames
    
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

class RTX5070QualityValidator:
    """Main quality validation system optimized for RTX 5070 workflow"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.temp_processing_dir = self.base_dir / "temp_processing"
        self.temp_processing_dir.mkdir(exist_ok=True)
        
        self.style_analyzer = EgyptianStyleAnalyzer()
        self.animation_analyzer = AnimationAnalyzer()
        
        # Quality thresholds
        self.thresholds = {
            'minimum_quality': 0.65,
            'good_quality': 0.75,
            'excellent_quality': 0.85
        }
        
        # Weights for overall score calculation
        self.weights = {
            'color_vibrancy': 0.25,
            'contrast_ratio': 0.20,
            'detail_complexity': 0.25,
            'egyptian_authenticity': 0.20,
            'animation_smoothness': 0.10  # Only for animated assets
        }
    
    def validate_single_asset(self, asset_path: Path, asset_type: str = "static") -> QualityMetrics:
        """Validate a single asset and return comprehensive metrics"""
        
        try:
            if asset_type == "animated":
                return self._validate_animated_asset(asset_path)
            else:
                return self._validate_static_asset(asset_path)
                
        except Exception as e:
            print(f"Error validating {asset_path}: {e}")
            return self._create_failed_metrics()
    
    def _validate_static_asset(self, asset_path: Path) -> QualityMetrics:
        """Validate static image asset"""
        
        image = Image.open(asset_path)
        
        # Color vibrancy analysis
        color_vibrancy = self._analyze_color_vibrancy(image)
        
        # Contrast analysis
        contrast_ratio = self._analyze_contrast(image)
        
        # Detail complexity
        detail_complexity = self.style_analyzer.analyze_pattern_complexity(image)
        
        # Egyptian style authenticity
        egyptian_authenticity = self.style_analyzer.analyze_color_authenticity(image)
        
        # Calculate overall score (no animation component for static)
        weights_static = {k: v for k, v in self.weights.items() 
                         if k != 'animation_smoothness'}
        total_weight = sum(weights_static.values())
        
        overall_score = (
            color_vibrancy * weights_static['color_vibrancy'] +
            contrast_ratio * weights_static['contrast_ratio'] +
            detail_complexity * weights_static['detail_complexity'] +
            egyptian_authenticity * weights_static['egyptian_authenticity']
        ) / total_weight
        
        return QualityMetrics(
            color_vibrancy=color_vibrancy,
            contrast_ratio=contrast_ratio,
            detail_complexity=detail_complexity,
            egyptian_authenticity=egyptian_authenticity,
            animation_smoothness=0.0,  # N/A for static assets
            overall_score=overall_score
        )
    
    def _validate_animated_asset(self, asset_path: Path) -> QualityMetrics:
        """Validate animated spritesheet asset"""
        
        # Analyze animation quality
        animation_smoothness, frames = self.animation_analyzer.analyze_spritesheet(asset_path)
        
        if not frames:
            return self._create_failed_metrics()
        
        # Analyze first frame for static qualities
        first_frame_metrics = self._validate_static_asset_from_image(frames[0])
        
        # Calculate overall score including animation
        overall_score = (
            first_frame_metrics.color_vibrancy * self.weights['color_vibrancy'] +
            first_frame_metrics.contrast_ratio * self.weights['contrast_ratio'] +
            first_frame_metrics.detail_complexity * self.weights['detail_complexity'] +
            first_frame_metrics.egyptian_authenticity * self.weights['egyptian_authenticity'] +
            animation_smoothness * self.weights['animation_smoothness']
        )
        
        return QualityMetrics(
            color_vibrancy=first_frame_metrics.color_vibrancy,
            contrast_ratio=first_frame_metrics.contrast_ratio,
            detail_complexity=first_frame_metrics.detail_complexity,
            egyptian_authenticity=first_frame_metrics.egyptian_authenticity,
            animation_smoothness=animation_smoothness,
            overall_score=overall_score
        )
    
    def _validate_static_asset_from_image(self, image: Image.Image) -> QualityMetrics:
        """Helper to validate static qualities from an Image object"""
        
        color_vibrancy = self._analyze_color_vibrancy(image)
        contrast_ratio = self._analyze_contrast(image)
        detail_complexity = self.style_analyzer.analyze_pattern_complexity(image)
        egyptian_authenticity = self.style_analyzer.analyze_color_authenticity(image)
        
        weights_static = {k: v for k, v in self.weights.items() 
                         if k != 'animation_smoothness'}
        total_weight = sum(weights_static.values())
        
        overall_score = (
            color_vibrancy * weights_static['color_vibrancy'] +
            contrast_ratio * weights_static['contrast_ratio'] +
            detail_complexity * weights_static['detail_complexity'] +
            egyptian_authenticity * weights_static['egyptian_authenticity']
        ) / total_weight
        
        return QualityMetrics(
            color_vibrancy=color_vibrancy,
            contrast_ratio=contrast_ratio,
            detail_complexity=detail_complexity,
            egyptian_authenticity=egyptian_authenticity,
            animation_smoothness=0.0,
            overall_score=overall_score
        )
    
    def _analyze_color_vibrancy(self, image: Image.Image) -> float:
        """Analyze color vibrancy using statistical methods"""
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate color statistics
        stat = ImageStat.Stat(image)
        
        # Standard deviation of RGB channels (higher = more vibrant)
        rgb_std = np.mean(stat.stddev[:3])  # Average of R, G, B std dev
        
        # Normalize to 0-1 range (empirically determined)
        vibrancy_score = min(rgb_std / 60.0, 1.0)
        
        return vibrancy_score
    
    def _analyze_contrast(self, image: Image.Image) -> float:
        """Analyze contrast using luminance analysis"""
        
        # Convert to grayscale for luminance analysis
        gray_img = image.convert('L')
        gray_array = np.array(gray_img)
        
        # Calculate RMS contrast (widely used metric)
        mean_luminance = np.mean(gray_array)
        rms_contrast = np.sqrt(np.mean((gray_array - mean_luminance) ** 2))
        
        # Normalize to 0-1 range
        contrast_score = min(rms_contrast / 80.0, 1.0)
        
        return contrast_score
    
    def _create_failed_metrics(self) -> QualityMetrics:
        """Create metrics object for failed validation"""
        return QualityMetrics(
            color_vibrancy=0.0,
            contrast_ratio=0.0,
            detail_complexity=0.0,
            egyptian_authenticity=0.0,
            animation_smoothness=0.0,
            overall_score=0.0
        )
    
    def batch_validate_directory(self, 
                                directory: Path, 
                                asset_type: str = "static",
                                parallel_workers: int = 4) -> Dict[str, QualityMetrics]:
        """Validate all assets in a directory using RTX 5070 parallel processing"""
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        asset_files = []
        
        for ext in image_extensions:
            asset_files.extend(directory.glob(f"*{ext}"))
        
        if not asset_files:
            print(f"No assets found in {directory}")
            return {}
        
        print(f"Validating {len(asset_files)} assets with {parallel_workers} workers...")
        
        results = {}
        
        # Use ThreadPoolExecutor for RTX 5070 parallel processing
        with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
            # Submit all validation jobs
            future_to_file = {
                executor.submit(self.validate_single_asset, asset_file, asset_type): asset_file
                for asset_file in asset_files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                asset_file = future_to_file[future]
                try:
                    metrics = future.result()
                    results[asset_file.name] = metrics
                    
                    # Print progress
                    quality_level = self._get_quality_level(metrics.overall_score)
                    print(f"✓ {asset_file.name}: {metrics.overall_score:.2f} ({quality_level})")
                    
                except Exception as e:
                    print(f"✗ {asset_file.name}: Validation failed - {e}")
                    results[asset_file.name] = self._create_failed_metrics()
        
        return results
    
    def _get_quality_level(self, score: float) -> str:
        """Get quality level description from score"""
        if score >= self.thresholds['excellent_quality']:
            return "EXCELLENT"
        elif score >= self.thresholds['good_quality']:
            return "GOOD"
        elif score >= self.thresholds['minimum_quality']:
            return "ACCEPTABLE"
        else:
            return "POOR"
    
    def save_validation_report(self, 
                              results: Dict[str, QualityMetrics], 
                              output_path: Path):
        """Save comprehensive validation report"""
        
        report = {
            'validation_timestamp': time.time(),
            'total_assets': len(results),
            'quality_distribution': {},
            'detailed_results': {}
        }
        
        # Calculate quality distribution
        quality_counts = {'EXCELLENT': 0, 'GOOD': 0, 'ACCEPTABLE': 0, 'POOR': 0}
        
        for filename, metrics in results.items():
            quality_level = self._get_quality_level(metrics.overall_score)
            quality_counts[quality_level] += 1
            
            report['detailed_results'][filename] = {
                **metrics.to_dict(),
                'quality_level': quality_level
            }
        
        report['quality_distribution'] = quality_counts
        
        # Summary statistics
        scores = [m.overall_score for m in results.values()]
        report['summary_statistics'] = {
            'mean_score': float(np.mean(scores)),
            'median_score': float(np.median(scores)),
            'std_score': float(np.std(scores)),
            'min_score': float(np.min(scores)),
            'max_score': float(np.max(scores))
        }
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Validation report saved to: {output_path}")
        print(f"Average Quality Score: {report['summary_statistics']['mean_score']:.2f}")
        print(f"Quality Distribution: {quality_counts}")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get validator statistics."""
        return {
            'thresholds_count': len(self.thresholds),
            'weights_count': len(self.weights),
            'minimum_quality': self.thresholds['minimum_quality'],
            'temp_processing_exists': self.temp_processing_dir.exists()
        }

if __name__ == "__main__":
    # Example usage
    validator = RTX5070QualityValidator()
    
    # Validate generated assets
    generated_dir = Path("assets/generated_art/cards")
    if generated_dir.exists():
        results = validator.batch_validate_directory(generated_dir, "static")
        validator.save_validation_report(results, Path("validation_report.json"))
    else:
        print("Generated assets directory not found. Run art generation first.")