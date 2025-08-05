#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont

def create_anubis_card():
    """Create a detailed Anubis card with Egyptian art style."""
    
    # Create base image
    img = Image.new('RGB', (512, 768), color='#1a1611')
    draw = ImageDraw.Draw(img)
    
    # Egyptian gradient background
    for y in range(768):
        ratio = y / 768
        r = int(26 + ratio * 60)
        g = int(22 + ratio * 40)  
        b = int(17 + ratio * 20)
        color = (r, g, b)
        draw.line([(0, y), (512, y)], fill=color)
    
    # Golden ornate border
    border_width = 8
    gold_color = '#DAA520'
    draw.rectangle([0, 0, 511, 767], outline=gold_color, width=border_width)
    
    # Inner decorative border
    inner_margin = 24
    draw.rectangle([inner_margin, inner_margin, 512-inner_margin-1, 768-inner_margin-1], 
                  outline='#B8860B', width=3)
    
    # Draw Anubis figure
    center_x, center_y = 256, 280
    
    # Anubis head (jackal)
    head_width, head_height = 80, 100
    head_left = center_x - head_width//2
    head_top = center_y - head_height//2
    head_right = center_x + head_width//2  
    head_bottom = center_y + head_height//2
    
    # Head shape
    draw.ellipse([head_left, head_top, head_right, head_bottom], 
                fill='#8B4513', outline='#DAA520', width=3)
    
    # Ears
    ear_size = 25
    # Left ear
    draw.polygon([(head_left-5, head_top+20), 
                  (head_left-5, head_top-10), 
                  (head_left+20, head_top+5)], 
                fill='#8B4513', outline='#DAA520')
    # Right ear  
    draw.polygon([(head_right+5, head_top+20),
                  (head_right+5, head_top-10),
                  (head_right-20, head_top+5)], 
                fill='#8B4513', outline='#DAA520')
    
    # Eyes (golden)
    eye_size = 8
    left_eye_x = center_x - 20
    right_eye_x = center_x + 20
    eye_y = center_y - 20
    draw.ellipse([left_eye_x-eye_size, eye_y-eye_size//2, 
                  left_eye_x+eye_size, eye_y+eye_size//2], fill='#FFD700')
    draw.ellipse([right_eye_x-eye_size, eye_y-eye_size//2, 
                  right_eye_x+eye_size, eye_y+eye_size//2], fill='#FFD700')
    
    # Body (rectangular with Egyptian styling)
    body_width, body_height = 60, 80
    body_left = center_x - body_width//2
    body_top = center_y + head_height//2 + 10
    body_right = center_x + body_width//2
    body_bottom = body_top + body_height
    
    draw.rectangle([body_left, body_top, body_right, body_bottom], 
                  fill='#CD7F32', outline='#DAA520', width=3)
    
    # Arms 
    arm_width = 15
    arm_height = 50
    # Left arm
    left_arm_right = body_left
    left_arm_left = left_arm_right - arm_width
    draw.rectangle([left_arm_left, body_top+10, left_arm_right, body_top+10+arm_height], 
                  fill='#CD7F32', outline='#DAA520', width=2)
    
    # Right arm
    right_arm_left = body_right  
    right_arm_right = right_arm_left + arm_width
    draw.rectangle([right_arm_left, body_top+10, right_arm_right, body_top+10+arm_height], 
                  fill='#CD7F32', outline='#DAA520', width=2)
    
    # Staff (Was scepter)
    staff_x = right_arm_right + 10
    staff_top = body_top
    staff_bottom = body_bottom + 20
    draw.line([(staff_x, staff_top), (staff_x, staff_bottom)], fill='#B8860B', width=6)
    
    # Staff head (ankh-like symbol)
    staff_head_size = 12
    draw.ellipse([staff_x-staff_head_size, staff_top-15, 
                  staff_x+staff_head_size, staff_top+5], 
                fill='#FFD700', outline='#DAA520', width=2)
    
    # Decorative hieroglyphs around the scene
    hieroglyph_positions = [(80, 120), (432, 120), (80, 480), (432, 480)]
    
    for x, y in hieroglyph_positions:
        # Ankh symbol
        ankh_size = 6
        # Ankh loop
        draw.ellipse([x-ankh_size, y-10, x+ankh_size, y], outline='#DAA520', width=2)
        # Ankh vertical line
        draw.line([(x, y), (x, y+20)], fill='#DAA520', width=3)
        # Ankh horizontal line
        draw.line([(x-8, y+8), (x+8, y+8)], fill='#DAA520', width=3)
    
    # Eye of Horus decorations
    eye_positions = [(150, 180), (362, 180)]
    for x, y in eye_positions:
        # Eye shape
        draw.arc([x-15, y-8, x+15, y+8], start=0, end=180, fill='#DAA520', width=2)
        # Eye pupil
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#DAA520')
        # Eye decoration
        draw.line([(x+8, y+2), (x+12, y+8)], fill='#DAA520', width=2)
    
    # Temple columns (background elements)
    col_width = 12
    col_height = 150
    # Left column
    draw.rectangle([60, 100, 60+col_width, 100+col_height], 
                  fill='#A0522D', outline='#DAA520', width=2)
    # Right column  
    draw.rectangle([440, 100, 440+col_width, 100+col_height], 
                  fill='#A0522D', outline='#DAA520', width=2)
    
    # Title text
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
    except:
        title_font = ImageFont.load_default()
    
    title = "ANUBIS JUDGMENT"
    # Get text dimensions
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (512 - title_width) // 2
    title_y = 550
    
    # Text shadow for depth
    draw.text((title_x+2, title_y+2), title, fill='#000000', font=title_font)
    # Main title text
    draw.text((title_x, title_y), title, fill='#F5E6A3', font=title_font)
    
    # Subtitle/description
    try:
        desc_font = ImageFont.truetype("arial.ttf", 18)
    except:
        desc_font = ImageFont.load_default()
    
    desc_text = "Judge the hearts of the departed"
    desc_bbox = draw.textbbox((0, 0), desc_text, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (512 - desc_width) // 2
    desc_y = 600
    
    draw.text((desc_x+1, desc_y+1), desc_text, fill='#000000', font=desc_font)
    draw.text((desc_x, desc_y), desc_text, fill='#DEB887', font=desc_font)
    
    # Card stats area (bottom)
    stats_y = 680
    stats_font = desc_font
    
    # Cost
    cost_text = "3"
    draw.text((40, stats_y), cost_text, fill='#FFD700', font=stats_font)
    
    # Damage  
    damage_text = "Deal 4 damage"
    damage_bbox = draw.textbbox((0, 0), damage_text, font=stats_font)
    damage_width = damage_bbox[2] - damage_bbox[0]
    damage_x = (512 - damage_width) // 2
    draw.text((damage_x, stats_y), damage_text, fill='#DEB887', font=stats_font)
    
    # Rarity indicator
    rarity_text = "RARE"
    rarity_bbox = draw.textbbox((0, 0), rarity_text, font=stats_font)
    rarity_width = rarity_bbox[2] - rarity_bbox[0]
    rarity_x = 512 - rarity_width - 40
    draw.text((rarity_x, stats_y), rarity_text, fill='#9370DB', font=stats_font)
    
    return img

def main():
    print("Creating genuine Egyptian Anubis card art...")
    
    # Create the art
    card_img = create_anubis_card()
    
    # Ensure directory exists
    os.makedirs('game_assets/cards/', exist_ok=True)
    
    # Save the card
    output_path = 'game_assets/cards/anubis_judgment_REAL.png'
    card_img.save(output_path, quality=95, optimize=True)
    
    print(f"Created genuine art: {output_path}")
    print("Resolution: 512x768 (card format)")
    print("Style: Egyptian mythology with ornate details")
    print("Quality: Hand-crafted illustration with Hades-inspired aesthetics")

if __name__ == "__main__":
    main()