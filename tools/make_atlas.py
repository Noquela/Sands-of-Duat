#!/usr/bin/env python
from PIL import Image
import sys, pathlib, json, math

src = pathlib.Path(sys.argv[1])   # folder with PNG RGBA frames (no background)
out_img = pathlib.Path(sys.argv[2])
out_meta = pathlib.Path(sys.argv[3])

frames = sorted(src.glob("*.png"))
assert frames, f"No frames found in {src}"

print(f"Creating atlas from {len(frames)} frames...")
imgs = [Image.open(f).convert("RGBA") for f in frames]
w, h = imgs[0].size

# Calculate grid layout
cols = math.ceil(math.sqrt(len(imgs)))
rows = math.ceil(len(imgs) / cols)
atlas = Image.new("RGBA", (cols*w, rows*h), (0,0,0,0))

# Pack frames and generate metadata
meta = {"w": w, "h": h, "cols": cols, "rows": rows, "frames": []}
for i, im in enumerate(imgs):
    cx, cy = i % cols, i // cols
    atlas.paste(im, (cx*w, cy*h))
    meta["frames"].append({"i": i, "x": cx*w, "y": cy*h, "w": w, "h": h, "name": frames[i].stem})

out_img.parent.mkdir(parents=True, exist_ok=True)
atlas.save(out_img)
out_meta.write_text(json.dumps(meta, indent=2))
print(f"OK: make_atlas -> {out_img} ({out_meta})")
print(f"Atlas size: {cols}x{rows} = {cols*rows} slots for {len(imgs)} frames")