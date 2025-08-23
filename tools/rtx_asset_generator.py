#!/usr/bin/env python3
"""
SANDS OF DUAT - RTX 5070 REAL AI Asset Generator
Uses actual Stable Diffusion with your RTX 5070 GPU for high-quality Egyptian assets
"""

import torch
import os
import time
from pathlib import Path

def check_gpu():
    """Check RTX 5070 availability."""
    if not torch.cuda.is_available():
        print("[WARNING] CUDA not available! Will use CPU for generation.")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    print(f"[GPU] Detected: {gpu_name}")
    print(f"[VRAM] Available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Test if we can actually use the GPU
    try:
        torch.cuda.empty_cache()
        test_tensor = torch.randn(10, 10).to("cuda")
        print("[GPU] RTX 5070 is ready for AI generation!")
        return True
    except Exception as e:
        print(f"[WARNING] GPU test failed: {e}")
        print("[INFO] Will use CPU for generation (slower but works)")
        return False

def install_requirements():
    """Install required packages for RTX generation."""
    print("[INSTALL] Installing RTX-optimized AI packages...")
    
    packages = [
        "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128",
        "diffusers transformers accelerate",
        "xformers",
        "pillow requests"
    ]
    
    for package in packages:
        print(f"Installing: {package}")
        os.system(f"pip install {package}")

def generate_isometric_characters():
    """Generate true 3D isometric character sprites for the game."""
    
    # Specialized isometric prompts for game characters
    character_prompts = {
        "pharaoh_warrior_iso": "3D isometric view, 3/4 angle perspective, majestic Egyptian pharaoh warrior, golden armor and headdress, holding ceremonial khopesh sword, muscular build, regal pose, standing at attention, game character sprite, clean transparent background, high detail, cinematic lighting, Hades game art style",
        
        "anubis_judge_iso": "3D isometric view, 3/4 angle perspective, intimidating Anubis jackal-headed judge, black and gold Egyptian ceremonial robes, holding scales of justice, tall imposing figure, ancient Egyptian deity, game character sprite, clean transparent background, dramatic lighting, Hades game art style",
        
        "mummy_guardian_iso": "3D isometric view, 3/4 angle perspective, menacing Egyptian mummy guardian, wrapped in ancient bandages, glowing red eyes, tattered royal burial wrappings, defensive combat stance, undead warrior, game character sprite, clean transparent background, eerie atmospheric lighting, Hades game art style",
        
        "set_chaos_iso": "3D isometric view, 3/4 angle perspective, fierce Set Egyptian god of chaos, red-skinned muscular warrior, distinctive Set animal head, bronze armor with chaos symbols, wielding curved war blade, aggressive battle pose, game character sprite, clean transparent background, intense dramatic lighting, Hades game art style",
        
        "isis_mother_iso": "3D isometric view, 3/4 angle perspective, graceful Isis Egyptian goddess, flowing white and gold robes, wings spread majestically, ankh staff in hand, serene yet powerful expression, divine aura, game character sprite, clean transparent background, ethereal magical lighting, Hades game art style",
        
        "ra_sun_god_iso": "3D isometric view, 3/4 angle perspective, radiant Ra sun god, falcon-headed deity, blazing solar disk crown, golden ornate armor, staff of power, commanding presence, divine solar energy, game character sprite, clean transparent background, brilliant golden lighting, Hades game art style"
    }
    
    return character_prompts

def generate_isometric_environments():
    """Generate 3D isometric environment elements."""
    
    environment_prompts = {
        # Floor textures
        "hieroglyph_floor": "seamless tileable Egyptian hieroglyph floor texture, 3D isometric perspective, ancient stone tiles with carved hieroglyphs, gold inlays, weathered sandstone, temple floor pattern, high resolution, game ready texture",
        
        "tomb_floor_ornate": "seamless tileable ornate Egyptian tomb floor, 3D isometric view, intricate geometric patterns, blue and gold mosaic tiles, pharaoh burial chamber style, luxurious temple flooring, game texture",
        
        # 3D Elements
        "egyptian_pillar_iso": "3D isometric Egyptian temple pillar, massive stone column with hieroglyphic carvings, lotus capital, weathered sandstone texture, ancient architecture, game environment asset, clean background",
        
        "torch_brazier_iso": "3D isometric Egyptian torch brazier, ornate bronze fire bowl on tall stand, flickering flames, warm orange glow, temple lighting fixture, game environment prop, transparent background",
        
        "anubis_statue_iso": "3D isometric Anubis statue, black stone carved deity, sitting jackal pose, golden accents, temple guardian sculpture, Egyptian art style, game decoration asset, clean background",
        
        "sarcophagus_iso": "3D isometric Egyptian sarcophagus, ornate golden burial casket, pharaoh mummy case, detailed hieroglyphic decorations, royal tomb artifact, game environment prop, transparent background",
        
        "obelisk_iso": "3D isometric Egyptian obelisk, tall stone monument with hieroglyphic inscriptions, weathered sandstone, ancient temple marker, imposing structure, game environment asset, clean background"
    }
    
    return environment_prompts

def generate_rtx_assets():
    """Generate assets using RTX 5070 or CPU."""
    try:
        from diffusers import DiffusionPipeline
        import torch
        from PIL import Image
        
        # Check if we can use GPU
        use_gpu = torch.cuda.is_available()
        device = "cuda" if use_gpu else "cpu"
        dtype = torch.float16 if use_gpu else torch.float32
        
        print(f"[AI] Loading SDXL (Stable Diffusion XL) for {device.upper()}...")
        print("[QUALITY] Using high-quality SDXL model for better assets!")
        
        # Load SDXL pipeline - MUCH better quality!
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=dtype,
            use_safetensors=True,
            variant="fp16" if use_gpu else None
        )
        pipe = pipe.to(device)
        
        # Device-specific optimizations  
        if use_gpu:
            print("[GPU] Using standard CUDA acceleration (XFormers disabled for RTX 5070)")
            # Skip XFormers due to RTX 5070 compatibility issues
            # pipe.enable_model_cpu_offload() # Skip this too to use full GPU
        
        print(f"[SUCCESS] Pipeline loaded! Using {device.upper()} acceleration")
        
        # Get specialized isometric prompts
        character_prompts = generate_isometric_characters()
        environment_prompts = generate_isometric_environments()
        
        # Combine all assets with specialized prompts
        assets = {
            # Character Sprites (True 3D isometric view)
            "pharaoh_warrior_iso": character_prompts["pharaoh_warrior_iso"],
            "anubis_judge_iso": character_prompts["anubis_judge_iso"], 
            "mummy_guardian_iso": character_prompts["mummy_guardian_iso"],
            "set_chaos_iso": character_prompts["set_chaos_iso"],
            "isis_mother_iso": character_prompts["isis_mother_iso"],
            "ra_sun_god_iso": character_prompts["ra_sun_god_iso"],
            
            # Floor Textures (3D isometric seamless)
            "hieroglyph_floor": environment_prompts["hieroglyph_floor"],
            "tomb_floor_ornate": environment_prompts["tomb_floor_ornate"],
            
            # 3D Environment Elements (isometric)
            "egyptian_pillar_iso": environment_prompts["egyptian_pillar_iso"],
            "torch_brazier_iso": environment_prompts["torch_brazier_iso"],
            "anubis_statue_iso": environment_prompts["anubis_statue_iso"],
            "sarcophagus_iso": environment_prompts["sarcophagus_iso"],
            "obelisk_iso": environment_prompts["obelisk_iso"],
            
            # UI Elements (3D styled)
            "ankh_health": "masterpiece, ultra detailed, 3D rendered UI icon, golden egyptian ankh symbol, health indicator, glowing effect, clean design, game interface, transparent background, 8k",
            "scarab_energy": "masterpiece, ultra detailed, 3D rendered UI icon, egyptian scarab beetle, energy symbol, blue glow, game interface, clean design, transparent background, 8k",
            "eye_of_horus": "masterpiece, ultra detailed, 3D rendered UI icon, eye of horus symbol, protection aura, golden glow, game interface, clean design, transparent background, 8k",
            
            # Weapons/Items (3D isometric)
            "khopesh_sword": "masterpiece, ultra detailed, 3D isometric view, egyptian khopesh sword, curved blade, golden handle, hieroglyph engravings, game weapon item, 3D rendered, clean background, 8k",
            "ankh_artifact": "masterpiece, ultra detailed, 3D isometric view, golden ankh artifact, mystical glow, floating effect, game collectible item, 3D rendered, clean background, 8k",
            "canopic_jar": "masterpiece, ultra detailed, 3D isometric view, egyptian canopic jar, ornate design, mystical contents, game item, 3D rendered, clean background, 8k"
        }
        
        # Create output directory
        output_dir = Path("ai_generated/rtx_generated")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for name, prompt in assets.items():
            print(f"\n[GEN] Generating: {name}")
            print(f"[PROMPT] {prompt}")
            
            start_time = time.time()
            
            # Generate with SDXL optimized settings
            image = pipe(
                prompt=prompt,
                negative_prompt="blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts",
                height=1152,  # SDXL optimal resolution  
                width=1152,   # Square format for game assets
                num_inference_steps=40,  # Higher steps for better quality
                guidance_scale=8.0,      # SDXL optimal guidance
                generator=torch.Generator(device=device).manual_seed(42)
            ).images[0]
            
            generation_time = time.time() - start_time
            
            # Save image
            output_path = output_dir / f"{name}_rtx.png"
            image.save(output_path)
            
            print(f"[SUCCESS] Generated in {generation_time:.2f}s")
            print(f"[SAVED] {output_path}")
            
            # Memory usage info
            if use_gpu:
                vram_used = torch.cuda.memory_allocated() / 1024**3
                print(f"[VRAM] Used: {vram_used:.2f} GB / 12 GB")
            else:
                print("[CPU] Memory usage varies, generation complete")
        
        print(f"\n[COMPLETE] AI ASSET GENERATION COMPLETE!")
        if use_gpu:
            print("[RTX] All assets generated using your RTX 5070 GPU!")
        else:
            print("[CPU] All assets generated using CPU (consider fixing CUDA for faster generation)")
        
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        print("Run: pip install diffusers transformers torch torchvision")
        return False
    except Exception as e:
        print(f"[ERROR] Error during generation: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("     RTX 5070 REAL AI ASSET GENERATOR")
    print("    Sands of Duat - Egyptian Assets")
    print("=" * 60)
    
    gpu_available = check_gpu()
    if not gpu_available:
        print("GPU not available, will use CPU generation...")
        use_cpu = input("Continue with CPU generation? (y/n): ").lower()
        if use_cpu != 'y':
            exit(1)
    
    print(f"\n[RTX] Starting RTX 5070 generation...")
    
    if generate_rtx_assets():
        print("\n[SUCCESS] Your RTX 5070 has generated real AI assets!")
    else:
        print("\n[ERROR] Generation failed. Check requirements above.")