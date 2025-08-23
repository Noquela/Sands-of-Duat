#!/usr/bin/env python3
"""
🔧 BLENDER HADES-STYLE PROCESSOR
Complete Blender pipeline for creating Hades-quality 3D assets:
- Import and clean mesh
- Apply Hades-style toon shaders  
- Add proper rigging with Rigify
- Create weapon sockets
- Export optimized .glb
"""

import bpy
import bmesh
import os
import sys
from mathutils import Vector, Matrix, Euler

def clear_scene():
    """Clear all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def import_mesh(mesh_path):
    """Import the raw mesh file"""
    print(f"Importing mesh: {mesh_path}")
    
    if mesh_path.endswith('.obj'):
        try:
            bpy.ops.wm.obj_import(filepath=mesh_path)
        except:
            # Fallback for older Blender versions
            bpy.ops.import_scene.obj(filepath=mesh_path)
    elif mesh_path.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=mesh_path)
    elif mesh_path.endswith('.ply'):
        bpy.ops.import_mesh.ply(filepath=mesh_path)
    else:
        print(f"Unsupported mesh format: {mesh_path}")
        return None
        
    # Get the imported object
    imported_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None
    if imported_obj:
        print(f"Imported: {imported_obj.name}")
        return imported_obj
    else:
        print("No object imported")
        return None

def clean_mesh(obj):
    """Clean and optimize the mesh"""
    print("Cleaning mesh...")
    
    # Enter edit mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Remove doubles and clean up
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.fill_holes()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("Mesh cleaned")

def create_hades_material(obj, material_name="HadesMaterial"):
    """Create Hades-style toon shader material"""
    print("🎨 Creating Hades-style material...")
    
    # Create new material
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes for Hades-style toon shader
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (400, 0)
    
    # Main toon shader
    toon_node = nodes.new('ShaderNodeBsdfToon')
    toon_node.location = (200, 0)
    toon_node.inputs['Roughness'].default_value = 0.8
    toon_node.inputs['Size'].default_value = 0.7
    toon_node.inputs['Smooth'].default_value = 0.1
    
    # Base color for Egyptian theme
    if "pharaoh" in material_name.lower() or "hero" in material_name.lower():
        toon_node.inputs['Color'].default_value = (0.8, 0.6, 0.2, 1.0)  # Golden
    elif "anubis" in material_name.lower():
        toon_node.inputs['Color'].default_value = (0.2, 0.2, 0.4, 1.0)  # Dark blue
    elif "mummy" in material_name.lower():
        toon_node.inputs['Color'].default_value = (0.6, 0.5, 0.3, 1.0)  # Sandy brown
    else:
        toon_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1.0)  # Gray default
        
    # ColorRamp for better toon shading
    colorramp_node = nodes.new('ShaderNodeValToRGB')
    colorramp_node.location = (0, 0)
    colorramp_node.color_ramp.elements[0].position = 0.3
    colorramp_node.color_ramp.elements[1].position = 0.8
    
    # Fresnel for rim lighting (Hades style)
    fresnel_node = nodes.new('ShaderNodeFresnel')
    fresnel_node.location = (-200, 100)
    fresnel_node.inputs['IOR'].default_value = 1.2
    
    # Mix for rim effect
    mix_node = nodes.new('ShaderNodeMixRGB')
    mix_node.location = (0, 100)
    mix_node.blend_type = 'ADD'
    mix_node.inputs['Fac'].default_value = 0.3
    mix_node.inputs['Color2'].default_value = (1.0, 0.8, 0.4, 1.0)  # Warm rim light
    
    # Connect nodes
    links.new(fresnel_node.outputs['Fac'], colorramp_node.inputs['Fac'])
    links.new(colorramp_node.outputs['Color'], mix_node.inputs['Color1'])
    links.new(toon_node.outputs['BSDF'], mix_node.inputs['Color1'])
    links.new(mix_node.outputs['Color'], output_node.inputs['Surface'])
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    print(f"✅ Hades material '{material_name}' created and assigned")

def add_rigify_rig(obj, character_type):
    """Add Rigify humanoid rig for animation"""
    print("🦴 Adding Rigify rig...")
    
    # Enable Rigify addon
    bpy.ops.preferences.addon_enable(module="rigify")
    
    # Add meta-rig
    bpy.ops.object.armature_add()
    rig = bpy.context.active_object
    rig.name = f"{obj.name}_Rig"
    
    # Scale rig to match character
    if "boss" in character_type.lower():
        rig.scale = (1.5, 1.5, 1.8)
    elif "enemy" in character_type.lower():
        rig.scale = (0.8, 0.8, 0.9)
    else:
        rig.scale = (1.0, 1.0, 1.0)
        
    bpy.ops.object.transform_apply(scale=True)
    
    # Generate Rigify rig
    try:
        bpy.ops.pose.rigify_generate()
        print("✅ Rigify rig generated")
        
        # Parent mesh to rig with automatic weights
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        rig.select_set(True)
        bpy.context.view_layer.objects.active = rig
        
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        print("✅ Mesh parented to rig")
        
    except Exception as e:
        print(f"⚠️ Rigify generation failed: {e}")
        print("💡 Using basic armature instead")
        # Fallback to basic armature
        add_basic_armature(obj)

def add_basic_armature(obj):
    """Add basic armature as fallback"""
    print("🦴 Adding basic armature...")
    
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    armature.name = f"{obj.name}_Armature"
    
    # Enter edit mode to add bones
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Add basic bones
    edit_bones = armature.data.edit_bones
    
    # Root bone
    root_bone = edit_bones.new("Root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0, 0.5)
    
    # Spine bones
    spine_bone = edit_bones.new("Spine")
    spine_bone.head = (0, 0, 0.5)
    spine_bone.tail = (0, 0, 1.5)
    spine_bone.parent = root_bone
    
    # Head bone
    head_bone = edit_bones.new("Head")
    head_bone.head = (0, 0, 2.5)
    head_bone.tail = (0, 0, 3.2)
    head_bone.parent = spine_bone
    
    # Arm bones
    arm_l_bone = edit_bones.new("Arm.L")
    arm_l_bone.head = (-1.0, 0, 2.2)
    arm_l_bone.tail = (-1.8, 0, 2.2)
    arm_l_bone.parent = spine_bone
    
    arm_r_bone = edit_bones.new("Arm.R")
    arm_r_bone.head = (1.0, 0, 2.2)
    arm_r_bone.tail = (1.8, 0, 2.2)
    arm_r_bone.parent = spine_bone
    
    # Leg bones
    leg_l_bone = edit_bones.new("Leg.L")
    leg_l_bone.head = (-0.3, 0, 0.5)
    leg_l_bone.tail = (-0.3, 0, -0.5)
    leg_l_bone.parent = root_bone
    
    leg_r_bone = edit_bones.new("Leg.R")
    leg_r_bone.head = (0.3, 0, 0.5)
    leg_r_bone.tail = (0.3, 0, -0.5)
    leg_r_bone.parent = root_bone
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Parent mesh to armature
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print("✅ Basic armature created and parented")

def add_weapon_sockets(obj):
    """Add weapon attachment sockets"""
    print("⚔️ Adding weapon sockets...")
    
    # Create empty objects as sockets
    sockets = [
        ("Socket_Hand_R", (1.8, 0, 2.2)),
        ("Socket_Hand_L", (-1.8, 0, 2.2)), 
        ("Socket_Back", (0, -0.5, 2.5)),
        ("Socket_Hip", (0.5, 0, 1.2))
    ]
    
    for socket_name, location in sockets:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
        socket = bpy.context.active_object
        socket.name = socket_name
        socket.parent = obj
        print(f"✅ Added socket: {socket_name}")

def add_basic_animations(armature):
    """Add basic idle animation"""
    print("🎬 Adding basic animations...")
    
    if not armature or armature.type != 'ARMATURE':
        print("⚠️ No armature found for animation")
        return
        
    # Create idle animation
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Create action
    action = bpy.data.actions.new(name="idle")
    armature.animation_data_create()
    armature.animation_data.action = action
    
    # Add simple breathing motion
    if "Spine" in armature.pose.bones:
        spine_bone = armature.pose.bones["Spine"]
        
        # Keyframe at frame 1
        bpy.context.scene.frame_set(1)
        spine_bone.scale = (1.0, 1.0, 1.0)
        spine_bone.keyframe_insert(data_path="scale")
        
        # Keyframe at frame 60 (slight scale)
        bpy.context.scene.frame_set(60)
        spine_bone.scale = (1.02, 1.02, 1.01)
        spine_bone.keyframe_insert(data_path="scale")
        
        # Keyframe at frame 120 (back to normal)
        bpy.context.scene.frame_set(120)
        spine_bone.scale = (1.0, 1.0, 1.0)
        spine_bone.keyframe_insert(data_path="scale")
        
    bpy.ops.object.mode_set(mode='OBJECT')
    print("✅ Basic idle animation added")

def setup_render_settings():
    """Setup Eevee render settings for Hades style"""
    print("🌟 Setting up Hades-style rendering...")
    
    # Use Eevee for real-time rendering
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    
    # Enable toon shading features
    eevee = bpy.context.scene.eevee
    eevee.use_taa = True
    eevee.taa_samples = 64
    eevee.use_bloom = True
    eevee.bloom_intensity = 0.5
    eevee.bloom_radius = 6.5
    
    # Enable subsurface scattering for skin
    eevee.use_ssr = True
    eevee.use_ssr_refraction = True
    
    print("✅ Render settings configured for Hades style")

def export_glb(obj, output_path, character_name):
    """Export the final model as .glb"""
    print(f"📦 Exporting to: {output_path}")
    
    # Select the character and its armature
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    
    # Also select armature if it exists
    for child in obj.children:
        if child.type == 'ARMATURE':
            child.select_set(True)
            
    # Find and select armature that has this object as child
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            for child in ob.children:
                if child == obj:
                    ob.select_set(True)
                    break
    
    # Export settings for Bevy compatibility
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        check_existing=False,
        export_format='GLB',
        export_selection=True,
        export_materials='EXPORT',
        export_animations=True,
        export_optimize_animation_size=True,
        export_anim_single_armature=True,
        export_force_indices=False,
        export_yup=False  # Bevy uses Z-up
    )
    
    print(f"✅ Exported {character_name} as .glb")

def main():
    """Main processing pipeline"""
    if len(sys.argv) < 4:
        print("Usage: blender --background --python blender_hades_processor.py -- input.obj output.glb character_name")
        return
        
    # Get command line arguments
    input_mesh = sys.argv[-3]
    output_path = sys.argv[-2] 
    character_name = sys.argv[-1]
    
    print(f"🏺 Processing Hades-style character: {character_name}")
    print(f"📥 Input: {input_mesh}")
    print(f"📦 Output: {output_path}")
    
    try:
        # Clear scene
        clear_scene()
        
        # Import mesh
        obj = import_mesh(input_mesh)
        if not obj:
            return
            
        # Clean mesh
        clean_mesh(obj)
        
        # Create Hades-style material
        create_hades_material(obj, f"{character_name}_Material")
        
        # Add rigging
        add_rigify_rig(obj, character_name)
        
        # Add weapon sockets
        add_weapon_sockets(obj)
        
        # Find armature and add animations
        armature = None
        for child in bpy.data.objects:
            if child.type == 'ARMATURE' and obj in [c for c in child.children]:
                armature = child
                break
                
        if armature:
            add_basic_animations(armature)
            
        # Setup render settings
        setup_render_settings()
        
        # Export as .glb
        export_glb(obj, output_path, character_name)
        
        print(f"🎉 Successfully processed {character_name}!")
        
    except Exception as e:
        print(f"❌ Error processing {character_name}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()