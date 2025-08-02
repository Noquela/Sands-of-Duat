#!/usr/bin/env python3
"""
Real-ESRGAN Upscaling System - Professional quality upscaling for Hades-Egyptian assets
Implements Real-ESRGAN, GFPGAN, and custom upscaling techniques for game-ready assets
"""

import torch
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageFilter, ImageEnhance
import asyncio
import time
import subprocess
import json

class RealESRGANUpscalingSystem:
    """Advanced upscaling system using Real-ESRGAN and custom techniques"""
    
    def __init__(self, device="cuda"):
        self.device = device
        self.upscalers = {}
        self.face_enhancers = {}
        self.custom_models = {}
        
        # Upscaling configurations for different asset types
        self.upscaling_configs = {
            "character_sprites": {
                "scale_factor": 4,
                "model": "RealESRGAN_x4plus",
                "tile_size": 512,
                "tile_pad": 32,
                "pre_pad": 16,
                "description": "High-detail character upscaling"
            },
            "environment_assets": {
                "scale_factor": 2,
                "model": "RealESRGAN_x2plus",
                "tile_size": 1024,
                "tile_pad": 64,
                "pre_pad": 32,
                "description": "Environment texture upscaling"
            },
            "ui_elements": {
                "scale_factor": 2,
                "model": "RealESRGAN_x2plus",
                "tile_size": 256,
                "tile_pad": 16,
                "pre_pad": 8,
                "description": "Clean UI element upscaling"
            },
            "pixel_art": {
                "scale_factor": 4,
                "model": "RealESRGAN_x4plus_anime_6B",
                "tile_size": 256,
                "tile_pad": 16,
                "pre_pad": 8,
                "description": "Pixel art and anime style upscaling"
            }
        }
        
        # Custom Egyptian artifact enhancement settings
        self.egyptian_enhancement_config = {
            "hieroglyph_sharpening": {
                "kernel": np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]),
                "strength": 0.8
            },
            "gold_enhancement": {
                "hue_range": (15, 45),  # Gold hue range
                "saturation_boost": 1.4,
                "brightness_boost": 1.2
            },
            "divine_aura_enhancement": {
                "glow_radius": 21,
                "glow_strength": 0.3,
                "color_temp": "warm"
            }
        }
        
        print("Real-ESRGAN Upscaling System initialized")
        print("   Multi-scale upscaling support")
        print("   Egyptian artifact enhancement")
        print("   Face enhancement for character portraits")
    
    async def setup_upscaling_models(self) -> bool:
        """Setup Real-ESRGAN and related upscaling models"""
        try:
            print("Setting up Real-ESRGAN upscaling models...")
            
            # Install dependencies
            await self._install_upscaling_dependencies()
            
            # Download and setup Real-ESRGAN models
            await self._setup_realesrgan_models()
            
            # Setup face enhancement models
            await self._setup_face_enhancement_models()
            
            # Create custom Egyptian upscaling filters
            await self._create_egyptian_enhancement_filters()
            
            print("Real-ESRGAN models setup complete!")
            return True
            
        except Exception as e:
            print(f"Real-ESRGAN setup failed: {e}")
            return False
    
    async def _install_upscaling_dependencies(self):
        """Install Real-ESRGAN and related dependencies"""
        dependencies = [
            "realesrgan",
            "basicsr",
            "facexlib",
            "gfpgan",
            "opencv-python",
            "Pillow>=8.0.0"
        ]
        
        print("Installing upscaling dependencies...")
        for dep in dependencies:
            try:
                subprocess.run([
                    "pip", "install", dep, "--quiet"
                ], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to install {dep}, continuing...")
    
    async def _setup_realesrgan_models(self):
        """Setup Real-ESRGAN models for different purposes"""
        try:
            from realesrgan import RealESRGANer
            from basicsr.archs.rrdbnet_arch import RRDBNet
            
            print("Loading Real-ESRGAN models...")
            
            # Model configurations
            model_configs = {
                "x4plus": {
                    "model_path": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
                    "scale": 4,
                    "arch": RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
                },
                "x2plus": {
                    "model_path": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
                    "scale": 2,
                    "arch": RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
                },
                "anime_6B": {
                    "model_path": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
                    "scale": 4,
                    "arch": RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
                }
            }
            
            # Initialize upscalers
            for model_name, config in model_configs.items():
                try:
                    upsampler = RealESRGANer(
                        scale=config["scale"],
                        model_path=config["model_path"],
                        model=config["arch"],
                        tile=512,
                        tile_pad=32,
                        pre_pad=16,
                        half=True if self.device == "cuda" else False,
                        gpu_id=0 if self.device == "cuda" else None
                    )
                    
                    self.upscalers[model_name] = upsampler
                    print(f"   Loaded Real-ESRGAN {model_name}")
                    
                except Exception as e:
                    print(f"   Failed to load {model_name}: {e}")
            
            # Create fallback upscaler
            if not self.upscalers:
                print("   Creating fallback PIL upscaler...")
                self.upscalers["fallback"] = "pil_lanczos"
            
        except Exception as e:
            print(f"Failed to setup Real-ESRGAN models: {e}")
            # Create fallback
            self.upscalers["fallback"] = "pil_lanczos"
    
    async def _setup_face_enhancement_models(self):
        """Setup GFPGAN for face enhancement"""
        try:
            from gfpgan import GFPGANer
            
            print("Setting up face enhancement models...")
            
            # GFPGAN for face restoration
            gfpgan = GFPGANer(
                model_path="https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth",
                upscale=2,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=self.upscalers.get("x2plus")
            )
            
            self.face_enhancers["gfpgan"] = gfpgan
            print("   GFPGAN face enhancer loaded")
            
        except Exception as e:
            print(f"   Face enhancement setup failed: {e}")
            # Continue without face enhancement
    
    async def _create_egyptian_enhancement_filters(self):
        """Create custom enhancement filters for Egyptian artifacts"""
        
        # Hieroglyph sharpening kernel
        hieroglyph_kernel = self.egyptian_enhancement_config["hieroglyph_sharpening"]["kernel"]
        
        # Gold enhancement parameters
        gold_config = self.egyptian_enhancement_config["gold_enhancement"]
        
        # Divine aura parameters
        aura_config = self.egyptian_enhancement_config["divine_aura_enhancement"]
        
        self.custom_models = {
            "hieroglyph_enhancer": {
                "type": "convolution",
                "kernel": hieroglyph_kernel,
                "description": "Sharpens hieroglyphic details"
            },
            "gold_enhancer": {
                "type": "color_enhancement",
                "config": gold_config,
                "description": "Enhances golden artifacts"
            },
            "divine_aura": {
                "type": "glow_effect",
                "config": aura_config,
                "description": "Adds divine aura glow"
            }
        }
        
        print("Egyptian enhancement filters created")
    
    async def upscale_egyptian_asset(self, 
                                   input_image: Image.Image,
                                   asset_type: str,
                                   target_scale: int = 4,
                                   enhance_egyptian_features: bool = True,
                                   output_name: str = "upscaled_asset") -> Dict[str, Any]:
        """Upscale Egyptian asset with specialized enhancements"""
        
        print(f"Upscaling {asset_type} asset with scale {target_scale}x...")
        start_time = time.time()
        
        try:
            # Convert PIL to numpy
            img_array = np.array(input_image)
            
            # Stage 1: Initial upscaling with Real-ESRGAN
            upscaled_array = await self._apply_realesrgan_upscaling(
                img_array, asset_type, target_scale
            )
            
            # Stage 2: Egyptian feature enhancement
            if enhance_egyptian_features:
                upscaled_array = await self._apply_egyptian_enhancements(
                    upscaled_array, asset_type
                )
            
            # Stage 3: Post-upscaling refinement
            refined_array = await self._apply_post_upscaling_refinement(
                upscaled_array, asset_type
            )
            
            # Stage 4: Final quality optimization
            final_array = await self._apply_final_quality_optimization(
                refined_array
            )
            
            # Convert back to PIL
            final_image = Image.fromarray(final_array)
            
            # Save with metadata
            output_path = await self._save_upscaled_asset(
                final_image, output_name, asset_type, target_scale
            )
            
            processing_time = time.time() - start_time
            
            result = {
                "status": "success",
                "asset_type": asset_type,
                "original_size": input_image.size,
                "upscaled_size": final_image.size,
                "scale_factor": target_scale,
                "output_path": str(output_path),
                "processing_time": processing_time,
                "enhancements_applied": enhance_egyptian_features
            }
            
            print(f"Upscaling complete: {input_image.size} -> {final_image.size} ({processing_time:.2f}s)")
            return result
            
        except Exception as e:
            print(f"Upscaling failed: {e}")
            return {
                "status": "failed",
                "asset_type": asset_type,
                "error": str(e)
            }
    
    async def _apply_realesrgan_upscaling(self, img_array: np.ndarray, 
                                        asset_type: str, 
                                        target_scale: int) -> np.ndarray:
        """Apply Real-ESRGAN upscaling based on asset type"""
        
        # Select appropriate model based on asset type and scale
        model_key = self._select_upscaling_model(asset_type, target_scale)
        
        if model_key in self.upscalers and model_key != "fallback":
            try:
                upsampler = self.upscalers[model_key]
                
                # Apply Real-ESRGAN upscaling
                upscaled_img, _ = upsampler.enhance(
                    img_array, 
                    outscale=target_scale
                )
                
                print(f"   Real-ESRGAN {model_key} upscaling applied")
                return upscaled_img
                
            except Exception as e:
                print(f"   Real-ESRGAN failed: {e}, using fallback")
        
        # Fallback to PIL upscaling
        return self._apply_fallback_upscaling(img_array, target_scale)
    
    def _select_upscaling_model(self, asset_type: str, target_scale: int) -> str:
        """Select appropriate upscaling model for asset type"""
        
        if asset_type in ["character_sprites", "portraits"]:
            if target_scale == 4:
                return "x4plus"
            elif target_scale == 2:
                return "x2plus"
        
        elif asset_type in ["pixel_art", "sprites"]:
            return "anime_6B"
        
        elif asset_type in ["environment_assets", "backgrounds"]:
            if target_scale <= 2:
                return "x2plus"
            else:
                return "x4plus"
        
        # Default selection
        if target_scale == 4:
            return "x4plus"
        elif target_scale == 2:
            return "x2plus"
        else:
            return "x4plus"
    
    def _apply_fallback_upscaling(self, img_array: np.ndarray, 
                                target_scale: int) -> np.ndarray:
        """Apply fallback PIL upscaling"""
        
        img_pil = Image.fromarray(img_array)
        
        # Calculate new dimensions
        width, height = img_pil.size
        new_width = width * target_scale
        new_height = height * target_scale
        
        # Apply Lanczos resampling with sharpening
        upscaled = img_pil.resize((new_width, new_height), Image.LANCZOS)
        upscaled = upscaled.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
        
        print(f"   Fallback PIL upscaling applied ({target_scale}x)")
        return np.array(upscaled)
    
    async def _apply_egyptian_enhancements(self, img_array: np.ndarray, 
                                         asset_type: str) -> np.ndarray:
        """Apply Egyptian-specific enhancements"""
        
        enhanced_img = img_array.copy()
        
        # Apply hieroglyph sharpening for character/artifact assets
        if asset_type in ["character_sprites", "artifacts", "ui_elements"]:
            enhanced_img = self._enhance_hieroglyphs(enhanced_img)
        
        # Apply gold enhancement for divine/royal assets
        if asset_type in ["character_sprites", "artifacts", "altars"]:
            enhanced_img = self._enhance_gold_elements(enhanced_img)
        
        # Apply divine aura for character/god assets
        if asset_type in ["character_sprites", "portraits"]:
            enhanced_img = self._add_divine_aura(enhanced_img)
        
        print("   Egyptian enhancements applied")
        return enhanced_img
    
    def _enhance_hieroglyphs(self, img_array: np.ndarray) -> np.ndarray:
        """Enhance hieroglyphic details and inscriptions"""
        
        # Apply sharpening kernel for fine details
        kernel = self.custom_models["hieroglyph_enhancer"]["kernel"]
        
        # Apply to each color channel
        enhanced = np.zeros_like(img_array)
        for i in range(3):
            enhanced[:, :, i] = cv2.filter2D(img_array[:, :, i], -1, kernel)
        
        # Blend with original
        strength = self.egyptian_enhancement_config["hieroglyph_sharpening"]["strength"]
        result = img_array * (1 - strength) + enhanced * strength
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _enhance_gold_elements(self, img_array: np.ndarray) -> np.ndarray:
        """Enhance golden artifacts and decorations"""
        
        # Convert to HSV for better color manipulation
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Define gold hue range
        gold_config = self.custom_models["gold_enhancer"]["config"]
        hue_min, hue_max = gold_config["hue_range"]
        
        # Create mask for golden areas
        gold_mask = cv2.inRange(hsv[:, :, 0], hue_min, hue_max)
        gold_mask = gold_mask.astype(np.float32) / 255.0
        
        # Enhance saturation and brightness in golden areas
        hsv[:, :, 1] = hsv[:, :, 1] * (1 + gold_mask * (gold_config["saturation_boost"] - 1))
        hsv[:, :, 2] = hsv[:, :, 2] * (1 + gold_mask * (gold_config["brightness_boost"] - 1))
        
        # Clip values
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        # Convert back to RGB
        enhanced_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return enhanced_rgb
    
    def _add_divine_aura(self, img_array: np.ndarray) -> np.ndarray:
        """Add subtle divine aura glow effect"""
        
        aura_config = self.custom_models["divine_aura"]["config"]
        
        # Create glow mask from bright areas
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        bright_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
        
        # Apply Gaussian blur for glow effect
        glow_radius = aura_config["glow_radius"]
        glow = cv2.GaussianBlur(img_array, (glow_radius, glow_radius), 0)
        
        # Create warm color temperature for divine feel
        if aura_config["color_temp"] == "warm":
            glow[:, :, 0] = np.minimum(glow[:, :, 0] * 1.1, 255)  # Enhance red
            glow[:, :, 1] = np.minimum(glow[:, :, 1] * 1.05, 255)  # Slight green
            glow[:, :, 2] = glow[:, :, 2] * 0.9  # Reduce blue
        
        # Blend glow with original using mask
        glow_mask_3ch = cv2.cvtColor(bright_mask, cv2.COLOR_GRAY2RGB) / 255.0
        glow_strength = aura_config["glow_strength"]
        
        result = img_array * (1 - glow_mask_3ch * glow_strength) + glow * (glow_mask_3ch * glow_strength)
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    async def _apply_post_upscaling_refinement(self, img_array: np.ndarray, 
                                             asset_type: str) -> np.ndarray:
        """Apply post-upscaling refinement techniques"""
        
        refined = img_array.copy()
        
        # Edge enhancement for game assets
        if asset_type in ["character_sprites", "ui_elements"]:
            refined = self._enhance_edges(refined)
        
        # Noise reduction for clean backgrounds
        if asset_type in ["environment_assets", "backgrounds"]:
            refined = self._reduce_upscaling_artifacts(refined)
        
        # Color correction and contrast adjustment
        refined = self._adjust_contrast_and_colors(refined)
        
        print("   Post-upscaling refinement applied")
        return refined
    
    def _enhance_edges(self, img_array: np.ndarray) -> np.ndarray:
        """Enhance edges for crisp game assets"""
        
        # Apply unsharp mask for edge enhancement
        img_pil = Image.fromarray(img_array)
        enhanced = img_pil.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
        
        return np.array(enhanced)
    
    def _reduce_upscaling_artifacts(self, img_array: np.ndarray) -> np.ndarray:
        """Reduce common upscaling artifacts"""
        
        # Apply bilateral filter to reduce noise while preserving edges
        cleaned = cv2.bilateralFilter(img_array, 9, 75, 75)
        
        # Slight Gaussian blur for very smooth areas
        smooth_mask = cv2.GaussianBlur(img_array, (5, 5), 0)
        
        # Blend based on edge detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_mask = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        edge_mask_3ch = cv2.cvtColor(edge_mask, cv2.COLOR_GRAY2RGB) / 255.0
        
        # Keep original edges, smooth other areas
        result = cleaned * (1 - edge_mask_3ch) + img_array * edge_mask_3ch
        
        return result.astype(np.uint8)
    
    def _adjust_contrast_and_colors(self, img_array: np.ndarray) -> np.ndarray:
        """Final contrast and color adjustments"""
        
        img_pil = Image.fromarray(img_array)
        
        # Slight contrast enhancement
        contrast_enhancer = ImageEnhance.Contrast(img_pil)
        img_pil = contrast_enhancer.enhance(1.1)
        
        # Color saturation boost for vibrant game art
        color_enhancer = ImageEnhance.Color(img_pil)
        img_pil = color_enhancer.enhance(1.05)
        
        # Brightness fine-tuning
        brightness_enhancer = ImageEnhance.Brightness(img_pil)
        img_pil = brightness_enhancer.enhance(1.02)
        
        return np.array(img_pil)
    
    async def _apply_final_quality_optimization(self, img_array: np.ndarray) -> np.ndarray:
        """Apply final quality optimization techniques"""
        
        # Remove any remaining compression artifacts
        optimized = cv2.medianBlur(img_array, 3)
        
        # Blend with original to maintain detail
        final = img_array * 0.8 + optimized * 0.2
        
        return final.astype(np.uint8)
    
    async def _save_upscaled_asset(self, image: Image.Image, asset_name: str,
                                 asset_type: str, scale_factor: int) -> Path:
        """Save upscaled asset with comprehensive metadata"""
        
        output_dir = Path("assets/generated/upscaled")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = f"{asset_name}_{scale_factor}x_upscaled.png"
        output_path = output_dir / filename
        
        # Save image with optimization
        image.save(output_path, "PNG", optimize=True, compress_level=6)
        
        # Save metadata
        metadata = {
            "asset_name": asset_name,
            "asset_type": asset_type,
            "scale_factor": scale_factor,
            "original_dimensions": "unknown",  # Would need to be passed from caller
            "upscaled_dimensions": image.size,
            "upscaling_model": self._get_used_model(asset_type, scale_factor),
            "enhancements_applied": [
                "hieroglyph_sharpening",
                "gold_enhancement", 
                "divine_aura",
                "edge_enhancement",
                "artifact_reduction"
            ],
            "processing_time": time.time(),
            "quality_settings": {
                "compression_level": 6,
                "optimization": True
            }
        }
        
        metadata_path = output_dir / f"{asset_name}_{scale_factor}x_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def _get_used_model(self, asset_type: str, scale_factor: int) -> str:
        """Get the model that would be used for this asset type and scale"""
        model_key = self._select_upscaling_model(asset_type, scale_factor)
        return f"Real-ESRGAN_{model_key}" if model_key != "fallback" else "PIL_Lanczos"
    
    async def batch_upscale_egyptian_assets(self, asset_directory: str) -> Dict[str, Any]:
        """Batch upscale all assets in a directory"""
        
        print(f"Batch upscaling assets in: {asset_directory}")
        
        asset_dir = Path(asset_directory)
        if not asset_dir.exists():
            return {"status": "failed", "error": "Directory does not exist"}
        
        results = {}
        total_assets = 0
        successful_upscales = 0
        
        # Process all PNG images in directory
        for image_path in asset_dir.glob("*.png"):
            total_assets += 1
            
            try:
                # Load image
                input_image = Image.open(image_path)
                
                # Determine asset type from filename/path
                asset_type = self._determine_asset_type(image_path.name)
                
                # Upscale asset
                result = await self.upscale_egyptian_asset(
                    input_image=input_image,
                    asset_type=asset_type,
                    target_scale=4,
                    enhance_egyptian_features=True,
                    output_name=image_path.stem
                )
                
                if result["status"] == "success":
                    successful_upscales += 1
                
                results[image_path.name] = result
                
            except Exception as e:
                results[image_path.name] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return {
            "status": "completed",
            "total_assets": total_assets,
            "successful_upscales": successful_upscales,
            "success_rate": successful_upscales / total_assets if total_assets > 0 else 0,
            "results": results
        }
    
    def _determine_asset_type(self, filename: str) -> str:
        """Determine asset type from filename"""
        
        filename_lower = filename.lower()
        
        if any(term in filename_lower for term in ["player", "character", "anubis", "ra", "thoth", "isis"]):
            return "character_sprites"
        elif any(term in filename_lower for term in ["environment", "background", "temple", "pyramid"]):
            return "environment_assets"
        elif any(term in filename_lower for term in ["ui", "button", "frame", "bar"]):
            return "ui_elements"
        elif any(term in filename_lower for term in ["artifact", "altar", "weapon"]):
            return "artifacts"
        else:
            return "character_sprites"  # Default

# Test function
async def test_upscaling_system():
    """Test Real-ESRGAN upscaling system"""
    print("Testing Real-ESRGAN Upscaling System...")
    
    system = RealESRGANUpscalingSystem()
    
    # Setup models
    setup_success = await system.setup_upscaling_models()
    if not setup_success:
        print("Upscaling setup failed")
        return
    
    # Create test image
    test_image = Image.new("RGB", (256, 256), color=(100, 150, 200))
    
    # Test upscaling
    result = await system.upscale_egyptian_asset(
        input_image=test_image,
        asset_type="character_sprites",
        target_scale=4,
        enhance_egyptian_features=True,
        output_name="test_upscale"
    )
    
    print(f"Upscaling test result: {result}")

if __name__ == "__main__":
    asyncio.run(test_upscaling_system())