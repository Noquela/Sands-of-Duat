#!/usr/bin/env python3
"""
DATASET GENERATOR - HADES EGYPTIAN FUSION
=========================================
Gera dataset real para treinamento LoRA usando ComfyUI API
"""

import requests
import json
import base64
import time
from pathlib import Path
from datetime import datetime
import uuid

class DatasetGenerator:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"  # ComfyUI default
        self.dataset_dir = Path("dataset/hades_egyptian")
        
        # Workflow básico para ComfyUI
        self.workflow_template = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 8.0,
                    "denoise": 1,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": "euler_a",
                    "scheduler": "normal",
                    "seed": 42,
                    "steps": 30
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage", 
                "inputs": {
                    "batch_size": 1,
                    "height": 1024,
                    "width": 1024
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": "PROMPT_PLACEHOLDER"
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1], 
                    "text": "blurry, low quality, amateur, multiple characters"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "hades_egyptian_dataset",
                    "images": ["8", 0]
                }
            }
        }

    def check_comfyui_connection(self):
        """Verifica se ComfyUI está rodando."""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats")
            if response.status_code == 200:
                print("ComfyUI conectado!")
                return True
        except:
            pass
        
        print("ComfyUI nao encontrado. Alternativas:")
        print("1. Instalar ComfyUI: https://github.com/comfyanonymous/ComfyUI")
        print("2. Usar Automatic1111 API")
        print("3. Usar script offline")
        return False

    def generate_with_local_script(self):
        """Gera dataset usando script Python local (fallback)."""
        print("GERANDO DATASET COM SCRIPT LOCAL")
        print("=" * 35)
        
        # Carrega prompts
        prompts_file = self.dataset_dir / "training_prompts.json"
        with open(prompts_file, 'r', encoding='utf-8') as f:
            dataset_info = json.load(f)
        
        # Cria script de geração offline
        generation_script = f'''#!/usr/bin/env python3
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
        print(f"SDXL carregado em {{device}}")
        
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
            hades_prompt = f"{{prompt}}, hades game art style, pen and ink style, dramatic chiaroscuro lighting, vibrant colors, masterpiece"
            
            print(f"Gerando: {{category}} - {{prompt[:50]}}")
            
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
                    filename = f"{{category}}_{{prompt_data['id']:03d}}_{{i+1}}.png"
                    image_path = images_dir / filename
                    image.save(image_path, "PNG")
                    
                    # Salva caption
                    caption_path = captions_dir / f"{{filename[:-4]}}.txt"
                    with open(caption_path, "w", encoding="utf-8") as f:
                        f.write(hades_prompt)
                    
                    generated_count += 1
                    print(f"  Salvo: {{filename}} ({{generated_count}}/{{len(dataset_info['prompts']) * 4}})")
                    
                    # Pausa para evitar overheating
                    torch.cuda.empty_cache()
                    
            except Exception as e:
                print(f"  ERRO: {{e}}")
                continue
        
        print(f"\\nDATASET COMPLETO: {{generated_count}} imagens geradas!")
        
    except Exception as e:
        print(f"ERRO no pipeline: {{e}}")

if __name__ == "__main__":
    generate_dataset()
'''
        
        # Salva script de geração
        script_file = self.dataset_dir / "generate_offline.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(generation_script)
        
        print(f"Script de geracao criado: {script_file}")
        print("Para executar:")
        print(f"cd {self.dataset_dir}")
        print("python generate_offline.py")
        
        return script_file

    def create_caption_template(self):
        """Cria template para captions do LoRA."""
        print("\nCRIANDO TEMPLATE DE CAPTIONS")
        print("=" * 30)
        
        caption_template = {
            "deity": [
                "hades_egyptian_art, {character} egyptian god, divine presence, dramatic chiaroscuro lighting, pen and ink style, vibrant colors, heroic proportions, masterpiece",
                "egyptian mythology, {character} deity, godlike aura, hand-painted digital art, Jen Zee style, dynamic composition, detailed character design"
            ],
            "hero": [
                "hades_egyptian_art, egyptian warrior hero, determined expression, battle ready pose, pharaonic armor, dramatic lighting, vibrant red gold colors",
                "heroic character, egyptian hero, combat stance, hades game style, pen and ink technique, professional game art"
            ],
            "creature": [
                "hades_egyptian_art, ancient egyptian creature, mystical being, otherworldly essence, dramatic shadows, vibrant colors, detailed design",
                "egyptian mythology creature, magical beast, pen and ink style, hades art influence, atmospheric lighting"
            ],
            "environment": [
                "hades_egyptian_art, ancient egyptian architecture, temple interior, dramatic lighting, atmospheric perspective, hieroglyphic details, epic scale",
                "egyptian environment, architectural grandeur, underworld atmosphere, cinematic composition, detailed background"
            ],
            "ui_element": [
                "hades_egyptian_art, ornate decorative frame, hieroglyphic patterns, gold blue colors, game UI design, detailed ornamentation",
                "egyptian ornamental design, decorative elements, game interface style, intricate patterns"
            ]
        }
        
        template_file = self.dataset_dir / "caption_templates.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(caption_template, f, indent=2, ensure_ascii=False)
        
        print(f"Templates salvos: {template_file}")
        print("Usar para criar captions variadas para cada categoria")
        
        return template_file

    def setup_dataset_generation(self):
        """Setup completo para geração de dataset."""
        print("SETUP GERACAO DE DATASET - LORA TRAINING")
        print("=" * 45)
        
        # Verifica ComfyUI
        comfy_available = self.check_comfyui_connection()
        
        if not comfy_available:
            print("Usando metodo offline...")
            script_file = self.generate_with_local_script()
        else:
            print("ComfyUI disponivel - implementar integracao")
            script_file = self.generate_with_local_script()  # Por agora
        
        # Templates de caption
        caption_file = self.create_caption_template()
        
        # Instruções finais
        instructions = f'''
INSTRUCOES PARA GERAR DATASET:
=============================

1. EXECUTAR GERACAO:
   cd {self.dataset_dir}
   python generate_offline.py

2. VERIFICAR RESULTADOS:
   - images/ : 64 imagens PNG (1024x1024)
   - captions/ : 64 arquivos TXT com prompts

3. INICIAR TREINAMENTO LORA:
   cd ../..
   ./train_lora.sh

TEMPO ESTIMADO:
- Geracao dataset: 30-60 min
- Treinamento LoRA: 2-4 horas
- Total: 3-5 horas

GPU NECESSARIA: Sim (CUDA)
VRAM MINIMA: 8GB (RTX 5070 = 12GB OK)
'''
        
        instructions_file = self.dataset_dir / "README_INSTRUCTIONS.txt"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print("\n" + "=" * 45)
        print("SETUP DATASET COMPLETO!")
        print(f"Script: {script_file}")
        print(f"Templates: {caption_file}")
        print(f"Instrucoes: {instructions_file}")
        print("PRONTO PARA GERAR DATASET!")
        
        return True

def main():
    """Executa setup de geração de dataset."""
    generator = DatasetGenerator()
    generator.setup_dataset_generation()

if __name__ == "__main__":
    main()