#!/usr/bin/env python3
"""
SANDS OF DUAT - Blender 3D Modeling Pipeline
Automated 3D model creation from SDXL concepts with rigging and animations
Run inside Blender: blender --background --python blender_3d_pipeline.py
"""

import bpy
import bmesh
import os
from pathlib import Path
from mathutils import Vector, Euler
import math

def clear_scene():
    """Clear default scene objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_pharaoh_hero():
    """Create low-poly pharaoh hero with rigging."""
    
    # Create base mesh (simplified humanoid)
    bpy.ops.mesh.primitive_cube_add()
    hero = bpy.context.object
    hero.name = "Hero_Pharaoh"
    
    # Enter edit mode and create basic humanoid shape
    bpy.context.view_layer.objects.active = hero
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Basic humanoid modeling (low-poly)
    bm = bmesh.from_mesh(hero.data)
    bm.clear()
    
    # Create simple humanoid mesh
    # Body (torso)
    bmesh.ops.create_cube(bm, size=2.0)
    
    # Scale for torso proportions
    for v in bm.verts:
        v.co.z *= 1.5  # Taller torso
        v.co.y *= 0.7  # Thinner torso
        v.co += Vector((0, 0, 1))  # Move up
    
    # Add head
    bm_head = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.6)
    for v in bm_head['verts']:
        v.co += Vector((0, 0, 3.5))
    
    # Add legs (simple cylinders)
    for side in [-0.4, 0.4]:
        bm_leg = bmesh.ops.create_cylinder(bm, radius=0.25, depth=2.0, segments=8)
        for v in bm_leg['verts']:
            v.co += Vector((side, 0, -1))
    
    # Add arms
    for side in [-1.2, 1.2]:
        bm_arm = bmesh.ops.create_cylinder(bm, radius=0.2, depth=1.8, segments=6)
        for v in bm_arm['verts']:
            v.co += Vector((side, 0, 2))
    
    # Update mesh
    bm.to_mesh(hero.data)
    bm.free()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return hero

def create_armature_with_sockets(hero):
    """Create armature with bone hierarchy and weapon sockets."""
    
    # Add armature
    bpy.ops.object.armature_add()
    armature = bpy.context.object
    armature.name = "Hero_Armature"
    
    # Enter edit mode for armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Get the default bone and rename it
    root_bone = armature.data.edit_bones[0]
    root_bone.name = "Root"
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0, 0.5)
    
    # Create bone hierarchy
    bones = {}
    
    # Spine bones
    spine1 = armature.data.edit_bones.new("Spine1")
    spine1.head = (0, 0, 0.5)
    spine1.tail = (0, 0, 1.5)
    spine1.parent = root_bone
    bones["spine1"] = spine1
    
    spine2 = armature.data.edit_bones.new("Spine2")
    spine2.head = (0, 0, 1.5)
    spine2.tail = (0, 0, 2.5)
    spine2.parent = spine1
    bones["spine2"] = spine2
    
    # Head bone
    head = armature.data.edit_bones.new("Head")
    head.head = (0, 0, 2.5)
    head.tail = (0, 0, 3.5)
    head.parent = spine2
    bones["head"] = head
    
    # Arm bones
    for side, x_pos in [("L", -1.2), ("R", 1.2)]:
        # Upper arm
        upper_arm = armature.data.edit_bones.new(f"UpperArm_{side}")
        upper_arm.head = (x_pos, 0, 2.2)
        upper_arm.tail = (x_pos, 0, 1.5)
        upper_arm.parent = spine2
        bones[f"upper_arm_{side.lower()}"] = upper_arm
        
        # Lower arm
        lower_arm = armature.data.edit_bones.new(f"LowerArm_{side}")
        lower_arm.head = (x_pos, 0, 1.5)
        lower_arm.tail = (x_pos, 0, 0.8)
        lower_arm.parent = upper_arm
        bones[f"lower_arm_{side.lower()}"] = lower_arm
        
        # Hand bone
        hand = armature.data.edit_bones.new(f"Hand_{side}")
        hand.head = (x_pos, 0, 0.8)
        hand.tail = (x_pos, 0, 0.5)
        hand.parent = lower_arm
        bones[f"hand_{side.lower()}"] = hand
    
    # Leg bones
    for side, x_pos in [("L", -0.4), ("R", 0.4)]:
        # Upper leg
        upper_leg = armature.data.edit_bones.new(f"UpperLeg_{side}")
        upper_leg.head = (x_pos, 0, 0)
        upper_leg.tail = (x_pos, 0, -1)
        upper_leg.parent = root_bone
        bones[f"upper_leg_{side.lower()}"] = upper_leg
        
        # Lower leg
        lower_leg = armature.data.edit_bones.new(f"LowerLeg_{side}")
        lower_leg.head = (x_pos, 0, -1)
        lower_leg.tail = (x_pos, 0, -2)
        lower_leg.parent = upper_leg
        bones[f"lower_leg_{side.lower()}"] = lower_leg
        
        # Foot
        foot = armature.data.edit_bones.new(f"Foot_{side}")
        foot.head = (x_pos, 0, -2)
        foot.tail = (x_pos, 0.3, -2)
        foot.parent = lower_leg
        bones[f"foot_{side.lower()}"] = foot
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create weapon sockets as empties
    sockets = {}
    
    # Right hand socket for weapons
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    socket_hand_r = bpy.context.object
    socket_hand_r.name = "Socket_Hand_R"
    socket_hand_r.parent = armature
    socket_hand_r.parent_bone = "Hand_R"
    socket_hand_r.parent_type = 'BONE'
    socket_hand_r.location = (0.2, 0, 0)  # Offset from hand bone
    sockets["hand_r"] = socket_hand_r
    
    # Back socket for secondary weapons
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    socket_back = bpy.context.object
    socket_back.name = "Socket_Back"
    socket_back.parent = armature
    socket_back.parent_bone = "Spine2"
    socket_back.parent_type = 'BONE'
    socket_back.location = (0, -0.3, 0)  # Behind the character
    sockets["back"] = socket_back
    
    return armature, sockets

def create_basic_animations(armature):
    """Create basic animations (idle, walk, attack)."""
    
    # Set armature as active
    bpy.context.view_layer.objects.active = armature
    
    # Create animation data
    armature.animation_data_create()
    
    # IDLE Animation
    idle_action = bpy.data.actions.new("Idle")
    armature.animation_data.action = idle_action
    
    # Set frame range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 60
    
    # Enter pose mode
    bpy.ops.object.mode_set(mode='POSE')
    
    # Animate breathing (subtle spine movement)
    spine2_bone = armature.pose.bones.get("Spine2")
    if spine2_bone:
        # Frame 1 - neutral
        bpy.context.scene.frame_set(1)
        spine2_bone.rotation_euler = Euler((0, 0, 0))
        spine2_bone.keyframe_insert(data_path="rotation_euler")
        
        # Frame 30 - slight expansion
        bpy.context.scene.frame_set(30)
        spine2_bone.rotation_euler = Euler((math.radians(2), 0, 0))
        spine2_bone.keyframe_insert(data_path="rotation_euler")
        
        # Frame 60 - back to neutral
        bpy.context.scene.frame_set(60)
        spine2_bone.rotation_euler = Euler((0, 0, 0))
        spine2_bone.keyframe_insert(data_path="rotation_euler")
    
    # WALK Animation
    walk_action = bpy.data.actions.new("Walk")
    
    # ATTACK Animation  
    attack_action = bpy.data.actions.new("Attack")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return {"idle": idle_action, "walk": walk_action, "attack": attack_action}

def apply_concept_texture(obj, texture_path):
    """Apply SDXL generated texture to object material."""
    
    # Create new material
    mat = bpy.data.materials.new(name=f"{obj.name}_Material")
    mat.use_nodes = True
    
    # Get material nodes
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Connect BSDF to output
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Add Image Texture node if texture exists
    if os.path.exists(texture_path):
        tex_node = nodes.new(type='ShaderNodeTexImage')
        tex_node.location = (-300, 0)
        
        # Load texture image
        img = bpy.data.images.load(texture_path)
        tex_node.image = img
        
        # Connect to BSDF
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(tex_node.outputs['Alpha'], bsdf.inputs['Alpha'])
        
        # Set alpha blend mode
        mat.blend_method = 'BLEND'
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def setup_vertex_groups_and_weights(hero, armature):
    """Setup vertex groups and automatic weights."""
    
    # Select hero mesh
    bpy.context.view_layer.objects.active = hero
    
    # Add armature modifier
    modifier = hero.modifiers.new(name="Armature", type='ARMATURE')
    modifier.object = armature
    
    # Create vertex groups for bones
    for bone in armature.data.bones:
        hero.vertex_groups.new(name=bone.name)
    
    # Automatic weights
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.select_all(action='DESELECT')
    hero.select_set(True)
    armature.select_set(True)
    
    # Parent with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

def export_glb(name, objects, output_dir):
    """Export objects as glTF (.glb) file."""
    
    # Select objects to export
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    
    # Export as glTF
    export_path = Path(output_dir) / f"{name}.glb"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    
    bpy.ops.export_scene.gltf(
        filepath=str(export_path),
        use_selection=True,
        export_format='GLB',
        export_animations=True,
        export_skins=True,
        export_morph=False,
        export_lights=False,
        export_cameras=False
    )
    
    print(f"[SUCCESS] Exported {name}.glb to {export_path}")

def create_weapon_khopesh():
    """Create khopesh sword weapon."""
    
    # Simple khopesh shape
    bpy.ops.mesh.primitive_cube_add()
    khopesh = bpy.context.object
    khopesh.name = "Khopesh_Sword"
    
    # Enter edit mode and shape into khopesh
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Scale to sword proportions
    bpy.ops.transform.resize(value=(0.1, 0.05, 1.5))
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Position for proper grip
    khopesh.location = (0, 0, 0.75)
    
    return khopesh

def main():
    """Main pipeline function."""
    
    print("SANDS OF DUAT - Blender 3D Modeling Pipeline")
    print("=" * 50)
    
    # Clear scene
    clear_scene()
    
    print("[STEP 1] Creating pharaoh hero mesh...")
    hero = create_pharaoh_hero()
    
    print("[STEP 2] Creating armature and weapon sockets...")
    armature, sockets = create_armature_with_sockets(hero)
    
    print("[STEP 3] Setting up vertex groups and weights...")
    setup_vertex_groups_and_weights(hero, armature)
    
    print("[STEP 4] Creating basic animations...")
    animations = create_basic_animations(armature)
    
    print("[STEP 5] Applying concept textures...")
    # Apply SDXL generated texture if available
    texture_path = "art/sdxl/textures/pharaoh_armor_albedo.png"
    if os.path.exists(texture_path):
        apply_concept_texture(hero, texture_path)
    
    print("[STEP 6] Creating weapons...")
    khopesh = create_weapon_khopesh()
    
    # Apply weapon texture
    weapon_texture_path = "art/sdxl/textures/khopesh_sword_concept.png"
    if os.path.exists(weapon_texture_path):
        apply_concept_texture(khopesh, weapon_texture_path)
    
    print("[STEP 7] Exporting glTF files...")
    
    # Export hero with armature
    export_glb("hero", [hero, armature] + list(sockets.values()), "assets/models")
    
    # Export weapons separately  
    export_glb("khopesh", [khopesh], "assets/models/weapons")
    
    print("[SUCCESS] 3D modeling pipeline complete!")
    print("[OUTPUT] glTF files saved to assets/models/")
    
    return True

if __name__ == "__main__":
    main()