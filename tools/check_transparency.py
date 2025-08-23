#!/usr/bin/env python
from PIL import Image
import sys, pathlib

def check_transparency(img_path):
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    total_pixels = width * height
    transparent_pixels = 0
    semi_transparent = 0
    opaque_pixels = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a == 0:
                transparent_pixels += 1
            elif a == 255:
                opaque_pixels += 1
            else:
                semi_transparent += 1
    
    print(f"{img_path.name}:")
    print(f"  Total pixels: {total_pixels}")
    print(f"  Transparent: {transparent_pixels} ({transparent_pixels/total_pixels*100:.1f}%)")
    print(f"  Semi-transparent: {semi_transparent} ({semi_transparent/total_pixels*100:.1f}%)")
    print(f"  Opaque: {opaque_pixels} ({opaque_pixels/total_pixels*100:.1f}%)")
    
    has_transparency = (transparent_pixels + semi_transparent) > 0
    print(f"  Has transparency: {has_transparency}")
    return has_transparency

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_transparency.py <image_or_folder>")
        sys.exit(1)
    
    path = pathlib.Path(sys.argv[1])
    if path.is_file():
        check_transparency(path)
    else:
        for png_file in path.glob("*.png"):
            check_transparency(png_file)
            print()