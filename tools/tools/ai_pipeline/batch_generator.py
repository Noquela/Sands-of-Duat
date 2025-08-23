#!/usr/bin/env python3
"""
Batch Generation Script for Hades-Quality Egyptian Characters
Uses ComfyUI API for automated, consistent art production
"""

import requests
import json
import time
import uuid
from pathlib import Path

class HadesArtBatchGenerator:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"
        self.output_dir = Path("tools/ai_pipeline/outputs/characters")
        
    def generate_character_variations(self, character_name, base_prompt, count=4):
        """Generate multiple variations of a character"""
        print(f"Generating {count} variations for {character_name}...")
        
        # Character-specific prompt additions
        character_prompts = {
            "pharaoh_hero": "pharaoh warrior, golden armor, khopesh sword, royal headdress, confident pose",
            "anubis_boss": "Anubis jackal god, powerful muscular build, ornate armor, intimidating pose, glowing eyes",
            "mummy_enemy": "ancient mummy warrior, wrapped bandages, glowing green eyes, desert tomb guardian",
            "isis_npc": "Isis goddess, elegant flowing robes, golden jewelry, graceful pose, divine aura"
        }
        
        specific_prompt = character_prompts.get(character_name, "Egyptian mythology character")
        full_prompt = f"{base_prompt}, {specific_prompt}"
        
        variations = []
        for i in range(count):
            # Add variation elements
            seed = hash(f"{character_name}_{i}") % 1000000
            variation_prompt = f"{full_prompt}, variation {i+1}, seed {seed}"
            
            result = self.generate_single_image(variation_prompt, seed)
            if result:
                variations.append(result)
                print(f"  Generated variation {i+1}")
            else:
                print(f"  Failed variation {i+1}")
        
        return variations
    
    def generate_single_image(self, prompt, seed):
        """Generate a single image using ComfyUI API"""
        # Load workflow template
        workflow_path = Path("tools/ai_pipeline/workflows/hades_character_generation.json")
        with open(workflow_path) as f:
            workflow = json.load(f)
        
        # Update workflow with prompt and seed
        workflow["nodes"]["2"]["inputs"]["text"] = prompt
        workflow["nodes"]["5"]["inputs"]["seed"] = seed
        
        # Send generation request
        try:
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Connection Error: {e}")
            return None

def main():
    generator = HadesArtBatchGenerator()
    
    # Base prompt for Hades-style quality
    base_prompt = """masterpiece, best quality, highly detailed, professional game art, 
                     Hades game art style, dramatic cinematic lighting, hand-painted texture, 
                     stylized proportions, rich saturated colors, ornate Egyptian details, 
                     dynamic pose, character portrait, 4K resolution"""
    
    characters = ["pharaoh_hero", "anubis_boss", "mummy_enemy", "isis_npc"]
    
    for character in characters:
        variations = generator.generate_character_variations(character, base_prompt)
        print(f"Generated {len(variations)} variations for {character}")

if __name__ == "__main__":
    main()
