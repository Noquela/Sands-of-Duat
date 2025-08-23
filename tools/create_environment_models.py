#!/usr/bin/env python3
"""
Create basic environment 3D models for Sands of Duat
"""

import bpy
import os

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_stone_pillar():
    """Create Egyptian stone pillar"""
    print("Creating stone pillar...")
    
    # Create base cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=3.0, location=(0, 0, 1.5))
    pillar = bpy.context.active_object
    pillar.name = "Stone_Pillar"
    
    # Create capital (top decoration)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3.2))
    capital = bpy.context.active_object
    capital.name = "Pillar_Capital"
    capital.scale = (0.6, 0.6, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    pillar.select_set(True)
    bpy.context.view_layer.objects.active = pillar
    capital.select_set(True)
    bpy.ops.object.join()
    
    # Material
    mat = bpy.data.materials.new(name="Sandstone")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.6, 0.5, 0.3, 1.0)
    bsdf.inputs[7].default_value = 0.8
    
    pillar.data.materials.append(mat)
    print("✅ Stone pillar created!")
    return pillar

def create_torch_brazier():
    """Create Egyptian torch brazier"""
    print("Creating torch brazier...")
    
    # Create base stand
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.5, location=(0, 0, 0.75))
    stand = bpy.context.active_object
    stand.name = "Brazier_Stand"
    
    # Create bowl
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0, 1.8))
    bowl = bpy.context.active_object
    bowl.name = "Brazier_Bowl"
    bowl.scale = (1.0, 1.0, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create flame (simple)
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, radius2=0.05, depth=0.5, location=(0, 0, 2.3))
    flame = bpy.context.active_object
    flame.name = "Flame"
    
    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    stand.select_set(True)
    bpy.context.view_layer.objects.active = stand
    bowl.select_set(True)
    flame.select_set(True)
    bpy.ops.object.join()
    
    # Material
    mat = bpy.data.materials.new(name="Bronze_Brazier")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.7, 0.5, 0.2, 1.0)
    bsdf.inputs[6].default_value = 0.6
    bsdf.inputs[7].default_value = 0.3
    
    stand.data.materials.append(mat)
    print("✅ Torch brazier created!")
    return stand

def create_anubis_statue():
    """Create Anubis guardian statue"""
    print("Creating Anubis statue...")
    
    # Create base pedestal
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
    pedestal = bpy.context.active_object
    pedestal.name = "Statue_Pedestal"
    pedestal.scale = (1.2, 0.8, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create Anubis body (simplified)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.8))
    body = bpy.context.active_object
    body.name = "Anubis_Statue_Body"
    body.scale = (0.8, 0.4, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create jackal head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.8))
    head = bpy.context.active_object
    head.name = "Anubis_Statue_Head"
    head.scale = (0.5, 0.7, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    pedestal.select_set(True)
    bpy.context.view_layer.objects.active = pedestal
    body.select_set(True)
    head.select_set(True)
    bpy.ops.object.join()
    
    # Material
    mat = bpy.data.materials.new(name="Stone_Statue")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.3, 0.3, 0.3, 1.0)
    bsdf.inputs[7].default_value = 0.6
    
    pedestal.data.materials.append(mat)
    print("✅ Anubis statue created!")
    return pedestal

def export_model(obj, filepath):
    """Export model as glTF"""
    print(f"Exporting {obj.name}...")
    
    # Select only the object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    
    # Export
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format='GLB',
    )
    print(f"✅ Exported {os.path.basename(filepath)}!")

def main():
    print("Creating environment models...")
    
    # Create output directory
    output_dir = "C:/Users/Bruno/Documents/Sand of Duat/assets/models/environment"
    os.makedirs(output_dir, exist_ok=True)
    
    # Stone pillar
    clear_scene()
    pillar = create_stone_pillar()
    export_model(pillar, os.path.join(output_dir, "stone_pillar.glb"))
    
    # Torch brazier
    clear_scene()
    brazier = create_torch_brazier()
    export_model(brazier, os.path.join(output_dir, "torch_brazier.glb"))
    
    # Anubis statue
    clear_scene()
    statue = create_anubis_statue()
    export_model(statue, os.path.join(output_dir, "anubis_statue.glb"))
    
    print("\n✅ All environment models created!")

if __name__ == "__main__":
    main()