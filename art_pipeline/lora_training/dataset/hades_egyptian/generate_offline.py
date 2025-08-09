#!/usr/bin/env python3
"""
OFFLINE DATASET GENERATION
==========================
Script para gerar dataset sem depender de APIs externas
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import json
from datetime import datetime

def generate_dataset():
    print("CARREGANDO SDXL...")
    
    # Configuração básica que deve funcionar
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        # Carrega pipeline básico
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device == "cuda" else None,
            use_safetensors=True
        )
        
        pipe = pipe.to(device)
        print(f"SDXL carregado em {device}")
        
        # Carrega prompts
        with open("training_prompts.json", "r", encoding="utf-8") as f:
            dataset_info = json.load(f)
        
        images_dir = Path("images")
        images_dir.mkdir(exist_ok=True)
        
        captions_dir = Path("captions")
        captions_dir.mkdir(exist_ok=True)
        
        generated_count = 0
        
        for prompt_data in dataset_info["prompts"]:
            prompt = prompt_data["prompt"]
            category = prompt_data["category"]
            
            # Adiciona elementos Hades ao prompt
            hades_prompt = f"{prompt}, hades game art style, pen and ink style, dramatic chiaroscuro lighting, vibrant colors, masterpiece"
            
            print(f"Gerando: {category} - {prompt[:50]}")
            
            try:
                # Gera 4 variações
                for i in range(4):
                    seed = 42 + prompt_data["id"] * 10 + i
                    
                    image = pipe(
                        prompt=hades_prompt,
                        negative_prompt="blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark",
                        width=1024,
                        height=1024,
                        num_inference_steps=30,
                        guidance_scale=7.5,
                        generator=torch.Generator(device=device).manual_seed(seed)
                    ).images[0]
                    
                    # Salva imagem
                    filename = f"{category}_{prompt_data['id']:03d}_{i+1}.png"
                    image_path = images_dir / filename
                    image.save(image_path, "PNG")
                    
                    # Salva caption
                    caption_path = captions_dir / f"{filename[:-4]}.txt"
                    with open(caption_path, "w", encoding="utf-8") as f:
                        f.write(hades_prompt)
                    
                    generated_count += 1
                    print(f"  Salvo: {filename} ({generated_count}/{len(dataset_info['prompts']) * 4})")
                    
                    # Pausa para evitar overheating
                    torch.cuda.empty_cache()
                    
            except Exception as e:
                print(f"  ERRO: {e}")
                continue
        
        print(f"\nDATASET COMPLETO: {generated_count} imagens geradas!")
        
    except Exception as e:
        print(f"ERRO no pipeline: {e}")

if __name__ == "__main__":
    generate_dataset()
