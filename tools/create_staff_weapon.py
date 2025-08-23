#!/usr/bin/env python3
"""
Create ceremonial staff weapon
"""

import bpy
import os

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_ceremonial_staff():
    print("Creating ceremonial staff...")
    
    # Create main shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=2.0, location=(0, 0, 1.0))
    shaft = bpy.context.active_object
    shaft.name = "Staff_Shaft"
    
    # Create ornate top
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(0, 0, 2.2))
    orb = bpy.context.active_object
    orb.name = "Staff_Orb"
    
    # Create ankh symbol on top
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.02, location=(0, 0, 2.5))
    ankh_top = bpy.context.active_object
    ankh_top.name = "Ankh_Top"
    
    # Create ankh cross
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, 2.35))
    ankh_cross = bpy.context.active_object
    ankh_cross.name = "Ankh_Cross"
    ankh_cross.scale = (0.4, 0.2, 3.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    shaft.select_set(True)
    bpy.context.view_layer.objects.active = shaft
    orb.select_set(True)
    ankh_top.select_set(True)
    ankh_cross.select_set(True)
    bpy.ops.object.join()
    
    staff = bpy.context.active_object
    staff.name = "Ceremonial_Staff"
    
    # Golden material
    mat = bpy.data.materials.new(name="Golden_Staff")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.9, 0.7, 0.1, 1.0)
    bsdf.inputs[6].default_value = 0.8
    bsdf.inputs[7].default_value = 0.1
    
    staff.data.materials.append(mat)
    print("✅ Ceremonial staff created!")
    return staff

def export_model(obj, filepath):
    print(f"Exporting {obj.name}...")
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format='GLB',
    )
    print(f"✅ Exported {os.path.basename(filepath)}!")

def main():
    clear_scene()
    staff = create_ceremonial_staff()
    
    output_dir = "C:/Users/Bruno/Documents/Sand of Duat/assets/models/weapons"
    os.makedirs(output_dir, exist_ok=True)
    export_model(staff, os.path.join(output_dir, "staff.glb"))
    print("✅ Staff weapon complete!")

if __name__ == "__main__":
    main()