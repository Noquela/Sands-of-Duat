#!/usr/bin/env python3
"""
🏺 HADES-QUALITY 3D PIPELINE
Complete free/open-source pipeline for generating Hades-style 3D assets

Pipeline Flow:
1. Generate concept art with SDXL + LoRAs
2. Create 3D mesh with TripoSR  
3. Process in Blender (retopo, rig, animate)
4. Export optimized .glb for Bevy
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import argparse

class Hades3DPipeline:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.assets_3d = self.project_root / "assets" / "3d"
        self.tools_3d = self.project_root / "tools" / "3d_pipeline"
        
    def setup_environment(self):
        """Setup the complete 3D pipeline environment"""
        print("Setting up Hades-Quality 3D Pipeline...")
        
        # Check if Blender is available
        blender_path = self.find_blender()
        if not blender_path:
            print("Blender not found. Please install Blender 3.6+ first.")
            return False
            
        print(f"Found Blender at: {blender_path}")
        
        # Install Python requirements
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", 
                          self.tools_3d / "requirements_3d.txt"], check=True)
            print("Python dependencies installed")
        except subprocess.CalledProcessError:
            print("Some dependencies failed to install, continuing anyway...")
            
        return True
        
    def find_blender(self):
        """Find Blender installation"""
        possible_paths = [
            "C:/Program Files/Blender Foundation/Blender 4.5/blender.exe",
            "C:/Program Files/Blender Foundation/Blender 4.4/blender.exe", 
            "C:/Program Files/Blender Foundation/Blender 4.3/blender.exe",
            "C:/Program Files/Blender Foundation/Blender 3.6/blender.exe",
            "/usr/bin/blender",
            "/Applications/Blender.app/Contents/MacOS/Blender"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        # Try to find in PATH
        try:
            result = subprocess.run(["where", "blender"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
            
        return None
        
    def generate_concept_art(self, character_name: str, prompt: str):
        """Generate concept art using local SDXL"""
        print(f"Generating concept art for: {character_name}")
        
        concept_script = self.tools_3d / "concept_generator.py"
        if not concept_script.exists():
            self.create_concept_generator()
            
        cmd = [sys.executable, str(concept_script), 
               "--character", character_name,
               "--prompt", prompt,
               "--output", str(self.assets_3d / "concepts")]
               
        try:
            subprocess.run(cmd, check=True)
            print(f"Concept art generated for {character_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate concept art: {e}")
            return False
            
    def create_3d_mesh(self, character_name: str):
        """Create 3D mesh from concept art using TripoSR"""
        print(f"🔺 Creating 3D mesh for: {character_name}")
        
        mesh_script = self.tools_3d / "triposr_generator.py"
        if not mesh_script.exists():
            self.create_triposr_generator()
            
        concept_path = self.assets_3d / "concepts" / f"{character_name}_concept.png"
        if not concept_path.exists():
            print(f"❌ Concept art not found: {concept_path}")
            return False
            
        cmd = [sys.executable, str(mesh_script),
               "--input", str(concept_path),
               "--output", str(self.assets_3d / "raw_meshes" / f"{character_name}.obj")]
               
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ 3D mesh created for {character_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create 3D mesh: {e}")
            return False
            
    def process_in_blender(self, character_name: str):
        """Process mesh in Blender with full pipeline"""
        print(f"🔧 Processing in Blender: {character_name}")
        
        blender_path = self.find_blender()
        if not blender_path:
            return False
            
        blender_script = self.tools_3d / "blender_hades_processor.py"
        if not blender_script.exists():
            self.create_blender_processor()
            
        raw_mesh = self.assets_3d / "raw_meshes" / f"{character_name}.obj"
        output_path = self.assets_3d / "characters" / f"{character_name}.glb"
        
        cmd = [blender_path, "--background", "--python", str(blender_script),
               "--", str(raw_mesh), str(output_path), character_name]
               
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Blender processing completed for {character_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Blender processing failed: {e}")
            return False
            
    def create_full_character(self, character_name: str, prompt: str):
        """Complete pipeline for creating a character"""
        print(f"\n🏺 Creating Hades-quality character: {character_name}")
        print(f"📝 Prompt: {prompt}")
        
        # Ensure output directories exist
        os.makedirs(self.assets_3d / "concepts", exist_ok=True)
        os.makedirs(self.assets_3d / "raw_meshes", exist_ok=True)
        os.makedirs(self.assets_3d / "characters", exist_ok=True)
        
        # Step 1: Generate concept art
        if not self.generate_concept_art(character_name, prompt):
            return False
            
        # Step 2: Create 3D mesh
        if not self.create_3d_mesh(character_name):
            return False
            
        # Step 3: Process in Blender
        if not self.process_in_blender(character_name):
            return False
            
        print(f"🎉 Character '{character_name}' created successfully!")
        return True
        
    def create_concept_generator(self):
        """Create the concept art generator script"""
        # We'll create this in the next step
        pass
        
    def create_triposr_generator(self):
        """Create the TripoSR mesh generator script"""
        # We'll create this in the next step
        pass
        
    def create_blender_processor(self):
        """Create the Blender processing script"""
        # We'll create this in the next step
        pass

def main():
    parser = argparse.ArgumentParser(description="Hades-Quality 3D Asset Pipeline")
    parser.add_argument("--setup", action="store_true", help="Setup the pipeline environment")
    parser.add_argument("--character", help="Character name to create")
    parser.add_argument("--prompt", help="Character description prompt")
    
    args = parser.parse_args()
    
    pipeline = Hades3DPipeline()
    
    if args.setup:
        if pipeline.setup_environment():
            print("🎉 Pipeline setup completed!")
        else:
            print("❌ Pipeline setup failed")
            return 1
            
    if args.character and args.prompt:
        if not pipeline.create_full_character(args.character, args.prompt):
            return 1
            
    return 0

if __name__ == "__main__":
    sys.exit(main())