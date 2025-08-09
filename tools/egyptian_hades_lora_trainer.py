#!/usr/bin/env python3
"""
EGYPTIAN-HADES GAME ART LoRA TRAINER
===================================

Custom LoRA training system for consistent, high-quality Egyptian/Hades-style game art.
This will create a specialized model for generating perfect assets for Sands of Duat.
"""

import os
import requests
from pathlib import Path
import json
from PIL import Image, ImageOps
import shutil
from urllib.parse import urlparse
import time

class EgyptianHadesLoRATrainer:
    def __init__(self):
        self.project_root = Path("../")
        self.training_dir = self.project_root / "lora_training"
        self.dataset_dir = self.training_dir / "dataset"
        self.output_dir = self.training_dir / "models"
        
        # Create directories
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.training_config = {
            "model_name": "egyptian-hades-gameart-v1",
            "base_model": "stabilityai/stable-diffusion-xl-base-1.0",
            "resolution": 1024,
            "batch_size": 1,
            "learning_rate": 1e-4,
            "max_train_steps": 1000,
            "save_every_n_steps": 100,
            "mixed_precision": "fp16",
            "gradient_accumulation_steps": 4
        }

    def create_training_dataset(self):
        """Create and organize training dataset for LoRA."""
        print("PHASE 1: Creating High-Quality Training Dataset...")
        
        # Define our dataset structure
        dataset_categories = {
            "hades_art": [
                "Hades game character portraits - Zagreus, gods, NPCs",
                "Hades weapon designs and UI elements", 
                "Hades architectural backgrounds",
                "Hades color palette and lighting style"
            ],
            "egyptian_art": [
                "Ancient Egyptian hieroglyphic art",
                "Egyptian gods and goddesses artwork",
                "Pharaonic portraits and royal imagery",
                "Egyptian temple and pyramid art",
                "Ancient Egyptian jewelry and artifacts"
            ],
            "card_game_art": [
                "Magic The Gathering card art - Egyptian themed",
                "Yu-Gi-Oh Egyptian god cards",
                "Hearthstone card art style",
                "Legends of Runeterra card frames"
            ]
        }
        
        # Create dataset structure
        for category, descriptions in dataset_categories.items():
            category_dir = self.dataset_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Create instruction file for manual curation
            instruction_file = category_dir / "COLLECTION_INSTRUCTIONS.txt"
            with open(instruction_file, 'w') as f:
                f.write(f"DATASET COLLECTION FOR: {category.upper()}\n")
                f.write("=" * 50 + "\n\n")
                f.write("Collect HIGH-QUALITY images for:\n")
                for desc in descriptions:
                    f.write(f"- {desc}\n")
                f.write("\nQUALITY REQUIREMENTS:\n")
                f.write("- Resolution: 1024x1024 minimum\n")
                f.write("- Clear, sharp images\n")
                f.write("- Consistent artistic quality\n")
                f.write("- No watermarks or text overlays\n")
                f.write("- Diverse poses and compositions\n")
                f.write("\nTarget: 15-25 images per category\n")
        
        print(f"Training dataset structure created at: {self.dataset_dir}")
        print("Next step: Manually curate 50-75 high-quality reference images")

    def prepare_dataset_for_training(self):
        """Process and prepare dataset for LoRA training."""
        print("PHASE 2: Processing Dataset for Training...")
        
        processed_dir = self.training_dir / "processed"
        processed_dir.mkdir(exist_ok=True)
        
        image_count = 0
        
        # Process all images in dataset
        for category_dir in self.dataset_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                print(f"Processing {category_dir.name}...")
                
                for img_file in category_dir.glob("*.{jpg,jpeg,png,webp}"):
                    if img_file.is_file():
                        self.process_training_image(img_file, processed_dir, image_count)
                        image_count += 1
        
        print(f"Processed {image_count} training images")
        self.create_training_metadata(processed_dir, image_count)

    def process_training_image(self, img_path: Path, output_dir: Path, index: int):
        """Process individual training image."""
        try:
            # Load and process image
            with Image.open(img_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to training resolution while maintaining aspect ratio
                img = ImageOps.fit(img, (self.training_config["resolution"], 
                                       self.training_config["resolution"]), 
                                 Image.Resampling.LANCZOS)
                
                # Save processed image
                output_path = output_dir / f"train_{index:04d}.jpg"
                img.save(output_path, "JPEG", quality=95)
                
                # Create corresponding caption file
                caption_path = output_dir / f"train_{index:04d}.txt"
                caption = self.generate_training_caption(img_path)
                with open(caption_path, 'w') as f:
                    f.write(caption)
                
                print(f"Processed: {img_path.name} -> {output_path.name}")
                
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    def generate_training_caption(self, img_path: Path) -> str:
        """Generate training caption for image based on category and filename."""
        category = img_path.parent.name
        filename = img_path.stem.lower()
        
        # Base trigger word for our LoRA
        caption = "egyptian_hades_art, "
        
        # Category-specific tags
        if "hades" in category.lower():
            caption += "hades game style, supergiant games art, "
            if "character" in filename:
                caption += "character portrait, "
            elif "weapon" in filename:
                caption += "weapon design, "
            elif "background" in filename:
                caption += "environment art, "
        
        elif "egyptian" in category.lower():
            caption += "ancient egyptian art, "
            if "god" in filename:
                caption += "egyptian deity, "
            elif "pharaoh" in filename:
                caption += "pharaonic art, "
            elif "temple" in filename:
                caption += "egyptian architecture, "
        
        elif "card" in category.lower():
            caption += "card game art, trading card design, "
        
        # Common quality tags
        caption += "masterpiece, high quality, detailed, professional game art"
        
        return caption

    def create_training_metadata(self, processed_dir: Path, image_count: int):
        """Create metadata files for training."""
        config = {
            **self.training_config,
            "num_train_images": image_count,
            "trigger_word": "egyptian_hades_art",
            "dataset_path": str(processed_dir),
            "regularization_images": None
        }
        
        # Save training config
        config_path = self.training_dir / "training_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Training configuration saved to: {config_path}")

    def create_kohya_training_script(self):
        """Create Kohya_ss training script for the LoRA."""
        print("PHASE 3: Creating Kohya_ss Training Script...")
        
        script_content = f"""#!/bin/bash
# Egyptian-Hades Game Art LoRA Training Script
# Generated automatically for Sands of Duat project

export MODEL_NAME="{self.training_config['model_name']}"
export INSTANCE_DIR="{self.training_dir}/processed"
export OUTPUT_DIR="{self.output_dir}"

python train_network.py \\
    --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \\
    --train_data_dir="$INSTANCE_DIR" \\
    --output_dir="$OUTPUT_DIR" \\
    --output_name="$MODEL_NAME" \\
    --resolution={self.training_config['resolution']} \\
    --train_batch_size={self.training_config['batch_size']} \\
    --learning_rate={self.training_config['learning_rate']} \\
    --max_train_steps={self.training_config['max_train_steps']} \\
    --save_every_n_steps={self.training_config['save_every_n_steps']} \\
    --mixed_precision="{self.training_config['mixed_precision']}" \\
    --gradient_accumulation_steps={self.training_config['gradient_accumulation_steps']} \\
    --network_module="networks.lora" \\
    --network_dim=32 \\
    --network_alpha=32 \\
    --optimizer_type="AdamW8bit" \\
    --lr_scheduler="cosine_with_restarts" \\
    --lr_warmup_steps=100 \\
    --noise_offset=0.1 \\
    --adaptive_noise_scale=0.00357 \\
    --multires_noise_iterations=10 \\
    --multires_noise_discount=0.1 \\
    --log_with=tensorboard \\
    --logging_dir="$OUTPUT_DIR/logs" \\
    --enable_bucket \\
    --min_bucket_reso=256 \\
    --max_bucket_reso=2048 \\
    --bucket_reso_steps=64 \\
    --cache_latents \\
    --cache_latents_to_disk \\
    --save_model_as=safetensors \\
    --persistent_data_loader_workers \\
    --max_data_loader_n_workers=8
"""
        
        script_path = self.training_dir / "train_lora.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        script_path.chmod(0o755)
        
        print(f"Kohya training script created: {script_path}")

    def create_generation_pipeline(self):
        """Create asset generation pipeline using the trained LoRA."""
        pipeline_script = f"""#!/usr/bin/env python3
'''
Egyptian-Hades LoRA Asset Generator
Generates consistent game assets using trained LoRA
'''

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from pathlib import Path

class EgyptianHadesAssetGenerator:
    def __init__(self, lora_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load SDXL pipeline
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to(self.device)
        
        # Load our custom LoRA
        self.pipe.load_lora_weights(lora_path)
        
        # Optimize for quality
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        self.pipe.enable_model_cpu_offload()
        
    def generate_card_art(self, card_name, card_desc):
        prompt = f"egyptian_hades_art, {{card_desc}}, trading card art, masterpiece, highly detailed, professional game art"
        
        negative = "low quality, blurry, text, watermark, signature"
        
        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative,
            width=768,
            height=1024,
            num_inference_steps=30,
            guidance_scale=7.5,
            num_images_per_prompt=1
        ).images[0]
        
        return image

# Usage example:
if __name__ == "__main__":
    generator = EgyptianHadesAssetGenerator("path/to/egyptian-hades-gameart-v1.safetensors")
    
    ra_card = generator.generate_card_art(
        "Ra Sun God", 
        "Ra the Egyptian sun god with falcon head and solar disk crown"
    )
    
    ra_card.save("ra_sun_god_lora.png")
"""
        
        pipeline_path = self.training_dir / "lora_asset_generator.py"
        with open(pipeline_path, 'w') as f:
            f.write(pipeline_script)
        
        print(f"Asset generation pipeline created: {pipeline_path}")

    def run_lora_setup(self):
        """Execute complete LoRA training setup."""
        print("=" * 60)
        print("EGYPTIAN-HADES LORA TRAINING SETUP")
        print("Creating custom LoRA for consistent game art")
        print("=" * 60)
        
        # Phase 1: Create dataset structure
        self.create_training_dataset()
        
        # Phase 3: Create training scripts
        self.create_kohya_training_script()
        
        # Phase 6: Create generation pipeline
        self.create_generation_pipeline()
        
        print("=" * 60)
        print("LORA TRAINING SETUP COMPLETE!")
        print("NEXT STEPS:")
        print("1. Collect 50-75 high-quality reference images")
        print("2. Place images in appropriate category folders")
        print("3. Run dataset processing")
        print("4. Execute LoRA training")
        print("5. Generate infinite high-quality assets!")
        print("=" * 60)

def main():
    trainer = EgyptianHadesLoRATrainer()
    trainer.run_lora_setup()

if __name__ == "__main__":
    main()