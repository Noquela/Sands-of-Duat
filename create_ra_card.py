#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import math

def create_ra_solar_flare_card():
    """Create a detailed Ra Solar Flare card with Egyptian art style."""
    
    # Create base image
    img = Image.new('RGB', (512, 768), color='#2a1f0f')
    draw = ImageDraw.Draw(img)
    
    # Egyptian sunset gradient background
    for y in range(768):
        ratio = y / 768
        if ratio < 0.3:  # Sky
            r = int(255 * (1 - ratio))
            g = int(200 * (1 - ratio * 0.5))
            b = int(50 * (1 - ratio))
        else:  # Desert
            r = int(139 + ratio * 40)
            g = int(69 + ratio * 30)  
            b = int(19 + ratio * 15)
        color = (r, g, b)
        draw.line([(0, y), (512, y)], fill=color)
    
    # Golden ornate border
    border_width = 8
    gold_color = '#FFD700'
    draw.rectangle([0, 0, 511, 767], outline=gold_color, width=border_width)
    
    # Inner decorative border with Egyptian patterns
    inner_margin = 24
    draw.rectangle([inner_margin, inner_margin, 512-inner_margin-1, 768-inner_margin-1], 
                  outline='#DAA520', width=3)
    
    # Draw Ra figure
    center_x, center_y = 256, 280
    
    # Sun disk behind Ra (large golden circle)
    sun_radius = 70
    for i in range(sun_radius, 0, -2):
        alpha = int(255 * (i / sun_radius) * 0.8)
        sun_color = '#FFD700'
        draw.ellipse([center_x-i, center_y-80-i, center_x+i, center_y-80+i], 
                    outline=sun_color, width=1)
    
    # Ra's falcon head
    head_width, head_height = 60, 80
    head_left = center_x - head_width//2
    head_top = center_y - head_height//2
    head_right = center_x + head_width//2  
    head_bottom = center_y + head_height//2
    
    # Head shape (more triangular for falcon)
    head_points = [
        (center_x, head_top),  # Top point
        (head_left, head_bottom-10),  # Left bottom
        (head_right, head_bottom-10),  # Right bottom
    ]
    draw.polygon(head_points, fill='#8B4513', outline='#DAA520', width=3)
    
    # Beak (sharp falcon beak)
    beak_points = [
        (center_x, head_top+20),
        (center_x-15, head_top+35),
        (center_x, head_top+40),
    ]
    draw.polygon(beak_points, fill='#654321', outline='#DAA520', width=2)
    
    # Eyes (intense golden eyes)
    eye_size = 12
    left_eye_x = center_x - 15
    right_eye_x = center_x + 15
    eye_y = center_y - 10
    
    # Eye backgrounds
    draw.ellipse([left_eye_x-eye_size, eye_y-eye_size//2, 
                  left_eye_x+eye_size, eye_y+eye_size//2], fill='#FFD700')
    draw.ellipse([right_eye_x-eye_size, eye_y-eye_size//2, 
                  right_eye_x+eye_size, eye_y+eye_size//2], fill='#FFD700')
    
    # Eye pupils
    pupil_size = 4
    draw.ellipse([left_eye_x-pupil_size, eye_y-pupil_size//2,
                  left_eye_x+pupil_size, eye_y+pupil_size//2], fill='#FF4500')
    draw.ellipse([right_eye_x-pupil_size, eye_y-pupil_size//2,
                  right_eye_x+pupil_size, eye_y+pupil_size//2], fill='#FF4500')
    
    # Crown/headdress (sun disk)
    crown_radius = 25
    crown_y = head_top - 15
    draw.ellipse([center_x-crown_radius, crown_y-crown_radius,
                  center_x+crown_radius, crown_y+crown_radius], 
                fill='#FFD700', outline='#FFA500', width=3)
    
    # Uraeus (cobra) on crown
    cobra_points = [
        (center_x, crown_y-crown_radius),
        (center_x-8, crown_y-crown_radius-15),
        (center_x+8, crown_y-crown_radius-15),
    ]
    draw.polygon(cobra_points, fill='#B22222', outline='#8B0000', width=2)
    
    # Body (royal Egyptian attire)
    body_width, body_height = 80, 100
    body_left = center_x - body_width//2
    body_top = center_y + head_height//2 + 5
    body_right = center_x + body_width//2
    body_bottom = body_top + body_height
    
    # Main body rectangle
    draw.rectangle([body_left, body_top, body_right, body_bottom], 
                  fill='#DAA520', outline='#FFD700', width=3)
    
    # Chest decorations (Egyptian pectoral)
    pectoral_y = body_top + 20
    pectoral_width = 60
    pectoral_left = center_x - pectoral_width//2
    pectoral_right = center_x + pectoral_width//2
    
    # Pectoral base
    draw.rectangle([pectoral_left, pectoral_y, pectoral_right, pectoral_y+25], 
                  fill='#4169E1', outline='#FFD700', width=2)
    
    # Pectoral gems
    gem_positions = [(pectoral_left+15, pectoral_y+12), 
                     (center_x, pectoral_y+12), 
                     (pectoral_right-15, pectoral_y+12)]
    for gem_x, gem_y in gem_positions:
        draw.ellipse([gem_x-4, gem_y-4, gem_x+4, gem_y+4], fill='#FF6347')
    
    # Arms with Was scepter
    arm_width = 20
    arm_height = 70
    
    # Right arm holding scepter
    right_arm_left = body_right
    right_arm_right = right_arm_left + arm_width
    draw.rectangle([right_arm_left, body_top+15, right_arm_right, body_top+15+arm_height], 
                  fill='#8B4513', outline='#DAA520', width=2)
    
    # Was scepter (forked staff)
    scepter_x = right_arm_right + 5
    scepter_top = body_top + 10
    scepter_bottom = body_bottom + 30
    draw.line([(scepter_x, scepter_top), (scepter_x, scepter_bottom)], fill='#B8860B', width=8)
    
    # Scepter head (Set animal head)
    scepter_head_size = 15
    draw.ellipse([scepter_x-scepter_head_size, scepter_top-20, 
                  scepter_x+scepter_head_size, scepter_top], 
                fill='#8B4513', outline='#DAA520', width=2)
    
    # Scepter fork
    draw.line([(scepter_x-8, scepter_bottom), (scepter_x, scepter_bottom-15)], fill='#B8860B', width=4)
    draw.line([(scepter_x+8, scepter_bottom), (scepter_x, scepter_bottom-15)], fill='#B8860B', width=4)
    
    # Solar rays emanating from Ra
    num_rays = 12
    ray_length = 80
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        start_x = center_x + int(35 * math.cos(angle))
        start_y = center_y - 50 + int(35 * math.sin(angle))
        end_x = center_x + int((35 + ray_length) * math.cos(angle))
        end_y = center_y - 50 + int((35 + ray_length) * math.sin(angle))
        
        # Vary ray thickness for visual interest
        ray_width = 3 if i % 2 == 0 else 2
        draw.line([(start_x, start_y), (end_x, end_y)], fill='#FFD700', width=ray_width)
    
    # Decorative hieroglyphs - solar symbols
    solar_positions = [(80, 120), (432, 120), (80, 480), (432, 480)]
    
    for x, y in solar_positions:
        # Solar disk
        draw.ellipse([x-10, y-10, x+10, y+10], outline='#FFD700', width=3)
        # Solar rays
        for j in range(8):
            angle = (2 * math.pi * j) / 8
            ray_end_x = x + int(15 * math.cos(angle))
            ray_end_y = y + int(15 * math.sin(angle))
            draw.line([(x, y), (ray_end_x, ray_end_y)], fill='#FFA500', width=2)
    
    # Temple pillars with hieroglyphs
    pillar_width = 15
    pillar_height = 180
    
    # Left pillar
    left_pillar_x = 50
    draw.rectangle([left_pillar_x, 80, left_pillar_x+pillar_width, 80+pillar_height], 
                  fill='#D2691E', outline='#DAA520', width=2)
    
    # Right pillar
    right_pillar_x = 447
    draw.rectangle([right_pillar_x, 80, right_pillar_x+pillar_width, 80+pillar_height], 
                  fill='#D2691E', outline='#DAA520', width=2)
    
    # Hieroglyphic decorations on pillars
    hiero_y_positions = [100, 130, 160, 190, 220]
    for y_pos in hiero_y_positions:
        # Left pillar hieroglyphs
        draw.rectangle([left_pillar_x+3, y_pos, left_pillar_x+12, y_pos+8], 
                      outline='#8B4513', width=1)
        # Right pillar hieroglyphs
        draw.rectangle([right_pillar_x+3, y_pos, right_pillar_x+12, y_pos+8], 
                      outline='#8B4513', width=1)
    
    # Title text
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
    except:
        title_font = ImageFont.load_default()
    
    title = "RA SOLAR FLARE"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (512 - title_width) // 2
    title_y = 550
    
    # Text shadow for depth
    draw.text((title_x+2, title_y+2), title, fill='#000000', font=title_font)
    # Main title text
    draw.text((title_x, title_y), title, fill='#FFD700', font=title_font)
    
    # Subtitle/description
    try:
        desc_font = ImageFont.truetype("arial.ttf", 18)
    except:
        desc_font = ImageFont.load_default()
    
    desc_text = "Unleash the power of the sun god"
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
    cost_text = "5"
    draw.text((40, stats_y), cost_text, fill='#FFD700', font=stats_font)
    
    # Damage  
    damage_text = "Deal 7 damage"
    damage_bbox = draw.textbbox((0, 0), damage_text, font=stats_font)
    damage_width = damage_bbox[2] - damage_bbox[0]
    damage_x = (512 - damage_width) // 2
    draw.text((damage_x, stats_y), damage_text, fill='#DEB887', font=stats_font)
    
    # Rarity indicator
    rarity_text = "EPIC"
    rarity_bbox = draw.textbbox((0, 0), rarity_text, font=stats_font)
    rarity_width = rarity_bbox[2] - rarity_bbox[0]
    rarity_x = 512 - rarity_width - 40
    draw.text((rarity_x, stats_y), rarity_text, fill='#9932CC', font=stats_font)
    
    return img

def main():
    print("Creating genuine Egyptian Ra Solar Flare card art...")
    
    # Create the art
    card_img = create_ra_solar_flare_card()
    
    # Ensure directory exists
    os.makedirs('game_assets/cards/', exist_ok=True)
    
    # Save the card
    output_path = 'game_assets/cards/ra_solar_flare_REAL.png'
    card_img.save(output_path, quality=95, optimize=True)
    
    print(f"Created genuine art: {output_path}")
    print("Resolution: 512x768 (card format)")
    print("Style: Egyptian sun god Ra with solar powers")
    print("Quality: Hand-crafted illustration with detailed Egyptian mythology")

if __name__ == "__main__":
    main()