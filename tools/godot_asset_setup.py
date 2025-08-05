#!/usr/bin/env python3
"""
Godot Asset Setup for Sands of Duat
Creates Godot scenes and resource files for all assets.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class GodotAssetSetup:
    """Setup assets directly in Godot project structure."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.godot_project = self.project_root / "godot" / "novo-projeto-de-jogo"
        self.assets_dir = self.project_root / "assets"
        
        # Ensure Godot project directories exist
        self.create_godot_directories()
    
    def create_godot_directories(self):
        """Create necessary directories in Godot project."""
        dirs = [
            "characters",
            "cards", 
            "environments",
            "sprites",
            "animations",
            "scenes/characters",
            "scenes/cards",
            "scenes/environments"
        ]
        
        for dir_name in dirs:
            (self.godot_project / dir_name).mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_name}")
    
    def copy_assets_to_godot(self):
        """Copy assets to Godot project structure."""
        import shutil
        
        # Copy sprites
        sprites_src = self.assets_dir / "sprites"
        sprites_dst = self.godot_project / "sprites"
        
        if sprites_src.exists():
            for file in sprites_src.glob("*.png"):
                shutil.copy2(file, sprites_dst / file.name)
                print(f"Copied sprite: {file.name}")
        
        # Copy card textures
        cards_src = self.assets_dir / "textures" / "cards"
        cards_dst = self.godot_project / "cards"
        
        if cards_src.exists():
            for file in cards_src.glob("*.png"):
                # Skip generic image files, focus on named cards
                if not file.name.startswith("image_"):
                    shutil.copy2(file, cards_dst / file.name)
                    print(f"Copied card: {file.name}")
        
        # Copy character textures
        chars_src = self.assets_dir / "textures" / "characters"
        chars_dst = self.godot_project / "characters"
        
        if chars_src.exists():
            for file in chars_src.glob("*.png"):
                if not file.name.startswith("image_"):
                    shutil.copy2(file, chars_dst / file.name)
                    print(f"Copied character: {file.name}")
        
        # Copy environments
        envs_src = self.assets_dir / "textures" / "environments"
        envs_dst = self.godot_project / "environments"
        
        if envs_src.exists():
            for file in envs_src.glob("*.png"):
                if not file.name.startswith("image_"):
                    shutil.copy2(file, envs_dst / file.name)
                    print(f"Copied environment: {file.name}")
    
    def create_import_files(self):
        """Create .import files for proper texture settings."""
        
        # Character texture import settings
        char_import = '''[remap]

importer="texture"
type="CompressedTexture2D"
uid="uid://generate_unique_id"
path="res://.godot/imported/{filename}-{hash}.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="res://characters/{filename}"
dest_files=["res://.godot/imported/{filename}-{hash}.ctex"]

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
        
        # Card texture import settings
        card_import = '''[remap]

importer="texture"
type="CompressedTexture2D"
uid="uid://generate_unique_id"
path="res://.godot/imported/{filename}-{hash}.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="res://cards/{filename}"
dest_files=["res://.godot/imported/{filename}-{hash}.ctex"]

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
        
        # Create import files for characters
        chars_dir = self.godot_project / "characters"
        if chars_dir.exists():
            for png_file in chars_dir.glob("*.png"):
                import_file = chars_dir / f"{png_file.name}.import"
                import_content = char_import.format(
                    filename=png_file.name,
                    hash="placeholder_hash"
                )
                with open(import_file, 'w') as f:
                    f.write(import_content)
                print(f"Created import for: {png_file.name}")
        
        # Create import files for cards
        cards_dir = self.godot_project / "cards"
        if cards_dir.exists():
            for png_file in cards_dir.glob("*.png"):
                import_file = cards_dir / f"{png_file.name}.import"
                import_content = card_import.format(
                    filename=png_file.name,
                    hash="placeholder_hash"
                )
                with open(import_file, 'w') as f:
                    f.write(import_content)
                print(f"Created card import for: {png_file.name}")
    
    def create_character_scenes(self):
        """Create character scene files with AnimatedSprite2D."""
        
        # Get spritesheet metadata
        sprites_dir = self.assets_dir / "sprites"
        
        character_scene_template = '''[gd_scene load_steps=3 format=3 uid="uid://generate_unique_id"]

[ext_resource type="Texture2D" uid="uid://placeholder" path="res://sprites/{spritesheet_name}" id="1_placeholder"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{{
&"default": {{
"frames": [{{
"duration": 1.0,
"texture": ExtResource("1_placeholder")
}}],
"loop": true,
"name": &"default",
"speed": 5.0
}},
&"idle": {{
"frames": [{{
"duration": 1.0,
"texture": ExtResource("1_placeholder")
}}],
"loop": true,
"name": &"idle",
"speed": {fps}
}}
}}]

[node name="{character_name}" type="CharacterBody2D"]

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
sprite_frames = SubResource("SpriteFrames_1")
animation = &"idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
'''
        
        # Create scenes for each character spritesheet
        if sprites_dir.exists():
            for spritesheet in sprites_dir.glob("*_spritesheet.png"):
                # Parse character name
                name_parts = spritesheet.stem.replace("_spritesheet", "").split("_")
                if len(name_parts) >= 2:
                    character_name = "_".join(name_parts[:-1])
                    animation_name = name_parts[-1]
                else:
                    character_name = name_parts[0]
                    animation_name = "idle"
                
                # Load metadata for FPS
                metadata_file = spritesheet.with_suffix('').with_suffix('.json')
                fps = 12  # default
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                            # Calculate FPS based on frame count (reasonable default)
                            frame_count = metadata.get('frame_count', 16)
                            fps = max(8, min(16, frame_count))
                    except:
                        pass
                
                # Create scene file
                scene_content = character_scene_template.format(
                    character_name=character_name.title().replace("_", ""),
                    spritesheet_name=spritesheet.name,
                    fps=fps
                )
                
                scene_file = self.godot_project / "scenes" / "characters" / f"{character_name}.tscn"
                with open(scene_file, 'w') as f:
                    f.write(scene_content)
                
                print(f"Created character scene: {character_name}.tscn")
    
    def create_card_scenes(self):
        """Create card scene files."""
        
        card_scene_template = '''[gd_scene load_steps=2 format=3 uid="uid://generate_unique_id"]

[ext_resource type="Texture2D" uid="uid://placeholder" path="res://cards/{card_texture}" id="1_placeholder"]

[node name="{card_name}" type="Control"]
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
offset_right = 100.0
text = "{card_display_name}"
horizontal_alignment = 1

[node name="AnimationPlayer" type="AnimationPlayer" parent="."]
'''
        
        # Create scenes for named cards
        cards_dir = self.assets_dir / "textures" / "cards"
        if cards_dir.exists():
            for card_file in cards_dir.glob("*.png"):
                if not card_file.name.startswith("image_"):
                    card_name = card_file.stem
                    display_name = card_name.replace("_", " ").title()
                    
                    scene_content = card_scene_template.format(
                        card_name=card_name.title().replace("_", ""),
                        card_texture=card_file.name,
                        card_display_name=display_name
                    )
                    
                    scene_file = self.godot_project / "scenes" / "cards" / f"{card_name}.tscn"
                    with open(scene_file, 'w') as f:
                        f.write(scene_content)
                    
                    print(f"Created card scene: {card_name}.tscn")
    
    def create_environment_scenes(self):
        """Create environment background scenes."""
        
        env_scene_template = '''[gd_scene load_steps=2 format=3 uid="uid://generate_unique_id"]

[ext_resource type="Texture2D" uid="uid://placeholder" path="res://environments/{env_texture}" id="1_placeholder"]

[node name="{env_name}" type="Node2D"]

[node name="Background" type="Sprite2D" parent="."]
texture = ExtResource("1_placeholder")
centered = false

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="ParallaxLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.5, 0.5)

[node name="BackgroundSprite" type="Sprite2D" parent="ParallaxBackground/ParallaxLayer"]
texture = ExtResource("1_placeholder")
centered = false
'''
        
        # Create scenes for environments
        envs_dir = self.assets_dir / "textures" / "environments"
        if envs_dir.exists():
            for env_file in envs_dir.glob("*.png"):
                if not env_file.name.startswith("image_"):
                    env_name = env_file.stem
                    
                    scene_content = env_scene_template.format(
                        env_name=env_name.title().replace("_", ""),
                        env_texture=env_file.name
                    )
                    
                    scene_file = self.godot_project / "scenes" / "environments" / f"{env_name}.tscn"
                    with open(scene_file, 'w') as f:
                        f.write(scene_content)
                    
                    print(f"Created environment scene: {env_name}.tscn")
    
    def setup_all_assets(self):
        """Setup all assets in Godot project."""
        print("=== GODOT ASSET SETUP ===")
        print()
        
        print("1. Creating directories...")
        self.create_godot_directories()
        print()
        
        print("2. Copying assets...")
        self.copy_assets_to_godot()
        print()
        
        print("3. Creating import files...")
        self.create_import_files()
        print()
        
        print("4. Creating character scenes...")
        self.create_character_scenes()
        print()
        
        print("5. Creating card scenes...")
        self.create_card_scenes()
        print()
        
        print("6. Creating environment scenes...")
        self.create_environment_scenes()
        print()
        
        print("✅ GODOT ASSET SETUP COMPLETE!")
        print()
        print("Next steps:")
        print("1. Open Godot project at: godot/novo-projeto-de-jogo/")
        print("2. Let Godot reimport all assets")
        print("3. Configure sprite animations in AnimatedSprite2D nodes")
        print("4. Test scenes in Godot editor")


def main():
    project_root = Path(__file__).parent.parent
    setup = GodotAssetSetup(project_root)
    setup.setup_all_assets()


if __name__ == "__main__":
    main()