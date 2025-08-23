# Sands of Duat - Tools Directory

This directory contains all development tools and scripts for the Sands of Duat Egyptian roguelike game.

## 🎯 MAIN PIPELINE

### `generate_true_3d_pipeline.py` 
**Complete TRUE 3D pipeline script**
- Generates SDXL concept art + textures
- Cleans backgrounds with AI
- Creates 3D models in Blender with rigging
- Exports glTF assets with animations
- Builds and tests the game at 120+ FPS

**Usage:** `python tools/generate_true_3d_pipeline.py`

---

## 🎨 AI ART GENERATION

### `generate_3d_concepts.py`
Generates concept art and textures for 3D modeling (NOT 3D models themselves)
- Character concept sheets (pharaoh, anubis, mummy)
- Weapon designs (khopesh, staff)
- Seamless textures (armor, fur, stone)
- Emissive textures (runes, glowing effects)

### `rtx_asset_generator.py` 
RTX 5070 optimized asset generator using SDXL
- High-quality 1152x1152 sprites
- Egyptian-themed characters and environments
- CUDA 12.8 acceleration

### `generate_hades_egyptian_assets.py`
Specialized generator for Hades-style Egyptian assets
- Professional art style matching Hades game
- Character sprites and environment pieces

---

## 🏗️ 3D MODELING & PROCESSING

### `blender_3d_pipeline.py`
Automated Blender script for TRUE 3D model creation
- Low-poly humanoid modeling
- Armature rigging with bone hierarchy
- Weapon sockets (Socket_Hand_R, Socket_Back)
- Basic animations (idle, walk, attack)
- glTF export with proper materials

**Usage:** `blender --background --python tools/blender_3d_pipeline.py`

### `clean_bg.py`
Background removal pipeline
- Uses rembg U²-Net AI model
- Fallback manual removal for solid backgrounds
- Creates clean PNG assets with alpha transparency

**Usage:** `python tools/clean_bg.py <input_dir> <output_dir> [method]`

---

## 🖼️ IMAGE PROCESSING

### `halo_fix.py`
Fixes color halos around transparent sprites
- Removes green/white edges from background removal
- Cleans up alpha channels for game integration

### `check_transparency.py`
Validates PNG transparency and alpha channels
- Checks if images have proper transparency
- Useful for debugging asset pipeline

### `make_atlas.py`
Creates texture atlases from sprite sequences
- Packs multiple frames into single texture
- Generates JSON layout for Bevy TextureAtlas

---

## 🎮 GAME INTEGRATION

### `pack_assets.py`
Optimizes and packages game assets
- Compresses textures for performance
- Validates asset formats
- Organizes files for Bevy loading

---

## 📦 LEGACY TOOLS

### `ai_asset_generator.py`
Basic AI asset generator (superseded by `generate_3d_concepts.py`)

### `generate_isometric_assets.py`
2D isometric sprite generator (superseded by 3D pipeline)

### `generate_environment_elements.py`
Environment asset generator (now part of 3D pipeline)

### `generate_missing_characters.py`
Character sprite generator (now part of 3D pipeline)

---

## ⚙️ CONFIGURATION

### `requirements.txt`
Python dependencies for the entire pipeline:
- PyTorch CUDA 12.8 for RTX 5070
- Diffusers for SDXL generation
- rembg for background removal
- OpenCV for image processing
- Blender integration libraries

### `generate_ai_assets.bat`
Windows batch file for quick AI generation (legacy)

---

## 🚀 QUICK START

1. **Setup environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r tools/requirements.txt
   ```

2. **Run complete TRUE 3D pipeline:**
   ```bash
   python tools/generate_true_3d_pipeline.py
   ```

3. **Individual tools:**
   ```bash
   # Generate concepts only
   python tools/generate_3d_concepts.py
   
   # Clean backgrounds
   python tools/clean_bg.py art/sdxl/concepts art/sdxl/clean
   
   # Run Blender pipeline
   blender --background --python tools/blender_3d_pipeline.py
   ```

---

## 🎯 WORKFLOW

The complete workflow transforms 2D AI-generated concepts into TRUE 3D game assets:

1. **SDXL Concepts** → Character designs, weapon concepts, textures
2. **Background Cleaning** → Remove backgrounds, add transparency
3. **3D Modeling** → Create low-poly models based on concepts
4. **Rigging & Animation** → Add bones, sockets, and animations
5. **glTF Export** → Export as Bevy-compatible 3D assets
6. **Game Integration** → Load 3D models with proper materials
7. **Performance Testing** → Ensure 120+ FPS at 3440x1440

This creates **real 3D graphics** like Hades, not 2D sprites on planes!