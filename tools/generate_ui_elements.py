"""
Generate UI Elements for Sands of Duat
Icons, buttons, frames, and interface components with Hades quality
"""

import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image

class UIElementGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = "assets/generated_art"
        
        # UI Elements to generate
        self.ui_elements = [
            # Card frames and borders
            {"name": "card_frame_legendary", "desc": "Golden ornate Egyptian card frame for legendary cards"},
            {"name": "card_frame_epic", "desc": "Silver Egyptian card frame with hieroglyphic borders"},
            {"name": "card_frame_rare", "desc": "Bronze Egyptian card frame with decorative elements"},
            {"name": "card_frame_common", "desc": "Simple stone Egyptian card frame"},
            
            # Game icons
            {"name": "hourglass_icon", "desc": "Egyptian hourglass sand timer icon"},
            {"name": "ankh_health_icon", "desc": "Ankh symbol for health display"},
            {"name": "scarab_energy_icon", "desc": "Sacred scarab beetle energy icon"},
            {"name": "pyramid_victory_icon", "desc": "Pyramid victory achievement icon"},
            
            # Menu buttons
            {"name": "play_button", "desc": "Egyptian style play button with hieroglyphs"},
            {"name": "deck_button", "desc": "Deck builder menu button with scroll design"},
            {"name": "settings_button", "desc": "Settings gear button with Egyptian styling"},
            {"name": "exit_button", "desc": "Exit door button with temple archway design"}
        ]

    def load_model(self):
        """Load the Stable Diffusion model"""
        if self.pipe is None:
            print("Loading Stable Diffusion XL for UI generation...")
            self.pipe = DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True
            )
            
            if self.device == "cuda":
                self.pipe = self.pipe.to("cuda")
                self.pipe.enable_model_cpu_offload()
            
            print("Model loaded!")

    def generate_ui_element(self, ui_data):
        """Generate a UI element"""
        print(f"Generating UI: {ui_data['name']}")
        
        prompt = f"""
        masterpiece, professional game UI element, clean design,
        supergiant games style UI, hades game interface quality,
        {ui_data['desc']}, ancient egyptian design elements,
        ornate details, golden accents, hieroglyphic decorations,
        game interface asset, transparent background suitable,
        high contrast, clear visibility, premium UI design,
        detailed rendering, polished finish
        """
        
        negative_prompt = """
        blurry, low quality, pixelated, amateur design,
        modern elements, realistic photo, cluttered design,
        poor contrast, illegible, messy, distorted,
        text, watermark, signature, background scenery
        """
        
        # Generate square UI elements for versatility
        with torch.no_grad():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.5,
                width=512,
                height=512,
                generator=torch.Generator(device=self.device).manual_seed(hash(ui_data['name']) % 10000)
            ).images[0]
        
        output_path = os.path.join(self.output_dir, f"ui_{ui_data['name']}.png")
        image.save(output_path)
        print(f"Saved: {output_path}")
        return output_path

    def generate_all_ui(self):
        """Generate all UI elements"""
        print("GENERATING SANDS OF DUAT UI ELEMENTS")
        print("=" * 50)
        
        self.load_model()
        
        for i, ui_element in enumerate(self.ui_elements):
            print(f"[{i+1}/{len(self.ui_elements)}] ", end="")
            self.generate_ui_element(ui_element)
        
        print("\nALL UI ELEMENTS GENERATED SUCCESSFULLY!")
        print(f"UI assets location: {self.output_dir}")

def main():
    generator = UIElementGenerator()
    generator.generate_all_ui()

if __name__ == "__main__":
    main()