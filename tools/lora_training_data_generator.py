#!/usr/bin/env python3
"""
LORA TRAINING DATA GENERATOR
===========================

PHASE 4: Generate high-quality training images for Egyptian-Hades LoRA
Creates consistent training dataset using SDXL with professional prompts
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
from PIL import Image
import json

class LoRATrainingDataGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.dataset_dir = Path("../lora_training/training_images")
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # Professional training data specifications
        self.training_specs = {
            "resolution": 1024,
            "inference_steps": 30,
            "guidance_scale": 7.5,
            "images_per_concept": 3,  # Generate 3 variations per concept
        }
        
        # Master style for consistency
        self.base_style = """
        masterpiece, highest quality, professional digital art,
        detailed illustration, sharp focus, rich colors,
        dramatic lighting, painterly style, concept art quality
        """
        
        self.negative_prompt = """
        low quality, blurry, pixelated, artifacts, watermark,
        signature, text overlay, amateur, sketch, dull colors,
        poor composition, distorted, deformed, out of focus
        """

    def setup_pipeline(self):
        """Initialize SDXL pipeline for training data generation."""
        print("PHASE 4: Setting up SDXL Pipeline for Training Data...")
        
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            variant="fp16" if self.device == "cuda" else None,
            use_safetensors=True
        )
        
        self.pipe = self.pipe.to(self.device)
        self.pipe.enable_model_cpu_offload()
        
        print("SDXL Pipeline ready for training data generation!")

    def generate_egyptian_training_data(self):
        """Generate Egyptian art training images."""
        print("Generating Egyptian Art Training Data...")
        
        egyptian_concepts = [
            {
                "name": "anubis_portraits",
                "prompts": [
                    f"{self.base_style}, Anubis Egyptian god portrait, jackal head, black fur, golden collar, amber eyes, divine presence, ancient Egyptian art style",
                    f"{self.base_style}, Anubis deity profile view, noble jackal features, ornate headdress, ceremonial regalia, mystical atmosphere",
                    f"{self.base_style}, Anubis god front facing, majestic jackal head, golden accessories, temple background, Egyptian mythology"
                ]
            },
            {
                "name": "ra_sun_god",
                "prompts": [
                    f"{self.base_style}, Ra Egyptian sun god, falcon head, solar disk crown, golden radiance, divine solar deity, ancient Egyptian art",
                    f"{self.base_style}, Ra sun god portrait, hawk head, blazing solar crown, golden light emanating, powerful divine presence",
                    f"{self.base_style}, Ra deity with solar disk, falcon features, brilliant golden aura, Egyptian temple setting, god of the sun"
                ]
            },
            {
                "name": "egyptian_temples",
                "prompts": [
                    f"{self.base_style}, ancient Egyptian temple interior, massive columns, hieroglyphic carvings, golden light, sacred architecture",
                    f"{self.base_style}, Egyptian temple entrance, colossal statues, carved pillars, dramatic lighting, monumental scale",
                    f"{self.base_style}, temple of the gods, Egyptian architecture, ornate decorations, mystical atmosphere, divine setting"
                ]
            },
            {
                "name": "hieroglyphic_art",
                "prompts": [
                    f"{self.base_style}, Egyptian hieroglyphic wall art, colorful symbols, ancient script, detailed carvings, temple wall",
                    f"{self.base_style}, hieroglyphic inscriptions, Egyptian writing system, ornate symbols, stone carving, ancient text",
                    f"{self.base_style}, Egyptian hieroglyphs, sacred symbols, colorful ancient writing, temple inscriptions, divine text"
                ]
            },
            {
                "name": "egyptian_artifacts",
                "prompts": [
                    f"{self.base_style}, Egyptian golden mask, pharaoh burial mask, ornate metalwork, precious stones, royal artifact",
                    f"{self.base_style}, ancient Egyptian jewelry, golden collar, precious gems, royal accessories, ceremonial ornaments",
                    f"{self.base_style}, Egyptian canopic jars, mummification artifacts, ancient vessels, hieroglyphic decorations"
                ]
            }
        ]
        
        self.generate_concept_images(egyptian_concepts, "egyptian")

    def generate_hades_style_training_data(self):
        """Generate Hades game style training images."""
        print("Generating Hades Art Style Training Data...")
        
        hades_concepts = [
            {
                "name": "character_portraits",
                "prompts": [
                    f"{self.base_style}, Hades game character portrait, dramatic lighting, hand-painted style, Supergiant Games art, dark fantasy",
                    f"{self.base_style}, underworld character design, Greek mythology, painterly illustration, rich colors, character art",
                    f"{self.base_style}, mythological character portrait, detailed facial features, dramatic shadows, fantasy art style"
                ]
            },
            {
                "name": "underworld_environments",
                "prompts": [
                    f"{self.base_style}, underworld environment, dark stone architecture, mystical lighting, Hades game background, otherworldly",
                    f"{self.base_style}, Greek underworld setting, shadowy chambers, ethereal glow, architectural details, mythological realm",
                    f"{self.base_style}, underworld palace interior, grand columns, mystical atmosphere, dark fantasy architecture"
                ]
            },
            {
                "name": "ui_elements",
                "prompts": [
                    f"{self.base_style}, fantasy game UI frame, ornate border design, dark colors, golden accents, Hades interface style",
                    f"{self.base_style}, game interface element, decorative frame, mythological motifs, elegant design, premium UI",
                    f"{self.base_style}, fantasy card frame, ornate border, dark theme, golden highlights, game interface design"
                ]
            }
        ]
        
        self.generate_concept_images(hades_concepts, "hades")

    def generate_card_game_training_data(self):
        """Generate card game style training images.""" 
        print("Generating Card Game Art Training Data...")
        
        card_concepts = [
            {
                "name": "fantasy_cards",
                "prompts": [
                    f"{self.base_style}, fantasy trading card art, magical creature, detailed illustration, card game artwork, premium quality",
                    f"{self.base_style}, mythological card art, legendary character, trading card illustration, fantasy artwork",
                    f"{self.base_style}, fantasy card portrait, magical being, detailed character art, card game design, epic quality"
                ]
            },
            {
                "name": "card_frames", 
                "prompts": [
                    f"{self.base_style}, ornate card frame, golden border, decorative elements, luxury card design, elegant frame",
                    f"{self.base_style}, fantasy card border, mystical frame design, ornate decorations, premium card template",
                    f"{self.base_style}, legendary card frame, golden ornate border, magical design elements, high-end card style"
                ]
            }
        ]
        
        self.generate_concept_images(card_concepts, "card_game")

    def generate_concept_images(self, concepts, category):
        """Generate images for a category of concepts."""
        category_dir = self.dataset_dir / category
        category_dir.mkdir(exist_ok=True)
        
        for concept in concepts:
            concept_dir = category_dir / concept["name"]
            concept_dir.mkdir(exist_ok=True)
            
            for i, prompt in enumerate(concept["prompts"]):
                print(f"Generating {category}/{concept['name']}/image_{i+1}...")
                
                try:
                    image = self.pipe(
                        prompt=prompt,
                        negative_prompt=self.negative_prompt,
                        width=self.training_specs["resolution"],
                        height=self.training_specs["resolution"],
                        num_inference_steps=self.training_specs["inference_steps"],
                        guidance_scale=self.training_specs["guidance_scale"],
                        generator=torch.Generator(device=self.device).manual_seed(42 + i)
                    ).images[0]
                    
                    # Save image
                    image_path = concept_dir / f"{concept['name']}_{i+1:02d}.jpg"
                    image.save(image_path, "JPEG", quality=95)
                    
                    # Create caption file for LoRA training
                    caption_path = concept_dir / f"{concept['name']}_{i+1:02d}.txt"
                    caption = self.create_training_caption(category, concept["name"], prompt)
                    with open(caption_path, 'w') as f:
                        f.write(caption)
                    
                    print(f"Saved: {image_path}")
                    time.sleep(2)  # Prevent overheating
                    
                except Exception as e:
                    print(f"Error generating {concept['name']} image {i+1}: {e}")

    def create_training_caption(self, category, concept_name, original_prompt):
        """Create LoRA training caption."""
        # Our trigger word
        caption = "egyptian_hades_art, "
        
        # Add category-specific tags
        if category == "egyptian":
            caption += "ancient egyptian art, "
            if "anubis" in concept_name:
                caption += "anubis egyptian god, jackal head, "
            elif "ra" in concept_name:
                caption += "ra sun god, falcon head, solar disk, "
            elif "temple" in concept_name:
                caption += "egyptian temple, ancient architecture, "
            elif "hieroglyphic" in concept_name:
                caption += "hieroglyphs, egyptian writing, ancient symbols, "
        elif category == "hades":
            caption += "hades game style, supergiant games art, "
            if "character" in concept_name:
                caption += "character portrait, "
            elif "environment" in concept_name:
                caption += "underworld environment, "
            elif "ui" in concept_name:
                caption += "game interface, "
        elif category == "card_game":
            caption += "fantasy card art, trading card design, "
        
        # Common quality tags
        caption += "masterpiece, high quality, detailed illustration, professional game art"
        
        return caption

    def prepare_for_lora_training(self):
        """Organize generated images for LoRA training."""
        print("Preparing dataset for LoRA training...")
        
        # Create final training directory
        final_dir = self.dataset_dir.parent / "final_training_data"
        final_dir.mkdir(exist_ok=True)
        
        image_count = 0
        
        # Copy all images to final directory with proper naming
        for category_dir in self.dataset_dir.iterdir():
            if category_dir.is_dir():
                for concept_dir in category_dir.iterdir():
                    if concept_dir.is_dir():
                        for img_file in concept_dir.glob("*.jpg"):
                            if img_file.is_file():
                                # Copy image
                                final_img_path = final_dir / f"train_{image_count:04d}.jpg"
                                img_file.rename(final_img_path)
                                
                                # Copy caption
                                caption_file = img_file.with_suffix('.txt')
                                if caption_file.exists():
                                    final_caption_path = final_dir / f"train_{image_count:04d}.txt"
                                    caption_file.rename(final_caption_path)
                                
                                image_count += 1
        
        print(f"Prepared {image_count} training images in {final_dir}")
        
        # Update training config
        config = {
            "model_name": "egyptian-hades-gameart-v1",
            "dataset_path": str(final_dir),
            "num_images": image_count,
            "trigger_word": "egyptian_hades_art",
            "resolution": self.training_specs["resolution"]
        }
        
        config_path = final_dir.parent / "training_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Training configuration saved: {config_path}")

    def run_training_data_generation(self):
        """Execute PHASE 4: Training Data Generation."""
        print("=" * 60)
        print("PHASE 4: LORA TRAINING DATA GENERATION")
        print("Creating high-quality training dataset")
        print("=" * 60)
        
        # Setup pipeline
        self.setup_pipeline()
        
        # Generate training images
        self.generate_egyptian_training_data()
        self.generate_hades_style_training_data()
        self.generate_card_game_training_data()
        
        # Prepare for training
        self.prepare_for_lora_training()
        
        print("=" * 60)
        print("PHASE 4 COMPLETE: TRAINING DATA GENERATED!")
        print("Ready for LoRA training with Kohya_ss")
        print("Next: Execute train_lora.sh script")
        print("=" * 60)

def main():
    generator = LoRATrainingDataGenerator()
    generator.run_training_data_generation()

if __name__ == "__main__":
    main()