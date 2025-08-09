#!/usr/bin/env python3
"""
BATCH HADES-EGYPTIAN ASSET GENERATION
Generate multiple professional assets for the game
"""

import os
os.environ['XFORMERS_DISABLED'] = '1'
import torch
from diffusers import StableDiffusionXLPipeline
from datetime import datetime
import json

def main():
    print('BATCH HADES-EGYPTIAN ASSET GENERATION')
    print('=' * 42)

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
    pipeline.enable_attention_slicing()
    print('Pipeline loaded successfully!')

    # High-priority Hades-Egyptian assets from our specifications
    assets_to_generate = [
        {
            "name": "anubis_deity_legendary",
            "prompt": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, pen and ink art style, dramatic chiaroscuro lighting, dark shadows, bright highlights, Hades game art style, Egyptian mythology, underworld deity, professional game art",
            "category": "legendary",
            "type": "deity"
        },
        {
            "name": "ra_sun_god_legendary", 
            "prompt": "Ra egyptian sun god with falcon head, solar disk crown, radiant golden aura, pen and ink art style, dramatic lighting, divine majesty, Hades game art style, Egyptian mythology, professional game art",
            "category": "legendary",
            "type": "deity"
        },
        {
            "name": "isis_goddess_legendary",
            "prompt": "Isis egyptian goddess with throne crown, protective wings spread, magical aura, pen and ink art style, dramatic chiaroscuro lighting, divine feminine power, Hades game art style, Egyptian mythology, professional game art",
            "category": "legendary", 
            "type": "deity"
        },
        {
            "name": "set_chaos_god_legendary",
            "prompt": "Set egyptian god of chaos with animal head, dark energy swirling, menacing presence, pen and ink art style, dramatic shadows, Hades game art style, Egyptian mythology, chaos deity, professional game art",
            "category": "legendary",
            "type": "deity"
        },
        {
            "name": "egyptian_warrior_epic",
            "prompt": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, khopesh sword, pen and ink art style, heroic proportions, dramatic lighting, Hades game art style, professional game art",
            "category": "epic",
            "type": "hero"
        },
        {
            "name": "sphinx_guardian_rare",
            "prompt": "Egyptian sphinx creature with lion body and human head, ancient wisdom in eyes, stone texture, pen and ink art style, mysterious presence, Hades game art style, mythological creature, professional game art",
            "category": "rare",
            "type": "creature"
        },
        {
            "name": "mummy_guardian_rare",
            "prompt": "Egyptian mummy guardian wrapped in ancient bandages, glowing eyes, desert tomb guardian, pen and ink art style, undead presence, Hades game art style, mythological creature, professional game art",
            "category": "rare",
            "type": "creature"
        },
        {
            "name": "temple_interior_epic",
            "prompt": "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic lighting, atmospheric shadows, pen and ink art style, Hades game art style, architectural grandeur, professional game art",
            "category": "epic",
            "type": "environment"
        }
    ]

    negative_prompt = "blurry, low quality, bad anatomy, deformed, cartoon, anime, photographic, realistic, 3d render, modern, contemporary"
    
    generated_assets = []
    total_assets = len(assets_to_generate)

    for i, asset in enumerate(assets_to_generate):
        print(f'\n[{i+1}/{total_assets}] Generating {asset["name"]}...')
        print(f'Category: {asset["category"]} | Type: {asset["type"]}')
        
        try:
            # Generate image
            image = pipeline(
                prompt=asset["prompt"],
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.5,
                width=1024,
                height=1024
            ).images[0]
            
            # Save image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'hades_egyptian_{asset["name"]}_{timestamp}.png'
            output_path = f'../../../assets/generated_art/{filename}'
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image.save(output_path)
            
            # Save metadata
            metadata = {
                "name": asset["name"],
                "category": asset["category"],
                "type": asset["type"],
                "prompt": asset["prompt"],
                "generation_date": datetime.now().isoformat(),
                "filename": filename,
                "specifications": {
                    "resolution": "1024x1024",
                    "format": "PNG",
                    "style": "Hades-Egyptian Fusion",
                    "quality": "Professional Game Art"
                }
            }
            
            metadata_path = f'../../../assets/generated_art/{filename.replace(".png", ".json")}'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            generated_assets.append({
                "name": asset["name"],
                "path": output_path,
                "metadata": metadata_path,
                "success": True
            })
            
            print(f'  SUCCESS: {filename}')
            
        except Exception as e:
            print(f'  FAILED: {str(e)}')
            generated_assets.append({
                "name": asset["name"],
                "success": False,
                "error": str(e)
            })

    # Generate batch report
    successful = sum(1 for asset in generated_assets if asset.get("success", False))
    print(f'\n' + '=' * 50)
    print('BATCH GENERATION COMPLETE')
    print(f'Total Assets: {total_assets}')
    print(f'Successfully Generated: {successful}')
    print(f'Failed: {total_assets - successful}')
    print(f'Success Rate: {(successful/total_assets)*100:.1f}%')
    
    # Save batch report
    report = {
        "batch_info": {
            "generation_date": datetime.now().isoformat(),
            "total_assets": total_assets,
            "successful": successful,
            "failed": total_assets - successful,
            "success_rate": (successful/total_assets)*100
        },
        "assets": generated_assets,
        "system_info": {
            "device": device,
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
            "pytorch_version": torch.__version__
        }
    }
    
    report_path = f'../../../assets/generated_art/batch_generation_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f'Batch report saved: {report_path}')
    print('\nHADES-EGYPTIAN ASSETS READY FOR QUALITY CONTROL!')

if __name__ == "__main__":
    main()