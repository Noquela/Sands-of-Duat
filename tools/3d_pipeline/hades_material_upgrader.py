#!/usr/bin/env python3
"""
Upgrade existing 3D models with Hades-quality materials and lighting
"""

import bpy
import sys
import os
from mathutils import Vector
import json

# Get arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]

input_file = argv[0]
output_file = argv[1] 
character_name = argv[2]

print(f"Upgrading to Hades quality: {character_name}")
print(f"Input: {input_file}")
print(f"Output: {output_file}")

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import GLB
try:
    bpy.ops.import_scene.gltf(filepath=input_file)
    print("Successfully imported GLB model")
except:
    print("GLB import failed, trying OBJ...")
    try:
        bpy.ops.import_scene.obj(filepath=input_file)
        print("Successfully imported OBJ model")
    except Exception as e:
        print(f"Both imports failed: {e}")
        sys.exit(1)

# Get the mesh object
mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not mesh_objects:
    print("No mesh objects found!")
    sys.exit(1)

obj = mesh_objects[0]
bpy.context.view_layer.objects.active = obj

# Create Hades-quality material
mat = bpy.data.materials.new(name=f"{character_name}_Hades")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear existing nodes
for node in nodes:
    nodes.remove(node)

# Create nodes
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
output = nodes.new('ShaderNodeOutputMaterial') 

# Position nodes
bsdf.location = (0, 0)
output.location = (400, 0)

# Link nodes
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Character-specific materials
if "pharaoh" in character_name.lower():
    bsdf.inputs['Base Color'].default_value = (0.831, 0.686, 0.216, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.7
    bsdf.inputs['Roughness'].default_value = 0.3
elif "anubis" in character_name.lower():
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.2, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.4
    # Add emission for glowing effect
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = (0.0, 0.5, 0.1, 1.0)
        bsdf.inputs['Emission Strength'].default_value = 0.3
elif "mummy" in character_name.lower():
    bsdf.inputs['Base Color'].default_value = (0.6, 0.5, 0.3, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.8
elif "isis" in character_name.lower():
    bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.2
    bsdf.inputs['Roughness'].default_value = 0.4

# Apply material
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# Setup dramatic lighting
# Remove existing lights
for light_obj in [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']:
    bpy.data.objects.remove(light_obj)

# Key light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
key_light = bpy.context.active_object
key_light.data.energy = 5.0
key_light.data.color = (1.0, 0.9, 0.7)

# Rim light
bpy.ops.object.light_add(type='AREA', location=(-5, -3, 8))
rim_light = bpy.context.active_object
rim_light.data.energy = 8.0
rim_light.data.color = (0.7, 0.8, 1.0)
rim_light.data.size = 5.0

# Export as GLB
os.makedirs(os.path.dirname(output_file), exist_ok=True)

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

bpy.ops.export_scene.gltf(
    filepath=output_file,
    export_format='GLB'
)

print(f"Successfully upgraded to: {output_file}")