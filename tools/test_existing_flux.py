#!/usr/bin/env python3
"""
TEST EXISTING FLUX GENERATOR
============================
Testa o gerador Flux existente do projeto
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from sands_of_duat.ai_art.flux_generator import get_flux_generator
    
    print("TESTANDO FLUX GENERATOR EXISTENTE")
    print("=" * 35)
    
    # Get generator
    flux_gen = get_flux_generator()
    
    print("Flux generator carregado!")
    print("Carregando modelo Flux.1-dev...")
    
    # Load model
    if flux_gen.load_model():
        print("SUCESSO - Modelo carregado!")
        
        # Test generation
        prompt = "Anubis egyptian god with jackal head, golden collar, hades game art style"
        print(f"Gerando: {prompt}")
        
        image = flux_gen.generate_hades_egyptian_art(prompt)
        
        if image:
            # Save test image
            output_path = Path("test_flux_output.png")
            image.save(output_path)
            print(f"SUCESSO - Imagem salva: {output_path}")
            
            # Show memory usage
            memory = flux_gen.get_memory_usage()
            if memory:
                print(f"VRAM: {memory['allocated_gb']:.2f}GB usado / {memory['total_vram_gb']:.1f}GB total")
        else:
            print("FALHA - Nao gerou imagem")
    else:
        print("FALHA - Nao carregou modelo")
        
except Exception as e:
    print(f"ERRO: {e}")
    print("\nPossíveis soluções:")
    print("1. Verificar se diffusers está instalado")
    print("2. Verificar se Flux.1-dev está disponível")
    print("3. Usar sistema alternativo")