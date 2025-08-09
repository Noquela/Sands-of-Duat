#!/bin/bash
# LORA TRAINING SCRIPT - HADES EGYPTIAN FUSION
# ============================================

echo "INICIANDO TREINAMENTO LORA HADES-EGYPTIAN"
echo "RTX 5070 - Configuracao otimizada"
echo "=========================================="

# Configurações do ambiente
export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH="${PYTHONPATH}:."

# Parâmetros do treinamento
MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"
DATASET_DIR="./dataset/hades_egyptian/images"
OUTPUT_DIR="./output/models"
LOG_DIR="./output/logs"

# Comando de treinamento
python -m accelerate.commands.launch --num_processes=1 --num_machines=1 --gpu_ids=0 \
  train_network.py \
  --pretrained_model_name_or_path="$MODEL_NAME" \
  --train_data_dir="$DATASET_DIR" \
  --output_dir="$OUTPUT_DIR" \
  --logging_dir="$LOG_DIR" \
  --resolution=1024 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --max_train_steps=1000 \
  --learning_rate=1e-4 \
  --lr_scheduler="cosine" \
  --lr_warmup_steps=100 \
  --network_module=networks.lora \
  --network_dim=128 \
  --network_alpha=32 \
  --mixed_precision="fp16" \
  --save_every_n_steps=250 \
  --enable_bucket \
  --cache_latents \
  --cache_text_encoder_outputs \
  --gradient_checkpointing \
  --xformers \
  --output_name="hades_egyptian_lora"

echo "TREINAMENTO CONCLUIDO!"
echo "Modelo LoRA salvo em: $OUTPUT_DIR"
