"""
Generate All Sands of Duat Game Assets
Comprehensive Hades-quality art generation for all game content
"""

import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import time

class SandsOfDuatAssetGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = "assets/generated_art"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Egyptian Cards Data (22 total, Ra already generated)
        self.egyptian_cards = [
            # Legendary Cards (5)
            {"name": "anubis_judgment", "title": "Anubis - Judge of the Dead", "type": "legendary", 
             "desc": "Weighs souls against truth, delivering divine justice"},
            {"name": "osiris_resurrection", "title": "Osiris - Lord of the Underworld", "type": "legendary",
             "desc": "Rules the realm of the dead, master of rebirth"},
            {"name": "horus_divine_sight", "title": "Horus - Sky God", "type": "legendary", 
             "desc": "Falcon deity with all-seeing divine vision"},
            {"name": "isis_protection", "title": "Isis - Mother Goddess", "type": "legendary",
             "desc": "Powerful protective magic and healing wisdom"},
            
            # Epic Cards (7)
            {"name": "thoth_wisdom", "title": "Thoth - God of Wisdom", "type": "epic",
             "desc": "Ibis-headed deity of knowledge and magic"},
            {"name": "bastet_feline_grace", "title": "Bastet - Cat Goddess", "type": "epic",
             "desc": "Feline deity of protection and joy"},
            {"name": "set_chaos_storm", "title": "Set - God of Chaos", "type": "epic",
             "desc": "Desert deity of storms and destruction"},
            {"name": "sekhmet_war_cry", "title": "Sekhmet - Lioness of War", "type": "epic", 
             "desc": "Fierce lioness goddess of battle"},
            {"name": "pharaoh_divine_mandate", "title": "Pharaoh's Divine Mandate", "type": "epic",
             "desc": "Royal authority blessed by the gods"},
            {"name": "pyramid_power", "title": "Pyramid Power", "type": "epic",
             "desc": "Ancient monument channeling divine energy"},
            {"name": "ankh_blessing", "title": "Ankh of Life", "type": "epic",
             "desc": "Sacred symbol granting eternal vitality"},
             
            # Rare Cards (5)
            {"name": "mummy_wrath", "title": "Mummy's Wrath", "type": "rare",
             "desc": "Undead guardian awakened from eternal rest"},
            {"name": "scarab_swarm", "title": "Scarab Swarm", "type": "rare", 
             "desc": "Sacred beetles consuming enemies"},
            {"name": "desert_whisper", "title": "Desert Whisper", "type": "rare",
             "desc": "Ancient secrets carried by desert winds"},
            {"name": "temple_offering", "title": "Temple Offering", "type": "rare",
             "desc": "Ritual sacrifice to appease the gods"},
            {"name": "canopic_jar_ritual", "title": "Canopic Jar Ritual", "type": "rare",
             "desc": "Mummification magic preserving essence"},
             
            # Common Cards (5)
            {"name": "sand_grain", "title": "Grain of Sand", "type": "common",
             "desc": "Simple desert magic, foundation of power"},
            {"name": "papyrus_scroll", "title": "Papyrus Scroll", "type": "common", 
             "desc": "Ancient knowledge recorded on reed paper"},
            {"name": "desert_meditation", "title": "Desert Meditation", "type": "common",
             "desc": "Peaceful contemplation in vast sands"},
            {"name": "sacred_scarab", "title": "Sacred Scarab", "type": "common",
             "desc": "Holy beetle symbol of transformation"},
            {"name": "whisper_of_thoth", "title": "Whisper of Thoth", "type": "common",
             "desc": "Faint divine guidance from wisdom god"}
        ]
        
        # Background scenes needed
        self.backgrounds = [
            {"name": "combat_underworld", "desc": "Egyptian underworld battlefield with hieroglyphic pillars"},
            {"name": "menu_temple", "desc": "Majestic Egyptian temple entrance with golden light"},
            {"name": "deck_builder_sanctum", "desc": "Sacred chamber with scrolls and mystical artifacts"},
            {"name": "victory_sunrise", "desc": "Dawn over Egyptian desert with pyramids"},
            {"name": "defeat_dusk", "desc": "Somber evening in ancient necropolis"}
        ]
        
        # Character portraits needed  
        self.characters = [
            {"name": "player_hero", "desc": "Egyptian hero adventurer with traditional garb"},
            {"name": "anubis_boss", "desc": "Imposing Anubis as major boss enemy"},
            {"name": "mummy_guardian", "desc": "Undead temple guardian wrapped in bandages"},
            {"name": "desert_scorpion", "desc": "Giant magical scorpion creature"},
            {"name": "sand_elemental", "desc": "Swirling sand creature with mystical energy"}
        ]

    def load_model(self):
        """Initialize the Stable Diffusion XL pipeline"""
        if self.pipe is None:
            print("Loading Stable Diffusion XL model...")
            self.pipe = DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True
            )
            
            if self.device == "cuda":
                self.pipe = self.pipe.to("cuda")
                self.pipe.enable_model_cpu_offload()
            
            print("Model loaded successfully!")

    def generate_card_art(self, card_data):
        """Generate artwork for a single card"""
        print(f"Generating: {card_data['title']}")
        
        # Build Hades-quality prompt based on card rarity
        rarity_styles = {
            "legendary": "legendary masterpiece, divine radiant energy, golden aura, supreme artistry",
            "epic": "epic quality, dramatic lighting, rich details, powerful atmosphere", 
            "rare": "high quality, detailed illustration, mystical energy, polished art",
            "common": "professional quality, clean illustration, atmospheric lighting"
        }
        
        prompt = f"""
        masterpiece, highly detailed, professional game art, supergiant games style,
        hand painted illustration, vibrant saturated colors, dramatic lighting contrasts,
        {rarity_styles[card_data['type']]},
        
        {card_data['desc']}, ancient egyptian mythology, hieroglyphic details,
        ornate jewelry, mystical atmosphere, desert temple background,
        rich textures, atmospheric lighting, premium quality,
        fantasy card game art, detailed rendering
        """
        
        negative_prompt = """
        blurry, low quality, pixelated, amateur, cartoon, anime,
        modern clothing, realistic photo, dull colors, dark lighting,
        low resolution, artifacts, distorted, ugly, deformed,
        text, watermark, signature
        """
        
        # Generate with consistent settings
        with torch.no_grad():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=8.0,
                width=768,
                height=1024,
                generator=torch.Generator(device=self.device).manual_seed(hash(card_data['name']) % 10000)
            ).images[0]
        
        # Save the image
        output_path = os.path.join(self.output_dir, f"{card_data['name']}.png")
        image.save(output_path)
        print(f"Saved: {output_path}")
        return output_path

    def generate_background_art(self, bg_data):
        """Generate background artwork"""
        print(f"Generating background: {bg_data['name']}")
        
        prompt = f"""
        masterpiece, highly detailed, professional game background art,
        supergiant games style, hand painted illustration, cinematic composition,
        dramatic lighting, rich atmospheric colors,
        
        {bg_data['desc']}, ancient egypt, detailed architecture,
        mystical atmosphere, golden hour lighting, epic scale,
        premium quality background art, 4k resolution
        """
        
        negative_prompt = """
        blurry, low quality, pixelated, amateur, modern elements,
        characters, figures, text, ui elements, watermark,
        dull colors, poor composition
        """
        
        with torch.no_grad():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
                width=1920,
                height=1080,
                generator=torch.Generator(device=self.device).manual_seed(hash(bg_data['name']) % 10000)
            ).images[0]
        
        output_path = os.path.join(self.output_dir, f"bg_{bg_data['name']}.png")
        image.save(output_path)
        print(f"Saved: {output_path}")
        return output_path

    def generate_character_art(self, char_data):
        """Generate character portrait artwork"""
        print(f"Generating character: {char_data['name']}")
        
        prompt = f"""
        masterpiece, highly detailed, professional character portrait art,
        supergiant games style, hand painted illustration, dramatic lighting,
        vibrant colors, detailed facial features, expressive pose,
        
        {char_data['desc']}, ancient egyptian setting, detailed costume,
        ornate accessories, mystical aura, rich textures,
        character design, premium game art quality
        """
        
        negative_prompt = """
        blurry, low quality, pixelated, amateur, modern clothing,
        realistic photo, dull colors, poor anatomy, deformed,
        background elements, text, watermark
        """
        
        with torch.no_grad():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=28,
                guidance_scale=8.5,
                width=512,
                height=768,
                generator=torch.Generator(device=self.device).manual_seed(hash(char_data['name']) % 10000)
            ).images[0]
        
        output_path = os.path.join(self.output_dir, f"char_{char_data['name']}.png")
        image.save(output_path)
        print(f"Saved: {output_path}")
        return output_path

    def generate_all_assets(self):
        """Generate all game assets systematically"""
        print("SANDS OF DUAT - GENERATING ALL GAME ASSETS")
        print("=" * 60)
        
        if self.device == "cuda":
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
            print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        
        self.load_model()
        
        total_assets = len(self.egyptian_cards) + len(self.backgrounds) + len(self.characters)
        current_asset = 0
        
        # Generate all card artwork
        print(f"\nGenerating {len(self.egyptian_cards)} Egyptian cards...")
        for card in self.egyptian_cards:
            current_asset += 1
            print(f"[{current_asset}/{total_assets}] ", end="")
            self.generate_card_art(card)
            time.sleep(1)  # Brief pause between generations
        
        print(f"\nGenerating {len(self.backgrounds)} background scenes...")
        for bg in self.backgrounds:
            current_asset += 1
            print(f"[{current_asset}/{total_assets}] ", end="")
            self.generate_background_art(bg)
            time.sleep(1)
            
        print(f"\nGenerating {len(self.characters)} character portraits...")
        for char in self.characters:
            current_asset += 1
            print(f"[{current_asset}/{total_assets}] ", end="")
            self.generate_character_art(char)
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print("ALL SANDS OF DUAT ASSETS GENERATED SUCCESSFULLY!")
        print(f"Total assets created: {total_assets}")
        print(f"Assets location: {self.output_dir}")

def main():
    generator = SandsOfDuatAssetGenerator()
    generator.generate_all_assets()

if __name__ == "__main__":
    main()