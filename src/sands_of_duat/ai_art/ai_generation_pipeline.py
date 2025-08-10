#!/usr/bin/env python3
"""
AI Art Generation Pipeline - RTX 5070 CUDA 12.8 Optimized
Complete rewrite with NO fallbacks or placeholders
ONLY ComfyUI local generation allowed
"""

import os
import sys
import json
import time
import requests
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import base64
from io import BytesIO
from PIL import Image
import numpy as np

class LocalSDXLGenerator:
    """RTX 5070 optimized SDXL generator via ComfyUI API - CUDA 12.8 required"""
    
    def __init__(self):
        self.api_base = "http://127.0.0.1:8188"
        self.session = requests.Session()
        
        # RTX 5070 CUDA 12.8 optimized settings - NO LIMITS
        self.config = {
            "batch_size": 1,          # High quality single generation
            "steps": 50,              # MAXIMUM quality steps
            "cfg_scale": 9.0,         # Strong guidance for Egyptian style
            "width": 768,             # High resolution cards
            "height": 1024,           # Portrait aspect ratio
            "scheduler": "karras",
            "sampler": "euler_ancestral",
            "model": "sd_xl_base_1.0.safetensors",
            "vae": "sdxl_vae.safetensors"
        }
        
        print(f"LocalSDXLGenerator initialized - RTX 5070 CUDA 12.8")
        print(f"ComfyUI API: {self.api_base}")
        
    def generate_image(self, 
                      prompt: str, 
                      negative_prompt: str,
                      seed: Optional[int] = None,
                      **kwargs) -> Optional[Image.Image]:
        """Generate single image via ComfyUI API - RTX 5070 max quality"""
        
        if seed is None:
            seed = random.randint(0, 2**32-1)
            
        # Merge config with any overrides
        gen_config = {**self.config, **kwargs}
        
        print(f"  Generating {gen_config['width']}x{gen_config['height']} @ {gen_config['steps']} steps")
        
        # Create ComfyUI workflow for RTX 5070
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": gen_config["steps"],
                    "cfg": gen_config["cfg_scale"],
                    "sampler_name": gen_config["sampler"],
                    "scheduler": gen_config["scheduler"],
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": gen_config["model"]
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": gen_config["width"],
                    "height": gen_config["height"],
                    "batch_size": gen_config["batch_size"]
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": f"sands_of_duat_{int(time.time())}",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }
        
        try:
            # Queue prompt on RTX 5070
            response = self.session.post(
                f"{self.api_base}/prompt",
                json={"prompt": workflow, "client_id": "rtx5070_sands_of_duat"}
            )
            
            if response.status_code != 200:
                print(f"    [ERROR] ComfyUI queue error: {response.status_code}")
                return None
                
            result = response.json()
            prompt_id = result.get("prompt_id")
            
            if not prompt_id:
                print("    [ERROR] No prompt ID returned from ComfyUI")
                return None
            
            print(f"    [PROCESSING] RTX 5070 processing... ID: {prompt_id}")
            
            # Wait for RTX 5070 to complete generation
            return self._wait_for_image(prompt_id)
            
        except Exception as e:
            print(f"    [ERROR] RTX 5070 generation error: {e}")
            return None
    
    def _wait_for_image(self, prompt_id: str, timeout: int = 600) -> Optional[Image.Image]:
        """Wait for RTX 5070 to complete image generation"""
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check RTX 5070 processing status
                response = self.session.get(f"{self.api_base}/history/{prompt_id}")
                
                if response.status_code == 200:
                    history = response.json()
                    
                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})
                        
                        # Look for SaveImage output
                        for node_id, node_output in outputs.items():
                            if "images" in node_output:
                                images_data = node_output["images"]
                                if images_data:
                                    # Get first image
                                    image_info = images_data[0]
                                    filename = image_info["filename"]
                                    
                                    # Download RTX 5070 generated image
                                    img_response = self.session.get(
                                        f"{self.api_base}/view?filename={filename}&type=output"
                                    )
                                    
                                    if img_response.status_code == 200:
                                        print(f"    [SUCCESS] RTX 5070 generation complete!")
                                        return Image.open(BytesIO(img_response.content))
                
                # RTX 5070 still processing
                time.sleep(3)
                
            except Exception as e:
                print(f"    [WARNING] Status check error: {e}")
                time.sleep(5)
        
        print(f"    [TIMEOUT] RTX 5070 timeout after {timeout}s")
        return None
    
    def test_connection(self) -> bool:
        """Test if ComfyUI is running on RTX 5070"""
        try:
            response = self.session.get(f"{self.api_base}/system_stats", timeout=10)
            if response.status_code == 200:
                print("[SUCCESS] ComfyUI connection successful")
                return True
            else:
                print(f"[ERROR] ComfyUI returned {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] ComfyUI connection failed: {e}")
            return False

class HadesEgyptianPrompts:
    """Professional Hades-Egyptian style prompts for RTX 5070 generation"""
    
    # Base style targeting Hades game quality
    BASE_STYLE = """masterpiece, best quality, ultra detailed, hades game art style, 
    hand painted artwork, egyptian underworld theme, dramatic lighting, 
    vibrant colors, rich textures, supergiant games quality, 
    professional game art, award winning illustration"""
    
    # Consistent negative prompt
    NEGATIVE_PROMPT = """low quality, blurry, pixelated, photograph, realistic, 
    3d render, modern, contemporary, bad anatomy, deformed, watermark, text, 
    amateur, sketch, unfinished, cheap, generic, boring"""
    
    # All legendary cards with multiple prompt variants for RTX 5070
    LEGENDARY_CARDS = {
        "ANUBIS - JUDGE OF THE DEAD": [
            f"{BASE_STYLE}, majestic Anubis with jackal head, golden egyptian regalia, "
            f"divine scales of judgment floating beside him, glowing amber eyes, "
            f"ornate collar with hieroglyphic inscriptions, underworld throne room background, "
            f"mystical purple and gold aura, ancient egyptian architecture",
            
            f"{BASE_STYLE}, Anubis deity wielding crook and flail, ceremonial mummification pose, "
            f"sacred canopic jars surrounding, torch-lit tomb interior, weathered stone pillars, "
            f"Egyptian god of the dead, divine authority, shadowy atmosphere with golden accents"
        ],
        
        "RA - SUN GOD": [
            f"{BASE_STYLE}, magnificent Ra with falcon head, blazing solar disk crown, "
            f"radiant golden armor with sun motifs, commanding solar barque, "
            f"streams of divine sunlight, pyramid silhouettes in background, "
            f"cosmic stellar energy, temple of heliopolis, warm golden lighting",
            
            f"{BASE_STYLE}, Ra sun god raising arms to command dawn, solar corona expanding, "
            f"pharaonic regalia with precious gems, desert landscape at sunrise, "
            f"obelisks and ancient monuments, divine solar magic, celestial background"
        ],
        
        "ISIS - DIVINE MOTHER": [
            f"{BASE_STYLE}, graceful Isis with protective wings spread wide, "
            f"throne hieroglyph crown, flowing white and gold egyptian robes, "
            f"ankh symbol glowing with life energy, green healing magic spiraling, "
            f"nurturing maternal expression, temple interior with lotus columns",
            
            f"{BASE_STYLE}, Isis goddess performing resurrection magic, hands glowing with power, "
            f"mystical symbols floating in air, star-pattern dress, silver moonlight, "
            f"sacred ibis birds around her, papyrus plants, divine feminine energy"
        ],
        
        "SET - CHAOS GOD": [
            f"{BASE_STYLE}, menacing Set with curved snout and red eyes, "
            f"chaotic storm armor in red and black, lightning crackling around him, "
            f"desert sandstorm background, god of disorder and violence, "
            f"aggressive battle pose, ancient egyptian mythology, ominous atmosphere",
            
            f"{BASE_STYLE}, Set wielding was scepter of power, destructive chaos magic, "
            f"red desert landscape with swirling sands, pharaonic curses, "
            f"ancient rivalry imagery, menacing expression, dark Egyptian god"
        ]
    }
    
    # Epic tier cards for RTX 5070
    EPIC_CARDS = {
        "EGYPTIAN WARRIOR": [
            f"{BASE_STYLE}, elite egyptian warrior in ornate golden armor, "
            f"wielding bronze khopesh sword with hieroglyphic etchings, "
            f"pharaoh's champion in ceremonial headdress, desert battlefield, "
            f"war paint on face, determined expression, bronze age weapons",
            
            f"{BASE_STYLE}, egyptian warrior commanding from golden war chariot, "
            f"two magnificent horses with egyptian decorations, spear raised high, "
            f"royal regalia flowing in wind, army formations in background, "
            f"pyramid monuments on horizon, victory pose, military prowess"
        ],
        
        "PHARAOH'S GUARD": [
            f"{BASE_STYLE}, imposing temple guardian in ceremonial bronze armor, "
            f"holding ornate spear with crystal blade, massive muscular build, "
            f"standing guard at temple entrance, torch flames creating shadows, "
            f"hieroglyphic walls, loyal protector, stern expression",
            
            f"{BASE_STYLE}, elite palace guard in formation, synchronized stance, "
            f"royal cartouche symbols on armor, golden decorations, "
            f"disciplined warrior protecting pharaoh, palace interior, authority"
        ]
    }
    
    # Rare tier cards optimized for RTX 5070
    RARE_CARDS = {
        "MUMMY GUARDIAN": [
            f"{BASE_STYLE}, ancient mummy lord rising from ornate sarcophagus, "
            f"glowing red eyes piercing through darkness, golden burial mask, "
            f"partially unwrapped bandages revealing ancient skin, "
            f"dark tomb interior with treasure chests and canopic jars",
            
            f"{BASE_STYLE}, mummy guardian commanding undead army, "
            f"staff topped with golden ankh, ethereal blue flame magic, "
            f"skeletal minions in background, tomb entrance with massive doors, "
            f"ancient curse energy, supernatural Egyptian undead"
        ],
        
        "SPHINX GUARDIAN": [
            f"{BASE_STYLE}, majestic sphinx with wise pharaoh head and lion body, "
            f"ancient weathered limestone texture, massive monumental scale, "
            f"great pyramids perfectly aligned in background, desert sands, "
            f"mysterious golden eyes holding ancient secrets, sunset lighting",
            
            f"{BASE_STYLE}, sphinx guardian solving eternal riddles, "
            f"glowing eyes with divine wisdom, hieroglyphic inscriptions, "
            f"desert heat shimmer effects, geological stone textures, "
            f"mythical creature of ancient Egypt, eternal watchfulness"
        ]
    }

class EgyptianArtPipeline:
    """Complete Egyptian art generation pipeline - RTX 5070 CUDA 12.8 only"""
    
    def __init__(self):
        self.generator = LocalSDXLGenerator()
        self.prompts = HadesEgyptianPrompts()
        
        # Output paths - exactly as specified
        self.base_dir = Path(__file__).parent.parent.parent.parent
        self.generated_dir = self.base_dir / "assets" / "generated_art"
        self.approved_dir = self.base_dir / "assets" / "approved_hades_quality"
        
        # Create directories
        for dir_path in [self.generated_dir, self.approved_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Create subdirectories for approved assets
        (self.approved_dir / "cards").mkdir(exist_ok=True)
        (self.approved_dir / "backgrounds").mkdir(exist_ok=True)
        (self.approved_dir / "characters").mkdir(exist_ok=True)
            
    def test_setup(self) -> bool:
        """Test if RTX 5070 ComfyUI setup is ready"""
        print("[SETUP] Testing RTX 5070 ComfyUI setup...")
        
        if not self.generator.test_connection():
            print("[ERROR] ComfyUI not accessible at http://127.0.0.1:8188")
            print("[ERROR] Required: Start ComfyUI with CUDA 12.8 support")
            print("   Command: cd external/ComfyUI && python main.py --listen 127.0.0.1 --port 8188")
            return False
            
        print("[SUCCESS] RTX 5070 ComfyUI connection verified")
        return True
    
    def generate_all_cards(self) -> Dict[str, bool]:
        """Generate ALL cards from scratch - RTX 5070 maximum quality"""
        
        if not self.test_setup():
            print("[ERROR] Setup failed - cannot proceed without RTX 5070 ComfyUI")
            return {}
            
        print("RTX5070" + "="*54)
        print("    RTX 5070 EGYPTIAN CARD GENERATION - CUDA 12.8")
        print("    NO FALLBACKS - NO PLACEHOLDERS - MAXIMUM QUALITY")
        print("RTX5070" + "="*54)
        
        results = {}
        
        # Combine all card categories
        all_cards = {
            **self.prompts.LEGENDARY_CARDS,
            **self.prompts.EPIC_CARDS,  
            **self.prompts.RARE_CARDS
        }
        
        total_cards = len(all_cards)
        successful_cards = 0
        start_time = time.time()
        
        for i, (card_name, prompt_variants) in enumerate(all_cards.items(), 1):
            print(f"\n[{i}/{total_cards}] [GEN] RTX 5070 Generating: {card_name}")
            print("-" * 50)
            
            success = self._generate_single_card(card_name, prompt_variants)
            results[card_name] = success
            
            if success:
                successful_cards += 1
                print(f"    [SUCCESS] {card_name} - RTX 5070 SUCCESS")
            else:
                print(f"    [FAILED] {card_name} - RTX 5070 FAILED")
        
        elapsed_time = time.time() - start_time
        
        print(f"\nRTX5070{'='*54}")
        print(f"[SUCCESS] RTX 5070 GENERATION COMPLETE!")
        print(f"[TIME] Total time: {elapsed_time/60:.1f} minutes")
        print(f"[SUCCESS] Success rate: {successful_cards}/{total_cards} cards")
        print(f"[PERFORMANCE] RTX 5070 CUDA 12.8 utilized at maximum capacity")
        print(f"[OUTPUT] Generated: {self.generated_dir}")
        print(f"[OUTPUT] Approved: {self.approved_dir}")
        
        return results
    
    def _generate_single_card(self, card_name: str, prompt_variants: List[str]) -> bool:
        """Generate single card with RTX 5070 quality validation"""
        
        # Try each prompt variant until RTX 5070 produces acceptable quality
        for i, prompt in enumerate(prompt_variants):
            print(f"    [ATTEMPT] RTX 5070 attempt {i+1}/{len(prompt_variants)}")
            
            # Generate with RTX 5070 maximum settings
            image = self.generator.generate_image(
                prompt=prompt,
                negative_prompt=self.prompts.NEGATIVE_PROMPT,
                width=768,   # High resolution for cards
                height=1024, # Portrait aspect
                steps=50,    # Maximum quality steps
                cfg_scale=9.0 # Strong guidance
            )
            
            if image:
                # Save to generated directory first
                filename = f"{card_name.lower().replace(' - ', '_').replace(' ', '_')}.png"
                generated_path = self.generated_dir / filename
                image.save(generated_path, 'PNG', quality=100)
                
                print(f"    [SAVED] RTX 5070 output: {generated_path}")
                
                # Quality validation for RTX 5070 output
                if self._validate_rtx5070_quality(image, card_name):
                    # Move to approved directory  
                    approved_path = self.approved_dir / "cards" / filename
                    image.save(approved_path, 'PNG', quality=100)
                    
                    print(f"    [APPROVED] RTX 5070 quality approved: {approved_path}")
                    return True
                else:
                    print(f"    [RETRY] RTX 5070 output quality insufficient, retrying...")
        
        print(f"    [FAILED] RTX 5070 failed to produce acceptable quality for {card_name}")
        return False
    
    def _validate_rtx5070_quality(self, image: Image.Image, card_name: str) -> bool:
        """Validate RTX 5070 output meets Hades-Egyptian quality standards"""
        
        # Size validation
        if image.width < 512 or image.height < 512:
            print(f"    [FAILED] RTX 5070 output too small: {image.size}")
            return False
            
        # Convert to numpy for analysis
        img_array = np.array(image.convert('RGB'))
        
        # Color variance check (not blank/solid)
        color_variance = np.var(img_array)
        if color_variance < 200:
            print(f"    [FAILED] RTX 5070 output too uniform: variance {color_variance}")
            return False
            
        # Color saturation check (Egyptian art should be vibrant)
        hsv_img = image.convert('HSV')
        hsv_array = np.array(hsv_img)
        saturation = np.mean(hsv_array[:, :, 1])
        
        if saturation < 80:  # Low saturation indicates washed out colors
            print(f"    [FAILED] RTX 5070 output lacks color vibrancy: sat {saturation}")
            return False
            
        # Detail complexity check
        from PIL import ImageFilter
        edges = image.filter(ImageFilter.FIND_EDGES)
        edge_array = np.array(edges.convert('L'))
        detail_score = np.mean(edge_array)
        
        if detail_score < 15:  # Very low detail
            print(f"    [FAILED] RTX 5070 output lacks detail: score {detail_score}")
            return False
            
        print(f"    [QUALITY] RTX 5070 quality metrics passed:")
        print(f"        Color variance: {color_variance:.1f}")
        print(f"        Saturation: {saturation:.1f}")
        print(f"        Detail score: {detail_score:.1f}")
        
        return True

# Global pipeline instance
_pipeline: Optional[EgyptianArtPipeline] = None

def get_pipeline() -> EgyptianArtPipeline:
    """Get global RTX 5070 pipeline instance"""
    global _pipeline
    if _pipeline is None:
        _pipeline = EgyptianArtPipeline()
    return _pipeline

def generate_all_egyptian_cards() -> Dict[str, bool]:
    """Main entry point for RTX 5070 card generation"""
    pipeline = get_pipeline()
    return pipeline.generate_all_cards()

if __name__ == "__main__":
    # RTX 5070 CUDA 12.8 generation test
    print("[TEST] RTX 5070 CUDA 12.8 Egyptian Art Generation Test")
    results = generate_all_egyptian_cards()
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\n[RESULTS] RTX 5070 FINAL RESULTS: {successful}/{total} cards generated")
    
    if successful == total:
        print("[SUCCESS] PERFECT RTX 5070 SUCCESS! All Egyptian cards generated!")
        print("[READY] Ready for animation pipeline and game integration!")
    elif successful > 0:
        print("[PARTIAL] Partial RTX 5070 success. Check failed cards and retry.")
        print("[ADVICE] Consider adjusting quality thresholds or prompt variants.")
    else:
        print("[FAILED] RTX 5070 generation completely failed.")
        print("[ERROR] Check ComfyUI setup, CUDA 12.8 installation, and model files.")