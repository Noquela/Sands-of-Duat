#!/usr/bin/env python3
"""
SANDS OF DUAT - Background Removal Pipeline
Remove backgrounds from SDXL generated concepts using U²‑Net
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import cv2

def remove_background_rembg(input_path, output_path):
    """Remove background using rembg U²‑Net model."""
    try:
        from rembg import remove
        
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
            
        # Remove background
        output_data = remove(input_data)
        
        # Save as PNG with alpha
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
            
        print(f"[SUCCESS] Background removed: {output_path}")
        return True
        
    except ImportError:
        print("[ERROR] rembg not installed. Run: pip install rembg")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to remove background: {e}")
        return False

def remove_background_manual(input_path, output_path, bg_color=(0, 255, 0)):
    """Manual background removal for solid color backgrounds."""
    try:
        # Load image
        img = cv2.imread(str(input_path))
        if img is None:
            return False
            
        # Convert to RGBA
        img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        
        # Create mask for background color (with tolerance)
        lower = np.array([bg_color[2] - 20, bg_color[1] - 20, bg_color[0] - 20])
        upper = np.array([bg_color[2] + 20, bg_color[1] + 20, bg_color[0] + 20])
        
        mask = cv2.inRange(img[:,:,:3], lower, upper)
        
        # Set alpha channel (transparent where mask is white)
        img_rgba[:, :, 3] = 255 - mask
        
        # Save as PNG
        cv2.imwrite(str(output_path), img_rgba)
        
        print(f"[SUCCESS] Manual BG removal: {output_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Manual BG removal failed: {e}")
        return False

def clean_backgrounds(input_dir, output_dir, method="auto"):
    """Clean backgrounds from all images in directory."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"[ERROR] Input directory not found: {input_path}")
        return
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[INFO] Processing images from {input_path} to {output_path}")
    print(f"[INFO] Method: {method}")
    
    # Process all images
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp'}
    processed = 0
    
    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            output_file = output_path / f"{img_file.stem}_clean.png"
            
            if method == "rembg":
                success = remove_background_rembg(img_file, output_file)
            elif method == "green":
                success = remove_background_manual(img_file, output_file, (0, 255, 0))
            else:  # auto
                # Try rembg first, fallback to manual
                success = remove_background_rembg(img_file, output_file)
                if not success:
                    success = remove_background_manual(img_file, output_file, (0, 255, 0))
            
            if success:
                processed += 1
    
    print(f"\\n[COMPLETE] Processed {processed} images")
    print(f"[OUTPUT] Clean images saved to: {output_path.absolute()}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_bg.py <input_dir> <output_dir> [method]")
        print("Methods: auto, rembg, green")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    method = sys.argv[3] if len(sys.argv) > 3 else "auto"
    
    clean_backgrounds(input_dir, output_dir, method)