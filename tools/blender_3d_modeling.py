#!/usr/bin/env python3
"""
Sands of Duat - Blender 3D Model Creator
Automated Blender script to create 3D models from SDXL concept art
"""

import bpy
import bmesh
import os
import sys
from mathutils import Vector, Euler
import math

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Clear meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

def create_hero_pharaoh():
    """Create 3D pharaoh hero model based on SDXL concept"""
    print("Creating 3D Pharaoh Hero...")
    
    # Create base humanoid body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    body = bpy.context.active_object
    body.name = "Hero_Body"
    
    # Scale body to humanoid proportions
    body.scale = (0.8, 0.4, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 0, 2.4))
    head = bpy.context.active_object
    head.name = "Hero_Head"
    
    # Create pharaoh headdress (nemes)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.1, 2.6))
    headdress = bpy.context.active_object
    headdress.name = "Hero_Headdress"
    headdress.scale = (1.2, 0.8, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create arms
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.2, location=(0.9, 0, 1.5))
    arm_r = bpy.context.active_object
    arm_r.name = "Hero_Arm_R"
    arm_r.rotation_euler = (0, 0, math.radians(90))
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.2, location=(-0.9, 0, 1.5))
    arm_l = bpy.context.active_object
    arm_l.name = "Hero_Arm_L"
    arm_l.rotation_euler = (0, 0, math.radians(90))
    
    # Create legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.0, location=(0.3, 0, 0.0))
    leg_r = bpy.context.active_object
    leg_r.name = "Hero_Leg_R"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.0, location=(-0.3, 0, 0.0))
    leg_l = bpy.context.active_object
    leg_l.name = "Hero_Leg_L"
    
    # Select all hero parts and join them
    hero_parts = [body, head, headdress, arm_r, arm_l, leg_r, leg_l]
    
    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select body first (will be the active object)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    
    # Select other parts
    for part in hero_parts[1:]:
        part.select_set(True)
    
    # Join all parts
    bpy.ops.object.join()
    
    hero = bpy.context.active_object
    hero.name = "Hero_Pharaoh"
    
    # Create golden pharaoh material
    mat = bpy.data.materials.new(name="Pharaoh_Gold")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.8, 0.6, 0.2, 1.0)  # Golden color
    bsdf.inputs[6].default_value = 0.8  # Metallic
    bsdf.inputs[7].default_value = 0.2  # Roughness
    
    hero.data.materials.append(mat)
    
    print("✅ Pharaoh Hero created!")
    return hero

def create_khopesh_weapon():
    """Create 3D khopesh sword based on SDXL concept"""
    print("Creating 3D Khopesh Weapon...")
    
    # Create handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.8, location=(0, 0, 0.4))
    handle = bpy.context.active_object
    handle.name = "Khopesh_Handle"
    
    # Create blade using cube and modify
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.0))
    blade = bpy.context.active_object
    blade.name = "Khopesh_Blade"
    blade.scale = (0.05, 0.15, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create curved tip (khopesh characteristic)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, 1.4))
    tip = bpy.context.active_object
    tip.name = "Khopesh_Tip"
    tip.scale = (0.03, 0.3, 0.1)
    tip.rotation_euler = (0, 0, math.radians(30))
    bpy.ops.object.transform_apply(scale=True)
    
    # Join weapon parts
    bpy.ops.object.select_all(action='DESELECT')
    handle.select_set(True)
    bpy.context.view_layer.objects.active = handle
    blade.select_set(True)
    tip.select_set(True)
    bpy.ops.object.join()
    
    khopesh = bpy.context.active_object
    khopesh.name = "Khopesh"
    
    # Create bronze weapon material
    mat = bpy.data.materials.new(name="Bronze_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.7, 0.5, 0.1, 1.0)  # Bronze color
    bsdf.inputs[6].default_value = 0.9  # Metallic
    bsdf.inputs[7].default_value = 0.1  # Roughness
    
    khopesh.data.materials.append(mat)
    
    print("✅ Khopesh Weapon created!")
    return khopesh

def create_enemy_mummy():
    """Create 3D mummy enemy based on SDXL concept"""
    print("Creating 3D Mummy Enemy...")
    
    # Create humanoid base
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    body = bpy.context.active_object
    body.name = "Mummy_Body"
    body.scale = (0.7, 0.3, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create wrapped head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, 0, 2.2))
    head = bpy.context.active_object
    head.name = "Mummy_Head"
    
    # Create bandaged arms
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=1.0, location=(0.8, 0, 1.4))
    arm_r = bpy.context.active_object
    arm_r.name = "Mummy_Arm_R"
    arm_r.rotation_euler = (0, 0, math.radians(90))
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=1.0, location=(-0.8, 0, 1.4))
    arm_l = bpy.context.active_object
    arm_l.name = "Mummy_Arm_L"
    arm_l.rotation_euler = (0, 0, math.radians(90))
    
    # Create legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=1.0, location=(0.25, 0, 0.0))
    leg_r = bpy.context.active_object
    leg_r.name = "Mummy_Leg_R"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=1.0, location=(-0.25, 0, 0.0))
    leg_l = bpy.context.active_object
    leg_l.name = "Mummy_Leg_L"
    
    # Join mummy parts
    mummy_parts = [body, head, arm_r, arm_l, leg_r, leg_l]
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    
    for part in mummy_parts[1:]:
        part.select_set(True)
    
    bpy.ops.object.join()
    
    mummy = bpy.context.active_object
    mummy.name = "Enemy_Mummy"
    
    # Create mummy bandage material
    mat = bpy.data.materials.new(name="Mummy_Bandages")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.9, 0.8, 0.6, 1.0)  # Aged bandage color
    bsdf.inputs[7].default_value = 0.8  # Roughness
    
    mummy.data.materials.append(mat)
    
    print("✅ Mummy Enemy created!")
    return mummy

def create_anubis_boss():
    """Create 3D Anubis boss based on SDXL concept"""
    print("Creating 3D Anubis Boss...")
    
    # Create larger humanoid body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.2))
    body = bpy.context.active_object
    body.name = "Anubis_Body"
    body.scale = (1.0, 0.5, 1.4)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create jackal head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.8))
    head = bpy.context.active_object
    head.name = "Anubis_Head"
    head.scale = (0.6, 0.8, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create jackal snout
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.4, 2.8))
    snout = bpy.context.active_object
    snout.name = "Anubis_Snout"
    snout.scale = (0.3, 0.4, 0.2)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create ears
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3, -0.1, 3.2))
    ear_r = bpy.context.active_object
    ear_r.name = "Anubis_Ear_R"
    ear_r.scale = (0.1, 0.2, 0.4)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.3, -0.1, 3.2))
    ear_l = bpy.context.active_object
    ear_l.name = "Anubis_Ear_L"
    ear_l.scale = (0.1, 0.2, 0.4)
    
    # Create powerful arms
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.4, location=(1.1, 0, 1.6))
    arm_r = bpy.context.active_object
    arm_r.name = "Anubis_Arm_R"
    arm_r.rotation_euler = (0, 0, math.radians(90))
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.4, location=(-1.1, 0, 1.6))
    arm_l = bpy.context.active_object
    arm_l.name = "Anubis_Arm_L"
    arm_l.rotation_euler = (0, 0, math.radians(90))
    
    # Create strong legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.2, location=(0.35, 0, 0.0))
    leg_r = bpy.context.active_object
    leg_r.name = "Anubis_Leg_R"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.2, location=(-0.35, 0, 0.0))
    leg_l = bpy.context.active_object
    leg_l.name = "Anubis_Leg_L"
    
    # Join Anubis parts
    anubis_parts = [body, head, snout, ear_r, ear_l, arm_r, arm_l, leg_r, leg_l]
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    
    for part in anubis_parts[1:]:
        part.select_set(True)
    
    bpy.ops.object.join()
    
    anubis = bpy.context.active_object
    anubis.name = "Boss_Anubis"
    
    # Create dark Anubis material
    mat = bpy.data.materials.new(name="Anubis_Dark")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark black
    bsdf.inputs[7].default_value = 0.4  # Moderate roughness
    
    anubis.data.materials.append(mat)
    
    print("✅ Anubis Boss created!")
    return anubis

def add_basic_rigging(obj, armature_name):
    """Add basic armature rigging to character"""
    print(f"Adding rigging to {obj.name}...")
    
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    
    # Create armature
    bpy.ops.object.armature_add(location=(0, 0, 0))
    armature = bpy.context.active_object
    armature.name = armature_name
    
    # Enter edit mode to add bones
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Clear default bone
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()
    
    # Add root bone
    bpy.ops.armature.bone_primitive_add(name="Root")
    root_bone = armature.data.edit_bones["Root"]
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0, 0.5)
    
    # Add spine bone
    bpy.ops.armature.bone_primitive_add(name="Spine")
    spine_bone = armature.data.edit_bones["Spine"]
    spine_bone.head = (0, 0, 0.5)
    spine_bone.tail = (0, 0, 1.5)
    spine_bone.parent = root_bone
    
    # Add head bone
    bpy.ops.armature.bone_primitive_add(name="Head")
    head_bone = armature.data.edit_bones["Head"]
    head_bone.head = (0, 0, 1.5)
    head_bone.tail = (0, 0, 2.5)
    head_bone.parent = spine_bone
    
    # Add right hand socket
    bpy.ops.armature.bone_primitive_add(name="Socket_Hand_R")
    hand_r_bone = armature.data.edit_bones["Socket_Hand_R"]
    hand_r_bone.head = (0.8, 0, 1.4)
    hand_r_bone.tail = (1.0, 0, 1.4)
    hand_r_bone.parent = spine_bone
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Parent mesh to armature with automatic weights
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    print(f"✅ Rigging added to {obj.name}!")
    return armature

def export_model(obj, filename):
    """Export model as glTF"""
    print(f"Exporting {obj.name} as {filename}...")
    
    # Ensure output directory exists
    output_dir = "C:/Users/Bruno/Documents/Sand of Duat/assets/models"
    os.makedirs(output_dir, exist_ok=True)
    
    # Select only the object and its armature for export
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    
    # Also select armature if it exists
    if obj.parent and obj.parent.type == 'ARMATURE':
        obj.parent.select_set(True)
    
    # Export as glTF
    filepath = os.path.join(output_dir, filename)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format='GLB',
        export_animations=True,
        export_skins=True,
        export_morph=True,
    )
    
    print(f"✅ Exported {filename}!")

def main():
    """Main function to create all 3D models"""
    print("=" * 60)
    print("SANDS OF DUAT - 3D MODEL CREATION")
    print("Creating models from SDXL concept art...")
    print("=" * 60)
    
    # Clear scene
    clear_scene()
    
    # Create hero and export
    print("\n[1/4] Creating Hero Pharaoh...")
    hero = create_hero_pharaoh()
    hero_armature = add_basic_rigging(hero, "Hero_Armature")
    export_model(hero, "hero.glb")
    
    # Clear scene for next model
    clear_scene()
    
    # Create weapon and export
    print("\n[2/4] Creating Khopesh Weapon...")
    weapon = create_khopesh_weapon()
    export_model(weapon, "weapons/khopesh.glb")
    
    # Clear scene for next model
    clear_scene()
    
    # Create mummy enemy and export
    print("\n[3/4] Creating Mummy Enemy...")
    mummy = create_enemy_mummy()
    mummy_armature = add_basic_rigging(mummy, "Mummy_Armature")
    export_model(mummy, "mummy_enemy.glb")
    
    # Clear scene for next model
    clear_scene()
    
    # Create Anubis boss and export
    print("\n[4/4] Creating Anubis Boss...")
    anubis = create_anubis_boss()
    anubis_armature = add_basic_rigging(anubis, "Anubis_Armature")
    export_model(anubis, "anubis_boss.glb")
    
    print("\n" + "=" * 60)
    print("✅ ALL 3D MODELS CREATED SUCCESSFULLY!")
    print("Models exported to: assets/models/")
    print("- hero.glb")
    print("- weapons/khopesh.glb") 
    print("- mummy_enemy.glb")
    print("- anubis_boss.glb")
    print("=" * 60)

if __name__ == "__main__":
    main()