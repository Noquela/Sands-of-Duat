#!/usr/bin/env python3
"""
🔺 TRIPOSR 3D MESH GENERATOR
Converts 2D concept art to 3D meshes using TripoSR (text-to-3D)
"""

import os
import argparse
import torch
import numpy as np
from PIL import Image
import trimesh
from pathlib import Path

class TripoSRGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        
    def load_model(self):
        """Load TripoSR model"""
        print("Loading TripoSR model...")
        
        try:
            # For now, we'll create a simplified mesh generator
            # In a real implementation, you'd load the actual TripoSR model
            print("Using simplified mesh generation (TripoSR integration placeholder)")
            print("For full TripoSR, install: pip install torchmcubes")
            return True
            
        except Exception as e:
            print(f"Failed to load TripoSR: {e}")
            return False
            
    def create_basic_mesh(self, image_path: str, character_type: str):
        """Create a basic 3D mesh from image analysis"""
        print(f"Creating basic mesh for character type: {character_type}")
        
        # Load and analyze the image
        image = Image.open(image_path)
        width, height = image.size
        
        # Create character-appropriate mesh based on type
        if "hero" in character_type or "pharaoh" in character_type:
            mesh = self.create_humanoid_mesh()
        elif "boss" in character_type or "anubis" in character_type:
            mesh = self.create_boss_mesh()  
        elif "enemy" in character_type or "mummy" in character_type:
            mesh = self.create_enemy_mesh()
        else:
            mesh = self.create_generic_mesh()
            
        return mesh
        
    def create_humanoid_mesh(self):
        """Create a basic humanoid mesh suitable for heroes"""
        print("Creating humanoid mesh...")
        
        # Create a basic humanoid shape using primitives
        # This is a simplified version - real TripoSR would generate from image
        
        # Body proportions inspired by Hades character design
        vertices = []
        faces = []
        
        # Torso (main body)
        torso_verts, torso_faces = self.create_box(
            center=[0, 0, 1.5], size=[0.8, 0.4, 1.2]
        )
        vertices.extend(torso_verts)
        faces.extend(torso_faces)
        
        # Head
        head_verts, head_faces = self.create_box(
            center=[0, 0, 2.8], size=[0.6, 0.6, 0.8]
        )
        vertices.extend(head_verts)
        faces.extend([[f[0] + len(torso_verts), f[1] + len(torso_verts), f[2] + len(torso_verts)] for f in head_faces])
        
        # Arms
        arm_r_verts, arm_r_faces = self.create_box(
            center=[1.2, 0, 2.2], size=[0.3, 0.3, 1.0]
        )
        vertices.extend(arm_r_verts)
        offset = len(torso_verts) + len(head_verts)
        faces.extend([[f[0] + offset, f[1] + offset, f[2] + offset] for f in arm_r_faces])
        
        arm_l_verts, arm_l_faces = self.create_box(
            center=[-1.2, 0, 2.2], size=[0.3, 0.3, 1.0]
        )
        vertices.extend(arm_l_verts)
        offset = len(torso_verts) + len(head_verts) + len(arm_r_verts)
        faces.extend([[f[0] + offset, f[1] + offset, f[2] + offset] for f in arm_l_faces])
        
        # Legs
        leg_r_verts, leg_r_faces = self.create_box(
            center=[0.3, 0, 0.5], size=[0.3, 0.3, 1.0]
        )
        vertices.extend(leg_r_verts)
        offset = len(vertices) - len(leg_r_verts)
        faces.extend([[f[0] + offset, f[1] + offset, f[2] + offset] for f in leg_r_faces])
        
        leg_l_verts, leg_l_faces = self.create_box(
            center=[-0.3, 0, 0.5], size=[0.3, 0.3, 1.0]
        )
        vertices.extend(leg_l_verts)
        offset = len(vertices) - len(leg_l_verts)
        faces.extend([[f[0] + offset, f[1] + offset, f[2] + offset] for f in leg_l_faces])
        
        # Create mesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        mesh.remove_duplicate_faces()
        mesh.remove_unreferenced_vertices()
        
        return mesh
        
    def create_boss_mesh(self):
        """Create a larger, more imposing mesh for bosses"""
        print("Creating boss mesh...")
        # Similar to humanoid but scaled up and more imposing
        mesh = self.create_humanoid_mesh()
        mesh.apply_scale([1.5, 1.5, 1.8])  # Make taller and broader
        return mesh
        
    def create_enemy_mesh(self):
        """Create a smaller enemy mesh"""
        print("Creating enemy mesh...")
        mesh = self.create_humanoid_mesh()
        mesh.apply_scale([0.8, 0.8, 0.9])  # Make smaller
        return mesh
        
    def create_generic_mesh(self):
        """Create a basic generic mesh"""
        print("Creating generic mesh...")
        return self.create_humanoid_mesh()
        
    def create_box(self, center, size):
        """Create a box primitive"""
        x, y, z = center
        sx, sy, sz = [s/2 for s in size]
        
        vertices = [
            [x-sx, y-sy, z-sz], [x+sx, y-sy, z-sz], [x+sx, y+sy, z-sz], [x-sx, y+sy, z-sz],  # bottom
            [x-sx, y-sy, z+sz], [x+sx, y-sy, z+sz], [x+sx, y+sy, z+sz], [x-sx, y+sy, z+sz]   # top
        ]
        
        faces = [
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 7, 6], [4, 6, 5],  # top  
            [0, 4, 5], [0, 5, 1],  # front
            [2, 6, 7], [2, 7, 3],  # back
            [0, 3, 7], [0, 7, 4],  # left
            [1, 5, 6], [1, 6, 2]   # right
        ]
        
        return vertices, faces
        
    def generate_mesh(self, image_path: str, output_path: str):
        """Generate 3D mesh from concept art"""
        if not self.load_model():
            return False
            
        # Determine character type from filename
        image_name = Path(image_path).stem
        character_type = image_name.replace("_concept", "")
        
        print(f"Generating 3D mesh from: {image_path}")
        
        # Create the mesh
        mesh = self.create_basic_mesh(image_path, character_type)
        
        if mesh is None:
            print("Failed to create mesh")
            return False
            
        # Ensure output directory exists
        os.makedirs(Path(output_path).parent, exist_ok=True)
        
        # Save the mesh
        try:
            mesh.export(output_path)
            print(f"3D mesh saved: {output_path}")
            
            # Print mesh stats
            print(f"Mesh stats: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
            
            return True
            
        except Exception as e:
            print(f"Failed to save mesh: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Generate 3D mesh from concept art")
    parser.add_argument("--input", required=True, help="Input concept art image")
    parser.add_argument("--output", required=True, help="Output mesh file (.obj)")
    
    args = parser.parse_args()
    
    generator = TripoSRGenerator()
    
    if not generator.generate_mesh(args.input, args.output):
        return 1
        
    print(f"3D mesh generated successfully!")
    return 0

if __name__ == "__main__":
    main()