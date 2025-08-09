"""
Simple Ra Card Generation using Stable Diffusion
Direct approach without complex pipelines
"""

import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image

def generate_ra_simple():
    print("GENERATING RA - SUN GOD CARD ART")
    print("=" * 50)
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        device = "cuda"
    else:
        print("Using CPU")
        device = "cpu"
    
    try:
        # Use Stable Diffusion XL for high quality
        print("\nLoading Stable Diffusion XL model...")
        
        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True
        )
        
        if device == "cuda":
            pipe = pipe.to("cuda")
            # Memory optimization for RTX 5070
            pipe.enable_model_cpu_offload()
        
        print("Model loaded successfully!")
        
        # Ra - Sun God prompt optimized for Hades-style quality
        prompt = """
        masterpiece, highly detailed, professional game art, 
        Ra the egyptian sun god, falcon headed deity, golden solar disk crown,
        ancient egyptian armor with hieroglyphs, powerful divine aura,
        radiant golden energy, warm desert lighting, detailed feathers,
        ornate jewelry, mystical atmosphere, rich colors, dramatic lighting,
        supergiant games art style, hand painted illustration,
        fantasy card game art, premium quality, 4k resolution
        """
        
        negative_prompt = """
        blurry, low quality, pixelated, amateur, cartoon, anime,
        modern clothing, realistic photo, dull colors, dark lighting,
        low resolution, artifacts, distorted, ugly, deformed
        """
        
        print("\nGenerating Ra artwork...")
        print(f"Prompt: {prompt[:100]}...")
        
        # Generate image with better settings
        with torch.no_grad():
            image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=8.0,
                width=768,
                height=1024,
                generator=torch.Generator(device=device).manual_seed(42)
            ).images[0]
        
        # Save the generated image
        output_dir = "assets/generated_art"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "ra_sun_god.png")
        image.save(output_path)
        
        print(f"\nRA ARTWORK GENERATED SUCCESSFULLY!")
        print(f"Saved to: {output_path}")
        print(f"Image size: {image.size}")
        
        # Basic quality check
        if image.size[0] >= 768 and image.size[1] >= 1024:
            print("QUALITY: High resolution achieved")
            return True
        else:
            print("QUALITY: Resolution lower than expected")
            return False
            
    except Exception as e:
        print(f"Error during generation: {e}")
        return False

if __name__ == "__main__":
    success = generate_ra_simple()
    if success:
        print("\nSUCCESS: Ra - Sun God card art generated!")
    else:
        print("\nFAILED: Could not generate Ra artwork")