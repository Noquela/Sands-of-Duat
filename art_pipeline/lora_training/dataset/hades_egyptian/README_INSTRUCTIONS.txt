
INSTRUCOES PARA GERAR DATASET:
=============================

1. EXECUTAR GERACAO:
   cd dataset\hades_egyptian
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
