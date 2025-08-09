#!/usr/bin/env python3
"""
SIMPLE MAX GPU UTILIZATION - RTX 5070
=====================================
Abordagem simples para usar máxima GPU sem conflitos
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
from datetime import datetime

def main():
    print("CONFIGURANDO SDXL PARA MAXIMA GPU UTILIZATION")
    print("RTX 5070 - MODO ALTA PERFORMANCE")
    print("=" * 50)
    
    device = "cuda"
    
    # Verifica GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"GPU: {gpu_name}")
        print(f"VRAM: {vram_gb:.1f}GB")
    
    # Limpa cache
    torch.cuda.empty_cache()
    
    print("Carregando SDXL...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True,
    )
    
    print("Movendo para GPU...")
    pipe = pipe.to(device)
    
    # Sem CPU offload para usar GPU 100%
    print("Configurado para GPU 100% - sem CPU offload")
    
    # Prompt Hades-Egyptian
    prompt = """Anubis egyptian god with jackal head, golden ceremonial collar, 
    dramatic chiaroscuro lighting, pen and ink style, hades game art, 
    vibrant red and gold colors, heroic proportions, masterpiece, 
    highly detailed"""
    
    negative_prompt = """blurry, low quality, amateur, multiple characters, 
    anime style, cartoon, text, watermark, bad anatomy"""
    
    print("GERANDO IMAGEM - MAXIMA QUALIDADE")
    print("Resolucao: 1024x1024")
    print("Steps: 30 (alta qualidade)")
    print("=" * 40)
    
    start_time = time.time()
    
    # Geração com configurações de alta qualidade
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        num_inference_steps=30,
        guidance_scale=8.0,
        generator=torch.Generator(device=device).manual_seed(42)
    ).images[0]
    
    generation_time = time.time() - start_time
    
    # Salva resultado
    output_dir = Path("../../assets/work_in_progress/max_gpu_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"max_gpu_anubis_{timestamp}.png"
    filepath = output_dir / filename
    
    image.save(filepath, "PNG")
    
    print(f"RESULTADO:")
    print(f"Tempo de geracao: {generation_time:.1f}s")
    print(f"Performance: {60/generation_time:.1f} imagens/minuto")
    print(f"Arquivo salvo: {filename}")
    print(f"Qualidade: 1024x1024 alta resolucao")
    
    # Monitora uso da GPU durante geração
    if torch.cuda.is_available():
        used_memory = torch.cuda.memory_allocated() / (1024**3)
        max_memory = torch.cuda.max_memory_allocated() / (1024**3)
        print(f"VRAM usada: {used_memory:.2f}GB")
        print(f"VRAM pico: {max_memory:.2f}GB")
    
    print("\nSUCESSO - Imagem gerada com maxima utilizacao da GPU!")
    return filepath

if __name__ == "__main__":
    result = main()