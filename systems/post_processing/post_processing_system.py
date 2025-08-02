#!/usr/bin/env python3
"""
Post-Processing System - Professional cel-shading, bloom, and Hades-style effects
Implements advanced post-processing pipeline for game-ready Egyptian assets
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import asyncio
import time
import json

class PostProcessingSystem:
    """Advanced post-processing system for Hades-Egyptian art style"""
    
    def __init__(self):
        self.processing_profiles = {}
        self.effect_presets = {}
        self.color_palettes = {}
        
        # Hades-style processing configurations
        self.hades_config = {
            "cel_shading": {
                "quantization_levels": 8,
                "edge_threshold": 0.1,
                "edge_thickness": 2,
                "color_smoothing": True,
                "edge_color": (0, 0, 0),  # Black outlines
                "description": "Hades-style cel-shading with bold outlines"
            },
            "bloom_effect": {
                "threshold": 180,
                "intensity": 0.3,
                "blur_radius": 21,
                "bloom_color_boost": 1.2,
                "divine_glow": True,
                "description": "Divine bloom effect for magical elements"
            },
            "contrast_enhancement": {
                "shadows": 0.9,
                "midtones": 1.1,
                "highlights": 1.3,
                "saturation_boost": 1.2,
                "vibrance": 1.15,
                "description": "Enhanced contrast for vibrant game art"
            },
            "artistic_stylization": {
                "paint_effect": True,
                "texture_overlay": 0.1,
                "color_temperature": "warm",
                "vignette_strength": 0.05,
                "description": "Artistic stylization for painted look"
            }
        }
        
        # Egyptian-specific color palettes
        self.egyptian_palettes = {
            "divine_gold": {
                "primary": [(255, 215, 0), (218, 165, 32), (184, 134, 11)],  # Golds
                "secondary": [(65, 105, 225), (30, 144, 255), (0, 191, 255)],  # Divine blues
                "accent": [(220, 20, 60), (255, 69, 0), (255, 140, 0)],  # Sacred reds/oranges
                "description": "Divine Egyptian gold and blue palette"
            },
            "desert_earth": {
                "primary": [(210, 180, 140), (188, 143, 143), (160, 82, 45)],  # Earth tones
                "secondary": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],  # Desert browns
                "accent": [(255, 215, 0), (255, 165, 0), (255, 140, 0)],  # Golden accents
                "description": "Desert and earth tone palette"
            },
            "royal_luxury": {
                "primary": [(138, 43, 226), (75, 0, 130), (72, 61, 139)],  # Royal purples
                "secondary": [(255, 215, 0), (255, 223, 0), (255, 255, 224)],  # Luxurious golds
                "accent": [(220, 20, 60), (178, 34, 34), (139, 0, 0)],  # Royal reds
                "description": "Royal Egyptian luxury palette"
            }
        }
        
        # Effect templates for different asset types
        self.effect_templates = {
            "character_portrait": [
                "cel_shading",
                "edge_enhancement", 
                "divine_bloom",
                "contrast_boost",
                "color_grading"
            ],
            "environment_asset": [
                "atmospheric_depth",
                "lighting_enhancement",
                "texture_detail",
                "color_harmony"
            ],
            "ui_element": [
                "clean_edges",
                "subtle_glow",
                "color_consistency",
                "readability_boost"
            ],
            "magical_effect": [
                "intense_bloom",
                "particle_glow",
                "energy_distortion",
                "mystical_aura"
            ]
        }
        
        print("Post-Processing System initialized")
        print("   Hades-style cel-shading")
        print("   Divine bloom effects")
        print("   Egyptian color palettes")
        print("   Asset-specific processing profiles")
    
    async def apply_hades_egyptian_processing(self, 
                                            input_image: Image.Image,
                                            asset_type: str = "character_portrait",
                                            style_intensity: float = 1.0,
                                            custom_effects: List[str] = None) -> Dict[str, Any]:
        """Apply complete Hades-Egyptian post-processing pipeline"""
        
        print(f"Applying Hades-Egyptian processing to {asset_type}...")
        start_time = time.time()
        
        try:
            # Convert to numpy for processing
            img_array = np.array(input_image)
            
            # Stage 1: Cel-shading effect
            cel_shaded = await self._apply_cel_shading_effect(
                img_array, style_intensity
            )
            
            # Stage 2: Divine bloom effect
            bloomed = await self._apply_divine_bloom_effect(
                cel_shaded, asset_type, style_intensity
            )
            
            # Stage 3: Contrast and color enhancement
            enhanced = await self._apply_contrast_enhancement(
                bloomed, style_intensity
            )
            
            # Stage 4: Egyptian color grading
            color_graded = await self._apply_egyptian_color_grading(
                enhanced, asset_type
            )
            
            # Stage 5: Asset-specific effects
            if custom_effects:
                final_array = await self._apply_custom_effects(
                    color_graded, custom_effects, style_intensity
                )
            else:
                final_array = await self._apply_template_effects(
                    color_graded, asset_type, style_intensity
                )
            
            # Stage 6: Final polish
            polished = await self._apply_final_polish(final_array)
            
            # Convert back to PIL
            final_image = Image.fromarray(polished)
            
            # Save processed asset
            output_path = await self._save_processed_asset(
                final_image, asset_type, style_intensity
            )
            
            processing_time = time.time() - start_time
            
            result = {
                "status": "success",
                "asset_type": asset_type,
                "style_intensity": style_intensity,
                "original_size": input_image.size,
                "processed_size": final_image.size,
                "output_path": str(output_path),
                "processing_time": processing_time,
                "effects_applied": self._get_applied_effects(asset_type, custom_effects)
            }
            
            print(f"Post-processing complete ({processing_time:.2f}s)")
            return result
            
        except Exception as e:
            print(f"Post-processing failed: {e}")
            return {
                "status": "failed",
                "asset_type": asset_type,
                "error": str(e)
            }
    
    async def _apply_cel_shading_effect(self, img_array: np.ndarray, 
                                       intensity: float) -> np.ndarray:
        """Apply Hades-style cel-shading with bold outlines"""
        
        config = self.hades_config["cel_shading"]
        
        # Stage 1: Color quantization for cel-shading
        quantized = self._quantize_colors(
            img_array, 
            int(config["quantization_levels"] * intensity)
        )
        
        # Stage 2: Edge detection and enhancement
        edges = self._detect_and_enhance_edges(
            img_array,
            config["edge_threshold"],
            config["edge_thickness"]
        )
        
        # Stage 3: Apply bilateral filter for smooth color areas
        if config["color_smoothing"]:
            smooth = cv2.bilateralFilter(quantized, 9, 75, 75)
            quantized = smooth
        
        # Stage 4: Combine with edge lines
        cel_shaded = self._combine_colors_and_edges(
            quantized, edges, config["edge_color"]
        )
        
        print("   Cel-shading effect applied")
        return cel_shaded
    
    def _quantize_colors(self, img_array: np.ndarray, levels: int) -> np.ndarray:
        """Quantize colors for cel-shading effect"""
        
        # Convert to float for processing
        img_float = img_array.astype(np.float32) / 255.0
        
        # Quantize each channel
        quantized = np.round(img_float * levels) / levels
        
        # Convert back to uint8
        return (quantized * 255).astype(np.uint8)
    
    def _detect_and_enhance_edges(self, img_array: np.ndarray, 
                                threshold: float, thickness: int) -> np.ndarray:
        """Detect and enhance edges for outline effect"""
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, 
                         int(threshold * 255 * 0.5), 
                         int(threshold * 255))
        
        # Dilate edges for thickness
        if thickness > 1:
            kernel = np.ones((thickness, thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def _combine_colors_and_edges(self, colors: np.ndarray, 
                                edges: np.ndarray, 
                                edge_color: Tuple[int, int, int]) -> np.ndarray:
        """Combine quantized colors with edge outlines"""
        
        # Convert edge mask to 3-channel
        edge_mask = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB) / 255.0
        
        # Create edge color array
        edge_color_array = np.full_like(colors, edge_color, dtype=np.uint8)
        
        # Combine: use edge color where edges exist, original colors elsewhere
        result = colors * (1 - edge_mask) + edge_color_array * edge_mask
        
        return result.astype(np.uint8)
    
    async def _apply_divine_bloom_effect(self, img_array: np.ndarray, 
                                       asset_type: str, 
                                       intensity: float) -> np.ndarray:
        """Apply divine bloom effect for magical atmosphere"""
        
        config = self.hades_config["bloom_effect"]
        
        # Create bloom mask from bright areas
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        bright_threshold = int(config["threshold"] * intensity)
        bloom_mask = cv2.threshold(gray, bright_threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Apply Gaussian blur for glow effect
        blur_radius = int(config["blur_radius"] * intensity)
        if blur_radius % 2 == 0:
            blur_radius += 1  # Must be odd
        
        bloom_glow = cv2.GaussianBlur(img_array, (blur_radius, blur_radius), 0)
        
        # Enhance bloom colors for divine effect
        if config["divine_glow"]:
            bloom_glow = self._enhance_divine_colors(bloom_glow)
        
        # Create 3-channel bloom mask
        bloom_mask_3ch = cv2.cvtColor(bloom_mask, cv2.COLOR_GRAY2RGB) / 255.0
        
        # Apply bloom effect
        bloom_intensity = config["intensity"] * intensity
        result = img_array * (1 - bloom_mask_3ch * bloom_intensity) + \
                bloom_glow * (bloom_mask_3ch * bloom_intensity)
        
        print("   Divine bloom effect applied")
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _enhance_divine_colors(self, img_array: np.ndarray) -> np.ndarray:
        """Enhance colors for divine/magical bloom effect"""
        
        # Convert to HSV for better color manipulation
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Boost saturation for more vibrant glow
        hsv[:, :, 1] = np.minimum(hsv[:, :, 1] * 1.3, 255)
        
        # Slight hue shift toward gold/blue (divine colors)
        # Add warm tone for golden divine effect
        hsv[:, :, 0] = (hsv[:, :, 0] + 10) % 180
        
        # Convert back to RGB
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return enhanced
    
    async def _apply_contrast_enhancement(self, img_array: np.ndarray, 
                                        intensity: float) -> np.ndarray:
        """Apply contrast enhancement for vibrant game art"""
        
        config = self.hades_config["contrast_enhancement"]
        
        # Convert to PIL for enhancement
        img_pil = Image.fromarray(img_array)
        
        # Contrast enhancement
        contrast_factor = 1.0 + (config["midtones"] - 1.0) * intensity
        contrast_enhancer = ImageEnhance.Contrast(img_pil)
        img_pil = contrast_enhancer.enhance(contrast_factor)
        
        # Color saturation boost
        saturation_factor = 1.0 + (config["saturation_boost"] - 1.0) * intensity
        color_enhancer = ImageEnhance.Color(img_pil)
        img_pil = color_enhancer.enhance(saturation_factor)
        
        # Brightness adjustment for highlights/shadows
        brightness_factor = 1.0 + (config["highlights"] - 1.0) * intensity * 0.1
        brightness_enhancer = ImageEnhance.Brightness(img_pil)
        img_pil = brightness_enhancer.enhance(brightness_factor)
        
        print("   Contrast enhancement applied")
        return np.array(img_pil)
    
    async def _apply_egyptian_color_grading(self, img_array: np.ndarray, 
                                          asset_type: str) -> np.ndarray:
        """Apply Egyptian-themed color grading"""
        
        # Select appropriate color palette based on asset type
        if asset_type in ["character_portrait", "character_sprites"]:
            palette_name = "divine_gold"
        elif asset_type in ["environment_asset", "backgrounds"]:
            palette_name = "desert_earth"
        else:
            palette_name = "royal_luxury"
        
        palette = self.egyptian_palettes[palette_name]
        
        # Apply color grading
        graded = self._apply_color_palette_grading(img_array, palette)
        
        print(f"   Egyptian color grading applied ({palette_name})")
        return graded
    
    def _apply_color_palette_grading(self, img_array: np.ndarray, 
                                   palette: Dict) -> np.ndarray:
        """Apply color palette grading to match Egyptian themes"""
        
        # Convert to HSV for color manipulation
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Get primary colors from palette
        primary_colors = palette["primary"]
        
        # Calculate average hue of primary colors
        primary_hues = []
        for color in primary_colors:
            # Convert RGB to HSV
            rgb_normalized = np.array(color).reshape(1, 1, 3) / 255.0
            color_hsv = cv2.cvtColor((rgb_normalized * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
            primary_hues.append(color_hsv[0, 0, 0])
        
        avg_hue = np.mean(primary_hues)
        
        # Subtle hue shift toward palette colors
        hue_shift = (avg_hue - np.mean(hsv[:, :, 0])) * 0.1
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
        
        # Enhance colors in palette range
        for color in primary_colors:
            color_hsv = cv2.cvtColor(np.array(color).reshape(1, 1, 3), cv2.COLOR_RGB2HSV)
            target_hue = color_hsv[0, 0, 0]
            
            # Create mask for similar hues
            hue_mask = np.abs(hsv[:, :, 0] - target_hue) < 20
            
            # Boost saturation for matching hues
            hsv[hue_mask, 1] = np.minimum(hsv[hue_mask, 1] * 1.15, 255)
        
        # Convert back to RGB
        graded = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return graded
    
    async def _apply_template_effects(self, img_array: np.ndarray, 
                                    asset_type: str, 
                                    intensity: float) -> np.ndarray:
        """Apply template effects based on asset type"""
        
        effects = self.effect_templates.get(asset_type, ["cel_shading"])
        result = img_array.copy()
        
        for effect in effects:
            if effect == "edge_enhancement":
                result = self._apply_edge_enhancement(result, intensity)
            elif effect == "divine_bloom":
                result = await self._apply_divine_bloom_effect(result, asset_type, intensity)
            elif effect == "atmospheric_depth":
                result = self._apply_atmospheric_depth(result, intensity)
            elif effect == "subtle_glow":
                result = self._apply_subtle_glow(result, intensity)
            elif effect == "mystical_aura":
                result = self._apply_mystical_aura(result, intensity)
        
        return result
    
    def _apply_edge_enhancement(self, img_array: np.ndarray, 
                              intensity: float) -> np.ndarray:
        """Apply edge enhancement for crisp details"""
        
        # Unsharp mask for edge enhancement
        img_pil = Image.fromarray(img_array)
        enhanced = img_pil.filter(ImageFilter.UnsharpMask(
            radius=1.5 * intensity,
            percent=int(120 * intensity),
            threshold=2
        ))
        
        return np.array(enhanced)
    
    def _apply_atmospheric_depth(self, img_array: np.ndarray, 
                               intensity: float) -> np.ndarray:
        """Apply atmospheric depth effect for environments"""
        
        height, width = img_array.shape[:2]
        
        # Create depth gradient (darker at bottom, lighter at top)
        depth_gradient = np.linspace(0.8, 1.2, height).reshape(-1, 1, 1)
        depth_gradient = np.repeat(depth_gradient, width, axis=1)
        depth_gradient = np.repeat(depth_gradient, 3, axis=2)
        
        # Apply depth effect
        result = img_array * depth_gradient * intensity + img_array * (1 - intensity)
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_subtle_glow(self, img_array: np.ndarray, 
                         intensity: float) -> np.ndarray:
        """Apply subtle glow for UI elements"""
        
        # Create soft glow
        blurred = cv2.GaussianBlur(img_array, (15, 15), 0)
        
        # Blend with original
        glow_strength = 0.2 * intensity
        result = img_array * (1 - glow_strength) + blurred * glow_strength
        
        return result.astype(np.uint8)
    
    def _apply_mystical_aura(self, img_array: np.ndarray, 
                           intensity: float) -> np.ndarray:
        """Apply mystical aura for magical effects"""
        
        # Create colorful aura effect
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Add color variation for mystical effect
        hsv[:, :, 0] = (hsv[:, :, 0] + np.random.randint(-10, 11, hsv.shape[:2])) % 180
        hsv[:, :, 1] = np.minimum(hsv[:, :, 1] * (1.2 * intensity), 255)
        
        # Add soft glow
        mystical = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        glowing = cv2.GaussianBlur(mystical, (25, 25), 0)
        
        # Combine effects
        result = mystical * 0.7 + glowing * (0.3 * intensity)
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    async def _apply_custom_effects(self, img_array: np.ndarray, 
                                  effects: List[str], 
                                  intensity: float) -> np.ndarray:
        """Apply custom list of effects"""
        
        result = img_array.copy()
        
        for effect in effects:
            if hasattr(self, f"_apply_{effect}"):
                effect_func = getattr(self, f"_apply_{effect}")
                result = effect_func(result, intensity)
            else:
                print(f"   Warning: Unknown effect '{effect}'")
        
        return result
    
    async def _apply_final_polish(self, img_array: np.ndarray) -> np.ndarray:
        """Apply final polish for professional quality"""
        
        # Subtle noise reduction
        polished = cv2.medianBlur(img_array, 3)
        
        # Blend with original to maintain detail
        final = img_array * 0.9 + polished * 0.1
        
        return final.astype(np.uint8)
    
    def _get_applied_effects(self, asset_type: str, 
                           custom_effects: Optional[List[str]]) -> List[str]:
        """Get list of effects that were applied"""
        
        base_effects = [
            "cel_shading",
            "divine_bloom", 
            "contrast_enhancement",
            "egyptian_color_grading"
        ]
        
        if custom_effects:
            return base_effects + custom_effects
        else:
            template_effects = self.effect_templates.get(asset_type, [])
            return base_effects + template_effects
    
    async def _save_processed_asset(self, image: Image.Image, 
                                  asset_type: str, 
                                  intensity: float) -> Path:
        """Save processed asset with metadata"""
        
        output_dir = Path("assets/generated/post_processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = int(time.time())
        filename = f"{asset_type}_processed_{intensity:.1f}_{timestamp}.png"
        output_path = output_dir / filename
        
        # Save image
        image.save(output_path, "PNG", optimize=True)
        
        # Save metadata
        metadata = {
            "asset_type": asset_type,
            "style_intensity": intensity,
            "processing_pipeline": "hades_egyptian",
            "effects_applied": self._get_applied_effects(asset_type, None),
            "color_palette": self._get_used_palette(asset_type),
            "processing_time": time.time(),
            "dimensions": image.size,
            "quality_settings": {
                "format": "PNG",
                "optimization": True
            }
        }
        
        metadata_path = output_dir / f"{asset_type}_processed_{intensity:.1f}_{timestamp}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def _get_used_palette(self, asset_type: str) -> str:
        """Get the color palette used for this asset type"""
        
        if asset_type in ["character_portrait", "character_sprites"]:
            return "divine_gold"
        elif asset_type in ["environment_asset", "backgrounds"]:
            return "desert_earth"
        else:
            return "royal_luxury"

# Test function
async def test_post_processing():
    """Test post-processing system"""
    print("Testing Post-Processing System...")
    
    system = PostProcessingSystem()
    
    # Create test image
    test_image = Image.new("RGB", (512, 512), color=(150, 100, 200))
    
    # Add some content to test effects
    draw = ImageDraw.Draw(test_image)
    draw.rectangle([100, 100, 400, 400], fill=(255, 215, 0), outline=(0, 0, 0), width=3)
    draw.ellipse([200, 200, 300, 300], fill=(65, 105, 225), outline=(255, 255, 255), width=2)
    
    # Test processing
    result = await system.apply_hades_egyptian_processing(
        input_image=test_image,
        asset_type="character_portrait",
        style_intensity=1.0
    )
    
    print(f"Post-processing test result: {result}")

if __name__ == "__main__":
    asyncio.run(test_post_processing())