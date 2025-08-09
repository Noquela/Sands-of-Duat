#!/bin/bash
# Egyptian-Hades Game Art LoRA Training Script
# Generated automatically for Sands of Duat project

export MODEL_NAME="egyptian-hades-gameart-v1"
export INSTANCE_DIR="..\lora_training/processed"
export OUTPUT_DIR="..\lora_training\models"

python train_network.py \
    --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
    --train_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --output_name="$MODEL_NAME" \
    --resolution=1024 \
    --train_batch_size=1 \
    --learning_rate=0.0001 \
    --max_train_steps=1000 \
    --save_every_n_steps=100 \
    --mixed_precision="fp16" \
    --gradient_accumulation_steps=4 \
    --network_module="networks.lora" \
    --network_dim=32 \
    --network_alpha=32 \
    --optimizer_type="AdamW8bit" \
    --lr_scheduler="cosine_with_restarts" \
    --lr_warmup_steps=100 \
    --noise_offset=0.1 \
    --adaptive_noise_scale=0.00357 \
    --multires_noise_iterations=10 \
    --multires_noise_discount=0.1 \
    --log_with=tensorboard \
    --logging_dir="$OUTPUT_DIR/logs" \
    --enable_bucket \
    --min_bucket_reso=256 \
    --max_bucket_reso=2048 \
    --bucket_reso_steps=64 \
    --cache_latents \
    --cache_latents_to_disk \
    --save_model_as=safetensors \
    --persistent_data_loader_workers \
    --max_data_loader_n_workers=8
