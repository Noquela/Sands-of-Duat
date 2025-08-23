#!/usr/bin/env python3
"""
Create advanced enemy models with proper rigging and attack telegraphs
"""

import bpy
import os
from mathutils import Vector

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_mummy_guardian():
    """Create mummy guardian with telegraph animations"""
    print("Creating mummy guardian...")
    
    # Create body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    torso = bpy.context.active_object
    torso.name = "Mummy_Torso"
    torso.scale = (0.7, 0.4, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.6))
    head = bpy.context.active_object
    head.name = "Mummy_Head"
    head.scale = (0.5, 0.5, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create arms
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.0, 0, 2.0))
    arm_r = bpy.context.active_object
    arm_r.name = "Mummy_Arm_R"
    arm_r.scale = (0.25, 0.25, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.0, 0, 2.0))
    arm_l = bpy.context.active_object
    arm_l.name = "Mummy_Arm_L"
    arm_l.scale = (0.25, 0.25, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Create legs
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.25, 0, 0))
    leg_r = bpy.context.active_object
    leg_r.name = "Mummy_Leg_R"
    leg_r.scale = (0.25, 0.25, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.25, 0, 0))
    leg_l = bpy.context.active_object
    leg_l.name = "Mummy_Leg_L"
    leg_l.scale = (0.25, 0.25, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    torso.select_set(True)
    bpy.context.view_layer.objects.active = torso
    head.select_set(True)
    arm_r.select_set(True)
    arm_l.select_set(True)
    leg_r.select_set(True)
    leg_l.select_set(True)
    bpy.ops.object.join()
    
    mummy = bpy.context.active_object
    mummy.name = "Mummy_Guardian"
    
    # Mummy material
    mat = bpy.data.materials.new(name="Mummy_Bandages")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.8, 0.7, 0.5, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    
    mummy.data.materials.append(mat)
    
    return mummy

def create_scorpion_enemy():
    """Create fast scorpion enemy with quick attack patterns"""
    print("Creating desert scorpion...")
    
    # Main body
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.3))
    body = bpy.context.active_object
    body.name = "Scorpion_Body"
    body.scale = (1.2, 0.6, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    
    # Tail segments
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, -1.0, 0.8))
    tail1 = bpy.context.active_object
    tail1.name = "Scorpion_Tail1"
    tail1.scale = (0.4, 0.4, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, -1.2, 1.5))
    tail2 = bpy.context.active_object
    tail2.name = "Scorpion_Tail2"
    tail2.scale = (0.3, 0.3, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Stinger
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, radius2=0.05, depth=0.3, location=(0, -1.2, 2.0))
    stinger = bpy.context.active_object
    stinger.name = "Scorpion_Stinger"
    
    # Claws
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0.8, 0.8, 0.4))
    claw_r = bpy.context.active_object
    claw_r.name = "Scorpion_Claw_R"
    claw_r.scale = (0.3, 0.8, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(-0.8, 0.8, 0.4))
    claw_l = bpy.context.active_object
    claw_l.name = "Scorpion_Claw_L"
    claw_l.scale = (0.3, 0.8, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    tail1.select_set(True)
    tail2.select_set(True)
    stinger.select_set(True)
    claw_r.select_set(True)
    claw_l.select_set(True)
    bpy.ops.object.join()
    
    scorpion = bpy.context.active_object
    scorpion.name = "Desert_Scorpion"
    
    # Scorpion material
    mat = bpy.data.materials.new(name="Scorpion_Chitin")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.4, 0.3, 0.1, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.3
    bsdf.inputs["Metallic"].default_value = 0.1
    
    scorpion.data.materials.append(mat)
    
    return scorpion

def create_anubis_priest():
    """Create Anubis priest with ranged attacks"""
    print("Creating Anubis priest...")
    
    # Create body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    torso = bpy.context.active_object
    torso.name = "Priest_Torso"
    torso.scale = (0.6, 0.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Jackal head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.5))
    head = bpy.context.active_object
    head.name = "Priest_Head"
    head.scale = (0.4, 0.8, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Long snout
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0.6, 2.5))
    snout = bpy.context.active_object
    snout.name = "Priest_Snout"
    snout.scale = (0.3, 0.6, 0.2)
    bpy.ops.object.transform_apply(scale=True)
    
    # Arms with staff positioning
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.8, 0, 2.0))
    arm_r = bpy.context.active_object
    arm_r.name = "Priest_Arm_R"
    arm_r.scale = (0.2, 0.2, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.8, 0, 2.0))
    arm_l = bpy.context.active_object
    arm_l.name = "Priest_Arm_L"
    arm_l.scale = (0.2, 0.2, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Robes (extended torso)
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 0.2))
    robe = bpy.context.active_object
    robe.name = "Priest_Robe"
    robe.scale = (0.8, 0.4, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    
    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    torso.select_set(True)
    bpy.context.view_layer.objects.active = torso
    head.select_set(True)
    snout.select_set(True)
    arm_r.select_set(True)
    arm_l.select_set(True)
    robe.select_set(True)
    bpy.ops.object.join()
    
    priest = bpy.context.active_object
    priest.name = "Anubis_Priest"
    
    # Dark priest material
    mat = bpy.data.materials.new(name="Dark_Priest")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.1, 0.1, 0.15, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.7
    
    # Add dark magic glow
    bsdf.inputs["Emission Color"].default_value = (0.3, 0.1, 0.8, 1.0)
    bsdf.inputs["Emission Strength"].default_value = 0.2
    
    priest.data.materials.append(mat)
    
    return priest

def create_simple_armature(obj, bone_positions):
    """Create simple armature for enemies"""
    # Create armature
    bpy.ops.object.armature_add(location=(0, 0, 0))
    armature = bpy.context.active_object
    armature.name = f"{obj.name}_Armature"
    
    # Enter edit mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Clear default bone
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()
    
    # Create bones based on positions
    for bone_name, (head_pos, tail_pos, parent) in bone_positions.items():
        bpy.ops.armature.bone_primitive_add(name=bone_name)
        bone = armature.data.edit_bones[bone_name]
        bone.head = Vector(head_pos)
        bone.tail = Vector(tail_pos)
        
        if parent and parent in armature.data.edit_bones:
            bone.parent = armature.data.edit_bones[parent]
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Bind mesh to armature
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    return armature

def create_attack_telegraph_animations(enemy, armature, enemy_type):
    """Create telegraph animations for enemy attacks"""
    print(f"Creating telegraph animations for {enemy_type}...")
    
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    if armature.animation_data:
        armature.animation_data.action = None
    
    # Telegraph animation
    telegraph_action = bpy.data.actions.new(name=f"{enemy_type}_Telegraph")
    armature.animation_data_create()
    armature.animation_data.action = telegraph_action
    
    if enemy_type == "Mummy":
        # Mummy wind-up animation
        bpy.context.scene.frame_set(1)
        if "Body" in armature.pose.bones:
            body_bone = armature.pose.bones["Body"]
            body_bone.rotation_euler = (0.0, 0.0, 0.0)
            body_bone.keyframe_insert(data_path="rotation_euler")
        
        # Wind up
        bpy.context.scene.frame_set(20)
        if "Body" in armature.pose.bones:
            body_bone.rotation_euler = (0.0, 0.0, -0.5)
            body_bone.keyframe_insert(data_path="rotation_euler")
        
        # Strike
        bpy.context.scene.frame_set(25)
        if "Body" in armature.pose.bones:
            body_bone.rotation_euler = (0.0, 0.0, 0.3)
            body_bone.keyframe_insert(data_path="rotation_euler")
    
    elif enemy_type == "Scorpion":
        # Quick stinger attack
        bpy.context.scene.frame_set(1)
        if "Tail" in armature.pose.bones:
            tail_bone = armature.pose.bones["Tail"]
            tail_bone.rotation_euler = (0.0, 0.0, 0.0)
            tail_bone.keyframe_insert(data_path="rotation_euler")
        
        # Raise tail
        bpy.context.scene.frame_set(10)
        if "Tail" in armature.pose.bones:
            tail_bone.rotation_euler = (-1.0, 0.0, 0.0)
            tail_bone.keyframe_insert(data_path="rotation_euler")
        
        # Strike down
        bpy.context.scene.frame_set(15)
        if "Tail" in armature.pose.bones:
            tail_bone.rotation_euler = (0.5, 0.0, 0.0)
            tail_bone.keyframe_insert(data_path="rotation_euler")
    
    elif enemy_type == "Priest":
        # Casting animation
        bpy.context.scene.frame_set(1)
        if "Body" in armature.pose.bones:
            body_bone = armature.pose.bones["Body"]
            body_bone.rotation_euler = (0.0, 0.0, 0.0)
            body_bone.keyframe_insert(data_path="rotation_euler")
        
        # Channel spell
        bpy.context.scene.frame_set(30)
        if "Body" in armature.pose.bones:
            body_bone.rotation_euler = (-0.2, 0.0, 0.0)
            body_bone.keyframe_insert(data_path="rotation_euler")
        
        # Cast
        bpy.context.scene.frame_set(40)
        if "Body" in armature.pose.bones:
            body_bone.rotation_euler = (0.1, 0.0, 0.0)
            body_bone.keyframe_insert(data_path="rotation_euler")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def export_enemy_glb(enemy, armature, output_path):
    """Export enemy with armature as glTF"""
    print(f"Exporting {enemy.name} to {output_path}...")
    
    bpy.ops.object.select_all(action='DESELECT')
    enemy.select_set(True)
    armature.select_set(True)
    
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        use_selection=True,
        export_format='GLB',
        export_animations=True,
        export_skins=True,
    )
    print(f"✅ Exported: {os.path.basename(output_path)}")

def main():
    print("Creating advanced enemy models...")
    
    output_dir = "C:/Users/Bruno/Documents/Sand of Duat/assets/models/enemies"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create Mummy Guardian
    clear_scene()
    mummy = create_mummy_guardian()
    mummy_bones = {
        "Root": ((0, 0, 0), (0, 0, 0.5), None),
        "Body": ((0, 0, 0.5), (0, 0, 2.0), "Root"),
        "Head": ((0, 0, 2.0), (0, 0, 2.8), "Body"),
        "Arm_R": ((0.8, 0, 1.8), (1.2, 0, 1.8), "Body"),
        "Arm_L": ((-0.8, 0, 1.8), (-1.2, 0, 1.8), "Body"),
    }
    mummy_armature = create_simple_armature(mummy, mummy_bones)
    create_attack_telegraph_animations(mummy, mummy_armature, "Mummy")
    export_enemy_glb(mummy, mummy_armature, os.path.join(output_dir, "mummy_guardian_advanced.glb"))
    
    # Create Desert Scorpion
    clear_scene()
    scorpion = create_scorpion_enemy()
    scorpion_bones = {
        "Root": ((0, 0, 0), (0, 0, 0.3), None),
        "Body": ((0, 0, 0.3), (0, -0.5, 0.3), "Root"),
        "Tail": ((0, -0.5, 0.3), (0, -1.2, 2.0), "Body"),
        "Claw_R": ((0.5, 0.5, 0.3), (0.8, 0.8, 0.4), "Body"),
        "Claw_L": ((-0.5, 0.5, 0.3), (-0.8, 0.8, 0.4), "Body"),
    }
    scorpion_armature = create_simple_armature(scorpion, scorpion_bones)
    create_attack_telegraph_animations(scorpion, scorpion_armature, "Scorpion")
    export_enemy_glb(scorpion, scorpion_armature, os.path.join(output_dir, "desert_scorpion.glb"))
    
    # Create Anubis Priest
    clear_scene()
    priest = create_anubis_priest()
    priest_bones = {
        "Root": ((0, 0, 0), (0, 0, 0.5), None),
        "Body": ((0, 0, 0.5), (0, 0, 2.0), "Root"),
        "Head": ((0, 0, 2.0), (0, 0, 2.8), "Body"),
        "Arm_R": ((0.6, 0, 1.8), (0.8, 0, 1.8), "Body"),
        "Arm_L": ((-0.6, 0, 1.8), (-0.8, 0, 1.8), "Body"),
    }
    priest_armature = create_simple_armature(priest, priest_bones)
    create_attack_telegraph_animations(priest, priest_armature, "Priest")
    export_enemy_glb(priest, priest_armature, os.path.join(output_dir, "anubis_priest.glb"))
    
    print("\n✅ Advanced enemy models complete!")
    print("Created:")
    print("- Mummy Guardian: Tank enemy with slow, telegraphed attacks")
    print("- Desert Scorpion: Fast enemy with quick stinger attacks")
    print("- Anubis Priest: Ranged caster with magic projectiles")
    print("All with proper rigging and attack telegraph animations!")

if __name__ == "__main__":
    main()