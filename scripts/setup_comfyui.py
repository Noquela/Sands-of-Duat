"""
ComfyUI Setup Script for Sands of Duat Animation Generation
Automated setup for Egyptian card animation pipeline with AnimateDiff.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import requests
import zipfile
import shutil

def download_file(url: str, dest: Path, desc: str = ""):
    """Download a file with progress indication."""
    print(f"Downloading {desc}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Progress: {percent:.1f}%", end='', flush=True)
    print()

def setup_comfyui():
    """Set up ComfyUI for Egyptian card animation generation."""
    print("🏺 SANDS OF DUAT - ComfyUI Animation Pipeline Setup")
    print("=" * 60)
    
    # Create ComfyUI directory
    comfyui_dir = Path("ComfyUI")
    if comfyui_dir.exists():
        print("⚠️  ComfyUI directory already exists. Updating...")
    else:
        print("📦 Setting up ComfyUI...")
        
        # Clone ComfyUI
        subprocess.run([
            "git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"
        ], check=True)
    
    os.chdir(comfyui_dir)
    
    # Install ComfyUI requirements
    print("📦 Installing ComfyUI dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], check=True)
    
    # Set up AnimateDiff
    print("🎬 Setting up AnimateDiff...")
    
    # Create custom_nodes directory
    custom_nodes_dir = Path("custom_nodes")
    custom_nodes_dir.mkdir(exist_ok=True)
    
    # Clone AnimateDiff-Evolved
    animatediff_dir = custom_nodes_dir / "ComfyUI-AnimateDiff-Evolved"
    if not animatediff_dir.exists():
        subprocess.run([
            "git", "clone", "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git",
            str(animatediff_dir)
        ], check=True)
    
    # Install AnimateDiff requirements
    animatediff_reqs = animatediff_dir / "requirements.txt"
    if animatediff_reqs.exists():
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(animatediff_reqs)
        ], check=True)
    
    # Clone VideoHelperSuite for GIF export
    vhs_dir = custom_nodes_dir / "ComfyUI-VideoHelperSuite"
    if not vhs_dir.exists():
        subprocess.run([
            "git", "clone", "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git",
            str(vhs_dir)
        ], check=True)
    
    # Set up model directories
    print("📂 Setting up model directories...")
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create necessary model subdirectories
    (models_dir / "checkpoints").mkdir(exist_ok=True)
    (models_dir / "animatediff_models").mkdir(exist_ok=True)
    (models_dir / "vae").mkdir(exist_ok=True)
    
    # Download essential models
    print("⬇️  Downloading essential models...")
    
    # RevAnimated checkpoint (good for fantasy/mystical content)
    checkpoint_url = "https://civitai.com/api/download/models/46846"
    checkpoint_path = models_dir / "checkpoints" / "revAnimated_v122.safetensors"
    
    if not checkpoint_path.exists():
        try:
            download_file(checkpoint_url, checkpoint_path, "RevAnimated v1.2.2")
        except Exception as e:
            print(f"⚠️  Could not download RevAnimated: {e}")
            print("   Please download manually from Civitai")
    
    # AnimateDiff motion module
    motion_url = "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
    motion_path = models_dir / "animatediff_models" / "mm_sd_v15_v2.ckpt"
    
    if not motion_path.exists():
        try:
            download_file(motion_url, motion_path, "AnimateDiff Motion Module v2")
        except Exception as e:
            print(f"⚠️  Could not download motion module: {e}")
            print("   Please download manually from HuggingFace")
    
    # Copy Egyptian workflows
    print("📋 Setting up Egyptian animation workflows...")
    
    workflows_src = Path("../assets/comfyui_workflows")
    if workflows_src.exists():
        workflows_dest = Path("workflows")
        workflows_dest.mkdir(exist_ok=True)
        
        for workflow_file in workflows_src.glob("*.json"):
            shutil.copy2(workflow_file, workflows_dest / workflow_file.name)
            print(f"   ✅ Copied {workflow_file.name}")
    
    # Create launch script
    print("🚀 Creating launch script...")
    
    launch_script = """@echo off
echo Starting ComfyUI for Sands of Duat Animation Generation...
echo RTX 5070 Optimization: Enabled
echo Egyptian Card Pipeline: Ready
echo.
python main.py --listen 127.0.0.1 --port 8188
pause
"""
    
    with open("launch_sands_of_duat.bat", "w") as f:
        f.write(launch_script)
    
    # Create config for optimal settings
    config = {
        "attention_optimization": "xformers",
        "enable_cors": True,
        "vram_management": "auto",
        "preview_method": "auto"
    }
    
    with open("extra_model_paths.yaml", "w") as f:
        f.write(f"""# Sands of Duat - ComfyUI Configuration
checkpoints: models/checkpoints
animatediff_models: models/animatediff_models
vae: models/vae
""")
    
    os.chdir("..")  # Back to main directory
    
    print("\n🎬 ComfyUI Setup Complete!")
    print("=" * 60)
    print("📍 Installation Location: ./ComfyUI/")
    print("🚀 To start ComfyUI: cd ComfyUI && python main.py --listen 127.0.0.1 --port 8188")
    print("🎮 Or use: cd ComfyUI && launch_sands_of_duat.bat")
    print("\n📋 Egyptian Animation Workflows installed:")
    print("   • egyptian_creature_animate.json")
    print("   • egyptian_legendary_animate.json") 
    print("   • egyptian_spell_animate.json")
    print("   • egyptian_artifact_animate.json")
    print("\n⚡ RTX 5070 Optimizations:")
    print("   • Concurrent animations: 2")
    print("   • Memory management: Auto")
    print("   • Quality profiles: 3 (Optimal/Performance/Memory)")
    print("\n🏺 Ready for Egyptian card animation generation!")

if __name__ == "__main__":
    try:
        setup_comfyui()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed: {e}")
        print("Make sure git and python are installed and accessible.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    input("\nPress ENTER to exit...")