#!/usr/bin/env python3
"""
SANDS OF DUAT - AI Asset Generator
Egyptian-themed asset generation pipeline using ComfyUI and Stable Diffusion

This script automates the generation of high-quality Egyptian-themed assets
for the Sands of Duat roguelike game using AI image generation.
"""

import os
import sys
import json
import requests
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import base64
from PIL import Image
from io import BytesIO

class EgyptianAssetGenerator:
    """AI-powered asset generator for Egyptian-themed game assets."""
    
    def __init__(self, comfyui_url: str = "http://127.0.0.1:8188"):
        """
        Initialize the asset generator.
        
        Args:
            comfyui_url: URL of the running ComfyUI server
        """
        self.comfyui_url = comfyui_url
        self.output_dir = Path("../ai_generated")
        self.workflows_dir = Path("workflows")
        
        # Ensure directories exist
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "sprites").mkdir(exist_ok=True)
        (self.output_dir / "backgrounds").mkdir(exist_ok=True)
        (self.output_dir / "ui").mkdir(exist_ok=True)
        (self.output_dir / "cards").mkdir(exist_ok=True)
        (self.output_dir / "characters").mkdir(exist_ok=True)
        
        self.workflows_dir.mkdir(exist_ok=True)
        
        # Egyptian-themed prompts
        self.base_prompts = {
            "style": "ancient egyptian art, papyrus texture, hieroglyphic border, golden accents, sandstone colors, detailed lineart, game asset style",
            "negative": "modern, contemporary, realistic photo, blurry, low quality, watermark, signature, text, letters",
            "quality": "masterpiece, best quality, highly detailed, sharp focus, vibrant colors"
        }
        
        # Asset type configurations
        self.asset_configs = {
            "character": {
                "size": (512, 512),
                "style_boost": "character design, full body, standing pose, game sprite, pixel perfect",
                "entities": [
                    "egyptian pharaoh warrior",
                    "anubis god of death", 
                    "isis goddess of magic",
                    "ra sun god",
                    "set god of chaos",
                    "mummy guardian",
                    "sphinx guardian",
                    "egyptian priest",
                    "scarab beetle monster",
                    "cobra snake enemy"
                ]
            },
            "background": {
                "size": (1920, 1080),
                "style_boost": "environment art, wide shot, atmospheric lighting, desert landscape",
                "entities": [
                    "pyramid complex at sunset",
                    "ancient egyptian temple interior",
                    "tomb chamber with treasures",
                    "desert oasis with palm trees",
                    "underworld river styx",
                    "pharaoh's throne room",
                    "library of alexandria",
                    "cairo marketplace",
                    "sphinx temple ruins",
                    "nile river valley"
                ]
            },
            "ui_element": {
                "size": (256, 256),
                "style_boost": "UI icon, game interface, clean design, centered composition",
                "entities": [
                    "ankh life symbol",
                    "scarab health orb",
                    "eye of horus mana crystal",
                    "golden egyptian frame",
                    "papyrus scroll background",
                    "hieroglyphic button design",
                    "cobra energy bar",
                    "pyramid progress indicator",
                    "egyptian coin currency",
                    "canopic jar container"
                ]
            },
            "weapon": {
                "size": (512, 256),
                "style_boost": "weapon design, detailed metalwork, magical glow, game item",
                "entities": [
                    "pharaoh's golden scepter",
                    "anubis ceremonial dagger",
                    "isis magic staff",
                    "ra's solar spear",
                    "egyptian khopesh sword",
                    "mummy wrapping whip",
                    "scarab shield",
                    "hieroglyphic bow",
                    "cobra venom blade",
                    "pyramid hammer"
                ]
            }
        }
    
    def check_comfyui_connection(self) -> bool:
        """Check if ComfyUI server is running and accessible."""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def create_workflow(self, asset_type: str, prompt: str, size: Tuple[int, int]) -> Dict:
        """
        Create a ComfyUI workflow for asset generation.
        
        Args:
            asset_type: Type of asset to generate
            prompt: Description of the asset
            size: Image dimensions (width, height)
            
        Returns:
            ComfyUI workflow dictionary
        """
        config = self.asset_configs.get(asset_type, self.asset_configs["character"])
        
        # Build complete prompt
        full_prompt = f"{prompt}, {config['style_boost']}, {self.base_prompts['style']}, {self.base_prompts['quality']}"
        
        workflow = {
            "1": {
                "inputs": {
                    "seed": -1,
                    "steps": 25,
                    "cfg": 7.5,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "2": {
                "inputs": {
                    "samples": ["1", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "3": {
                "inputs": {
                    "filename_prefix": f"sands_of_duat_{asset_type}",
                    "images": ["2", 0]
                },
                "class_type": "SaveImage"
            },
            "4": {
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": size[0],
                    "height": size[1],
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": full_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": self.base_prompts['negative'],
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            }
        }
        
        return workflow
    
    def queue_workflow(self, workflow: Dict) -> Optional[str]:
        """
        Queue a workflow in ComfyUI.
        
        Args:
            workflow: The workflow to execute
            
        Returns:
            Prompt ID if successful, None otherwise
        """
        try:
            response = requests.post(f"{self.comfyui_url}/prompt", json={"prompt": workflow})
            if response.status_code == 200:
                result = response.json()
                return result.get("prompt_id")
        except requests.exceptions.RequestException as e:
            print(f"Error queuing workflow: {e}")
        return None
    
    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> bool:
        """
        Wait for a queued workflow to complete.
        
        Args:
            prompt_id: ID of the queued prompt
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if completed successfully, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check queue status
                response = requests.get(f"{self.comfyui_url}/queue")
                if response.status_code == 200:
                    queue_data = response.json()
                    
                    # Check if our prompt is still in queue
                    queue_remaining = queue_data.get("queue_remaining", [])
                    queue_running = queue_data.get("queue_running", [])
                    
                    prompt_in_queue = any(item[1] == prompt_id for item in queue_remaining + queue_running)
                    
                    if not prompt_in_queue:
                        # Prompt completed
                        return True
                
                time.sleep(2)
                
            except requests.exceptions.RequestException:
                time.sleep(5)
        
        return False
    
    def generate_asset(self, asset_type: str, entity_name: str, custom_prompt: Optional[str] = None) -> bool:
        """
        Generate a single asset.
        
        Args:
            asset_type: Type of asset (character, background, ui_element, weapon)
            entity_name: Name of the entity to generate
            custom_prompt: Optional custom prompt override
            
        Returns:
            True if generation was successful
        """
        if not self.check_comfyui_connection():
            print("❌ ComfyUI server is not running! Please start ComfyUI first.")
            return False
        
        config = self.asset_configs.get(asset_type)
        if not config:
            print(f"❌ Unknown asset type: {asset_type}")
            return False
        
        prompt = custom_prompt or entity_name
        workflow = self.create_workflow(asset_type, prompt, config["size"])
        
        print(f"🎨 Generating {asset_type}: {entity_name}")
        print(f"   Prompt: {prompt}")
        print(f"   Size: {config['size']}")
        
        prompt_id = self.queue_workflow(workflow)
        if not prompt_id:
            print("❌ Failed to queue workflow")
            return False
        
        print(f"   Queued with ID: {prompt_id}")
        print("   Waiting for generation to complete...")
        
        if self.wait_for_completion(prompt_id):
            print("✅ Generation completed!")
            return True
        else:
            print("❌ Generation timed out")
            return False
    
    def generate_batch(self, asset_type: str, count: Optional[int] = None) -> int:
        """
        Generate multiple assets of the same type.
        
        Args:
            asset_type: Type of assets to generate
            count: Number of assets to generate (None = all available)
            
        Returns:
            Number of successfully generated assets
        """
        config = self.asset_configs.get(asset_type)
        if not config:
            print(f"❌ Unknown asset type: {asset_type}")
            return 0
        
        entities = config["entities"]
        if count:
            entities = entities[:count]
        
        print(f"🏭 Starting batch generation of {len(entities)} {asset_type} assets...")
        
        successful = 0
        for i, entity in enumerate(entities, 1):
            print(f"\n📊 Progress: {i}/{len(entities)}")
            if self.generate_asset(asset_type, entity):
                successful += 1
            else:
                print(f"⚠️ Failed to generate: {entity}")
            
            # Small delay between generations
            time.sleep(1)
        
        print(f"\n🎉 Batch complete! {successful}/{len(entities)} assets generated successfully.")
        return successful
    
    def generate_complete_set(self) -> Dict[str, int]:
        """
        Generate a complete set of assets for the game.
        
        Returns:
            Dictionary with results for each asset type
        """
        print("🚀 Starting complete asset generation for Sands of Duat...")
        print("=" * 60)
        
        results = {}
        asset_types = ["character", "ui_element", "weapon", "background"]
        
        for asset_type in asset_types:
            print(f"\n🎨 Generating {asset_type} assets...")
            results[asset_type] = self.generate_batch(asset_type, count=5)  # Generate 5 of each type
        
        print("\n" + "=" * 60)
        print("🎊 COMPLETE ASSET GENERATION FINISHED!")
        print("\nResults:")
        for asset_type, count in results.items():
            print(f"  {asset_type}: {count} assets")
        
        total = sum(results.values())
        print(f"\nTotal assets generated: {total}")
        
        return results


def main():
    """Main CLI interface for the asset generator."""
    parser = argparse.ArgumentParser(description="Sands of Duat AI Asset Generator")
    
    parser.add_argument("--url", default="http://127.0.0.1:8188", 
                       help="ComfyUI server URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Single asset generation
    single_parser = subparsers.add_parser("generate", help="Generate a single asset")
    single_parser.add_argument("asset_type", choices=["character", "background", "ui_element", "weapon"],
                              help="Type of asset to generate")
    single_parser.add_argument("name", help="Name/description of the asset")
    single_parser.add_argument("--prompt", help="Custom prompt override")
    
    # Batch generation
    batch_parser = subparsers.add_parser("batch", help="Generate multiple assets of one type")
    batch_parser.add_argument("asset_type", choices=["character", "background", "ui_element", "weapon"],
                             help="Type of assets to generate")
    batch_parser.add_argument("--count", type=int, help="Number of assets to generate")
    
    # Complete set generation
    subparsers.add_parser("all", help="Generate complete asset set for the game")
    
    # Test connection
    subparsers.add_parser("test", help="Test ComfyUI connection")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    generator = EgyptianAssetGenerator(args.url)
    
    if args.command == "test":
        if generator.check_comfyui_connection():
            print("✅ ComfyUI connection successful!")
        else:
            print("❌ Cannot connect to ComfyUI. Make sure it's running at", args.url)
    
    elif args.command == "generate":
        generator.generate_asset(args.asset_type, args.name, args.prompt)
    
    elif args.command == "batch":
        generator.generate_batch(args.asset_type, args.count)
    
    elif args.command == "all":
        generator.generate_complete_set()


if __name__ == "__main__":
    main()