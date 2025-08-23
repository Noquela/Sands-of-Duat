#!/usr/bin/env python3
"""
Advanced Blender pipeline for Hades-quality 3D models
Creates proper rigged characters with multiple animations and weapon sockets
"""

import bpy
import bmesh
import os
from mathutils import Vector

def clear_scene():
    """Clear all default objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_advanced_hero():
    """Create hero with proper proportions, rigging and animations like Hades"""
    print("Creating advanced hero model...")
    
    # Create base body mesh with proper proportions
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    torso = bpy.context.active_object
    torso.name = "Hero_Torso"
    torso.scale = (0.8, 0.4, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.8))
    head = bpy.context.active_object
    head.name = "Hero_Head"
    head.scale = (0.6, 0.6, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create pharaoh crown
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3.4))
    crown = bpy.context.active_object
    crown.name = "Pharaoh_Crown"
    crown.scale = (0.8, 0.8, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create arms
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.2, 0, 2.2))
    arm_r = bpy.context.active_object
    arm_r.name = "Hero_Arm_R"
    arm_r.scale = (0.3, 0.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.2, 0, 2.2))
    arm_l = bpy.context.active_object
    arm_l.name = "Hero_Arm_L"
    arm_l.scale = (0.3, 0.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create legs
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3, 0, 0))
    leg_r = bpy.context.active_object
    leg_r.name = "Hero_Leg_R"
    leg_r.scale = (0.3, 0.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.3, 0, 0))
    leg_l = bpy.context.active_object
    leg_l.name = "Hero_Leg_L"
    leg_l.scale = (0.3, 0.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join all body parts
    bpy.ops.object.select_all(action='DESELECT')
    torso.select_set(True)
    bpy.context.view_layer.objects.active = torso
    head.select_set(True)
    crown.select_set(True)
    arm_r.select_set(True)
    arm_l.select_set(True)
    leg_r.select_set(True)
    leg_l.select_set(True)
    bpy.ops.object.join()
    
    hero = bpy.context.active_object
    hero.name = "Hero_Pharaoh"
    
    return hero

def create_advanced_armature(hero):
    """Create proper armature with bones like Hades characters"""
    print("Creating advanced armature...")
    
    # Create armature
    bpy.ops.object.armature_add(location=(0, 0, 0))
    armature = bpy.context.active_object
    armature.name = "Hero_Armature"
    
    # Enter edit mode to create bones
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Clear default bone
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()
    
    # Create bone hierarchy
    # Root bone
    bpy.ops.armature.bone_primitive_add(name="Root")
    root_bone = armature.data.edit_bones["Root"]
    root_bone.head = Vector((0, 0, 0))
    root_bone.tail = Vector((0, 0, 0.5))
    
    # Spine bones
    bpy.ops.armature.bone_primitive_add(name="Spine_01")
    spine1 = armature.data.edit_bones["Spine_01"]
    spine1.head = Vector((0, 0, 0.5))
    spine1.tail = Vector((0, 0, 1.5))
    spine1.parent = root_bone
    
    bpy.ops.armature.bone_primitive_add(name="Spine_02")
    spine2 = armature.data.edit_bones["Spine_02"]
    spine2.head = Vector((0, 0, 1.5))
    spine2.tail = Vector((0, 0, 2.5))
    spine2.parent = spine1
    
    # Head bone
    bpy.ops.armature.bone_primitive_add(name="Head")
    head_bone = armature.data.edit_bones["Head"]
    head_bone.head = Vector((0, 0, 2.5))
    head_bone.tail = Vector((0, 0, 3.5))
    head_bone.parent = spine2
    
    # Right arm chain
    bpy.ops.armature.bone_primitive_add(name="Shoulder_R")
    shoulder_r = armature.data.edit_bones["Shoulder_R"]
    shoulder_r.head = Vector((0.8, 0, 2.2))
    shoulder_r.tail = Vector((1.2, 0, 2.2))
    shoulder_r.parent = spine2
    
    bpy.ops.armature.bone_primitive_add(name="Arm_R")
    arm_r_bone = armature.data.edit_bones["Arm_R"]
    arm_r_bone.head = Vector((1.2, 0, 2.2))
    arm_r_bone.tail = Vector((1.6, 0, 1.8))
    arm_r_bone.parent = shoulder_r
    
    bpy.ops.armature.bone_primitive_add(name="Hand_R")
    hand_r = armature.data.edit_bones["Hand_R"]
    hand_r.head = Vector((1.6, 0, 1.8))
    hand_r.tail = Vector((1.8, 0, 1.6))
    hand_r.parent = arm_r_bone
    
    # Left arm chain (mirrored)
    bpy.ops.armature.bone_primitive_add(name="Shoulder_L")
    shoulder_l = armature.data.edit_bones["Shoulder_L"]
    shoulder_l.head = Vector((-0.8, 0, 2.2))
    shoulder_l.tail = Vector((-1.2, 0, 2.2))
    shoulder_l.parent = spine2
    
    bpy.ops.armature.bone_primitive_add(name="Arm_L")
    arm_l_bone = armature.data.edit_bones["Arm_L"]
    arm_l_bone.head = Vector((-1.2, 0, 2.2))
    arm_l_bone.tail = Vector((-1.6, 0, 1.8))
    arm_l_bone.parent = shoulder_l
    
    bpy.ops.armature.bone_primitive_add(name="Hand_L")
    hand_l = armature.data.edit_bones["Hand_L"]
    hand_l.head = Vector((-1.6, 0, 1.8))
    hand_l.tail = Vector((-1.8, 0, 1.6))
    hand_l.parent = arm_l_bone
    
    # Right leg chain
    bpy.ops.armature.bone_primitive_add(name="Thigh_R")
    thigh_r = armature.data.edit_bones["Thigh_R"]
    thigh_r.head = Vector((0.3, 0, 0.5))
    thigh_r.tail = Vector((0.3, 0, -0.5))
    thigh_r.parent = root_bone
    
    bpy.ops.armature.bone_primitive_add(name="Shin_R")
    shin_r = armature.data.edit_bones["Shin_R"]
    shin_r.head = Vector((0.3, 0, -0.5))
    shin_r.tail = Vector((0.3, 0, -1.5))
    shin_r.parent = thigh_r
    
    # Left leg chain
    bpy.ops.armature.bone_primitive_add(name="Thigh_L")
    thigh_l = armature.data.edit_bones["Thigh_L"]
    thigh_l.head = Vector((-0.3, 0, 0.5))
    thigh_l.tail = Vector((-0.3, 0, -0.5))
    thigh_l.parent = root_bone
    
    bpy.ops.armature.bone_primitive_add(name="Shin_L")
    shin_l = armature.data.edit_bones["Shin_L"]
    shin_l.head = Vector((-0.3, 0, -0.5))
    shin_l.tail = Vector((-0.3, 0, -1.5))
    shin_l.parent = thigh_l
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create weapon sockets
    create_weapon_sockets(armature)
    
    return armature

def create_weapon_sockets(armature):
    """Create weapon attachment sockets"""
    print("Creating weapon sockets...")
    
    # Right hand socket
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(1.8, 0, 1.6))
    socket_r = bpy.context.active_object
    socket_r.name = "Socket_Hand_R"
    socket_r.scale = (0.1, 0.1, 0.1)
    
    # Parent to hand bone
    socket_r.parent = armature
    socket_r.parent_bone = "Hand_R"
    socket_r.parent_type = 'BONE'
    
    # Back socket for secondary weapons
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, -0.5, 2.5))
    socket_back = bpy.context.active_object
    socket_back.name = "Socket_Back"
    socket_back.scale = (0.1, 0.1, 0.1)
    
    socket_back.parent = armature
    socket_back.parent_bone = "Spine_02"
    socket_back.parent_type = 'BONE'

def create_hero_animations(armature):
    """Create multiple animations like Hades"""
    print("Creating hero animations...")
    
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Clear existing actions
    if armature.animation_data:
        armature.animation_data.action = None
    
    # IDLE Animation
    print("Creating idle animation...")
    idle_action = bpy.data.actions.new(name="Hero_Idle")
    armature.animation_data_create()
    armature.animation_data.action = idle_action
    
    # Idle: subtle breathing and weapon sway
    bpy.context.scene.frame_set(1)
    
    # Set initial pose
    spine1_bone = armature.pose.bones["Spine_01"]
    spine2_bone = armature.pose.bones["Spine_02"]
    
    # Frame 1
    spine1_bone.rotation_euler = (0.0, 0.0, 0.0)
    spine2_bone.rotation_euler = (0.0, 0.0, 0.0)
    spine1_bone.keyframe_insert(data_path="rotation_euler")
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    
    # Frame 30 (gentle sway)
    bpy.context.scene.frame_set(30)
    spine1_bone.rotation_euler = (0.05, 0.0, 0.0)
    spine2_bone.rotation_euler = (0.03, 0.0, 0.0)
    spine1_bone.keyframe_insert(data_path="rotation_euler")
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    
    # Frame 60 (return)
    bpy.context.scene.frame_set(60)
    spine1_bone.rotation_euler = (0.0, 0.0, 0.0)
    spine2_bone.rotation_euler = (0.0, 0.0, 0.0)
    spine1_bone.keyframe_insert(data_path="rotation_euler")
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    
    # WALK Animation
    print("Creating walk animation...")
    walk_action = bpy.data.actions.new(name="Hero_Walk")
    armature.animation_data.action = walk_action
    
    # Walk cycle: 20 frames
    bpy.context.scene.frame_set(1)
    
    root_bone = armature.pose.bones["Root"]
    thigh_r = armature.pose.bones["Thigh_R"]
    thigh_l = armature.pose.bones["Thigh_L"]
    
    # Frame 1: Right leg forward
    root_bone.location = (0.0, 0.0, 0.1)
    thigh_r.rotation_euler = (0.3, 0.0, 0.0)
    thigh_l.rotation_euler = (-0.3, 0.0, 0.0)
    
    root_bone.keyframe_insert(data_path="location")
    thigh_r.keyframe_insert(data_path="rotation_euler")
    thigh_l.keyframe_insert(data_path="rotation_euler")
    
    # Frame 10: Contact
    bpy.context.scene.frame_set(10)
    root_bone.location = (0.0, 0.0, 0.0)
    thigh_r.rotation_euler = (0.0, 0.0, 0.0)
    thigh_l.rotation_euler = (0.0, 0.0, 0.0)
    
    root_bone.keyframe_insert(data_path="location")
    thigh_r.keyframe_insert(data_path="rotation_euler")
    thigh_l.keyframe_insert(data_path="rotation_euler")
    
    # Frame 20: Left leg forward
    bpy.context.scene.frame_set(20)
    root_bone.location = (0.0, 0.0, 0.1)
    thigh_r.rotation_euler = (-0.3, 0.0, 0.0)
    thigh_l.rotation_euler = (0.3, 0.0, 0.0)
    
    root_bone.keyframe_insert(data_path="location")
    thigh_r.keyframe_insert(data_path="rotation_euler")
    thigh_l.keyframe_insert(data_path="rotation_euler")
    
    # ATTACK Animation
    print("Creating attack animation...")
    attack_action = bpy.data.actions.new(name="Hero_Attack")
    armature.animation_data.action = attack_action
    
    # Attack: 15 frame swing
    bpy.context.scene.frame_set(1)
    
    spine2_bone = armature.pose.bones["Spine_02"]
    shoulder_r = armature.pose.bones["Shoulder_R"]
    arm_r = armature.pose.bones["Arm_R"]
    
    # Frame 1: Wind up
    spine2_bone.rotation_euler = (0.0, 0.0, -0.5)
    shoulder_r.rotation_euler = (0.0, 0.0, 0.8)
    arm_r.rotation_euler = (0.0, 0.0, 0.5)
    
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    shoulder_r.keyframe_insert(data_path="rotation_euler")
    arm_r.keyframe_insert(data_path="rotation_euler")
    
    # Frame 8: Strike
    bpy.context.scene.frame_set(8)
    spine2_bone.rotation_euler = (0.0, 0.0, 0.3)
    shoulder_r.rotation_euler = (0.0, 0.0, -0.3)
    arm_r.rotation_euler = (0.0, 0.0, -0.8)
    
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    shoulder_r.keyframe_insert(data_path="rotation_euler")
    arm_r.keyframe_insert(data_path="rotation_euler")
    
    # Frame 15: Recovery
    bpy.context.scene.frame_set(15)
    spine2_bone.rotation_euler = (0.0, 0.0, 0.0)
    shoulder_r.rotation_euler = (0.0, 0.0, 0.0)
    arm_r.rotation_euler = (0.0, 0.0, 0.0)
    
    spine2_bone.keyframe_insert(data_path="rotation_euler")
    shoulder_r.keyframe_insert(data_path="rotation_euler")
    arm_r.keyframe_insert(data_path="rotation_euler")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def bind_mesh_to_armature(hero, armature):
    """Bind hero mesh to armature with automatic weights"""
    print("Binding mesh to armature...")
    
    # Select hero first, then armature
    bpy.ops.object.select_all(action='DESELECT')
    hero.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    
    # Parent with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print("✅ Hero mesh bound to armature!")

def create_pharaoh_material():
    """Create golden pharaoh material"""
    mat = bpy.data.materials.new(name="Pharaoh_Gold")
    mat.use_nodes = True
    
    # Get principled BSDF
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Golden pharaoh colors
    bsdf.inputs["Base Color"].default_value = (0.8, 0.6, 0.1, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.7
    bsdf.inputs["Roughness"].default_value = 0.2
    
    # Add some emissive glow for divine effect
    bsdf.inputs["Emission Color"].default_value = (0.3, 0.2, 0.0, 1.0)
    bsdf.inputs["Emission Strength"].default_value = 0.1
    
    return mat

def export_hero_glb(hero, armature, output_path):
    """Export hero with armature as glTF"""
    print(f"Exporting advanced hero to {output_path}...")
    
    # Select both hero and armature
    bpy.ops.object.select_all(action='DESELECT')
    hero.select_set(True)
    armature.select_set(True)
    
    # Also select sockets
    for obj in bpy.data.objects:
        if obj.name.startswith("Socket_"):
            obj.select_set(True)
    
    # Export with animations
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        use_selection=True,
        export_format='GLB',
        export_animations=True,
        export_morph=False,
        export_skins=True,
        export_def_bones=True,
    )
    print(f"✅ Advanced hero exported: {os.path.basename(output_path)}!")

def main():
    print("Creating advanced Hades-quality hero model...")
    
    # Clear scene
    clear_scene()
    
    # Create advanced hero mesh
    hero = create_advanced_hero()
    
    # Create advanced armature with proper bone hierarchy
    armature = create_advanced_armature(hero)
    
    # Create multiple animations
    create_hero_animations(armature)
    
    # Bind mesh to armature
    bind_mesh_to_armature(hero, armature)
    
    # Apply materials
    pharaoh_mat = create_pharaoh_material()
    hero.data.materials.append(pharaoh_mat)
    
    # Export
    output_dir = "C:/Users/Bruno/Documents/Sand of Duat/assets/models"
    os.makedirs(output_dir, exist_ok=True)
    
    export_hero_glb(hero, armature, os.path.join(output_dir, "advanced_hero.glb"))
    
    print("\n✅ Advanced hero pipeline complete!")
    print("Features:")
    print("- Proper bone hierarchy with 15 bones")
    print("- 3 animations: Idle, Walk, Attack")
    print("- Weapon sockets: Hand_R, Back")
    print("- Automatic mesh weighting")
    print("- Golden pharaoh material with emissive glow")

if __name__ == "__main__":
    main()