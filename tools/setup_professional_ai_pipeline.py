#!/usr/bin/env python3
"""
Professional AI Art Pipeline Setup for RTX 5070
Sets up ComfyUI, SDXL, ControlNet, and advanced 3D AI tools
Optimized for game asset generation with Hades-quality output
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class ProfessionalAISetup:
    def __init__(self):
        self.base_dir = Path("tools/ai_pipeline")
        self.comfyui_dir = self.base_dir / "ComfyUI"
        self.models_dir = self.base_dir / "models"
        
    def setup_environment(self):
        """Create the professional AI environment structure"""
        print("Setting up Professional AI Art Pipeline...")
        
        # Create directory structure
        directories = [
            self.base_dir,
            self.comfyui_dir,
            self.models_dir / "checkpoints",
            self.models_dir / "loras",
            self.models_dir / "controlnet",
            self.models_dir / "vae",
            self.models_dir / "upscale_models",
            self.base_dir / "workflows",
            self.base_dir / "outputs" / "characters",
            self.base_dir / "outputs" / "environments",
            self.base_dir / "outputs" / "textures",
            self.base_dir / "outputs" / "ui_elements"
        ]
        
        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {dir_path}")
    
    def install_comfyui(self):
        """Install ComfyUI with RTX 5070 optimizations"""
        print("\nInstalling ComfyUI...")
        
        if not self.comfyui_dir.exists():
            # Clone ComfyUI
            subprocess.run([
                "git", "clone", "https://github.com/comfyanonymous/ComfyUI.git",
                str(self.comfyui_dir)
            ], check=True)
        
        # Install dependencies with CUDA support
        requirements = [
            "torch==2.1.0+cu121",
            "torchvision==0.16.0+cu121", 
            "torchaudio==2.1.0+cu121",
            "xformers==0.0.22.post7",
            "--extra-index-url https://download.pytorch.org/whl/cu121",
            "opencv-python",
            "Pillow>=9.5.0",
            "numpy",
            "safetensors>=0.3.2",
            "aiohttp",
            "pyyaml",
            "Pillow",
            "scipy",
            "tqdm",
            "psutil"
        ]
        
        for req in requirements:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", req], check=True)
                print(f"  Installed: {req}")
            except subprocess.CalledProcessError:
                print(f"  Failed to install: {req}")
    
    def create_model_download_script(self):
        """Create script to download essential models for game art"""
        script_content = '''#!/usr/bin/env python3
"""
Download essential models for Hades-quality game art generation
Optimized for RTX 5070 (12GB VRAM)
"""

import requests
import os
from pathlib import Path
from tqdm import tqdm

def download_file(url, filename):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename.name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            progress_bar.update(size)

def main():
    models_dir = Path("tools/ai_pipeline/models")
    
    # Essential models for game art generation
    models = {
        # SDXL Base Model (High quality)
        "checkpoints/sd_xl_base_1.0.safetensors": 
            "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
        
        # SDXL Refiner (For ultra-high quality)
        "checkpoints/sd_xl_refiner_1.0.safetensors":
            "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
        
        # VAE for SDXL
        "vae/sdxl_vae.safetensors":
            "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors",
        
        # ControlNet for precise poses
        "controlnet/controlnet-openpose-sdxl-1.0.safetensors":
            "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_canny_full.safetensors",
        
        # Upscaling model
        "upscale_models/RealESRGAN_x4plus.pth":
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    }
    
    print("Downloading professional AI models for RTX 5070...")
    
    for relative_path, url in models.items():
        full_path = models_dir / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not full_path.exists():
            print(f"\\nDownloading {relative_path}...")
            try:
                download_file(url, full_path)
                print(f"  Downloaded: {relative_path}")
            except Exception as e:
                print(f"  Failed to download {relative_path}: {e}")
        else:
            print(f"  Already exists: {relative_path}")
    
    print("\\nModel download complete!")

if __name__ == "__main__":
    main()
'''
        
        script_path = self.base_dir / "download_models.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"  Created model download script: {script_path}")
    
    def create_hades_workflow(self):
        """Create ComfyUI workflow optimized for Hades-style art"""
        workflow = {
            "workflow_name": "Hades_Style_Egyptian_Character_Generation",
            "description": "Professional workflow for generating Hades-quality Egyptian characters",
            "nodes": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {
                        "ckpt_name": "sd_xl_base_1.0.safetensors"
                    }
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "masterpiece, best quality, highly detailed, Hades game art style, Egyptian mythology character, dramatic lighting, hand-painted texture, stylized proportions, rich colors, ornate details",
                        "clip": ["1", 1]
                    }
                },
                "3": {
                    "class_type": "CLIPTextEncode", 
                    "inputs": {
                        "text": "low quality, blurry, pixelated, amateur, simple, flat lighting, plain background, modern clothing",
                        "clip": ["1", 1]
                    }
                },
                "4": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {
                        "width": 1024,
                        "height": 1024,
                        "batch_size": 1
                    }
                },
                "5": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": 42,
                        "steps": 30,
                        "cfg": 8.0,
                        "sampler_name": "euler",
                        "scheduler": "karras",
                        "denoise": 1.0,
                        "model": ["1", 0],
                        "positive": ["2", 0],
                        "negative": ["3", 0],
                        "latent_image": ["4", 0]
                    }
                },
                "6": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["5", 0],
                        "vae": ["1", 2]
                    }
                },
                "7": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "images": ["6", 0],
                        "filename_prefix": "hades_egyptian_character"
                    }
                }
            }
        }
        
        workflow_path = self.base_dir / "workflows" / "hades_character_generation.json"
        with open(workflow_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"  Created Hades workflow: {workflow_path}")
    
    def create_batch_generator(self):
        """Create batch generation script for consistent art production"""
        script_content = '''#!/usr/bin/env python3
"""
Batch Generation Script for Hades-Quality Egyptian Characters
Uses ComfyUI API for automated, consistent art production
"""

import requests
import json
import time
import uuid
from pathlib import Path

class HadesArtBatchGenerator:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"
        self.output_dir = Path("tools/ai_pipeline/outputs/characters")
        
    def generate_character_variations(self, character_name, base_prompt, count=4):
        """Generate multiple variations of a character"""
        print(f"Generating {count} variations for {character_name}...")
        
        # Character-specific prompt additions
        character_prompts = {
            "pharaoh_hero": "pharaoh warrior, golden armor, khopesh sword, royal headdress, confident pose",
            "anubis_boss": "Anubis jackal god, powerful muscular build, ornate armor, intimidating pose, glowing eyes",
            "mummy_enemy": "ancient mummy warrior, wrapped bandages, glowing green eyes, desert tomb guardian",
            "isis_npc": "Isis goddess, elegant flowing robes, golden jewelry, graceful pose, divine aura"
        }
        
        specific_prompt = character_prompts.get(character_name, "Egyptian mythology character")
        full_prompt = f"{base_prompt}, {specific_prompt}"
        
        variations = []
        for i in range(count):
            # Add variation elements
            seed = hash(f"{character_name}_{i}") % 1000000
            variation_prompt = f"{full_prompt}, variation {i+1}, seed {seed}"
            
            result = self.generate_single_image(variation_prompt, seed)
            if result:
                variations.append(result)
                print(f"  Generated variation {i+1}")
            else:
                print(f"  Failed variation {i+1}")
        
        return variations
    
    def generate_single_image(self, prompt, seed):
        """Generate a single image using ComfyUI API"""
        # Load workflow template
        workflow_path = Path("tools/ai_pipeline/workflows/hades_character_generation.json")
        with open(workflow_path) as f:
            workflow = json.load(f)
        
        # Update workflow with prompt and seed
        workflow["nodes"]["2"]["inputs"]["text"] = prompt
        workflow["nodes"]["5"]["inputs"]["seed"] = seed
        
        # Send generation request
        try:
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Connection Error: {e}")
            return None

def main():
    generator = HadesArtBatchGenerator()
    
    # Base prompt for Hades-style quality
    base_prompt = """masterpiece, best quality, highly detailed, professional game art, 
                     Hades game art style, dramatic cinematic lighting, hand-painted texture, 
                     stylized proportions, rich saturated colors, ornate Egyptian details, 
                     dynamic pose, character portrait, 4K resolution"""
    
    characters = ["pharaoh_hero", "anubis_boss", "mummy_enemy", "isis_npc"]
    
    for character in characters:
        variations = generator.generate_character_variations(character, base_prompt)
        print(f"Generated {len(variations)} variations for {character}")

if __name__ == "__main__":
    main()
'''
        
        script_path = self.base_dir / "batch_generator.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"  Created batch generator: {script_path}")
    
    def create_pbr_material_generator(self):
        """Create PBR material generation system"""
        script_content = '''#!/usr/bin/env python3
"""
PBR Material Generation for Hades-Quality 3D Assets
Generates Albedo, Normal, Roughness, Metallic, and AO maps
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path

class PBRMaterialGenerator:
    def __init__(self):
        self.input_dir = Path("tools/ai_pipeline/outputs/characters")
        self.output_dir = Path("assets/3d/textures/pbr")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_pbr_set(self, albedo_path, character_name):
        """Generate complete PBR material set from albedo map"""
        print(f"Generating PBR materials for {character_name}...")
        
        # Load albedo image
        albedo = Image.open(albedo_path)
        albedo_cv = cv2.cvtColor(np.array(albedo), cv2.COLOR_RGB2BGR)
        
        # Generate Normal Map
        normal_map = self.generate_normal_map(albedo_cv)
        normal_path = self.output_dir / f"{character_name}_normal.png"
        cv2.imwrite(str(normal_path), normal_map)
        
        # Generate Roughness Map
        roughness_map = self.generate_roughness_map(albedo_cv)
        roughness_path = self.output_dir / f"{character_name}_roughness.png"
        cv2.imwrite(str(roughness_path), roughness_map)
        
        # Generate Metallic Map
        metallic_map = self.generate_metallic_map(albedo_cv)
        metallic_path = self.output_dir / f"{character_name}_metallic.png"
        cv2.imwrite(str(metallic_path), metallic_map)
        
        # Generate AO Map
        ao_map = self.generate_ao_map(albedo_cv)
        ao_path = self.output_dir / f"{character_name}_ao.png"
        cv2.imwrite(str(ao_path), ao_map)
        
        # Save enhanced albedo
        enhanced_albedo = self.enhance_albedo(albedo)
        albedo_path = self.output_dir / f"{character_name}_albedo.png"
        enhanced_albedo.save(albedo_path)
        
        print(f"  Generated complete PBR set for {character_name}")
        return {
            "albedo": albedo_path,
            "normal": normal_path,
            "roughness": roughness_path,
            "metallic": metallic_path,
            "ao": ao_path
        }
    
    def generate_normal_map(self, image):
        """Generate normal map from albedo"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Calculate gradients
        grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        
        # Normalize and convert to normal map
        normal = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        normal[:, :, 0] = np.clip(127 + grad_x * 0.5, 0, 255)  # Red = X
        normal[:, :, 1] = np.clip(127 - grad_y * 0.5, 0, 255)  # Green = Y
        normal[:, :, 2] = 255  # Blue = Z (up)
        
        return normal
    
    def generate_roughness_map(self, image):
        """Generate roughness map"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use variance to determine roughness
        kernel = np.ones((5, 5), np.float32) / 25
        smooth = cv2.filter2D(gray, -1, kernel)
        roughness = np.abs(gray.astype(np.float32) - smooth.astype(np.float32))
        
        # Normalize and enhance
        roughness = np.clip(roughness * 3 + 100, 0, 255).astype(np.uint8)
        
        return cv2.cvtColor(roughness, cv2.COLOR_GRAY2BGR)
    
    def generate_metallic_map(self, image):
        """Generate metallic map based on color analysis"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detect metallic areas (high saturation + specific hue ranges)
        metallic = np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Gold/brass detection
        gold_mask = cv2.inRange(hsv, (15, 100, 100), (35, 255, 255))
        metallic = cv2.bitwise_or(metallic, gold_mask)
        
        # Silver detection  
        silver_mask = cv2.inRange(hsv, (0, 0, 180), (255, 30, 255))
        metallic = cv2.bitwise_or(metallic, silver_mask)
        
        return cv2.cvtColor(metallic, cv2.COLOR_GRAY2BGR)
    
    def generate_ao_map(self, image):
        """Generate ambient occlusion map"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create AO effect using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        ao = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        # Enhance contrast
        ao = cv2.equalizeHist(ao)
        
        return cv2.cvtColor(ao, cv2.COLOR_GRAY2BGR)
    
    def enhance_albedo(self, image):
        """Enhance albedo for game use"""
        # Increase saturation
        enhancer = ImageEnhance.Color(image)
        enhanced = enhancer.enhance(1.2)
        
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        return enhanced

def main():
    generator = PBRMaterialGenerator()
    
    # Process all character concept images
    input_dir = Path("assets/3d/concepts")
    for concept_file in input_dir.glob("*.png"):
        if concept_file.is_file():
            character_name = concept_file.stem.replace("_concept", "")
            pbr_set = generator.generate_pbr_set(concept_file, character_name)
            print(f"PBR materials generated for {character_name}")

if __name__ == "__main__":
    main()
'''
        
        script_path = self.base_dir / "pbr_material_generator.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"  Created PBR material generator: {script_path}")

def main():
    setup = ProfessionalAISetup()
    
    print("Setting up Professional AI Art Pipeline for RTX 5070...")
    
    setup.setup_environment()
    setup.install_comfyui()
    setup.create_model_download_script()
    setup.create_hades_workflow()
    setup.create_batch_generator()
    setup.create_pbr_material_generator()
    
    print("\nProfessional AI Art Pipeline setup complete!")
    print("\nNext steps:")
    print("1. Run: python tools/ai_pipeline/download_models.py")
    print("2. Start ComfyUI: cd tools/ai_pipeline/ComfyUI && python main.py")
    print("3. Run batch generator: python tools/ai_pipeline/batch_generator.py")
    print("4. Generate PBR materials: python tools/ai_pipeline/pbr_material_generator.py")

if __name__ == "__main__":
    main()