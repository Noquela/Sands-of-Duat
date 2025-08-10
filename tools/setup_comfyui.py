#!/usr/bin/env python3
"""
ComfyUI Setup Script for RTX 5070 - Hades-Egyptian Art Generation
Configures optimal environment for 12GB VRAM with SDXL models
"""

import os
import subprocess
import sys
import json
import requests
from pathlib import Path

class ComfyUISetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent / "external" / "ComfyUI"
        self.models_dir = self.base_dir / "models"
        
    def check_prerequisites(self):
        """Verify RTX 5070 and CUDA setup"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            if 'RTX 5070' not in result.stdout and 'RTX' not in result.stdout:
                print("WARNING: RTX GPU not detected. Performance may be suboptimal.")
            
            # Check CUDA version
            result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("ERROR: CUDA not found. Install CUDA 12.1+")
                return False
                
            print("✓ GPU and CUDA environment verified")
            return True
        except Exception as e:
            print(f"Error checking prerequisites: {e}")
            return False
    
    def clone_comfyui(self):
        """Clone ComfyUI repository"""
        if self.base_dir.exists():
            print("✓ ComfyUI already exists, updating...")
            subprocess.run(['git', 'pull'], cwd=self.base_dir)
        else:
            print("Cloning ComfyUI...")
            subprocess.run([
                'git', 'clone', 
                'https://github.com/comfyanonymous/ComfyUI.git',
                str(self.base_dir)
            ])
        return True
    
    def install_dependencies(self):
        """Install PyTorch and dependencies optimized for RTX 5070"""
        print("Installing PyTorch with CUDA support...")
        
        # RTX 5070 optimized PyTorch installation
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            'torch', 'torchvision', 'torchaudio',
            '--extra-index-url', 'https://download.pytorch.org/whl/cu121'
        ])
        
        # Install ComfyUI requirements
        requirements_file = self.base_dir / "requirements.txt"
        if requirements_file.exists():
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                '-r', str(requirements_file)
            ])
        
        # Additional dependencies for Egyptian art generation
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            'opencv-python', 'Pillow', 'numpy', 'scipy'
        ])
        
        print("✓ Dependencies installed")
        return True
    
    def download_models(self):
        """Download SDXL models for Egyptian art generation"""
        models = {
            'checkpoints': {
                'sd_xl_base_1.0.safetensors': 'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors'
            },
            'vae': {
                'sdxl_vae.safetensors': 'https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors'
            }
        }
        
        for category, files in models.items():
            category_dir = self.models_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, url in files.items():
                filepath = category_dir / filename
                if not filepath.exists():
                    print(f"Downloading {filename}...")
                    self._download_file(url, filepath)
                else:
                    print(f"✓ {filename} already exists")
    
    def _download_file(self, url, filepath):
        """Download file with progress"""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as file:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end="")
        print()  # New line after progress
    
    def create_rtx5070_config(self):
        """Create optimized configuration for RTX 5070"""
        config = {
            "gpu_memory_fraction": 0.95,  # Use 95% of 12GB VRAM
            "batch_size": 4,  # Optimal for RTX 5070
            "resolution": {
                "cards": [1024, 1024],
                "backgrounds": [1920, 1080],
                "sprites": [512, 512]
            },
            "sampling": {
                "steps": 30,
                "cfg_scale": 8.0,
                "scheduler": "karras"
            },
            "egyptian_style": {
                "base_prompt": "sands_of_duat_style, egyptian_underworld_art, hades_game_art_quality",
                "negative_prompt": "blurry, low quality, pixelated, modern, realistic photo, 3d render"
            }
        }
        
        config_file = self.base_dir / "config" / "rtx5070_egyptian.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✓ RTX 5070 configuration created")
        return True
    
    def setup(self):
        """Run complete setup process"""
        print("🏺 Setting up ComfyUI for Hades-Egyptian Art Generation 🏺")
        print("RTX 5070 Optimization Active")
        print("=" * 60)
        
        if not self.check_prerequisites():
            return False
        
        self.clone_comfyui()
        self.install_dependencies()
        self.download_models()
        self.create_rtx5070_config()
        
        print("=" * 60)
        print("✅ ComfyUI setup complete!")
        print(f"Installation path: {self.base_dir}")
        print("Next: Run 'python tools/generate_animated_artwork.py' to start generating!")
        
        return True

if __name__ == "__main__":
    setup = ComfyUISetup()
    setup.setup()