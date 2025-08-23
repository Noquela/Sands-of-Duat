#!/usr/bin/env python3
"""
Fast placeholder concept generator for testing
Creates simple colored rectangles with character info
"""

import os
import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

def generate_placeholder_concept(character_name: str, prompt: str, output_dir: str):
    """Generate a placeholder concept art image"""
    print(f"Generating placeholder concept for: {character_name}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a 1024x1024 image
    width, height = 1024, 1024
    
    # Choose color based on character type
    if "pharaoh" in character_name.lower() or "hero" in character_name.lower():
        bg_color = (180, 140, 70)  # Golden brown
        text_color = (255, 215, 0)  # Gold
    elif "anubis" in character_name.lower():
        bg_color = (50, 50, 100)  # Dark blue
        text_color = (200, 200, 255)  # Light blue
    elif "mummy" in character_name.lower():
        bg_color = (140, 120, 80)  # Sandy brown
        text_color = (200, 180, 140)  # Light tan
    else:
        bg_color = (100, 100, 100)  # Gray
        text_color = (200, 200, 200)  # Light gray
    
    # Create image
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font
    try:
        font_size = 48
        font = ImageFont.truetype("arial.ttf", font_size)
        title_font = ImageFont.truetype("arial.ttf", font_size + 20)
    except:
        font = ImageFont.load_default()
        title_font = font
    
    # Draw character name
    title_text = character_name.replace('_', ' ').title()
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 100), title_text, fill=text_color, font=title_font)
    
    # Draw a simple character silhouette
    if "hero" in character_name.lower():
        # Draw heroic figure
        draw.ellipse([450, 300, 574, 424], fill=text_color)  # Head
        draw.rectangle([462, 424, 562, 624], fill=text_color)  # Body
        draw.rectangle([412, 454, 462, 594], fill=text_color)  # Left arm
        draw.rectangle([562, 454, 612, 594], fill=text_color)  # Right arm
        draw.rectangle([482, 624, 522, 824], fill=text_color)  # Left leg
        draw.rectangle([542, 624, 582, 824], fill=text_color)  # Right leg
    elif "boss" in character_name.lower():
        # Draw larger boss figure
        draw.ellipse([430, 250, 594, 414], fill=text_color)  # Head
        draw.rectangle([442, 414, 582, 674], fill=text_color)  # Body
        draw.rectangle([372, 444, 442, 644], fill=text_color)  # Left arm
        draw.rectangle([582, 444, 652, 644], fill=text_color)  # Right arm
        draw.rectangle([462, 674, 502, 874], fill=text_color)  # Left leg
        draw.rectangle([522, 674, 562, 874], fill=text_color)  # Right leg
    else:
        # Draw generic figure
        draw.ellipse([462, 350, 562, 450], fill=text_color)  # Head
        draw.rectangle([482, 450, 542, 600], fill=text_color)  # Body
        draw.rectangle([452, 470, 482, 580], fill=text_color)  # Left arm
        draw.rectangle([542, 470, 572, 580], fill=text_color)  # Right arm
        draw.rectangle([492, 600, 512, 750], fill=text_color)  # Left leg
        draw.rectangle([512, 600, 532, 750], fill=text_color)  # Right leg
    
    # Draw prompt text (wrapped)
    prompt_lines = []
    words = prompt.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < width - 100:
            current_line = test_line
        else:
            if current_line:
                prompt_lines.append(current_line)
            current_line = word
    
    if current_line:
        prompt_lines.append(current_line)
    
    # Draw prompt lines
    y_pos = height - 200
    for line in prompt_lines[-3:]:  # Only show last 3 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x_pos = (width - line_width) // 2
        draw.text((x_pos, y_pos), line, fill=text_color, font=font)
        y_pos += 40
    
    # Save the image
    concept_path = Path(output_dir) / f"{character_name}_concept.png"
    image.save(concept_path, "PNG")
    
    # Save metadata
    metadata = {
        "character_name": character_name,
        "style": "placeholder_concept",
        "resolution": f"{width}x{height}",
        "prompt": prompt
    }
    
    metadata_path = Path(output_dir) / f"{character_name}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Placeholder concept saved: {concept_path}")
    return concept_path

def main():
    parser = argparse.ArgumentParser(description="Generate placeholder concept art")
    parser.add_argument("--character", required=True, help="Character name")
    parser.add_argument("--prompt", help="Character description")
    parser.add_argument("--output", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    prompt = args.prompt or f"Placeholder concept for {args.character}"
    generate_placeholder_concept(args.character, prompt, args.output)
    
    print(f"Placeholder concept for '{args.character}' generated successfully!")
    return 0

if __name__ == "__main__":
    main()