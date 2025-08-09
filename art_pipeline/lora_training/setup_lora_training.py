#!/usr/bin/env python3
"""
LORA TRAINING SETUP - HADES EGYPTIAN FUSION
===========================================
Sistema completo para treinar LoRA especializado
"""

import os
import json
from pathlib import Path
from datetime import datetime

class LoRATrainingSetup:
    def __init__(self):
        self.base_dir = Path(".")
        self.dataset_dir = self.base_dir / "dataset" / "hades_egyptian"
        self.output_dir = self.base_dir / "output"
        self.config_dir = self.base_dir / "configs"
        
        # Configurações otimizadas para RTX 5070
        self.training_config = {
            "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
            "resolution": 1024,
            "batch_size": 1,  # RTX 5070 safe
            "learning_rate": 1e-4,
            "lr_scheduler": "cosine",
            "max_train_steps": 1000,
            "save_every_n_steps": 250,
            "mixed_precision": "fp16",
            "gradient_accumulation_steps": 4,
            
            # LoRA específico
            "network_alpha": 32,
            "network_dim": 128,
            "network_module": "networks.lora",
            
            # Otimizações RTX 5070
            "xformers": True,
            "cache_latents": True,
            "enable_bucket": True,
        }

    def create_directory_structure(self):
        """Cria estrutura de diretórios para treinamento."""
        print("CRIANDO ESTRUTURA DE DIRETORIOS LORA")
        print("=" * 40)
        
        # Diretórios principais
        dirs_to_create = [
            self.dataset_dir / "images",
            self.dataset_dir / "captions", 
            self.output_dir / "models",
            self.output_dir / "logs",
            self.output_dir / "samples",
            self.config_dir,
        ]
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Criado: {dir_path}")
        
        print("Estrutura de diretorios criada!")
        return True

    def create_dataset_images(self):
        """Cria dataset de imagens para treinamento."""
        print("\nCRIANDO DATASET DE IMAGENS HADES-EGYPTIAN")
        print("=" * 45)
        
        # Lista de prompts para gerar dataset
        training_prompts = [
            # Deidades egípcias estilo Hades
            "Anubis egyptian god with jackal head, golden collar, dramatic chiaroscuro lighting, pen and ink style",
            "Ra sun god with falcon head, solar disk crown, heroic proportions, vibrant colors",
            "Isis goddess with wings spread, protective pose, blue and gold colors, divine aura",
            "Set chaos god with unique creature head, red and black colors, menacing expression",
            "Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance",
            
            # Heróis egípcios estilo Hades
            "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors",
            "Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details",
            "Egyptian priestess hero with staff, flowing robes, mystical blue glow",
            
            # Criaturas egípcias estilo Hades  
            "Ancient egyptian sphinx creature, lion body, human head, golden brown colors",
            "Scarab beetle creature, metallic green blue carapace, magical glow",
            "Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance",
            
            # Ambientes egípcios estilo Hades
            "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows",
            "Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance",
            "Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture",
            
            # Elementos UI egípcios
            "Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style",
            "Ancient papyrus scroll background, aged texture, hieroglyphic text, mystical symbols",
        ]
        
        # Cria arquivo de prompts para dataset
        prompts_file = self.dataset_dir / "training_prompts.json"
        
        dataset_info = {
            "total_prompts": len(training_prompts),
            "target_images": len(training_prompts) * 4,  # 4 variações cada
            "style": "hades_egyptian_fusion",
            "prompts": [
                {
                    "id": i,
                    "prompt": prompt,
                    "variations": 4,
                    "category": self._categorize_prompt(prompt)
                }
                for i, prompt in enumerate(training_prompts)
            ],
            "created": datetime.now().isoformat()
        }
        
        with open(prompts_file, 'w', encoding='utf-8') as f:
            json.dump(dataset_info, f, indent=2, ensure_ascii=False)
        
        print(f"Dataset planejado: {len(training_prompts)} prompts base")
        print(f"Target total: {len(training_prompts) * 4} imagens")
        print(f"Arquivo prompts: {prompts_file}")
        
        return dataset_info

    def _categorize_prompt(self, prompt):
        """Categoriza prompt para organização."""
        if "god" in prompt or "goddess" in prompt:
            return "deity"
        elif "hero" in prompt or "warrior" in prompt or "pharaoh" in prompt:
            return "hero"  
        elif "creature" in prompt or "sphinx" in prompt or "scarab" in prompt:
            return "creature"
        elif "temple" in prompt or "tomb" in prompt or "pyramid" in prompt:
            return "environment"
        elif "frame" in prompt or "scroll" in prompt or "UI" in prompt:
            return "ui_element"
        else:
            return "misc"

    def create_training_config(self):
        """Cria arquivo de configuração para treinamento LoRA."""
        print("\nCRIANDO CONFIGURACAO DE TREINAMENTO")
        print("=" * 35)
        
        # Configuração completa do treinamento
        full_config = {
            "model": {
                "pretrained_model_name_or_path": self.training_config["model_name"],
                "vae": None,  # Usar VAE padrão
                "text_encoder": None,  # Usar text encoder padrão
            },
            
            "dataset": {
                "train_data_dir": str(self.dataset_dir / "images"),
                "caption_extension": ".txt",
                "resolution": f"{self.training_config['resolution']},{self.training_config['resolution']}",
                "batch_size": self.training_config["batch_size"],
                "enable_bucket": self.training_config["enable_bucket"],
                "min_bucket_reso": 256,
                "max_bucket_reso": 2048,
                "bucket_reso_steps": 64,
            },
            
            "training": {
                "max_train_steps": self.training_config["max_train_steps"],
                "learning_rate": self.training_config["learning_rate"],
                "lr_scheduler": self.training_config["lr_scheduler"],
                "lr_warmup_steps": 100,
                "gradient_accumulation_steps": self.training_config["gradient_accumulation_steps"],
                "mixed_precision": self.training_config["mixed_precision"],
                "save_every_n_steps": self.training_config["save_every_n_steps"],
                "save_state": True,
                "resume": None,
            },
            
            "network": {
                "network_module": self.training_config["network_module"],
                "network_dim": self.training_config["network_dim"],
                "network_alpha": self.training_config["network_alpha"],
                "network_args": {
                    "conv_dim": 64,
                    "conv_alpha": 32,
                }
            },
            
            "output": {
                "output_dir": str(self.output_dir / "models"),
                "logging_dir": str(self.output_dir / "logs"),
                "log_with": "tensorboard",
                "output_name": "hades_egyptian_lora",
            },
            
            "optimization": {
                "optimizer_type": "AdamW8bit",
                "xformers": self.training_config["xformers"],
                "cache_latents": self.training_config["cache_latents"],
                "cache_text_encoder_outputs": True,
                "gradient_checkpointing": True,
            },
            
            "validation": {
                "sample_every_n_steps": 250,
                "sample_prompts": [
                    "Anubis egyptian god, hades art style, masterpiece",
                    "Ra sun god, hades art style, vibrant colors",
                    "Egyptian hero warrior, hades art style, detailed"
                ],
                "sample_sampler": "euler_a",
                "sample_steps": 20,
            }
        }
        
        # Salva configuração
        config_file = self.config_dir / "lora_training_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(full_config, f, indent=2, ensure_ascii=False)
        
        print(f"Configuracao salva: {config_file}")
        print(f"Modelo base: {self.training_config['model_name']}")
        print(f"Resolucao: {self.training_config['resolution']}x{self.training_config['resolution']}")
        print(f"Max steps: {self.training_config['max_train_steps']}")
        print(f"Batch size: {self.training_config['batch_size']} (RTX 5070 safe)")
        
        return config_file

    def create_training_script(self):
        """Cria script de treinamento executável."""
        print("\nCRIANDO SCRIPT DE TREINAMENTO")
        print("=" * 30)
        
        training_script = '''#!/bin/bash
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
python -m accelerate.commands.launch --num_processes=1 --num_machines=1 --gpu_ids=0 \\
  train_network.py \\
  --pretrained_model_name_or_path="$MODEL_NAME" \\
  --train_data_dir="$DATASET_DIR" \\
  --output_dir="$OUTPUT_DIR" \\
  --logging_dir="$LOG_DIR" \\
  --resolution=1024 \\
  --train_batch_size=1 \\
  --gradient_accumulation_steps=4 \\
  --max_train_steps=1000 \\
  --learning_rate=1e-4 \\
  --lr_scheduler="cosine" \\
  --lr_warmup_steps=100 \\
  --network_module=networks.lora \\
  --network_dim=128 \\
  --network_alpha=32 \\
  --mixed_precision="fp16" \\
  --save_every_n_steps=250 \\
  --enable_bucket \\
  --cache_latents \\
  --cache_text_encoder_outputs \\
  --gradient_checkpointing \\
  --xformers \\
  --output_name="hades_egyptian_lora"

echo "TREINAMENTO CONCLUIDO!"
echo "Modelo LoRA salvo em: $OUTPUT_DIR"
'''
        
        script_file = self.base_dir / "train_lora.sh"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(training_script)
        
        # Torna executável (Unix/Linux)
        try:
            os.chmod(script_file, 0o755)
        except:
            pass  # Windows não precisa
        
        print(f"Script criado: {script_file}")
        print("Para executar: ./train_lora.sh")
        
        return script_file

    def setup_complete_lora_training(self):
        """Setup completo do sistema de treinamento LoRA."""
        print("SETUP COMPLETO LORA TRAINING - HADES EGYPTIAN")
        print("=" * 50)
        
        try:
            # 1. Estrutura de diretórios
            self.create_directory_structure()
            
            # 2. Dataset de prompts
            dataset_info = self.create_dataset_images()
            
            # 3. Configuração de treinamento
            config_file = self.create_training_config()
            
            # 4. Script executável
            script_file = self.create_training_script()
            
            # 5. Relatório final
            setup_report = {
                "timestamp": datetime.now().isoformat(),
                "setup_status": "complete",
                "dataset_prompts": len(dataset_info["prompts"]),
                "target_images": dataset_info["target_images"],
                "config_file": str(config_file),
                "training_script": str(script_file),
                "gpu_optimized_for": "RTX 5070",
                "estimated_training_time": "2-4 hours",
                "next_steps": [
                    "1. Gerar imagens do dataset usando SDXL",
                    "2. Criar captions para cada imagem",
                    "3. Executar script de treinamento",
                    "4. Testar LoRA treinado"
                ]
            }
            
            report_file = self.base_dir / "lora_setup_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(setup_report, f, indent=2, ensure_ascii=False)
            
            print("\n" + "=" * 50)
            print("SETUP LORA COMPLETO!")
            print(f"Dataset: {dataset_info['target_images']} imagens planejadas")
            print(f"Configuracao: {config_file}")
            print(f"Script: {script_file}")
            print(f"Relatorio: {report_file}")
            print("PRONTO PARA INICIAR TREINAMENTO!")
            
            return True
            
        except Exception as e:
            print(f"ERRO no setup: {e}")
            return False

def main():
    """Executa setup completo LoRA."""
    setup = LoRATrainingSetup()
    success = setup.setup_complete_lora_training()
    
    if success:
        print("\nSUCESSO - Sistema LoRA configurado!")
    else:
        print("\nFALHA - Erro na configuracao LoRA")

if __name__ == "__main__":
    main()