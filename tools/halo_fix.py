#!/usr/bin/env python
from PIL import Image, ImageFilter
import sys, pathlib

inp = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

def fix_one(p):
    print(f"Fixing halo for {p.name}...")
    im = Image.open(p).convert("RGBA")
    rgb, a = im.split()[:3], im.split()[3]
    
    # Clean up alpha channel - slight erosion and blur to remove halos
    a = a.filter(ImageFilter.MinFilter(3))
    a = a.filter(ImageFilter.GaussianBlur(0.5))
    
    result = Image.merge("RGBA", (*rgb, a))
    output_path = out / p.name
    result.save(output_path)
    print(f"Fixed: {output_path}")

if inp.is_file():
    fix_one(inp)
else:
    for f in inp.glob("*.png"):
        fix_one(f)
print("OK: halo_fix completed")