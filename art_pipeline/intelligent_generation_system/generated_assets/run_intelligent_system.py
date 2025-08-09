
#!/usr/bin/env python3
"""
EXECUTE INTELLIGENT GENERATION SYSTEM
=====================================
Ponto de entrada principal para FASE 4
"""

import sys
from pathlib import Path

def main():
    print("SISTEMA INTELIGENTE DE GERACAO - FASE 4")
    print("=" * 40)
    print("Hades-Egyptian Asset Generation System")
    print()
    
    print("COMPONENTES DISPONIVEIS:")
    components = [
        ("Master Coordinator", "master_coordinator.py", "Sistema principal de coordenação"),
        ("ComfyUI Batch", "comfyui_batch_generation.py", "Geração em batch via ComfyUI"),
        ("Automatic1111", "automatic1111_batch.py", "Geração via A1111 API"),
        ("Quality Control", "quality_control_system.py", "Sistema de controle de qualidade"),
        ("Fooocus Guide", "fooocus_generation_guide.md", "Guia manual Fooocus"),
        ("Online Guide", "online_services_guide.md", "Guia serviços online")
    ]
    
    for i, (name, file, desc) in enumerate(components, 1):
        filepath = Path(file)
        status = "✓" if filepath.exists() else "✗"
        print(f"{i}. {status} {name}")
        print(f"   File: {file}")
        print(f"   Desc: {desc}")
        print()
    
    print("EXECUÇÃO RECOMENDADA:")
    print("1. Execute: python master_coordinator.py")
    print("2. Siga as instruções do coordenador")
    print("3. Gere 64 assets usando método preferido")
    print("4. Execute controle de qualidade")
    print("5. Finalize para FASE 5")
    
    print("\nPara iniciar, execute: python master_coordinator.py")

if __name__ == "__main__":
    main()
