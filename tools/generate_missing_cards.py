#!/usr/bin/env python3
"""
Generate Missing Card Assets for Sands of Duat
Creates AI-generated textures for cards that don't have assets yet.
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.gen_art import ArtGenerator
    AI_AVAILABLE = True
except ImportError:
    print("AI art generation not available, creating placeholder cards")
    AI_AVAILABLE = False

from PIL import Image, ImageDraw, ImageFont


class MissingCardGenerator:
    """Generate missing card assets for the game."""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.output_dir = project_root / "assets" / "textures" / "cards"
        self.godot_cards_dir = project_root / "godot" / "novo-projeto-de-jogo" / "cards"
        
        # Ensure output directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.godot_cards_dir.mkdir(parents=True, exist_ok=True)
        
        # Card specifications
        self.missing_cards = [
            "Desert Whisper",
            "Sand Grain", 
            "Tomb Strike",
            "Ankh Blessing",
            "Scarab Swarm",
            "Papyrus Scroll",
            "Mummy's Wrath",
            "Isis's Grace",
            "Thoth's Wisdom",
            "Ra's Solar Flare",
            "Pharaoh's Resurrection"
        ]
        
        # Egyptian-themed prompts for each card
        self.card_prompts = {
            "Desert Whisper": "Ancient Egyptian papyrus with mystical hieroglyphs glowing, sand particles swirling, magical aura, detailed art, card game style",
            "Sand Grain": "Single golden sand grain magnified, Egyptian desert background, detailed texture, warm lighting, trading card art style",
            "Tomb Strike": "Egyptian sarcophagus with energy burst, golden rays, ancient tomb interior, action scene, detailed illustration",
            "Ankh Blessing": "Golden ankh symbol glowing with divine light, Egyptian temple background, holy aura, detailed religious art",
            "Scarab Swarm": "Swarm of golden scarab beetles, Egyptian hieroglyphs, detailed insect art, mystical energy, trading card style",
            "Papyrus Scroll": "Ancient papyrus scroll with glowing hieroglyphs, Egyptian writing, detailed texture, warm candlelight",
            "Mummy's Wrath": "Angry mummy emerging from sarcophagus, bandages flowing, Egyptian tomb, detailed horror art, dramatic lighting",
            "Isis's Grace": "Goddess Isis with outstretched wings, divine light, Egyptian temple, detailed mythological art, golden colors",
            "Thoth's Wisdom": "Ibis-headed god Thoth with scroll and quill, Egyptian library, detailed deity art, scholarly atmosphere",
            "Ra's Solar Flare": "Sun god Ra with brilliant solar flare, Egyptian sun disk, intense golden light, powerful divine art",
            "Pharaoh's Resurrection": "Pharaoh rising from golden sarcophagus, divine restoration, Egyptian tomb, detailed royal art, magical energy"
        }
    
    def _setup_logging(self):
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "card_generation.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def create_placeholder_card(self, card_name: str) -> str:
        """Create a placeholder card image."""
        # Create 512x512 card image
        img = Image.new('RGB', (512, 512), color='#2C1810')  # Dark brown
        draw = ImageDraw.Draw(img)
        
        # Try to load a better font, fallback to default
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw Egyptian-themed background
        # Gold border
        border_width = 8
        draw.rectangle(
            [border_width, border_width, 512-border_width, 512-border_width],
            outline='#DAA520',  # Goldenrod
            width=border_width
        )
        
        # Inner background with Egyptian pattern
        inner_color = '#8B4513'  # Saddle brown
        draw.rectangle([border_width*2, border_width*2, 512-border_width*2, 512-border_width*2], 
                      fill=inner_color)
        
        # Card title area
        title_height = 80
        draw.rectangle([border_width*2, border_width*2, 512-border_width*2, border_width*2 + title_height],
                      fill='#DAA520')
        
        # Draw card name
        text_bbox = draw.textbbox((0, 0), card_name, font=font_large)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        text_x = (512 - text_width) // 2
        text_y = border_width*2 + (title_height - text_height) // 2
        
        draw.text((text_x, text_y), card_name, fill='#2C1810', font=font_large)
        
        # Add Egyptian symbols/decorations
        # Simple hieroglyph-like decorations
        symbol_y = 200
        for i in range(3):
            x = 100 + i * 150
            # Simple ankh-like symbol
            draw.ellipse([x-10, symbol_y-10, x+10, symbol_y+10], outline='#DAA520', width=3)
            draw.line([x, symbol_y+10, x, symbol_y+40], fill='#DAA520', width=3)
            draw.line([x-8, symbol_y+25, x+8, symbol_y+25], fill='#DAA520', width=3)
        
        # Add "SANDS OF DUAT" text at bottom
        footer_text = "SANDS OF DUAT"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=font_small)
        footer_width = footer_bbox[2] - footer_bbox[0]
        footer_x = (512 - footer_width) // 2
        footer_y = 512 - 40
        
        draw.text((footer_x, footer_y), footer_text, fill='#DAA520', font=font_small)
        
        # Save image
        filename = card_name.lower().replace(" ", "_").replace("'", "")
        filepath = self.output_dir / f"{filename}.png"
        img.save(filepath, "PNG")
        
        return str(filepath)
    
    def generate_ai_card(self, card_name: str) -> str:
        """Generate card using AI if available."""
        if not AI_AVAILABLE:
            return self.create_placeholder_card(card_name)
        
        try:
            # Initialize AI generator
            generator = ArtGenerator(model="sdturbo", medvram=True)
            
            # Get prompt for this card
            prompt = self.card_prompts.get(card_name, f"Egyptian themed trading card art for {card_name}")
            
            # Generate image
            filename = card_name.lower().replace(" ", "_").replace("'", "")
            output_path = self.output_dir / f"{filename}.png"
            
            self.logger.info(f"Generating AI art for: {card_name}")
            
            # Use the art generator
            image = generator.generate_image(
                prompt=prompt,
                width=512,
                height=512,
                num_inference_steps=4,
                guidance_scale=1.0
            )
            
            if image:
                image.save(output_path)
                self.logger.info(f"Generated: {output_path}")
                return str(output_path)
            else:
                self.logger.warning(f"AI generation failed for {card_name}, creating placeholder")
                return self.create_placeholder_card(card_name)
                
        except Exception as e:
            self.logger.error(f"Error generating AI art for {card_name}: {e}")
            return self.create_placeholder_card(card_name)
    
    def copy_to_godot(self, source_path: str, card_name: str):
        """Copy generated card to Godot project."""
        import shutil
        
        filename = card_name.lower().replace(" ", "_").replace("'", "")
        dest_path = self.godot_cards_dir / f"{filename}.png"
        
        shutil.copy2(source_path, dest_path)
        
        # Create import file
        import_content = f'''[remap]

importer="texture"
type="CompressedTexture2D"
uid="uid://generate_unique_id"
path="res://.godot/imported/{filename}.png-placeholder_hash.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="res://cards/{filename}.png"
dest_files=["res://.godot/imported/{filename}.png-placeholder_hash.ctex"]

[params]

compress/mode=0
compress/high_quality=false
compress/lossy_quality=0.7
compress/hdr_compression=1
compress/normal_map=0
compress/channel_pack=0
mipmaps/generate=false
mipmaps/limit=-1
roughness/mode=0
roughness/src_normal=""
process/fix_alpha_border=true
process/premult_alpha=false
process/normal_map_invert_y=false
process/hdr_as_srgb=false
process/hdr_clamp_exposure=false
process/size_limit=0
detect_3d/compress_to=1
'''
        
        import_file = dest_path.with_suffix('.png.import')
        with open(import_file, 'w') as f:
            f.write(import_content)
        
        self.logger.info(f"Copied to Godot: {dest_path}")
    
    def create_godot_scene(self, card_name: str):
        """Create Godot scene file for the card."""
        filename = card_name.lower().replace(" ", "_").replace("'", "")
        display_name = card_name
        
        scene_content = f'''[gd_scene load_steps=2 format=3 uid="uid://generate_unique_id"]

[ext_resource type="Texture2D" uid="uid://placeholder" path="res://cards/{filename}.png" id="1_placeholder"]

[node name="{card_name.replace(' ', '').replace("'", "")}" type="Control"]
layout_mode = 3
anchors_preset = 0

[node name="CardBackground" type="NinePatchRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0

[node name="CardImage" type="TextureRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
texture = ExtResource("1_placeholder")
expand_mode = 1
stretch_mode = 5

[node name="CardTitle" type="Label" parent="."]
layout_mode = 1
anchors_preset = 2
anchor_top = 1.0
anchor_bottom = 1.0
offset_top = -23.0
offset_right = 150.0
text = "{display_name}"
horizontal_alignment = 1

[node name="AnimationPlayer" type="AnimationPlayer" parent="."]
'''
        
        scene_dir = self.godot_cards_dir.parent / "scenes" / "cards"
        scene_dir.mkdir(parents=True, exist_ok=True)
        
        scene_file = scene_dir / f"{filename}.tscn"
        with open(scene_file, 'w') as f:
            f.write(scene_content)
        
        self.logger.info(f"Created scene: {scene_file}")
    
    def generate_all_missing_cards(self):
        """Generate all missing card assets."""
        self.logger.info("Starting missing card generation...")
        
        generated_count = 0
        
        for card_name in self.missing_cards:
            self.logger.info(f"Processing: {card_name}")
            
            try:
                # Generate the card image
                if AI_AVAILABLE:
                    image_path = self.generate_ai_card(card_name)
                else:
                    image_path = self.create_placeholder_card(card_name)
                
                # Copy to Godot project
                self.copy_to_godot(image_path, card_name)
                
                # Create Godot scene
                self.create_godot_scene(card_name)
                
                generated_count += 1
                self.logger.info(f"✓ Completed: {card_name}")
                
            except Exception as e:
                self.logger.error(f"Failed to process {card_name}: {e}")
        
        self.logger.info(f"Card generation complete: {generated_count}/{len(self.missing_cards)} cards generated")
        
        return generated_count


def main():
    generator = MissingCardGenerator()
    generator.generate_all_missing_cards()


if __name__ == "__main__":
    main()