#!/usr/bin/env python3
"""
PBR Material Generation for Hades-Quality 3D Assets
Generates Albedo, Normal, Roughness, Metallic, and AO maps
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path
import os

class PBRMaterialGenerator:
    def __init__(self):
        self.input_dir = Path("tools/ai_pipeline/tools/ai_pipeline/outputs/characters")
        # Check if the nested path exists, otherwise use direct path
        if not self.input_dir.exists():
            self.input_dir = Path("tools/ai_pipeline/outputs/characters")
        self.output_dir = Path("assets/3d/textures/pbr")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_pbr_set(self, albedo_path, character_name):
        """Generate complete PBR material set from albedo map"""
        print(f"Generating PBR materials for {character_name}...")
        
        # Load albedo image
        try:
            albedo = Image.open(albedo_path)
            albedo_cv = cv2.cvtColor(np.array(albedo), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error loading image {albedo_path}: {e}")
            return None
        
        # Generate Normal Map
        normal_map = self.generate_normal_map(albedo_cv)
        normal_path = self.output_dir / f"{character_name}_normal.png"
        cv2.imwrite(str(normal_path), normal_map)
        
        # Generate Roughness Map
        roughness_map = self.generate_roughness_map(albedo_cv)
        roughness_path = self.output_dir / f"{character_name}_roughness.png"
        cv2.imwrite(str(roughness_path), roughness_map)
        
        # Generate Metallic Map
        metallic_map = self.generate_metallic_map(albedo_cv)
        metallic_path = self.output_dir / f"{character_name}_metallic.png"
        cv2.imwrite(str(metallic_path), metallic_map)
        
        # Generate AO Map
        ao_map = self.generate_ao_map(albedo_cv)
        ao_path = self.output_dir / f"{character_name}_ao.png"
        cv2.imwrite(str(ao_path), ao_map)
        
        # Save enhanced albedo
        enhanced_albedo = self.enhance_albedo(albedo)
        albedo_path = self.output_dir / f"{character_name}_albedo.png"
        enhanced_albedo.save(albedo_path)
        
        print(f"  Generated complete PBR set for {character_name}")
        return {
            "albedo": albedo_path,
            "normal": normal_path,
            "roughness": roughness_path,
            "metallic": metallic_path,
            "ao": ao_path
        }
    
    def generate_normal_map(self, image):
        """Generate normal map from albedo"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Calculate gradients
        grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        
        # Normalize and convert to normal map
        normal = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        normal[:, :, 0] = np.clip(127 + grad_x * 0.5, 0, 255)  # Red = X
        normal[:, :, 1] = np.clip(127 - grad_y * 0.5, 0, 255)  # Green = Y
        normal[:, :, 2] = 255  # Blue = Z (up)
        
        return normal
    
    def generate_roughness_map(self, image):
        """Generate roughness map"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use variance to determine roughness
        kernel = np.ones((5, 5), np.float32) / 25
        smooth = cv2.filter2D(gray, -1, kernel)
        roughness = np.abs(gray.astype(np.float32) - smooth.astype(np.float32))
        
        # Normalize and enhance
        roughness = np.clip(roughness * 3 + 100, 0, 255).astype(np.uint8)
        
        return cv2.cvtColor(roughness, cv2.COLOR_GRAY2BGR)
    
    def generate_metallic_map(self, image):
        """Generate metallic map based on color analysis"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detect metallic areas (high saturation + specific hue ranges)
        metallic = np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Gold/brass detection
        gold_mask = cv2.inRange(hsv, (15, 100, 100), (35, 255, 255))
        metallic = cv2.bitwise_or(metallic, gold_mask)
        
        # Silver detection  
        silver_mask = cv2.inRange(hsv, (0, 0, 180), (255, 30, 255))
        metallic = cv2.bitwise_or(metallic, silver_mask)
        
        return cv2.cvtColor(metallic, cv2.COLOR_GRAY2BGR)
    
    def generate_ao_map(self, image):
        """Generate ambient occlusion map"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create AO effect using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        ao = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        # Enhance contrast
        ao = cv2.equalizeHist(ao)
        
        return cv2.cvtColor(ao, cv2.COLOR_GRAY2BGR)
    
    def enhance_albedo(self, image):
        """Enhance albedo for game use"""
        # Increase saturation
        enhancer = ImageEnhance.Color(image)
        enhanced = enhancer.enhance(1.2)
        
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        return enhanced

def main():
    generator = PBRMaterialGenerator()
    
    print("Generating PBR materials from concept art...")
    
    # Process all generated character concept images
    characters_processed = 0
    
    for concept_file in generator.input_dir.glob("*.png"):
        if concept_file.is_file() and "concept" in concept_file.name:
            # Extract character name from filename
            character_name = concept_file.stem
            character_name = character_name.replace("_concept_v1", "").replace("_concept_v2", "").replace("_concept_v3", "")
            
            # Only process one version per character to avoid duplicates
            if "v1" in concept_file.name:
                pbr_set = generator.generate_pbr_set(concept_file, character_name)
                if pbr_set:
                    characters_processed += 1
                    print(f"PBR materials generated for {character_name}")
    
    print(f"\nPBR generation complete! Processed {characters_processed} characters")
    print(f"Materials saved to: {generator.output_dir}")

if __name__ == "__main__":
    main()