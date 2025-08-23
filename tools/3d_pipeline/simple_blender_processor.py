#!/usr/bin/env python3
"""
Simple Blender processor without Unicode issues
Creates basic Hades-style 3D character from OBJ
"""

import bpy
import os
import sys

def clear_scene():
    """Clear all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def import_mesh(mesh_path):
    """Import OBJ mesh"""
    print(f"Importing: {mesh_path}")
    
    try:
        bpy.ops.wm.obj_import(filepath=mesh_path)
    except:
        try:
            bpy.ops.import_scene.obj(filepath=mesh_path)
        except:
            print("Failed to import OBJ file")
            return None
    
    imported_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None
    if imported_obj:
        print(f"Success: {imported_obj.name}")
        return imported_obj
    return None

def create_simple_material(obj):
    """Create simple material"""
    print("Creating material...")
    
    mat = bpy.data.materials.new(name="HadesMaterial")
    mat.use_nodes = True
    
    # Set golden color for pharaoh
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.8, 0.6, 0.2, 1.0)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.3
    mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.5
    
    # Assign to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    print("Material created")

def export_glb(obj, output_path):
    """Export as GLB"""
    print(f"Exporting to: {output_path}")
    
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT'
    )
    
    print("Export complete")

def main():
    if len(sys.argv) < 4:
        print("Usage: blender --background --python simple_blender_processor.py -- input.obj output.glb character_name")
        return
    
    input_mesh = sys.argv[-3]
    output_path = sys.argv[-2] 
    character_name = sys.argv[-1]
    
    print(f"Processing: {character_name}")
    print(f"Input: {input_mesh}")
    print(f"Output: {output_path}")
    
    try:
        clear_scene()
        obj = import_mesh(input_mesh)
        
        if not obj:
            print("Import failed")
            return
            
        create_simple_material(obj)
        export_glb(obj, output_path)
        
        print(f"Success! {character_name} processed")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()