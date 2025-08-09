#!/usr/bin/env python3
"""
TESTE REAL DE GERAÇÃO - SDXL
============================
Vamos realmente gerar uma imagem para verificar se funciona.
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
from datetime import datetime

def test_real_generation():
    """Testa geração real de uma imagem."""
    print("Testando geração REAL com SDXL...")
    
    # Configuração
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando: {device}")
    
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Carrega pipeline
    print("Carregando SDXL...")
    try:
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device == "cuda" else None,
            use_safetensors=True
        ).to(device)
        
        # Otimizações
        pipe.enable_model_cpu_offload()
        if hasattr(pipe, 'enable_attention_slicing'):
            pipe.enable_attention_slicing(1)
            
        print("SDXL carregado com sucesso!")
        
    except Exception as e:
        print(f"Erro carregando SDXL: {e}")
        return None
    
    # Prompt simples para teste
    prompt = "Anubis egyptian god with jackal head, golden collar, dramatic lighting, digital art"
    negative_prompt = "blurry, low quality, multiple characters, text, watermark"
    
    print(f"Prompt: {prompt}")
    print("Gerando imagem...")
    
    try:
        start_time = time.time()
        
        # Geração
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=512,  # Menor para teste rápido
            height=512,
            num_inference_steps=20,  # Menos steps para teste
            guidance_scale=7.5,
            generator=torch.Generator(device=device).manual_seed(42)
        ).images[0]
        
        generation_time = time.time() - start_time
        print(f"Gerado em {generation_time:.1f}s")
        
        # Salva
        output_dir = Path("../../assets/work_in_progress/real_test")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"real_test_anubis_{timestamp}.png"
        filepath = output_dir / filename
        
        image.save(filepath, "PNG")
        print(f"Salvo: {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"Erro na geração: {e}")
        return None

if __name__ == "__main__":
    result = test_real_generation()
    if result:
        print("SUCESSO - Imagem real gerada!")
    else:
        print("FALHA - Não conseguiu gerar imagem real")