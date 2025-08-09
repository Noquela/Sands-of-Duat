"""
SANDS OF DUAT - HADES-QUALITY ASSET VALIDATOR
==============================================

Professional asset validation system ensuring every generated artwork meets
Hades-level artistic excellence and Egyptian thematic consistency.
"""

import cv2
import numpy as np
from PIL import Image, ImageStat
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationCriteria:
    """Hades-quality validation criteria."""
    min_resolution: Tuple[int, int] = (512, 512)
    max_resolution: Tuple[int, int] = (2048, 2048)
    
    # Color and quality thresholds
    min_color_variety: float = 0.6  # Color diversity score
    min_contrast_ratio: float = 0.4  # Dynamic range
    min_saturation: float = 0.3     # Vibrant colors like Hades
    max_blur_score: float = 0.3     # Sharpness requirement
    
    # Egyptian theme validation
    required_color_palette: List[str] = None  # Gold, blue, etc.
    forbidden_elements: List[str] = None      # Modern items, etc.
    
    # Hades-style requirements
    min_artistic_score: float = 0.75  # Overall artistic quality
    painterly_threshold: float = 0.6   # Hand-painted appearance
    
    def __post_init__(self):
        if self.required_color_palette is None:
            self.required_color_palette = ["gold", "lapis_lazuli", "papyrus", "desert_sand"]
        if self.forbidden_elements is None:
            self.forbidden_elements = ["modern", "digital", "photographic", "3d_render"]

@dataclass 
class ValidationResult:
    """Result of asset validation."""
    asset_path: str
    passed: bool
    overall_score: float
    
    # Individual metric scores
    resolution_score: float = 0.0
    color_variety_score: float = 0.0
    contrast_score: float = 0.0
    saturation_score: float = 0.0
    sharpness_score: float = 0.0
    egyptian_theme_score: float = 0.0
    hades_quality_score: float = 0.0
    
    # Detailed feedback
    issues: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.recommendations is None:
            self.recommendations = []

class HadesQualityValidator:
    """
    Professional asset validator targeting Hades-level artistic excellence.
    """
    
    def __init__(self, criteria: Optional[ValidationCriteria] = None):
        self.criteria = criteria or ValidationCriteria()
        
        # Egyptian color palette (RGB values)
        self.egyptian_colors = {
            "gold": [(255, 215, 0), (218, 165, 32), (255, 223, 0)],
            "lapis_lazuli": [(26, 81, 171), (65, 105, 225), (0, 71, 171)],
            "papyrus": [(245, 245, 220), (255, 248, 220), (250, 240, 190)],
            "desert_sand": [(194, 178, 128), (210, 180, 140), (188, 143, 143)],
            "dark_blue": [(25, 25, 112), (0, 0, 139), (72, 61, 139)]
        }
        
        logger.info("Hades-Quality Asset Validator initialized")
    
    def validate_asset(self, asset_path: str) -> ValidationResult:
        """Validate a single asset for Hades-level quality."""
        
        logger.info(f"Validating asset: {Path(asset_path).name}")
        
        try:
            # Load image
            image = Image.open(asset_path)
            cv_image = cv2.imread(asset_path)
            
            result = ValidationResult(asset_path=asset_path, passed=False, overall_score=0.0)
            
            # Run all validation checks
            result.resolution_score = self._check_resolution(image, result)
            result.color_variety_score = self._check_color_variety(image, result)
            result.contrast_score = self._check_contrast(cv_image, result)
            result.saturation_score = self._check_saturation(image, result)
            result.sharpness_score = self._check_sharpness(cv_image, result)
            result.egyptian_theme_score = self._check_egyptian_theme(image, result)
            result.hades_quality_score = self._check_hades_quality(image, result)
            
            # Calculate overall score (weighted average)
            weights = {
                'resolution': 0.10,
                'color_variety': 0.15,
                'contrast': 0.15,
                'saturation': 0.15,
                'sharpness': 0.15,
                'egyptian_theme': 0.15,
                'hades_quality': 0.15
            }
            
            result.overall_score = (
                result.resolution_score * weights['resolution'] +
                result.color_variety_score * weights['color_variety'] +
                result.contrast_score * weights['contrast'] +
                result.saturation_score * weights['saturation'] +
                result.sharpness_score * weights['sharpness'] +
                result.egyptian_theme_score * weights['egyptian_theme'] +
                result.hades_quality_score * weights['hades_quality']
            )
            
            # Determine if asset passes
            result.passed = (
                result.overall_score >= self.criteria.min_artistic_score and
                len(result.issues) == 0
            )
            
            if result.passed:
                logger.info(f"✅ Asset passed validation: {result.overall_score:.2f}")
            else:
                logger.warning(f"❌ Asset failed validation: {result.overall_score:.2f}")
                for issue in result.issues:
                    logger.warning(f"   Issue: {issue}")
            
            return result
            
        except Exception as e:
            logger.error(f"Validation error for {asset_path}: {e}")
            return ValidationResult(
                asset_path=asset_path,
                passed=False,
                overall_score=0.0,
                issues=[f"Validation failed: {str(e)}"]
            )
    
    def _check_resolution(self, image: Image.Image, result: ValidationResult) -> float:
        """Check if resolution meets Hades-quality standards."""
        width, height = image.size
        min_w, min_h = self.criteria.min_resolution
        max_w, max_h = self.criteria.max_resolution
        
        if width < min_w or height < min_h:
            result.issues.append(f"Resolution too low: {width}x{height} (min: {min_w}x{min_h})")
            return 0.0
        
        if width > max_w or height > max_h:
            result.issues.append(f"Resolution too high: {width}x{height} (max: {max_w}x{max_h})")
            return 0.5
        
        # Score based on how close to optimal resolution
        optimal_score = min(width / min_w, height / min_h, max_w / width, max_h / height)
        return min(1.0, optimal_score)
    
    def _check_color_variety(self, image: Image.Image, result: ValidationResult) -> float:
        """Check color diversity - Hades has rich, varied palettes."""
        
        # Convert to HSV for better color analysis
        hsv_image = image.convert('HSV')
        colors = list(hsv_image.getdata())
        
        # Calculate unique hues
        hues = [color[0] for color in colors]
        unique_hues = len(set(hues)) / 256.0  # Normalize by max possible hues
        
        if unique_hues < self.criteria.min_color_variety:
            result.issues.append(f"Insufficient color variety: {unique_hues:.2f} (min: {self.criteria.min_color_variety})")
            result.recommendations.append("Add more color variation to match Hades' rich palette")
        
        return min(1.0, unique_hues / self.criteria.min_color_variety)
    
    def _check_contrast(self, cv_image: np.ndarray, result: ValidationResult) -> float:
        """Check dynamic contrast - Hades has dramatic lighting."""
        
        # Convert to grayscale for contrast analysis
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate contrast as standard deviation of pixel values
        contrast = np.std(gray) / 255.0
        
        if contrast < self.criteria.min_contrast_ratio:
            result.issues.append(f"Low contrast: {contrast:.2f} (min: {self.criteria.min_contrast_ratio})")
            result.recommendations.append("Increase dramatic lighting contrasts like in Hades")
        
        return min(1.0, contrast / self.criteria.min_contrast_ratio)
    
    def _check_saturation(self, image: Image.Image, result: ValidationResult) -> float:
        """Check color saturation - Hades uses vibrant colors."""
        
        hsv_image = image.convert('HSV')
        stat = ImageStat.Stat(hsv_image)
        
        # Get average saturation (second channel in HSV)
        avg_saturation = stat.mean[1] / 255.0
        
        if avg_saturation < self.criteria.min_saturation:
            result.issues.append(f"Low saturation: {avg_saturation:.2f} (min: {self.criteria.min_saturation})")
            result.recommendations.append("Increase color saturation for Hades-level vibrancy")
        
        return min(1.0, avg_saturation / self.criteria.min_saturation)
    
    def _check_sharpness(self, cv_image: np.ndarray, result: ValidationResult) -> float:
        """Check image sharpness - Hades art is crisp and detailed."""
        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance (measure of sharpness)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_score = 1.0 - min(1.0, laplacian_var / 1000.0)  # Normalize
        
        if blur_score > self.criteria.max_blur_score:
            result.issues.append(f"Image too blurry: {blur_score:.2f} (max: {self.criteria.max_blur_score})")
            result.recommendations.append("Increase sharpness and detail clarity")
        
        return 1.0 - blur_score
    
    def _check_egyptian_theme(self, image: Image.Image, result: ValidationResult) -> float:
        """Check adherence to Egyptian visual themes."""
        
        # Analyze dominant colors
        colors = image.convert('RGB').getcolors(maxcolors=256*256*256)
        if not colors:
            return 0.0
        
        # Sort by frequency
        colors.sort(key=lambda x: x[0], reverse=True)
        dominant_colors = [color[1] for color in colors[:10]]  # Top 10 colors
        
        # Check for Egyptian color palette presence
        egyptian_color_score = 0.0
        total_pixels = sum(color[0] for color in colors)
        
        for pixel_count, rgb in colors[:20]:  # Check top 20 colors
            for palette_name, palette_colors in self.egyptian_colors.items():
                for palette_rgb in palette_colors:
                    # Calculate color distance
                    distance = sum(abs(c1 - c2) for c1, c2 in zip(rgb, palette_rgb))
                    if distance < 50:  # Close enough to palette color
                        egyptian_color_score += (pixel_count / total_pixels)
                        break
        
        if egyptian_color_score < 0.3:
            result.recommendations.append("Incorporate more Egyptian color palette (gold, lapis lazuli, papyrus)")
        
        return min(1.0, egyptian_color_score / 0.5)  # Target at least 50% Egyptian colors
    
    def _check_hades_quality(self, image: Image.Image, result: ValidationResult) -> float:
        """Check for Hades-style artistic quality indicators."""
        
        # This is a simplified version - in production you might use ML models
        # trained on Hades artwork to detect style similarity
        
        quality_indicators = []
        
        # Check for painterly texture (not too smooth)
        rgb_array = np.array(image.convert('RGB'))
        texture_variance = np.var(rgb_array, axis=(0, 1)).mean()
        painterly_score = min(1.0, texture_variance / 1000.0)
        quality_indicators.append(painterly_score)
        
        # Check for artistic composition (rule of thirds, etc.)
        # This is simplified - could be much more sophisticated
        composition_score = 0.8  # Placeholder for composition analysis
        quality_indicators.append(composition_score)
        
        # Check for detail richness
        detail_score = min(1.0, self._calculate_detail_richness(image))
        quality_indicators.append(detail_score)
        
        overall_quality = sum(quality_indicators) / len(quality_indicators)
        
        if overall_quality < self.criteria.painterly_threshold:
            result.recommendations.append("Enhance painterly, hand-drawn quality like Hades artwork")
        
        return overall_quality
    
    def _calculate_detail_richness(self, image: Image.Image) -> float:
        """Calculate detail richness of the artwork."""
        
        # Convert to grayscale for edge detection
        gray = np.array(image.convert('L'))
        
        # Use Canny edge detection to find detail areas
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        return min(1.0, edge_density * 10)  # Scale appropriately
    
    def batch_validate_assets(self, asset_paths: List[str]) -> List[ValidationResult]:
        """Validate multiple assets for Hades-quality standards."""
        
        logger.info(f"Batch validating {len(asset_paths)} assets")
        
        results = []
        passed_count = 0
        
        for asset_path in asset_paths:
            result = self.validate_asset(asset_path)
            results.append(result)
            
            if result.passed:
                passed_count += 1
        
        logger.info(f"Batch validation complete: {passed_count}/{len(asset_paths)} passed")
        
        return results
    
    def generate_validation_report(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        
        total_assets = len(results)
        passed_assets = sum(1 for r in results if r.passed)
        failed_assets = total_assets - passed_assets
        
        avg_score = sum(r.overall_score for r in results) / total_assets if results else 0.0
        
        # Category breakdown
        score_breakdown = {
            'resolution': sum(r.resolution_score for r in results) / total_assets,
            'color_variety': sum(r.color_variety_score for r in results) / total_assets,
            'contrast': sum(r.contrast_score for r in results) / total_assets,
            'saturation': sum(r.saturation_score for r in results) / total_assets,
            'sharpness': sum(r.sharpness_score for r in results) / total_assets,
            'egyptian_theme': sum(r.egyptian_theme_score for r in results) / total_assets,
            'hades_quality': sum(r.hades_quality_score for r in results) / total_assets
        }
        
        # Common issues
        all_issues = []
        for result in results:
            all_issues.extend(result.issues)
        
        issue_frequency = {}
        for issue in all_issues:
            issue_frequency[issue] = issue_frequency.get(issue, 0) + 1
        
        report = {
            'summary': {
                'total_assets': total_assets,
                'passed_assets': passed_assets,
                'failed_assets': failed_assets,
                'pass_rate': (passed_assets / total_assets * 100) if total_assets > 0 else 0,
                'average_score': avg_score
            },
            'score_breakdown': score_breakdown,
            'common_issues': sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True),
            'detailed_results': [
                {
                    'asset': Path(r.asset_path).name,
                    'passed': r.passed,
                    'score': r.overall_score,
                    'issues': r.issues
                }
                for r in results
            ]
        }
        
        return report

# Global validator instance
_asset_validator: Optional[HadesQualityValidator] = None

def get_asset_validator() -> HadesQualityValidator:
    """Get the global asset validator instance."""
    global _asset_validator
    if _asset_validator is None:
        _asset_validator = HadesQualityValidator()
    return _asset_validator