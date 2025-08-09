#!/usr/bin/env python3
"""
HADES-EGYPTIAN ASSET GENERATION
ASCII-safe version for Windows console
"""

import os
os.environ['XFORMERS_DISABLED'] = '1'
import torch
from diffusers import StableDiffusionXLPipeline
from datetime import datetime

def main():
    print('TESTING HADES-EGYPTIAN ASSET GENERATION')
    print('=' * 45)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Device: {device}')
    if torch.cuda.is_available():
        print(f'GPU: {torch.cuda.get_device_name(0)}')
        print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')

    print('\nLoading SDXL pipeline...')
    pipeline = StableDiffusionXLPipeline.from_pretrained(
        'stabilityai/stable-diffusion-xl-base-1.0',
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant='fp16'
    )
    pipeline = pipeline.to(device)
    pipeline.enable_attention_slicing()  # Memory optimization
    print('Pipeline loaded successfully!')

    # Hades-Egyptian prompt from our specifications
    prompt = '''Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, pen and ink art style, dramatic chiaroscuro lighting, dark shadows, bright highlights, Hades game art style, Egyptian mythology, underworld deity, professional game art'''

    negative_prompt = '''blurry, low quality, bad anatomy, deformed, cartoon, anime, photographic, realistic, 3d render'''

    print(f'\nGenerating: {prompt[:60]}...')
    print('This may take 1-2 minutes on RTX 5070...')

    # Generate with optimized settings
    image = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=25,
        guidance_scale=7.5,
        width=1024,
        height=1024
    ).images[0]

    # Save to generated_art directory
    output_path = '../../../assets/generated_art/hades_egyptian_anubis_test_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)

    print(f'\nSUCCESS! Generated: {output_path}')
    print('First Hades-Egyptian asset created!')
    
    return output_path

if __name__ == "__main__":
    main()